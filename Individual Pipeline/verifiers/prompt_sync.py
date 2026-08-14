"""Compatibility CLI for synchronizing verifier-owned prompt views."""

from __future__ import annotations

import argparse
from pathlib import Path

from prompt_sync import COMPONENT_ROOT, expected_views, write_views


LOCAL_PROMPTS = COMPONENT_ROOT / "verifiers" / "prompts"
VERIFIER_PREFIX = "verifiers/prompts/"


def expected_prompts() -> dict[str, str]:
    return {
        relative.removeprefix(VERIFIER_PREFIX): prompt
        for relative, prompt in expected_views().items()
        if relative.startswith(VERIFIER_PREFIX)
    }


SECTIONS = tuple(expected_prompts())


def write_prompt_copies() -> None:
    write_views()


def stale_prompt_copies() -> list[str]:
    stale = []
    for name, expected in expected_prompts().items():
        path = LOCAL_PROMPTS / name
        if not path.is_file() or path.read_text(encoding="utf-8-sig") != expected:
            stale.append(name)
    return stale


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    if args.write:
        write_prompt_copies()
        print(f"wrote {len(SECTIONS)} verifier prompt views")
        return 0

    stale = stale_prompt_copies()
    if stale:
        print("stale verifier prompt views: " + ", ".join(stale))
        return 1
    print(f"verifier prompt views current ({len(SECTIONS)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
