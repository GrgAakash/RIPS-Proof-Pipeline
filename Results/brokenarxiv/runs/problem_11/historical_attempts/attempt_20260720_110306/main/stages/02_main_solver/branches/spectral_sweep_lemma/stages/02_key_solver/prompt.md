Fresh no-history solver-only branch experiment. Do not use memory, prior task history, previous outputs outside this prompt, answer keys, files outside this prompt, web search/internet, API keys, or Python. You are branch SS1. This is a no-internet Dynamic Worker Solver run. Follow the latest Dynamic Worker Solver prompt from `pipeline_sources/Prompt Packet/Prompts.md`: as Main Solver with `work_scope: global_solution`, solve the complete branch target in one coherent argument before support workers. Use only supplied packet, allowed definitions, current branch Manager routing, standard background, and facts proved in your own proof. Do not use external sources.

Required output sections:
1. Assignment restatement
2. Subproof or failure, with final proof body wrapped in `<!-- BEGIN_FINAL_PROOF -->` and `<!-- END_FINAL_PROOF -->` if solved
3. Solver failure output and candidate guidance as one fenced YAML block with standard keys; include `main_solver_proof_key: true` only if complete
4. Local Source Ledger, including critical claim statuses and addendum
5. Interface notes for Manager acceptance
6. Web-source confirmation

--- INPUTS FOR THIS BRANCH RUN ---
Cleaned skeleton/packet:
Standalone auxiliary lemma packet only. It contains the target lemma statement and definitions: spectral radius of adjacency matrix, induced edge count e(H[S]), and d_{3/2}(H)=max_{nonempty S subset V(H)} e(H[S])/|S|^{3/2}. No prior theorem statements, proof content, or answer key.

Target lemma:
There is an absolute constant C>0 such that every N-vertex graph H with at least one edge satisfies
lambda(H) <= C sqrt(N) d_{3/2}(H),
where lambda(H) is the adjacency spectral radius and d_{3/2}(H)=max_{nonempty S subseteq V(H)} e(H[S]) / |S|^{3/2}.

Additional mathematical guidance:
None

Branch Manager routing plan:
1. Target normalization: prove the exact target lemma for finite simple undirected N-vertex H with at least one edge. C absolute.
2. Obligations: prove uniform quadratic form x^T A_H x <= C sqrt(N) d_{3/2}(H)||x||_2^2 for all real x, then Rayleigh.
3. Tools: definition e(S)<=D|S|^{3/2}; Rayleigh quotient; nonnegative reduction |x^TAx|<=|x|^TA|x|; layer-cake; nested threshold-set edge control; finite integral closure if valid.
4. Subclaims:
SC1 reduce to nonnegative vectors.
SC2 for nonnegative x, use S_t={v:x_v>=t} and express x^TAx as integral over ordered edge counts between S_s and S_t.
SC3 control nested threshold edge counts from induced d_{3/2}; distinguish ordered/unordered factors.
SC4 bound resulting threshold integral by O(sqrt(N)||x||_2^2) with no log loss.
SC5 take Rayleigh supremum.
5. Critical Claims Ledger:
```yaml
critical_claim_id: CC001
claim: "Bounding |x^T A_H x| for all real x by B||x||_2^2 is sufficient to bound the adjacency spectral radius by B."
why_critical: "If only the top eigenvalue for nonnegative vectors is controlled, negative eigenvalues might be missed."
live_alternatives: ["Rayleigh/operator norm bound controls spectral radius", "Only largest eigenvalue controlled"]
resolution_test: "Use symmetry of A_H and |x^TA_Hx| <= |x|^TA_H|x| to check all real x."
basis: standard_background
status: ESTABLISHED
owner: Manager
```
```yaml
critical_claim_id: CC002
claim: "For nested threshold sets T subseteq S, the ordered edge count between S and T is at most 2e(H[S]) and therefore at most 2d_{3/2}(H)|S|^{3/2}."
why_critical: "This injects induced-edge control and convention errors change constants."
live_alternatives: ["factor 1 unordered", "factor 2 ordered", "larger bound if nesting mishandled"]
resolution_test: "Fix x^TA_Hx as ordered adjacency sum and verify every counted ordered edge has both endpoints inside the larger threshold set S."
basis: derived_here
status: OPEN
owner: Main Solver
```
```yaml
critical_claim_id: CC003
claim: "The threshold integral produces O(sqrt(N)||x||_2^2) with no logarithmic loss."
why_critical: "A log loss would not prove the lemma."
live_alternatives: ["double integral reduces to constant times integral t n(t)^{3/2}dt", "dyadic summation introduces log N"]
resolution_test: "With n(t)=|S_t|, compute the double integral carefully using min/max threshold ordering, then apply n(t)^{3/2}<=sqrt(N)n(t) and ||x||_2^2=int 2t n(t)dt, or identify failure."
basis: derived_here
status: OPEN
owner: Main Solver
```
6. Key step: SC4 threshold integral closure.

Subsolver assignment:
SS1:
role: Main Solver
work_scope: global_solution
assigned_subclaim_ids: [SC1, SC2, SC3, SC4, SC5]
task: Produce one coherent self-contained candidate proof of the exact target lemma using the spectral threshold-sweep route if valid, or another internally proved route. Do not cite external theorems beyond standard finite-dimensional symmetric-matrix background and elementary finite integral identities. Prove the ordered/unordered edge-count convention carefully.
required_deliverable: Candidate answer, complete scratch-work attempt, uncertain_steps, help_requests, proposed_board_updates. Include explicit handling of CC002 and CC003.
connection_to_target: Owns the complete proof of lambda(H)<=C sqrt(N)d_{3/2}(H).
where_used_in_final_solution: Main body of the branch proof, subject to Defender review.
independence_constraint: Must not rely on Defender, Midfielders, Attackers, prior task history, answer keys, web search, or unsupported formal statements.
failure_or_salvage_focus: If the threshold integral route fails, identify exactly whether the failure is spectral reduction, edge-count control, or integral closure, and propose the smallest needed auxiliary subclaim.