"""Guidance handoff artifacts for the next solver cascade."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from verifiers.run_store import write_json_artifact

RERUN_SOLVER_WITH_GUIDANCE = "RERUN_SOLVER_WITH_GUIDANCE"


def build_next_guidance_handoff(summary: Any) -> dict | None:
    data = _summary_dict(summary)
    if data.get("protocol_action") != RERUN_SOLVER_WITH_GUIDANCE:
        return None

    seed = _none_if_empty(data.get("candidate_guidance_seed"))
    if seed is None:
        return None

    return {
        "handoff_type": "NEXT_SOLVER_GUIDANCE",
        "guidance_list": [seed],
        "source_status": data.get("status"),
        "source_verifier_stage": data.get("stopped_stage") or data.get("stage"),
        "protocol_source": data.get("protocol_source"),
        "derived_a_status": data.get("derived_a_status"),
        "protocol_action": data.get("protocol_action"),
        "protocol_next_step": data.get("protocol_next_step"),
        "rerun_starts_at": data.get("rerun_starts_at"),
        "current_cascade_action": data.get("current_cascade_action"),
    }


def write_next_guidance_if_applicable(run_dir: Path, summary: Any) -> dict | None:
    handoff = build_next_guidance_handoff(summary)
    if handoff is not None:
        write_json_artifact(run_dir / "next_guidance.json", handoff)
    return handoff


def _summary_dict(summary: Any) -> dict:
    if isinstance(summary, dict):
        return summary
    if is_dataclass(summary):
        return asdict(summary)
    if hasattr(summary, "to_dict"):
        return summary.to_dict()
    raise TypeError(f"Unsupported summary type: {type(summary)!r}")


def _none_if_empty(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned or cleaned.lower().strip(" .") in {"none", "not applicable", "n/a"}:
        return None
    return cleaned
