## 1 Assignment

S5 assembles the contradiction proof using S1-S4 only. The result is conditional on the precise S1, S3, and S4 lemmas being valid and matching each other’s hypotheses.

## 2 Subproof/Failure

Assume for contradiction that there is a nonempty open interval `I ⊂ J \ D`.

Normalize monotonicity. If `f` is strictly decreasing, replace it by `g = -f`. Then `g` is definable, continuous, and strictly increasing, and for every `x ∈ J`,

```text
(g(x+t)-g(x))/t = - (f(x+t)-f(x))/t.
```

So the derivative limit exists for `g` at `x` iff it exists for `f` at `x`. Hence `D_g = D_f`. Thus it is enough to prove the result for the strictly increasing case.

Now assume `f` is strictly increasing.

Since every `x ∈ I` lies outside `D`, the derivative limit at `x` does not exist in `M`. By S1 classification, each such `x` falls into one of the S1 bad derivative alternatives.

By S4, from the open interval `I` of bad points, there is a nonempty open subinterval `I0 ⊂ I`, fixed parameters `alpha < beta` in `M`, and one fixed S1 pattern such that every `x ∈ I0` realizes that same `(alpha, beta, pattern)` alternative.

By S3, no nonempty open interval can consist entirely of points realizing one fixed S1 bad pattern with fixed `alpha < beta`.

This contradicts the existence of `I0`.

Therefore `J \ D` contains no nonempty open interval.

Failure/conditional point: S5 cannot independently prove the theorem without the actual S1-S4 packet. The contradiction is complete only if:

```text
S1 classifies every non-differentiability point into the patterns later handled by S3.
S4 uniformizes S1 on a nonempty open subinterval with fixed alpha, beta, and fixed pattern.
S3 rules out every fixed pattern produced by S4.
```

## 3 YAML

```yaml
status: conditional_proof_assembled
target: "J \\ D contains no nonempty open interval"
normalization:
  decreasing_case: "replace f by -f"
  derivative_domain_preserved: true
contradiction_assumption: "exists nonempty open I subset J \\ D"
dependencies:
  S1: "classification of derivative failure points"
  S4: "uniformization to fixed alpha, beta, and pattern on open subinterval"
  S3: "fixed-pattern open interval impossible"
conclusion: "contradiction, hence no nonempty open interval in J \\ D"
conditional_remaining:
  - "exact S1 statement not supplied"
  - "exact S3 statement not supplied"
  - "exact S4 statement not supplied"
  - "must verify S4 patterns are exactly covered by S3"
```

## 4 Ledger

Used/proven internally:

```text
If f is decreasing, g = -f is increasing.
Derivative existence is invariant under multiplying by -1.
So D_f = D_g.
Contradiction setup reduces to increasing f.
```

Used as packet facts:

```text
S1 classification.
S4 fixed alpha/beta/pattern extraction.
S3 impossibility of a fixed bad pattern on a nonempty open interval.
```

Not used:

```text
No web sources.
No external theorems beyond named S1-S4.
No files, APIs, tools, or code.
```

## 5 S6 Notes

S6 should verify the interfaces:

```text
1. S1 applies to definable continuous strictly increasing f on J.
2. S1 covers all failures of derivative existence in M, including oscillation and unbounded behavior if those are separate cases.
3. S4 produces alpha < beta in M and a single pattern on a nonempty open subinterval.
4. S3 rules out every pattern S4 can output.
5. The decreasing case is fully covered by the f -> -f normalization.
```

## 6 Web Confirmation

No web confirmation was used. The prompt forbids web/external sources, so this proof is packet-only and conditional on S1-S4.