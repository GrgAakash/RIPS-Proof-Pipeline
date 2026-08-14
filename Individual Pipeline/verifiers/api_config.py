"""Configuration helpers for optional OpenAI-backed verifier runs."""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass


DEFAULT_VERIFIER_MODEL = "gpt-5.2"
DEFAULT_MAX_OUTPUT_TOKENS = 4096
DEFAULT_TIMEOUT_SECONDS = 120.0


@dataclass(frozen=True)
class ApiConfig:
    model: str = DEFAULT_VERIFIER_MODEL
    max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
    reasoning_effort: str | None = None
    api_key_present: bool = False
    dry_run: bool = False

    def to_public_dict(self) -> dict:
        return asdict(self)


def load_api_config(*, require_api_key: bool = True) -> ApiConfig:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    config = ApiConfig(
        model=os.environ.get("OPENAI_VERIFIER_MODEL", DEFAULT_VERIFIER_MODEL).strip() or DEFAULT_VERIFIER_MODEL,
        max_output_tokens=_int_env("OPENAI_VERIFIER_MAX_OUTPUT_TOKENS", DEFAULT_MAX_OUTPUT_TOKENS),
        timeout_seconds=_float_env("OPENAI_VERIFIER_TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS),
        reasoning_effort=_optional_env("OPENAI_VERIFIER_REASONING_EFFORT"),
        api_key_present=bool(api_key),
        dry_run=_bool_env("OPENAI_VERIFIER_DRY_RUN", False),
    )
    if require_api_key and not config.api_key_present and not config.dry_run:
        raise RuntimeError("OPENAI_API_KEY is not set. Set it in the environment before running API verifier mode.")
    return config


def _int_env(name: str, default: int) -> int:
    value = os.environ.get(name, "").strip()
    if not value:
        return default
    try:
        parsed = int(value)
    except ValueError:
        return default
    return parsed if parsed > 0 else default


def _float_env(name: str, default: float) -> float:
    value = os.environ.get(name, "").strip()
    if not value:
        return default
    try:
        parsed = float(value)
    except ValueError:
        return default
    return parsed if parsed > 0 else default


def _bool_env(name: str, default: bool) -> bool:
    value = os.environ.get(name, "").strip().lower()
    if not value:
        return default
    return value in {"1", "true", "yes", "on"}


def _optional_env(name: str) -> str | None:
    value = os.environ.get(name, "").strip()
    return value or None
