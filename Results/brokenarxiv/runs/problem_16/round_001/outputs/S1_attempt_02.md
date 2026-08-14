1. Assignment restatement

S-ID: S1

assigned subclaim(s): C1 and C2.

what must be proved:
C1: For a finite Galois splitting field \(K/\mathbb Q\), with \(G=\operatorname{Gal}(K/\mathbb Q)\), a place \(w\mid p\), \(D=\operatorname{Gal}(K_w/\mathbb Q_p)\), and \(X=X^*(T_K)\), establish
\[
T(\mathbb Q)=\operatorname{Hom}_G(X,K^*),\qquad
T(\mathbb Q_p)=\operatorname{Hom}_D(X,K_w^*).
\]
C2: Define the local character-valuation map
\[
\nu_T:T(\mathbb Q_p)\to \operatorname{Hom}_D(X,\mathbb Z),
\qquad
t\mapsto(\chi\mapsto v_w(\chi(t))),
\]
and prove that its kernel is exactly \(T(\mathbb Z_p)\), the maximal compact subgroup of \(T(\mathbb Q_p)\).

declared prerequisite subclaims: None external. C2 uses the local description proved in C1.

2. Subproof or failure

Let \(K/\mathbb Q\) be a finite Galois extension splitting \(T\), let \(G=\operatorname{Gal}(K/\mathbb Q)\), choose a place \(w\mid p\), and put \(L=K_w\), \(F=\mathbb Q_p\). Let
\[
D=\{g\in G:gw=w\}.
\]
Then \(L/F\) is finite Galois and \(D\simeq \operatorname{Gal}(L/F)\). Let \(X=X^*(T_K)\). Since \(T_K\) is a split torus, \(X\) is a finite free abelian group, and the evaluation pairing gives a functorial identification
\[
T(K)\simeq \operatorname{Hom}_{\mathbb Z}(X,K^*).
\]
The Galois action on \(X\) is the usual descent action, and under the above identification the induced \(G\)-action on \(\operatorname{Hom}_{\mathbb Z}(X,K^*)\) is
\[
(g\varphi)(\chi)=g\bigl(\varphi(g^{-1}\chi)\bigr).
\]
Thus the fixed points are exactly the equivariant homomorphisms \(\varphi:X\to K^*\), i.e.
\[
T(K)^G=\operatorname{Hom}_G(X,K^*).
\]
By faithfully flat Galois descent for affine varieties,
\[
T(\mathbb Q)=T(K)^G,
\]
so
\[
T(\mathbb Q)=\operatorname{Hom}_G(X,K^*).
\]

The same argument over \(F=\mathbb Q_p\) gives the local statement. Since \(K\) splits \(T\), the completion \(L=K_w\) splits \(T_F\). The character lattice of \(T_L\) is still \(X\), now with the restricted \(D\)-action. Hence
\[
T(L)\simeq \operatorname{Hom}_{\mathbb Z}(X,L^*),
\]
and Galois descent for \(L/F\) gives
\[
T(F)=T(L)^D=\operatorname{Hom}_D(X,L^*).
\]
Therefore
\[
T(\mathbb Q_p)=\operatorname{Hom}_D(X,K_w^*).
\]
This proves C1.

Now define \(v_w:L^*\to \mathbb Z\) to be the normalized discrete valuation. For \(t\in T(F)\), viewed through C1 as a \(D\)-equivariant homomorphism \(\varphi_t:X\to L^*\), define
\[
\nu_T(t)(\chi)=v_w(\varphi_t(\chi))=v_w(\chi(t)).
\]
This is a group homomorphism \(X\to \mathbb Z\), because characters multiply under the group law and valuations add. It is \(D\)-equivariant, with trivial \(D\)-action on \(\mathbb Z\), since for \(d\in D\),
\[
\nu_T(t)(d\chi)=v_w(\varphi_t(d\chi))
=v_w(d\varphi_t(\chi))
=v_w(\varphi_t(\chi)),
\]
using \(D\)-invariance of \(v_w\). Thus
\[
\nu_T:T(F)\to \operatorname{Hom}_D(X,\mathbb Z)
\]
is well-defined.

Let \(\mathcal O_L\) be the valuation ring of \(L\). Then
\[
\ker(\nu_T)
=
\{\varphi\in \operatorname{Hom}_D(X,L^*):v_w(\varphi(\chi))=0\text{ for all }\chi\in X\}
=
\operatorname{Hom}_D(X,\mathcal O_L^*).
\]
Choose a \(\mathbb Z\)-basis of \(X\). Then \(\operatorname{Hom}_{\mathbb Z}(X,\mathcal O_L^*)\cong(\mathcal O_L^*)^r\), where \(r=\operatorname{rank}X\). Since \(\mathcal O_L^*\) is compact, this group is compact, and \(\operatorname{Hom}_D(X,\mathcal O_L^*)\) is a closed subgroup. Hence \(\ker(\nu_T)\) is compact.

Conversely, let \(C\subseteq T(F)\) be any compact subgroup. The map \(\nu_T\) is continuous, and \(\operatorname{Hom}_D(X,\mathbb Z)\) is a discrete torsion-free abelian group. Therefore \(\nu_T(C)\) is a compact subgroup of a discrete group, hence finite; since the target is torsion-free, \(\nu_T(C)=0\). Thus every compact subgroup \(C\) of \(T(F)\) lies inside \(\ker(\nu_T)\).

So \(\ker(\nu_T)\) is itself compact and contains every compact subgroup of \(T(F)\). Therefore it is the maximal compact subgroup of \(T(F)=T(\mathbb Q_p)\). Since \(T(\mathbb Z_p)\) denotes this maximal compact subgroup,
\[
\ker(\nu_T)=T(\mathbb Z_p).
\]
This proves C2.

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
claim_or_fact_used: A torus split over \(K\) has a finite free character lattice \(X=X^*(T_K)\), and evaluation identifies \(T(K)\) with \(\operatorname{Hom}_{\mathbb Z}(X,K^*)\).  
source_status: standard background fact  
cited_label_or_name: Split torus character-lattice anti-equivalence  
exact_statement_used: For a split torus \(S\) over a field \(E\), with character lattice \(X^*(S)\), one has functorially \(S(A)=\operatorname{Hom}_{\mathbb Z}(X^*(S),A^*)\) for every \(E\)-algebra \(A\).  
hypotheses_or_conditions_needed: \(T_K\) is split.  
where_hypotheses_are_checked: \(K\) was chosen as a splitting field.  
strength_used: Identification for \(A=K\) and \(A=K_w\).  
notes: Used to pass from torus points to homomorphisms from characters.

claim_id: L2  
proof_location: Section 2, first paragraph  
claim_or_fact_used: \(T(\mathbb Q)=T(K)^G\).  
source_status: standard background fact  
cited_label_or_name: Galois descent for affine schemes  
exact_statement_used: If \(E/F\) is finite Galois and \(Y\) is an affine \(F\)-scheme, then \(Y(F)=Y(E)^{\operatorname{Gal}(E/F)}\).  
hypotheses_or_conditions_needed: \(K/\mathbb Q\) finite Galois; \(T\) affine over \(\mathbb Q\).  
where_hypotheses_are_checked: \(K/\mathbb Q\) is chosen finite Galois; algebraic tori are affine algebraic groups.  
strength_used: Equality on rational points.  
notes: Used for the global Hom description.

claim_id: L3  
proof_location: Section 2, first paragraph  
claim_or_fact_used: Fixed homomorphisms under the induced Galois action are exactly equivariant homomorphisms.  
source_status: proved inside the current proof  
cited_label_or_name: Equivariance computation  
exact_statement_used: Under \((g\varphi)(\chi)=g(\varphi(g^{-1}\chi))\), the condition \(g\varphi=\varphi\) is equivalent to \(\varphi(g\chi)=g\varphi(\chi)\).  
hypotheses_or_conditions_needed: Standard descent action on \(X\) and natural Galois action on \(K^*\).  
where_hypotheses_are_checked: Defined in the proof.  
strength_used: Identifies \(T(K)^G\) with \(\operatorname{Hom}_G(X,K^*)\).  
notes: Same argument used locally for \(D\).

claim_id: L4  
proof_location: Section 2, second paragraph  
claim_or_fact_used: \(K_w/\mathbb Q_p\) is finite Galois with Galois group the decomposition group \(D\).  
source_status: standard background fact  
cited_label_or_name: Completion and decomposition group for a Galois extension  
exact_statement_used: If \(K/\mathbb Q\) is finite Galois and \(w\mid p\), then \(K_w/\mathbb Q_p\) is finite Galois and \(\operatorname{Gal}(K_w/\mathbb Q_p)\cong D_w\).  
hypotheses_or_conditions_needed: \(K/\mathbb Q\) finite Galois; \(w\mid p\).  
where_hypotheses_are_checked: Fixed at the start of the subproof.  
strength_used: Allows local Galois descent with group \(D\).  
notes: Also ensures \(K_w\) is a local splitting field.

claim_id: L5  
proof_location: Section 2, second paragraph  
claim_or_fact_used: \(T(\mathbb Q_p)=T(K_w)^D\).  
source_status: standard background fact  
cited_label_or_name: Local Galois descent for affine schemes  
exact_statement_used: If \(L/F\) is finite Galois and \(Y\) is affine over \(F\), then \(Y(F)=Y(L)^{\operatorname{Gal}(L/F)}\).  
hypotheses_or_conditions_needed: \(L=K_w\), \(F=\mathbb Q_p\), \(L/F\) finite Galois, \(T\) affine.  
where_hypotheses_are_checked: L4 and the fact that tori are affine.  
strength_used: Equality on local points.  
notes: Used for the local Hom description.

claim_id: L6  
proof_location: Section 2, definition of \(\nu_T\)  
claim_or_fact_used: The valuation \(v_w\) is invariant under \(D\), and \(v_w(L^*)=\mathbb Z\) with kernel \(\mathcal O_L^*\).  
source_status: standard background fact  
cited_label_or_name: Galois invariance of normalized valuation on a local field  
exact_statement_used: For a finite Galois extension \(L/F\), every \(d\in\operatorname{Gal}(L/F)\) preserves the normalized valuation on \(L\).  
hypotheses_or_conditions_needed: \(L/F\) finite Galois.  
where_hypotheses_are_checked: L4.  
strength_used: Proves \(\nu_T(t)\in\operatorname{Hom}_D(X,\mathbb Z)\) and identifies the valuation-zero subgroup with \(\mathcal O_L^*\).  
notes: Load-bearing for C2.

claim_id: L7  
proof_location: Section 2, compactness of \(\ker(\nu_T)\)  
claim_or_fact_used: \(\mathcal O_L^*\) is compact.  
source_status: standard background fact  
cited_label_or_name: Compactness of the unit group of a nonarchimedean local field  
exact_statement_used: If \(L\) is a finite extension of \(\mathbb Q_p\), then its valuation ring \(\mathcal O_L\) is compact and \(\mathcal O_L^*\) is a closed compact subgroup.  
hypotheses_or_conditions_needed: \(L=K_w\) finite over \(\mathbb Q_p\).  
where_hypotheses_are_checked: L4.  
strength_used: Shows \(\operatorname{Hom}_D(X,\mathcal O_L^*)\) is compact.  
notes: Uses finite rank of \(X\).

claim_id: L8  
proof_location: Section 2, maximality argument  
claim_or_fact_used: A compact subgroup of a discrete torsion-free abelian group is trivial.  
source_status: proved inside the current proof  
cited_label_or_name: Compact-discrete torsion-free argument  
exact_statement_used: The continuous image of a compact group in a discrete group is finite; a finite subgroup of a torsion-free abelian group is zero.  
hypotheses_or_conditions_needed: \(\operatorname{Hom}_D(X,\mathbb Z)\) is discrete and torsion-free.  
where_hypotheses_are_checked: It is a subgroup of \(\operatorname{Hom}_{\mathbb Z}(X,\mathbb Z)\), a free abelian group.  
strength_used: Shows every compact subgroup of \(T(\mathbb Q_p)\) lies in \(\ker(\nu_T)\).  
notes: This proves maximality.

claim_id: L9  
proof_location: Section 2, final paragraph  
claim_or_fact_used: \(T(\mathbb Z_p)\) denotes the maximal compact subgroup of \(T(\mathbb Q_p)\).  
source_status: provided definition / notation / assumption  
cited_label_or_name: Packet notation for \(T(\mathbb Z_p)\)  
exact_statement_used: \(T(\mathbb Z_p)\) denotes the maximal compact subgroup of \(T(\mathbb Q_p)\).  
hypotheses_or_conditions_needed: \(T\) a \(\mathbb Q\)-torus and \(p\) a prime.  
where_hypotheses_are_checked: Given in the target setup.  
strength_used: Identifies the proved maximal compact subgroup \(\ker(\nu_T)\) with \(T(\mathbb Z_p)\).  
notes: No integral model interpretation is used.

5. Interface notes for S6

what this subproof establishes: C1 and C2. It gives the global and local character-lattice descriptions and proves that the local character-valuation kernel is exactly \(T(\mathbb Z_p)\).

what remains conditional: The target theorem still requires C3, C4, and C5. This subproof does not construct rational points matching prescribed valuations.

failure_output_type: solved

candidate guidance sentence, if any: None.

auxiliary lemma candidate, if any: None.

notation introduced: \(F=\mathbb Q_p\), \(L=K_w\), \(G=\operatorname{Gal}(K/\mathbb Q)\), \(D=\operatorname{Gal}(K_w/\mathbb Q_p)\), \(X=X^*(T_K)\), \(\nu_T\).

risk points: The equality \(T(\mathbb Z_p)=\ker(\nu_T)\) uses \(T(\mathbb Z_p)\) only as the maximal compact subgroup, not as points of a chosen integral model. The Hom descriptions depend on the standard Galois action convention on characters.

6. Web-source confirmation

no web sources used