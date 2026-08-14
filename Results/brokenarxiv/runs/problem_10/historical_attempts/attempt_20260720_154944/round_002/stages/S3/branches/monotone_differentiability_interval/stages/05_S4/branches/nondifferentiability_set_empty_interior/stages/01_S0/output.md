**1 Target Decomposition**

Normalize first: if `f` is decreasing, replace it by `-f`. Derivative existence is unchanged up to sign, so solvers may assume `f` is strictly increasing.

Use the secant slope notation

```text
s(x,y) = (f(y)-f(x))/(y-x),  x != y.
```

Main contradiction shape:

1. Assume `J \ D` contains a nonempty open interval `I`.
2. For each bad point, classify failure of the two-sided derivative through left/right local slope cuts:
   - right-side oscillation,
   - left-side oscillation,
   - left/right cut mismatch,
   - unbounded slope behavior,
   - convergence to a non-realized cut outside `M`.
3. Prove a uniformization lemma: from an interval of bad points, extract a smaller open interval `I0`, fixed `alpha < beta` in `M`, and a fixed side-pattern witnessing badness everywhere on `I0`.
4. Let `gamma` satisfy `alpha < gamma < beta`, and tilt:
   ```text
   g(x) = f(x) - gamma x.
   ```
   Slopes of `f` below `alpha` become strict decreases of `g`; slopes above `beta` become strict increases of `g`.
5. Use weak o-minimality to show a definable continuous `g` cannot have the resulting fixed local oscillation/extremum pattern on a whole open interval.
6. Contradiction. Hence `J \ D` contains no nonempty open interval.

**2 Available Tools**

Allowed or derivable from the packet:

- Ordered-field algebra for secant slopes and affine tilts.
- Basic interval topology in ordered fields.
- Definability closure under first-order formulas.
- Weak o-minimality: every definable subset of `M` is a finite union of convex sets.
- Definable-family uniformization: if a definable family of one-dimensional conditions covers an interval, finite-convex behavior lets one extract a subinterval with fixed parameters/pattern.
- A local monotonicity lemma for definable continuous one-variable functions, to be proved from weak o-minimality, not imported as an external theorem.

**3 Subclaim Support Graph With S1-S5 Assignments**

`S1`: Slope-cut setup and definability.

- Define left/right lower and upper slope cuts using first-order formulas.
- Show all conditions like “arbitrarily close right secants have slope `< alpha`” or `> beta` are definable.
- Classify derivative failure into oscillation, one-sided failure, mismatch, unboundedness, or non-realized cut.

`S2`: Weak local monotonicity for definable continuous functions.

- Prove from weak o-minimality that a definable continuous `g:I -> M` has a nonempty open subinterval on which it is monotone.
- Equivalent usable form: no definable continuous function can exhibit fixed strict up/down oscillation at every point of an open interval.

`S3`: Fixed-pattern contradiction by tilting.

- Given fixed `alpha < beta` and a fixed bad pattern on an interval, choose `gamma` between them.
- Translate slope inequalities for `f` into local increase/decrease behavior of `g=f-gamma x`.
- Use `S2` to rule out:
  - right oscillation,
  - left oscillation,
  - left/right mismatch patterns,
  - every-point local max/min patterns.

`S4`: Uniformization of badness.

- Starting from `I subset J\D`, extract a smaller interval with fixed `alpha < beta` and one fixed bad side-pattern.
- Must handle:
  - non-uniform slope gaps,
  - one-sided oscillation,
  - left/right derivative-cut mismatch,
  - unbounded slope behavior by choosing comparison slopes beyond a global secant,
  - non-realized cuts by comparing against realized secant slopes and passing to transition intervals.

`S5`: Assembly.

- Normalize monotonicity.
- Apply `S1` classification.
- Use `S4` to get fixed `alpha,beta,pattern`.
- Apply `S3`.
- Conclude contradiction.

Dependency graph:

```text
S1 -> S4
S2 -> S3
S4 + S3 -> S5
```

**4 Hardest Step Prediction**

`S4` is the hardest. The dangerous case is not ordinary oscillation, but an interval where slopes appear to converge everywhere to non-realized cuts outside `M`. The solver must avoid assuming Dedekind completeness. The route should compare those cuts with realized secant slopes in `M`; weak o-minimal finite-convex behavior then forces either a fixed ordinary gap pattern or a point where the cut is realized, contradicting badness.

**5 Failure-Mode Checks**

- Do not assume real completeness, compactness, measure, Baire category, or classical a.e. differentiability.
- Do not use an external monotonicity theorem unless it is reproved from weak o-minimality.
- Do not let `alpha,beta` vary with `x` in the final contradiction.
- Treat left and right slopes separately before merging.
- For unbounded slopes, compare against a global secant so “large slope everywhere” becomes impossible.
- For non-realized cuts, force contact with realized slopes in `M`; do not silently identify cuts with elements of `M`.

**6 Assignment Table**

| Solver | Task |
|---|---|
| S1 | Formal slope-cut definitions, definability, derivative-failure taxonomy |
| S2 | Prove weak local monotonicity/anti-oscillation lemma for definable continuous functions |
| S3 | Prove fixed `alpha < beta` fixed-pattern contradiction via tilt |
| S4 | Prove interval-badness uniformizes to fixed `alpha,beta,pattern`, including unbounded and external-cut cases |
| S5 | Assemble contradiction proof from S1-S4 without adding new external facts |

**7 Web-Source Confirmation**

Not performed. The packet explicitly forbids web, external sources, code, tools, files, and API keys for this solver branch.