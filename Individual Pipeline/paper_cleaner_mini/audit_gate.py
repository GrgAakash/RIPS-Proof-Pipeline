"""Dependency-free pass/fail rule for one independently audited package."""

from __future__ import annotations


def package_audit_pass(
    *,
    self_contained: bool,
    leak_free: bool,
    sufficient: bool,
    issues: list[dict],
    det_leak_spans: list[str],
    unknown_commands: list[str],
    hash_matches: bool,
) -> bool:
    """Return true only when every pre-solver package audit gate is clear."""

    return (
        self_contained
        and leak_free
        and sufficient
        and not any(issue.get("severity") == "fatal" for issue in issues)
        and not det_leak_spans
        and not unknown_commands
        and hash_matches
    )
