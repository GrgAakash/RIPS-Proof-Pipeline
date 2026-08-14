1. Assignment restatement

S-ID: S3

assigned subclaim(s): SC3

what must be proved: Derive exact formulas for
\[
A(\mathcal P)+2A^\ast(\mathrm E_{0.5}(\mathcal P)),\qquad
A(\mathcal P)-2A^\ast(\mathrm E_{0.5}(\mathcal P))
\]
in paired symmetric/antisymmetric edge variables, and reduce
\[
A(\mathcal P)+2|A^\ast|
\]
to the maximum of these two quantities.

declared prerequisite subclaims: SC1 for the paired opposite-edge parametrization. SC2 is not needed as an external premise beyond the definition of \(W_i\), since the Wigner edge identity is rederived below.

2. Subproof or failure

Assume the polygon has been oriented counterclockwise. By the declared SC1 prerequisite, for \(i=1,\dots,n\) we may write
\[
e_i=\ell_i u_i,\qquad e_{i+n}=-\ell_{i+n}u_i,
\]
where \(\ell_i,\ell_{i+n}>0\), and \(u_i\) are the first \(n\) cyclic edge directions. Define
\[
s_i=\frac{\ell_i+\ell_{i+n}}2,\qquad d_i=\frac{\ell_i-\ell_{i+n}}2,
\]
and vector variables
\[
X_i=s_i u_i,\qquad Y_i=d_i u_i.
\]
Then
\[
e_i=X_i+Y_i,\qquad e_{i+n}=Y_i-X_i.
\]
Closure gives
\[
0=\sum_{i=1}^{2n}e_i=\sum_{i=1}^n(e_i+e_{i+n})=2\sum_{i=1}^nY_i,
\]
so
\[
\sum_{i=1}^nY_i=0.
\]

For any closed polygonal chain with edge vectors \(g_1,\dots,g_m\), its oriented area is
\[
\frac12\sum_{1\le i<j\le m}\det(g_i,g_j).
\]
Apply this first to \(\mathcal P\), whose edge sequence is
\[
X_1+Y_1,\dots,X_n+Y_n,\;Y_1-X_1,\dots,Y_n-X_n.
\]
Let
\[
B_X=\sum_{1\le i<j\le n}\det(X_i,X_j),\qquad
B_Y=\sum_{1\le i<j\le n}\det(Y_i,Y_j).
\]
The cross block contributes
\[
\sum_{i,j=1}^n\det(X_i+Y_i,Y_j-X_j)
=
\det\left(\sum_i(X_i+Y_i),\sum_j(Y_j-X_j)\right)=0,
\]
because the two half-sums are negatives by closure. Also, for each \(i<j\),
\[
\det(X_i+Y_i,X_j+Y_j)+\det(Y_i-X_i,Y_j-X_j)
=
2\det(X_i,X_j)+2\det(Y_i,Y_j).
\]
Therefore
\[
A(\mathcal P)=B_X+B_Y.
\]

Now compute the Wigner area. From
\[
W_i=\frac{P_i+P_{i+n}}2
\]
we get
\[
W_{i+1}-W_i=\frac12(e_i+e_{i+n})=Y_i
\]
for \(i=1,\dots,n\), and similarly \(W_{i+n+1}-W_{i+n}=Y_i\). Thus the Wigner edge sequence is
\[
Y_1,\dots,Y_n,Y_1,\dots,Y_n.
\]
Using the same edge-area formula,
\[
A^\ast(\mathrm E_{0.5}(\mathcal P))
=
\frac12\left(
B_Y+\sum_{i,j=1}^n\det(Y_i,Y_j)+B_Y
\right).
\]
Since
\[
\sum_{i,j=1}^n\det(Y_i,Y_j)=\det\left(\sum_iY_i,\sum_jY_j\right)=0,
\]
we obtain
\[
A^\ast(\mathrm E_{0.5}(\mathcal P))=B_Y.
\]

Hence
\[
A(\mathcal P)+2A^\ast(\mathrm E_{0.5}(\mathcal P))
=
B_X+3B_Y,
\]
and
\[
A(\mathcal P)-2A^\ast(\mathrm E_{0.5}(\mathcal P))
=
B_X-B_Y.
\]

Equivalently, if
\[
\Delta_{ij}:=\det(u_i,u_j)\qquad(1\le i<j\le n),
\]
then
\[
B_X=\sum_{1\le i<j\le n}s_is_j\Delta_{ij},\qquad
B_Y=\sum_{1\le i<j\le n}d_id_j\Delta_{ij},
\]
so the exact scalar formulas are
\[
A(\mathcal P)+2A^\ast
=
\sum_{1\le i<j\le n}(s_is_j+3d_id_j)\Delta_{ij},
\]
and
\[
A(\mathcal P)-2A^\ast
=
\sum_{1\le i<j\le n}(s_is_j-d_id_j)\Delta_{ij}.
\]
In original paired lengths,
\[
A(\mathcal P)=\frac12\sum_{i<j}(\ell_i\ell_j+\ell_{i+n}\ell_{j+n})\Delta_{ij},
\]
\[
A^\ast=\frac14\sum_{i<j}(\ell_i-\ell_{i+n})(\ell_j-\ell_{j+n})\Delta_{ij},
\]
and
\[
A(\mathcal P)-2A^\ast
=
\frac12\sum_{i<j}(\ell_i\ell_{j+n}+\ell_{i+n}\ell_j)\Delta_{ij}.
\]

Finally, for any real number \(T\),
\[
B+2|T|=\max\{B+2T,B-2T\}.
\]
With \(B=A(\mathcal P)\) and \(T=A^\ast(\mathrm E_{0.5}(\mathcal P))\), this gives the exact reduction
\[
A(\mathcal P)+2|A^\ast|
=
\max\{B_X+3B_Y,\;B_X-B_Y\}.
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

claim_id: L1  
proof_location: Section 2, first paragraph  
claim_or_fact_used: Opposite-edge parametrization  
source_status: declared prerequisite subclaim  
cited_label_or_name: SC1  
exact_statement_used: After counterclockwise orientation, \(e_i=\ell_i u_i\) and \(e_{i+n}=-\ell_{i+n}u_i\) with positive lengths.  
hypotheses_or_conditions_needed: Convexity and opposite parallelism.  
where_hypotheses_are_checked: Delegated to SC1.  
strength_used: Only paired edge representation.  
notes: No equality or angle conclusions from SC1 are used.

claim_id: L2  
proof_location: Section 2, closure computation  
claim_or_fact_used: Closure of polygon edge vectors  
source_status: standard background fact  
cited_label_or_name: closed polygon edge sum  
exact_statement_used: For a closed polygon, \(\sum e_i=0\).  
hypotheses_or_conditions_needed: \(P_{2n+1}=P_1\).  
where_hypotheses_are_checked: Target theorem uses cyclic polygon vertices.  
strength_used: Used to prove \(\sum_iY_i=0\).  
notes: Elementary telescoping sum.

claim_id: L3  
proof_location: Section 2, area formula paragraph  
claim_or_fact_used: Edge-vector oriented area formula  
source_status: standard background fact  
cited_label_or_name: determinant edge-area formula  
exact_statement_used: For a closed polygonal chain with ordered edge vectors \(g_1,\dots,g_m\), oriented area equals \(\frac12\sum_{i<j}\det(g_i,g_j)\).  
hypotheses_or_conditions_needed: Closed polygonal chain.  
where_hypotheses_are_checked: Applied to \(\mathcal P\) and to the closed Wigner chain.  
strength_used: Exact formula.  
notes: Follows by translating the initial vertex to \(0\) and expanding \(Q_i=\sum_{r<i}g_r\).

claim_id: L4  
proof_location: Section 2, block expansion  
claim_or_fact_used: Bilinearity and alternating property of determinant  
source_status: standard background fact  
cited_label_or_name: determinant algebra  
exact_statement_used: \(\det(a+b,c+d)\) expands bilinearly and \(\det(v,v)=0\).  
hypotheses_or_conditions_needed: Planar vectors.  
where_hypotheses_are_checked: All edge variables are planar vectors.  
strength_used: Exact algebraic expansion.  
notes: Used in area decomposition.

claim_id: L5  
proof_location: Section 2, cross-block computation  
claim_or_fact_used: Double-sum determinant identity  
source_status: proved inside the current proof  
cited_label_or_name: none  
exact_statement_used: \(\sum_{i,j}\det(v_i,w_j)=\det(\sum_i v_i,\sum_j w_j)\).  
hypotheses_or_conditions_needed: Finite vector families.  
where_hypotheses_are_checked: The sums are finite over \(1,\dots,n\).  
strength_used: Exact identity.  
notes: Immediate from bilinearity.

claim_id: L6  
proof_location: Section 2, Wigner edge computation  
claim_or_fact_used: Wigner edge formula  
source_status: proved inside the current proof  
cited_label_or_name: none  
exact_statement_used: \(W_{i+1}-W_i=\frac12(e_i+e_{i+n})=Y_i\).  
hypotheses_or_conditions_needed: \(W_i=(P_i+P_{i+n})/2\).  
where_hypotheses_are_checked: This is the target theorem’s definition of Wigner vertices.  
strength_used: Exact edge identity.  
notes: Reproves the needed part of SC2.

claim_id: L7  
proof_location: Section 2, final absolute-value paragraph  
claim_or_fact_used: Absolute value maximum identity  
source_status: standard background fact  
cited_label_or_name: elementary real identity  
exact_statement_used: For real \(B,T\), \(B+2|T|=\max\{B+2T,B-2T\}\).  
hypotheses_or_conditions_needed: \(B,T\in\mathbb R\).  
where_hypotheses_are_checked: \(A\) and \(A^\ast\) are real-valued areas.  
strength_used: Exact identity.  
notes: This is the requested absolute-value reduction.

5. Interface notes for S6

what this subproof establishes: Conditional on SC1’s paired-edge normalization,
\[
A=B_X+B_Y,\qquad A^\ast=B_Y,
\]
hence
\[
A+2A^\ast=B_X+3B_Y,\qquad A-2A^\ast=B_X-B_Y,
\]
with
\[
B_X=\sum_{i<j}s_is_j\det(u_i,u_j),\qquad
B_Y=\sum_{i<j}d_id_j\det(u_i,u_j).
\]

what remains conditional: SC1’s normalization and all sharp estimates/equality analysis in S4-S5.

failure_output_type: solved

candidate guidance sentence, if any: null

auxiliary lemma candidate, if any: null

notation introduced: \(s_i,d_i,X_i,Y_i,\Delta_{ij},B_X,B_Y\).

risk points: The formula for \(A+2A^\ast\) is exact but not termwise positive in the \(d_i\). S4 should not treat \(d_i\) as arbitrary independent variables without also using the closure constraint \(\sum_i d_i u_i=0\) and the length constraints inherited from \(\ell_i,\ell_{i+n}>0\).

6. Web-source confirmation

no web sources used