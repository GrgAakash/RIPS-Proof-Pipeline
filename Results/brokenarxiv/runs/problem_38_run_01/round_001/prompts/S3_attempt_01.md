Fresh no-history solver-only pipeline run. Role: S3 Subproblem Solver. Do not use memory, prior task history, web search, internet, API keys, code execution, terminal commands, scripts, CAS, simulations, or file reads. Use only the text in this prompt.

Cleaned skeleton packet: proof-free target statement only; no supporting lemmas.

Target theorem / problem statement:
Let \(\mathcal{P}\) be a convex planar polygon with \(2n\) vertices \(P_1, \dots, P_{2n}\) (where indices are taken modulo \(2n\)) such that the edges \(e_i = P_{i+1} - P_i\) satisfy \(e_i \parallel e_{i+n}\) and \(\langle e_i, e_{i+1} \rangle > 0\) for all \(i\). Let \(L(\mathcal{P})\) be its perimeter, \(A(\mathcal{P})\) be the area enclosed by \(\mathcal{P}\), and \(A^\ast(\mathrm{E}_{0.5}(\mathcal P))\) denote the oriented area of the Wigner caustic of \(\mathcal{P}\), which is the polygon with vertices \(W_i = \frac{P_i + P_{i+n}}{2}\) and oriented area \(A^\ast(\mathrm{E}_{0.5}(\mathcal P)) = \frac{1}{2} \sum_{i=1}^{2n} \det(W_i, W_{i+1})\). Then
\[
L(\mathcal{P})^2\geqslant 8n\tan\left(\frac{\pi}{2n}\right)\cdot\bigl( A(\mathcal P)+2\left|A^\ast\left(\mathrm{E}_{0.5}(\mathcal P)\right)\right|\bigr),
\]
and equality holds if and only if \(\mathcal{P}\) is a regular \(2n\)-gon.

Allowed supporting statements: Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. No additional formal supporting statements are provided.
Additional mathematical guidance: None.

S0 blueprint summary:
SC1: normalize opposite parallel edges.
SC2: Wigner edge formula and Wigner area edge expansion.
SC3: The two quantities \(A+2A^\ast\) and \(A-2A^\ast\) admit nonnegative quadratic-form representations in paired variables and handle the absolute value.
SC4: sharp estimate.
SC5/SC6: equality.
Assignment table:
S3: Derive exact formulas for \(A(\mathcal P)\pm2A^\ast(\mathrm E_{0.5}(\mathcal P))\) using paired symmetric and antisymmetric edge variables. Make the absolute value reduction precise.

----------------------------------------------------------------
S1-S5 Subproblem Solver. Fresh no-internet chats, one per assignment.
----------------------------------------------------------------
You are S3, a Subproblem Solver. Your task is to solve only your assigned subproblem from the S0 blueprint. Do not write the full proof.

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
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. No additional formal supporting statements are provided. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

If required inputs are missing, stop and write "SETUP FAILURE: missing input." Then list the
missing input(s).

Produce exactly the following sections.

1. Assignment restatement

S-ID:
assigned subclaim(s):
what must be proved:
declared prerequisite subclaims:

2. Subproof or failure

Write a rigorous subproof for the assigned subclaim(s). If you cannot prove the assigned
subclaim(s) from allowed materials, write "SUBPROBLEM UNSOLVED" and name the missing obstacle.

3. Solver failure output and candidate guidance

Write the controller-facing summary as one fenced YAML block. Use the exact solved YAML if solved; otherwise choose one allowed failure output type and provide one concrete candidate item if possible.

4. Local Source Ledger

For every load-bearing mathematical claim, theorem, lemma, identity, formula, construction, or
nontrivial background fact used, list claim_id, proof_location, claim_or_fact_used, source_status,
cited_label_or_name, exact_statement_used, hypotheses_or_conditions_needed,
where_hypotheses_are_checked, strength_used, notes.

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

--- INPUTS FOR THIS RUN ---
Target theorem:
[as stated above]

Additional mathematical guidance:
None

S0 blueprint:
[as stated above]

Assigned subproblem:
Derive exact formulas for \(A(\mathcal P)\pm2A^\ast(\mathrm E_{0.5}(\mathcal P))\) using paired symmetric and antisymmetric edge variables. Make the absolute value reduction precise.