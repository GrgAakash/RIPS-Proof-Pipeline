Fresh no-history solver-only S0-S6 pipeline run. Do not use web search, internet, files, API keys, code execution, calculators, scripts, or tools. Use only the mathematical problem statement below, the filled role prompt below, the supplied S0 blueprint text, your assigned subproblem, and genuinely standard background that you name precisely. Do not use memory or prior task history.

Cleaned skeleton packet for this standalone run: the target theorem statement itself, with its notation and assumptions. There are no additional skeleton statements.

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
Standalone problem packet only. Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. No formal skeleton theorem/lemma/proposition/corollary statements are supplied. No prior statements, later-but-upstream inclusions, exclusions, or unclear formal statements are available. Genuinely standard background may be used only if named precisely and with the exact version needed.

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
Let N >= 3 be an integer. For any N-component hyperbolic link L subset S^3 with exterior X_L = S^3 \ int(N(L)), where N(L) is a regular neighborhood of L, if P subset X_L is an incompressible spanning planar surface, meaning a planar surface with exactly one boundary component on each boundary torus of X_L, then at least one boundary component of P must have a slope a/p in standard meridian-longitude coordinates that is either meridional or integral, i.e. p in {0, 1}.

Additional mathematical guidance:
None

S0 blueprint:
1. Target decomposition

target_label: Target theorem  
target_type: universal implication about boundary slopes of incompressible planar spanning surfaces in hyperbolic link exteriors  
main_goal: prove that not all boundary slopes of `P` can be non-meridional non-integral.  
variables_and_parameters: `N >= 3`; `L = L_1 ∪ ... ∪ L_N ⊂ S^3`; exterior `X_L`; boundary tori `T_i = ∂N(L_i)`; meridian-longitude basis `(μ_i, λ_i)`; planar incompressible spanning surface `P`; slopes `r_i = a_i/p_i` of `∂P ∩ T_i`, in reduced standard form with `p_i >= 0`.  
conclusion_to_prove: for some `i`, `p_i ∈ {0,1}`, equivalently `r_i` is meridional or integral.

2. Available tools

tool: slope-distance conversion  
source_status: standard background fact  
exact_statement_or_fact: for slopes `a/p` and meridian `1/0`, the geometric intersection distance is `Δ(a/p, 1/0) = p` after normalizing `p >= 0`. Thus `p ∈ {0,1}` iff the slope has distance at most `1` from the meridian.  
intended_role_in_proof: translate the theorem into the contradiction assumption `Δ(r_i, μ_i) >= 2` for all `i`.

tool: Dehn filling along boundary slopes  
source_status: standard background fact  
exact_statement_or_fact: filling `T_i` along slope `r_i` attaches a solid torus `V_i` whose meridian disk has boundary slope `r_i`.  
intended_role_in_proof: fill all `T_i` along the slopes of `∂P`, so each boundary component of `P` caps off by a meridian disk.

tool: capped planar surface becomes a sphere  
source_status: standard background fact  
exact_statement_or_fact: a planar surface with exactly one boundary component on each of `N` filled tori caps off to a closed genus-zero surface, hence an embedded `S^2`.  
intended_role_in_proof: produce a sphere `\widehat P` in the filled closed manifold.

tool: sphere meeting a filling core once is essential  
source_status: standard background fact  
exact_statement_or_fact: if a sphere bounded a 3-ball, every closed curve would meet it algebraically/mod-2 zero times; a filling core meeting the cap disk once meets `\widehat P` once, so `\widehat P` cannot bound a ball.  
intended_role_in_proof: show the filled manifold is reducible.

tool: core-once reducible filling obstruction  
source_status: proved inside the current proof  
exact_statement_or_fact: if `L ⊂ S^3` is a hyperbolic link with `N >= 3`, and a full Dehn filling along slopes `r_i` produces an essential sphere intersecting each filling solid-torus core exactly once, then some `Δ(r_i, μ_i) <= 1`.  
intended_role_in_proof: this is the key nontrivial lemma giving the contradiction.

3. Subclaim support graph

id: C1  
statement: Normalize each slope as `r_i = a_i/p_i`, `p_i >= 0`, and assume for contradiction that every `p_i >= 2`.  
uses_prior_subclaims: none  
purpose: convert the negation of the conclusion into high meridian distance on every boundary torus.  
status: standard background  
suggested_solver: S1

id: C2  
statement: Dehn filling `X_L` along all slopes `r_i` caps `P` to an embedded sphere `\widehat P`.  
uses_prior_subclaims: C1  
purpose: convert the planar surface into a reducing-sphere candidate.  
status: standard background  
suggested_solver: S2

id: C3  
statement: `\widehat P` is essential in the filled manifold.  
uses_prior_subclaims: C2  
purpose: prove that the filling is reducible.  
status: standard background  
suggested_solver: S2

id: C4  
statement: In the situation of C2-C3, hyperbolicity of `L` and `N >= 3` force some filled slope to satisfy `Δ(r_i, μ_i) <= 1`.  
uses_prior_subclaims: C2, C3  
purpose: provide the decisive reducible-filling obstruction.  
status: must be proved in final proof  
suggested_solver: S4

id: C5  
statement: Since `Δ(r_i, μ_i) = p_i`, C4 contradicts C1; therefore some `p_i ∈ {0,1}`.  
uses_prior_subclaims: C1, C4  
purpose: assemble the contradiction and finish the theorem.  
status: standard background  
suggested_solver: S5

4. Hardest step prediction

hardest_step_id: C4  
hardest_step_description: proving the core-once reducible filling obstruction without importing an unsupported reducible surgery theorem.  
risk_if_wrong: the proof would either become circular, essentially restating the target theorem, or rely on an unallowed deep external result.  
how_final_proof_should_handle_it: isolate C4 as a named internal lemma, prove it independently from standard 3-manifold tools, and explicitly verify that its hypotheses match the capped surface produced from `P`.

5. Failure-mode checks

circularity_check: C4 must not assume the target theorem or any equivalent boundary-slope statement.  
full_theorem_check: the plan covers every `N >= 3`, every hyperbolic `N`-component link, and every incompressible planar spanning surface with one boundary component per torus.  
source_check: no prior skeleton statements, web sources, or hidden lemmas are used; C4 is marked as needing proof inside the current proof.  
hypothesis_check: do not add boundary-incompressibility, orientation choices, or extra link assumptions unless they are proved or purely notational.  
notation_check: use reduced slopes `a_i/p_i` with `p_i >= 0`; meridian is `1/0`; integral slopes are `a/1`.  
standard_background_check: only elementary Dehn filling conventions, slope distance, capping, and mod-2 intersection/parity are treated as standard.

6. Subproblem assignment table

S1: Set up notation. Let `T_i = ∂N(L_i)`, choose `(μ_i, λ_i)`, write each boundary slope as reduced `a_i/p_i`, and prove the equivalence between “not meridional or integral” and `p_i >= 2`.

S2: Perform the Dehn-filling construction along the boundary slopes of `P`. Show that `P` caps to an embedded sphere `\widehat P`, and that each filling core intersects `\widehat P` exactly once.

S3: Verify reducibility data carefully: prove `\widehat P` cannot bound a 3-ball using the one-intersection parity argument, and record all hypotheses needed for the obstruction lemma.

S4: Prove the core-once reducible filling obstruction: for a hyperbolic `N >= 3` link in `S^3`, such a reducing sphere after full filling forces at least one filling slope to have meridian distance at most `1`.

S5: Assemble the proof by contradiction. Apply S4, translate `Δ(r_i, μ_i) <= 1` into `p_i ∈ {0,1}`, and conclude that at least one boundary component of `P` is meridional or integral.

7. Web-source confirmation

no web sources used

Assigned subproblem:
S1: Set up notation. Let `T_i = ∂N(L_i)`, choose `(μ_i, λ_i)`, write each boundary slope as reduced `a_i/p_i`, and prove the equivalence between “not meridional or integral” and `p_i >= 2`.