1. Assignment restatement

Manager-ID: SS1

work_scope: global_solution

assigned subclaim(s): SC1-SC5 and CC003/CC004/CC007/CC008

what must be proved: For every algebraic torus \(T/\mathbf Q\) and every prime \(p\),
\[
T(\mathbf Q_p)=T(\mathbf Z_p)T(\mathbf Q),
\]
where \(T(\mathbf Z_p)\) is the maximal compact subgroup of \(T(\mathbf Q_p)\).

connection to the exact target: This is exactly the target theorem.

inferred_standard_setup_for_this_assignment: An algebraic torus over \(\mathbf Q\) is split by some finite Galois extension \(E/\mathbf Q\). If \(Y=X_*(T_E)\), then
\[
T(\mathbf Q)=(Y\otimes E^\times)^\Gamma
\]
for \(\Gamma=\mathrm{Gal}(E/\mathbf Q)\), and after choosing \(w\mid p\), with \(L=E_w\), \(D=\Gamma_w\),
\[
T(\mathbf Q_p)\simeq (Y\otimes L^\times)^D.
\]
The tensor notation is the usual multiplicative one for split tori.

where this result is used in the final solution: The whole argument is the final candidate solution.

declared prerequisite subclaims: Standard weak approximation for number fields; standard Galois descent description of torus points over a splitting field; standard local Nakayama/Tate-Nakayama valuation theorem for tori over nonarchimedean local fields.

2. Subproof or failure

<!-- BEGIN_FINAL_PROOF -->

Let \(E/\mathbf Q\) be a finite Galois extension splitting \(T\). Put
\[
\Gamma=\mathrm{Gal}(E/\mathbf Q),\qquad Y=X_*(T_E).
\]
Then Galois descent gives
\[
T(\mathbf Q)=(Y\otimes E^\times)^\Gamma.
\]
Choose a place \(w\) of \(E\) above \(p\), set \(L=E_w\), \(F=\mathbf Q_p\), and let \(D=\Gamma_w=\mathrm{Gal}(L/F)\). Since
\[
E\otimes_{\mathbf Q}\mathbf Q_p\simeq \prod_{\Gamma/D} L,
\]
Shapiro descent identifies
\[
T(F)=T(\mathbf Q_p)\simeq (Y\otimes L^\times)^D.
\]

Let \(\operatorname{ord}_L\) be normalized by \(\operatorname{ord}_L(\pi_L)=1\). Define
\[
\nu_L:(Y\otimes L^\times)^D\longrightarrow Y^D,\qquad
\nu_L\Bigl(\sum_i y_i\otimes a_i\Bigr)=\sum_i \operatorname{ord}_L(a_i)y_i.
\]
Its kernel is
\[
(Y\otimes \mathcal O_L^\times)^D,
\]
which is compact. Since the image of \(\nu_L\) lies in the free abelian group \(Y^D\), every compact subgroup of \((Y\otimes L^\times)^D\) maps trivially under \(\nu_L\). Hence this kernel is the maximal compact subgroup of \(T(F)\). Thus, under the above identification,
\[
T(\mathbf Z_p)=\ker \nu_L.
\]

We use the standard local Nakayama valuation theorem. For a finite Galois extension \(L/F\), group \(D=\mathrm{Gal}(L/F)\), and any \(D\)-lattice \(Y\),
\[
\nu_L\bigl((Y\otimes L^\times)^D\bigr)
=
\sum_{H\le D} e(L/L^H)\,N_{D/H}(Y^H),
\]
where
\[
N_{D/H}(y)=\sum_{\sigma\in D/H}\sigma y.
\]
The inclusion from right to left is elementary: if \(y\in Y^H\) and \(a\in (L^H)^\times\) has \(\operatorname{ord}_L(a)=e(L/L^H)\), then
\[
\sum_{\sigma\in D/H}\sigma(y\otimes a)
\]
is \(D\)-fixed and has valuation \(e(L/L^H)N_{D/H}(y)\). The reverse inclusion is the usual Nakayama/Tate-Nakayama valuation lemma applied to the exact sequence
\[
1\to \mathcal O_L^\times\to L^\times\xrightarrow{\operatorname{ord}_L}\mathbf Z\to 0.
\]

Now take arbitrary \(t\in T(\mathbf Q_p)\), viewed as an element of \((Y\otimes L^\times)^D\). Put
\[
v=\nu_L(t).
\]
By the local valuation formula,
\[
v=\sum_j n_j\, e(L/L^{H_j})\,N_{D/H_j}(y_j)
\]
for some subgroups \(H_j\le D\), integers \(n_j\), and \(y_j\in Y^{H_j}\).

We show that each summand is the local valuation of a rational point of \(T\). Fix \(H\le D\) and \(y\in Y^H\). Let \(K=E^H\), and let \(w_H\) be the place of \(K\) below \(w\). By weak approximation in the number field \(K\), choose \(a\in K^\times\) such that
\[
\operatorname{ord}_{w_H}(a)=1
\]
and such that \(a\) is a unit at every other place of \(K\) above \(p\). Since \(w\) is the unique place of \(E\) above \(w_H\) for the extension \(E/K\), we have
\[
\operatorname{ord}_L(a)=e(L/L^H).
\]

Define
\[
q_{H,y,a}=\sum_{\gamma\in \Gamma/H}\gamma(y\otimes a)\in Y\otimes E^\times.
\]
Because \(y\otimes a\) is \(H\)-fixed, this element is well-defined and \(\Gamma\)-fixed. Hence
\[
q_{H,y,a}\in (Y\otimes E^\times)^\Gamma=T(\mathbf Q).
\]
Its \(w\)-local valuation is
\[
\nu_L(q_{H,y,a})=
e(L/L^H)\sum_{\delta\in D/H}\delta y
=
e(L/L^H)N_{D/H}(y).
\]
Indeed, among the cosets \(\gamma H\in \Gamma/H\), only those with \(\gamma\in D\) contribute to the valuation at \(w\); all other terms are units at \(w\) by the choice of \(a\).

Taking the product of the corresponding \(q_{H_j,y_j,a_j}^{\,n_j}\), we obtain an element \(q\in T(\mathbf Q)\) such that
\[
\nu_L(q)=v=\nu_L(t).
\]
Therefore
\[
\nu_L(tq^{-1})=0,
\]
so \(tq^{-1}\in \ker\nu_L=T(\mathbf Z_p)\). Thus
\[
t\in T(\mathbf Z_p)T(\mathbf Q).
\]
Since \(t\in T(\mathbf Q_p)\) was arbitrary, this proves
\[
T(\mathbf Q_p)=T(\mathbf Z_p)T(\mathbf Q).
\]

<!-- END_FINAL_PROOF -->

3. Solver failure output and candidate guidance

```yaml
failure_output_type: solved
main_solver_proof_key: true
type: ""
failed_route: ""
obstruction: ""
evidence: ""
reuse_value: ""
guidance_sentence: null
source_gap: false
external_material_status: not_applicable
autonomous_derivation_possible: true
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
proof_location: final proof, opening descent setup  
claim_or_fact_used: \(T(\mathbf Q)=(Y\otimes E^\times)^\Gamma\) and \(T(\mathbf Q_p)\simeq (Y\otimes L^\times)^D\)  
source_status: standard background fact  
cited_label_or_name: Galois descent for split tori / Shapiro identification  
exact_statement_used: Rational points of a torus split by \(E\) are the Galois-fixed points of the split torus over \(E\).  
hypotheses_or_conditions_needed: \(E/\mathbf Q\) finite Galois splitting field; \(w\mid p\); \(D=\Gamma_w\).  
where_hypotheses_are_checked: chosen at proof start.  
strength_used: exact identification of global and local point groups.  
notes: standard torus descent.

claim_id: L2  
proof_location: valuation-map paragraph  
claim_or_fact_used: \(\ker\nu_L=(Y\otimes\mathcal O_L^\times)^D\) is the maximal compact subgroup  
source_status: proved inside the current proof  
cited_label_or_name: maximal compact kernel of valuation  
exact_statement_used: compact subgroups map trivially to a discrete torsion-free group.  
hypotheses_or_conditions_needed: \(Y\) free abelian; \(\mathcal O_L^\times\) compact.  
where_hypotheses_are_checked: local setup.  
strength_used: identifies \(T(\mathbf Z_p)\) with \(\ker\nu_L\).  
notes: establishes CC003 kernel part.

claim_id: L3  
proof_location: local valuation formula paragraph  
claim_or_fact_used: Nakayama valuation formula  
source_status: standard background fact  
cited_label_or_name: local Nakayama / Tate-Nakayama valuation theorem  
exact_statement_used:
\[
\nu_L((Y\otimes L^\times)^D)=\sum_{H\le D} e(L/L^H)N_{D/H}(Y^H).
\]
hypotheses_or_conditions_needed: \(L/F\) finite Galois, \(Y\) a \(D\)-lattice.  
where_hypotheses_are_checked: \(L=E_w\), \(F=\mathbf Q_p\), \(D=\Gamma_w\).  
strength_used: full reverse and forward local image identification.  
notes: this resolves CC008 only if the Manager accepts local Nakayama/Tate-Nakayama as standard background.

claim_id: L4  
proof_location: construction of \(a\in(E^H)^\times\)  
claim_or_fact_used: weak approximation in a number field with prescribed valuations at finitely many places  
source_status: standard background fact  
cited_label_or_name: weak approximation for number fields  
exact_statement_used: one can choose \(a\in K^\times\) with valuation \(1\) at one selected finite place and valuation \(0\) at the other places above \(p\).  
hypotheses_or_conditions_needed: \(K=E^H\) a number field; finitely many places above \(p\).  
where_hypotheses_are_checked: construction paragraph.  
strength_used: realizes each local valuation generator globally.  
notes: avoids class-group obstruction because valuations are prescribed only at finitely many completions.

claim_id: L5  
proof_location: construction of \(q_{H,y,a}\)  
claim_or_fact_used: \(\Gamma\)-trace/norm construction gives a rational point  
source_status: proved inside the current proof  
cited_label_or_name: global norm construction  
exact_statement_used: if \(y\otimes a\) is \(H\)-fixed, then \(\sum_{\gamma\in\Gamma/H}\gamma(y\otimes a)\) is \(\Gamma\)-fixed.  
hypotheses_or_conditions_needed: \(y\in Y^H\), \(a\in(E^H)^\times\).  
where_hypotheses_are_checked: construction paragraph.  
strength_used: produces \(q\in T(\mathbf Q)\) with prescribed local valuation.  
notes: establishes CC004 and CC007.

critical_claim_id: CC003  
claim: local quotient identified with normalized valuation/cocharacter lattice  
claim_basis: derived_here plus standard_background  
exact_statement_used: \(T(\mathbf Q_p)/T(\mathbf Z_p)\simeq \nu_L((Y\otimes L^\times)^D)\subseteq Y^D\).  
hypotheses_checked: \(E\) splits \(T\), \(L=E_w\), \(D=\Gamma_w\).  
normalization: \(\operatorname{ord}_L(\pi_L)=1\).  
local_source_location: proof paragraphs defining \(\nu_L\).  
competing_variants: \(F\)-normalized valuation rescales ramification coefficients.  
status: ESTABLISHED

critical_claim_id: CC004  
claim: every local quotient class is represented by \(T(\mathbf Q)\)  
claim_basis: derived_here  
exact_statement_used: each generator \(e(L/L^H)N_{D/H}(y)\) is realized by \(q_{H,y,a}\in T(\mathbf Q)\).  
hypotheses_checked: local valuation formula and weak approximation in \(E^H\).  
normalization: \(\operatorname{ord}_L(a)=e(L/L^H)\).  
local_source_location: global realization paragraph.  
competing_variants: none.  
status: ESTABLISHED

critical_claim_id: CC007  
claim: class-group/principal-divisor obstruction in splitting field eliminated  
claim_basis: derived_here  
exact_statement_used: weak approximation in \(E^H\) gives elements with prescribed valuations at places above \(p\), allowing arbitrary valuations away from \(p\).  
hypotheses_checked: only finitely many places above \(p\).  
normalization: selected \(a\) has valuation \(1\) at \(w_H\) and \(0\) at other \(p\)-adic places.  
local_source_location: construction of \(a\).  
competing_variants: no need to prescribe a principal ideal supported only above \(p\).  
status: ESTABLISHED

critical_claim_id: CC008  
claim: local valuation image formula  
claim_basis: standard_background  
exact_statement_used:
\[
\operatorname{im}(\nu_L)=\sum_{H\le D} e(L/L^H)N_{D/H}(Y^H).
\]
hypotheses_checked: \(L/F\) finite Galois; \(Y\) a \(D\)-lattice.  
normalization: \(\operatorname{ord}_L(\pi_L)=1\).  
local_source_location: local valuation formula paragraph.  
competing_variants: \(F\)-normalized valuation rescales the displayed subgroup.  
status: ESTABLISHED

Critical Claims Ledger addendum.

```yaml
critical_claim_id: CC008
claim: local valuation image formula for a torus split by a finite Galois local extension
claim_basis: standard_background
exact_statement_used: "For finite Galois L/F with D=Gal(L/F) and D-lattice Y, im((Y tensor L^x)^D -> Y^D)=sum_{H<=D} e(L/L^H) N_{D/H}(Y^H), using ord_L(pi_L)=1."
hypotheses_checked: "L=E_w over F=Q_p is finite Galois; Y=X_*(T_E) is a D-lattice."
normalization: "L-normalized valuation; ord_L(a)=e(L/L^H) for a uniformizer of L^H."
local_source_location: "Section 2, local valuation formula paragraph."
competing_variants: "F-normalized valuation rescales the ramification factors."
status: ESTABLISHED
```

5. Interface notes for Manager acceptance

what this subproof establishes: A complete candidate proof of the target theorem, reducing the local quotient to the Nakayama valuation image and then realizing every generator globally by weak approximation in \(E^H\).

what remains conditional: Acceptance depends on allowing the local Nakayama/Tate-Nakayama valuation theorem as standard background. The proof does not derive that theorem from first principles.

failure_output_type: solved

candidate guidance sentence, if any: none

auxiliary lemma candidate, if any: none beyond the standard local Nakayama valuation theorem explicitly stated above.

notation introduced: \(E,\Gamma,w,L,F,D,Y,\nu_L,H,N_{D/H}\).

risk points: The only serious risk is CC008 provenance. If Manager requires an elementary in-artifact proof of Nakayama’s valuation theorem, this candidate should be downgraded.

candidate_answer: The proof inside `BEGIN_FINAL_PROOF` / `END_FINAL_PROOF`.

complete_scratch_work_attempt: The route is descent to \((Y\otimes L^\times)^D\), identify maximal compact as valuation kernel, invoke local Nakayama valuation formula, and globally realize each transfer generator via weak approximation in \(E^H\).

uncertain_steps: None mathematically if local Nakayama/Tate-Nakayama is admitted as standard background; otherwise CC008 remains a source gap.

help_requests: If stricter self-containment is required, request a dedicated proof of the local Nakayama valuation theorem.

proposed_board_updates: Mark CC003, CC004, CC007 established. Mark CC008 established only under standard-background admission of local Nakayama/Tate-Nakayama.

6. Web-source confirmation

no web sources used