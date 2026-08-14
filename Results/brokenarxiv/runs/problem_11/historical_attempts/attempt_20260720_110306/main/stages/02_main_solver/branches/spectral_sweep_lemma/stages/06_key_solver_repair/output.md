**1. Assignment Restatement**

Branch SS1, Main Solver, `work_scope: global_solution`. Target: prove that for some absolute constant `C>0`, every `N`-vertex graph `H` with at least one edge satisfies
\[
\lambda(H)\le C\sqrt N\, d_{3/2}(H),
\qquad
d_{3/2}(H)=\max_{\emptyset\ne S\subseteq V(H)}\frac{e(H[S])}{|S|^{3/2}}.
\]

No web, Python, prior outputs, memory, answer keys, API keys, or external files used.

**2. Subproof**

Solved.

[BEGIN FINAL PROOF BODY: SS1-proof-v1]

Let
\[
D=d_{3/2}(H).
\]
Since `H` has an edge, taking its two endpoints gives
\[
D\ge \frac1{2^{3/2}}.
\]

Let `A` be the adjacency matrix. Since `A` is nonnegative, the Rayleigh quotient may be tested on nonnegative vectors: for any real `x`,
\[
x^TAx\le |x|^TA|x|.
\]
So fix `y\ge 0`. For `t\ge 0`, define
\[
S_t=\{v:y_v>t\},\qquad n(t)=|S_t|.
\]
For `s,t\ge 0`, let `M(s,t)` be the number of ordered adjacent pairs `(u,v)` with `u\in S_s` and `v\in S_t`. Layer cake gives
\[
y^TAy=\int_0^\infty\int_0^\infty M(s,t)\,ds\,dt
=2\int_0^\infty\int_0^t M(s,t)\,ds\,dt.
\]

We need a nested-set edge bound. If `T\subseteq S`, `|T|=b`, `|S|=a`, then the number of ordered edge incidences from `S` to `T` is at most
\[
6D\,a\sqrt b.
\]
Indeed, if `a\le 2b`, this is at most
\[
2e(H[S])\le 2Da^{3/2}\le 2\sqrt2\,Da\sqrt b.
\]
If `a>2b`, choose uniformly a `b`-set `R\subseteq S\setminus T`. Since every `T\cup R` has size `2b`,
\[
e(H[T\cup R])\le D(2b)^{3/2}.
\]
Averaging over `R` gives
\[
e(T)+\frac{b}{a-b}e(T,S\setminus T)\le D(2b)^{3/2},
\]
so
\[
e(T,S\setminus T)\le 2^{3/2}Da\sqrt b.
\]
Together with `e(T)\le Db^{3/2}`, the ordered incidence count is at most `6Da sqrt b`.

Applying this with `T=S_t\subseteq S_s=S` for `s\le t`,
\[
M(s,t)\le 6D\,n(s)\sqrt{n(t)}.
\]
Hence
\[
y^TAy\le 12D\int_0^\infty \sqrt{n(t)}
\left(\int_0^t n(s)\,ds\right)dt.
\]

We use the following Hardy-type threshold lemma.

**Lemma.** If `n(t)` is a decreasing threshold-count function with `0\le n(t)\le N`, then
\[
\int_0^\infty \sqrt{n(t)}
\left(\int_0^t n(s)\,ds\right)dt
\le 9\sqrt N\int_0^\infty t\,n(t)\,dt.
\]

Proof of lemma. Put `f=n/N`, so `0\le f\le 1`, and write `g=\sqrt f`. Let
\[
L=\int_0^\infty t g(t)^2\,dt.
\]
The desired estimate is equivalent to
\[
\int_0^\infty g(t)\int_0^t g(s)^2\,ds\,dt\le 9L.
\]
Let `tau(a)=|\{t:g(t)>a\}|`, `0<a\le 1`. Then
\[
L=\int_0^1 a\,\tau(a)^2\,da.
\]
Expanding both `g(s)^2` and `g(t)` by layer cake gives two regions in the `(a,b)` level variables. The region `a<b` contributes at most
\[
\frac12\int_0^1 a^2\tau(a)^2\,da\le \frac12L.
\]
The region `b<a` contributes
\[
2\int_0^1 a\tau(a)\left(\int_0^a\tau(b)\,db\right)da.
\]
The weighted Hardy inequality for decreasing functions,
\[
\int_0^1 a h(a)\left(\int_0^a h(b)\,db\right)da
\le 4\int_0^1 a h(a)^2\,da,
\]
applied to `h=\tau`, bounds this by `8L`. This proves the lemma.

Finally,
\[
\int_0^\infty t\,n(t)\,dt=\frac12\sum_v y_v^2=\frac12\|y\|_2^2.
\]
Thus
\[
y^TAy\le 12D\cdot 9\sqrt N\cdot \frac12\|y\|_2^2
=54D\sqrt N\,\|y\|_2^2.
\]
Taking the supremum over nonzero `y\ge 0`,
\[
\lambda(H)\le 54D\sqrt N.
\]
So the target lemma holds with absolute constant `C=54`.

[END FINAL PROOF BODY]

**3. Solver Failure / Guidance YAML**

```yaml
main_solver_proof_key: SS1-proof-v1
solver: SS1
work_scope: global_solution
target_status: solved
solver_failure_output:
  failed: false
  obstruction: null
candidate_guidance:
  - id: SS2-defender-check
    autonomy_safe: true
    guidance: "Check the nested-set sampling bound and the weighted Hardy threshold lemma. The prior false arbitrary-D integral estimate is not used."
critical_claims:
  CC001: proved
  CC002: repaired_and_proved
  CC003: replaced_by_hardy_closure
```

**4. Local Source Ledger / Claim Status**

Local sources used: only the prompt text and Manager-approved support/admission.

Claim statuses:
- `CC001`: proved by nonnegative Rayleigh reduction and layer cake.
- `CC002`: repaired with the nested-set random sampling bound.
- `CC003`: repaired by replacing the false arbitrary-`D` estimate with a Hardy-type threshold closure.

Addendum: SS3’s warning is respected; the invalid displayed analytic inequality is not used.

**5. Interface Notes**

No files read or written. No Python. No API keys. No internet. Constants are not optimized.

**6. Web-Source Confirmation**

No web search or internet access was used.