```yaml
role: S3
round: 3
subproblem: reducible_filling_obstruction
decision: C
status: unsolved
output_type: branch_lemma_target
web_used: false
tools_used: false
```

**1. Claim**
I cannot honestly discharge the assigned obstruction from only genuinely standard background without importing a specialized Scharlemann/Gordon-Luecke link-surgery theorem whose exact statement I cannot verify here.

The needed obstruction is:

If `L` is an `N >= 3` component hyperbolic link in `S^3`, and full Dehn filling along slopes `r_i` gives a reducible manifold `M`, with a reducing sphere `S` intersecting every filling core exactly once, then for some component `i`,
\[
\Delta(r_i,\mu_i)\le 1,
\]
equivalently `r_i = a/p` has `p in {0,1}`.

**2. Fit To Target**
If this obstruction is available, the main target follows by filling each boundary torus of `X_L` along the boundary slope of the planar spanning surface `P`.

After filling, capping the `N` boundary components of `P` by meridian disks in the attached solid tori gives a sphere. Because `P` is planar with one boundary component on each torus, that sphere intersects each attached filling core exactly once. The expected S0 route is then to show this sphere is a reducing sphere, apply the obstruction, and conclude some boundary slope has denominator `0` or `1`.

**3. Why I Am Not Choosing A Or B**
I do not have a direct proof short enough to be reliable here. A graph-of-intersection proof would need the full machinery of labelled fat-vertex graphs on the reducing sphere and another surface, parity rules, Scharlemann cycles, and a final contradiction when all denominators are at least `2`. That is exactly the specialized reducible link-surgery theorem named in the guidance.

I also cannot safely choose B because the assignment explicitly says not to cite informally. The theorem needed is plausible and standard in the Scharlemann/Gordon-Luecke circle, but I cannot state its bibliographic theorem number or fully verified hypotheses from memory without risk of handwaving.

**4. Local Source Ledger**
```yaml
used_sources:
  - target_theorem
  - guidance_item_1
  - guidance_item_2
  - S0_assignment
  - assigned_subproblem
  - standard_background:
      - Dehn filling notation
      - slope distance from meridian equals denominator in reduced meridian-longitude coordinates
      - capping a planar spanning surface after filling produces a sphere meeting each filling core once
not_used:
  - web
  - files
  - tools
  - calculators
  - scripts
  - prior_history
```

**5. Blocker**
The missing ingredient is precisely the specialized reducible surgery result for links in `S^3` with a reducing sphere meeting every attached surgery core once. Without that theorem or a supplied proof route, the obstruction is not derivable from elementary 3-manifold background alone.

**6. Branch Lemma Target**
Prove the following lemma.

```yaml
branch_lemma_target:
  name: core_once_reducible_link_surgery_obstruction
  statement: >
    Let L be an n-component link in S^3, n >= 3. Let M be obtained by
    Dehn surgery on every component of L with slopes r_1,...,r_n.
    Suppose M is reducible and has a reducing sphere S such that S
    intersects each surgery solid torus in exactly one meridian disk,
    equivalently S intersects each surgery core exactly once. Then for
    some component i, Delta(r_i, mu_i) <= 1.
  required_precision:
    - State whether L must be nonsplit, hyperbolic, or merely a link in S^3.
    - State whether M may contain S^1 x S^2 summands.
    - State whether the reducing sphere must be chosen with minimal intersection
      with the surgery solid tori.
    - Conclude explicitly that in coordinates r_i = a_i / p_i relative to
      the meridian, some p_i is 0 or 1.
```
