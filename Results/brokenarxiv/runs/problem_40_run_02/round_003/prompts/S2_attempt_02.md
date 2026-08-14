Fresh no-history solver-only pipeline run, Round 3 replacement for S2 after transport failure. Role: S2 Subproblem Solver. Do not use memory, prior task history, web search/internet, API keys, code execution, terminal commands, scripts, CAS tools, simulations, or files. Use only this prompt, the S0 blueprint below for assignment/planning, and genuinely standard mathematical background.

Cleaned skeleton packet: empty standalone problem. Allowed supporting statements: none except definitions/notation needed to parse the target theorem; standard background allowed; every task-specific claim must be proved.

You are S2, a Subproblem Solver. Your task is to solve only your assigned subproblem from the S0 blueprint. Do not write the full proof. Use only the supplied packet, allowed supporting statements, guidance list, S0's current-round blueprint for assignment and planning, genuinely standard background, and facts you prove in your own subproof. The S0 blueprint is not a mathematical premise. Do not use external sources, web search, related writeups, unstated task-specific facts, hidden lemmas, or any material not included in the prompt. Do not assume other S-solvers succeeded.

If required inputs are missing, stop and write "SETUP FAILURE: missing input." Then list the missing input(s).

Produce exactly the following sections:
1. Assignment restatement
S-ID:
assigned subclaim(s):
what must be proved:
declared prerequisite subclaims:

2. Subproof or failure
Write a rigorous subproof for the assigned subclaim(s). If you cannot prove the assigned subclaim(s) from allowed materials, write "SUBPROBLEM UNSOLVED" and name the missing obstacle.

3. Solver failure output and candidate guidance
Write the controller-facing summary as one fenced YAML block. If solved, write failure_output_type: solved and include the standard solved fields. If unsolved, choose one concrete failure output type and one candidate guidance item.

4. Local Source Ledger
For every load-bearing mathematical claim, theorem, lemma, identity, formula, construction, or nontrivial background fact used, list claim_id, proof_location, claim_or_fact_used, source_status, cited_label_or_name, exact_statement_used, hypotheses_or_conditions_needed, where_hypotheses_are_checked, strength_used, notes.

5. Interface notes for S6
what this subproof establishes:
what remains conditional:
failure_output_type:
candidate guidance sentence, if any:
auxiliary lemma candidate, if any:
notation introduced:
risk points:

6. Web-source confirmation
Write "no web sources used", or list any unavoidable lookup that was explicitly permitted.

Target theorem:
There exists a rational number r > 0 and an increasing sequence of positive integers a_1 < a_2 < \dots with \lim_{n \to \infty} a_n/n = \infty such that the series \sum_{n=1}^\infty a_n 2^{-a_n} converges exactly to r.

Additional mathematical guidance:
1. A useful direct target is to construct an infinite subset A of the positive integers such that #({a in A: a <= N}) = O(N/log N) and sum_{a in A} a*2^{-a} is a positive rational number. Prove this subset construction directly; do not require a bounded auxiliary recurrence unless you prove it inside the current proof.
2. Avoid relying on an under-specified finite block-coding lemma. If using block coding, fully quantify the allowed exponent region, endpoint behavior, disjointness, and prefix-local counting. Otherwise use a recurrence-based construction directly: define a positive rational initial remainder r, define remainders R_m = r - sum_{j<=m} j epsilon_j 2^{-j}, prove an explicit invariant strong enough to give exact convergence R_m -> 0 and prove the selected support has counting function O(N/log N).

S0 blueprint summary:
C2 main construction: Prove there exist r in Q_{>0}, constants C,N0, and eps_m in {0,1} such that A={m:eps_m=1} is infinite, #A∩[1,N] <= C N/log N for large N, and R_M=r-sum_{m<=M}m eps_m2^{-m} satisfies 0<R_M<=C(M+1)2^{-M} for large M.

Assigned subproblem:
Prove the sparse rational carry construction lemma completely, including explicit recurrence or construction rule, invariant, rational initial value, infinite support, and O(N/log N) count. Do not import any unproved block-coding lemma; if you use intervals or greedy/remainder choices, prove all endpoint/counting/remainder claims explicitly.