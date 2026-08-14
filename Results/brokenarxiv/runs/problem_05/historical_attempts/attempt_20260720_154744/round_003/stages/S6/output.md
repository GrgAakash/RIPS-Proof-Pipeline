**1. Composition Map**

S0’s route works through S1, S2, S4, and S5 except for the S3 obstruction.

- S1 supplies the capped sphere \(\widehat P\) after Dehn filling along the boundary slopes.
- S2 proves \(\widehat P\) cannot bound a ball because each filling core intersects it once.
- S4 verifies the conditional applicability of the desired reducible-surgery obstruction.
- S5 translates \(\Delta(a_i/p_i,\mu_i)\le 1\) into \(p_i\in\{0,1\}\).

The only missing ingredient is the specialized link-surgery theorem:

> If surgery on every component of an \(n\)-component link in \(S^3\), \(n\ge 3\), gives a reducible manifold with a reducing sphere meeting every surgery core exactly once, then at least one surgery slope has distance at most \(1\) from the meridian.

I cannot honestly prove that theorem from the allowed material and genuinely standard background in this no-source/no-history setting. Therefore the final proof below is a conditional proof, and the exact obstacle is recorded.

---

**2. Final Proof Wrapped Markers**

`BEGIN FINAL PROOF`

Let \(L=L_1\cup\cdots\cup L_N\subset S^3\) be a hyperbolic \(N\)-component link, \(N\ge 3\), and let  
\[
X_L=S^3\setminus \operatorname{int}N(L).
\]
Let \(P\subset X_L\) be a connected incompressible spanning planar surface with exactly one boundary component on each boundary torus \(T_i=\partial N(L_i)\). Write the slope of \(\partial P\cap T_i\) as
\[
r_i=a_i/p_i
\]
in standard meridian-longitude coordinates, so \(r_i\) is represented by the primitive class
\[
a_i\mu_i+p_i\lambda_i.
\]

Perform Dehn filling on every \(T_i\) along the slope \(r_i\). Let \(V_i\) be the filling solid torus and let \(c_i\) be its core. Since \(\partial P\cap T_i\) has slope \(r_i\), it bounds a meridian disk \(D_i\subset V_i\). Hence
\[
\widehat P=P\cup D_1\cup\cdots\cup D_N
\]
is a closed embedded surface in the filled manifold
\[
M=L(r_1,\dots,r_N).
\]

Because \(P\) is connected planar with \(N\) boundary components, capping its \(N\) boundary circles by disks gives
\[
\widehat P\cong S^2.
\]
Moreover, each core \(c_i\) intersects the disk \(D_i\) exactly once and is disjoint from \(P\) and from the other disks \(D_j\). Therefore
\[
|c_i\cap \widehat P|=1
\]
for every \(i\).

The sphere \(\widehat P\) does not bound a 3-ball in \(M\). Indeed, if \(\widehat P=\partial B\) for some 3-ball \(B\), then every closed curve in \(M\), in particular each \(c_i\), would have even mod-2 intersection number with \(\partial B\). But \(c_i\) intersects \(\widehat P\) exactly once, contradiction. Thus \(\widehat P\) is a reducing sphere.

At this point one needs the following specialized reducible-surgery obstruction:

\[
\textbf{Required obstruction.}
\]
If \(L\subset S^3\) is an \(n\)-component link, \(n\ge 3\), and surgery on every component along slopes \(r_1,\dots,r_n\) produces a reducible manifold with a reducing sphere intersecting every surgery core exactly once, then for some component \(i\),
\[
\Delta(r_i,\mu_i)\le 1.
\]

Assuming this obstruction, there exists \(i\) such that
\[
\Delta(r_i,\mu_i)\le 1.
\]
For \(r_i=a_i/p_i\), represented by \(a_i\mu_i+p_i\lambda_i\), and the meridian \(\mu_i=1/0\), the slope distance is
\[
\Delta(a_i/p_i,\mu_i)=|a_i\cdot 0-1\cdot p_i|=|p_i|.
\]
Hence \(|p_i|\le 1\). With the usual normalization \(p_i\ge 0\), this gives
\[
p_i\in\{0,1\}.
\]
If \(p_i=0\), then \(r_i\) is meridional. If \(p_i=1\), then \(r_i\) is integral. Therefore at least one boundary component of \(P\) has meridional or integral slope.

`END FINAL PROOF`

---

**3. Composer YAML Fixed Schema**

```yaml
status: incomplete_conditional
theorem_proved: false
conditional_on:
  - name: core_once_reducible_link_surgery_obstruction
    statement: >
      If surgery on every component of an n-component link in S^3, n >= 3,
      produces a reducible manifold with a reducing sphere intersecting every
      surgery core exactly once, then at least one surgery slope has distance
      at most 1 from the meridian.
resolved_components:
  - capping_planar_surface_to_sphere
  - core_intersection_once
  - non_ball_bounding_parity_argument
  - denominator_distance_translation
unresolved_components:
  - precise proof or exact admissible citation of the reducible-surgery obstruction
exact_obstacle: >
  The needed obstruction is a specialized Scharlemann/Gordon-Luecke-type
  theorem for full surgery on links. It was not proved in S3 and cannot be
  reconstructed honestly from only the supplied material and standard background
  without importing a precise external theorem.
```

---

**4. Source Ledger Markers**

`BEGIN SOURCE LEDGER`

Allowed inputs used:

- Target theorem.
- Guidance items 1 and 2.
- Round-3 S0 blueprint.
- Round-3 S1 capping output.
- Round-3 S2 parity/non-ball-bounding output.
- Round-3 S3 obstruction audit and failure report.
- Round-3 S4 conditional applicability audit.
- Round-3 S5 denominator translation.

External sources used: none.

Web used: no.

Prior-round artifacts used: no.

`END SOURCE LEDGER`

---

**5. Completion Checklist Markers**

`BEGIN COMPLETION CHECKLIST`

- Capping construction included: yes.
- \(\widehat P\cong S^2\) justified under connected planar convention: yes.
- Each filling core intersects \(\widehat P\) once: yes.
- \(\widehat P\) shown not to bound a ball: yes.
- Reducible-surgery obstruction proved: no.
- Reducible-surgery obstruction clearly isolated: yes.
- Denominator conclusion derived conditionally: yes.
- Fake proof avoided: yes.

`END COMPLETION CHECKLIST`

---

**6. Web-Source Confirmation Markers**

`BEGIN WEB-SOURCE CONFIRMATION`

Web access used: no.

Internet sources consulted: none.

Reason: user explicitly prohibited web, internet, files, tools, APIs, code execution, calculators, scripts, memory, prior history.

`END WEB-SOURCE CONFIRMATION`

---

**7. LaTeX Artifact**

```latex
\begin{proof}
Let \(L=L_1\cup\cdots\cup L_N\subset S^3\) be a hyperbolic
\(N\)-component link, \(N\ge 3\), and let
\[
X_L=S^3\setminus \operatorname{int}N(L).
\]
Let \(P\subset X_L\) be a connected incompressible spanning planar surface
with exactly one boundary component on each boundary torus
\(T_i=\partial N(L_i)\). Write the slope of \(\partial P\cap T_i\) as
\(r_i=a_i/p_i\), represented by the primitive class
\[
a_i\mu_i+p_i\lambda_i.
\]

Fill each \(T_i\) along the slope \(r_i\). Let \(V_i\) be the corresponding
filling solid torus and \(c_i\) its core. Since \(\partial P\cap T_i\) has
slope \(r_i\), it bounds a meridian disk \(D_i\subset V_i\). Hence
\[
\widehat P=P\cup D_1\cup\cdots\cup D_N
\]
is a closed embedded surface in the filled manifold
\[
M=L(r_1,\dots,r_N).
\]
Because \(P\) is connected planar with \(N\) boundary components,
\(\widehat P\cong S^2\).

Each core \(c_i\) intersects \(D_i\) exactly once and is disjoint from
\(P\) and from \(D_j\) for \(j\ne i\). Thus
\[
|c_i\cap \widehat P|=1
\]
for every \(i\).

The sphere \(\widehat P\) cannot bound a 3-ball. If
\(\widehat P=\partial B\), then every closed curve has even mod-\(2\)
intersection with \(\partial B\), whereas each \(c_i\) intersects
\(\widehat P\) exactly once. This contradiction shows that \(\widehat P\)
is a reducing sphere.

We now require the following reducible-surgery obstruction: if surgery on
every component of an \(n\)-component link in \(S^3\), \(n\ge 3\), produces
a reducible manifold with a reducing sphere intersecting every surgery core
exactly once, then for some \(i\),
\[
\Delta(r_i,\mu_i)\le 1.
\]
Applying this obstruction gives such an index \(i\).

Finally,
\[
\Delta(a_i/p_i,\mu_i)=\Delta(a_i/p_i,1/0)
  =|a_i\cdot 0-1\cdot p_i|
  =|p_i|.
\]
Therefore \(|p_i|\le 1\). With the usual normalization \(p_i\ge 0\), we get
\(p_i\in\{0,1\}\). If \(p_i=0\), the slope is meridional; if \(p_i=1\), the
slope is integral. Thus at least one boundary component of \(P\) has
meridional or integral slope.
\end{proof}
```

This is not a completed unconditional proof: the exact unresolved obstacle is the core-once reducible link-surgery obstruction.