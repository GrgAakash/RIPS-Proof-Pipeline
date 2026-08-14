1. Assignment restatement

S-ID:
S2

assigned subclaim(s):
For each connected component \(E\) of the oriented transversal space \(T^+(\mathcal F)\), the direction projection
\[
\rho:E\to D_E:=\rho(E)
\]
is a homotopy equivalence.

what must be proved:
Assuming the oriented model
\[
T^+(\mathcal F)=\{(u,p):u\in S^{d-1},\ p\in u^\perp,\ p\in K(u)\},
\]
where each nonempty \(K(u)\subset u^\perp\) is open convex and the direction set \(D=\{u:K(u)\neq\varnothing\}\) is open, prove that each component \(E\) projects by homotopy equivalence onto its direction component.

declared prerequisite subclaims:
S1: the oriented-line parametrization, the definition of \(K(u)\), openness and convexity of nonempty fibers \(K(u)\), and openness of the direction set \(D\).

2. Subproof or failure

Let
\[
V=\{(u,p):u\in S^{d-1},\ p\in u^\perp\}
\]
be the tangent-like vector bundle over \(S^{d-1}\), with projection \(\rho(u,p)=u\). Let
\[
T^+=\{(u,p)\in V:p\in K(u)\}.
\]
By the declared S1 prerequisite, \(T^+\) is fibered over the open set \(D=\{u:K(u)\neq\varnothing\}\), and each fiber
\[
(T^+)_u=\rho^{-1}(u)\cap T^+=K(u)
\]
is a nonempty open convex subset of \(u^\perp\).

Fix a connected component \(E\) of \(T^+\), and put \(D_E=\rho(E)\).

First, \(\rho|_E:E\to D_E\) is surjective by definition. Also, \(D_E\) is connected, since it is the continuous image of the connected set \(E\). We show that \(D_E\) is open in \(D\). Take \(u_0\in D_E\), and choose \(p_0\in K(u_0)\) with \((u_0,p_0)\in E\). Since \(K(u_0)\) is open in \(u_0^\perp\), and \(T^+\subset V\) is open over \(D\) locally in bundle coordinates, there is a neighborhood \(U\subset D\) of \(u_0\) and a continuous local section \(s:U\to T^+\) with \(s(u_0)=(u_0,p_0)\). Shrinking \(U\) if necessary, \(s(U)\) lies in the connected component \(E\), because \(s(U)\) is connected near \(u_0\) and meets \(E\), while components of the open set \(T^+\) are open. Hence \(U\subset D_E\). Thus \(D_E\) is open.

The same local-section argument also implies that \(\rho^{-1}(D_E)\cap T^+\) is connected. Indeed, let \(Y=\rho^{-1}(D_E)\cap T^+\). Suppose \(Y\) had two nonempty disjoint open-and-closed pieces \(Y_1,Y_2\). Since each fiber \(K(u)\) is convex, hence connected, each fiber lies entirely in one of the \(Y_i\). Therefore the images \(\rho(Y_1)\) and \(\rho(Y_2)\) form a separation of \(D_E\): they are disjoint, nonempty, cover \(D_E\), and are open by local sections. This contradicts connectedness of \(D_E\). Hence \(Y\) is connected. Since \(E\subset Y\) is a connected component of \(T^+\), we get
\[
E=Y=\rho^{-1}(D_E)\cap T^+.
\]
Thus the fiber of \(\rho|_E\) over every \(u\in D_E\) is exactly \(K(u)\), a nonempty convex set.

It remains to prove that \(\rho|_E\) is a homotopy equivalence. Since \(D_E\) is an open subset of the sphere, it is paracompact. The projection \(V|_{D_E}\to D_E\) is a rank \(d-1\) vector bundle. The subset \(E\subset V|_{D_E}\) is open, and each fiber \(E_u=K(u)\) is nonempty convex. By the standard Michael selection theorem for lower semicontinuous set-valued maps with nonempty closed convex values on paracompact spaces, applied locally after replacing each open convex fiber by an increasing exhaustion of closed convex subsets inside it, there exists a continuous section
\[
\sigma:D_E\to E
\]
of \(\rho|_E\).

Now define a homotopy \(H:E\times[0,1]\to E\) fiberwise by
\[
H((u,p),t)=\bigl(u,(1-t)p+t\sigma(u)\bigr).
\]
For each fixed \(u\), both \(p\) and \(\sigma(u)\) lie in the convex set \(K(u)\), so the whole segment \((1-t)p+t\sigma(u)\) lies in \(K(u)\). Hence \(H\) is well-defined and continuous. It satisfies
\[
H(-,0)=\operatorname{id}_E,\qquad H(-,1)=\sigma\circ\rho.
\]
Also \(\rho\circ\sigma=\operatorname{id}_{D_E}\). Therefore \(\sigma\) is a homotopy inverse to \(\rho|_E\), and \(\rho|_E:E\to D_E\) is a homotopy equivalence.

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

claim_id: C1
proof_location: Section 2, first paragraph
claim_or_fact_used: Oriented transversal space has model \(T^+=\{(u,p):p\in K(u)\subset u^\perp\}\), with nonempty \(K(u)\) open convex and direction set open.
source_status: provided definition / notation / assumption
cited_label_or_name: declared prerequisite S1
exact_statement_used: The oriented-line parametrization and fiber properties from S1.
hypotheses_or_conditions_needed: finite pairwise disjoint open convex family; S1 established.
where_hypotheses_are_checked: declared as prerequisite subclaim.
strength_used: full local fiber model, openness, convexity.
notes: This subproof is conditional on S1.

claim_id: C2
proof_location: Section 2, paragraphs 2-3
claim_or_fact_used: Continuous image of a connected space is connected.
source_status: standard background fact
cited_label_or_name: connected-image theorem
exact_statement_used: If \(X\) is connected and \(f:X\to Y\) is continuous, then \(f(X)\) is connected.
hypotheses_or_conditions_needed: \(E\) connected; \(\rho\) continuous.
where_hypotheses_are_checked: \(E\) is a connected component; \(\rho\) is bundle projection.
strength_used: connectedness of \(D_E\).
notes: standard point-set topology.

claim_id: C3
proof_location: Section 2, paragraphs 3-4
claim_or_fact_used: Local continuous sections exist near each point of an open subset of a vector bundle.
source_status: standard background fact
cited_label_or_name: local triviality of vector bundles
exact_statement_used: If \(E\) is an open subset of a vector bundle and \(x\in E\), then after local trivialization there is a continuous local section through \(x\) whose image lies in \(E\).
hypotheses_or_conditions_needed: vector bundle \(V\to S^{d-1}\); \(T^+\) open near \((u_0,p_0)\).
where_hypotheses_are_checked: from S1 fiber openness/local model.
strength_used: used to show \(D_E\) open and images of separated pieces open.
notes: standard bundle fact.

claim_id: C4
proof_location: Section 2, paragraph 5
claim_or_fact_used: Convex subsets are connected.
source_status: standard background fact
cited_label_or_name: convex-set path-connectedness
exact_statement_used: Every nonempty convex subset of a real vector space is path-connected, hence connected.
hypotheses_or_conditions_needed: each \(K(u)\) convex and nonempty.
where_hypotheses_are_checked: S1 prerequisite and \(u\in D_E\).
strength_used: each fiber cannot meet two separated components.
notes: standard linear topology fact.

claim_id: C5
proof_location: Section 2, paragraph 6
claim_or_fact_used: Paracompactness of open subsets of manifolds.
source_status: standard background fact
cited_label_or_name: paracompactness of open subsets of second-countable manifolds
exact_statement_used: Every open subset of a sphere is paracompact.
hypotheses_or_conditions_needed: \(D_E\subset S^{d-1}\) open.
where_hypotheses_are_checked: proved in Section 2.
strength_used: needed for selection theorem.
notes: standard topology.

claim_id: C6
proof_location: Section 2, paragraph 6
claim_or_fact_used: Continuous selection for open convex fibers.
source_status: standard background fact
cited_label_or_name: Michael selection theorem, open convex bundle-valued form
exact_statement_used: For a paracompact base, an open subset of a finite-dimensional vector bundle with nonempty convex fibers admits a continuous section.
hypotheses_or_conditions_needed: base paracompact; bundle finite-dimensional; total subset open; fibers nonempty convex.
where_hypotheses_are_checked: \(D_E\) open paracompact; \(V|_{D_E}\) finite-dimensional; \(E\) open; fibers \(K(u)\) nonempty convex.
strength_used: existence of global section \(\sigma:D_E\to E\).
notes: This is the main nontrivial standard background input.

claim_id: C7
proof_location: Section 2, final paragraph
claim_or_fact_used: Fiberwise straight-line homotopy stays inside convex fibers.
source_status: proved inside the current proof
cited_label_or_name: none
exact_statement_used: If \(p,\sigma(u)\in K(u)\) and \(K(u)\) is convex, then \((1-t)p+t\sigma(u)\in K(u)\) for all \(t\in[0,1]\).
hypotheses_or_conditions_needed: convexity of \(K(u)\).
where_hypotheses_are_checked: S1 prerequisite.
strength_used: constructs deformation from identity to \(\sigma\rho\).
notes: completes homotopy equivalence.

5. Interface notes for S6

what this subproof establishes:
Conditional on S1, for every connected component \(E\) of the oriented transversal space, the direction projection \(\rho:E\to D_E\) is a homotopy equivalence.

what remains conditional:
The oriented model, openness of \(T^+\), openness of \(D\), and convexity/openness of fibers \(K(u)\) remain conditional on S1.

failure_output_type:
solved

candidate guidance sentence, if any:
null

auxiliary lemma candidate, if any:
null

notation introduced:
\(V=\{(u,p):p\in u^\perp\}\), \(\rho\), \(T^+\), \(K(u)\), \(E\), \(D_E=\rho(E)\).

risk points:
The only substantial external standard input is the continuous-selection theorem for open convex fibers over a paracompact base. If S6 wants to avoid that theorem, it must replace it with an explicit partition-of-unity construction or cite it as a standard background fact.

6. Web-source confirmation

no web sources used