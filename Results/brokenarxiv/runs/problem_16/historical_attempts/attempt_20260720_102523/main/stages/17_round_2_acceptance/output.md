1. **Composition Map**

- Target theorem: `T(Q_p)=T(Z_p)T(Q)` and `T(Z_p)` maximal compact.
  Status: **not accepted / unresolved**.
- Critical dependency: local Nakayama valuation reverse inclusion for finite Galois local `L/F`, `D=Gal(L/F)`, and arbitrary `D`-lattice `Y`.
  Status: **missing**.
- SS3 contribution: proves only easy containment `sum subset im(nu_L)` with ramification factors/non-normal `H`.
  Status: **partial only**.
- Main Solver integration: explicitly declares `SUBPROBLEM UNSOLVED`, `main_solver_proof_key:false`.
  Status: **failure artifact preserved**.

2. **Main Solver Authorship And Proof-Reference Audit**

Main Solver did not provide a complete proof of the target theorem. The decisive reverse local inclusion was not established by approved support. The proof references a “standard cohomological Nakayama” result, but that theorem is neither proved nor allowed as prior support. Defender agreed the blocker is genuine and no hidden accepted proof remains.

3. **Manager Failure Output And Candidate Guidance YAML**

```yaml
answer_status: UNRESOLVED
manager_acceptance_key: false
main_solver_proof_complete: false
main_solver_proof_used_as_final: false
failure_output_type: branch_lemma_target
preserve_main_solver_artifact: true
proof_replacement_supplied: false
candidate_guidance:
  - Prove Guidance H_2 directly: for finite Galois local L/F with D=Gal(L/F) and D-lattice Y, establish the reverse inclusion
    nu_L((Y tensor L^x)^D) subset sum_{H<=D} e(L/L^H) N_{D/H}(Y^H)
    without invoking an unapproved transfer-generation theorem.
```

4. **Source Ledger Markers**

```text
SOURCE_LEDGER_BEGIN
- User-provided target theorem.
- User-provided allowed support restrictions.
- User-provided Guidance H_2.
- User-provided Round 2 artifacts.
- No external sources.
SOURCE_LEDGER_END
```

5. **Background And Assumptions Manifest Markers**

```text
BACKGROUND_AND_ASSUMPTIONS_BEGIN
- Only definitions/notation are allowed as background.
- No prior formal theorem equivalent to or downstream from the target may be used.
- No repair or replacement proof is supplied.
BACKGROUND_AND_ASSUMPTIONS_END
```

6. **Completion Checklist Markers**

```text
COMPLETION_CHECKLIST_BEGIN
- Acceptance decision given: not accepted.
- Critical missing claim identified.
- Main Solver failure artifact preserved.
- One actionable guidance item supplied.
COMPLETION_CHECKLIST_END
```

7. **Web-Source Confirmation Markers**

```text
WEB_SOURCE_CONFIRMATION_BEGIN
No web sources used.
WEB_SOURCE_CONFIRMATION_END
```