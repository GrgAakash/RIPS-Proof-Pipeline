"""Deterministic bridge from Paper Cleaner Mini packages to solver inputs."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from solver.skeleton_source_gate import (
    SkeletonSourceGateDecision,
    SkeletonSourceGateError,
    expected_grant_ids,
)


SECTION_HEADINGS = (
    "## 0. Macro definitions",
    "## 1. Notation and conventions",
    "## 2. Standing assumptions",
    "## 3. Known external results (may be used without proof)",
    "## 4. Definitions",
    "## 5. Available results (statements only; may be used without proof)",
    "## 6. Target",
)
CLASSIFICATION_TAGS = frozenset({
    "paper_original_result",
    "cited_prior_result",
    "protocol_validation",
})
PACKET_MODE_RE = re.compile(
    r"<!--\s*SOLVER_INTERNET_MODE:\s*(none|source_supported)\s*-->",
    re.IGNORECASE,
)
PROOF_PAIRING_METHODS = frozenset({
    "explicit-label", "explicit-heading-label", "adjacent",
    "explicit-label-recovery",
})


class CleanerBridgeError(RuntimeError):
    """Raised when a cleaner package is not ready for solver export."""


@dataclass(frozen=True)
class CleanerSections:
    skeleton: str
    target: str
    section3: str
    section5: str


@dataclass(frozen=True)
class CleanerPackage:
    paper_id: str
    target_id: str
    problem_path: Path
    problem_text: str
    problem_sha256: str
    sections: CleanerSections
    bibliography: str
    target_proof: str
    full_source: str
    stage2_report: dict
    audit_record: dict
    audit_model: str
    cleaner_models: dict
    target_statement_sha256: str = ""
    target_proof_sha256: str = ""


def packet_internet_mode(packet_path: str | Path, *, required: bool = False) -> str | None:
    text = Path(packet_path).read_text(encoding="utf-8")
    match = PACKET_MODE_RE.search(text)
    if match is None:
        if required:
            raise CleanerBridgeError(
                f"prompt packet lacks SOLVER_INTERNET_MODE metadata: {packet_path}"
            )
        return None
    return match.group(1).lower()


def split_cleaner_problem(text: str) -> CleanerSections:
    """Split the cleaner's exact seven-section Markdown package."""

    positions: list[tuple[int, int]] = []
    for heading in SECTION_HEADINGS:
        matches = list(re.finditer(rf"(?m)^{re.escape(heading)}\s*$", text))
        if len(matches) != 1:
            raise CleanerBridgeError(
                f"cleaner problem must contain heading exactly once: {heading}"
            )
        positions.append((matches[0].start(), matches[0].end()))
    if positions != sorted(positions):
        raise CleanerBridgeError("cleaner problem sections are out of order")

    section_bodies: list[str] = []
    for index, (_start, end) in enumerate(positions):
        next_start = positions[index + 1][0] if index + 1 < len(positions) else len(text)
        section_bodies.append(text[end:next_start].strip())

    skeleton = text[positions[0][0]:positions[6][0]].strip()
    target = section_bodies[6]
    if not target:
        raise CleanerBridgeError("cleaner target section is empty")
    return CleanerSections(
        skeleton=skeleton,
        target=target,
        section3=section_bodies[3],
        section5=section_bodies[5],
    )


def load_cleaner_package(
    cleaner_runs_dir: str | Path,
    paper_id: str,
    target_id: str,
) -> CleanerPackage:
    """Load one shipped mini package and require a hash-bound audit pass."""

    root = Path(cleaner_runs_dir)
    paper_root = root / paper_id
    manifest = _read_json(paper_root / "manifest.json", "cleaner manifest")
    entries = [
        entry for entry in manifest.get("packages", [])
        if entry.get("target_id") == target_id
    ]
    if len(entries) != 1:
        raise CleanerBridgeError(
            f"expected one shipped package for {paper_id}/{target_id}, found {len(entries)}"
        )
    problem_path = paper_root / entries[0]["path"]
    problem_text = problem_path.read_text(encoding="utf-8")
    problem_sha = sha256_text(problem_text)
    stage2_report = _read_json(problem_path.parent / "report.json", "stage2 report")
    if stage2_report.get("problem_sha256") != problem_sha:
        raise CleanerBridgeError("stage2 report is stale or not bound to the current problem.md")

    audit_report = _read_json(root / "audit" / "audit_report.json", "independent audit report")
    audit_records = [
        record
        for paper in audit_report.get("papers", [])
        if paper.get("paper_id") == paper_id
        for record in paper.get("packages", [])
        if record.get("target_id") == target_id
    ]
    if len(audit_records) != 1:
        raise CleanerBridgeError(
            f"expected one independent audit record for {paper_id}/{target_id}"
        )
    audit_record = audit_records[0]
    if not audit_record.get("audit_pass"):
        raise CleanerBridgeError("independent cleaner audit did not pass")
    if audit_record.get("problem_sha256") != problem_sha or not audit_record.get("hash_matches"):
        raise CleanerBridgeError("independent audit is stale or hash-mismatched")

    index = _read_json(paper_root / "index" / "statements.v2.json", "statement index")
    if index.get("schema_version") != 2:
        raise CleanerBridgeError(
            "stale statement index; rerun Paper Cleaner Step 2/3 to create "
            "source/proof provenance schema version 2"
        )
    statements = [item for item in index.get("statements", []) if item.get("id") == target_id]
    if len(statements) != 1:
        raise CleanerBridgeError(f"target {target_id!r} missing or duplicated in statement index")
    bibliography = _bibliography_text(index)
    meta = _read_json(paper_root / "source" / "meta.json", "paper metadata")
    source_name = "flat.md" if meta.get("source_type") == "ocr" else "flat.tex"
    full_source = (paper_root / "source" / source_name).read_text(encoding="utf-8")
    statement = statements[0]
    statement_text = str(statement.get("statement_tex", ""))
    statement_sha = str(statement.get("statement_sha256", ""))
    source_start = statement.get("source_start", -1)
    source_end = statement.get("source_end", -1)
    if statement.get("added_by") != "parser" or not statement.get("source_verified"):
        raise CleanerBridgeError("selected target is not deterministically source-backed")
    if statement.get("source_file") != f"source/{source_name}":
        raise CleanerBridgeError("selected target source file does not match the paper source")
    if not statement_text or not statement_sha or sha256_text(statement_text) != statement_sha:
        raise CleanerBridgeError("selected target statement hash is missing or invalid")
    if not isinstance(source_start, int) or not isinstance(source_end, int) \
            or not (0 <= source_start < source_end <= len(full_source)):
        raise CleanerBridgeError("selected target source span is invalid")
    source_slice = full_source[source_start:source_end]
    if sha256_text(source_slice) != statement.get("source_sha256") \
            or statement_text not in source_slice:
        raise CleanerBridgeError("selected target does not match its frozen source slice")
    proof_text = str(statement.get("proof_tex") or "")
    proof_sha = str(statement.get("proof_sha256", ""))
    proof_start = statement.get("proof_source_start", -1)
    proof_end = statement.get("proof_source_end", -1)
    proof_ok = (
        bool(proof_text)
        and statement.get("proof_source_verified") is True
        and statement.get("proof_pairing") in PROOF_PAIRING_METHODS
        and statement.get("proof_source_file") == f"source/{source_name}"
        and isinstance(proof_start, int)
        and isinstance(proof_end, int)
        and 0 <= proof_start < proof_end <= len(full_source)
        and bool(proof_sha)
        and sha256_text(proof_text) == proof_sha
        and sha256_text(full_source[proof_start:proof_end])
            == statement.get("proof_source_sha256")
        and proof_text in full_source[proof_start:proof_end]
    )
    if not proof_ok:
        raise CleanerBridgeError(
            "selected target proof is not backed by a valid source span, "
            "hashes, and deterministic pairing"
        )
    target_record = _read_json(problem_path.parent / "target.json", "frozen target record")
    target_tex = (problem_path.parent / "target.tex").read_text(encoding="utf-8")
    expected_record = {
        "target_id": target_id,
        "statement_sha256": statement_sha,
        "source_file": statement.get("source_file"),
        "source_start": source_start,
        "source_end": source_end,
        "source_sha256": statement.get("source_sha256"),
        "proof_sha256": proof_sha,
        "proof_source_file": statement.get("proof_source_file"),
        "proof_source_start": proof_start,
        "proof_source_end": proof_end,
        "proof_source_sha256": statement.get("proof_source_sha256"),
        "proof_source_verified": statement.get("proof_source_verified"),
        "proof_pairing": statement.get("proof_pairing"),
    }
    if target_tex != statement_text or target_record != expected_record:
        raise CleanerBridgeError("frozen target artifacts do not match the statement index")
    sections = split_cleaner_problem(problem_text)
    expected_target = f"**Target statement.**\n\n{statement_text}".strip()
    if sections.target != expected_target:
        raise CleanerBridgeError("cleaner Section 6 does not exactly match the frozen target")
    if re.sub(r"\s+", " ", statement_text).strip() in \
            re.sub(r"\s+", " ", sections.skeleton):
        raise CleanerBridgeError("target statement is duplicated in the allowed-support skeleton")
    if stage2_report.get("input_hashes", {}).get("target") != statement_sha:
        raise CleanerBridgeError("stage2 report is not bound to the frozen target")
    if stage2_report.get("input_hashes", {}).get("reference_proof") != proof_sha:
        raise CleanerBridgeError(
            "stage2 report is not bound to the source-backed reference proof"
        )
    if audit_record.get("det_target_issues"):
        raise CleanerBridgeError("independent audit reported target-integrity issues")
    summary_path = root / "stage2_summary.json"
    summary = _read_json(summary_path, "stage2 summary") if summary_path.exists() else {}

    return CleanerPackage(
        paper_id=paper_id,
        target_id=target_id,
        problem_path=problem_path,
        problem_text=problem_text,
        problem_sha256=problem_sha,
        sections=sections,
        bibliography=bibliography,
        target_proof=proof_text,
        full_source=full_source,
        stage2_report=stage2_report,
        audit_record=audit_record,
        audit_model=str(audit_report.get("model", "")),
        cleaner_models=dict(summary.get("models", {})),
        target_statement_sha256=statement_sha,
        target_proof_sha256=proof_sha,
    )


def export_solver_bundle(
    *,
    package: CleanerPackage,
    output_dir: str | Path,
    packet_path: str | Path,
    classification_tag: str,
    source_gate_decision: SkeletonSourceGateDecision,
    source_gate_dir: str | Path,
    source_audit_model: str,
    include_private_final_checker: bool = False,
) -> Path:
    """Write one atomic, solver-native bundle after every hard gate passes."""

    _validate_frozen_package(package)
    _validate_classification_tag(classification_tag)
    _validate_source_gate(package, source_gate_decision, Path(source_gate_dir))
    packet_path = Path(packet_path)
    packet_mode = packet_internet_mode(packet_path, required=True)
    packet_sha = sha256_text(packet_path.read_text(encoding="utf-8"))
    output_root = Path(output_dir)

    public_files, private_files = _solver_file_contents(
        package, include_private_final_checker
    )

    hashes = {name: sha256_text(content) for name, content in {**public_files, **private_files}.items()}
    audit_summary = _sanitized_audit(package)
    manifest = {
        "schema_version": 2,
        "paper_id": package.paper_id,
        "target_id": package.target_id,
        "target_scope": "target_scoped_proof_informed",
        "run_tags": [classification_tag, "skeleton_guided_measurement"],
        "source_problem_sha256": package.problem_sha256,
        "target_statement_sha256": package.target_statement_sha256,
        "packet_file": str(packet_path),
        "packet_sha256": packet_sha,
        "solver_internet_mode": packet_mode,
        "cleaner_models": package.cleaner_models,
        "independent_audit_model": package.audit_model,
        "source_audit_model": source_audit_model,
        "cleaner_audit": audit_summary,
        "skeleton_source_gate": source_gate_decision.to_dict(),
        "support_counts": {
            "external_results": len(source_gate_decision.expected_grant_ids),
            "own_paper_statement_markers": len(re.findall(r"\*\*[^*]+\*\*", package.sections.section5)),
        },
        "private_final_checker_material": include_private_final_checker,
        "file_sha256": hashes,
    }
    manifest_text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"

    if output_root.exists():
        _validate_idempotent_output(
            output_root, manifest, {**public_files, **private_files, "setup_manifest.json": manifest_text}
        )
        return output_root / "solver_input"

    output_root.parent.mkdir(parents=True, exist_ok=True)
    temp_root = Path(tempfile.mkdtemp(prefix=f".{output_root.name}.", dir=output_root.parent))
    try:
        solver_input = temp_root / "solver_input"
        for name, content in public_files.items():
            _write_text(solver_input / name, content)
        for name, content in private_files.items():
            _write_text(solver_input / name, content)
        _write_text(solver_input / "setup_manifest.json", manifest_text)
        controller = temp_root / "controller"
        _write_text(
            controller / "skeleton_audit.json",
            json.dumps(audit_summary, indent=2, sort_keys=True) + "\n",
        )
        gate_source = Path(source_gate_dir)
        if gate_source.exists():
            shutil.copytree(gate_source, controller / "skeleton_source_gate")
        os.replace(temp_root, output_root)
    except Exception:
        shutil.rmtree(temp_root, ignore_errors=True)
        raise
    return output_root / "solver_input"


def reuse_prepared_solver_bundle(
    *,
    package: CleanerPackage,
    output_dir: str | Path,
    packet_path: str | Path,
    classification_tag: str,
    source_audit_model: str,
    include_private_final_checker: bool = False,
) -> Path | None:
    """Return a current prepared bundle without repeating the source-gate calls."""

    output_root = Path(output_dir)
    if not output_root.exists():
        return None
    _validate_frozen_package(package)
    _validate_classification_tag(classification_tag)
    packet_path = Path(packet_path)
    packet_mode = packet_internet_mode(packet_path, required=True)
    packet_sha = sha256_text(packet_path.read_text(encoding="utf-8"))
    public_files, private_files = _solver_file_contents(
        package, include_private_final_checker
    )
    expected_hashes = {
        name: sha256_text(content)
        for name, content in {**public_files, **private_files}.items()
    }
    manifest = _read_json(
        output_root / "solver_input" / "setup_manifest.json",
        "prepared setup manifest",
    )
    expected = {
        "schema_version": 2,
        "paper_id": package.paper_id,
        "target_id": package.target_id,
        "target_scope": "target_scoped_proof_informed",
        "run_tags": [classification_tag, "skeleton_guided_measurement"],
        "source_problem_sha256": package.problem_sha256,
        "target_statement_sha256": package.target_statement_sha256,
        "packet_sha256": packet_sha,
        "solver_internet_mode": packet_mode,
        "cleaner_models": package.cleaner_models,
        "independent_audit_model": package.audit_model,
        "source_audit_model": source_audit_model,
        "private_final_checker_material": include_private_final_checker,
        "file_sha256": expected_hashes,
    }
    if any(manifest.get(key) != value for key, value in expected.items()):
        raise CleanerBridgeError(
            f"prepared output already exists with different inputs; use a fresh directory: "
            f"{output_root}"
        )
    for name, content in {**public_files, **private_files}.items():
        path = output_root / "solver_input" / name
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            raise CleanerBridgeError(f"prepared output file drifted: {path}")
    try:
        decision = SkeletonSourceGateDecision(**manifest["skeleton_source_gate"])
    except (KeyError, TypeError) as exc:
        raise CleanerBridgeError("prepared setup manifest has an invalid source-gate decision") from exc
    _validate_source_gate(
        package,
        decision,
        output_root / "controller" / "skeleton_source_gate",
    )
    return output_root / "solver_input"


def _allowed_support(sections: CleanerSections) -> str:
    return f"""Definitions, notation, conventions, and standing assumptions in Sections 1, 2, and 4 of the cleaned skeleton are allowed.

The following independently source-gated external results from Section 3 are allowed exactly as written:

{sections.section3 or 'None.'}

The following prior own-paper statements from Section 5 are allowed exactly as written:

{sections.section5 or 'None.'}

Section 6 is the target and is not an allowed premise. No statement equivalent to, stronger than, or logically downstream from the target may be used as a premise.
"""


def _validate_classification_tag(classification_tag: str) -> None:
    if classification_tag not in CLASSIFICATION_TAGS:
        raise CleanerBridgeError(
            "classification tag must be paper_original_result, cited_prior_result, "
            "or protocol_validation"
        )


def _validate_frozen_package(package: CleanerPackage) -> None:
    if not re.fullmatch(r"[0-9a-f]{64}", package.target_statement_sha256):
        raise CleanerBridgeError("cleaner package lacks a valid frozen-target hash")
    if (not re.fullmatch(r"[0-9a-f]{64}", package.target_proof_sha256)
            or sha256_text(package.target_proof) != package.target_proof_sha256):
        raise CleanerBridgeError("cleaner package lacks a valid source-backed proof hash")


def _solver_file_contents(
    package: CleanerPackage,
    include_private_final_checker: bool,
) -> tuple[dict[str, str], dict[str, str]]:
    public_files = {
        "target.md": package.sections.target.rstrip() + "\n",
        "skeleton.md": package.sections.skeleton.rstrip() + "\n",
        "allowed_support.md": _allowed_support(package.sections).rstrip() + "\n",
        "guidance.md": "",
    }
    if package.bibliography:
        public_files["bibliography.bib"] = package.bibliography.rstrip() + "\n"
    private_files: dict[str, str] = {}
    if include_private_final_checker:
        if not package.target_proof:
            raise CleanerBridgeError("private Final Checker requested but target proof is empty")
        private_files = {
            "private/gold_proof.md": package.target_proof.rstrip() + "\n",
            "private/source.md": package.full_source.rstrip() + "\n",
        }
    return public_files, private_files


def _validate_source_gate(
    package: CleanerPackage,
    decision: SkeletonSourceGateDecision,
    source_gate_dir: Path,
) -> None:
    try:
        grants = expected_grant_ids(package.sections.section3)
    except SkeletonSourceGateError as exc:
        raise CleanerBridgeError(str(exc)) from exc
    if grants:
        if decision.gate_result != "GOOD_TO_GO" or not decision.verifier_ran:
            raise CleanerBridgeError(
                f"skeleton source gate did not pass: {decision.gate_result}"
            )
        inventories = (
            decision.expected_grant_ids,
            decision.generator_grant_ids,
            decision.verifier_grant_ids,
        )
        if any(
            len(inventory) != len(grants) or sorted(inventory) != sorted(grants)
            for inventory in inventories
        ):
            raise CleanerBridgeError(
                "skeleton source gate decision does not match the Section 3 grant inventory"
            )
    elif (
        decision.gate_result != "NOT_APPLICABLE"
        or decision.expected_grant_ids
        or decision.generator_grant_ids
        or decision.verifier_grant_ids
        or decision.verifier_ran
    ):
        raise CleanerBridgeError(
            "an empty Section 3 requires an exact NOT_APPLICABLE source-gate decision"
        )

    decision_path = source_gate_dir / "skeleton_source_gate_decision.json"
    saved = _read_json(decision_path, "skeleton source-gate decision")
    if saved != decision.to_dict():
        raise CleanerBridgeError("saved skeleton source-gate decision does not match export input")


def _sanitized_audit(package: CleanerPackage) -> dict:
    audit = package.audit_record.get("audit", {})
    return {
        "audit_pass": True,
        "problem_sha256": package.problem_sha256,
        "target_statement_sha256": package.target_statement_sha256,
        "hash_matches": True,
        "self_contained": bool(audit.get("self_contained")),
        "leak_free": bool(audit.get("leak_free")),
        "sufficient": bool(audit.get("sufficient")),
        "fatal_issue_count": sum(
            1 for issue in audit.get("issues", []) if issue.get("severity") == "fatal"
        ),
        "deterministic_leak_count": len(package.audit_record.get("det_leak_spans", [])),
        "unknown_command_count": len(package.audit_record.get("det_unknown_commands", [])),
    }


def _bibliography_text(index: dict) -> str:
    entries = []
    for citation in index.get("citations", []):
        raw = str(citation.get("raw_bib", "")).strip()
        if raw:
            entries.append(f"% citation_key: {citation.get('key', '')}\n{raw}")
    return "\n\n".join(entries)


def _validate_idempotent_output(output_root: Path, manifest: dict, files: dict[str, str]) -> None:
    manifest_path = output_root / "solver_input" / "setup_manifest.json"
    if not manifest_path.exists():
        raise CleanerBridgeError(f"output directory already exists and is not a prepared bundle: {output_root}")
    existing = json.loads(manifest_path.read_text(encoding="utf-8"))
    keys = (
        "schema_version",
        "paper_id",
        "target_id",
        "source_problem_sha256",
        "target_statement_sha256",
        "packet_sha256",
        "run_tags",
        "private_final_checker_material",
        "file_sha256",
    )
    if any(existing.get(key) != manifest.get(key) for key in keys):
        raise CleanerBridgeError(
            f"prepared output already exists with different inputs: {output_root}"
        )
    for name, expected in files.items():
        path = output_root / "solver_input" / name
        if not path.exists() or path.read_text(encoding="utf-8") != expected:
            raise CleanerBridgeError(f"prepared output file drifted: {path}")


def _read_json(path: Path, label: str) -> dict:
    if not path.exists():
        raise CleanerBridgeError(f"{label} does not exist: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CleanerBridgeError(f"cannot read {label} at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CleanerBridgeError(f"{label} must be a JSON object: {path}")
    return value


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
