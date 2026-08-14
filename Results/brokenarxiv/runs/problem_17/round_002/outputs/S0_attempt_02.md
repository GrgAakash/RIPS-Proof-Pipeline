1. Target decomposition

target_label:
Ample generics for the Fraisse limit of finite two-sorted ultrametric spaces with dc-embeddings.

target_type:
Fraisse-limit automorphism group theorem via the Kechris-Rosendal / Hodges-Hodkinson-Lascar-Shelah weak-amalgamation criterion.

main_goal:
For every integer `n >= 1`, prove that the class `K_p^n` of finite `n`-systems of partial automorphisms over the Fraisse class has JEP and WAP; then apply the standard criterion.

variables_and_parameters:
`K`: finite two-sorted ultrametric spaces with dc-embeddings.  
`U`: Fraisse limit of `K`.  
`n >= 1`: fixed arity for tuples of automorphisms.  
`S,T,A,B,C`: finite objects in `K_p^n`.  
`p_i`: point-sort partial automorphism in an `n`-system.  
`q_i`: distance-sort partial order-preserving partial injection associated to `p_i`.

conclusion_to_prove:
`Aut(U)` has ample generics, i.e. for every `n >= 1`, the diagonal conjugacy action of `Aut(U)` on `Aut(U)^n` has a comeager orbit.

2. Available tools

tool:
Fraisse-limit setup for `K`.

source_status:
allowed supporting statement / standard background fact.

exact_statement_or_fact:
If `K` is a countable Fraisse class with limit `U`, then finite partial isomorphisms of members of `K` embed into `U`, and automorphisms of `U` are controlled by finite partial automorphism systems over `K`.

intended_role_in_proof:
Allows use of the KR/HHLS criterion after proving the required class-specific properties for `K_p^n`.

tool:
KR/HHLS ample generics criterion.

source_status:
allowed supporting statement / standard background fact.

exact_statement_or_fact:
For a Fraisse class `K` with limit `U`, `Aut(U)` has ample generics iff for every `n >= 1`, the class `K_p^n` of finite structures equipped with `n` partial automorphisms has the joint embedding property and the weak amalgamation property.

intended_role_in_proof:
Reduces the target theorem to finite combinatorial amalgamation of `n`-systems.

tool:
Free ultrametric amalgamation over a common subspace.

source_status:
proved inside the current proof.

exact_statement_or_fact:
Given finite ultrametric spaces `B,C` over a common finite subspace `A`, after amalgamating the distance sorts into one finite linear order, define for `b in B`, `c in C`
`d(b,c)=min_{a in A} max(d_B(b,a), d_C(a,c))`.
Then this gives a finite ultrametric extending both sides.

intended_role_in_proof:
Supplies the point-sort amalgam once the distance-sort order has been prepared.

tool:
Finite linear-order amalgamation for distance sorts.

source_status:
proved inside the current proof.

exact_statement_or_fact:
Given two finite linearly ordered distance sets extending a common finite ordered subset, there is a finite linear order amalgam preserving the two embeddings and identifying the common part.

intended_role_in_proof:
Basic distance-sort amalgamation for JEP/AP-level arguments.

tool:
Prepared-system distance equivariance lemma.

source_status:
additional guidance item / proved inside the current proof.

exact_statement_or_fact:
For every finite `n`-system `S in K_p^n`, there is a finite extension `T` such that any two finite extensions of `T` admit a finite linear ordered distance-sort amalgam where each union of corresponding distance partial maps is a well-defined order-preserving partial injection, and the min-max bridge distances over the base are equivariant under these partial maps.

intended_role_in_proof:
This is the central WAP witness construction.

tool:
Orbit completion for finite partial injections.

source_status:
proved inside the current proof.

exact_statement_or_fact:
A finite family of partial injections can be extended on a finite set to finite partial bijections whose relevant finite orbits are long enough and whose images/domains contain all distances needed for the later bridge calculations.

intended_role_in_proof:
Used to build the prepared witness `T`.

tool:
Two-sorted dc-embedding bookkeeping.

source_status:
provided definition / notation / proved inside current proof.

exact_statement_or_fact:
A dc-embedding consists of an injective point map and an order-preserving distance-sort injection preserving `0` and all point distances.

intended_role_in_proof:
Ensures all finite constructions remain objects and embeddings in the intended category.

3. Subclaim support graph

id:
SC1

statement:
For each `n`, define `K_p^n` precisely: objects are finite two-sorted ultrametric spaces equipped with `n` finite partial automorphisms, each consisting of compatible point and distance partial maps; morphisms are dc-embeddings respecting all partial maps. This is the correct class used by the KR/HHLS criterion.

uses_prior_subclaims:
none.

purpose:
Fixes notation and prevents ambiguity about partial automorphisms in the two-sorted setting.

status:
must be proved in final proof.

suggested_solver:
S1.

id:
SC2

statement:
`K_p^n` has JEP for every `n >= 1`.

uses_prior_subclaims:
SC1.

purpose:
One half of the KR/HHLS criterion.

status:
must be proved in final proof.

suggested_solver:
S2.

id:
SC3

statement:
Finite free ultrametric amalgamation works over a common subspace once the distance sorts are placed in one finite linear order, using bridge distances
`d(b,c)=min_a max(d(b,a),d(a,c))`.

uses_prior_subclaims:
SC1.

purpose:
Gives the point-sort amalgamation mechanism used both for JEP and WAP.

status:
must be proved in final proof.

suggested_solver:
S2.

id:
SC4

statement:
For every finite `n`-system `S`, there is a finite prepared extension `T` such that every relevant point-distance value and every value forced by applying the partial distance maps is represented in the distance sort, with enough finite orbit closure to compare values consistently.

uses_prior_subclaims:
SC1.

purpose:
Constructs the WAP witness before arbitrary extensions are amalgamated.

status:
must be proved in final proof.

suggested_solver:
S3.

id:
SC5

statement:
Prepared-system distance amalgamation/equivariance lemma: any two finite extensions of the prepared witness `T` have a finite ordered distance-sort amalgam in which the unions of corresponding distance partial maps are well-defined order-preserving partial injections, and the min-max bridge distances over `T` are equivariant.

uses_prior_subclaims:
SC4.

purpose:
Hard finite-order combinatorial lemma required by the additional guidance.

status:
must be proved in final proof.

suggested_solver:
S4.

id:
SC6

statement:
Using SC3 and SC5, any two finite extensions of `T` in `K_p^n` amalgamate over `S`, so `K_p^n` has WAP.

uses_prior_subclaims:
SC1, SC3, SC4, SC5.

purpose:
Completes the class-specific hypothesis of the KR/HHLS criterion.

status:
must be proved in final proof.

suggested_solver:
S5.

id:
SC7

statement:
By SC2 and SC6 for every `n >= 1`, the KR/HHLS criterion applies, hence `Aut(U)` has ample generics.

uses_prior_subclaims:
SC1, SC2, SC6.

purpose:
Final theorem-level reduction.

status:
standard background plus proved class-specific hypotheses.

suggested_solver:
S5.

4. Hardest step prediction

hardest_step_id:
SC5.

hardest_step_description:
The main difficulty is not ordinary ultrametric amalgamation but simultaneous ordered-distance amalgamation respecting finitely many partial distance maps. The final proof must guarantee that after amalgamating two arbitrary extensions of the prepared witness, each union of corresponding distance partial maps is still a well-defined order-preserving partial injection, and that bridge distances defined by the min-max formula are carried correctly by these maps.

risk_if_wrong:
If the distance-sort amalgam is not equivariant, the point-sort bridge distances may fail to be preserved by the partial automorphisms. Then the WAP amalgam would not be an object of `K_p^n`.

how_final_proof_should_handle_it:
The proof should isolate a purely finite linear-order lemma. It should explicitly track cuts over the prepared base, show that new distances from the two extensions can be inserted into a common finite linear order without reversing any required comparison, and prove equivariance of the bridge formula from equivariance on base distances.

5. Failure-mode checks

circularity_check:
Do not assume ample generics, cofinal amalgamation, or WAP for this class. Only the general KR/HHLS criterion may be used.

full_theorem_check:
The proof must handle every `n >= 1`, not just one automorphism.

source_check:
No web sources, prior outputs, answer keys, or external files are used. All class-specific facts are assigned as subclaims to prove.

hypothesis_check:
The final proof must verify both JEP and WAP for `K_p^n`; JEP alone is insufficient.

notation_check:
The two sorts must remain separate: point maps and distance-sort maps both have to be included in every partial automorphism and embedding.

standard_background_check:
Standard background is limited to Fraisse facts and the KR/HHLS criterion, stated abstractly. The finite ordered-distance amalgamation and ultrametric bridge construction are not treated as black boxes.

6. Subproblem assignment table

S1:
Define `K_p^n` in the two-sorted dc-setting. Spell out objects, morphisms, extensions, and compatibility of point and distance partial maps. Verify that this is the class to which the KR/HHLS criterion applies.

S2:
Prove finite free ultrametric amalgamation over a common subspace after distance-sort amalgamation, including the min-max bridge formula and the ultrametric inequality. Use it to prove JEP for `K_p^n`.

S3:
Construct the prepared extension `T` of an arbitrary finite `n`-system `S`. The construction must close enough finite point and distance data under the partial maps so later arbitrary extensions can be amalgamated equivariantly.

S4:
Prove the prepared-system ordered-distance amalgamation/equivariance lemma required by the guidance. This should be a finite linear-order argument with explicit verification that all union distance maps remain order-preserving partial injections.

S5:
Combine the prepared distance amalgam with the free ultrametric point amalgam to prove WAP for `K_p^n`; then apply the KR/HHLS criterion for all `n >= 1` to conclude ample generics for `Aut(U)`.

7. Web-source confirmation

no web sources used.