Fresh no-history solver-only branch experiment. Do not use memory, prior task history, previous outputs outside this prompt, answer keys, files outside this prompt, web search/internet, API keys, or Python. This is a no-internet Manager Assistance Routing run after branch Main Solver's first draft. Use the latest Manager Assistance Routing prompt structure from `pipeline_sources/Prompt Packet/Prompts.md`. Controller limits: branch depth 1 of max 2; max_support_items_total remaining=2; max_specialist_batches_per_round=2.

You are the Manager in the assistance-routing phase. Read Main Solver's first complete-proof attempt and decide whether bounded assistance is justified. Do not solve the mathematics yourself. Add a Midfielder only for one concrete bottleneck or one expectation-blind checking assignment; add no agents for broad reassurance. Keep SS1 Main Solver and SS2 Defender from the initial branch plan.

Produce exactly sections: 1. Post-Main Solver assessment; 5. Critical Claims Ledger; 8. Subsolver execution plan; 9. Subsolver assignment table; 10. Web-source confirmation.

--- INPUTS FOR THIS BRANCH RUN ---
Target lemma:
There is an absolute constant C>0 such that every N-vertex graph H with at least one edge satisfies lambda(H) <= C sqrt(N) d_{3/2}(H), where d_{3/2}(H)=max_{nonempty S subseteq V(H)} e(H[S]) / |S|^{3/2}.

Additional mathematical guidance:
None

Initial branch Manager routing plan:
SS1 Main Solver assigned SC1-SC5: reduce to quadratic-form/nonnegative vector; threshold layer-cake; nested threshold edge control; integral closure O(sqrt(N)||x||_2^2); Rayleigh conclusion. SS2 Defender runs last. Critical claims: CC001 real Rayleigh/operator norm reduction; CC002 ordered edge count for nested threshold sets; CC003 threshold integral closure with no logarithmic loss.

Branch Main Solver draft:
1. Assignment restatement: SS1 global solution for lambda(H)<=C sqrt(N)d_{3/2}(H).

2. Subproof:
Let D=d_{3/2}(H)>0. For real x, y=|x| gives |x^TAx|<=y^TAy, so y>=0. Define S_t={v:y_v>=t}, n(t)=|S_t|. Let M(s,t) be ordered edge count between S_s and S_t. Layer cake gives y^TAy=int int M(s,t) ds dt. Bounds: M(s,t)<=n(s)n(t); if s<=t then S_t subset S_s, every counted ordered edge has endpoints in S_s, so M(s,t)<=2e(H[S_s])<=2D n(s)^{3/2}; symmetric on other half. Therefore
 y^TAy <= 2 int_0^infty int_0^t min{n(s)n(t), 2D n(s)^{3/2}} ds dt.
Then SS1 states a finite integral estimate: for nonincreasing step n from y,
 2 int_0^infty int_0^t min{n(s)n(t),2D n(s)^{3/2}} ds dt <= 16D sqrt(N) int_0^infty 2t n(t)dt.
It says this follows by splitting inner integral according to whether n(t)<=4D^2 or n(t)>4D^2, using product bound in first range and induced-edge bound in second, monotonicity and distribution identities, after summing threshold intervals. It gives no detailed summation.
Conclusion: |x^TAx|<=16D sqrt(N)||x||_2^2; lambda<=16 sqrt(N)D. YAML solved, main_solver_proof_key true. Risk point: finite integral closure CC003.

Your task:
Decide whether to add a support worker. If yes, make the assignment narrow and self-contained, preferably expectation-blind if it is a pure inequality check. The support worker may see the inequality and definitions but should not be told the desired answer if checking-mode is chosen.