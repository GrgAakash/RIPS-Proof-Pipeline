Fresh no-history solver-only branch pipeline, branch depth 1. You are S0, the Blueprint Solver, for the branch lemma only. No memory, no prior task history, no web, no external sources, no code/tools/files/API keys. Use only the supplied cleaned packet, allowed support, guidance, and genuinely standard background. Do not write the final proof.

Cleaned packet for branch:
- A weakly o-minimal structure is a linearly ordered structure in which every definable subset of the domain is a finite union of convex sets.
- M=(M,+,·,≤,...) is a weakly o-minimal expansion of an ordered field.
- J⊆M is a nonempty open interval.
- f:J->M is definable, continuous, and strictly monotone.
- Differentiability is the usual ordered-field derivative.

Allowed support:
Definitions, notation, and assumptions needed to parse the branch target. No external theorem statements. No theorem equivalent to the branch target may be cited without proof.

Additional mathematical guidance:
1. Work with nonempty open intervals throughout; the empty-interval convention is not being used.

Branch target theorem:
Let M be a weakly o-minimal expansion of an ordered field. Let J be a nonempty open interval in M, and let f:J->M be definable, continuous, and strictly monotone. Then there exists a nonempty open interval J1⊆J such that for every x∈J1, the limit
lim_{h->0} (f(x+h)-f(x))/h
exists as an element of M, with h constrained by x+h∈J.

Parent note: This branch lemma is intended to unblock the strictly monotone branch of the main theorem. Do not prove or cite the main theorem.

Produce exactly these S0 sections:
1. Target decomposition
2. Available tools
3. Subclaim support graph with 3-8 subclaims assigned to S1-S5
4. Hardest step prediction
5. Failure-mode checks
6. Subproblem assignment table S1-S5
7. Web-source confirmation