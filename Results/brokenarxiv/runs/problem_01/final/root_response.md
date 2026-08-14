Ran the requested fresh solver-only S0-S6 pipeline, with no verifier pipeline and no web search. The solver pipeline did not prove the statement; final S6 concluded the statement is false as stated.

Core obstruction: because “a largest cluster” allows ties, failure requires a non-root cluster to become strictly larger than the root. For any fixed `p > 0`, condition on the first `K-1` edges being retained. This has probability `p^(K-1) > 0` and leaves the process at time `K` with one root cluster of size `K` and no challengers.

Starting from that state, S6 composed the bound
\[
P(p)\ge p^{K-1}Q_K(p),
\]
where \(Q_K(p)\) is the probability that no future challenger strictly overtakes the root. A singleton challenger born when the root has size \(m\) has strict-overtake probability at most \(2^{1-m}\). Summing over all future challenger births gives
\[
\mathbb P(B\ge1)
\le 2(1-p)\sum_{n\ge K}\mathbb E[2^{-R_n}]
\le 2(1-p)\sum_{n\ge K}2^{-K}\left(\frac Kn\right)^{pK/2}.
\]
For sufficiently large `K`, this is `< 1`, so \(Q_K(p)>0\). Hence \(P(p)>0\) for every \(p\in(0,1]\).

So no \(p_c\in(0,1)\) with \(P(p)=0\) below \(p_c\) can exist under the stated model and tie-allowed wording.