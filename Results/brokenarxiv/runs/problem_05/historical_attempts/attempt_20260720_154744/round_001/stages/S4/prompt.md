Fresh no-history solver-only S0-S6 pipeline run. Do not use web search, internet, files, API keys, code execution, calculators, scripts, or tools. Use only the mathematical problem statement below, the filled role prompt below, the supplied S0 blueprint text, your assigned subproblem, and genuinely standard background that you name precisely. Do not use memory or prior task history.

Cleaned skeleton packet for this standalone run: the target theorem statement itself, with its notation and assumptions. There are no additional skeleton statements.

You are S4, a Subproblem Solver. Your task is to solve only your assigned subproblem from the S0 blueprint. Do not write the full proof.

Use only the supplied packet, allowed supporting statements, guidance list, S0's current-round blueprint for assignment and planning, genuinely standard background, and facts you prove in your own subproof. The S0 blueprint is not a mathematical premise: do not cite it as proof of a mathematical fact. Do not use external sources, web search, related writeups, unstated task-specific facts, hidden lemmas, or any material not included in the provided packet.

Do not assume other S-solvers succeeded. If your assignment uses another subclaim, state that prerequisite explicitly.

Allowed supporting statements:
Standalone problem packet only. Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. No formal skeleton theorem/lemma/proposition/corollary statements are supplied. No prior statements, later-but-upstream inclusions, exclusions, or unclear formal statements are available. Genuinely standard background may be used only if named precisely and with the exact version needed.

Produce exactly sections 1 through 6 from the fixed S1-S5 Subproblem Solver prompt, including solved/failure YAML and local source ledger.

--- INPUTS FOR THIS RUN ---
Target theorem:
Let N >= 3 be an integer. For any N-component hyperbolic link L subset S^3 with exterior X_L = S^3 \ int(N(L)), where N(L) is a regular neighborhood of L, if P subset X_L is an incompressible spanning planar surface, meaning a planar surface with exactly one boundary component on each boundary torus of X_L, then at least one boundary component of P must have a slope a/p in standard meridian-longitude coordinates that is either meridional or integral, i.e. p in {0, 1}.

Additional mathematical guidance:
None

S0 blueprint:
C1: Normalize each slope as `r_i = a_i/p_i`, `p_i >= 0`, and assume for contradiction that every `p_i >= 2`.
C2: Dehn filling `X_L` along all slopes `r_i` caps `P` to an embedded sphere `\widehat P`.
C3: `\widehat P` is essential in the filled manifold.
C4: In the situation of C2-C3, hyperbolicity of `L` and `N >= 3` force some filled slope to satisfy `Δ(r_i, μ_i) <= 1`.
C5: Since `Δ(r_i, μ_i) = p_i`, C4 contradicts C1; therefore some `p_i ∈ {0,1}`.
Assignments: S1 notation/slope equivalence; S2 capping/filling and core intersections; S3 reducibility data and one-intersection parity; S4 core-once reducible filling obstruction; S5 assembly.

Assigned subproblem:
S4: Prove the core-once reducible filling obstruction: for a hyperbolic `N >= 3` link in `S^3`, such a reducing sphere after full filling forces at least one filling slope to have meridian distance at most `1`.

Important: If you cannot prove this from the supplied packet and genuinely standard background without importing a deep named theorem as an unsupported black box, mark the subproblem unsolved and give a precise candidate lemma or missing theorem.