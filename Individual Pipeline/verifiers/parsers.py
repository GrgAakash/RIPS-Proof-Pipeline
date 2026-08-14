"""Parsers for Prompt Packet-style verifier outputs."""

from __future__ import annotations

import re

from verifiers.schemas import AReport, Agreement, BReport, CReport, ComposerAReport, DerivedAStatus, TriState


PUNCTUATION_FREE_VALUES = {
    "yes.",
    "no.",
    "unclear.",
    "none.",
    "unsure.",
    "not applicable.",
    "inside key step.",
    "outside key step.",
    "blueprint.",
    "s1-s5.",
    "no key step.",
}


def parse_a_report(raw_text: str, *, run_id: str, skeleton_ref: str) -> AReport:
    return AReport(
        run_id=run_id,
        skeleton_ref=skeleton_ref,
        raw_text=raw_text,
        non_fillable_gaps_present=_tri(_last_value(raw_text, "Non-fillable gaps present?")),
        fillable_only_gaps_present=_tri(_last_value(raw_text, "Fillable-only gaps present?")),
        disallowed_premises_present=_tri(_last_value(raw_text, "Disallowed premises present?")),
        omitted_case_or_weaker_statement_present=_tri(_last_value(raw_text, "Omitted case / weaker statement present?")),
        allowed_formal_skeleton_statements_used=_last_value(raw_text, "Allowed formal skeleton statements used beyond definitions:"),
        disallowed_skeleton_statements_cited=_last_value(raw_text, "Disallowed skeleton statements cited:"),
        standard_background_heavy=_tri(_last_value(raw_text, "Standard-background-heavy?")),
        web_source_issue=_tri(_last_value(raw_text, "Web-source issue?")),
        candidate_guidance_seed=_seed(_last_value(raw_text, "Candidate guidance seed, if any:")),
    )


def parse_composer_a_report(raw_text: str, *, skeleton_ref: str) -> ComposerAReport:
    allowed_raw = _last_value(raw_text, "Allowed formal skeleton statements used beyond definitions:")
    disallowed_raw = _last_value(raw_text, "Disallowed skeleton statements cited:")
    return ComposerAReport(
        skeleton_ref=skeleton_ref,
        raw_text=raw_text,
        non_fillable_gaps_present=_tri(_last_value(raw_text, "Non-fillable gaps present?")),
        fillable_only_gaps_present=_tri(_last_value(raw_text, "Fillable-only gaps present?")),
        disallowed_premises_present=_tri(_last_value(raw_text, "Disallowed premises present?")),
        omitted_case_or_weaker_statement_present=_tri(_last_value(raw_text, "Omitted case / weaker statement present?")),
        allowed_formal_skeleton_statements_used=allowed_raw,
        allowed_formal_skeleton_statements_used_count=_coupling_count(allowed_raw),
        allowed_formal_skeleton_statements_used_list=_coupling_list(allowed_raw),
        disallowed_skeleton_statements_cited=disallowed_raw,
        disallowed_skeleton_statements_cited_count=_coupling_count(disallowed_raw),
        disallowed_skeleton_statements_cited_list=_coupling_list(disallowed_raw),
        standard_background_heavy=_tri(_last_value(raw_text, "Standard-background-heavy?")),
        web_source_issue=_tri(_last_value(raw_text, "Web-source issue?")),
        same_issue_recurring_across_reports=_tri(_last_value(raw_text, "Same issue recurring across reports?")),
        candidate_guidance_seed=_seed(_last_value(raw_text, "Candidate guidance seed, if any:")),
        implied_status_agreement=_agreement(raw_text),
    )


def parse_b_report(raw_text: str, *, skeleton_ref: str) -> BReport:
    return BReport(
        skeleton_ref=skeleton_ref,
        raw_text=raw_text,
        weakest_point_found=_yes_no_unclear(_last_value(raw_text, "Weakest point found?")),
        weakest_point=_last_value(raw_text, "Weakest point (step + claim, or \"None\"):"),
        fillable=_fillable(_last_value(raw_text, "Fillable:")),
        weakest_point_location=_last_value(raw_text, "Weakest point location"),
        source_status=_last_value(raw_text, "Source status:"),
        missing_claim=_last_value(raw_text, "Missing claim, or \"None\":"),
        disallowed_premise_at_weakest_point=_yes_no_na(_last_value(raw_text, "Disallowed premise at the weakest point?")),
        web_source_issue=_web_source_issue(raw_text),
    )


def parse_c_report(raw_text: str, *, skeleton_ref: str) -> CReport:
    return CReport(
        skeleton_ref=skeleton_ref,
        raw_text=raw_text,
        most_serious_attack=_last_value(raw_text, "Most serious attack (step + claim):"),
        attack_location=_last_value(raw_text, "Attack location"),
        source_status=_last_value(raw_text, "Source status:"),
        broke=_broke(_last_value(raw_text, "Broke:")),
        failing_step=_last_value(raw_text, "If broke, the false claim or failing step:"),
        exact_check_needed=_last_value(raw_text, "If unsure, exact check needed to decide:"),
        disallowed_premise_at_attacked_point=_yes_no_unclear(_last_value(raw_text, "Disallowed premise at the attacked point?")),
        web_source_issue=_web_source_issue(raw_text),
    )


def derive_a_status(report: ComposerAReport) -> DerivedAStatus:
    demonstrably_false = getattr(report, "demonstrably_false_step", "UNCLEAR")
    if report.disallowed_premises_present == "YES" or demonstrably_false == "YES":
        return "A_INVALID"
    if report.non_fillable_gaps_present == "YES" or report.omitted_case_or_weaker_statement_present == "YES":
        return "A_NOT_VERIFIED"
    if (
        report.fillable_only_gaps_present == "YES"
        and report.disallowed_premises_present == "NO"
        and report.non_fillable_gaps_present == "NO"
        and report.omitted_case_or_weaker_statement_present == "NO"
    ):
        return "A_ALMOST"
    if (
        report.non_fillable_gaps_present == "NO"
        and report.fillable_only_gaps_present == "NO"
        and report.disallowed_premises_present == "NO"
        and report.omitted_case_or_weaker_statement_present == "NO"
    ):
        return "A_VERIFIED"
    return "A_UNCLEAR"


def has_clear_seed(seed: str | None) -> bool:
    return bool(seed and _seed(seed) != "None")


def _last_value(text: str, label: str) -> str:
    pattern = re.compile(rf"(?im)^\s*(?:[-*]\s*)?{_label_regex(label)}\s*(.*)$")
    matches = list(pattern.finditer(text))
    if not matches:
        return ""
    value = _strip_option_prefix(matches[-1].group(1).strip())
    if not value:
        return ""
    return _clean_value(value)


def _label_regex(label: str) -> str:
    label = label.strip()
    marker = r"[*_`]+"
    if label and label[-1] in {":", "?"}:
        core = re.escape(label[:-1].strip())
        punctuation = re.escape(label[-1])
        return rf"(?:{marker})?{core}(?:{marker})?\s*{punctuation}(?:{marker})?"
    return rf"(?:{marker})?{re.escape(label)}(?:{marker})?"


def _strip_option_prefix(value: str) -> str:
    value = value.strip()
    if value.startswith("("):
        end = value.find("):")
        if end >= 0:
            return value[end + 2 :].strip()
    if value.startswith(":"):
        return value[1:].strip()
    return value


def _clean_value(value: str) -> str:
    value = value.strip()
    value = re.sub(r"^[*_`\s]+|[*_`\s]+$", "", value)
    value = value.strip()
    value = re.sub(r"\s+", " ", value)
    if value.endswith(".") and value.lower() in PUNCTUATION_FREE_VALUES:
        value = value[:-1]
    return value.strip()


def _tri(value: str) -> TriState:
    normalized = _clean_value(value).lower().rstrip(".")
    if normalized.startswith("yes"):
        return "YES"
    if normalized.startswith("no"):
        return "NO"
    if normalized.startswith("unclear"):
        return "UNCLEAR"
    return "UNCLEAR"


def _seed(value: str) -> str:
    cleaned = _clean_value(value)
    if not cleaned:
        return "None"
    lowered = cleaned.lower().strip(" .")
    if lowered in {"none", "n/a", "not applicable"}:
        return "None"
    if lowered.startswith("[one standalone"):
        return "None"
    return cleaned


def _agreement(text: str) -> Agreement:
    lines = [
        line
        for line in text.splitlines()
        if (
            "implied status agreement" in line.lower()
            or ("controller" in line.lower() and ("agree" in line.lower() or "majority" in line.lower()))
        )
    ]
    haystack = _clean_value(lines[-1]) if lines else _clean_value(text)
    lowered = haystack.lower()
    if "no majority" in lowered:
        return "no_majority"
    if "majority agree" in lowered:
        return "majority_agree"
    if "not all agree" in lowered:
        return "unclear"
    if "all agree" in lowered:
        return "all_agree"
    return "unclear"


def _yes_no_unclear(value: str) -> str:
    normalized = _clean_value(value).lower().rstrip(".")
    if normalized.startswith("yes"):
        return "yes"
    if normalized.startswith("no"):
        return "no"
    if normalized.startswith("unclear"):
        return "unclear"
    return "unclear"


def _yes_no_na(value: str) -> str:
    normalized = _clean_value(value).lower().rstrip(".")
    if normalized.startswith("not applicable") or normalized in {"n/a", "na"}:
        return "not applicable"
    if normalized.startswith("yes"):
        return "yes"
    if normalized.startswith("no"):
        return "no"
    return "unclear"


def _fillable(value: str) -> str:
    normalized = _clean_value(value).lower().rstrip(".")
    if normalized.startswith("not applicable") or normalized in {"n/a", "na"}:
        return "not applicable"
    if normalized.startswith("yes"):
        return "yes"
    if normalized.startswith("no"):
        return "no"
    return "unclear"


def _broke(value: str) -> str:
    normalized = _clean_value(value).lower().rstrip(".")
    if normalized.startswith("yes"):
        return "yes"
    if normalized.startswith("no"):
        return "no"
    if normalized.startswith("unsure"):
        return "unsure"
    return "unclear"


def _web_source_issue(text: str) -> TriState:
    explicit = _last_value(text, "Web-source issue?")
    if explicit:
        return _tri(explicit)
    lines = [line.strip().lower() for line in text.splitlines() if "web" in line.lower()]
    haystack = " ".join(lines)
    if not haystack:
        return "UNCLEAR"
    if "no web sources used" in haystack or "no web source" in haystack:
        return "NO"
    if any(term in haystack for term in ("web lookup", "web search", "internet", "browser", "url", "http")):
        return "YES"
    return "UNCLEAR"


def _coupling_count(value: str) -> int | None:
    match = re.search(r"(?:\[\s*)?(\d+)\s*\+\s*\[", value)
    if match:
        return int(match.group(1))
    return None


def _coupling_list(value: str) -> list[str]:
    match = re.search(r"(?:\[\s*)?\d+\s*\+\s*\[(.*?)\]\s*\]?", value)
    if not match:
        return []
    content = match.group(1).strip()
    if not content:
        return []
    return [item.strip().strip("'\"") for item in content.split(",") if item.strip()]
