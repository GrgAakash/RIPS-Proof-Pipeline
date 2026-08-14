Problem 18:
Let $(X,\mathcal{E})$ be a uniformly locally finite coarse space. For every $p \in \{0\} \cup [1, \infty]$, let $B^p_u(X,\mathcal{E})$ denote the $\ell^p$ uniform Roe algebra, which is the norm completion of the algebra $\mathbb{C}_u[X, \mathcal{E}]$ of controlled propagation operators on $\ell^p(X)$. A closed, two-sided ideal $I$ of $B^p_u(X,\mathcal{E})$ is called a geometric ideal if $I \cap \mathbb{C}_u[X, \mathcal{E}]$ is dense in $I$. For $p, q \in (1, \infty)$, the lattice of geometric ideals in $B^p_u(X,\mathcal{E})$ is isomorphic to the lattice of geometric ideals in $B^q_u(X,\mathcal{E})$ if and only if $p = q$ or $\frac{1}{p} + \frac{1}{q} = 1$.

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
