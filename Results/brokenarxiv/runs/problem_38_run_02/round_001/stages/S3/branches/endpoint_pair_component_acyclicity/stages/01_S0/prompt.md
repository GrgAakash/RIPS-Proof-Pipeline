You are running as a fresh no-history solver subagent for a branch lemma. Do not use web search, internet, API keys, memory, prior task history, previous outputs, files, code execution, terminal commands, CAS tools, simulations, notebooks, or helper programs. Use only the mathematical content in this prompt and standard background.

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

Allowed supporting statements:
None. Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. No formal supporting statement may be cited without proof. Genuinely standard background facts may be used only when explicitly named and stated.

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
Branch Lemma E001 candidate. Let C_1,...,C_n be pairwise disjoint open convex subsets of R^d, with n >= 2, and fix an ordering sigma of {1,...,n}. Let D_sigma be the set of u in S^{d-1} for which there exists an oriented line with direction u meeting C_{sigma(1)},...,C_{sigma(n)} in that order. Then every connected component of D_sigma is acyclic, i.e. has trivial reduced homology.

Additional mathematical guidance:
None

Cleaned skeleton packet:
The target statement above is the full supplied packet. There are no additional definitions, lemmas, propositions, or allowed supporting statements.