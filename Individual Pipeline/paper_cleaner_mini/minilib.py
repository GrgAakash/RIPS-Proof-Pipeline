"""Self-contained support library for the mini pipeline.

Ports (unchanged in behavior) of the pieces of the main paper_cleaner
repo that stage2.py / audit.py need: config + run context, the LLM call
layer (cache, retries, structured outputs), the data schemas, and the
deterministic LaTeX checks (std-command whitelist, macro residue,
verbatim-proof leak scan). One file so the mini folder stays mini.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import random
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, Optional, Type

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

REPO_ROOT = Path(__file__).resolve().parent
PROGRESS_ON = os.environ.get("PAPER_CLEANER_PROGRESS", "1") != "0"


# ------------------------------------------------------------- exceptions

class TaskFailed(Exception):
    """A single LLM task still fails after exhausting retries."""

    def __init__(self, task: str, detail: str = ""):
        super().__init__(f"llm task {task} failed: {detail}")
        self.task = task
        self.detail = detail


class ConfigError(Exception):
    pass


# ----------------------------------------------------------------- config

class StandardCfg(BaseModel):
    temperature: float = 0


class ReasoningCfg(BaseModel):
    reasoning_effort: str = "high"


class LlmCfg(BaseModel):
    standard: StandardCfg = Field(default_factory=StandardCfg)
    reasoning: ReasoningCfg = Field(default_factory=ReasoningCfg)
    max_output_tokens: dict[str, int] = Field(default_factory=dict)
    structured_outputs: bool = True
    validation_retries: int = 2
    network_retries: int = 8
    parallel: int = 2
    cache: bool = True


class Config(BaseModel):
    provider: str = "openai"                     # openai | azure
    llm: LlmCfg = Field(default_factory=LlmCfg)


def load_config(path: str | Path) -> Config:
    try:
        raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        return Config.model_validate(raw)
    except (OSError, yaml.YAMLError, ValidationError) as e:
        raise ConfigError(str(e)) from e


# -------------------------------------------------------------- utilities

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def atomic_write_text(p: Path, text: str) -> None:
    tmp = p.with_name(f"{p.name}.{os.getpid()}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, p)


# ------------------------------------------------------------ run context

class RunContext:
    """Per-paper directories, config, cache and logging."""

    def __init__(self, paper_id: str, cfg: Config,
                 runs_dir: str | Path = "runs"):
        self.paper_id = paper_id
        self.cfg = cfg
        self.run_dir = Path(runs_dir) / paper_id
        self.prompts_dir = REPO_ROOT / "prompts"
        self.data_dir = REPO_ROOT / "data"
        for sub in ("source", "index", "roles", "packages", "cache", "logs"):
            (self.run_dir / sub).mkdir(parents=True, exist_ok=True)
        self.step_name = ""

    def path(self, rel: str) -> Path:
        return self.run_dir / rel

    def read_json(self, rel: str) -> Any:
        return json.loads(self.path(rel).read_text(encoding="utf-8"))

    def write_json(self, rel: str, obj: Any) -> None:
        p = self.path(rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(obj, BaseModel):
            text = obj.model_dump_json(indent=2, by_alias=True)
        else:
            text = json.dumps(obj, indent=2, ensure_ascii=False,
                              default=_dump)
        atomic_write_text(p, text)

    def read_model(self, rel: str, model_cls):
        return model_cls.model_validate_json(
            self.path(rel).read_text(encoding="utf-8"))

    def prompt_text(self, task: str) -> str:
        return (self.prompts_dir / f"{task}.txt").read_text(encoding="utf-8")

    def progress(self, msg: str) -> None:
        if PROGRESS_ON:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[{ts}] {self.paper_id} {self.step_name or '-':<5} | "
                  f"{msg}", file=sys.stderr, flush=True)

    def log_event(self, **kw) -> None:
        kw.setdefault("ts", now_iso())
        kw.setdefault("paper", self.paper_id)
        kw.setdefault("step", self.step_name)
        with open(self.path("logs/run.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(kw, ensure_ascii=False, default=str) + "\n")


def _dump(o):
    if isinstance(o, BaseModel):
        return o.model_dump(by_alias=True)
    raise TypeError(f"not JSON serializable: {type(o)}")


# ---------------------------------------------------------- data schemas
# Field-compatible with the main repo's schemas.py (unknown JSON keys are
# ignored on read; everything the mini writes matches the main layout).

class Meta(BaseModel):
    paper_id: str
    title: str = ""
    paper_date: str = ""
    field_baseline: str = ""
    source_type: Literal["latex", "ocr"] = "latex"


class GlobalItem(BaseModel):
    id: str
    kind: str = "notation"
    scope: str = "paper"
    text_tex: str


class Statement(BaseModel):
    id: str
    env_type: str
    latex_label: str = ""
    display_name: str = ""
    section: str = ""
    order_index: int = 0
    statement_tex: str
    statement_sha256: str = ""
    source_file: str = ""
    source_start: int = -1
    source_end: int = -1
    source_sha256: str = ""
    source_verified: bool = False
    proof_tex: Optional[str] = None
    proof_location: str = "omitted"
    proof_sha256: str = ""
    proof_source_file: str = ""
    proof_source_start: int = -1
    proof_source_end: int = -1
    proof_source_sha256: str = ""
    proof_source_verified: bool = False
    proof_pairing: str = ""
    added_by: str = "parser"


class Citation(BaseModel):
    key: str
    raw_bib: str


class StatementsIndex(BaseModel):
    schema_version: Literal[2]
    paper_id: str
    macros_tex: str = ""
    global_context: list[GlobalItem] = Field(default_factory=list)
    statements: list[Statement] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)

    def by_id(self) -> dict[str, Statement]:
        return {s.id: s for s in self.statements}

    def gc_by_id(self) -> dict[str, GlobalItem]:
        return {g.id: g for g in self.global_context}


class ExternalDep(BaseModel):
    used_by: str
    citation_key: str = ""
    usage_quote: str = ""
    stated_in_paper: bool = False
    statement_tex: str = ""
    statement_origin: str = ""


class DepGraph(BaseModel):
    external_deps: list[ExternalDep] = Field(default_factory=list)


class Selection(BaseModel):
    mains: list[str] = Field(default_factory=list)
    hardest: list[str] = Field(default_factory=list)


class PkgEntry(BaseModel):
    target_id: str
    env_type: str
    role: str = "unknown"
    selected_as: str = "main"
    policy: str
    path: str
    topo_rank: int = 0
    proof_chars: int = 0
    self_contained: bool = True
    leak_clean: bool = True


class Manifest(BaseModel):
    paper_id: str
    paper_date: str = ""
    pipeline_version: str = "stage2-min-source-v2"
    packages: list[PkgEntry] = Field(default_factory=list)
    stats: dict[str, int] = Field(default_factory=dict)


# LLM output models: extra="forbid" + all fields required (OpenAI strict).

class _LLM(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AuditIssue(_LLM):
    kind: Literal["undefined-symbol", "undefined-term", "missing-result",
                  "leak", "other"]
    quote: str
    explanation: str
    severity: Literal["fatal", "minor"]


class AuditPkgOut(_LLM):
    issues: list[AuditIssue]
    self_contained: bool
    leak_free: bool
    sufficient: bool
    confidence: Literal["high", "medium", "low"]
    summary: str


class AuditExclOut(_LLM):
    exclusion_justified: bool
    paper_resolves_it: bool
    where_in_paper: str
    verdict: str
    confidence: Literal["high", "medium", "low"]


# ---------------------------------------------------------- LLM call layer

_client = None
_client_provider = None


def get_client(provider: str):
    global _client, _client_provider
    if _client is not None and _client_provider == provider:
        return _client
    if provider == "openai":
        from openai import AsyncOpenAI
        _client = AsyncOpenAI(timeout=600.0)          # reads OPENAI_API_KEY
    elif provider == "azure":
        from openai import AsyncAzureOpenAI
        api_version = os.environ.get("OPENAI_API_VERSION")
        if not api_version:
            raise ValueError("provider=azure requires OPENAI_API_VERSION")
        _client = AsyncAzureOpenAI(api_version=api_version, timeout=600.0)
    else:
        raise ValueError(f"unknown provider: {provider}")
    _client_provider = provider
    return _client


def is_reasoning(model: str) -> bool:
    """o-series and gpt-5-series take reasoning_effort, not temperature."""
    return model.startswith(("o", "gpt-5"))


def split_system_user(text: str) -> tuple[str, str]:
    mode, sys_lines, usr_lines = None, [], []
    for ln in text.split("\n"):
        if ln.strip() == "SYSTEM":
            mode = "s"
            continue
        if ln.strip() == "USER":
            mode = "u"
            continue
        (sys_lines if mode == "s" else usr_lines).append(ln)
    return "\n".join(sys_lines).strip(), "\n".join(usr_lines).strip()


def fill(tmpl: str, vars: dict[str, Any]) -> str:
    out = tmpl
    for k, v in vars.items():
        out = out.replace(f"<<{k}>>", str(v))
    return out


def extract_json(text: str) -> str:
    """Brace-balancing scan for the first top-level JSON object."""
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
    from openai import (APIConnectionError, APIStatusError, APITimeoutError,
                        RateLimitError)
    retries = ctx.cfg.llm.network_retries
    last_exc: Optional[Exception] = None
    for attempt in range(retries + 1):
        try:
            return await coro_factory()
        except (RateLimitError, APIConnectionError, APITimeoutError) as e:
            last_exc = e
            wait = (_retry_after_seconds(e)
                    or min(60.0, (2 ** attempt) + random.random()))
        except APIStatusError as e:
            if e.status_code < 500:
                raise
            last_exc = e
            wait = (_retry_after_seconds(e)
                    or min(60.0, (2 ** attempt) + random.random()))
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
    if hasattr(client.chat.completions, "parse"):
        return client.chat.completions.parse
    return client.beta.chat.completions.parse


def _build_messages(model: str, sys_txt: str, usr: str) -> list[dict]:
    role = "developer" if is_reasoning(model) else "system"
    return [{"role": role, "content": sys_txt}, {"role": "user", "content": usr}]


def _param_extra(ctx: RunContext, model: str) -> dict:
    if is_reasoning(model):
        return {"reasoning_effort": ctx.cfg.llm.reasoning.reasoning_effort}
    return {"temperature": ctx.cfg.llm.standard.temperature}


def cache_key(model: str, tmpl: str, vars: dict[str, Any], schema_name: str,
              extra: dict) -> str:
    parts = (model + sha256_text(tmpl)
             + canonical_json({k: str(v) for k, v in vars.items()})
             + schema_name
             + canonical_json({k: str(v) for k, v in extra.items()}))
    return sha256_text(parts)


async def call_llm(ctx: RunContext, task: str, vars: dict[str, Any],
                   schema: Type[BaseModel], model: str,
                   use_cache: bool = True) -> BaseModel:
    """Unified call entry. Returns a validated schema instance; raises
    TaskFailed after exhausting retries. Results cache under cache/."""
    tmpl = ctx.prompt_text(task)
    sys_txt, usr = split_system_user(fill(tmpl, vars))
    extra = _param_extra(ctx, model)

    key = cache_key(model, tmpl, vars, schema.__name__, extra)
    cache_file = ctx.path(f"cache/{task}-{key[:32]}.json")
    if use_cache and ctx.cfg.llm.cache and cache_file.exists():
        obj = schema.model_validate_json(
            cache_file.read_text(encoding="utf-8"))
        ctx.log_event(task=task, model=model, cache_key=key[:32], ok=True,
                      cache_hit=True, in_tok=0, out_tok=0,
                      reasoning_tok=0, ms=0)
        return obj

    if os.environ.get("PAPER_CLEANER_OFFLINE"):
        raise TaskFailed(task, "PAPER_CLEANER_OFFLINE is set and the call "
                               "missed the cache — refusing a live API call")

    client = get_client(ctx.cfg.provider)
    msgs = _build_messages(model, sys_txt, usr)
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
    ctx.progress(f"{task} {model} {time.monotonic() - t0:.1f}s "
                 f"in={usage.get('in_tok', 0)} out={usage.get('out_tok', 0)}")
    return obj


async def _call_structured(ctx, task, client, model, msgs, schema, max_tok,
                           extra, key):
    """response_format=schema; token budget doubles (max 4x) on truncation
    because reasoning tokens count against max_completion_tokens."""
    parse = _parse_endpoint(client)
    last_detail = ""
    budget = max_tok
    for attempt in range(ctx.cfg.llm.validation_retries + 1):
        try:
            rsp = await _with_network_retry(ctx, lambda: parse(
                model=model, messages=msgs, response_format=schema,
                max_completion_tokens=budget, **extra))
        except Exception as e:
            if ("LengthFinishReason" in type(e).__name__
                    and budget < max_tok * 4):
                last_detail = f"length-truncated at {budget} tokens"
                ctx.log_event(task=task, model=model, cache_key=key[:32],
                              ok=False, detail=last_detail)
                budget = min(budget * 2, max_tok * 4)
                continue
            raise
        msg = rsp.choices[0].message
        if getattr(msg, "refusal", None):
            last_detail = f"refusal: {msg.refusal}"
            ctx.log_event(task=task, model=model, cache_key=key[:32],
                          ok=False, refusal=str(msg.refusal)[:300])
            continue
        obj = msg.parsed
        if obj is None:
            last_detail = (f"no parsed object "
                           f"(finish={rsp.choices[0].finish_reason})")
            ctx.log_event(task=task, model=model, cache_key=key[:32],
                          ok=False, detail=last_detail)
            if rsp.choices[0].finish_reason == "length":
                budget = min(budget * 2, max_tok * 4)
            continue
        object.__setattr__(obj, "_usage_log", _usage(rsp))
        return obj
    raise TaskFailed(task, last_detail)


async def _call_fallback(ctx, task, client, model, msgs, schema, max_tok,
                         extra, key):
    """Plain create + extract_json + validation, errors fed back."""
    work = list(msgs)
    last_detail = ""
    for attempt in range(ctx.cfg.llm.validation_retries + 1):
        rsp = await _with_network_retry(
            ctx, lambda: client.chat.completions.create(
                model=model, messages=work, max_completion_tokens=max_tok,
                **extra))
        content = rsp.choices[0].message.content or ""
        try:
            obj = schema.model_validate_json(extract_json(content))
            object.__setattr__(obj, "_usage_log", _usage(rsp))
            return obj
        except Exception as e:
            last_detail = str(e)[:500]
            ctx.log_event(task=task, model=model, cache_key=key[:32],
                          ok=False, detail=last_detail)
            work = work + [
                {"role": "assistant", "content": content[:8000]},
                {"role": "user", "content":
                 f"Your previous output failed schema validation:\n"
                 f"{last_detail}\nOutput ONLY the corrected single JSON "
                 f"object."}]
    raise TaskFailed(task, last_detail)


def _usage(rsp) -> dict:
    u = getattr(rsp, "usage", None)
    if u is None:
        return {"in_tok": 0, "out_tok": 0, "reasoning_tok": 0}
    det = getattr(u, "completion_tokens_details", None)
    return {"in_tok": getattr(u, "prompt_tokens", 0) or 0,
            "out_tok": getattr(u, "completion_tokens", 0) or 0,
            "reasoning_tok":
                (getattr(det, "reasoning_tokens", 0) or 0) if det else 0}


def run_async(coro):
    return asyncio.run(coro)


# Strongest-first; "auto" picks the first the account serves. Keep this a
# DIFFERENT tier from any cheap in-loop models if you add them.
MODEL_PREFERENCE = ("gpt-5.5", "gpt-5.4", "gpt-5.2", "gpt-5.1", "gpt-5",
                    "o3")


async def pick_model(provider: str, requested: str) -> str:
    if requested and requested != "auto":
        return requested
    client = get_client(provider)
    page = await client.models.list()
    have = {m.id for m in page.data}
    for m in MODEL_PREFERENCE:
        if m in have:
            return m
    cand = sorted((m for m in have if m.startswith(("gpt-5", "o3"))),
                  reverse=True)
    if cand:
        return cand[0]
    raise SystemExit(f"no strong model available; account serves: "
                     f"{sorted(have)[:20]} ...")


# ------------------------------------------------- deterministic checks
# Ports of gates.py / step7_verify.py pieces (same behavior).

CMD_RE = re.compile(r"\\([A-Za-z@]+)")
DEFINED_RE = re.compile(
    r"\\(?:newcommand|renewcommand|providecommand|def|DeclareMathOperator"
    r"|NewDocumentCommand|RenewDocumentCommand|ProvideDocumentCommand"
    r"|DeclarePairedDelimiterX?|DeclareMathAlphabet|mathchardef|let)\*?"
    r"\s*\{?\\([A-Za-z@]+)\}?")
SEC3_RE = re.compile(r"## 3\. Known external results.*?(?=\n## \d)",
                     re.DOTALL)
_WS_RE = re.compile(r"\s+")


def load_std_commands(ctx: RunContext) -> set[str]:
    p = ctx.data_dir / "latex_std_commands.txt"
    return {ln.strip() for ln in p.read_text(encoding="utf-8").splitlines()
            if ln.strip()}


def _norm_ws(s: str) -> str:
    s = (s.replace("’", "'").replace("‘", "'")
          .replace("“", '"').replace("”", '"'))
    return _WS_RE.sub(" ", s).strip()


def g3_macro_residue(ctx: RunContext, problem_md: str, macros_tex: str,
                     flat_source: str) -> tuple[list[str], str]:
    """Each \\cmd in problem_md must be std, single-letter, or defined in
    macros_tex; otherwise try to recover its definition from the source."""
    std = load_std_commands(ctx)
    defined = set(DEFINED_RE.findall(macros_tex)) | set(DEFINED_RE.findall(problem_md))
    unknown, appended = [], []
    for cmd in sorted(set(CMD_RE.findall(problem_md))):
        if cmd in std or cmd in defined or len(cmd) == 1:
            continue
        mo = re.search(
            r"\\(?:newcommand|renewcommand|providecommand|def|"
            r"DeclareMathOperator)\*?\s*\{?\\" + re.escape(cmd)
            + r"(?![A-Za-z@]).*", flat_source)
        if mo:
            appended.append(mo.group(0))
            defined.add(cmd)
        else:
            unknown.append(cmd)
    return unknown, "\n".join(appended)


def g5_leak_scan(problem_md: str, proof_tex: str,
                 allowed_texts: list[str] | tuple = (),
                 min_len: int = 120, stride: int = 20,
                 max_span: int = 1200) -> list[str]:
    """Slide windows of the normalized proof over the normalized file; a
    match extends to its maximal span. Spans fully inside an allowed text
    (target statement, granted block source, macros) are legitimate."""
    hay = _norm_ws(problem_md)
    needle = _norm_ws(proof_tex)
    if len(needle) < min_len:
        return []
    allowed = [_norm_ws(a) for a in allowed_texts if a and a.strip()]
    spans: list[str] = []
    i, n = 0, len(needle)
    while i + min_len <= n:
        window = needle[i:i + min_len]
        if window in hay:
            j = i + min_len
            while j < min(n, i + max_span) and needle[i:j + 1] in hay:
                j += 1
            frag = needle[i:j]
            probe = frag.strip()
            if probe and not any(probe in a for a in allowed):
                spans.append(frag)
            i = j
        else:
            i += stride
    return spans


def g5_leak_spans_dedup(new: list[str], seen: list[str]) -> list[str]:
    return [s for s in new if not any(s in t or t in s for t in seen)]


def _authoritative_text(index: StatementsIndex, bid: str) -> str | None:
    s = index.by_id().get(bid)
    if s is not None:
        return s.statement_tex
    g = index.gc_by_id().get(bid)
    if g is not None:
        return g.text_tex
    return None


def ship_leak_spans(index: StatementsIndex, graph: DepGraph,
                    target: Statement, problem_md: str,
                    assembly: dict) -> list[str]:
    """Deterministic pre-ship leak scan; Section 3 additionally scanned at
    a 50-char floor (the usage-quote leak class). Usage-quote grants never
    whitelist anything."""
    stmt_grade = [x.statement_tex for x in graph.external_deps
                  if x.statement_origin != "usage-quote"]
    allowed = [target.statement_tex, index.macros_tex] + stmt_grade
    allowed += [_authoritative_text(index, bid) or "" for bid in
                (assembly.get("defs", []) + assembly.get("res", [])
                 + assembly.get("gcs", []))]
    spans = g5_leak_scan(problem_md, target.proof_tex or "", allowed)
    m = SEC3_RE.search(problem_md)
    if m:
        spans += g5_leak_spans_dedup(
            g5_leak_scan(m.group(0), target.proof_tex or "", stmt_grade,
                         min_len=50, stride=10), spans)
    return spans
