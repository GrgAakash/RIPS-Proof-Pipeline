Ran the fresh no-history solver-only S0-S6 pipeline for 3 rounds using the specified S0-S6 prompt packet. I did not run any verifier pipeline, web search, code execution, API-key tooling, or memory-dependent step.

Outcome: the solver pipeline did **not** produce an unconditional proof.

The repeated blocking point was the same in all rounds: the proof needs a nontrivial denominator obstruction of the following form:

```text
If alpha-filling along the boundary slopes contains the capped sphere meeting
each alpha-filling core exactly once, meridian filling gives S^3, and all
Delta(alpha_i, mu_i) >= 2, then contradiction.
```

S1/S2 consistently proved the elementary setup:

```text
Delta(alpha_i, mu_i) = |p_i|,
all-meridian filling recovers S^3,
alpha-filling caps P to a sphere,
each alpha-filling core intersects that sphere exactly once.
```

But S3/S4 could not prove the essentiality/denominator obstruction from the standalone theorem plus standard background. S4 concluded that an external multi-component reducible Dehn surgery denominator theorem is required, or else the standalone target may need additional hypotheses.

So the final solver artifact is only conditional:

```text
If the missing C5 denominator obstruction and essentiality of the capped sphere
are supplied, then assuming all p_i notin {0,1} gives all Delta(alpha_i,mu_i)>=2,
contradicting C5; hence some p_i is in {0,1}.
```

I did not silently convert that conditional argument into a proof.
