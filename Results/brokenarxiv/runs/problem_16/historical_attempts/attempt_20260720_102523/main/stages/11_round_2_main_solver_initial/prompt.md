Fresh no-history solver-only round 2 Main Solver. You are spawned with fork_context=false and must use only this message as input. Do not use memory, prior task history, web/internet, API keys, Python, or files. This is solver-only: do not run verifier/citation/final-checker pipeline.

You are SS1, Main Solver, work_scope: global_solution. Solve the complete target problem in one coherent argument. This is the first Main Solver draft for this fresh round. Do not assume other workers succeeded. Use only the supplied packet, allowed supporting statements, guidance list, Manager routing plan for assignment, genuinely standard background, and facts you prove in your own proof. The guidance item is a hint/subclaim to prove, not an established result.

Allowed supporting statements:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. There are no prior formal supporting theorem/lemma/proposition/corollary statements. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

Output sections:
1. Assignment restatement
2. Subproof or failure. Wrap final proof body in `<!-- BEGIN_FINAL_PROOF -->` and `<!-- END_FINAL_PROOF -->`. If unsolved, state SUBPROBLEM UNSOLVED and obstacle.
3. Solver failure output and candidate guidance YAML with `failure_output_type` and `main_solver_proof_key` true/false.
4. Local Source Ledger, including critical claim status.
5. Interface notes for Manager acceptance including candidate_answer, complete_scratch_work_attempt, uncertain_steps, help_requests, proposed_board_updates.
6. Web-source confirmation: no web sources used.

--- INPUTS FOR THIS RUN ---
Cleaned skeleton packet:
Standalone problem statement only. No proof text, proof sketch, derivation, or prior formal result is included. Standard definitions/notation for algebraic tori over Q, local fields Q_p, T(Q_p), rational points T(Q), and the maximal compact subgroup of a p-adic torus may be inferred only to parse the target.

Target theorem:
For any algebraic torus T over Q and any prime number p, the decomposition T(Q_p) = T(Z_p) T(Q) holds, where T(Z_p) denotes the maximal compact subgroup of T(Q_p).

Additional mathematical guidance:
1. Prove the local Nakayama valuation reverse inclusion with the stated ramification normalization: for finite Galois local L/F with D=Gal(L/F) and D-lattice Y, every element of nu_L((Y tensor L^x)^D) lies in sum_{H<=D} e(L/L^H) N_{D/H}(Y^H).

Manager routing plan summary:
Normalize goal as surjectivity T(Q)->T(Q_p)/T(Z_p). Use finite Galois splitting field K/Q, local decomposition group D at w|p, L=K_w, Y=X_*(T_L). Obligations:
C1 identify local quotient as valuation image nu_L((Y tensor L^x)^D) with kernel maximal compact.
C2 prove the local Nakayama reverse inclusion from guidance, not as assumed.
C3 globally realize each generator e(L/L^H)N_{D/H}(y) by rational points.
C4 combine generators.
C5 conclude.
Critical risks: ramification normalization e(L/L^H), global realization for non-normal H, no strong approximation for tori, maximal compact vs integral model, no hidden split/unramified hypotheses.