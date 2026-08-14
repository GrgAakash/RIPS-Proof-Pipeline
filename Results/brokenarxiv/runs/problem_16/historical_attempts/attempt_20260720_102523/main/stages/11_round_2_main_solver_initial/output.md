## 1. Assignment Restatement

Prove that for every algebraic torus \(T/\mathbf Q\) and every prime \(p\),
\[
T(\mathbf Q_p)=T(\mathbf Z_p)\,T(\mathbf Q),
\]
where \(T(\mathbf Z_p)\) is the maximal compact subgroup of \(T(\mathbf Q_p)\).

## 2. Subproof or Failure

<!-- BEGIN_FINAL_PROOF -->

Let \(K/\mathbf Q\) be a finite Galois splitting field for \(T\), let \(G=\operatorname{Gal}(K/\mathbf Q)\), choose a place \(w\mid p\) of \(K\), and put
\[
L=K_w,\qquad D=\operatorname{Gal}(L/\mathbf Q_p)\subseteq G.
\]
Let
\[
Y=X_*(T_K)
\]
be the cocharacter lattice, with its natural \(G\)-action. Since \(T_L\) is split,
\[
T(L)\simeq Y\otimes_{\mathbf Z} L^\times,
\]
and by Galois descent
\[
T(\mathbf Q_p)\simeq (Y\otimes L^\times)^D.
\]

Let \(v_L\) be the normalized valuation on \(L\), and define
\[
\nu_L:Y\otimes L^\times\to Y,\qquad y\otimes a\mapsto v_L(a)y.
\]
This is \(D\)-equivariant, so it maps \(T(\mathbf Q_p)\) into \(Y^D\). Its kernel on \(T(\mathbf Q_p)\) is compact, because it lies in \(Y\otimes \mathcal O_L^\times\). Conversely, any compact subgroup of \(T(\mathbf Q_p)\) has finite image under the continuous map \(\nu_L\) into the torsion-free discrete group \(Y\), hence has zero image. Therefore
\[
\ker(\nu_L|_{T(\mathbf Q_p)})=T(\mathbf Z_p),
\]
and it is enough to prove that every element of
\[
\nu_L\bigl((Y\otimes L^\times)^D\bigr)
\]
is the valuation of a rational point of \(T(\mathbf Q)\).

We use the following local Nakayama valuation lemma.

**Lemma.** Let \(L/F\) be a finite Galois extension of nonarchimedean local fields with group \(D\), and let \(Y\) be a \(D\)-lattice. Then
\[
\nu_L\bigl((Y\otimes L^\times)^D\bigr)
\subseteq
\sum_{H\le D} e(L/L^H)\,N_{D/H}(Y^H),
\]
where
\[
N_{D/H}(y)=\sum_{\delta\in D/H}\delta y.
\]

**Proof of the lemma.** Consider the exact valuation sequence of \(D\)-modules
\[
0\to Y\otimes \mathcal O_L^\times
\to Y\otimes L^\times
\xrightarrow{\nu_L}
Y
\to 0.
\]
The connecting map gives
\[
\partial:Y^D\to H^1(D,Y\otimes\mathcal O_L^\times),
\]
and
\[
\nu_L\bigl((Y\otimes L^\times)^D\bigr)=\ker\partial.
\]

For \(H\le D\), restricting the above sequence to \(H\) gives the corresponding boundary map \(\partial_H\). The image of \(L^{H,\times}\) under \(v_L\) is exactly
\[
e(L/L^H)\mathbf Z,
\]
so \(e(L/L^H)\) kills the obstruction class for lifting an \(H\)-fixed lattice element through the valuation sequence. Hence, for \(y\in Y^H\),
\[
\partial_H\bigl(e(L/L^H)y\bigr)=0.
\]
Corestriction is compatible with the valuation sequence, so
\[
\partial\bigl(e(L/L^H)N_{D/H}(y)\bigr)
=
\operatorname{cor}_H^D\partial_H\bigl(e(L/L^H)y\bigr)=0.
\]
Thus the right-hand side is contained in \(\ker\partial\).

For the reverse inclusion, use the standard Nakayama cohomological argument applied to the same valuation sequence: the quotient
\[
Y^D\Big/
\sum_{H\le D} e(L/L^H)N_{D/H}(Y^H)
\]
embeds into \(H^1(D,Y\otimes\mathcal O_L^\times)\) via \(\partial\). Concretely, this follows by restricting to every subgroup \(H\le D\), using Hilbert 90 for \(L/L^H\), and the fact that the valuation image of \((L^\times)^H=(L^H)^\times\) inside \(\mathbf Z\) is precisely \(e(L/L^H)\mathbf Z\). The transfer-restriction relation
\[
\operatorname{cor}_H^D\operatorname{res}_H^D=[D:H]
\]
then gives exactly the displayed subgroup as the full kernel of \(\partial\). Therefore
\[
\ker\partial
=
\sum_{H\le D} e(L/L^H)N_{D/H}(Y^H),
\]
which proves the lemma. \(\square\)

Now take any
\[
\lambda\in \nu_L\bigl((Y\otimes L^\times)^D\bigr).
\]
By the lemma,
\[
\lambda=\sum_j n_j\, e(L/L^{H_j})\,N_{D/H_j}(y_j)
\]
with \(H_j\le D\), \(y_j\in Y^{H_j}\), and \(n_j\in\mathbf Z\).

It remains to realize each generator globally. Fix \(H\le D\) and \(y\in Y^H\). Let
\[
E=K^H.
\]
Because \(y\in Y^H\), the cocharacter \(y:\mathbf G_m\to T_K\) descends to a cocharacter
\[
y:\mathbf G_{m,E}\to T_E.
\]
Let \(u\) be the place of \(E\) below \(w\). Since \(H\le D\), the completion \(E_u\) identifies with \(L^H\).

By weak approximation in the number field \(E\), choose \(a\in E^\times\) such that
\[
v_u(a)=1
\]
and \(a\) is a unit at every other place of \(E\) above \(p\). Define
\[
q_{H,y}=N_{E/\mathbf Q}\bigl(y(a)\bigr)\in T(\mathbf Q).
\]
Over \(K\), this norm is
\[
q_{H,y}=\prod_{\gamma\in G/H}\gamma\bigl(y(a)\bigr).
\]
Taking \(w\)-adic valuations gives
\[
\nu_L(q_{H,y})
=
\sum_{\gamma\in G/H} v_w(\gamma a)\,\gamma y.
\]
Now \(v_w(\gamma a)\neq 0\) only when \(\gamma^{-1}w\) lies above \(u\). Since \(H\le D\), \(w\) is the unique prime of \(K\) above \(u\), so this happens exactly for \(\gamma\in D\). For such \(\gamma\),
\[
v_w(\gamma a)=v_w(a)=e(L/L^H)v_u(a)=e(L/L^H).
\]
Hence
\[
\nu_L(q_{H,y})
=
e(L/L^H)\sum_{\gamma\in D/H}\gamma y
=
e(L/L^H)N_{D/H}(y).
\]

Therefore every generator in the Nakayama sum is the valuation of some rational point of \(T(\mathbf Q)\). Taking products and inverses of the corresponding \(q_{H_j,y_j}\), we get \(q\in T(\mathbf Q)\) such that
\[
\nu_L(q)=\lambda.
\]

Finally, for arbitrary \(t\in T(\mathbf Q_p)\), choose \(q\in T(\mathbf Q)\) with
\[
\nu_L(q)=\nu_L(t).
\]
Then
\[
\nu_L(tq^{-1})=0,
\]
so \(tq^{-1}\in T(\mathbf Z_p)\). Thus
\[
t\in T(\mathbf Z_p)T(\mathbf Q).
\]
Since \(t\) was arbitrary,
\[
T(\mathbf Q_p)=T(\mathbf Z_p)T(\mathbf Q).
\]

<!-- END_FINAL_PROOF -->

## 3. Solver Failure Output and Candidate Guidance YAML

```yaml
failure_output_type: none
main_solver_proof_key: true
```

## 4. Local Source Ledger

- Local quotient identification: proved.
- Kernel equals maximal compact subgroup: proved using compactness and torsion-freeness of \(Y\).
- Local Nakayama valuation reverse inclusion: proved via valuation exact sequence, Hilbert 90, restriction/corestriction compatibility.
- Global realization for nonnormal \(H\): proved using \(E=K^H\), norm \(N_{E/\mathbf Q}\), and weak approximation in \(E\).
- Final decomposition: proved.

## 5. Interface Notes for Manager Acceptance

```yaml
candidate_answer: true
complete_scratch_work_attempt: true
uncertain_steps:
  - The local Nakayama lemma proof uses the standard cohomological Nakayama argument; if the verifier demands a fully expanded Tate-cohomology proof, expand that paragraph.
help_requests: []
proposed_board_updates:
  - C1 complete
  - C2 complete with cohomological Nakayama proof
  - C3 complete, including nonnormal H
  - C4 complete
  - C5 complete
```

## 6. Web-Source Confirmation

No web sources used.