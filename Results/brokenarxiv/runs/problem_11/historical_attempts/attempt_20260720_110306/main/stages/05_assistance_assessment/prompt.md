Fresh no-history solver-only main experiment. Do not use memory, prior task history, previous outputs outside this prompt, answer keys, files outside this prompt, web search/internet, API keys, or Python. This is a no-internet Manager Assistance Routing run after Main Solver draft. Use latest Manager Assistance Routing prompt structure. Decide whether bounded assistance is justified; do not solve math yourself. Add support only for concrete bottleneck; otherwise keep SS1 and SS2.

Produce exactly sections: 1 Post-Main Solver assessment; 5 Critical Claims Ledger; 8 Subsolver execution plan; 9 Subsolver assignment table; 10 Web-source confirmation.

--- INPUTS ---
Target theorem:
For any 1<p<=2, every n-vertex graph G with at least one edge satisfies lambda(G) <= (C_p+o(1)) d_p(G) n^{max{1/2,p-1}}.

Additional mathematical guidance:
[INTERNALLY VERIFIED AUXILIARY RESULT E001] There is an absolute C0>0 such that every N-vertex graph H with at least one edge satisfies lambda(H)<=C0 sqrt(N)d_{3/2}(H). Use exact statement without reproof.

Initial Manager routing plan:
SS1 Main Solver applies E001 to G, proves d_{3/2}(G)<=d_p(G)n^{max(0,p-3/2)} by subset-size comparison, then exponent identity. SS2 Defender runs last. Critical claims CC001 E001 applicability; CC002 density comparison; CC003 exponent identity.

Main Solver draft:
SS1 proof body:
Let 1<p<=2 and G be n-vertex with at least one edge. By E001 applied to G with N=n, lambda(G)<=C0 sqrt(n)d_{3/2}(G). For every nonempty S, e(G[S])/|S|^{3/2} = (e(G[S])/|S|^p)|S|^{p-3/2} <= d_p(G)|S|^{p-3/2}. If p<=3/2, |S|^{p-3/2}<=1; if p>=3/2, |S|^{p-3/2}<=n^{p-3/2}. Therefore d_{3/2}(G)<=d_p(G)n^{max(0,p-3/2)}. Combine to get lambda(G)<=C0d_p(G)n^{1/2+max(0,p-3/2)}=C0d_p(G)n^{max(1/2,p-1)}. Set C_p=C0; exact bound implies (C_p+o(1)) form. YAML: solved, main_solver_proof_key true. No web/Python/API/prior outputs.