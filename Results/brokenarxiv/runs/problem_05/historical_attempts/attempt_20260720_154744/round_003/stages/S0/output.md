## 1. Target Decomposition

Goal: prove that for an incompressible planar spanning surface  
\(P\subset X_L\), where \(L\subset S^3\) is an \(N\)-component hyperbolic link with \(N\ge 3\), at least one boundary slope of \(P\) has denominator \(p\in\{0,1\}\).

Blueprint route:

1. Let the boundary slope of \(P\) on the \(i\)-th boundary torus \(T_i\) be \(r_i=a_i/p_i\).
2. Perform full Dehn filling of \(X_L\) along the slopes \(r_1,\dots,r_N\).
3. Since each \(\partial_i P\) bounds a meridian disk in the corresponding filling solid torus, the surface \(P\) caps off to an embedded sphere
   \[
   \widehat P\subset X_L(r_1,\dots,r_N).
   \]
4. Each capping disk intersects the corresponding filling core once, so \(\widehat P\) intersects every filling core exactly once.
5. Show \(\widehat P\) is a reducing sphere.
6. Apply a precise reducible-surgery obstruction: if surgery on all components of a link in \(S^3\) gives a reducible manifold with a reducing sphere intersecting every surgery core once, then at least one filling slope has meridional distance \(\le 1\).
7. Since \(\Delta(a_i/p_i,\mu_i)=|p_i|\) in standard meridian-longitude coordinates, some \(|p_i|\le 1\), hence \(p_i\in\{0,1\}\) up to the usual unoriented slope convention.

The main burden is Step 5 or Step 6. The cleanest blueprint is to isolate Step 6 as the central theorem to be proved by later solvers, unless accepted as standard under exact hypotheses.

## 2. Available Tools

Allowed standard background, stated precisely:

- **Hyperbolic link exterior is irreducible and boundary-irreducible.**  
  If \(X_L\) admits a complete finite-volume hyperbolic metric with torus cusps, then \(X_L\) is irreducible, atoroidal, and boundary-irreducible.

- **Slope distance formula.**  
  In meridian-longitude coordinates, if \(r=a/p\) and \(\mu=1/0\), then
  \[
  \Delta(r,\mu)=|p|.
  \]

- **Dehn filling capping principle.**  
  If a properly embedded surface \(P\subset X_L\) has boundary slope \(r_i\) on \(T_i\), then after filling \(T_i\) along \(r_i\), the corresponding boundary component of \(P\) caps off by a meridian disk of the filling solid torus.

- **Reducible surgery obstruction to be proved or explicitly accepted.**  
  Exact target statement:
  If surgery on all components of an \(N\)-component link in \(S^3\), \(N\ge 3\), produces a reducible manifold and there is a reducing sphere intersecting every surgery core exactly once, then at least one surgery slope has meridional distance at most \(1\).

This last statement should not be used informally. It should be assigned as a major subproblem unless the final proof explicitly names it as a genuinely standard Scharlemann/Gordon-Luecke type theorem with exact hypotheses.

## 3. Subclaim Support Graph

### Subclaim A, suggested S1  
For the boundary slopes \(r_i\) of \(P\), the filled manifold
\[
M=X_L(r_1,\dots,r_N)
\]
contains a sphere \(\widehat P\) obtained by capping \(P\) with meridian disks of the filling solid tori.

Supports: direct Dehn filling construction.

Depends on: none.

### Subclaim B, suggested S1  
The sphere \(\widehat P\) intersects each filling core exactly once.

Supports: each capping disk is a meridian disk of the corresponding filling solid torus.

Depends on: Subclaim A.

### Subclaim C, suggested S2  
The sphere \(\widehat P\) is essential in \(M\), hence is a reducing sphere.

Possible proof route: argue that if \(\widehat P\) bounded a ball, then after removing the filling solid tori, \(P\) would be boundary-parallel or compressible in \(X_L\), contradicting incompressibility and the fact that \(P\) has one boundary component on each of \(N\ge 3\) distinct boundary tori of a hyperbolic link exterior.

This step needs careful handling. Incompressibility alone may not automatically imply the capped sphere is reducing after arbitrary boundary-slope filling, so S2 should prove the exact implication needed here.

Depends on: Subclaims A, B; hyperbolic irreducibility/boundary-irreducibility.

### Subclaim D, suggested S3-S4  
Core-once reducible filling obstruction:

Let \(L\subset S^3\) be an \(N\)-component link, \(N\ge 3\). Suppose full surgery along slopes \(r_1,\dots,r_N\) gives a reducible manifold \(M\), and some reducing sphere intersects every surgery core exactly once. Then
\[
\min_i \Delta(r_i,\mu_i)\le 1.
\]

This is the hardest external-style ingredient. It should either be proved directly or cited only as a precisely formulated standard Scharlemann/Gordon-Luecke type reducible surgery theorem.

Depends on: Subclaims B, C.

### Subclaim E, suggested S5  
Translate the obstruction into the desired slope statement:

Since \(r_i=a_i/p_i\) and \(\mu_i=1/0\),
\[
\Delta(r_i,\mu_i)=|p_i|.
\]
Thus \(\Delta(r_i,\mu_i)\le 1\) implies \(p_i=0\) or \(|p_i|=1\). Under unoriented slope convention this is exactly meridional or integral.

Depends on: Subclaim D.

## 4. Hardest Step Prediction

The hardest step is Subclaim D, the core-once reducible filling obstruction.

Subclaim C is also nontrivial, but it is local to the constructed surface. Subclaim D is a global surgery theorem. The proof likely requires Scharlemann cycle / planar graph machinery or a Gordon-Luecke style reducible surgery argument. Because the guidance explicitly warns not to assume it informally, the final proof must either:

- prove this obstruction in full under the exact hypotheses above, or
- identify it as a genuinely standard theorem with exact statement, hypotheses, and conclusion.

Without Subclaim D, the argument only proves the existence of a core-once reducing sphere, not the denominator bound.

## 5. Failure-Mode Checks

- Do not merely say “reducible surgery theorem” without exact hypotheses. The needed theorem is specifically for full surgery on a link in \(S^3\), with a reducing sphere meeting every surgery core once.

- Verify \(\widehat P\) is actually reducing. A capped planar surface is always a sphere, but it could a priori bound a ball. This must be ruled out.

- Check slope conventions. In coordinates \(a/p\), meridian is denominator \(0\), integral slopes have denominator \(1\), and distance from meridian is \(|p|\).

- Do not use hyperbolicity to claim anything stronger than standard irreducibility, boundary-irreducibility, and nonsplit behavior unless explicitly justified.

- Ensure \(N\ge 3\) is used. It is relevant both to preventing degenerate planar-surface behavior and to the intended reducible filling obstruction.

## 6. Subproblem Assignment Table

| Solver | Assignment | Output Needed |
|---|---|---|
| S1 | Prove capping construction | Show \(P\) caps to a sphere \(\widehat P\) after filling along its boundary slopes, and each core is intersected once. |
| S2 | Prove essentiality of \(\widehat P\) | Show \(\widehat P\) is a reducing sphere, using incompressibility of \(P\), \(N\ge 3\), and hyperbolic irreducibility/boundary-irreducibility. |
| S3 | Establish reducible filling obstruction | Either prove or precisely formulate the Scharlemann/Gordon-Luecke type theorem under the exact core-once hypotheses. |
| S4 | Audit obstruction hypotheses | Check that the theorem from S3 applies to the filled manifold built from \(P\). |
| S5 | Finish denominator translation | Convert \(\Delta(r_i,\mu_i)\le 1\) into \(p_i\in\{0,1\}\). |

## 7. Web-Source Confirmation

No web search, internet access, files, tools, code execution, calculators, APIs, or prior task history were used.