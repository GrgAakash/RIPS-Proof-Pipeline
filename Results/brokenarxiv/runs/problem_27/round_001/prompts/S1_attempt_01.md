Fresh no-history solver-only S1 run. Do not use memory, prior task history, answer keys, web search, internet, API keys, terminal, code execution, files, or tools. Use only the mathematical input in this prompt and genuinely standard background. If the assigned claim is false or insufficient, say so; do not fabricate a proof.

Cleaned skeleton packet for this run:
The target theorem statement below is the complete mathematical packet. Definitions/notation appearing in the statement are available: Coxeter group W, irreducible Coxeter group, length function ell, Bruhat order and Bruhat interval [u,v], interval length ell(v)-ell(u), isomorphism type of a finite poset interval. No paper skeleton, bibliography, or additional formal supporting statements are supplied.

----------------------------------------------------------------
S1-S5 Subproblem Solver. Fresh no-internet chats, one per assignment.
----------------------------------------------------------------
You are S1, a Subproblem Solver. Your task is to solve only
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
No formal supporting statements are supplied. Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. Genuinely standard background about Coxeter systems, the length function, Bruhat order, reduced expressions, and the subword criterion may be used only if explicitly stated as standard background. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

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
Problem 27: Let W be an irreducible Coxeter group. For each fixed integer k >= 0, only finitely many isomorphism types of Bruhat intervals of length k (where the length of an interval [u,v] is defined as ell(v)-ell(u) with ell being the length function on W) occur in W if and only if W is a finite Coxeter group.

Additional mathematical guidance:
None

S0 blueprint:
1. Target decomposition

target_label:
Problem 27

target_type:
if and only if classification theorem

main_goal:
Show that an irreducible Coxeter group `W` has finitely many Bruhat-interval isomorphism types in every fixed interval length `k >= 0` exactly when `W` is finite.

variables_and_parameters:
`W`: irreducible Coxeter group.  
`ell`: length function.  
`[u,v]`: Bruhat interval with `u <= v`.  
`k >= 0`: fixed integer interval length `ell(v)-ell(u)`.

conclusion_to_prove:
For every fixed `k >= 0`, only finitely many finite-poset isomorphism types of Bruhat intervals `[u,v]` with `ell(v)-ell(u)=k` occur in `W` if and only if `W` is finite.

2. Available tools

tool:
Finite Coxeter group has finitely many intervals.

source_status:
standard background fact

exact_statement_or_fact:
If `W` is finite, then there are only finitely many pairs `(u,v)` with `u <= v`; hence only finitely many Bruhat intervals, and therefore only finitely many isomorphism types in each fixed length.

intended_role_in_proof:
Proves the easy forward implication from finiteness of `W` to the interval-finiteness property.

tool:
Subword criterion for Bruhat order.

source_status:
standard background fact

exact_statement_or_fact:
For a reduced expression of `v`, elements `x <= v` are represented by subwords of that reduced expression, with Bruhat order detected through subword containment after allowing reduced representatives.

intended_role_in_proof:
Used to build and compare intervals inside carefully chosen long words in an infinite Coxeter group.

tool:
Infinite irreducible Coxeter groups contain arbitrarily long reduced words with controlled local Coxeter behavior.

source_status:
standard background fact / must be justified inside current proof

exact_statement_or_fact:
If `W` is infinite and irreducible, then one can find reduced words of arbitrarily large length whose Bruhat subword structure contains arbitrarily large distinguishable finite configurations.

intended_role_in_proof:
This is the key source of infinitely many non-isomorphic fixed-length intervals. It must be made precise in the final proof.

tool:
Ranked-poset invariants distinguish interval isomorphism types.

source_status:
standard background fact

exact_statement_or_fact:
If two finite Bruhat intervals are isomorphic as posets, then they have the same rank sizes, covering graph degrees, numbers of elements in each rank, and comparable-element counts.

intended_role_in_proof:
Provides concrete invariants for proving that the constructed intervals are pairwise non-isomorphic.

tool:
Construction of fixed-length intervals with unbounded internal size/invariant.

source_status:
proved inside the current proof

exact_statement_or_fact:
For some fixed `k`, depending only on the infinite irreducible Coxeter system, there exists an infinite family of intervals `[u_n,v_n]` with `ell(v_n)-ell(u_n)=k` whose poset invariants are pairwise distinct.

intended_role_in_proof:
Proves the contrapositive: if `W` is infinite irreducible, then the stated finite-type property fails.

3. Subclaim support graph

id:
SC1

statement:
If `W` is finite, then for each fixed `k >= 0`, only finitely many Bruhat intervals of length `k` occur, hence only finitely many isomorphism types occur.

uses_prior_subclaims:
none

purpose:
Prove the easy implication.

status:
standard background

suggested_solver:
S1

id:
SC2

statement:
It suffices for the converse to prove the contrapositive: if `W` is infinite and irreducible, then there exists at least one fixed integer `k >= 0` for which infinitely many Bruhat-interval isomorphism types of length `k` occur.

uses_prior_subclaims:
none

purpose:
Clarify the logical structure of the hard direction.

status:
standard background

suggested_solver:
S1

id:
SC3

statement:
In an infinite irreducible Coxeter group, one can construct an infinite sequence of comparable pairs `u_n <= v_n` with a common difference `ell(v_n)-ell(u_n)=k`, where the Bruhat intervals `[u_n,v_n]` contain a numerical poset invariant growing with `n`.

uses_prior_subclaims:
SC2

purpose:
Main constructive step for the infinite case.

status:
must be proved in final proof

suggested_solver:
S2

id:
SC4

statement:
The invariant chosen in SC3 is preserved by finite-poset isomorphism.

uses_prior_subclaims:
SC3

purpose:
Turns the constructed growing invariant into pairwise non-isomorphism.

status:
standard background

suggested_solver:
S3

id:
SC5

statement:
The intervals constructed in SC3 really have the same fixed length `k`.

uses_prior_subclaims:
SC3

purpose:
Prevents the construction from merely producing infinitely many intervals of unbounded length, which would not prove the target statement.

status:
must be proved in final proof

suggested_solver:
S4

id:
SC6

statement:
Combining SC3-SC5 gives infinitely many isomorphism types of Bruhat intervals of one fixed length `k` in every infinite irreducible Coxeter group.

uses_prior_subclaims:
SC3, SC4, SC5

purpose:
Completes the contrapositive of the converse implication.

status:
must be proved in final proof

suggested_solver:
S5

4. Hardest step prediction

hardest_step_id:
SC3

hardest_step_description:
The hard point is producing, in every infinite irreducible Coxeter group, intervals of one fixed length whose isomorphism types vary infinitely. The proof must not merely use arbitrarily long intervals `[e,w]`; the length difference must remain fixed.

risk_if_wrong:
If the construction only gives intervals of increasing length, or if the proposed invariant is not actually unbounded at fixed interval length, the converse fails. This is also the point where circular use of the target theorem is most likely.

how_final_proof_should_handle_it:
The final proof should give an explicit uniform construction of pairs `u_n <= v_n`, verify reducedness and Bruhat comparability using the subword criterion, compute `ell(v_n)-ell(u_n)=k`, and exhibit a concrete isomorphism invariant such as rank cardinalities, covering degrees, or number of elements with a specified local order property.

5. Failure-mode checks

circularity_check:
Do not assume any known classification theorem saying the target statement is true. The infinite-case construction must be proved directly from standard Coxeter/Bruhat facts.

full_theorem_check:
Both directions must be proved. The finite case is immediate; the infinite irreducible case requires producing failure for at least one fixed `k`.

source_check:
No formal supporting statements or additional guidance are supplied. Only standard Coxeter background and facts proved inside the current proof may be used.

hypothesis_check:
Irreducibility must be used in the infinite-case construction. The proof should not silently pass to reducible products or assume finite rank unless justified.

notation_check:
`length` of an interval means `ell(v)-ell(u)`, not cardinality of the interval.

standard_background_check:
Allowed standard background includes Coxeter systems, reduced expressions, length, Bruhat order, and the subword criterion. Any stronger structural claim about infinite irreducible Coxeter groups must be proved inside the current proof unless genuinely standard and explicitly stated.

6. Subproblem assignment table

S1:
Prove SC1 and SC2. Give the finite-group argument and restate the converse as a contrapositive. Do not address the construction of infinite families.

S2:
Prove SC3. Starting only from standard Coxeter/Bruhat facts, construct in an arbitrary infinite irreducible Coxeter group an infinite family of comparable pairs `u_n <= v_n` whose Bruhat intervals have one fixed length and a growing finite-poset invariant.

S3:
Prove SC4. Identify exactly which invariant from S2 is used and prove it is preserved by finite-poset isomorphism.

S4:
Prove SC5. Check reduced expressions, Bruhat comparability, and the exact equality `ell(v_n)-ell(u_n)=k` for the construction from S2.

S5:
Assemble SC1-SC5 into the theorem. Verify that the argument proves the stated “for each fixed `k`” property for finite `W`, and its failure for infinite irreducible `W`.

7. Web-source confirmation

no web sources used

Assigned subproblem:
Prove SC1 and SC2. Give the finite-group argument and restate the converse as a contrapositive. Do not address the construction of infinite families.