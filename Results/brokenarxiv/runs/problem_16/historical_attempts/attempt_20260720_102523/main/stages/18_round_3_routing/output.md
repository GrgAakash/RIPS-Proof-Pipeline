**1. Target Normalization**

Work only from the stated theorem. Normalize notation as follows:

Let `K/Q` be a finite Galois splitting field for `T`, `G = Gal(K/Q)`, choose a place `w | p`, set `L = K_w`, and let `D <= G` be the decomposition group at `w`. Let `Y = X_*(T_K)`, a free `Z`-lattice with `G`-action.

Use the standard invariant descriptions to be proved in the solution:

`T(Q) = (Y tensor K^x)^G`,  
`T(Q_p) = (Y tensor L^x)^D`.

Normalize the local valuation by `v_L(L^x) = Z`, and define

`nu_L : Y tensor L^x -> Y`.

The target becomes the valuation-surjectivity task:

Show every local valuation class in `nu_L((Y tensor L^x)^D)` is attained by some global element of `(Y tensor K^x)^G`; then the quotient has zero valuation and lies in `T(Z_p)`.

This is the target reformulated, not an available supporting theorem.

**2. Task-Adaptive Proof Obligations**

O1. Prove the invariant descriptions of `T(Q)` and `T(Q_p)` from the chosen splitting field and cocharacter lattice.

O2. Prove that `T(Z_p)` is exactly the kernel of `nu_L` on `(Y tensor L^x)^D`, with the stated valuation normalization.

O3. Prove the local valuation image description. Define

`R_D(Y) = sum_{H <= D} e(L/L^H) N_{D/H}(Y^H) <= Y^D`.

The solver must prove both inclusions, especially the hard reverse inclusion:

`nu_L((Y tensor L^x)^D) <= R_D(Y)`.

O4. Prove that each generator `e(L/L^H) N_{D/H}(y)`, with `H <= D` and `y in Y^H`, is realized by a global rational point using weak approximation in `K^H`.

O5. Combine O3 and O4 to obtain valuation surjectivity, then finish by multiplying by a compact element.

**3. Available Tools**

Allowed:

- Definitions of algebraic tori, splitting fields, cocharacter lattices, decomposition groups, local valuations, and maximal compact subgroups.
- Elementary Galois descent for split tori.
- Elementary valuation exact sequence `1 -> O_L^x -> L^x -> Z -> 0`.
- Weak approximation in number fields, preferably stated only in the narrow form needed for prescribed valuations at finitely many places.

Not allowed:

- Web/internet.
- Prior theorem packets.
- Named Nakayama or Tate-Nakayama citation as a black box.
- Any unproved transfer-generation theorem.
- Python, files, API keys, verifier/citation/final-checker pipeline.

**4. Subclaim Support Graph**

Definitions  
-> local/global invariant models  
-> valuation map and compact-kernel identification  
-> local image formula `nu_L((Y tensor L^x)^D) = R_D(Y)`  
-> global realization of each `R_D(Y)` generator  
-> valuation surjectivity from `T(Q)` to `T(Q_p)/T(Z_p)`  
-> target theorem.

The critical bottleneck is the local reverse inclusion into `R_D(Y)`.

**5. Critical Claims Ledger**

`C1`: Descent model for rational points.  
Risk: convention mismatch between character and cocharacter tensors.  
Owner: SS1. Defender checks notation.

`C2`: Maximal compact equals valuation kernel.  
Risk: accidentally assuming good reduction.  
Owner: SS1. Defender checks ramified cases.

`C3`: Local reverse inclusion with ramification factors.  
Risk: banned black-box Nakayama argument, missing nonnormal subgroups, saturation errors.  
Owner: SS1. Defender treats this as the main audit target.

`C4`: Global realization of local transfer generators.  
Risk: using principal ideal assumptions instead of weak approximation; mishandling conjugate `p`-adic places.  
Owner: SS1. Defender checks place bookkeeping.

`C5`: Final multiplication step.  
Risk: proving only finite-index surjectivity instead of full surjectivity.  
Owner: SS1. Defender checks exact equality.

**6. Key-Step and Main Solver Selection**

Key step: prove `nu_L((Y tensor L^x)^D) <= sum_{H <= D} e(L/L^H) N_{D/H}(Y^H)` from scratch.

Select SS1 as Main Solver because the proof lives or dies on this local valuation reverse inclusion plus its global realization. SS1 must either produce the full transfer-generation proof, including nonnormal `H`, ramification normalization, denominator control, and saturation, or explicitly switch to a different complete route that avoids the lemma.

Select SS2 as Defender to audit only after SS1 has produced the main proof draft.

**7. Failure-Mode Checks**

- Do not cite Nakayama/Tate-Nakayama by name as a substitute for proof.
- Do not silently replace `e(L/L^H)` by `[D:H]`; these differ with residue degree.
- Do not restrict to normal subgroups `H`; the sum is over all `H <= D`.
- Do not assume `T` has good reduction at `p`.
- Do not prove only a rational or finite-index statement; integral saturation is essential.
- Do not use weak approximation for tori; use weak approximation in fields `K^H`.
- Do not assume prescribed local valuations force principal ideals globally.
- Do not let the local splitting field choice affect the final statement.

**8. Subsolver Execution Plan**

SS1 Main Solver:

1. Set up `K, G, w, L, D, Y`, invariant point descriptions, and valuation notation.
2. Establish compact-kernel identification.
3. Prove the local valuation image formula, with the reverse inclusion fully expanded.
4. For every local generator `e(L/L^H)N_{D/H}(y)`, construct a global `G`-invariant tensor using an element of `K^H` chosen by weak approximation.
5. Combine valuation equality with compact-kernel identification to produce the decomposition.

SS2 Defender:

1. Check SS1 did not use banned citations or hidden downstream claims.
2. Audit the local reverse inclusion line by line.
3. Verify ramification factors and valuation normalization.
4. Check nonnormal subgroup handling.
5. Confirm the global approximation construction contributes only the intended local valuation at `w`.
6. Confirm the final step proves equality, not just density or finite index.

**9. Subsolver Assignment Table**

| Subsolver | Role | Assignment |
|---|---|---|
| SS1 | Main Solver | Build the complete proof, centered on the local valuation reverse inclusion and global realization of its generators. |
| SS2 | Defender | Audit SS1’s proof for forbidden black boxes, normalization errors, subgroup errors, saturation gaps, and final logical completeness. |

**10. Web-Source Confirmation**

No web or internet source confirmation is allowed or used. All routing is based solely on the provided problem statement and mathematical guidance.