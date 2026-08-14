"""Integrity-checked, reader-facing assembly for accepted branch proofs."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path

from solver.schemas import SealedBranchProof


_PROOF_ID_RE = re.compile(r"^[A-Z][A-Z0-9_-]*$")
_LOCAL_MODULE_LINK_RE = re.compile(
    r"\[([^\]\n]+)\]\(proof_modules/[A-Za-z0-9_.-]+\.md(?:#[^)]+)?\)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class SealedProofAssemblyReport:
    passed: bool
    attached_count: int
    attached_proof_ids: list[str] = field(default_factory=list)
    violations: list[str] = field(default_factory=list)
    candidate_sha256: str = ""
    assembled_sha256: str = ""
    module_files: list[str] = field(default_factory=list)
    guide_file: str = ""
    registry_file: str = ""
    professor_source_file: str = ""
    tex_attempted: bool = False
    tex_succeeded: bool = False
    tex_converter: str = ""
    tex_message: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class SealedProofPackage:
    """Final proof plus deterministic human-navigation artifacts."""

    final_proof_md: str
    final_proof_tex: str | None = None
    professor_source_md: str = ""
    proof_guide_md: str = ""
    proof_registry_json: str = ""
    module_files: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class _ValidatedProof:
    record: SealedBranchProof
    proof_text: str
    module_file: str


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def assemble_final_proof(
    candidate_proof: str,
    sealed_proofs: list[SealedBranchProof],
    run_root: Path,
) -> tuple[str, SealedProofAssemblyReport]:
    """Compatibility wrapper returning the assembled Markdown and audit report."""

    package, report = build_final_proof_package(candidate_proof, sealed_proofs, run_root)
    return package.final_proof_md, report


def build_final_proof_package(
    candidate_proof: str,
    sealed_proofs: list[SealedBranchProof],
    run_root: Path,
) -> tuple[SealedProofPackage, SealedProofAssemblyReport]:
    """Build clickable Markdown modules and a self-contained TeX proof package.

    Solver-visible prompts are unchanged. This function runs only after S6 has
    cited every accepted branch result and immediately before the verifier
    cascade receives the final proof.
    """

    candidate = candidate_proof.rstrip()
    candidate_hash = sha256_text(candidate)
    if not sealed_proofs:
        package = SealedProofPackage(final_proof_md=candidate)
        return package, SealedProofAssemblyReport(
            passed=True,
            attached_count=0,
            candidate_sha256=candidate_hash,
            assembled_sha256=sha256_text(candidate),
        )

    validated, violations = _validate_sealed_proofs(
        candidate,
        sealed_proofs,
        run_root,
    )
    if violations:
        return SealedProofPackage(final_proof_md=candidate), SealedProofAssemblyReport(
            passed=False,
            attached_count=len(validated),
            attached_proof_ids=[item.record.proof_id for item in validated],
            violations=violations,
            candidate_sha256=candidate_hash,
        )

    linked_candidate = candidate
    for item in validated:
        linked_candidate = _link_proof_reference(
            linked_candidate,
            item.record.proof_id,
            item.module_file,
        )

    appendix = _proof_appendix(validated)
    assembled = (
        f"{linked_candidate}\n\n"
        "# Internally Verified Auxiliary Results\n\n"
        "The results below were proved in isolated branch pipelines. Later solver "
        "rounds received only their exact statements and verified status. Each "
        "reference opens a standalone, hash-audited proof module.\n\n"
        f"{appendix}"
    )
    module_files = {
        item.module_file: _module_markdown(item, validated)
        for item in validated
    }
    proof_guide = _proof_guide(validated)
    registry = _proof_registry(validated)
    professor_source = _professor_source(assembled, validated)
    tex, tex_attempted, converter, tex_message = _convert_professor_tex(professor_source)

    package = SealedProofPackage(
        final_proof_md=assembled,
        final_proof_tex=tex,
        professor_source_md=professor_source,
        proof_guide_md=proof_guide,
        proof_registry_json=json.dumps(registry, indent=2, sort_keys=True) + "\n",
        module_files=module_files,
    )
    report = SealedProofAssemblyReport(
        passed=True,
        attached_count=len(validated),
        attached_proof_ids=[item.record.proof_id for item in validated],
        candidate_sha256=candidate_hash,
        assembled_sha256=sha256_text(assembled),
        module_files=sorted(module_files),
        guide_file="PROOF_GUIDE.md",
        registry_file="proof_registry.json",
        professor_source_file="professor_source.md",
        tex_attempted=tex_attempted,
        tex_succeeded=tex is not None,
        tex_converter=converter,
        tex_message=tex_message,
    )
    return package, report


def _validate_sealed_proofs(
    candidate: str,
    sealed_proofs: list[SealedBranchProof],
    run_root: Path,
) -> tuple[list[_ValidatedProof], list[str]]:
    root = run_root.resolve()
    validated: list[_ValidatedProof] = []
    violations: list[str] = []
    seen_ids: set[str] = set()

    for record in sealed_proofs:
        proof_id = record.proof_id.strip()
        if not proof_id or proof_id in seen_ids:
            violations.append(f"duplicate or empty proof id: {proof_id!r}")
            continue
        seen_ids.add(proof_id)
        if _PROOF_ID_RE.fullmatch(proof_id) is None:
            violations.append(f"invalid proof id: {proof_id!r}")
            continue
        if not _contains_proof_reference(candidate, proof_id):
            violations.append(
                f"{proof_id}: candidate final proof does not cite the sealed result"
            )
            continue

        relative = Path(record.artifact_path)
        if relative.is_absolute():
            violations.append(f"{proof_id}: artifact path must be relative")
            continue
        artifact = (root / relative).resolve()
        try:
            artifact.relative_to(root)
        except ValueError:
            violations.append(f"{proof_id}: artifact path escapes run root")
            continue
        if not artifact.is_file():
            violations.append(f"{proof_id}: sealed proof artifact is missing")
            continue

        original = artifact.read_text(encoding="utf-8")
        if sha256_text(original) != record.proof_sha256:
            violations.append(f"{proof_id}: sealed proof hash mismatch")
            continue
        # Nested branch packages can contain links local to the nested run.
        # Their proof bodies are already embedded transitively, so remove only
        # those stale links while preserving their mathematical labels.
        proof_text = _LOCAL_MODULE_LINK_RE.sub(r"\1", original.rstrip())
        validated.append(
            _ValidatedProof(
                record=record,
                proof_text=proof_text,
                module_file=f"proof_modules/{proof_id}.md",
            )
        )
    return validated, violations


def _contains_proof_reference(text: str, proof_id: str) -> bool:
    return re.search(rf"(?<![A-Za-z0-9_]){re.escape(proof_id)}(?![A-Za-z0-9_])", text) is not None


def _link_proof_reference(text: str, proof_id: str, module_file: str) -> str:
    existing_link = re.compile(
        rf"\[{re.escape(proof_id)}\]\([^)\n]+\)",
        re.IGNORECASE,
    )
    text = existing_link.sub(f"[{proof_id}]({module_file})", text)
    pattern = re.compile(
        rf"\[{re.escape(proof_id)}\](?!\()"
        rf"|(?<![A-Za-z0-9_\[]){re.escape(proof_id)}(?![A-Za-z0-9_\]])"
    )
    return pattern.sub(f"[{proof_id}]({module_file})", text)


def _proof_appendix(proofs: list[_ValidatedProof]) -> str:
    blocks: list[str] = []
    available = {item.record.proof_id for item in proofs}
    for item in proofs:
        record = item.record
        where_used = record.where_used.strip() or "As cited in the main proof."
        dependencies = _dependency_text(record.dependencies, available)
        blocks.append(
            f"## Auxiliary Result {record.proof_id} {{#proof-{record.proof_id}}}\n\n"
            f"[Open standalone proof module]({item.module_file})\n\n"
            "**Status.** Independently verified internal branch result.\n\n"
            f"**Use location.** {where_used}\n\n"
            f"**Nested dependencies.** {dependencies}\n\n"
            "**Statement.**\n\n"
            f"{record.lemma_statement.strip()}\n\n"
            "**Proof.**\n\n"
            f"{item.proof_text}"
        )
    return "\n\n".join(blocks)


def _module_markdown(item: _ValidatedProof, proofs: list[_ValidatedProof]) -> str:
    record = item.record
    available = {proof.record.proof_id for proof in proofs}
    dependencies = _dependency_text(record.dependencies, available, prefix="")
    where_used = record.where_used.strip() or "As cited in the main proof."
    return (
        f"# Auxiliary Result {record.proof_id}\n\n"
        "[Back to the final proof](../final_proof.md)\n\n"
        f"- **Internal ID:** `{record.proof_id}`\n"
        f"- **Status:** independently verified branch result\n"
        f"- **Source:** `{record.source_problem_id}`, round {record.source_round}\n"
        f"- **Use location:** {where_used}\n"
        f"- **Nested dependencies:** {dependencies}\n"
        f"- **Proof SHA-256:** `{record.proof_sha256}`\n\n"
        "## Statement\n\n"
        f"{record.lemma_statement.strip()}\n\n"
        "## Proof\n\n"
        f"{item.proof_text}\n"
    )


def _dependency_text(
    dependencies: list[str],
    available: set[str],
    *,
    prefix: str = "proof_modules/",
) -> str:
    if not dependencies:
        return "None"
    labels = []
    for dependency in dependencies:
        if dependency in available:
            labels.append(f"[{dependency}]({prefix}{dependency}.md)")
        else:
            labels.append(f"{dependency} (embedded transitively)")
    return ", ".join(labels)


def _proof_guide(proofs: list[_ValidatedProof]) -> str:
    entries = []
    for item in proofs:
        statement = " ".join(item.record.lemma_statement.split())
        entries.append(
            f"- [{item.record.proof_id}: {statement}]({item.module_file})"
        )
    return (
        "# Proof Guide\n\n"
        "Start with the [final composed proof](final_proof.md). Its internal "
        "references open the independently verified branch proofs below.\n\n"
        "## Internally Verified Results\n\n"
        + "\n".join(entries)
        + "\n"
    )


def _proof_registry(proofs: list[_ValidatedProof]) -> dict:
    return {
        "version": 1,
        "proofs": [
            {
                "proof_id": item.record.proof_id,
                "statement": item.record.lemma_statement.strip(),
                "file": item.module_file,
                "proof_sha256": item.record.proof_sha256,
                "source_problem_id": item.record.source_problem_id,
                "source_round": item.record.source_round,
                "where_used": item.record.where_used,
                "dependencies": list(item.record.dependencies),
                "solver_received_statement": item.record.solver_received_statement,
                "solver_received_proof": item.record.solver_received_proof,
            }
            for item in proofs
        ],
    }


def _professor_source(assembled: str, proofs: list[_ValidatedProof]) -> str:
    source = assembled
    for item in proofs:
        proof_id = item.record.proof_id
        pattern = re.compile(
            rf"\[([^\]]+)\]\({re.escape(item.module_file)}(?:#[^)]+)?\)",
            re.IGNORECASE,
        )
        source = pattern.sub(rf"[\1](#proof-{proof_id})", source)
    return source.rstrip() + "\n"


def _convert_professor_tex(source: str) -> tuple[str | None, bool, str, str]:
    converter = shutil.which("pandoc")
    if converter is None:
        return None, False, "", "pandoc is unavailable; Markdown proof package was preserved"
    command = [
        converter,
        "--from=markdown+tex_math_dollars+tex_math_single_backslash+raw_tex",
        "--to=latex",
        "--standalone",
        "--table-of-contents",
        "--wrap=none",
        "--metadata",
        "title=Reconstructed Proof Package",
        "--metadata",
        "date=",
        "--variable",
        "geometry:margin=1in",
        "--variable",
        "colorlinks=true",
        "--variable",
        "linkcolor=blue",
        "--variable",
        "urlcolor=blue",
    ]
    try:
        completed = subprocess.run(
            command,
            input=source,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, True, converter, f"pandoc failed: {exc}"
    tex = _normalize_equation_tags(completed.stdout.strip())
    if completed.returncode != 0 or "\\documentclass" not in tex or "\\end{document}" not in tex:
        detail = completed.stderr.strip() or "pandoc did not produce standalone TeX"
        return None, True, converter, detail
    return tex, True, converter, "self-contained linked TeX assembled successfully"


def _normalize_equation_tags(tex: str) -> str:
    tex = re.sub(r"\\tag\*?\{([^{}]+)\}", r"\\qquad(\1)", tex)
    return tex.replace(r"\left{", r"\left\{").replace(r"\right}", r"\right\}")
