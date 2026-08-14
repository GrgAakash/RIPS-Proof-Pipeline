1. Attack inventory

- CC001: `T(Z_p)` means the maximal compact subgroup. Attack: checked whether proof uses integral-model points. Outcome: held.
- CC002: target is surjectivity `T(Q) -> T(Q_p)/T(Z_p)`. Attack: quotient reduction by the maximal compact subgroup. Outcome: held.
- CC003: local quotient via valuation lattice. Attack: checked kernel/maximal compact argument and normalization; `G_m` with ramified nonminimal splitting field shows quotient maps to `e(L/F)Z`, not all `Y^D`. Outcome: held only if stated as `im(nu_L)`, not full `Y^D`.
- CC004: every local class represented by `T(Q)`. Attack: checked global coset construction and valuation computation. Outcome: undecidable from packet materials because it depends on CC008 reverse inclusion.
- CC005: weak approximation for arbitrary `Q`-tori. Attack: traced usage. Outcome: held as not used; proof uses only number-field weak approximation.
- CC006: no hidden split/unramified/quasi-trivial hypotheses. Attack: tested `G_m`, restriction of scalars, norm-one tori, ramified local splitting fields. Outcome: held conditional on CC008.
- CC007: class-group/principal-divisor obstruction eliminated. Attack: checked whether weak approximation in `K=E^H` requires a principal divisor supported only above `p`. Outcome: held for each generator; full claim remains conditional on CC008.
- CC008: local valuation image formula. Attack: verified RHS subset matches SS3’s uniformizer/norm construction and ramification normalization; attacked reverse inclusion. Outcome: undecidable from packet materials; reverse inclusion is imported as Nakayama/Tate-Nakayama and not proved.
- Claim basis for CC008: “standard local Nakayama/Tate-Nakayama valuation theorem.” Attack: compared to allowed supporting statements and SS3 report. Outcome: broken as an unconditional packet-supported basis.

2. Findings

The unresolved challenge is CC008. The proof needs:
`im(nu_L) ⊆ sum_{H<=D} e(L/L^H) N_{D/H}(Y^H)`.
SS3 proves only the opposite containment. Main Solver imports the missing reverse containment as “standard local Nakayama/Tate-Nakayama,” but the packet does not admit that theorem and no proof is supplied.

Live competing candidates:
- Main formula is exactly correct.
- The image strictly contains the displayed transfer-generated subgroup for some `D`-lattice.
- The correct formula requires additional cohomological, subgroup, or normalization terms.
- None of the above.

Evidence that would discharge the challenge: a self-contained proof of the local Nakayama valuation lemma with the stated `ord_L` normalization, or an explicit Manager admission that this exact theorem is allowed standard background.

Downstream, CC003, CC004, and CC007 cannot be marked established unconditionally. Their internal computations look consistent, but they rely on CC008 to know that every local valuation vector decomposes into the globalizable transfer generators.

3. Defender verdict

```yaml
role_task_status: completed
defender_verdict: BLOCK
blocks_acceptance: true
critical_ledger_underreach_audit: PASS
critical_ledger_overreach_audit: PASS
background_manifest_underreach_audit: PASS
background_manifest_misclassification_audit: FAIL
attacked_claims: ["CC001", "CC002", "CC003", "CC004", "CC005", "CC006", "CC007", "CC008", "claim_basis labels", "global valuation computation"]
challenged_claim_ids: ["CC003", "CC004", "CC007", "CC008"]
competing_candidates: ["im(nu_L) equals the displayed transfer sum", "im(nu_L) strictly contains the displayed transfer sum", "the correct image formula has additional subgroup/cohomological/normalization terms", "none-of-the-above"]
obstruction: "The reverse inclusion in the local Nakayama valuation formula is unproved and not admitted by the allowed packet."
required_resolution: "Prove or explicitly admit the exact local Nakayama/Tate-Nakayama valuation lemma with L-normalized valuation."
source_gap: true
external_material_status: unavailable
autonomous_derivation_possible: true
candidate_lemma_statement: "For the chosen finite Galois local extension L/F with group D and D-lattice Y, every element of nu_L((Y tensor L^x)^D) lies in sum_{H<=D} e(L/L^H) N_{D/H}(Y^H)."
why_unblocks: "Together with SS3's proved RHS subset, this gives CC008 equality and makes Main Solver's global generator construction cover every local quotient class."
where_used: "Main Solver paragraph beginning 'Use the standard local Nakayama valuation theorem'; CC008, downstream CC003/CC004/CC007."
allowed_inputs: "Packet definitions, standard local-field valuation sequence, D-lattice formalism, and SS3 RHS-subset construction; not the target theorem."
dependencies: []
weaker_than_target: YES
equivalent_or_stronger: NO
recommended: YES
```

4. Role-completion summary

```yaml
failure_output_type: solved
type: "defender_block"
failed_route: "Main Solver proof"
obstruction: "CC008 reverse inclusion is an unproved source gap."
evidence: "SS3 explicitly proved only RHS subset and marked reverse inclusion SOURCE_GAP; Main Solver imports it as standard background without proof."
reuse_value: "Global construction and class-group obstruction analysis can be reused once CC008 is supplied."
guidance_sentence: "Prove the local Nakayama valuation reverse inclusion with the stated ramification normalization."
candidate_lemma_statement: "For the chosen finite Galois local extension L/F with group D and D-lattice Y, every element of nu_L((Y tensor L^x)^D) lies in sum_{H<=D} e(L/L^H) N_{D/H}(Y^H)."
why_unblocks: "It completes CC008 and makes the local-to-global valuation matching step valid."
where_used: "CC008 in Main Solver's proof."
allowed_inputs: "Packet definitions, local-field valuation exact sequence, D-lattice formalism, SS3 RHS-subset result."
dependencies: []
weaker_than_target: YES
equivalent_or_stronger: NO
recommended: YES
```

5. Local Source Ledger

Facts used in computations:
- If `a in (L^H)^x` has normalized valuation `ord_{L^H}(a)=1`, then `ord_L(a)=e(L/L^H)`.
- For `H <= D`, `K=E^H` has `K_{w_H}=L^H`, and `w` is the unique place of `E` above `w_H` in `E/K`.
- Weak approximation in a number field can prescribe exact valuations at finitely many places by choosing sufficiently close local approximations.
- For `G_m` with trivial `D`-action, `nu_L(F^x)=e(L/F)Z`; hence “quotient equals full `Y^D`” is false under `L`-normalized valuation unless `e=1`.
- For quadratic norm-one ramified/inert local examples, `Y^D=0`, so the local quotient is compact/trivial, matching the proof’s normalization tests.
- For restriction of scalars with permutation lattice, the valuation image is generated by the orbit-sum, matching the transfer construction.

Critical-claim audit:
- CC001: claimed basis packet; audited basis packet definition; mismatch no.
- CC002: claimed basis elementary reduction; audited basis elementary quotient argument; mismatch no.
- CC003: claimed basis local valuation proof; audited basis valid only as quotient `im(nu_L)` and dependent on CC008 for exact image; mismatch yes if accepted unconditionally.
- CC004: claimed basis local formula plus global construction; audited basis conditional on CC008; mismatch yes if accepted unconditionally.
- CC005: claimed basis not used; audited basis not used except number-field weak approximation; mismatch no.
- CC006: claimed basis target hypotheses; audited basis no hidden split/unramified restriction found; mismatch no.
- CC007: claimed basis global construction; audited basis class-group issue eliminated for generators, but full claim conditional on CC008; mismatch yes if accepted unconditionally.
- CC008: claimed basis standard Nakayama/Tate-Nakayama; audited basis RHS subset proved by SS3, reverse inclusion unproved/source gap; mismatch yes.

6. Web-source confirmation

no web sources used