1. Assignment restatement

S-ID:
S4

assigned subclaim(s):
Analyze the orientation-reversal quotient from oriented line transversals to unoriented line transversals.

what must be proved:
For a connected component \(X\) of the unoriented transversal space \(T(\mathcal F)\), describe \(q^{-1}(X)\) inside the oriented transversal space \(T^+(\mathcal F)\), where \(q\) forgets orientation. Then prove that if oriented transversal components are acyclic, \(X\) is acyclic.

declared prerequisite subclaims:
The only declared prerequisite is:

Every connected component \(E\) of the oriented transversal space \(T^+(\mathcal F)\) is acyclic.

This prerequisite is not proved here.

2. Subproof or failure

Let \(\mathcal F=\{C_1,\dots,C_n\}\), with \(n\ge 2\), be a finite pairwise disjoint family of open convex subsets of \(\mathbb R^d\). Let \(L\) denote the unoriented line space, and let \(L^+\) denote the oriented line space. Model

\[
L^+=\{(u,p):u\in S^{d-1},\ p\in u^\perp\},
\]

where \((u,p)\) represents the oriented line \(p+\mathbb R u\). Orientation reversal is

\[
r(u,p)=(-u,p).
\]

Let \(q:L^+\to L\) forget orientation. The map \(q\) is the quotient by the free involution \(r\), and is a two-sheeted covering map. Define

\[
T^+(\mathcal F)=q^{-1}(T(\mathcal F)).
\]

First, define an order invariant on \(T^+(\mathcal F)\). For \(e=(u,p)\in T^+(\mathcal F)\), write

\[
\gamma_e(t)=p+tu.
\]

For each \(i\), set

\[
I_i(e)=\{t\in\mathbb R:\gamma_e(t)\in C_i\}.
\]

Since \(C_i\) is open and convex, \(I_i(e)\) is an open convex subset of \(\mathbb R\), hence an open interval, possibly unbounded. Since \(e\) is a transversal, each \(I_i(e)\) is nonempty. Since the \(C_i\) are pairwise disjoint, the intervals \(I_i(e)\) are pairwise disjoint. Because \(n\ge 2\), no \(I_i(e)\) can equal all of \(\mathbb R\): if \(I_i(e)=\mathbb R\), then the whole line lies in \(C_i\), contradicting that the same line also meets some disjoint \(C_j\).

Thus the intervals \(I_i(e)\) have a well-defined strict linear order along the oriented line. Write this order as \(\operatorname{ord}(e)\).

The map \(e\mapsto \operatorname{ord}(e)\) is locally constant. Indeed, fix \(e_0=(u_0,p_0)\). Choose parameters \(t_i\in I_i(e_0)\). If the order at \(e_0\) is, say,

\[
I_{i_1}(e_0)<I_{i_2}(e_0)<\cdots<I_{i_n}(e_0),
\]

choose the \(t_{i_j}\) in that same increasing order. Since each \(C_i\) is open and \(\gamma_{e_0}(t_i)\in C_i\), for \(e\) sufficiently close to \(e_0\) we still have \(\gamma_e(t_i)\in C_i\). Hence the same ordered witnesses persist, so the order cannot change in a small neighborhood. Therefore \(\operatorname{ord}\) is locally constant, and hence constant on every connected component of \(T^+(\mathcal F)\).

Now observe how orientation reversal acts. Since

\[
\gamma_{r(e)}(t)=p-tu=\gamma_e(-t),
\]

we have

\[
I_i(r(e))=-I_i(e).
\]

Therefore \(\operatorname{ord}(r(e))\) is the reverse of \(\operatorname{ord}(e)\). Because \(n\ge 2\), a strict ordering of \(n\) distinct labels is not equal to its reverse. Hence no connected component \(E\) of \(T^+(\mathcal F)\) can satisfy \(r(E)=E\). Thus \(E\) and \(r(E)\) are always distinct oriented components.

Let \(X\) be a connected component of \(T(\mathcal F)\), and pick \(e\in q^{-1}(X)\). Let \(E\) be the connected component of \(T^+(\mathcal F)\) containing \(e\). Since \(q(E)\) is connected and meets \(X\), maximality of \(X\) gives \(q(E)\subseteq X\).

The transversal space \(T(\mathcal F)\) is locally path-connected: locally, a line meeting each open set \(C_i\) continues to meet each \(C_i\) under small perturbations, and the ambient line space is locally path-connected. Therefore connected components of \(T(\mathcal F)\) are path-connected. Since \(q:T^+(\mathcal F)\to T(\mathcal F)\) is a covering map, every path in \(X\) starting at \(q(e)\) lifts uniquely after choosing the initial lift \(e\). Hence every point of \(X\) lies in \(q(E)\). Thus

\[
q(E)=X.
\]

Similarly, \(q(r(E))=X\). Also \(r(E)\ne E\).

Now let \(E'\) be any connected component of \(q^{-1}(X)\). By the same path-lifting argument, \(q(E')=X\). Therefore \(E'\) meets the two-point fiber \(q^{-1}(q(e))=\{e,r(e)\}\). Hence \(E'=E\) or \(E'=r(E)\). So

\[
q^{-1}(X)=E\sqcup r(E),
\]

with \(E\) and \(r(E)\) distinct connected components of \(T^+(\mathcal F)\).

Finally, \(q|_E:E\to X\) is bijective. It is surjective by the previous paragraph. It is injective because each unoriented line has exactly two oriented lifts, exchanged by \(r\), and \(E\cap r(E)=\varnothing\). Since \(q\) is a covering map, a bijective restriction to one sheet is a homeomorphism. Therefore

\[
X\cong E.
\]

By the declared prerequisite, \(E\) is acyclic. Hence \(X\) is acyclic.

Thus S4 is solved, conditionally on the oriented-component acyclicity prerequisite.

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

claim_id: S4-1  
proof_location: Section 2, opening model of \(L^+\) and \(q\)  
claim_or_fact_used: Oriented affine lines are modeled by \((u,p)\in S^{d-1}\times\mathbb R^d\) with \(p\in u^\perp\), and orientation reversal is \((u,p)\mapsto(-u,p)\).  
source_status: standard background fact  
cited_label_or_name: standard parametrization of oriented affine lines  
exact_statement_used: Every oriented affine line has a unique representation \(p+\mathbb R u\) with \(u\in S^{d-1}\) and \(p\in u^\perp\).  
hypotheses_or_conditions_needed: Euclidean structure on \(\mathbb R^d\).  
where_hypotheses_are_checked: Target theorem works in \(\mathbb R^d\).  
strength_used: Full parametrization and orientation reversal.  
notes: This is only a model for the natural topology.

claim_id: S4-2  
proof_location: Section 2, covering discussion  
claim_or_fact_used: Forgetting orientation gives a two-sheeted covering \(q:L^+\to L\).  
source_status: standard background fact  
cited_label_or_name: quotient by free antipodal involution on oriented line space  
exact_statement_used: The quotient of \(L^+\) by \((u,p)\sim(-u,p)\) is the unoriented line space, and the quotient map is a two-sheeted covering.  
hypotheses_or_conditions_needed: The involution is free.  
where_hypotheses_are_checked: \((u,p)\ne(-u,p)\) because \(u\ne -u\) for \(u\in S^{d-1}\), including \(d=1\).  
strength_used: Covering and two-point fibers.  
notes: Local sheets are obtained by choosing a hemisphere of directions.

claim_id: S4-3  
proof_location: Section 2, definition of \(I_i(e)\)  
claim_or_fact_used: Intersection of an open convex set with a line is an open convex subset of \(\mathbb R\).  
source_status: standard background fact  
cited_label_or_name: convexity and openness under affine preimage  
exact_statement_used: If \(C\subset\mathbb R^d\) is open convex and \(\gamma:\mathbb R\to\mathbb R^d\) is affine, then \(\gamma^{-1}(C)\) is open and convex in \(\mathbb R\).  
hypotheses_or_conditions_needed: \(C_i\) open convex; \(\gamma_e\) affine.  
where_hypotheses_are_checked: Given by the target theorem and definition of \(\gamma_e\).  
strength_used: \(I_i(e)\) is an open interval, possibly unbounded.  
notes: Nonempty because \(e\) is a transversal.

claim_id: S4-4  
proof_location: Section 2, order invariant  
claim_or_fact_used: Pairwise disjoint nonempty intervals in \(\mathbb R\) have a strict linear left-to-right order.  
source_status: standard background fact  
cited_label_or_name: order of disjoint intervals on the real line  
exact_statement_used: For two disjoint intervals \(A,B\subset\mathbb R\), either every point of \(A\) is less than every point of \(B\), or every point of \(B\) is less than every point of \(A\).  
hypotheses_or_conditions_needed: \(A,B\) are disjoint intervals.  
where_hypotheses_are_checked: The \(I_i(e)\) are pairwise disjoint intervals.  
strength_used: Defines \(\operatorname{ord}(e)\).  
notes: Applied finitely many times.

claim_id: S4-5  
proof_location: Section 2, local constancy paragraph  
claim_or_fact_used: The order invariant is locally constant.  
source_status: proved inside the current proof  
cited_label_or_name: local persistence of witnesses  
exact_statement_used: If \(e_0\in T^+(\mathcal F)\), then all sufficiently nearby oriented transversals have the same order of intersection intervals.  
hypotheses_or_conditions_needed: Each \(C_i\) is open; finitely many \(C_i\).  
where_hypotheses_are_checked: Given in the target theorem.  
strength_used: Constancy on connected components.  
notes: Uses selected parameters \(t_i\) inside each \(C_i\).

claim_id: S4-6  
proof_location: Section 2, reversal paragraph  
claim_or_fact_used: Orientation reversal reverses the order invariant.  
source_status: proved inside the current proof  
cited_label_or_name: reversal identity  
exact_statement_used: \(I_i(r(e))=-I_i(e)\), so \(\operatorname{ord}(r(e))\) is the reverse order.  
hypotheses_or_conditions_needed: Definition \(r(u,p)=(-u,p)\).  
where_hypotheses_are_checked: Established in the oriented-line model.  
strength_used: Shows \(E\ne r(E)\).  
notes: Uses \(n\ge2\).

claim_id: S4-7  
proof_location: Section 2, path-lifting paragraph  
claim_or_fact_used: Components of \(T(\mathcal F)\) are path-connected.  
source_status: standard background fact plus checked openness  
cited_label_or_name: locally path-connected components are path components  
exact_statement_used: In a locally path-connected space, connected components are path-connected.  
hypotheses_or_conditions_needed: \(T(\mathcal F)\) is locally path-connected.  
where_hypotheses_are_checked: \(T(\mathcal F)\) is open in the line space because meeting open sets persists under small perturbations.  
strength_used: Allows path lifting from one point of \(X\) to any other.  
notes: This is a topological background fact.

claim_id: S4-8  
proof_location: Section 2, surjectivity of \(q(E)\to X\)  
claim_or_fact_used: Path lifting for covering maps.  
source_status: standard background fact  
cited_label_or_name: path lifting theorem  
exact_statement_used: Given a covering map \(p:Y\to X\), a path in \(X\), and a chosen lift of its initial point, there is a unique lifted path.  
hypotheses_or_conditions_needed: \(q:T^+(\mathcal F)\to T(\mathcal F)\) is a covering map.  
where_hypotheses_are_checked: From S4-2 restricted to the invariant subspace.  
strength_used: Proves \(q(E)=X\).  
notes: No homology used here.

claim_id: S4-9  
proof_location: Section 2, final homeomorphism argument  
claim_or_fact_used: A bijective one-sheet restriction of a covering map is a homeomorphism.  
source_status: standard background fact  
cited_label_or_name: one-sheet covering homeomorphism  
exact_statement_used: If \(p:Y\to X\) is a covering map and \(p|_A:A\to X\) is bijective with \(A\) a union of sheets locally, then \(p|_A\) is a homeomorphism.  
hypotheses_or_conditions_needed: \(q|_E\) is bijective and \(q\) is a covering map.  
where_hypotheses_are_checked: Surjectivity and injectivity proved in Section 2.  
strength_used: Gives \(X\cong E\).  
notes: This is the step transferring acyclicity.

claim_id: S4-10  
proof_location: Section 2, last paragraph  
claim_or_fact_used: Homeomorphic spaces have isomorphic reduced homology groups.  
source_status: standard background fact  
cited_label_or_name: topological invariance of reduced homology  
exact_statement_used: If \(X\cong E\), then \(\widetilde H_k(X)\cong \widetilde H_k(E)\) for all \(k\).  
hypotheses_or_conditions_needed: \(q|_E:E\to X\) is a homeomorphism; \(E\) acyclic.  
where_hypotheses_are_checked: Homeomorphism proved in Section 2; acyclicity is the declared prerequisite.  
strength_used: Concludes \(X\) acyclic.  
notes: This is the acyclicity-passing step.

5. Interface notes for S6

what this subproof establishes:
For every connected component \(X\) of the unoriented transversal space,

\[
q^{-1}(X)=E\sqcup r(E),
\]

where \(E\) and \(r(E)\) are distinct oriented components, and each restriction \(q|_E:E\to X\), \(q|_{r(E)}:r(E)\to X\) is a homeomorphism.

what remains conditional:
Acyclicity of the oriented component \(E\).

failure_output_type:
solved

candidate guidance sentence, if any:
null

auxiliary lemma candidate, if any:
null

notation introduced:
\(L^+\), \(L\), \(q\), \(r\), \(T^+(\mathcal F)\), \(\gamma_e(t)\), \(I_i(e)\), \(\operatorname{ord}(e)\).

risk points:
The possible “one invariant oriented component over \(X\)” case is ruled out using the order of pairwise disjoint convex sets along an oriented transversal. Without pairwise disjointness and \(n\ge2\), this argument would fail.

6. Web-source confirmation

no web sources used