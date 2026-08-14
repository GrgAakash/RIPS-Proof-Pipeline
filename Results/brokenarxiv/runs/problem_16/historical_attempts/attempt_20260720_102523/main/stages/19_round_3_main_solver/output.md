1. **Assignment Restatement**

Prove, using only this prompt and no web/files/tools, that for every algebraic torus `T` over `Q` and every prime `p`,

`T(Q_p) = T(Z_p) T(Q)`,

with `T(Z_p)` maximal compact. The proof must not cite Nakayama/Tate-Nakayama or an unproved transfer-generation theorem. The local valuation reverse inclusion must be fully proved if used.

2. **Subproof Or Failure**

Unsolved.

I cannot honestly complete the requested proof under the stated constraints, because the main required ingredient is exactly the hard local transfer-generation statement:

For finite Galois local `L/F`, `D = Gal(L/F)`, and a `D`-lattice `Y`, one needs a precise description of the image of the valuation map on `T(F)` in terms of transfers

`sum_{H <= D} e(L/L^H) N_{D/H}(Y^H)`,

including arbitrary nonnormal subgroups, ramification factors, denominators, and saturation.

I can outline the standard route:

- Choose a finite Galois splitting field `K/Q` for `T`.
- Let `w | p`, `L = K_w`, and `D = Gal(L/Q_p)`.
- Write `Y = X_*(T_K)`.
- The maximal compact subgroup of `T(Q_p)` is the kernel of the canonical valuation map.
- One needs to show every local valuation class of `T(Q_p)` is produced by a global point of `T(Q)`.
- The intended global construction uses weak approximation in fixed fields `K^H` to realize local uniformizer valuations and hence the transfer generators.
- This reduces the theorem to the local valuation image formula above.

But the reverse inclusion in that local formula is nontrivial. Proving it from scratch would require building the valuation image of `T(F)` by resolving the `D`-lattice through permutation lattices, tracking fixed points under all decomposition subgroups, proving the relevant kernel-generation statement for arbitrary subgroups, then checking ramification normalization and saturation. That is essentially the forbidden unproved transfer-generation theorem unless all of those details are supplied.

I therefore cannot mark the target theorem solved.

3. **Solver Failure Output YAML**

```yaml
failure_output_type: unsolved
main_solver_proof_key: false
reason: >
  The proof reduces to the local valuation reverse inclusion / transfer-generation
  statement for arbitrary D-lattices. I cannot supply a complete self-contained
  proof with nonnormal subgroups, ramification factors, denominators, and
  saturation details within this response without relying on a forbidden
  unproved theorem.
```

4. **Local Source Ledger And Critical Claim Statuses**

- `T(Z_p)` is the maximal compact subgroup of `T(Q_p)`: plausible/standard, but not fully proved here.
- Local valuation map description for tori split by `L/F`: partially described, not proved.
- Reverse inclusion  
  `im(nu_L) subset sum_{H <= D} e(L/L^H) N_{D/H}(Y^H)`: not proved.
- Global realization of transfer generators by weak approximation in `K^H`: plausible route, not completed because the local input is missing.
- Final equality `T(Q_p)=T(Z_p)T(Q)`: not established.

5. **Interface Notes For Manager Acceptance**

This should be treated as a solver failure, not a proof. The blockage is exactly the requested audit target: the local reverse inclusion. A successful next attempt must either give a full elementary proof of that local transfer-generation statement or avoid it by a genuinely different argument.

6. **Web-Source Confirmation**

No web sources used.