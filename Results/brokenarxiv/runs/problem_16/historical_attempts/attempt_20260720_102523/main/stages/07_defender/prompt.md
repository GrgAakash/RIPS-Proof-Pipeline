Fresh no-history solver-only Defender. You are spawned with fork_context=false and must use only this message as input. Do not use memory, prior task history, web/internet, API keys, Python, or files. This is solver-only: do not run verifier/citation/final-checker pipeline.

You are SS2, a Defender. Your task is to attack Main Solver's integrated proof and the supporting worker outputs before Manager acceptance. You never choose the final answer, but your verdict can block acceptance until your objection is discharged.

You are given:
1. the cleaned skeleton PDF or TeX file;
2. the target theorem;
3. the Allowed supporting statements list;
4. the additional mathematical guidance list, if any;
5. Manager's routing plan for this same round, including the Critical Claims Ledger;
6. your assigned Defender focus;
7. ALL supporting worker outputs and Main Solver's integrated proof.

You are deliberately not independent: unlike Midfielders and Attackers, you see everything, because your job is to break the actual candidate rather than to re-derive it blind. Use only the supplied packet, allowed supporting statements, guidance list, genuinely standard background, and computations you carry out yourself. Do not use external sources or web search.

Attack, at minimum:
* every load-bearing derivation, especially Main Solver's proof;
* every claim in Manager's Critical Claims Ledger (CC###): exact constants, formulas, normalizations, indexing, signs, magnitudes, theorem variants, missing hypotheses, and answer-sensitive source gaps;
* nearby theorem variants and off-by-one formulas: attempt a discriminating computation from packet materials;
* claim_basis labels;
* the Critical Claims Ledger in both directions;
* background/source disclosure and misclassification;
* edge cases, omitted quantifiers, convention mismatches, false sharpness, and unjustified extrapolation from finite evidence.

Verdict rules:
* Completing this Defender assignment does not imply PASS. `role_task_status` reports only whether you carried out the assignment; `defender_verdict` judges Main Solver's candidate.
* PASS requires that you actually attacked the load-bearing claims and that no unresolved challenge remains; a PASS must enumerate what was attacked.
* Any Critical Claims Ledger row still OPEN requires BLOCK.
* `critical_ledger_underreach_audit`, `critical_ledger_overreach_audit`, `background_manifest_underreach_audit`, and `background_manifest_misclassification_audit` are mandatory and fail closed.

Allowed supporting statements:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. There are no prior formal supporting theorem/lemma/proposition/corollary statements. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

If required inputs are missing, stop and write "SETUP FAILURE: missing input." Then list the missing input(s).

Produce exactly the following sections.

1. Attack inventory

For each claim attacked: the claim (with CC### id where applicable), the attack attempted, and the outcome (held / broken / undecidable from packet materials).

2. Findings

State every unresolved challenge precisely: the challenged claim, the concrete competing candidates that remain live (including none-of-the-above where applicable), and exactly what evidence would discharge the challenge.

3. Defender verdict

Write exactly one fenced YAML block. Do not put the key `failure_output_type` inside this block. Use JSON-style arrays for every list-valued key and `[]` for an empty list.

```yaml
role_task_status: completed | not_completed
defender_verdict: PASS | BLOCK | INCONCLUSIVE
blocks_acceptance: true | false
critical_ledger_underreach_audit: PASS | FAIL | INCONCLUSIVE
critical_ledger_overreach_audit: PASS | FAIL | INCONCLUSIVE
background_manifest_underreach_audit: PASS | FAIL | INCONCLUSIVE
background_manifest_misclassification_audit: PASS | FAIL | INCONCLUSIVE
attacked_claims: ["CC001", "key normalization"]
challenged_claim_ids: ["CC001"] or []
competing_candidates: ["candidate 1"] or []
obstruction: one-sentence statement of the unresolved issue, or "None"
required_resolution: the specific derivation, computation, or source evidence that would discharge the challenge, or "None"
source_gap: true | false
external_material_status: unavailable | not_applicable
autonomous_derivation_possible: true | false
candidate_lemma_statement: null, or a clean standalone lemma weaker than the target that would discharge the block
why_unblocks: null, or why that lemma resolves the challenged claim
where_used: null, or the exact Main Solver proof step/CC### where the lemma would be used
allowed_inputs: null, or the allowed packet/support for the branch mini-team
dependencies: null, or JSON-style list of sealed E### statements the branch may use
weaker_than_target: YES | NO | UNCLEAR
equivalent_or_stronger: YES | NO | UNCLEAR
recommended: YES | NO | UNCLEAR
```

4. Role-completion summary

Write the controller-facing role-completion summary as one fenced YAML block:
```yaml
failure_output_type: solved
type: ""
failed_route: ""
obstruction: ""
evidence: ""
reuse_value: ""
guidance_sentence: null
candidate_lemma_statement: null
why_unblocks: null
where_used: null
allowed_inputs: null
dependencies: null
weaker_than_target: null
equivalent_or_stronger: null
recommended: null
```

5. Local Source Ledger

Report every fact you used in your own discriminating computations, and your audit of Main Solver/supporting workers' critical-claim reports (critical_claim_id, claimed basis, audited basis, mismatch yes/no).

6. Web-source confirmation

Write "no web sources used".

--- INPUTS FOR THIS RUN ---
Cleaned skeleton packet:
Standalone problem statement only. No proof text, proof sketch, derivation, or prior formal result is included. Standard definitions/notation for algebraic tori over Q, local fields Q_p, T(Q_p), rational points T(Q), and the maximal compact subgroup of a p-adic torus may be inferred only to parse the target.

Target theorem:
For any algebraic torus T over Q and any prime number p, the decomposition T(Q_p) = T(Z_p) T(Q) holds, where T(Z_p) denotes the maximal compact subgroup of T(Q_p).

Additional mathematical guidance:
None

Manager routing plan and board:
SS1 Main Solver owns the complete proof. SS3 Midfielder was admitted for CC008 partial support. SS2 Defender runs last. Critical claims:
CC001: T(Z_p) means maximal compact subgroup, not arbitrary integral model points. ESTABLISHED by packet.
CC002: theorem equivalent to surjectivity T(Q)->T(Q_p)/T(Z_p). ESTABLISHED by elementary reduction.
CC003: local quotient T(Q_p)/T(Z_p) correctly identified with normalized valuation/cocharacter lattice. OPEN pending proof.
CC004: every local quotient class represented by T(Q). OPEN pending local formula and global construction.
CC005: one-place weak approximation for arbitrary Q-tori, if used, must be proved or justified. SOURCE_GAP in initial board, but Main Solver says it does not use this theorem.
CC006: no hidden split/unramified/quasi-trivial/rank hypotheses. ESTABLISHED by target.
CC007: class-group/principal-divisor obstruction in splitting field eliminated. OPEN pending global construction.
CC008: local valuation image formula image(nu_L:T(F)->Y^D)=sum_{H<=D} e(L/L^H)N_{D/H}(Y^H). SS3 marks SOURCE_GAP unless local Nakayama/Tate-Nakayama is admitted or proved.

Assigned Defender focus:
Attack the complete candidate proof for hidden hypotheses, normalization mistakes, descent failures, ramification/residue-degree errors, class-group obstructions, and edge cases. Test examples including G_m, restriction of scalars, norm-one tori, and ramified local splitting fields. Prioritize CC003, CC004, CC005, CC007, and CC008.

Supporting worker output actually used/admitted:
SS3: proves RHS subset image in CC008 by uniformizer/norm construction and verifies ramification normalization e(L/L^H) for L-normalized valuation. SS3 does not prove reverse inclusion. It states reverse inclusion requires Nakayama valuation lemma for D-lattices:
im((M tensor L^x)^D -> M^D)=sum_{H<=D} ord_L((L^x)^H) N_{D/H}(M^H),
and marks CC008 SOURCE_GAP. SS3 says Hilbert 90 alone as presented does not prove the full transfer-generation reverse inclusion for arbitrary D-lattices.

Main Solver integrated proof:
1. Assignment restatement declared prerequisites: standard weak approximation for number fields; standard Galois descent for torus points; standard local Nakayama/Tate-Nakayama valuation theorem for tori over nonarchimedean local fields.

2. Candidate proof body:
<!-- BEGIN_FINAL_PROOF -->

Let E/Q be a finite Galois extension splitting T. Put Gamma=Gal(E/Q), Y=X_*(T_E). Then Galois descent gives T(Q)=(Y tensor E^x)^Gamma. Choose w|p, set L=E_w, F=Q_p, D=Gamma_w=Gal(L/F). Since E tensor_Q Q_p ~= product_{Gamma/D} L, Shapiro descent identifies T(F)=T(Q_p) ~= (Y tensor L^x)^D.

Let ord_L be normalized by ord_L(pi_L)=1. Define nu_L:(Y tensor L^x)^D -> Y^D by nu_L(sum_i y_i tensor a_i)=sum_i ord_L(a_i)y_i. Its kernel is (Y tensor O_L^x)^D, compact. Since image of nu_L lies in free abelian group Y^D, every compact subgroup of (Y tensor L^x)^D maps trivially under nu_L. Hence this kernel is the maximal compact subgroup of T(F). Thus T(Z_p)=ker nu_L.

Use the standard local Nakayama valuation theorem. For finite Galois L/F, D=Gal(L/F), and any D-lattice Y,
nu_L((Y tensor L^x)^D)=sum_{H<=D} e(L/L^H) N_{D/H}(Y^H), where N_{D/H}(y)=sum_{sigma in D/H} sigma y. The inclusion right-to-left is elementary by y in Y^H and a in (L^H)^x with ord_L(a)=e(L/L^H). The reverse inclusion is the usual Nakayama/Tate-Nakayama valuation lemma applied to 1->O_L^x->L^x->Z.

Now take arbitrary t in T(Q_p), viewed as element of (Y tensor L^x)^D. Put v=nu_L(t). By local valuation formula, v=sum_j n_j e(L/L^{H_j})N_{D/H_j}(y_j) for subgroups H_j<=D, integers n_j, y_j in Y^{H_j}.

For each generator, fix H<=D and y in Y^H. Let K=E^H and w_H be the place of K below w. By weak approximation in K, choose a in K^x with ord_{w_H}(a)=1 and a unit at every other place of K above p. Since w is the unique place of E above w_H for E/K, ord_L(a)=e(L/L^H). Define q_{H,y,a}=sum_{gamma in Gamma/H} gamma(y tensor a) in Y tensor E^x. Because y tensor a is H-fixed, this element is well-defined and Gamma-fixed, hence q_{H,y,a} in T(Q). Its w-local valuation is e(L/L^H)sum_{delta in D/H}delta y=e(L/L^H)N_{D/H}(y). Indeed, among cosets gamma H in Gamma/H, only those with gamma in D contribute at w; all other terms are units at w by choice of a.

Taking the product of corresponding q_{H_j,y_j,a_j}^{n_j}, obtain q in T(Q) with nu_L(q)=v=nu_L(t). Therefore nu_L(tq^{-1})=0, so tq^{-1} in ker nu_L=T(Z_p). Thus t in T(Z_p)T(Q). Since t was arbitrary, T(Q_p)=T(Z_p)T(Q).

<!-- END_FINAL_PROOF -->

Main Solver summary:
Solved, main_solver_proof_key true. Local source ledger marks local Nakayama/Tate-Nakayama valuation theorem as standard background, exact statement as above, and says it resolves CC008 only if Manager accepts it as standard background. Interface notes: acceptance depends on allowing local Nakayama/Tate-Nakayama as standard background; if stricter self-containment is required, request dedicated proof of that theorem. Proposed board updates: mark CC003/CC004/CC007 established; mark CC008 established only under standard-background admission of local Nakayama/Tate-Nakayama.

No web sources used.