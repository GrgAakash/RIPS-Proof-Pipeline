"""Small JSON and model-output helpers required by the standalone solver."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class SolverIOError(RuntimeError):
    """Raised when a solver artifact is missing or malformed."""


def read_json(path: Path) -> dict[str, Any]:
    """Read one JSON object from disk."""

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SolverIOError(f"Missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SolverIOError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SolverIOError(f"Expected a JSON object in {path}")
    return value


def write_json(path: Path, data: dict[str, Any]) -> None:
    """Write stable, human-readable JSON."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_json_object(text: str, record_name: str) -> dict[str, Any]:
    """Extract one model-produced JSON object from a noisy response."""

    data = _try_load_json_object(text)
    if data is None:
        raise SolverIOError(f"{record_name} did not return a JSON object:\n{text}")
    return data


def _try_load_json_object(text: str) -> dict[str, Any] | None:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = _strip_fenced_json(stripped)
    data = _loads_json_object(stripped)
    if data is not None:
        return data
    for snippet in reversed(_balanced_objects(stripped)):
        data = _loads_json_object(snippet)
        if data is not None:
            return data
    return None


def _loads_json_object(text: str) -> dict[str, Any] | None:
    for candidate in (text, _escape_invalid_json_backslashes(text)):
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            return data
    return None


def _escape_invalid_json_backslashes(text: str) -> str:
    valid_escapes = {'"', "\\", "/", "b", "f", "n", "r", "t", "u"}
    chars: list[str] = []
    in_string = False
    index = 0
    while index < len(text):
        char = text[index]
        if not in_string:
            chars.append(char)
            if char == '"':
                in_string = True
            index += 1
            continue
        if char == "\\":
            next_char = text[index + 1] if index + 1 < len(text) else ""
            if next_char in valid_escapes:
                chars.append(char)
                if next_char:
                    chars.append(next_char)
                    index += 2
                else:
                    index += 1
            else:
                chars.append("\\\\")
                index += 1
            continue
        chars.append(char)
        if char == '"':
            in_string = False
        index += 1
    return "".join(chars)


def _balanced_objects(text: str) -> list[str]:
    snippets: list[str] = []
    index = 0
    while index < len(text):
        start = text.find("{", index)
        if start < 0:
            break
        end = _balanced_object_end(text, start)
        if end is None:
            index = start + 1
            continue
        snippets.append(text[start : end + 1])
        index = end + 1
    return snippets


def _balanced_object_end(text: str, start: int) -> int | None:
    if start < 0 or start >= len(text) or text[start] != "{":
        return None
    depth = 0
    in_string = False
    escape = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    return None


def _strip_fenced_json(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()
