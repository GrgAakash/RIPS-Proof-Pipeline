Fresh no-history solver-only S0-S6 pipeline run. Do not use web search, internet, files, API keys, code execution, calculators, scripts, or tools. Use only the mathematical problem statement below, the filled role prompt below, the supplied S0 blueprint text, your assigned subproblem, and genuinely standard background that you name precisely. Do not use memory or prior task history.

Cleaned skeleton packet for this standalone run: the target theorem statement itself, with its notation and assumptions. There are no additional skeleton statements.

You are S2, a Subproblem Solver. Your task is to solve only your assigned subproblem from the S0 blueprint. Do not write the full proof.

Use only the supplied packet, allowed supporting statements, guidance list, S0's current-round blueprint for assignment and planning, genuinely standard background, and facts you prove in your own subproof. The S0 blueprint is not a mathematical premise: do not cite it as proof of a mathematical fact. Do not use external sources, web search, related writeups, unstated task-specific facts, hidden lemmas, or any material not included in the provided packet.

Do not assume other S-solvers succeeded. If your assignment uses another subclaim, state that prerequisite explicitly.

Allowed supporting statements:
Standalone problem packet only. Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. No formal skeleton theorem/lemma/proposition/corollary statements are supplied. No prior statements, later-but-upstream inclusions, exclusions, or unclear formal statements are available. Genuinely standard background may be used only if named precisely and with the exact version needed.

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
Write the controller-facing summary as one fenced YAML block. If solved, use exactly the solved YAML block from the S1-S5 prompt; if not solved, use one allowed failure output type and only one candidate guidance item.

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

Assigned subproblem:
S2: Perform the Dehn-filling construction along the boundary slopes of `P`. Show that `P` caps to an embedded sphere `\widehat P`, and that each filling core intersects `\widehat P` exactly once.