Fresh no-history solver-only Main/Manager pipeline. You are spawned with fork_context=false and must use only this message as input. Do not use memory, prior task history, web/internet, API keys, Python, or files. This is solver-only: do not run any verifier/citation/final-checker pipeline.

You are the Manager in the routing phase. Your task is to create an executable routing plan for the normalized target problem. Do not write the final solution. Do not certify an unsupported candidate answer as established. You may record plausible candidate answers, theorem-recognition routes, or inferred standard setup as non-evidentiary context for Main Solver, Midfielders, Attackers, and the Defender to test, derive, or challenge.

Use the solver/manager collaborative architecture. In this initial routing pass, select exactly one active worker as Main Solver, the Main Solver, who owns the complete proof, and exactly one separate Defender who runs last and attacks Main Solver's integrated proof. Do not launch Midfielders or Attackers yet. Specialist staffing is a later Manager decision made only after reading Main Solver's first attempt, uncertain_steps, help_requests, and proposed_board_updates.

Work in two passes. First perform a semantic reading pass: reconstruct the intended standard setup from the target's named objects, invariants, notation, and usual admissibility conditions, then develop the mathematical mechanism, support graph, and worker assignments without classifying ideas by provenance. Then audit that plan by filling the Critical Claims Ledger. Do not delete a potentially useful route merely because its provenance is uncertain; keep the route visible and mark the uncertainty honestly in the second pass.

You are given:
1. a cleaned skeleton PDF or TeX file;
2. the target problem or statement;
3. the Allowed supporting statements list;
4. the additional mathematical guidance list, if any.

Use only the supplied packet, the allowed supporting statements, the guidance list, genuinely standard background, and facts that later subproblem solvers would need to prove inside the current solution. Do not use external sources, web search, related writeups, unstated task-specific facts, hidden lemmas, or any material not included in the provided packet.

Allowed supporting statements for this run:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. There are no prior formal supporting theorem/lemma/proposition/corollary statements. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

If required inputs are missing, stop and write "SETUP FAILURE: missing input." Then list the missing input(s). Treat the standalone skeleton below as the supplied cleaned skeleton packet.

Produce exactly the following sections.

1. Target normalization

target_label:
task_type: proof / exact value / expression / optimization / bound / classification / existence-or-nonexistence / computation / other
exact_target_statement:
variables_domains_assumptions_and_quantifiers:
inferred_standard_setup:
reading_assumptions_used:
required_final_output:
required_directions:

2. Task-adaptive proof obligations

Do not force every task into an upper-bound/lower-bound or construction/obstruction template. Fill each field from the actual target. For a field that genuinely does not apply, write `NOT_APPLICABLE` followed by a short reason. Do not leave a field blank.

primary_claim:
converse_or_sharpness_requirement:
existence_or_feasibility_requirement:
uniqueness_or_exhaustiveness_requirement:
domain_and_edge_cases:
independent_stress_test:

3. Available tools

For each planned tool:
tool:
source_status: provided definition / notation / assumption; allowed supporting statement; additional guidance item; standard background fact; proved inside the current proof; or unsupported or unclear.
exact_statement_or_fact:
intended_role_in_proof:

4. Subclaim support graph

Identify 1-15 load-bearing subclaims or obligations. Use the smallest graph that faithfully describes the proof; do not manufacture subclaims to justify more agents. These are context for Main Solver's first attempt and possible post-Main-Solver assistance routing, not permission to launch specialists before Main Solver. For each:
id:
statement:
uses_prior_subclaims:
purpose:
status: follows from allowed statement / follows from guidance / standard background / must be proved in final solution.
suggested_solver: one of the active IDs SS1 through SS10.

5. Critical Claims Ledger

Before assigning workers, actively search for the small set of exact claims that can change the requested answer, proof validity, answer status, or acceptance: exact constants, formulas, normalizations, signs, magnitudes, indexing conventions, theorem variants, missing hypotheses, and answer-sensitive packet-external imports. Do not add routine definitions, ordinary setup, or answer-insensitive background. Give each claim a stable id CC001, CC002, ... Record each critical claim as one fenced YAML block:

```yaml
critical_claim_id: CC001
claim:
why_critical:
live_alternatives: []
resolution_test:
basis: packet_statement | derived_here | sealed_guidance_E### | standard_background | packet_external_unestablished | unsupported_or_source_gap
status: OPEN | ESTABLISHED | SOURCE_GAP
owner: Manager / Main Solver / one active SS-ID / None
```

If no claim qualifies, write "None found" and state which ambiguity, theorem-variant, normalization, hypothesis, and source-gap checks were performed.

6. Key-step and Main Solver selection

hardest_step_id:
hardest_step_description:
risk_if_wrong:
main_solver_id: one active SS-ID
key_solver_id: the same active SS-ID as main_solver_id
global_solver_id: the same active SS-ID as main_solver_id
why_this_solver_is_M:
what_would_invalidate_the_route:

7. Failure-mode checks

circularity_check:
full_theorem_check:
source_check:
hypothesis_check:
notation_check:
standard_background_check:
answer_anchor_check:
task_type_obligation_check:

8. Subsolver execution plan

Choose the minimum active worker set for the first phase: Main Solver plus one separate Defender. Do not add Midfielders or Attackers in this initial plan.

constructive_solver_count: 1
subsolver_count: 2
subsolver_count_rationale:
specialist_escalation_rationale: `NOT_NEEDED - post-Main-Solver assistance routing has not run yet`
main_solver_id: one active constructive SS-ID
global_solver_id: exactly the same SS-ID as main_solver_id
key_solver_id: exactly the same SS-ID as main_solver_id
defender_solver_id: one different active SS-ID
stress_test_solver_id: exactly the same SS-ID as defender_solver_id
attacker_solver_ids: []
coverage_check: PASS / FAIL - explain whether Main Solver plus any justified Midfielders/Attackers cover every required proof obligation
independence_check: PASS / FAIL - identify and remove duplicate or paraphrased assignments

Exactly one active worker must be Main Solver and receive `work_scope: global_solution`. Exactly one active worker must be the Defender and receive `work_scope: adversarial_stress_test`. Main Solver and the Defender must be different. The Defender runs LAST and receives Main Solver's integrated proof plus any support artifacts Main Solver actually used; do not assign it a constructive proof obligation.

9. Subsolver assignment table

Write exactly two contiguous assignments named SS1 and SS2. Every assignment must be self-contained and must not require seeing any source outside the supplied packet and this blueprint. Do not list inactive IDs. For each active SS-ID use:

SS#:
role: Main Solver / midfielder / attacker / defender
work_scope: global_solution / assigned_subclaim / alternative_route / adversarial_stress_test
assigned_subclaim_ids:
task:
required_deliverable:
connection_to_target:
where_used_in_final_solution:
independence_constraint:
failure_or_salvage_focus:

The `main_solver_id` assignment must use `work_scope: global_solution`, cover the exact target, and require one coherent complete candidate solution before support workers are launched. Main Solver must emit candidate answer, complete scratch-work attempt, uncertain_steps, help_requests, and proposed_board_updates. The Defender assignment must use `work_scope: adversarial_stress_test`.

10. Web-source confirmation

Write "no web sources used".

--- INPUTS FOR THIS RUN ---
Cleaned skeleton packet:
Standalone problem statement only. No proof text, proof sketch, derivation, or prior formal result is included. Standard definitions/notation for algebraic tori over Q, local fields Q_p, T(Q_p), rational points T(Q), and the maximal compact subgroup of a p-adic torus may be inferred only to parse the target.

Target theorem:
For any algebraic torus T over Q and any prime number p, the decomposition T(Q_p) = T(Z_p) T(Q) holds, where T(Z_p) denotes the maximal compact subgroup of T(Q_p).

Additional mathematical guidance:
None