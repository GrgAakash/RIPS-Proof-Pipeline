<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/rips-proof-mark-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="docs/rips-proof-mark.png">
    <img src="docs/rips-proof-mark.png" width="132" alt="RIPS Proof Pipeline project mark">
  </picture>
</p>

<h1 align="center">Source Map</h1>

<p align="center">
  <strong>Find the code, commands, and saved results.</strong>
</p>

<p align="center">
  <a href="README.md">Project home</a> ·
  <a href="Commands/README.md">Commands</a> ·
  <a href="Prompt%20Packet/README.md">Prompt protocol</a> ·
  <a href="Outputs/README.md">Artifact guide</a>
</p>

Use the tables below to find a starting point. Expand a section for the files
behind that part of the pipeline.

## Find the right starting point

| I want to… | Start here |
|---|---|
| Follow a real run's inputs and outputs | [Cayley's-formula worked example](Examples/cayley/README.md) |
| Run one paper or theorem packet | [Command guide](Commands/README.md) |
| Understand the complete execution order | [Operational flow chart](Prompt%20Packet/FlowChart.md) |
| Inspect or modify source extraction | [Full paper cleaner guide](Individual%20Pipeline/paper_cleaner/README.md) |
| Inspect target packaging and audit | [Mini cleaner guide](Individual%20Pipeline/paper_cleaner_mini/README.md) |
| Follow S0-S6, branching, or routing | [Solver guide](Individual%20Pipeline/solver/README.md) |
| Inspect citation and proof-review gates | [Citation guide](Individual%20Pipeline/citation/README.md) · [Verifier guide](Individual%20Pipeline/verifiers/README.md) |
| Edit a role's instructions | [Prompt protocol](Prompt%20Packet/README.md) |
| Interpret a completed run | [Output artifact guide](Outputs/README.md) |
| Browse reviewed public examples | [Results index](Results/README.md) |
| Compare with-context and without-context results | [Paper-reproduction reports](Results/paper_reproduction/README.md) |

## Pipeline at a glance

| Layer | Responsibility | Primary location |
|---|---|---|
| Source preparation | Retrieve, normalize, index, and select targets | [`paper_cleaner/`](Individual%20Pipeline/paper_cleaner/) |
| Target packaging | Author, check, repair, and independently audit one packet | [`paper_cleaner_mini/`](Individual%20Pipeline/paper_cleaner_mini/) |
| Source boundary | Export only an audited public packet and validate external grants | [`cleaner_bridge.py`](Individual%20Pipeline/solver/cleaner_bridge.py) · [`skeleton_source_gate.py`](Individual%20Pipeline/solver/skeleton_source_gate.py) |
| Proof reconstruction | Run S0-S6, branches, assembly, and deterministic routing | [`solver/`](Individual%20Pipeline/solver/) |
| Evidence gates | Check citations and run the A/Composer/B/C cascade | [`citation/`](Individual%20Pipeline/citation/) · [`verifiers/`](Individual%20Pipeline/verifiers/) |
| Public evidence | Publish only deliberately reviewed artifacts | [`Results/`](Results/) |

## Complete implementation index

`Individual Pipeline/` holds the five Python components listed below; it is not
itself an importable package. Edit those files directly—there is no separate
`Codes/` copy. Links use file paths so code edits do not leave stale line numbers.

<details>
<summary><strong>Workspace and public surface</strong> — folders, packaging, tests, and README assets</summary>

### Workspace

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
- [Examples/cayley/](Examples/cayley/README.md): reviewed manual Codex-subagent
  worked example, with role packets, outputs, proof PDFs, and integrity hashes.
- [Results/](Results/): deliberately reviewed public evaluation artifacts.
- [Results/paper_reproduction/](Results/paper_reproduction/README.md): with-context
  and without-context setups, final results, and deduplicated target records.
- [Results/paper_reproduction/subjects.json](Results/paper_reproduction/subjects.json):
  primary arXiv categories and paper titles for the subject-coverage view.
- [Results/paper_reproduction/paired_outcomes.md](Results/paper_reproduction/paired_outcomes.md):
  four-way context comparison by subject, matched targets, and unresolved labels.
- [tests/](tests/): offline solver and verifier regression tests.
- [docs/pipeline-overview.svg](docs/pipeline-overview.svg): public README
  architecture figure.
- [docs/build_results_charts.py](docs/build_results_charts.py): generates the
  [benchmark](docs/benchmark-results.svg),
  [paper-reproduction](docs/paper-reproduction-results.svg), and
  [subject-coverage](docs/paper-subject-coverage.svg) figures plus the subject lists.
- [docs/build_paired_results.py](docs/build_paired_results.py): matches report
  targets and generates the paired subject breakdown without model calls.
- [docs/rips-proof-mark.png](docs/rips-proof-mark.png) and
  [docs/rips-proof-mark-dark.png](docs/rips-proof-mark-dark.png): light- and
  dark-mode variants of the public README project mark.
- [CONTRIBUTING.md](CONTRIBUTING.md): development workflow, reporting guidance,
  privacy rules, and pull-request checklist.
- [CITATION.cff](CITATION.cff): machine-readable project citation metadata.
- [.github/workflows/ci.yml](.github/workflows/ci.yml): offline regression,
  prompt-synchronization, and documentation-link checks.
- [pyproject.toml](pyproject.toml): package metadata, optional dependencies,
  installed command names, and editable-package layout.
- [CONTRIBUTORS.md](CONTRIBUTORS.md): project provenance and contributor roles.

</details>

<details>
<summary><strong>Entry points</strong> — installed commands and repository-level wrappers</summary>

### Entry points

- [run_pipeline.py](run_pipeline.py): wrapper for the `run-cleaner-solver` CLI.
- [solver/cli.py](Individual%20Pipeline/solver/cli.py): implementation behind
  `integrated-math-solver`, `python -m solver`, solver-only runs, preparation,
  and integrated cleaner-to-solver runs.
- [verifiers/cli.py](Individual%20Pipeline/verifiers/cli.py): implementation
  behind `integrated-verifiers` and `python -m verifiers`.
- [citation/cli.py](Individual%20Pipeline/citation/cli.py): standalone Citation
  Generator/Verifier command surface.
- [Commands/prepare_paper_input.sh](Commands/prepare_paper_input.sh): prepare an
  arXiv paper through cleaner Step 5.
- [Commands/run_mini_from_arxiv.sh](Commands/run_mini_from_arxiv.sh): run the
  full-paper cleaner through Step 5, then Mini and its independent audit.
- [Commands/run_no_internet.sh](Commands/run_no_internet.sh): closed-book S0-S6.
- [Commands/run_full_internet.sh](Commands/run_full_internet.sh): hosted-search
  S0-S6.

The complete command matrix, defaults, cost boundary, and output locations are
in [Commands/README.md](Commands/README.md).

</details>

<details>
<summary><strong>Full paper cleaner</strong> — current Steps 1–5 plus retained legacy Steps 6–8</summary>

### Full paper cleaner

The current integrated route uses this component for Steps 1–5, then hands the
selected target to Mini. `run.py` retains Steps 6–8 for older standalone
cleaner runs; those stages are not part of the current Mini-to-S0–S6 route.

- [paper_cleaner/run.py](Individual%20Pipeline/paper_cleaner/run.py): resumable
  Step 1-Step 8 orchestration and batch index generation.
- [paper_cleaner/audit.py](Individual%20Pipeline/paper_cleaner/audit.py):
  independent full-source audit of shipped packages and exclusions.
- [paper_cleaner/src/step1_get_source.py](Individual%20Pipeline/paper_cleaner/src/step1_get_source.py):
  source retrieval and normalization.
- [paper_cleaner/src/step2_parse.py](Individual%20Pipeline/paper_cleaner/src/step2_parse.py): statement
  extraction, proof pairing, and source-backed indexing.
- [paper_cleaner/src/step3_fill_index.py](Individual%20Pipeline/paper_cleaner/src/step3_fill_index.py):
  controlled index completion and targeted dependency filling.
- [paper_cleaner/src/step4_deps.py](Individual%20Pipeline/paper_cleaner/src/step4_deps.py): dependency
  extraction and graph construction.
- [paper_cleaner/src/step5_select_mains.py](Individual%20Pipeline/paper_cleaner/src/step5_select_mains.py):
  eligible target selection.
- [paper_cleaner/src/step6_package.py](Individual%20Pipeline/paper_cleaner/src/step6_package.py):
  draft package assembly and external-result resolution.
- [paper_cleaner/src/step7_verify.py](Individual%20Pipeline/paper_cleaner/src/step7_verify.py):
  self-containment, sufficiency, leak, and package-repair gates.
- [paper_cleaner/src/step8_report.py](Individual%20Pipeline/paper_cleaner/src/step8_report.py):
  human-readable dependency graph, dashboard, and selection rationale.
- [paper_cleaner/src/target_integrity.py](Individual%20Pipeline/paper_cleaner/src/target_integrity.py):
  source-derived statement identity, proof provenance, frozen-target checks,
  and canonical target rendering.
- [paper_cleaner/src/gates.py](Individual%20Pipeline/paper_cleaner/src/gates.py):
  deterministic cleaner quality gates and leak scans.
- [paper_cleaner/src/graph_utils.py](Individual%20Pipeline/paper_cleaner/src/graph_utils.py):
  dependency-graph cleaning, closure, eligibility, and signals.
- [paper_cleaner/src/latex_utils.py](Individual%20Pipeline/paper_cleaner/src/latex_utils.py):
  LaTeX normalization, macro handling, and reference scanning.
- [paper_cleaner/src/common.py](Individual%20Pipeline/paper_cleaner/src/common.py),
  [schemas.py](Individual%20Pipeline/paper_cleaner/src/schemas.py), and
  [llm.py](Individual%20Pipeline/paper_cleaner/src/llm.py): configuration,
  typed artifacts, structured logging, caching, retries, and model calls.
- [paper_cleaner/src/tar_compat.py](Individual%20Pipeline/paper_cleaner/src/tar_compat.py):
  safe source-archive extraction across supported Python versions.
- [paper_cleaner/config.yaml](Individual%20Pipeline/paper_cleaner/config.yaml):
  full-cleaner models, limits, and operational defaults.
- [paper_cleaner/prompts/](Individual%20Pipeline/paper_cleaner/prompts/):
  component-owned cleaner and cleaner-audit prompts.

</details>

<details>
<summary><strong>Target-scoped Mini cleaner</strong> — author, check, repair, validate, and audit one package</summary>

### Target-scoped Mini cleaner

- [paper_cleaner_mini/run.py](Individual%20Pipeline/paper_cleaner_mini/run.py):
  arXiv-reference normalization and end-to-end Mini command construction.
- [paper_cleaner_mini/stage2.py](Individual%20Pipeline/paper_cleaner_mini/stage2.py):
  target package author/check/repair stages and frozen-target enforcement.
- [paper_cleaner_mini/audit.py](Individual%20Pipeline/paper_cleaner_mini/audit.py):
  independent package and exclusion audit.
- [paper_cleaner_mini/audit_gate.py](Individual%20Pipeline/paper_cleaner_mini/audit_gate.py):
  dependency-free audit pass/fail rule.
- [paper_cleaner_mini/package_validation.py](Individual%20Pipeline/paper_cleaner_mini/package_validation.py):
  deterministic target, source, support, and package checks.
- [paper_cleaner_mini/compare_audits.py](Individual%20Pipeline/paper_cleaner_mini/compare_audits.py):
  side-by-side comparison of two audit reports.
- [paper_cleaner_mini/minilib.py](Individual%20Pipeline/paper_cleaner_mini/minilib.py):
  self-contained configuration, schema, model-call, LaTeX, and leak-check
  support used by Mini.
- [paper_cleaner_mini/config.yaml](Individual%20Pipeline/paper_cleaner_mini/config.yaml):
  Mini models, limits, and operational defaults.

</details>

<details>
<summary><strong>Cleaner-to-solver bridge</strong> — enforce the public packet and source boundary</summary>

### Cleaner-to-solver bridge

- [solver/cleaner_bridge.py](Individual%20Pipeline/solver/cleaner_bridge.py): audited export into the
  public solver packet.
- [solver/skeleton_source_gate.py](Individual%20Pipeline/solver/skeleton_source_gate.py): restricted
  source-validation gate.

</details>

<details>
<summary><strong>Solver</strong> — prompts, S0-S6, branching, routing, state, and proof assembly</summary>

### Solver

- [solver/prompt_loader.py](Individual%20Pipeline/solver/prompt_loader.py): role extraction from the
  selected prompt packet.
- [solver/packet.py](Individual%20Pipeline/solver/packet.py): common system/user
  prompt payload passed to model clients.
- [solver/agent_calls.py](Individual%20Pipeline/solver/agent_calls.py): S0-S6,
  exact-target, citation, verifier, and Final Checker calls.
- [solver/llm.py](Individual%20Pipeline/solver/llm.py): narrow model-client
  interface, deterministic mock client, and OpenAI-compatible implementation.
- [solver/orchestrator.py](Individual%20Pipeline/solver/orchestrator.py): rounds, parallel modules,
  branches, gates, and terminal state.
- [solver/controller.py](Individual%20Pipeline/solver/controller.py): deterministic routing and stop
  rules.
- [solver/run_store.py](Individual%20Pipeline/solver/run_store.py): recursive run
  layout plus state, round, branch, and verifier artifact persistence.
- [solver/sealed_proofs.py](Individual%20Pipeline/solver/sealed_proofs.py): hash-verified branch proof
  persistence and release.
- [solver/s6_artifacts.py](Individual%20Pipeline/solver/s6_artifacts.py): proof, source-ledger, and
  completion-artifact splitting.
- [solver/report_parsers.py](Individual%20Pipeline/solver/report_parsers.py): structured model-report
  parsing.
- [solver/schemas.py](Individual%20Pipeline/solver/schemas.py): typed solver,
  verifier, controller, and pipeline-state records.
- [solver/config.py](Individual%20Pipeline/solver/config.py): API-key resolution
  and environment configuration policy.
- [solver/io_utils.py](Individual%20Pipeline/solver/io_utils.py): JSON and
  model-output file helpers.
- [solver/mock.py](Individual%20Pipeline/solver/mock.py): deterministic offline scenarios.
- [solver/prompts/](Individual%20Pipeline/solver/prompts/): generated S0, S1-S5, S6, and source-gate
  prompt views, separated by internet mode where necessary.

</details>

<details>
<summary><strong>Citation and verification</strong> — source ledger, A/Composer/B/C, replay, and evidence persistence</summary>

### Citation and verification

- [citation/cli.py](Individual%20Pipeline/citation/cli.py): standalone citation
  gate argument parsing and execution.
- [citation/gate.py](Individual%20Pipeline/citation/gate.py): citation stage execution and decision.
- [citation/prompts.py](Individual%20Pipeline/citation/prompts.py): public-only prompt assembly.
- [citation/parsers.py](Individual%20Pipeline/citation/parsers.py): citation report parsing.
- [citation/clients.py](Individual%20Pipeline/citation/clients.py): deterministic
  mock and OpenAI-compatible citation clients.
- [citation/models.py](Individual%20Pipeline/citation/models.py) and
  [constants.py](Individual%20Pipeline/citation/constants.py): typed reports,
  decisions, protocol values, and public-material constraints.
- [citation/prompts/](Individual%20Pipeline/citation/prompts/): generated Citation Generator and
  Citation Verifier views.
- [verifiers/cli.py](Individual%20Pipeline/verifiers/cli.py): mock, individual
  API stage, full API cascade, and manual-replay command surface.
- [verifiers/api_smoke.py](Individual%20Pipeline/verifiers/api_smoke.py):
  persisted individual-stage and full-cascade API execution.
- [verifiers/orchestrator.py](Individual%20Pipeline/verifiers/orchestrator.py):
  deterministic standalone routing and offline mock cascade.
- [verifiers/api_runners.py](Individual%20Pipeline/verifiers/api_runners.py): A/Composer/B/C prompt
  assembly.
- [verifiers/api_client.py](Individual%20Pipeline/verifiers/api_client.py) and
  [api_config.py](Individual%20Pipeline/verifiers/api_config.py): optional
  OpenAI-backed calls and non-secret runtime configuration.
- [verifiers/parsers.py](Individual%20Pipeline/verifiers/parsers.py): verifier report parsing.
- [verifiers/guidance_handoff.py](Individual%20Pipeline/verifiers/guidance_handoff.py):
  validated next-solver guidance artifact creation.
- [verifiers/manual_replay.py](Individual%20Pipeline/verifiers/manual_replay.py):
  route saved manual reports without new model calls.
- [verifiers/mock.py](Individual%20Pipeline/verifiers/mock.py): deterministic
  standalone verifier responses.
- [verifiers/run_store.py](Individual%20Pipeline/verifiers/run_store.py) and
  [schemas.py](Individual%20Pipeline/verifiers/schemas.py): standalone verifier
  artifact persistence and typed protocol records.
- [verifiers/prompt_sync.py](Individual%20Pipeline/verifiers/prompt_sync.py): canonical prompt-copy
  compatibility command for verifier-owned views.
- [verifiers/prompts/](Individual%20Pipeline/verifiers/prompts/): generated Problem Statement,
  A/B/C, Composer A, and Final Checker views.
- [verifiers/SubPipeline_Verifiers.md](Individual%20Pipeline/verifiers/SubPipeline_Verifiers.md):
  detailed standalone verifier protocol notes.

</details>

<details>
<summary><strong>Canonical prompt ownership</strong> — where role contracts live and how generated views stay synchronized</summary>

### Canonical prompt ownership

- [Prompt Packet/Prompts.md](Prompt%20Packet/Prompts.md): canonical no-internet
  S0-S6, citation, verifier, controller, and Final Checker packet.
- [Prompt Packet/PromptsWithFullInternet.md](Prompt%20Packet/PromptsWithFullInternet.md):
  canonical source-supported solver packet.
- [Prompt Packet/FlowChart.md](Prompt%20Packet/FlowChart.md): implemented runtime
  order and exits, plus explicitly marked manual/standalone protocol paths.
- [prompt_sync.py](prompt_sync.py): the repository-wide generator and drift
  checker for the component-owned prompt views listed above.

Edit canonical prompt text in `Prompt Packet/`, then regenerate its component
views. Do not hand-edit generated prompt copies.

</details>

<details>
<summary><strong>Verification</strong> — offline integrity, routing, parser, prompt, and documentation tests</summary>

### Verification

- [tests/test_solver_bundle.py](tests/test_solver_bundle.py): package imports,
  both prompt modes, citation gate, and terminal mock runs.
- [tests/test_target_integrity.py](tests/test_target_integrity.py): stable
  statement identity, source/proof provenance, frozen targets, and bridge
  rejection behavior.
- [tests/test_documentation_links.py](tests/test_documentation_links.py): local
  paths, image targets, and section anchors resolve; all public READMEs are
  included in the checked document list.
- [tests/test_solver_schedule.py](tests/test_solver_schedule.py): key-solver-first
  execution in both prompt modes, early stops, and documented citation output paths.
- [tests/test_historical_reports.py](tests/test_historical_reports.py): imported
  target records match the final-branch snapshot; counts, rates, unique targets,
  and README summaries stay consistent.
- [tests/test_results_charts.py](tests/test_results_charts.py): chart values,
  generated-file drift, accessible SVG labels, and subject coverage of the exact
  paper collection.
- [tests/test_paired_results.py](tests/test_paired_results.py): target matching,
  documented renumbering, excluded records, manual passes, and subject counts.
- [tests/verifier_pipeline/](tests/verifier_pipeline/): mock, parser,
  prompt-sync, and mocked API cascade tests.
- [tests/test_prompt_views.py](tests/test_prompt_views.py): repository-wide
  component prompt ownership and drift checks.
- [tests/test_pipeline_gates.py](tests/test_pipeline_gates.py): offline
  Problem Statement, skeleton-source, and cleaner-bridge hard-gate tests.

The verifier sub-suite is split into
[API execution](tests/verifier_pipeline/test_api_smoke.py),
[mock prompt formatting](tests/verifier_pipeline/test_mock_prompt_format.py),
[routing](tests/verifier_pipeline/test_orchestrator.py),
[report parsing](tests/verifier_pipeline/test_parsers.py), and
[prompt-copy drift](tests/verifier_pipeline/test_prompt_copies.py).

</details>

<details>
<summary><strong>Keeping this map current</strong> — two checks maintain links and prompt ownership</summary>

### Keeping this map current

Run these checks after moving code, changing prompt ownership, or adding a new
public entry point:

```bash
python3 -B prompt_sync.py --check
PYTHONPATH='Individual Pipeline' \
  python3 -B -m unittest discover -s tests -p 'test*.py'
```

`tests/test_documentation_links.py` checks the source map, root guides,
component READMEs, the Mini HTML walkthrough, input/output contracts, and
public-results documentation. It checks local paths and section anchors and
flags public READMEs missing from its coverage list.
Responsibility descriptions still require review when modules are added,
renamed, or split; avoiding fixed line-number links prevents ordinary code
movement from creating silent documentation drift.

</details>
