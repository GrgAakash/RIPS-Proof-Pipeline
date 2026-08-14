#!/usr/bin/env python3
"""Thin entry point for the canonical ``run-cleaner-solver`` command."""

from __future__ import annotations

import sys
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = SCRIPT_ROOT / "Individual Pipeline"


def main(argv: list[str] | None = None) -> int:
    """Run the integrated pipeline without duplicating its implementation."""

    src = str(SRC_ROOT)
    if src not in sys.path:
        sys.path.insert(0, src)
    from solver.cli import main as cli_main

    arguments = list(sys.argv[1:] if argv is None else argv)
    return cli_main(["run-cleaner-solver", *arguments])


if __name__ == "__main__":
    raise SystemExit(main())
