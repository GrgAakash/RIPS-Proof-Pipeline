Fresh no-history solver-only pipeline run. Role: S1 Subproblem Solver. Do not use memory, prior task history, web search, internet, API keys, code execution, terminal commands, scripts, CAS, simulations, or file reads. Use only the text in this prompt.

Cleaned skeleton packet for this run: proof-free statement only; no supporting lemmas, no source grants, no proof sketches.

Target theorem / problem statement:
Let \(\mathcal{P}\) be a convex planar polygon with \(2n\) vertices \(P_1, \dots, P_{2n}\) (where indices are taken modulo \(2n\)) such that the edges \(e_i = P_{i+1} - P_i\) satisfy \(e_i \parallel e_{i+n}\) and \(\langle e_i, e_{i+1} \rangle > 0\) for all \(i\). Let \(L(\mathcal{P})\) be its perimeter, \(A(\mathcal{P})\) be the area enclosed by \(\mathcal{P}\), and \(A^\ast(\mathrm{E}_{0.5}(\mathcal P))\) denote the oriented area of the Wigner caustic of \(\mathcal{P}\), which is the polygon with vertices \(W_i = \frac{P_i + P_{i+n}}{2}\) and oriented area \(A^\ast(\mathrm{E}_{0.5}(\mathcal P)) = \frac{1}{2} \sum_{i=1}^{2n} \det(W_i, W_{i+1})\). Then
\[
L(\mathcal{P})^2\geqslant 8n\tan\left(\frac{\pi}{2n}\right)\cdot\bigl( A(\mathcal P)+2\left|A^\ast\left(\mathrm{E}_{0.5}(\mathcal P)\right)\right|\bigr),
\]
and equality holds if and only if \(\mathcal{P}\) is a regular \(2n\)-gon.

Allowed supporting statements for this run: Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. No additional formal supporting statements are provided. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

Additional mathematical guidance: None.

S0 blueprint:
1. Target decomposition

target_label: Polygonal Wigner-caustic isoperimetric inequality

target_type: sharp geometric inequality with equality classification

main_goal: prove the stated lower bound for \(L(\mathcal P)^2\) in terms of \(A(\mathcal P)+2|A^\ast(\mathrm E_{0.5}(\mathcal P))|\), and characterize equality.

variables_and_parameters: integer \(n\), convex \(2n\)-gon \(\mathcal P=(P_1,\dots,P_{2n})\), edge vectors \(e_i=P_{i+1}-P_i\), Wigner vertices \(W_i=(P_i+P_{i+n})/2\), perimeter \(L(\mathcal P)\), area \(A(\mathcal P)\), oriented Wigner-caustic area \(A^\ast(\mathrm E_{0.5}(\mathcal P))\).

conclusion_to_prove:
\[
L(\mathcal{P})^2\geq 8n\tan\left(\frac{\pi}{2n}\right)
\left(A(\mathcal P)+2\left|A^\ast(\mathrm E_{0.5}(\mathcal P))\right|\right),
\]
with equality if and only if \(\mathcal P\) is a regular \(2n\)-gon.

2. Available tools

[omitted here only for brevity in this assignment packet: use no mathematical premise from the omission; the full subclaim assignment below is authoritative]

3. Subclaim support graph
SC1: Under the hypotheses, after orienting \(\mathcal P\) counterclockwise, opposite edges satisfy \(e_{i+n}=-\lambda_i e_i\) with \(\lambda_i>0\), and the edge directions have turning angles \(\theta_i\in(0,\pi/2)\) summing to \(2\pi\). Suggested solver S1.
SC2: The Wigner caustic edge vectors are \(\frac12(e_i+e_{i+n})\), and its oriented area can be expressed as a quadratic form in the paired edge data. Suggested solver S2.
SC3: The two quantities \(A+2A^\ast\) and \(A-2A^\ast\) admit nonnegative quadratic-form representations in paired variables and handle the absolute value. Suggested solver S3.
SC4: For each quadratic form, prove the sharp estimate with constant \(8n\tan(\pi/(2n))\). Suggested solver S4.
SC5/SC6: equality tracking and regular converse. Suggested solver S5.

4. Hardest step prediction: SC4, the sharp algebraic/trigonometric inequality.

6. Subproblem assignment table
S1: Prove the geometric normalization: orient the polygon, show \(e_{i+n}=-\lambda_i e_i\) with \(\lambda_i>0\), introduce edge lengths and turning angles, and verify \(\theta_i\in(0,\pi/2)\), \(\sum\theta_i=2\pi\).
S2: Starting only from \(W_i=(P_i+P_{i+n})/2\), derive the Wigner edge formula and expand \(A^\ast(\mathrm E_{0.5}(\mathcal P))\) in edge variables.
S3: Derive exact formulas for \(A(\mathcal P)\pm2A^\ast(\mathrm E_{0.5}(\mathcal P))\) using paired symmetric and antisymmetric edge variables. Make the absolute value reduction precise.
S4: Prove the sharp quadratic inequality controlling the area expressions by \(L(\mathcal P)^2\), with constant \(8n\tan(\pi/(2n))\). This must be an internal proof from elementary algebra, convexity, and trigonometry.
S5: Track equality cases through S1-S4. Prove equality forces equal angles and equal side lengths, hence regularity, and verify directly that the regular \(2n\)-gon attains equality.

----------------------------------------------------------------
S1-S5 Subproblem Solver. Fresh no-internet chats, one per assignment.
----------------------------------------------------------------
You are S1, a Subproblem Solver. Your task is to solve only your assigned subproblem from the S0 blueprint. Do not write the full proof.

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

Write the controller-facing summary as one fenced YAML block. Do not put prose before this
YAML block inside section 3. The key `failure_output_type` must contain exactly one allowed
top-level value; put subtypes such as `unresolved key lemma` under `type`.

If the assigned subclaim is solved, write exactly:

```yaml
failure_output_type: solved
type: ""
failed_route: ""
obstruction: ""
evidence: ""
reuse_value: ""
guidance_sentence: null
candidate_lemma_statement: null
why_unblocks: null
where_used: null
allowed_inputs: null
dependencies: null
weaker_than_target: null
equivalent_or_stronger: null
recommended: null
```

If the assigned subclaim is not solved, choose exactly one failure output type:

- forbidden-route / obstruction guidance;
- branch lemma target;
- ordinary hint request;
- no useful guidance item found.

Use this priority order:

1. forbidden-route / obstruction guidance;
2. branch lemma target;
3. ordinary hint request;
4. no useful guidance item found.

Do not output more than one candidate guidance item. Do not give vague advice such as "try a
different method", "use more structure", or "this is hard." If you cannot identify a concrete
reusable obstruction, clean branch lemma, or specific missing idea, choose "no useful guidance
item found."

For any unsolved output, fill the same YAML keys:

```yaml
failure_output_type: forbidden-route / obstruction guidance | branch lemma target | ordinary hint request | no useful guidance item found
type: counterexample / missing hypothesis / false strengthening / circular dependency / unresolved key lemma / source failure / ordinary hint request / other precise obstruction / no useful guidance item found
failed_route: ""
obstruction: ""
evidence: ""
reuse_value: ""
guidance_sentence: null
candidate_lemma_statement: null
why_unblocks: null
where_used: null
allowed_inputs: null
dependencies: null
weaker_than_target: null
equivalent_or_stronger: null
recommended: null
```

Use "forbidden-route / obstruction guidance" when you found a concrete reason a route failed,
such as a counterexample, false stronger theorem, circular dependency, or missing required
hypothesis. The guidance sentence should help the next run avoid repeating that failed route.

Use "branch lemma target" when the proof reduces to one clean standalone statement that may be
true or false and could be run as a separate S0-S6 mini-pipeline. For this type, fill the YAML
keys `candidate_lemma_statement`, `why_unblocks`, `where_used`, `allowed_inputs`,
`dependencies`, `weaker_than_target`, `equivalent_or_stronger`, and `recommended`.

The candidate lemma should be a standalone mathematical statement that could be pasted as the
target theorem for a separate S0-S6 mini-pipeline. Do not include the current failed proof as
context for that mini-pipeline. Include only the candidate lemma statement, allowed inputs, and
the minimal parent note explaining why the main pipeline needs it. If no clean standalone lemma
can be stated, say so.

Use "ordinary hint request" only when no route has been disproved and no clean branch lemma is
available, but you can name a specific missing tool, theorem, estimate, construction, or search
direction. The evidence field must explain exactly where that missing idea would enter the
proof.

Use "no useful guidance item found" when the subproblem remains unsolved but you cannot give a
specific, evidence-backed item that would help a later run.

4. Local Source Ledger

For every load-bearing mathematical claim, theorem, lemma, identity, formula, construction, or
nontrivial background fact used:
claim_id:
proof_location:
claim_or_fact_used:
source_status: provided definition / notation / assumption; allowed supporting statement;
additional guidance item; standard background fact; proved inside the current proof; or
unsupported or unclear.
cited_label_or_name:
exact_statement_used:
hypotheses_or_conditions_needed:
where_hypotheses_are_checked:
strength_used:
notes:

Do not cite vague sources such as "well-known", "standard", "classical", or "by the
literature" unless you name the exact fact and state the version used. If you use a standard
background fact, name the fact, state the version used, and explain why it applies. If you
prove a claim inside the current subproof, mark the source status as "proved inside the current
proof" and point to the proof location. If a nontrivial fact is not in the provided packet, not
in the allowed supporting statements, not in the guidance list, not genuinely standard
background, and not proved inside the current subproof, mark it "unsupported or unclear."

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
Prove the geometric normalization: orient the polygon, show \(e_{i+n}=-\lambda_i e_i\) with \(\lambda_i>0\), introduce edge lengths and turning angles, and verify \(\theta_i\in(0,\pi/2)\), \(\sum\theta_i=2\pi\).