Fresh no-history solver-only BRANCH Main Solver. Branch depth 1 of max 2. You are spawned with fork_context=false and must use only this message as input. Do not use memory, prior task history, web/internet, API keys, Python, or files. This is solver-only: do not run verifier/citation/final-checker pipeline.

You are SS1, a Subproblem Solver in a branch pipeline. work_scope: global_solution for the branch target only. Solve the complete branch target in one coherent argument. Do not prove the parent torus theorem.

Use only the supplied branch packet, allowed supporting statements, Manager routing plan for assignment, genuinely standard background, and facts you prove here. Do not use Tate-Nakayama, Nakayama valuation image theorem, or an equivalent transfer-generation theorem unless you prove it inside this branch. Do not use external sources or web search.

Allowed supporting statements:
Definitions of finite Galois extensions of nonarchimedean local fields, Galois groups, fixed fields, ramification index, D-lattices, tensor notation for split tori/cocharacter lattices, local valuation sequence 1 -> O_L^x -> L^x -> Z -> 0, and basic Hilbert 90 for finite Galois extensions are allowed. The target branch lemma itself, Tate-Nakayama/Nakayama valuation image theorem, or an equivalent transfer-generation theorem is not allowed unless proved inside the branch.

Output sections:
1. Assignment restatement
2. Subproof or failure. For global_solution, wrap the proof body in `<!-- BEGIN_FINAL_PROOF -->` and `<!-- END_FINAL_PROOF -->`. If unsolved, state SUBPROBLEM UNSOLVED and the obstacle.
3. Solver failure output and candidate guidance, with YAML including failure_output_type and main_solver_proof_key.
4. Local Source Ledger.
5. Interface notes for Manager acceptance.
6. Web-source confirmation: no web sources used.

--- INPUTS FOR THIS BRANCH RUN ---
Branch target theorem:
Let L/F be a finite Galois extension of nonarchimedean local fields, D=Gal(L/F), and Y a finite free Z-lattice with D-action. Normalize ord_L by ord_L(pi_L)=1. Define nu_L:(Y tensor_Z L^x)^D -> Y^D by applying ord_L to the L^x factor. Then every element of im(nu_L) lies in sum_{H<=D} e(L/L^H) N_{D/H}(Y^H), where N_{D/H}(y)=sum_{sigma in D/H} sigma y.

Parent note for why needed:
Together with already-established forward inclusion, this reverse inclusion gives the local valuation image formula needed for the parent torus decomposition. Do not prove parent target here.

Branch Manager routing plan summary:
SS1 must prove the full branch target with explicit cocycle/kernel reasoning and Hilbert 90 only where permitted. Key high-risk claim: kernel-generation by transfer terms. SS2 Defender will run last to audit forbidden dependency leakage, exactness, direction, and ramification normalization.
Critical claims:
CC001: connecting-map kernel for 0 -> Y tensor O_L^x -> Y tensor L^x -> Y -> 0 is exactly im(nu_L).
CC002: kernel of connecting map is contained in sum_{H<=D} e(L/L^H)N_{D/H}(Y^H).
CC003: e(L/L^H) is the correct valuation contribution from L^H inside L.

Additional mathematical guidance:
None