#!/usr/bin/env python3
"""Generate component-owned prompt views from the canonical prompt packets."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

def _resolve_layout(module_root: Path, install_prefix: Path) -> tuple[Path, Path]:
    """Locate generated prompt views and the canonical packet in either layout."""

    source_component_root = module_root / "Individual Pipeline"
    if source_component_root.is_dir():
        return source_component_root, module_root / "Prompt Packet"

    # Wheels install packages into site-packages but ``data-files`` into the
    # environment prefix.  Keeping both locations explicit makes the command
    # work from any current working directory after installation.
    installed_packet_root = install_prefix / "Prompt Packet"
    return module_root, installed_packet_root


MODULE_ROOT = Path(__file__).resolve().parent
COMPONENT_ROOT, PACKET_ROOT = _resolve_layout(MODULE_ROOT, Path(sys.prefix))
if str(COMPONENT_ROOT) not in sys.path:
    sys.path.insert(0, str(COMPONENT_ROOT))

from citation.prompts import CitationPromptTemplates  # noqa: E402
from solver.prompt_loader import PacketPrompts  # noqa: E402
from solver.skeleton_source_gate import SkeletonSourcePromptTemplates  # noqa: E402


NO_INTERNET_PACKET = PACKET_ROOT / "Prompts.md"
FULL_INTERNET_PACKET = PACKET_ROOT / "PromptsWithFullInternet.md"

SOLVER_ROLES = {
    "s0": "s0.md",
    "subproblem": "s1_s5_subproblem.md",
    "s6": "s6.md",
}
SOURCE_GATE_ROLES = {
    "skeleton_source_generator": "skeleton_source_generator.md",
    "skeleton_source_verifier": "skeleton_source_verifier.md",
}
CITATION_ROLES = {
    "citation_generator": "citation_generator.md",
    "citation_verifier": "citation_verifier.md",
}
VERIFIER_ROLES = {
    "verifier_a": "verifier_a.md",
    "verifier_b": "verifier_b.md",
    "verifier_c": "verifier_c.md",
    "composer_a": "composer_a.md",
    "final_checker": "final_checker.md",
}

_DIVIDER_RE = re.compile(r"(?m)^(?:={16,}|-{16,})\s*$")
_PROBLEM_STATEMENT_ANCHOR = "You are the Problem Statement Verifier."


class PromptSyncError(RuntimeError):
    """Raised when canonical packets cannot produce unambiguous prompt views."""


def _extract_to_divider(packet_text: str, anchor: str) -> str:
    start = packet_text.find(anchor)
    if start < 0:
        raise PromptSyncError(f"prompt anchor not found: {anchor!r}")
    divider = _DIVIDER_RE.search(packet_text, start)
    end = divider.start() if divider else len(packet_text)
    return packet_text[start:end].strip() + "\n"


def _require_shared(
    label: str,
    no_internet: dict[str, str],
    full_internet: dict[str, str],
) -> dict[str, str]:
    if no_internet.keys() != full_internet.keys():
        raise PromptSyncError(f"{label}: role sets differ between canonical packets")
    changed = [role for role in no_internet if no_internet[role] != full_internet[role]]
    if changed:
        raise PromptSyncError(
            f"{label}: shared prompt text differs between canonical packets: "
            + ", ".join(changed)
        )
    return no_internet


def expected_views() -> dict[str, str]:
    """Return every generated prompt path and its canonical text."""

    no_solver = PacketPrompts.from_file(NO_INTERNET_PACKET).prompts
    web_solver = PacketPrompts.from_file(FULL_INTERNET_PACKET).prompts
    no_source = SkeletonSourcePromptTemplates.from_file(NO_INTERNET_PACKET).prompts
    web_source = SkeletonSourcePromptTemplates.from_file(FULL_INTERNET_PACKET).prompts
    no_citation = CitationPromptTemplates.from_file(NO_INTERNET_PACKET).prompts
    web_citation = CitationPromptTemplates.from_file(FULL_INTERNET_PACKET).prompts

    shared_source = _require_shared("source gate", no_source, web_source)
    shared_citation = _require_shared("citation", no_citation, web_citation)
    shared_verifiers = _require_shared(
        "verifier",
        {role: no_solver[role] for role in VERIFIER_ROLES},
        {role: web_solver[role] for role in VERIFIER_ROLES},
    )

    no_text = NO_INTERNET_PACKET.read_text(encoding="utf-8")
    web_text = FULL_INTERNET_PACKET.read_text(encoding="utf-8")
    no_problem = _extract_to_divider(no_text, _PROBLEM_STATEMENT_ANCHOR)
    web_problem = _extract_to_divider(web_text, _PROBLEM_STATEMENT_ANCHOR)
    if no_problem != web_problem:
        raise PromptSyncError(
            "problem statement verifier differs between canonical packets"
        )

    views: dict[str, str] = {}
    for role, filename in SOLVER_ROLES.items():
        views[f"solver/prompts/no_internet/{filename}"] = no_solver[role]
        views[f"solver/prompts/full_internet/{filename}"] = web_solver[role]
    for role, filename in SOURCE_GATE_ROLES.items():
        views[f"solver/prompts/source_gate/{filename}"] = shared_source[role]
    for role, filename in CITATION_ROLES.items():
        views[f"citation/prompts/{filename}"] = shared_citation[role]
    for role, filename in VERIFIER_ROLES.items():
        views[f"verifiers/prompts/{filename}"] = shared_verifiers[role]
    views["verifiers/prompts/problem_statement_verifier.md"] = no_problem
    return views


def stale_views() -> list[str]:
    stale = []
    for relative, expected in expected_views().items():
        path = COMPONENT_ROOT / relative
        if not path.is_file() or path.read_text(encoding="utf-8-sig") != expected:
            stale.append(relative)
    return stale


def write_views() -> dict[str, str]:
    views = expected_views()
    for relative, prompt in views.items():
        path = COMPONENT_ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(prompt, encoding="utf-8")
    return views


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    try:
        if args.write:
            views = write_views()
            print(f"wrote {len(views)} component prompt views")
            return 0
        stale = stale_views()
    except (OSError, ValueError, PromptSyncError) as exc:
        print(f"error: {exc}")
        return 1

    if stale:
        print("stale component prompt views:")
        for relative in stale:
            print(f"- {relative}")
        return 1
    print(f"component prompt views current ({len(expected_views())} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
