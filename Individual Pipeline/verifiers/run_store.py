"""Run artifact storage for the standalone verifier mock pipeline."""

from __future__ import annotations

import json
from pathlib import Path

from verifiers.schemas import PipelineSummary, VerifierInput


def make_run_dir(output_root: str | Path, run_id: str) -> Path:
    run_dir = Path(output_root) / run_id
    (run_dir / "raw").mkdir(parents=True, exist_ok=True)
    (run_dir / "parsed").mkdir(parents=True, exist_ok=True)
    return run_dir


def write_inputs(run_dir: Path, inputs: VerifierInput) -> None:
    _write_json(run_dir / "inputs.json", inputs.to_dict())


def write_raw(run_dir: Path, name: str, text: str) -> None:
    path = run_dir / "raw" / f"{name}.md"
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_parsed(run_dir: Path, name: str, data: dict) -> None:
    _write_json(run_dir / "parsed" / f"{name}.json", data)


def write_summary(run_dir: Path, summary: PipelineSummary) -> None:
    _write_json(run_dir / "summary.json", summary.to_dict())


def write_json_artifact(path: Path, data: dict) -> None:
    _write_json(path, data)


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
