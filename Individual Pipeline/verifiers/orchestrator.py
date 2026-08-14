"""Mock-only orchestrator for the standalone verifier cascade."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from verifiers.guidance_handoff import write_next_guidance_if_applicable
from verifiers.mock import A_RUN_IDS, compose_a_output, make_a_output, make_b_output, make_c_output
from verifiers.parsers import derive_a_status, has_clear_seed, parse_a_report, parse_b_report, parse_c_report, parse_composer_a_report
from verifiers.run_store import make_run_dir, write_inputs, write_parsed, write_raw, write_summary
from verifiers.schemas import BReport, CReport, PipelineSummary, VerifierInput

FRESH_SOLVER_RERUN = "FRESH_MULTI_SOLVER_RUN_FROM_S0"
S0_ENTRYPOINT = "S0_BLUEPRINT"
MATH_GAP_ADJUDICATION = "MATH_GAP_ADJUDICATION"
FINAL_CHECKER_GATE = "FINAL_CHECKER_GATE"
END_CURRENT_CASCADE = "END_CURRENT_VERIFIER_CASCADE"
CASCADE_CLEAR = "CASCADE_CLEAR"
FIX_INPUT_AND_RERUN = "FIX_INPUT_AND_RERUN"
FIX_INPUT = "FIX_INPUT"
VOID_OR_MANUAL_REVIEW = "VOID_OR_MANUAL_REVIEW"
WEB_CONTAMINATION_REVIEW = "WEB_CONTAMINATION_REVIEW"
HUMAN_ADJUDICATION_REQUIRED = "HUMAN_ADJUDICATION_REQUIRED"
COUPLING_PROVENANCE_ADJUDICATION = "COUPLING_PROVENANCE_ADJUDICATION"
CASCADE_CLEAR_WITH_PROVENANCE_BLOCK = "CASCADE_CLEAR_WITH_PROVENANCE_BLOCK"


def run_mock_pipeline(
    inputs: VerifierInput,
    *,
    output_root: str | Path,
    scenario: str = "clean",
    run_id: str | None = None,
) -> PipelineSummary:
    run_id = run_id or _default_run_id(scenario)
    run_dir = make_run_dir(output_root, run_id)
    write_inputs(run_dir, inputs)

    missing = inputs.missing_fields()
    if missing:
        summary = PipelineSummary(
            status="SETUP_FAILURE",
            skeleton_ref=inputs.skeleton_ref,
            stopped_stage="setup",
            protocol_action=FIX_INPUT,
            protocol_next_step=FIX_INPUT_AND_RERUN,
            current_cascade_action="NOT_RUN_SETUP_FAILURE",
            missing_inputs=missing,
        )
        _write_summary_and_handoff(run_dir, summary)
        return summary

    a_reports = []
    for a_run_id in A_RUN_IDS:
        raw = make_a_output(a_run_id, scenario)
        write_raw(run_dir, f"verifier_{a_run_id.lower()}", raw)
        parsed = parse_a_report(raw, run_id=a_run_id, skeleton_ref=inputs.skeleton_ref)
        a_reports.append(parsed)
        write_parsed(run_dir, f"verifier_{a_run_id.lower()}", parsed.to_dict())

    composer_raw = compose_a_output(a_reports)
    write_raw(run_dir, "composer_a", composer_raw)
    composer = parse_composer_a_report(composer_raw, skeleton_ref=inputs.skeleton_ref)
    write_parsed(run_dir, "composer_a", composer.to_dict())
    derived_a_status = derive_a_status(composer)

    summary = _route_after_composer(inputs.skeleton_ref, composer, derived_a_status)
    if summary is not None:
        _write_summary_and_handoff(run_dir, summary)
        return summary

    b_raw = make_b_output(scenario)
    write_raw(run_dir, "verifier_b", b_raw)
    b_report = parse_b_report(b_raw, skeleton_ref=inputs.skeleton_ref)
    write_parsed(run_dir, "verifier_b", b_report.to_dict())
    summary = _route_after_b(inputs.skeleton_ref, b_report, derived_a_status)
    if summary is not None:
        _write_summary_and_handoff(run_dir, summary)
        return summary

    c_raw = make_c_output(scenario)
    write_raw(run_dir, "verifier_c", c_raw)
    c_report = parse_c_report(c_raw, skeleton_ref=inputs.skeleton_ref)
    write_parsed(run_dir, "verifier_c", c_report.to_dict())
    summary = _route_after_c(inputs.skeleton_ref, c_report, derived_a_status, run_metadata=inputs.run_metadata)
    _write_summary_and_handoff(run_dir, summary)
    return summary


def _write_summary_and_handoff(run_dir: Path, summary: PipelineSummary) -> None:
    write_summary(run_dir, summary)
    write_next_guidance_if_applicable(run_dir, summary)


def _route_after_composer(skeleton_ref: str, composer, derived_a_status: str) -> PipelineSummary | None:
    if composer.web_source_issue == "YES":
        return _web_contamination_summary(skeleton_ref, "composer_a", derived_a_status, protocol_source="A")
    if composer.disallowed_premises_present == "YES":
        return PipelineSummary(
            status="STOPPED_DISALLOWED_PREMISE",
            skeleton_ref=skeleton_ref,
            stopped_stage="composer_a",
            derived_a_status=derived_a_status,
            protocol_action="RERUN_SOLVER_WITH_GUIDANCE",
            protocol_source="A",
            protocol_next_step=FRESH_SOLVER_RERUN,
            rerun_starts_at=S0_ENTRYPOINT,
            current_cascade_action=END_CURRENT_CASCADE,
            candidate_guidance_seed=_guidance_from_a_disallowed_premise(composer.candidate_guidance_seed),
        )
    if composer.implied_status_agreement == "no_majority":
        return PipelineSummary(
            status="STOPPED_NO_MAJORITY",
            skeleton_ref=skeleton_ref,
            stopped_stage="composer_a",
            derived_a_status=derived_a_status,
            protocol_action="HUMAN_ADJUDICATION_REQUIRED",
            protocol_source="A",
            protocol_next_step=MATH_GAP_ADJUDICATION,
            current_cascade_action=END_CURRENT_CASCADE,
            candidate_guidance_seed=_none_if_empty(composer.candidate_guidance_seed),
        )
    if derived_a_status in {"A_INVALID", "A_NOT_VERIFIED"} and has_clear_seed(composer.candidate_guidance_seed):
        return PipelineSummary(
            status="STOPPED_GUIDANCE_SEED",
            skeleton_ref=skeleton_ref,
            stopped_stage="composer_a",
            derived_a_status=derived_a_status,
            protocol_action="RERUN_SOLVER_WITH_GUIDANCE",
            protocol_source="A",
            protocol_next_step=FRESH_SOLVER_RERUN,
            rerun_starts_at=S0_ENTRYPOINT,
            current_cascade_action=END_CURRENT_CASCADE,
            candidate_guidance_seed=composer.candidate_guidance_seed,
        )
    return None


def _route_after_b(skeleton_ref: str, b_report: BReport, derived_a_status: str) -> PipelineSummary | None:
    if b_report.web_source_issue == "YES":
        return _web_contamination_summary(
            skeleton_ref,
            "verifier_b",
            derived_a_status,
            protocol_source="B",
            b_ran=True,
        )
    if b_report.disallowed_premise_at_weakest_point == "yes" or (
        b_report.weakest_point_found == "yes" and b_report.fillable == "no"
    ):
        return PipelineSummary(
            status="STOPPED_AFTER_B",
            skeleton_ref=skeleton_ref,
            stopped_stage="verifier_b",
            derived_a_status=derived_a_status,
            protocol_action="RERUN_SOLVER_WITH_GUIDANCE",
            protocol_source="B",
            protocol_next_step=FRESH_SOLVER_RERUN,
            rerun_starts_at=S0_ENTRYPOINT,
            current_cascade_action=END_CURRENT_CASCADE,
            candidate_guidance_seed=_guidance_from_b(b_report),
            b_ran=True,
            c_ran=False,
        )
    return None


def _route_after_c(
    skeleton_ref: str,
    c_report: CReport,
    derived_a_status: str,
    *,
    run_metadata: dict | None = None,
) -> PipelineSummary:
    if c_report.web_source_issue == "YES":
        return _web_contamination_summary(
            skeleton_ref,
            "verifier_c",
            derived_a_status,
            protocol_source="C",
            b_ran=True,
            c_ran=True,
        )
    if c_report.broke == "yes":
        return PipelineSummary(
            status="COMPLETED_C_BROKE",
            skeleton_ref=skeleton_ref,
            stopped_stage="verifier_c",
            derived_a_status=derived_a_status,
            protocol_action="RERUN_SOLVER_WITH_GUIDANCE",
            protocol_source="C",
            protocol_next_step=FRESH_SOLVER_RERUN,
            rerun_starts_at=S0_ENTRYPOINT,
            current_cascade_action=END_CURRENT_CASCADE,
            candidate_guidance_seed=_guidance_from_c(c_report),
            b_ran=True,
            c_ran=True,
        )
    if c_report.broke == "unsure":
        return PipelineSummary(
            status="COMPLETED_C_UNSURE",
            skeleton_ref=skeleton_ref,
            stopped_stage="verifier_c",
            derived_a_status=derived_a_status,
            protocol_action=HUMAN_ADJUDICATION_REQUIRED,
            protocol_source="C",
            protocol_next_step=MATH_GAP_ADJUDICATION,
            current_cascade_action=END_CURRENT_CASCADE,
            candidate_guidance_seed=_none_if_empty(c_report.exact_check_needed),
            b_ran=True,
            c_ran=True,
        )
    if c_report.broke != "no":
        return PipelineSummary(
            status="COMPLETED_C_UNSURE",
            skeleton_ref=skeleton_ref,
            stopped_stage="verifier_c",
            derived_a_status=derived_a_status,
            protocol_action=HUMAN_ADJUDICATION_REQUIRED,
            protocol_source="C",
            protocol_next_step=MATH_GAP_ADJUDICATION,
            current_cascade_action=END_CURRENT_CASCADE,
            b_ran=True,
            c_ran=True,
        )
    if derived_a_status not in {"A_VERIFIED", "A_ALMOST"}:
        return PipelineSummary(
            status="COMPLETED_C_CLEAN",
            skeleton_ref=skeleton_ref,
            stopped_stage="verifier_c",
            derived_a_status=derived_a_status,
            protocol_action=HUMAN_ADJUDICATION_REQUIRED,
            protocol_source="A",
            protocol_next_step=MATH_GAP_ADJUDICATION,
            current_cascade_action=END_CURRENT_CASCADE,
            b_ran=True,
            c_ran=True,
        )
    low_coupling = _route_low_coupling_after_clean_c(skeleton_ref, derived_a_status, run_metadata or {})
    if low_coupling is not None:
        return low_coupling
    return PipelineSummary(
        status="COMPLETED_C_CLEAN",
        skeleton_ref=skeleton_ref,
        stopped_stage="verifier_c",
        derived_a_status=derived_a_status,
        protocol_next_step=FINAL_CHECKER_GATE,
        current_cascade_action=CASCADE_CLEAR,
        b_ran=True,
        c_ran=True,
    )


def _route_low_coupling_after_clean_c(
    skeleton_ref: str,
    derived_a_status: str,
    run_metadata: dict,
) -> PipelineSummary | None:
    tags = run_metadata.get("run_tags", [])
    if isinstance(tags, str):
        tags = [tags]
    if (
        "paper_original_result" in tags
        and run_metadata.get("allowed_proof_skeleton_coupling") == "LOW"
        and derived_a_status in {"A_VERIFIED", "A_ALMOST"}
    ):
        return PipelineSummary(
            status="COMPLETED_C_CLEAN_LOW_COUPLING",
            skeleton_ref=skeleton_ref,
            stopped_stage="verifier_c",
            derived_a_status=derived_a_status,
            protocol_action=HUMAN_ADJUDICATION_REQUIRED,
            protocol_next_step=COUPLING_PROVENANCE_ADJUDICATION,
            current_cascade_action=CASCADE_CLEAR_WITH_PROVENANCE_BLOCK,
            b_ran=True,
            c_ran=True,
        )
    return None


def _web_contamination_summary(
    skeleton_ref: str,
    stopped_stage: str,
    derived_a_status: str,
    *,
    protocol_source: str,
    b_ran: bool = False,
    c_ran: bool = False,
) -> PipelineSummary:
    return PipelineSummary(
        status="STOPPED_WEB_CONTAMINATION",
        skeleton_ref=skeleton_ref,
        stopped_stage=stopped_stage,
        derived_a_status=derived_a_status,
        protocol_action=VOID_OR_MANUAL_REVIEW,
        protocol_source=protocol_source,
        protocol_next_step=WEB_CONTAMINATION_REVIEW,
        current_cascade_action=END_CURRENT_CASCADE,
        b_ran=b_ran,
        c_ran=c_ran,
    )


def _guidance_from_b(b_report: BReport) -> str:
    if _none_if_empty(b_report.missing_claim):
        return b_report.missing_claim
    if b_report.disallowed_premise_at_weakest_point == "yes":
        return "Remove the disallowed premise at Verifier B's weakest point and prove the needed claim from allowed materials."
    if _none_if_empty(b_report.weakest_point_location):
        return f"Repair Verifier B's unfillable weakest point at {b_report.weakest_point_location}."
    return "Repair Verifier B's unfillable weakest point."


def _guidance_from_c(c_report: CReport) -> str:
    if _none_if_empty(c_report.failing_step):
        return c_report.failing_step
    if _none_if_empty(c_report.most_serious_attack):
        return c_report.most_serious_attack
    return "Repair the failing point identified by Verifier C."


def _guidance_from_a_disallowed_premise(seed: str | None) -> str:
    if _none_if_empty(seed):
        return seed.strip()
    return "Remove the disallowed premise and prove the needed claim using only allowed supporting statements."


def _none_if_empty(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned or cleaned.lower().strip(" .") in {"none", "not applicable", "n/a"}:
        return None
    return cleaned


def _default_run_id(scenario: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in scenario)
    return f"mock_{safe}_{stamp}"
