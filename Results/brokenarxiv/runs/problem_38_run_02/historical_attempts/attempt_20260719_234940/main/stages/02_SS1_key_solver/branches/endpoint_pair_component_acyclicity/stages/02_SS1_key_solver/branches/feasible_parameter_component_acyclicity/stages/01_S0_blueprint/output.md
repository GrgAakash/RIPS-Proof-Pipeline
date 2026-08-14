1. Target normalization

target_label: feasible-parameter acyclicity for ordered convex transversals

task_type: proof

exact_target_statement: For `d>=1`, `m>=2`, and pairwise disjoint open convex `C_1,...,C_m subset R^d`, with `Delta`, `P_lambda`, and `D` as defined, prove every connected component of `D` has trivial reduced singular homology. For `m=2`, `Delta` is a point and `D` is that point if `C_1,C_2` are nonempty, otherwise empty.

statement_use_board:
  GIVEN:
    - statement_fragment: `d>=1`, `m>=2`, `C_i` pairwise disjoint open convex subsets of `R^d`
      permitted_use: local premise
    - statement_fragment: `0=lambda_1<lambda_2<...<lambda_{m-1}<lambda_m=1`
      permitted_use: parsing setup
    - statement_fragment: `P_lambda={(a,b) in C_1 x C_m : (1-lambda_i)a+lambda_i b in C_i}`
      permitted_use: parsing setup
    - statement_fragment: `D={lambda in Delta : P_lambda nonempty}`
      permitted_use: parsing setup
  TARGET:
    - statement_fragment: every connected component of `D` is acyclic
      requested_output_role: prove reduced singular homology vanishes
  SOURCE_OR_THEOREM_CLAIM:
    - statement_fragment: finite-dimensional good-cover / acyclic-carrier machinery
      answer_determining: true
      permitted_use: route_guidance_only
      needed_distinguishing_support: exact in-artifact statement and proof
    - statement_fragment: specialized line-transversal acyclicity theorem
      answer_determining: true
      permitted_use: not_used
      needed_distinguishing_support: None; forbidden by run instructions

variables_domains_assumptions_and_quantifiers: Universal quantifiers over all allowed `d,m,C_i`; `lambda` ranges over the open ordered simplex for `m>=3`; reduced singular homology is taken with integer coefficients unless final proof explicitly proves a stronger coefficient statement.

inferred_standard_setup: For fixed `lambda`, `P_lambda` is an open convex subset of `C_1 x C_m`. For fixed `(a,b)`, the admissible parameter set is `B_(a,b)=Delta cap prod_i I_i(a,b)`, where `I_i(a,b)={t : (1-t)a+tb in C_i}` is an open interval or empty.

reading_assumptions_used: Empty convex sets are allowed unless excluded; if any required `C_i` is empty then `D` has no components. The `m=2` convention is part of the target.

required_final_output: A proof, not merely a recognition statement, that every connected component of `D` has all reduced singular homology groups zero.

required_directions: Prove the nontrivial `m>=3` case and separately dispatch `m=2` and empty-set edge cases.

2. Task-adaptive proof obligations

primary_claim: Each connected component `Omega` of `D` is acyclic.

converse_or_sharpness_requirement: NOT_APPLICABLE - no converse, classification, or optimal bound is requested.

existence_or_feasibility_requirement: Show the feasible set is exactly the projection of the endpoint-parameter incidence relation and handle the case where no feasible parameters exist.

uniqueness_or_exhaustiveness_requirement: Cover every connected component of `D`, not only the component containing a chosen base parameter.

domain_and_edge_cases: `m=2`; `m=3`; some `C_i` empty; strict inequalities in `Delta`; open rather than closed convex sets; reduced `H_0` for connected components.

independent_stress_test: Attack the central topological lemma, infinite-cover passage, component restriction, hidden use of forbidden line-transversal results, and all edge cases.

3. Available tools

tool: affine preimage and finite intersection convexity
source_status: standard background fact
exact_statement_or_fact: Preimages of convex open sets under affine maps are convex open; products and finite intersections of convex open sets are convex open.
intended_role_in_proof: Establish convexity of `P_lambda` and parameter boxes.

tool: interval section of a convex set along a line
source_status: standard background fact
exact_statement_or_fact: For fixed `a,b`, `{t : (1-t)a+tb in C_i}` is an open interval, possibly empty.
intended_role_in_proof: Describe fixed-endpoint feasible parameter boxes.

tool: finite-dimensional good-cover nerve / acyclic-carrier argument
source_status: proved inside the current proof
exact_statement_or_fact: Exact finite-cover homology comparison needed for convex open cover pieces and acyclic intersections.
intended_role_in_proof: Reduce homology of a compact cycle in a component to a finite combinatorial carrier.

tool: box-incidence acyclicity lemma
source_status: proved inside the current proof
exact_statement_or_fact: For this endpoint/parameter incidence relation, convex endpoint fibers plus convex parameter boxes force every projection component in parameter space to be acyclic.
intended_role_in_proof: Main mechanism proving the target.

tool: ordinary singular homology compactness/direct-limit facts
source_status: standard background fact
exact_statement_or_fact: A singular cycle has compact image and is controlled by a finite subcover; reduced homology of a point is zero.
intended_role_in_proof: Pass from finite carrier arguments to singular homology of arbitrary components.

4. Subclaim support graph

id: SC1
statement: If `m=2` or some `C_i` is empty, the theorem follows directly from the stated convention or vacuity.
uses_prior_subclaims: []
purpose: Edge-case discharge.
status: must be proved in final solution.
suggested_solver: SS3

id: SC2
statement: For each fixed `lambda in Delta`, `P_lambda` is open convex in `C_1 x C_m`.
uses_prior_subclaims: []
purpose: Vertical convex fiber of the incidence relation.
status: must be proved in final solution.
suggested_solver: SS3

id: SC3
statement: For each fixed `(a,b)`, `B_(a,b)={lambda : (a,b) in P_lambda}` is open convex, and every nonempty `B_(a,b)` lies in one connected component of `D`.
uses_prior_subclaims: []
purpose: Horizontal convex fiber and component-local cover.
status: must be proved in final solution.
suggested_solver: SS3

id: SC4
statement: For `m>=3`, `D` is the parameter projection of the incidence relation `R={(a,b,lambda):(a,b) in P_lambda}` whose vertical and horizontal fibers are convex.
uses_prior_subclaims: [SC2, SC3]
purpose: Normalize the target into a convex-incidence problem.
status: must be proved in final solution.
suggested_solver: SS1

id: SC5
statement: The exact box-incidence acyclicity lemma applies to every connected component of the parameter projection.
uses_prior_subclaims: [SC2, SC3, SC4]
purpose: Main homological engine.
status: must be proved in final solution.
suggested_solver: SS2

id: SC6
statement: Applying SC5 to `R` gives trivial reduced singular homology for every component of `D`.
uses_prior_subclaims: [SC1, SC4, SC5]
purpose: Final target deduction.
status: must be proved in final solution.
suggested_solver: SS1

5. Target-determining claim register

claim_id: TDC-1
claim: The fixed-parameter fibers `P_lambda` are convex at exactly the strength needed for the carrier argument.
why_it_determines_the_answer: Without this, the topological mechanism cannot fill cycles.
known_competing_variants: Convex only after closure; nonempty but disconnected; open convex as required.
expected_basis: derived_here

claim_id: TDC-2
claim: The fixed-endpoint parameter sets `B_(a,b)` are convex and component-local.
why_it_determines_the_answer: The cover of each component depends on these sets being acyclic and not crossing components.
known_competing_variants: Arbitrary good covers by boxes can have holes; component-locality is essential.
expected_basis: derived_here

claim_id: TDC-3
claim: The central topological lemma proves reduced singular homology of full components, not merely finite nerves or path-connectedness.
why_it_determines_the_answer: This is the exact acyclicity conclusion.
known_competing_variants: finite-cover acyclicity only; weak homotopy only; connectedness only.
expected_basis: derived_here

claim_id: TDC-4
claim: The `m=2` and empty-set conventions do not create an exceptional component with nontrivial reduced homology.
why_it_determines_the_answer: The theorem is quantified over all `m>=2`.
known_competing_variants: treating empty `D` as acyclic space rather than as having no components; forgetting the singleton convention.
expected_basis: derived_here

6. Mathematical Unknowns Ledger (blind-spot pass)

```yaml
unknown_id: U001
kind: theorem_identity
description: Exact strength and validity of the box-incidence acyclicity lemma needed for TDC-3.
target_determining: true
current_evidence: Fixed-parameter and fixed-endpoint fibers are convex, but arbitrary convex good covers can still have holes.
candidate_resolutions: ["a finite-dimensional acyclic-carrier/Dowker-style proof works for this incidence structure", "the convex-fiber facts alone are insufficient and the route must be narrowed or replaced"]
downstream_outcomes: ["target proof can proceed through SC5", "SC5 cannot be used and the global solver must find another mechanism"]
answer_sensitivity_rationale: The theorem's homology conclusion rests on this exact global step.
resolution_test_id: RTEST-001
required_resolution_test: State and prove the precise lemma, including finite-cycle reduction and component passage, without citing specialized line-transversal acyclicity.
assigned_solver: SS2
status: OPEN
```

```yaml
unknown_id: U002
kind: missing_hypothesis
description: Whether open/infinite covers can be reduced to finite homological data inside one connected component.
target_determining: true
current_evidence: Singular cycles have compact image, but the cover by all endpoint boxes is generally infinite and not chosen locally finite.
candidate_resolutions: ["compact image plus good-cover refinement gives finite carrier control", "a non-locally-finite gap prevents the argument"]
downstream_outcomes: ["ordinary singular homology vanishing follows", "only a finite approximation statement is proved"]
answer_sensitivity_rationale: The target concerns full singular homology of components.
resolution_test_id: RTEST-002
required_resolution_test: Give a chain-level finite-subcover reduction for an arbitrary singular cycle in a component and show the filling remains in that component.
assigned_solver: SS2
status: OPEN
```

```yaml
unknown_id: U003
kind: missing_hypothesis
description: Exact use of pairwise disjointness in the convex-box encoding for TDC-2.
target_determining: false
current_evidence: Convexity of `B_(a,b)` seems to follow from line-interval preimages and `Delta`; disjointness may only enforce geometric interpretation/order.
candidate_resolutions: ["disjointness is unnecessary for SC2-SC3", "disjointness is needed later in SC5 or an order argument"]
downstream_outcomes: ["proof records disjointness as unused in local convexity", "proof identifies the exact later hypothesis use"]
answer_sensitivity_rationale: Both outcomes can still prove the same target if the final proof accounts for the hypothesis.
resolution_test_id: None
required_resolution_test: None
assigned_solver: SS3
status: OPEN
```

```yaml
unknown_id: U004
kind: convention
description: Edge convention for empty convex sets and the `m=2` point simplex, related to TDC-4.
target_determining: true
current_evidence: Target explicitly supplies the `m=2` convention; for empty `D`, there are no connected components.
candidate_resolutions: ["handle by vacuity/singleton reduced homology", "incorrectly require nonempty all `C_i` without proof"]
downstream_outcomes: ["edge cases are discharged", "the universal theorem is not fully proved"]
answer_sensitivity_rationale: A missing edge-case proof leaves the quantified theorem incomplete.
resolution_test_id: RTEST-004
required_resolution_test: Write the explicit `m=2` and empty-`C_i` argument before invoking the `m>=3` machinery.
assigned_solver: SS3
status: OPEN
```

7. Key-step and key-solver selection

hardest_step_id: SC5

hardest_step_description: Prove the exact finite-dimensional box-incidence acyclicity lemma and pass it to singular homology of each component.

risk_if_wrong: The argument collapses to a good-cover observation, which is insufficient because good covers by convex sets can model nontrivial homology.

key_solver_id: SS1

global_solver_id: SS1

why_this_solver_is_key: SS1 must produce the complete proof, integrate the topological lemma only if fully derived, and ensure all edge cases and unknowns are discharged.

what_would_invalidate_the_route: A counterexample to SC5 under the exact incidence hypotheses, failure of the finite-cover-to-component passage, or hidden reliance on a forbidden line-transversal theorem.

8. Failure-mode checks

circularity_check: Do not assume component acyclicity, contractibility of line-transversal spaces, or any theorem equivalent to the target.

full_theorem_check: Cover all `d>=1`, all `m>=2`, all components, and possible empty sets.

source_check: No web, no prior branch output, no specialized line-transversal acyclicity citation.

hypothesis_check: Verify openness, convexity, strict ordering, pairwise disjointness, and nonempty/vacuous cases exactly where used.

notation_check: Keep endpoint variables `(a,b)`, parameters `lambda_i`, and line-section variables `t` distinct.

standard_background_check: Any nerve/carrier theorem must be stated and proved or used only at exact elementary finite-dimensional strength.

answer_anchor_check: The final conclusion is vanishing reduced singular homology of each component, not just connectedness or local contractibility.

task_type_obligation_check: This is a proof task; no final solution is written by S0, but subsolvers must be assigned deliverables capable of producing one.

9. Subsolver execution plan

constructive_solver_count: 3

subsolver_count: 4

subsolver_count_rationale: One global/key solver is necessary for a complete candidate proof; one topological specialist is justified by the central homological carrier lemma; one geometric/edge-case specialist is justified by independent local convexity and boundary obligations; one adversarial stress tester runs last.

specialist_escalation_rationale: SS2 is needed for SC5 and U001-U002. SS3 is needed for SC1-SC3 and U003-U004. No additional specialists are justified.

global_solver_id: SS1

key_solver_id: SS1

stress_test_solver_id: SS4

coverage_check: PASS - SC1 through SC6 and U001 through U004 are assigned.

independence_check: PASS - SS2 proves the abstract topological engine; SS3 verifies geometric hypotheses and edge cases; SS1 integrates into a complete proof; SS4 only attacks completed constructive outputs.

10. Subsolver assignment table

SS1:
role: global/key solver
work_scope: global_solution
assigned_subclaim_ids: SC1, SC2, SC3, SC4, SC5, SC6
task: Produce one coherent complete candidate proof of the target. Use the endpoint/parameter incidence relation, prove all required convexity facts, include or correctly invoke an in-artifact proof of SC5, and handle all edge cases.
required_deliverable: Complete proof candidate with an unknown-discharge table for U001-U004 and explicit treatment of TDC-1 through TDC-4.
connection_to_target: Directly proves the target theorem.
where_used_in_final_solution: Base candidate for S6 composition.
independence_constraint: Must not see other current-round constructive outputs before submitting.
failure_or_salvage_focus: If SC5 is too broad or false, narrow the lemma to the exact interpolation incidence relation or report the obstruction precisely.

SS2:
role: targeted specialist
work_scope: assigned_subclaim
assigned_subclaim_ids: SC5
task: Prove the exact box-incidence acyclicity lemma needed for the theorem, including finite-cycle reduction, convex carrier construction, and passage from finite data to reduced singular homology of a component.
required_deliverable: Rigorous standalone subproof of SC5, or a precise obstruction/counterexample showing the planned lemma is invalid.
connection_to_target: Supplies the main homological engine.
where_used_in_final_solution: Inserted at the central proof step after SC2-SC4.
independence_constraint: Work only from the target statement, allowed support rules, and this blueprint; do not use line-transversal acyclicity theorems.
failure_or_salvage_focus: Distinguish failure of arbitrary good covers from any extra structure supplied by endpoint convex fibers.

SS3:
role: targeted specialist
work_scope: assigned_subclaim
assigned_subclaim_ids: SC1, SC2, SC3
task: Verify all local geometric and edge-case facts: `m=2`, empty sets, convexity/openness of `P_lambda`, interval nature of line sections, convexity/openness/component-locality of `B_(a,b)`, and exact role of pairwise disjointness.
required_deliverable: Concise rigorous subproofs of SC1-SC3 and proposed resolutions for U003-U004.
connection_to_target: Supplies the hypotheses needed before the topological engine can be applied.
where_used_in_final_solution: Opening normalization and incidence-verification sections.
independence_constraint: Do not attempt the global homology proof except as needed to state hypotheses cleanly.
failure_or_salvage_focus: Find any edge case where strict inequalities, emptiness, or ordering breaks the incidence setup.

SS4:
role: adversarial stress test
work_scope: adversarial_stress_test
assigned_subclaim_ids: SC1, SC2, SC3, SC4, SC5, SC6
task: After receiving all constructive outputs, try to break the proof. Attack SC5, U001-U002, infinite-cover handling, component-locality, edge cases, and any hidden citation or theorem-strength mismatch.
required_deliverable: Stress report with `stress_test_verdict: PASS / BLOCK / INCONCLUSIVE`, list of attacked TDCs, unresolved unknowns, and any blocking defects.
connection_to_target: Prevents acceptance of an unsupported acyclicity proof.
where_used_in_final_solution: Determines whether S6 may compose or must route a challenge/support request.
independence_constraint: Runs last and receives the constructive outputs; has no constructive proof obligation.
failure_or_salvage_focus: Block if the proof proves only connectedness, finite nerve acyclicity, or a stronger unsupported theorem without proof.

11. Web-source confirmation

no web sources used