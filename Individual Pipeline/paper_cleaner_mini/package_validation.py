"""Dependency-free deterministic checks for Mini problem packages."""

from __future__ import annotations

import hashlib
import re
from typing import Any


SECTION3_HEADING = "## 3. Known external results (may be used without proof)"
SECTION4_HEADING = "## 4. Definitions"
SECTION6_HEADING = "## 6. Target"
EXT_ID_RE = re.compile(r"\*\*\[(R\d+)\]\*\*", re.IGNORECASE)
SOURCE_LINE_RE = re.compile(r"\A\s*Source:\s*([^\n]+)", re.IGNORECASE)
VAGUE_SOURCE_RE = re.compile(
    r"^(?:none|unknown|unclear|tbd|citation needed|standard result|"
    r"standard theorem|textbook result)\.?$",
    re.IGNORECASE,
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_target_section(*, statement_tex: str) -> str:
    """Render Section 6 from the frozen text, without inferred metadata."""

    if not statement_tex:
        raise ValueError("target statement is empty")
    return f"{SECTION6_HEADING}\n\n**Target statement.**\n\n{statement_tex}\n"


def canonicalize_target_section(
    body: str,
    *,
    statement_tex: str,
) -> str:
    """Delete any model-written Section 6 and append the frozen target."""

    start = body.find(SECTION6_HEADING)
    prefix = (body[:start] if start >= 0 else body).rstrip()
    target = canonical_target_section(statement_tex=statement_tex)
    return f"{prefix}\n\n{target}" if prefix else target


def target_identity_issues(
    body: str,
    *,
    statement_tex: str,
    statement_sha256: str,
) -> list[dict]:
    """Report an invalid frozen hash or any Section 6 target drift."""

    start = body.find(SECTION6_HEADING)
    prefix = body[:start] if start >= 0 else body
    norm_target = re.sub(r"\s+", " ", statement_tex).strip()
    norm_prefix = re.sub(r"\s+", " ", prefix)
    expected = canonical_target_section(statement_tex=statement_tex)
    actual = body[start:] if start >= 0 else ""
    hash_ok = bool(statement_sha256) and \
        sha256_text(statement_tex) == statement_sha256
    duplicated = bool(norm_target and norm_target in norm_prefix)
    if hash_ok and not duplicated and actual.strip() == expected.strip():
        return []
    return [{
        "kind": "other",
        "quote": actual.strip()[:300] or "Section 6 is missing",
        "explanation": (
            "The target is duplicated outside Section 6, its frozen hash is "
            "invalid, or Section 6 does not exactly match the source-backed "
            "target recorded in statements.v2.json"
        ),
        "severity": "fatal",
        "fix_hint": "restore Section 6 and target artifacts from the verified source slice",
    }]


def statement_source_issues(
    *,
    added_by: str,
    source_verified: bool,
    source_file: str,
    source_start: int,
    source_end: int,
    source_sha256: str,
    statement_tex: str,
    statement_sha256: str,
    flat_source: str,
    expected_source_file: str,
) -> list[str]:
    """Return reasons a target is not deterministically source-backed."""

    issues: list[str] = []
    if added_by != "parser":
        issues.append("statement was introduced by a model")
    if not source_verified:
        issues.append("statement is not marked source-verified")
    if source_file != expected_source_file:
        issues.append("statement source file does not match the paper source")
    if not (0 <= source_start < source_end <= len(flat_source)):
        issues.append("statement source span is invalid")
        source_slice = ""
    else:
        source_slice = flat_source[source_start:source_end]
    if not statement_sha256 or sha256_text(statement_tex) != statement_sha256:
        issues.append("statement text does not match its recorded hash")
    if not source_sha256 or (source_slice and sha256_text(source_slice) != source_sha256):
        issues.append("source slice does not match its recorded hash")
    if source_slice and statement_tex not in source_slice:
        issues.append("statement text is not an exact substring of its source slice")
    return issues


PROOF_PAIRING_METHODS = frozenset({
    "explicit-label", "explicit-heading-label", "adjacent",
    "explicit-label-recovery",
})


def proof_source_issues(
    *,
    proof_tex: str,
    proof_sha256: str,
    proof_source_file: str,
    proof_source_start: int,
    proof_source_end: int,
    proof_source_sha256: str,
    proof_source_verified: bool,
    proof_pairing: str,
    flat_source: str,
    expected_source_file: str,
) -> list[str]:
    """Return reasons a private reference proof is not source-authenticated."""

    issues: list[str] = []
    if not proof_tex:
        issues.append("proof text is missing")
    if not proof_source_verified:
        issues.append("proof is not marked source-verified")
    if proof_pairing not in PROOF_PAIRING_METHODS:
        issues.append("proof lacks an approved deterministic pairing method")
    if proof_source_file != expected_source_file:
        issues.append("proof source file does not match the paper source")
    if not (0 <= proof_source_start < proof_source_end <= len(flat_source)):
        issues.append("proof source span is invalid")
        source_slice = ""
    else:
        source_slice = flat_source[proof_source_start:proof_source_end]
    if not proof_sha256 or sha256_text(proof_tex) != proof_sha256:
        issues.append("proof text does not match its recorded hash")
    if not proof_source_sha256 or (
        source_slice and sha256_text(source_slice) != proof_source_sha256
    ):
        issues.append("proof source slice does not match its recorded hash")
    if source_slice and proof_tex not in source_slice:
        issues.append("proof text is not an exact substring of its source slice")
    return issues


def frozen_target_record(**fields: Any) -> dict[str, Any]:
    """Select the immutable target fields stored beside ``target.tex``."""

    keys = (
        "target_id", "statement_sha256", "source_file", "source_start",
        "source_end", "source_sha256", "proof_sha256", "proof_source_file",
        "proof_source_start", "proof_source_end", "proof_source_sha256",
        "proof_source_verified", "proof_pairing",
    )
    return {key: fields[key] for key in keys}


def frozen_target_artifact_issues(
    *,
    target_tex: str,
    statement_tex: str,
    record: dict[str, Any],
    expected_record: dict[str, Any],
) -> list[str]:
    issues: list[str] = []
    if target_tex != statement_tex:
        issues.append("target.tex does not exactly match the indexed target")
    if not isinstance(record, dict):
        issues.append("target.json must contain a JSON object")
    elif record != expected_record:
        missing = sorted(set(expected_record) - set(record))
        extra = sorted(set(record) - set(expected_record))
        if missing:
            issues.append("target.json is missing fields: " + ", ".join(missing))
        if extra:
            issues.append("target.json has unexpected fields: " + ", ".join(extra))
        for key in sorted(set(expected_record) & set(record)):
            if record[key] != expected_record[key]:
                issues.append(f"target.json field {key} does not match the index")
    return issues


def section3_source_issues(body: str, citation_keys: list[str]) -> list[dict]:
    """Reject grants without a bibliography key or complete named source."""

    start = body.find(SECTION3_HEADING)
    end = body.find(SECTION4_HEADING, start + len(SECTION3_HEADING))
    if start < 0 or end < 0:
        return []  # the stage-2 structure check reports malformed boundaries
    section3 = body[start + len(SECTION3_HEADING):end]
    grants = list(EXT_ID_RE.finditer(section3))
    issues = []
    seen: set[str] = set()
    keys = [key.strip() for key in citation_keys if key.strip()]
    for position, grant in enumerate(grants):
        grant_id = grant.group(1).upper()
        block_end = (
            grants[position + 1].start()
            if position + 1 < len(grants)
            else len(section3)
        )
        source_match = SOURCE_LINE_RE.match(section3[grant.end():block_end])
        source = source_match.group(1).strip() if source_match else ""
        if grant_id in seen:
            issues.append({
                "kind": "other",
                "quote": f"**[{grant_id}]**",
                "explanation": "duplicate Section 3 external-grant identifier",
                "severity": "fatal",
                "fix_hint": "renumber Section 3 grants so each [Rn] occurs exactly once",
            })
        seen.add(grant_id)
        source_words = re.findall(r"[A-Za-z][A-Za-z'-]+", source)
        cites_known_key = any(
            re.search(
                rf"(?<![A-Za-z0-9_-]){re.escape(key)}(?![A-Za-z0-9_-])",
                source,
            )
            for key in keys
        )
        names_author_and_title = (
            len(source_words) >= 3
            and any(separator in source for separator in (",", ":", ";", " - "))
        )
        if (
            not source
            or VAGUE_SOURCE_RE.fullmatch(source)
            or not (cites_known_key or names_author_and_title)
        ):
            issues.append({
                "kind": "other",
                "quote": f"**[{grant_id}]**",
                "explanation": (
                    "Section 3 grant lacks an immediate bibliography key or named "
                    "external source"
                ),
                "severity": "fatal",
                "fix_hint": (
                    "write 'Source: <bibliography key or author and title>' "
                    f"immediately after **[{grant_id}]**"
                ),
            })
    return issues
