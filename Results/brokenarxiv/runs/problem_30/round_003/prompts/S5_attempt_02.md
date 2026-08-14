Fresh no-history restrictions:
- Fresh no-history S5 solver rerun after setup failure. Do not use memory, prior task history, previous outputs, answer keys, web/internet/API keys, code execution, CAS, simulations, notebooks, tools, or files.
- Use only the full target theorem below, allowed support, guidance, current-round S0 blueprint summary, standard background, and your own reasoning.

Allowed support: Definitions, notation, and assumptions in the target theorem and genuinely standard mathematical/statistical background only. No statement equivalent to, stronger than, or downstream from the target theorem is allowed.

Fixed S1-S5 role: You are S5, a Subproblem Solver. Solve only assigned subproblem. Do not write full proof. S0 blueprint is not a mathematical premise. If missing input, report SETUP FAILURE. Produce sections: 1 Assignment restatement; 2 Subproof or failure; 3 YAML failure output; 4 Local Source Ledger; 5 Interface notes for S6; 6 Web-source confirmation.

Full target theorem:
Let Ga(alpha, beta) denote the Gamma distribution with density p(z; alpha, beta)=z^{alpha-1}/(beta^alpha Gamma(alpha)) exp(-z/beta) for z>0, using beta as a scale parameter. Consider predicting y~Ga(T alpha,beta) based on an independent observation x~Ga(alpha,beta), where alpha>0 and T>0 are known constants, and beta>0 is unknown. Under Kullback-Leibler loss, the Bayesian predictive density for y based on the Jeffreys prior pi(beta) proportional to 1/beta is admissible if and only if alpha>1. Prove the statement.

Additional guidance:
1. Do not rely on an unprovided “displayed risk-improvement inequality” for the 0<alpha<=1 half. The proof must either state and prove from the gamma model a self-contained perturbation/complete-class criterion yielding a valid dominating predictive density, including the exact perturbation and normalization, or else report the precise standalone lemma needed; S4/S6 must not treat the inadmissibility half as solved without this load-bearing proof.
2. The remaining load-bearing lemma to prove is: For fixed T>0 and 0<alpha<=1, with k=(T+1)alpha, there exist bounded measurable h:(0,infty)->[-1,1] and epsilon in (0,1) such that A_r^h(z)=z^r/Gamma(r) int_0^infty u^(r-1) exp(-zu) h(u) du and q_{epsilon,h}(y|x)=q_J(y|x)[1+epsilon A_k^h(x+y)]/[1+epsilon A_alpha^h(x)] is normalized and E_lambda log([1+epsilon A_k^h(X+Y)]/[1+epsilon A_alpha^h(X)]) >=0 for every lambda>0, with strict inequality for at least one lambda. The proof must either establish this lemma directly from the gamma model, including exact h and epsilon or a fully proved existence argument, or prove a self-contained complete-class theorem strong enough to imply inadmissibility for 0<alpha<=1, including alpha=1 explicitly.

Current-round S0 blueprint summary:
S1 compute q_J; S2 prove perturbation normalization; S3 derive perturbation KL risk difference; S4 prove perturbation existence for 0<alpha<=1; S5 prove alpha>1 admissibility via predictive-KL Blyth, and state how final S6 should assemble with S4 if S4 solves inadmissibility. Hardest: S4; second hardest: gamma boundary estimates for Blyth alpha>1.

Assigned subproblem:
Prove the alpha>1 admissibility half via a predictive-KL Blyth criterion and gamma boundary estimates; also state how final S6 should assemble with S4 if S4 solves the inadmissibility lemma. If S4 is not available, do not assert the full iff theorem.