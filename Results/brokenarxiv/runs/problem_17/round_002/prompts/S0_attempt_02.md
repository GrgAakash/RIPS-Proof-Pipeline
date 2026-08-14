Fresh no-history solver-only S0 run. Do not use web search, internet, external files, API keys, prior task history, memory, previous outputs, answer keys, or tools. Use only the mathematical problem statement supplied in this prompt, allowed support, current additional mathematical guidance below, and genuinely standard background that you explicitly name and state. This is fork_turns=none / fork_context=false.

Cleaned skeleton packet for this run:
A two-sorted ultrametric space is a structure consisting of a set of points X, a linearly ordered set of distances D_X with a least element 0, and a symmetric map d: X x X -> D_X such that d(x,y)=0 if and only if x=y, and d(x,z) <= max{d(x,y), d(y,z)}. A dc-embedding from X to Y consists of an injective map f: X -> Y and an order-preserving injection D_f: D_X -> D_Y preserving 0 such that d_Y(f(x),f(y)) = D_f(d_X(x,y)). Let U be the Fraisse limit of the class of all finite two-sorted ultrametric spaces with dc-embeddings. Target: Aut(U) has ample generics, meaning that for every integer n >= 1, Aut(U)^n has a comeager conjugacy class.

Allowed supporting statements:
Definitions, notation, and assumptions in the cleaned skeleton packet above are allowed. Genuinely standard background may be used only if it is named, stated precisely enough for use, and not equivalent to the target theorem. In particular, standard Fraisse-limit facts and standard Kechris-Rosendal/Hodges-Hodkinson-Lascar-Shelah criteria for ample generics may be used if stated; the required class-specific hypotheses for this target must be proved in the current proof. No statement equivalent to, stronger than, or logically downstream from the target theorem may be assumed.

Additional mathematical guidance:
1. Prove the finite ordered-distance amalgamation/equivariance lemma for arbitrary extensions of the prepared witness, or replace the preparation step with a stronger finite preparation that directly implies prepared-system amalgamation: for every finite n-system S in K_p^n, find a finite extension T such that any two finite extensions of T admit a finite linear ordered distance-sort amalgam where each union of corresponding distance partial maps is a well-defined order-preserving partial injection, and the min-max bridge distances over the base are equivariant under these partial maps.

----------------------------------------------------------------
S0 Blueprint Solver. Fresh no-internet chat.
----------------------------------------------------------------
You are S0, the Blueprint Solver. Your task is to create a proof blueprint for the target
theorem. Do not write the final proof.

You are given:
1. a cleaned skeleton PDF or TeX file;
2. the target theorem;
3. the Allowed supporting statements list;
4. the additional mathematical guidance list, if any.

Use only the supplied packet, the allowed supporting statements, the guidance list, genuinely
standard background, and facts that later subproblem solvers would need to prove inside the
current proof. Do not use external sources, web search, related writeups, unstated
task-specific facts, hidden lemmas, or any material not included in the provided packet.

If a guidance item is labeled `[INTERNALLY VERIFIED AUXILIARY RESULT E###]`, treat exactly its
stated lemma as established and available without reproof. Record E### as an additional-guidance
tool wherever it is used. Do not reconstruct its hidden branch proof or infer a stronger claim.

The blueprint is part of the current-round proof artifact. It may be inspected by verifiers,
but it is not carried into later Solver rounds.

Allowed supporting statements:
Definitions, notation, and assumptions in the cleaned skeleton packet above are allowed. Genuinely standard background may be used only if it is named, stated precisely enough for use, and not equivalent to the target theorem. In particular, standard Fraisse-limit facts and standard Kechris-Rosendal/Hodges-Hodkinson-Lascar-Shelah criteria for ample generics may be used if stated; the required class-specific hypotheses for this target must be proved in the current proof. No statement equivalent to, stronger than, or logically downstream from the target theorem may be assumed.

If required inputs are missing, stop and write "SETUP FAILURE: missing input." Then list the
missing input(s).

Produce exactly the following sections.

1. Target decomposition

target_label:
target_type:
main_goal:
variables_and_parameters:
conclusion_to_prove:

2. Available tools

For each planned tool:
tool:
source_status: provided definition / notation / assumption; allowed supporting statement;
additional guidance item; standard background fact; proved inside the current proof; or
unsupported or unclear.
exact_statement_or_fact:
intended_role_in_proof:

3. Subclaim support graph

Break the proof into 3-8 subclaims. For each:
id:
statement:
uses_prior_subclaims:
purpose:
status: follows from allowed statement / follows from guidance / standard background / must be
proved in final proof.
suggested_solver: S1 / S2 / S3 / S4 / S5.

4. Hardest step prediction

hardest_step_id:
hardest_step_description:
risk_if_wrong:
how_final_proof_should_handle_it:

5. Failure-mode checks

circularity_check:
full_theorem_check:
source_check:
hypothesis_check:
notation_check:
standard_background_check:

6. Subproblem assignment table

Assign S1-S5. Each assignment should be self-contained and should not require seeing any
source outside the supplied packet and this blueprint.

S1:
S2:
S3:
S4:
S5:

7. Web-source confirmation

Write "no web sources used", or list any unavoidable lookup that was explicitly permitted.

--- INPUTS FOR THIS RUN ---
Target theorem:
Let U be the Fraisse limit of the class of all finite two-sorted ultrametric spaces with dc-embeddings. Then Aut(U) has ample generics, meaning that for every integer n >= 1, Aut(U)^n has a comeager conjugacy class.

Additional mathematical guidance:
1. Prove the finite ordered-distance amalgamation/equivariance lemma for arbitrary extensions of the prepared witness, or replace the preparation step with a stronger finite preparation that directly implies prepared-system amalgamation: for every finite n-system S in K_p^n, find a finite extension T such that any two finite extensions of T admit a finite linear ordered distance-sort amalgam where each union of corresponding distance partial maps is a well-defined order-preserving partial injection, and the min-max bridge distances over the base are equivariant under these partial maps.