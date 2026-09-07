# Paper Cleaner

Paper Cleaner reads a mathematics paper and identifies the theorems you can
ask the solver to reconstruct. It records each statement, where it appears,
and which earlier results it depends on.

The current workflow uses **Steps 1–5** to prepare the paper and select a
theorem. Paper Cleaner Mini then prepares the input for that theorem.

## Paper Cleaner versus Paper Cleaner Mini

Use both components, in this order. “Mini” refers to its one-theorem scope,
not a cheaper or smaller replacement for the first cleaner:

```text
paper or PDF
    -> Paper Cleaner Steps 1-5
    -> selected target ID
    -> Paper Cleaner Mini
    -> audited target packet
    -> source gate and S0-S6
```

| Component | Scope | Decides or produces |
|---|---|---|
| **Paper Cleaner** | the whole paper | normalized source, statement index, dependencies, and selected target IDs |
| **Paper Cleaner Mini** | one selected target at a time | the definitions, assumptions, and permitted prior results supplied to the solver |

Paper Cleaner answers **which theorem to attempt**. Mini answers **what context
the solver can use**. Mini keeps the selected theorem unchanged.

The older Steps 6–8 are still available for standalone cleaner runs. The
end-to-end commands use Mini instead of those steps.

## Normal use

Install the repository once from its root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[pipeline]'
```

Then prepare one arXiv paper through target selection:

```bash
export OPENAI_API_KEY='...'
ARXIV=2606.16585 ./Commands/prepare_paper_input.sh
```

The command writes to:

```text
Inputs/paper_cleaner_input/<paper-id>/
  source/flat.tex
  source/meta.json
  index/statements.v2.json
  roles/selection.json
  status.json
  logs/run.jsonl
```

Open these two files first:

- `roles/selection.json`, which lists the selected `mains` and `hardest`
  target IDs;
- `index/statements.v2.json`, which records each statement, its source span,
  hashes, and paired proof evidence.

An ID such as `stmt-a83f71c209d4` identifies a statement in the source. It is
not a guessed LaTeX theorem number.

Continue with [Paper Cleaner Mini](../paper_cleaner_mini/README.md) after
choosing a target ID.

## What the five preparation steps do

1. **Fetch and flatten the source.** Prefer arXiv LaTeX; use the configured OCR
   route only for a local PDF.
2. **Index the mathematics.** Locate statements, definitions, proofs, source
   spans, and hashes.
3. **Fill parser gaps.** Recover notation or declarations that appear in prose.
4. **Trace dependencies.** Build the statement-dependency graph.
5. **Select targets.** Record the main and difficult results eligible for later
   packaging.

Models suggest missing context, dependencies, and targets. Code checks the
source identity and decides whether each stage can continue.

## Direct commands

Run these from `Individual Pipeline/paper_cleaner/` with the root environment
active:

```bash
# One arXiv paper, stopping at the handoff used by Mini
python run.py --arxiv 2604.04891 --stop-after step5

# A batch file containing one arXiv ID per line
python run.py --ids /path/to/papers.txt --stop-after step5

# A local PDF; requires the OCR command configured in config.yaml
python run.py --pdf /path/to/paper.pdf --paper-id local-paper --stop-after step5
```

Useful options are `--config PATH`, `--runs-dir PATH`, and
`--stop-after step1` through `step8`. Run `python run.py --help` for the
current argument list.

With no `--stop-after` option, the cleaner runs all eight stages:

```text
1 source retrieval       5 target selection
2 structural parsing     6 legacy package assembly
3 index completion       7 legacy verification and repair
4 dependency extraction  8 reports and dashboards
```

That older route saves its packages under `runs/<paper-id>/`. They are separate
from the Mini packages used by the integrated solver.

## Target integrity

A target must match an exact passage in a source file. The cleaner records
separate hashes for the statement and its proof so later checks can detect
changes. If a proof names a theorem that cannot be identified, the pairing is
left unresolved. An untitled proof may be paired only by strict source
adjacency.

Packaging copies the selected statement into `target.tex`, `target.json`, and
Section 6 of `problem.md`. Missing hashes, changed source text, or a changed
target stop the run.

## Reading and resuming a run

For a full eight-stage run, start with:

| File | Use it for |
|---|---|
| `runs/index.html` | batch navigation |
| `runs/<paper>/status.json` | completed, rejected, or failed stage |
| `runs/<paper>/manifest.json` | packages that actually shipped |
| `runs/<paper>/excluded.json` | rejected targets and reason codes |
| `runs/<paper>/logs/run.jsonl` | provider errors and detailed diagnostics |
| `runs/<paper>/report/dashboard.html` | paper-level summary |

Rerunning the same command can reuse cached work. Changes to prompts, settings,
inputs, or the cache may trigger new API calls; check the provider's usage
records for actual costs.

If no package was produced, read `status.json` and `excluded.json` for the
reason. Missing source material or a failed check is different from a solver
failing to prove the theorem.

Run directories can contain paper text, reference proofs, and raw model
responses. Git ignores them; review individual files before sharing them.

## Files in this component

| Path | Purpose |
|---|---|
| `run.py` | eight-stage orchestrator and resume logic |
| `audit.py` | independent package and exclusion audit |
| `config.yaml` | providers, models, limits, selection, OCR, and parallelism |
| `src/step1_get_source.py` | retrieval and source normalization |
| `src/step2_parse.py` | structural and proof indexing |
| `src/step3_fill_index.py` | contextual index completion |
| `src/step4_deps.py` | dependency extraction |
| `src/step5_select_mains.py` | target selection |
| `src/step6_package.py` | retained full-cleaner packaging |
| `src/step7_verify.py` | retained review and repair stages |
| `src/step8_report.py` | manifests, dashboards, and reports |
| `src/target_integrity.py` | opaque IDs, source hashes, and frozen-target checks |

## Checks

From the repository root:

```bash
PYTHONPATH='Individual Pipeline' \
  python -m unittest discover -s tests -p 'test*.py'

python prompt_sync.py --check
```

For installation, end-to-end commands, and artifact interpretation, use the
[project README](../../README.md), [command guide](../../Commands/README.md),
and [source map](../../SOURCE_MAP.md).
