Problem 29:
For $0<q<1$, let the $q$-Pochhammer symbol be defined as $(q;q)*k = \\prod*{j=0}^{k-1} (1 - q^{j+1})$ for $k \ge 1$ with $(q;q)_0 = 1$. Define the normalized $q$-Borel transform $\mathcal{B}*q$ on formal power series by \\[ \\mathcal{B}q\\left(\\sum{k=0}^\\infty a\_k\\frac{z^k}{k!}\\right) =\\sum*{k=0}^\infty a_k\frac{q^{k(k-1)/2}(1-q)^k}{(q;q)_k}z^k . \] Let $\mathcal{L-P}$ denote the classical Laguerre--Pólya class of real entire functions. Then for every $q \in (0,1)$, the transform $\mathcal{B}_q$ restricts to a bijection on $\mathcal{L-P}$, meaning it maps $\mathcal{L-P}$ surjectively onto itself.



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
