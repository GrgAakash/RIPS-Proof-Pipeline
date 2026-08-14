1. Assignment restatement

Prove the S5 projection step: if the ordered-transversal space `T_sigma` has acyclic connected components, then every connected component of `D_sigma = pi(T_sigma)` is acyclic, where `pi:T_sigma -> D_sigma` is projection to the direction `u`.

2. Subproof or failure

Let

`E = { (u,p) in S^{d-1} x R^d : p in u^\perp }`

with bundle projection `q:E -> S^{d-1}`. Then `T_sigma subset E`, and `pi = q|_{T_sigma}`.

Use the following standard selection/deformation lemma.

**Convex-Fiber Selection Lemma.** Let `q:E -> B` be a finite-dimensional real vector bundle over a paracompact Hausdorff space `B`. If `U subset E` is open and every fiber `U_b = U cap E_b` is nonempty and convex, then `q|_U:U -> B` is a homotopy equivalence.

Proof of lemma: for each `b in B`, choose `e_b in U_b`. Since `U` is open and `E` is locally trivial, after shrinking around `b` there is a local continuous section landing in `U`. A locally finite partition of unity subordinate to these neighborhoods gives a global section `s:B -> U`: at each `b`, take the finite convex combination of the local section values in the vector space `E_b`. Convexity of `U_b` keeps the value inside `U_b`. Then

`H(e,t) = (1-t)e + t s(q(e))`

is a fiberwise straight-line homotopy inside `U`, so `q|_U` is homotopy inverse to `s`.

Now let `D_0` be a connected component of `D_sigma`, and put

`T_0 = pi^{-1}(D_0)`.

By the earlier fiber result needed for this interface, `T_0 -> D_0` has nonempty convex fibers and `T_0` is open in the vector bundle over `D_0`. Since `D_0` is an open subspace of the sphere, it is paracompact. The lemma applies, so

`pi_0:T_0 -> D_0`

is a homotopy equivalence.

Also, `T_0` is connected: the deformation retracts `T_0` onto `s(D_0)`, and `s(D_0)` is connected because `D_0` is connected. Hence `T_0` lies in one connected component of `T_sigma`. Conversely, if a connected component of `T_sigma` containing `T_0` had a point over another component of `D_sigma`, its image under `pi` would be a connected subset of `D_sigma` meeting two distinct connected components, impossible. Therefore `T_0` is itself a connected component of `T_sigma`.

Assuming the S4 input that connected components of `T_sigma` are acyclic, `T_0` is acyclic.

The exact standard homological theorem used is **homotopy invariance of reduced singular homology**: if `f:X -> Y` is a homotopy equivalence, then for every `k >= 0`, the induced map

`f_*: \widetilde H_k(X; Z) -> \widetilde H_k(Y; Z)`

is an isomorphism. Verification: if `g` is a homotopy inverse, then homotopic maps induce the same homology map, so `g_* f_* = id` and `f_* g_* = id`.

Applying this to `pi_0:T_0 -> D_0` gives

`\widetilde H_k(D_0; Z) cong \widetilde H_k(T_0; Z) = 0`

for all `k >= 0`. Thus every connected component `D_0` of `D_sigma` is acyclic.

3. Solver failure output and candidate guidance

```yaml
failure_output_type: solved
failure_reason: null
missing_input: null
candidate_statement: null
candidate_guidance: null
```

4. Local Source Ledger

Prompt packet only. Standard background used: vector bundle local triviality, paracompact partitions of unity, convex combinations in vector bundle fibers, and homotopy invariance of reduced singular homology.

5. Interface notes for S6

S6 may use this as the projection-transfer step provided earlier parts establish: `T_sigma` is open in `E`, each nonempty fiber over `D_sigma` is convex, and every connected component of `T_sigma` is acyclic. This subproof then gives acyclicity of every connected component of `D_sigma`.

6. Web-source confirmation

No web sources used.