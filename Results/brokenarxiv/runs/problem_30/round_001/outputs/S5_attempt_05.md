1. Assignment Restatement

Assemble the theorem from the component subclaims, verify that all predictive densities are proper and finite, check that domination is strict when `0 < alpha <= 1`, and note that the admissibility threshold does not depend on `T > 0`.

2. Subproof or Failure

This assembly requires the following prerequisites from earlier subproblems:

- SC1: the Jeffreys predictive density is
  \[
  q_J(y\mid x)=
  \frac{\Gamma((T+1)\alpha)}{\Gamma(\alpha)\Gamma(T\alpha)}
  \frac{x^\alpha y^{T\alpha-1}}{(x+y)^{(T+1)\alpha}},\qquad x,y>0.
  \]
- SC3: for `alpha > 1`, Blyth’s method proves admissibility of `q_J`.
- SC4: for `0 < alpha <= 1`, there exists a predictive density `q_*` whose KL risk is everywhere no larger than that of `q_J`.

Given SC1, propriety of `q_J` follows by the change of variables `u=y/(x+y)`. Then
\[
y=xu/(1-u),\qquad dy=x(1-u)^{-2}du,
\]
and the integral of `q_J` over `y>0` becomes
\[
\frac{\Gamma((T+1)\alpha)}{\Gamma(\alpha)\Gamma(T\alpha)}
\int_0^1 u^{T\alpha-1}(1-u)^{\alpha-1}\,du=1.
\]
Thus `q_J` is a proper density for every `x>0`, `alpha>0`, and `T>0`. It is finite for every `x,y>0`.

The posterior under Jeffreys’ prior is also proper: the marginal kernel is
\[
\beta^{-\alpha-1}\exp(-x/\beta),
\]
whose integral over `beta>0` is finite for every `x>0` and `alpha>0`.

For the admissible direction, SC3 supplies exactly the needed Blyth conclusion: when `alpha>1`, no predictive density can uniformly improve the KL risk of `q_J` with strict improvement somewhere. Therefore `q_J` is admissible.

For the inadmissible direction, SC4 supplies a dominating predictive density `q_*` for `0 < alpha <= 1`. To obtain inadmissibility rather than mere weak domination, one must check strictness: if SC4’s perturbation is nonzero and produces a genuine density different from `q_J` on a set of positive measure in `(x,y)`, then equality of KL risks everywhere would force equality of the predictive densities almost surely under the joint law for each beta, by the strict convexity/identifiability property of KL divergence. Since the perturbation is nontrivial, equality everywhere is impossible. Hence the domination is strict for at least one beta, so `q_J` is inadmissible.

Finally, the threshold is independent of `T`: in the assembled proof, `T>0` only appears in proper beta/gamma normalizing factors and in the beta-prime predictive shape. The admissibility split from SC3 and SC4 depends on `alpha` alone. Therefore the Jeffreys predictive density is admissible if and only if `alpha>1`, for every fixed `T>0`.

3. Solver Failure Output and Candidate Guidance with the Required YAML

```yaml
status: conditional_success
failure: null
candidate_guidance:
  - SC5 assembly is valid provided SC1, SC3, and SC4 are established.
  - S6 should ensure SC4 states strict domination, or at least supplies enough nontriviality to infer strictness from KL strict convexity.
  - S6 should verify any perturbed predictive density used in SC4 is normalized and finite for every x > 0.
```

4. Local Source Ledger

- Target theorem statement.
- S0 blueprint used only for assignment structure and identification of prerequisites.
- Standard facts used: beta integral, gamma integral, posterior propriety check, and strictness property of KL divergence.

5. Interface Notes for S6

The final theorem can be assembled once SC1, SC3, and SC4 are available. The main point to preserve is that SC4 must provide a genuinely nontrivial dominating predictive density; otherwise inadmissibility is not established. The propriety of `q_J` is elementary and independent of `T` except through positive beta-function parameters.

6. Web-Source Confirmation

No web sources, internet search, files, tools, simulations, CAS, notebooks, or code execution were used.