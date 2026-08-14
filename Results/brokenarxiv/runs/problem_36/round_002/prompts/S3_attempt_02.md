Fresh no-history solver-only pipeline run. You are fresh S3 for Round 2. Do not use memory, prior task history, previous outputs except the S0 blueprint pasted in this prompt, answer keys, files outside this prompt, web search, internet, API keys, or code execution. Do not call tools. Use only the statement below, the S0 blueprint below, standard background, and reasoning in this chat.

S1-S5 Subproblem Solver. Fresh no-internet chats, one per assignment.
----------------------------------------------------------------
You are S3, a Subproblem Solver. Your task is to solve only
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
Definitions, notation, and assumptions in the target statement are allowed. There are no additional formal supporting statements, no later-but-upstream inclusions, and no exclusions. The cleaned skeleton packet for this standalone problem is exactly the target statement below.

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
Problem 36. Consider the siblings variant of the coupon collector's problem: coupons are drawn independently from a set of N types according to a probability vector p = (p_1, ..., p_N). A main collector (collector 1) retains the first coupon of each type and passes all subsequent duplicate coupons to collector 2, who similarly retains the first coupon of each type they receive and passes duplicates to collector 3, and so forth. The drawing process stops as soon as collector 1 has collected all N types. Let U_j^N(p) denote the number of missing coupon types for collector j at this stopping time. For integers N >= 2 and j >= 2, the expected deficit E[U_j^N(p)] is a Schur-concave function of p on the probability simplex, which establishes that it achieves its maximum at the uniform distribution p = (1/N, ..., 1/N).

Additional mathematical guidance:
1. Do not attempt to prove the Schur derivative inequality or closed-simplex Schur-concavity before resolving this concrete obstruction: for N=3 and j=2, the standard formula route gives at p=(1/2,7/16,1/16) that partial_x F - partial_y F = 1841/36450 > 0 while x-y=1/16>0, so either identify an error in that formula/arithmetic or conclude the Schur-concavity claim cannot be proved as stated.

S0 blueprint:
1. Target decomposition

target_label: Problem 36

target_type: Schur-concavity theorem for an expected coupon-collector deficit

main_goal: Show, for every N >= 2 and j >= 2, that E[U_j^N(p)] is Schur-concave in p.

variables_and_parameters: N >= 2; j >= 2; probability vector p = (p_1, ..., p_N) in the probability simplex; sibling collectors indexed by positive integers; stopping time when collector 1 first has all N types.

conclusion_to_prove: E[U_j^N(p)] is Schur-concave on the probability simplex, hence maximized at p = (1/N, ..., 1/N).

2. Available tools

Definition of siblings coupon collector process; definition of U_j^N(p); Schur derivative criterion: for a differentiable symmetric function F on the simplex interior, Schur-concavity requires (p_a-p_b)(partial_a F-partial_b F)<=0 for every pair; guidance obstruction: for N=3,j=2, at p=(1/2,7/16,1/16), partial_xF-partial_yF=1841/36450>0 and x-y=1/16>0; symmetry of expected deficit; counterexample logic.

3. Subclaim support graph
S0.1: For the target theorem, N=3,j=2 is included. Suggested S1.
S0.2: At p=(1/2,7/16,1/16), x-y=1/16>0. Suggested S2.
S0.3: The supplied obstruction asserts partial_xF-partial_yF=1841/36450>0. Suggested S2.
S0.4: The Schur-concavity derivative condition would require (x-y)(partial_xF-partial_yF)<=0. Suggested S3.
S0.5: The supplied signs give positive product, violating the necessary condition. Suggested S4.
S0.6: Since no corrected formula or arithmetic is supplied in the packet, the available information supports concluding that the Schur-concavity claim cannot be proved as stated. Suggested S5.

4. Hardest step prediction
Hardest step S0.5: deciding whether derivative obstruction is genuine. The final proof should not attempt Schur-concavity until it independently verifies or corrects the N=3,j=2 computation. With only supplied packet, the safe conclusion is that the theorem cannot be proved as stated.

5. Failure-mode checks
Universal theorem includes N=3,j=2; p=(1/2,7/16,1/16) lies in the interior; F denotes p -> E[U_2^3(p)] in the concrete obstruction; standard fact is Schur derivative criterion.

6. Subproblem assignment table
S1: Verify that N=3,j=2 is valid and p=(1/2,7/16,1/16) is interior.
S2: Record x-y=1/16>0 and partial_xF-partial_yF=1841/36450>0.
S3: State the standard Schur-concavity derivative criterion for differentiable symmetric functions on the simplex interior.
S4: Combine S2 and S3 to show the derivative inequality is violated.
S5: Conclude that absent a correction, theorem cannot be proved as stated.

7. Web-source confirmation
no web sources used

Assigned subproblem:
S3: State the standard Schur-concavity derivative criterion for differentiable symmetric functions on the simplex interior.