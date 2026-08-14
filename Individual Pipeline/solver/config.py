"""Shared configuration helpers for environment variables and local secrets.

This module deliberately stores only *names* and parsing rules. Runtime secret
values still come from environment variables or ignored local files, and no
caller should log the returned API key string.

It is the single place that encodes the project's API-key resolution policy
(documented in the README "API key resolution" section): the ``--api-key-env`` name,
the ``DEEPSEEK_API_KEY`` / ``OPENAI_API_KEY`` fallbacks, and the local
``API_key.md`` file. ``cli.py`` and ``llm.py`` consume these helpers so the
lookup order stays consistent across the codebase.
"""

from __future__ import annotations

import os
import re
from pathlib import Path


# --- API-key resolution policy ---
# Default environment variable consulted when no explicit ``--api-key-env`` is
# given, plus the fixed fallback chain. Order here defines lookup precedence.
DEFAULT_API_KEY_ENV = "OPENAI_API_KEY"
API_KEY_ENV_FALLBACKS = ("DEEPSEEK_API_KEY", "OPENAI_API_KEY")
# Local, git-ignored file scanned as a last resort when no env var is set.
DEFAULT_API_KEY_FILE = Path("API_key.md")

# Match the common OpenAI-style ``sk-...`` form first, then a generic long
# token. The fallback keeps compatibility with providers whose keys are not
# prefixed, but callers should avoid printing the matched value.
API_KEY_TOKEN_RE = re.compile(r"(?:sk-[A-Za-z0-9_-]+|[A-Za-z0-9][A-Za-z0-9_-]{19,})")


def ordered_api_key_env_names(primary: str | None = DEFAULT_API_KEY_ENV) -> list[str]:
    """Return API-key environment variable names in lookup order without duplicates.

    The caller's preferred variable (``primary``) is tried first, then the fixed
    fallbacks. ``dict.fromkeys`` preserves first-seen order while dropping the
    duplicate that occurs when ``primary`` is itself one of the fallbacks
    (e.g. the default ``OPENAI_API_KEY``). ``None`` entries are skipped so an
    unset ``--api-key-env`` does not introduce a blank name.
    """

    names = [primary, *API_KEY_ENV_FALLBACKS]
    return list(dict.fromkeys(name for name in names if name))


def extract_api_key_from_text(text: str) -> str | None:
    """Extract the first likely key token from a local key file.

    Provider keys sometimes lack a prefix, but accepting any long token in any
    prose would be too error-prone. Generic tokens are accepted only when the
    line looks like a direct key assignment or contains the token alone.

    Returns the first accepted token, or ``None`` if no line yields one.
    """

    for line in text.splitlines():
        stripped = line.strip()
        # Skip blank lines and Markdown comments/prose markers so a key file can
        # carry human notes without their words being mistaken for tokens.
        if not stripped or stripped.startswith("#"):
            continue
        for match in API_KEY_TOKEN_RE.finditer(stripped):
            token = match.group(0).strip()
            # ``sk-`` tokens are unambiguous; generic long tokens are trusted
            # only when the surrounding line reads like a key assignment.
            if token.startswith("sk-") or _looks_like_key_line(stripped, token):
                return token
    return None


def _looks_like_key_line(line: str, token: str) -> bool:
    """Accept generic provider tokens only from simple key-like lines.

    A line qualifies when it is exactly the token, or when the text preceding
    the token mentions an assignment-style marker (``api``/``key``/``token``/
    ``secret``). This is the guard that keeps long ordinary words in prose from
    being returned as keys.
    """

    if line == token:
        return True
    prefix = line[: line.find(token)].lower()
    if any(marker in prefix for marker in ("api", "key", "token", "secret")):
        return True
    return False


# --- Optional environment-variable parsing ---
# These helpers back the optional CLI overrides (prices, token caps, hint-worker
# sets). Each treats an unset or empty variable as "not provided" so callers can
# distinguish a real value from a default without raising on missing config.

def optional_float_env(name: str) -> float | None:
    """Parse an optional float environment variable, treating unset/empty as absent."""

    value = os.environ.get(name)
    return float(value) if value not in {None, ""} else None


def optional_int_env(name: str) -> int | None:
    """Parse an optional integer environment variable, treating unset/empty as absent."""

    value = os.environ.get(name)
    return int(value) if value not in {None, ""} else None


def optional_set_env(name: str) -> set[str]:
    """Parse a comma-separated environment variable into a trimmed set.

    Empty items (from stray commas or surrounding whitespace) are dropped, and
    an unset/empty variable yields an empty set rather than ``None``.
    """

    value = os.environ.get(name)
    if value in {None, ""}:
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}
