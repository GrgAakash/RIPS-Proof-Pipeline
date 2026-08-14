## 1. Assignment Restatement

Prove the target theorem for all `1 < p <= 2`: for every `n`-vertex graph `G` with at least one edge,
\[
\lambda(G)\le (C_p+o(1))\,d_p(G)\,n^{\max\{1/2,p-1\}},
\]
using only the packet definitions and the internally verified auxiliary result E001.

## 2. Subproof or Failure

<!-- BEGIN_FINAL_PROOF -->
Let \(1<p\le 2\), and let \(G\) be an \(n\)-vertex graph with at least one edge.

By the internally verified auxiliary result E001, applied directly to \(G\) with \(N=n\), there is an absolute constant \(C_0>0\) such that
\[
\lambda(G)\le C_0\sqrt n\, d_{3/2}(G).
\]

It remains to compare \(d_{3/2}(G)\) with \(d_p(G)\). For every nonempty subset \(S\subseteq V(G)\), by the definition of \(d_p(G)\),
\[
\frac{e(G[S])}{|S|^p}\le d_p(G).
\]
Therefore
\[
\frac{e(G[S])}{|S|^{3/2}}
=
\frac{e(G[S])}{|S|^p}\,|S|^{p-3/2}
\le
d_p(G)|S|^{p-3/2}.
\]

If \(p\le 3/2\), then \(p-3/2\le 0\), and since \(|S|\ge 1\),
\[
|S|^{p-3/2}\le 1.
\]
Thus
\[
\frac{e(G[S])}{|S|^{3/2}}\le d_p(G).
\]

If \(p\ge 3/2\), then \(p-3/2\ge 0\), and since \(|S|\le n\),
\[
|S|^{p-3/2}\le n^{p-3/2}.
\]
Thus
\[
\frac{e(G[S])}{|S|^{3/2}}\le d_p(G)n^{p-3/2}.
\]

Taking the maximum over all nonempty \(S\subseteq V(G)\), we obtain
\[
d_{3/2}(G)\le d_p(G)n^{\max(0,p-3/2)}.
\]
Combining this with E001 gives
\[
\lambda(G)
\le
C_0\sqrt n\, d_p(G)n^{\max(0,p-3/2)}
=
C_0d_p(G)n^{1/2+\max(0,p-3/2)}.
\]

Finally,
\[
1/2+\max(0,p-3/2)=\max(1/2,p-1),
\]
because if \(p\le 3/2\) the left side is \(1/2\), while if \(p\ge 3/2\) it is \(p-1\). Hence
\[
\lambda(G)\le C_0d_p(G)n^{\max\{1/2,p-1\}}.
\]

Set \(C_p=C_0\). Since this exact bound holds for every such \(n\)-vertex graph \(G\), it implies
\[
\lambda(G)\le (C_p+o(1))d_p(G)n^{\max\{1/2,p-1\}}
\]
as \(n\to\infty\). This proves the theorem.
<!-- END_FINAL_PROOF -->

## 3. Solver Failure Output and Candidate Guidance YAML

```yaml
failure_output_type: solved
main_solver_proof_key: true
status: complete
used_guidance:
  - E001
```

## 4. Local Source Ledger and Critical Claim Statuses/Addendum

Local sources used: supplied theorem packet only.

Critical claim statuses:

- CC001: Proved by direct application of E001 to \(G\) with \(N=n\).
- CC002: Proved from the definitions by splitting \(p\le 3/2\) and \(p\ge 3/2\).
- CC003: Proved by the same two-case split.

No additional lemmas beyond E001 and elementary exponent comparison were used.

## 5. Interface Notes for Manager Acceptance

The proof uses E001 exactly as stated and only at the load-bearing spectral-radius step. The remainder is a direct comparison of \(d_{3/2}(G)\) and \(d_p(G)\) from definitions, followed by the exponent identity needed for the target asymptotic form.

## 6. Web-Source Confirmation

No web search, internet access, API keys, Python, prior outputs, answer keys, or external files were used.