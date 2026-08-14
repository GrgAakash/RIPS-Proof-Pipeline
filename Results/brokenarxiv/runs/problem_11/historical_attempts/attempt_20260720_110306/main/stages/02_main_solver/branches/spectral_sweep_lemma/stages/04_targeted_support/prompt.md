Fresh no-history solver-only branch experiment. Do not use memory, prior task history, previous outputs outside this prompt, answer keys, files outside this prompt, web search/internet, API keys, or Python. You are branch SS3. This is a no-internet Dynamic Worker Solver run as a checking-mode Midfielder for an assigned subclaim only. Follow the latest Dynamic Worker Solver structure: produce sections 1-6; solve only assigned subclaim; do not write the full target proof.

Allowed supporting statements: definitions and standard finite integral/sum manipulations only. No external sources or theorem recall.

--- INPUTS FOR THIS BRANCH RUN ---
Assigned subproblem:
SS3:
role: midfielder
work_scope: assigned_subclaim
assigned_subclaim_ids: CC003
task: Expectation-blind check of the following standalone inequality. Let y >= 0 be a finite vector, S_t={v:y_v>=t}, n(t)=|S_t|, so n is nonincreasing and 0 <= n(t) <= N. Let D>0. Determine whether there is an absolute constant K such that
  2 ∫_0^∞ ∫_0^t min{n(s)n(t), 2D n(s)^{3/2}} ds dt <= K D sqrt(N) ∫_0^∞ 2t n(t) dt
for all such threshold functions arising from finite vectors.
required_deliverable: A self-contained PASS/BLOCK report for the inequality, including the exact constant if proven or the precise failing configuration if not.
connection_to_target: This is a closure estimate converting a layer-cake quadratic form bound into a Rayleigh quotient bound, but do not assume any desired result.
where_used_in_final_solution: Used only to discharge CC003.
independence_constraint: Do not assume Main Solver's conclusion or desired answer; evaluate the inequality on its own terms.
failure_or_salvage_focus: If the displayed bound is false, identify whether a nearby bound with modified constant, split, or hypothesis remains usable.

Target lemma context (for notation only): There is an absolute C such that lambda(H)<=C sqrt(N)d_{3/2}(H). You are not proving this full lemma.

Additional mathematical guidance: None.