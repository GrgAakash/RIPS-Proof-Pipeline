"""Single-stage and full-cascade API runners for the verifier subsystem."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from verifiers.api_client import ApiVerifierResult
from verifiers.api_config import ApiConfig, load_api_config
from verifiers.api_runners import ApiCall, run_composer_a_api, run_verifier_a_api, run_verifier_b_api, run_verifier_c_api
from verifiers.guidance_handoff import write_next_guidance_if_applicable
from verifiers.orchestrator import _route_after_b, _route_after_c, _route_after_composer
from verifiers.parsers import derive_a_status, parse_a_report, parse_b_report, parse_c_report, parse_composer_a_report
from verifiers.run_store import make_run_dir, write_inputs, write_json_artifact, write_parsed, write_raw
from verifiers.schemas import VerifierInput


def run_api_a1_smoke(
    inputs: VerifierInput,
    *,
    output_root: str | Path,
    run_id: str | None = None,
    config: ApiConfig | None = None,
    api_call: ApiCall | None = None,
) -> dict:
    return run_api_a_stage_smoke(
        inputs,
        stage="A1",
        output_root=output_root,
        run_id=run_id,
        config=config,
        api_call=api_call,
    )


def run_api_a_stage_smoke(
    inputs: VerifierInput,
    *,
    stage: str,
    output_root: str | Path,
    run_id: str | None = None,
    config: ApiConfig | None = None,
    api_call: ApiCall | None = None,
) -> dict:
    stage = stage.upper()
    if stage not in {"A1", "A2", "A3"}:
        raise ValueError("stage must be one of A1, A2, or A3")

    run_id = run_id or _default_run_id()
    config = config or load_api_config(require_api_key=True)
    run_dir = make_run_dir(output_root, run_id)
    write_inputs(run_dir, inputs)
    write_json_artifact(run_dir / "api_config.json", config.to_public_dict())

    artifact_name = f"verifier_{stage.lower()}"
    missing = inputs.missing_fields()
    if missing:
        summary = {
            "status": f"API_{stage}_SETUP_FAILURE",
            "run_id": run_id,
            "stage": artifact_name,
            "missing_inputs": missing,
            "api_call_made": False,
        }
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    result = run_verifier_a_api(inputs, run_id=stage, config=config, api_call=api_call)
    write_json_artifact(run_dir / "parsed" / f"api_{artifact_name}_call.json", result.to_dict())

    if result.error:
        summary = {
            "status": f"API_{stage}_CALL_FAILED",
            "run_id": run_id,
            "stage": artifact_name,
            "model": result.model,
            "latency_ms": result.latency_ms,
            "api_call_made": not config.dry_run,
            "error": result.error,
        }
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    if not result.raw_text.strip():
        summary = _call_failed_summary(f"API_{stage}_EMPTY_OUTPUT", run_id, artifact_name, result, config)
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    if _is_model_setup_failure(result.raw_text):
        write_raw(run_dir, artifact_name, result.raw_text)
        summary = {
            "status": f"API_{stage}_MODEL_SETUP_FAILURE",
            "run_id": run_id,
            "stage": artifact_name,
            "model": result.model,
            "latency_ms": result.latency_ms,
            "api_call_made": not config.dry_run,
            "protocol_action": "FIX_INPUT",
            "protocol_next_step": "FIX_INPUT_AND_RERUN",
        }
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    write_raw(run_dir, artifact_name, result.raw_text)
    parsed = parse_a_report(result.raw_text, run_id=stage, skeleton_ref=inputs.skeleton_ref)
    write_parsed(run_dir, artifact_name, parsed.to_dict())

    summary = {
        "status": f"API_{stage}_SMOKE_PARSED",
        "run_id": run_id,
        "stage": artifact_name,
        "model": result.model,
        "latency_ms": result.latency_ms,
        "api_call_made": not config.dry_run,
        "parsed_status_fields": {
            "non_fillable_gaps_present": parsed.non_fillable_gaps_present,
            "fillable_only_gaps_present": parsed.fillable_only_gaps_present,
            "disallowed_premises_present": parsed.disallowed_premises_present,
            "omitted_case_or_weaker_statement_present": parsed.omitted_case_or_weaker_statement_present,
            "web_source_issue": parsed.web_source_issue,
        },
    }
    write_json_artifact(run_dir / "summary.json", summary)
    return summary


def run_api_composer_a_smoke(
    *,
    a_reports: dict[str, str],
    skeleton_ref: str,
    output_root: str | Path,
    run_id: str | None = None,
    step_id_map: str = "None",
    config: ApiConfig | None = None,
    api_call: ApiCall | None = None,
) -> dict:
    run_id = run_id or _default_composer_run_id()
    config = config or load_api_config(require_api_key=True)
    run_dir = make_run_dir(output_root, run_id)
    write_json_artifact(run_dir / "api_config.json", config.to_public_dict())
    write_json_artifact(
        run_dir / "inputs.json",
        {
            "skeleton_ref": skeleton_ref,
            "step_id_map": step_id_map,
            "a_report_names": sorted(a_reports),
        },
    )

    missing = [name for name in ("A1", "A2", "A3") if not a_reports.get(name, "").strip()]
    if not skeleton_ref.strip():
        missing.append("skeleton_ref")
    if missing:
        summary = {
            "status": "API_COMPOSER_A_SETUP_FAILURE",
            "run_id": run_id,
            "stage": "composer_a",
            "missing_inputs": missing,
            "api_call_made": False,
        }
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    result = run_composer_a_api(
        a_reports=a_reports,
        step_id_map=step_id_map,
        config=config,
        api_call=api_call,
    )
    write_json_artifact(run_dir / "parsed" / "api_composer_a_call.json", result.to_dict())

    if result.error:
        summary = {
            "status": "API_COMPOSER_A_CALL_FAILED",
            "run_id": run_id,
            "stage": "composer_a",
            "model": result.model,
            "latency_ms": result.latency_ms,
            "api_call_made": not config.dry_run,
            "error": result.error,
        }
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    if not result.raw_text.strip():
        summary = _call_failed_summary("API_COMPOSER_A_EMPTY_OUTPUT", run_id, "composer_a", result, config)
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    if _is_model_setup_failure(result.raw_text):
        write_raw(run_dir, "composer_a", result.raw_text)
        summary = {
            "status": "API_COMPOSER_A_MODEL_SETUP_FAILURE",
            "run_id": run_id,
            "stage": "composer_a",
            "model": result.model,
            "latency_ms": result.latency_ms,
            "api_call_made": not config.dry_run,
            "protocol_action": "FIX_INPUT",
            "protocol_next_step": "FIX_INPUT_AND_RERUN",
        }
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    write_raw(run_dir, "composer_a", result.raw_text)
    parsed = parse_composer_a_report(result.raw_text, skeleton_ref=skeleton_ref)
    write_parsed(run_dir, "composer_a", parsed.to_dict())
    derived_a_status = derive_a_status(parsed)

    summary = {
        "status": "API_COMPOSER_A_SMOKE_PARSED",
        "run_id": run_id,
        "stage": "composer_a",
        "model": result.model,
        "latency_ms": result.latency_ms,
        "api_call_made": not config.dry_run,
        "derived_a_status": derived_a_status,
        "parsed_status_fields": {
            "non_fillable_gaps_present": parsed.non_fillable_gaps_present,
            "fillable_only_gaps_present": parsed.fillable_only_gaps_present,
            "disallowed_premises_present": parsed.disallowed_premises_present,
            "omitted_case_or_weaker_statement_present": parsed.omitted_case_or_weaker_statement_present,
            "web_source_issue": parsed.web_source_issue,
            "implied_status_agreement": parsed.implied_status_agreement,
        },
    }
    route_summary = _route_after_composer(skeleton_ref, parsed, derived_a_status)
    if route_summary is not None:
        route_data = route_summary.to_dict()
        summary.update(
            {
                "cascade_route_status": route_data["status"],
                "stopped_stage": route_data["stopped_stage"],
                "protocol_action": route_data["protocol_action"],
                "protocol_source": route_data["protocol_source"],
                "protocol_next_step": route_data["protocol_next_step"],
                "rerun_starts_at": route_data["rerun_starts_at"],
                "current_cascade_action": route_data["current_cascade_action"],
                "candidate_guidance_seed": route_data["candidate_guidance_seed"],
            }
        )
    write_json_artifact(run_dir / "summary.json", summary)
    write_next_guidance_if_applicable(run_dir, summary)
    return summary


def run_api_b_smoke(
    inputs: VerifierInput,
    *,
    derived_a_status: str,
    output_root: str | Path,
    run_id: str | None = None,
    config: ApiConfig | None = None,
    api_call: ApiCall | None = None,
) -> dict:
    run_id = run_id or _default_b_run_id()
    config = config or load_api_config(require_api_key=True)
    run_dir = make_run_dir(output_root, run_id)
    write_inputs(run_dir, inputs)
    write_json_artifact(run_dir / "api_config.json", config.to_public_dict())

    missing = inputs.missing_fields()
    if missing:
        summary = _setup_failure_summary("API_B_SETUP_FAILURE", run_id, "verifier_b", missing)
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    result = run_verifier_b_api(inputs, config=config, api_call=api_call)
    write_json_artifact(run_dir / "parsed" / "api_verifier_b_call.json", result.to_dict())
    if result.error:
        summary = _call_failed_summary("API_B_CALL_FAILED", run_id, "verifier_b", result, config)
        write_json_artifact(run_dir / "summary.json", summary)
        return summary
    if not result.raw_text.strip():
        summary = _call_failed_summary("API_B_EMPTY_OUTPUT", run_id, "verifier_b", result, config)
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    if _is_model_setup_failure(result.raw_text):
        write_raw(run_dir, "verifier_b", result.raw_text)
        summary = _model_setup_failure_summary("API_B_MODEL_SETUP_FAILURE", run_id, "verifier_b", result, config)
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    write_raw(run_dir, "verifier_b", result.raw_text)
    parsed = parse_b_report(result.raw_text, skeleton_ref=inputs.skeleton_ref)
    write_parsed(run_dir, "verifier_b", parsed.to_dict())
    summary = {
        "status": "API_B_SMOKE_PARSED",
        "run_id": run_id,
        "stage": "verifier_b",
        "model": result.model,
        "latency_ms": result.latency_ms,
        "api_call_made": not config.dry_run,
        "derived_a_status": derived_a_status,
        "parsed_status_fields": {
            "weakest_point_found": parsed.weakest_point_found,
            "fillable": parsed.fillable,
            "disallowed_premise_at_weakest_point": parsed.disallowed_premise_at_weakest_point,
            "web_source_issue": parsed.web_source_issue,
        },
    }
    route_summary = _route_after_b(inputs.skeleton_ref, parsed, derived_a_status)
    if route_summary is None:
        summary["cascade_route_status"] = "CONTINUE_TO_C"
    else:
        summary.update(_route_summary_fields(route_summary))
    write_json_artifact(run_dir / "summary.json", summary)
    write_next_guidance_if_applicable(run_dir, summary)
    return summary


def run_api_c_smoke(
    inputs: VerifierInput,
    *,
    derived_a_status: str,
    output_root: str | Path,
    run_id: str | None = None,
    config: ApiConfig | None = None,
    api_call: ApiCall | None = None,
) -> dict:
    run_id = run_id or _default_c_run_id()
    config = config or load_api_config(require_api_key=True)
    run_dir = make_run_dir(output_root, run_id)
    write_inputs(run_dir, inputs)
    write_json_artifact(run_dir / "api_config.json", config.to_public_dict())

    missing = inputs.missing_fields()
    if missing:
        summary = _setup_failure_summary("API_C_SETUP_FAILURE", run_id, "verifier_c", missing)
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    result = run_verifier_c_api(inputs, config=config, api_call=api_call)
    write_json_artifact(run_dir / "parsed" / "api_verifier_c_call.json", result.to_dict())
    if result.error:
        summary = _call_failed_summary("API_C_CALL_FAILED", run_id, "verifier_c", result, config)
        write_json_artifact(run_dir / "summary.json", summary)
        return summary
    if not result.raw_text.strip():
        summary = _call_failed_summary("API_C_EMPTY_OUTPUT", run_id, "verifier_c", result, config)
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    if _is_model_setup_failure(result.raw_text):
        write_raw(run_dir, "verifier_c", result.raw_text)
        summary = _model_setup_failure_summary("API_C_MODEL_SETUP_FAILURE", run_id, "verifier_c", result, config)
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    write_raw(run_dir, "verifier_c", result.raw_text)
    parsed = parse_c_report(result.raw_text, skeleton_ref=inputs.skeleton_ref)
    write_parsed(run_dir, "verifier_c", parsed.to_dict())
    route_summary = _route_after_c(inputs.skeleton_ref, parsed, derived_a_status)
    summary = {
        "status": "API_C_SMOKE_PARSED",
        "run_id": run_id,
        "stage": "verifier_c",
        "model": result.model,
        "latency_ms": result.latency_ms,
        "api_call_made": not config.dry_run,
        "derived_a_status": derived_a_status,
        "parsed_status_fields": {
            "broke": parsed.broke,
            "disallowed_premise_at_attacked_point": parsed.disallowed_premise_at_attacked_point,
            "web_source_issue": parsed.web_source_issue,
        },
        **_route_summary_fields(route_summary),
    }
    write_json_artifact(run_dir / "summary.json", summary)
    write_next_guidance_if_applicable(run_dir, summary)
    return summary


def run_api_cascade(
    inputs: VerifierInput,
    *,
    output_root: str | Path,
    run_id: str | None = None,
    step_id_map: str = "None",
    config: ApiConfig | None = None,
    api_call: ApiCall | None = None,
) -> dict:
    """Run the verifier-only API cascade as one explicit automation command.

    This still does not run a solver, Final Checker, citation verifier, or full
    Decision Controller. It only drives the A/B/C verifier subpipeline until a
    verifier route says to stop or hand off.
    """

    run_id = run_id or _default_cascade_run_id()
    config = config or load_api_config(require_api_key=True)
    run_dir = make_run_dir(output_root, run_id)
    stage_root = run_dir / "stages"
    write_inputs(run_dir, inputs)
    write_json_artifact(run_dir / "api_config.json", config.to_public_dict())

    missing = inputs.missing_fields()
    if missing:
        summary = {
            "status": "API_CASCADE_SETUP_FAILURE",
            "run_id": run_id,
            "stage": "api_cascade",
            "missing_inputs": missing,
            "api_call_made": False,
            "protocol_action": "FIX_INPUT",
            "protocol_next_step": "FIX_INPUT_AND_RERUN",
            "current_cascade_action": "NOT_RUN_SETUP_FAILURE",
            "stage_summaries": [],
        }
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    stage_summaries: list[dict] = []
    a_reports: dict[str, str] = {}
    for stage in ("A1", "A2", "A3"):
        stage_run_id = stage.lower()
        stage_summary = run_api_a_stage_smoke(
            inputs,
            stage=stage,
            output_root=stage_root,
            run_id=stage_run_id,
            config=config,
            api_call=api_call,
        )
        stage_summaries.append(stage_summary)
        if stage_summary.get("status") != f"API_{stage}_SMOKE_PARSED":
            summary = _cascade_stage_failure_summary(run_id, stage_summary, stage_summaries)
            write_json_artifact(run_dir / "summary.json", summary)
            return summary
        a_reports[stage] = (stage_root / stage_run_id / "raw" / f"verifier_{stage.lower()}.md").read_text(
            encoding="utf-8"
        )

    composer_summary = run_api_composer_a_smoke(
        a_reports=a_reports,
        skeleton_ref=inputs.skeleton_ref,
        step_id_map=step_id_map,
        output_root=stage_root,
        run_id="composer_a",
        config=config,
        api_call=api_call,
    )
    stage_summaries.append(composer_summary)
    if composer_summary.get("status") != "API_COMPOSER_A_SMOKE_PARSED":
        summary = _cascade_stage_failure_summary(run_id, composer_summary, stage_summaries)
        write_json_artifact(run_dir / "summary.json", summary)
        return summary
    if composer_summary.get("cascade_route_status"):
        summary = _cascade_routed_summary(run_id, composer_summary, stage_summaries)
        write_json_artifact(run_dir / "summary.json", summary)
        write_next_guidance_if_applicable(run_dir, summary)
        return summary

    derived_a_status = composer_summary["derived_a_status"]
    b_summary = run_api_b_smoke(
        inputs,
        derived_a_status=derived_a_status,
        output_root=stage_root,
        run_id="verifier_b",
        config=config,
        api_call=api_call,
    )
    stage_summaries.append(b_summary)
    if b_summary.get("status") != "API_B_SMOKE_PARSED":
        summary = _cascade_stage_failure_summary(run_id, b_summary, stage_summaries)
        write_json_artifact(run_dir / "summary.json", summary)
        return summary
    if b_summary.get("cascade_route_status") != "CONTINUE_TO_C":
        summary = _cascade_routed_summary(run_id, b_summary, stage_summaries)
        write_json_artifact(run_dir / "summary.json", summary)
        write_next_guidance_if_applicable(run_dir, summary)
        return summary

    c_summary = run_api_c_smoke(
        inputs,
        derived_a_status=derived_a_status,
        output_root=stage_root,
        run_id="verifier_c",
        config=config,
        api_call=api_call,
    )
    stage_summaries.append(c_summary)
    if c_summary.get("status") != "API_C_SMOKE_PARSED":
        summary = _cascade_stage_failure_summary(run_id, c_summary, stage_summaries)
        write_json_artifact(run_dir / "summary.json", summary)
        return summary

    summary = _cascade_routed_summary(run_id, c_summary, stage_summaries)
    write_json_artifact(run_dir / "summary.json", summary)
    write_next_guidance_if_applicable(run_dir, summary)
    return summary


def _default_run_id() -> str:
    return "api_a_stage_smoke_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _default_composer_run_id() -> str:
    return "api_composer_a_smoke_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _default_b_run_id() -> str:
    return "api_b_smoke_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _default_c_run_id() -> str:
    return "api_c_smoke_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _default_cascade_run_id() -> str:
    return "api_cascade_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _is_model_setup_failure(raw_text: str) -> bool:
    return raw_text.lstrip().upper().startswith("SETUP FAILURE")


def _setup_failure_summary(status: str, run_id: str, stage: str, missing: list[str]) -> dict:
    return {
        "status": status,
        "run_id": run_id,
        "stage": stage,
        "missing_inputs": missing,
        "api_call_made": False,
    }


def _call_failed_summary(status: str, run_id: str, stage: str, result: ApiVerifierResult, config: ApiConfig) -> dict:
    return {
        "status": status,
        "run_id": run_id,
        "stage": stage,
        "model": result.model,
        "latency_ms": result.latency_ms,
        "api_call_made": not config.dry_run,
        "error": result.error,
    }


def _model_setup_failure_summary(status: str, run_id: str, stage: str, result: ApiVerifierResult, config: ApiConfig) -> dict:
    return {
        "status": status,
        "run_id": run_id,
        "stage": stage,
        "model": result.model,
        "latency_ms": result.latency_ms,
        "api_call_made": not config.dry_run,
        "protocol_action": "FIX_INPUT",
        "protocol_next_step": "FIX_INPUT_AND_RERUN",
    }


def _route_summary_fields(route_summary) -> dict:
    route_data = route_summary.to_dict()
    return {
        "cascade_route_status": route_data["status"],
        "stopped_stage": route_data["stopped_stage"],
        "protocol_action": route_data["protocol_action"],
        "protocol_source": route_data["protocol_source"],
        "protocol_next_step": route_data["protocol_next_step"],
        "rerun_starts_at": route_data["rerun_starts_at"],
        "current_cascade_action": route_data["current_cascade_action"],
        "candidate_guidance_seed": route_data["candidate_guidance_seed"],
    }


def _cascade_stage_failure_summary(run_id: str, stage_summary: dict, stage_summaries: list[dict]) -> dict:
    return {
        "status": "API_CASCADE_STAGE_FAILED",
        "run_id": run_id,
        "stage": "api_cascade",
        "failed_stage": stage_summary.get("stage"),
        "failed_stage_status": stage_summary.get("status"),
        "api_call_made": any(item.get("api_call_made") for item in stage_summaries),
        "protocol_action": stage_summary.get("protocol_action"),
        "protocol_next_step": stage_summary.get("protocol_next_step"),
        "current_cascade_action": stage_summary.get("current_cascade_action", "END_CURRENT_VERIFIER_CASCADE"),
        "stage_summaries": stage_summaries,
    }


def _cascade_routed_summary(run_id: str, routed_stage_summary: dict, stage_summaries: list[dict]) -> dict:
    route_status = routed_stage_summary.get("cascade_route_status")
    summary = {
        "status": route_status or routed_stage_summary.get("status"),
        "run_id": run_id,
        "stage": "api_cascade",
        "stopped_stage": routed_stage_summary.get("stopped_stage", routed_stage_summary.get("stage")),
        "derived_a_status": routed_stage_summary.get("derived_a_status"),
        "api_call_made": any(item.get("api_call_made") for item in stage_summaries),
        "protocol_action": routed_stage_summary.get("protocol_action"),
        "protocol_source": routed_stage_summary.get("protocol_source"),
        "protocol_next_step": routed_stage_summary.get("protocol_next_step"),
        "rerun_starts_at": routed_stage_summary.get("rerun_starts_at"),
        "current_cascade_action": routed_stage_summary.get("current_cascade_action"),
        "candidate_guidance_seed": routed_stage_summary.get("candidate_guidance_seed"),
        "stage_summaries": stage_summaries,
    }
    return summary
