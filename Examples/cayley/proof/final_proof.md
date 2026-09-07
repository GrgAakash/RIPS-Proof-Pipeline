We prove the theorem by counting functions. Let
$$
\mathcal F_n=\{f:[n]\to[n]\}
$$
and let
$$
A_n=\{f\in\mathcal F_n: G_f\text{ has a unique cyclic vertex}\}.
$$
1. The sample-space count and probability reduction.
The map
$$
f\longmapsto (f(1),f(2),\ldots,f(n))
$$
is a bijection from $\mathcal F_n$ to the set of $n$-tuples in $[n]^n$: the values $f(1),\ldots,f(n)$ determine $f$, and every $n$-tuple in $[n]^n$ determines such a function. Since each of the $n$ coordinates has $n$ choices,
$$
|\mathcal F_n|=n^n.
$$
By the supplied uniform finite probability convention,
$$
\Pr(A_n)=\frac{|A_n|}{|\mathcal F_n|}=\frac{|A_n|}{n^n}.
$$
It remains to prove that $|A_n|=n^{n-1}$.

2. Basic orbit structure.
For $f:[n]\to[n]$, define $f^0(x)=x$ and $f^{k+1}(x)=f(f^k(x))$. For any fixed $x\in[n]$, the $n+1$ elements
$$
f^0(x),f^1(x),\ldots,f^n(x)
$$
lie in the $n$-element set $[n]$, so two are equal. Choose $b>0$ minimal such that $f^a(x)=f^b(x)$ for some $a<b$. Then
$$
f^a(x),f^{a+1}(x),\ldots,f^{b-1}(x)
$$
are pairwise distinct, and the directed edges of $G_f$ carry each listed vertex to the next one, with $f^{b-1}(x)$ mapping back to $f^a(x)$. Thus every forward orbit eventually enters a directed cycle.

If $G_f$ has a unique cyclic vertex $r$, then the cycle containing $r$ cannot contain any vertex distinct from $r$. Hence that cycle is the one-vertex loop at $r$, so $f(r)=r$. Also, the eventual cycle reached by any $x\in[n]$ consists of cyclic vertices, so under the same uniqueness hypothesis it must be the loop at $r$. Therefore every vertex reaches $r$ after finitely many iterations of $f$.

3. [KEY STEP] Fixed-root enumeration.
Fix $r\in[n]$, and let
$$
\mathcal A_{n,r}=\{f:[n]\to[n]\colon r\text{ is the unique cyclic vertex of }G_f\}.
$$
We prove that $|\mathcal A_{n,r}|=n^{n-2}$ for $n\ge2$, and that $|\mathcal A_{1,1}|=1$.

If $n=1$, then $[1]=\{1\}$, $r=1$, and the only function $[1]\to[1]$ satisfies $f(1)=1$. Its graph has the single loop at $1$, so $|\mathcal A_{1,1}|=1$.

Assume now that $n\ge2$. We construct a bijection
$$
\Phi:\mathcal A_{n,r}\to [n]^{n-2}.
$$
For a subset $R\subseteq[n]$ containing $r$, call $a\in R\setminus\{r\}$ an $R$-leaf if no vertex $y\in R\setminus\{a\}$ has $f(y)=a$.

Given $f\in\mathcal A_{n,r}$, start with $R_1=[n]$. At step $k=1,\ldots,n-2$, choose $a_k$ to be the least $R_k$-leaf in $R_k\setminus\{r\}$, set
$$
w_k=f(a_k),
$$
and put $R_{k+1}=R_k\setminus\{a_k\}$. We claim this is well-defined. Suppose at the beginning of a step that $r\in R_k$, $f(R_k)\subseteq R_k$, and every element of $R_k$ reaches $r$. These properties hold initially by Step 2. If no $R_k$-leaf existed in $R_k\setminus\{r\}$, then for every $u\in R_k\setminus\{r\}$ there would be a vertex $p(u)\in R_k\setminus\{u\}$ with $f(p(u))=u$. Since $f(r)=r$, this $p(u)$ also lies in $R_k\setminus\{r\}$. Iterating $p$ inside the finite set $R_k\setminus\{r\}$ would eventually repeat, producing a directed cycle for $f$ entirely outside $r$, a contradiction because every element of $R_k$ reaches the loop at $r$. Thus a non-root $R_k$-leaf exists, and the least one exists by finiteness.

For the chosen $a_k$, we have $f(a_k)\ne a_k$, since otherwise $a_k\ne r$ would be cyclic. Because $a_k$ is an $R_k$-leaf, no vertex of $R_k$ maps to $a_k$. Therefore deleting $a_k$ preserves $f(R_{k+1})\subseteq R_{k+1}$. The remaining vertices still reach $r$: a path from a remaining vertex to $r$ cannot pass through $a_k$, since that would require some remaining vertex to map to $a_k$. This proves the induction and hence the encoding is defined through step $n-2$. After these removals, $R_{n-1}=\{r,b\}$ for one non-root vertex $b$. Since $f(R_{n-1})\subseteq R_{n-1}$, $f(r)=r$, and $b$ reaches $r$, we have $f(b)=r$. The encoded word is
$$
\Phi(f)=(w_1,\ldots,w_{n-2})\in[n]^{n-2}.
$$
We now define an inverse decoding map. Given a word
$$
w=(w_1,\ldots,w_{n-2})\in[n]^{n-2},
$$
start with $R_1=[n]$. For $k=1,\ldots,n-2$, choose $a_k$ to be the least element of $R_k\setminus\{r\}$ that does not occur among the suffix letters
$$
w_k,w_{k+1},\ldots,w_{n-2}.
$$
Such an element exists because $R_k\setminus\{r\}$ has $n-k$ elements, while this suffix has length $n-k-1$. Define $f(a_k)=w_k$ and put $R_{k+1}=R_k\setminus\{a_k\}$. This assignment is legitimate: $w_k\ne a_k$ because $a_k$ is absent from the suffix containing $w_k$; and $w_k$ has not been removed earlier, for if $w_k=a_j$ with $j<k$, then $a_j$ would have appeared in the suffix $w_j,\ldots,w_{n-2}$, contradicting the choice of $a_j$. Hence $w_k\in R_k\setminus\{a_k\}$.

After the $n-2$ steps, the remaining set is $\{r,b\}$ for one non-root vertex $b$. Define
$$
f(b)=r,\qquad f(r)=r.
$$
This gives a function $f:[n]\to[n]$. Assign index $k$ to $a_k$, index $n-1$ to $b$, and index $n$ to $r$. For every $v\ne r$, the vertex $f(v)$ has strictly larger index than $v$. Therefore repeated application of $f$ from any non-root vertex strictly increases this index until it reaches $r$, while $r$ is fixed. Thus the only directed cycle is the loop at $r$, so the decoded function belongs to $\mathcal A_{n,r}$. Call this decoding map $\Psi:[n]^{n-2}\to\mathcal A_{n,r}$.

It remains to show that $\Phi$ and $\Psi$ are inverse maps. First let $f\in\mathcal A_{n,r}$, let $\Phi(f)=w$, and use the remaining sets $R_k$ from the encoding. At any step $k$, for $y\in R_k\setminus\{r\}$,
$$
y\text{ is an }R_k\text{-leaf}
\quad\Longleftrightarrow\quad
y\text{ does not occur among }w_k,\ldots,w_{n-2}.
$$
If $y=w_j=f(a_j)$ for some $j\ge k$, then the still-present vertex $a_j\ne y$ maps to $y$, so $y$ is not an $R_k$-leaf. Conversely, if $y$ is not an $R_k$-leaf, choose $z\in R_k\setminus\{y\}$ with $f(z)=y$. Since $y\ne r$, this $z$ cannot be $r$; and from the terminal observation above it cannot be the final non-root vertex $b$, because $f(b)=r$. Thus $z=a_j$ for some $j\ge k$, and $w_j=f(a_j)=y$. The encoding and decoding algorithms therefore choose the same least vertex at each step, assign the same value there, and remove the same vertex. Induction on $k$ gives $\Psi(\Phi(f))=f$, including the final assignments $f(b)=r$ and $f(r)=r$.

Conversely, let $w\in[n]^{n-2}$, let $\Psi(w)=f$, and let $a_1,\ldots,a_{n-2}$ be the decoded vertices. At step $k$, the vertex $a_k$ is an $R_k$-leaf for the decoded function: it does not occur in the suffix $w_k,\ldots,w_{n-2}$, so no later removed vertex maps to it, and the final vertices $b$ and $r$ both map to $r$. If $y\in R_k\setminus\{r\}$ and $y<a_k$, then the choice of $a_k$ forces $y$ to occur in the suffix $w_k,\ldots,w_{n-2}$, so some still-present vertex maps to $y$. Hence no smaller non-root remaining vertex is an $R_k$-leaf. The encoding of $f$ therefore removes exactly $a_k$ at step $k$ and records $f(a_k)=w_k$. Hence $\Phi(\Psi(w))=w$.

Thus $\Phi$ is a bijection from $\mathcal A_{n,r}$ to $[n]^{n-2}$. There are $n^{n-2}$ words of length $n-2$ over the $n$-element alphabet $[n]$, so
$$
|\mathcal A_{n,r}|=n^{n-2}\qquad(n\ge2).
$$
4. Assembly over the possible cyclic vertices.
For each $r\in[n]$, let
$$
A_{n,r}=\{f\in\mathcal F_n: r\text{ is the unique cyclic vertex of }G_f\}.
$$
Then
$$
A_n=\bigsqcup_{r\in[n]} A_{n,r}.
$$
Indeed, every function in $A_n$ has a unique cyclic vertex, and that vertex is some $r\in[n]$, so the function lies in $A_{n,r}$. Conversely, membership in some $A_{n,r}$ means precisely that $G_f$ has a unique cyclic vertex. The union is disjoint because one function cannot have two different unique cyclic vertices.

If $n=1$, then $A_n=A_{1,1}$, so $|A_n|=1=1^{1-1}=n^{n-1}$. If $n\ge2$, then the fixed-root count from Step 3 gives $|A_{n,r}|=n^{n-2}$ for every $r\in[n]$. Since there are $n$ possible roots and the union is disjoint,
$$
|A_n|=\sum_{r\in[n]} |A_{n,r}|
=\sum_{r\in[n]} n^{n-2}
=n\cdot n^{n-2}
=n^{n-1}.
$$
Thus $|A_n|=n^{n-1}$ for every positive integer $n$.

5. Final probability computation.
Substituting the favorable count into the uniform finite probability formula gives
$$
\Pr(A_n)=\frac{|A_n|}{n^n}
=\frac{n^{n-1}}{n^n}
=\frac{n^{n-1}}{n\cdot n^{n-1}}
=\frac1n.
$$
Therefore the probability that a uniform random function $f:[n]\to[n]$ has a unique cyclic vertex is $1/n$, as claimed.
