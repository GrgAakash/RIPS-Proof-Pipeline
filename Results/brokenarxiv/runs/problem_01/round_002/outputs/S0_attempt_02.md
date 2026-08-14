1. Target Decomposition

target_label: Problem 01

target_type: threshold theorem for persistent root leadership in percolated random recursive trees

main_goal: Prove that the probability `P(p)` of the root cluster remaining a largest cluster at every time has a nontrivial critical threshold.

variables_and_parameters: fixed `p in (0,1]`; random recursive tree grown from root `0`; each new edge retained independently with probability `p`; `P(p)` is the probability that no non-root cluster ever becomes strictly larger than the root cluster.

conclusion_to_prove: There exists `p_c in (0,1)` such that `P(p)=0` for `p<p_c` and `P(p)>0` for `p>p_c`.

2. Available Tools

tool: natural growth description
source_status: provided definition / notation / assumption
exact_statement_or_fact: At time `n`, vertex `n` attaches to a uniformly chosen parent in `{0,...,n-1}`, and the new edge is retained with probability `p`.
intended_role_in_proof: Gives Markovian cluster-size dynamics.

tool: tie convention
source_status: provided definition / notation / assumption
exact_statement_or_fact: Root-leadership failure occurs only when some non-root cluster becomes strictly larger than the root cluster; ties are allowed.
intended_role_in_proof: Determines absorbing failure boundary for deficit process.

tool: cluster size transition rule
source_status: standard background fact
exact_statement_or_fact: Conditional on current cluster sizes, the next vertex joins a cluster of size `s` with probability `s/(n+1)` if its edge is retained, and otherwise starts a singleton challenger cluster.
intended_role_in_proof: Converts percolation growth into a preferential-attachment urn/branching-style process.

tool: deficit/challenger process theorem
source_status: proved inside the current proof
exact_statement_or_fact: For a Markov process tracking the root size and all challenger deficits `D_i(n)=R(n)-C_i(n)`, there is a parameter-dependent criterion separating almost-sure eventual strict overtake from positive-probability eternal non-overtake.
intended_role_in_proof: Main engine proving small-`p` failure and large-`p` success.

tool: monotone threshold definition
source_status: proved inside the current proof
exact_statement_or_fact: The set `{p: P(p)>0}` is an upper interval once the deficit/challenger criterion is written in terms of a parameter monotone in `p`.
intended_role_in_proof: Allows definition of `p_c := inf {p: P(p)>0}` and proves the zero/positive dichotomy away from `p_c`.

tool: small-`p` failure
source_status: proved inside the current proof
exact_statement_or_fact: For sufficiently small `p>0`, with probability one some challenger eventually becomes strictly larger than the root cluster.
intended_role_in_proof: Shows `p_c>0`.

tool: large-`p` success
source_status: proved inside the current proof
exact_statement_or_fact: For sufficiently large `p<1`, with positive probability the root cluster is never strictly overtaken.
intended_role_in_proof: Shows `p_c<1`.

3. Subclaim Support Graph

id: S1
statement: Derive the exact cluster-size dynamics: conditional on current cluster sizes, a cluster of size `s` receives the new vertex with probability `p s/(n+1)`, while with probability `1-p` the new vertex starts a new singleton cluster.
uses_prior_subclaims: none
purpose: Establishes the stochastic process to be analyzed.
status: standard background / must be proved in final proof
suggested_solver: S1

id: S2
statement: Reformulate root leadership as survival of a deficit process: if `R(n)` is the root-cluster size and `C_i(n)` are challenger sizes, success is exactly the event `C_i(n) <= R(n)` for all challengers `i` and all times `n`.
uses_prior_subclaims: S1
purpose: Encodes the strict-loss/tie convention correctly.
status: must be proved in final proof
suggested_solver: S2

id: S3
statement: Prove a deficit/challenger criterion: there exists a monotone parameter function `theta(p)` and a critical value `theta_*` such that the deficit process survives with positive probability when `theta(p)>theta_*`, and dies almost surely when `theta(p)<theta_*`.
uses_prior_subclaims: S1, S2
purpose: Supplies the central extinction/survival theorem required by the guidance.
status: must be proved in final proof
suggested_solver: S3

id: S4
statement: Prove small-`p` failure: for all sufficiently small `p`, the root grows too slowly relative to the accumulating challenger population, so some challenger strictly overtakes the root almost surely.
uses_prior_subclaims: S3
purpose: Establishes `P(p)=0` on a nonempty initial interval.
status: must be proved in final proof
suggested_solver: S4

id: S5
statement: Prove large-`p` success: for all sufficiently large `p<1`, with positive probability early root growth creates enough permanent advantage that every challenger remains at most tied with the root forever.
uses_prior_subclaims: S3
purpose: Establishes `P(p)>0` on a nonempty terminal interval.
status: must be proved in final proof
suggested_solver: S5

id: S6
statement: Define `p_c := inf {p in (0,1): P(p)>0}` and use the monotone criterion to prove `P(p)=0` for `p<p_c` and `P(p)>0` for `p>p_c`.
uses_prior_subclaims: S3, S4, S5
purpose: Converts the criterion into the claimed critical probability.
status: must be proved in final proof
suggested_solver: S3

4. Hardest Step Prediction

hardest_step_id: S3

hardest_step_description: Proving the deficit/challenger extinction/survival criterion rigorously, rather than assuming a branching-process comparison. The proof must handle infinitely many challenger clusters born over time and the fact that ties with the root are allowed.

risk_if_wrong: If the criterion is only heuristic, or if it treats ties as failures, the final threshold statement may be circular or prove the wrong event.

how_final_proof_should_handle_it: Build an explicit Markov domination/embedded process. Show one-sided bounds: below the critical parameter, infinitely many challenger opportunities force strict overtake almost surely; above it, construct a positive-probability event on which root increments dominate all challenger increments uniformly. Prove all couplings and boundary conventions directly.

5. Failure-Mode Checks

circularity_check: Do not assume the target threshold theorem or any equivalent monotonicity of `P(p)`; monotonicity must come from the proved deficit criterion.

full_theorem_check: The proof must show both `p_c>0` and `p_c<1`, not merely define a formal threshold.

source_check: No external percolation results specific to recursive trees may be invoked unless proved inside the current proof.

hypothesis_check: Keep `p in (0,1]`; the theorem only needs the threshold inside `(0,1)`, with positivity for all `p>p_c`.

notation_check: Clearly distinguish root size `R(n)`, challenger sizes `C_i(n)`, deficits `D_i(n)=R(n)-C_i(n)`, and strict failure `C_i(n)>R(n)`.

standard_background_check: Standard martingale, coupling, urn-process, Borel-Cantelli, and elementary branching-process facts may be used only in generic form; any model-specific criterion must be proved.

6. Subproblem Assignment Table

S1: Derive the conditional cluster-size transition law from the recursive-tree growth rule and retained/deleted edge coin flip. State it as a Markov chain on the multiset of cluster sizes with one distinguished root cluster.

S2: Formalize the success event using deficits. Prove that root remains a largest cluster at every time exactly when all challenger deficits remain nonnegative for all times, allowing zero deficits as ties.

S3: Prove the central deficit/challenger theorem. The theorem should give a parameter-dependent survival/extinction criterion, prove the criterion from the transition law, and show that the favorable parameter region is monotone in `p`.

S4: Use the deficit theorem to prove small-`p` failure. Give explicit constants or inequalities showing that for some `epsilon>0`, all `p<epsilon` fall in the almost-sure extinction/overtake regime.

S5: Use the deficit theorem to prove large-`p` success. Give explicit constants or inequalities showing that for some `eta<1`, all `p>eta` have positive probability of eternal root non-overtake.

7. Web-Source Confirmation

no web sources used