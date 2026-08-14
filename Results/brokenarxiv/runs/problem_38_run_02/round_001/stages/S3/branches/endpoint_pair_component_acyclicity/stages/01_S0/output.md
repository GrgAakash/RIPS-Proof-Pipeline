1. Target decomposition

target_label:  
Branch Lemma E001 candidate

target_type:  
Acyclicity theorem for connected components of an ordered line-transversal direction set.

main_goal:  
Show that each connected component of `D_sigma ⊂ S^{d-1}` has trivial reduced homology.

variables_and_parameters:  
`d ≥ 1`; `n ≥ 2`; pairwise disjoint open convex sets `C_1,...,C_n ⊂ R^d`; an ordering `sigma` of `{1,...,n}`; the unit sphere `S^{d-1}`; the direction set `D_sigma`.

conclusion_to_prove:  
For every connected component `K` of `D_sigma`, `\widetilde H_*(K) = 0`.

2. Available tools

tool:  
Line-space parametrization by direction and offset.

source_status: standard background fact.

exact_statement_or_fact:  
For fixed `u ∈ S^{d-1}`, every oriented line with direction `u` is uniquely expressible as `{p + t u : t ∈ R}` with `p ∈ u^\perp`.

intended_role_in_proof:  
Convert the existence of an oriented line with direction `u` into a condition on offsets `p ∈ u^\perp`.

tool:  
Convex projection.

source_status: standard background fact.

exact_statement_or_fact:  
The orthogonal projection of an open convex subset of `R^d` onto a linear subspace is open and convex.

intended_role_in_proof:  
For fixed `u`, the set of offsets whose lines meet `C_i` is an open convex subset of `u^\perp`.

tool:  
Convex interval sections.

source_status: standard background fact.

exact_statement_or_fact:  
If `C ⊂ R^d` is open and convex, then for any affine line `L`, the intersection `L ∩ C` is either empty or an open interval in `L`.

intended_role_in_proof:  
Along any transversal line, each `C_i` contributes a single open interval, so the order condition is well-defined by interval order.

tool:  
Parameter space of ordered transversals.

source_status: proved inside the current proof.

exact_statement_or_fact:  
Define  
`T_sigma = {(u,p) : u ∈ S^{d-1}, p ∈ u^\perp, p + R u meets C_{sigma(1)},...,C_{sigma(n)} in that order}`.  
Then `D_sigma` is the projection of `T_sigma` to the first coordinate.

intended_role_in_proof:  
Replace `D_sigma` by a fiberwise convex or contractible total space whose projection controls homology.

tool:  
Fiber convexity/contractibility.

source_status: proved inside the current proof.

exact_statement_or_fact:  
For each fixed `u`, the fiber  
`T_sigma(u) = {p ∈ u^\perp : (u,p) ∈ T_sigma}`  
is either empty or open convex, hence contractible.

intended_role_in_proof:  
Provides contractible fibers over directions.

tool:  
Projection homotopy equivalence or Vietoris-type acyclicity principle.

source_status: standard background fact, but must be explicitly stated in final proof.

exact_statement_or_fact:  
If a continuous proper map between reasonable spaces has acyclic fibers and satisfies the hypotheses of the Vietoris-Begle theorem, then it induces isomorphisms on homology. A local version may be applied over compact subsets or connected components when properness is obtained by restriction.

intended_role_in_proof:  
Transfer acyclicity from a suitable ordered-transversal space to connected components of `D_sigma`.

tool:  
Convex sets are acyclic.

source_status: standard background fact.

exact_statement_or_fact:  
Every nonempty convex subset of Euclidean space is contractible, hence has trivial reduced homology.

intended_role_in_proof:  
Used for fibers and any convex model space built during the proof.

3. Subclaim support graph

id: S1  
statement:  
For each `u ∈ S^{d-1}`, the oriented lines with direction `u` are parametrized by offsets `p ∈ u^\perp`, and for each `i`, the set of offsets whose line meets `C_i` is open convex.  
uses_prior_subclaims: none.  
purpose:  
Set up the fiber description of ordered transversals.  
status: standard background / must be proved in final proof.  
suggested_solver: S1.

id: S2  
statement:  
For fixed `(u,p)`, if the line `p + R u` meets each relevant `C_i`, then each intersection is an open interval in the line parameter `t`, and the order condition is equivalent to a finite system of strict inequalities between these intervals.  
uses_prior_subclaims: S1.  
purpose:  
Make the order condition precise and stable under small perturbations.  
status: must be proved in final proof.  
suggested_solver: S2.

id: S3  
statement:  
For fixed `u`, the fiber `T_sigma(u)` of offsets producing the order `sigma` is either empty or open convex.  
uses_prior_subclaims: S1, S2.  
purpose:  
This is the main geometric step needed for acyclicity.  
status: must be proved in final proof.  
suggested_solver: S3.

id: S4  
statement:  
Each connected component of the total ordered-transversal space `T_sigma` lying over a connected component of `D_sigma` is acyclic.  
uses_prior_subclaims: S3.  
purpose:  
Build an acyclic model space before projecting to directions.  
status: must be proved in final proof.  
suggested_solver: S4.

id: S5  
statement:  
The projection `pi : T_sigma → D_sigma`, `pi(u,p)=u`, preserves reduced homology on connected components, because its fibers over directions are nonempty acyclic and the map satisfies an applicable Vietoris-Begle or equivalent homological fiber theorem after the needed local/properness reductions.  
uses_prior_subclaims: S3, S4.  
purpose:  
Transfer acyclicity from the ordered-transversal parameter space to each connected component of `D_sigma`.  
status: must be proved in final proof.  
suggested_solver: S5.

4. Hardest step prediction

hardest_step_id:  
S3/S5.

hardest_step_description:  
The delicate point is proving that the offset fiber for a fixed direction is convex under the ordered condition, and then justifying that projection from ordered transversals to directions does not create homology.

risk_if_wrong:  
If the ordered fibers are not convex, or if the projection theorem is applied without its hypotheses, the proof may only show that `D_sigma` is covered by acyclic fibers, which is not enough to prove its connected components are acyclic.

how_final_proof_should_handle_it:  
The final proof should give a direct convexity argument for the ordered-offset fiber, not only for the unordered transversal fiber. It should also state the exact homological projection theorem being used and verify its hypotheses, including local compactness/paracompactness and any compactness or properness reduction.

5. Failure-mode checks

circularity_check:  
Do not cite the target acyclicity theorem, any line-transversal “pinched ball” theorem, or any known geometric permutation theorem.

full_theorem_check:  
The proof must address every connected component of `D_sigma`, not merely show that `D_sigma` is nonempty, open, or locally contractible.

source_check:  
No supporting statements are provided. Every nonstandard geometric fact about ordered line transversals must be proved inside the final proof.

hypothesis_check:  
Use all assumptions correctly: openness gives stable interval intersections; convexity gives interval sections and convex projected sets; pairwise disjointness prevents interval overlap and makes the order unambiguous; `n ≥ 2` avoids degenerate single-set ordering.

notation_check:  
Clarify whether “meeting in that order” means increasing line parameter along the oriented direction `u`, and define `T_sigma`, fibers, and projection maps explicitly.

standard_background_check:  
Any standard background beyond elementary convexity, line parametrization, and basic homology must be named and stated, especially if using Vietoris-Begle or another homological fiber theorem.

6. Subproblem assignment table

S1:  
Prove the fixed-direction line parametrization and show that projections of each `C_i` to `u^\perp` are open convex. Define the unordered transversal fiber as the intersection of these projections.

S2:  
For a fixed line `p + R u`, prove that intersections with the `C_i` are open intervals and formalize the order condition using interval endpoints or strict separation of intervals.

S3:  
Prove that for fixed `u`, the set of offsets producing the order `sigma` is empty or open convex. This must include the convexity of the ordered inequality conditions.

S4:  
Construct the ordered-transversal space `T_sigma`, analyze its connected components over a connected component of `D_sigma`, and prove the needed acyclicity result for that total space.

S5:  
Prove that projection `T_sigma → D_sigma` transfers acyclicity to each connected component of `D_sigma`, stating and verifying the exact standard homological theorem used.

7. Web-source confirmation

no web sources used