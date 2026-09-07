# Run outputs

Runs save their outputs here, where Git ignores them. Start with `state.json`
to see how a run ended, then open its proof and review reports. A proof file
alone does not tell you whether it passed review.

Integrated pipeline runs and standalone verifier runs use separate folders;
neither continues from the other's output.

## Integrated S0-S6 runs

```text
Outputs/<run-name>/
  cleaner/                          Mini and package-audit evidence
  solver/<problem-id>/
    state.json                      controller status and stop reason
    round_NNN/
      S0.md ... S6.md               raw role outputs reached in this round
      candidate_final_proof.md      proof extracted from S6
      final_proof.md                assembled proof used downstream
      problem_statement_verifier.md
      citation_gate/
        citation_gate_summary.json
        attempt_001/
          citation_generator_output.md
          citation_verifier_output.md
          citation_gate_decision.json
      verifier_a1.md
      verifier_a2.md
      verifier_a3.md
      composer_a.md
      verifier_b.md
      verifier_c.md
```

Files appear only for stages that ran. A target mismatch stops review before
the citation checks; a citation failure stops it before Verifier A.

Citation retries use separate `attempt_NNN/` folders; the summary records which
attempts ran. See the [citation guide](../Individual%20Pipeline/citation/README.md#runtime-artifacts)
for the saved prompts and reports. The Python runtime does not currently save
every role's complete prompt. You can explore public role packets in the
[worked example](../Examples/cayley/README.md#follow-the-run).

Runs with accepted branch proofs can also contain:

```text
PROOF_GUIDE.md
proof_registry.json
proof_modules/
```

`final_proof.tex` appears only when S6 supplies TeX or the optional conversion
path succeeds.

## How to audit a run

1. Read `state.json` for the exact terminal status and stop reason.
2. Identify the final round reached.
3. Compare `target.md` with the Problem Statement Verifier report.
4. Inspect the citation-gate summary and its underlying reports.
5. Read all A reports, Composer A, B, and C—not only the most favorable report.
6. If a private Final Checker ran, confirm its status without exposing its
   privileged inputs or detailed reasoning.
7. Report unresolved gates explicitly.

## Standalone verifier runs

Direct `python -m verifiers` commands default to:

```text
Outputs/verifier/<verifier-run-id>/
```

This location is used for mocks, manual replay, and focused verifier checks.
The integrated solver neither reads from nor continues these runs.

## Publication boundary

Run folders can contain paper excerpts, private reference material, and
unfinished arguments. Review files before sharing them. For files you intend
to track under `publishable/`, follow the [publication checklist](publishable/README.md).
