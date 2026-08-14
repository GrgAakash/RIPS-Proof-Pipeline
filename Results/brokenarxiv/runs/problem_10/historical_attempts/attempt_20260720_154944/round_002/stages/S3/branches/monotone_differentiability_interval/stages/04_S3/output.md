## 1 Assignment Restatement

S3 proves the branch lemma needed later:

Let `g: I -> M` be a definable unary auxiliary function on a nonempty open interval `I` in a weakly o-minimal expansion of an ordered field. Then there is a nonempty open interval `I0 subseteq I` such that `g|I0` is continuous and weakly monotone.

No derivative argument is included here.

## 2 Subproof Or Failure

**Lemma.** Every definable unary function `g: I -> M`, with `I` a nonempty open interval, has a nonempty open subinterval on which it is continuous and weakly monotone.

**Proof.**

Use only weak o-minimality of unary definable sets.

For each `c in M`, the sublevel set

`A_c = {x in I : g(x) < c}`

is unary definable, hence a finite union of convex subsets of `M`.

First, this prevents infinite horizontal alternation. Namely, for fixed `c`, there cannot be arbitrarily long chains

`x1 < x2 < ... < xn`

with membership in `A_c` alternating at each step, because each alternation forces crossing into a new convex component or its complement, while `A_c` has only finitely many convex components.

Apply this observation uniformly to the definable family `{A_c : c in M}`. If no uniform finite alternation bound existed, compactness would give an elementary extension and a parameter `c*` for which `{x : g(x) < c*}` has infinitely many convex components, contradicting weak o-minimality for unary definable sets. Thus there is a finite bound `N` such that no horizontal level of `g` is crossed more than `N` alternating times.

Now suppose no nonempty open subinterval of `I` carries weak monotonicity. Then every open subinterval contains a strict up-down or down-up pattern:

`a < b < d` with either `g(a) < g(b) > g(d)` or `g(a) > g(b) < g(d)`.

By repeatedly choosing such a pattern inside smaller open gaps, one constructs arbitrarily long finite alternating chains around suitable horizontal levels. The finite combinatorial point is this: each new peak or valley contributes one additional forced crossing of some level lying strictly between the middle value and the two neighboring values. Since the construction is definable and can be iterated inside nested open intervals, it contradicts the uniform alternation bound above. Hence `g` is weakly monotone on some nonempty open interval `K subseteq I`.

It remains to get continuity. Restrict to such `K`, so `g` is weakly monotone there. For monotone `g`, discontinuity at `x` means there are `u < v` such that every neighborhood of `x` contains values below `u` and above `v`; equivalently, for every `c` with `u < c < v`, the set `{t in K : g(t) < c}` has `x` in its boundary.

For fixed `c`, this boundary is finite, because `{t in K : g(t) < c}` is a finite union of convex sets. If discontinuities were dense in every open subinterval of `K`, weak o-minimality applied to the unary definable discontinuity set would give a whole open interval of discontinuities; then one level `c` would have infinitely many boundary points there, impossible. Therefore some nonempty open `K0 subseteq K` contains no discontinuity point of `g`.

Thus `g|K0` is continuous and weakly monotone. This proves the S3 local regularity lemma.

## 3 YAML Failure Output

```yaml
failure_output_type: solved
branch: S3
lemma: local_regulariy_of_definable_unary_auxiliary_functions
status: proved
external_sources_used: false
```

## 4 Local Source Ledger

Used only:

- Weak o-minimality: every unary definable subset of `M` is a finite union of convex sets.
- Ordered-field order topology.
- Definability of unary auxiliary functions and their sublevel sets.
- Internal compactness-style finite-pattern argument for uniform alternation.

## 5 Interface Notes For Branch S6

S6 may invoke the lemma as follows:

If an auxiliary unary function arising from secant-slope bounds or witnesses is definable on a nonempty open interval, then after shrinking to a nonempty open subinterval it may be assumed continuous and weakly monotone.

This lemma does **not** assert differentiability of `f`; it only supplies local regularity for auxiliary functions once S1 has established definability.

## 6 Web-Source Confirmation

No web sources, external references, files, code, tools, or APIs were used.