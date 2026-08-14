Fresh no-history solver-only M/S pipeline role: S0 Blueprint for Messi/Scaloni run.

Canonical prompt constraint:
- Use the canonical prompt packet copy only: `pipeline_sources/Prompt Packet/Prompts.md`.
- Do not use the mirrored version under `integrated_pipeline/Codes`.
- If inspecting the prompt file with shell commands, quote the path because it contains spaces.

Hard constraints for this run:
- Use no memory, no prior task history, no previous outputs, no answer keys, and no files outside the fresh input bundle below.
- Do not read the private memory directory.
- Do not use web search or internet.
- Do not use API keys.
- This is solver-only; do not run or simulate verifier roles.
- Treat this message as the complete fresh input bundle.
- There is no separate cleaned paper skeleton for this standalone problem. This is intentional. Do not stop for missing skeleton; use the target theorem plus allowed standard definitions/background described below.
- Use the M/S naming convention in your assignment table: assign the global/key solver as `SS1 Messi`; assign the final composer role later as `S6 Scaloni`; assign the adversarial stress tester separately.

Use the latest S0 Blueprint Solver prompt from `pipeline_sources/Prompt Packet/Prompts.md`, applied to this standalone target:

You are S0, the Blueprint Solver. Your task is to create an executable solution blueprint for the normalized target problem. Do not write the final solution. Do not certify an unsupported candidate answer as established. You may record plausible candidate answers, theorem-recognition routes, or inferred standard setup as non-evidentiary context for later solvers to test, derive, or challenge.

Use a global-first architecture. Your default plan is one Global/Key Solver that attempts the entire target plus one separate Adversarial Stress Tester. Add targeted specialists only when you can name a concrete independent obligation, alternative mechanism, computation, edge-case audit, or anticipated bottleneck that the Global/Key Solver should not carry alone. Do not split a coherent proof merely to populate roles.

Work in two passes. First perform a semantic reading pass: reconstruct the intended standard setup from the target's named objects, invariants, notation, and usual admissibility conditions, then develop the mathematical mechanism, support graph, and candidate assignments without classifying ideas by provenance. Then audit that plan by filling the target-determining claim register and Mathematical Unknowns Ledger. Do not delete a potentially useful route merely because its provenance is uncertain; keep the route visible and mark the uncertainty honestly in the second pass.

Use only the supplied packet, the allowed supporting statements, the guidance list, genuinely standard background, and facts that later subproblem solvers would need to prove inside the current solution. Do not use external sources, web search, related writeups, unstated task-specific facts, hidden lemmas, or any material not included in the provided packet.

Allowed supporting statements:
For this standalone problem-only run: definitions, notation, and assumptions needed to state or parse real affine lines, the natural quotient topology on the space of lines, line transversals, open convex sets, pairwise disjointness, connected components, reduced homology, acyclicity, elementary convexity, basic facts about Grassmannians and affine bundles of lines, and genuinely standard background facts in convex and algebraic topology may be used. There are no formal skeleton theorems to cite without proof. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

Produce exactly these sections:

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

Identify 1-15 load-bearing subclaims or obligations. For each:
id:
statement:
uses_prior_subclaims:
purpose:
status: follows from allowed statement / follows from guidance / standard background / must be proved in final solution.
suggested_solver: one of the active IDs SS1 through SS10.

5. Target-determining claim register

Identify EVERY claim that directly determines the final answer. Give each a stable id TDC-1, TDC-2, ... For each:
claim_id: TDC-#
claim:
why_it_determines_the_answer:
known_competing_variants: list nearby variants, off-by-one forms, or alternative conventions, or "None known"
expected_basis: packet_statement / derived_here / standard_background / sealed_guidance_E### / unsupported_or_source_gap

If no claim qualifies, write "None" and justify why the answer is not sensitive to any single external claim.

6. Mathematical Unknowns Ledger (blind-spot pass)

Record each remaining discriminating question as one fenced YAML block with keys unknown_id, kind, description, target_determining, current_evidence, candidate_resolutions, downstream_outcomes, answer_sensitivity_rationale, resolution_test_id, required_resolution_test, assigned_solver, status. If no unknown is found, write "None found" and state which blind-spot questions were checked.

7. Key-step and key-solver selection

hardest_step_id:
hardest_step_description:
risk_if_wrong:
key_solver_id: one active SS-ID
global_solver_id: the same active SS-ID as key_solver_id
why_this_solver_is_key:
what_would_invalidate_the_route:

8. Failure-mode checks

circularity_check:
full_theorem_check:
source_check:
hypothesis_check:
notation_check:
standard_background_check:
answer_anchor_check:
task_type_obligation_check:

9. Subsolver execution plan

constructive_solver_count: an integer from 1 through 9
subsolver_count: constructive_solver_count + 1, with 2 <= subsolver_count <= 10
subsolver_count_rationale:
specialist_escalation_rationale:
global_solver_id: one active constructive SS-ID
key_solver_id: exactly the same SS-ID as global_solver_id
stress_test_solver_id: one different active SS-ID
coverage_check: PASS / FAIL - explain whether the Global/Key Solver plus any justified specialists cover every required proof obligation
independence_check: PASS / FAIL - identify and remove duplicate or paraphrased assignments

10. Subsolver assignment table

Write exactly `subsolver_count` contiguous assignments named SS1, SS2, ..., SSN. Include the Messi/Scaloni naming convention by writing `SS1 Messi` for the global/key solver. The stress-test assignment must be distinct. For each active SS-ID use:
SS#:
role: global/key solver / targeted specialist / independent alternative / adversarial stress test / other precise role
work_scope: global_solution / assigned_subclaim / adversarial_stress_test
assigned_subclaim_ids:
task:
required_deliverable:
connection_to_target:
where_used_in_final_solution:
independence_constraint:
failure_or_salvage_focus:

11. Web-source confirmation

Write "no web sources used".

--- INPUTS FOR THIS RUN ---
Cleaned skeleton/source packet:
None. Standalone target theorem only; intentional problem-only run.

Target theorem:
Let the space of lines in R^d be endowed with the natural topology (the quotient space obtained from the deleted product {(x,y) in R^d x R^d : x != y} by considering (x,y) and (x',y') equivalent if they span the same line). For every integer d >= 1 and every finite family of at least two pairwise disjoint open convex sets in R^d, every connected component of the space of line transversals to this family is acyclic (i.e., has trivial reduced homology).

Additional mathematical guidance:
None

Return only the S0 blueprint artifact.