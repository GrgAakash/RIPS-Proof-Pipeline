Fresh no-history solver-only Main/Manager pipeline, round 3 (final allowed guidance round). You are spawned with fork_context=false and must use only this message as input. Do not use memory, prior task history, web/internet, API keys, Python, or files. This is solver-only: do not run verifier/citation/final-checker pipeline. Do not infer any previous attempt from the guidance; it is only mathematical guidance.

You are the Manager in the routing phase. Create an executable routing plan. Do not write the final solution. Select exactly one Main Solver SS1 and one Defender SS2 initially; no Midfielders/Attackers before Main Solver.

Allowed supporting statements:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. There are no prior formal supporting theorem/lemma/proposition/corollary statements. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

Produce sections 1-10: Target normalization; Task-adaptive proof obligations; Available tools; Subclaim support graph; Critical Claims Ledger; Key-step and Main Solver selection; Failure-mode checks; Subsolver execution plan with SS1 Main Solver and SS2 Defender; Subsolver assignment table exactly SS1 and SS2; Web-source confirmation.

--- INPUTS FOR THIS RUN ---
Cleaned skeleton packet:
Standalone problem statement only. No proof text, proof sketch, derivation, or prior formal result is included. Standard definitions/notation for algebraic tori over Q, local fields Q_p, T(Q_p), rational points T(Q), and the maximal compact subgroup of a p-adic torus may be inferred only to parse the target.

Target theorem:
For any algebraic torus T over Q and any prime number p, the decomposition T(Q_p) = T(Z_p) T(Q) holds, where T(Z_p) denotes the maximal compact subgroup of T(Q_p).

Additional mathematical guidance:
1. Prove the local Nakayama valuation reverse inclusion with the stated ramification normalization: for finite Galois local L/F with D=Gal(L/F) and D-lattice Y, every element of nu_L((Y tensor L^x)^D) lies in sum_{H<=D} e(L/L^H) N_{D/H}(Y^H).
2. Do not settle the local valuation image formula by citing a named Nakayama/Tate-Nakayama theorem or an unproved transfer-generation theorem; either give a complete proof of the transfer-generation kernel statement for arbitrary D-lattices, including nonnormal subgroups, ramification factors, denominator and saturation details, or choose a different route that avoids the lemma.