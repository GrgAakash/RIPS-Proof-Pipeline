```yaml
stage: S4
role: Subproblem Solver
round: 3
mode: solver-only-no-history
subproblem: Audit obstruction hypotheses
assumption: exact reducible full surgery core-once theorem is available
status: conditional
verdict: construction supplies the core-once data, but reducibility needs an extra nontriviality check
```

## 1. Claim Under Audit

Assume an exact theorem of the following needed form:

> If a full Dehn filling of a hyperbolic link exterior in `S^3` is reducible, and there is a reducing sphere meeting each attached solid-torus core exactly once, then one filling slope is meridional or integral.

Then the natural construction from `P` gives the required “core-once” sphere after filling along the boundary slopes of `P`.

## 2. Filling And Capping Construction

Let the boundary slope of `P` on the `i`th boundary torus be `r_i`.

Perform full Dehn filling of `X_L` along all slopes `r_1,...,r_N`. Since `∂P` has one component on each boundary torus and each component has slope `r_i`, each boundary component of `P` bounds a meridian disk in the corresponding attached solid torus.

Capping `P` with these `N` meridian disks gives a closed surface

`S = P ∪ D_1 ∪ ... ∪ D_N`.

Because `P` is planar with `N` boundary components, `S` is a sphere.

## 3. Core-Once Hypothesis

For each filled component, the attached solid torus has core `c_i`.

The capping disk `D_i` is a meridian disk of that solid torus, so `c_i` intersects `D_i` transversely once. The core `c_i` is disjoint from `P` and from the other capping disks.

Therefore

`|c_i ∩ S| = 1`

for every `i`.

So the “core-once” part of the bottleneck theorem is satisfied, provided the theorem requires one intersection with each surgery core.

## 4. Reducibility Hypothesis

The capped surface `S` is a sphere in the filled manifold. To apply the obstruction theorem, `S` must be a reducing sphere, i.e. it must not bound a 3-ball.

This is the delicate point.

The construction proves that `S` is a sphere meeting every filling core once, but it does not by itself prove that `S` is essential. Incompressibility of `P` in `X_L` strongly suggests nontriviality, but the implication

`P incompressible in X_L`  
`=> capped sphere S is a reducing sphere after filling`

is not automatic without an additional argument.

The missing check is: if `S` bounded a ball in the filled manifold, why would that contradict incompressibility, boundary-incompressibility, hyperbolicity, spanning, or `N >= 3`?

That contradiction is not established from the assigned data alone.

## 5. Conditional Conclusion

Conditional on proving that the capped sphere `S` is a reducing sphere, all other hypotheses of the exact reducible full-surgery core-once theorem appear satisfied:

- `L` is hyperbolic.
- The filling is full, one slope on every component.
- The capped planar surface is a sphere.
- Each surgery core intersects the sphere exactly once.

The remaining gap is precisely the reducibility/essentiality of the capped sphere.

## 6. Local Source Ledger

```yaml
local_sources:
  target_theorem:
    used: true
    content_used:
      - N >= 3
      - L hyperbolic in S^3
      - P incompressible spanning planar surface
      - one boundary component of P on each boundary torus
      - desired slope conclusion p in {0,1}
  guidance:
    used: true
    content_used:
      - exact bottleneck theorem is reducible full surgery core-once theorem
      - do not assume theorem unless exact
  S0_blueprint:
    used: true
    content_used:
      - audit obstruction hypotheses
  assignment:
    used: true
    content_used:
      - assume exact theorem is available
      - check capping/reducing-sphere construction hypotheses
      - identify unchecked gaps
  standard_background:
    used: true
    content_used:
      - Dehn filling along a boundary slope caps that boundary curve by a meridian disk
      - planar surface with all boundary components capped becomes a sphere
      - core of attached solid torus meets a meridian disk once
      - reducing sphere means an essential sphere, not merely any embedded sphere
external_sources: []
tools_used: []
```