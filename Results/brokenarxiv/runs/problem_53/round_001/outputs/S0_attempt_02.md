1. Target decomposition

target_label: Problem 53  
target_type: conditional blow-up criterion / exclusion of finite-time splash at bounded curvature  
main_goal: Prove by contradiction that finite-time material self-intersection of the free boundary cannot occur while the boundary curvature remains uniformly bounded.  
variables_and_parameters: dimension `d >= 2`; classical smooth solution on `[0,T_*)`; exterior fluid domain `Omega(t)=R^d \ B(t)`; compact smooth embedded free boundary `Gamma(t)=partial B(t)`; material parametrization `X(t,a)`; viscosity `nu>0`; surface tension `sigma>0`; principal curvatures `kappa_i`; curvature size  
`K(t)=sup_{x in Gamma(t)} max_i |kappa_i(x,t)|`.  
conclusion_to_prove: If there exist distinct labels `a != b` with `|X(t,a)-X(t,b)| -> 0` as `t upward T_*`, then necessarily  
`limsup_{t upward T_*} K(t)=+infinity`.

2. Available tools

tool: Classical smoothness before `T_*`  
source_status: provided definition / assumption  
exact_statement_or_fact: For every compact subinterval `[0,T] subset [0,T_*)`, the free boundary, velocity, pressure, curvature, normal, and material parametrization are smooth and meaningful.  
intended_role_in_proof: Allows all geometric evolution identities, localization, and compactness arguments before the alleged collapse time.

tool: Material parametrization and kinematic condition  
source_status: provided definition / assumption  
exact_statement_or_fact: The boundary is transported by the fluid velocity: `partial_t X(t,a)=u(X(t,a),t)` for labels on the reference hypersurface.  
intended_role_in_proof: Converts geometric self-intersection into a statement about two transported boundary labels and gives control of their separation from velocity regularity.

tool: Dynamic stress balance with surface tension  
source_status: provided definition / assumption  
exact_statement_or_fact: On `Gamma(t)`, the viscous fluid stress balances the surface-tension force proportional to mean curvature.  
intended_role_in_proof: Supplies boundary regularity and elliptic/parabolic control when curvature is bounded.

tool: Local graph representation from bounded curvature  
source_status: standard background fact  
exact_statement_or_fact: A smooth embedded hypersurface with uniformly bounded second fundamental form admits uniform local graph charts at sufficiently small scale, with controlled `C^{1,1}` norm, around every boundary point.  
intended_role_in_proof: Reduces the possible splash region to two or more controlled nearby graph sheets.

tool: Compactness of bounded-curvature embedded hypersurfaces in local charts  
source_status: standard background fact  
exact_statement_or_fact: Uniform local graph bounds imply subsequential convergence in local `C^1` and weak higher norms, after choosing charts and times approaching `T_*`.  
intended_role_in_proof: Produces a limiting local configuration at the first contact point if curvature stays bounded.

tool: Parabolic regularity for viscous free-boundary Navier-Stokes with surface tension  
source_status: proved inside the current proof  
exact_statement_or_fact: Under a uniform curvature bound and classical smoothness before `T_*`, the local graph functions, velocity, pressure, and stress enjoy uniform higher regularity estimates up to `T_*` in any controlled coordinate patch.  
intended_role_in_proof: Prevents loss of regularity other than curvature blow-up and makes the limiting contact configuration smooth enough to analyze.

tool: No-splash local uniqueness / separation lemma  
source_status: proved inside the current proof  
exact_statement_or_fact: In the one-phase viscous surface-tension problem, two distinct material boundary sheets cannot first meet at finite time while remaining smooth with uniformly bounded curvature and controlled local PDE norms.  
intended_role_in_proof: This is the decisive contradiction to bounded-curvature self-intersection.

tool: Continuation criterion  
source_status: proved inside the current proof  
exact_statement_or_fact: If curvature and the corresponding local free-boundary regularity norms remain bounded up to `T_*`, then the classical solution extends past `T_*` as an embedded free-boundary solution.  
intended_role_in_proof: Alternative formulation of the no-splash contradiction: bounded curvature would allow continuation, contradicting the assumed first loss of injectivity.

3. Subclaim support graph

id: SC1  
statement: If the theorem fails, then there is a classical smooth solution with finite `T_*`, labels `a != b` satisfying `|X(t,a)-X(t,b)| -> 0`, and a constant `M < infinity` such that `K(t) <= M` for all `t<T_*` close to `T_*`.  
uses_prior_subclaims: none  
purpose: Sets up contradiction.  
status: must be proved in final proof.  
suggested_solver: S1

id: SC2  
statement: Under `K(t) <= M`, every boundary point near `T_*` has a uniform local graph representation with controlled slope and second derivative, after rotating coordinates.  
uses_prior_subclaims: SC1  
purpose: Converts the geometric problem into controlled local sheets.  
status: standard background / must be proved in final proof with standard differential geometry.  
suggested_solver: S1

id: SC3  
statement: The approaching labels from SC1 generate, after passing to times `t_n upward T_*`, a limiting local configuration in which two distinct boundary sheets meet at a common point while each sheet remains a controlled smooth graph up to the limit.  
uses_prior_subclaims: SC1, SC2  
purpose: Identifies the precise local splash scenario.  
status: must be proved in final proof.  
suggested_solver: S2

id: SC4  
statement: Uniform curvature control plus the Navier-Stokes equations, kinematic condition, and surface-tension stress balance yield uniform local parabolic/free-boundary regularity estimates near the alleged contact point up to time `T_*`.  
uses_prior_subclaims: SC2, SC3  
purpose: Rules out hidden degeneration of the PDE variables while curvature remains bounded.  
status: must be proved in final proof.  
suggested_solver: S3

id: SC5  
statement: A first contact of two distinct material free-boundary sheets at finite time is impossible under the local regularity estimates of SC4.  
uses_prior_subclaims: SC3, SC4  
purpose: Gives the main contradiction to bounded-curvature splash.  
status: must be proved in final proof.  
suggested_solver: S4

id: SC6  
statement: Therefore the assumption `sup_{t<T_*} K(t)<infinity` is false, so `limsup_{t upward T_*} K(t)=+infinity`.  
uses_prior_subclaims: SC1, SC5  
purpose: Closes the blow-up criterion.  
status: must be proved in final proof.  
suggested_solver: S5

4. Hardest step prediction

hardest_step_id: SC5  
hardest_step_description: Proving that two distinct boundary sheets cannot first touch while all geometric and PDE norms remain controlled. Pure geometry is insufficient because bounded-curvature embedded hypersurfaces can have separate sheets approaching each other. The proof must use viscosity, surface tension, the kinematic condition, and local well-posedness/uniqueness for the free-boundary system.  
risk_if_wrong: If SC5 is replaced by a purely geometric assertion, the proof becomes false: bounded curvature alone does not prevent near self-contact.  
how_final_proof_should_handle_it: The final proof should explicitly localize near the putative contact, flatten the two sheets, use the PDE estimates from SC4, and invoke or prove a local uniqueness/continuation argument showing that the smooth free-boundary solution extends past `T_*` as an embedded interface, contradicting the definition of collapse.

5. Failure-mode checks

circularity_check: Do not assume the target theorem or any no-splash theorem equivalent to it. Any no-splash principle must be proved locally from the equations and regularity estimates inside the current proof.  
full_theorem_check: The conclusion must be curvature blow-up along `t upward T_*`, not merely failure of smoothness or loss of parametrization.  
source_check: No external sources, web search, prior outputs, or hidden lemmas are used.  
hypothesis_check: The argument must use `nu>0`, `sigma>0`, one-phase free boundary, exterior bubble geometry, classical smoothness for `t<T_*`, and material loss of injectivity.  
notation_check: `K(t)` is the supremum over `Gamma(t)` of the largest absolute principal curvature. “Bubble collapse” means material self-intersection, not necessarily volume collapse to a point.  
standard_background_check: Standard differential geometry may supply local graph charts and compactness, but global separation cannot be inferred from curvature bounds alone.

6. Subproblem assignment table

S1: Formalize the contradiction setup and prove the local graph lemma from bounded principal curvatures. State carefully that this gives only local control, not global injectivity.

S2: Starting from two labels whose images approach, extract a sequence of times and local coordinate systems producing a limiting two-sheet contact configuration. Track distinct material labels and preserve the embeddedness for every `t<T_*`.

S3: Prove the local PDE regularity estimate under bounded curvature: flatten the interface, express the one-phase viscous surface-tension system in local coordinates, and obtain uniform control of velocity, pressure, stress, and graph functions up to `T_*`.

S4: Prove the no-first-contact lemma for two locally smooth material boundary sheets satisfying the one-phase viscous surface-tension system with the regularity supplied by S3.

S5: Assemble S1-S4 into the contradiction proof and conclude `limsup_{t upward T_*} K(t)=+infinity`.

7. Web-source confirmation

no web sources used