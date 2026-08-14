Fresh no-history solver-only branch experiment. Do not use memory, prior task history, previous outputs outside this prompt, answer keys, files outside this prompt, web search/internet, API keys, or Python. You are branch SS2, Defender. This is a no-internet Defender run after Main Solver. Use the latest Defender prompt from `pipeline_sources/Prompt Packet/Prompts.md`: attack Main Solver's integrated proof and support artifacts; never choose final answer; verdict can block acceptance. Use only supplied packet, allowed definitions, guidance, standard background, and computations you carry out yourself.

Produce exactly sections:
1. Attack inventory
2. Findings
3. Defender verdict as fenced YAML with keys role_task_status, defender_verdict, blocks_acceptance, audits, attacked_claims, challenged_claim_ids, competing_candidates, obstruction, required_resolution, source_gap, external_material_status, autonomous_derivation_possible, candidate_lemma_statement, why_unblocks, where_used, allowed_inputs, dependencies, weaker_than_target, equivalent_or_stronger, recommended
4. Role-completion summary YAML with standard Dynamic Solver solved keys
5. Local Source Ledger
6. Web-source confirmation

--- INPUTS FOR THIS BRANCH RUN ---
Cleaned skeleton/packet:
Standalone auxiliary lemma packet only. It contains target lemma and definitions: spectral radius of adjacency matrix, induced edge count e(H[S]), and d_{3/2}(H)=max e(H[S])/|S|^{3/2}. No prior theorem/proof content.

Target lemma:
There is an absolute constant C>0 such that every N-vertex graph H with at least one edge satisfies lambda(H) <= C sqrt(N) d_{3/2}(H).

Additional mathematical guidance: None.

Branch Manager routing plan:
SS1 Main Solver assigned full proof. SS2 Defender attacks final proof. Critical claims:
CC001: Bounding |x^TA_Hx| for all real x by B||x||_2^2 suffices to bound adjacency spectral radius by B; resolution via symmetry/nonnegative reduction.
CC002: Nested threshold edge/count or incidence bound must be correctly derived from induced e(S)<=D|S|^{3/2}; watch ordered/unordered factors.
CC003: Threshold/integral closure must produce O(sqrt(N)||x||_2^2) with no log loss; previous arbitrary-D estimate was blocked by SS3 and replaced.

Support artifacts:
SS3 support blocked SS1's earlier arbitrary-D integral inequality with a concrete analytic counterexample for D=1/(2sqrt N). Support admission admitted this only as a warning because graph D>=2^{-3/2}; SS1's repaired proof says it no longer uses the invalid arbitrary-D estimate.

Main Solver integrated proof to attack:
Let D=d_{3/2}(H). Since H has an edge, D>=2^{-3/2}. Let A be the adjacency matrix. Since A is nonnegative, for any real x, x^TAx<=|x|^TA|x|, so fix y>=0. For t>=0, define S_t={v:y_v>t}, n(t)=|S_t|. Let M(s,t) be the number of ordered adjacent pairs (u,v) with u in S_s and v in S_t. Layer cake gives
 y^TAy = ∫_0∞∫_0∞ M(s,t) dsdt = 2∫_0∞∫_0^t M(s,t) dsdt.
Nested-set edge bound: If T subseteq S, |T|=b, |S|=a, then ordered edge incidences from S to T are at most 6D a sqrt b. Proof: If a<=2b, count <=2e(H[S])<=2Da^{3/2}<=2sqrt2 D a sqrt b. If a>2b, choose uniformly b-set R subset S\T. Then e(T∪R)<=D(2b)^{3/2}. Averaging gives e(T)+b/(a-b)e(T,S\T)<=D(2b)^{3/2}, so e(T,S\T)<=2^{3/2}Da sqrt b. Together with e(T)<=Db^{3/2}, ordered incidence count <=6Da sqrt b.
Applying T=S_t subset S_s for s<=t gives M(s,t)<=6D n(s)sqrt{n(t)}. Hence
 y^TAy <= 12D ∫_0∞ sqrt{n(t)} (∫_0^t n(s)ds) dt.
Hardy-type threshold lemma: If n(t) is a decreasing threshold-count function with 0<=n(t)<=N, then
 ∫_0∞ sqrt{n(t)} (∫_0^t n(s)ds) dt <= 9 sqrt N ∫_0∞ t n(t)dt.
Proof offered: Put f=n/N, g=sqrt f, L=∫ t g(t)^2dt. Need show ∫ g(t)∫_0^t g(s)^2dsdt <=9L. Let tau(a)=|{t:g(t)>a}|, 0<a<=1. Then L=∫_0^1 a tau(a)^2 da. Expanding g(s)^2 and g(t) by layer cake gives two regions. Region a<b contributes <=1/2∫ a^2 tau(a)^2da<=1/2L. Region b<a contributes 2∫_0^1 a tau(a)(∫_0^a tau(b)db)da. Weighted Hardy inequality for decreasing functions ∫_0^1 a h(a)(∫_0^a h(b)db)da <=4∫_0^1 a h(a)^2da applied to h=tau bounds by 8L.
Finally ∫ t n(t)dt=1/2||y||_2^2, so y^TAy<=54D sqrt N||y||_2^2. Thus lambda(H)<=54D sqrt N.

Defender focus:
Attack CC001, CC002, CC003. In particular, verify the nested-set sampling proof, the transition from M(s,t) to the integral, and the Hardy-type threshold lemma including layer-cake expansion and the weighted Hardy inequality. Stress-test on stars, complete graphs, complete bipartite graphs, one-edge graph plus isolated vertices, and possible threshold functions. Do not use web.