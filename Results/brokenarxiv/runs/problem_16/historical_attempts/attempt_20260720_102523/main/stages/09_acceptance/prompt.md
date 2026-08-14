Fresh no-history solver-only Manager Acceptance phase. You are spawned with fork_context=false and must use only this message as input. Do not use memory, prior task history, web/internet, API keys, Python, or files. This is solver-only: do not run verifier/citation/final-checker pipeline.

You are the Manager in the acceptance phase. Your task is to decide whether Main Solver's complete proof can be accepted and packaged as the final candidate solution for the target problem. You own routing and acceptance. Main Solver owns the proof.

Work in two explicit passes. First inspect Main Solver's proof and supporting artifacts without deciding provenance label or answer status. Preserve Main Solver's proof as the only complete proof candidate; use Midfielder/branch outputs only as evidence that Main Solver explicitly integrated or as audit context. Only after candidate proof is fixed, perform a provenance pass filling critical-claim discharges, Source Ledger, Background and Assumptions Manifest, answer_status, and candidate_basis. Do not repair, rewrite, splice, average, or replace Main Solver's proof.

Use only the supplied packet, allowed supporting statements, guidance list, Manager routing plan for organization, Main Solver's proof, active support outputs, genuinely standard background, and facts proved inside Main Solver's proof. Do not use external sources or web search. If a blocking challenge is not RESOLVED, write FINAL PROOF NOT COMPLETED or report a SOURCE_GAP obstruction, never ESTABLISHED.

Allowed supporting statements:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. There are no prior formal supporting theorem/lemma/proposition/corollary statements. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

Produce sections:
1. Composition map. Include discharge records for every blocking challenge and critical-claim discharge table for all CC###.
2. Main Solver authorship and proof-reference audit.
3. Manager failure output and candidate guidance. Include YAML with failure_output_type, answer_status, candidate_basis, manager_acceptance_key, main_solver_id, main_solver_proof_complete, main_solver_proof_used_as_final, main_solver_proof_replaced:false, base_change_defect_ids:[], changes_to_base:[], incompatible_outputs_averaged:false, unsupported_claims_added:false, and guidance fields.
4. Source Ledger wrapped in markers.
5. Background and Assumptions Manifest wrapped in markers.
6. Completion checklist wrapped in markers.
7. Web-source confirmation wrapped in markers.

--- INPUTS FOR THIS RUN ---
Cleaned skeleton packet:
Standalone problem statement only. No proof text, proof sketch, derivation, or prior formal result is included. Standard definitions/notation for algebraic tori over Q, local fields Q_p, T(Q_p), rational points T(Q), and the maximal compact subgroup of a p-adic torus may be inferred only to parse the target.

Target theorem:
For any algebraic torus T over Q and any prime number p, the decomposition T(Q_p) = T(Z_p) T(Q) holds, where T(Z_p) denotes the maximal compact subgroup of T(Q_p).

Additional mathematical guidance:
None

Manager routing plan and active worker summary:
Initial Manager selected SS1 Main Solver and SS2 Defender. Assistance Manager added SS3 for CC008. SS3 admitted partial support only. Main Solver integrated support and wrote candidate proof. Defender blocked. Checking-mode resolver returned CC008 unresolved. A branch pipeline on the local reverse-inclusion lemma was opened; branch Defender blocked branch acceptance, so no sealed E result exists.

Critical Claims Board:
CC001: T(Z_p) means maximal compact subgroup. ESTABLISHED by packet.
CC002: theorem equivalent to surjectivity T(Q)->T(Q_p)/T(Z_p). ESTABLISHED by elementary reduction.
CC003: local quotient T(Q_p)/T(Z_p) correctly identified with normalized valuation/cocharacter image. Dependent on CC008; unresolved for exact image.
CC004: every local quotient class represented by T(Q). Dependent on CC008; global construction works for transfer generators.
CC005: one-place weak approximation for arbitrary Q-tori, if used, must be proved. Main proof does not use this; uses number-field weak approximation.
CC006: no hidden split/unramified/quasi-trivial/rank hypotheses. Held conditional on CC008.
CC007: class-group/principal-divisor obstruction eliminated. Held for transfer generators but full claim dependent on CC008.
CC008: local valuation image formula image(nu_L:T(F)->Y^D)=sum_{H<=D}e(L/L^H)N_{D/H}(Y^H). Forward inclusion and normalization established by SS3; reverse inclusion unproved/source gap.

Main Solver integrated proof:
<!-- BEGIN_FINAL_PROOF -->
Let E/Q be a finite Galois extension splitting T. Put Gamma=Gal(E/Q), Y=X_*(T_E). Then Galois descent gives T(Q)=(Y tensor E^x)^Gamma. Choose w|p, set L=E_w, F=Q_p, D=Gamma_w=Gal(L/F). Since E tensor_Q Q_p ~= product_{Gamma/D} L, Shapiro descent identifies T(F)=T(Q_p) ~= (Y tensor L^x)^D.

Let ord_L be normalized by ord_L(pi_L)=1. Define nu_L:(Y tensor L^x)^D -> Y^D by nu_L(sum_i y_i tensor a_i)=sum_i ord_L(a_i)y_i. Its kernel is (Y tensor O_L^x)^D, compact. Since image of nu_L lies in free abelian group Y^D, every compact subgroup of (Y tensor L^x)^D maps trivially under nu_L. Hence this kernel is the maximal compact subgroup of T(F). Thus T(Z_p)=ker nu_L.

Use the standard local Nakayama valuation theorem. For finite Galois L/F, D=Gal(L/F), and any D-lattice Y,
nu_L((Y tensor L^x)^D)=sum_{H<=D} e(L/L^H) N_{D/H}(Y^H), where N_{D/H}(y)=sum_{sigma in D/H} sigma y. The inclusion right-to-left is elementary by y in Y^H and a in (L^H)^x with ord_L(a)=e(L/L^H). The reverse inclusion is the usual Nakayama/Tate-Nakayama valuation lemma applied to 1->O_L^x->L^x->Z.

Now take arbitrary t in T(Q_p), viewed as element of (Y tensor L^x)^D. Put v=nu_L(t). By local valuation formula, v=sum_j n_j e(L/L^{H_j})N_{D/H_j}(y_j) for subgroups H_j<=D, integers n_j, y_j in Y^{H_j}.

For each generator, fix H<=D and y in Y^H. Let K=E^H and w_H be the place of K below w. By weak approximation in K, choose a in K^x with ord_{w_H}(a)=1 and a unit at every other place of K above p. Since w is the unique place of E above w_H for E/K, ord_L(a)=e(L/L^H). Define q_{H,y,a}=sum_{gamma in Gamma/H} gamma(y tensor a) in Y tensor E^x. Because y tensor a is H-fixed, this element is well-defined and Gamma-fixed, hence q_{H,y,a} in T(Q). Its w-local valuation is e(L/L^H)sum_{delta in D/H}delta y=e(L/L^H)N_{D/H}(y). Indeed, among cosets gamma H in Gamma/H, only those with gamma in D contribute at w; all other terms are units at w by choice of a.

Taking the product of corresponding q_{H_j,y_j,a_j}^{n_j}, obtain q in T(Q) with nu_L(q)=v=nu_L(t). Therefore nu_L(tq^{-1})=0, so tq^{-1} in ker nu_L=T(Z_p). Thus t in T(Z_p)T(Q). Since t was arbitrary, T(Q_p)=T(Z_p)T(Q).
<!-- END_FINAL_PROOF -->
Main Solver proof key true; but interface notes say acceptance depends on allowing local Nakayama/Tate-Nakayama as standard background; if stricter self-containment required, request dedicated proof.

SS3 support:
Forward inclusion transfer sum subset image and ramification normalization established. Reverse inclusion not proved; CC008 marked SOURCE_GAP unless Nakayama lemma is admitted/proved.

Defender report:
BLOCK. Challenged CC003/CC004/CC007/CC008. Obstruction: reverse inclusion in local Nakayama valuation formula is unproved and not admitted by allowed packet. Required resolution: prove/admit exact local Nakayama/Tate-Nakayama valuation lemma with L-normalized valuation. Candidate lemma: For chosen finite Galois local L/F with D-lattice Y, every element of nu_L((Y tensor L^x)^D) lies in sum_{H<=D} e(L/L^H)N_{D/H}(Y^H). This is weaker than parent target and recommended.

Checking-mode resolver:
UNRESOLVED for CC008 and dependent CC003/CC004/CC007. It found special tests consistent but no supplied/derived proof of arbitrary-lattice reverse inclusion.

Branch pipeline result:
Branch target was the local reverse inclusion. Branch Main Solver attempted proof via transfer-duality lemma. Branch Defender BLOCKED: transfer-duality lemma was asserted, not proved; double-coset divisibility and dual lattice rescaling incomplete; no sealed E result accepted.

No web sources used.