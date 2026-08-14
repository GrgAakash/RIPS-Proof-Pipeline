## 1. YAML

```yaml
stage: S1
role: Subproblem Solver
round: 3
mode: no-history
assigned_subproblem: "Prove the capping construction rigorously and note assumptions about connectedness of planar surface."
result: solved
dependencies_used:
  - standard_definition_of_Dehn_filling
  - standard_surface_capping_by_meridian_disks
assumptions:
  - P is properly embedded in X_L
  - P has exactly one boundary component on each boundary torus
  - each boundary component is an essential slope on its torus
  - to obtain one capped sphere, P is connected
connectedness_note: "If P is not connected, capping gives a disjoint union of spheres, one for each planar component, not necessarily a single sphere."
```

## 2. Local Source Ledger

No external sources used. Only standard background:

```yaml
local_source_ledger:
  target_theorem: used
  guidance: used_only_as_context
  S0_blueprint: used
  assigned_subproblem: used
  external_web: none
  files: none
  tools: none
  prior_history: none
  standard_background:
    - Dehn filling attaches a solid torus so that the chosen slope bounds a meridian disk.
    - A connected compact genus-zero surface with k boundary components caps to S^2 after attaching k disks.
    - The core circle of a solid torus intersects a meridian disk algebraically and geometrically once.
```

## 3. Subproblem Statement

Let \(L=L_1\cup\cdots\cup L_N\) be an \(N\)-component link with exterior

\[
X_L=S^3\setminus \operatorname{int}\nu(L),
\]

and boundary tori \(T_i=\partial \nu(L_i)\). Let \(P\subset X_L\) be a properly embedded planar spanning surface with exactly one boundary component on each \(T_i\). Write

\[
\alpha_i=\partial P\cap T_i
\]

for the boundary slope on \(T_i\).

After Dehn filling \(X_L\) along the slopes \(\alpha_1,\dots,\alpha_N\), prove that \(P\) caps off to a sphere \(\widehat P\), and that each filling core intersects \(\widehat P\) exactly once.

## 4. Proof

Let

\[
M=X_L(\alpha_1,\dots,\alpha_N)
\]

be the manifold obtained by Dehn filling each boundary torus \(T_i\) along the slope \(\alpha_i\). Thus for each \(i\), a solid torus \(V_i\) is attached to \(T_i\) so that the curve \(\alpha_i\subset T_i\) bounds a meridian disk \(D_i\subset V_i\).

Since \(P\) has exactly one boundary component on \(T_i\), and that boundary component has slope \(\alpha_i\), we may choose \(D_i\) with

\[
\partial D_i=\partial P\cap T_i.
\]

Define

\[
\widehat P
=
P\cup D_1\cup\cdots\cup D_N
\subset M.
\]

The disks \(D_i\) lie in distinct filling solid tori, and each is attached to \(P\) along exactly one boundary circle. Therefore \(\widehat P\) is a closed embedded surface.

If \(P\) is connected and planar, then \(P\) is a compact connected genus-zero surface with \(N\) boundary components. Capping each boundary component by a disk produces a compact connected closed genus-zero surface. Hence

\[
\widehat P\cong S^2.
\]

Now let \(c_i\subset V_i\) be the core circle of the \(i\)-th filling solid torus. A meridian disk \(D_i\) of \(V_i\) intersects the core \(c_i\) transversely in one point. Since \(c_i\) lies entirely inside \(V_i\), it is disjoint from \(P\) and from all disks \(D_j\) with \(j\neq i\). Therefore

\[
|c_i\cap \widehat P|=|c_i\cap D_i|=1.
\]

Thus every filling core intersects the capped surface \(\widehat P\) geometrically once.

## 5. Connectedness Assumption

The statement “\(P\) caps to a sphere \(\widehat P\)” requires \(P\) to be connected.

If “planar surface” is being used in the connected sense, then the proof above applies directly. If disconnected planar surfaces are allowed, then capping all boundary components produces a disjoint union of spheres, one for each connected component of \(P\). In that case, each filling core still intersects the capped component corresponding to its boundary circle exactly once, but there is not necessarily a single sphere meeting all filling cores.

Thus S0 should explicitly assume or invoke the convention that a spanning planar surface is connected.

## 6. Output for Later Stages

The capping construction is valid in the following precise form:

```yaml
capping_construction:
  input:
    manifold: "X_L with boundary tori T_1,...,T_N"
    surface: "connected properly embedded planar P"
    boundary_condition: "one boundary component of P on each T_i"
    filling_slopes: "alpha_i = slope of ∂P on T_i"
  conclusion:
    filled_manifold: "M = X_L(alpha_1,...,alpha_N)"
    capped_surface: "widehat P = P union meridian disks D_i"
    topology: "widehat P is S^2"
    filling_core_intersections: "each filling core c_i intersects widehat P exactly once"
  caveat:
    disconnected_P: "capping gives a disjoint union of spheres, not necessarily one sphere"
```