**1. Assignment Restatement**

Show only the local capping claim: after Dehn filling each boundary torus of `X_L` along the boundary slope `r_i` of `P`, the planar spanning surface `P` caps off to an embedded sphere `S`, and the core of each filling solid torus intersects `S` exactly once. Also record the slope convention needed later for `Delta(a_i/p_i, mu_i)=|p_i|`.

**2. Subproof Or Failure**

Let the boundary tori of `X_L` be `T_1, ..., T_N`, one for each component of `L`. Since `P` is a spanning planar surface, `P` has exactly one boundary component on each `T_i`. Denote this boundary curve by `gamma_i = P ∩ T_i`.

For each `i`, let `r_i` be the slope represented by `gamma_i`. Perform Dehn filling along `r_i`, so attach a solid torus `V_i` to `T_i` in such a way that `gamma_i` bounds a meridian disk `D_i` of `V_i`.

Standard background used: in Dehn filling along a slope `r` on a torus boundary component, the attached solid torus is glued so that the slope `r` bounds a meridian disk in the attached solid torus.

Because the `V_i` are attached to distinct boundary components, the disks `D_i` have pairwise disjoint interiors, and their interiors are disjoint from `X_L`. Therefore

```text
S = P ∪ D_1 ∪ ... ∪ D_N
```

is an embedded closed surface in the filled manifold.

Topologically, `P` is planar with exactly `N` boundary components. Capping each boundary component with one disk gives a closed connected genus-zero surface. Hence `S` is homeomorphic to `S^2`.

Now consider the filling core `c_i ⊂ V_i`. In the standard model `V_i = D^2 × S^1`, a meridian disk is `D^2 × {pt}` and the core is `{0} × S^1`; these meet transversely in exactly one point. Since `S ∩ V_i = D_i`, it follows that `c_i` intersects `S` exactly once. Also, for `j ≠ i`, `c_i` is disjoint from `D_j` and from `P ⊂ X_L`, so there are no additional intersections.

Thus, after Dehn filling along the boundary slopes of `P`, the capped surface `S` is an embedded sphere, and each filling core intersects `S` exactly once.

Slope notation for later: fix the standard meridian-longitude basis `(mu_i, lambda_i)` on `T_i`. A slope written `a_i/p_i` represents the primitive unoriented class

```text
±(a_i mu_i + p_i lambda_i),
```

with `gcd(a_i, p_i)=1`. The meridian is `mu_i = 1/0`. The geometric intersection number between slopes `a/p` and `b/q` is

```text
Delta(a/p, b/q) = |aq - bp|.
```

Therefore

```text
Delta(a_i/p_i, mu_i) = Delta(a_i/p_i, 1/0) = |a_i·0 - 1·p_i| = |p_i|.
```

**3. Solver Failure Output And Candidate Guidance**

```yaml
solver: S1
status: success
assigned_subproblem: "Capping P after filling along its boundary slopes gives an embedded sphere meeting each filling core once; establish slope notation."
failure: null
proved_claims:
  - "Each boundary component gamma_i of P bounds a meridian disk D_i in the corresponding filling solid torus V_i after r_i-Dehn filling."
  - "P union the meridian disks D_i is an embedded closed surface."
  - "Since P is planar with N boundary components, the capped surface is S^2."
  - "Each filling core c_i intersects the capped sphere exactly once."
  - "With slope convention a/p = ±(a mu + p lambda), Delta(a/p, mu)=|p|."
candidate_guidance:
  - "S6 may use this only as the local capping/intersection input."
  - "This subproof does not establish that the sphere is reducing."
  - "This subproof does not prove the core-once reducible filling obstruction."
dependencies_used:
  - "Definition of Dehn filling along a slope."
  - "Standard solid torus model: meridian disk intersects core once."
  - "Classification fact: a connected planar surface capped along all boundary components is S^2."
```

**4. Local Source Ledger**

No external sources, files, tools, calculators, code execution, APIs, prior memory, or web search used.

Standard background named precisely:

- Dehn filling convention: filling along slope `r` attaches a solid torus whose meridian bounds `r`.
- Solid torus model `D^2 × S^1`: core `{0} × S^1` intersects a meridian disk `D^2 × {pt}` once.
- Surface classification fact: a connected planar surface with all boundary components capped by disks becomes `S^2`.

**5. Interface Notes For S6**

S6 can import the conclusion that the filled manifold contains an embedded sphere `S` obtained from `P`, and every filling core meets `S` exactly once. S6 still needs separate justification that `S` is a reducing sphere if that is required for the bottleneck obstruction.

**6. Web-Source Confirmation**

No web sources were used.