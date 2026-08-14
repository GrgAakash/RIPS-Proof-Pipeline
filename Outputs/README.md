# Outputs

There are two independent output layouts.

## Integrated S0-S6 runs

Commands such as `Commands/run_no_internet.sh` and
`Commands/run_full_internet.sh` write:

```text
Outputs/<run-name>/
|-- cleaner/
`-- solver/
    `-- <problem-id>/
        `-- round_NNN/
            |-- problem_statement_verifier.md
            |-- verifier_a1.md
            |-- verifier_a2.md
            |-- verifier_a3.md
            |-- composer_a.md
            |-- verifier_b.md
            `-- verifier_c.md
```

These verifier files are part of the corresponding S0-S6 run. They appear only
for stages reached by that round; a target mismatch stops before citation and
the A/B/C cascade.

## Standalone verifier runs

Direct commands under `python -m verifiers`, including mocks, manual replays,
and focused API checks, default to:

```text
Outputs/verifier/<verifier-run-id>/
```

This optional folder is not read by the integrated pipeline and is not another
stage after `Outputs/<run-name>/solver/`. It may be absent until a standalone
verifier command creates it. Callers can choose another location with
`--output-root`.

Ordinary output is ignored because it can contain large model traces, paper
excerpts, or private material. After review, copy only intentional release
artifacts into `publishable/`.
