"""Citation Generator -> Citation Verifier gate controller."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from .models import CitationGateDecision, CitationGeneratorReport, CitationVerifierReport, PromptPacket
from .parsers import parse_citation_generator_report, parse_citation_verifier_report
from .prompts import (
    DEFAULT_PACKET_PATH,
    CitationPromptTemplates,
    build_citation_generator_prompt,
    build_citation_reformat_prompt,
    build_citation_verifier_prompt,
)


def decide_after_generator(report: CitationGeneratorReport) -> CitationGateDecision | None:
    """Return a terminal decision after the generator, or None to run verifier."""

    if report.possible_target_source_leakage == "YES":
        return CitationGateDecision(
            "LEAKAGE_RISK",
            "Citation Generator reported possible target-source leakage.",
            False,
            None,
            report,
        )
    if report.parse_status != "OK":
        return CitationGateDecision(
            "UNCLEAR",
            "Citation Generator summary was missing required fields.",
            False,
            None,
            report,
        )
    if report.recommended_next_step == "MANUAL_REVIEW_FOR_LEAKAGE":
        return CitationGateDecision(
            "UNCLEAR",
            "Citation Generator requested leakage review without reporting positive leakage.",
            False,
            None,
            report,
        )
    if report.recommended_next_step == "SOURCE_LEDGER_REPAIR_NEEDED":
        return CitationGateDecision(
            "SOURCE_LEDGER_REPAIR_NEEDED",
            "Citation Generator requested source-ledger repair.",
            False,
            None,
            report,
        )
    if report.recommended_next_step != "PROCEED_TO_CITATION_VERIFIER":
        return CitationGateDecision(
            "UNCLEAR",
            "Citation Generator summary could not be parsed into a safe next step.",
            False,
            None,
            report,
        )
    return None


def decide_after_verifier(
    generator_report: CitationGeneratorReport, verifier_report: CitationVerifierReport
) -> CitationGateDecision:
    """Produce the final citation gate decision."""

    gate = verifier_report.citation_gate_result if verifier_report.parse_status == "OK" else "UNCLEAR"
    reason_by_gate = {
        "GOOD_TO_GO": "Citation Verifier returned GOOD_TO_GO.",
        "SOURCE_LEDGER_REPAIR_NEEDED": "Citation Verifier requested source-ledger repair.",
        "BLOCKING_SOURCE_ISSUE": "Citation Verifier found a substantive blocking source issue.",
        "LEAKAGE_RISK": "Citation Verifier reported leakage risk.",
        "UNCLEAR": "Citation Verifier result was unclear or malformed.",
    }
    guidance = verifier_report.candidate_guidance_seed
    if guidance.strip().lower() == "none":
        guidance = None
    return CitationGateDecision(
        gate,
        reason_by_gate.get(gate, reason_by_gate["UNCLEAR"]),
        True,
        guidance,
        generator_report,
        verifier_report,
    )


def run_citation_gate(
    *,
    output_dir: Path,
    target_theorem: str,
    provided_packet: str,
    allowed_supporting_statements: str,
    guidance: str,
    proof: str,
    solver_source_ledger: str,
    client,
    bibliography: str = "None",
    prompt_templates: CitationPromptTemplates | None = None,
    metadata: dict | None = None,
    progress: Callable[[str], None] | None = None,
) -> CitationGateDecision:
    """Run Citation Generator then Citation Verifier as a persisted gate."""

    output_dir.mkdir(parents=True, exist_ok=True)
    base_metadata = dict(metadata or {})
    prompt_templates = prompt_templates or CitationPromptTemplates.from_file(
        DEFAULT_PACKET_PATH
    )

    generator_prompt = build_citation_generator_prompt(
        target_theorem=target_theorem,
        provided_packet=provided_packet,
        allowed_supporting_statements=allowed_supporting_statements,
        guidance=guidance,
        proof=proof,
        solver_source_ledger=solver_source_ledger,
        bibliography=bibliography,
        prompt_templates=prompt_templates,
    )
    _write_prompt(output_dir / "citation_generator_prompt.json", generator_prompt)
    _emit(progress, "[citation] generator start")
    generator_response = client.complete(generator_prompt, {**base_metadata, "role": "citation_generator", "attempt": 1})
    (output_dir / "citation_generator_output.md").write_text(generator_response.text.rstrip() + "\n", encoding="utf-8")
    generator_report = parse_citation_generator_report(generator_response.text)
    if generator_report.parse_status != "OK":
        generator_report = _retry_generator_reformat(output_dir, generator_response.text, client, base_metadata, progress)
    _write_json(output_dir / "citation_generator_parsed.json", generator_report.to_dict())

    generator_decision = decide_after_generator(generator_report)
    if generator_decision is not None:
        _write_json(output_dir / "citation_gate_decision.json", generator_decision.to_dict())
        _emit(progress, f"[citation] stop gate={generator_decision.gate_result}")
        return generator_decision

    verifier_prompt = build_citation_verifier_prompt(
        target_theorem=target_theorem,
        provided_packet=provided_packet,
        allowed_supporting_statements=allowed_supporting_statements,
        guidance=guidance,
        proof=proof,
        citation_generator_source_ledger=generator_response.text,
        bibliography=bibliography,
        prompt_templates=prompt_templates,
    )
    _write_prompt(output_dir / "citation_verifier_prompt.json", verifier_prompt)
    _emit(progress, "[citation] verifier start")
    verifier_response = client.complete(verifier_prompt, {**base_metadata, "role": "citation_verifier", "attempt": 1})
    (output_dir / "citation_verifier_output.md").write_text(verifier_response.text.rstrip() + "\n", encoding="utf-8")
    verifier_report = parse_citation_verifier_report(verifier_response.text)
    if verifier_report.parse_status != "OK":
        verifier_report = _retry_verifier_reformat(output_dir, verifier_response.text, client, base_metadata, progress)
    _write_json(output_dir / "citation_verifier_parsed.json", verifier_report.to_dict())

    decision = decide_after_verifier(generator_report, verifier_report)
    _write_json(output_dir / "citation_gate_decision.json", decision.to_dict())
    _emit(progress, f"[citation] done gate={decision.gate_result}")
    return decision


def _retry_generator_reformat(
    output_dir: Path,
    previous_response: str,
    client,
    metadata: dict,
    progress: Callable[[str], None] | None,
) -> CitationGeneratorReport:
    required = [
        "Source Ledger complete",
        "Internet used",
        "Possible target-source leakage encountered",
        "Unsupported or unclear sources present",
        "Suspicious standard-background claims present",
        "External sources checked",
        "Recommended next step",
    ]
    prompt = build_citation_reformat_prompt("Citation Generator", required, previous_response)
    _write_prompt(output_dir / "citation_generator_reformat_prompt.json", prompt)
    _emit(progress, "[citation] generator reformat retry")
    response = client.complete(
        prompt,
        {**metadata, "role": "citation_reformat", "reformat_for": "citation_generator", "attempt": 2},
    )
    (output_dir / "citation_generator_reformat_output.md").write_text(response.text.rstrip() + "\n", encoding="utf-8")
    return parse_citation_generator_report(response.text)


def _retry_verifier_reformat(
    output_dir: Path,
    previous_response: str,
    client,
    metadata: dict,
    progress: Callable[[str], None] | None,
) -> CitationVerifierReport:
    required = [
        "Citation gate result",
        "Source Ledger present",
        "Missing source entries present",
        "Disallowed sources present",
        "Overstrengthened or misquoted sources present",
        "Suspicious standard-background claims present",
        "External source issue present",
        "Citation-only repair needed",
        "Substantive source issue present",
        "Candidate guidance seed, if any",
    ]
    prompt = build_citation_reformat_prompt("Citation Verifier", required, previous_response)
    _write_prompt(output_dir / "citation_verifier_reformat_prompt.json", prompt)
    _emit(progress, "[citation] verifier reformat retry")
    response = client.complete(
        prompt,
        {**metadata, "role": "citation_reformat", "reformat_for": "citation_verifier", "attempt": 2},
    )
    (output_dir / "citation_verifier_reformat_output.md").write_text(response.text.rstrip() + "\n", encoding="utf-8")
    return parse_citation_verifier_report(response.text)


def _write_prompt(path: Path, prompt: PromptPacket) -> None:
    _write_json(path, {"role": prompt.role, "system": prompt.system, "user": prompt.user})


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _emit(progress: Callable[[str], None] | None, message: str) -> None:
    if progress is not None:
        progress(message)
