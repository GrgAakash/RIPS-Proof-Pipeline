## 1. Subproblem

Verify the boundary and distance setup for the branch target.

Let  
`X = S^3 \ int N(L)`  
be the exterior of the `n`-component link, with boundary tori `T_1,...,T_n`.

After Dehn filling `X(r_1,...,r_n) = M`, each attached surgery solid torus is denoted `V_i`.

## 2. Boundary Data

By hypothesis, the reducing sphere `S ⊂ M` intersects each surgery solid torus `V_i` in exactly one meridian disk.

Therefore

```text
P = S ∩ X
```

is obtained from the sphere `S` by deleting the interiors of those `n` meridian disks.

So `P` is a planar surface with exactly `n` boundary components, and there is exactly one boundary component on each torus `T_i`.

## 3. Slope Identification

The unique curve

```text
∂P ∩ T_i
```

is the boundary of the meridian disk `S ∩ V_i`.

In Dehn filling, the meridian disk of the attached solid torus has boundary equal to the filling slope. Hence

```text
slope(∂P ∩ T_i) = r_i.
```

Thus `∂P` has exactly one component on each `T_i`, and that component has slope `r_i`.

## 4. Meridional Filling

The original link exterior `X` recovers `S^3` by meridional filling:

```text
X(μ_1,...,μ_n) = S^3,
```

where `μ_i` is the meridian slope of the original link component `L_i` on `T_i`.

Thus the two relevant slopes on each boundary torus are:

```text
r_i  = surgery/filling slope producing M,
μ_i  = meridional slope recovering S^3.
```

## 5. YAML

```yaml
subproblem: boundary_data_and_distance_translation
objects:
  link: "L subset S^3"
  exterior: "X = S^3 \\ int N(L)"
  boundary_tori: ["T_1", "...", "T_n"]
  surgery_slopes: ["r_1", "...", "r_n"]
  meridian_slopes: ["mu_1", "...", "mu_n"]
  filled_manifold: "M = X(r_1,...,r_n)"
  reducing_sphere: "S subset M"
  punctured_surface: "P = S cap X"

verified_claims:
  - "S intersects each surgery solid torus V_i in exactly one meridian disk."
  - "P is S with n open disks removed."
  - "partial P has exactly one component on each T_i."
  - "The component of partial P on T_i has slope r_i."
  - "Meridional filling X(mu_1,...,mu_n) recovers S^3."
  - "The negation of 'some Delta(r_i,mu_i) <= 1' is 'for all i, Delta(r_i,mu_i) >= 2'."

distance_translation:
  desired_conclusion: "exists i such that Delta(r_i, mu_i) <= 1"
  contradiction_assumption: "for every i, Delta(r_i, mu_i) >= 2"
  reason: "Slope distance is a nonnegative integer."
```

## 6. Source Ledger

```yaml
sources_used:
  branch_target:
    - "Reducing sphere S intersects each surgery solid torus in exactly one meridian disk/core once."
    - "Goal: prove some Delta(r_i,mu_i) <= 1."
  branch_S0_blueprint:
    - "P = S cap X has one boundary component on each T_i with slope r_i."
    - "Assume contradiction Delta >= 2 for all i."
    - "Meridional filling recovers S^3."
  standard_background:
    - "In Dehn filling, the meridian of the attached solid torus represents the filling slope."
    - "The exterior of a link in S^3 meridionally filled along all components recovers S^3."
    - "Distance between slopes is their minimal geometric intersection number, hence a nonnegative integer."
external_sources: []
tools_used: []
```