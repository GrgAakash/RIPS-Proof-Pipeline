1. Assignment restatement

S-ID: S2

assigned subclaim(s): SC2

what must be proved: Starting from
\[
W_i=\frac{P_i+P_{i+n}}2,
\]
derive
\[
W_{i+1}-W_i=\frac12(e_i+e_{i+n}),
\]
and express the oriented Wigner-caustic area
\[
A^\ast(\mathrm E_{0.5}(\mathcal P))=\frac12\sum_{i=1}^{2n}\det(W_i,W_{i+1})
\]
as an explicit quadratic expression in edge variables.

declared prerequisite subclaims: None for the raw edge formula and area expansion. If the final proof wants the specialized form \(e_{i+n}=-\lambda_i e_i\), that specialization is conditional on SC1.

2. Subproof or failure

Let
\[
w_i:=W_{i+1}-W_i
\]
denote the edge vector of the Wigner polygon. Using only the definition of \(W_i\) and the edge definition \(e_i=P_{i+1}-P_i\), we compute
\[
\begin{aligned}
w_i
&=W_{i+1}-W_i \\
&=\frac{P_{i+1}+P_{i+n+1}}2-\frac{P_i+P_{i+n}}2\\
&=\frac{(P_{i+1}-P_i)+(P_{i+n+1}-P_{i+n})}{2}\\
&=\frac12(e_i+e_{i+n}).
\end{aligned}
\]
Thus
\[
\boxed{W_{i+1}-W_i=\frac12(e_i+e_{i+n}).}
\]

Also, because indices are modulo \(2n\),
\[
W_{i+n}=\frac{P_{i+n}+P_{i+2n}}2
=\frac{P_{i+n}+P_i}2
=W_i.
\]
Therefore the Wigner sequence has period \(n\), and \(w_{i+n}=w_i\). Consequently,
\[
\begin{aligned}
A^\ast(\mathrm E_{0.5}(\mathcal P))
&=\frac12\sum_{i=1}^{2n}\det(W_i,W_{i+1})\\
&=\sum_{i=1}^{n}\det(W_i,W_{i+1}).
\end{aligned}
\]
Equivalently, the target definition counts two traversals of the closed \(n\)-periodic Wigner polygon.

We now rewrite this in edge variables. For any closed polygon \(Q_1,\dots,Q_m\) with edge vectors \(q_i=Q_{i+1}-Q_i\), its oriented area is translation invariant. Translating so that \(Q_1=0\), one has
\[
Q_i=\sum_{j=1}^{i-1}q_j,
\]
and hence
\[
\frac12\sum_{i=1}^m\det(Q_i,Q_{i+1})
=\frac12\sum_{i=1}^m\det(Q_i,q_i)
=\frac12\sum_{1\le j<i\le m}\det(q_j,q_i).
\]

Apply this to the primitive Wigner polygon \(W_1,\dots,W_n\). Its ordinary oriented area over one traversal is
\[
B=\frac12\sum_{i=1}^n\det(W_i,W_{i+1})
=\frac12\sum_{1\le j<i\le n}\det(w_j,w_i).
\]
Since \(A^\ast\) uses two traversals,
\[
A^\ast(\mathrm E_{0.5}(\mathcal P))=2B
=\sum_{1\le j<i\le n}\det(w_j,w_i).
\]
Substituting \(w_i=\frac12(e_i+e_{i+n})\), we obtain
\[
\boxed{
A^\ast(\mathrm E_{0.5}(\mathcal P))
=\frac14\sum_{1\le j<i\le n}
\det(e_j+e_{j+n},\,e_i+e_{i+n})
}.
\]
Expanding by bilinearity of the determinant gives the fully expanded edge formula:
\[
\boxed{
A^\ast
=\frac14\sum_{1\le j<i\le n}
\Bigl[
\det(e_j,e_i)
+\det(e_j,e_{i+n})
+\det(e_{j+n},e_i)
+\det(e_{j+n},e_{i+n})
\Bigr].
}
\]

If SC1 is later supplied, so that \(e_{i+n}=-\lambda_i e_i\) with \(\lambda_i>0\), then the same formula specializes to
\[
w_i=\frac12(1-\lambda_i)e_i
\]
and
\[
\boxed{
A^\ast
=\frac14\sum_{1\le j<i\le n}
(1-\lambda_j)(1-\lambda_i)\det(e_j,e_i).
}
\]
Equivalently, if \(e_i=\ell_i u_i\), \(e_{i+n}=-\ell_{i+n}u_i\), and
\[
d_i=\frac{\ell_i-\ell_{i+n}}2,
\]
then
\[
\boxed{
A^\ast
=\sum_{1\le j<i\le n}d_jd_i\det(u_j,u_i).
}
\]

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

4. Local Source Ledger

claim_id: S2-L1  
proof_location: Section 2, first displayed computation.  
claim_or_fact_used: Definition of edge vectors.  
source_status: provided definition / notation / assumption.  
cited_label_or_name: Target theorem notation.  
exact_statement_used: \(e_i=P_{i+1}-P_i\).  
hypotheses_or_conditions_needed: Vertices indexed cyclically.  
where_hypotheses_are_checked: Given in target theorem.  
strength_used: Exact definition only.  
notes: Used to rewrite \(P_{i+1}-P_i\) and \(P_{i+n+1}-P_{i+n}\).

claim_id: S2-L2  
proof_location: Section 2, first displayed computation.  
claim_or_fact_used: Definition of Wigner vertices.  
source_status: provided definition / notation / assumption.  
cited_label_or_name: Target theorem notation.  
exact_statement_used: \(W_i=(P_i+P_{i+n})/2\).  
hypotheses_or_conditions_needed: Indices modulo \(2n\).  
where_hypotheses_are_checked: Given in target theorem.  
strength_used: Exact definition only.  
notes: Produces the Wigner edge formula.

claim_id: S2-L3  
proof_location: Section 2, paragraph proving \(W_{i+n}=W_i\).  
claim_or_fact_used: Cyclic indexing modulo \(2n\).  
source_status: provided definition / notation / assumption.  
cited_label_or_name: Target theorem indexing convention.  
exact_statement_used: \(P_{i+2n}=P_i\).  
hypotheses_or_conditions_needed: Indices taken modulo \(2n\).  
where_hypotheses_are_checked: Given in target theorem.  
strength_used: Exact convention only.  
notes: Shows the Wigner polygon is \(n\)-periodic.

claim_id: S2-L4  
proof_location: Section 2, area reduction to primitive Wigner polygon.  
claim_or_fact_used: Oriented area definition.  
source_status: provided definition / notation / assumption.  
cited_label_or_name: Target theorem definition of \(A^\ast\).  
exact_statement_used: \(A^\ast=\frac12\sum_{i=1}^{2n}\det(W_i,W_{i+1})\).  
hypotheses_or_conditions_needed: Wigner vertices indexed cyclically.  
where_hypotheses_are_checked: Given in target theorem and proved \(W_{i+n}=W_i\).  
strength_used: Exact definition only.  
notes: The factor of two is important because the \(2n\)-term Wigner sequence traverses an \(n\)-periodic polygon twice.

claim_id: S2-L5  
proof_location: Section 2, closed-polygon edge-area derivation.  
claim_or_fact_used: Translation invariance of oriented shoelace area for closed polygons.  
source_status: proved inside the current proof.  
cited_label_or_name: Translation invariance of determinant area.  
exact_statement_used: Translating every vertex of a closed polygon by a fixed vector does not change \(\frac12\sum_i\det(Q_i,Q_{i+1})\).  
hypotheses_or_conditions_needed: Closed cyclic polygon, so \(\sum_i(Q_{i+1}-Q_i)=0\).  
where_hypotheses_are_checked: The primitive Wigner polygon is closed because \(W_{n+1}=W_1\).  
strength_used: Only translation to set the first vertex equal to \(0\).  
notes: This is also a standard determinant-area fact, but it was proved directly.

claim_id: S2-L6  
proof_location: Section 2, derivation of \(\frac12\sum_{j<i}\det(q_j,q_i)\).  
claim_or_fact_used: Edge-sum representation of vertices after translation.  
source_status: proved inside the current proof.  
cited_label_or_name: Closed polygon edge-area formula.  
exact_statement_used: If \(Q_1=0\) and \(q_i=Q_{i+1}-Q_i\), then \(Q_i=\sum_{j=1}^{i-1}q_j\) and
\[
\frac12\sum_i\det(Q_i,Q_{i+1})
=\frac12\sum_{j<i}\det(q_j,q_i).
\]
hypotheses_or_conditions_needed: Vertices ordered cyclically; determinant bilinear and alternating.  
where_hypotheses_are_checked: Applied to \(W_1,\dots,W_n\), which is cyclic because \(W_{n+1}=W_1\).  
strength_used: Exact finite-sum identity.  
notes: No convexity is needed for this identity.

claim_id: S2-L7  
proof_location: Section 2, expansion of determinant.  
claim_or_fact_used: Bilinearity of determinant.  
source_status: standard background fact.  
cited_label_or_name: Bilinearity of the planar determinant.  
exact_statement_used: \(\det(a+b,c+d)=\det(a,c)+\det(a,d)+\det(b,c)+\det(b,d)\).  
hypotheses_or_conditions_needed: Vectors in the plane.  
where_hypotheses_are_checked: All \(e_i\) are planar edge vectors.  
strength_used: Exact algebraic identity.  
notes: Used to expand \(A^\ast\) into edge-pair determinant terms.

claim_id: S2-L8  
proof_location: Section 2, final conditional specialization.  
claim_or_fact_used: Substitution under opposite-edge reduction.  
source_status: proved inside the current proof.  
cited_label_or_name: Conditional SC1 specialization.  
exact_statement_used: If \(e_{i+n}=-\lambda_i e_i\), then \(e_i+e_{i+n}=(1-\lambda_i)e_i\).  
hypotheses_or_conditions_needed: SC1 supplies \(e_{i+n}=-\lambda_i e_i\).  
where_hypotheses_are_checked: Declared conditional on SC1, not proved in S2.  
strength_used: Pure substitution.  
notes: Not needed for the raw S2 formula, but useful for S3.

5. Interface notes for S6

what this subproof establishes: The Wigner edge vectors satisfy
\[
W_{i+1}-W_i=\frac12(e_i+e_{i+n}),
\]
and the oriented Wigner-caustic area is
\[
A^\ast
=\frac14\sum_{1\le j<i\le n}\det(e_j+e_{j+n},e_i+e_{i+n}).
\]

what remains conditional: The reduced forms involving \(\lambda_i\), \(\ell_i\), \(u_i\), or \(d_i\) require SC1 or equivalent opposite-edge normalization.

failure_output_type: solved

candidate guidance sentence, if any: null

auxiliary lemma candidate, if any: null

notation introduced: \(w_i=W_{i+1}-W_i\); optionally \(\Delta_i=e_i+e_{i+n}\) may be used later, with \(w_i=\Delta_i/2\).

risk points: The Wigner sequence is \(n\)-periodic, so the \(2n\)-vertex oriented area in the theorem counts two traversals of the primitive Wigner polygon. Missing this doubles or halves the final area expression.

6. Web-source confirmation

no web sources used