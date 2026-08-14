1. Assignment restatement

S-ID: S2

assigned subclaim(s): SC2 and SC3

what must be proved: Set up the Terwilliger algebra for the association scheme from the orbit Schur ring, state the almost-commutative criterion, and prove that when \(H=\{1\}\), the Terwilliger algebra is \(\operatorname{Mat}_{|G|}(\mathbb C)\), the standard module is the primary module, and the algebra is almost commutative.

declared prerequisite subclaims: None.

2. Subproof or failure

Let the vertex set be \(G\), and take the Terwilliger algebra with respect to the base vertex \(1_G\). For an \(H\)-orbit \(X\subseteq G\), the corresponding Cayley relation is
\[
R_X=\{(a,b)\in G\times G: a^{-1}b\in X\},
\]
with adjacency matrix \(A_X\). The dual idempotent \(E_X^*\) is the diagonal projection onto the coordinate subspace spanned by \(\{e_x:x\in X\}\), where \(\{e_x:x\in G\}\) is the standard basis of \(V=\mathbb C^G\). The Terwilliger algebra is
\[
T=\langle A_X,E_X^*: X\text{ an }H\text{-orbit in }G\rangle\leq \operatorname{End}_{\mathbb C}(V).
\]

The almost-commutative criterion used here is: \(T\) is almost commutative if and only if every irreducible \(T\)-module other than the primary module is one-dimensional.

Now assume \(H=\{1\}\). Then every \(H\)-orbit is a singleton. Write \(A_s\) for the adjacency matrix attached to \(\{s\}\), so
\[
(A_s)_{u,v}=1 \quad\Longleftrightarrow\quad u^{-1}v=s.
\]
Also write \(E_x^*\) for the diagonal projection onto \(\mathbb C e_x\).

For any \(x,y\in G\), consider
\[
E_x^* A_{x^{-1}y} E_y^*.
\]
On a basis vector \(e_z\), this is zero unless \(z=y\). If \(z=y\), then
\[
A_{x^{-1}y}e_y=e_x,
\]
because the unique \(u\in G\) satisfying \(u^{-1}y=x^{-1}y\) is \(u=x\). Therefore
\[
E_x^* A_{x^{-1}y} E_y^* e_z
=
\begin{cases}
e_x,& z=y,\\
0,& z\neq y.
\end{cases}
\]
Thus \(E_x^* A_{x^{-1}y} E_y^*\) is the matrix unit \(M_{x,y}\). Since this holds for every \(x,y\in G\), all matrix units lie in \(T\). Hence
\[
T=\operatorname{End}_{\mathbb C}(V)\cong \operatorname{Mat}_{|G|}(\mathbb C).
\]

It follows directly that \(V\) is irreducible as a \(T\)-module: if \(0\neq W\leq V\) is \(T\)-stable and \(w=\sum_z c_z e_z\in W\) has \(c_y\neq 0\), then for every \(x\in G\),
\[
M_{x,y}w=c_y e_x\in W,
\]
so all basis vectors \(e_x\) lie in \(W\), and therefore \(W=V\).

The primary module is the span of the vectors \(E_X^*\mathbf 1\), where \(X\) ranges over the subconstituents and \(\mathbf 1=\sum_{g\in G}e_g\). In the case \(H=\{1\}\), the subconstituents are the singletons \(\{x\}\), and
\[
E_x^*\mathbf 1=e_x.
\]
Hence the primary module is \(\operatorname{span}\{e_x:x\in G\}=V\). Thus the standard module itself is the primary module.

Since \(V\) is the only irreducible \(T\)-submodule appearing in the standard module and it is primary, there are no nonprimary irreducible \(T\)-modules to check. By the almost-commutative criterion, \(T\) is almost commutative.

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

claim_id: S2-1  
proof_location: Section 2, first paragraph  
claim_or_fact_used: The association scheme from \(S(G,H)\) has relations indexed by \(H\)-orbits, with Cayley relation \(R_X=\{(a,b):a^{-1}b\in X\}\).  
source_status: provided definition / notation / assumption  
cited_label_or_name: Orbit Schur ring / Cayley association scheme setup  
exact_statement_used: Basic sets are \(H\)-orbits on \(G\), and the associated Cayley relations are indexed by those orbits.  
hypotheses_or_conditions_needed: \(G\) finite group, \(H\leq \operatorname{Aut}(G)\).  
where_hypotheses_are_checked: Given in target theorem.  
strength_used: Only relation indexing and adjacency notation.  
notes: Basepoint fixed as \(1_G\).

claim_id: S2-2  
proof_location: Section 2, second paragraph  
claim_or_fact_used: Almost commutativity is checked by nonprimary irreducible \(T\)-modules being one-dimensional.  
source_status: provided definition / notation / assumption  
cited_label_or_name: Almost-commutative Terwilliger criterion  
exact_statement_used: \(T\) is almost commutative iff every irreducible \(T\)-module other than the primary module is one-dimensional.  
hypotheses_or_conditions_needed: \(T\) is the Terwilliger algebra of the association scheme.  
where_hypotheses_are_checked: Established in the setup.  
strength_used: Full criterion.  
notes: Used only after proving the \(H=\{1\}\) module structure.

claim_id: S2-3  
proof_location: Section 2, “Now assume \(H=\{1\}\)”  
claim_or_fact_used: If \(H=\{1\}\), each \(H\)-orbit is a singleton.  
source_status: standard background fact  
cited_label_or_name: Definition of orbit under a group action  
exact_statement_used: The orbit of \(x\) under the trivial group action is \(\{x\}\).  
hypotheses_or_conditions_needed: \(H=\{1\}\).  
where_hypotheses_are_checked: Assumed for SC3.  
strength_used: All basic sets become singletons.  
notes: This is immediate from the definition of orbit.

claim_id: S2-4  
proof_location: Section 2, matrix-unit computation  
claim_or_fact_used: \(E_x^*A_{x^{-1}y}E_y^*=M_{x,y}\).  
source_status: proved inside the current proof  
cited_label_or_name: Matrix-unit computation  
exact_statement_used: For all \(x,y,z\in G\), \(E_x^*A_{x^{-1}y}E_y^*e_z=e_x\) if \(z=y\), and \(0\) otherwise.  
hypotheses_or_conditions_needed: Singleton relations and the Cayley convention \(u^{-1}v=s\).  
where_hypotheses_are_checked: \(H=\{1\}\), so singleton relations exist.  
strength_used: Gives every matrix unit in \(T\).  
notes: No commutativity of \(G\) is needed for this computation.

claim_id: S2-5  
proof_location: Section 2, after matrix-unit computation  
claim_or_fact_used: The full set of matrix units spans \(\operatorname{End}_{\mathbb C}(V)\).  
source_status: standard background fact  
cited_label_or_name: Matrix-unit basis of full matrix algebra  
exact_statement_used: For a finite basis \(\{e_x\}\), the maps \(M_{x,y}\) form a basis of \(\operatorname{End}_{\mathbb C}(V)\).  
hypotheses_or_conditions_needed: \(V\) is finite-dimensional with basis indexed by \(G\).  
where_hypotheses_are_checked: \(G\) is finite.  
strength_used: Since \(T\) contains all \(M_{x,y}\), \(T=\operatorname{End}_{\mathbb C}(V)\).  
notes: Standard finite-dimensional linear algebra.

claim_id: S2-6  
proof_location: Section 2, irreducibility paragraph  
claim_or_fact_used: \(V\) is irreducible as a module for \(\operatorname{End}_{\mathbb C}(V)\).  
source_status: proved inside the current proof  
cited_label_or_name: Irreducibility from matrix units  
exact_statement_used: Any nonzero \(T\)-stable subspace containing a vector with nonzero \(e_y\)-coefficient contains every \(e_x\), hence equals \(V\).  
hypotheses_or_conditions_needed: All matrix units \(M_{x,y}\) lie in \(T\).  
where_hypotheses_are_checked: Established by S2-4 and S2-5.  
strength_used: Shows the standard module has no proper nonzero \(T\)-submodule.  
notes: This also identifies the only irreducible constituent of the standard module.

claim_id: S2-7  
proof_location: Section 2, primary-module paragraph  
claim_or_fact_used: The primary module is spanned by \(E_X^*\mathbf 1\) over all subconstituents \(X\).  
source_status: standard background fact  
cited_label_or_name: Primary Terwilliger module description  
exact_statement_used: For a based association scheme, the primary module is \(\operatorname{span}\{E_X^*\mathbf 1:X\text{ a subconstituent}\}\).  
hypotheses_or_conditions_needed: Terwilliger algebra taken with respect to a base vertex.  
where_hypotheses_are_checked: Base vertex \(1_G\) fixed in setup.  
strength_used: In singleton case, this span equals \(V\).  
notes: Used only to identify the primary module.

claim_id: S2-8  
proof_location: Section 2, final paragraph  
claim_or_fact_used: If there are no nonprimary irreducible modules, the criterion is satisfied vacuously.  
source_status: standard background fact  
cited_label_or_name: Vacuous truth  
exact_statement_used: A universal condition over an empty collection is true.  
hypotheses_or_conditions_needed: The only irreducible \(T\)-module in the standard module is the primary module.  
where_hypotheses_are_checked: Established in S2-6 and S2-7.  
strength_used: Concludes almost commutativity.  
notes: Applies the criterion from S2-2.

5. Interface notes for S6

what this subproof establishes: SC2 and SC3. It sets up \(T\), states the almost-commutative criterion, and proves that \(H=\{1\}\) implies \(T=\operatorname{Mat}_{|G|}(\mathbb C)\), with the standard module equal to the primary module, hence \(T\) is almost commutative.

what remains conditional: Nothing inside S2 is conditional on other subclaims.

failure_output_type: solved

candidate guidance sentence, if any: None.

auxiliary lemma candidate, if any: None.

notation introduced: \(V=\mathbb C^G\), basis vectors \(e_x\), adjacency matrices \(A_X\) and \(A_s\), dual idempotents \(E_X^*\) and \(E_x^*\), matrix units \(M_{x,y}\).

risk points: The matrix-unit formula depends on the chosen Cayley relation convention \(a^{-1}b=s\). If the final proof uses the opposite convention, replace \(A_{x^{-1}y}\) by the corresponding inverse-indexed adjacency matrix; the matrix-unit argument is unchanged.

6. Web-source confirmation

no web sources used