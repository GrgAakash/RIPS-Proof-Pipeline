1. Target normalization

target_label: main spectral-radius/density bound  
task_type: proof  
exact_target_statement: For every fixed \(1<p\le 2\), there is a constant \(C_p>0\), depending only on \(p\), such that every \(n\)-vertex graph \(G\) with at least one edge satisfies
\[
\lambda(G)\le (C_p+o(1))\,d_p(G)\,n^{\max\{1/2,p-1\}}
\]
as \(n\to\infty\), where \(d_p(G)=\max_{\emptyset\ne S\subseteq V(G)} e(G[S])/|S|^p\).  
variables_domains_assumptions_and_quantifiers: \(G\) is a finite \(n\)-vertex graph with at least one edge; \(1<p\le 2\) is fixed; \(\lambda(G)\) is adjacency spectral radius; \(S\) ranges over nonempty vertex subsets.  
inferred_standard_setup: Use the supplied \(p=3/2\) spectral-radius estimate E001 and compare \(d_{3/2}(G)\) to \(d_p(G)\) by elementary maximization over subsets.  
reading_assumptions_used: Graphs are finite simple graphs as implied by adjacency matrix and induced edge count notation; asymptotic \(o(1)\) is with fixed \(p\) and \(n\to\infty\).  
required_final_output: A proof establishing the stated inequality with some \(C_p\), ideally by proving the stronger bound with \(C_p=C_0\).  
required_directions: Prove the upper bound only; no lower-bound or sharpness claim is requested.

2. Task-adaptive proof obligations

primary_claim: Derive \(\lambda(G)\le C_p d_p(G)n^{\max\{1/2,p-1\}}\), which implies the stated \((C_p+o(1))\) version.  
converse_or_sharpness_requirement: NOT_APPLICABLE; the theorem asks only for existence of an upper-bound constant.  
existence_or_feasibility_requirement: Show a valid constant \(C_p>0\) exists for every fixed \(1<p\le2\).  
uniqueness_or_exhaustiveness_requirement: NOT_APPLICABLE; no classification or uniqueness statement is present.  
domain_and_edge_cases: Handle \(p<3/2\), \(p=3/2\), \(p>3/2\), and graphs with at least one edge; subsets with zero induced edges contribute zero to all relevant maxima.  
independent_stress_test: Check the exponent against complete graphs and sparse graphs such as a single edge: the route should give \(n^{p-1}\) for \(p\ge3/2\) and \(n^{1/2}\) for \(p\le3/2\).

3. Available tools

tool: Definition of \(d_p(G)\)  
source_status: provided definition / notation / assumption  
exact_statement_or_fact: \(d_p(G)=\max_{\emptyset\ne S\subseteq V(G)} e(G[S])/|S|^p\).  
intended_role_in_proof: Convert every induced-subgraph edge count into \(e(G[S])\le d_p(G)|S|^p\).

tool: [INTERNALLY VERIFIED AUXILIARY RESULT E001]  
source_status: additional guidance item  
exact_statement_or_fact: There is an absolute constant \(C_0>0\) such that every \(N\)-vertex graph \(H\) with at least one edge satisfies \(\lambda(H)\le C_0\sqrt N\,d_{3/2}(H)\).  
intended_role_in_proof: Apply with \(H=G\), \(N=n\), then reduce to bounding \(d_{3/2}(G)\) by \(d_p(G)\).

tool: Subset-size comparison  
source_status: proved inside the current proof  
exact_statement_or_fact: For every nonempty \(S\subseteq V(G)\),
\[
\frac{e(G[S])}{|S|^{3/2}}
\le d_p(G)|S|^{p-3/2}.
\]
Then \(|S|^{p-3/2}\le1\) if \(p\le3/2\), and \(|S|^{p-3/2}\le n^{p-3/2}\) if \(p\ge3/2\).  
intended_role_in_proof: Establish \(d_{3/2}(G)\le d_p(G)n^{\max\{0,p-3/2\}}\).

tool: Elementary exponent arithmetic  
source_status: standard background fact  
exact_statement_or_fact: \(\sqrt n\,n^{\max\{0,p-3/2\}}=n^{\max\{1/2,p-1\}}\).  
intended_role_in_proof: Convert the E001 bound into the target exponent.

4. Subclaim support graph

id: SC001  
statement: E001 applies to \(G\), giving \(\lambda(G)\le C_0\sqrt n\,d_{3/2}(G)\).  
uses_prior_subclaims: []  
purpose: Main spectral-radius input.  
status: follows from guidance  
suggested_solver: SS1

id: SC002  
statement: For each nonempty \(S\), \(e(G[S])/|S|^{3/2}\le d_p(G)|S|^{p-3/2}\).  
uses_prior_subclaims: []  
purpose: Pointwise comparison of density parameters.  
status: must be proved in final solution  
suggested_solver: SS1

id: SC003  
statement: \(d_{3/2}(G)\le d_p(G)n^{\max\{0,p-3/2\}}\) for all \(1<p\le2\).  
uses_prior_subclaims: [SC002]  
purpose: Bridge from E001 to the target \(p\)-density.  
status: must be proved in final solution  
suggested_solver: SS1

id: SC004  
statement: Combining SC001 and SC003 yields \(\lambda(G)\le C_0d_p(G)n^{\max\{1/2,p-1\}}\).  
uses_prior_subclaims: [SC001, SC003]  
purpose: Complete the target bound.  
status: must be proved in final solution  
suggested_solver: SS1

id: SC005  
statement: The stronger exact bound implies the requested \((C_p+o(1))\) form with \(C_p=C_0\).  
uses_prior_subclaims: [SC004]  
purpose: Match the theorem’s asymptotic phrasing.  
status: must be proved in final solution  
suggested_solver: SS1

5. Critical Claims Ledger

```yaml
critical_claim_id: CC001
claim: "E001 may be applied directly to the target graph G with N=n, because G is an n-vertex graph with at least one edge."
why_critical: "This is the only permitted nontrivial spectral-radius input; without it the route has no spectral estimate."
live_alternatives: []
resolution_test: "Check E001 hypotheses against the target hypotheses exactly."
basis: sealed_guidance_E001
status: ESTABLISHED
owner: SS1
```

```yaml
critical_claim_id: CC002
claim: "For all 1<p<=2, d_{3/2}(G) <= d_p(G) n^{max(0,p-3/2)}."
why_critical: "This comparison determines the final power of n and is the only bridge from E001 to the desired p-density."
live_alternatives: ["d_{3/2}(G) <= d_p(G) n^{p-3/2} for all p", "d_{3/2}(G) <= d_p(G) n^{max(0,p-3/2)}"]
resolution_test: "For each nonempty S, compare e(G[S])/|S|^{3/2} with d_p(G)|S|^{p-3/2}, then split p<=3/2 and p>=3/2."
basis: derived_here
status: ESTABLISHED
owner: SS1
```

```yaml
critical_claim_id: CC003
claim: "The exponent after applying E001 is 1/2 + max(0,p-3/2) = max(1/2,p-1)."
why_critical: "A wrong exponent would change the target theorem."
live_alternatives: ["max(1/2,p-1)", "p-1 for all p", "1/2 for all p"]
resolution_test: "Evaluate the expression separately on p<=3/2 and p>=3/2."
basis: derived_here
status: ESTABLISHED
owner: SS1
```

6. Key-step and Main Solver selection

hardest_step_id: SC003  
hardest_step_description: Prove the density comparison \(d_{3/2}(G)\le d_p(G)n^{\max\{0,p-3/2\}}\) without mishandling the \(p<3/2\) case.  
risk_if_wrong: The final exponent becomes false or unsupported, especially if \(n^{p-3/2}\) is used when \(p<3/2\).  
main_solver_id: SS1  
key_solver_id: SS1  
global_solver_id: SS1  
why_this_solver_is_M: The proof is short and globally integrated; one Main Solver should own the E001 application, the density comparison, and the final asymptotic conversion.  
what_would_invalidate_the_route: Any failure of E001 applicability, any counterexample to CC002, or an interpretation of \(o(1)\) requiring more than a fixed exact constant bound.

7. Failure-mode checks

circularity_check: PASS; the route uses only E001 and elementary comparison, not the target theorem.  
full_theorem_check: PASS; covers every fixed \(1<p\le2\), every \(n\)-vertex graph with at least one edge, and the requested asymptotic inequality.  
source_check: PASS; no external theorem or paper-specific result is used besides E001.  
hypothesis_check: PASS; E001 requires at least one edge, matching the target.  
notation_check: PASS; \(d_{3/2}\) is the same induced-density maximum as \(d_p\) with \(p=3/2\).  
standard_background_check: PASS; only elementary inequalities for subset sizes and exponents are used.  
answer_anchor_check: PASS; the final bound can take \(C_p=C_0\), an absolute constant and therefore a valid \(p\)-dependent constant.  
task_type_obligation_check: PASS; proof task only, no construction, converse, or sharpness obligation.

8. Subsolver execution plan

constructive_solver_count: 1  
subsolver_count: 2  
subsolver_count_rationale: One Main Solver is sufficient for the complete proof; one separate Defender runs last to attack edge cases, exponent arithmetic, E001 usage, and asymptotic phrasing.  
specialist_escalation_rationale: `NOT_NEEDED - post-Main-Solver assistance routing has not run yet`  
main_solver_id: SS1  
global_solver_id: SS1  
key_solver_id: SS1  
defender_solver_id: SS2  
stress_test_solver_id: SS2  
attacker_solver_ids: []  
coverage_check: PASS - SS1 covers SC001-SC005; SS2 provides only adversarial review after the integrated proof exists.  
independence_check: PASS - SS1 and SS2 have distinct roles; no duplicate constructive assignment is present.

9. Subsolver assignment table

SS1:  
role: Main Solver  
work_scope: global_solution  
assigned_subclaim_ids: [SC001, SC002, SC003, SC004, SC005]  
task: Produce one coherent complete proof of the target theorem using E001 exactly as stated and proving all remaining comparison steps from definitions.  
required_deliverable: Candidate answer, complete scratch-work attempt, uncertain_steps, help_requests, and proposed_board_updates.  
connection_to_target: SS1 owns the full derivation of \(\lambda(G)\le(C_p+o(1))d_p(G)n^{\max\{1/2,p-1\}}\).  
where_used_in_final_solution: Entire final proof.  
independence_constraint: Do not use web sources, prior outputs, hidden proof of E001, answer keys, or unlisted lemmas.  
failure_or_salvage_focus: If the direct comparison fails, isolate whether the obstruction is \(p<3/2\), zero-edge subsets, or asymptotic constant phrasing.

SS2:  
role: defender  
work_scope: adversarial_stress_test  
assigned_subclaim_ids: []  
task: Run last, after receiving SS1’s integrated proof, and attack the proof for circularity, misuse of E001, wrong exponent handling, missing edge cases, and unsupported constants.  
required_deliverable: A concise adversarial report listing fatal flaws if any, otherwise a pass with residual risks.  
connection_to_target: Protects validity of the final upper-bound proof.  
where_used_in_final_solution: Used only to decide whether SS1’s proof needs repair before finalization.  
independence_constraint: Do not construct an alternative proof unless needed to explain a detected flaw; do not use sources outside the supplied packet and this blueprint.  
failure_or_salvage_focus: Focus on \(p<3/2\), \(p=3/2\), \(p>3/2\), single-edge graphs, complete graphs, and the transition from an exact bound to \((C_p+o(1))\).

10. Web-source confirmation

no web sources used