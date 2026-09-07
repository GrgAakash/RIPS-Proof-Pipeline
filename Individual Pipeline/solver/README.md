# Solver

This package runs the proof-solving team. S0 makes a plan, S1-S5 work through
its parts, and S6 combines them into a proof. The controller saves each step
and decides whether to review the proof, try again, or stop.

## Entry points

After installing the repository with `python -m pip install -e '.[pipeline]'`:

```bash
python -m solver --help
python -m solver run-open-problem --help
python -m solver prepare-cleaner-problem --help
python -m solver run-cleaner-solver --help
```

| Command | Purpose |
|---|---|
| `run-open-problem` | Run S0-S6 on an existing theorem packet |
| `prepare-cleaner-problem` | Source-audit and export one Paper Cleaner Mini package |
| `run-cleaner-solver` | Run Mini, package gates, export, S0-S6, citation, and verifiers |

For a paper run, start with the shell scripts in the
[command guide](../../Commands/README.md).

## S0-S6 lifecycle

Both prompt modes use the same key-solver-first rule. Enabling internet access
does not change that order.

1. S0 makes a plan and chooses the key solver.
2. The key solver runs first. If it returns `solved`, the other four solvers run
   their assigned parts, with a limit on parallel calls.
3. S6 writes a single candidate proof.
4. Code assembles the proof files, including any accepted branch proofs.
5. Reviewers check the target statement and citations.
6. If those checks pass, A1/A2/A3, Composer A, B, and C review the mathematics.
7. The controller decides whether to retry, attempt a separate lemma, request
   human review, or proceed to the final check, within the run's limits.
8. If a private reference proof is supplied, the Final Checker reviews the
   candidate. Without it, a passing review chain can reach
   `accepted_cascade_only`. Runs that stop earlier do not reach this check.

Read `state.json` to see where the run stopped and which reviews it completed.

## Important modules

| Module | Responsibility |
|---|---|
| `cli.py` | CLI parsing and integrated entry points |
| `orchestrator.py` | rounds, branches, gates, and terminal lifecycle |
| `controller.py` | deterministic decisions and stop rules |
| `agent_calls.py` | role calls and prompt packets |
| `prompt_loader.py` | canonical-packet role extraction |
| `cleaner_bridge.py` | audited cleaner export into solver inputs |
| `skeleton_source_gate.py` | restricted validation of Section 3 grants |
| `sealed_proofs.py` | branch-proof sealing and final assembly |
| `s6_artifacts.py` | deterministic S6 artifact splitting |
| `report_parsers.py` | structured model-report parsing |
| `run_store.py` | persisted state and round artifacts |
| `mock.py` | deterministic offline scenarios |

The [citation](../citation/README.md) and [verifier](../verifiers/README.md)
guides explain the review stages.

## Prompt ownership

The runtime reads its role prompts from the selected file in
[Prompt Packet/](../../Prompt%20Packet/README.md). The copies in `prompts/` are
generated for reference. Edit the original packet, then regenerate the copies:

```bash
python prompt_sync.py --write
python prompt_sync.py --check
```

## Input and output contracts

- Hand-authored inputs: [`Inputs/solver_input/README.md`](../../Inputs/solver_input/README.md)
- Run artifacts: [`Outputs/README.md`](../../Outputs/README.md)
- Complete source map: [`SOURCE_MAP.md`](../../SOURCE_MAP.md)

## Claim boundary

S6 produces a candidate, not an acceptance decision. Its proof may still fail
the statement, source, or mathematical reviews. Report the final status from
`state.json`; these model-based checks are not formal verification.
