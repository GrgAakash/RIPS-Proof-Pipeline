```yaml
solver: S3
assigned_subproblem: core-once reducible filling obstruction
status: unsolved
disposition: exact standard theorem not identified as genuinely standard
```

**1. Problem Restatement**

Assigned obstruction:

Given a hyperbolic `N`-component link exterior `X_L`, `N >= 3`, suppose full Dehn filling along slopes `r_i` gives a reducible manifold and there is a reducing sphere meeting every filling core exactly once. Show, or justify as standard, that some slope satisfies

```text
Delta(r_i, mu_i) <= 1.
```

Equivalently, not all filling slopes can have meridional distance at least `2`.

**2. Attempted Reduction**

Let `S` be the reducing sphere in the filled manifold, and let `K_i` be the filling cores. Since `S` meets each `K_i` once, deleting neighborhoods of the cores turns `S` into a planar surface `P subset X_L` with one boundary component on each boundary torus and boundary slope `r_i`.

Thus the obstruction is equivalent to saying:

If a hyperbolic link exterior in `S^3` contains a planar spanning surface whose capped-off surface after filling is a reducing sphere meeting every surgery core once, then at least one boundary slope is meridional or integral.

This is precisely the bottleneck needed by S0.

**3. Standard Background Considered**

Standard background named:

- Dehn filling and slope distance.
- Reducing sphere and irreducibility.
- Hyperbolic link exteriors are irreducible, boundary-irreducible, atoroidal, and anannular.
- Capping a planar spanning surface after Dehn filling produces a sphere meeting each filling core once.
- Gordon-Luecke type reducible surgery philosophy: reducible Dehn fillings on hyperbolic 3-manifolds are strongly constrained.

However, these standard facts alone do not prove the stated multi-cusp, all-cores-once obstruction.

**4. Candidate Exact Theorem Needed**

The needed input appears to be a Scharlemann-type reducible surgery theorem for links in `S^3`, in the following exact form:

> Let `L` be a link in `S^3`, and suppose surgery on all components of `L` produces a reducible manifold. If there is a reducing sphere in the surgered manifold intersecting every surgery core exactly once, then at least one surgery coefficient has denominator `0` or `1`; equivalently, for some component, the surgery slope has distance at most `1` from the meridian.

I cannot certify this exact formulation as genuinely standard from the allowed materials alone. It is close to known reducible-surgery results of Scharlemann and Gordon-Luecke, but the “intersects every filling core once” and “some denominator <= 1” formulation needs an exact citation or proof.

**5. Result**

I do not prove the obstruction from the allowed standard background.

I also do not mark it as established standard background, because the exact accepted theorem with these hypotheses has not been identified rigorously enough.

So the assigned subproblem remains unsolved.

**6. Local Source Ledger**

```yaml
local_sources_used:
  - problem_statement
  - role_prompt
  - S0_blueprint
  - assigned_subproblem
  - guidance
external_sources_used: []
tools_used: []
web_search_used: false
code_execution_used: false
prior_history_used: false
standard_background_named:
  - Dehn filling and slope distance
  - Reducing sphere and irreducibility
  - Hyperbolic link exteriors are irreducible, boundary-irreducible, atoroidal, and anannular
  - Capping a planar spanning surface after Dehn filling produces a sphere meeting each filling core once
  - Gordon-Luecke type reducible surgery philosophy
```

Candidate guidance item:

Identify or prove the exact Scharlemann/Gordon-Luecke reducible surgery theorem for links in `S^3` stating that a reducible full surgery with a reducing sphere meeting every surgery core once forces at least one surgery slope to have meridional distance `<= 1`.