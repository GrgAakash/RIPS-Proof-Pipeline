"""Typed records for the autonomous S0-S6 open-problem workflow.

Every record mirrors one structured artifact of the protocol in
``Prompt Packet/PromptsWithFullInternet.md``:

- ``SolverFailureOutput``  -> the "Solver failure output and candidate guidance"
  section that S1-S5 and S6 must emit (solved / forbidden-route / branch lemma /
  ordinary hint / no useful guidance).
- ``BranchLemmaCandidate`` -> the branch-lemma fields of that section.
- ``SubproblemResult``     -> one S1-S5 run, parsed.
- ``ComposedProofResult``  -> one S6 run, parsed.
- ``ProblemStatementReport`` -> the exact-target alignment gate after S6.
- ``ComposerAGoldReport``  -> Composer A's "Gold Verifier A evidence report".
- ``VerifierBReport``      -> Verifier B's final summary fields.
- ``VerifierCReport``      -> Verifier C's final summary fields.
- ``FinalCheckerDecision`` -> the privileged Final Checker JSON.
- ``ControllerDecision``   -> one deterministic routing decision.
- ``PipelineState``        -> persisted per-pipeline state (guidance list,
  budget, round index, branch registry).

Unlike the legacy benchmark records, these records are parsed from *labeled
markdown* authored by models, so fields default to tolerant values ("unclear",
empty strings) instead of raising. Normalization of raw text into the canonical
enums below lives in ``report_parsers.py``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


# --- Canonical failure output types (protocol section 3 of S1-S5 / S6) -------
SOLVED = "solved"
FORBIDDEN_ROUTE = "forbidden_route"
BRANCH_LEMMA = "branch_lemma"
ORDINARY_HINT = "ordinary_hint"
NO_USEFUL_GUIDANCE = "no_useful_guidance"
UNPARSEABLE = "unparseable"

FAILURE_OUTPUT_TYPES = (
    SOLVED,
    FORBIDDEN_ROUTE,
    BRANCH_LEMMA,
    ORDINARY_HINT,
    NO_USEFUL_GUIDANCE,
    UNPARSEABLE,
)

# Priority order for selecting the single guidance item of a failed round.
# Lower index = stronger. UNPARSEABLE is treated like NO_USEFUL_GUIDANCE.
FAILURE_PRIORITY = {
    FORBIDDEN_ROUTE: 0,
    BRANCH_LEMMA: 1,
    ORDINARY_HINT: 2,
    NO_USEFUL_GUIDANCE: 3,
    UNPARSEABLE: 3,
    SOLVED: 4,
}

# --- Yes / no / unclear tri-state used across verifier summaries -------------
YES = "yes"
NO = "no"
UNCLEAR = "unclear"
NOT_APPLICABLE = "not_applicable"

# --- Controller outcomes ------------------------------------------------------
OUTCOME_RUN_VERIFICATION = "RUN_VERIFICATION"
OUTCOME_RERUN_WITH_GUIDANCE = "RERUN_WITH_GUIDANCE"
OUTCOME_OPEN_BRANCH = "OPEN_BRANCH"
OUTCOME_RERUN_UNCHANGED = "RERUN_UNCHANGED"
OUTCOME_NEEDS_HUMAN_REVIEW = "NEEDS_HUMAN_REVIEW"
OUTCOME_STOPPED_BUDGET = "STOPPED_BUDGET"
OUTCOME_RUN_NEXT_STAGE = "RUN_NEXT_STAGE"
OUTCOME_ACCEPTED = "ACCEPTED"
OUTCOME_ACCEPTED_CASCADE_ONLY = "ACCEPTED_CASCADE_ONLY"
OUTCOME_REJECTED_FINAL_CHECK = "REJECTED_FINAL_CHECK"

# --- Derived Verifier A statuses (decision tree, Step 2) ----------------------
A_VERIFIED = "A_VERIFIED"
A_ALMOST = "A_ALMOST"
A_NOT_VERIFIED = "A_NOT_VERIFIED"
A_INVALID = "A_INVALID"

# Pipeline terminal / running statuses persisted in state.json.
STATUS_RUNNING = "running"
STATUS_ACCEPTED = "accepted"
STATUS_ACCEPTED_CASCADE_ONLY = "accepted_cascade_only"
STATUS_REJECTED_FINAL_CHECK = "rejected_final_check"
STATUS_STOPPED_BUDGET = "stopped_budget"
STATUS_NEEDS_HUMAN_REVIEW = "needs_human_review"
STATUS_STOPPED_MAX_ROUNDS = "stopped_max_rounds"


@dataclass(frozen=True)
class BranchLemmaCandidate:
    """The branch-lemma fields a solver fills for ``branch lemma target``."""

    lemma_statement: str = ""
    why_unblocks: str = ""
    where_used: str = ""
    allowed_inputs: str = ""
    dependencies: str = ""
    weaker_than_target: str = UNCLEAR  # yes / no / unclear
    equivalent_or_stronger: str = UNCLEAR  # yes / no / unclear
    recommended: str = UNCLEAR  # yes / no / unclear

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BranchLemmaCandidate":
        return cls(
            lemma_statement=str(data.get("lemma_statement", "")),
            why_unblocks=str(data.get("why_unblocks", "")),
            where_used=str(data.get("where_used", "")),
            allowed_inputs=str(data.get("allowed_inputs", "")),
            dependencies=str(data.get("dependencies", "")),
            weaker_than_target=str(data.get("weaker_than_target", UNCLEAR)),
            equivalent_or_stronger=str(data.get("equivalent_or_stronger", UNCLEAR)),
            recommended=str(data.get("recommended", UNCLEAR)),
        )

    @property
    def branchable(self) -> bool:
        """Whether the solver's own flags permit opening a branch pipeline.

        The controller refuses to branch when the solver marked the lemma as
        (possibly) equivalent to / stronger than / downstream from the target,
        or explicitly recommended against a mini-pipeline, or gave no statement.
        """

        if not self.lemma_statement.strip():
            return False
        if self.equivalent_or_stronger == YES:
            return False
        if self.recommended == NO:
            return False
        return True


@dataclass(frozen=True)
class SealedBranchProof:
    """An accepted branch proof withheld from all later solver prompts.

    ``artifact_path`` is relative to the owning pipeline's run root. The
    deterministic final assembler verifies ``proof_sha256`` before attaching
    the proof to the verifier-facing final artifact.
    """

    proof_id: str
    lemma_statement: str
    artifact_path: str
    source_problem_id: str
    source_round: int
    proof_sha256: str
    where_used: str = ""
    dependencies: list[str] = field(default_factory=list)
    guidance_origin: str = "internal_branch"
    solver_received_statement: bool = True
    solver_received_proof: bool = False
    proof_attached_during_final_assembly: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SealedBranchProof":
        dependencies = data.get("dependencies", [])
        if isinstance(dependencies, str):
            dependencies = [dependencies]
        return cls(
            proof_id=str(data.get("proof_id", "")),
            lemma_statement=str(data.get("lemma_statement", "")),
            artifact_path=str(data.get("artifact_path", "")),
            source_problem_id=str(data.get("source_problem_id", "")),
            source_round=int(data.get("source_round", 0)),
            proof_sha256=str(data.get("proof_sha256", "")),
            where_used=str(data.get("where_used", "")),
            dependencies=[str(item) for item in dependencies],
            guidance_origin=str(data.get("guidance_origin", "internal_branch")),
            solver_received_statement=bool(data.get("solver_received_statement", True)),
            solver_received_proof=bool(data.get("solver_received_proof", False)),
            proof_attached_during_final_assembly=bool(
                data.get("proof_attached_during_final_assembly", True)
            ),
        )


@dataclass(frozen=True)
class SolverFailureOutput:
    """Section 3 of an S1-S5 / S6 output: the classified failure + guidance."""

    source: str  # "S1".."S6"
    failure_output_type: str  # one of FAILURE_OUTPUT_TYPES
    type_detail: str = ""  # counterexample / missing hypothesis / ...
    failed_route: str = ""
    obstruction: str = ""
    evidence: str = ""
    reuse_value: str = ""
    guidance_sentence: str = ""
    branch_lemma: BranchLemmaCandidate | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SolverFailureOutput":
        branch = data.get("branch_lemma")
        return cls(
            source=str(data.get("source", "")),
            failure_output_type=str(data.get("failure_output_type", UNPARSEABLE)),
            type_detail=str(data.get("type_detail", "")),
            failed_route=str(data.get("failed_route", "")),
            obstruction=str(data.get("obstruction", "")),
            evidence=str(data.get("evidence", "")),
            reuse_value=str(data.get("reuse_value", "")),
            guidance_sentence=str(data.get("guidance_sentence", "")),
            branch_lemma=None if branch is None else BranchLemmaCandidate.from_dict(branch),
        )

    @property
    def priority(self) -> int:
        return FAILURE_PRIORITY.get(self.failure_output_type, FAILURE_PRIORITY[NO_USEFUL_GUIDANCE])

    @property
    def has_usable_guidance(self) -> bool:
        """A candidate is usable only with a non-empty guidance sentence.

        Branch-lemma candidates are usable via ``branch_lemma`` instead, so they
        do not require a guidance sentence.
        """

        if self.failure_output_type == FORBIDDEN_ROUTE or self.failure_output_type == ORDINARY_HINT:
            sentence = self.guidance_sentence.strip()
            return bool(sentence) and sentence.lower() != "none"
        if self.failure_output_type == BRANCH_LEMMA:
            return self.branch_lemma is not None and bool(self.branch_lemma.lemma_statement.strip())
        return False


@dataclass(frozen=True)
class SubproblemResult:
    """One parsed S1-S5 run."""

    s_id: str  # "S1".."S5"
    solved: bool
    failure: SolverFailureOutput
    setup_failure: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "s_id": self.s_id,
            "solved": self.solved,
            "failure": self.failure.to_dict(),
            "setup_failure": self.setup_failure,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SubproblemResult":
        return cls(
            s_id=str(data.get("s_id", "")),
            solved=bool(data.get("solved", False)),
            failure=SolverFailureOutput.from_dict(data.get("failure", {})),
            setup_failure=bool(data.get("setup_failure", False)),
        )


@dataclass(frozen=True)
class ComposedProofResult:
    """One parsed S6 run: either a complete candidate proof or a failure output."""

    complete: bool
    proof_text: str = ""
    failure: SolverFailureOutput | None = None
    setup_failure: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "complete": self.complete,
            "proof_text": self.proof_text,
            "failure": None if self.failure is None else self.failure.to_dict(),
            "setup_failure": self.setup_failure,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ComposedProofResult":
        failure = data.get("failure")
        return cls(
            complete=bool(data.get("complete", False)),
            proof_text=str(data.get("proof_text", "")),
            failure=None if failure is None else SolverFailureOutput.from_dict(failure),
            setup_failure=bool(data.get("setup_failure", False)),
        )


@dataclass(frozen=True)
class ProblemStatementReport:
    """Problem Statement Verifier's controller-facing summary."""

    artifact_role: str = ""
    problem_statement_match: str = UNCLEAR  # yes / no / unclear
    actual_statement: str = ""
    mismatch_type: str = ""
    recommended_action: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProblemStatementReport":
        return cls(
            artifact_role=str(data.get("artifact_role", "")),
            problem_statement_match=str(data.get("problem_statement_match", UNCLEAR)),
            actual_statement=str(data.get("actual_statement", "")),
            mismatch_type=str(data.get("mismatch_type", "")),
            recommended_action=str(data.get("recommended_action", "")),
        )


@dataclass(frozen=True)
class ComposerAGoldReport:
    """Composer A's compact 'Gold Verifier A evidence report' fields."""

    non_fillable_gaps: str = UNCLEAR  # yes / no / unclear
    fillable_only_gaps: str = UNCLEAR
    disallowed_premises: str = UNCLEAR
    omitted_case_or_weaker: str = UNCLEAR
    standard_background_heavy: str = UNCLEAR
    web_source_issue: str = UNCLEAR
    recurring_issue: str = UNCLEAR
    no_majority: bool = False  # from the disagreement map
    guidance_seed: str = ""  # "" when the report says "None"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ComposerAGoldReport":
        return cls(
            non_fillable_gaps=str(data.get("non_fillable_gaps", UNCLEAR)),
            fillable_only_gaps=str(data.get("fillable_only_gaps", UNCLEAR)),
            disallowed_premises=str(data.get("disallowed_premises", UNCLEAR)),
            omitted_case_or_weaker=str(data.get("omitted_case_or_weaker", UNCLEAR)),
            standard_background_heavy=str(data.get("standard_background_heavy", UNCLEAR)),
            web_source_issue=str(data.get("web_source_issue", UNCLEAR)),
            recurring_issue=str(data.get("recurring_issue", UNCLEAR)),
            no_majority=bool(data.get("no_majority", False)),
            guidance_seed=str(data.get("guidance_seed", "")),
        )


@dataclass(frozen=True)
class VerifierBReport:
    """Verifier B final-summary fields (single weakest point + fillability)."""

    weakest_point_found: str = UNCLEAR  # yes / no / unclear
    weakest_point: str = ""
    missing_claim: str = ""
    fillable: str = UNCLEAR  # yes / no / not_applicable / unclear
    disallowed_premise: str = UNCLEAR  # yes / no / not_applicable / unclear

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VerifierBReport":
        return cls(
            weakest_point_found=str(data.get("weakest_point_found", UNCLEAR)),
            weakest_point=str(data.get("weakest_point", "")),
            missing_claim=str(data.get("missing_claim", "")),
            fillable=str(data.get("fillable", UNCLEAR)),
            disallowed_premise=str(data.get("disallowed_premise", UNCLEAR)),
        )


@dataclass(frozen=True)
class VerifierCReport:
    """Verifier C final-summary fields (adversarial break test)."""

    attack: str = ""
    broke: str = UNCLEAR  # yes / no / unsure / unclear
    failing_step: str = ""
    check_needed: str = ""
    disallowed_premise: str = UNCLEAR  # yes / no / unclear

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VerifierCReport":
        return cls(
            attack=str(data.get("attack", "")),
            broke=str(data.get("broke", UNCLEAR)),
            failing_step=str(data.get("failing_step", "")),
            check_needed=str(data.get("check_needed", "")),
            disallowed_premise=str(data.get("disallowed_premise", UNCLEAR)),
        )


@dataclass(frozen=True)
class FinalCheckerDecision:
    """The privileged Final Checker's JSON verdict.

    ``private_rationale`` stays in run artifacts only; it must never flow back
    into any solver or verifier prompt (a FAIL is terminal in this protocol).
    """

    decision: str  # "PASS" or "FAIL"
    failure_category: str = "none"  # none / mathematical / source / scope
    private_rationale: str = ""
    source_concern: str | None = None
    public_diagnosis: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FinalCheckerDecision":
        decision = str(data.get("decision", "")).strip().upper()
        if decision not in {"PASS", "FAIL"}:
            raise ValueError(f"FinalCheckerDecision.decision must be PASS or FAIL; got {decision!r}")
        diagnosis = data.get("public_diagnosis", [])
        if isinstance(diagnosis, str):
            diagnosis = [diagnosis]
        source_concern = data.get("source_concern")
        return cls(
            decision=decision,
            failure_category=str(data.get("failure_category", "none")),
            private_rationale=str(data.get("private_rationale", "")),
            source_concern=None if source_concern is None else str(source_concern),
            public_diagnosis=[str(item) for item in diagnosis],
        )


@dataclass(frozen=True)
class ControllerDecision:
    """One deterministic routing decision, persisted per round/stage."""

    outcome: str
    rule_fired: str
    stage: str  # solver / problem_statement_verifier / citation / verifier cascade
    guidance_sentence: str = ""  # nonempty only when a guidance item is appended
    guidance_source: str = ""  # e.g. "S4", "verifier_b", "branch:branch_001"
    branch_lemma: BranchLemmaCandidate | None = None
    sealed_branch_proof: SealedBranchProof | None = None
    adjudication_kind: str = ""  # math_gap / ... when NEEDS_HUMAN_REVIEW
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ControllerDecision":
        branch = data.get("branch_lemma")
        sealed = data.get("sealed_branch_proof")
        return cls(
            outcome=str(data.get("outcome", "")),
            rule_fired=str(data.get("rule_fired", "")),
            stage=str(data.get("stage", "")),
            guidance_sentence=str(data.get("guidance_sentence", "")),
            guidance_source=str(data.get("guidance_source", "")),
            branch_lemma=None if branch is None else BranchLemmaCandidate.from_dict(branch),
            sealed_branch_proof=(
                None if sealed is None else SealedBranchProof.from_dict(sealed)
            ),
            adjudication_kind=str(data.get("adjudication_kind", "")),
            notes=str(data.get("notes", "")),
        )


@dataclass
class PipelineState:
    """Persisted per-pipeline state (main run or one branch run)."""

    problem_id: str
    status: str = STATUS_RUNNING
    round_index: int = 0  # rounds completed so far
    guidance: list[str] = field(default_factory=list)
    sealed_branch_proofs: list[SealedBranchProof] = field(default_factory=list)
    branch_count: int = 0  # branches opened by this pipeline and its children
    depth: int = 0  # 0 = main pipeline
    consecutive_no_guidance: int = 0
    final_proof_round: int | None = None  # round whose S6 proof was accepted
    stop_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PipelineState":
        return cls(
            problem_id=str(data.get("problem_id", "")),
            status=str(data.get("status", STATUS_RUNNING)),
            round_index=int(data.get("round_index", 0)),
            guidance=[str(item) for item in data.get("guidance", [])],
            sealed_branch_proofs=[
                SealedBranchProof.from_dict(item)
                for item in data.get("sealed_branch_proofs", [])
            ],
            branch_count=int(data.get("branch_count", 0)),
            depth=int(data.get("depth", 0)),
            consecutive_no_guidance=int(data.get("consecutive_no_guidance", 0)),
            final_proof_round=(
                None if data.get("final_proof_round") is None else int(data["final_proof_round"])
            ),
            stop_reason=str(data.get("stop_reason", "")),
        )
