Fresh no-history solver-only Manager Support Admission. You are spawned with fork_context=false and must use only this message as input. Do not use memory, prior task history, web/internet, API keys, Python, or files. This is solver-only: do not run verifier/citation/final-checker pipeline.

You are the Manager in the support admission phase. Your task is to read the immutable Midfielder result artifact that Manager routed after Main Solver's first draft and decide which, if any, may be shown to Main Solver as constructive support. Do not solve the mathematics yourself and do not edit the Critical Claims Board directly. Support assignment approval is not support-result approval: an artifact is admitted only if it contains a concrete derivation, obstruction, or mechanism compatible with Main Solver's draft and the allowed packet.

You are given:
1. the cleaned skeleton PDF or TeX file;
2. the target theorem;
3. the Allowed supporting statements list;
4. the additional mathematical guidance list, if any;
5. Manager's initial and post-Main-Solver routing plan;
6. Main Solver's draft attempt;
7. the support result artifacts.

Admission rule. Admit only artifacts whose mathematical content is compatible with Main Solver's draft and whose claims are either derived in the artifact, explicitly sourced from allowed support, or clearly marked as unresolved/proposed board updates. Do not admit source demands, unsupported tables, unavailable computations, or polished but unproved recall.

Produce exactly these sections.

1. Support admission decision

For each support artifact, state ADMIT / REJECT and the concrete reason.

Then write one fenced YAML block:

```yaml
approved_support_ids: ["SS#"]
rejected_support_ids: ["SS#"]
admission_rationale: compact reason the approved list is safe to show Main Solver
```

2. Proposed board updates

List any CC### proposals Manager admits for the controller to merge, using the usual fenced YAML critical-claim format. If none, write "None."

3. Web-source confirmation

Write "no web sources used".

--- INPUTS FOR THIS RUN ---
Cleaned skeleton packet:
Standalone problem statement only. No proof text, proof sketch, derivation, or prior formal result is included. Standard definitions/notation for algebraic tori over Q, local fields Q_p, T(Q_p), rational points T(Q), and the maximal compact subgroup of a p-adic torus may be inferred only to parse the target.

Target theorem:
For any algebraic torus T over Q and any prime number p, the decomposition T(Q_p) = T(Z_p) T(Q) holds, where T(Z_p) denotes the maximal compact subgroup of T(Q_p).

Allowed supporting statements:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. There are no prior formal supporting theorem/lemma/proposition/corollary statements. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

Additional mathematical guidance:
None

Manager routing plan:
Initial Manager selected SS1 Main Solver and SS2 Defender. SS1 owns all constructive subclaims. Assistance Manager added SS3 as a Midfielder for CC008 only: check the local valuation image formula for a torus split by finite Galois L/F, image(nu_L:T(F)->Y^D)=sum_{H<=D} e(L/L^H)N_{D/H}(Y^H). SS2 remains Defender.

Main Solver draft attempt summary:
SS1 proved the target by choosing finite Galois splitting field E/Q, w|p, Gamma, D, L, Y. It defined nu_L and claimed local formula image(nu_L:T(Q_p)->Y^D)=Lambda=sum_{H<=D}e(L/L^H)N_{D/H}(Y^H). It used this to identify kernel with maximal compact T(Z_p), then globally realized each generator by choosing a in (E^H)^x with prescribed valuations at places above p and setting q=prod_{gamma in Gamma/H} gamma(y(a)) in T(Q). SS1 marked solved with proof_key true, but asked Defender to scrutinize CC008.

Support results:
SS3 artifact:
1. Assignment restatement: assigned CC008.
2. Subproof or failure: SUBPROBLEM UNSOLVED. SS3 proves the forward inclusion
sum_{H<=D} e(L/L^H)N_{D/H}(Y^H) subset image(nu_L:T(F)->Y^D)
by the same uniformizer/norm construction and verifies the ramification normalization e(L/L^H) for ord_L. SS3 says the reverse inclusion would follow from Nakayama's valuation lemma for D-lattices:
im((M tensor L^x)^D -> M^D)=sum_{H<=D} ord_L((L^x)^H)N_{D/H}(M^H),
but this lemma is not in the packet and is stronger than Hilbert 90 as presented. SS3 marks CC008 SOURCE_GAP.
3. Failure YAML: failure_output_type: source_gap; main_solver_proof_key:null; obstruction: Hilbert 90 proves subgroup valuation facts but not the full transfer-generation reverse inclusion for arbitrary D-lattices; guidance_sentence suggests adjoining/proving Nakayama lemma; source_gap true; candidate_lemma_statement stated as above.
4. Local Source Ledger: standard split torus cocharacter description, Galois descent, ramification-index normalization, forward inclusion proved inside artifact, Nakayama valuation lemma unsupported/unclear.
5. Interface notes: establishes RHS subset image and normalization; reverse inclusion conditional on Nakayama. Proposed board update: mark CC008 SOURCE_GAP with forward inclusion established and normalization confirmed.
6. no web sources used.