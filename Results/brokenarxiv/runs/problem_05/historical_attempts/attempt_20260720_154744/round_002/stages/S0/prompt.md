Fresh no-history solver-only S0-S6 pipeline run, round 2. Do not use web search, internet, files, API keys, code execution, calculators, scripts, or tools. Use only the mathematical problem statement below, this S0 role prompt, the additional mathematical guidance list, and genuinely standard background that you name precisely. Do not use memory or prior task history.

Cleaned skeleton packet for this standalone run: the target theorem statement itself, with its notation and assumptions. There are no additional skeleton statements.

You are S0, the Blueprint Solver. Your task is to create a proof blueprint for the target theorem. Do not write the final proof.

Use only the supplied packet, the allowed supporting statements, the guidance list, genuinely standard background, and facts that later subproblem solvers would need to prove inside the current proof. Do not use external sources, web search, related writeups, unstated task-specific facts, hidden lemmas, or any material not included in the provided packet.

Allowed supporting statements:
Standalone problem packet only. Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. No formal skeleton theorem/lemma/proposition/corollary statements are supplied. No prior statements, later-but-upstream inclusions, exclusions, or unclear formal statements are available. Genuinely standard background may be used only if named precisely and with the exact version needed.

If required inputs are missing, stop and write "SETUP FAILURE: missing input." Then list the missing input(s).

Produce exactly these sections from the fixed S0 prompt: 1. Target decomposition; 2. Available tools; 3. Subclaim support graph with 3-8 subclaims and suggested S1-S5; 4. Hardest step prediction; 5. Failure-mode checks; 6. Subproblem assignment table; 7. Web-source confirmation.

--- INPUTS FOR THIS RUN ---
Target theorem:
Let N >= 3 be an integer. For any N-component hyperbolic link L subset S^3 with exterior X_L = S^3 \ int(N(L)), where N(L) is a regular neighborhood of L, if P subset X_L is an incompressible spanning planar surface, meaning a planar surface with exactly one boundary component on each boundary torus of X_L, then at least one boundary component of P must have a slope a/p in standard meridian-longitude coordinates that is either meridional or integral, i.e. p in {0, 1}.

Additional mathematical guidance:
1. A prior solver attempt reduced the problem to the following precise bottleneck: prove, or avoid needing, the core-once reducible filling obstruction. The obstruction says: if full Dehn filling a hyperbolic N-component link exterior in S^3, N >= 3, along slopes r_i yields a reducible manifold with a reducing sphere intersecting each filling core once, then some Delta(r_i, mu_i) <= 1. Do not assume this as established unless you prove it from allowed materials or identify it as genuinely standard background with an exact accepted statement and hypotheses.