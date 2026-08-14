1. Assignment restatement

S-ID: S4

assigned subclaim(s): SC4

what must be proved: Prove the sharp quadratic estimate controlling the SC3 area expressions by
\[
L(\mathcal P)^2
\]
with constant
\[
8n\tan\left(\frac{\pi}{2n}\right).
\]
Equivalently, for the relevant quadratic form \(Q\) representing one of
\[
A(\mathcal P)+2A^\ast(\mathrm E_{0.5}(\mathcal P)),
\qquad
A(\mathcal P)-2A^\ast(\mathrm E_{0.5}(\mathcal P)),
\]
prove
\[
8n\tan\left(\frac{\pi}{2n}\right)Q\le L(\mathcal P)^2.
\]

declared prerequisite subclaims: SC1 and SC3. The exact SC3 quadratic forms are not supplied in the prompt.

2. Subproof or failure

SUBPROBLEM UNSOLVED.

The obstruction is stronger than a missing proof: the stated target inequality is false under the definitions in the prompt.

Take \(n=3\). Let
\[
u_1=(1,0),\quad
u_2=\left(\frac12,\frac{\sqrt3}{2}\right),\quad
u_3=\left(-\frac12,\frac{\sqrt3}{2}\right),
\]
and define the six edge vectors
\[
e_1=\frac32u_1,\quad
e_2=\frac12u_2,\quad
e_3=\frac32u_3,\quad
e_4=-\frac12u_1,\quad
e_5=-\frac32u_2,\quad
e_6=-\frac12u_3.
\]
They sum to zero because
\[
e_1+\cdots+e_6=u_1-u_2+u_3=0.
\]
The edge directions are
\[
0,\frac\pi3,\frac{2\pi}3,\pi,\frac{4\pi}3,\frac{5\pi}3,
\]
so the polygon is convex, each adjacent angle is \(\pi/3\), and therefore
\[
\langle e_i,e_{i+1}\rangle>0
\]
for every \(i\). Also \(e_i\parallel e_{i+3}\).

With \(P_1=(0,0)\), the vertices are
\[
P_1=(0,0),\quad
P_2=\left(\frac32,0\right),\quad
P_3=\left(\frac74,\frac{\sqrt3}{4}\right),
\]
\[
P_4=(1,\sqrt3),\quad
P_5=\left(\frac12,\sqrt3\right),\quad
P_6=\left(-\frac14,\frac{\sqrt3}{4}\right).
\]
The perimeter is
\[
L= \frac32+\frac12+\frac32+\frac12+\frac32+\frac12=6.
\]

Using the determinant area formula,
\[
A(\mathcal P)=\frac12\sum_{i=1}^6\det(P_i,P_{i+1})=\frac{11\sqrt3}{8}.
\]

The Wigner vertices are
\[
W_1=\frac{P_1+P_4}{2}=\left(\frac12,\frac{\sqrt3}{2}\right),
\quad
W_2=\frac{P_2+P_5}{2}=\left(1,\frac{\sqrt3}{2}\right),
\]
\[
W_3=\frac{P_3+P_6}{2}=\left(\frac34,\frac{\sqrt3}{4}\right),
\]
and \(W_4=W_1\), \(W_5=W_2\), \(W_6=W_3\). Hence
\[
A^\ast(\mathrm E_{0.5}(\mathcal P))
=
\frac12\sum_{i=1}^6\det(W_i,W_{i+1})
=
-\frac{\sqrt3}{8}.
\]
Therefore
\[
A(\mathcal P)+2|A^\ast(\mathrm E_{0.5}(\mathcal P))|
=
\frac{11\sqrt3}{8}+2\cdot\frac{\sqrt3}{8}
=
\frac{13\sqrt3}{8}.
\]
Since
\[
8n\tan\left(\frac{\pi}{2n}\right)
=
24\tan\left(\frac\pi6\right)
=
\frac{24}{\sqrt3}
=
8\sqrt3,
\]
the claimed inequality would require
\[
36=L^2\ge 8\sqrt3\cdot\frac{13\sqrt3}{8}=39,
\]
which is false.

Thus SC4 cannot be proved as stated.

3. Solver failure output and candidate guidance

```yaml
failure_output_type: forbidden-route / obstruction guidance
type: counterexample
failed_route: "Attempting to prove SC4 as stated."
obstruction: "The stated inequality is false for a convex hexagon satisfying all listed hypotheses."
evidence: "For n=3 with edges (3/2)u1, (1/2)u2, (3/2)u3, -(1/2)u1, -(3/2)u2, -(1/2)u3, where u1=(1,0), u2=(1/2,sqrt(3)/2), u3=(-1/2,sqrt(3)/2), one gets L^2=36 but 8n tan(pi/(2n))(A+2|A*|)=39."
reuse_value: "This counterexample blocks SC4 and the target theorem under the prompt's Wigner area convention."
guidance_sentence: "Do not attempt to prove SC4 with the stated coefficient 2 in front of |A*| and the 2n-vertex oriented Wigner area definition; the theorem needs a corrected hypothesis, constant, coefficient, or area convention."
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

claim_id: C1  
proof_location: Section 2, construction of the hexagon.  
claim_or_fact_used: The displayed edge vectors close to form a polygon.  
source_status: proved inside the current proof.  
cited_label_or_name: vector closure computation.  
exact_statement_used: \(e_1+\cdots+e_6=u_1-u_2+u_3=0\).  
hypotheses_or_conditions_needed: Definitions of \(u_1,u_2,u_3\).  
where_hypotheses_are_checked: Section 2.  
strength_used: Exact closure.  
notes: This verifies the constructed edge chain returns to its starting point.

claim_id: C2  
proof_location: Section 2, hypothesis verification.  
claim_or_fact_used: The polygon is convex because its positive edge vectors have strictly cyclic directions \(0,\pi/3,2\pi/3,\pi,4\pi/3,5\pi/3\).  
source_status: standard background fact.  
cited_label_or_name: cyclic edge-direction convexity criterion.  
exact_statement_used: A closed polygon whose positive edge vectors have arguments strictly increasing through one full turn and whose exterior turns lie in \((0,\pi)\) is convex.  
hypotheses_or_conditions_needed: Positive edge lengths, closed chain, cyclic edge directions.  
where_hypotheses_are_checked: Section 2.  
strength_used: Convexity of this explicit hexagon.  
notes: The exterior turns are all \(\pi/3\).

claim_id: C3  
proof_location: Section 2, dot-product check.  
claim_or_fact_used: Adjacent edge vectors making angle \(\pi/3\) have positive dot product.  
source_status: standard background fact.  
cited_label_or_name: dot product angle formula.  
exact_statement_used: \(\langle a,b\rangle=|a||b|\cos\theta\), and \(\cos(\pi/3)>0\).  
hypotheses_or_conditions_needed: Adjacent directions differ by \(\pi/3\), lengths positive.  
where_hypotheses_are_checked: Section 2.  
strength_used: Positivity for all adjacent pairs.  
notes: Includes the cyclic pair \(e_6,e_1\).

claim_id: C4  
proof_location: Section 2, area computation for \(\mathcal P\).  
claim_or_fact_used: Shoelace/determinant area formula.  
source_status: standard background fact.  
cited_label_or_name: polygon determinant area formula.  
exact_statement_used: For a counterclockwise polygon, \(A=\frac12\sum_i\det(P_i,P_{i+1})\).  
hypotheses_or_conditions_needed: Vertices listed in cyclic order.  
where_hypotheses_are_checked: Section 2 by construction and convexity verification.  
strength_used: Exact area \(11\sqrt3/8\).  
notes: This formula is also part of the target theorem’s notation for oriented areas.

claim_id: C5  
proof_location: Section 2, Wigner vertex computation.  
claim_or_fact_used: Definition of Wigner vertices.  
source_status: provided definition / notation / assumption.  
cited_label_or_name: target theorem definition of \(W_i\).  
exact_statement_used: \(W_i=(P_i+P_{i+n})/2\), here \(n=3\).  
hypotheses_or_conditions_needed: Listed vertices \(P_i\).  
where_hypotheses_are_checked: Section 2.  
strength_used: Exact Wigner vertices \(W_1,W_2,W_3\) and repetition.  
notes: No external Wigner caustic fact is used.

claim_id: C6  
proof_location: Section 2, Wigner oriented area computation.  
claim_or_fact_used: Definition of \(A^\ast(\mathrm E_{0.5}(\mathcal P))\).  
source_status: provided definition / notation / assumption.  
cited_label_or_name: target theorem definition of oriented Wigner area.  
exact_statement_used: \(A^\ast=\frac12\sum_{i=1}^{2n}\det(W_i,W_{i+1})\).  
hypotheses_or_conditions_needed: Computed \(W_i\).  
where_hypotheses_are_checked: Section 2.  
strength_used: Exact value \(-\sqrt3/8\).  
notes: The repeated Wigner triangle is counted according to the prompt’s \(2n\)-term definition.

claim_id: C7  
proof_location: Section 2, contradiction calculation.  
claim_or_fact_used: Elementary trigonometric value.  
source_status: standard background fact.  
cited_label_or_name: special-angle tangent value.  
exact_statement_used: \(\tan(\pi/6)=1/\sqrt3\).  
hypotheses_or_conditions_needed: \(n=3\).  
where_hypotheses_are_checked: Section 2.  
strength_used: Exact constant \(8n\tan(\pi/(2n))=8\sqrt3\).  
notes: Used to compute the claimed RHS.

claim_id: C8  
proof_location: Section 2, final inequality comparison.  
claim_or_fact_used: Arithmetic comparison.  
source_status: proved inside the current proof.  
cited_label_or_name: explicit numerical contradiction.  
exact_statement_used: \(36<39\).  
hypotheses_or_conditions_needed: Values \(L^2=36\) and RHS \(=39\).  
where_hypotheses_are_checked: Section 2.  
strength_used: Direct falsification of the claimed inequality.  
notes: This blocks SC4 as stated.

5. Interface notes for S6

what this subproof establishes: SC4 is false as stated; the target theorem is also false under the prompt’s definitions.

what remains conditional: Nothing in SC4 can be salvaged without changing some theorem data, such as the coefficient of \(|A^\ast|\), the Wigner area convention, the constant, or adding an extra hypothesis.

failure_output_type: forbidden-route / obstruction guidance

candidate guidance sentence, if any: Do not attempt to prove SC4 with the stated coefficient 2 and the prompt’s \(2n\)-term oriented Wigner area definition; the explicit convex hexagon above violates the bound.

auxiliary lemma candidate, if any: None.

notation introduced: \(u_1,u_2,u_3\), explicit hexagon vertices \(P_1,\dots,P_6\), and Wigner vertices \(W_1,\dots,W_6\).

risk points: The counterexample relies on using the Wigner area exactly as defined in the prompt, including the repeated \(2n\)-vertex Wigner polygon. If a different convention counts only the distinct Wigner loop once, the numerical obstruction changes.

6. Web-source confirmation

no web sources used