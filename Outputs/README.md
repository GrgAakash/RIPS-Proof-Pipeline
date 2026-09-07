# Run outputs

This directory contains ignored local run artifacts. The integrated pipeline
and standalone verifier utility use separate layouts and do not consume one
another's output.

> [!IMPORTANT]
> The presence of a proof file is not an acceptance decision. Begin with the
> terminal `state.json`, then inspect the artifacts for the gates actually
> reached.

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
        citation_generator.md
        citation_verifier.md
        citation_gate_summary.json
      verifier_a1.md
      verifier_a2.md
      verifier_a3.md
      composer_a.md
      verifier_b.md
      verifier_c.md
```

Only reached stages are present. A target mismatch stops before citation and
the A/B/C cascade; a citation failure stops before Verifier A.

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

Ordinary outputs can contain paper excerpts, raw model responses, private
material, and misleading intermediate claims. They remain ignored. Only
deliberately reviewed release artifacts belong under `publishable/`; follow the
[`publishable` checklist](publishable/README.md) before tracking one.
