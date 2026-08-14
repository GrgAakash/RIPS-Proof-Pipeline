**1. Target Decomposition**

Reduce the theorem to finding interior in the differentiability set.

Let  
`D = {x in J : lim_{h -> 0, x+h in J} (f(x+h)-f(x))/h exists in M}`.

Plan:

1. Show `D` is definable.
2. By weak o-minimality, `D` is a finite union of convex sets.
3. Prove `D` is not finite and, more strongly, that its complement cannot contain every point of some open interval.
4. Conclude some nonempty open interval `J1 ⊆ J` is contained in `D`.

Do not prove the theorem directly; prove the needed structural lemmas below.

**2. Available Tools**

Allowed standard background:

- Ordered-field algebra and order topology.
- Usual epsilon-delta definition of derivative.
- Continuity and strict monotonicity of `f`.
- Definability is closed under first-order quantification.
- In a weakly o-minimal structure, every definable unary set is a finite union of convex sets.
- A finite union of convex subsets of an open interval either has nonempty interior or is finite/discrete in the relevant interval.

Useful derived notions:

- Secant slope:
  `S(x,y) = (f(y)-f(x))/(y-x)` for `x != y`.
- One-sided local slope predicates:
  `S^+(x,h) = (f(x+h)-f(x))/h` for `h > 0`,
  `S^-(x,h) = (f(x)-f(x-h))/h` for `h > 0`.
- Derivative existence at `x` is equivalent to the two one-sided slope limits existing in `M` and being equal.

**3. Subclaim Support Graph With 3-8 Subclaims Assigned To S1-S5**

S1. Definability of differentiability and oscillation predicates  
Show that `D` is definable. Also define, for `epsilon > 0`, the predicate saying that right/left secant slopes near `x` have oscillation at least `epsilon`; verify these are definable unary predicates after quantifying over small `h`.

S2. Weak-o-minimal consequence for bad sets  
For any definable set `A ⊆ J`, if `A` meets every nonempty open subinterval of some open `U ⊆ J`, then `A` contains a nonempty open interval. Equivalently, a definable unary set with empty interior is locally finite in the sense needed here.

S3. Local monotonicity/regularity for definable unary auxiliary functions  
Prove from weak o-minimality, not by citation, that a definable unary function has a nonempty open interval on which it is continuous and weakly monotone. Apply this only to auxiliary functions arising from secant-slope bounds or witnesses, not to replace the target theorem.

S4. No interval of persistent slope oscillation  
Assume toward contradiction that derivative failure occurs at every point of a nonempty open interval `U`. Use S1-S3 to shrink to an interval where the failure has a uniform definable form: two nearby secant slopes remain separated by some positive amount in an ordered way. Show this creates an infinite alternation pattern in a unary definable set, contradicting weak o-minimality.

S5. Assembly  
Use S1 and S2 to reduce to excluding an open interval of non-differentiability. Invoke S4 for that exclusion. Since `D` is definable and its complement has no open subinterval inside some smaller open interval, conclude `D` contains a nonempty open interval `J1`.

Support graph:

`S1 -> S5`  
`S2 -> S5`  
`S3 -> S4`  
`S1 + S2 + S3 -> S4`  
`S4 -> S5`

**4. Hardest Step Prediction**

The hardest step is S4.

The key risk is converting pointwise derivative failure into a uniform interval-level contradiction without smuggling in real-analysis theorems such as Lebesgue differentiation, measure theory, Baire category, or an external monotonicity theorem. The proof must stay first-order/weak-o-minimal: isolate definable oscillation witnesses, shrink intervals using finite-convex decomposition, then force a forbidden infinite alternation in a unary definable set.

**5. Failure-Mode Checks**

- Do not cite the o-minimal monotonicity theorem or weak-o-minimal differentiability theorem.
- Do not use measure, countability, completeness of `M`, or real-closedness unless proved from assumptions, which it is not.
- Keep all intervals nonempty and open.
- Remember the derivative value must lie in `M`; avoid arguments using completion cuts unless they are eliminated.
- The domain condition `x+h in J` must remain in every slope predicate.
- Strict monotonicity gives nonzero secant denominators and ordered secant behavior, but it does not by itself imply differentiability.
- Avoid proving the parent theorem.

**6. Subproblem Assignment Table S1-S5**

| Solver | Assignment | Output Needed |
|---|---|---|
| S1 | Formalize derivative-existence and oscillation predicates | Definability proof for `D` and bad-slope predicates |
| S2 | Extract unary-set consequences of weak o-minimality | Lemma: definable dense/bad sets contain intervals; empty-interior definable sets are locally finite |
| S3 | Prove local regularity of definable unary auxiliary functions | Interval-shrinking lemma for definable unary functions used in S4 |
| S4 | Core contradiction | No open interval can consist entirely of non-differentiability points |
| S5 | Assemble branch proof skeleton | Derive existence of `J1 ⊆ J` from S1-S4 without writing the final proof |

**7. Web-Source Confirmation**

No web sources used. This follows the branch instruction: no web, no external sources.