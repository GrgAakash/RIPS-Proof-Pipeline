1. Challenge restatement

TDC-2 claims: every connected component of a fixed-order oriented line-transversal space is acyclic.

TDC-3 claims: the endpoint-incidence and convex-fiber maps used toward TDC-2 are valid for open, possibly noncompact convex sets and ordinary reduced homology. The live narrowed version permits an explicit endpoint-to-line deformation retract, but not an unproved broad nonproper convex-fiber homology-transfer theorem.

U002 asks whether fixed-order oriented acyclicity is true componentwise, not merely for a whole fixed-order stratum. Its required test is to attach an incidence object to an arbitrary component and prove that object acyclic, or give a counterexample/obstruction showing the componentwise claim cannot be established.

Live candidates:

Candidate A: every endpoint-pair component is acyclic; therefore every fixed-order oriented line-transversal component is acyclic.

Candidate B: the endpoint-pair component lemma is false; some endpoint-pair component has nontrivial reduced homology, so TDC-2 may fail.

Candidate C: only the endpoint-to-line homotopy equivalence and one-endpoint convex-fiber facts are established; componentwise endpoint-pair acyclicity remains unproved, and broad nonproper convex-fiber transfer is invalid or insufficient.

2. Discriminating analysis

Let the fixed oriented order be `C_1 < ... < C_m`, and let `T` be the corresponding oriented line-transversal stratum. For an oriented line `ell(t)=p+t u`, define `I_i(ell)={t: ell(t) in C_i}`. Since each `C_i` is open convex, `I_i(ell)` is an open interval whenever nonempty. In the fixed-order stratum, `I_1(ell) < ... < I_m(ell)`.

Endpoint-to-line transfer: define
`E={(ell,s,t): ell in T, s in I_1(ell), t in I_m(ell)}`.
The map `(ell,s,t) -> (ell(s),ell(t))` is a homeomorphism from `E` to the endpoint-pair space `P`, because two ordered endpoint hits determine the oriented line continuously, and the order ensures the segment from the first endpoint to the last crosses the intermediate sets in the displayed order.

For each open convex `C`, a continuous selector of `I_C(ell)` can be built as
`c_C(ell)= integral_I t e^{-t^2} dt / integral_I e^{-t^2} dt`,
where `I=I_C(ell)`. The denominator is positive and finite, the weighted average lies inside the open interval `I`, and continuity follows by dominated convergence because line membership indicators converge away from the at-most-endpoint boundary set on the line. Thus `ell -> c_{C_1}(ell)` and `ell -> c_{C_m}(ell)` give a continuous section of `E -> T`. The straight-line homotopy in the interval fibers,
`(s,t) -> ((1-r)s+r c_{C_1}(ell), (1-r)t+r c_{C_m}(ell))`,
stays in `I_1(ell) x I_m(ell)`. Therefore the endpoint-to-line map is a deformation-retract equivalence. By homotopy invariance of ordinary reduced singular homology, this limited transfer is valid. This supports Candidate C’s TDC-3 narrowing.

One-endpoint fibers: for fixed `x in C_1`, let `F_x={y in C_m: [x,y] meets C_2,...,C_{m-1} in order}`. If `y^0,y^1 in F_x`, choose witnesses
`z_i^j=x+lambda_i^j(y^j-x) in C_i` with
`0<lambda_2^j<...<lambda_{m-1}^j<1`. Put `r_i^j=1/lambda_i^j`, so
`r_2^j>...>r_{m-1}^j>1`. For `0<theta<1`, set
`y^theta=(1-theta)y^0+theta y^1`,
`r_i^theta=(1-theta)r_i^0+theta r_i^1`, and
`z_i^theta=((1-theta)r_i^0 z_i^0+theta r_i^1 z_i^1)/r_i^theta`.
Convexity gives `z_i^theta in C_i`, and
`z_i^theta=x+(1/r_i^theta)(y^theta-x)`. The strict inequalities among the `r_i` are preserved, so the corresponding `lambda_i^theta=1/r_i^theta` remain strictly ordered. Also `y^theta in C_m`. Hence `F_x` is convex; openness follows from openness of the `C_i` and strict parameter inequalities. This again supports only the limited part of Candidate C.

Small cases do not resolve the general challenge. If `m=2`, then `P=C_1 x C_2`, a product of convex contractible sets, so it is acyclic. If `d=1`, each nonempty fixed-order oriented line space is a point. These computations support Candidate A only in degenerate cases and do not eliminate either Candidate A or Candidate B in general.

Component-attached incidence attempt for U002: for an arbitrary component `K` of `P`, define
`Q_K={(a,b,lambda_2,...,lambda_{m-1}): (a,b) in K, 0<lambda_2<...<lambda_{m-1}<1, a+lambda_i(b-a) in C_i}`.
For fixed `(a,b)`, the fiber is the product of the open parameter intervals where the segment lies in each `C_i`; in fixed order these intervals are disjoint and ordered, so this fiber is convex. The same interval-selector construction gives a deformation retract from `Q_K` to `K`. Therefore `Q_K` is acyclic exactly when `K` is acyclic; this incidence object does not prove acyclicity.

Projection to one endpoint also does not close the gap. The fibers over a first endpoint are convex, but the projection image of a component is not proved convex or acyclic from the supplied materials. The packet’s annulus warning is decisive against the broad inference: `A x (0,1)` with `A` an open annulus has convex vertical fibers, but it deformation retracts to `A`, and ordinary singular homology has `H_1(A) ~= H_1(S^1) ~= Z`. Thus convex fibers alone do not imply acyclicity.

Discriminating outcome: the explicit endpoint-to-line homotopy equivalence and one-endpoint convexity facts are established. A complete proof that every endpoint-pair component is acyclic was not derived, and no counterexample with nontrivial reduced homology was derived. Therefore TDC-2 and U002 remain unresolved from the allowed materials.

3. Resolution

```yaml
challenged_claim_id: TDC-2
resolution_verdict: UNRESOLVED
selected_candidate: "None"
derivation_basis: insufficient
derivation_or_source: "Section 2: limited endpoint-to-line deformation retract and one-endpoint convexity are derived, but componentwise endpoint-pair acyclicity is not proved and no counterexample is derived."
resolution_test_result: "Degenerate cases m=2 and d=1 are acyclic; the general endpoint-pair component K remains undecided. Candidate A is not proved, and Candidate B is not witnessed."
rejected_candidates: []
reason_each_is_rejected: "None"
```

```yaml
challenged_claim_id: TDC-3
resolution_verdict: RESOLVED
selected_candidate: "Candidate C"
derivation_basis: derived_here
derivation_or_source: "Section 2: Endpoint-to-line transfer and one-endpoint fibers; packet Exhibit 3 annulus warning."
resolution_test_result: "The endpoint-to-line map is valid in the narrowed explicit deformation-retract form for open possibly noncompact convex sets, and fixed-first-endpoint fibers are open convex. A broad nonproper convex-fiber acyclicity transfer is not established and is insufficient without controlling the base/component image."
rejected_candidates: ["Candidate A", "Candidate B"]
reason_each_is_rejected: "Candidate A adds unproved endpoint-pair component acyclicity; Candidate B asserts a counterexample, but none is derived here."
```

```yaml
challenged_claim_id: U002
resolution_verdict: UNRESOLVED
selected_candidate: "None"
derivation_basis: insufficient
derivation_or_source: "Section 2: Component-attached incidence object Q_K was defined, but its deformation retract to K makes the acyclicity question circular."
resolution_test_result: "The required componentwise test was attempted: Q_K has convex parameter fibers and is homotopy equivalent to K, so it does not prove K acyclic. No componentwise proof and no counterexample/obstruction to the truth of the statement was derived."
rejected_candidates: []
reason_each_is_rejected: "None"
```

4. Web-source confirmation

no web sources used