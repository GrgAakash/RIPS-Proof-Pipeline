I ran the requested fresh no-history solver-only S0-S6 pipeline, with no web search, no verifier pipeline, and no code execution for solving.

The run did **not** produce a proof. S6 returned `FINAL PROOF NOT COMPLETED`.

Key result from the pipeline:

- `S2` proved the upper-bound lifting lemma: if `Q` is `F`-saturated, then `K_1 ∨ Q` is `K_1 ∨ F`-saturated.
- `S4` proved the universal deletion lemma: if `G` is `K_1 ∨ F`-saturated with a universal vertex `v`, then `G-v` is `F`-saturated.
- `S5` showed the target equality follows conditionally from those two lemmas plus a structural lemma saying every near-extremal `K_1 ∨ F`-saturated graph has a universal vertex.
- `S3` found that this structural lemma is false as stated: for arbitrarily large `n = pq + 1`, the graph `qK_p ∪ K_1` is `K_1 ∨ (K_{p-1}^- ∪ K_1)`-saturated and has no universal vertex.

S6’s composer conclusion was that the current solver artifacts cannot prove the requested equality, because the planned lower-bound route depends on that false universal-vertex lemma. No verifier pipeline was run, per your instruction.