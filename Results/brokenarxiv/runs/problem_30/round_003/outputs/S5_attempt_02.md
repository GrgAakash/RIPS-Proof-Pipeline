## 1 Assignment Restatement

Prove only the `alpha > 1` half: the Jeffreys-prior Bayesian predictive density is admissible under predictive KL loss. Use a predictive-KL Blyth argument with gamma boundary estimates. Do not prove the `0 < alpha <= 1` inadmissibility half; only say how S6 should combine this with S4 if S4 proves the perturbation lemma.

## 2 Subproof Or Failure

Set `lambda = 1 / beta`. Then

\[
f_r(z\mid \lambda)=\frac{\lambda^r z^{r-1}e^{-\lambda z}}{\Gamma(r)},\qquad z>0,
\]

and Jeffreys prior is \(\mu(d\lambda)=d\lambda/\lambda\). Put \(\gamma=T\alpha\) and \(k=(T+1)\alpha=\alpha+\gamma\).

The formal Jeffreys predictive density is

\[
q_J(y\mid x)
=
\frac{\Gamma(k)}{\Gamma(\alpha)\Gamma(\gamma)}
\frac{x^\alpha y^{\gamma-1}}{(x+y)^k}.
\]

For \(h\ge 0\), define

\[
A_r^h(z)=\frac{z^r}{\Gamma(r)}
\int_0^\infty u^{r-1}e^{-zu}h(u)\,du.
\]

The Bayes predictive density under prior \(h(\lambda)\mu(d\lambda)\) is

\[
q_h(y\mid x)=q_J(y\mid x)\frac{A_k^h(x+y)}{A_\alpha^h(x)}.
\]

Use the proper priors

\[
h_n(\lambda)=\exp\{-|\log \lambda|/n\},\qquad 
\nu_n(d\lambda)=h_n(\lambda)\frac{d\lambda}{\lambda}.
\]

They are finite, since \(\int h_n\,d\lambda/\lambda=2n\), and \(h_n(\lambda)\to 1\) pointwise.

Let \(q_n=q_{h_n}\). The unnormalised Bayes risk gap is

\[
\Delta_n
=
B_{\nu_n}(q_J)-B_{\nu_n}(q_n)
=
\int m_J(x)A_\alpha^{h_n}(x)
E_{q_J(\cdot\mid x)}
\left[
R_n\log R_n
\right]dx,
\]

where

\[
R_n=\frac{A_k^{h_n}(x+Y)}{A_\alpha^{h_n}(x)}.
\]

Under \(q_J(\cdot\mid x)\),

\[
V=\frac{x}{x+Y}\sim \operatorname{Beta}(\alpha,\gamma),
\]

independently of \(x\). Also \(E_{q_J}(R_n\mid x)=1\).

Because \(h_n\) is log-Lipschitz,

\[
\frac{h_n(a)}{h_n(b)}
\le
\exp\left(\frac{|\log a-\log b|}{n}\right).
\]

Writing \(G_r\sim \operatorname{Ga}(r,1)\),

\[
A_r^{h_n}(z)=E\,h_n(G_r/z).
\]

Using the log-Lipschitz bound with \(z=x\) and \(z=x/V\), and using the gamma moment bounds

\[
E(G_\alpha^{-1})<\infty,\qquad E(G_k^{-1})<\infty,
\]

which hold when \(\alpha>1\), one obtains constants \(C_0,C_1<\infty\), depending only on \(\alpha,T\), such that for all large \(n\),

\[
|\log R_n|
\le
\frac{C_0}{n}(1+|\log V|).
\]

Since \(\alpha>1\),

\[
E(V^{-1})<\infty,
\qquad
V\sim \operatorname{Beta}(\alpha,\gamma).
\]

Using \(E(R_n\mid x)=1\) and the elementary inequality

\[
e^u u-e^u+1 \le C u^2 e^{|u|},
\]

the previous bound gives

\[
E_{q_J(\cdot\mid x)}[R_n\log R_n]
\le
\frac{C_1}{n^2},
\]

uniformly in \(x\). Therefore

\[
\Delta_n
\le
\frac{C_1}{n^2}
\int m_J(x)A_\alpha^{h_n}(x)\,dx
=
\frac{C_1}{n^2}\int h_n(\lambda)\frac{d\lambda}{\lambda}
=
\frac{2C_1}{n}
\to 0.
\]

Now apply the predictive-KL Blyth criterion. If some predictive density \(q\) dominated \(q_J\), with strict improvement at some \(\lambda_0\), then the KL risk improvement

\[
D(\lambda)=R(\lambda,q_J)-R(\lambda,q)
\]

would be nonnegative everywhere and positive on a nontrivial neighborhood of \(\lambda_0\). Hence, for all large \(n\),

\[
\int h_n(\lambda)D(\lambda)\frac{d\lambda}{\lambda}
\]

would be bounded below by a positive constant. But since \(q_n\) is Bayes under \(\nu_n\),

\[
\int h_nD\,d\mu
=
B_{\nu_n}(q_J)-B_{\nu_n}(q)
\le
B_{\nu_n}(q_J)-B_{\nu_n}(q_n)
=
\Delta_n
\to 0,
\]

a contradiction. Thus no predictive density strictly dominates \(q_J\). Therefore \(q_J\) is admissible for \(\alpha>1\).

## 3 YAML Failure Output

```yaml
failure: false
missing_input: []
blocked_on_s4: false
```

## 4 Local Source Ledger

- Used only the target theorem’s model and notation.
- Used standard gamma, beta, Bayes predictive, KL risk, and Blyth admissibility facts.
- Used no prior task history, files, tools, computation, answer keys, or web sources.

## 5 Interface Notes For S6

S6 may use this as the complete admissibility half for \(\alpha>1\).

For the full iff theorem, S6 must separately import S4’s proof of the stated perturbation/inadmissibility lemma for \(0<\alpha\le 1\). If S4 does not prove that lemma, S6 should not claim the full iff theorem; it should state that only the \(\alpha>1\) admissibility direction has been established.

## 6 Web-Source Confirmation

No web sources were used.