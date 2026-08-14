"""Restricted-web source gate for cleaner-generated Section 3 grants."""

from __future__ import annotations

import json
import re
import textwrap
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

from solver.packet import PromptPacket


GENERATOR_ROLE = "skeleton_source_generator"
VERIFIER_ROLE = "skeleton_source_verifier"
INTERNET_ROLES = frozenset({GENERATOR_ROLE, VERIFIER_ROLE})

_ANCHORS = {
    GENERATOR_ROLE: "You are the Skeleton Source Generator.",
    VERIFIER_ROLE: "You are the Skeleton Source Verifier.",
}
_REQUIRED = {
    GENERATOR_ROLE: (
        "[PASTE TARGET THEOREM]",
        "[PASTE SECTION 3 EXTERNAL GRANTS]",
        '[PASTE BIBLIOGRAPHY / .BIB / .BBL, OR WRITE "None"]',
    ),
    VERIFIER_ROLE: (
        "[PASTE TARGET THEOREM]",
        "[PASTE SECTION 3 EXTERNAL GRANTS]",
        "[PASTE SKELETON SOURCE LEDGER]",
        '[PASTE BIBLIOGRAPHY / .BIB / .BBL, OR WRITE "None"]',
    ),
}
_DIVIDER_RE = re.compile(r"(?m)^(?:={16,}|-{16,})\s*$")
_INPUTS_MARKER = "--- INPUTS FOR THIS RUN ---"
_GRANT_RE = re.compile(r"\*\*\[(R\d+)\]\*\*", re.IGNORECASE)
_GRANT_LINE_RE = re.compile(r"(?mi)^\s*grant_id\s*:\s*(R\d+)\s*$")
_YAML_RE = re.compile(
    r"^[ \t]*```(?:yaml|yml)[ \t]*\r?\n(.*?)^[ \t]*```[ \t]*$",
    re.IGNORECASE | re.DOTALL | re.MULTILINE,
)
_YAML_FIELD_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_ -]*):(?:\s*(.*))?$")


class SkeletonSourceGateError(RuntimeError):
    """Raised when source-gate inputs or prompt templates are invalid."""


@dataclass(frozen=True)
class SkeletonSourceGateDecision:
    gate_result: str
    reason: str
    expected_grant_ids: list[str]
    generator_grant_ids: list[str]
    verifier_grant_ids: list[str]
    verifier_ran: bool
    generator_summary: dict[str, str]
    verifier_summary: dict[str, str] | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class SkeletonSourcePromptTemplates:
    prompts: dict[str, str]

    @classmethod
    def from_file(cls, path: str | Path) -> "SkeletonSourcePromptTemplates":
        packet_path = Path(path)
        if not packet_path.exists():
            raise SkeletonSourceGateError(f"prompt packet does not exist: {packet_path}")
        text = packet_path.read_text(encoding="utf-8")
        prompts = {
            role: _extract_prompt(text, role, anchor)
            for role, anchor in _ANCHORS.items()
        }
        return cls(prompts)

    def build_generator(self, target: str, section3: str, bibliography: str) -> PromptPacket:
        return self._build(
            GENERATOR_ROLE,
            {
                "[PASTE TARGET THEOREM]": target,
                "[PASTE SECTION 3 EXTERNAL GRANTS]": section3,
                '[PASTE BIBLIOGRAPHY / .BIB / .BBL, OR WRITE "None"]': bibliography or "None",
            },
        )

    def build_verifier(
        self,
        target: str,
        section3: str,
        bibliography: str,
        ledger: str,
    ) -> PromptPacket:
        return self._build(
            VERIFIER_ROLE,
            {
                "[PASTE TARGET THEOREM]": target,
                "[PASTE SECTION 3 EXTERNAL GRANTS]": section3,
                "[PASTE SKELETON SOURCE LEDGER]": ledger,
                '[PASTE BIBLIOGRAPHY / .BIB / .BBL, OR WRITE "None"]': bibliography or "None",
            },
        )

    def _build(self, role: str, replacements: dict[str, str]) -> PromptPacket:
        text = self.prompts[role]
        for placeholder, value in replacements.items():
            if placeholder not in text:
                raise SkeletonSourceGateError(f"{role}: missing placeholder {placeholder}")
            text = text.replace(placeholder, value)
        system, marker, user = text.partition(_INPUTS_MARKER)
        if not marker:
            raise SkeletonSourceGateError(f"{role}: missing {_INPUTS_MARKER!r}")
        return PromptPacket(role=role, system=system.strip(), user=user.strip())


class MockSkeletonSourceClient:
    """Deterministic source-gate client used by offline integration tests."""

    model = "mock-skeleton-source"

    def __init__(self, scenario: str = "all_supported") -> None:
        self.scenario = scenario
        self.calls: list[str] = []

    def complete(self, prompt: PromptPacket, metadata: dict):
        from solver.llm import LLMResponse

        self.calls.append(prompt.role)
        ids = re.findall(r"expected_grant_id:\s*(R\d+)", prompt.user)
        if self.scenario == "leakage":
            gate = "LEAKAGE_RISK"
            leakage = "YES"
        elif self.scenario == "unsupported":
            gate = "BLOCKING_SOURCE_ISSUE"
            leakage = "NO"
        else:
            gate = "GOOD_TO_GO"
            leakage = "NO"
        if prompt.role == GENERATOR_ROLE:
            items = "\n\n".join(
                f"grant_id: {grant_id}\n"
                "source_identifier: mock-source-key\n"
                "source_status: VERIFIED\n"
                "exact_statement_checked: YES\n"
                "hypotheses_checked: YES\n"
                "source_location: Theorem 1\n"
                "url_or_reference_checked: https://example.invalid/source\n"
                "notes: deterministic mock"
                for grant_id in ids
            )
        else:
            items = "\n\n".join(
                f"grant_id: {grant_id}\n"
                "verdict: VERIFIED\n"
                "source_identifier: mock-source-key\n"
                "exact_location_checked: Theorem 1\n"
                "explanation: statement and hypotheses match"
                for grant_id in ids
            )
        if prompt.role == GENERATOR_ROLE:
            recommendation = (
                "PROCEED_TO_SKELETON_SOURCE_VERIFIER"
                if gate == "GOOD_TO_GO"
                else gate
            )
            text = f"""{items}

```yaml
recommended_next_step: {recommendation}
possible_target_source_leakage: {leakage}
unsupported_or_unclear_grants: {'NO' if gate == 'GOOD_TO_GO' else 'YES'}
```
"""
        else:
            text = f"""{items}

```yaml
gate_result: {gate}
possible_target_source_leakage: {leakage}
missing_grants: NO
source_location_issues: {'NO' if gate == 'GOOD_TO_GO' else 'YES'}
hypothesis_mismatches: NO
unsupported_or_unclear_grants: {'NO' if gate == 'GOOD_TO_GO' else 'YES'}
```
"""
        return LLMResponse(text=text, model=self.model)


def expected_grant_ids(section3: str) -> list[str]:
    """Return Section 3 grant IDs, rejecting duplicate identifiers."""

    ids = [match.upper() for match in _GRANT_RE.findall(section3)]
    if len(ids) != len(set(ids)):
        raise SkeletonSourceGateError("Section 3 contains duplicate [Rn] grant IDs")
    return ids


def run_skeleton_source_gate(
    *,
    output_dir: Path,
    target: str,
    section3: str,
    bibliography: str,
    templates: SkeletonSourcePromptTemplates,
    client,
    progress: Callable[[str], None] | None = None,
) -> SkeletonSourceGateDecision:
    """Run the source generator and verifier; only exact GOOD_TO_GO passes."""

    output_dir.mkdir(parents=True, exist_ok=True)
    expected = expected_grant_ids(section3)
    if not expected:
        decision = SkeletonSourceGateDecision(
            gate_result="NOT_APPLICABLE",
            reason="Section 3 contains no external grants.",
            expected_grant_ids=[],
            generator_grant_ids=[],
            verifier_grant_ids=[],
            verifier_ran=False,
            generator_summary={},
        )
        _write_json(output_dir / "skeleton_source_gate_decision.json", decision.to_dict())
        return decision

    annotated_section = _annotate_expected_ids(section3, expected)
    generator_prompt = templates.build_generator(target, annotated_section, bibliography)
    _write_prompt(output_dir / "skeleton_source_generator_prompt.json", generator_prompt)
    _emit(progress, "[skeleton-source] generator start")
    generator = client.complete(generator_prompt, {"role": GENERATOR_ROLE})
    (output_dir / "skeleton_source_generator_output.md").write_text(
        generator.text.rstrip() + "\n", encoding="utf-8"
    )
    generator_items = _reported_items(generator.text)
    generator_ids = [item["grant_id"] for item in generator_items]
    generator_summary = _last_yaml_map(generator.text)
    _write_json(output_dir / "skeleton_source_generator_parsed.json", {
        "items": generator_items,
        "grant_ids": generator_ids,
        "summary": generator_summary,
    })

    early_result = _generator_gate(
        expected, generator_ids, generator_items, generator_summary
    )
    if early_result is not None:
        result, reason = early_result
        decision = SkeletonSourceGateDecision(
            gate_result=result,
            reason=reason,
            expected_grant_ids=expected,
            generator_grant_ids=generator_ids,
            verifier_grant_ids=[],
            verifier_ran=False,
            generator_summary=generator_summary,
        )
        _write_json(output_dir / "skeleton_source_gate_decision.json", decision.to_dict())
        return decision

    verifier_prompt = templates.build_verifier(
        target, annotated_section, bibliography, generator.text
    )
    _write_prompt(output_dir / "skeleton_source_verifier_prompt.json", verifier_prompt)
    _emit(progress, "[skeleton-source] verifier start")
    verifier = client.complete(verifier_prompt, {"role": VERIFIER_ROLE})
    (output_dir / "skeleton_source_verifier_output.md").write_text(
        verifier.text.rstrip() + "\n", encoding="utf-8"
    )
    verifier_items = _reported_items(verifier.text)
    verifier_ids = [item["grant_id"] for item in verifier_items]
    verifier_summary = _last_yaml_map(verifier.text)
    _write_json(output_dir / "skeleton_source_verifier_parsed.json", {
        "items": verifier_items,
        "grant_ids": verifier_ids,
        "summary": verifier_summary,
    })
    result, reason = _verifier_gate(
        expected, verifier_ids, verifier_items, verifier_summary
    )
    decision = SkeletonSourceGateDecision(
        gate_result=result,
        reason=reason,
        expected_grant_ids=expected,
        generator_grant_ids=generator_ids,
        verifier_grant_ids=verifier_ids,
        verifier_ran=True,
        generator_summary=generator_summary,
        verifier_summary=verifier_summary,
    )
    _write_json(output_dir / "skeleton_source_gate_decision.json", decision.to_dict())
    _emit(progress, f"[skeleton-source] done gate={result}")
    return decision


def _extract_prompt(packet: str, role: str, anchor: str) -> str:
    start = packet.find(anchor)
    if start < 0:
        raise SkeletonSourceGateError(f"{role}: prompt anchor not found")
    divider = _DIVIDER_RE.search(packet, start)
    text = packet[start: divider.start() if divider else len(packet)].strip()
    for placeholder in _REQUIRED[role]:
        if placeholder not in text:
            raise SkeletonSourceGateError(f"{role}: required placeholder missing: {placeholder}")
    return text


def _annotate_expected_ids(section3: str, ids: list[str]) -> str:
    labels = "\n".join(f"expected_grant_id: {grant_id}" for grant_id in ids)
    return f"{section3.rstrip()}\n\nController inventory (not source evidence):\n{labels}"


def _reported_items(text: str) -> list[dict[str, str]]:
    """Parse the controller-facing flat fields for each grant item."""

    yaml_matches = list(_YAML_RE.finditer(text))
    report = text[:yaml_matches[-1].start()] if yaml_matches else text
    starts = list(_GRANT_LINE_RE.finditer(report))
    items: list[dict[str, str]] = []
    for index, start in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(report)
        block = report[start.start():end]
        item: dict[str, str] = {"grant_id": start.group(1).upper()}
        current_key = ""
        for line in block.splitlines()[1:]:
            field = _YAML_FIELD_RE.match(line.strip())
            if field is not None:
                current_key = re.sub(
                    r"[^a-z0-9]+", "_", field.group(1).lower()
                ).strip("_")
                item[current_key] = (field.group(2) or "").strip().strip('"\'')
            elif current_key and line.strip():
                item[current_key] = " ".join(
                    part for part in (item[current_key], line.strip()) if part
                )
        items.append(item)
    return items


def _last_yaml_map(text: str) -> dict[str, str]:
    matches = list(_YAML_RE.finditer(text))
    if not matches:
        return {}
    data: dict[str, str] = {}
    for raw in textwrap.dedent(matches[-1].group(1)).splitlines():
        match = _YAML_FIELD_RE.match(raw)
        if match is None:
            continue
        key = re.sub(r"[^a-z0-9]+", "_", match.group(1).lower()).strip("_")
        value = (match.group(2) or "").strip().strip('"\'')
        data[key] = value
    return data


def _same_ids(expected: list[str], reported: list[str]) -> bool:
    return len(reported) == len(expected) and sorted(reported) == sorted(expected)


def _generator_gate(
    expected: list[str],
    reported: list[str],
    items: list[dict[str, str]],
    summary: dict[str, str],
) -> tuple[str, str] | None:
    if not _same_ids(expected, reported):
        return "UNCLEAR", "Generator did not report every Section 3 grant exactly once."
    if summary.get("possible_target_source_leakage", "").upper() == "YES":
        return "LEAKAGE_RISK", "Generator reported possible target-source leakage."
    if summary.get("possible_target_source_leakage", "").upper() != "NO":
        return "UNCLEAR", "Generator did not give a clear leakage decision."
    required = (
        "source_identifier",
        "exact_statement_checked",
        "hypotheses_checked",
        "source_location",
        "url_or_reference_checked",
    )
    if any(
        item.get("source_status", "").upper() != "VERIFIED"
        or any(not item.get(field, "").strip() for field in required)
        for item in items
    ):
        return "BLOCKING_SOURCE_ISSUE", "Generator left a grant or source location unverified."
    if summary.get("unsupported_or_unclear_grants", "").upper() == "YES":
        return "BLOCKING_SOURCE_ISSUE", "Generator reported an unsupported or unclear grant."
    if summary.get("unsupported_or_unclear_grants", "").upper() != "NO":
        return "UNCLEAR", "Generator did not clearly classify unsupported grants."
    recommendation = summary.get("recommended_next_step", "").upper()
    if recommendation == "PROCEED_TO_SKELETON_SOURCE_VERIFIER":
        return None
    if recommendation in {"SOURCE_LEDGER_REPAIR_NEEDED", "BLOCKING_SOURCE_ISSUE", "LEAKAGE_RISK"}:
        return recommendation, "Generator did not approve the source ledger."
    return "UNCLEAR", "Generator summary was missing or malformed."


def _verifier_gate(
    expected: list[str],
    reported: list[str],
    items: list[dict[str, str]],
    summary: dict[str, str],
) -> tuple[str, str]:
    if not _same_ids(expected, reported):
        return "UNCLEAR", "Verifier did not report every Section 3 grant exactly once."
    if summary.get("possible_target_source_leakage", "").upper() == "YES":
        return "LEAKAGE_RISK", "Verifier reported possible target-source leakage."
    if summary.get("possible_target_source_leakage", "").upper() != "NO":
        return "UNCLEAR", "Verifier did not give a clear leakage decision."
    required = ("source_identifier", "exact_location_checked", "explanation")
    if any(
        item.get("verdict", "").upper() != "VERIFIED"
        or any(not item.get(field, "").strip() for field in required)
        for item in items
    ):
        return "BLOCKING_SOURCE_ISSUE", "Verifier did not verify every grant at an exact location."
    gate = summary.get("gate_result", "").upper()
    issue_fields = (
        "missing_grants",
        "source_location_issues",
        "hypothesis_mismatches",
        "unsupported_or_unclear_grants",
    )
    issue_values = [summary.get(field, "").upper() for field in issue_fields]
    if any(value == "YES" for value in issue_values):
        return "BLOCKING_SOURCE_ISSUE", "Verifier reported a blocking grant or source issue."
    if any(value != "NO" for value in issue_values):
        return "UNCLEAR", "Verifier issue summary was missing or malformed."
    if gate == "GOOD_TO_GO":
        return "GOOD_TO_GO", "Every Section 3 grant was source-verified."
    if gate in {
        "SOURCE_LEDGER_REPAIR_NEEDED",
        "BLOCKING_SOURCE_ISSUE",
        "LEAKAGE_RISK",
        "UNCLEAR",
    }:
        return gate, "Verifier did not approve every Section 3 grant."
    return "UNCLEAR", "Verifier summary was missing, contradictory, or malformed."


def _write_prompt(path: Path, prompt: PromptPacket) -> None:
    _write_json(path, {"role": prompt.role, "system": prompt.system, "user": prompt.user})


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _emit(progress: Callable[[str], None] | None, message: str) -> None:
    if progress is not None:
        progress(message)
