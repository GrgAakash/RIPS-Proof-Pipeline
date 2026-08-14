Fresh no-history solver-only S0-S6 pipeline run. Do not use web search, internet, files, API keys, code execution, calculators, scripts, or tools. Use only the mathematical problem statement below, the filled S6 role prompt below, S0 blueprint, S1-S5 outputs, and genuinely standard background that you name precisely. Do not use memory or prior task history.

Cleaned skeleton packet for this standalone run: the target theorem statement itself, with its notation and assumptions. There are no additional skeleton statements.

You are S6, the Composer Solver. Your task is to compose a single final candidate proof of the target theorem from the current-round S0 blueprint and S1-S5 subproblem outputs.

Use only the supplied packet, allowed supporting statements, guidance list, S0 blueprint for organization, S1-S5 outputs that actually prove their claimed subclaims, genuinely standard background, and facts proved inside your composed proof. The S0 blueprint is not a mathematical premise: do not cite it as proof of a mathematical fact. Do not use external sources, web search, related writeups, unstated task-specific facts, hidden lemmas, or any material not included in the provided packet.

Do not silently fill a missing major subproof. If S1-S5 leave a required subclaim unsolved, either prove it fully from allowed materials in the composed proof and mark it as proved inside current proof, or report the obstacle. Do not cite the target theorem, an equivalent theorem, a stronger theorem, or a logically downstream statement.

Allowed supporting statements:
Standalone problem packet only. Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. No formal skeleton theorem/lemma/proposition/corollary statements are supplied. No prior statements, later-but-upstream inclusions, exclusions, or unclear formal statements are available. Genuinely standard background may be used only if named precisely and with the exact version needed.

If required inputs are missing, stop and write "SETUP FAILURE: missing input." Then list the missing input(s).

Produce exactly these sections: 1. Composition map; 2. Final proof wrapped in <!-- BEGIN_FINAL_PROOF --> and <!-- END_FINAL_PROOF -->; 3. Composer failure output and candidate guidance as one fenced YAML block using the fixed S6 schema; 4. Source Ledger wrapped in <!-- BEGIN_SOURCE_LEDGER --> and <!-- END_SOURCE_LEDGER -->; 5. Completion checklist wrapped in <!-- BEGIN_COMPLETION_CHECKLIST --> and <!-- END_COMPLETION_CHECKLIST -->; 6. Web-source confirmation wrapped in <!-- BEGIN_WEB_SOURCE_CONFIRMATION --> and <!-- END_WEB_SOURCE_CONFIRMATION -->; 7. LaTeX artifact. Include exactly one [KEY STEP] in any attempted complete proof. If you cannot write a complete proof from the supplied artifacts and standard background, write "FINAL PROOF NOT COMPLETED" and identify the exact blocking point. Do not fake a complete proof.

--- INPUTS FOR THIS RUN ---
Target theorem:
Let N >= 3 be an integer. For any N-component hyperbolic link L subset S^3 with exterior X_L = S^3 \ int(N(L)), where N(L) is a regular neighborhood of L, if P subset X_L is an incompressible spanning planar surface, meaning a planar surface with exactly one boundary component on each boundary torus of X_L, then at least one boundary component of P must have a slope a/p in standard meridian-longitude coordinates that is either meridional or integral, i.e. p in {0, 1}.

Additional mathematical guidance:
None

S0 blueprint summary:
S0 decomposed the proof into: C1 slope normalization and contradiction assumption p_i >= 2 for all i; C2 Dehn filling along boundary slopes caps P to an embedded sphere widehat P; C3 widehat P is essential in the filled manifold by core-intersection parity; C4 core-once reducible filling obstruction for hyperbolic N >= 3 links: such a reducing sphere after full filling forces some Delta(r_i,mu_i)<=1; C5 translate Delta(a_i/p_i,mu_i)=p_i and conclude. S0 predicted C4 as the hardest step and warned that it must not be assumed circularly or imported as an unsupported deep theorem.

S1 output:
S1 solved notation setup. Let T_i=partial N(L_i), choose standard meridian-longitude coordinates (mu_i,lambda_i), and let gamma_i=partial P cap T_i have reduced slope r_i=a_i/p_i with p_i>=0. By the target convention, meridional or integral is exactly p_i in {0,1}. Hence not meridional or integral is equivalent to p_i notin {0,1}, and since p_i is a nonnegative integer this is equivalent to p_i>=2. S1 marked this solved and used no web sources.

S2 output:
S2 solved the capping construction. For each i, fill T_i along r_i by a solid torus V_i whose meridian disk D_i has boundary gamma_i. Then widehat P = P union D_1 union ... union D_N is an embedded closed surface. Since P is planar with exactly N boundary components, capping all boundary components gives a closed connected genus-zero surface, hence a sphere. If c_i is the core of V_i, then c_i intersects D_i once and is disjoint from P and from other caps, so each filling core intersects widehat P exactly once. S2 noted that essentiality is not proved there.

S3 output:
S3 solved the reducibility data conditional on S2. Let M be the full filling along the r_i. Each core K_i intersects widehat P exactly once. If widehat P bounded a 3-ball B in M, then any closed curve has mod-2 intersection zero with partial B=widehat P; but K_i has one transverse intersection with widehat P. Contradiction. Thus widehat P cannot bound a 3-ball. S3 recorded the downstream obstruction hypotheses: L hyperbolic, N>=3, full filling along slopes r_i, embedded sphere widehat P, every core meets it once, and widehat P does not bound a ball.

S4 output:
S4 did not solve the core-once reducible filling obstruction. It stated that the following missing theorem is required and is not derivable from the standalone packet and elementary standard background: "For a hyperbolic N-component link L in S^3 with N >= 3, if full Dehn filling along slopes r_i yields a reducible manifold with a reducing sphere intersecting each filling core once, then some slope r_i satisfies Delta(r_i, mu_i) <= 1." S4 said this appears to be a specialized reducible Dehn filling theorem and did not import it as a black box.

S5 output:
S5 solved the final assembly only conditional on S4. If no boundary component is meridional or integral, S1 gives p_i>=2 for all i. S2-S3 give a filled manifold with an essential sphere meeting every filling core once. If S4 were available, it would give some Delta(r_i,mu_i)<=1. Standard slope distance gives Delta(a_i/p_i,mu_i)=p_i because p_i>=0, contradicting p_i>=2. Therefore some p_i in {0,1}. S5 explicitly marked dependence on S4.