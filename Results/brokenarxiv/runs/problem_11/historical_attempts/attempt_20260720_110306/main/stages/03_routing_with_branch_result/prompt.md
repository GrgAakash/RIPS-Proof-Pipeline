Fresh no-history solver-only main experiment. Do not use memory, prior task history, previous outputs outside this prompt, answer keys, files outside this prompt, web search/internet, API keys, or Python. This is a no-internet Manager Routing run for the main theorem after one internally verified auxiliary result has been released as guidance. Use the latest Manager Routing prompt from `pipeline_sources/Prompt Packet/Prompts.md` in the required section structure. No verifier pipeline.

Allowed supporting statements:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. No formal theorem, lemma, proposition, corollary, or paper-skeleton statement is supplied or allowed without reproof, except the exact internally verified auxiliary result E001 below.

If a guidance item is labeled `[INTERNALLY VERIFIED AUXILIARY RESULT E###]`, treat exactly its stated lemma as established and available without reproof. Record E### as an additional-guidance tool wherever it is used. Do not reconstruct its hidden branch proof or infer a stronger claim.

Produce exactly sections 1-10 as in Manager Routing: Target normalization; Task-adaptive proof obligations; Available tools; Subclaim support graph; Critical Claims Ledger; Key-step and Main Solver selection; Failure-mode checks; Subsolver execution plan; Subsolver assignment table; Web-source confirmation. Select exactly SS1 Main Solver and SS2 Defender, no specialists initially.

--- INPUTS FOR THIS RUN ---
Cleaned skeleton/packet:
Standalone theorem packet only. It contains the target statement and definitions: spectral radius of adjacency matrix, induced edge count e(G[S]), and d_p(G)=max_{nonempty S subset V(G)} e(G[S])/|S|^p. No prior theorem statements, no proof content, no answer key.

Target theorem:
Let lambda(G) denote the spectral radius (the largest eigenvalue of the adjacency matrix) of a graph G. For any 1 < p <= 2 and any n-vertex graph G, define d_p(G)=max_{nonempty S subseteq V(G)} e(G[S])/|S|^p, where e(G[S]) is the number of edges in the subgraph induced by S. Then there exists a constant C_p > 0 depending only on p such that every n-vertex graph G with at least one edge satisfies lambda(G) <= (C_p+o(1)) d_p(G) n^{max{1/2, p-1}} as n -> infinity.

Additional mathematical guidance:
[INTERNALLY VERIFIED AUXILIARY RESULT E001] Lemma statement: There is an absolute constant C0>0 such that every N-vertex graph H with at least one edge satisfies lambda(H) <= C0 sqrt(N) d_{3/2}(H), where d_{3/2}(H)=max_{nonempty S subseteq V(H)} e(H[S])/|S|^{3/2}. Independently verified status: ESTABLISHED by branch Manager acceptance. Permission: use this exact statement without reproof. Intended use location: reduce the main theorem to comparing d_{3/2}(G) with d_p(G).