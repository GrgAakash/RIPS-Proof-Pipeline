Fresh no-history solver-only branch experiment. Do not use memory, prior task history, previous outputs outside this prompt, answer keys, files outside this prompt, web search/internet, API keys, or Python. This is a no-internet Manager Acceptance run for the auxiliary branch lemma. Use the latest Manager Acceptance prompt from `pipeline_sources/Prompt Packet/Prompts.md`: decide whether Main Solver's complete proof can be accepted and packaged. Preserve Main Solver's proof as the only complete proof candidate; do not repair/rewrite it. Use active support outputs as audit context only. Acceptance requires Main Solver proof key and Manager acceptance key, every critical claim established, and no undischarged Defender block.

Produce sections:
1. Composition map, including critical-claim discharge table and blocking challenge discharge records if any
2. Main Solver authorship and proof-reference audit
3. Manager failure output and candidate guidance YAML including answer_status, candidate_basis, manager_acceptance_key, main_solver_id, proof packaging controls
4. Source Ledger inside markers
5. Background and Assumptions Manifest inside markers
6. Completion checklist inside markers
7. Web-source confirmation inside markers

--- INPUTS FOR THIS BRANCH RUN ---
Cleaned skeleton/packet:
Standalone auxiliary lemma packet only. It contains target lemma and definitions: spectral radius of adjacency matrix, induced edge count e(H[S]), and d_{3/2}(H)=max e(H[S])/|S|^{3/2}. No prior theorem/proof content.

Target lemma:
There is an absolute constant C>0 such that every N-vertex graph H with at least one edge satisfies lambda(H) <= C sqrt(N) d_{3/2}(H).

Additional mathematical guidance: None.

Manager routing plan:
SS1 Main Solver assigned full proof. SS2 Defender attacks final proof. Critical claims:
CC001: Bounding |x^TA_Hx| for all real x by B||x||_2^2 suffices to bound adjacency spectral radius by B.
CC002: Nested threshold incidence bound must be correctly derived from induced e(S)<=D|S|^{3/2}; watch ordered/unordered factors.
CC003: Threshold/integral closure must produce O(sqrt(N)||x||_2^2) with no log loss.

Active worker outputs:
SS3 support history: Earlier support blocked SS1's first arbitrary-D integral inequality with a concrete analytic counterexample for D=1/(2sqrt N). Support admission admitted this as a warning only because graph D=d_{3/2}(H)>=2^{-3/2}. SS1's repaired proof does not use the invalid arbitrary-D estimate.

SS1 Main Solver integrated proof:
Main Solver says solved. It did not use web/Python. Treat `target_status: solved` and proof text below as Main Solver's proof key; if strict key parsing matters, record any key-format caveat honestly.

[BEGIN FINAL PROOF BODY: SS1-proof-v1]
Let D=d_{3/2}(H). Since H has an edge, taking its two endpoints gives D>=1/2^{3/2}.
Let A be the adjacency matrix. Since A is nonnegative, the Rayleigh quotient may be tested on nonnegative vectors: for any real x, x^TAx<=|x|^TA|x|. So fix y>=0. For t>=0, define S_t={v:y_v>t}, n(t)=|S_t|. For s,t>=0, let M(s,t) be the number of ordered adjacent pairs (u,v) with u in S_s and v in S_t. Layer cake gives
 y^TAy=∫_0∞∫_0∞ M(s,t) ds dt =2∫_0∞∫_0^t M(s,t) ds dt.
Nested-set edge bound. If T subseteq S, |T|=b, |S|=a, then ordered edge incidences from S to T are at most 6D a sqrt b. If a<=2b, count <=2e(H[S])<=2Da^{3/2}<=2sqrt2 Da sqrt b. If a>2b, choose uniformly b-set R subset S\T. Since every T∪R has size 2b, e(H[T∪R])<=D(2b)^{3/2}. Averaging over R gives e(T)+b/(a-b)e(T,S\T)<=D(2b)^{3/2}, so e(T,S\T)<=2^{3/2}Da sqrt b. Together with e(T)<=Db^{3/2}, ordered incidence count <=6Da sqrt b.
Applying with T=S_t subseteq S_s=S for s<=t, M(s,t)<=6D n(s)sqrt{n(t)}. Hence
 y^TAy<=12D∫_0∞ sqrt{n(t)}(∫_0^t n(s)ds)dt.
Hardy threshold lemma: If n(t) is a decreasing threshold-count function with 0<=n(t)<=N, then
 ∫_0∞ sqrt{n(t)}(∫_0^t n(s)ds)dt <= 9sqrt N∫_0∞ t n(t)dt.
Proof: Put f=n/N, g=sqrt f, L=∫_0∞ t g(t)^2dt. Need ∫ g(t)∫_0^t g(s)^2dsdt <=9L. Let tau(a)=|{t:g(t)>a}|, 0<a<=1. Then L=∫_0^1 a tau(a)^2 da. Expanding both g(s)^2 and g(t) by layer cake gives two regions. Region a<b contributes <=1/2∫_0^1 a^2tau(a)^2da<=1/2L. Region b<a contributes 2∫_0^1 a tau(a)(∫_0^a tau(b)db)da. The weighted Hardy inequality for decreasing functions, ∫_0^1 a h(a)(∫_0^a h(b)db)da <=4∫_0^1 a h(a)^2da, applied to h=tau, bounds this by 8L. This proves the lemma.
Finally ∫_0∞ t n(t)dt=1/2 sum_v y_v^2=1/2||y||_2^2. Thus y^TAy<=12D*9sqrtN*1/2||y||_2^2=54DsqrtN||y||_2^2. Taking supremum over nonzero y>=0, lambda(H)<=54DsqrtN. So the target lemma holds with C=54.
[END FINAL PROOF BODY]

SS1 YAML summary: target_status solved; candidate guidance only says Defender should check nested-set sampling and Hardy threshold lemma; critical claims CC001 proved, CC002 repaired/proved, CC003 replaced by Hardy closure.

SS2 Defender output:
Role completed. Defender verdict PASS, blocks_acceptance false. Attacked CC001, CC002, CC003, stress tests, source classification. Findings: no unresolved challenge. It audited spectral reduction, nested threshold incidence bound, and Hardy threshold closure as held. Stress tests on stars, complete graphs, complete bipartite graphs, and one-edge-plus-isolates consistent. Local Source Ledger classifies spectral theorem as standard background, nested-set sampling as derived, threshold Hardy inequality as derived/current audit with standard layer-cake identities. No new critical claims. Web-source confirmation: no web sources used.