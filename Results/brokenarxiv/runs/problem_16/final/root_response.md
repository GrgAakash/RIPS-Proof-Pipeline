Completed the solver-only S0-S6 run. I did not run a verifier pipeline, did not use web search, and did not use code execution for the mathematical work. The prompt packet was found at `Codes/Prompt Packet/Prompts.md`.

Round 1 failed at the key valuation-lifting step. Round 2 used one guidance item: prove equality of the global and local valuation images, not false surjectivity onto all `D`-invariant valuations. Round 2 S6 returned `failure_output_type: solved`.

**S6 Final Proof**
Let `K/Q` be a finite Galois extension splitting `T`, choose `w | p`, set `L=K_w`, `G=Gal(K/Q)`, `D=Gal(L/Q_p)`, and `X=X^*(T_K)`. By split-torus character duality and Galois descent,
\[
T(\mathbb Q)=\operatorname{Hom}_G(X,K^*),\qquad
T(\mathbb Q_p)=\operatorname{Hom}_D(X,L^*).
\]

Let `v=v_w`. The induced map
\[
\nu_L:\operatorname{Hom}_D(X,L^*)\to \operatorname{Hom}_D(X,\mathbb Z)
\]
has kernel `Hom_D(X,O_L^*)`, which is compact. Any compact subgroup maps to a compact subgroup of the discrete torsion-free group `Hom_D(X,Z)`, hence to `0`. Thus
\[
T(\mathbb Z_p)=\ker \nu_L.
\]

The key step is equality of valuation images:
\[
\operatorname{im}\bigl(\operatorname{Hom}_G(X,K^*)\to \operatorname{Hom}_D(X,\mathbb Z)\bigr)
=
\operatorname{im}\bigl(\operatorname{Hom}_D(X,L^*)\to \operatorname{Hom}_D(X,\mathbb Z)\bigr).
\]
S6 proves this using transfer generators. For `H ≤ D`, let `e_H` generate `v((L^H)^*)`, define
\[
(\tau_H^D\lambda)(x)=\sum_{r\in D/H}\lambda(r^{-1}x),
\]
and
\[
J_X=\sum_{H\le D} e_H\,\tau_H^D\operatorname{Hom}_H(X,\mathbb Z).
\]
The local image equals `J_X`, and weak approximation in `K^H` realizes each generator globally. Hence the two images are equal.

Now take `t∈T(Q_p)`, viewed as `f∈Hom_D(X,L^*)`. By image equality choose `q∈Hom_G(X,K^*)=T(Q)` with the same valuation image as `f`. Then `fq^{-1}∈ker ν_L=T(Z_p)`, so
\[
t\in T(\mathbb Z_p)T(\mathbb Q).
\]
The reverse inclusion is immediate. Therefore
\[
T(\mathbb Q_p)=T(\mathbb Z_p)T(\mathbb Q).
\]

No verifier/Defender/Manager/Main roles were run.