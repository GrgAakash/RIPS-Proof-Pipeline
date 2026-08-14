Problem 43:
Let $N \ge 1$ be an integer, $0<s<1$, $p>1$, $0\le\gamma<\min(2s,N,2s(p-1))$, and $u_0\in L^1(\mathbb{R}^N)\cap L^\infty(\mathbb{R}^N)$ be a non-negative function not identically zero. Let $T_\varepsilon \in (0, \infty]$ denote the lifespan of mild solutions to the fractional semilinear parabolic Cauchy problem $u_t + (-\Delta)^s u = |x|^{-\gamma}\,|u|^p$ on $(0,\infty)\times\mathbb{R}^N$ with initial data $u(0,x)=\varepsilon\,u_0(x)$, where $(-\Delta)^s$ is the fractional Laplacian defined by $(-\Delta)^s f(x) = c_{N,s} \text{ P.V.} \int_{\mathbb{R}^N} \frac{f(x) - f(y)}{|x - y|^{N+2s}} dy$ with $c_{N,s} = \frac{2^{2s} \Gamma\left(\frac{N+2s}{2}\right)}{\pi^{N/2} |\Gamma(-s)|}$. Define the critical exponent $p_F = 1+\frac{2s-\gamma}{N}$. Then there exists $\varepsilon_0 > 0$ such that for all $0 < \varepsilon < \varepsilon_0$, $T_\varepsilon < \infty$ if $1<p < p_F$, and $T_\varepsilon = +\infty$ if $p \ge p_F$.


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
