```yaml
s5_subproblem:
  role: S5 Subproblem Solver
  round: 3
  assignment: Finish denominator translation
  status: solved
  dependencies:
    conditional:
      - If an earlier obstruction step proves Delta(slope, meridian) <= 1 for some boundary component, this S5 step converts that bound into p in {0,1}.
  conclusion: Under standard slope normalization, Delta(a/p, meridian)=|p|, so Delta<=1 implies p=0 or p=1.
```

**1. Claim**

Let a slope on a boundary torus be written in standard meridian-longitude coordinates as  
\[
a/p \leftrightarrow a\mu+p\lambda,
\]
with \(\gcd(a,p)=1\), and with slopes unoriented. If \(\mu\) is the meridian slope, then
\[
\Delta(a/p,\mu)=|p|.
\]

Hence if some prior obstruction proves \(\Delta(a/p,\mu)\le 1\), then standard normalization gives \(p\in\{0,1\}\).

**2. Setup**

Choose the usual oriented basis \((\mu,\lambda)\) for \(H_1(\partial X_L)\), where \(\mu\) is the meridian and \(\lambda\) is the preferred longitude. A primitive unoriented slope \(a/p\) is represented by the primitive class
\[
a\mu+p\lambda.
\]

The meridian is represented by
\[
\mu = 1\mu+0\lambda,
\]
i.e. by slope \(1/0\).

**3. Distance Computation**

For primitive slopes \(r=a/p\) and \(s=b/q\), their geometric intersection number is
\[
\Delta(r,s)=|aq-bp|.
\]

Taking \(s=\mu=1/0\), we get
\[
\Delta(a/p,\mu)
=
\left|a\cdot 0-1\cdot p\right|
=
|p|.
\]

So the denominator \(p\), up to sign, is exactly the distance from the meridian.

**4. Translation of \(\Delta\le 1\)**

If an earlier part of the proof gives
\[
\Delta(a/p,\mu)\le 1,
\]
then by the computation above,
\[
|p|\le 1.
\]

Since slopes are unoriented, replacing \(a\mu+p\lambda\) by its negative gives the same slope. Thus one may use the standard normalization \(p\ge 0\). Therefore
\[
p\in\{0,1\}.
\]

**5. Meridional and Integral Cases**

If \(p=0\), then \(\gcd(a,0)=1\), so \(|a|=1\). Thus the slope is
\[
\pm\mu,
\]
which is the meridian slope.

If \(p=1\), the slope is
\[
a/1,
\]
which is an integral slope in the standard meridian-longitude normalization.

Therefore \(\Delta(a/p,\mu)\le 1\) implies the slope is either meridional or integral.

**6. Local Source Ledger**

```yaml
local_source_ledger:
  used_sources:
    - target_theorem
    - s0_assignment
    - assigned_subproblem
    - standard_background:
        - primitive slope notation on a torus
        - meridian-longitude basis
        - slope distance formula Delta(a/p,b/q)=|aq-bp|
  external_dependencies:
    - name: obstruction_step
      status: conditional
      content_needed: proves Delta(boundary_slope, meridian) <= 1 for at least one boundary component
  not_used:
    - web
    - files
    - code_execution
    - calculators
    - prior_history
```