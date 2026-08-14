"""Thin OpenAI API wrapper for verifier calls.

This module is intentionally small: it sends text to the API and returns raw
text plus non-secret metadata. Routing and parsing stay in the existing
verifiers modules.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from time import perf_counter
from typing import Any

from verifiers.api_config import ApiConfig


@dataclass(frozen=True)
class ApiVerifierResult:
    raw_text: str
    model: str
    usage: dict[str, Any] = field(default_factory=dict)
    latency_ms: int = 0
    error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def call_openai_verifier(prompt: str, *, config: ApiConfig) -> ApiVerifierResult:
    if config.dry_run:
        return ApiVerifierResult(
            raw_text="",
            model=config.model,
            usage={},
            latency_ms=0,
            error="dry_run_enabled",
        )

    start = perf_counter()
    try:
        from openai import OpenAI

        client = OpenAI(timeout=config.timeout_seconds)
        request = {
            "model": config.model,
            "input": prompt,
            "max_output_tokens": config.max_output_tokens,
        }
        if config.reasoning_effort:
            request["reasoning"] = {"effort": config.reasoning_effort}
        response = client.responses.create(**request)
        latency_ms = int((perf_counter() - start) * 1000)
        return ApiVerifierResult(
            raw_text=getattr(response, "output_text", "") or "",
            model=config.model,
            usage=_usage_to_dict(getattr(response, "usage", None)),
            latency_ms=latency_ms,
            error=None,
        )
    except Exception as exc:  # pragma: no cover - exact SDK/network exceptions vary.
        latency_ms = int((perf_counter() - start) * 1000)
        return ApiVerifierResult(
            raw_text="",
            model=config.model,
            usage={},
            latency_ms=latency_ms,
            error=f"{exc.__class__.__name__}: {exc}",
        )


def _usage_to_dict(usage: Any) -> dict[str, Any]:
    if usage is None:
        return {}
    if hasattr(usage, "model_dump"):
        return usage.model_dump()
    if hasattr(usage, "dict"):
        return usage.dict()
    if isinstance(usage, dict):
        return usage
    return {}
