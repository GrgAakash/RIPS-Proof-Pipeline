**1 Assignment**

S1 deliverable: formalize slope predicates and derivative-failure cases.

Let `J(t)` define the interval and write `f(t)` as shorthand for the definable graph of `f`.

For `x in J`, define right and left secant quotients:

```text
q_+(x,y) = (f(y)-f(x))/(y-x),   x < y
q_-(x,y) = (f(x)-f(y))/(x-y),   y < x
```

The following are first-order definable.

Right arbitrarily close slopes:

```text
Arb^<_+(x,a) :=
  forall d>0 exists y [J(y) and x<y<x+d and f(y)-f(x) < a(y-x)].

Arb^>_+(x,a) :=
  forall d>0 exists y [J(y) and x<y<x+d and f(y)-f(x) > a(y-x)].
```

Left arbitrarily close slopes:

```text
Arb^<_-(x,a) :=
  forall d>0 exists y [J(y) and x-d<y<x and f(x)-f(y) < a(x-y)].

Arb^>_-(x,a) :=
  forall d>0 exists y [J(y) and x-d<y<x and f(x)-f(y) > a(x-y)].
```

Eventual lower and upper slope bounds:

```text
Ev^>_+(x,a) :=
  exists d>0 forall y [J(y) and x<y<x+d -> f(y)-f(x) > a(y-x)].

Ev^<_+(x,a) :=
  exists d>0 forall y [J(y) and x<y<x+d -> f(y)-f(x) < a(y-x)].
```

and similarly on the left using `f(x)-f(y)` and `x-y`.

Open lower and upper slope cuts:

```text
LC_sigma(x,a) := exists c [a<c and Ev^>_sigma(x,c)].
UC_sigma(x,a) := exists c [c<a and Ev^<_sigma(x,c)].
```

Thus `LC_sigma(x,-)` is an initial segment and `UC_sigma(x,-)` is a final segment.

One-sided finite derivative limit:

```text
Lim_+(x,l) :=
  forall eps>0 exists d>0 forall y [
    J(y) and x<y<x+d ->
    (l-eps)(y-x) < f(y)-f(x) < (l+eps)(y-x)
  ].
```

Likewise,

```text
Lim_-(x,l) :=
  forall eps>0 exists d>0 forall y [
    J(y) and x-d<y<x ->
    (l-eps)(x-y) < f(x)-f(y) < (l+eps)(x-y)
  ].
```

Then

```text
D(x) := exists l [Lim_-(x,l) and Lim_+(x,l)].
```

So `D` and `J \ D` are definable.

**2 Subproof / Failure**

For each side `sigma in {+,-}`:

`Lim_sigma(x,l)` iff

```text
forall a [LC_sigma(x,a) <-> a<l]
and
forall b [UC_sigma(x,b) <-> l<b].
```

Proof: if `q_sigma -> l`, every `a<l` lies below some eventual lower bound and every `b>l` lies above some eventual upper bound. Conversely, `LC(l-eps)` and `UC(l+eps)` give eventual trapping between `l-eps` and `l+eps`.

Failure taxonomy:

```text
OneSidedFailure_sigma(x) := not exists l Lim_sigma(x,l).

UnboundedAbove_sigma(x) := forall B Arb^>_sigma(x,B).
UnboundedBelow_sigma(x) := forall B Arb^<_sigma(x,B).

Osc_sigma(x) :=
  exists a<b [Arb^<_sigma(x,a) and Arb^>_sigma(x,b)].

NonRealizedCut_sigma(x) :=
  Bnd_sigma(x)
  and not Osc_sigma(x)
  and not exists l Lim_sigma(x,l).

Mismatch(x) :=
  exists l_-, l_+ [
    Lim_-(x,l_-) and Lim_+(x,l_+) and l_- != l_+
  ].
```

where

```text
Bnd_sigma(x) := exists a,b [Ev^>_sigma(x,a) and Ev^<_sigma(x,b)].
```

Thus every `x in J \ D` falls into one of:

```text
one-sided failure,
unboundedness,
oscillation,
non-realized cut,
mismatch.
```

More precisely: if one side lacks a finite limit, then either it is unbounded, oscillatory, or bounded non-oscillatory with a non-realized slope cut. If both one-sided limits exist, failure of the two-sided derivative is exactly mismatch.

**3 YAML**

```yaml
S1:
  role: formal_slope_cut_definitions
  objects_defined:
    - right_secant_slope
    - left_secant_slope
    - arbitrary_close_slope_lt_gt
    - eventual_slope_bounds
    - lower_slope_cut
    - upper_slope_cut
    - one_sided_limits
    - derivative_domain_D
    - failure_taxonomy
  definability_status: proved_first_order
  derivative_failure_cases:
    - one_sided_failure
    - unboundedness
    - oscillation
    - non_realized_cut
    - mismatch
  dependencies:
    - ordered_field_arithmetic
    - definability_of_J
    - definability_of_graph_of_f
  external_sources_used: false
```

**4 Ledger**

```text
Claim: Arbitrarily close slope inequalities are definable.
Status: proved by explicit formulas.

Claim: Eventual lower/upper slope bounds are definable.
Status: proved by explicit formulas.

Claim: Lower/upper slope cuts are definable.
Status: proved as quantified formulas over eventual bounds.

Claim: One-sided derivative limits are definable.
Status: proved by epsilon-delta first-order formulas.

Claim: D is definable.
Status: proved as exists l [Lim_- and Lim_+].

Claim: Derivative failure splits into one-sided failure or mismatch.
Status: proved directly from definition of two-sided derivative.

Claim: One-sided failure splits into unboundedness, oscillation, or non-realized cut.
Status: proved by bounded/unbounded dichotomy plus oscillatory/non-oscillatory dichotomy.
```

**5 S6 Notes**

Use these definable predicates to reduce any hypothetical open interval inside `J \ D` to an open interval of one failure type. The next branch should rule out open intervals of unboundedness, oscillation, non-realized cuts, and mismatch using weak o-minimality plus monotonicity/continuity.

**6 Web Confirmation**

No web, external sources, files, tools, APIs, or prior history were used.