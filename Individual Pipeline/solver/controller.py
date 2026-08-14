"""Deterministic Decision Controller for the open-problem workflow.

This module is pure routing logic: no model calls, no filesystem access. It
implements, as code, the packet's Decision Controller rules ("can be temp chat,
manual, or deterministic code") for the stages the autonomous pipeline runs:

* Solver stage: pool the failure outputs of S6 and S1-S5, select at most ONE
  guidance action per round using the protocol priority
  forbidden-route > branch lemma > ordinary hint > no useful guidance.
* Citation gate: block Verifier A until Citation Verifier returns GOOD_TO_GO;
  source-ledger repairs rerun without guidance, substantive source failures
  may contribute exactly one guidance item, and leakage/unclear results stop.
* Verifier cascade: derive the Verifier A status from Composer A's gold report
  and walk decision-tree Steps 2-8 (disagreement gate, B fillability gate,
  C break gate, Final Checker gate, budget stop).

Invariants enforced here:

* At most one guidance item is appended per failed round.
* The 10-item guidance budget is absorbing: any rerun-with-guidance route hits
  STOPPED_BUDGET instead once the list is full.
* Guidance passed forward is always a single standalone sentence -- never a
  verifier report, a failed proof, or a branch transcript.
"""

from __future__ import annotations

from dataclasses import dataclass

from solver.schemas import (
    A_ALMOST,
    A_INVALID,
    A_NOT_VERIFIED,
    A_VERIFIED,
    BRANCH_LEMMA,
    ComposedProofResult,
    ComposerAGoldReport,
    ControllerDecision,
    FORBIDDEN_ROUTE,
    FinalCheckerDecision,
    NO,
    NOT_APPLICABLE,
    ORDINARY_HINT,
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
    ProblemStatementReport,
    SolverFailureOutput,
    SubproblemResult,
    UNCLEAR,
    YES,
)


@dataclass(frozen=True)
class ControllerConfig:
    """Caps and knobs for the deterministic controller."""

    max_guidance: int = 10  # protocol stopping rule: at most 10 guidance items
    max_branch_depth: int = 1  # 1 = main pipeline may branch; branches may not
    max_total_branches: int = 3  # branches opened across the whole run
    max_no_guidance_rounds: int = 1  # unchanged reruns tolerated before human review


def budget_exhausted(state: PipelineState, config: ControllerConfig) -> bool:
    return len(state.guidance) >= config.max_guidance


def pool_failure_candidates(
    composed: ComposedProofResult,
    subproblems: list[SubproblemResult],
) -> list[SolverFailureOutput]:
    """Collect this round's failure outputs, S6 first, sorted by protocol priority.

    Only unsolved outputs contribute. The sort is stable, so within one
    priority class S6's candidate wins, then S1..S5 in order -- the tie-break
    rule for selecting the single guidance item of the round.
    """

    candidates: list[SolverFailureOutput] = []
    if not composed.complete and composed.failure is not None:
        candidates.append(composed.failure)
    for result in subproblems:
        if not result.solved:
            candidates.append(result.failure)
    return sorted(candidates, key=lambda item: item.priority)


def decide_solver_stage(
    composed: ComposedProofResult,
    subproblems: list[SubproblemResult],
    state: PipelineState,
    config: ControllerConfig,
    allow_branches: bool = True,
) -> ControllerDecision:
    """Route one completed solver round (S0 -> S1-S5 -> S6).

    ``allow_branches=False`` re-routes after an inconclusive branch: the same
    candidate pool is reconsidered with branch-lemma candidates skipped so the
    controller falls through to the next-strongest item.
    """

    if composed.complete:
        return ControllerDecision(
            outcome=OUTCOME_RUN_VERIFICATION,
            rule_fired="s6_complete",
            stage="solver",
        )

    for candidate in pool_failure_candidates(composed, subproblems):
        if candidate.failure_output_type == FORBIDDEN_ROUTE and candidate.has_usable_guidance:
            return _guidance_or_budget(
                state,
                config,
                stage="solver",
                rule="forbidden_route",
                sentence=candidate.guidance_sentence,
                source=candidate.source,
            )
        if candidate.failure_output_type == BRANCH_LEMMA and allow_branches:
            lemma = candidate.branch_lemma
            if lemma is None or not lemma.branchable:
                continue  # solver's own flags forbid branching; downgrade
            if state.depth + 1 > config.max_branch_depth:
                continue
            if state.branch_count >= config.max_total_branches:
                continue
            if budget_exhausted(state, config):
                # A branch outcome would need a guidance slot to return through.
                return ControllerDecision(
                    outcome=OUTCOME_STOPPED_BUDGET,
                    rule_fired="branch_lemma_budget_exhausted",
                    stage="solver",
                    notes="Not reproduced within the 10-guidance budget.",
                )
            return ControllerDecision(
                outcome=OUTCOME_OPEN_BRANCH,
                rule_fired="branch_lemma",
                stage="solver",
                guidance_source=candidate.source,
                branch_lemma=lemma,
            )
        if candidate.failure_output_type == ORDINARY_HINT and candidate.has_usable_guidance:
            return _guidance_or_budget(
                state,
                config,
                stage="solver",
                rule="ordinary_hint",
                sentence=candidate.guidance_sentence,
                source=candidate.source,
            )

    # No usable guidance anywhere this round.
    if state.consecutive_no_guidance >= config.max_no_guidance_rounds:
        return ControllerDecision(
            outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
            rule_fired="no_useful_guidance_repeated",
            stage="solver",
            adjudication_kind="math_gap",
            notes="Consecutive rounds produced no usable guidance item.",
        )
    return ControllerDecision(
        outcome=OUTCOME_RERUN_UNCHANGED,
        rule_fired="no_useful_guidance",
        stage="solver",
    )


def collapse_branch_outcome(
    lemma_statement: str,
    branch_state: PipelineState,
) -> tuple[str, str]:
    """Collapse a finished branch pipeline into (kind, guidance sentence).

    kind is "proved", "disproved", or "inconclusive". Only proved/disproved
    produce a sentence (which the parent counts against its guidance budget).
    The disproved detection is deliberately conservative: it requires a
    forbidden-route style item in the branch's own guidance list that speaks of
    falsity or a counterexample.
    """

    lemma = lemma_statement.strip()
    if branch_state.status in {"accepted", "accepted_cascade_only"}:
        sentence = (
            "The following auxiliary lemma was established in a separate branch "
            f"run and may be used as a supporting fact: {lemma}"
        )
        return "proved", sentence
    for item in branch_state.guidance:
        lowered = item.lower()
        if "counterexample" in lowered or "false" in lowered or "disproved" in lowered:
            sentence = (
                "Do not assume the following auxiliary lemma; a branch "
                f"investigation produced evidence that it is false: {lemma} "
                f"Branch finding: {item.strip()}"
            )
            return "disproved", sentence
    return "inconclusive", ""


# ---------------------------------------------------------------------------
# Citation gate and verifier cascade (decision tree Steps 2-8)
# ---------------------------------------------------------------------------


def route_after_problem_statement_verifier(
    report: ProblemStatementReport,
    state: PipelineState,
    config: ControllerConfig,
) -> ControllerDecision:
    """Require an exact-target match before citation and proof verification."""

    if report.problem_statement_match == YES:
        return ControllerDecision(
            outcome=OUTCOME_RUN_NEXT_STAGE,
            rule_fired="problem_statement_match",
            stage="problem_statement_verifier",
            notes=report.actual_statement,
        )
    if report.problem_statement_match == NO:
        if state.consecutive_no_guidance >= config.max_no_guidance_rounds:
            return ControllerDecision(
                outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
                rule_fired="problem_statement_mismatch_repeated",
                stage="problem_statement_verifier",
                adjudication_kind="target_alignment",
                notes=report.mismatch_type or report.actual_statement,
            )
        return ControllerDecision(
            outcome=OUTCOME_RERUN_UNCHANGED,
            rule_fired="problem_statement_mismatch",
            stage="problem_statement_verifier",
            notes=report.recommended_action or report.mismatch_type,
        )
    return ControllerDecision(
        outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
        rule_fired="problem_statement_unclear",
        stage="problem_statement_verifier",
        adjudication_kind="target_alignment",
        notes=report.recommended_action or "The checked output's target could not be determined.",
    )


def route_after_citation_gate(
    gate_result: str,
    candidate_guidance_seed: str | None,
    reason: str,
    state: PipelineState,
    config: ControllerConfig,
) -> ControllerDecision:
    """Route the Citation Generator/Verifier hard gate before Verifier A."""

    gate = gate_result.strip().upper()
    if gate == "GOOD_TO_GO":
        return ControllerDecision(
            outcome=OUTCOME_RUN_NEXT_STAGE,
            rule_fired="citation_good_to_go",
            stage="citation",
            notes=reason,
        )
    if gate == "SOURCE_LEDGER_REPAIR_NEEDED":
        if state.consecutive_no_guidance >= config.max_no_guidance_rounds:
            return ControllerDecision(
                outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
                rule_fired="citation_ledger_repair_repeated",
                stage="citation",
                adjudication_kind="source_hygiene",
                notes=(
                    "The citation layer repeatedly requested source-ledger repair "
                    "without producing a guidance item."
                ),
            )
        return ControllerDecision(
            outcome=OUTCOME_RERUN_UNCHANGED,
            rule_fired="citation_ledger_repair",
            stage="citation",
            notes=reason,
        )
    if gate == "BLOCKING_SOURCE_ISSUE":
        seed = (candidate_guidance_seed or "").strip()
        if seed:
            return _guidance_or_budget(
                state,
                config,
                stage="citation",
                rule="citation_blocking_source_issue",
                sentence=seed,
                source="citation_verifier",
            )
        return ControllerDecision(
            outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
            rule_fired="citation_blocking_source_issue_without_seed",
            stage="citation",
            adjudication_kind="source_hygiene",
            notes=reason or "Citation Verifier found a blocking issue but supplied no guidance seed.",
        )
    if gate == "LEAKAGE_RISK":
        return ControllerDecision(
            outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
            rule_fired="citation_leakage_risk",
            stage="citation",
            adjudication_kind="source_hygiene",
            notes=reason or "Citation role reported possible target-source leakage.",
        )
    return ControllerDecision(
        outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
        rule_fired="citation_unclear",
        stage="citation",
        adjudication_kind="source_hygiene",
        notes=reason or f"Citation gate returned an unsupported result: {gate or 'empty'}.",
    )


def derive_a_status(report: ComposerAGoldReport) -> str:
    """Derive the Verifier A status from Composer A's gold report (Step 2).

    UNCLEAR answers on the blocking questions are treated as not verified so an
    unparseable or hedged report can never accidentally clear the cascade.
    """

    if report.disallowed_premises == YES:
        return A_INVALID
    if report.non_fillable_gaps == YES or report.omitted_case_or_weaker == YES:
        return A_NOT_VERIFIED
    if UNCLEAR in {report.disallowed_premises, report.non_fillable_gaps, report.omitted_case_or_weaker}:
        return A_NOT_VERIFIED
    if report.fillable_only_gaps == YES:
        return A_ALMOST
    return A_VERIFIED


def route_after_composer_a(
    report: ComposerAGoldReport,
    state: PipelineState,
    config: ControllerConfig,
) -> ControllerDecision:
    """Steps 3-4 entry: disagreement gate, then A-status routing."""

    if report.no_majority:
        return ControllerDecision(
            outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
            rule_fired="composer_a_no_majority",
            stage="composer_a",
            adjudication_kind="math_gap",
        )
    a_status = derive_a_status(report)
    if a_status in {A_NOT_VERIFIED, A_INVALID}:
        seed = report.guidance_seed.strip()
        if seed:
            return _guidance_or_budget(
                state,
                config,
                stage="composer_a",
                rule=f"{a_status.lower()}_with_seed",
                sentence=seed,
                source="verifier_a",
            )
        # No clear seed: run B anyway; A's flagged issue still blocks acceptance.
        return ControllerDecision(
            outcome=OUTCOME_RUN_NEXT_STAGE,
            rule_fired=f"{a_status.lower()}_no_seed_run_b",
            stage="composer_a",
            notes="Verifier A flagged issues without a clear guidance seed; acceptance stays blocked.",
        )
    return ControllerDecision(
        outcome=OUTCOME_RUN_NEXT_STAGE,
        rule_fired=f"{a_status.lower()}_run_b",
        stage="composer_a",
    )


def route_after_verifier_b(
    report,
    state: PipelineState,
    config: ControllerConfig,
) -> ControllerDecision:
    """Step 4 (B): non-fillable weakest point or disallowed premise reruns.

    The packet's acceptance rule requires "(Weakest point found? no, or
    Weakest point found? yes and Fillable: yes) AND B records no disallowed
    premise". Any B report that cannot be read into one of those states must
    not be allowed to fall through toward acceptance, so unreadable or
    contradictory reports route to human review instead of to Verifier C.
    """

    if report.weakest_point_found == NO:
        if report.disallowed_premise == YES:
            # Contradictory: a disallowed premise "at the weakest point" with
            # no weakest point found. Never let it drift toward acceptance.
            return ControllerDecision(
                outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
                rule_fired="b_contradictory_disallowed_premise",
                stage="verifier_b",
                adjudication_kind="math_gap",
                notes="Verifier B reported a disallowed premise but no weakest point.",
            )
        return ControllerDecision(
            outcome=OUTCOME_RUN_NEXT_STAGE,
            rule_fired="b_no_weakest_point_run_c",
            stage="verifier_b",
        )
    if report.weakest_point_found == YES:
        if report.fillable == NO or report.disallowed_premise == YES:
            # Guidance is mechanically formed from B's own missing-claim /
            # weakest-point fields; an empty formation means the report gave
            # the controller nothing to repackage -> human review.
            sentence = _verifier_b_guidance(report)
            if not sentence:
                return ControllerDecision(
                    outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
                    rule_fired="b_blocking_without_missing_claim",
                    stage="verifier_b",
                    adjudication_kind="math_gap",
                    notes="Verifier B blocked the proof but stated no missing claim to repackage.",
                )
            return _guidance_or_budget(
                state,
                config,
                stage="verifier_b",
                rule="b_nonfillable_weakest_point",
                sentence=sentence,
                source="verifier_b",
            )
        if report.fillable == YES and report.disallowed_premise in {NO, NOT_APPLICABLE}:
            return ControllerDecision(
                outcome=OUTCOME_RUN_NEXT_STAGE,
                rule_fired="b_fillable_run_c",
                stage="verifier_b",
            )
        # Weakest point found but fillable/disallowed not readable as the
        # protocol's yes/no answers: acceptance cannot be justified.
        return ControllerDecision(
            outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
            rule_fired="b_unreadable_fillability",
            stage="verifier_b",
            adjudication_kind="math_gap",
            notes="Verifier B found a weakest point but fillable/disallowed fields were unreadable.",
        )
    return ControllerDecision(
        outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
        rule_fired="b_unclear",
        stage="verifier_b",
        adjudication_kind="math_gap",
        notes="Verifier B report could not be read as a clear yes/no.",
    )


def route_after_verifier_c(
    report,
    a_status: str,
    state: PipelineState,
    config: ControllerConfig,
) -> ControllerDecision:
    """Step 4 (C): break -> rerun; unsure -> human; no -> Final Checker gate."""

    if report.broke == "yes":
        sentence = _verifier_c_guidance(report)
        if not sentence:
            return ControllerDecision(
                outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
                rule_fired="c_broke_without_failing_step",
                stage="verifier_c",
                adjudication_kind="math_gap",
                notes="Verifier C reported a break but stated no failing step to repackage.",
            )
        return _guidance_or_budget(
            state,
            config,
            stage="verifier_c",
            rule="c_broke",
            sentence=sentence,
            source="verifier_c",
        )
    if report.broke == "unsure":
        return ControllerDecision(
            outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
            rule_fired="c_unsure",
            stage="verifier_c",
            adjudication_kind="math_gap",
            notes=report.check_needed,
        )
    if report.broke == "no":
        if report.disallowed_premise not in {NO, NOT_APPLICABLE}:
            # Acceptance requires "C broke: no, no disallowed premise". A
            # recorded (or unreadable) disallowed-premise answer that was not
            # load-bearing enough to break the proof still blocks acceptance;
            # without the citing sentence there is nothing to repackage
            # mechanically.
            return ControllerDecision(
                outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
                rule_fired="c_disallowed_premise_without_break",
                stage="verifier_c",
                adjudication_kind="math_gap",
                notes="Verifier C's disallowed-premise answer blocks acceptance.",
            )
        if a_status in {A_VERIFIED, A_ALMOST}:
            return ControllerDecision(
                outcome=OUTCOME_RUN_NEXT_STAGE,
                rule_fired="c_no_break_cascade_clear",
                stage="verifier_c",
            )
        return ControllerDecision(
            outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
            rule_fired="c_no_break_but_a_blocked",
            stage="verifier_c",
            adjudication_kind="math_gap",
            notes="Verifier A flagged issues, but B and C produced no guidance source.",
        )
    return ControllerDecision(
        outcome=OUTCOME_NEEDS_HUMAN_REVIEW,
        rule_fired="c_unparseable",
        stage="verifier_c",
        adjudication_kind="math_gap",
        notes="Verifier C report could not be read as broke yes/no/unsure.",
    )


def route_final(
    decision: FinalCheckerDecision | None,
    gold_available: bool,
) -> ControllerDecision:
    """Steps 6-7: Final Checker gate, or cascade-only acceptance without gold."""

    if not gold_available:
        return ControllerDecision(
            outcome=OUTCOME_ACCEPTED_CASCADE_ONLY,
            rule_fired="no_gold_cascade_only",
            stage="final_checker",
            notes="Candidate proof passed the solver/verifier cascade; no gold proof exists to certify truth.",
        )
    if decision is None:
        return ControllerDecision(
            outcome=OUTCOME_RUN_NEXT_STAGE,
            rule_fired="final_checker_pending",
            stage="final_checker",
        )
    if decision.decision == "PASS":
        return ControllerDecision(
            outcome=OUTCOME_ACCEPTED,
            rule_fired="final_checker_pass",
            stage="final_checker",
        )
    return ControllerDecision(
        outcome=OUTCOME_REJECTED_FINAL_CHECK,
        rule_fired="final_checker_fail",
        stage="final_checker",
        notes=(
            "Terminal for the attempt: no rerun and no guidance item. "
            "Cascade false-accept: the gold-blind A/B/C cascade cleared this "
            "proof but the Final Checker rejected it; count it toward the "
            "cascade's false-accept rate."
        ),
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _guidance_or_budget(
    state: PipelineState,
    config: ControllerConfig,
    stage: str,
    rule: str,
    sentence: str,
    source: str,
) -> ControllerDecision:
    """Emit RERUN_WITH_GUIDANCE, or STOPPED_BUDGET when the list is full."""

    if budget_exhausted(state, config):
        return ControllerDecision(
            outcome=OUTCOME_STOPPED_BUDGET,
            rule_fired=f"{rule}_budget_exhausted",
            stage=stage,
            notes="Not reproduced within the 10-guidance budget.",
        )
    return ControllerDecision(
        outcome=OUTCOME_RERUN_WITH_GUIDANCE,
        rule_fired=rule,
        stage=stage,
        guidance_sentence=sentence.strip(),
        guidance_source=source,
    )


def _verifier_b_guidance(report) -> str:
    """Build the one standalone forward-looking sentence from a B report.

    Deterministic templating only -- the mathematical content is repackaged
    verbatim from the report's missing-claim (preferred) or weakest-point
    field, never rewritten. Returns "" when the report supplies no content,
    so the caller can refuse to append an empty guidance item.
    """

    if report.missing_claim.strip():
        return (
            "A complete proof must explicitly establish the following claim: "
            f"{report.missing_claim.strip()}"
        )
    if report.weakest_point.strip():
        return (
            "A complete proof must rigorously justify the following point: "
            f"{report.weakest_point.strip()}"
        )
    return ""


def _verifier_c_guidance(report) -> str:
    """Build the one standalone forward-looking sentence from a C report.

    Same repackaging rule as :func:`_verifier_b_guidance`: the failing step
    (preferred) or attack description is quoted verbatim; "" when absent.
    """

    detail = report.failing_step.strip() or report.attack.strip()
    if not detail:
        return ""
    return (
        "Any proof must avoid the following identified failure point and "
        f"handle it rigorously: {detail}"
    )
