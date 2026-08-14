Problem 38:
Let $\mathcal{P}$ be a convex planar polygon with $2n$ vertices $P_1, \dots, P_{2n}$ (where indices are taken modulo $2n$) such that the edges $e_i = P_{i+1} - P_i$ satisfy $e_i \parallel e_{i+n}$ and $\langle e_i, e_{i+1} \rangle > 0$ for all $i$. Let $L(\mathcal{P})$ be its perimeter, $A(\mathcal{P})$ be the area enclosed by $\mathcal{P}$, and $A^\ast\left(\mathrm{E}*{0.5}(\\mathcal P)\\right)$ denote the oriented area of the Wigner caustic of $\\mathcal{P}$, which is the polygon with vertices $W\_i = \\frac{P\_i + P*{i+n}}{2}$ and oriented area $A^\ast(\mathrm{E}*{0.5}(\\mathcal P)) = \\frac{1}{2} \\sum*{i=1}^{2n} \det(W_i, W_{i+1})$. Then $$L(\mathcal{P})^2\geqslant 8n\tan\left(\frac{\pi}{2n}\right)\cdot\big( A(\mathcal P)+2\left|A^\ast\left(\mathrm{E}_{0.5}(\mathcal P)\right)\right|\big),$$ and equality holds if and only if $\mathcal{P}$ is a regular $2n$-gon.



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
