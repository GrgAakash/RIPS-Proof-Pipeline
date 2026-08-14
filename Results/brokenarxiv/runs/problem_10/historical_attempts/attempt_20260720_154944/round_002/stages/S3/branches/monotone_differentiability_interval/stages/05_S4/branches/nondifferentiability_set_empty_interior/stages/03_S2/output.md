## 1 Assignment

S2 task: supply the weak local monotonicity / anti-oscillation ingredient for a definable continuous unary function in a weakly o-minimal expansion of an ordered field.

## 2 Subproof / Failure

I can prove the anti-oscillation form directly from weak o-minimality:

**Lemma.** Let `A ⊆ I` be definable, with `I` a nonempty open interval. Then `A` cannot alternate with its complement infinitely often inside `I`.

**Proof.** By weak o-minimality, `A` is a finite union of convex subsets of `M`. Hence along the order on `I`, membership in `A` can change only finitely many times. Therefore there is no sequence

`x0 < x1 < x2 < ...`

inside `I` with `x_i ∈ A` iff `x_{i+1} ∉ A` for all `i`. Equivalently, any alleged fixed definable up/down oscillation that forces such alternation contradicts weak o-minimality. ∎

A useful corollary:

**Fixed-level anti-oscillation.** There are no definable continuous `g:I -> M` and fixed `α < β` such that every nonempty open subinterval of `I` contains points

`u < v < w`

with either

`g(u) < α < β < g(v)` and `g(w) < α`

or the reversed valley pattern.

Indeed, set `A = {x ∈ I : g(x) < α}`. Each such oscillation forces two distinct `A`-pieces separated by a point outside `A`. Repeating inside smaller subintervals gives arbitrarily many convex components of `A`, impossible by weak o-minimality.

**Failure note.** I do not have a fully self-contained proof, using only the packet and no imported weak monotonicity/cell-decomposition theorem, of the stronger statement:

> every definable continuous `g:I -> M` has a nonempty open subinterval on which it is monotone.

That statement is the standard weak monotonicity consequence of weak o-minimality, but proving it from scratch needs an additional decomposition/uniformity argument not contained in the packet. The direct anti-oscillation lemma above is proved.

## 3 YAML

```yaml
s2_status: partial
proved:
  - finite alternation obstruction for unary definable sets
  - fixed-level strict up/down anti-oscillation for definable continuous functions
not_proved_from_packet:
  - full local monotonicity theorem for arbitrary definable continuous unary functions
needed_extra_if_used:
  - weak monotonicity theorem
  - or weak cell/decomposition theorem for unary definable functions
```

## 4 Ledger

Used facts proved here:

- Weak o-minimality: every definable unary set is a finite union of convex sets.
- A finite union of convex sets has only finitely many membership alternations.
- A fixed-level up/down oscillation forces arbitrarily many alternations in one definable unary set.

No outside facts used.

## 5 S6 Notes

S6 may safely invoke the following proved form:

> If an argument produces a definable unary set whose membership must alternate arbitrarily often on an open interval, contradiction.

In derivative work, this is enough if the failure of derivative can be converted, after shrinking, into a fixed-threshold oscillation of some definable auxiliary quantity.

Do not cite S2 as having proved the full monotone-subinterval theorem unless another branch supplies weak monotonicity/cell decomposition.

## 6 Web Confirmation

No web, files, tools, or external sources used, per instruction.