# Solver Package

This is the standalone S0-S6 mathematical solver. The package supports both
`Prompts.md` (no hosted web search for S0-S6) and
`PromptsWithFullInternet.md` (source-supported solver web search).
In both modes, the sibling `../citation/` package runs restricted
source-checking web search after S6 and blocks Verifier A until the Citation
Verifier returns `GOOD_TO_GO`.

## Entry and shared runtime

- `cli.py`: `run-open-problem`, `prepare-cleaner-problem`, and
  `run-cleaner-solver` commands.
- `llm.py`: OpenAI-compatible and mock model clients, retries, reasoning
  settings, and hosted web-search controls.
- `config.py`: environment and API-key resolution.
- `packet.py`: the small system/user prompt payload type.
- `io_utils.py`: JSON parsing and run-file helpers used by the solver.

## S0-S6 pipeline

- `orchestrator.py`: rounds, S1-S5 parallelism, branches, citation gate,
  verifier cascade, and terminal state.
- `agent_calls.py`: S0-S6, citation, verifier, composer, and final-checker calls.
- `controller.py`: deterministic routing and stopping rules.
- `prompt_loader.py`: fixed-role prompt extraction from the selected packet.
- `schemas.py`: typed solver, report, controller, and state records.
- `report_parsers.py`: model report parsing.
- `run_store.py`: persisted state and per-round artifacts.
- `s6_artifacts.py`: deterministic splitting of S6 output artifacts.
- `mock.py`: deterministic offline scenarios.

## Citation gate

- `../citation/prompts.py`: Citation Generator/Verifier prompt extraction.
- `../citation/gate.py`: gate execution and persisted audit artifacts.
- `../citation/parsers.py`: controller-summary parsing.
- `../citation/models.py`: typed citation reports and decisions.
- `../citation/clients.py`: deterministic offline citation responses.

## Prompt views

`prompts/` contains generated S0, S1-S5, S6, and source-gate prompt views for
component-level review. The runtime source of truth remains the selected file
under `../../Prompt Packet/`. From the repository root, regenerate views with
`python prompt_sync.py --write`.

## Cleaner integration

- `cleaner_bridge.py`: audited cleaner-package export into solver inputs.
- `skeleton_source_gate.py`: restricted source-validation gate before S0-S6.

The standalone repository intentionally contains no nested `open_problem/` and
no legacy benchmark orchestrator, bundle, metrics, or model-record modules.
