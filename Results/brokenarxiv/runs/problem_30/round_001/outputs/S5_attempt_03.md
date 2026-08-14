1. Assignment Restatement

For fixed `alpha > 1` and `T > 0`, prove the Jeffreys-prior Bayesian predictive density is admissible under KL loss. The requested method is Blyth: construct proper cutoff priors of the form `w_n(beta)/beta`, let their Bayes predictive densities be `q_n`, and show the integrated KL gap between `q_J` and `q_n` tends to zero, with the convergence relying on `alpha > 1`.

2. Subproof or Failure

Let

```text
p_alpha(x | beta) = x^{alpha-1} exp(-x/beta) / (beta^alpha Gamma(alpha)),
p_T(y | beta) = y^{T alpha-1} exp(-y/beta) / (beta^{T alpha} Gamma(T alpha)).
```

The Jeffreys prior is `pi_J(beta) ∝ 1/beta`. Its posterior after observing `x` is proportional to

```text
beta^{-(alpha+1)} exp(-x/beta),
```

and its predictive density is

```text
q_J(y | x)
= Gamma((T+1)alpha)/(Gamma(alpha) Gamma(T alpha))
  x^alpha y^{T alpha-1} / (x+y)^((T+1)alpha).
```

Now construct proper priors. For `n >= 3`, define

```text
w_n(beta) =
  1                         if 1/n <= beta <= n,
  log(n beta)/log n          if 1/n^2 <= beta < 1/n,
  log(n^2/beta)/log n        if n < beta <= n^2,
  0                         otherwise.
```

Then `0 <= w_n <= 1`, `w_n(beta) -> 1` for each fixed `beta > 0`, and

```text
C_n := ∫_0^∞ w_n(beta) d beta / beta < ∞.
```

Let

```text
pi_n(beta) = C_n^{-1} w_n(beta)/beta.
```

Let `q_n` be the Bayes predictive density under `pi_n`. Since `pi_n` is proper, `q_n` is Bayes among all predictive densities under the prior `pi_n`.

Write

```text
m_J(x) = ∫ p_alpha(x | beta) d beta / beta,
m_J(x,y) = ∫ p_alpha(x | beta) p_T(y | beta) d beta / beta,
```

and similarly

```text
m_n(x) = ∫ p_alpha(x | beta) w_n(beta) d beta / beta,
m_n(x,y) = ∫ p_alpha(x | beta) p_T(y | beta) w_n(beta) d beta / beta.
```

The normalizing constant `C_n` cancels in the posterior predictive, so

```text
q_n(y | x) = m_n(x,y)/m_n(x),
q_J(y | x) = m_J(x,y)/m_J(x).
```

For the integrated KL gap,

```text
Delta_n
:= ∫ pi_n(beta) [R(beta, q_J) - R(beta, q_n)] d beta.
```

Standard Bayes predictive optimality gives `Delta_n >= 0`. Also,

```text
Delta_n
= ∫∫∫ pi_n(beta) p_alpha(x | beta) p_T(y | beta)
    log(q_n(y | x)/q_J(y | x)) dy dx d beta.
```

Substituting the mixture forms and integrating out `beta` gives

```text
Delta_n
= C_n^{-1} ∫∫ m_n(x,y)
   log{ m_n(x,y)m_J(x) / [m_J(x,y)m_n(x)] } dy dx.
```

Since `0 <= w_n <= 1`, we have `m_n(x,y) <= m_J(x,y)`, hence

```text
log{ m_n(x,y)/m_J(x,y) } <= 0.
```

Therefore

```text
Delta_n
<= C_n^{-1} ∫∫ m_n(x,y) log{m_J(x)/m_n(x)} dy dx.
```

Because `∫ m_n(x,y) dy = m_n(x)`, this becomes

```text
Delta_n
<= C_n^{-1} ∫ m_n(x) log{m_J(x)/m_n(x)} dx.      (*)
```

Now compute the ratio. Up to constants independent of `w_n`,

```text
m_J(x)
= x^{alpha-1}/Gamma(alpha) ∫ beta^{-(alpha+1)} exp(-x/beta) d beta
= Gamma(alpha) x^{-1}/Gamma(alpha)
= x^{-1}.
```

More importantly, with the substitution `u = x/beta`,

```text
m_n(x)/m_J(x)
= Gamma(alpha)^{-1} ∫_0^∞ u^{alpha-1} e^{-u} w_n(x/u) du.
```

Thus `m_n(x)/m_J(x)` is an average of `w_n(x/U)` where `U ~ Ga(alpha, 1)`. Since `w_n = 1` whenever `1/n <= x/u <= n`, the deficit is supported on

```text
x/u < 1/n  or  x/u > n,
```

that is,

```text
u > n x  or  u < x/n.
```

Set

```text
a_n(x) := 1 - m_n(x)/m_J(x).
```

Then

```text
0 <= a_n(x) <= P(U > n x) + P(U < x/n).
```

Using `log(1/t) <= (1-t)/t` is too crude near zero. Instead split the integral in `(*)` according to the two cutoff regions and use the exact logarithmic taper. The only nonzero contribution comes from where `w_n` differs from `1`, namely roughly `beta < 1/n` or `beta > n`. The lower tail is harmless because the Gamma likelihood contributes `exp(-x/beta)`. The upper tail is decisive.

For the upper tail `beta > n`, the loss from cutoff is controlled by

```text
∫_n^∞ beta^{-1} P_beta(X in transition/tail) d beta.
```

After the change of variables `x = beta z`, the relevant tail bound reduces to an integral of order

```text
(log n)^{-1} ∫_n^{n^2} beta^{-1} beta^{-(alpha-1)} d beta
  + ∫_{n^2}^∞ beta^{-1} beta^{-(alpha-1)} d beta.
```

Equivalently,

```text
O((log n)^{-1} n^{-(alpha-1)}) + O(n^{-2(alpha-1)}).
```

This tends to zero exactly when `alpha > 1`. The lower cutoff contributes exponentially small terms after the same substitution because `exp(-x/beta)` suppresses `beta ↓ 0`.

Hence

```text
Delta_n -> 0   as n -> ∞,        when alpha > 1.
```

By Blyth’s admissibility criterion, since `q_n` is Bayes under the proper prior `pi_n`, `q_J` is the pointwise limit generalized Bayes rule, and the integrated Bayes regret `Delta_n` tends to zero, `q_J` is admissible for `alpha > 1`.

3. Solver Failure Output and Candidate Guidance with Required YAML

```yaml
status: partial
failure_point: "The proof gives the standard Blyth construction and identifies the alpha > 1 tail rate, but the final cutoff-gap estimate is presented as a bound outline rather than a fully expanded epsilon-level integral calculation."
candidate_guidance:
  - "S6 should expand the transition-region estimate from inequality (*) into a line-by-line bound using the explicit logarithmic cutoff w_n."
  - "The key required rate is the upper-tail integral O((log n)^-1 n^{-(alpha-1)}) + O(n^{-2(alpha-1)}), with the lower-tail cutoff exponentially negligible."
  - "No external lemma beyond Blyth's criterion and elementary Gamma tail/integral estimates should be needed."
```

4. Local Source Ledger

Only the supplied theorem statement, the assigned S0 blueprint for task planning, and standard Bayesian decision-theoretic facts were used. No external sources, web search, code execution, simulations, files, or answer keys were used.

5. Interface Notes for S6

The load-bearing output is the Blyth sequence

```text
pi_n(beta) ∝ w_n(beta)/beta
```

with logarithmic cutoff on `[1/n^2,1/n]`, flat part on `[1/n,n]`, and logarithmic cutoff on `[n,n^2]`.

The admissibility interface is:

```text
Delta_n = ∫ pi_n(beta) [R(beta,q_J)-R(beta,q_n)] d beta >= 0,
Delta_n -> 0 for alpha > 1.
```

The point needing polishing is the fully explicit bound from `(*)` to the displayed rate.

6. Web-Source Confirmation

No web sources were used.