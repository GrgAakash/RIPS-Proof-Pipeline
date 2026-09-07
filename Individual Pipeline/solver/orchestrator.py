"""Autonomous orchestrator for the S0-S6 open-problem workflow.

Drives rounds of S0 -> S1-S5 -> S6, hands every parsed output to the
deterministic controller, and executes its routing: append one guidance item
and rerun fresh, open a branch pipeline on a candidate lemma, walk the
verifier cascade, invoke the privileged Final Checker (gold mode only), or
stop (budget / human review / max rounds).

Markovian invariant, enforced structurally: the only solver-visible state
carried into a new round is the cumulative guidance list. Accepted branch
proofs are persisted separately as sealed artifacts and attached only to the
final verifier-facing proof. Blueprints, proof bodies, and verifier reports
from earlier rounds never enter later solver prompts.
"""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Callable

from solver.io_utils import write_json
from solver.agent_calls import AgentCaller
from solver.controller import (
    ControllerConfig,
    budget_exhausted,
    collapse_branch_outcome,
    decide_solver_stage,
    derive_a_status,
    route_after_composer_a,
    route_after_citation_gate,
    route_after_problem_statement_verifier,
    route_after_verifier_b,
    route_after_verifier_c,
    route_final,
)
from solver.report_parsers import (
    has_leakage_marker,
    has_setup_failure,
    normalize_failure_type,
    normalize_tristate,
    parse_composer_a_report,
    parse_composer_output,
    parse_final_checker_output,
    parse_problem_statement_report,
    parse_s0_assignments,
    parse_s0_hardest_solver,
    parse_s0_key_solver,
    parse_subproblem_output,
    parse_verifier_b_report,
    parse_verifier_c_report,
)
from solver.run_store import OpenRunStore, slugify
from solver.s6_artifacts import derive_s6_artifact_files
from solver.sealed_proofs import (
    build_final_proof_package,
    sha256_text,
)
from solver.schemas import (
    BRANCH_LEMMA,
    BranchLemmaCandidate,
    ComposedProofResult,
    ControllerDecision,
    OUTCOME_ACCEPTED,
    OUTCOME_ACCEPTED_CASCADE_ONLY,
    OUTCOME_NEEDS_HUMAN_REVIEW,
    OUTCOME_OPEN_BRANCH,
    OUTCOME_REJECTED_FINAL_CHECK,
    OUTCOME_RERUN_UNCHANGED,
    OUTCOME_RERUN_WITH_GUIDANCE,
    OUTCOME_RUN_NEXT_STAGE,
    OUTCOME_RUN_VERIFICATION,
    OUTCOME_STOPPED_BUDGET,
    PipelineState,
    SealedBranchProof,
    STATUS_ACCEPTED,
    STATUS_ACCEPTED_CASCADE_ONLY,
    STATUS_NEEDS_HUMAN_REVIEW,
    STATUS_REJECTED_FINAL_CHECK,
    STATUS_RUNNING,
    STATUS_STOPPED_BUDGET,
    STATUS_STOPPED_MAX_ROUNDS,
    SolverFailureOutput,
    SubproblemResult,
    UNPARSEABLE,
)


S_IDS = ("S1", "S2", "S3", "S4", "S5")

_FALLBACK_ASSIGNMENT = (
    "Solve the subclaim assigned to your S-ID in the S0 blueprint's "
    "subproblem assignment table (section 6)."
)


@dataclass(frozen=True)
class ProblemInputs:
    """One target problem: skeleton, target, and optional private material."""

    problem_id: str
    target: str
    skeleton: str
    allowed_support: str | None = None  # None -> packet default rule
    initial_guidance: list[str] = field(default_factory=list)
    bibliography: str | None = None
    gold_proof: str | None = None  # enables the privileged Final Checker
    full_source: str | None = None

    @classmethod
    def load(cls, problem_dir: str | Path) -> "ProblemInputs":
        """Load a problem directory.

        Required: ``target.md`` and one of ``skeleton.md`` / ``skeleton.tex``.
        Optional: ``allowed_support.md``, ``guidance.md`` (one item per
        non-empty line), ``bibliography.bib`` / ``bibliography.bbl`` /
        ``bibliography.md``, ``private/gold_proof.md``, ``private/source.md``.
        """

        directory = Path(problem_dir)
        target_path = directory / "target.md"
        if not target_path.exists():
            raise FileNotFoundError(f"missing required problem file: {target_path}")
        skeleton_path = directory / "skeleton.md"
        if not skeleton_path.exists():
            skeleton_path = directory / "skeleton.tex"
        if not skeleton_path.exists():
            raise FileNotFoundError(f"missing required skeleton.md or skeleton.tex in {directory}")
        allowed_path = directory / "allowed_support.md"
        guidance_path = directory / "guidance.md"
        gold_path = directory / "private" / "gold_proof.md"
        source_path = directory / "private" / "source.md"
        bibliography_path = next(
            (
                directory / name
                for name in ("bibliography.bib", "bibliography.bbl", "bibliography.md")
                if (directory / name).exists()
            ),
            None,
        )
        guidance: list[str] = []
        if guidance_path.exists():
            guidance = [
                line.strip().lstrip("0123456789.").strip()
                for line in guidance_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
        return cls(
            problem_id=directory.name,
            target=target_path.read_text(encoding="utf-8").strip(),
            skeleton=skeleton_path.read_text(encoding="utf-8").strip(),
            allowed_support=(
                allowed_path.read_text(encoding="utf-8").strip() if allowed_path.exists() else None
            ),
            initial_guidance=guidance,
            bibliography=(
                bibliography_path.read_text(encoding="utf-8").strip()
                if bibliography_path is not None
                else None
            ),
            gold_proof=gold_path.read_text(encoding="utf-8").strip() if gold_path.exists() else None,
            full_source=source_path.read_text(encoding="utf-8").strip() if source_path.exists() else None,
        )


@dataclass(frozen=True)
class OpenRunConfig:
    """Loop bounds for one autonomous run (controller caps live separately)."""

    max_rounds: int = 12
    run_verifiers: bool = True
    solver_workers: int = 5  # S1-S5 fan-out
    solver_delay_seconds: float = 0.0  # inter-call pause (sequential mode only)
    pre_round_delay_seconds: float = 0.0  # sleep before S0 to let TPM window reset
    citation_max_attempts: int = 2  # citation-only repair attempts for one proof
    verifier_a_runs: int = 3  # required A1/A2/A3 ensemble
    key_solver_id: str | None = None  # optional fixed S1-S5 id for key-model routing


@dataclass
class _BranchRegistry:
    """Run-wide branch counter shared by the main pipeline and its children."""

    opened: int = 0


class OpenProblemOrchestrator:
    """Run one pipeline (the main problem or a branch lemma) to a terminal state."""

    def __init__(
        self,
        problem: ProblemInputs,
        caller: AgentCaller,
        store: OpenRunStore,
        config: OpenRunConfig | None = None,
        controller_config: ControllerConfig | None = None,
        progress: Callable[[str], None] | None = None,
        depth: int = 0,
        branch_registry: _BranchRegistry | None = None,
    ) -> None:
        self.problem = problem
        self.caller = caller
        self.store = store
        self.config = config or OpenRunConfig()
        self.controller_config = controller_config or ControllerConfig()
        self.progress = progress
        self.depth = depth
        self.branch_registry = branch_registry or _BranchRegistry()

    # ------------------------------------------------------------------ run

    def run(self) -> PipelineState:
        state = self.store.load_state()
        if state is None:
            state = PipelineState(
                problem_id=self.problem.problem_id,
                guidance=list(self.problem.initial_guidance),
                depth=self.depth,
            )
        self.branch_registry.opened = max(self.branch_registry.opened, state.branch_count)
        while state.status == STATUS_RUNNING:
            if state.round_index >= self.config.max_rounds:
                state.status = STATUS_STOPPED_MAX_ROUNDS
                state.stop_reason = f"max_rounds={self.config.max_rounds} reached"
                break
            round_no = state.round_index + 1
            self._emit(f"round {round_no} start (guidance items: {len(state.guidance)})")
            try:
                self._run_round(round_no, state)
            except BaseException:
                # A crashed round (API failure, Ctrl-C, ...) must not consume a
                # round number: on --resume the same round is redone from S0.
                # Persist guidance/branch state so nothing already decided is lost.
                state.branch_count = self.branch_registry.opened
                self.store.save_state(state)
                raise
            state.round_index = max(state.round_index, round_no)
            state.branch_count = self.branch_registry.opened
            self.store.save_state(state)
        self.store.save_state(state)
        self._emit(f"pipeline finished: status={state.status}")
        return state

    # ---------------------------------------------------------------- round

    def _run_round(self, round_no: int, state: PipelineState) -> None:
        guidance = list(state.guidance)

        # --- pre-round TPM breathing room -----------------------------------
        if self.config.pre_round_delay_seconds > 0:
            delay = self.config.pre_round_delay_seconds
            self._emit(f"round={round_no} pre-round delay {delay:g}s (letting TPM window reset)")
            time.sleep(delay)

        # --- S0 blueprint ---------------------------------------------------
        blueprint = self.caller.call_s0(
            self.problem.target, guidance, self.problem.skeleton, self.problem.allowed_support, round_no
        )
        self.store.save_text(round_no, "S0.md", blueprint)
        if has_setup_failure(blueprint):
            self._halt_for_setup_failure(round_no, state, "S0 reported SETUP FAILURE")
            return
        if has_leakage_marker(blueprint):
            self._halt_for_leakage(round_no, state, "S0")
            return
        assignments = parse_s0_assignments(blueprint)
        designated_key_solver_id = parse_s0_key_solver(blueprint)
        key_solver_first = self.caller.prompts.requires_key_solver_first
        if key_solver_first and designated_key_solver_id not in S_IDS:
            self._halt_for_setup_failure(
                round_no,
                state,
                "S0 did not designate exactly one valid key_solver_id",
            )
            return
        routing_key_solver_id = (
            self.config.key_solver_id
            or designated_key_solver_id
            or parse_s0_hardest_solver(blueprint)
        )
        if designated_key_solver_id is not None:
            self._emit(
                f"round {round_no} S0 designated key solver: {designated_key_solver_id}"
            )
        elif routing_key_solver_id is not None:
            self._emit(
                f"round {round_no} key-model solver selected: {routing_key_solver_id}"
            )

        # --- S1-S5: both canonical packets require the key-first schedule ----
        outputs: dict[str, str] = {}
        parsed_by_id: dict[str, SubproblemResult] = {}

        def call_subproblem(s_id: str) -> str:
            return self.caller.call_subproblem(
                s_id,
                self.problem.target,
                guidance,
                blueprint,
                assignments.get(s_id, _FALLBACK_ASSIGNMENT),
                self.problem.skeleton,
                self.problem.allowed_support,
                round_no,
                s_id == routing_key_solver_id,
            )

        def parse_and_store_subproblem(s_id: str, text: str) -> SubproblemResult:
            self.store.save_text(round_no, f"{s_id}.md", text)
            result = self._parse_subproblem_with_retry(text, s_id, round_no)
            self.store.save_parsed(round_no, s_id, result.to_dict())
            outputs[s_id] = text
            parsed_by_id[s_id] = result
            return result

        def call_subproblems(
            s_ids: list[str], *, delay_before_first: bool = False
        ) -> dict[str, str]:
            if self.config.solver_workers <= 1 and self.config.solver_delay_seconds > 0:
                called: dict[str, str] = {}
                for index, s_id in enumerate(s_ids):
                    if delay_before_first or index > 0:
                        delay = self.config.solver_delay_seconds
                        self._emit(
                            f"round={round_no} waiting {delay:g}s before {s_id} call"
                        )
                        time.sleep(delay)
                    called[s_id] = call_subproblem(s_id)
                return called

            workers = max(1, min(self.config.solver_workers, len(s_ids)))
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {
                    s_id: executor.submit(call_subproblem, s_id) for s_id in s_ids
                }
                return {s_id: future.result() for s_id, future in futures.items()}

        if key_solver_first:
            assert designated_key_solver_id is not None
            key_result = parse_and_store_subproblem(
                designated_key_solver_id,
                call_subproblem(designated_key_solver_id),
            )
            if has_leakage_marker(outputs[designated_key_solver_id]):
                self._halt_for_leakage(round_no, state, designated_key_solver_id)
                return
            if key_result.setup_failure:
                self._halt_for_setup_failure(
                    round_no,
                    state,
                    f"{designated_key_solver_id} reported SETUP FAILURE",
                )
                return
            if not key_result.solved:
                gate_composed = ComposedProofResult(complete=False)
                gate_subproblems = [key_result]
                decision = decide_solver_stage(
                    gate_composed,
                    gate_subproblems,
                    state,
                    self.controller_config,
                )
                if decision.outcome == OUTCOME_OPEN_BRANCH:
                    decision = self._run_branch(
                        round_no,
                        decision,
                        gate_composed,
                        gate_subproblems,
                        state,
                    )
                self.store.save_parsed(
                    round_no,
                    "key_solver_gate",
                    {
                        "key_solver_id": designated_key_solver_id,
                        "result": key_result.to_dict(),
                        "decision": decision.to_dict(),
                        "skipped_solvers": [
                            s_id for s_id in S_IDS if s_id != designated_key_solver_id
                        ],
                        "skipped_s6": True,
                    },
                )
                self.store.save_decision(round_no, decision)
                self._emit(
                    f"round={round_no} key solver {designated_key_solver_id} did not "
                    "solve its assignment; skipped remaining siblings and S6"
                )
                self._apply_solver_outcome(decision, state)
                return

        remaining_ids = [s_id for s_id in S_IDS if s_id not in parsed_by_id]
        remaining_outputs = call_subproblems(
            remaining_ids,
            delay_before_first=key_solver_first,
        )
        for s_id in remaining_ids:
            parse_and_store_subproblem(s_id, remaining_outputs[s_id])

        subproblems = [parsed_by_id[s_id] for s_id in S_IDS]
        leaked = [s_id for s_id in S_IDS if has_leakage_marker(outputs[s_id])]
        if leaked:
            self._halt_for_leakage(round_no, state, ", ".join(leaked))
            return

        # --- S6 composition ---------------------------------------------------
        joined_outputs = "\n\n".join(
            f"### {s_id} output\n\n{outputs[s_id].strip()}" for s_id in S_IDS
        )
        s6_text = self.caller.call_s6(
            self.problem.target,
            guidance,
            blueprint,
            joined_outputs,
            self.problem.skeleton,
            self.problem.allowed_support,
            round_no,
        )
        self.store.save_text(round_no, "S6.md", s6_text)
        # Split S6 into file-level artifacts. The proof remains a candidate
        # until sealed branch proofs have been integrity-checked and attached.
        s6_artifacts = derive_s6_artifact_files(s6_text)
        candidate_proof = s6_artifacts.pop("final_proof.md", "")
        candidate_tex = s6_artifacts.pop("final_proof.tex", "")
        if not candidate_proof:
            candidate_proof = s6_text
        self.store.save_text(round_no, "candidate_final_proof.md", candidate_proof)
        if candidate_tex:
            self.store.save_text(round_no, "candidate_final_proof.tex", candidate_tex)
        for artifact_name, artifact_text in s6_artifacts.items():
            self.store.save_text(round_no, artifact_name, artifact_text)
        if has_leakage_marker(s6_text):
            self._halt_for_leakage(round_no, state, "S6")
            return
        composed = self._parse_composer_with_retry(s6_text, round_no)
        self.store.save_parsed(round_no, "S6", composed.to_dict())

        # --- Controller: solver stage ---------------------------------------
        decision = decide_solver_stage(composed, subproblems, state, self.controller_config)
        self.store.save_decision(round_no, decision)

        if decision.outcome == OUTCOME_RUN_VERIFICATION:
            proof_package, assembly_report = build_final_proof_package(
                candidate_proof,
                state.sealed_branch_proofs,
                self.store.root,
            )
            assembled_proof = proof_package.final_proof_md
            self.store.save_parsed(round_no, "sealed_proof_assembly", assembly_report.to_dict())
            if not assembly_report.passed:
                decision = ControllerDecision(
                    outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
                    rule_fired="sealed_proof_assembly_failed",
                    stage="final_assembly",
                    adjudication_kind="artifact_integrity",
                    notes="; ".join(assembly_report.violations),
                )
                self.store.save_decision(round_no, decision)
                self._apply_solver_outcome(decision, state)
                return
            self.store.save_text(round_no, "final_proof.md", assembled_proof)
            for artifact_name, artifact_text in proof_package.module_files.items():
                self.store.save_text(round_no, artifact_name, artifact_text)
            if proof_package.proof_guide_md:
                self.store.save_text(round_no, "PROOF_GUIDE.md", proof_package.proof_guide_md)
            if proof_package.proof_registry_json:
                self.store.save_text(
                    round_no,
                    "proof_registry.json",
                    proof_package.proof_registry_json,
                )
            if proof_package.professor_source_md:
                self.store.save_text(
                    round_no,
                    "professor_source.md",
                    proof_package.professor_source_md,
                )
            if proof_package.final_proof_tex:
                self.store.save_text(
                    round_no,
                    "final_proof.tex",
                    proof_package.final_proof_tex,
                )
            elif candidate_tex and not state.sealed_branch_proofs:
                self.store.save_text(round_no, "final_proof.tex", candidate_tex)
            artifact = self._proof_artifact(
                blueprint,
                joined_outputs,
                s6_text,
                assembled_proof,
            )
            final = self._run_cascade(
                round_no,
                artifact,
                assembled_proof,
                s6_artifacts.get("source_ledger.md", ""),
                state,
            )
            self.store.save_decision(round_no, final)
            self._apply_cascade_outcome(final, round_no, state)
            return

        if decision.outcome == OUTCOME_OPEN_BRANCH:
            decision = self._run_branch(round_no, decision, composed, subproblems, state)
            self.store.save_decision(round_no, decision)

        self._apply_solver_outcome(decision, state)

    # ------------------------------------------------------------- branches

    def _run_branch(
        self,
        round_no: int,
        decision: ControllerDecision,
        composed: ComposedProofResult,
        subproblems: list[SubproblemResult],
        state: PipelineState,
    ) -> ControllerDecision:
        """Run one nested pipeline on the candidate lemma; collapse its outcome."""

        lemma = decision.branch_lemma
        assert lemma is not None  # decide_solver_stage only branches with a lemma
        self.branch_registry.opened += 1
        branch_index = self.branch_registry.opened
        slug = slugify(lemma.lemma_statement)
        branch_store = OpenRunStore(self.store.branch_root(branch_index, slug))
        branch_store.write_parent_note(
            "This branch pipeline was opened automatically.\n\n"
            f"Parent problem: {self.problem.problem_id}\n"
            f"Parent round: {round_no}\n"
            f"Proposing solver: {decision.guidance_source}\n\n"
            "Candidate lemma (the branch target):\n\n"
            f"{lemma.lemma_statement}\n\n"
            "Why the parent needs it:\n\n"
            f"{lemma.why_unblocks or 'Not stated.'}"
        )
        branch_problem = ProblemInputs(
            problem_id=f"branch_{branch_index:03d}_{slug}",
            target=lemma.lemma_statement,
            skeleton=self.problem.skeleton,
            allowed_support=lemma.allowed_inputs or self.problem.allowed_support,
            initial_guidance=[],  # branches start with an empty guidance list
            bibliography=self.problem.bibliography,
        )
        branch_caller = replace(
            self.caller,
            base_metadata={
                **self.caller.base_metadata,
                "pipeline": branch_problem.problem_id,
                "depth": self.depth + 1,
            },
        )
        self._emit(f"opening branch {branch_problem.problem_id} on: {lemma.lemma_statement[:80]}")
        branch = OpenProblemOrchestrator(
            problem=branch_problem,
            caller=branch_caller,
            store=branch_store,
            config=self.config,
            controller_config=self.controller_config,
            progress=self.progress,
            depth=self.depth + 1,
            branch_registry=self.branch_registry,
        )
        branch_state = branch.run()

        kind, sentence = collapse_branch_outcome(lemma.lemma_statement, branch_state)
        self._emit(f"branch {branch_problem.problem_id} collapsed: {kind}")
        if kind in {"proved", "disproved"}:
            if budget_exhausted(state, self.controller_config):
                return ControllerDecision(
                    outcome=OUTCOME_STOPPED_BUDGET,
                    rule_fired=f"branch_{kind}_budget_exhausted",
                    stage="solver",
                    notes="Not reproduced within the 10-guidance budget.",
                )
            sealed_proof = None
            if kind == "proved":
                if branch_state.final_proof_round is None:
                    return ControllerDecision(
                        outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
                        rule_fired="accepted_branch_missing_final_round",
                        stage="solver",
                        adjudication_kind="artifact_integrity",
                        notes=(
                            f"Accepted branch {branch_problem.problem_id} has no final proof round."
                        ),
                    )
                branch_proof_path = (
                    branch_store.round_dir(branch_state.final_proof_round) / "final_proof.md"
                )
                if not branch_proof_path.is_file():
                    return ControllerDecision(
                        outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
                        rule_fired="accepted_branch_missing_proof_artifact",
                        stage="solver",
                        adjudication_kind="artifact_integrity",
                        notes=f"Accepted branch proof is missing: {branch_proof_path}",
                    )
                proof_id = f"E{branch_index:03d}"
                branch_proof = branch_proof_path.read_text(encoding="utf-8")
                copied_path = self.store.save_text(
                    round_no,
                    f"sealed_branch_proofs/{proof_id}_{slug}.md",
                    branch_proof,
                )
                copied_text = copied_path.read_text(encoding="utf-8")
                sealed_proof = SealedBranchProof(
                    proof_id=proof_id,
                    lemma_statement=lemma.lemma_statement.strip(),
                    artifact_path=copied_path.relative_to(self.store.root).as_posix(),
                    source_problem_id=branch_problem.problem_id,
                    source_round=branch_state.final_proof_round,
                    proof_sha256=sha256_text(copied_text),
                    where_used=lemma.where_used.strip() or lemma.why_unblocks.strip(),
                    dependencies=[item.proof_id for item in branch_state.sealed_branch_proofs],
                )
                sentence = _internal_branch_guidance(sealed_proof)
            return ControllerDecision(
                outcome=OUTCOME_RERUN_WITH_GUIDANCE,
                rule_fired=f"branch_{kind}",
                stage="solver",
                guidance_sentence=sentence,
                guidance_source=f"branch:{branch_problem.problem_id}",
                sealed_branch_proof=sealed_proof,
            )
        # Inconclusive branch: reconsider this round's pool without branching.
        return decide_solver_stage(
            composed, subproblems, state, self.controller_config, allow_branches=False
        )

    # ------------------------------------------------------------- cascade

    def _run_cascade(
        self,
        round_no: int,
        proof_artifact: str,
        final_proof: str,
        solver_source_ledger: str,
        state: PipelineState,
    ) -> ControllerDecision:
        """Problem-statement gate -> citation gate -> A ensemble -> Composer A -> B -> C."""

        statement_text = self.caller.call_problem_statement_verifier(
            target=self.problem.target,
            artifact_role="Solver proof",
            agent_output=proof_artifact,
            skeleton=self.problem.skeleton,
            round_index=round_no,
        )
        self.store.save_text(round_no, "problem_statement_verifier.md", statement_text)
        statement_report = parse_problem_statement_report(statement_text)
        self.store.save_parsed(
            round_no, "problem_statement_verifier", statement_report.to_dict()
        )
        statement_decision = route_after_problem_statement_verifier(
            statement_report, state, self.controller_config
        )
        self.store.save_decision(round_no, statement_decision)
        if statement_decision.outcome != OUTCOME_RUN_NEXT_STAGE:
            return statement_decision

        citation_decision, source_ledger, citation_report = self._run_citation_layer(
            round_no,
            final_proof,
            solver_source_ledger,
            state,
        )
        self.store.save_decision(round_no, citation_decision)
        if citation_decision.outcome != OUTCOME_RUN_NEXT_STAGE:
            return citation_decision

        gold_available = self.problem.gold_proof is not None
        if not self.config.run_verifiers:
            if not gold_available:
                return ControllerDecision(
                    outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
                    rule_fired="verifiers_skipped_no_gold",
                    stage="final_checker",
                    adjudication_kind="math_gap",
                    notes=(
                        "Verifier cascade was skipped (--no-verifiers) and no gold proof "
                        "is available; this is a solver-only candidate requiring human review."
                    ),
                )
            return self._final_gate(
                round_no, final_proof, gold_available, list(state.guidance)
            )

        # A1..A3 in parallel, then Composer A merges the reports.
        labels = [f"A{i}" for i in range(1, self.config.verifier_a_runs + 1)]
        reports: dict[str, str] = {}
        with ThreadPoolExecutor(max_workers=len(labels)) as executor:
            futures = {
                label: executor.submit(
                    self.caller.call_verifier_a,
                    label,
                    self.problem.target,
                    list(state.guidance),
                    proof_artifact,
                    self.problem.skeleton,
                    self.problem.allowed_support,
                    round_no,
                    source_ledger,
                    citation_report,
                )
                for label in labels
            }
            for label, future in futures.items():
                reports[label] = future.result()
        for label in labels:
            self.store.save_text(round_no, f"verifier_{label.lower()}.md", reports[label])
        composer_text = self.caller.call_composer_a([reports[label] for label in labels], round_no)
        self.store.save_text(round_no, "composer_a.md", composer_text)
        gold_report = parse_composer_a_report(composer_text)
        self.store.save_parsed(round_no, "composer_a", gold_report.to_dict())
        decision = route_after_composer_a(gold_report, state, self.controller_config)
        self.store.save_decision(round_no, decision)
        if decision.outcome != OUTCOME_RUN_NEXT_STAGE:
            return decision
        a_status = derive_a_status(gold_report)

        b_text = self.caller.call_verifier_b(
            self.problem.target,
            list(state.guidance),
            proof_artifact,
            self.problem.skeleton,
            self.problem.allowed_support,
            round_no,
            source_ledger,
            citation_report,
        )
        self.store.save_text(round_no, "verifier_b.md", b_text)
        b_report = parse_verifier_b_report(b_text)
        self.store.save_parsed(round_no, "verifier_b", b_report.to_dict())
        decision = route_after_verifier_b(b_report, state, self.controller_config)
        self.store.save_decision(round_no, decision)
        if decision.outcome != OUTCOME_RUN_NEXT_STAGE:
            return decision

        c_text = self.caller.call_verifier_c(
            self.problem.target,
            list(state.guidance),
            proof_artifact,
            self.problem.skeleton,
            self.problem.allowed_support,
            round_no,
            source_ledger,
            citation_report,
        )
        self.store.save_text(round_no, "verifier_c.md", c_text)
        c_report = parse_verifier_c_report(c_text)
        self.store.save_parsed(round_no, "verifier_c", c_report.to_dict())
        decision = route_after_verifier_c(c_report, a_status, state, self.controller_config)
        self.store.save_decision(round_no, decision)
        if decision.outcome != OUTCOME_RUN_NEXT_STAGE:
            return decision

        return self._final_gate(round_no, final_proof, gold_available, list(state.guidance))

    def _run_citation_layer(
        self,
        round_no: int,
        final_proof: str,
        solver_source_ledger: str,
        state: PipelineState,
    ) -> tuple[ControllerDecision, str, str]:
        """Run citation-only repairs, then map the final gate result to routing."""

        root = self.store.round_dir(round_no) / "citation_gate"
        attempts = max(1, self.config.citation_max_attempts)
        gate = None
        attempt_dir = root
        for attempt in range(1, attempts + 1):
            attempt_dir = root / f"attempt_{attempt:03d}"
            gate = self.caller.call_citation_gate(
                output_dir=attempt_dir,
                target=self.problem.target,
                provided_packet=self.problem.skeleton,
                allowed_support=self.problem.allowed_support,
                guidance=list(state.guidance),
                proof=final_proof,
                solver_source_ledger=solver_source_ledger,
                bibliography=self.problem.bibliography,
                round_index=round_no,
                attempt=attempt,
            )
            if gate.gate_result != "SOURCE_LEDGER_REPAIR_NEEDED" or attempt == attempts:
                break
            self._emit(
                f"round={round_no} citation ledger repair; retrying citation layer "
                f"({attempt + 1}/{attempts})"
            )

        assert gate is not None
        decision = route_after_citation_gate(
            gate.gate_result,
            gate.candidate_guidance_seed,
            gate.reason,
            state,
            self.controller_config,
        )
        write_json(
            root / "citation_gate_summary.json",
            {
                "attempts_run": attempt,
                "max_attempts": attempts,
                "final_gate": gate.to_dict(),
                "controller_decision": decision.to_dict(),
            },
        )
        source_ledger = _read_optional_text(
            attempt_dir / "citation_generator_output.md"
        )
        citation_report = _read_optional_text(
            attempt_dir / "citation_verifier_output.md"
        )
        return decision, source_ledger, citation_report

    def _final_gate(
        self,
        round_no: int,
        final_proof: str,
        gold_available: bool,
        guidance: list[str],
    ) -> ControllerDecision:
        """Final Checker in gold mode; cascade-only acceptance otherwise."""

        if not gold_available:
            return route_final(None, gold_available=False)
        checker_text = self.caller.call_final_checker(
            self.problem.target,
            self.problem.skeleton,
            final_proof,
            self.problem.gold_proof or "",
            self.problem.full_source,
            guidance,
            round_no,
        )
        self.store.save_text(round_no, "final_checker.json", checker_text)
        try:
            verdict = parse_final_checker_output(checker_text)
        except Exception as exc:  # noqa: BLE001 - unparseable verdict -> human review
            return ControllerDecision(
                outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
                rule_fired="final_checker_unparseable",
                stage="final_checker",
                adjudication_kind="math_gap",
                notes=f"Final Checker output could not be parsed: {exc}",
            )
        self.store.save_parsed(round_no, "final_checker", verdict.to_dict())
        return route_final(verdict, gold_available=True)

    # ------------------------------------------------------------ outcomes

    def _apply_solver_outcome(self, decision: ControllerDecision, state: PipelineState) -> None:
        if decision.outcome == OUTCOME_RERUN_WITH_GUIDANCE:
            sealed = decision.sealed_branch_proof
            if sealed is not None:
                existing = next(
                    (
                        item
                        for item in state.sealed_branch_proofs
                        if item.proof_id == sealed.proof_id
                    ),
                    None,
                )
                if existing is not None and existing != sealed:
                    state.status = STATUS_NEEDS_HUMAN_REVIEW
                    state.stop_reason = (
                        f"Conflicting sealed proof metadata for {sealed.proof_id}."
                    )
                    return
                if existing is None:
                    state.sealed_branch_proofs.append(sealed)
            state.guidance.append(decision.guidance_sentence)
            state.consecutive_no_guidance = 0
            self._emit(f"guidance appended ({decision.guidance_source}): {decision.guidance_sentence[:100]}")
            return
        if decision.outcome == OUTCOME_RERUN_UNCHANGED:
            state.consecutive_no_guidance += 1
            return
        if decision.outcome == OUTCOME_NEEDS_HUMAN_REVIEW:
            state.status = STATUS_NEEDS_HUMAN_REVIEW
            state.stop_reason = decision.notes or decision.rule_fired
            return
        if decision.outcome == OUTCOME_STOPPED_BUDGET:
            state.status = STATUS_STOPPED_BUDGET
            state.stop_reason = "Not reproduced within the 10-guidance budget."
            return
        raise ValueError(f"unexpected solver-stage outcome: {decision.outcome}")

    def _apply_cascade_outcome(
        self, decision: ControllerDecision, round_no: int, state: PipelineState
    ) -> None:
        if decision.outcome == OUTCOME_ACCEPTED:
            state.status = STATUS_ACCEPTED
            state.final_proof_round = round_no
            return
        if decision.outcome == OUTCOME_ACCEPTED_CASCADE_ONLY:
            state.status = STATUS_ACCEPTED_CASCADE_ONLY
            state.final_proof_round = round_no
            return
        if decision.outcome == OUTCOME_REJECTED_FINAL_CHECK:
            state.status = STATUS_REJECTED_FINAL_CHECK
            state.stop_reason = decision.notes or "Final Checker FAIL is terminal."
            return
        # Rerun-with-guidance / human-review / budget outcomes route like the
        # solver stage.
        self._apply_solver_outcome(decision, state)

    def _halt_for_setup_failure(self, round_no: int, state: PipelineState, note: str) -> None:
        decision = ControllerDecision(
            outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
            rule_fired="setup_failure",
            stage="solver",
            adjudication_kind="setup",
            notes=note,
        )
        self.store.save_decision(round_no, decision)
        state.status = STATUS_NEEDS_HUMAN_REVIEW
        state.stop_reason = note

    def _halt_for_leakage(self, round_no: int, state: PipelineState, roles: str) -> None:
        """Packet Operating Rule 2: an internet-enabled role that reports
        'Possible target-source leakage encountered.' stops the run; the
        controller (human) then voids it or reviews it manually. This is an
        absorbing hard gate, never a proof failure and never a guidance item.
        """

        note = (
            f"Possible target-source leakage encountered (reported by {roles}). "
            "Void the run or review it manually per Operating Rule 2."
        )
        decision = ControllerDecision(
            outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
            rule_fired="target_source_leakage",
            stage="solver",
            adjudication_kind="source_hygiene",
            notes=note,
        )
        self.store.save_decision(round_no, decision)
        state.status = STATUS_NEEDS_HUMAN_REVIEW
        state.stop_reason = note

    # ------------------------------------------------------------- parsing

    def _parse_subproblem_with_retry(self, text: str, s_id: str, round_no: int) -> SubproblemResult:
        result = parse_subproblem_output(text, s_id)
        if result.solved or result.failure.failure_output_type != UNPARSEABLE:
            return result
        data = self.caller.reformat_failure_output(text, round_no)
        if data is None:
            return result
        failure = _failure_from_reformat(data, s_id)
        return SubproblemResult(
            s_id=s_id, solved=False, failure=failure, setup_failure=result.setup_failure
        )

    def _parse_composer_with_retry(self, text: str, round_no: int) -> ComposedProofResult:
        result = parse_composer_output(text)
        if result.complete or (
            result.failure is not None and result.failure.failure_output_type != UNPARSEABLE
        ):
            return result
        data = self.caller.reformat_failure_output(text, round_no)
        if data is None:
            return result
        return ComposedProofResult(
            complete=False,
            failure=_failure_from_reformat(data, "S6"),
            setup_failure=result.setup_failure,
        )

    @staticmethod
    def _proof_artifact(
        blueprint: str,
        joined_outputs: str,
        s6_text: str,
        final_proof: str,
    ) -> str:
        """Verifier artifact: current-round provenance plus assembled final proof."""

        return (
            "## S0 blueprint\n\n"
            f"{blueprint.strip()}\n\n"
            "## S1-S5 subproblem outputs\n\n"
            f"{joined_outputs.strip()}\n\n"
            "## S6 composed final proof\n\n"
            f"{s6_text.strip()}\n\n"
            "## Final verifier-facing proof\n\n"
            f"{final_proof.strip()}"
        )

    def _emit(self, message: str) -> None:
        if self.progress is not None:
            label = self.problem.problem_id if self.depth else "main"
            self.progress(f"[{label}] {message}")


def _internal_branch_guidance(record: SealedBranchProof) -> str:
    """Statement-only guidance released after an isolated branch is accepted."""

    where_used = record.where_used.strip() or "Use only where its exact statement applies."
    return (
        f"[INTERNALLY VERIFIED AUXILIARY RESULT {record.proof_id}]\n"
        f"Statement: {record.lemma_statement.strip()}\n"
        "Status: independently verified in an isolated branch.\n"
        "Permission: may be used without reproof; infer nothing stronger than the exact statement.\n"
        f"Use location: {where_used}"
    )


def _failure_from_reformat(data: dict, source: str) -> SolverFailureOutput:
    """Build a failure record from the mechanical reformatter's JSON."""

    failure_type = normalize_failure_type(str(data.get("failure_output_type", "")))
    if failure_type == UNPARSEABLE:
        failure_type = "no_useful_guidance"
    branch: BranchLemmaCandidate | None = None
    if failure_type == BRANCH_LEMMA:
        branch = BranchLemmaCandidate(
            lemma_statement=str(data.get("candidate_lemma_statement", "")),
            equivalent_or_stronger=normalize_tristate(str(data.get("lemma_equivalent_or_stronger", ""))),
            recommended=normalize_tristate(str(data.get("lemma_recommended", ""))),
        )
    return SolverFailureOutput(
        source=source,
        failure_output_type=failure_type,
        type_detail=str(data.get("type", "")),
        failed_route=str(data.get("failed_route", "")),
        obstruction=str(data.get("obstruction", "")),
        evidence=str(data.get("evidence", "")),
        reuse_value=str(data.get("reuse_value", "")),
        guidance_sentence=str(data.get("guidance_sentence", "")),
        branch_lemma=branch,
    )


def _read_optional_text(path: Path) -> str:
    """Read an optional citation artifact without masking gate decisions."""

    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8").strip()
