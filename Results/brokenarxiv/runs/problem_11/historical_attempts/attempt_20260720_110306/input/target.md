Let $\lambda(G)$ denote the spectral radius (the largest eigenvalue of the adjacency matrix) of a graph $G$. For any $1 < p \le 2$ and any $n$-vertex graph $G$, define $d_p(G)=\max_{\varnothing\ne S\subseteq V(G)}\frac{e(G[S])}{|S|^p}$, where $e(G[S])$ is the number of edges in the subgraph induced by $S$. Then there exists a constant $C_p > 0$ depending only on $p$ such that every $n$-vertex graph $G$ with at least one edge satisfies $\lambda(G) \le (C_p+o(1))d_p(G)n^{\max\{1/2, p-1\}}$ as $n \to \infty$.


Run a fresh no-history solver-only Main/Manager pipeline on this problem:
Prove the statement.
Fresh no-history experiment:
Use the latest Main /Manager solver prompt from:
  pipeline_sources/Prompt Packet/Prompts.md
Run only the solver pipeline; do not run a verifier pipeline.
Do not use memory, prior task history, previous outputs, answer keys, or files outside the fresh input bundle.
Do not read the private memory directory.
Spawn every subagent with fork_turns="none" / fork_context=false.
Do not use web search or internet.
Do not use API keys and do not use Python
solver-only default:
max_guidance_rounds = 3
max_support_items_total = 3
max_branch_depth = 2
max_specialist_batches_per_round = 2
max_challenge_resolver_calls_per_round = 2
