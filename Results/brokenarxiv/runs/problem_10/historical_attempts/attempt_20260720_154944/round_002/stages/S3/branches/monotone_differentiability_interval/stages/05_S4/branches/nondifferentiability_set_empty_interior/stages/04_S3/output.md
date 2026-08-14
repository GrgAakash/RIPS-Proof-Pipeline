**1. Assignment**

S3 proves the fixed-pattern contradiction. Assume S0 has already reduced an open bad interval to:

- a nonempty open interval `I ⊆ J`,
- fixed `alpha < beta`,
- one fixed bad slope pattern holding at every `x ∈ I`.

We show no such fixed pattern can occur.

**2. Subproof/Failure**

Choose `gamma = (alpha + beta)/2`, so `alpha < gamma < beta`. Define

```text
g(x) = f(x) - gamma x.
```

For `x != y`, write

```text
s_x(y) = (f(y)-f(x))/(y-x).
```

The tilt converts slope inequalities into comparisons with `g(x)`:

- If `y > x`, then `s_x(y) < alpha` implies `g(y) < g(x)`, while `s_x(y) > beta` implies `g(y) > g(x)`.
- If `y < x`, the denominator reverses signs: `s_x(y) < alpha` implies `g(y) > g(x)`, while `s_x(y) > beta` implies `g(y) < g(x)`.

Now check the fixed bad patterns.

If the bad pattern gives both `< alpha` and `> beta` slopes arbitrarily close on the right of every `x`, then `g` has values both below and above `g(x)` arbitrarily close on the right of every `x`. This is right oscillation, forbidden by S2.

If the same happens on the left, the sign-reversed table gives left oscillation of `g`, also forbidden by S2.

If the fixed pattern separates the two sides, then the table gives one of the mismatch/extremum cases. For example:

- right slopes `< alpha` and left slopes `> beta` give `g(y) < g(x)` on both sides near `x`, so every `x` is a local maximum of `g`;
- right slopes `> beta` and left slopes `< alpha` give `g(y) > g(x)` on both sides near `x`, so every `x` is a local minimum of `g`.

Both every-point local maximum and every-point local minimum patterns are forbidden by S2. The remaining left/right mismatch formulations are exactly these same sign conflicts after translating through the table.

Thus every S0 fixed bad pattern contradicts S2. Therefore no nonempty open interval can be contained in `J \ D`.

**3. YAML**

```yaml
s3_status: success
proved: fixed_alpha_beta_bad_patterns_are_impossible
uses:
  - S0_fixed_pattern_reduction
  - S2_no_right_oscillation
  - S2_no_left_oscillation
  - S2_no_left_right_mismatch
  - S2_no_every_point_local_extrema
tilt:
  gamma: "(alpha + beta) / 2"
  function: "g(x) = f(x) - gamma*x"
conclusion: "J \\ D contains no nonempty open interval, assuming S0 reduction covers all bad intervals"
```

**4. Ledger**

Proved inside S3:

- Existence of `gamma` between `alpha` and `beta`.
- Exact sign translation from slope bounds for `f` to local comparisons for `g`.
- Right fixed oscillation becomes right oscillation of `g`.
- Left fixed oscillation becomes left oscillation of `g`.
- Left/right separated fixed patterns become every-point local max/min patterns for `g`.

Dependencies:

- S0 supplies the fixed `alpha < beta` and fixed bad pattern after shrinking.
- S2 rules out the translated local behavior patterns for definable continuous `g`.

**5. S6 Notes**

S6 should verify that S0’s reduction covers all nondifferentiability modes, including one-sided mismatch and any unbounded quotient cases. S3 only handles the fixed finite `alpha < beta` separated-pattern contradiction.

**6. Web Confirmation**

No web or external sources used, per instruction.