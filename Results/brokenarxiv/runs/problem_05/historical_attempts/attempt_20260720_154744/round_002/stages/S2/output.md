1. YAML
```yaml
solver: S2
assigned_subproblem: "Show the capped sphere S is a reducing sphere in the filled manifold"
scope: "Only proves non-ball-bounding once S1 capping is available; records hypotheses for later obstruction"
uses_prior_history: false
uses_tools_or_web: false
standard_background:
  - "Dehn filling notation"
  - "mod 2 intersection number"
  - "definition of reducing sphere"
```

2. Setup

Let \(M\) be the manifold obtained from \(X_L\) by Dehn filling each boundary torus along the slope represented by the corresponding boundary component of \(P\). By S1’s capping construction, \(P\) caps off with one meridian disk in each attached solid torus, producing an embedded sphere
\[
S \subset M.
\]

For each filled solid torus \(V_i\), let \(c_i\) denote its core circle. Since the capping disk in \(V_i\) is a meridian disk, \(c_i\) intersects that disk transversely exactly once and is disjoint from \(P\) and from the other capping disks. Hence
\[
|c_i \cap S| = 1
\]
for every filled component \(i\).

3. Claim

The sphere \(S\) is a reducing sphere in \(M\): it is an embedded \(2\)-sphere and it does not bound a \(3\)-ball in \(M\).

4. Proof

The embeddedness and spherical topology of \(S\) are supplied by the capping construction.

It remains to prove that \(S\) cannot bound a \(3\)-ball. Suppose, for contradiction, that \(S=\partial B\) for some embedded \(3\)-ball \(B \subset M\).

Take any filling core \(c_i\). It is a closed curve in \(M\), transverse to \(S\), and it intersects \(S\) exactly once. But a closed curve has mod \(2\) intersection number zero with the boundary of a compact \(3\)-manifold region. Equivalently, every time a closed curve enters the ball \(B\), it must later leave it, so its total number of transverse intersections with \(\partial B=S\) is even.

This contradicts \(|c_i \cap S|=1\). Therefore \(S\) does not bound a \(3\)-ball.

Thus \(S\) is a reducing sphere in the filled manifold \(M\).

5. Hypotheses Needed Later For The Bottleneck Obstruction

For the later “core-once reducible filling obstruction,” the needed hypotheses should include at least:

- \(X_L\) is the exterior of a hyperbolic link, hence compact, orientable, irreducible, boundary-irreducible, atoroidal, and with torus boundary.
- \(M\) is obtained by Dehn filling boundary tori of \(X_L\).
- The capped surface \(S\subset M\) is a reducing sphere.
- At least one attached filling core \(c_i\) intersects \(S\) transversely exactly once.
- The obstruction must apply to reducible Dehn fillings where a filling core has algebraic or mod \(2\) intersection number one with a reducing sphere.
- Any use of the obstruction must state whether it concerns one filled cusp or simultaneous multi-cusp filling, and whether other filled slopes are arbitrary, nonmeridional, or required to satisfy distance assumptions.

6. Local Source Ledger

```yaml
local_sources:
  problem_statement:
    used_for:
      - target theorem
      - link exterior notation
      - spanning planar surface hypotheses
  S0_blueprint:
    used_for:
      - fill along boundary slopes
      - cap P to sphere S
      - prove S reducing
      - record obstruction hypotheses
  assigned_subproblem:
    used_for:
      - restrict proof to non-ball-bounding argument
      - use filling core intersecting S exactly once
  standard_background:
    - "Dehn filling notation"
    - "mod 2 intersection number"
    - "definition of reducing sphere"
external_sources: []
tools_used: []
```