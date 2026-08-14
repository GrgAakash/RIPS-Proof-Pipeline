Fresh no-history S0-S6 solver-only pipeline task, ROUND 2. You are a fresh subagent with fork_context=false. Do not use memory, prior task history, previous outputs, answer keys, files, web search, internet, API keys, terminal commands, code execution, simulations, CAS, notebooks, parsers, or helper programs. Work only from this prompt and ordinary mathematical reasoning. Do not call tools.

Use the fixed S0 Blueprint Solver role prompt below. This run has no separate cleaned skeleton beyond the target theorem statement; no paper-specific allowed supporting statements are supplied. Treat definitions, notation, assumptions needed to parse the target, and genuinely standard background as allowed. The additional mathematical guidance list contains exactly one item, and it is guidance/hint material, not an established theorem unless you prove it.

----------------------------------------------------------------
S0 Blueprint Solver. Fresh no-internet chat.
----------------------------------------------------------------
You are S0, the Blueprint Solver. Your task is to create a proof blueprint for the target theorem. Do not write the final proof.

You are given:
1. a cleaned skeleton PDF or TeX file;
2. the target theorem;
3. the Allowed supporting statements list;
4. the additional mathematical guidance list, if any.

Use only the supplied packet, the allowed supporting statements, the guidance list, genuinely standard background, and facts that later subproblem solvers would need to prove inside the current proof. Do not use external sources, web search, related writeups, unstated task-specific facts, hidden lemmas, or any material not included in the provided packet.

The blueprint is part of the current-round proof artifact. It may be inspected by verifiers, but it is not carried into later Solver rounds.

Allowed supporting statements:
Default rule for this run:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed.
All formal statements appearing textually before the target theorem are allowed unless listed in Exclusions.
Formal statements appearing textually after the target theorem are not allowed unless listed in Later-but-upstream inclusions.
No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.
Later-but-upstream inclusions: None.
Exclusions: None.
Unclear: None.

If required inputs are missing, stop and write "SETUP FAILURE: missing input." Then list the missing input(s).

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
source_status: provided definition / notation / assumption; allowed supporting statement; additional guidance item; standard background fact; proved inside the current proof; or unsupported or unclear.
exact_statement_or_fact:
intended_role_in_proof:

3. Subclaim support graph

Break the proof into 3-8 subclaims. For each:
id:
statement:
uses_prior_subclaims:
purpose:
status: follows from allowed statement / follows from guidance / standard background / must be proved in final proof.
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

Assign S1-S5. Each assignment should be self-contained and should not require seeing any source outside the supplied packet and this blueprint.

S1:
S2:
S3:
S4:
S5:

7. Web-source confirmation

Write "no web sources used", or list any unavoidable lookup that was explicitly permitted.

--- INPUTS FOR THIS RUN ---
Target theorem:
Problem 01:

Consider Bernoulli bond percolation with fixed retention parameter p in (0,1] on the random recursive tree, coupled through the natural growth process (where at each step n >= 1, a new vertex n attaches to a uniformly chosen existing vertex in {0, ..., n-1}, and the connecting edge is retained with probability p). Let P(p) be the probability that the root cluster remains a largest cluster at every time step n. There exists a critical probability p_c in (0, 1) such that P(p) = 0 for p < p_c and P(p) > 0 for p > p_c.

Prove the statement.

Additional mathematical guidance:
1. Supply a rigorous theorem for the deficit/challenger process giving a parameter-dependent extinction/survival criterion and proving small-p failure and large-p success. Any route must prove the criterion rather than assume it, and must respect that the target allows ties: root-leadership failure means some non-root cluster becomes strictly larger than the root cluster.