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