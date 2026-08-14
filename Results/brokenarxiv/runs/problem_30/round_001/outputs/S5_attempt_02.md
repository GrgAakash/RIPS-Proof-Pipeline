1. Assignment Restatement

Provide the decision-theoretic tools for the proof: the KL risk-difference identity, proper-prior Bayes optimality, a Blyth admissibility criterion suitable for generalized Bayes predictive densities, and the explicit perturbed-prior predictive density formula \(q_h\).

2. Subproof or Failure

For a predictive density \(q(y\mid x)\), define the KL risk
\[
R(\beta,q)
=
E_\beta\left[
\log \frac{p_T(Y;\beta)}{q(Y\mid X)}
\right],
\]
where \(X\sim \mathrm{Ga}(\alpha,\beta)\), \(Y\sim \mathrm{Ga}(T\alpha,\beta)\), independently, and
\[
p_T(y;\beta)
=
\frac{y^{T\alpha-1}}{\beta^{T\alpha}\Gamma(T\alpha)}e^{-y/\beta}.
\]

For two predictive densities \(q_1,q_2\),
\[
R(\beta,q_1)-R(\beta,q_2)
=
E_\beta\left[
\log \frac{q_2(Y\mid X)}{q_1(Y\mid X)}
\right].
\]
Indeed, the true-density term \(\log p_T(Y;\beta)\) cancels.

If \(\pi\) is a proper prior on \(\beta\), its posterior predictive density is
\[
q_\pi(y\mid x)
=
\int_0^\infty p_T(y;\beta)\,\pi(d\beta\mid x).
\]
This density minimizes integrated KL risk
\[
\int R(\beta,q)\,\pi(d\beta)
\]
over all predictive densities \(q\). Equivalently, for every \(q\),
\[
\int \{R(\beta,q)-R(\beta,q_\pi)\}\,\pi(d\beta)\ge 0.
\]
This is the standard posterior pointwise KL projection argument: conditional on \(X=x\), the posterior predictive \(q_\pi(\cdot\mid x)\) minimizes
\[
\int D_{\mathrm{KL}}\bigl(p_T(\cdot;\beta),q(\cdot\mid x)\bigr)\,\pi(d\beta\mid x).
\]

A useful Blyth criterion is the following. Let \(q_0\) be a generalized Bayes predictive density. Suppose there exists a sequence of proper priors \(\pi_n\) with Bayes predictive densities \(q_n\) such that
\[
\int \{R(\beta,q_0)-R(\beta,q_n)\}\,\pi_n(d\beta)\to 0.
\]
If the priors \(\pi_n\) put positive mass on every nonempty open subset of \((0,\infty)\), then \(q_0\) is admissible. The proof is standard: if some \(q\) dominated \(q_0\), with strict improvement on an open set, then
\[
\int \{R(\beta,q_0)-R(\beta,q)\}\,\pi_n(d\beta)
\]
would stay positive along \(n\), contradicting Bayes optimality of \(q_n\) and the assumed vanishing gap.

For a perturbed Jeffreys-type prior
\[
\pi_h(\beta)=\frac{h(\beta)}{\beta},
\]
where \(h\ge 0\) is measurable and chosen so that the relevant marginal integrals are finite, the corresponding predictive density is
\[
q_h(y\mid x)
=
\frac{
\int_0^\infty p_T(y;\beta)p_\alpha(x;\beta)\,h(\beta)\beta^{-1}\,d\beta
}{
\int_0^\infty p_\alpha(x;\beta)\,h(\beta)\beta^{-1}\,d\beta
}.
\]
Using
\[
p_\alpha(x;\beta)
=
\frac{x^{\alpha-1}}{\beta^\alpha\Gamma(\alpha)}e^{-x/\beta},
\]
this becomes
\[
q_h(y\mid x)
=
\frac{
\frac{x^{\alpha-1}y^{T\alpha-1}}{\Gamma(\alpha)\Gamma(T\alpha)}
\int_0^\infty h(\beta)\beta^{-(T+1)\alpha-1}e^{-(x+y)/\beta}\,d\beta
}{
\frac{x^{\alpha-1}}{\Gamma(\alpha)}
\int_0^\infty h(\beta)\beta^{-\alpha-1}e^{-x/\beta}\,d\beta
}.
\]
After cancellation,
\[
q_h(y\mid x)
=
\frac{y^{T\alpha-1}}{\Gamma(T\alpha)}
\frac{
\int_0^\infty h(\beta)\beta^{-(T+1)\alpha-1}e^{-(x+y)/\beta}\,d\beta
}{
\int_0^\infty h(\beta)\beta^{-\alpha-1}e^{-x/\beta}\,d\beta
}.
\]

For \(h\equiv 1\), this reduces to the Jeffreys predictive density
\[
q_J(y\mid x)
=
\frac{\Gamma((T+1)\alpha)}{\Gamma(\alpha)\Gamma(T\alpha)}
\frac{x^\alpha y^{T\alpha-1}}{(x+y)^{(T+1)\alpha}}.
\]

3. Solver Failure Output and Candidate Guidance With Required YAML

```yaml
status: success
failure: null
candidate_guidance: []
```

4. Local Source Ledger

Used only:
- Target theorem statement.
- S0 blueprint for assignment scope only.
- Standard decision-theoretic facts about KL risk, Bayes predictive densities, and Blyth’s method.
- Direct algebra from the Gamma density in the problem statement.

No external files, web search, answer keys, simulations, CAS tools, notebooks, or code execution were used.

5. Interface Notes for S6

This subproof supplies the common risk-difference identity and the perturbed-prior formula \(q_h\). SC3 can use the Blyth criterion with proper cutoff priors \(\pi_n(d\beta)\propto w_n(\beta)\beta^{-1}d\beta\). SC4 can use the risk-difference identity and \(q_h\) formula to test domination by bounded positive perturbations \(h\).

6. Web-Source Confirmation

No web sources were used.