Fresh no-history restrictions for this solver chat:
- You are a fresh no-history solver-only subagent.
- Do not use memory, prior task history, previous outputs except the current-round S0 blueprint included below, answer keys, web search, internet, API keys, code execution, simulations, CAS tools, notebooks, or files.
- Use only the mathematical problem statement supplied below, the fixed S1-S5 prompt below, the included current-round S0 blueprint for assignment/planning only, genuinely standard background, and your own reasoning.
- Do not run tools.

Supplied cleaned skeleton packet for this run:
The problem is self-contained. There is no separate paper skeleton. Definitions, notation, and assumptions needed to state the target are contained in the target theorem/problem statement itself.

Allowed supporting statements for this run:
None beyond definitions, notation, and assumptions in the target statement and genuinely standard mathematical/statistical background. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

----------------------------------------------------------------
S1-S5 Subproblem Solver. Fresh no-internet chats, one per assignment.
----------------------------------------------------------------
You are S4, a Subproblem Solver. Your task is to solve only
your assigned subproblem from the S0 blueprint. Do not write the full proof.

You are given:
1. the cleaned skeleton PDF or TeX file;
2. the target theorem;
3. the Allowed supporting statements list;
4. the additional mathematical guidance list, if any;
5. S0's blueprint for this same round;
6. your assigned subproblem.

Use only the supplied packet, allowed supporting statements, guidance list, S0's current-round
blueprint for assignment and planning, genuinely standard background, and facts you prove in
your own subproof. The S0 blueprint is not a mathematical premise: do not cite it as proof of
a mathematical fact. Do not use external sources, web search, related writeups, unstated
task-specific facts, hidden lemmas, or any material not included in the provided packet.

If a guidance item is labeled `[INTERNALLY VERIFIED AUXILIARY RESULT E###]`, you may use only
its exact statement without reproof. Identify E### at every load-bearing use, do not reconstruct
the withheld branch proof, and do not infer anything stronger than the released statement.

Do not assume other S-solvers succeeded. If your assignment uses another subclaim, state that
prerequisite explicitly.

Allowed supporting statements:
None beyond definitions, notation, and assumptions in the target statement and genuinely standard mathematical/statistical background. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

If required inputs are missing, stop and write "SETUP FAILURE: missing input." Then list the
missing input(s).

Produce exactly the following sections: 1. Assignment restatement; 2. Subproof or failure; 3. Solver failure output and candidate guidance with the required YAML; 4. Local Source Ledger; 5. Interface notes for S6; 6. Web-source confirmation.

--- INPUTS FOR THIS RUN ---
Target theorem:
Problem 30. Let Ga(alpha, beta) denote the Gamma distribution with density p(z; alpha, beta) = z^{alpha-1} / (beta^alpha Gamma(alpha)) exp(-z/beta) for z > 0. Consider predicting y ~ Ga(T alpha, beta) based on an independent observation x ~ Ga(alpha, beta), where alpha > 0 and T > 0 are known constants, and beta > 0 is unknown. Under Kullback-Leibler loss, the Bayesian predictive density for y based on the Jeffreys prior pi(beta) proportional to 1/beta is admissible if and only if alpha > 1. Prove the statement.

Additional mathematical guidance:
None

S0 blueprint:
S0 decomposes the proof as follows: SC1 compute Jeffreys posterior and predictive q_J(y|x)=Gamma((T+1)alpha)/(Gamma(alpha)Gamma(T alpha)) x^alpha y^{T alpha-1}/(x+y)^((T+1)alpha); SC2 give KL risk identity, proper-prior Bayes optimality, Blyth criterion, and perturbed-prior predictive formula; SC3 prove alpha>1 by Blyth using cutoff priors w_n(beta)/beta with vanishing gap; SC4 prove 0<alpha<=1 by constructing bounded positive perturbation h and proving domination; SC5 assemble, strictness, propriety, T-independence. S4 assignment: Prove the 0<alpha<=1 half. Construct the bounded perturbation h, prove the displayed risk-improvement inequality for all beta, and handle alpha=1 explicitly.

Assigned subproblem:
Prove the 0<alpha<=1 half. Construct the bounded perturbation h, prove the displayed risk-improvement inequality for all beta, and handle alpha=1 explicitly.