## 1. YAML

```yaml
role: S5
subproblem: final slope-distance translation and conditional assembly
status: conditional
uses_bottleneck_obstruction: conditional_only
claims_full_theorem: false
main_dependency:
  - bottleneck_obstruction: "For some boundary component slope r_i of P, Delta(r_i, mu_i) <= 1."
standard_background:
  - "Standard slope parametrization on a torus"
  - "Standard geometric intersection formula for slopes"
```

## 2. Assigned Claim

Conditional on the bottleneck obstruction:

> If for some boundary torus \(T_i\), the boundary slope \(r_i\) of \(P\) satisfies  
> \[
> \Delta(r_i,\mu_i)\le 1,
> \]
> then that boundary slope is meridional or integral. Equivalently, if
> \[
> r_i=a_i/p_i
> \]
> in lowest terms, then after the usual sign normalization \(p_i\ge 0\), one has
> \[
> p_i\in\{0,1\}.
> \]

## 3. Dependencies

This subproblem uses only:

1. The conditional bottleneck obstruction:
   \[
   \exists i \quad \Delta(r_i,\mu_i)\le 1.
   \]

2. Standard slope parametrization on a torus: with a chosen meridian-longitude basis \((\mu_i,\lambda_i)\), a slope \(a_i/p_i\) in lowest terms represents the primitive class
   \[
   a_i\mu_i+p_i\lambda_i,
   \]
   with the meridian represented by \(1/0\).

3. Standard geometric intersection formula for slopes:
   \[
   \Delta(a/p,c/d)=|ad-pc|.
   \]

No separate supporting lemma is asserted.

## 4. Slope-Distance Translation

Let \(r_i=a_i/p_i\) be a boundary slope in lowest terms, and let \(\mu_i=1/0\). Then

\[
\Delta(r_i,\mu_i)
=
\Delta(a_i/p_i,1/0)
=
|a_i\cdot 0-p_i\cdot 1|
=
|p_i|.
\]

Thus the conditional obstruction \(\Delta(r_i,\mu_i)\le 1\) gives

\[
|p_i|\le 1.
\]

Since \(a_i/p_i\) is written in lowest terms and slope signs are identified by multiplying numerator and denominator by \(-1\), we may normalize \(p_i\ge 0\). Hence

\[
p_i\in\{0,1\}.
\]

If \(p_i=0\), then \(r_i=1/0\), the meridional slope.  
If \(p_i=1\), then \(r_i=a_i/1\), an integral slope.

Therefore the boundary component corresponding to \(T_i\) has meridional or integral slope.

## 5. Conditional Assembly

Assume the bottleneck obstruction has been proved or is available for the given incompressible spanning planar surface \(P\subset X_L\). Then there exists at least one boundary component \(\partial_i P\subset T_i\) whose slope \(r_i\) satisfies

\[
\Delta(r_i,\mu_i)\le 1.
\]

By the slope-distance calculation above, writing \(r_i=a_i/p_i\) in lowest terms gives \(p_i\in\{0,1\}\). Hence that boundary component is meridional or integral.

Thus the target theorem follows from the bottleneck obstruction. Without that obstruction, this subproblem proves only the final translation and conditional assembly, not the full theorem.

## 6. Local Source Ledger

```yaml
local_sources:
  problem_statement:
    used_for:
      - target theorem
      - notation X_L
      - hypotheses on L and P
  S0_blueprint:
    used_for:
      - conditional assembly structure
      - instruction that final proof occurs once obstruction is proved/applied
  assignment:
    used_for:
      - limiting scope to slope-distance translation and conditional assembly
  guidance:
    used_for:
      - conditional use of Delta(r_i, mu_i) <= 1
      - warning not to assume obstruction unconditionally
  standard_background:
    - "Standard slope parametrization on a torus"
    - "Standard geometric intersection formula for slopes"
external_sources: []
tools_used: []
web_search_used: false
prior_history_used: false
```