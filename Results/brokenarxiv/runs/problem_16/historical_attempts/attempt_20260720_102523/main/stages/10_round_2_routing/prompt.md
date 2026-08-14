Fresh no-history solver-only Main/Manager pipeline, round 2. You are spawned with fork_context=false and must use only this message as input. Do not use memory, prior task history, web/internet, API keys, Python, or files. This is solver-only: do not run verifier/citation/final-checker pipeline. Do not infer any previous attempt from the guidance; it is just a mathematical hint.

You are the Manager in the routing phase. Your task is to create an executable routing plan for the normalized target problem. Do not write the final solution. Do not certify an unsupported candidate answer as established. You may record plausible candidate answers, theorem-recognition routes, or inferred standard setup as non-evidentiary context for Main Solver, Midfielders, Attackers, and the Defender to test, derive, or challenge.

Use the solver/manager collaborative architecture. In this initial routing pass, select exactly one active worker as Main Solver, the Main Solver, who owns the complete proof, and exactly one separate Defender who runs last and attacks Main Solver's integrated proof. Do not launch Midfielders or Attackers yet. Specialist staffing is a later Manager decision made only after reading Main Solver's first attempt, uncertain_steps, help_requests, and proposed_board_updates.

Use only the supplied packet, allowed supporting statements, guidance list, genuinely standard background, and facts that later subproblem solvers would need to prove inside the current solution. Do not use external sources, web search, related writeups, unstated task-specific facts, hidden lemmas, or any material not included in the provided packet.

Allowed supporting statements:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. There are no prior formal supporting theorem/lemma/proposition/corollary statements. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

Produce exactly the following sections: 1. Target normalization; 2. Task-adaptive proof obligations; 3. Available tools; 4. Subclaim support graph; 5. Critical Claims Ledger; 6. Key-step and Main Solver selection; 7. Failure-mode checks; 8. Subsolver execution plan with exactly SS1 Main Solver and SS2 Defender initially; 9. Subsolver assignment table exactly SS1 and SS2; 10. Web-source confirmation.

--- INPUTS FOR THIS RUN ---
Cleaned skeleton packet:
Standalone problem statement only. No proof text, proof sketch, derivation, or prior formal result is included. Standard definitions/notation for algebraic tori over Q, local fields Q_p, T(Q_p), rational points T(Q), and the maximal compact subgroup of a p-adic torus may be inferred only to parse the target.

Target theorem:
For any algebraic torus T over Q and any prime number p, the decomposition T(Q_p) = T(Z_p) T(Q) holds, where T(Z_p) denotes the maximal compact subgroup of T(Q_p).

Additional mathematical guidance:
1. Prove the local Nakayama valuation reverse inclusion with the stated ramification normalization: for finite Galois local L/F with D=Gal(L/F) and D-lattice Y, every element of nu_L((Y tensor L^x)^D) lies in sum_{H<=D} e(L/L^H) N_{D/H}(Y^H).