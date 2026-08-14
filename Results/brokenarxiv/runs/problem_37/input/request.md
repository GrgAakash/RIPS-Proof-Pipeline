Problem 37:
Let $H$ be a graph. A graph $G$ is $H$-saturated if $G$ is $H$-free, but adding any edge between two non-adjacent vertices of $G$ yields an $H$-copy as a subgraph. The saturation number $\mathrm{sat}(n, H)$ is the minimum number of edges in an $H$-saturated graph on $n$ vertices. Let $K_m^-$ denote the graph obtained by deleting one edge from the complete graph $K_m$, and let $K_1 \vee F$ denote the join of a single vertex and a graph $F$. For any integer $p \ge 4$ and $F = K_{p-1}^- \cup K_1$, we have the equality $\mathrm{sat}(n, K_1 \vee F) = n - 1 + \mathrm{sat}(n - 1, F)$ for sufficiently large $n$.


Run a fresh no-history solver-only S0-S6 pipeline on this problem:
Prove the statement.

Use the S0-S6 solver prompts from:
  pipeline_sources/Prompt Packet/Prompts.md

Use only these solver roles:
- S0 Blueprint Solver
- S1-S5 Subproblem Solvers
- S6 Composer Solver

Do not use the Main/Manager roles:
- no Manager Routing
- no Main Solver
- no Manager Assistance Routing
- no Manager Support Admission
- no Defender
- no Manager Acceptance

Do not run a verifier pipeline.

Fresh no-history restrictions:
- Do not use memory, prior task history, previous outputs, answer keys, or files outside the fresh input bundle.
- Do not read the private memory directory.
- Spawn every subagent with fork_turns="none" / fork_context=false.
- Do not use web search or internet.
- Do not use API keys.

Tool and execution restrictions:
- No code execution of any kind for solving.
- Do not use Python, Ruby, Perl, Node/JavaScript, shell scripts, compiled programs, notebooks, CAS tools, awk/sed-based computation, simulations, parsers, or helper programs.
- Do not use terminal commands for mathematical work.
- Permitted tooling only:
  1. read the specified prompt packet file;
  2. spawn fresh no-history S0-S6 subagents with fork_context=false;
  3. collect their outputs.
- File reads are permitted only for the specified prompt packet and any directly necessary prompt-packet metadata needed to locate it.

solver-only S0-S6 defaults:
- max_guidance_rounds = 3
- max_branch_depth = 2
- run S0 once per round
- run S1-S5 fresh from S0 assignments
- run S6 fresh from S0 blueprint + S1-S5 outputs
