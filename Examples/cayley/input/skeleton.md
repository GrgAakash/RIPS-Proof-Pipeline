# 0. Macro Definitions

```tex
\newcommand{\sh}[2]{\mathrm{sh}_{#1}(#2)}
\newcommand{\cyc}[2]{\mathrm{cyc}_{#1}(#2)}
\newcommand{\Ccyc}[2]{\mathrm{Cyc}_{#1}(#2)}
\newcommand{\cF}{\mathcal{F}}
\renewcommand{\Pr}{\mathbb{P}}
\newcommand{\ba}{{\mathbf{a}}}
\newcommand{\bb}{{\mathbf{b}}}
\newcommand{\be}{{\mathbf{e}}}
\newcommand{\hE}{{\hat{E}}}
\newcommand{\hF}{{\hat{F}}}
\newcommand{\tO}{{\widetilde{O}}}
```

# 1. Notation and Conventions

Throughout, $n$ is a positive integer.

Elementary notation convention: $[n]$ denotes the finite set $\{1,2,\ldots,n\}$.

Elementary finite probability convention: a uniform random function $f:[n]\to[n]$ means a function chosen uniformly from the finite set of all functions from $[n]$ to $[n]$.

# 2. Standing Assumptions

$n$ is a positive integer.

# 3. Known External Results

None.

# 4. Definitions

Let $f:[n]\to[n]$, and let $G_f$ be its associated directed graph, with vertex set $[n]$ and directed edges $(i,f(i))$ for $i \in [n]$. A vertex is *cyclic* if it belongs to a cycle of $G_f$.

# 5. Available Results

No formal paper statement is granted as support under this definitions-only policy.

EXCLUDED under the run's definitions-only support policy:

The probability that a uniform random function $f:[n]\to [n]$ has a unique cyclic vertex is~$\frac{1}{n}$.

EXCLUDED under the run's definitions-only support policy:

Functions $f$ having a unique cyclic vertex are in bijection with rooted trees on $[n]$ (the unique cyclic vertex is the root, and edges are oriented towards the root).

EXCLUDED under the run's definitions-only support policy:

Cayley's formula asserts that there are $n^{n-2}$ trees on the vertex set $[n]$, or equivalently there are $n^{n-1}$ rooted trees.

EXCLUDED under the run's definitions-only support policy:

Let $H_n$ denote the height of a uniform random vertex in a uniform random rooted tree with $n$ vertices. Then $1+H_n$ has the same law as the time of first repetition in a i.i.d. sequence of uniform variables on~$[n]$ (time of first collision in the coupon collector process).
