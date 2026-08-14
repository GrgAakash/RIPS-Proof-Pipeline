Fresh no-history solver-only branch experiment. Do not use memory, prior task history, previous outputs outside this prompt, answer keys, files outside this prompt, web search/internet, API keys, or Python. You are branch SS1. This is a no-internet Dynamic Worker Solver integration/repair phase. Follow the latest Dynamic Worker Solver prompt: as Main Solver with work_scope global_solution, produce a complete branch proof if possible; consider only Manager-approved support below; do not use unsupported black-box estimates.

Required output sections:
1. Assignment restatement
2. Subproof or failure, with final proof body wrapped if solved
3. Solver failure output and candidate guidance YAML with standard keys and main_solver_proof_key
4. Local Source Ledger and critical claim statuses/addendum
5. Interface notes
6. Web-source confirmation

--- INPUTS FOR THIS BRANCH RUN ---
Target lemma:
There is an absolute constant C>0 such that every N-vertex graph H with at least one edge satisfies lambda(H) <= C sqrt(N) d_{3/2}(H), where d_{3/2}(H)=max_{nonempty S subseteq V(H)} e(H[S]) / |S|^{3/2}.

Additional mathematical guidance: None.

Branch routing summary:
SS1 is Main Solver. SS2 Defender runs last. Critical claims: CC001 Rayleigh/operator norm reduction; CC002 ordered edge count for nested threshold sets; CC003 threshold integral closure with no logarithmic loss.

Your prior draft:
You reduced to nonnegative y, thresholds S_t, n(t), ordered M(s,t), layer-cake y^TAy=int int M. You used M(s,t)<=n(s)n(t) and for s<=t, M(s,t)<=2D n(s)^{3/2}. You then asserted
  2∫_0∞∫_0^t min{n(s)n(t),2D n(s)^{3/2}} dsdt <=16D√N∫_0∞2t n(t)dt.

Approved support/admission:
SS3 correctly identifies that the displayed threshold integral estimate is false as a purely analytic statement for arbitrary positive D. Counterexample: N=m, y=(1,m^{-1/2},...,m^{-1/2}), D=1/(2√m), giving LHS about 2√m while D√N∫2tn(t)dt is O(1). This is admissible as a warning against your proof as written.
However, SS3's counterexample uses D below the graph-forced lower bound: in the actual graph setting with H having at least one edge and D=d_{3/2}(H), D>=2^{-3/2}. Therefore SS3 does not disprove the graph lemma. The Manager-approved board update is:
CC003: Main Solver's displayed integral estimate is false in the stated arbitrary-D analytic form. Need repair or reprove the closure with D=d_{3/2}(H), N fixed, and the edge-forced lower bound D>=2^{-3/2} included, or replace the threshold closure step.

Your task:
Repair the branch proof if possible. You may use the graph-forced lower bound D>=2^{-3/2}; if you use a threshold/integral inequality, prove it fully under the actual hypotheses. If you cannot, output incomplete with one autonomy-safe guidance item or clean branch lemma target.