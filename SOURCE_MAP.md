# Source Map

This is a curated guide to where each responsibility is implemented. All
Python packages listed here are editable source; there is no generated
`Codes/` mirror. The `Individual Pipeline/` directory is a container for the
five implementation components, not a renamed project or an importable Python
package.

## Workspace

- [Individual Pipeline/](Individual%20Pipeline/): container for the five
  implementation components below.
  - [solver/](Individual%20Pipeline/solver/): S0-S6 orchestration, branch
    handling, proof assembly, and the integrated CLI.
  - [citation/](Individual%20Pipeline/citation/): post-S6 Citation Generator and
    Citation Verifier gate.
  - [verifiers/](Individual%20Pipeline/verifiers/): isolated A1/A2/A3, Composer
    A, B, and C runner.
  - [paper_cleaner/](Individual%20Pipeline/paper_cleaner/): arXiv ingestion,
    statement indexing, dependency extraction, and target selection.
  - [paper_cleaner_mini/](Individual%20Pipeline/paper_cleaner_mini/): one-target
    author/check/repair and audit workflow.
- [Prompt Packet/](Prompt%20Packet/): canonical role prompts and operational
  flow chart.
- [prompt_sync.py](prompt_sync.py): generates and checks component-owned prompt
  views from the canonical packets.
- [Commands/](Commands/): reusable shell entry points.
- [Inputs/](Inputs/): ignored local input workspace.
- [Outputs/](Outputs/): ignored local run workspace.
- [tests/](tests/): offline solver and verifier regression tests.

## Integrated entry points

- [run_pipeline.py](run_pipeline.py): wrapper for the `run-cleaner-solver` CLI.
- [Commands/run_no_internet.sh](Commands/run_no_internet.sh): closed-book S0-S6.
- [Commands/run_full_internet.sh](Commands/run_full_internet.sh): hosted-search
  S0-S6.

## Cleaner and bridge

- [paper_cleaner/run.py](Individual%20Pipeline/paper_cleaner/run.py): resumable
  paper preparation.
- [paper_cleaner/src/step1_get_source.py](Individual%20Pipeline/paper_cleaner/src/step1_get_source.py):
  source retrieval and normalization.
- [paper_cleaner/src/step2_parse.py](Individual%20Pipeline/paper_cleaner/src/step2_parse.py): statement
  and proof indexing.
- [paper_cleaner/src/step4_deps.py](Individual%20Pipeline/paper_cleaner/src/step4_deps.py): dependency
  extraction.
- [paper_cleaner/src/step5_select_mains.py](Individual%20Pipeline/paper_cleaner/src/step5_select_mains.py):
  eligible target selection.
- [paper_cleaner_mini/stage2.py](Individual%20Pipeline/paper_cleaner_mini/stage2.py): target package
  author/check/repair stages.
- [paper_cleaner_mini/audit.py](Individual%20Pipeline/paper_cleaner_mini/audit.py): independent package
  audit.
- [solver/cleaner_bridge.py](Individual%20Pipeline/solver/cleaner_bridge.py): audited export into the
  public solver packet.
- [solver/skeleton_source_gate.py](Individual%20Pipeline/solver/skeleton_source_gate.py): restricted
  source-validation gate.

## Solver

- [solver/cli.py](Individual%20Pipeline/solver/cli.py): solver-only and integrated
  command surface.
- [solver/prompt_loader.py](Individual%20Pipeline/solver/prompt_loader.py): role extraction from the
  selected prompt packet.
- [solver/agent_calls.py](Individual%20Pipeline/solver/agent_calls.py): S0-S6 and verifier calls.
- [solver/orchestrator.py](Individual%20Pipeline/solver/orchestrator.py): rounds, parallel modules,
  branches, gates, and terminal state.
- [solver/controller.py](Individual%20Pipeline/solver/controller.py): deterministic routing and stop
  rules.
- [solver/sealed_proofs.py](Individual%20Pipeline/solver/sealed_proofs.py): hash-verified branch proof
  persistence and release.
- [solver/s6_artifacts.py](Individual%20Pipeline/solver/s6_artifacts.py): proof, source-ledger, and
  completion-artifact splitting.
- [solver/report_parsers.py](Individual%20Pipeline/solver/report_parsers.py): structured model-report
  parsing.
- [solver/mock.py](Individual%20Pipeline/solver/mock.py): deterministic offline scenarios.
- [solver/prompts/](Individual%20Pipeline/solver/prompts/): generated S0, S1-S5, S6, and source-gate
  prompt views, separated by internet mode where necessary.

## Citation and verification

- [citation/gate.py](Individual%20Pipeline/citation/gate.py): citation stage execution and decision.
- [citation/prompts.py](Individual%20Pipeline/citation/prompts.py): public-only prompt assembly.
- [citation/parsers.py](Individual%20Pipeline/citation/parsers.py): citation report parsing.
- [citation/prompts/](Individual%20Pipeline/citation/prompts/): generated Citation Generator and
  Citation Verifier views.
- [verifiers/orchestrator.py](Individual%20Pipeline/verifiers/orchestrator.py): verifier-only routing.
- [verifiers/api_runners.py](Individual%20Pipeline/verifiers/api_runners.py): A/Composer/B/C prompt
  assembly.
- [verifiers/parsers.py](Individual%20Pipeline/verifiers/parsers.py): verifier report parsing.
- [verifiers/prompt_sync.py](Individual%20Pipeline/verifiers/prompt_sync.py): canonical prompt-copy
  compatibility command for verifier-owned views.
- [verifiers/prompts/](Individual%20Pipeline/verifiers/prompts/): generated Problem Statement,
  A/B/C, Composer A, and Final Checker views.

## Verification

- [tests/test_solver_bundle.py](tests/test_solver_bundle.py): package imports,
  both prompt modes, citation gate, and terminal mock runs.
- [tests/verifier_pipeline/](tests/verifier_pipeline/): mock, parser,
  prompt-sync, and mocked API cascade tests.
- [tests/test_prompt_views.py](tests/test_prompt_views.py): repository-wide
  component prompt ownership and drift checks.
- [tests/test_pipeline_gates.py](tests/test_pipeline_gates.py): offline
  Problem Statement, skeleton-source, and cleaner-bridge hard-gate tests.
