# Command guide

The scripts in this directory are the stable entry points for paper preparation
and integrated runs. They resolve the repository root from their own location,
so they may be called from any working directory.

> [!CAUTION]
> Every command in the table below except the offline tests and mock clients can
> make paid API calls. Review the model, internet mode, private-data setting,
> and output directory before starting a run.

## Command matrix

| Command | Purpose | Required values | Default output |
|---|---|---|---|
| `prepare_paper_input.sh` | Fetch and prepare one paper through cleaner Step 5 | `OPENAI_API_KEY`, `ARXIV` | `Inputs/paper_cleaner_input/<paper-id>/` |
| `run_mini_from_arxiv.sh` | Prepare through Step 5, then run Mini and its audit | `OPENAI_API_KEY`, `ARXIV` | `Inputs/paper_cleaner_input/` and `Outputs/mini/` |
| `run_no_internet.sh` | Run the integrated pipeline with closed-book S0-S6 | `OPENAI_API_KEY`, `PAPER_ID`, `TARGET_ID` | `Outputs/<run-name>/` |
| `run_full_internet.sh` | Run the integrated pipeline with hosted search for S0-S6 | `OPENAI_API_KEY`, `PAPER_ID`, `TARGET_ID` | `Outputs/<run-name>/` |

The “no internet” label applies to S0-S6. The pre-solver source gate and
post-proof citation gate may still use restricted source checking.

`run_mini_from_arxiv.sh` is a self-contained convenience command: it invokes
the full-paper cleaner through Step 5 before starting Mini. If those inputs
already exist, the integrated target commands reuse them and begin with Mini.

## Recommended workflow

### 1. Prepare a paper

```bash
export OPENAI_API_KEY='...'
ARXIV=2606.16585 ./Commands/prepare_paper_input.sh
```

Inspect `Inputs/paper_cleaner_input/2606.16585/roles/selection.json` and choose
one source-backed target ID of the form `stmt-...`.

### 2. Run one target

```bash
PAPER_ID=2606.16585 \
TARGET_ID=stmt-a83f71c209d4 \
RUN_NAME=2606.16585_stmt-a83f71c209d4_no_internet \
  ./Commands/run_no_internet.sh
```

Replace the final command with `run_full_internet.sh` for source-supported
solver browsing.

### 3. Inspect the terminal evidence

Begin with:

```text
Outputs/<run-name>/solver/<problem-id>/state.json
Outputs/<run-name>/solver/<problem-id>/round_NNN/
```

Do not infer acceptance from the presence of `S6.md` or `final_proof.md` alone.
Read the terminal status and the gate artifacts that were actually produced.

## Environment variables

| Variable | Default | Meaning |
|---|---|---|
| `PYTHON_BIN` | `python3` | Python executable used by the wrapper |
| `MODEL` | `gpt-5.5` | Cleaner, source-audit, and solver model |
| `RUN_NAME` | derived from paper, target, and mode | Input/output namespace |
| `RUN_TAG` | `paper_original_result` | Run provenance label |
| `SOLVER_WORKERS` | `2` | Parallel S1-S5 API calls |
| `SOLVER_DELAY_SECONDS` | `0` | Delay between solver calls |
| `MAX_ROUNDS` | `3` | Main solver-round ceiling |
| `MAX_BRANCH_DEPTH` | `2` | Maximum nested branch depth |
| `MAX_BRANCHES` | `3` | Branch budget |
| `CITATION_MODEL` | value of `MODEL` | Citation Generator/Verifier model |
| `CITATION_MAX_ATTEMPTS` | `2` | Citation-gate attempt ceiling |
| `CITATION_WEB_SEARCH_CONTEXT_SIZE` | `medium` | Hosted-search context size for citation checks |
| `INCLUDE_PRIVATE_FINAL_CHECKER` | `1` | Include isolated gold/source material for the final check |

Set `INCLUDE_PRIVATE_FINAL_CHECKER=0` when the run must remain public-only. In
that mode the strongest possible terminal label is cascade-only acceptance.

## Cost and privacy boundary

- Preparation, Mini, source checking, solver, citation, and verifier roles may
  each generate model usage.
- Increasing parallelism does not reduce token consumption and may increase
  rate-limit retries.
- Prepared inputs and outputs can contain third-party paper text and raw model
  responses; their workspaces are ignored by Git.
- Private gold proofs and full source belong only in the ignored private bundle
  used by the Final Checker.
- Never place credentials in command history, committed files, run reports, or
  bug reports.

For a zero-cost first check, use the offline mock and regression commands in
the [root README](../README.md#quick-start).
