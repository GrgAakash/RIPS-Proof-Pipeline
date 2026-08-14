"""LLM client abstraction plus mock and OpenAI-compatible implementations.

This module is the only place where the pipeline talks to a language model. It
exposes three things to the rest of the controller (see
``docs/PROJECT_OVERVIEW.md``):

* ``LLMClient`` -- a deliberately narrow protocol so the orchestrator, bundle
  builder, and tests never depend on a concrete provider or on network access.
* ``MockLLMClient`` -- a deterministic, offline client. It emits fixed marker
  strings (``MOCK_PROOF_OK``, ``MOCK_PROOF_MAJOR_GAP``, ...) that downstream
  roles and the test suite key on to drive specific Solver -> Verifier ->
  Final Checker scenarios without a real model.
* ``OpenAICompatibleClient`` -- a stdlib-only (``urllib``) client for real
  OpenAI-compatible providers. It supports chat-completions and, for GPT-5.5
  reasoning models, the Responses API.

Privacy note: some prompts carry privileged gold proofs / source context (only
the Final Checker role receives those). The OpenAI-compatible client is written
to avoid persisting provider error bodies, which can echo prompt text. See
``OpenAICompatibleClient.complete``.
"""

from __future__ import annotations

import json
import os
import random
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from solver.config import optional_float_env, optional_int_env, optional_set_env
from solver.packet import PromptPacket


WEB_SEARCH_FORBIDDEN_ROLES = frozenset(
    {
        "problem_statement_verifier",
        "verifier_a",
        "composer_a",
        "verifier_b",
        "verifier_c",
        "final_checker",
        "reformatter",
    }
)


@dataclass(frozen=True)
class LLMResponse:
    """Normalized completion payload returned by every client implementation."""

    text: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cost_usd: float | None = None
    raw: dict | None = None


class LLMClient(Protocol):
    """Small protocol used by the orchestrator, tests, and mock client."""

    model: str

    def complete(self, prompt: PromptPacket, metadata: dict) -> LLMResponse:
        """Return a completion for one role prompt."""


@dataclass
class MockLLMClient:
    """Deterministic local client used for tests and smoke runs."""

    model: str = "mock-mvp-model"
    calls: list[dict] = field(default_factory=list)

    def complete(self, prompt: PromptPacket, metadata: dict) -> LLMResponse:
        self.calls.append({"role": prompt.role, **metadata})
        role = prompt.role
        if role == "solver":
            return LLMResponse(text=self._solve(metadata), model=self.model)
        if role == "verifier":
            return LLMResponse(text=self._verify(prompt.user, metadata), model=self.model)
        if role == "final_checker":
            return LLMResponse(text=self._check(prompt.user), model=self.model)
        if role == "paper_scout":
            return LLMResponse(text="[]", model=self.model)
        if role == "paper_cleaner":
            return LLMResponse(
                text="Mock Paper Cleaner does not generate benchmark artifacts. Use a real API client for this role.",
                model=self.model,
            )
        if role in {"bundle_builder", "bundle_repair"}:
            paper_id = str(metadata.get("paper_id", "paper_toy"))
            return LLMResponse(text=_mock_bundle(paper_id), model=self.model)
        if role == "hint_maker":
            task_id = str(metadata.get("task_id", "R000"))
            return LLMResponse(text=_mock_hints(task_id), model=self.model)
        if role == "hint_repair":
            task_id = str(metadata.get("task_id", "R000"))
            return LLMResponse(text=_mock_hints(task_id), model=self.model)
        return LLMResponse(text="", model=self.model)

    def _solve(self, metadata: dict) -> str:
        scenario = str(metadata.get("scenario", "pass_h0"))
        hint_level = int(metadata.get("hint_level", 0))
        submission = int(metadata.get("submission", 1))
        task_id = str(metadata.get("task_id", "R000"))
        if scenario == "unsolved":
            return f"{task_id}: MOCK_PROOF_MAJOR_GAP. The decisive implication is asserted without proof."
        if scenario == "revision_pass" and submission == 1:
            return f"{task_id}: MOCK_PROOF_MAJOR_GAP. This first version intentionally omits the core step."
        if scenario == "checker_reject_then_hint" and hint_level == 0:
            return f"{task_id}: MOCK_PROOF_CHECKER_REJECT. The verifier thinks this is close, but the gold check should reject it."
        return f"{task_id}: MOCK_PROOF_OK. A complete proof using only the public prefix and released hints."

    def _verify(self, user_prompt: str, metadata: dict) -> str:
        proof = _section(user_prompt, "CANDIDATE PROOF")
        stage = str(metadata.get("verifier_stage", "skeleton"))
        if "MOCK_PROOF_OK" in proof:
            data = {
                "stage": stage,
                "grade": 4,
                "summary": "The proof is complete for the mock benchmark.",
                "blocking_issues": [],
                "repair_request": "",
                "failure_type": "none",
                "audit": [f"{stage} accepted the mock proof."],
            }
        elif "MOCK_PROOF_CHECKER_REJECT" in proof:
            data = {
                "stage": stage,
                "grade": 3,
                "summary": "The proof appears essentially correct but needs privileged checking.",
                "blocking_issues": [],
                "repair_request": "",
                "failure_type": "none",
                "audit": [f"{stage} found no blocking public defect."],
            }
        elif "MOCK_PROOF_MAJOR_GAP" in proof:
            data = {
                "stage": stage,
                "grade": 2,
                "summary": "A central implication is missing.",
                "blocking_issues": ["The core step is asserted without justification."],
                "repair_request": "Justify the missing central implication.",
                "failure_type": "invalid_claim",
                "audit": [f"{stage} found the mock central gap."],
            }
        else:
            data = {
                "stage": stage,
                "grade": 1,
                "summary": "The proof does not address the target.",
                "blocking_issues": ["No recognizable proof marker was found."],
                "repair_request": "Provide a coherent proof of the target.",
                "failure_type": "missing_subgoal",
                "audit": [f"{stage} found no recognizable proof."],
            }
        return json.dumps(data)

    def _check(self, user_prompt: str) -> str:
        proof = _section(user_prompt, "CANDIDATE PROOF")
        if "MOCK_PROOF_OK" in proof:
            data = {
                "decision": "PASS",
                "private_rationale": "Mock proof marker accepted.",
                "source_concern": None,
                "public_diagnosis": [],
                "recommended_hint": None,
            }
        else:
            data = {
                "decision": "FAIL",
                "private_rationale": "Mock proof marker rejected.",
                "source_concern": None,
                "public_diagnosis": ["The proof passed public verification but fails the privileged mock check."],
                "recommended_hint": "Use the next released hint.",
            }
        return json.dumps(data)


@dataclass
class OpenAICompatibleClient:
    """OpenAI-compatible client with chat-completions and Responses support."""

    model: str
    base_url: str = "https://api.openai.com/v1"
    api_key: str | None = None
    temperature: float = 0.0
    # Reasoning models at high effort routinely run for several minutes on the
    # big packet prompts; the official SDKs default to 10 minutes, and xhigh
    # calls can exceed even that, so allow 15.
    timeout_seconds: int = 900
    max_tokens: int | None = None
    # Transient-failure retries for one request: attempts on HTTP 429 and 5xx,
    # honoring Retry-After when the provider sends it, else exponential backoff
    # (10s, 20s, 40s, 80s, 160s, 180s-capped). Total patience must exceed the
    # provider's actual rate window: for gpt-5.5 on tier-1 the TPM window can
    # take 180-300s to clear, so we honor Retry-After up to 600s and cap the
    # fallback backoff at 180s rather than 60s.
    max_attempts: int = 8
    retry_base_seconds: float = 10.0
    api_surface: str = "auto"  # auto | chat | responses
    thinking: str | None = None
    reasoning_effort: str | None = None
    json_response_roles: set[str] = field(default_factory=set)
    # Roles allowed to browse via the hosted web_search tool (Responses API
    # only). Gating is per prompt.role, so one shared client instance can serve
    # both internet-enabled solver roles and browsing-forbidden verifier roles
    # without the latter ever receiving the tool.
    web_search_roles: set[str] = field(default_factory=set)
    require_web_search_roles: set[str] = field(default_factory=set)
    web_search_context_size: str | None = None
    input_price_per_1m: float | None = None
    output_price_per_1m: float | None = None

    def __post_init__(self) -> None:
        forbidden = WEB_SEARCH_FORBIDDEN_ROLES & (
            self.web_search_roles | self.require_web_search_roles
        )
        if forbidden:
            names = ", ".join(sorted(forbidden))
            raise ValueError(f"web search is forbidden for verifier/checker roles: {names}")

    @classmethod
    def from_env(cls, model: str | None = None) -> "OpenAICompatibleClient":
        selected_model = model or os.environ.get("OPENAI_MODEL", "gpt-4.1")
        return cls(
            model=selected_model,
            base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            api_key=os.environ.get("OPENAI_API_KEY"),
            temperature=float(os.environ.get("OPENAI_TEMPERATURE", "0")),
            timeout_seconds=optional_int_env("OPENAI_TIMEOUT_SECONDS") or 900,
            max_tokens=optional_int_env("OPENAI_MAX_TOKENS"),
            api_surface=os.environ.get("OPENAI_API_SURFACE", "auto"),
            thinking=os.environ.get("DEEPSEEK_THINKING") or None,
            reasoning_effort=(
                os.environ.get("DEEPSEEK_REASONING_EFFORT") or os.environ.get("OPENAI_REASONING_EFFORT") or None
            ),
            json_response_roles=optional_set_env("OPENAI_JSON_RESPONSE_ROLES"),
            web_search_roles=optional_set_env("OPENAI_WEB_SEARCH_ROLES"),
            require_web_search_roles=optional_set_env("OPENAI_REQUIRE_WEB_SEARCH_ROLES"),
            web_search_context_size=os.environ.get("OPENAI_WEB_SEARCH_CONTEXT_SIZE") or None,
            input_price_per_1m=optional_float_env("OPENAI_INPUT_PRICE_PER_1M"),
            output_price_per_1m=optional_float_env("OPENAI_OUTPUT_PRICE_PER_1M"),
        )

    def complete(self, prompt: PromptPacket, metadata: dict) -> LLMResponse:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is required for OpenAICompatibleClient")
        if self._use_responses_api():
            return self._complete_responses(prompt)
        return self._complete_chat(prompt)

    def _complete_chat(self, prompt: PromptPacket) -> LLMResponse:
        if prompt.role in self.web_search_roles:
            # The hosted web_search tool exists only on the Responses API; a
            # silent fallback would run an "internet-enabled" role without
            # internet and invalidate the run's browsing claims.
            raise RuntimeError(
                f"role {prompt.role!r} requires the hosted web_search tool, which needs the "
                "Responses API; use a Responses-capable model or --api-surface responses"
            )
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [
                {"role": "system", "content": prompt.system},
                {"role": "user", "content": prompt.user},
            ],
        }
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens
        if self.thinking is not None:
            payload["thinking"] = {"type": self.thinking}
        effort = self._normalized_reasoning_effort()
        if effort is not None:
            payload["reasoning_effort"] = effort
        if prompt.role in self.json_response_roles:
            payload["response_format"] = {"type": "json_object"}

        data = self._post_json("chat/completions", payload)
        choice = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        prompt_tokens = int(usage.get("prompt_tokens", 0))
        completion_tokens = int(usage.get("completion_tokens", 0))
        return LLMResponse(
            text=choice,
            model=str(data.get("model", self.model)),
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=self._estimate_cost(prompt_tokens, completion_tokens),
            raw=data,
        )

    def _complete_responses(self, prompt: PromptPacket) -> LLMResponse:
        payload: dict = {
            "model": self.model,
            "input": [
                {"role": "system", "content": prompt.system},
                {"role": "user", "content": prompt.user},
            ],
        }
        if self.max_tokens is not None:
            payload["max_output_tokens"] = self.max_tokens
        effort = self._normalized_reasoning_effort()
        if effort is not None:
            payload["reasoning"] = {"effort": effort}
        if prompt.role in self.web_search_roles:
            # Hosted browsing per the internet-enabled packet. Only roles the
            # protocol permits to browse (solver roles in source-supported
            # mode, plus restricted citation/source-checking roles) are placed
            # here. Proof verifiers and the Final Checker are never included.
            tool: dict = {"type": "web_search"}
            if self.web_search_context_size is not None:
                tool["search_context_size"] = self.web_search_context_size
            payload["tools"] = [tool]
            if prompt.role in self.require_web_search_roles:
                payload["tool_choice"] = "required"
        if prompt.role in self.json_response_roles:
            payload["text"] = {"format": {"type": "json_object"}}

        data = self._post_json("responses", payload)
        text = self._extract_responses_text(data)
        usage = data.get("usage", {})
        prompt_tokens = int(usage.get("input_tokens", usage.get("prompt_tokens", 0)))
        completion_tokens = int(usage.get("output_tokens", usage.get("completion_tokens", 0)))
        return LLMResponse(
            text=text,
            model=str(data.get("model", self.model)),
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=self._estimate_cost(prompt_tokens, completion_tokens),
            raw=data,
        )

    # HTTP statuses treated as transient: rate limits, request timeouts,
    # conflicts, and server-side errors (the same set the official OpenAI SDKs
    # retry by default).
    RETRYABLE_STATUSES = frozenset({408, 409, 429, 500, 502, 503, 504})

    def _post_json(self, path: str, payload: dict) -> dict:
        body = json.dumps(payload).encode("utf-8")
        last_status: int | None = None
        last_code: str | None = None
        for attempt in range(1, max(1, self.max_attempts) + 1):
            request = urllib.request.Request(
                url=f"{self.base_url.rstrip('/')}/{path}",
                data=body,
                method="POST",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
            try:
                with urllib.request.urlopen(
                    request, timeout=self.timeout_seconds, context=_ssl_context()
                ) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                # Extract only the provider's short machine-readable error code;
                # the body itself may echo prompt text and is never surfaced.
                last_status = exc.code
                last_code = _safe_error_code(exc)
                if exc.code in self.RETRYABLE_STATUSES and attempt < max(1, self.max_attempts):
                    delay = _retry_delay(exc, attempt, self.retry_base_seconds)
                    # Status/code/delay only -- never anything prompt-derived.
                    print(
                        f"[llm] transient API error {exc.code}"
                        + (f" ({last_code})" if last_code else "")
                        + f"; retrying in {delay:.0f}s (attempt {attempt}/{self.max_attempts})",
                        file=sys.stderr,
                        flush=True,
                    )
                    time.sleep(delay)
                    continue
                raise RuntimeError(_redacted_api_error(last_status, last_code)) from exc
        raise RuntimeError(_redacted_api_error(last_status, last_code))

    def _use_responses_api(self) -> bool:
        surface = self.api_surface.lower().strip()
        if surface == "responses":
            return True
        if surface == "chat":
            return False
        return self.model.startswith("gpt-5.5")

    def _normalized_reasoning_effort(self) -> str | None:
        if self.reasoning_effort is None:
            return None
        raw = self.reasoning_effort.strip()
        if raw.lower() == "omit":
            return None
        aliases = {
            "extra_high": "xhigh",
            "extra-high": "xhigh",
            "very_high": "xhigh",
            "very-high": "xhigh",
        }
        return aliases.get(raw.lower(), raw)

    @staticmethod
    def _extract_responses_text(data: dict) -> str:
        if isinstance(data.get("output_text"), str):
            return data["output_text"]
        chunks: list[str] = []
        for item in data.get("output", []):
            if item.get("type") == "message":
                for content in item.get("content", []):
                    if isinstance(content.get("text"), str):
                        chunks.append(content["text"])
            elif isinstance(item.get("text"), str):
                chunks.append(item["text"])
        return "\n".join(chunks)

    def _estimate_cost(self, prompt_tokens: int, completion_tokens: int) -> float | None:
        if self.input_price_per_1m is None or self.output_price_per_1m is None:
            return None
        return (
            prompt_tokens / 1_000_000 * self.input_price_per_1m
            + completion_tokens / 1_000_000 * self.output_price_per_1m
        )


# Only accept short enum-like error codes so nothing prompt-derived can leak
# into error messages (provider codes look like "insufficient_quota" or
# "rate_limit_exceeded").
_SAFE_ERROR_CODE_RE = re.compile(r"^[A-Za-z0-9_.\-]{1,64}$")


def _safe_error_code(exc: urllib.error.HTTPError) -> str | None:
    """Extract the provider's machine-readable error code, never the message.

    Reads the error body (which must be drained anyway), parses it as JSON, and
    returns ``error.code`` / ``error.type`` only when it looks like a short
    enum value. Anything else -- including parse failures -- yields ``None`` so
    prompt-echoing bodies can never reach logs or stderr.
    """

    try:
        raw = exc.read()
    except Exception:  # noqa: BLE001 - draining best-effort
        return None
    try:
        data = json.loads(raw.decode("utf-8", errors="replace"))
        error = data.get("error", {})
        candidate = error.get("code") or error.get("type")
    except Exception:  # noqa: BLE001 - non-JSON bodies are simply dropped
        return None
    if isinstance(candidate, str) and _SAFE_ERROR_CODE_RE.match(candidate):
        return candidate
    return None


def _retry_delay(exc: urllib.error.HTTPError, attempt: int, base_seconds: float) -> float:
    """Delay before the next attempt: Retry-After when sane, else backoff.

    Retry-After is honored up to 600s so that TPM windows of 3-5 minutes
    (common for gpt-5.5 on tier-1 keys) are actually respected rather than
    silently ignored. Values above 600s are treated as insane and fall back
    to the exponential backoff, which is capped at 180s.
    """

    retry_after = exc.headers.get("Retry-After") if exc.headers else None
    if retry_after:
        try:
            parsed = float(retry_after)
            if 0 <= parsed <= 600:
                return parsed
        except ValueError:
            pass
    backoff = min(base_seconds * (2 ** (attempt - 1)), 180.0)
    return min(backoff + random.uniform(0.0, 1.0), 180.0)


def _redacted_api_error(status: int | None, code: str | None) -> str:
    """Build the user-facing error string: status + safe code, body withheld."""

    detail = f" ({code})" if code else ""
    return (
        f"OpenAI-compatible API error {status}{detail}: "
        "response body omitted to avoid leaking prompt data"
    )


def make_client(kind: str, model: str | None = None) -> LLMClient:
    """Factory used by library callers that do not need CLI-only options."""

    if kind == "mock":
        return MockLLMClient(model=model or "mock-mvp-model")
    if kind in {"openai", "api"}:
        return OpenAICompatibleClient.from_env(model=model)
    raise ValueError(f"Unknown client kind: {kind}")


def _ssl_context() -> ssl.SSLContext:
    cafile = _find_cafile()
    if cafile is not None:
        return ssl.create_default_context(cafile=str(cafile))
    return ssl.create_default_context()


def _find_cafile() -> Path | None:
    candidates: list[str | None] = [
        os.environ.get("SSL_CERT_FILE"),
        ssl.get_default_verify_paths().cafile,
        "/etc/ssl/certs/ca-certificates.crt",
        "/etc/ssl/cert.pem",
        "/private/etc/ssl/cert.pem",
        "/opt/anaconda3/ssl/cacert.pem",
    ]
    try:
        import certifi  # type: ignore

        candidates.insert(1, certifi.where())
    except Exception:
        pass
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return Path(candidate)
    return None


def _section(prompt: str, title: str) -> str:
    pattern = rf"(?ms)^{re.escape(title)}\n(.*?)(?:\n[A-Z][A-Z _]+\n|\Z)"
    match = re.search(pattern, prompt)
    if not match:
        return prompt
    return match.group(1).strip()


def _mock_hints(task_id: str) -> str:
    lines = [f"# {task_id} hints", ""]
    for level in range(1, 11):
        lines.extend([f"## H{level}", f"Mock cumulative hint {level} for {task_id}.", ""])
    return "\n".join(lines).rstrip() + "\n"


def _mock_bundle(paper_id: str) -> str:
    """Build a complete toy benchmark bundle as the bundle-builder file-block text."""

    task_specs = [
        (
            "R001",
            1,
            "theorem",
            "mock_pass_h0",
            "Every mock complete proof establishes the first target. [MOCK_PASS_H0]",
            False,
            None,
        ),
        (
            "R002",
            2,
            "lemma",
            "mock_revision_pass",
            "The second target requires one verifier-guided revision in the mock loop. [MOCK_REVISION_PASS]",
            False,
            None,
        ),
        (
            "R003",
            3,
            "proposition",
            "mock_checker_reject_then_hint",
            "The third target first passes the Verifier but is rejected by the Final Checker until one hint is released. [MOCK_CHECKER_REJECT_THEN_HINT]",
            False,
            None,
        ),
        (
            "R004",
            4,
            "corollary",
            "mock_unsolved",
            "The fourth target remains unsolved in the mock loop. [MOCK_UNSOLVED]",
            False,
            None,
        ),
        (
            "R005",
            5,
            "theorem",
            "skip example",
            "This target is marked skip_mvp because its proof intentionally depends on unavailable later material.",
            True,
            "Depends on unavailable later material.",
        ),
    ]
    cleaned_lines = [
        "# Toy Linear Prefix Paper",
        "",
        "We work in a toy mathematical setting. Earlier result statements may be cited by their result IDs.",
        "",
    ]
    tasks_jsonl: list[str] = []
    gold_blocks: list[str] = []
    for task_id, order, result_type, title, statement, skip_mvp, skip_reason in task_specs:
        cleaned_lines.extend([f"## {task_id} {result_type.title()}", "", statement, ""])
        tasks_jsonl.append(
            json.dumps(
                {
                    "paper_id": paper_id,
                    "task_id": task_id,
                    "order": order,
                    "result_type": result_type,
                    "title": title,
                    "target_statement": statement,
                    "prefix_end_marker": task_id,
                    "skip_mvp": skip_mvp,
                    "skip_reason": skip_reason,
                },
                separators=(",", ":"),
            )
        )
        if not skip_mvp:
            gold_blocks.extend(
                [
                    f"---BEGIN FILE private/gold/{task_id}.md---",
                    f"# {task_id} source proof",
                    "",
                    "SOURCE_PROOF_SENTINEL. The toy proof accepts MOCK_PROOF_OK.",
                    "---END FILE---",
                ]
            )
    blocks = [
        "---BEGIN FILE cleaned_paper.md---",
        "\n".join(cleaned_lines).rstrip(),
        "---END FILE---",
        "---BEGIN FILE tasks.jsonl---",
        "\n".join(tasks_jsonl),
        "---END FILE---",
        *gold_blocks,
    ]
    return "\n".join(blocks) + "\n"
