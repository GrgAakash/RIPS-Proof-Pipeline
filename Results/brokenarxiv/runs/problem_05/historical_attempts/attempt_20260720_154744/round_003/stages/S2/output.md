```yaml
role: S2
round: 3
subproblem: "Show widehat P does not bound a 3-ball in the filled manifold when each filling core intersects it once."
status: solved
claim_strength: elementary
uses_incompressibility: false
uses_hyperbolicity: false
uses_N_ge_3: false_for_obstruction
main_obstruction: "A closed curve has mod-2 intersection number 0 with the boundary of a 3-ball."
```

## 1. Setup

Let \(P\subset X_L\) be a spanning planar surface with one boundary component on each boundary torus. Fill each boundary torus along the slope represented by \(\partial P\). Denote the filled manifold by

\[
M=X_L(\partial P),
\]

and cap \(P\) by the meridian disks of the attached solid tori. The result is a closed surface

\[
\widehat P \subset M.
\]

Since \(P\) is planar and all its boundary components are capped by disks, \(\widehat P\cong S^2\).

Let \(c_i\) be the core of the \(i\)-th attached solid torus. Each \(c_i\) meets the corresponding capping disk once and is disjoint from the rest of \(\widehat P\). Hence

\[
|c_i\cap \widehat P|=1
\]

for every filling core \(c_i\), after the standard transverse positioning.

## 2. Claim

\[
\widehat P
\]
does not bound a 3-ball in \(M\).

## 3. Proof

Suppose, for contradiction, that \(\widehat P=\partial B\) for some embedded 3-ball \(B\subset M\).

Let \(c_i\) be any filling core. It is a closed curve in \(M\), and it intersects \(\widehat P=\partial B\) transversely in exactly one point.

But a closed curve cannot intersect the boundary of a compact 3-dimensional region in an odd number of transverse points. Equivalently, each time the curve crosses \(\partial B\), it switches between being inside \(B\) and outside \(B\). Since the curve is closed, it must return to its starting side, so the total number of crossings is even.

Thus

\[
|c_i\cap \partial B|\equiv 0 \pmod 2.
\]

This contradicts

\[
|c_i\cap \widehat P|=1.
\]

Therefore \(\widehat P\) does not bound a 3-ball in \(M\).

## 4. Homological Form

The same argument can be phrased as mod-2 intersection theory. If \(\widehat P=\partial B\), then \([\widehat P]=0\in H_2(M;\mathbb Z_2)\). Therefore every closed 1-cycle has zero mod-2 intersection with \(\widehat P\). But each filling core \(c_i\) satisfies

\[
[c_i]\cdot [\widehat P]=1\in \mathbb Z_2,
\]

a contradiction.

## 5. Dependence Record

Incompressibility of \(P\) is not needed for this subproblem.

The argument only uses:

- \(\widehat P\) is a closed embedded sphere after capping;
- each filling core is a closed curve;
- each filling core intersects \(\widehat P\) exactly once;
- a closed curve has even mod-2 intersection with the boundary of a 3-ball.

No hyperbolicity, irreducibility, boundary-irreducibility, or \(N\ge 3\) is needed for the parity obstruction itself.

## 6. Local Source Ledger

```yaml
local_sources:
  - name: "Standard mod-2 intersection parity"
    type: "standard background"
    content_used: "A closed curve intersects the boundary of a compact 3-chain evenly mod 2."
  - name: "Capping construction"
    type: "standard Dehn filling background"
    content_used: "After filling along the boundary slope of P, each boundary component of P caps by a meridian disk, and the attached solid-torus core intersects that disk once."
  - name: "Planar surface fact"
    type: "standard topology"
    content_used: "A planar surface capped along all boundary components becomes S^2."
```