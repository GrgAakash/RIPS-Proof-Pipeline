**1 Assignment Restatement**

S1 proves that the derivative-existence locus

\[
D=\{x\in J:\lim_{h\to 0,\ x+h\in J}\frac{f(x+h)-f(x)}{h}\in M\}
\]

is definable, and supplies definable slope oscillation predicates for later branches.

**2 Subproof Or Failure**

Let \(\Gamma_f(u,v)\) be the definable graph of \(f\). Then \(J(u)\) is definable, for instance by \(\exists v\,\Gamma_f(u,v)\).

Define the slope relation

\[
\operatorname{Slope}(x,h,s)
\]

by

\[
h\neq 0\wedge J(x)\wedge J(x+h)\wedge
\exists y,z\bigl(\Gamma_f(x,y)\wedge \Gamma_f(x+h,z)\wedge sh=z-y\bigr).
\]

This is definable in the ordered-field language expanded by the given structure. Since \(h\neq 0\), \(s\) is uniquely the quotient

\[
s=\frac{f(x+h)-f(x)}{h}.
\]

Use \(|u|<r\) as shorthand for \(-r<u<r\).

Define

\[
\operatorname{Der}(x,\ell)
\]

by

\[
J(x)\wedge
\forall \varepsilon>0\ \exists \delta>0\ \forall h\,\forall s
\Bigl(
\operatorname{Slope}(x,h,s)\wedge |h|<\delta
\rightarrow |s-\ell|<\varepsilon
\Bigr).
\]

This is a first-order formula, hence definable. It is exactly the usual ordered-field \(\varepsilon\)-\(\delta\) definition of the derivative limit at \(x\), restricted to \(x+h\in J\). Therefore

\[
D(x):\Longleftrightarrow \exists \ell\,\operatorname{Der}(x,\ell)
\]

defines \(D\). Thus \(D\subseteq J\) is definable.

For oscillation, let \(\sigma,\tau\in\{+,-,\pm\}\), with side conditions

\[
\operatorname{Side}_+(h): h>0,\quad
\operatorname{Side}_-(h): h<0,\quad
\operatorname{Side}_{\pm}(h): h\neq 0.
\]

For \(a<b\), define the bad-slope oscillation predicate

\[
\operatorname{Osc}_{\sigma,\tau}(x,a,b)
\]

by

\[
J(x)\wedge a<b\wedge
\forall \delta>0\ \exists h,k,s,t
\Bigl(
\operatorname{Slope}(x,h,s)\wedge \operatorname{Slope}(x,k,t)
\wedge |h|<\delta\wedge |k|<\delta
\wedge \operatorname{Side}_\sigma(h)\wedge \operatorname{Side}_\tau(k)
\wedge s<a\wedge t>b
\Bigr).
\]

This says that arbitrarily close to \(x\), the difference quotients have values below \(a\) and above \(b\). It is definable uniformly in \((x,a,b)\). For fixed \(a<b\), each bad set

\[
B_{\sigma,\tau,a,b}:=\{x\in J:\operatorname{Osc}_{\sigma,\tau}(x,a,b)\}
\]

is unary definable.

Also useful are the unbounded-slope predicates:

\[
\operatorname{Unbdd}^{\uparrow}_\sigma(x):
J(x)\wedge
\forall R\,\forall\delta>0\ \exists h,s
\bigl(\operatorname{Slope}(x,h,s)\wedge |h|<\delta
\wedge \operatorname{Side}_\sigma(h)\wedge s>R\bigr),
\]

and

\[
\operatorname{Unbdd}^{\downarrow}_\sigma(x):
J(x)\wedge
\forall R\,\forall\delta>0\ \exists h,s
\bigl(\operatorname{Slope}(x,h,s)\wedge |h|<\delta
\wedge \operatorname{Side}_\sigma(h)\wedge s<R\bigr).
\]

Both are definable.

For later use with ordinary secant slopes, define

\[
\operatorname{Sec}(u,v,s):
J(u)\wedge J(v)\wedge u<v\wedge
\exists y,z\bigl(\Gamma_f(u,y)\wedge \Gamma_f(v,z)\wedge s(v-u)=z-y\bigr).
\]

Then the local secant oscillation predicate

\[
\operatorname{SecOsc}(x,a,b)
\]

given by

\[
J(x)\wedge a<b\wedge
\forall\delta>0\ \exists u<v,\ u'<v',\ s,t
\Bigl(
\operatorname{Sec}(u,v,s)\wedge \operatorname{Sec}(u',v',t)
\wedge |u-x|<\delta\wedge |v-x|<\delta
\wedge |u'-x|<\delta\wedge |v'-x|<\delta
\wedge s<a\wedge t>b
\Bigr)
\]

is also definable.

**3 YAML**

```yaml
failure_output_type: solved
output_type: branch_lemma
branch: S1
result: D and the point-slope, directional oscillation, unbounded-slope, and secant-oscillation predicates are definable.
uses_weak_o_minimality: false
parameters_allowed: parameters defining f and J, plus slope thresholds a and b
```

**4 Local Source Ledger**

Used only the supplied packet facts: \(M\) is an ordered-field expansion, \(f\) has definable graph, \(J\) is the definable domain/open interval, ordered-field algebra, and first-order closure under Boolean operations and quantifiers.

**5 Interface Notes For Branch S6**

S6 may treat \(D\), \(B_{\sigma,\tau,a,b}\), \(\operatorname{Unbdd}^{\uparrow/\downarrow}_\sigma\), and \(\operatorname{SecOsc}(\cdot,a,b)\) as unary definable sets for fixed parameters. No interval-emptiness, local regularity, or no-persistent-oscillation claim is proved here.

**6 Web-Source Confirmation**

No web sources, external tools, files, APIs, or prior task history were used.