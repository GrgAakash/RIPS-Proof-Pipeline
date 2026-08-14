1. Assignment restatement

S-ID: SS2  
work_scope: assigned_subclaim  
assigned subclaim(s): SC2/TDC-3  
what must be proved: an exact componentwise homology-transfer lemma for the endpoint/witness incidence projections, with hypotheses verified for `W -> P` and `W -> D`.  
connection to the exact target: this supplies only the homology-transfer step; it does not prove acyclicity of `P` components by itself.  
inferred_standard_setup_for_this_assignment: all spaces have Euclidean subspace topology; singular homology uses integer coefficients unless otherwise specified; for `m=2`, `Delta` is the one-point open subset of `R^0`.  
where this result is used in the final solution: to replace component homology of endpoint components in `P` by component homology of witness-parameter components in `D`, through `W`.  
declared prerequisite subclaims: none beyond the stated definitions and allowed elementary topology/convexity.

2. Subproof or failure

**Lemma.** Let `B` be an open subset of `R^q`, let `E subset B x R^N` be open, and let `p:E -> B` be projection. Assume every fiber
`E_b = {y in R^N : (b,y) in E}`
is nonempty and convex. Then `p` is a homotopy equivalence on each connected component. More precisely, for every connected component `B0` of `B`, `p^{-1}(B0)` is a connected component of `E`, and
`p|_{p^{-1}(B0)} : p^{-1}(B0) -> B0`
is a homotopy equivalence. Hence it induces isomorphisms on ordinary singular homology in all degrees.

Proof. For each `b in B`, choose `y_b in E_b`. Since `E` is open, there is an open neighborhood `U_b` of `b` such that `U_b x {y_b} subset E`. Because open subsets of Euclidean space are paracompact, choose a locally finite partition of unity `{phi_alpha}` subordinate to a refinement of `{U_b}`. For each `alpha`, choose `b(alpha)` with `supp(phi_alpha) subset U_{b(alpha)}` and put `y_alpha=y_{b(alpha)}`. Define
`sigma(x)=sum_alpha phi_alpha(x)y_alpha`.
The sum is locally finite. If `phi_alpha(x)>0`, then `x in U_{b(alpha)}`, so `y_alpha in E_x`; by convexity of `E_x`, `sigma(x) in E_x`. Thus `s(x)=(x,sigma(x))` is a continuous section.

Now
`H((b,y),t)=(b,(1-t)y+t sigma(b))`
lies in `E` for all `t in [0,1]`, again by convexity of `E_b`. This is a deformation from `id_E` to `s p`, while `p s=id_B`; hence `p` is a homotopy equivalence.

For components, each component of an open Euclidean set is path-connected. If `B0` is a component of `B`, then any two points of `p^{-1}(B0)` can be joined by moving vertically inside convex fibers to the section, moving along the section over a path in `B0`, and moving vertically again. Hence `p^{-1}(B0)` is path-connected and is exactly one component of `E`. The restricted homotopy equivalence follows.

Apply this to `W -> P`. Let `n=m-2`. For `(a,b) in P`, the fiber is
`{lambda in Delta : (1-lambda_i)a + lambda_i b in C_i for i=2,...,m-1}`.
For fixed `(a,b)`, each condition is the inverse image of the convex set `C_i` under an affine map in `lambda_i`; intersecting these convex sets with the convex open ordering simplex `Delta` gives a nonempty convex fiber. `W` is open because all incidence conditions are inverse images of open sets under continuous maps, and `P` is open because it is the projection of the open set `W`. Thus every component of `W` maps by `W -> P` homotopy equivalently onto a component of `P`.

Apply this to `W -> D`. For fixed `lambda in D`, the fiber is
`P_lambda = (C_1 x C_m) cap ⋂_{i=2}^{m-1} L_i^{-1}(C_i)`,
where `L_i(a,b)=(1-lambda_i)a+lambda_i b`. Each `L_i^{-1}(C_i)` is open and convex in `R^{2d}`, and `C_1 x C_m` is open and convex, so `P_lambda` is nonempty convex. Also `D` is open as the projection of open `W`. Thus every component of `W` maps by `W -> D` homotopy equivalently onto a component of `D`.

Consequently, if `K` is a connected component of `W`, then `K`, `pi_P(K)`, and `pi_D(K)` have canonically transferred singular homology through homotopy equivalences:
`H_*(pi_P(K)) ≅ H_*(K) ≅ H_*(pi_D(K))`.
This establishes the requested componentwise homology-transfer claim only.

3. Solver failure output and candidate guidance

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

4. Local Source Ledger, including TDC reports and Unknowns addendum

claim_id: L1  
proof_location: Section 2, convex-fiber projection lemma  
claim_or_fact_used: open convex-fiber projections over Euclidean open bases admit continuous sections and fiberwise straight-line deformation retractions  
source_status: proved inside the current proof  
cited_label_or_name: convex-fiber projection lemma  
exact_statement_used: as stated in Section 2  
hypotheses_or_conditions_needed: `B` open Euclidean, `E` open in `B x R^N`, fibers nonempty convex  
where_hypotheses_are_checked: checked for `W -> P` and `W -> D` in Section 2  
strength_used: homotopy equivalence on connected components and homology isomorphism  
notes: no acyclicity conclusion is inferred without an acyclicity input for the corresponding base component

claim_id: L2  
proof_location: Section 2, applications  
claim_or_fact_used: affine preimages and intersections of open convex sets are open convex  
source_status: standard background fact / elementary convexity  
cited_label_or_name: elementary convexity  
exact_statement_used: affine inverse images preserve convexity and openness; finite intersections preserve both  
hypotheses_or_conditions_needed: `C_i` open convex; maps `L_i` affine  
where_hypotheses_are_checked: target setup and definitions of `L_i`  
strength_used: fiber convexity for both incidence projections  
notes: pairwise disjointness is not needed for SC2

claim_id: L3  
proof_location: Section 2, lemma proof  
claim_or_fact_used: open subsets of Euclidean space are paracompact and admit locally finite partitions of unity subordinate to open covers  
source_status: allowed supporting statement  
cited_label_or_name: Euclidean partition of unity  
exact_statement_used: every open cover of an open Euclidean subset has a locally finite subordinate partition of unity  
hypotheses_or_conditions_needed: base is open in Euclidean space  
where_hypotheses_are_checked: `P` and `D` are open projections of open `W`  
strength_used: construction of continuous section  
notes: used exactly at stated strength

claim_id: TDC-3  
claim: endpoint/witness incidence projections preserve component homology  
claim_basis: derived_here  
exact_statement_used: each connected component of `W` maps homotopy equivalently onto a connected component of `P` under `W -> P` and onto a connected component of `D` under `W -> D`  
hypotheses_checked: openness of `W`, `P`, `D`; nonempty convex fibers for both projections  
normalization: ordinary singular homology, integer coefficients unless otherwise specified  
local_source_location: Section 2  
competing_variants: arbitrary convex fibers without openness/section hypotheses are not used  
status: ESTABLISHED

```yaml
unknown_id: U001
kind: projection-lemma verification
description: exact projection lemma required for componentwise homology transfer through W
target_determining: true
current_evidence: Section 2 proves the convex-fiber projection lemma and verifies it for W -> P and W -> D
candidate_resolutions:
  - resolved_by_current_subproof
downstream_outcomes: component homology may be transferred between corresponding components of P, W, and D
answer_sensitivity_rationale: without this lemma, acyclicity of D components would not transfer to P components
resolution_test_id: U001-required_resolution_test
required_resolution_test: State and prove exact projection lemma used, then verify its hypotheses for witness and endpoint-to-line maps componentwise.
assigned_solver: SS2
status: RESOLVED
```

No new unknowns.

5. Interface notes for S6

what this subproof establishes: `W -> P` and `W -> D` are componentwise homotopy equivalences, hence induce singular homology isomorphisms on corresponding connected components.  
what remains conditional: any later claim that components of `P` are acyclic still requires an independent proof that the corresponding components of `D` are acyclic.  
failure_output_type: solved

6. Web-source confirmation

no web sources used