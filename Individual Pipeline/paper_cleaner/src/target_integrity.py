"""Deterministic statement identity and immutable-target checks.

The parser cannot safely emulate arbitrary LaTeX theorem counters. Statement
identity therefore comes from source evidence, never a displayed number. A
selected target must retain an exact source slice and every public package must
carry the indexed statement verbatim.
"""
from __future__ import annotations

import re
from typing import Any

from .common import sha256_text
from .schemas import Statement


TARGET_HEADING = "## 6. Target"


def _unique_id(base: str, used_ids: set[str]) -> str:
    """Return ``base`` or a deterministic collision suffix."""

    if base not in used_ids:
        return base
    seq = 2
    while f"{base}-{seq}" in used_ids:
        seq += 1
    return f"{base}-{seq}"


def source_statement_id(
    *,
    paper_id: str,
    env_type: str,
    statement_tex: str,
    latex_label: str,
    used_ids: set[str],
    duplicate_label: bool = False,
) -> str:
    """Make an opaque ID from a source label or exact statement text."""

    if latex_label.strip() and duplicate_label:
        evidence = (
            f"duplicate-label\0{latex_label.strip()}\0{env_type}\0{statement_tex}"
        )
    elif latex_label.strip():
        evidence = f"label\0{latex_label.strip()}"
    else:
        evidence = f"statement\0{env_type}\0{statement_tex}"
    digest = sha256_text(f"{paper_id}\0{evidence}")[:12]
    return _unique_id(f"stmt-{digest}", used_ids)


def context_statement_id(
    *,
    paper_id: str,
    added_by: str,
    env_type: str,
    statement_tex: str,
    used_ids: set[str],
) -> str:
    """Make an opaque ID for non-authoritative, model-added context."""

    digest = sha256_text(
        f"{paper_id}\0context\0{added_by}\0{env_type}\0{statement_tex}"
    )[:12]
    return _unique_id(f"ctx-{digest}", used_ids)


def statement_source_issues(
    statement: Statement,
    *,
    flat_source: str,
    expected_source_file: str,
) -> list[str]:
    """Return reasons a statement is not provably backed by the source file."""

    issues: list[str] = []
    if statement.added_by != "parser":
        issues.append("statement was introduced by a model")
    if not statement.source_verified:
        issues.append("statement is not marked source-verified")
    if statement.source_file != expected_source_file:
        issues.append("statement source file does not match the paper source")
    if not (0 <= statement.source_start < statement.source_end <= len(flat_source)):
        issues.append("statement source span is invalid")
        source_slice = ""
    else:
        source_slice = flat_source[statement.source_start:statement.source_end]
    if not statement.statement_sha256:
        issues.append("statement hash is missing")
    elif sha256_text(statement.statement_tex) != statement.statement_sha256:
        issues.append("statement text does not match its recorded hash")
    if not statement.source_sha256:
        issues.append("source-slice hash is missing")
    elif source_slice and sha256_text(source_slice) != statement.source_sha256:
        issues.append("source slice does not match its recorded hash")
    if source_slice and statement.statement_tex not in source_slice:
        issues.append("statement text is not an exact substring of its source slice")
    return issues


PROOF_PAIRING_METHODS = frozenset({
    "explicit-label",
    "explicit-heading-label",
    "adjacent",
    "explicit-label-recovery",
})


def proof_source_issues(
    statement: Statement,
    *,
    flat_source: str,
    expected_source_file: str,
) -> list[str]:
    """Return reasons a reference proof lacks verified source provenance."""

    issues: list[str] = []
    proof = statement.proof_tex or ""
    if not proof:
        issues.append("proof text is missing")
    if not statement.proof_source_verified:
        issues.append("proof is not marked source-verified")
    if statement.proof_pairing not in PROOF_PAIRING_METHODS:
        issues.append("proof lacks an approved deterministic pairing method")
    if statement.proof_source_file != expected_source_file:
        issues.append("proof source file does not match the paper source")
    if not (
        0
        <= statement.proof_source_start
        < statement.proof_source_end
        <= len(flat_source)
    ):
        issues.append("proof source span is invalid")
        source_slice = ""
    else:
        source_slice = flat_source[
            statement.proof_source_start:statement.proof_source_end
        ]
    if not statement.proof_sha256:
        issues.append("proof hash is missing")
    elif sha256_text(proof) != statement.proof_sha256:
        issues.append("proof text does not match its recorded hash")
    if not statement.proof_source_sha256:
        issues.append("proof source-slice hash is missing")
    elif source_slice and sha256_text(source_slice) != statement.proof_source_sha256:
        issues.append("proof source slice does not match its recorded hash")
    if source_slice and proof not in source_slice:
        issues.append("proof text is not an exact substring of its source slice")
    return issues


def canonical_target_section(statement_tex: str) -> str:
    """Render the target without an inferred number, name, or paraphrase."""

    if not statement_tex:
        raise ValueError("target statement is empty")
    return f"{TARGET_HEADING}\n\n**Target statement.**\n\n{statement_tex}\n"


def canonicalize_target_section(body: str, *, statement_tex: str) -> str:
    """Delete any model-written target and append the frozen target verbatim."""

    start = body.find(TARGET_HEADING)
    prefix = body[:start] if start >= 0 else body
    prefix = prefix.rstrip()
    target = canonical_target_section(statement_tex)
    return f"{prefix}\n\n{target}" if prefix else target


def target_identity_issues(problem_or_body: str, statement: Statement) -> list[str]:
    """Reject an invalid index hash or any packaged Section 6 target drift."""

    issues: list[str] = []
    if not statement.statement_sha256:
        issues.append("target statement hash is missing")
    elif sha256_text(statement.statement_tex) != statement.statement_sha256:
        issues.append("indexed target text does not match its frozen hash")
    start = problem_or_body.find(TARGET_HEADING)
    prefix = problem_or_body[:start] if start >= 0 else problem_or_body
    norm_target = re.sub(r"\s+", " ", statement.statement_tex).strip()
    norm_prefix = re.sub(r"\s+", " ", prefix)
    if norm_target and norm_target in norm_prefix:
        issues.append("the target statement appears outside controller-owned Section 6")
    actual = problem_or_body[start:] if start >= 0 else ""
    expected = canonical_target_section(statement.statement_tex)
    if actual.strip() != expected.strip():
        issues.append("Section 6 does not exactly match the frozen target")
    return issues


def frozen_target_record(statement: Statement) -> dict[str, Any]:
    """Metadata stored beside ``target.tex`` for independent verification."""

    return {
        "target_id": statement.id,
        "statement_sha256": statement.statement_sha256,
        "source_file": statement.source_file,
        "source_start": statement.source_start,
        "source_end": statement.source_end,
        "source_sha256": statement.source_sha256,
        "proof_sha256": statement.proof_sha256,
        "proof_source_file": statement.proof_source_file,
        "proof_source_start": statement.proof_source_start,
        "proof_source_end": statement.proof_source_end,
        "proof_source_sha256": statement.proof_source_sha256,
        "proof_source_verified": statement.proof_source_verified,
        "proof_pairing": statement.proof_pairing,
    }


def frozen_target_artifact_issues(
    statement: Statement,
    *,
    target_tex: str,
    record: dict[str, Any],
) -> list[str]:
    """Verify the read-only target artifacts stored with a package."""

    issues: list[str] = []
    if target_tex != statement.statement_tex:
        issues.append("target.tex does not exactly match the indexed target")
    expected = frozen_target_record(statement)
    if not isinstance(record, dict):
        issues.append("target.json must contain a JSON object")
    elif record != expected:
        missing = sorted(set(expected) - set(record))
        extra = sorted(set(record) - set(expected))
        if missing:
            issues.append("target.json is missing fields: " + ", ".join(missing))
        if extra:
            issues.append("target.json has unexpected fields: " + ", ".join(extra))
        for key in sorted(set(expected) & set(record)):
            if record[key] != expected[key]:
                issues.append(f"target.json field {key} does not match the index")
    return issues
