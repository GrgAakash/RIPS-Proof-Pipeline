Fresh no-history solver-only round 2 Midfielder. You are spawned with fork_context=false and must use only this message as input. Do not use memory, prior task history, web/internet, API keys, Python, or files. This is solver-only.

You are SS3, a Midfielder with work_scope: assigned_subclaim. Solve only the assigned local subclaim and do not write the full target proof.

Use only this packet, allowed supporting statements, and facts you prove in your own subproof. Do not use Tate-Nakayama, Nakayama valuation image theorem, or an equivalent transfer-generation theorem unless you prove it inside this artifact. Do not use web/external sources.

Allowed supporting statements:
Definitions of finite Galois extensions of nonarchimedean local fields, Galois groups, fixed fields, ramification index, D-lattices, tensor notation, local valuation sequence 1 -> O_L^x -> L^x -> Z -> 0, Hilbert 90 for finite Galois extensions, and basic finite group cohomology/restriction/corestriction identities are allowed. The target local reverse inclusion itself is not allowed unless proved here.

Output sections:
1. Assignment restatement
2. Subproof or failure. If solved, give a rigorous proof. If unsolved, say SUBPROBLEM UNSOLVED and identify the obstacle.
3. Solver failure output YAML with main_solver_proof_key:null.
4. Local Source Ledger.
5. Interface notes for Manager acceptance.
6. Web-source confirmation: no web sources used.

--- INPUTS FOR THIS RUN ---
Assigned subclaim CL8:
Let L/F be a finite Galois extension of nonarchimedean local fields, D=Gal(L/F), and Y a finite free Z-lattice with D-action. Normalize ord_L by ord_L(pi_L)=1. Define nu_L:(Y tensor_Z L^x)^D -> Y^D by applying ord_L to the L^x factor. Prove, or precisely fail to prove, the reverse inclusion
im(nu_L) subset sum_{H<=D} e(L/L^H) N_{D/H}(Y^H),
where N_{D/H}(y)=sum_{sigma in D/H} sigma y.

Required checks:
- explicit ramification factor e(L/L^H);
- nonnormal H handling;
- clarify whether a boundary/corestriction sketch using Hilbert 90 and cor-res identities actually proves the inclusion or needs a missing theorem.

Target theorem context only:
This local lemma would support a proof of T(Q_p)=T(Z_p)T(Q) for Q-tori, but do not prove that parent theorem.

No web sources used.