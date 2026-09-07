# Paper Cleaner

Paper Cleaner retrieves a paper, builds a source-backed statement index, traces
dependencies, and selects candidate target theorems.

For the current RIPS workflow, its normal job ends at **Step 5**. Paper Cleaner
Mini takes the selected target from there and builds the solver-facing theorem
packet. Steps 6-8 remain available for older cleaner experiments, but they are
not the packaging route used by the repository's end-to-end commands.

## Paper Cleaner versus Paper Cleaner Mini

Despite the name, Mini is not a lightweight alternative to Paper Cleaner. The
two components run in sequence:

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

In other words, Paper Cleaner answers **which theorem is being attempted and
where it came from**. Mini answers **what the solver may know while attempting
that exact theorem**. Mini does not select a different target, and the models
inside Mini cannot rewrite the frozen target statement.

The non-mini cleaner can still continue through its older Steps 6-8 when run
without `--stop-after step5`. That is a retained legacy workflow, not the
current integrated route into S0-S6.

> [!CAUTION]
> Cleaner run directories contain third-party paper text, reference proofs, and
> raw model responses. They are ignored by Git. Do not publish a run directory
> wholesale.

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

The two files worth opening first are:

- `roles/selection.json`, which lists the selected `mains` and `hardest`
  target IDs;
- `index/statements.v2.json`, which records each statement, its source span,
  hashes, and paired proof evidence.

Target IDs are intentionally opaque—for example, `stmt-a83f71c209d4`. The
cleaner does not guess LaTeX theorem numbering.

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

Models may propose contextual entries, dependency edges, or target
nominations. Code owns the target identity and every control-flow decision.

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

Running without `--stop-after step5` executes the retained full eight-stage
cleaner:

```text
1 source retrieval       5 target selection
2 structural parsing     6 legacy package assembly
3 index completion       7 legacy verification and repair
4 dependency extraction  8 reports and dashboards
```

That route writes manifests and theorem packages under `runs/<paper-id>/`. Do
not confuse those legacy packages with the target-scoped Mini packages used by
the integrated solver.

## Target integrity

A target is eligible only when the cleaner can bind it to an exact source file
and span. The statement and its paired proof receive separate hashes and
provenance records. An explicit proof title that cannot be resolved is recorded
as unresolved; it does not fall back to proximity. Untitled proofs may be
paired by strict source adjacency.

Later packaging stages freeze the selected statement in `target.tex`,
`target.json`, and Section 6 of `problem.md`. Missing hashes, changed source
slices, or target drift are hard failures.

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

Steps use input fingerprints and model calls use a cache. Re-running the same
command can reuse compatible work. Changes to prompts, configuration, inputs,
or cache state may trigger new API calls, so provider telemetry remains the
source of truth for cost.

If a paper produces no package, inspect `status.json` and `excluded.json`
before treating that as a property of the mathematics. It may instead indicate
missing context, source evidence, an audit failure, or a pipeline defect.

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
