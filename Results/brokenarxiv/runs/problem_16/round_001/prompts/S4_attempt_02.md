CLEANED SKELETON PACKET FOR THIS RUN

Definitions/notation allowed for parsing the target:
- An algebraic torus T over Q is a Q-group that becomes isomorphic to a power of G_m over a finite extension of Q.
- For a prime p, Q_p is the p-adic field.
- T(Q_p) denotes the group of Q_p-points.
- T(Q) denotes the group of Q-points.
- T(Z_p) denotes the maximal compact subgroup of T(Q_p).

Formal statements before the target theorem: None.
Later-but-upstream inclusions: None.
Exclusions: None.
Unclear: None.

Target theorem:
For any algebraic torus T over Q and any prime number p, the decomposition T(Q_p) = T(Z_p)T(Q) holds, where T(Z_p) denotes the maximal compact subgroup of T(Q_p).
You are S4, a Subproblem Solver. Your task is to solve only your assigned subproblem from the S0 blueprint. Do not write the full proof.

You are given:
1. the cleaned skeleton PDF or TeX file;
2. the target theorem;
3. the Allowed supporting statements list;
4. the additional mathematical guidance list, if any;
5. S0's blueprint for this same round;
6. your assigned subproblem.

Use only the supplied packet, allowed supporting statements, guidance list, S0's current-round blueprint for assignment and planning, genuinely standard background, and facts you prove in your own subproof. The S0 blueprint is not a mathematical premise: do not cite it as proof of a mathematical fact. Do not use external sources, web search, related writeups, unstated task-specific facts, hidden lemmas, or any material not included in the provided packet.

If a guidance item is labeled `[INTERNALLY VERIFIED AUXILIARY RESULT E###]`, you may use only its exact statement without reproof. Identify E### at every load-bearing use, do not reconstruct the withheld branch proof, and do not infer anything stronger than the released statement.

Do not assume other S-solvers succeeded. If your assignment uses another subclaim, state that prerequisite explicitly.

Allowed supporting statements:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed.
No formal skeleton statement may be cited without reproof because there are no formal statements before the target theorem in this standalone packet.
Genuinely standard background may be used as permitted by the fixed solver prompt.

This list or rule is authoritative for this run.

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
For any algebraic torus T over Q and any prime number p, the decomposition T(Q_p) = T(Z_p)T(Q) holds, where T(Z_p) denotes the maximal compact subgroup of T(Q_p).

Additional mathematical guidance:
None

S0 blueprint:
1. Target decomposition

target_label:
local_rational_compact_decomposition_for_Q_tori

target_type:
Theorem.

main_goal:
Show that every local point of a Q-torus at p differs from a rational point by an element of the maximal compact subgroup.

variables_and_parameters:
T: an algebraic torus over Q.
p: a prime number.
Q_p: the p-adic field.
T(Q_p): local p-adic points.
T(Q): rational points.
T(Z_p): the maximal compact subgroup of T(Q_p).

conclusion_to_prove:
For every t in T(Q_p), there exist k in T(Z_p) and q in T(Q) such that t = kq. Equivalently, T(Q_p) = T(Z_p)T(Q).

2. Available tools

tool:
Character lattice description of a torus.

source_status:
standard background fact.

exact_statement_or_fact:
If K/Q is a finite Galois splitting field for T, G = Gal(K/Q), and X = X^*(T_K), then T(Q) identifies with Hom_G(X, K^*) and, after choosing a place w of K over p with decomposition group D, T(Q_p) identifies with Hom_D(X, K_w^*).

intended_role_in_proof:
Translate the decomposition problem into a statement about matching valuations of character values.

tool:
Existence of finite Galois splitting field.

source_status:
standard background fact.

exact_statement_or_fact:
Every algebraic torus over Q becomes split over some finite Galois extension K/Q.

intended_role_in_proof:
Allows use of character lattices and valuation maps over a splitting field.

tool:
Local valuation map for tori.

source_status:
proved inside the current proof.

exact_statement_or_fact:
For F = Q_p, a finite Galois splitting field L/F, and D = Gal(L/F), the map t ↦ (χ ↦ v_L(χ(t))) from T(F) to Hom_D(X^*(T_L), Z) has kernel equal to the maximal compact subgroup T(Z_p), with image canonically identifying T(F)/T(Z_p).

intended_role_in_proof:
Reduces the target equality to surjectivity of rational points onto the local valuation quotient.

tool:
Number-field valuation flexibility.

source_status:
standard background fact, with elementary proof allowed.

exact_statement_or_fact:
For a number field K and finitely many primes of K, elements of K^* can be chosen with prescribed valuations at those primes, with no restrictions imposed at primes outside the chosen finite set.

intended_role_in_proof:
Provides the raw global elements needed to match prescribed p-adic valuations.

tool:
Equivariant valuation lifting lemma.

source_status:
proved inside the current proof.

exact_statement_or_fact:
Let K/Q be finite Galois, G = Gal(K/Q), w | p, D the decomposition group at w, and X a finite free G-lattice. Any valuation homomorphism X -> Z arising from a local D-equivariant homomorphism X -> K_w^* is also v_w composed with some global G-equivariant homomorphism X -> K^*.

intended_role_in_proof:
This is the central arithmetic step: it produces q in T(Q) with the same local valuation data as a given t in T(Q_p).

3. Subclaim support graph

C1: Choose a finite Galois splitting field K/Q for T, a place w | p, set G = Gal(K/Q), D = Gal(K_w/Q_p), and X = X^*(T_K). Then T(Q) = Hom_G(X, K^*) and T(Q_p) = Hom_D(X, K_w^*).
C2: For the local torus T/Q_p, the character-valuation map on T(Q_p) has kernel exactly T(Z_p), the maximal compact subgroup.
C3: For any t in T(Q_p), the local valuation homomorphism χ ↦ v_w(χ(t)) is realized by some rational point q in T(Q); that is, v_w(χ(q)) = v_w(χ(t)) for every χ in X.
C4: If t in T(Q_p) and q in T(Q) have identical local character valuations over K_w, then tq^{-1} belongs to T(Z_p).
C5: Every t in T(Q_p) can be written t = kq with k in T(Z_p) and q in T(Q).

4. Hardest step prediction
hardest_step_id: C3
hardest_step_description: Proving the equivariant valuation lifting lemma without assuming the desired theorem. The proof must show exact surjectivity, not merely finite cokernel.

5. Failure-mode checks
Do not cite the target theorem, weak approximation for tori in the same form, or adelic class-number statements that already imply the target. Handle every Q-torus. No web sources or external writeups.

6. Subproblem assignment table
S1: Prove C1 and C2. Work with a finite Galois splitting field K/Q and local splitting field K_w/Q_p. Establish the Hom_G and Hom_D descriptions, define the character-valuation map, and prove its kernel is exactly the maximal compact subgroup T(Z_p).
S2: Prove C3. State and prove the equivariant valuation lifting lemma for a finite free G-lattice X, using prescribed valuations in K^* and the G/D decomposition above p. Ensure the result gives exact valuation matching, not just finite-index matching.
S3: Prove C4. Starting from equal local character valuations for t and q, show all character values of tq^{-1} have valuation zero over K_w, then use C2 to conclude tq^{-1} is in T(Z_p).
S4: Assemble C3 and C4 into the target factorization. For arbitrary t in T(Q_p), choose q in T(Q) by C3, set k = tq^{-1}, and conclude k in T(Z_p).
S5: Perform the final consistency audit: independence of the choice of K and w, compatibility with ramified and split cases, and confirmation that T(Z_p) is used only as maximal compact.

7. Web-source confirmation
no web sources used

Assigned subproblem:
S4: Assemble C3 and C4 into the target factorization. For arbitrary t in T(Q_p), choose q in T(Q) by C3, set k = tq^{-1}, and conclude k in T(Z_p).