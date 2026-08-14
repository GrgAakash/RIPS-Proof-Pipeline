1. Assignment Restatement

S-ID: S1

assigned subclaim(s): Oriented-line parametrization and projection criterion.

what must be proved: Define the oriented line space by pairs \((u,p)\) with \(u\in S^{d-1}\) and \(p\in u^\perp\), define
\[
K(u)=\bigcap_i \pi_u(C_i),
\]
where \(\pi_u:\mathbb R^d\to u^\perp\) is orthogonal projection, and prove that an oriented line with direction \(u\) is a transversal exactly when \(p\in K(u)\). Also prove each nonempty \(K(u)\) is open convex and the direction set
\[
D=\{u\in S^{d-1}:K(u)\neq\varnothing\}
\]
is open.

declared prerequisite subclaims: None.

2. Subproof or Failure

Let \(F=\{C_1,\dots,C_n\}\) be a finite family of pairwise disjoint open convex subsets of \(\mathbb R^d\), with \(n\ge 2\). Pairwise disjointness is not needed for this subclaim.

For \(u\in S^{d-1}\), let
\[
u^\perp=\{z\in\mathbb R^d:z\cdot u=0\},
\]
and let
\[
\pi_u(x)=x-(x\cdot u)u
\]
be the orthogonal projection of \(\mathbb R^d\) onto \(u^\perp\).

Every oriented affine line in \(\mathbb R^d\) has a unique representation
\[
\ell(u,p)=\{p+tu:t\in\mathbb R\},
\]
with \(u\in S^{d-1}\) and \(p\in u^\perp\). Indeed, \(u\) is the chosen unit direction of the oriented line. Among all points of the affine line, there is a unique point perpendicular to \(u\): if \(x_0\) is any point on the line, then
\[
p=x_0-(x_0\cdot u)u
\]
lies on the same affine line and satisfies \(p\cdot u=0\). If \(p,p'\in u^\perp\) define the same oriented line with direction \(u\), then \(p'=p+tu\) for some \(t\), and taking dot product with \(u\) gives \(0=0+t\), so \(t=0\), hence \(p=p'\).

Now fix \(u\in S^{d-1}\), \(p\in u^\perp\), and an index \(i\). The line \(\ell(u,p)\) meets \(C_i\) if and only if \(p\in \pi_u(C_i)\). If \(\ell(u,p)\cap C_i\neq\varnothing\), choose \(x\in C_i\cap \ell(u,p)\). Then \(x=p+tu\) for some \(t\), so \(\pi_u(x)=p\), hence \(p\in\pi_u(C_i)\). Conversely, if \(p\in\pi_u(C_i)\), then \(p=\pi_u(x)\) for some \(x\in C_i\). Thus \(x=p+(x\cdot u)u\in \ell(u,p)\), so \(\ell(u,p)\cap C_i\neq\varnothing\).

Therefore \(\ell(u,p)\) meets every \(C_i\) if and only if
\[
p\in \bigcap_{i=1}^n \pi_u(C_i)=K(u).
\]
Thus the oriented line-transversal space is naturally identified with
\[
T^+(F)=\{(u,p):u\in S^{d-1},\ p\in u^\perp,\ p\in K(u)\}.
\]

For each \(u\), every \(\pi_u(C_i)\subset u^\perp\) is convex because \(\pi_u\) is linear and the image of a convex set under a linear map is convex. It is open in \(u^\perp\) because \(\pi_u:\mathbb R^d\to u^\perp\) is a surjective linear map, hence an open map between finite-dimensional Euclidean spaces. Therefore \(K(u)\), being a finite intersection of open convex subsets of \(u^\perp\), is open and convex whenever it is nonempty.

It remains to prove that
\[
D=\{u\in S^{d-1}:K(u)\neq\varnothing\}
\]
is open. Suppose \(u_0\in D\). Choose
\[
p_0\in K(u_0)=\bigcap_i \pi_{u_0}(C_i).
\]
For each \(i\), choose \(x_i\in C_i\) with \(\pi_{u_0}(x_i)=p_0\). Then all \(x_i\) lie on the same line \(\ell(u_0,p_0)\).

Since each \(C_i\) is open and \(x_i\in C_i\), choose \(\varepsilon_i>0\) such that the open ball \(B(x_i,\varepsilon_i)\subset C_i\). Let
\[
\varepsilon=\min_i \varepsilon_i>0.
\]
For \(u\) close to \(u_0\), the orthogonal projections \(\pi_u(x_i)\) are all close to \(\pi_{u_0}(x_i)=p_0\). More precisely, the map
\[
u\mapsto \pi_u(x_i)
\]
is continuous for each fixed \(x_i\), so after shrinking to a neighborhood \(U\) of \(u_0\) in \(S^{d-1}\), all projected points \(\pi_u(x_i)\) lie within a small common neighborhood of \(p_0\) in \(\mathbb R^d\).

We need a common point in all \(\pi_u(C_i)\). For this, observe that because \(B(x_i,\varepsilon_i)\subset C_i\), its projection \(\pi_u(B(x_i,\varepsilon_i))\) contains the open ball of radius \(\varepsilon_i\) around \(\pi_u(x_i)\) inside \(u^\perp\). Indeed, if \(q\in u^\perp\) and \(\|q-\pi_u(x_i)\|<\varepsilon_i\), then
\[
y=x_i+(q-\pi_u(x_i))
\]
satisfies \(\pi_u(y)=q\) and
\[
\|y-x_i\|=\|q-\pi_u(x_i)\|<\varepsilon_i,
\]
so \(y\in B(x_i,\varepsilon_i)\subset C_i\). Hence \(q\in\pi_u(C_i)\).

Choose \(U\) small enough that for every \(u\in U\) and every \(i\),
\[
\|\pi_u(x_i)-\pi_u(x_1)\|<\varepsilon/2.
\]
Then \(\pi_u(x_1)\in u^\perp\), and for every \(i\),
\[
\pi_u(x_1)\in B_{u^\perp}(\pi_u(x_i),\varepsilon_i)\subset \pi_u(C_i).
\]
Thus \(\pi_u(x_1)\in K(u)\), so \(K(u)\neq\varnothing\). Therefore \(U\subset D\), proving that \(D\) is open in \(S^{d-1}\).

For \(d=1\), the same argument applies with \(u^\perp=\{0\}\), or directly: \(S^0=\{-1,1\}\) is discrete, so every subset of \(S^0\), including \(D\), is open.

3. Solver Failure Output And Candidate Guidance

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

claim_id: S1-C1  
proof_location: Section 2, paragraphs 2-3  
claim_or_fact_used: Every oriented affine line has a unique representation \(\ell(u,p)=p+\mathbb R u\) with \(u\in S^{d-1}\), \(p\in u^\perp\).  
source_status: proved inside the current proof  
cited_label_or_name: none  
exact_statement_used: As stated above.  
hypotheses_or_conditions_needed: Euclidean inner product on \(\mathbb R^d\).  
where_hypotheses_are_checked: Built into the ambient space \(\mathbb R^d\).  
strength_used: Full uniqueness and existence.  
notes: Standard orthogonal decomposition is used explicitly.

claim_id: S1-C2  
proof_location: Section 2, paragraphs 4-5  
claim_or_fact_used: \(\ell(u,p)\cap C_i\neq\varnothing\) if and only if \(p\in\pi_u(C_i)\).  
source_status: proved inside the current proof  
cited_label_or_name: projection criterion  
exact_statement_used: For fixed \(u,p,i\), meeting \(C_i\) is equivalent to \(p\in\pi_u(C_i)\).  
hypotheses_or_conditions_needed: \(p\in u^\perp\), \(\pi_u\) orthogonal projection.  
where_hypotheses_are_checked: Definitions of \(u^\perp\), \(\pi_u\), and \(\ell(u,p)\).  
strength_used: Full equivalence.  
notes: This is the main parametrization criterion.

claim_id: S1-C3  
proof_location: Section 2, paragraph 6  
claim_or_fact_used: Linear images of convex sets are convex.  
source_status: standard background fact  
cited_label_or_name: preservation of convexity under linear maps  
exact_statement_used: If \(A\) is convex and \(L\) is linear, then \(L(A)\) is convex.  
hypotheses_or_conditions_needed: \(C_i\) convex; \(\pi_u\) linear.  
where_hypotheses_are_checked: \(C_i\) are assumed convex; \(\pi_u(x)=x-(x\cdot u)u\) is linear.  
strength_used: Applied to \(\pi_u(C_i)\).  
notes: Genuinely standard finite-dimensional convexity fact.

claim_id: S1-C4  
proof_location: Section 2, paragraph 6  
claim_or_fact_used: A surjective linear map between finite-dimensional Euclidean spaces is open.  
source_status: standard background fact  
cited_label_or_name: finite-dimensional open mapping theorem for linear maps  
exact_statement_used: If \(L:V\to W\) is surjective linear between finite-dimensional normed spaces, then \(L\) maps open subsets of \(V\) to open subsets of \(W\).  
hypotheses_or_conditions_needed: \(\pi_u:\mathbb R^d\to u^\perp\) is surjective linear.  
where_hypotheses_are_checked: Orthogonal projection is linear and restricts as identity on \(u^\perp\).  
strength_used: Used to show \(\pi_u(C_i)\) is open in \(u^\perp\).  
notes: Could also be proved directly by projecting balls.

claim_id: S1-C5  
proof_location: Section 2, paragraph 6  
claim_or_fact_used: Finite intersections of open convex sets are open convex.  
source_status: standard background fact  
cited_label_or_name: finite-intersection property for open convex sets  
exact_statement_used: A finite intersection of open sets is open, and a finite intersection of convex sets is convex.  
hypotheses_or_conditions_needed: Each \(\pi_u(C_i)\) is open convex.  
where_hypotheses_are_checked: Established immediately before use.  
strength_used: Used to prove each nonempty \(K(u)\) is open convex.  
notes: Empty intersections are avoided by the phrase “whenever nonempty.”

claim_id: S1-C6  
proof_location: Section 2, paragraphs 7-13  
claim_or_fact_used: The direction set \(D=\{u:K(u)\neq\varnothing\}\) is open.  
source_status: proved inside the current proof  
cited_label_or_name: openness of direction set  
exact_statement_used: For every \(u_0\in D\), there is a neighborhood \(U\subset S^{d-1}\) of \(u_0\) such that \(U\subset D\).  
hypotheses_or_conditions_needed: Each \(C_i\) open; finitely many \(C_i\); projection maps vary continuously in \(u\).  
where_hypotheses_are_checked: Openness gives balls \(B(x_i,\varepsilon_i)\subset C_i\); finiteness gives positive minimum \(\varepsilon\); continuity follows from the explicit formula for \(\pi_u(x)\).  
strength_used: Full openness of \(D\).  
notes: Pairwise disjointness is not used.

claim_id: S1-C7  
proof_location: Section 2, paragraph 10  
claim_or_fact_used: For fixed \(x\), the map \(u\mapsto\pi_u(x)\) is continuous.  
source_status: standard background fact  
cited_label_or_name: continuity of polynomial/vector operations  
exact_statement_used: Since \(\pi_u(x)=x-(x\cdot u)u\), the map \(u\mapsto\pi_u(x)\) is continuous on \(S^{d-1}\).  
hypotheses_or_conditions_needed: Fixed \(x\in\mathbb R^d\).  
where_hypotheses_are_checked: \(x_i\) are fixed after choosing them.  
strength_used: Used to keep projected points close for \(u\) near \(u_0\).  
notes: Directly follows from continuity of dot product and scalar multiplication.

5. Interface Notes For S6

what this subproof establishes: The oriented transversal space is exactly
\[
T^+(F)=\{(u,p):u\in S^{d-1},\ p\in u^\perp,\ p\in K(u)\},
\]
where \(K(u)=\bigcap_i\pi_u(C_i)\). Each nonempty \(K(u)\) is open convex, and the direction set \(D=\{u:K(u)\neq\varnothing\}\) is open.

what remains conditional: Nothing inside S1 depends on later subclaims. Later assembly still needs S2-S5.

failure_output_type: solved

candidate guidance sentence, if any: None.

auxiliary lemma candidate, if any: None.

notation introduced: \(u^\perp\), \(\pi_u\), \(\ell(u,p)\), \(K(u)\), \(T^+(F)\), \(D\).

risk points: The proof uses the oriented-line space, not the unoriented quotient. Passing to unoriented components is outside S1.

6. Web-Source Confirmation

no web sources used