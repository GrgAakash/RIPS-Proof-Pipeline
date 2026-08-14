Fresh no-history solver-only Manager assistance-routing phase. You are spawned with fork_context=false and must use only this message as input. Do not use memory, prior task history, web/internet, API keys, Python, or files. This is solver-only: do not run verifier/citation/final-checker pipeline.

You are the Manager in the assistance-routing phase. Your task is to read Main Solver's first complete-proof attempt and decide whether bounded assistance is justified. Do not solve the mathematics yourself. Do not edit the Critical Claims Board directly; emit proposed board updates only through the executable plan, and the controller will merge them.

You are given:
1. the cleaned skeleton PDF or TeX file;
2. the target theorem;
3. the Allowed supporting statements list;
4. the additional mathematical guidance list, if any;
5. Manager's initial routing plan and initial Critical Claims Board;
6. Main Solver's draft attempt, including scratch work, uncertain_steps, help_requests, and proposed_board_updates.

Staffing rule. Start from the already selected Main Solver and Defender. Add a Midfielder only for one concrete contextual bottleneck Main Solver exposed or for one expectation-blind checking assignment Manager must route. Add an Attacker only when Main Solver is blocked or when Manager can state why a genuinely independent complete route is justified. Do not add agents for vague coverage, consensus, or parallel reassurance. The round's total active SS workers must remain between 2 and 10. Solver-only defaults for this experiment: max_support_items_total=3, max_specialist_batches_per_round=2, max_challenge_resolver_calls_per_round=2.

Visibility rule. Constructive Midfielders may see the target, relevant board claim, Main Solver's surrounding proof context, and why the lemma matters. Checking-mode Midfielders must be expectation-blind and must not be shown the desired answer. First-pass Attackers must be blind to Main Solver's detailed proof and candidate answer; route them only the target, allowed materials, and their independent route objective. Midfielder-to-Midfielder collaboration is allowed only if you record the dependency in the assignment.

Produce exactly these sections. The execution plan must be complete and contiguous: if you add support, repeat Main Solver and Defender assignments as SS1 and SS2 and then add SS3, SS4, ... as needed. Main Solver and Defender IDs must match the initial plan.

1. Post-Main Solver assessment

main_solver_draft_read: YES / NO
candidate_answer_seen:
uncertain_steps_seen:
help_requests_seen:
assistance_justification:
no_support_reason_if_any:

5. Critical Claims Ledger

Restate any new or changed CC### proposals from Main Solver that Manager admits for controller merging. Use the same fenced YAML proposal format as worker artifacts (`critical_claim_id`, `claim`, `why_critical`, `live_alternatives`, `resolution_test`, `basis`, `status`, `owner`). If none, write "None found after Manager's post-Main-Solver assistance check."

8. Subsolver execution plan

subsolver_count: integer 2 through 10
constructive_solver_count: subsolver_count minus 1
subsolver_count_rationale:
specialist_escalation_rationale: for each worker beyond Main Solver and the Defender, state whether the worker is a Midfielder or Attacker and the concrete mathematical need; otherwise write `NOT_NEEDED - Main Solver plus Defender is sufficient`
main_solver_id: the same SS-ID selected in Manager's initial plan
global_solver_id: exactly the same SS-ID as main_solver_id
key_solver_id: exactly the same SS-ID as main_solver_id
defender_solver_id: the same Defender SS-ID selected in Manager's initial plan
stress_test_solver_id: exactly the same SS-ID as defender_solver_id
attacker_solver_ids: JSON-style list of active non-Main Solver, non-Defender Attackers, or []
coverage_check: PASS / FAIL - explain why the chosen team is sufficient and bounded
independence_check: PASS / FAIL - identify duplicate assignments and remove them

9. Subsolver assignment table

Write exactly `subsolver_count` contiguous assignments named SS1, SS2, ..., SSN. Every assignment must be self-contained and must not require seeing material outside the supplied packet, the initial Manager plan, and the visibility allowed for that role.

SS#:
role: Main Solver / midfielder / attacker / defender
work_scope: global_solution / assigned_subclaim / alternative_route / adversarial_stress_test
assigned_subclaim_ids:
task:
required_deliverable:
connection_to_target:
where_used_in_final_solution:
independence_constraint:
failure_or_salvage_focus:

10. Web-source confirmation

Write "no web sources used".

--- INPUTS FOR THIS RUN ---
Cleaned skeleton packet:
Standalone problem statement only. No proof text, proof sketch, derivation, or prior formal result is included. Standard definitions/notation for algebraic tori over Q, local fields Q_p, T(Q_p), rational points T(Q), and the maximal compact subgroup of a p-adic torus may be inferred only to parse the target.

Target theorem:
For any algebraic torus T over Q and any prime number p, the decomposition T(Q_p) = T(Z_p) T(Q) holds, where T(Z_p) denotes the maximal compact subgroup of T(Q_p).

Allowed supporting statements:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. There are no prior formal supporting theorem/lemma/proposition/corollary statements. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

Additional mathematical guidance:
None

Initial Manager routing plan:
Target normalized as: prove for arbitrary algebraic torus T/Q and arbitrary prime p that T(Q_p)=T(Z_p)T(Q), where T(Z_p) is the maximal compact subgroup of T(Q_p). Main Solver SS1 owns all constructive subclaims SC1-SC5: identify local quotient by maximal compact, prove local valuation quotient, globalize every local quotient class to T(Q), conclude equality, check edge cases. Defender SS2 runs last and attacks local quotient normalization, hidden hypotheses, ramification/residue-degree factors, class-group obstructions, descent validity, and edge cases. Initial critical claims:
CC001: T(Z_p) means maximal compact subgroup, not arbitrary integral model points. ESTABLISHED by packet.
CC002: theorem equivalent to surjectivity T(Q)->T(Q_p)/T(Z_p). ESTABLISHED by elementary reduction.
CC003: local quotient T(Q_p)/T(Z_p) correctly identified with normalized valuation/cocharacter lattice. OPEN.
CC004: every local quotient class represented by T(Q). OPEN.
CC005: one-place weak approximation for arbitrary Q-tori, if used, must be proved or justified. SOURCE_GAP.
CC006: no hidden split/unramified/quasi-trivial/rank hypotheses. ESTABLISHED by target.
CC007: class-group/principal-divisor obstruction in splitting field eliminated. OPEN.

Main Solver draft:
SS1 produced a complete candidate proof with proof key true. Essential proof body:
- Choose finite Galois splitting field E/Q, w|p, Gamma=Gal(E/Q), D=Gamma_w, L=E_w, F=Q_p, Y=X_*(T_E).
- Define valuation over L: nu_L:T(L)->Y by <chi,nu_L(t)>=ord_L(chi(t)). For t in T(F)=T(L)^D, nu_L(t) in Y^D.
- Claim local valuation image formula:
  nu_L(T(F)) = Lambda_p(T) := sum_{H<=D} e(L/L^H) N_{D/H}(Y^H) subset Y^D.
  Main Solver gave one inclusion using y in Y^H and uniformizer pi_H of L^H, product over D/H of delta(y(pi_H)), with valuation e(L/L^H)N_{D/H}y. It asserted the reverse inclusion as Nakayama's elementary valuation lemma from 1->O_L^x->L^x->Z->0 after applying D-equivariant homomorphisms from the character lattice, with Hilbert 90 exactness.
- Kernel of nu_L:T(F)->Lambda_p(T) is T(F) cap T(O_L), compact; any compact subgroup maps trivially to the discrete free abelian Lambda_p(T); hence kernel is maximal compact T(Z_p). Therefore T(Q_p)/T(Z_p) ~= Lambda_p(T).
- For global surjectivity, realize generators e(L/L^H)N_{D/H}y. For H<=D and y in Y^H, choose a in (E^H)^x by weak approximation with ord_u(a)=1 at place u below w and ord_{u'}(a)=0 for every other u'|p. Define q=prod_{gamma in Gamma/H} gamma(y(a)) in T(E). This is Gamma-invariant, hence q in T(Q). Local valuation at w receives contribution exactly from gamma in D, each with ord_L=e(L/L^H), so nu_L(q)=e(L/L^H)N_{D/H}y. Therefore every local quotient generator is represented by T(Q).
- For x in T(Q_p), choose q in T(Q) with nu_L(q)=nu_L(x). Then xq^{-1} is in kernel T(Z_p), proving containment; reverse containment formal. Edge cases trivial torus and anisotropic local torus noted.

Main Solver uncertain_steps:
None marked unsupported, but CC008 is the technical claim most worth adversarial checking.

Main Solver help_requests:
Defender should test CC008 on G_m, Res_{K/Q}G_m, norm-one tori, and ramified local extensions.

Main Solver proposed_board_updates:
Mark CC003, CC004, and CC007 as established if Defender accepts the Nakayama valuation computation. Add CC008:
```yaml
critical_claim_id: CC008
claim: The local valuation image for a torus split by a finite Galois local extension L/F is generated by norm/corestriction valuations e(L/L^H)N_{D/H}(Y^H).
claim_basis: derived_here
exact_statement_used: For D=Gal(L/F), image(nu_L:T(F)->Y^D)=sum_{H<=D} e(L/L^H)N_{D/H}(Y^H).
hypotheses_checked: L/F finite Galois, T split over L, Y=X_*(T_L).
normalization: ord_L is used; ramification factors are explicit.
local_source_location: Section 2, local valuation computation.
competing_variants: The naive lattice Y^D can be too large when ramification is present.
status: ESTABLISHED
```

Main Solver source/risk summary:
Uses standard split torus valuation map, weak approximation in number fields, and Galois descent. Claims local valuation image formula is proved inside current proof but recognizes it as the key technical risk. No web sources used.