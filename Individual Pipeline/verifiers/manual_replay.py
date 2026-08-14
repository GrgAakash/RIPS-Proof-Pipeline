"""Replay existing manual verifier outputs through the verifier routing logic."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from verifiers.orchestrator import _route_after_b, _route_after_c, _route_after_composer
from verifiers.parsers import derive_a_status, parse_a_report, parse_b_report, parse_c_report, parse_composer_a_report
from verifiers.run_store import make_run_dir, write_parsed, write_raw, write_summary
from verifiers.schemas import PipelineSummary


A_FILE_KEYS = (("A1", "verifier_a1"), ("A2", "verifier_a2"), ("A3", "verifier_a3"))


def run_manual_replay(
    *,
    a1_path: str | Path,
    a2_path: str | Path,
    a3_path: str | Path,
    composer_a_path: str | Path,
    verifier_b_path: str | Path | None,
    verifier_c_path: str | Path | None,
    skeleton_ref: str,
    output_root: str | Path,
    run_id: str | None = None,
) -> PipelineSummary:
    """Parse saved manual outputs, route them, and store replay artifacts."""

    run_id = run_id or _default_manual_run_id()
    run_dir = make_run_dir(output_root, run_id)
    paths = {
        "a1_path": Path(a1_path),
        "a2_path": Path(a2_path),
        "a3_path": Path(a3_path),
        "composer_a_path": Path(composer_a_path),
        "verifier_b_path": Path(verifier_b_path) if verifier_b_path else None,
        "verifier_c_path": Path(verifier_c_path) if verifier_c_path else None,
    }
    _write_manual_files(run_dir, paths, skeleton_ref)

    missing = _missing_required(paths, skeleton_ref, require_b=False, require_c=False)
    if missing:
        summary = PipelineSummary(
            status="SETUP_FAILURE",
            skeleton_ref=skeleton_ref,
            stopped_stage="setup",
            protocol_action="FIX_INPUT",
            protocol_next_step="FIX_INPUT_AND_RERUN",
            current_cascade_action="NOT_RUN_SETUP_FAILURE",
            missing_inputs=missing,
        )
        write_summary(run_dir, summary)
        return summary

    for run_name, artifact_name in A_FILE_KEYS:
        raw = _read(paths[f"{run_name.lower()}_path"])
        write_raw(run_dir, artifact_name, raw)
        parsed = parse_a_report(raw, run_id=run_name, skeleton_ref=skeleton_ref)
        write_parsed(run_dir, artifact_name, parsed.to_dict())

    composer_raw = _read(paths["composer_a_path"])
    write_raw(run_dir, "composer_a", composer_raw)
    composer = parse_composer_a_report(composer_raw, skeleton_ref=skeleton_ref)
    write_parsed(run_dir, "composer_a", composer.to_dict())
    derived_a_status = derive_a_status(composer)

    summary = _route_after_composer(skeleton_ref, composer, derived_a_status)
    if summary is not None:
        write_summary(run_dir, summary)
        return summary

    missing_b = _missing_required(paths, skeleton_ref, require_b=True, require_c=False)
    if missing_b:
        summary = PipelineSummary(
            status="SETUP_FAILURE",
            skeleton_ref=skeleton_ref,
            stopped_stage="verifier_b_setup",
            derived_a_status=derived_a_status,
            protocol_action="FIX_INPUT",
            protocol_next_step="FIX_INPUT_AND_RERUN",
            current_cascade_action="NOT_RUN_SETUP_FAILURE",
            missing_inputs=missing_b,
        )
        write_summary(run_dir, summary)
        return summary

    b_raw = _read(paths["verifier_b_path"])
    write_raw(run_dir, "verifier_b", b_raw)
    b_report = parse_b_report(b_raw, skeleton_ref=skeleton_ref)
    write_parsed(run_dir, "verifier_b", b_report.to_dict())
    summary = _route_after_b(skeleton_ref, b_report, derived_a_status)
    if summary is not None:
        write_summary(run_dir, summary)
        return summary

    missing_c = _missing_required(paths, skeleton_ref, require_b=True, require_c=True)
    if missing_c:
        summary = PipelineSummary(
            status="SETUP_FAILURE",
            skeleton_ref=skeleton_ref,
            stopped_stage="verifier_c_setup",
            derived_a_status=derived_a_status,
            protocol_action="FIX_INPUT",
            protocol_next_step="FIX_INPUT_AND_RERUN",
            current_cascade_action="NOT_RUN_SETUP_FAILURE",
            b_ran=True,
            missing_inputs=missing_c,
        )
        write_summary(run_dir, summary)
        return summary

    c_raw = _read(paths["verifier_c_path"])
    write_raw(run_dir, "verifier_c", c_raw)
    c_report = parse_c_report(c_raw, skeleton_ref=skeleton_ref)
    write_parsed(run_dir, "verifier_c", c_report.to_dict())
    summary = _route_after_c(skeleton_ref, c_report, derived_a_status)
    write_summary(run_dir, summary)
    return summary


def _missing_required(paths: dict[str, Path | None], skeleton_ref: str, *, require_b: bool, require_c: bool) -> list[str]:
    missing: list[str] = []
    if not skeleton_ref.strip():
        missing.append("skeleton_ref")
    required = ["a1_path", "a2_path", "a3_path", "composer_a_path"]
    if require_b:
        required.append("verifier_b_path")
    if require_c:
        required.append("verifier_c_path")
    for key in required:
        path = paths[key]
        if path is None or not path.exists() or not path.is_file():
            missing.append(key)
    return missing


def _read(path: Path | None) -> str:
    if path is None:
        return ""
    return path.read_text(encoding="utf-8-sig")


def _write_manual_files(run_dir: Path, paths: dict[str, Path | None], skeleton_ref: str) -> None:
    data = {key: str(path) if path else None for key, path in paths.items()}
    data["skeleton_ref"] = skeleton_ref
    (run_dir / "manual_files.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _default_manual_run_id() -> str:
    return "manual_replay_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
