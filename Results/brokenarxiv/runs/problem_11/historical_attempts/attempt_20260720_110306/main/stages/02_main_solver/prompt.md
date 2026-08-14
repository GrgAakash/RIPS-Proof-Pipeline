Fresh no-history solver-only experiment. Do not use memory, prior task history, previous outputs outside this prompt, answer keys, files outside this prompt, web search/internet, API keys, or Python. You are SS1. This is a no-internet Dynamic Worker Solver integration/repair phase. Spawn setting: fork_context=false. Follow the latest Dynamic Worker Solver prompt from `pipeline_sources/Prompt Packet/Prompts.md`: as Main Solver with `work_scope: global_solution`, solve the complete target problem in one coherent argument; in the integration/repair phase, consider only Manager-approved constructive results supplied here. Write a full candidate solution, not suggestions; make clear whether your proof key is ready for Manager acceptance. Use only the supplied packet, allowed definitions, current-round Manager routing, approved support artifact, standard background, and facts proved in your own proof. Do not cite the Manager plan/support as mathematical premise unless the relevant derivation is present and correct. Do not use external sources.

Required output sections:
1. Assignment restatement
2. Subproof or failure, with the final proof body wrapped in `<!-- BEGIN_FINAL_PROOF -->` and `<!-- END_FINAL_PROOF -->` if solved
3. Solver failure output and candidate guidance as one fenced YAML block with the standard keys; include `main_solver_proof_key: true` only if complete
4. Local Source Ledger, including critical claim statuses and addendum
5. Interface notes for Manager acceptance
6. Web-source confirmation

--- INPUTS FOR THIS RUN ---
Cleaned skeleton/packet:
Standalone theorem packet only. It contains the target statement and definitions: spectral radius of adjacency matrix, induced edge count e(G[S]), and d_p(G)=max_{nonempty S subset V(G)} e(G[S])/|S|^p. No prior lemmas or proof content.

Target theorem:
Let lambda(G) denote the spectral radius (the largest eigenvalue of the adjacency matrix) of a graph G. For any 1 < p <= 2 and any n-vertex graph G, define d_p(G)=max_{nonempty S subseteq V(G)} e(G[S])/|S|^p, where e(G[S]) is the number of edges in the subgraph induced by S. Then there exists a constant C_p > 0 depending only on p such that every n-vertex graph G with at least one edge satisfies lambda(G) <= (C_p+o(1)) d_p(G) n^{max{1/2, p-1}} as n -> infinity.

Additional mathematical guidance:
None

Manager routing plan summary:
SS1 is Main Solver, work_scope global_solution, assigned SC1-SC7: Rayleigh reduction, induced-density subset/cut estimates, level or threshold decomposition, weighted edge contribution, analytic bound with exponent max{1/2,p-1}, endpoints, asymptotic uniformity. SS2 is Defender and runs later. Critical claims: CC001 exponent max{1/2,p-1}; CC002 all cut/rectangle estimates must be explicitly derived from induced-density, no unsupported sharper cut; CC003 constants/o(1) uniform in G; CC004 p=2 endpoint; CC005 e(G)>=1 gives d_p(G)>0. Assistance Manager admitted SS3 and proposed CC006 below.

Your first draft summary:
You proved a nested incidence estimate for B subseteq A: I(B,A)<=K_pD|A||B|^{p-1}, reduced by layer-cake to lambda <= 2K_pD int H(t)F(t)^{p-1}dt, and handled q=p-1 !=1/2 by splitting at tau=n^{-1/2}. For q=1/2 you invoked a weighted Hardy inequality for arbitrary decreasing sequences.

Approved support bundle:
SS3 is ADMITTED. It contains a concrete obstruction to your q=1/2 endpoint step. SS3 proves the claimed general monotone-sequence estimate is false: for n=2^r, c=r^{-1/2}, b=n^{-1/2}, x_i=b+c sum_{j=0}^{r-1}2^{-j/2} 1_{i<=2^j}, after normalization, sum_k sqrt(k)T_k(x_k-x_{k+1}) and equivalently 2 int H(t)F(t)^{1/2}dt can be Omega(sqrt(n log n)). Therefore the q=1/2 endpoint cannot be closed using only that general sequence inequality. This does not disprove the graph theorem, but it invalidates your invoked Hardy step.

Proposed new/changed board item from support admission:
```yaml
critical_claim_id: CC006
claim: "The q=1/2 endpoint cannot be justified by the general monotone-sequence inequality sum_k sqrt(k) T_k (x_k-x_{k+1}) <= C sqrt(n) under only x decreasing, x >= 0, and sum x_i^2 = 1; SS3 gives normalized examples with lower bound Omega(sqrt(n log n))."
why_critical: "This invalidates the Main Solver's first endpoint proof at p=3/2."
live_alternatives: ["find extra graph/Perron-vector structure", "use a different analytic decomposition", "accept a log loss, which is insufficient for the target"]
resolution_test: "Give a replacement proof of the p=3/2 endpoint that does not rely on the false general sequence inequality, or mark the proof incomplete."
basis: derived_here
status: OPEN
owner: Main Solver
```

Your task now:
Produce a repaired complete proof of the exact target if possible. You may keep any valid parts of your first draft, but you must not use the false q=1/2 monotone-sequence inequality or its equivalent general integral bound. If you cannot repair, output an unsolved YAML with exactly one autonomy-safe guidance item or branch lemma target.