1. Target normalization

target_label: Spectral sweep auxiliary lemma

task_type: proof

exact_target_statement: There is an absolute constant \(C>0\) such that every \(N\)-vertex graph \(H\) with at least one edge satisfies
\[
\lambda(H)\le C\sqrt N\, d_{3/2}(H),
\]
where \(\lambda(H)\) is the adjacency spectral radius and
\[
d_{3/2}(H)=\max_{\emptyset\ne S\subseteq V(H)}\frac{e(H[S])}{|S|^{3/2}}.
\]

variables_domains_assumptions_and_quantifiers: \(H\) is a finite simple undirected graph, \(N=|V(H)|\), \(N\ge2\), \(H\) has at least one edge, \(S\) ranges over nonempty vertex subsets, \(e(H[S])\) is the induced edge count, and \(C\) must be independent of \(H\) and \(N\).

inferred_standard_setup: The adjacency matrix is real symmetric and nonnegative. The proof may use the Rayleigh quotient for symmetric matrices and elementary finite-sum/integral layer-cake identities. It should prove all graph-specific estimates from the definition of \(d_{3/2}\).

reading_assumptions_used: “Graph” is read as finite simple undirected graph. No skeleton theorem, paper lemma, external spectral estimate, or answer key is available. The parent intended-use note is motivational only and is not part of the branch target.

required_final_output: A self-contained proof of the displayed inequality with some explicit or implicit absolute constant \(C\).

required_directions: Only the upper bound \(\lambda(H)\le C\sqrt N\,d_{3/2}(H)\) is required. No sharpness, converse, or best constant is required.

2. Task-adaptive proof obligations

primary_claim: Prove a uniform quadratic-form bound
\[
x^\top A_H x\le C\sqrt N\,d_{3/2}(H)\|x\|_2^2
\]
for all real vectors \(x\), then take the Rayleigh supremum.

converse_or_sharpness_requirement: NOT_APPLICABLE - the target asks only for existence of an absolute constant.

existence_or_feasibility_requirement: Establish that one admissible absolute constant works for all finite \(N\)-vertex graphs with at least one edge.

uniqueness_or_exhaustiveness_requirement: NOT_APPLICABLE - no classification or unique extremal structure is requested.

domain_and_edge_cases: Handle isolated vertices, disconnected graphs, the one-edge graph, threshold sets that are empty, zero vector exclusion in Rayleigh quotients, and sign changes in test vectors.

independent_stress_test: Defender should test the route on a star, complete graph, complete bipartite graph with unequal sides, one-edge graph plus isolated vertices, and vectors with mixed signs.

3. Available tools

tool: Definition of \(d_{3/2}(H)\)
source_status: provided definition
exact_statement_or_fact: For every nonempty \(S\subseteq V(H)\), \(e(H[S])\le d_{3/2}(H)|S|^{3/2}\).
intended_role_in_proof: Converts every threshold-set induced edge count into the target density parameter.

tool: Rayleigh quotient for real symmetric matrices
source_status: standard background fact
exact_statement_or_fact: The spectral radius of the adjacency matrix can be bounded by proving \(|x^\top A_Hx|\le B\|x\|_2^2\) for all real \(x\).
intended_role_in_proof: Reduces the spectral claim to a quadratic-form estimate.

tool: Nonnegative reduction
source_status: standard background fact / proved inside the current proof
exact_statement_or_fact: Since \(A_H\) has nonnegative entries, \(|x^\top A_Hx|\le |x|^\top A_H|x|\).
intended_role_in_proof: Allows Main Solver to work only with nonnegative vectors.

tool: Layer-cake representation
source_status: standard background fact / proved inside the current proof
exact_statement_or_fact: For \(x_v\ge0\), \(x_v=\int_0^\infty 1_{\{x_v\ge t\}}dt\) and \(x_v^2=\int_0^\infty 2t\,1_{\{x_v\ge t\}}dt\).
intended_role_in_proof: Expresses the adjacency quadratic form and \(\ell_2\)-norm through threshold sets.

tool: Nested threshold-set edge control
source_status: proved inside the current proof
exact_statement_or_fact: If \(T\subseteq S\), the ordered adjacency edge count from \(S\) to \(T\) is at most \(2e(H[S])\le 2d_{3/2}(H)|S|^{3/2}\).
intended_role_in_proof: Controls cross-threshold contributions without importing a cut-norm theorem.

tool: Finite integral inequality
source_status: proved inside the current proof
exact_statement_or_fact: If \(n(t)=|\{v:x_v\ge t\}|\le N\), then \(n(t)^{3/2}\le \sqrt N\,n(t)\), so the threshold integral is bounded by a constant times \(\sqrt N\|x\|_2^2\).
intended_role_in_proof: Produces the required \(\sqrt N\) factor and avoids logarithmic loss.

4. Subclaim support graph

id: SC1
statement: It suffices to prove the quadratic-form bound for nonnegative vectors \(x\).
uses_prior_subclaims: []
purpose: Converts the spectral-radius target into an analytic inequality over threshold sets.
status: standard background / must be proved in final solution as a short reduction.
suggested_solver: SS1

id: SC2
statement: For nonnegative \(x\), write \(S_t=\{v:x_v\ge t\}\) and express \(x^\top A_Hx\) as an integral over ordered edge counts between \(S_s\) and \(S_t\).
uses_prior_subclaims: [SC1]
purpose: Creates the spectral sweep mechanism.
status: must be proved in final solution.
suggested_solver: SS1

id: SC3
statement: Since threshold sets are nested, the ordered edge count between \(S_s\) and \(S_t\) is at most \(2d_{3/2}(H)|S_{\min(s,t)}|^{3/2}\), up to the chosen convention for ordered pairs.
uses_prior_subclaims: [SC2]
purpose: Injects the definition of \(d_{3/2}\) into the Rayleigh estimate.
status: must be proved in final solution.
suggested_solver: SS1

id: SC4
statement: The double integral of \(|S_{\min(s,t)}|^{3/2}\) is bounded by an absolute constant times \(\sqrt N\|x\|_2^2\).
uses_prior_subclaims: [SC3]
purpose: Closes the analytic estimate with the correct \(N\)-dependence.
status: must be proved in final solution.
suggested_solver: SS1

id: SC5
statement: Taking the supremum over nonzero \(x\) gives \(\lambda(H)\le C\sqrt N\,d_{3/2}(H)\).
uses_prior_subclaims: [SC1, SC2, SC3, SC4]
purpose: Returns from the quadratic-form estimate to the exact target lemma.
status: must be proved in final solution.
suggested_solver: SS1

5. Critical Claims Ledger

```yaml
critical_claim_id: CC001
claim: Bounding |x^T A_H x| for all real x by B||x||_2^2 is sufficient to bound the adjacency spectral radius by B.
why_critical: If the route only bounds the top eigenvalue for nonnegative vectors but misses possible negative eigenvalues, it may not control spectral radius.
live_alternatives: ["Rayleigh/operator norm bound controls spectral radius", "Only largest eigenvalue is controlled and negative eigenvalues require a separate argument"]
resolution_test: Use symmetry of A_H and the inequality |x^T A_H x| <= |x|^T A_H |x| to check the bound for every real vector.
basis: standard_background
status: ESTABLISHED
owner: Manager
```

```yaml
critical_claim_id: CC002
claim: For nested threshold sets T subseteq S, the ordered edge count between S and T is at most 2e(H[S]) and therefore at most 2d_{3/2}(H)|S|^{3/2}.
why_critical: This is the point where induced-edge control must dominate cross-threshold contributions; a wrong ordered/unordered convention can break the proof or change constants.
live_alternatives: ["factor 1 with unordered convention", "factor 2 with ordered adjacency convention", "larger bound needed if nesting is mishandled"]
resolution_test: Fix the convention in x^T A_H x as an ordered adjacency sum and verify that every counted ordered edge has both endpoints inside the larger threshold set S.
basis: derived_here
status: OPEN
owner: Main Solver
```

```yaml
critical_claim_id: CC003
claim: The threshold integral produces O(sqrt(N)||x||_2^2) with no logarithmic loss.
why_critical: A logarithmic loss would not prove the stated absolute-constant lemma.
live_alternatives: ["double integral equals or is bounded by a constant times integral t n(t)^{3/2} dt", "dyadic summation introduces an avoidable log N loss"]
resolution_test: With n(t)=|S_t|, compute the double integral using min(s,t) ordering and then apply n(t)^{3/2} <= sqrt(N)n(t) and ||x||_2^2 = integral 2t n(t) dt.
basis: derived_here
status: OPEN
owner: Main Solver
```

6. Key-step and Main Solver selection

hardest_step_id: SC4

hardest_step_description: Convert the two-parameter threshold integral into a one-parameter integral bounded by \(\sqrt N\|x\|_2^2\), preserving only an absolute constant.

risk_if_wrong: The plan may prove only a weaker logarithmic or incorrectly normalized estimate.

main_solver_id: SS1

key_solver_id: SS1

global_solver_id: SS1

why_this_solver_is_M: The proof is short and tightly coupled: spectral reduction, threshold decomposition, induced-edge control, and integral closure should be written as one coherent solution rather than split across constructive specialists.

what_would_invalidate_the_route: Failure of the nested-set ordered-edge bound, failure of the layer-cake identity under the chosen conventions, or discovery that the spectral-radius reduction controls only one side of the spectrum.

7. Failure-mode checks

circularity_check: The route must not assume the target lemma or any equivalent hereditary spectral-density theorem.

full_theorem_check: The final proof must cover every \(N\)-vertex graph with at least one edge, including disconnected graphs and graphs with isolated vertices.

source_check: No formal theorem, paper lemma, external spectral inequality, web source, or answer key is permitted. Only definitions, standard symmetric-matrix background, and internally proved estimates may be used.

hypothesis_check: Confirm \(N\ge2\) follows from “at least one edge,” and ensure empty threshold sets are harmless.

notation_check: Distinguish unordered induced edge count \(e(H[S])\) from ordered adjacency counts in \(x^\top A_Hx\).

standard_background_check: Rayleigh quotient, symmetry of adjacency matrices, finite Fubini/Tonelli, and elementary layer-cake identities are acceptable; graph-specific density estimates must be proved.

answer_anchor_check: The result asks for some absolute \(C\), so exact constants from factors 2 or 4 are not answer-sensitive as long as they are finite and universal.

task_type_obligation_check: This is a proof task, not an optimization or sharp-value task; no lower bound or extremal example is required.

8. Subsolver execution plan

constructive_solver_count: 1

subsolver_count: 2

subsolver_count_rationale: The first phase needs one Main Solver to produce a complete integrated proof and one separate Defender to attack that proof after it exists.

specialist_escalation_rationale: `NOT_NEEDED - post-Main-Solver assistance routing has not run yet`

main_solver_id: SS1

global_solver_id: SS1

key_solver_id: SS1

defender_solver_id: SS2

stress_test_solver_id: SS2

attacker_solver_ids: []

coverage_check: PASS - SS1 covers all constructive proof obligations SC1-SC5; SS2 covers adversarial stress testing after SS1 submits the integrated proof.

independence_check: PASS - SS1 has the only constructive assignment, and SS2 has no constructive proof obligation.

9. Subsolver assignment table

SS1:
role: Main Solver
work_scope: global_solution
assigned_subclaim_ids: [SC1, SC2, SC3, SC4, SC5]
task: Produce one coherent self-contained candidate proof of the exact target lemma using the spectral threshold-sweep route. Do not cite external theorems beyond standard finite-dimensional symmetric-matrix background and elementary finite integral identities. Prove the ordered/unordered edge-count convention carefully.
required_deliverable: Candidate answer, complete scratch-work attempt, uncertain_steps, help_requests, and proposed_board_updates. Include explicit handling of CC002 and CC003.
connection_to_target: Owns the complete proof of \(\lambda(H)\le C\sqrt N d_{3/2}(H)\).
where_used_in_final_solution: Main body of the eventual final proof, subject to Defender review.
independence_constraint: Must not rely on Defender, Midfielders, Attackers, prior task history, answer keys, web search, or unsupported formal statements.
failure_or_salvage_focus: If the threshold integral route fails, identify exactly whether the failure is spectral reduction, edge-count control, or integral closure, and propose the smallest needed auxiliary subclaim.

SS2:
role: defender
work_scope: adversarial_stress_test
assigned_subclaim_ids: []
task: Run last after receiving SS1’s integrated proof. Attack the proof for circularity, hidden external lemmas, ordered/unordered factor errors, threshold nesting mistakes, missing sign handling, empty-set issues, and edge cases such as stars, complete graphs, complete bipartite graphs, and one-edge graphs.
required_deliverable: A structured adversarial report listing PASS/BLOCK status, any failed Critical Claims Ledger items, exact location of defects, and whether defects are repairable without changing the route.
connection_to_target: Tests whether SS1’s proof genuinely establishes the target lemma under the packet restrictions.
where_used_in_final_solution: Used only for acceptance or repair decisions after the Main Solver proof exists.
independence_constraint: Must not supply a constructive replacement proof unless explicitly asked in a later routing round.
failure_or_salvage_focus: Focus on invalid reductions, hidden logarithmic losses, convention mismatches, and any use of non-allowed supporting statements.

10. Web-source confirmation

no web sources used