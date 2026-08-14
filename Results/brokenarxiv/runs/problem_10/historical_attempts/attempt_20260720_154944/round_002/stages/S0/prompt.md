Fresh no-history solver-only S0 round. Do not use memory, prior task history, external sources, web search, API keys, tools, code execution, or files. Use only the supplied cleaned packet, target theorem, allowed support, guidance, and genuinely standard background. This is S0 only, not a verifier/manager/defender role.

Supplied cleaned skeleton packet for this run:
- Definition/assumption: A weakly o-minimal structure is a linearly ordered structure in which every definable subset of the domain is a finite union of convex sets.
- Assumption: M = (M,+,·,≤,...) is a weakly o-minimal expansion of an ordered field.
- Notation: U ⊆ M is an open definable set; f: U -> M is definable; differentiability is the usual one-variable derivative over the ordered field topology.
- No other paper skeleton, source, or allowed formal theorem statement is supplied.

----------------------------------------------------------------
S0 Blueprint Solver. Fresh no-internet chat.
----------------------------------------------------------------
You are S0, the Blueprint Solver. Your task is to create a proof blueprint for the target
theorem. Do not write the final proof.

You are given:
1. a cleaned skeleton PDF or TeX file;
2. the target theorem;
3. the Allowed supporting statements list;
4. the additional mathematical guidance list, if any.

Use only the supplied packet, the allowed supporting statements, the guidance list, genuinely
standard background, and facts that later subproblem solvers would need to prove inside the
current proof. Do not use external sources, web search, related writeups, unstated
task-specific facts, hidden lemmas, or any material not included in the provided packet.

If a guidance item is labeled `[INTERNALLY VERIFIED AUXILIARY RESULT E###]`, treat exactly its
stated lemma as established and available without reproof. Record E### as an additional-guidance
tool wherever it is used. Do not reconstruct its hidden branch proof or infer a stronger claim.

The blueprint is part of the current-round proof artifact. It may be inspected by verifiers,
but it is not carried into later Solver rounds.

Allowed supporting statements:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed.
No formal theorem/lemma/proposition/corollary statements are supplied as allowed support.
No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.
Later-but-upstream inclusions: None.
Exclusions: None.
Unclear: None.
This list or rule is authoritative for this run.

If required inputs are missing, stop and write "SETUP FAILURE: missing input." Then list the missing input(s).

Produce exactly the following sections.

1. Target decomposition

target_label:
target_type:
main_goal:
variables_and_parameters:
conclusion_to_prove:

2. Available tools

For each planned tool:
tool:
source_status: provided definition / notation / assumption; allowed supporting statement; additional guidance item; standard background fact; proved inside the current proof; or unsupported or unclear.
exact_statement_or_fact:
intended_role_in_proof:

3. Subclaim support graph

Break the proof into 3-8 subclaims. For each:
id:
statement:
uses_prior_subclaims:
purpose:
status: follows from allowed statement / follows from guidance / standard background / must be proved in final proof.
suggested_solver: S1 / S2 / S3 / S4 / S5.

4. Hardest step prediction

hardest_step_id:
hardest_step_description:
risk_if_wrong:
how_final_proof_should_handle_it:

5. Failure-mode checks

circularity_check:
full_theorem_check:
source_check:
hypothesis_check:
notation_check:
standard_background_check:

6. Subproblem assignment table

Assign S1-S5. Each assignment should be self-contained and should not require seeing any source outside the supplied packet and this blueprint.

S1:
S2:
S3:
S4:
S5:

7. Web-source confirmation

Write "no web sources used", or list any unavoidable lookup that was explicitly permitted.

--- INPUTS FOR THIS RUN ---
Target theorem:
A weakly o-minimal structure is a linearly ordered structure in which every definable subset of the domain is a finite union of convex sets. Let M = (M, +, ·, ≤, ...) be a weakly o-minimal expansion of an ordered field. Then for any nonempty open definable set U ⊆ M and any definable function f : U -> M, there exists a nonempty open interval I ⊆ U on which f is differentiable.

Additional mathematical guidance:
1. The exact original statement must be read with U nonempty, or else the empty-open-set case is a counterexample under the usual nonempty meaning of open interval. Prove the intended nonempty-open-set version and keep the nonempty hypothesis explicit.