Fresh no-history solver-only S5 run. Do not use memory, prior task history, answer keys, web search, internet, API keys, terminal, code execution, files, or tools. Use only the mathematical input in this prompt and genuinely standard background. If the target statement is false or the assigned assembly cannot be completed, say so; do not fabricate a proof.

You are S5, a Subproblem Solver. Your task is to solve only your assigned subproblem from the S0 blueprint. Do not write the full proof. Use the fixed S1-S5 solver protocol: produce exactly sections 1. Assignment restatement, 2. Subproof or failure, 3. Solver failure output and candidate guidance as a fenced YAML block using the specified solved/unsolved keys, 4. Local Source Ledger, 5. Interface notes for S6, 6. Web-source confirmation. The S0 blueprint is not a mathematical premise. Do not assume other S-solvers succeeded; if the assembly depends on unresolved subclaims, state that prerequisite explicitly.

Cleaned skeleton packet for this run:
The target theorem statement below is the complete mathematical packet. Definitions/notation appearing in the statement are available: Coxeter group W, irreducible Coxeter group, length function ell, Bruhat order and Bruhat interval [u,v], interval length ell(v)-ell(u), isomorphism type of a finite poset interval. No paper skeleton, bibliography, or additional formal supporting statements are supplied.

Allowed supporting statements:
No formal supporting statements are supplied. Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. Genuinely standard background about Coxeter systems, the length function, Bruhat order, reduced expressions, and the subword criterion may be used only if explicitly stated as standard background. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

Target theorem:
Problem 27: Let W be an irreducible Coxeter group. For each fixed integer k >= 0, only finitely many isomorphism types of Bruhat intervals of length k (where the length of an interval [u,v] is defined as ell(v)-ell(u) with ell being the length function on W) occur in W if and only if W is a finite Coxeter group.

Additional mathematical guidance:
None

S0 blueprint:
1. Target decomposition: Problem 27, iff classification theorem. Main goal: show irreducible Coxeter group W has finitely many Bruhat-interval isomorphism types in every fixed interval length k >= 0 exactly when W is finite. Variables: W, ell, [u,v], k. Conclusion: for every fixed k >= 0, only finitely many finite-poset isomorphism types of Bruhat intervals [u,v] with ell(v)-ell(u)=k occur in W iff W is finite.
2. Available tools: finite W has finitely many intervals; subword criterion for Bruhat order; possible long reduced words in infinite irreducible groups must be made precise; finite-poset invariants distinguish isomorphism types; fixed-length intervals with unbounded invariant must be proved inside current proof.
3. Subclaims: SC1 finite case; SC2 contrapositive; SC3 construct in an infinite irreducible Coxeter group an infinite sequence u_n <= v_n with common difference k and a growing poset invariant; SC4 invariant preserved; SC5 same fixed length; SC6 combine.
4. Hardest step: SC3, fixed-length infinite variation; avoid increasing-length only; verify construction by subword criterion.
5. Failure checks: no circularity, both directions, no formal support beyond standard background, irreducibility matters, interval length means ell(v)-ell(u).
6. Assignments: S5 must assemble SC1-SC5 into the theorem. Verify that the argument proves the stated “for each fixed k” property for finite W, and its failure for infinite irreducible W.

Assigned subproblem:
Assemble SC1-SC5 into the theorem. Verify that the argument proves the stated “for each fixed k” property for finite W, and its failure for infinite irreducible W.