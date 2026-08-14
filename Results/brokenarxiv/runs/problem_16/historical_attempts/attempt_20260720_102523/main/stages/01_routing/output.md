1. Target normalization

target_label: unnamed target theorem

task_type: proof

exact_target_statement:
For every algebraic torus `T` over `Q` and every prime number `p`,
`T(Q_p) = T(Z_p) T(Q)`,
where `T(Z_p)` denotes the maximal compact subgroup of the locally compact group `T(Q_p)`.

variables_domains_assumptions_and_quantifiers:
`T` ranges over all algebraic tori over `Q`; `p` ranges over all rational primes. `T(Q)` is embedded in `T(Q_p)` by the natural inclusion `Q -> Q_p`. `T(Z_p)` is the maximal compact subgroup of `T(Q_p)`.

inferred_standard_setup:
An algebraic torus means a connected affine algebraic group that becomes isomorphic to a power of `G_m` over an algebraic closure. Local field notation, rational points, character/cocharacter lattices, splitting fields, and maximal compact subgroups of `p`-adic tori may be used only as standard parsing/setup.

reading_assumptions_used:
`T(Z_p)` is not assumed to come from a chosen integral model; it is the maximal compact subgroup by definition in the target. The desired equality means every element of `T(Q_p)` can be written as `k q` with `k in T(Z_p)` and `q in T(Q)`.

required_final_output:
A proof of the stated decomposition for arbitrary `T/Q` and arbitrary prime `p`, or a valid demonstration that the stated theorem is false if Main Solver finds an obstruction.

required_directions:
The inclusion `T(Z_p)T(Q) subset T(Q_p)` is formal. The nontrivial direction is: for each `x in T(Q_p)`, find `q in T(Q)` such that `x q^{-1} in T(Z_p)`.

2. Task-adaptive proof obligations

primary_claim:
The natural map `T(Q) -> T(Q_p)/T(Z_p)` is surjective.

converse_or_sharpness_requirement:
The reverse containment is automatic from subgroup membership. No sharpness, optimal constant, or extremal value is involved.

existence_or_feasibility_requirement:
For every local component/valuation class of `T(Q_p)` modulo its maximal compact subgroup, construct or prove existence of a rational point of `T(Q)` with that same class.

uniqueness_or_exhaustiveness_requirement:
No uniqueness of the factorization is required. Exhaustiveness of all local cosets modulo `T(Z_p)` is required.

domain_and_edge_cases:
Must cover split tori, anisotropic tori over `Q_p`, ramified and unramified splitting at `p`, norm-one type examples, `p=2`, and the trivial torus.

independent_stress_test:
After Main Solver produces a complete proof, Defender should test it on `G_m`, `Res_{K/Q} G_m`, norm-one tori, anisotropic local cases, ramified local extensions, and possible class-group/principal-divisor obstructions.

3. Available tools

tool:
Definitions of algebraic tori, rational points, local fields, maximal compact subgroup.
source_status: provided definition / notation / assumption
exact_statement_or_fact:
The packet allows standard definitions and notation needed to parse the theorem.
intended_role_in_proof:
Fix the objects and prevent ambiguity about `T(Z_p)`.

tool:
Character and cocharacter lattices of a torus with Galois action.
source_status: standard background fact
exact_statement_or_fact:
For a torus split by a finite Galois extension, its characters and cocharacters form finitely generated free abelian groups with compatible Galois actions determining the torus.
intended_role_in_proof:
Provide the language for local valuation/component computations.

tool:
Local valuation/Kottwitz-style map for a `p`-adic torus.
source_status: proved inside the current proof
exact_statement_or_fact:
Main Solver must establish the correct discrete quotient map from `T(Q_p)` to the component/valuation lattice whose kernel is the maximal compact subgroup `T(Z_p)`.
intended_role_in_proof:
Reduce the desired decomposition to surjectivity of `T(Q)` onto this discrete quotient.

tool:
Weak approximation / principal ideal control in number fields.
source_status: standard background fact
exact_statement_or_fact:
For a number field, prescribed valuations at finitely many finite places can be arranged by a global element after allowing auxiliary support away from those places, using standard ideal-class/approximation facts.
intended_role_in_proof:
Potentially globalize local valuation data at primes above `p`.

tool:
Galois descent for rational torus points.
source_status: standard background fact
exact_statement_or_fact:
If a torus `T/Q` is split by `E/Q`, then `T(Q)` is the Galois-fixed part of `T(E)` under the natural semilinear action.
intended_role_in_proof:
Convert a Galois-compatible construction over a splitting field into a rational point.

tool:
One-place weak approximation for tori.
source_status: unsupported or unclear
exact_statement_or_fact:
The possible assertion that `T(Q)` is dense in `T(Q_p)` for every `Q`-torus would imply the target because cosets of `T(Z_p)` are open.
intended_role_in_proof:
Possible alternate route only if Main Solver proves it with the required hypotheses; it must not be imported as an allowed prior theorem.

4. Subclaim support graph

id: SC1
statement:
Identify a canonical local component/valuation quotient `Lambda_p(T)` and map `nu_p: T(Q_p) -> Lambda_p(T)` such that `ker(nu_p)=T(Z_p)`.
uses_prior_subclaims: []
purpose:
Turns the group decomposition into a discrete surjectivity problem.
status: must be proved in final solution
suggested_solver: SS1

id: SC2
statement:
Show that `nu_p` is surjective onto the correctly normalized local lattice.
uses_prior_subclaims: [SC1]
purpose:
Ensures every local coset has a valuation representative and no local quotient class is missed.
status: must be proved in final solution
suggested_solver: SS1

id: SC3
statement:
For every `lambda in Lambda_p(T)`, construct or prove existence of `q in T(Q)` with `nu_p(q)=lambda`.
uses_prior_subclaims: [SC1, SC2]
purpose:
This is the main arithmetic globalization step.
status: must be proved in final solution
suggested_solver: SS1

id: SC4
statement:
Conclude that for every `x in T(Q_p)`, choosing `q in T(Q)` with `nu_p(q)=nu_p(x)` gives `xq^{-1} in T(Z_p)`.
uses_prior_subclaims: [SC1, SC3]
purpose:
Derives the nontrivial containment `T(Q_p) subset T(Z_p)T(Q)`.
status: must be proved in final solution
suggested_solver: SS1

id: SC5
statement:
Check the formal containment `T(Z_p)T(Q) subset T(Q_p)` and all edge cases.
uses_prior_subclaims: []
purpose:
Completes the equality and prevents missed degeneracies.
status: must be proved in final solution
suggested_solver: SS1

5. Critical Claims Ledger

```yaml
critical_claim_id: CC001
claim: "T(Z_p) means the maximal compact subgroup of T(Q_p), not the Z_p-points of an arbitrary integral model."
why_critical: "The theorem can change meaning if an integral model interpretation is substituted."
live_alternatives: ["maximal compact subgroup", "points of a chosen integral model"]
resolution_test: "Use the packet's explicit definition and avoid model-dependent arguments unless they recover the maximal compact subgroup."
basis: packet_statement
status: ESTABLISHED
owner: Manager
```

```yaml
critical_claim_id: CC002
claim: "The theorem is equivalent to surjectivity of T(Q) -> T(Q_p)/T(Z_p)."
why_critical: "This is the central reduction; proving only density, only finite-index image, or only split cases would not settle the exact target."
live_alternatives: ["surjective image", "dense image", "finite-index image", "surjective only after replacing T"]
resolution_test: "For arbitrary x in T(Q_p), verify existence of q in T(Q) with xq^{-1} in T(Z_p)."
basis: derived_here
status: ESTABLISHED
owner: Manager
```

```yaml
critical_claim_id: CC003
claim: "The local quotient T(Q_p)/T(Z_p) must be identified with the correctly normalized valuation/cocharacter lattice."
why_critical: "Using the wrong lattice, such as an uncorrected dual of rational characters, can introduce ramification or residue-degree errors."
live_alternatives: ["Kottwitz-style cocharacter quotient", "dual of Q_p-rational characters", "split-rank valuation lattice", "finite-index variant"]
resolution_test: "Test the formula on Res_{L/Q_p} G_m for ramified and unramified finite extensions L/Q_p."
basis: standard_background
status: OPEN
owner: Main Solver
```

```yaml
critical_claim_id: CC004
claim: "Every class in the local quotient T(Q_p)/T(Z_p) is represented by a rational point of T(Q)."
why_critical: "This is essentially the nontrivial direction of the target theorem."
live_alternatives: ["true for all Q-tori", "true only for quasi-trivial or split tori", "false due to a global obstruction"]
resolution_test: "Derive the globalization step from allowed standard facts, or produce a counterexample if an obstruction survives."
basis: unsupported_or_source_gap
status: OPEN
owner: Main Solver
```

```yaml
critical_claim_id: CC005
claim: "One-place weak approximation for arbitrary Q-tori, if used, must be proved or justified with exact hypotheses."
why_critical: "It is stronger than the target and cannot be silently imported as a prior theorem equivalent or downstream from the target."
live_alternatives: ["prove one-place weak approximation", "avoid it and prove only valuation surjectivity", "find failure of weak approximation affecting the target"]
resolution_test: "If invoked, provide a self-contained derivation adequate for arbitrary algebraic tori over Q."
basis: packet_external_unestablished
status: SOURCE_GAP
owner: Main Solver
```

```yaml
critical_claim_id: CC006
claim: "No hidden hypotheses such as split over Q, unramified at p, quasi-trivial, or positive Q-rank are present."
why_critical: "A proof under extra hypotheses would not prove the stated theorem."
live_alternatives: ["arbitrary Q-torus", "split torus", "unramified torus at p", "quasi-trivial torus"]
resolution_test: "Verify each reduction preserves arbitrary tori and arbitrary primes, including ramified and anisotropic cases."
basis: packet_statement
status: ESTABLISHED
owner: Manager
```

```yaml
critical_claim_id: CC007
claim: "Any class-group or principal-divisor obstruction in the splitting field can be eliminated in the globalization step."
why_critical: "A surviving obstruction would directly invalidate surjectivity onto the local quotient."
live_alternatives: ["auxiliary primes eliminate obstruction", "descent equations eliminate obstruction", "obstruction gives counterexample"]
resolution_test: "In the splitting-field construction, track prescribed valuations at places over p and prove the auxiliary choices still descend to T(Q)."
basis: unsupported_or_source_gap
status: OPEN
owner: Main Solver
```

6. Key-step and Main Solver selection

hardest_step_id: SC3

hardest_step_description:
Globalize an arbitrary local component/valuation class to a rational point of the torus without adding hidden hypotheses on `T` or on the prime `p`.

risk_if_wrong:
The proof may establish only a finite-index statement, only a split/quasi-trivial case, or a false theorem.

main_solver_id: SS1

key_solver_id: SS1

global_solver_id: SS1

why_this_solver_is_M:
Only one constructive worker is needed initially because the main uncertainty is global coherence: the local quotient identification, globalization step, descent, and final equality must be integrated in one proof attempt before splitting assistance.

what_would_invalidate_the_route:
A counterexample from a torus whose rational points do not meet every local maximal-compact coset; an incorrect local quotient normalization; an unproved use of weak approximation for arbitrary tori; or a hidden restriction to split, unramified, quasi-trivial, or norm-one special cases.

7. Failure-mode checks

circularity_check:
Do not use the target theorem or a stronger local-global theorem for tori as a black box unless it is proved inside the solution.

full_theorem_check:
The proof must handle every algebraic torus over `Q` and every prime `p`, not just split or quasi-trivial examples.

source_check:
No formal supporting theorem is supplied beyond definitions/notation. Any nontrivial arithmetic lemma must be standard background with exact hypotheses or proved in the current solution.

hypothesis_check:
No smooth integral model, good reduction, unramified splitting, connected component convention, or rank condition may be assumed unless derived or unnecessary.

notation_check:
`T(Z_p)` is the maximal compact subgroup. `T(Q)` is embedded into `T(Q_p)` through `Q subset Q_p`.

standard_background_check:
Permitted standard background includes basic torus character theory, local fields, valuations, number-field approximation, and Galois descent. It does not include an unsupported theorem equivalent to the target.

answer_anchor_check:
The answer is anchored by the exact equality `T(Q_p)=T(Z_p)T(Q)`. The proof must show equality of subsets, not merely density or finite index.

task_type_obligation_check:
This is a proof task. There is no numerical value, optimization, classification, or uniqueness output.

8. Subsolver execution plan

constructive_solver_count: 1

subsolver_count: 2

subsolver_count_rationale:
Initial phase uses exactly one Main Solver to produce a coherent complete candidate solution and exactly one separate Defender to attack it afterward. No specialist subclaims should be launched until Main Solver identifies uncertain steps or help requests.

specialist_escalation_rationale: `NOT_NEEDED - post-Main-Solver assistance routing has not run yet`

main_solver_id: SS1

global_solver_id: SS1

key_solver_id: SS1

defender_solver_id: SS2

stress_test_solver_id: SS2

attacker_solver_ids: []

coverage_check: PASS - SS1 owns all constructive proof obligations SC1-SC5; SS2 independently stress-tests the integrated proof after SS1 finishes.

independence_check: PASS - SS1 and SS2 have distinct roles; no duplicate constructive assignments are made.

9. Subsolver assignment table

SS1:
role: Main Solver
work_scope: global_solution
assigned_subclaim_ids: [SC1, SC2, SC3, SC4, SC5]
task:
Produce one coherent complete candidate solution to the exact target theorem. Establish the correct local quotient by the maximal compact subgroup, prove or replace the globalization step for arbitrary `Q`-tori and arbitrary primes, handle edge cases, and conclude the equality. Do not rely on any theorem equivalent to or stronger than the target unless proved inside the attempt.
required_deliverable:
Candidate answer, complete scratch-work attempt, uncertain_steps, help_requests, and proposed_board_updates. If the theorem appears false, provide the precise obstruction or counterexample candidate instead of forcing a proof.
connection_to_target:
Owns the full proof of `T(Q_p)=T(Z_p)T(Q)`.
where_used_in_final_solution:
Main body of the final proof, subject to later Defender review.
independence_constraint:
Work only from the packet, allowed definitions, standard background, and internally proved lemmas. Do not use external sources or prior writeups.
failure_or_salvage_focus:
If the direct valuation-globalization route fails, test whether one-place weak approximation can be proved; if that fails, search for a valid counterexample among norm-one or non-quasi-trivial tori.

SS2:
role: defender
work_scope: adversarial_stress_test
assigned_subclaim_ids: []
task:
Run last. Attack Main Solver's integrated proof and any support artifacts actually used. Check local quotient normalization, hidden hypotheses, circular imports, ramification/residue-degree factors, class-group obstructions, descent validity, and edge cases.
required_deliverable:
A list of proof breaks or a concise defense report. If a break is found, identify the exact claim and give a concrete stress-test example or missing lemma.
connection_to_target:
Ensures the proposed proof genuinely establishes the target for arbitrary `T/Q` and prime `p`.
where_used_in_final_solution:
Final quality gate before accepting or revising Main Solver's proof.
independence_constraint:
Do not construct an alternative proof unless needed to expose a flaw. Do not assume Main Solver's uncertain steps are valid.
failure_or_salvage_focus:
Prioritize attacks on CC003, CC004, CC005, and CC007, especially ramified induced tori, norm-one tori, anisotropic local cases, and hidden use of weak approximation.

10. Web-source confirmation

no web sources used.