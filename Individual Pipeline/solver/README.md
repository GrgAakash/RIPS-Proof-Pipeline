# Solver

This package implements the S0-S6 proof-reconstruction workflow, deterministic
routing, branching, final proof assembly, and integration with citation and
verification gates.

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

The repository-level shell wrappers in [`Commands/`](../../Commands/README.md)
are the recommended interface for ordinary paper runs.

## S0-S6 lifecycle

1. S0 creates a proof blueprint and identifies one key solver.
2. S1-S5 solve assigned obligations, with bounded parallelism.
3. S6 composes a single candidate proof.
4. Deterministic code splits and assembles the proof artifacts.
5. The exact-target and citation gates run.
6. A1/A2/A3, Composer A, B, and C run if prior gates clear.
7. The controller selects a bounded rerun, branch, human-review, or final route.
8. On the final route, a private gold proof enables the Final Checker; a clean
   public-only cascade can instead reach `accepted_cascade_only`. The controller
   then records the resulting terminal state. Earlier stops do not run the
   Final Checker.

The presence of an S6 response is not an acceptance decision. Read `state.json`
and the artifacts for the gates actually reached.

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

The sibling [`citation`](../citation/README.md) and
[`verifiers`](../verifiers/README.md) packages own their focused subsystems.

## Prompt ownership

The runtime source of truth is the selected canonical file under
[`Prompt Packet/`](../../Prompt%20Packet/README.md). Files in `prompts/` are
generated review views and must not be edited directly.

```bash
python prompt_sync.py --write
python prompt_sync.py --check
```

## Input and output contracts

- Hand-authored inputs: [`Inputs/solver_input/README.md`](../../Inputs/solver_input/README.md)
- Run artifacts: [`Outputs/README.md`](../../Outputs/README.md)
- Complete source map: [`SOURCE_MAP.md`](../../SOURCE_MAP.md)

## Claim boundary

The solver searches for and composes candidate arguments. It is not a formal
proof kernel. A mathematically persuasive response may still fail target,
source, citation, coupling, or verifier gates; the terminal status is the
authoritative workflow result.
