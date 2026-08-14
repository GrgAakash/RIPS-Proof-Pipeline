"""Scripted offline mock client for the open-problem workflow.

``ScriptedMockClient`` implements the :class:`~solver.llm.LLMClient`
protocol and emits realistic labeled-markdown role outputs, so the whole
pipeline (parsers, controller, orchestrator, run store) can run end-to-end with
no network. Behavior is selected by a ``scenario`` name plus the routing
metadata each call carries (role, round, depth, s_id).

Scenarios:

* ``solved_round1``                -- S6 composes a proof in round 1; cascade clear.
* ``forbidden_then_solved``        -- round 1: S4 reports a forbidden route; round 2 solves.
* ``hint_then_solved``             -- round 1: S3 requests an ordinary hint; round 2 solves.
* ``branch_then_solved``           -- round 1: S2 proposes a branch lemma; the branch
                                      pipeline solves it; the main run solves in round 2.
* ``nested_branch_statement_only`` -- main S2 opens a branch whose S4 opens a
                                      sub-branch; both accepted proofs remain sealed.
* ``never_guidance``               -- S6 never completes and nobody has guidance.
* ``forbidden_loop``               -- a fresh forbidden-route item every round (budget test).
* ``cascade_a_reject_then_solved`` -- round 1 proof rejected by Verifier A seed; round 2 clear.
* ``cascade_b_reject_then_solved`` -- round 1 proof rejected by Verifier B; round 2 clear.
* ``final_checker_fail``           -- cascade clear but the privileged checker rejects.
* ``leakage_round1``               -- S3 reports possible target-source leakage; the
                                      controller must halt the run for source-hygiene review.

The mock outputs double as parser fixtures: they follow the exact labeled
formats the fixed prompts mandate.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from solver.llm import LLMResponse
from citation.clients import mock_citation_response
from solver.packet import PromptPacket


MOCK_LEMMA_STATEMENT = (
    "For every finite family of operators B_alpha with the mock incidence "
    "structure, the signed block T_p satisfies ||T_p|| <= 2*sqrt(N)."
)

MOCK_NESTED_LEMMA_STATEMENT = (
    "Every mock incidence block has signed norm at most two."
)


def _blueprint() -> str:
    assignments = "\n".join(
        f"S{index}:  \nProve subclaim SC{index} of the mock decomposition using only allowed materials."
        for index in range(1, 6)
    )
    return f"""1. Target decomposition

target_label:
Mock target theorem.

2. Available tools

tool:
Mock allowed statements.

3. Subclaim support graph

id: SC1
statement: Mock subclaim chain.

4. Hardest step prediction

hardest_step_id: SC3
key_solver_id: S3
why_key_solver_is_decisive: SC3 is the load-bearing mock subclaim.

5. Failure-mode checks

circularity_check: none.

6. Subproblem assignment table

{assignments}

7. Web-source confirmation

Internet used? NO
"""


def _solved_subproblem(s_id: str) -> str:
    return f"""1. Assignment restatement

S-ID:
{s_id}

2. Subproof or failure

A complete rigorous mock subproof of the assigned subclaim.

3. Solver failure output and candidate guidance

failure_output_type: solved
candidate guidance usable? NO
guidance sentence: None

4. Local Source Ledger

claim_id: L1

5. Interface notes for S6

what this subproof establishes: the assigned subclaim.
failure_output_type: solved

6. Web-source confirmation

Internet used? NO
"""


def _unsolved_subproblem(s_id: str, failure_type: str, extra_fields: str) -> str:
    return f"""1. Assignment restatement

S-ID:
{s_id}

2. Subproof or failure

SUBPROBLEM UNSOLVED: the assigned subclaim resisted all allowed routes.

3. Solver failure output and candidate guidance

failure_output_type: {failure_type}
{extra_fields}

4. Local Source Ledger

claim_id: L1

5. Interface notes for S6

what this subproof establishes: nothing conclusive.

6. Web-source confirmation

Internet used? NO
"""


def _forbidden_subproblem(s_id: str, sentence: str) -> str:
    fields = f"""type: counterexample
failed route or missing step:
The general arbitrary-coefficient estimate route.
obstruction or missing idea:
A finite-dimensional counterexample.
evidence:
Direct computation on the degree-10 diagonal vector.
reuse value:
Prevents repeating a disproved route.
guidance sentence:
{sentence}"""
    return _unsolved_subproblem(s_id, "forbidden-route / obstruction guidance", fields)


def _hint_subproblem(s_id: str, sentence: str) -> str:
    fields = f"""type: ordinary hint request
failed route or missing step:
No route disproved; a specific tool is missing.
obstruction or missing idea:
A missing structural estimate.
evidence:
The estimate would enter at the final block bound.
reuse value:
Points the next run at a concrete tool.
guidance sentence:
{sentence}"""
    return _unsolved_subproblem(s_id, "ordinary hint request", fields)


def _branch_subproblem(s_id: str, lemma_statement: str = MOCK_LEMMA_STATEMENT) -> str:
    fields = f"""type: unresolved key lemma
failed route or missing step:
The proof reduces to one standalone lemma.
obstruction or missing idea:
The candidate lemma below.
evidence:
All remaining steps follow from it directly.
reuse value:
A clean mini-pipeline target.
guidance sentence:
None

candidate lemma statement:
{lemma_statement}
why this lemma would unblock the assigned subclaim:
It supplies the only missing block estimate.
exact place where the main proof would use it:
The final norm bound of the composed proof.
allowed inputs for the auxiliary lemma:
Finite-dimensional exterior algebra facts only.
dependencies from the skeleton, guidance, or explicitly logged external sources:
None.
does the candidate lemma appear to be weaker than the target theorem? YES
does the candidate lemma appear equivalent to, stronger than, or downstream from the target theorem? NO
recommended mini-pipeline target? YES"""
    return _unsolved_subproblem(s_id, "branch lemma target", fields)


def _leakage_subproblem(s_id: str) -> str:
    return f"""1. Assignment restatement

S-ID:
{s_id}

2. Subproof or failure

Possible target-source leakage encountered.

While searching for supporting results, a source appearing to contain the
target theorem's proof was surfaced. Per protocol, this run stops here.

6. Web-source confirmation

Internet used? YES
Sources opened: a page that appears to contain the target's source article.
"""


def _no_guidance_subproblem(s_id: str) -> str:
    fields = """type: no useful guidance item found
failed route or missing step:
Multiple routes stalled without a reusable obstruction.
obstruction or missing idea:
None identified.
evidence:
None.
reuse value:
None.
guidance sentence:
None"""
    return _unsolved_subproblem(s_id, "no useful guidance item found", fields)


def _s6_complete(
    proof_marker: str = "MOCK_FINAL_PROOF",
    internal_result_id: str | None = None,
) -> str:
    internal_step = (
        f"Step 2. [KEY STEP] Apply internally verified auxiliary result {internal_result_id}."
        if internal_result_id
        else "Step 2. [KEY STEP] Apply the mock block bound."
    )
    return f"""1. Composition map

S0 blueprint used? YES
S1-S5 outputs used: S1, S2, S3, S4, S5
[KEY STEP] source: S3

2. Final proof

Step 1. {proof_marker}: assemble the subclaims into the target estimate.
{internal_step}
Step 3. Conclude the target theorem.

3. Composer failure output and candidate guidance

failure_output_type: solved
candidate guidance usable? NO
guidance sentence: None

4. Source Ledger

claim_id: F1

5. Completion checklist

Did the proof prove the exact target theorem? YES

6. Web-source confirmation

Internet used? NO

7. LaTeX artifact

Mock LaTeX omitted.
"""


def _s6_incomplete() -> str:
    return """1. Composition map

S0 blueprint used? YES
S1-S5 outputs used: S1, S2, S3, S4, S5

2. Final proof

FINAL PROOF NOT COMPLETED: a required subclaim is unresolved.

3. Composer failure output and candidate guidance

failure_output_type: no useful guidance item found
type: no useful guidance item found
failed route or missing step:
A required subclaim is unresolved.
obstruction or missing idea:
None beyond the reporting S-solver.
evidence:
None.
reuse value:
None.
guidance sentence:
None

4. Source Ledger

claim_id: F1

5. Completion checklist

Did the proof prove the exact target theorem? NO

6. Web-source confirmation

Internet used? NO
"""


def _verifier_a_report(clear: bool) -> str:
    verdict = "JUSTIFIED" if clear else "GAP"
    return f"""1. Target restatement

The mock target theorem.

2. Step ledger

Step 1: {verdict}: follows from the mock subclaims.

9. Controller-facing summary

Non-fillable gaps present? {"NO" if clear else "YES"}
Fillable-only gaps present? NO
Disallowed premises present? NO
Omitted case / weaker statement present? NO
Standard-background-heavy? NO
Web-source issue? NO
Candidate guidance seed, if any: None
"""


def _problem_statement_verifier(match: bool = True) -> str:
    return f"""1. Target restatement

The mock target theorem.

2. Statement addressed by the checked output

{"The mock target theorem." if match else "A different mock theorem."}

3. Alignment check

{"MATCH" if match else "MISMATCH"}

4. Evidence

The checked output explicitly identifies its target.

5. Controller-facing summary

Artifact role checked: Solver proof
Problem statement match? {"YES" if match else "NO"}
Actual statement addressed: {"The mock target theorem." if match else "A different mock theorem."}
Mismatch type, if any: {"none" if match else "different statement"}
Recommended controller action: {"continue" if match else "rerun Solver with exact target"}
"""


def _composer_a(clear: bool, seed: str | None = None) -> str:
    return f"""1. Input inventory

Three Verifier A reports were merged.

6. Disagreement map

all agree

8. Gold Verifier A evidence report for the Decision Controller

Non-fillable gaps present? {"NO" if clear else "YES"}
Fillable-only gaps present? NO
Disallowed premises present? NO
Omitted case / weaker statement present? NO
Standard-background-heavy? NO
Web-source issue? NO
Same issue recurring across reports? {"NO" if clear else "YES"}
Candidate guidance seed, if any: {seed or "None"}
"""


def _verifier_b(clear: bool, missing_claim: str | None = None) -> str:
    if clear:
        summary = """Weakest point found? no
Weakest point (step + claim, or "None"): None
Missing claim, or "None": None
Fillable: not applicable
Disallowed premise at the weakest point? not applicable"""
    else:
        summary = f"""Weakest point found? yes
Weakest point (step + claim, or "None"): Step 2, the mock block bound.
Missing claim, or "None": {missing_claim or "The mock block bound must be proved for every block."}
Fillable: no
Disallowed premise at the weakest point? no"""
    return f"""1. Weakest point

{"No weakest point found." if clear else "Step 2, the mock block bound."}

Final summary format:

{summary}
"""


def _verifier_c(clear: bool) -> str:
    if clear:
        summary = """Most serious attack (step + claim): Step 2, the mock block bound.
Attack location (inside key step / outside key step / blueprint / S1-S5 / no key step / unclear / not applicable): inside key step
Broke: no
If broke, the false claim or failing step: None
If unsure, exact check needed to decide: None
Source status: proved inside the proposed proof
Disallowed premise at the attacked point? no"""
    else:
        summary = """Most serious attack (step + claim): Step 2, the mock block bound.
Attack location (inside key step / outside key step / blueprint / S1-S5 / no key step / unclear / not applicable): inside key step
Broke: yes
If broke, the false claim or failing step: The mock block bound fails on the diagonal test vector.
If unsure, exact check needed to decide: None
Source status: unsupported
Disallowed premise at the attacked point? no"""
    return f"""1. Most serious possible failure point

The mock block bound.

Final summary format:

{summary}
"""


def _final_checker(passed: bool) -> str:
    if passed:
        data = {
            "decision": "PASS",
            "failure_category": "none",
            "private_rationale": "Mock candidate matches the gold argument's obligations.",
            "source_concern": None,
            "public_diagnosis": [],
        }
    else:
        data = {
            "decision": "FAIL",
            "failure_category": "mathematical",
            "private_rationale": "Mock candidate misses a gold-proof obligation.",
            "source_concern": None,
            "public_diagnosis": ["The candidate does not discharge a required obligation."],
        }
    return json.dumps(data)


@dataclass
class ScriptedMockClient:
    """Offline scripted client driving one named end-to-end scenario."""

    scenario: str = "solved_round1"
    model: str = "scripted-mock"
    calls: list[dict] = field(default_factory=list)

    def complete(self, prompt: PromptPacket, metadata: dict) -> LLMResponse:
        # The full prompt text is recorded so tests can assert the Markovian
        # invariant: later-round prompts carry only the guidance list, never
        # earlier-round artifacts.
        self.calls.append({"role": prompt.role, "system": prompt.system, "user": prompt.user, **metadata})
        text = self._respond(prompt.role, metadata)
        return LLMResponse(text=text, model=self.model)

    def _respond(self, role: str, metadata: dict) -> str:
        round_index = int(metadata.get("round", 1))
        depth = int(metadata.get("depth", 0))
        s_id = str(metadata.get("s_id", ""))
        scenario = self.scenario

        if role == "s0":
            return _blueprint()
        if role == "reformatter":
            return json.dumps({"failure_output_type": "no useful guidance item found"})
        if role == "subproblem":
            return self._subproblem(scenario, round_index, depth, s_id)
        if role == "s6":
            return self._s6(scenario, round_index, depth)
        if role == "problem_statement_verifier":
            mismatch = (
                scenario == "problem_statement_mismatch_then_solved"
                and round_index == 1
                and depth == 0
            )
            return _problem_statement_verifier(match=not mismatch)
        if role in {"citation_generator", "citation_verifier", "citation_reformat"}:
            return mock_citation_response(role, metadata)
        if role == "verifier_a":
            return _verifier_a_report(clear=True)
        if role == "composer_a":
            if scenario == "cascade_a_reject_then_solved" and round_index == 1 and depth == 0:
                return _composer_a(clear=False, seed="Establish the mock block bound before assembling the proof.")
            return _composer_a(clear=True)
        if role == "verifier_b":
            if scenario == "cascade_b_reject_then_solved" and round_index == 1 and depth == 0:
                return _verifier_b(clear=False)
            return _verifier_b(clear=True)
        if role == "verifier_c":
            return _verifier_c(clear=True)
        if role == "final_checker":
            return _final_checker(passed=scenario != "final_checker_fail")
        return ""

    def _subproblem(self, scenario: str, round_index: int, depth: int, s_id: str) -> str:
        if (
            scenario == "nested_branch_statement_only"
            and depth == 1
            and round_index == 1
            and s_id == "S4"
        ):
            return _branch_subproblem(s_id, MOCK_NESTED_LEMMA_STATEMENT)
        if depth > 0:
            # Branch pipelines solve immediately in every scripted scenario.
            return _solved_subproblem(s_id)
        if scenario == "forbidden_then_solved" and round_index == 1 and s_id == "S4":
            return _forbidden_subproblem(
                s_id,
                "Do not use the arbitrary-coefficient row-column estimate; that stronger estimate is false.",
            )
        if scenario == "forbidden_loop" and s_id == "S4":
            return _forbidden_subproblem(
                s_id,
                f"Avoid mock false route number {round_index}; it is disproved by a counterexample.",
            )
        if scenario == "hint_then_solved" and round_index == 1 and s_id == "S3":
            return _hint_subproblem(
                s_id,
                "Look for a direct estimate using the symmetrized matrix-unit structure.",
            )
        if (
            scenario in {"branch_then_solved", "nested_branch_statement_only"}
            and round_index == 1
            and s_id == "S2"
        ):
            return _branch_subproblem(s_id)
        if scenario == "never_guidance" and s_id == "S5":
            return _no_guidance_subproblem(s_id)
        if scenario == "leakage_round1" and s_id == "S3":
            return _leakage_subproblem(s_id)
        return _solved_subproblem(s_id)

    def _s6(self, scenario: str, round_index: int, depth: int) -> str:
        if scenario == "nested_branch_statement_only":
            if depth == 0 and round_index == 1:
                return _s6_incomplete()
            if depth == 1 and round_index == 1:
                return _s6_incomplete()
            if depth == 0:
                return _s6_complete("MAIN_FINAL_PROOF_BODY", "E001")
            if depth == 1:
                return _s6_complete("BRANCH_DEPTH_1_PROOF_BODY", "E002")
            return _s6_complete("BRANCH_DEPTH_2_PROOF_BODY")
        if scenario == "branch_then_solved" and depth == 0 and round_index > 1:
            return _s6_complete("MOCK_FINAL_PROOF", "E001")
        if depth > 0:
            return _s6_complete(f"BRANCH_DEPTH_{depth}_PROOF_BODY")
        if scenario in {"forbidden_then_solved", "hint_then_solved", "branch_then_solved"} and round_index == 1:
            return _s6_incomplete()
        if scenario in {"never_guidance", "forbidden_loop"}:
            return _s6_incomplete()
        return _s6_complete()
