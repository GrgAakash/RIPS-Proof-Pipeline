Completed the fresh solver-only S0-S6 run. No verifier pipeline was run. Round 1 isolated the missing uniform free-semigroup input; round 2 used one guidance item naming that standard theorem, and S6 composed the proof.

**Proof.** Let \(S\) be a finite generating set and write \(B_S(n)\) for the word ball. Property (T) implies \(G\) is finitely generated. Since \(G\) is acylindrically hyperbolic, it admits a non-elementary acylindrical action on a Gromov-hyperbolic space \(X\).

Use the standard uniform free-semigroup theorem for non-elementary acylindrical actions: for this fixed action \(G\curvearrowright X\), there is \(L\in\mathbb N\), depending only on the action and not on \(S\), such that for every finite generating set \(S\), \(B_S(L)\) contains two elements \(a,b\) generating a free semigroup.

For each \(n\ge 1\), the \(2^n\) positive words of length \(n\) in \(a,b\) are distinct. Since \(|a|_S,|b|_S\le L\), each such word has \(S\)-length at most \(nL\). Hence
\[
|B_S(nL)|\ge 2^n .
\]
Therefore
\[
\omega(G,S)\ge \limsup_{n\to\infty}|B_S(nL)|^{1/(nL)}
\ge \lim_{n\to\infty}(2^n)^{1/(nL)}
=2^{1/L}.
\]
The same \(L\) works for every finite generating set \(S\), so
\[
\inf_S \omega(G,S)\ge 2^{1/L}>1.
\]
Thus \(G\) has uniform exponential growth.