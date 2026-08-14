Fresh no-history solver-only round 2 Main Solver integration pass. You are spawned with fork_context=false and must use only this message as input. Do not use memory, prior task history, web/internet, API keys, Python, or files. This is solver-only.

You are SS1, Main Solver, work_scope: global_solution. This is the integration/repair phase. Consider only Manager-approved support below. Do not assume CL8 is solved. You must either (a) provide a complete proof of the missing local reverse inclusion inside your final proof, or (b) mark SUBPROBLEM UNSOLVED and set main_solver_proof_key false. Do not cite Nakayama/Tate-Nakayama or a transfer-generation theorem as standard without proof.

Allowed supporting statements:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. There are no prior formal supporting theorem/lemma/proposition/corollary statements. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed. Additional guidance is a hint, not established.

Output sections:
1. Assignment restatement
2. Subproof or failure. Wrap final proof body in `<!-- BEGIN_FINAL_PROOF -->` and `<!-- END_FINAL_PROOF -->` if solved; otherwise say SUBPROBLEM UNSOLVED and obstacle.
3. Solver failure output and candidate guidance YAML with main_solver_proof_key true/false and, if unsolved, one guidance item.
4. Local Source Ledger.
5. Interface notes for Manager acceptance.
6. Web-source confirmation: no web sources used.

Inputs:
Target theorem: For any algebraic torus T over Q and prime p, T(Q_p)=T(Z_p)T(Q), T(Z_p) maximal compact.
Guidance: Prove local Nakayama valuation reverse inclusion: for finite Galois local L/F with D-lattice Y, im(nu_L) subset sum_{H<=D} e(L/L^H)N_{D/H}(Y^H).
Your draft proof: complete target proof but local reverse inclusion was compressed as standard Nakayama cohomological argument.
Manager-approved support from SS3: ADMITTED only partial content:
- proved easy containment sum_H e(L/L^H)N_{D/H}(Y^H) subset im(nu_L);
- verified ramification factor e(L/L^H) and nonnormal H handling for easy direction;
- identified unsolved obstruction: Hilbert 90 plus boundary/cor-res does not prove kernel transfer-generation for arbitrary D-lattice Y without an additional Nakayama-style transfer-generation theorem.
Rejected support: SS3 did NOT prove CL8 reverse inclusion. CL8 remains unsolved unless you prove it now.
No web sources used.