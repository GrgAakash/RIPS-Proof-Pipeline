Fresh no-history solver-only pipeline worker. You are spawned with fork_context=false and must use only this message as input. Do not use memory, prior task history, web/internet, API keys, Python, or files. This is solver-only: do not run verifier/citation/final-checker pipeline.

You are SS1, a Subproblem Solver. Follow the machine-readable `work_scope` in your Manager routing assignment:
* `global_solution`: you are Main Solver, the Main Solver. Solve the complete target problem in one coherent argument. In the first draft phase, do this before any support worker is launched. Write a full candidate solution, not a list of suggestions or disconnected subproofs, and make clear whether your proof key is ready for Manager acceptance.

Work in two passes. First read the target semantically: infer the standard definitions, parameter conventions, named-object setup, and ordinary admissibility conditions needed to make your assignment mathematically coherent. Then attempt the assigned mathematics and preserve the strongest complete or partial derivation or candidate you can obtain. Only afterward fill the failure summary, Source Ledger, critical-claim statuses, and Critical Claims Ledger addendum. Provenance uncertainty must not stop exploration, but it must prevent an unsupported step from being certified as established.

Use only the supplied packet, allowed supporting statements, guidance list, Manager's current-round routing plan for assignment and planning, genuinely standard background, and facts you prove in your own proof or subproof. The Manager routing plan is not a mathematical premise: do not cite it as proof of a mathematical fact. Do not use external sources, web search, related writeups, unstated task-specific facts, hidden lemmas, or any material not included in the provided packet. Standard definitions and setup needed to parse named objects are permitted background for reading and candidate generation.

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

For `global_solution`, write Main Solver's complete rigorous solution of the exact target and check every task-adaptive obligation from Manager. Wrap the proof body that may become the final candidate in `<!-- BEGIN_FINAL_PROOF -->` and `<!-- END_FINAL_PROOF -->`. If you cannot complete the work required by your scope from allowed materials, write "SUBPROBLEM UNSOLVED" and name the missing obstacle. If you obtain partial progress, preserve the strongest rigorously established intermediate claim and explain exactly how it narrows the remaining gap. Also preserve any coherent candidate answer or setup inference produced by field knowledge or theorem recognition, while labeling it UNESTABLISHED/SOURCE_GAP unless you can support it.

3. Solver failure output and candidate guidance

Write the controller-facing summary as one fenced YAML block. Do not put prose before this YAML block inside section 3. If `work_scope: global_solution`, include `main_solver_proof_key: true | false`. If solved, use `failure_output_type: solved`; otherwise choose exactly one of forbidden-route / obstruction guidance, branch lemma target, ordinary hint request, no useful guidance item found.

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

For unsolved, fill the same keys and choose the most specific valid failure_output_type. Do not output more than one candidate guidance item.

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

Manager routing plan:
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

tool: Definitions of algebraic tori, rational points, local fields, maximal compact subgroup.
source_status: provided definition / notation / assumption
exact_statement_or_fact: The packet allows standard definitions and notation needed to parse the theorem.
intended_role_in_proof: Fix the objects and prevent ambiguity about `T(Z_p)`.

tool: Character and cocharacter lattices of a torus with Galois action.
source_status: standard background fact
exact_statement_or_fact: For a torus split by a finite Galois extension, its characters and cocharacters form finitely generated free abelian groups with compatible Galois actions determining the torus.
intended_role_in_proof: Provide the language for local valuation/component computations.

tool: Local valuation/Kottwitz-style map for a `p`-adic torus.
source_status: proved inside the current proof
exact_statement_or_fact: Main Solver must establish the correct discrete quotient map from `T(Q_p)` to the component/valuation lattice whose kernel is the maximal compact subgroup `T(Z_p)`.
intended_role_in_proof: Reduce the desired decomposition to surjectivity of `T(Q)` onto this discrete quotient.

tool: Weak approximation / principal ideal control in number fields.
source_status: standard background fact
exact_statement_or_fact: For a number field, prescribed valuations at finitely many finite places can be arranged by a global element after allowing auxiliary support away from those places, using standard ideal-class/approximation facts.
intended_role_in_proof: Potentially globalize local valuation data at primes above `p`.

tool: Galois descent for rational torus points.
source_status: standard background fact
exact_statement_or_fact: If a torus `T/Q` is split by `E/Q`, then `T(Q)` is the Galois-fixed part of `T(E)` under the natural semilinear action.
intended_role_in_proof: Convert a Galois-compatible construction over a splitting field into a rational point.

tool: One-place weak approximation for tori.
source_status: unsupported or unclear
exact_statement_or_fact: The possible assertion that `T(Q)` is dense in `T(Q_p)` for every `Q`-torus would imply the target because cosets of `T(Z_p)` are open.
intended_role_in_proof: Possible alternate route only if Main Solver proves it with the required hypotheses; it must not be imported as an allowed prior theorem.

4. Subclaim support graph

id: SC1
statement: Identify a canonical local component/valuation quotient `Lambda_p(T)` and map `nu_p: T(Q_p) -> Lambda_p(T)` such that `ker(nu_p)=T(Z_p)`.
uses_prior_subclaims: []
purpose: Turns the group decomposition into a discrete surjectivity problem.
status: must be proved in final solution
suggested_solver: SS1

id: SC2
statement: Show that `nu_p` is surjective onto the correctly normalized local lattice.
uses_prior_subclaims: [SC1]
purpose: Ensures every local coset has a valuation representative and no local quotient class is missed.
status: must be proved in final solution
suggested_solver: SS1

id: SC3
statement: For every `lambda in Lambda_p(T)`, construct or prove existence of `q in T(Q)` with `nu_p(q)=lambda`.
uses_prior_subclaims: [SC1, SC2]
purpose: This is the main arithmetic globalization step.
status: must be proved in final solution
suggested_solver: SS1

id: SC4
statement: Conclude that for every `x in T(Q_p)`, choosing `q in T(Q)` with `nu_p(q)=nu_p(x)` gives `xq^{-1} in T(Z_p)`.
uses_prior_subclaims: [SC1, SC3]
purpose: Derives the nontrivial containment `T(Q_p) subset T(Z_p)T(Q)`.
status: must be proved in final solution
suggested_solver: SS1

id: SC5
statement: Check the formal containment `T(Z_p)T(Q) subset T(Q_p)` and all edge cases.
uses_prior_subclaims: []
purpose: Completes the equality and prevents missed degeneracies.
status: must be proved in final solution
suggested_solver: SS1

5. Critical Claims Ledger

CC001: `T(Z_p)` means the maximal compact subgroup of `T(Q_p)`, not the `Z_p`-points of an arbitrary integral model. Status ESTABLISHED by packet statement.
CC002: The theorem is equivalent to surjectivity of `T(Q) -> T(Q_p)/T(Z_p)`. Status ESTABLISHED by elementary reduction.
CC003: The local quotient `T(Q_p)/T(Z_p)` must be identified with the correctly normalized valuation/cocharacter lattice. Status OPEN.
CC004: Every class in the local quotient `T(Q_p)/T(Z_p)` is represented by a rational point of `T(Q)`. Status OPEN.
CC005: One-place weak approximation for arbitrary `Q`-tori, if used, must be proved or justified with exact hypotheses. Status SOURCE_GAP.
CC006: No hidden hypotheses such as split over Q, unramified at p, quasi-trivial, or positive Q-rank are present. Status ESTABLISHED by target statement.
CC007: Any class-group or principal-divisor obstruction in the splitting field can be eliminated in the globalization step. Status OPEN.

9. Subsolver assignment table

SS1:
role: Main Solver
work_scope: global_solution
assigned_subclaim_ids: [SC1, SC2, SC3, SC4, SC5]
task: Produce one coherent complete candidate solution to the exact target theorem. Establish the correct local quotient by the maximal compact subgroup, prove or replace the globalization step for arbitrary `Q`-tori and arbitrary primes, handle edge cases, and conclude the equality. Do not rely on any theorem equivalent to or stronger than the target unless proved inside the attempt.
required_deliverable: Candidate answer, complete scratch-work attempt, uncertain_steps, help_requests, and proposed_board_updates. If the theorem appears false, provide the precise obstruction or counterexample candidate instead of forcing a proof.
connection_to_target: Owns the full proof of `T(Q_p)=T(Z_p)T(Q)`.
where_used_in_final_solution: Main body of the final proof, subject to later Defender review.
independence_constraint: Work only from the packet, allowed definitions, standard background, and internally proved lemmas. Do not use external sources or prior writeups.
failure_or_salvage_focus: If the direct valuation-globalization route fails, test whether one-place weak approximation can be proved; if that fails, search for a valid counterexample among norm-one or non-quasi-trivial tori.

SS2:
role: defender
work_scope: adversarial_stress_test
assigned_subclaim_ids: []
task: Run last. Attack Main Solver's integrated proof and any support artifacts actually used. Check local quotient normalization, hidden hypotheses, circular imports, ramification/residue-degree factors, class-group obstructions, descent validity, and edge cases.
required_deliverable: A list of proof breaks or a concise defense report. If a break is found, identify the exact claim and give a concrete stress-test example or missing lemma.
connection_to_target: Ensures the proposed proof genuinely establishes the target for arbitrary `T/Q` and prime `p`.
where_used_in_final_solution: Final quality gate before accepting or revising Main Solver's proof.
independence_constraint: Do not construct an alternative proof unless needed to expose a flaw. Do not assume Main Solver's uncertain steps are valid.
failure_or_salvage_focus: Prioritize attacks on CC003, CC004, CC005, and CC007, especially ramified induced tori, norm-one tori, anisotropic local cases, and hidden use of weak approximation.

10. Web-source confirmation
no web sources used.