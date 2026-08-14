Problem 36:
Consider the siblings variant of the coupon collector's problem: coupons are drawn independently from a set of $N$ types according to a probability vector $\mathbf{p} = (p_1, \ldots, p_N)$. A main collector (collector 1) retains the first coupon of each type and passes all subsequent duplicate coupons to collector 2, who similarly retains the first coupon of each type they receive and passes duplicates to collector 3, and so forth. The drawing process stops as soon as collector 1 has collected all $N$ types. Let $U_j^N(\mathbf{p})$ denote the number of missing coupon types for collector $j$ at this stopping time. For integers $N \ge 2$ and $j \ge 2$, the expected deficit $\mathbb{E}[U_j^N(\mathbf{p})]$ is a Schur-concave function of $\mathbf{p}$ on the probability simplex, which establishes that it achieves its maximum at the uniform distribution $\mathbf{p} = (1/N, \ldots, 1/N)$.


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
