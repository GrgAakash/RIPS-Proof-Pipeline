"""The single entry point for model calls (§11.2 / §11.3, OpenAI adapter).

Path A (default): native Structured Outputs -- response_format receives the
pydantic model, the API guarantees a valid output at the decoding layer, and
.parse() hands back the object directly.
Path B (structured_outputs=false fallback): plain create + extract_json +
pydantic validation; on failure, the error is appended back into messages and
retried up to validation_retries times.
"""
from __future__ import annotations

import asyncio
import json
import os
import random
import time
from typing import Any, Optional, Type

from pydantic import BaseModel

from .common import (RunContext, TaskFailed, atomic_write_text,
                     canonical_json, sha256_text)
from .schemas import TASK_SCHEMAS

_client = None
_client_provider = None


def get_client(provider: str):
    """Construct and cache an AsyncOpenAI / AsyncAzureOpenAI per provider."""
    global _client, _client_provider
    if _client is not None and _client_provider == provider:
        return _client
    if provider == "openai":
        from openai import AsyncOpenAI
        _client = AsyncOpenAI(timeout=600.0)                 # reads OPENAI_API_KEY
    elif provider == "azure":
        from openai import AsyncAzureOpenAI
        api_version = os.environ.get("OPENAI_API_VERSION")
        if not api_version:                # json_schema needs 2024-08-01-preview+
            raise ValueError("provider=azure requires the OPENAI_API_VERSION "
                             "env var (e.g. 2024-08-01-preview)")
        _client = AsyncAzureOpenAI(                       # reads AZURE_OPENAI_ENDPOINT / _API_KEY
            api_version=api_version, timeout=600.0)
    else:
        raise ValueError(f"unknown provider: {provider}")
    _client_provider = provider
    return _client


def is_reasoning(model: str) -> bool:
    """The o series (o1/o3/o4-mini...) and gpt-5 series are the reasoning tier
    (both take reasoning_effort and reject a custom temperature)."""
    return model.startswith(("o", "gpt-5"))


def split_system_user(text: str) -> tuple[str, str]:
    """The prompt file has SYSTEM/USER sections separated by line-leading keywords."""
    lines = text.split("\n")
    mode, sys_lines, usr_lines = None, [], []
    for ln in lines:
        if ln.strip() == "SYSTEM":
            mode = "s"
            continue
        if ln.strip() == "USER":
            mode = "u"
            continue
        (sys_lines if mode == "s" else usr_lines).append(ln)
    return "\n".join(sys_lines).strip(), "\n".join(usr_lines).strip()


def fill(tmpl: str, vars: dict[str, Any]) -> str:
    """Bind <<k>> placeholders via str.replace (plan §11.2)."""
    out = tmpl
    for k, v in vars.items():
        out = out.replace(f"<<{k}>>", str(v))
    return out


def extract_json(text: str) -> str:
    """Brace-balancing scan for the first top-level JSON object, skipping
    braces inside strings (used by path B)."""
    start = text.find("{")
    if start < 0:
        raise ValueError("no JSON object found in response")
    depth, in_str, esc = 0, False, False
    for i in range(start, len(text)):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]
    raise ValueError("unbalanced JSON braces in response")


async def _with_network_retry(ctx: RunContext, coro_factory):
    """Hand-rolled tenacity-style retry: exponential backoff on 429/5xx/
    connection errors, honoring the server's retry-after when present."""
    from openai import (APIConnectionError, APIStatusError, APITimeoutError,
                        RateLimitError)
    retries = ctx.cfg.llm.network_retries
    last_exc: Optional[Exception] = None
    for attempt in range(retries + 1):
        try:
            return await coro_factory()
        except (RateLimitError, APIConnectionError, APITimeoutError) as e:
            last_exc = e
            wait = _retry_after_seconds(e) or min(60.0, (2 ** attempt) + random.random())
        except APIStatusError as e:
            if e.status_code < 500:
                raise                      # 4xx (except 429) is not retried
            last_exc = e
            wait = _retry_after_seconds(e) or min(60.0, (2 ** attempt) + random.random())
        if attempt < retries:
            await asyncio.sleep(wait)
    raise last_exc  # type: ignore[misc]


def _retry_after_seconds(exc) -> Optional[float]:
    try:
        ra = exc.response.headers.get("retry-after")
        return float(ra) if ra else None
    except Exception:
        return None


def _parse_endpoint(client):
    """openai>=1.92 uses chat.completions.parse; older versions fall under beta."""
    if hasattr(client.chat.completions, "parse"):
        return client.chat.completions.parse
    return client.beta.chat.completions.parse


def _build_messages(model: str, sys: str, usr: str) -> list[dict]:
    # o series: system content goes into the developer role;
    # gpt series: plain system (§11.2 key point 3)
    role = "developer" if is_reasoning(model) else "system"
    return [{"role": role, "content": sys}, {"role": "user", "content": usr}]


def _param_extra(ctx: RunContext, model: str) -> dict:
    # Parameter tiering: the o series takes reasoning_effort, the gpt series
    # takes temperature (§11.2 key point 2)
    if is_reasoning(model):
        return {"reasoning_effort": ctx.cfg.llm.reasoning.reasoning_effort}
    return {"temperature": ctx.cfg.llm.standard.temperature}


def cache_key(model: str, tmpl: str, vars: dict[str, Any], schema_name: str,
              extra: Optional[dict] = None) -> str:
    """Cache key = model + prompt template + variable bindings + schema name
    (§11.2), plus — since the reproducibility fix — the sampling params
    (temperature / reasoning_effort). extra=None yields the legacy pre-fix key."""
    parts = model + sha256_text(tmpl) + canonical_json(
        {k: str(v) for k, v in vars.items()}) + schema_name
    if extra is not None:
        parts += canonical_json({k: str(v) for k, v in extra.items()})
    return sha256_text(parts)


# Sampling params in effect when the pre-fix caches (runs/, tests/_runs/) were
# recorded. A legacy cache file may only be trusted when the current params
# equal these — otherwise a param change would silently read stale results.
_LEGACY_PARAMS = ({"temperature": 0.0}, {"reasoning_effort": "medium"})


async def call_llm(ctx: RunContext, task: str, vars: dict[str, Any],
                   schema: Optional[Type[BaseModel]] = None,
                   model: Optional[str] = None,
                   use_cache: bool = True) -> BaseModel:
    """Unified call entry point. Returns a pydantic instance of schema; raises TaskFailed on failure."""
    schema = schema or TASK_SCHEMAS[task]
    model = model or ctx.cfg.models.for_task(task)
    tmpl = ctx.prompt_text(task)
    sys, usr = split_system_user(fill(tmpl, vars))
    extra = _param_extra(ctx, model)

    key = cache_key(model, tmpl, vars, schema.__name__, extra)
    cache_file = ctx.path(f"cache/{task}-{key[:32]}.json")
    if use_cache and ctx.cfg.llm.cache:
        hit = cache_file if cache_file.exists() else None
        if hit is None and any(extra == lp for lp in _LEGACY_PARAMS):
            legacy_key = cache_key(model, tmpl, vars, schema.__name__)
            legacy = ctx.path(f"cache/{task}-{legacy_key[:32]}.json")
            if legacy.exists():
                hit = legacy
        if hit is not None:
            obj = schema.model_validate_json(hit.read_text(encoding="utf-8"))
            if hit is not cache_file:              # migrate legacy entry to the param-aware key
                atomic_write_text(cache_file, obj.model_dump_json())
            ctx.log_event(task=task, model=model, cache_key=key[:32], ok=True,
                          cache_hit=True, in_tok=0, out_tok=0,
                          reasoning_tok=0, ms=0)
            return obj

    if os.environ.get("PAPER_CLEANER_OFFLINE"):
        raise TaskFailed(task, "PAPER_CLEANER_OFFLINE is set and the call "
                               "missed the cache — refusing a live API call")

    client = get_client(ctx.cfg.provider)
    msgs = _build_messages(model, sys, usr)
    max_tok = ctx.cfg.llm.max_output_tokens.get(task, 4000)
    t0 = time.monotonic()

    if ctx.cfg.llm.structured_outputs:
        obj = await _call_structured(ctx, task, client, model, msgs, schema,
                                     max_tok, extra, key)
    else:
        obj = await _call_fallback(ctx, task, client, model, msgs, schema,
                                   max_tok, extra, key)

    if use_cache and ctx.cfg.llm.cache:
        atomic_write_text(cache_file, obj.model_dump_json())
    usage = getattr(obj, "_usage_log", {})
    ctx.log_event(task=task, model=model, cache_key=key[:32], ok=True,
                  cache_hit=False, ms=int((time.monotonic() - t0) * 1000),
                  **usage)
    # live calls are the slow ones — one progress line each (cache hits silent)
    ctx.progress(f"{task} {model} {time.monotonic() - t0:.1f}s "
                 f"in={usage.get('in_tok', 0)} out={usage.get('out_tok', 0)}")
    return obj


async def _call_structured(ctx, task, client, model, msgs, schema, max_tok,
                           extra, key):
    """Path A: response_format=schema for hard-constrained decoding.

    On length truncation (the o series burns output budget on reasoning
    tokens) the next attempt doubles the token budget, capped at 4x.
    """
    parse = _parse_endpoint(client)
    last_detail = ""
    budget = max_tok
    for attempt in range(ctx.cfg.llm.validation_retries + 1):
        try:
            rsp = await _with_network_retry(ctx, lambda: parse(
                model=model, messages=msgs, response_format=schema,
                max_completion_tokens=budget, **extra))
        except Exception as e:
            if "LengthFinishReason" in type(e).__name__ and budget < max_tok * 4:
                last_detail = f"length-truncated at {budget} tokens"
                ctx.log_event(task=task, model=model, cache_key=key[:32],
                              ok=False, detail=last_detail)
                budget = min(budget * 2, max_tok * 4)
                continue
            raise
        msg = rsp.choices[0].message
        if getattr(msg, "refusal", None):                     # safety refusal, extremely rare
            last_detail = f"refusal: {msg.refusal}"
            ctx.log_event(task=task, model=model, cache_key=key[:32], ok=False,
                          refusal=str(msg.refusal)[:300])
            continue
        obj = msg.parsed                                      # already a pydantic instance
        if obj is None:                                       # length truncation, etc.
            last_detail = f"no parsed object (finish={rsp.choices[0].finish_reason})"
            ctx.log_event(task=task, model=model, cache_key=key[:32], ok=False,
                          detail=last_detail)
            if rsp.choices[0].finish_reason == "length":
                budget = min(budget * 2, max_tok * 4)
            continue
        object.__setattr__(obj, "_usage_log", _usage(rsp))
        return obj
    raise TaskFailed(task, last_detail)


async def _call_fallback(ctx, task, client, model, msgs, schema, max_tok,
                         extra, key):
    """Path B: plain create + extract_json + pydantic validation, with errors fed back for retry."""
    work = list(msgs)
    last_detail = ""
    for attempt in range(ctx.cfg.llm.validation_retries + 1):
        rsp = await _with_network_retry(ctx, lambda: client.chat.completions.create(
            model=model, messages=work, max_completion_tokens=max_tok, **extra))
        content = rsp.choices[0].message.content or ""
        try:
            obj = schema.model_validate_json(extract_json(content))
            object.__setattr__(obj, "_usage_log", _usage(rsp))
            return obj
        except Exception as e:
            last_detail = str(e)[:500]
            ctx.log_event(task=task, model=model, cache_key=key[:32], ok=False,
                          detail=last_detail)
            work = work + [
                {"role": "assistant", "content": content[:8000]},
                {"role": "user", "content":
                 f"Your previous output failed schema validation:\n{last_detail}\n"
                 f"Output ONLY the corrected single JSON object."}]
    raise TaskFailed(task, last_detail)


def _usage(rsp) -> dict:
    u = getattr(rsp, "usage", None)
    if u is None:
        return {"in_tok": 0, "out_tok": 0, "reasoning_tok": 0}
    det = getattr(u, "completion_tokens_details", None)
    return {"in_tok": getattr(u, "prompt_tokens", 0) or 0,
            "out_tok": getattr(u, "completion_tokens", 0) or 0,
            "reasoning_tok": getattr(det, "reasoning_tokens", 0) or 0 if det else 0}


def run_async(coro):
    """Unified wrapper for step modules' synchronous entry point to run asyncio."""
    return asyncio.run(coro)
