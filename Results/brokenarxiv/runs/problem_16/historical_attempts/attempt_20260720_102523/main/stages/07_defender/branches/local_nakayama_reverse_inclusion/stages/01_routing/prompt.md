Fresh no-history solver-only BRANCH Manager routing phase. Branch depth 1 of max 2. You are spawned with fork_context=false and must use only this message as input. Do not use memory, prior task history, web/internet, API keys, Python, or files. This is solver-only: do not run verifier/citation/final-checker pipeline.

Branch target type: clean standalone auxiliary lemma, weaker than the parent target. If accepted, the controller may seal it as E001 and later main solvers may use only its exact statement, not this branch history.

You are the Manager in the routing phase. Your task is to create an executable routing plan for the normalized branch problem. Do not write the final solution. Use the solver/manager collaborative architecture. In this initial routing pass, select exactly one active worker as Main Solver, who owns the complete branch proof, and exactly one separate Defender who runs last. Do not launch Midfielders or Attackers yet.

Use only the supplied branch packet, allowed supporting statements, genuinely standard background, and facts workers prove inside the branch. Do not use external sources or web search.

Allowed supporting statements:
Definitions of finite Galois extensions of nonarchimedean local fields, Galois groups, fixed fields, ramification index, D-lattices, tensor notation for split tori/cocharacter lattices, local valuation sequence 1 -> O_L^x -> L^x -> Z -> 0, and basic Hilbert 90 for finite Galois extensions are allowed. The target branch lemma itself, Tate-Nakayama/Nakayama valuation image theorem, or an equivalent transfer-generation theorem is not allowed unless proved inside the branch.

Produce exactly these sections, adapted to the branch target:
1. Target normalization
2. Task-adaptive proof obligations
3. Available tools
4. Subclaim support graph
5. Critical Claims Ledger with CC### YAML blocks or None found
6. Key-step and Main Solver selection
7. Failure-mode checks
8. Subsolver execution plan with constructive_solver_count: 1, subsolver_count: 2, SS1 Main Solver, SS2 Defender
9. Subsolver assignment table exactly SS1 and SS2
10. Web-source confirmation: no web sources used

--- INPUTS FOR THIS BRANCH RUN ---
Branch target theorem:
Let L/F be a finite Galois extension of nonarchimedean local fields, D=Gal(L/F), and Y a finite free Z-lattice with D-action. Normalize ord_L by ord_L(pi_L)=1. Define nu_L:(Y tensor_Z L^x)^D -> Y^D by applying ord_L to the L^x factor. Then every element of im(nu_L) lies in sum_{H<=D} e(L/L^H) N_{D/H}(Y^H), where N_{D/H}(y)=sum_{sigma in D/H} sigma y.

Parent note for why needed:
Together with the already-established forward inclusion, this reverse inclusion gives the local valuation image formula needed for the torus decomposition target. Do not prove the parent target here.

Additional mathematical guidance:
None