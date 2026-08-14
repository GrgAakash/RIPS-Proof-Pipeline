"""Tolerant Markdown parsers for citation-gate summaries."""

from __future__ import annotations

import re

from .constants import CITATION_GATE_RESULTS, GENERATOR_NEXT_STEPS, YES_NO_UNCLEAR
from .models import CitationGeneratorReport, CitationVerifierReport


def parse_citation_generator_report(text: str) -> CitationGeneratorReport:
    """Parse the Citation Generator's controller-facing Markdown summary."""

    summary = _summary_region(text, ("citation generator summary",))
    missing: list[str] = []
    ledger_complete = _required_choice(summary, "Source Ledger complete", YES_NO_UNCLEAR, missing)
    internet_used = _required_choice(summary, "Internet used", YES_NO_UNCLEAR, missing)
    leakage = _required_choice(summary, "Possible target-source leakage encountered", YES_NO_UNCLEAR, missing)
    unsupported = _required_choice(summary, "Unsupported or unclear sources present", YES_NO_UNCLEAR, missing)
    suspicious = _required_choice(summary, "Suspicious standard-background claims present", YES_NO_UNCLEAR, missing)
    external_sources = _field_value(summary, "External sources checked")
    if external_sources is None:
        missing.append("External sources checked")
        external_sources = "UNCLEAR"
    next_step = _required_choice(summary, "Recommended next step", GENERATOR_NEXT_STEPS, missing)
    return CitationGeneratorReport(
        source_ledger_complete=ledger_complete,
        internet_used=internet_used,
        possible_target_source_leakage=leakage,
        unsupported_or_unclear_sources_present=unsupported,
        suspicious_standard_background_claims_present=suspicious,
        external_sources_checked=external_sources,
        recommended_next_step=next_step,
        parse_status="OK" if not missing else "UNCLEAR",
        missing_fields=missing,
    )


def parse_citation_verifier_report(text: str) -> CitationVerifierReport:
    """Parse the Citation Verifier's controller-facing Markdown summary."""

    summary = _summary_region(text, ("controller facing summary", "citation verifier summary"))
    missing: list[str] = []
    gate = _required_choice(summary, "Citation gate result", CITATION_GATE_RESULTS, missing)
    ledger = _required_choice(summary, "Source Ledger present", YES_NO_UNCLEAR, missing)
    missing_entries = _required_choice(summary, "Missing source entries present", YES_NO_UNCLEAR, missing)
    disallowed = _required_choice(summary, "Disallowed sources present", YES_NO_UNCLEAR, missing)
    overstrengthened = _required_choice(summary, "Overstrengthened or misquoted sources present", YES_NO_UNCLEAR, missing)
    suspicious = _required_choice(summary, "Suspicious standard-background claims present", YES_NO_UNCLEAR, missing)
    external_issue = _required_choice(summary, "External source issue present", YES_NO_UNCLEAR, missing)
    citation_repair = _required_choice(summary, "Citation-only repair needed", YES_NO_UNCLEAR, missing)
    substantive_issue = _required_choice(summary, "Substantive source issue present", YES_NO_UNCLEAR, missing)
    guidance = _field_value(summary, "Candidate guidance seed, if any")
    if guidance is None:
        missing.append("Candidate guidance seed, if any")
        guidance = "None"
    return CitationVerifierReport(
        citation_gate_result=gate,
        source_ledger_present=ledger,
        missing_source_entries_present=missing_entries,
        disallowed_sources_present=disallowed,
        overstrengthened_or_misquoted_sources_present=overstrengthened,
        suspicious_standard_background_claims_present=suspicious,
        external_source_issue_present=external_issue,
        citation_only_repair_needed=citation_repair,
        substantive_source_issue_present=substantive_issue,
        candidate_guidance_seed=guidance,
        parse_status="OK" if not missing else "UNCLEAR",
        missing_fields=missing,
    )


def _summary_region(text: str, markers: tuple[str, ...]) -> str:
    best_start = -1
    for marker in markers:
        words = re.findall(r"[A-Za-z0-9]+", marker)
        pattern = r"\b" + r"[^A-Za-z0-9]+".join(re.escape(word) for word in words) + r"\b"
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            best_start = max(best_start, match.start())
    return text[best_start:] if best_start >= 0 else text


def _required_choice(text: str, label: str, allowed: set[str], missing: list[str]) -> str:
    raw = _field_value(text, label)
    value = _normalize_choice(raw, allowed)
    if raw is None:
        missing.append(label)
    elif value == "UNCLEAR" and _normalize_label(raw) != "unclear":
        missing.append(label)
    return value


def _field_value(text: str, label: str) -> str | None:
    target = _normalize_label(label)
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"\s*(?:[-*]\s*)?([^:]+?)\s*:\s*(.*)$", line)
        if match is None:
            continue
        if _normalize_label(match.group(1)) != target:
            continue
        value = match.group(2).strip()
        if value:
            return value
        for follow in lines[index + 1 :]:
            stripped = follow.strip()
            if stripped:
                return stripped
        return ""
    for line in lines:
        value = _loose_line_value(line, label)
        if value is not None:
            return value
    return None


def _normalize_label(label: str) -> str:
    label = re.sub(r"^\s*(?:[-*]\s*)?(?:\d+[.)]\s*)?", "", label)
    return re.sub(r"[^a-z0-9]+", "", label.lower())


def _loose_line_value(line: str, label: str) -> str | None:
    words = re.findall(r"[A-Za-z0-9]+", label)
    pattern = r"^\s*(?:[-*]\s*)?(?:\d+[.)]\s*)?" + r"[^A-Za-z0-9]+".join(re.escape(word) for word in words)
    match = re.match(pattern, line, flags=re.IGNORECASE)
    if match is None:
        return None
    value = line[match.end() :].strip(" \t:-?[]")
    return value or None


def _normalize_choice(value: str | None, allowed: set[str]) -> str:
    if value is None:
        return "UNCLEAR"
    normalized = re.sub(r"[^A-Z0-9]+", "_", value.upper()).strip("_")
    if normalized in allowed:
        return normalized
    matches = [choice for choice in allowed if choice != "UNCLEAR" and choice in normalized]
    return matches[0] if len(matches) == 1 else "UNCLEAR"
