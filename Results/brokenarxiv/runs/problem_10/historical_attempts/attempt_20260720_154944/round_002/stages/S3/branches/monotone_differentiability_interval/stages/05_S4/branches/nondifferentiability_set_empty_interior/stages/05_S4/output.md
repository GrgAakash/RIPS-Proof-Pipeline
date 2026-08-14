## 1. Assignment

S4 goal: from an assumed nonempty open interval `I subset J \ D`, extract a smaller open interval `U`, fixed `alpha < beta` in `M`, and one uniform bad slope pattern.

Normalize by replacing `f` with `-f` if needed, so `f` is strictly increasing. For `u < v`, write

```text
S(u,v) = (f(v)-f(u))/(v-u).
```

The extracted pattern is one of:

- right oscillation: near every `x in U`, right secants are both `< alpha` and `> beta`;
- left oscillation: same on the left;
- left/right gap: left secants are eventually `< alpha` and right secants eventually `> beta`, or the reverse;
- high side cut: for a fixed global secant `s`, with `s < alpha < beta`, one fixed side has secants eventually `> beta`;
- low side cut: with `alpha < beta < s`, one fixed side has secants eventually `< alpha`.

## 2. Subproof / Failure

S4 succeeds.

Two weak-o-minimal consequences used and proved from finite convexity of unary definable sets:

1. Rectangularization: if `E subset U x M` is definable and each fiber `E_x` contains a nonempty interval, then after shrinking `U` there are fixed `alpha < beta` with `(alpha,beta) subset E_x` for every `x in U`.  
Proof sketch: weak o-minimality gives uniformly finitely many convex components in definable one-variable fibers; otherwise compactness gives one fiber with infinitely many convex components. Choose the first nondegenerate component on an open base interval. Its endpoints are definable cuts; if no constants can be trapped between them on a subinterval, some unary level set alternates infinitely often, contradicting weak o-minimality.

2. Nested-threshold extraction: if a definable nested family `X_t` covers an open interval, then some `X_t` contains an open interval.  
Proof: if every `X_t` had empty interior, uniform finiteness would bound all `|X_t|`; finitely many points in the covered interval then force one larger threshold to contain more than that bound.

Now assume `I subset J \ D` is open. Pick `p < q` in `I` and let `s = S(p,q)`.

For a side-slope germ at `x`, either:

- it oscillates across some realized interval of slopes;
- it is unbounded above; or
- it has a finite cut-limit, possibly not realized in `M`.

If a right or left oscillation occurs on an open set, rectangularization gives fixed `alpha < beta` and the corresponding uniform oscillation pattern.

If unbounded behavior occurs on an open set, choose a comparison slope above the global secant. If slopes are eventually above it on an open subinterval, nested-threshold extraction gives the high-side pattern. If not, the same germ is frequently below that comparison and arbitrarily high, so it reduces to the oscillation case with fixed `alpha < beta`.

After removing oscillation and unbounded cases, both one-sided slope germs have finite cut-limits. If the left and right cuts are separated on an open interval, the separator slopes form definable interval fibers; rectangularization gives fixed `alpha < beta` and a uniform left/right gap pattern.

The only remaining possibility on an open interval is that the left and right cut-limits agree at every point. If this common cut is realized in `M`, then the derivative exists there, contradicting `I subset J \ D`. Hence the common cut is non-realized. Compare it with the realized global secant `s`. Since the cut is not `s`, it is either above or below `s`. Weak o-minimality leaves an open subinterval with one fixed comparison direction. Nested-threshold extraction then gives either fixed `s < alpha < beta` with side secants eventually `> beta`, or fixed `alpha < beta < s` with side secants eventually `< alpha`.

Transition points where the cut comparison changes are only convex-component boundaries. Passing to realized secant slopes across those transition intervals gives the same high/low alternative on one side; they cannot fill an open interval.

## 3. YAML

```yaml
s4_status: success
input_assumption: "nonempty open I subset J \\ D"
normalization: "replace f by -f if needed, so f is increasing"
output:
  interval: "nonempty open U subset I"
  constants: "alpha < beta in M"
  pattern:
    one_of:
      - right_oscillation
      - left_oscillation
      - left_low_right_high
      - left_high_right_low
      - side_high_over_global_secant
      - side_low_under_global_secant
missing_obstruction: null
external_sources_used: false
```

## 4. Ledger

- `S(u,v)` is definable and continuous off the diagonal.
- Weak o-minimality supplies finite convex decomposition of unary definable fibers.
- Non-uniform slope gaps are made uniform by rectangularization.
- Unbounded slopes are compared with a realized global secant.
- Non-realized cuts are compared with realized secants, then reduced to fixed high/low side patterns.
- No open interval can remain outside these alternatives.

## 5. S6 Notes

S6 may assume: there are `U`, `alpha < beta`, and one fixed pattern above.  
For high/low patterns, retain the containing interval `(p,q)` and its realized secant `s`, with either `s < alpha < beta` or `alpha < beta < s`.  
The remaining contradiction should use slope algebra/finite-chain arguments, not any further badness classification.

## 6. Web Confirmation

No web or external sources used, per the packet restriction.