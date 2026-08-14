Fresh no-history solver-only round 3 Main Solver. Use only this message. No memory, prior task history, web/internet, API keys, Python, or files. This is solver-only.

You are SS1, Main Solver, work_scope: global_solution. Solve the target in one coherent argument, or declare unsolved. You must not cite Nakayama/Tate-Nakayama or an unproved transfer-generation theorem. If you use the local reverse inclusion, prove it fully with nonnormal subgroups, ramification factors, denominator and saturation details. Alternatively find a complete different route avoiding it.

Allowed supporting statements:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. No prior formal supporting theorem/lemma/proposition/corollary statements. No statement equivalent to, stronger than, or downstream from the target theorem is allowed.

Output sections:
1. Assignment restatement
2. Subproof or failure, with `<!-- BEGIN_FINAL_PROOF -->` markers if solved.
3. Solver failure output YAML with failure_output_type and main_solver_proof_key true/false.
4. Local Source Ledger and critical claim statuses.
5. Interface notes for Manager acceptance.
6. Web-source confirmation: no web sources used.

Inputs:
Target theorem: For any algebraic torus T over Q and prime p, T(Q_p)=T(Z_p)T(Q), T(Z_p) maximal compact.
Guidance:
1. Prove the local Nakayama valuation reverse inclusion with stated ramification normalization: finite Galois local L/F, D=Gal(L/F), D-lattice Y, im(nu_L) subset sum_{H<=D} e(L/L^H)N_{D/H}(Y^H).
2. Do not settle local valuation image by citing named Nakayama/Tate-Nakayama or an unproved transfer-generation theorem; either give complete proof of transfer-generation kernel statement for arbitrary D-lattices, including nonnormal subgroups, ramification factors, denominator and saturation details, or choose a different route avoiding the lemma.
Manager plan: set up global splitting field K/Q, G=Gal(K/Q), place w|p, L=K_w, decomposition group D, Y=X_*(T_K). Need invariant descriptions, compact-kernel identification, local valuation formula, global realization of transfer generators by weak approximation in K^H, and final decomposition. Main audit target is local reverse inclusion.