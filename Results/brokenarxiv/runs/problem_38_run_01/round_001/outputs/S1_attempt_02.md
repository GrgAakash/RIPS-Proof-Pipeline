1. Assignment Restatement

S-ID: S1

assigned subclaim(s): SC1

what must be proved: After choosing the counterclockwise cyclic orientation of the convex polygon, prove that each opposite edge is oppositely directed and parallel:
\[
e_{i+n}=-\lambda_i e_i,\qquad \lambda_i>0,
\]
and introduce edge lengths/unit directions and turning angles
\[
e_i=\ell_i u_i,\qquad \ell_i>0,\quad \|u_i\|=1,
\]
with
\[
\theta_i\in(0,\pi/2),\qquad \sum_{i=1}^{2n}\theta_i=2\pi.
\]

declared prerequisite subclaims: none.

2. Subproof or Failure

Assume the listed vertices are taken in cyclic boundary order. If the order is clockwise, reverse the cyclic order and relabel. This preserves convexity, the condition \(e_i\parallel e_{i+n}\), and the adjacent positivity condition, since the new edges are negatives of old edges with adjacent indices reversed. Hence we may assume the polygon is oriented counterclockwise.

Because \(\mathcal P\) is a convex polygon with genuine vertices, every edge vector is nonzero. Write
\[
\ell_i=\|e_i\|>0,\qquad u_i=\frac{e_i}{\ell_i}.
\]
Thus \(e_i=\ell_i u_i\), where \(u_i\) is a unit vector.

For a counterclockwise convex polygon, the directed edge directions rotate monotonically counterclockwise once around the unit circle. Therefore there are unique exterior turning angles
\[
\theta_i\in(0,\pi)
\]
such that \(u_{i+1}\) is obtained from \(u_i\) by counterclockwise rotation through \(\theta_i\). The total turning around a convex polygon is one full turn, so
\[
\sum_{i=1}^{2n}\theta_i=2\pi.
\]

Now use the strict adjacent dot-product hypothesis. Since the angle from \(e_i\) to \(e_{i+1}\) is \(\theta_i\),
\[
\langle e_i,e_{i+1}\rangle
=\ell_i\ell_{i+1}\cos\theta_i.
\]
The lengths are positive and \(\langle e_i,e_{i+1}\rangle>0\), so \(\cos\theta_i>0\). Since already \(\theta_i\in(0,\pi)\), this gives
\[
\theta_i\in(0,\pi/2)
\]
for every \(i\).

It remains to prove the sign in the opposite-parallel relation. Fix \(i\). Let
\[
T_i=\theta_i+\theta_{i+1}+\cdots+\theta_{i+n-1},
\]
with indices read cyclically and with the lifted edge direction chosen continuously along the counterclockwise boundary. Since every \(\theta_j>0\) and the complementary sum is also positive,
\[
0<T_i<2\pi.
\]
The direction \(u_{i+n}\) is obtained from \(u_i\) by rotation through \(T_i\). But \(e_{i+n}\parallel e_i\), hence \(u_{i+n}\) is parallel to \(u_i\), so \(T_i\) is congruent to either \(0\) or \(\pi\) modulo \(2\pi\). The inequalities \(0<T_i<2\pi\) exclude \(0\) and \(2\pi\), leaving only
\[
T_i=\pi.
\]
Therefore
\[
u_{i+n}=-u_i.
\]
Consequently
\[
e_{i+n}=\ell_{i+n}u_{i+n}
=-\ell_{i+n}u_i
=-\frac{\ell_{i+n}}{\ell_i}e_i.
\]
Setting
\[
\lambda_i=\frac{\ell_{i+n}}{\ell_i}>0
\]
proves
\[
e_{i+n}=-\lambda_i e_i.
\]

Also, by polygon closure,
\[
\sum_{i=1}^{2n}e_i=0,
\]
so the paired form of the closure condition is
\[
\sum_{i=1}^{n}(e_i+e_{i+n})=0,
\]
equivalently
\[
\sum_{i=1}^{n}(1-\lambda_i)e_i=0.
\]

Thus SC1 is proved.

3. Solver Failure Output and Candidate Guidance

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

4. Local Source Ledger

claim_id: S1-L1  
proof_location: Section 2, first paragraph  
claim_or_fact_used: A convex polygon listed cyclically can be oriented counterclockwise by reversing the order if necessary; reversal preserves the stated parallelism and adjacent dot-product positivity.  
source_status: standard background fact / proved inside the current proof  
cited_label_or_name: cyclic orientation normalization  
exact_statement_used: Reversing cyclic order changes each edge to the negative of an old edge and reverses adjacency, so parallelism of opposite edges and positivity of adjacent dot products remain valid.  
hypotheses_or_conditions_needed: vertices are listed in cyclic boundary order; indices are modulo \(2n\).  
where_hypotheses_are_checked: target theorem notation and polygon convention.  
strength_used: only invariance of the local hypotheses under reversal.  
notes: If a final proof fixes the original labeling as already counterclockwise, this paragraph can be replaced by “assume the cyclic orientation is counterclockwise.”

claim_id: S1-L2  
proof_location: Section 2, edge decomposition paragraph  
claim_or_fact_used: Every nonzero edge vector has a positive length and a unit direction.  
source_status: standard background fact  
cited_label_or_name: vector normalization  
exact_statement_used: If \(e_i\neq 0\), then \(e_i=\|e_i\|(e_i/\|e_i\|)\), with \(\|e_i\|>0\).  
hypotheses_or_conditions_needed: \(P_i\neq P_{i+1}\).  
where_hypotheses_are_checked: genuine vertices of a convex polygon give nonzero edges.  
strength_used: defines \(\ell_i\) and \(u_i\).  
notes: none.

claim_id: S1-L3  
proof_location: Section 2, turning-angle paragraph  
claim_or_fact_used: Counterclockwise convex polygon total turning theorem.  
source_status: standard background fact  
cited_label_or_name: total turning theorem for convex polygons  
exact_statement_used: For a counterclockwise convex polygon with genuine vertices, consecutive edge directions turn by angles \(\theta_i\in(0,\pi)\), and \(\sum_i\theta_i=2\pi\).  
hypotheses_or_conditions_needed: convexity, counterclockwise cyclic order, genuine vertices.  
where_hypotheses_are_checked: orientation normalization and convex polygon assumption.  
strength_used: existence, positivity, and total sum of turning angles.  
notes: If collinear consecutive boundary points were allowed as “vertices,” strict positivity of \(\theta_i\) would need an added convention or reduction.

claim_id: S1-L4  
proof_location: Section 2, dot-product paragraph  
claim_or_fact_used: Dot product angle formula.  
source_status: standard background fact  
cited_label_or_name: Euclidean dot product formula  
exact_statement_used: If the angle between nonzero vectors \(a,b\) is \(\theta\), then \(\langle a,b\rangle=\|a\|\|b\|\cos\theta\).  
hypotheses_or_conditions_needed: nonzero adjacent edge vectors; \(\theta_i\in(0,\pi)\).  
where_hypotheses_are_checked: S1-L2 and S1-L3.  
strength_used: converts \(\langle e_i,e_{i+1}\rangle>0\) into \(\theta_i\in(0,\pi/2)\).  
notes: none.

claim_id: S1-L5  
proof_location: Section 2, opposite-parallel paragraph  
claim_or_fact_used: Opposite parallel edges are oppositely directed in the convex cyclic order.  
source_status: proved inside the current proof  
cited_label_or_name: opposite-parallel sign claim  
exact_statement_used: If \(e_i\parallel e_{i+n}\), then the cumulative turn \(T_i\) from \(e_i\) to \(e_{i+n}\) is \(\pi\), hence \(u_{i+n}=-u_i\).  
hypotheses_or_conditions_needed: \(e_i\parallel e_{i+n}\), positive turning angles, total turning \(2\pi\), and \(n<2n\).  
where_hypotheses_are_checked: target theorem and S1-L3.  
strength_used: proves \(e_{i+n}=-(\ell_{i+n}/\ell_i)e_i\).  
notes: This also gives \(T_i=\pi\) for every \(i\), a useful later normalization.

claim_id: S1-L6  
proof_location: Section 2, final paragraph  
claim_or_fact_used: Polygon closure.  
source_status: standard background fact  
cited_label_or_name: closed polygon edge-sum identity  
exact_statement_used: For cyclic vertices \(P_1,\dots,P_{2n}\), \(\sum_{i=1}^{2n}(P_{i+1}-P_i)=0\).  
hypotheses_or_conditions_needed: \(P_{2n+1}=P_1\).  
where_hypotheses_are_checked: indices are taken modulo \(2n\).  
strength_used: records \(\sum_{i=1}^n(1-\lambda_i)e_i=0\).  
notes: This closure identity is not needed to prove the sign of \(\lambda_i\), but is a harmless normalization consequence.

5. Interface Notes for S6

what this subproof establishes: After counterclockwise orientation, \(e_i=\ell_i u_i\) with \(\ell_i>0\), the exterior turns satisfy \(\theta_i\in(0,\pi/2)\) and \(\sum_i\theta_i=2\pi\), and opposite edges satisfy \(e_{i+n}=-\lambda_i e_i\), \(\lambda_i>0\).

what remains conditional: Later solvers must still derive the Wigner area formulas, quadratic decompositions, sharp inequality, and equality case.

failure_output_type: solved

candidate guidance sentence, if any: none

auxiliary lemma candidate, if any: none

notation introduced: \(\ell_i=\|e_i\|\), \(u_i=e_i/\ell_i\), \(\theta_i\), \(T_i=\sum_{k=0}^{n-1}\theta_{i+k}\), \(\lambda_i=\ell_{i+n}/\ell_i\).

risk points: The proof uses the standard convention that the listed points are genuine convex polygon vertices, not redundant collinear boundary points. Also, since all \(\theta_i<\pi/2\) and their sum is \(2\pi\), the hypotheses force \(n>2\); this matters for the final equality discussion because a regular square would have adjacent dot product \(0\), not \(>0\).

6. Web-Source Confirmation

no web sources used