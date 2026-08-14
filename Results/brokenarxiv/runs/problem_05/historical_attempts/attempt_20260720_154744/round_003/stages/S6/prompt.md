Fresh no-history solver-only S0-S6 pipeline run, round 3 final composer. No web, internet, files, API keys, code execution, calculators, scripts, tools, memory, or prior history. Use only the target theorem, guidance, current-round S0 blueprint, current-round S1-S5 outputs, and genuinely standard background. Do not use previous round artifacts.

You are S6, Composer Solver. Compose final candidate proof from current-round S0 and S1-S5. If a required subclaim is unsolved, either prove it fully from allowed material or report the exact obstacle. Do not fake a proof. Produce sections: 1. Composition map; 2. Final proof wrapped markers; 3. Composer YAML fixed schema; 4. Source Ledger markers; 5. Completion checklist markers; 6. Web-source confirmation markers; 7. LaTeX artifact.

Target theorem: Let N >= 3 be an integer. For any N-component hyperbolic link L subset S^3 with exterior X_L = S^3 \ int(N(L)), where N(L) is a regular neighborhood of L, if P subset X_L is an incompressible spanning planar surface, meaning a planar surface with exactly one boundary component on each boundary torus of X_L, then at least one boundary component of P must have a slope a/p in standard meridian-longitude coordinates that is either meridional or integral, i.e. p in {0, 1}.

Guidance:
1. Prove or avoid core-once reducible filling obstruction: full Dehn filling a hyperbolic N-component link exterior in S^3, N>=3, along slopes r_i yielding reducible manifold with reducing sphere intersecting each filling core once implies some Delta(r_i,mu_i)<=1. Do not assume unless proved or exact standard theorem.
2. Exact candidate theorem: Scharlemann/Gordon-Luecke-type reducible surgery theorem for links in S^3: if surgery on all components produces reducible manifold and reducing sphere intersects every surgery core exactly once, then at least one surgery coefficient has denominator 0 or 1. Do not cite informally.

Round-3 S0 blueprint:
S0 route: fill along boundary slopes r_i; cap P to sphere widehat P; each core intersects once; prove widehat P reducing; apply precise reducible-surgery obstruction; translate Delta(a_i/p_i,mu_i)=|p_i|. Hardest step is obstruction. S0 assigns S1 capping, S2 reducing sphere, S3 obstruction, S4 audit, S5 denominator translation.

S1 output:
S1 solved capping construction assuming connected planar surface convention. Let alpha_i=partial P cap T_i. Fill along alpha_i, attach V_i, choose meridian disks D_i with boundary alpha_i. widehat P=P union D_i is closed embedded. If P is connected planar with N boundary components, widehat P is S^2. Each filling core c_i intersects its meridian disk D_i once and is disjoint from P and other disks, so |c_i cap widehat P|=1. Caveat: if planar surfaces are allowed disconnected, capping gives disjoint union of spheres, not one sphere; target likely uses connected surface convention.

S2 output:
S2 solved non-ball-bounding. If widehat P bounded a 3-ball B, any closed filling core c_i transverse to partial B would have even mod-2 intersection with partial B, but c_i intersects widehat P exactly once. Contradiction. Thus widehat P does not bound a 3-ball. Incompressibility, hyperbolicity, and N>=3 are not needed for this parity step.

S3 output:
S3 did not solve obstruction and chose branch lemma target. It could not honestly discharge the obstruction from standard background without importing specialized Scharlemann/Gordon-Luecke link-surgery theorem whose exact statement could not be verified. Branch lemma target: Let L be an n-component link in S^3, n>=3. Let M be obtained by Dehn surgery on every component with slopes r_1,...,r_n. Suppose M is reducible and has a reducing sphere S such that S intersects each surgery solid torus in exactly one meridian disk, equivalently each surgery core exactly once. Then for some component i, Delta(r_i,mu_i)<=1. Required precision: state nonsplit/hyperbolic assumptions, S^1xS^2 cases, minimal intersection, and denominator conclusion.

S4 output:
S4 audited applicability conditionally assuming exact theorem available. It found capping supplies full filling and core-once data. It initially said reducibility needed extra check, but S2 supplies that check via parity. Conditional on exact theorem, all hypotheses appear satisfied: L hyperbolic, full filling one slope on every component, capped planar surface is sphere, each core intersects sphere once, and S2 proves reducing.

S5 output:
S5 solved denominator translation. For slope a/p represented by a mu + p lambda and meridian 1/0, Delta(a/p,mu)=|a*0-1*p|=|p|. If Delta<=1, then |p|<=1; normalizing p>=0 gives p in {0,1}. p=0 is meridional; p=1 is integral. Conditional dependency: need obstruction to give Delta<=1.