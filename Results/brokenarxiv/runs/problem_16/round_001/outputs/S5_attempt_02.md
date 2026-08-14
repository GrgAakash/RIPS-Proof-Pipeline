1. Assignment restatement

S-ID: S5

assigned subclaim(s):
Final consistency audit for the proof strategy: auxiliary choices of splitting field \(K\) and place \(w\mid p\), ramified and split cases, and the use of \(T(\mathbb Z_p)\).

what must be proved:
The planned argument, if the earlier mathematical subclaims are supplied independently, has no hidden dependence on \(K\) or \(w\), does not exclude ramified or split cases, and uses \(T(\mathbb Z_p)\) only in the target’s stated sense: the maximal compact subgroup of \(T(\mathbb Q_p)\).

declared prerequisite subclaims:
None for the audit itself. For insertion into the full proof, C1-C4/C5 remain external prerequisites and are not proved here.

2. Subproof or failure

Fix an algebraic closure of \(\mathbb Q\). If \(K\) and \(K'\) are two finite Galois splitting fields for \(T\), their compositum \(M=KK'\) is again finite Galois over \(\mathbb Q\) and splits \(T\). The character lattice is intrinsic after base change:
\[
X^*(T_K)\cong X^*(T_M)\cong X^*(T_{\overline{\mathbb Q}}),
\]
with only the finite Galois group through which the action is recorded changing.

Let \(w\mid p\) be a place of \(K\), and let \(u\mid w\) be a place of \(M\). For normalized additive valuations,
\[
v_u(x)=e(u/w)v_w(x)\qquad (x\in K_w^*),
\]
where \(e(u/w)>0\). Hence zero valuation conditions and equality of two valuations are unchanged after passing from \(K_w\) to \(M_u\). Therefore conditions such as
\[
v_w(\chi(a))=v_w(\chi(b))\quad\text{for all }\chi
\]
or
\[
v_w(\chi(a b^{-1}))=0\quad\text{for all }\chi
\]
are equivalent to the corresponding conditions over \(M_u\). Since any two choices of splitting field are compared through such an \(M\), the valuation criterion used in the planned proof is independent of the chosen splitting field.

Now fix \(K\), and compare two primes \(w,w'\mid p\). Because \(K/\mathbb Q\) is Galois, \(w'=gw\) for some \(g\in G=\mathrm{Gal}(K/\mathbb Q)\), and the decomposition groups satisfy
\[
D_{w'}=gD_wg^{-1}.
\]
The automorphism \(g\) induces an isomorphism of completions \(K_w\cong K_{w'}\), and normalized valuations satisfy
\[
v_{w'}(g a)=v_w(a).
\]
Under the corresponding relabeling of characters by the \(G\)-action, a \(D_w\)-equivariant local character-value homomorphism is carried to a \(D_{w'}\)-equivariant one. Since \(g\) acts bijectively on the character lattice, “for every character” valuation equalities and zero-valuation conditions are preserved. Thus the proof does not depend on the selected prime \(w\mid p\).

Ramification causes no exceptional case. The only valuation facts used above are valid for every finite extension of \(p\)-adic fields: the valuation ring exists, the value group is \(\mathbb Z\) after normalization, restriction of valuations scales by the positive ramification index, and field automorphisms preserve valuation. Inertia is already contained in the decomposition group \(D\), so no unramifiedness assumption is hidden.

The split case is also compatible. If \(T\) is split over \(\mathbb Q\), one may take \(K=\mathbb Q\), \(D=1\), and \(T\cong \mathbb G_m^r\). Then
\[
T(\mathbb Q_p)\cong (\mathbb Q_p^*)^r,\qquad
T(\mathbb Q)\cong (\mathbb Q^*)^r,
\]
and the maximal compact subgroup is \((\mathbb Z_p^*)^r\). Since every \(x\in\mathbb Q_p^*\) has \(x=u p^n\) with \(u\in\mathbb Z_p^*\) and \(p^n\in\mathbb Q^*\), the planned statement specializes to the usual coordinatewise decomposition.

Finally, \(T(\mathbb Z_p)\) is not being used as the \(\mathbb Z_p\)-points of a chosen integral model. In this packet it is notation for the maximal compact subgroup of \(T(\mathbb Q_p)\). The planned proof only needs that subgroup after a valuation-kernel identification has been separately proved; afterward it uses only subgroup membership inside \(T(\mathbb Q_p)\) and the natural inclusion \(T(\mathbb Q)\subset T(\mathbb Q_p)\).

Thus the consistency audit is solved.

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
proof_location: Section 2, paragraph 1  
claim_or_fact_used: Common refinement of splitting fields.  
source_status: standard background fact  
cited_label_or_name: Compositum of finite Galois splitting fields  
exact_statement_used: If \(K,K'/\mathbb Q\) are finite Galois splitting fields for \(T\), then \(KK'/\mathbb Q\) is finite Galois and also splits \(T\).  
hypotheses_or_conditions_needed: \(K,K'\) finite Galois over \(\mathbb Q\), both split \(T\).  
where_hypotheses_are_checked: Section 2, first sentence.  
strength_used: Only existence of a common finite Galois splitting refinement.  
notes: Does not use the target theorem.

claim_id: L2  
proof_location: Section 2, paragraph 1  
claim_or_fact_used: Character lattices are preserved under extension of a splitting field.  
source_status: standard background fact  
cited_label_or_name: Base change of characters for split tori  
exact_statement_used: If \(L/K\) and \(T_K\) is split, then base change identifies \(X^*(T_K)\) with \(X^*(T_L)\).  
hypotheses_or_conditions_needed: \(T_K\) split.  
where_hypotheses_are_checked: \(K\) is chosen as a splitting field.  
strength_used: Identification of the same intrinsic character lattice.  
notes: Used only for choice-independence.

claim_id: L3  
proof_location: Section 2, paragraph 2  
claim_or_fact_used: Valuation scaling under finite local extension.  
source_status: standard background fact  
cited_label_or_name: Ramification index formula for normalized valuations  
exact_statement_used: For \(M_u/K_w\), \(v_u(x)=e(u/w)v_w(x)\) for \(x\in K_w^*\).  
hypotheses_or_conditions_needed: \(M_u/K_w\) finite extension of discretely valued local fields.  
where_hypotheses_are_checked: \(u\mid w\) over finite number fields.  
strength_used: Preservation of equality and zero valuation because \(e(u/w)>0\).  
notes: Handles ramified extensions as well.

claim_id: L4  
proof_location: Section 2, paragraph 3  
claim_or_fact_used: Galois group acts transitively on primes above \(p\).  
source_status: standard background fact  
cited_label_or_name: Transitivity of primes in a finite Galois extension  
exact_statement_used: If \(K/\mathbb Q\) is finite Galois and \(w,w'\mid p\), then \(w'=gw\) for some \(g\in\mathrm{Gal}(K/\mathbb Q)\).  
hypotheses_or_conditions_needed: \(K/\mathbb Q\) finite Galois.  
where_hypotheses_are_checked: Setup of the proof.  
strength_used: Comparison of choices of \(w\).  
notes: No arithmetic approximation theorem involved.

claim_id: L5  
proof_location: Section 2, paragraph 3  
claim_or_fact_used: Conjugacy of decomposition groups.  
source_status: standard background fact  
cited_label_or_name: Decomposition group conjugacy  
exact_statement_used: If \(w'=gw\), then \(D_{w'}=gD_wg^{-1}\).  
hypotheses_or_conditions_needed: \(K/\mathbb Q\) finite Galois, \(w'=gw\).  
where_hypotheses_are_checked: Section 2, paragraph 3.  
strength_used: Compatibility of \(D\)-equivariance under changing \(w\).  
notes: Used only for audit.

claim_id: L6  
proof_location: Section 2, paragraph 3  
claim_or_fact_used: Valuations are transported by field automorphisms.  
source_status: standard background fact  
cited_label_or_name: Transport of valuations by a Galois automorphism  
exact_statement_used: If \(w'=gw\), then \(v_{w'}(ga)=v_w(a)\).  
hypotheses_or_conditions_needed: \(g\in\mathrm{Gal}(K/\mathbb Q)\), \(a\in K_w^*\).  
where_hypotheses_are_checked: Section 2, paragraph 3.  
strength_used: Preservation of valuation equalities under changing \(w\).  
notes: Applies equally in ramified cases.

claim_id: L7  
proof_location: Section 2, paragraph 5  
claim_or_fact_used: Split torus coordinate description.  
source_status: standard background fact  
cited_label_or_name: Points of a split torus  
exact_statement_used: If \(T\cong\mathbb G_m^r\) over \(F\), then \(T(F)\cong(F^*)^r\).  
hypotheses_or_conditions_needed: \(T\) split over \(F\).  
where_hypotheses_are_checked: Split-case audit assumes \(T\) split over \(\mathbb Q\).  
strength_used: Coordinatewise verification.  
notes: Only confirms compatibility with the easy case.

claim_id: L8  
proof_location: Section 2, paragraph 5  
claim_or_fact_used: Multiplicative decomposition of \(\mathbb Q_p^*\).  
source_status: proved inside the current proof  
cited_label_or_name: \(p\)-adic unit decomposition  
exact_statement_used: Every \(x\in\mathbb Q_p^*\) can be written \(x=u p^n\), with \(u\in\mathbb Z_p^*\) and \(n\in\mathbb Z\).  
hypotheses_or_conditions_needed: \(x\neq 0\).  
where_hypotheses_are_checked: \(x\in\mathbb Q_p^*\).  
strength_used: Coordinatewise split-case factorization.  
notes: Immediate from the normalized \(p\)-adic valuation.

claim_id: L9  
proof_location: Section 2, final paragraph  
claim_or_fact_used: Meaning of \(T(\mathbb Z_p)\).  
source_status: provided definition / notation / assumption  
cited_label_or_name: Target theorem notation  
exact_statement_used: \(T(\mathbb Z_p)\) denotes the maximal compact subgroup of \(T(\mathbb Q_p)\).  
hypotheses_or_conditions_needed: \(T\) a \(\mathbb Q\)-torus and \(p\) a prime.  
where_hypotheses_are_checked: Target theorem.  
strength_used: Only the subgroup meaning, not integral-model points.  
notes: This is central to the notation audit.

claim_id: L10  
proof_location: Section 2, final paragraph  
claim_or_fact_used: Natural inclusion of rational points into local points.  
source_status: standard background fact  
cited_label_or_name: Functoriality of points  
exact_statement_used: The field embedding \(\mathbb Q\hookrightarrow\mathbb Q_p\) induces \(T(\mathbb Q)\to T(\mathbb Q_p)\).  
hypotheses_or_conditions_needed: \(T\) is a \(\mathbb Q\)-group.  
where_hypotheses_are_checked: Target theorem.  
strength_used: Product \(T(\mathbb Z_p)T(\mathbb Q)\) inside \(T(\mathbb Q_p)\).  
notes: No injectivity issue is needed beyond the usual separatedness of algebraic groups over fields.

5. Interface notes for S6

what this subproof establishes:
The auxiliary choices \(K\) and \(w\) do not affect the valuation equalities or compact-membership criterion used by the planned proof. Ramified and split cases are covered. \(T(\mathbb Z_p)\) is used only as the maximal compact subgroup.

what remains conditional:
The actual proofs of C1, C2, C3, C4, and the assembly C5.

failure_output_type:
solved

candidate guidance sentence, if any:
None.

auxiliary lemma candidate, if any:
None.

notation introduced:
\(M=KK'\), \(u\mid w\), \(e(u/w)\), \(D_w\).

risk points:
The audit does not prove the equivariant valuation lifting lemma C3 or the valuation-kernel statement C2; those must be supplied elsewhere.

6. Web-source confirmation

no web sources used