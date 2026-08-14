1. Assignment restatement

S-ID: SS2  
work_scope: assigned_subclaim  
assigned subclaim(s): SC6, SC7, SC8  
what must be proved: convexity/acyclicity of endpoint-incidence fibers, acyclicity of the endpoint-incidence component attached to an oriented transversal component, and acyclicity transfer from that incidence component to the oriented line component, including open noncompact cases.  
connection to the exact target: this is the technical engine needed for fixed-order oriented components before the final unoriented quotient step.  
inferred_standard_setup_for_this_assignment: use the oriented line model \(\widetilde{\mathcal L}_d=\{(u,p):u\in S^{d-1},p\in u^\perp\}\), with line \(p+\mathbb R u\). For an open convex set \(C\), \(I_C(u,p)=\{t:p+tu\in C\}\) is an open interval, possibly unbounded. For pairwise disjoint sets met by the same oriented line, the nonempty intervals \(I_C\) are disjoint and hence have a definite order.  
where this result is used in the final solution: S6 may use the established SC6 and SC8 lemmas directly; SC7 remains the missing branch lemma identified below.  
declared prerequisite subclaims: none assumed as mathematical facts.

2. Subproof or failure

SUBPROBLEM UNSOLVED: SC6 and SC8 are established below. SC7, the acyclicity of every endpoint-incidence component, is reduced to a clean standalone branch lemma but is not proved from the allowed inputs here. The obstruction is that convexity of the single-endpoint fibers alone does not force the total incidence component to be acyclic.

Lemma 1, line intervals and canonical endpoint selection.  
Let \(C\subset \mathbb R^d\) be open convex. For an oriented line \(\ell=(u,p)\), \(I_C(\ell)=\{t:p+tu\in C\}\) is an open convex subset of \(\mathbb R\), hence an open interval, ray, all of \(\mathbb R\), or empty. On the domain where \(I_C(\ell)\neq\emptyset\), write \(I_C(\ell)=(\alpha(\ell),\beta(\ell))\) with endpoints in \([-\infty,\infty]\). Define
\[
\tau_C(\ell)=\tan\left(\frac{\arctan(\alpha(\ell))+\arctan(\beta(\ell))}{2}\right),
\]
where \(\arctan(\pm\infty)=\pm\pi/2\). Then \(\tau_C(\ell)\in I_C(\ell)\), and \(\tau_C\) is continuous.

Proof. Convexity and openness of \(I_C(\ell)\) are immediate from convexity and openness of \(C\). If \(\ell_m\to \ell\) and \(I_C(\ell)\neq\emptyset\), then points strictly inside \(I_C(\ell)\) remain inside \(I_C(\ell_m)\) eventually by openness. Points outside \(\overline{I_C(\ell)}\) correspond to points outside \(\overline C\), using \(\overline{C\cap \ell}=\overline C\cap \ell\) when \(C\cap\ell\neq\emptyset\); they remain outside eventually. Since the \(I_C(\ell_m)\) are intervals, this forces extended endpoint convergence \(\alpha(\ell_m)\to\alpha(\ell)\), \(\beta(\ell_m)\to\beta(\ell)\). The displayed arctangent formula is continuous in those extended endpoints and gives a point strictly between them.

Lemma 2, pointed cone fibers.  
Fix \(x\in\mathbb R^d\), and let \(K\subset\mathbb R^d\) be open convex. The pointed beyond-cone
\[
\operatorname{Cone}^+_x(K)=\{x+r(z-x):z\in K,\ r>1\}
\]
is open and convex. If nonempty, it is contractible.

Proof. It is a union of open homothetic copies \(x+r(K-x)\), so it is open. If \(y_a=x+r_a(z_a-x)\) and \(y_b=x+r_b(z_b-x)\), then for \(0\le\theta\le1\),
\[
(1-\theta)y_a+\theta y_b
=x+r_\theta(z_\theta-x),
\]
where \(r_\theta=(1-\theta)r_a+\theta r_b>1\) and
\[
z_\theta=\frac{(1-\theta)r_a z_a+\theta r_b z_b}{r_\theta}\in K.
\]
Thus the cone is convex, hence contractible when nonempty.

Lemma 3, ordered endpoint fibers.  
Let \(C_1,\dots,C_n\) be pairwise disjoint open convex sets, ordered as written, and fix \(x\in C_1\). Define
\[
F_x=\{y\in C_n:\exists\,0<\lambda_2<\cdots<\lambda_{n-1}<1
\text{ with }(1-\lambda_i)x+\lambda_i y\in C_i\}.
\]
For \(n=2\), set \(F_x=C_2\). For every \(n\ge2\), \(F_x\) is open and convex; hence each nonempty \(F_x\) is acyclic.

Proof. Openness follows by keeping the same strict parameters \(\lambda_i\) and using openness of the \(C_i\). For convexity, write \(r_i=1/\lambda_i\), so \(r_2>\cdots>r_{n-1}>1\), and witnesses have the form \(y=x+r_i(z_i-x)\) with \(z_i\in C_i\). Given two points \(y_a,y_b\in F_x\), choose witnesses \(r_{i,a},z_{i,a}\) and \(r_{i,b},z_{i,b}\). For \(y_\theta=(1-\theta)y_a+\theta y_b\), set
\[
r_{i,\theta}=(1-\theta)r_{i,a}+\theta r_{i,b},
\quad
z_{i,\theta}=\frac{(1-\theta)r_{i,a}z_{i,a}+\theta r_{i,b}z_{i,b}}{r_{i,\theta}}.
\]
Then \(z_{i,\theta}\in C_i\), the strict inequalities among the \(r_i\)'s are preserved, and \(y_\theta=x+r_{i,\theta}(z_{i,\theta}-x)\). Also \(y_\theta\in C_n\) by convexity. Thus \(F_x\) is convex.

Lemma 4, endpoint-to-line transfer for open noncompact sets.  
Let \(U\) be any connected component of an oriented fixed-order transversal space for \(C_1,\dots,C_n\), ordered so that \(C_1\) is first and \(C_n\) is last. Define
\[
E_U=\{(\ell,a,b):\ell\in U,\ a\in I_{C_1}(\ell),\ b\in I_{C_n}(\ell)\}.
\]
The projection \(q:E_U\to U\), \(q(\ell,a,b)=\ell\), is a homotopy equivalence. Therefore \(q\) induces isomorphisms on ordinary and reduced singular homology. In particular, if \(E_U\) is acyclic, then \(U\) is acyclic.

Proof. By Lemma 1, \(\tau_{C_1}\) and \(\tau_{C_n}\) are continuous on \(U\). The map
\[
s(\ell)=(\ell,\tau_{C_1}(\ell),\tau_{C_n}(\ell))
\]
is a continuous section of \(q\). Each fiber \(q^{-1}(\ell)=I_{C_1}(\ell)\times I_{C_n}(\ell)\) is convex, including in unbounded cases. The homotopy
\[
H_r(\ell,a,b)=\bigl(\ell,(1-r)a+r\tau_{C_1}(\ell),(1-r)b+r\tau_{C_n}(\ell)\bigr)
\]
stays inside the same fiber for \(0\le r\le1\). Hence \(E_U\) deformation retracts onto \(s(U)\cong U\). No compactness, properness, or Vietoris-Begle theorem is used.

Reduction and remaining SC7 gap.  
For an order \(C_1,\dots,C_n\), define the endpoint-pair incidence space
\[
P=\{(x,y)\in C_1\times C_n:\exists\,0<\lambda_2<\cdots<\lambda_{n-1}<1,\ 
(1-\lambda_i)x+\lambda_i y\in C_i\}.
\]
For a line component \(U\), the relevant component \(P_U\) is homeomorphic to \(E_U\) by sending \((\ell,a,b)\) to the two endpoint points on \(\ell\). Lemma 4 shows that \(P_U\) and \(U\) have the same homotopy type. Thus SC7 would follow from the branch lemma: every connected component of \(P\) is acyclic.

The attempted route “project \(P\) to the first endpoint and use convex fibers” is insufficient by itself. Lemma 3 proves those fibers are convex, but convex fibers over an arbitrary open image do not imply acyclicity of the total space. For example, \(X=A\times(0,1)\subset\mathbb R^2\times\mathbb R\), where \(A=\{b\in\mathbb R^2:1<\|b\|<2\}\), has open convex fibers over \(\mathbb R^2\), but \(X\) deformation retracts to an annulus and has nontrivial \(H_1\). Therefore the missing ingredient is a proof that the actual endpoint-incidence components \(P_U\), not merely their point-fibers, are acyclic.

3. Solver failure output and candidate guidance

```yaml
failure_output_type: branch lemma target
type: unresolved key lemma
failed_route: "Projecting endpoint incidence to the first endpoint and using only convexity of the fibers."
obstruction: "Convex fibers alone do not force the total endpoint-incidence component to be acyclic; the projection image/component must also be controlled by additional geometry."
evidence: "The space A x (0,1), with A an open annulus in R^2, has open convex fibers over R^2 but has nontrivial H_1."
reuse_value: "SC6 is proved for pointed cones and ordered single-endpoint fibers; SC8 is proved by an explicit deformation retract, including unbounded open intervals."
guidance_sentence: "Prove endpoint-pair incidence component acyclicity directly; do not infer it from single-endpoint convex fibers unless the projection image component is also proved acyclic."
candidate_lemma_statement: "Let C_1,...,C_n be pairwise disjoint open convex subsets of R^d and fix the displayed order. Let P be the set of endpoint pairs (x,y) in C_1 x C_n for which the open segment from x to y meets C_2,...,C_{n-1} in that order. Then every connected component of P is acyclic for ordinary reduced homology."
why_unblocks: "By the endpoint-to-line deformation retract proved here, the corresponding oriented fixed-order line component has the same homotopy type as its endpoint-incidence component."
where_used: "SC7 and then TDC-2/TDC-3 in S6's final assembly."
allowed_inputs: "Target definitions, elementary convexity, ordinary singular homology, basic topology of oriented affine line space."
dependencies: "Use Lemma 3 for fiber convexity and Lemma 4 for the endpoint-to-line homotopy equivalence."
weaker_than_target: true
equivalent_or_stronger: "Equivalent to the unresolved endpoint-incidence core for fixed-order oriented components after SC8; weaker than the full unoriented target theorem."
recommended: true
```

4. Local Source Ledger, including TDC reports and Unknowns addendum

claim_id: L1  
proof_location: Section 2, inferred setup and Lemma 1  
claim_or_fact_used: intersection of an affine line with an open convex set is an open interval, ray, all of \(\mathbb R\), or empty  
source_status: standard background fact  
cited_label_or_name: convex subsets of \(\mathbb R\) are intervals  
exact_statement_used: nonempty open convex subsets of \(\mathbb R\) are open intervals, possibly unbounded  
hypotheses_or_conditions_needed: \(C\) open convex; affine line parameterized continuously  
where_hypotheses_are_checked: target assumptions and oriented setup  
strength_used: exact  
notes: no transversal theorem used

claim_id: L2  
proof_location: Lemma 1  
claim_or_fact_used: canonical selector \(\tau_C\) is continuous for line intersections with open convex \(C\)  
source_status: proved inside the current proof  
cited_label_or_name: arctangent midpoint selector  
exact_statement_used: extended endpoints of \(I_C(\ell)\) vary continuously on the nonempty-intersection domain, and the arctangent midpoint lies inside the interval  
hypotheses_or_conditions_needed: \(C\) open convex; \(I_C(\ell)\neq\emptyset\)  
where_hypotheses_are_checked: Lemma 1  
strength_used: exact  
notes: handles unbounded and whole-line intervals

claim_id: L3  
proof_location: Lemma 2  
claim_or_fact_used: pointed beyond-cones through open convex sets are open convex  
source_status: proved inside the current proof  
cited_label_or_name: pointed cone convexity  
exact_statement_used: \(\operatorname{Cone}^+_x(K)=\{x+r(z-x):z\in K,r>1\}\) is open convex  
hypotheses_or_conditions_needed: \(K\) open convex  
where_hypotheses_are_checked: Lemma 2  
strength_used: exact  
notes: supplies SC6 cone-fiber part

claim_id: L4  
proof_location: Lemma 3  
claim_or_fact_used: ordered endpoint fibers \(F_x\) are open convex  
source_status: proved inside the current proof  
cited_label_or_name: ordered endpoint fiber convexity  
exact_statement_used: for fixed \(x\in C_1\), the set of \(y\in C_n\) whose segment from \(x\) meets the intermediate \(C_i\)'s in order is open convex  
hypotheses_or_conditions_needed: \(C_i\) open convex; order encoded by strict parameters  
where_hypotheses_are_checked: Lemma 3  
strength_used: exact  
notes: supplies SC6 single-endpoint fiber part

claim_id: L5  
proof_location: Lemma 4  
claim_or_fact_used: endpoint-to-line incidence projection is a homotopy equivalence  
source_status: proved inside the current proof  
cited_label_or_name: endpoint-to-line deformation retract  
exact_statement_used: \(E_U\to U\) deformation retracts along convex interval-product fibers using \(\tau_{C_1},\tau_{C_n}\)  
hypotheses_or_conditions_needed: \(U\) fixed-order oriented line component; first and last intersections nonempty open intervals  
where_hypotheses_are_checked: Lemma 4  
strength_used: exact  
notes: proves SC8 and resolves the open/noncompact transfer issue for this map

claim_id: L6  
proof_location: Lemmas 2-4  
claim_or_fact_used: nonempty convex subsets of Euclidean space are contractible and hence acyclic  
source_status: standard background fact  
cited_label_or_name: straight-line contraction of convex sets  
exact_statement_used: \(H_t(x)=(1-t)x+tx_0\) contracts a convex set to \(x_0\)  
hypotheses_or_conditions_needed: nonempty convex set  
where_hypotheses_are_checked: Lemmas 2 and 3  
strength_used: exact  
notes: ordinary reduced homology acyclicity follows

claim_id: L7  
proof_location: Lemma 4  
claim_or_fact_used: homotopy equivalence induces isomorphism on ordinary and reduced singular homology  
source_status: standard background fact  
cited_label_or_name: homotopy invariance of singular homology  
exact_statement_used: deformation retracts induce homology isomorphisms  
hypotheses_or_conditions_needed: topological spaces; ordinary singular homology  
where_hypotheses_are_checked: Lemma 4  
strength_used: exact  
notes: no proper-map theorem used

claim_id: L8  
proof_location: Section 2, final paragraph  
claim_or_fact_used: convex-fiber projection alone does not imply total acyclicity  
source_status: proved inside the current proof  
cited_label_or_name: annulus times interval obstruction  
exact_statement_used: \(A\times(0,1)\), with \(A\) an open annulus, has convex vertical fibers but nontrivial \(H_1\)  
hypotheses_or_conditions_needed: standard homotopy type of annulus  
where_hypotheses_are_checked: explicit construction  
strength_used: obstruction only  
notes: explains why SC7 remains open

TDC report:

claim_id: TDC-2  
claim: Every connected component of a fixed-order oriented transversal space is acyclic.  
claim_basis: unsupported_or_source_gap  
exact_statement_used: not established; reduced to endpoint-pair incidence component acyclicity plus Lemma 4  
hypotheses_checked: pairwise disjoint open convex sets; fixed oriented order  
normalization: oriented lines \((u,p)\), order by increasing line parameter  
local_source_location: Section 2, Lemma 4 and reduction paragraph  
competing_variants: ["endpoint-incidence components acyclic", "only single-endpoint fibers convex, insufficient"]  
status: UNESTABLISHED

claim_id: TDC-3  
claim: Endpoint-incidence and convex-fiber maps are valid for open, possibly noncompact convex sets and ordinary reduced homology.  
claim_basis: derived_here  
exact_statement_used: pointed cone and ordered endpoint fibers are convex; endpoint-to-line projection is a deformation retract and hence homology equivalence  
hypotheses_checked: open convex sets, possibly unbounded; ordinary singular homology  
normalization: no compactness/properness hypothesis; no Vietoris-Begle theorem invoked  
local_source_location: Lemmas 1-4  
competing_variants: ["general acyclic-fiber transfer for arbitrary nonproper maps, not asserted", "explicit convex-fiber deformation retract for the needed endpoint-to-line map, established"]  
status: ESTABLISHED in the stated limited form

Unknowns addendum:

```yaml
unknown_id: U002
kind: unresolved key lemma
description: "Whether fixed-order oriented acyclicity holds componentwise via endpoint-incidence acyclicity."
target_determining: true
current_evidence: "SC8 reduces each oriented line component to its endpoint-incidence component; SC6 proves relevant single-endpoint fibers convex, but that does not imply total incidence acyclicity."
candidate_resolutions: ["Prove the endpoint-pair incidence component acyclicity branch lemma stated in section 3."]
downstream_outcomes: ["If resolved, TDC-2 follows using Lemma 4.", "If false, the proposed endpoint-incidence route cannot prove the target."]
answer_sensitivity_rationale: "TDC-2 is the fixed-order oriented component acyclicity input needed before passing to unoriented line components."
resolution_test_id: "U002-endpoint-component-acyclicity"
required_resolution_test: "Define the incidence object attached to an arbitrary component and prove its acyclicity without assuming the full fixed-order stratum is connected."
assigned_solver: "SS2"
status: OPEN
```

```yaml
unknown_id: U003
kind: transfer validity
description: "Whether homological fiber-transfer tools apply to open, noncompact incidence maps with ordinary reduced homology."
target_determining: true
current_evidence: "For the endpoint-to-line map, an explicit continuous section and fiberwise straight-line deformation retract are proved; unbounded intervals are handled by the arctangent endpoint selector."
candidate_resolutions: ["Use Lemma 4 instead of a nonproper Vietoris-Begle argument."]
downstream_outcomes: ["Acyclicity of the endpoint-incidence component transfers to the oriented line component.", "No compact-exhaustion or properness condition is needed for SC8."]
answer_sensitivity_rationale: "Without this transfer, SC7 would not imply acyclicity of the line component."
resolution_test_id: "U003-open-noncompact-transfer"
required_resolution_test: "Give a self-contained homology-transfer proof or replacement for the needed maps in ordinary reduced homology."
assigned_solver: "SS2"
status: RESOLVED for the endpoint-to-line and convex-fiber maps explicitly proved here
```

No new unknowns beyond U002 and U003.

5. Interface notes for S6

what this subproof establishes: SC6 is established for pointed cones and ordered fixed-first-endpoint fibers. SC8 is established by an explicit deformation retract \(E_U\simeq U\), valid for open and noncompact convex sets.  
what remains conditional: SC7 remains conditional on proving endpoint-pair incidence component acyclicity.  
failure_output_type: branch lemma target  
candidate guidance sentence, if any: Prove endpoint-pair incidence component acyclicity directly; do not infer it from single-endpoint convex fibers unless the projection image component is also proved acyclic.  
auxiliary lemma candidate, if any: the section 3 candidate lemma for components of \(P\).  
notation introduced: \(I_C(\ell)\), \(\tau_C(\ell)\), \(\operatorname{Cone}^+_x(K)\), \(F_x\), \(E_U\), \(P\).  
risk points: The proved transfer is not a general Vietoris-Begle theorem. Convex fibers alone are insufficient for SC7; the annulus-times-interval example blocks that route.

6. Web-source confirmation

no web sources used