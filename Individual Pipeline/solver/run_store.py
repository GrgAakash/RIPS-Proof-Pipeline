"""Run-folder layout and state persistence for the open-problem workflow.

Layout (one root per pipeline; branches recurse with the same shape):

    <root>/
      state.json                       # PipelineState
      round_001/
        S0.md  S1.md ... S5.md  S6.md
        candidate_final_proof.md [candidate_final_proof.tex]   # split from S6.md
        final_proof.md [final_proof.tex]                       # final-only assembly
        PROOF_GUIDE.md proof_registry.json professor_source.md # reader package
        proof_modules/E001.md                                  # clickable branch proof
        sealed_branch_proofs/E001_<slug>.md                    # hidden from later solvers
        source_ledger.md
        completion_checklist.md web_source_confirmation.md     # (s6_artifacts.py)
        citation_gate/
          attempt_001/ citation_generator_* citation_verifier_*
          citation_gate_summary.json
        verifier_a1.md verifier_a2.md verifier_a3.md composer_a.md
        verifier_b.md verifier_c.md final_checker.json
        parsed/S1.json ... controller_decision_solver.json ...
        controller_decision.json       # the round's final decision
      branches/
        branch_001_<slug>/             # own state.json, rounds, parent_note.md

Accepted branch proof bodies are persisted and hash-checked, but later solver
rounds receive only their statement-level guidance records. Every artifact and
controller decision is persisted so each routing step is auditable.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

from solver.io_utils import read_json, write_json
from solver.schemas import ControllerDecision, PipelineState


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str, max_length: int = 32) -> str:
    """Filesystem-safe branch-name slug from a lemma statement."""

    slug = _SLUG_RE.sub("_", text.strip().lower()).strip("_")
    return slug[:max_length].rstrip("_") or "lemma"


def _normalize_root(root: Path) -> Path:
    """Use a Windows extended-length (``\\\\?\\``) path for the run root.

    Branch runs nest deeply (``branches/branch_NNN_<slug>/round_NNN/parsed/...``),
    which can push absolute paths past the legacy 260-character MAX_PATH limit
    and make writes fail with FileNotFoundError. The ``\\\\?\\`` prefix lifts
    that limit; on non-Windows platforms the path is returned unchanged.
    """

    if os.name != "nt":
        return root
    text = os.path.abspath(root)
    if text.startswith("\\\\?\\"):
        return Path(text)
    if text.startswith("\\\\"):  # UNC share
        return Path("\\\\?\\UNC" + text[1:])
    return Path("\\\\?\\" + text)


@dataclass(frozen=True)
class OpenRunStore:
    """Path helper + persistence for one pipeline (main run or one branch)."""

    root: Path

    def __post_init__(self) -> None:
        # Frozen dataclass: normalize in place so every derived path (rounds,
        # branches, parsed artifacts) inherits the long-path-safe root.
        object.__setattr__(self, "root", _normalize_root(Path(self.root)))

    @property
    def state_path(self) -> Path:
        return self.root / "state.json"

    def round_dir(self, round_index: int) -> Path:
        return self.root / f"round_{round_index:03d}"

    def parsed_dir(self, round_index: int) -> Path:
        return self.round_dir(round_index) / "parsed"

    def branch_root(self, branch_index: int, slug: str) -> Path:
        return self.root / "branches" / f"branch_{branch_index:03d}_{slug}"

    # --- persistence -----------------------------------------------------

    def save_text(self, round_index: int, name: str, text: str) -> Path:
        path = self.round_dir(round_index) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.rstrip() + "\n", encoding="utf-8")
        return path

    def save_parsed(self, round_index: int, name: str, data: dict) -> Path:
        path = self.parsed_dir(round_index) / f"{name}.json"
        write_json(path, data)
        return path

    def save_decision(self, round_index: int, decision: ControllerDecision) -> None:
        """Persist a stage decision and mirror it as the round's latest decision."""

        directory = self.parsed_dir(round_index)
        write_json(directory / f"controller_decision_{decision.stage}.json", decision.to_dict())
        write_json(self.round_dir(round_index) / "controller_decision.json", decision.to_dict())

    def save_state(self, state: PipelineState) -> None:
        write_json(self.state_path, state.to_dict())

    def load_state(self) -> PipelineState | None:
        if not self.state_path.exists():
            return None
        return PipelineState.from_dict(read_json(self.state_path))

    def write_parent_note(self, note: str) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "parent_note.md").write_text(note.rstrip() + "\n", encoding="utf-8")
