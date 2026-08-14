Fresh no-history solver-only S2 run. Do not use memory, prior task history, answer keys, web search, internet, API keys, terminal, code execution, files, or tools. Use only the mathematical input in this prompt and genuinely standard background. If the assigned claim is false or insufficient, say so; do not fabricate a proof.

Cleaned skeleton packet for this run:
The target theorem statement below is the complete mathematical packet. Definitions/notation appearing in the statement are available: Coxeter group W, irreducible Coxeter group, length function ell, Bruhat order and Bruhat interval [u,v], interval length ell(v)-ell(u), isomorphism type of a finite poset interval. No paper skeleton, bibliography, or additional formal supporting statements are supplied.

Use the fixed S1-S5 Subproblem Solver role requirements from Prompts.md: produce sections 1-6, solve only your assignment, include YAML failure output, local source ledger, interface notes, and web-source confirmation.

Target theorem:
Problem 27: Let W be an irreducible Coxeter group. For each fixed integer k >= 0, only finitely many isomorphism types of Bruhat intervals of length k (where the length of an interval [u,v] is defined as ell(v)-ell(u) with ell being the length function on W) occur in W if and only if W is a finite Coxeter group.

Allowed supporting statements:
No formal supporting statements are supplied. Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. Genuinely standard background about Coxeter systems, the length function, Bruhat order, reduced expressions, and the subword criterion may be used only if explicitly stated as standard background. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

Additional mathematical guidance:
None

S0 blueprint:
[Same S0 blueprint as supplied to S1. Key assignment for S2: Prove SC3. Starting only from standard Coxeter/Bruhat facts, construct in an arbitrary infinite irreducible Coxeter group an infinite family of comparable pairs u_n <= v_n whose Bruhat intervals have one fixed length and a growing finite-poset invariant. Hardest step: do not merely construct increasing-length intervals; fixed interval length is required.]

Assigned subproblem:
Prove SC3. Starting only from standard Coxeter/Bruhat facts, construct in an arbitrary infinite irreducible Coxeter group an infinite family of comparable pairs u_n <= v_n whose Bruhat intervals have one fixed length and a growing finite-poset invariant.