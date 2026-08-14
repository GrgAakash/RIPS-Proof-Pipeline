Fresh no-history solver-only branch experiment. Do not use memory, prior task history, previous outputs outside this prompt, answer keys, files outside this prompt, web search/internet, API keys, or Python. This is a no-internet Manager Support Admission run after branch support worker SS3. Use the latest Manager Support Admission prompt structure.

You are the Manager in support admission. Read the immutable support result and decide whether it may be shown to Main Solver. Do not solve the math yourself. Admit concrete derivations/obstructions compatible with Main Solver's draft; reject unsupported claims.

Produce sections: 1. Support admission decision with YAML approved/rejected; 2. Proposed board updates; 3. Web-source confirmation.

--- INPUTS ---
Target lemma:
There is an absolute constant C>0 such that every N-vertex graph H with at least one edge satisfies lambda(H)<=C sqrt(N)d_{3/2}(H), where d_{3/2}(H)=max_{nonempty S}e(H[S])/|S|^{3/2}.

Additional mathematical guidance: None.

Branch Manager routing: SS1 Main Solver; SS2 Defender; SS3 checking-mode Midfielder assigned CC003, the threshold integral closure. CC001 Rayleigh reduction; CC002 nested ordered edge-count convention; CC003 threshold integral closure no log.

Branch Main Solver draft: claimed proof using layer cake and bounds M(s,t)<=n(s)n(t), M(s,t)<=2D n(s)^{3/2} for s<=t, then asserted integral estimate
2∫∫_{s<t} min{n(s)n(t),2D n(s)^{3/2}} <= 16D√N∫2t n(t)dt.

Support result SS3:
Verdict BLOCK. The displayed inequality is false as stated for arbitrary D>0. Counterexample: N=m, y=(1,m^{-1/2},...,m^{-1/2}), D=1/(2√m). Then n(t)=m for 0<t<=a=m^{-1/2}, n(t)=1 for a<t<=1. LHS = 2√m -1 + m^{-1/2}-2m^{-1}+m^{-3/2}. RHS normalizer D√N∫2t n(t)dt = 1-1/(2m), so no absolute K works for all D. Failure mechanism: short high-multiplicity layer followed by long singleton tail. Salvage note: a nearby bound would be true if the second term used the lower layer size n(t)^{3/2}, but that may not be graph-justified.

Controller note: In the actual graph lemma, D=d_{3/2}(H) and H has an edge, so D>=2^{-3/2}. This note is not a proof; decide admission of SS3's obstruction and any board update.