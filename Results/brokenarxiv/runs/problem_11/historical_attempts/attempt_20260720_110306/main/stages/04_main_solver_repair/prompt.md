Fresh no-history solver-only main experiment. Do not use memory, prior task history, previous outputs outside this prompt, answer keys, files outside this prompt, web search/internet, API keys, or Python. You are main SS1. This is a no-internet Dynamic Worker Solver run. Follow the latest Dynamic Worker Solver prompt structure: as Main Solver with work_scope global_solution, prove the complete target in one coherent argument; use only supplied packet, allowed definitions, guidance E001 exactly as stated, Manager routing for assignment, standard background, and facts proved in your own proof.

If a guidance item is labeled `[INTERNALLY VERIFIED AUXILIARY RESULT E###]`, use only its exact statement without reproof and identify E### at every load-bearing use. Do not reconstruct its hidden branch proof or infer stronger claims.

Required output sections:
1. Assignment restatement
2. Subproof or failure, with final proof body wrapped in `<!-- BEGIN_FINAL_PROOF -->` and `<!-- END_FINAL_PROOF -->`
3. Solver failure output and candidate guidance YAML with `failure_output_type: solved` and `main_solver_proof_key: true` only if complete
4. Local Source Ledger and critical claim statuses/addendum
5. Interface notes for Manager acceptance
6. Web-source confirmation

--- INPUTS FOR THIS MAIN RUN ---
Cleaned skeleton/packet:
Standalone theorem packet only. It contains the target statement and definitions: spectral radius of adjacency matrix, induced edge count e(G[S]), and d_p(G)=max_{nonempty S subset V(G)} e(G[S])/|S|^p. No prior theorem statements, no proof content, no answer key.

Target theorem:
Let lambda(G) denote the spectral radius (the largest eigenvalue of the adjacency matrix) of a graph G. For any 1 < p <= 2 and any n-vertex graph G, define d_p(G)=max_{nonempty S subseteq V(G)} e(G[S])/|S|^p, where e(G[S]) is the number of edges in the subgraph induced by S. Then there exists a constant C_p > 0 depending only on p such that every n-vertex graph G with at least one edge satisfies lambda(G) <= (C_p+o(1)) d_p(G) n^{max{1/2, p-1}} as n -> infinity.

Additional mathematical guidance:
[INTERNALLY VERIFIED AUXILIARY RESULT E001] Lemma statement: There is an absolute constant C0>0 such that every N-vertex graph H with at least one edge satisfies lambda(H) <= C0 sqrt(N) d_{3/2}(H), where d_{3/2}(H)=max_{nonempty S subseteq V(H)} e(H[S])/|S|^{3/2}. Independently verified status: ESTABLISHED by branch Manager acceptance. Permission: use this exact statement without reproof. Intended use location: reduce the main theorem to comparing d_{3/2}(G) with d_p(G).

Main Manager routing plan:
SS1 Main Solver assigned SC001-SC005:
SC001: Apply E001 to G with N=n: lambda(G)<=C0 sqrt(n)d_{3/2}(G).
SC002: For each nonempty S, prove e(G[S])/|S|^{3/2} <= d_p(G)|S|^{p-3/2}.
SC003: Prove d_{3/2}(G)<=d_p(G)n^{max(0,p-3/2)} for all 1<p<=2.
SC004: Combine to get lambda(G)<=C0 d_p(G)n^{max{1/2,p-1}}.
SC005: Exact bound implies (C_p+o(1)) form with C_p=C0.
Critical claims:
CC001: E001 applies directly to G with N=n because G is n-vertex and has at least one edge. Basis sealed_guidance_E001.
CC002: For all 1<p<=2, d_{3/2}(G)<=d_p(G)n^{max(0,p-3/2)}. Split p<=3/2 and p>=3/2.
CC003: 1/2+max(0,p-3/2)=max(1/2,p-1). Split p<=3/2 and p>=3/2.

Subsolver assignment:
SS1 role Main Solver, work_scope global_solution, assigned SC001-SC005. Produce one coherent complete proof using E001 exactly as stated and proving all comparison steps from definitions. Do not use web, hidden proof of E001, prior outputs, answer keys, or unlisted lemmas.