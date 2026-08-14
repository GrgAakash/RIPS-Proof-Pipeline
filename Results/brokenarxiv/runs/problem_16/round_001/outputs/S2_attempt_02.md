1. Assignment restatement

S-ID: S2

assigned subclaim(s): C3

what must be proved:  
Given a finite Galois splitting field \(K/\mathbb Q\), \(G=\mathrm{Gal}(K/\mathbb Q)\), a place \(w\mid p\), decomposition group \(D\), and finite free \(G\)-lattice \(X=X^*(T_K)\), prove that for every \(t\in T(\mathbb Q_p)=\mathrm{Hom}_D(X,K_w^*)\), the valuation homomorphism
\[
\lambda_t:X\to \mathbb Z,\qquad \lambda_t(\chi)=v_w(\chi(t))
\]
is realized by some \(q\in T(\mathbb Q)=\mathrm{Hom}_G(X,K^*)\), i.e.
\[
v_w(\chi(q))=v_w(\chi(t))
\quad\text{for all }\chi\in X.
\]

declared prerequisite subclaims:  
C1 is needed for the identifications \(T(\mathbb Q)=\mathrm{Hom}_G(X,K^*)\) and \(T(\mathbb Q_p)=\mathrm{Hom}_D(X,K_w^*)\). No other solver result is assumed.

2. Subproof or failure

SUBPROBLEM UNSOLVED.

The missing obstacle is the exact equivariant lifting step:
\[
\operatorname{Im}\!\left(\mathrm{Hom}_G(X,K^*)\xrightarrow{v_w}
\mathrm{Hom}_D(X,\mathbb Z)\right)
=
\operatorname{Im}\!\left(\mathrm{Hom}_D(X,K_w^*)\xrightarrow{v_w}
\mathrm{Hom}_D(X,\mathbb Z)\right).
\]
The allowed number-field valuation flexibility gives nonequivariant elements of \(K^*\) with prescribed valuations at selected primes, but it does not by itself force the multiplicative homomorphism \(X\to K^*\) to be \(G\)-equivariant.

A tempting stronger route is false: one cannot prove that every element of \(\mathrm{Hom}_D(X,\mathbb Z)\) lifts globally. For example, take \(X=\mathbb Z\) with trivial \(G\)-action, corresponding to \(\mathbb G_m\), and choose a Galois extension \(K/\mathbb Q\) ramified at \(p\) with ramification index \(e>1\) at \(w\). Then
\[
\mathrm{Hom}_D(X,\mathbb Z)\cong \mathbb Z.
\]
But
\[
\mathrm{Hom}_G(X,K^*)=(K^*)^G=\mathbb Q^*,
\]
and for every \(a\in\mathbb Q^*\),
\[
v_w(a)=e\,v_p(a)\in e\mathbb Z.
\]
Thus the valuation \(1\in \mathbb Z\) is \(D\)-invariant but cannot be globally lifted. This shows that the condition “arising from a local \(D\)-equivariant homomorphism \(X\to K_w^*\)” is essential. In the same example, the local \(D\)-equivariant points are \((K_w^*)^D=\mathbb Q_p^*\), whose \(w\)-valuations are also exactly \(e\mathbb Z\).

I do not have, from the supplied packet and permitted standard tools alone, a rigorous proof of the exact image equality above for arbitrary finite free \(G\)-lattices \(X\).

3. Solver failure output and candidate guidance

```yaml
failure_output_type: forbidden-route / obstruction guidance
type: false strengthening
failed_route: "Prove that every D-invariant valuation homomorphism X -> Z is globally realizable by a G-equivariant homomorphism X -> K^*."
obstruction: "This stronger statement ignores ramification divisibility constraints and is false even for the split torus G_m when the chosen auxiliary splitting field K/Q is ramified at p."
evidence: "Let X=Z with trivial G-action and let K/Q be Galois ramified at p with ramification index e>1. Then Hom_D(X,Z)=Z, but Hom_G(X,K^*)=Q^*, and v_w(Q^*)=eZ. Hence the D-invariant valuation 1 cannot be lifted globally. It is also not locally arising from Hom_D(X,K_w^*)=(K_w^*)^D=Q_p^*, whose w-valuations are eZ."
reuse_value: "Prevents later solvers from replacing the required 'locally arising' image equality by the false surjectivity onto all Hom_D(X,Z)."
guidance_sentence: "Keep the locally arising hypothesis throughout; the needed statement is equality of the global and local valuation images, not surjectivity onto all D-invariant integer homomorphisms."
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
proof_location: Section 1  
claim_or_fact_used: Character-lattice interpretations of rational and local points.  
source_status: allowed supporting statement  
cited_label_or_name: C1 prerequisite  
exact_statement_used: With \(K/\mathbb Q\) finite Galois splitting \(T\), \(G=\mathrm{Gal}(K/\mathbb Q)\), \(w\mid p\), and \(D\) the decomposition group, \(T(\mathbb Q)=\mathrm{Hom}_G(X,K^*)\) and \(T(\mathbb Q_p)=\mathrm{Hom}_D(X,K_w^*)\).  
hypotheses_or_conditions_needed: \(K\) splits \(T\); \(X=X^*(T_K)\); \(D\) is the decomposition group at \(w\).  
where_hypotheses_are_checked: Assignment restatement.  
strength_used: Full identification.  
notes: Declared as prerequisite, not reproved.

claim_id: L2  
proof_location: Section 2, counterexample  
claim_or_fact_used: For \(X=\mathbb Z\) with trivial \(G\)-action, \(\mathrm{Hom}_G(X,K^*)=(K^*)^G=\mathbb Q^*\).  
source_status: standard background fact  
cited_label_or_name: Fixed points of a finite Galois extension  
exact_statement_used: If \(K/\mathbb Q\) is Galois with group \(G\), then \((K^*)^G=\mathbb Q^*\).  
hypotheses_or_conditions_needed: \(K/\mathbb Q\) finite Galois.  
where_hypotheses_are_checked: Counterexample setup.  
strength_used: Exact equality of fixed multiplicative groups.  
notes: Standard Galois theory.

claim_id: L3  
proof_location: Section 2, counterexample  
claim_or_fact_used: Valuation scaling under ramification.  
source_status: standard background fact  
cited_label_or_name: Ramification index valuation formula  
exact_statement_used: If \(w\mid p\) in \(K/\mathbb Q\) has ramification index \(e\), then for \(a\in\mathbb Q^*\), \(v_w(a)=e\,v_p(a)\).  
hypotheses_or_conditions_needed: \(v_w\) normalized on \(K_w\); \(v_p\) normalized on \(\mathbb Q_p\).  
where_hypotheses_are_checked: Counterexample setup.  
strength_used: Shows \(v_w(\mathbb Q^*)=e\mathbb Z\).  
notes: Standard valuation theory.

claim_id: L4  
proof_location: Section 2, counterexample  
claim_or_fact_used: Local fixed field under the decomposition group.  
source_status: standard background fact  
cited_label_or_name: Local Galois fixed field  
exact_statement_used: For \(K_w/\mathbb Q_p\) with decomposition group \(D\), \((K_w^*)^D=\mathbb Q_p^*\).  
hypotheses_or_conditions_needed: \(D=\mathrm{Gal}(K_w/\mathbb Q_p)\).  
where_hypotheses_are_checked: Counterexample setup.  
strength_used: Identifies local \(D\)-equivariant points in the \(X=\mathbb Z\) case.  
notes: Standard local Galois theory.

claim_id: L5  
proof_location: Section 2  
claim_or_fact_used: The stronger statement “all of \(\mathrm{Hom}_D(X,\mathbb Z)\) lifts globally” is false.  
source_status: proved inside the current proof  
cited_label_or_name: false-strengthening counterexample  
exact_statement_used: For \(X=\mathbb Z\) trivial and ramified \(K/\mathbb Q\) at \(p\), the element \(1\in\mathrm{Hom}_D(X,\mathbb Z)\) cannot lie in the image of \(\mathrm{Hom}_G(X,K^*)\to\mathrm{Hom}_D(X,\mathbb Z)\).  
hypotheses_or_conditions_needed: \(e(w/p)>1\).  
where_hypotheses_are_checked: Counterexample setup.  
strength_used: Demonstrates obstruction to a tempting proof route.  
notes: This does not disprove C3 because \(1\) is not locally arising in this setup.

5. Interface notes for S6

what this subproof establishes:  
It establishes that the naive strengthening “every \(D\)-invariant valuation homomorphism lifts globally” is false, and that the “locally arising” hypothesis is essential.

what remains conditional:  
C3 itself remains unproved. The missing exact statement is equality of global and local valuation images.

failure_output_type:  
forbidden-route / obstruction guidance

candidate guidance sentence, if any:  
Keep the locally arising hypothesis throughout; the needed statement is equality of the global and local valuation images, not surjectivity onto all \(D\)-invariant integer homomorphisms.

auxiliary lemma candidate, if any:  
None supplied under the required priority rule, though the unresolved needed lemma is the global/local valuation image equality stated in Section 2.

notation introduced:  
\(\lambda_t(\chi)=v_w(\chi(t))\); \(e=e(w/p)\).

risk points:  
The S2 step cannot be completed by number-field prescribed valuations alone, because equivariance and ramification impose additional constraints.

6. Web-source confirmation

no web sources used