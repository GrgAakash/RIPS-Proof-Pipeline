Fresh no-history solver-only branch experiment. Do not use memory, prior task history, previous outputs outside this prompt, answer keys, files outside this prompt, web search/internet, API keys, or Python. This is a no-internet Manager Routing run for an auxiliary branch lemma. Use the latest Manager Routing solver prompt from `pipeline_sources/Prompt Packet/Prompts.md`, in the required section structure. Controller limits: branch depth 1 of max 2; max guidance rounds=3; max_support_items_total remaining=2; no verifier pipeline.

You are the Manager in the routing phase. Create an executable routing plan for the normalized target problem. Do not write the final solution. Select exactly one active worker as Main Solver and exactly one separate Defender. Do not launch Midfielders or Attackers yet. Work in two passes: semantic reading/math mechanism first, then Critical Claims Ledger. Use only the supplied packet, allowed definitions, standard background, and facts proved inside the current solution. No external sources/web.

Allowed supporting statements:
Definitions, notation, and assumptions needed to state or parse the target lemma are allowed. No formal theorem, lemma, proposition, corollary, or paper-skeleton statement is supplied or allowed without reproof.

Produce exactly sections 1,2,3,4,5,6,7,8,9,10 as in the Manager Routing prompt: Target normalization; Task-adaptive proof obligations; Available tools; Subclaim support graph; Critical Claims Ledger; Key-step and Main Solver selection; Failure-mode checks; Subsolver execution plan; Subsolver assignment table; Web-source confirmation.

--- INPUTS FOR THIS BRANCH RUN ---
Cleaned skeleton/packet:
Standalone auxiliary lemma packet only. It contains the target lemma statement below and the definitions appearing in it: spectral radius of the adjacency matrix, induced edge count e(H[S]), and d_{3/2}(H)=max_{nonempty S subset V(H)} e(H[S])/|S|^{3/2}. No prior theorem statements, no proof content, no answer key.

Target lemma:
There is an absolute constant C>0 such that every N-vertex graph H with at least one edge satisfies
lambda(H) <= C sqrt(N) d_{3/2}(H),
where lambda(H) is the adjacency spectral radius and d_{3/2}(H)=max_{nonempty S subseteq V(H)} e(H[S]) / |S|^{3/2}.

Parent intended use note:
If this lemma is established, the main theorem follows by comparing d_{3/2}(G) to d_p(G): for p<=3/2 and any S with at least one edge, |S|^{p-3/2}<=2^{p-3/2}; for p>=3/2, |S|^{p-3/2}<=n^{p-3/2}. This note is only motivation; the branch target is exactly the spectral sweep lemma above.

Additional mathematical guidance:
None