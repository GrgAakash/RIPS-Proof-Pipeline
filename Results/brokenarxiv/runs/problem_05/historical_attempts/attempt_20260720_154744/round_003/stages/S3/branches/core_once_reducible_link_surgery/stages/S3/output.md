1. YAML

```yaml
subproblem: S3 labeled intersection graph setup
status: partial_setup_with_gap
result:
  can_define:
    - reducible-surgery punctured sphere P = S ∩ X
    - vertices/labels/endpoints from boundary components on link-exterior tori
    - endpoint multiplicities assuming Delta(r_i, mu_i) >= 2
  cannot_define_from_given_data:
    - a second planar surface Q in X with boundary slope mu_i on every T_i
    - a full pair of dual labeled planar graphs G_P and G_Q
    - parity/sign rules that require both planar graphs
obstacle: "The branch target supplies only the reducing sphere S after r-filling. Meridional filling gives S^3, but no specific sphere/disk system Q with boundary on all T_i and slope mu_i is specified."
```

2. Surfaces

Let  
`X = S^3 \ int N(L)` be the link exterior, with boundary tori  
`T_1, ..., T_n`.

Let `M = X(r_1, ..., r_n)` be the filled manifold. For each component, let `V_i` be the attached solid torus and let `K_i` be its core.

The reducing sphere `S ⊂ M` satisfies

```text
|S ∩ K_i| = 1  for every i = 1,...,n.
```

After isotoping `S` to meet each `V_i` in one meridian disk of `V_i`, define

```text
P = S ∩ X.
```

Then `P` is a planar surface. Since `S` meets each surgery core once, `P` has exactly one boundary component on each `T_i`, and that boundary component has slope `r_i`.

Thus

```text
∂P = p_1 ∪ ... ∪ p_n,
p_i ⊂ T_i,
slope(p_i) = r_i.
```

3. Candidate Second Surface And Gap

The S0 blueprint says meridional filling recovers `S^3`. Indeed,

```text
X(μ_1, ..., μ_n) = S^3.
```

To build the standard two-graph machinery, one needs another properly embedded planar surface

```text
Q ⊂ X
```

whose boundary components lie on the same tori and have meridional slopes `μ_i`.

But the branch target does not provide such a `Q`.

Meridional filling alone gives attached solid tori in `S^3`; it does not canonically produce a planar surface in `X` with one meridional boundary component on every `T_i`. A system of meridian disks for the attached solid tori lives inside the filling solid tori, not inside `X`. Their co-cores are also filling data, not by themselves a second punctured sphere or planar surface in the exterior.

So the usual paired labeled graphs `G_P` and `G_Q` cannot be fully set up from the stated data alone.

4. Graph On `P`

One can still define the part of the graph supported on `P`, assuming a second surface `Q` has been supplied.

Suppose, additionally, that `Q ⊂ X` is a properly embedded planar surface with boundary components

```text
q_j ⊂ T_j,
slope(q_j) = μ_j,
```

at least one on each relevant `T_j`.

Put `P` and `Q` in general position and isotope them so that `|P ∩ Q|` is minimal among such choices. Then `P ∩ Q` consists of properly embedded arcs and possibly closed curves. Minimality plus incompressibility/boundary-incompressibility hypotheses, if available, are usually used to remove closed curves and trivial arcs. Those hypotheses are not supplied here, so this cleanup cannot be asserted without extra assumptions.

After capping `∂P` by the meridian disks `S ∩ V_i`, one obtains the sphere `S`. The graph `G_P` on `S` is defined as follows:

```text
vertices: the capping disks corresponding to p_i = ∂P ∩ T_i
vertex label: i
edges: arc components of P ∩ Q
edge endpoints: where the arc meets ∂P
endpoint label: j if the endpoint lies on q_j ⊂ ∂Q ∩ T_j
```

Equivalently, each vertex of `G_P` corresponds to one boundary component of `P`, hence to one surgery torus `T_i`.

Because `P` has exactly one boundary component on each `T_i`, `G_P` has exactly `n` vertices.

5. Endpoint Counts Under `Delta(r_i, μ_i) >= 2`

On each torus `T_i`, the boundary curve `p_i` has slope `r_i`, while a meridional boundary curve `q_i` of `Q` has slope `μ_i`.

Their geometric intersection number is

```text
Δ(r_i, μ_i).
```

If `Q` has exactly one meridional boundary component on `T_i`, then the vertex of `G_P` corresponding to `p_i` has exactly

```text
Δ(r_i, μ_i)
```

endpoints labeled `i`.

Under the contradiction hypothesis

```text
Δ(r_i, μ_i) >= 2 for every i,
```

each such vertex has at least two endpoints with label `i`.

More generally, if `Q` has `m_i` meridional boundary components on `T_i`, then the vertex corresponding to `p_i` has

```text
m_i Δ(r_i, μ_i)
```

endpoints labeled `i`, hence at least `2m_i` such endpoints under the same hypothesis.

The same statement with `P` and `Q` reversed would give endpoint counts in `G_Q`, but only after `Q` is actually specified.

6. Parity And Sign Rules

The standard sign convention is this.

Choose orientations of `P`, `Q`, and of each boundary torus `T_i`. Around each vertex of `G_P`, the boundary orientation of the corresponding capped disk gives a cyclic order of edge endpoints. A vertex is called positive or negative depending on whether its induced boundary orientation agrees with the chosen orientation convention on the corresponding torus. The same is done for vertices of `G_Q`.

For an edge `e` of `P ∩ Q`:

```text
e is positive in G_P
  if its two endpoints lie on vertices of G_P with the same sign;

e is negative in G_P
  if its two endpoints lie on vertices of G_P with opposite signs.
```

Similarly for `G_Q`.

The usual parity rule says:

```text
An edge is positive in G_P iff it is negative in G_Q,
and negative in G_P iff it is positive in G_Q.
```

But this parity rule is a statement about two oriented surfaces and their two associated graphs. Since the branch target supplies only `P`, and does not supply a second planar surface `Q`, the parity rule cannot be invoked yet.

Source ledger:

```yaml
used_sources:
  - branch_target
  - branch_S0_blueprint
  - assigned_subproblem
  - standard_background:
      - Dehn filling notation
      - punctured reducing sphere construction
      - labeled intersection graph conventions for two properly embedded planar surfaces
not_used:
  - web
  - files
  - code_execution
  - calculators
  - prior_history
```