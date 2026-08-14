Fresh no-history solver-only Main Solver integration/repair phase. You are spawned with fork_context=false and must use only this message as input. Do not use memory, prior task history, web/internet, API keys, Python, or files. This is solver-only: do not run verifier/citation/final-checker pipeline.

You are SS1, a Subproblem Solver. Follow the machine-readable `work_scope` in your Manager routing assignment:
* `global_solution`: you are Main Solver, the Main Solver. Solve the complete target problem in one coherent argument. This is the integration/repair phase: consider only Manager-approved constructive results supplied in your assignment. Write a full candidate solution, not a list of suggestions or disconnected subproofs, and make clear whether your proof key is ready for Manager acceptance.

Work in two passes. First read the target semantically: infer the standard definitions, parameter conventions, named-object setup, and ordinary admissibility conditions needed to make your assignment mathematically coherent. Then attempt the assigned mathematics and preserve the strongest complete or partial derivation or candidate you can obtain. Only afterward fill the failure summary, Source Ledger, critical-claim statuses, and Critical Claims Ledger addendum. Provenance uncertainty must not stop exploration, but it must prevent an unsupported step from being certified as established.

Use only the supplied packet, allowed supporting statements, guidance list, Manager's current-round routing plan for assignment and planning, the support bundle supplied here, genuinely standard background, and facts you prove in your own proof or subproof. The Manager routing plan and support bundle are not mathematical premises: do not cite them as proof of a mathematical fact unless the relevant derivation is present and correct. Do not use external sources, web search, related writeups, unstated task-specific facts, hidden lemmas, or any material not included in the provided packet.

Allowed supporting statements:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. There are no prior formal supporting theorem/lemma/proposition/corollary statements. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

If required inputs are missing, stop and write "SETUP FAILURE: missing input." Then list the missing input(s).

Produce exactly the following sections.

1. Assignment restatement

Manager-ID:
work_scope:
assigned subclaim(s):
what must be proved:
connection to the exact target:
inferred_standard_setup_for_this_assignment:
where this result is used in the final solution:
declared prerequisite subclaims:

2. Subproof or failure

For `global_solution`, write Main Solver's complete rigorous solution of the exact target and check every task-adaptive obligation from Manager. Wrap the proof body that may become the final candidate in `<!-- BEGIN_FINAL_PROOF -->` and `<!-- END_FINAL_PROOF -->`. If you cannot complete the work required by your scope from allowed materials, write "SUBPROBLEM UNSOLVED" and name the missing obstacle. If you obtain partial progress, preserve the strongest rigorously established intermediate claim and explain exactly how it narrows the remaining gap. If your work depends on a critical claim you cannot resolve, record it in the Critical Claims Ledger addendum below and mark it UNESTABLISHED or SOURCE_GAP.

3. Solver failure output and candidate guidance

Write the controller-facing summary as one fenced YAML block. Do not put prose before this YAML block inside section 3. If `work_scope: global_solution`, include `main_solver_proof_key: true | false`. If solved, use `failure_output_type: solved`; otherwise choose exactly one of forbidden-route / obstruction guidance, branch lemma target, ordinary hint request, no useful guidance item found. Do not output more than one candidate guidance item.

For solved, write exactly these keys:
```yaml
failure_output_type: solved
main_solver_proof_key: true | false | null
type: ""
failed_route: ""
obstruction: ""
evidence: ""
reuse_value: ""
guidance_sentence: null
source_gap: false
external_material_status: not_applicable
autonomous_derivation_possible: true
candidate_lemma_statement: null
why_unblocks: null
where_used: null
allowed_inputs: null
dependencies: null
weaker_than_target: null
equivalent_or_stronger: null
recommended: null
```

For unsolved, fill the same keys and choose the most specific valid failure_output_type.

4. Local Source Ledger

For every load-bearing mathematical claim, theorem, lemma, identity, formula, construction, or nontrivial background fact used:
claim_id:
proof_location:
claim_or_fact_used:
source_status: provided definition / notation / assumption; allowed supporting statement; additional guidance item; standard background fact; proved inside the current proof; or unsupported or unclear.
cited_label_or_name:
exact_statement_used:
hypotheses_or_conditions_needed:
where_hypotheses_are_checked:
strength_used:
notes:

If your work uses or fixes any claim listed in Manager's Critical Claims Ledger (CC###), additionally report for each such claim:
critical_claim_id: CC###
claim:
claim_basis: packet_statement / derived_here / standard_background / sealed_guidance_E### / unsupported_or_source_gap
exact_statement_used:
hypotheses_checked:
normalization:
local_source_location:
competing_variants:
status: ESTABLISHED / UNESTABLISHED / SOURCE_GAP

Critical Claims Ledger addendum. If your work surfaced a critical claim not already in Manager's ledger -- or showed that a listed claim is established or is a genuine source gap -- record one fenced YAML block per claim in Manager's ledger format. If none, write "No new critical claims."

5. Interface notes for Manager acceptance

what this subproof establishes:
what remains conditional:
failure_output_type:
candidate guidance sentence, if any:
auxiliary lemma candidate, if any:
notation introduced:
risk points:
candidate_answer:
complete_scratch_work_attempt:
uncertain_steps:
help_requests:
proposed_board_updates:

6. Web-source confirmation

Write "no web sources used".

--- INPUTS FOR THIS RUN ---
Cleaned skeleton packet:
Standalone problem statement only. No proof text, proof sketch, derivation, or prior formal result is included. Standard definitions/notation for algebraic tori over Q, local fields Q_p, T(Q_p), rational points T(Q), and the maximal compact subgroup of a p-adic torus may be inferred only to parse the target.

Target theorem:
For any algebraic torus T over Q and any prime number p, the decomposition T(Q_p) = T(Z_p) T(Q) holds, where T(Z_p) denotes the maximal compact subgroup of T(Q_p).

Additional mathematical guidance:
None

Manager routing and assistance plan:
SS1 remains Main Solver for global_solution, assigned SC1-SC5 and CC003/CC004/CC007/CC008. SS3 was admitted as support for CC008. SS2 Defender will run last after this integration pass. Initial critical claims:
CC001: T(Z_p) means maximal compact subgroup, not arbitrary integral model points. ESTABLISHED by packet.
CC002: theorem equivalent to surjectivity T(Q)->T(Q_p)/T(Z_p). ESTABLISHED by elementary reduction.
CC003: local quotient T(Q_p)/T(Z_p) correctly identified with normalized valuation/cocharacter lattice. OPEN.
CC004: every local quotient class represented by T(Q). OPEN.
CC005: one-place weak approximation for arbitrary Q-tori, if used, must be proved or justified. SOURCE_GAP.
CC006: no hidden split/unramified/quasi-trivial/rank hypotheses. ESTABLISHED by target.
CC007: class-group/principal-divisor obstruction in splitting field eliminated. OPEN.
CC008: local valuation image formula image(nu_L:T(F)->Y^D)=sum_{H<=D} e(L/L^H)N_{D/H}(Y^H). SOURCE_GAP after admitted SS3 support unless you provide a complete in-artifact proof or corrected route.

Your earlier draft proof summary supplied for repair:
You attempted to prove the target by choosing finite Galois splitting field E/Q, w|p, Gamma, D, L, Y. You defined nu_L and claimed local formula image(nu_L:T(Q_p)->Y^D)=Lambda=sum_{H<=D}e(L/L^H)N_{D/H}(Y^H). You used this to identify kernel with maximal compact T(Z_p), then globally realized each generator by choosing a in (E^H)^x with prescribed valuations at places above p and setting q=prod_{gamma in Gamma/H} gamma(y(a)) in T(Q). You marked solved with proof_key true, but asked to scrutinize CC008.

Manager-approved support bundle from SS3:
SS3 is ADMITTED only for these contents:
- SS3 proves the forward inclusion sum_{H<=D} e(L/L^H)N_{D/H}(Y^H) subset image(nu_L:T(F)->Y^D) by the uniformizer/norm construction.
- SS3 verifies the ramification normalization: with ord_L(pi_L)=1, coefficient e(L/L^H) is correct; for F-normalized valuation it would rescale.
- SS3 does NOT prove the reverse inclusion. It marks CC008 as SOURCE_GAP unless you prove the Nakayama valuation lemma or avoid the need for it.
- SS3 candidate missing lemma: For finite Galois L/F with D=Gal(L/F) and any D-lattice M, im((M tensor L^x)^D -> M^D) equals sum_{H<=D} ord_L((L^x)^H) N_{D/H}(M^H). Substituting M=Y and ord_L((L^H)^x)=e(L/L^H)Z gives CC008.
- SS3 obstruction: Hilbert 90 alone, as presented, proves subgroup valuation facts but not the full transfer-generation reverse inclusion for arbitrary D-lattices.

No web sources used.