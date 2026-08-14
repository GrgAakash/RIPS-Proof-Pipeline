# Paper Cleaner Mini

**In one sentence: a minimal counterpart to the main repo's 8-step graph pipeline — three strong-model roles that each hold the full paper (author / adversarial checker / repairer) generate "prove this theorem" problem packages in the same format, with the same independent audit acting as referee.**

The core author/check/repair pipeline is **self-contained**: its support code lives in local
`minilib.py`, `audit_gate.py`, and `package_validation.py`; its prompts and
LaTeX whitelist are bundled. It runs even if you delete the main repo's
`paper_cleaner/`. (Note: `inputs/` is git-ignored because it contains
third-party paper text — if you cloned this from GitHub, regenerate it via the
main pipeline; see "Adding a new paper?" below.)

For a new arXiv paper, `run.py` uses the sibling `paper_cleaner/` only for
Steps 1-5: source download, flattening, statement indexing, dependency
analysis, and target selection. It deliberately stops before that pipeline's
older package-generation and verification stages, then runs Mini.

## How it works

For each target in the prepared paper's `roles/selection.json`:

```
author  (full paper in hand, target proof marked off-limits)  → editable Sections 0–5
controller (no model)                                        → append frozen Section 6
     ↓
deterministic gates: structure / target integrity / macro closure / proof-leak scan
                     (the independent audit repeats the same target checks)
     ↓
checker (full paper in hand, adversarial)                     → issues + three verdicts
     ↓ not passed
repair  (full paper in hand)                                  → revised body → back to the gates
     ↓ still failing after --max-repairs rounds
excluded.json (reason code + unresolved items, same format as the main pipeline)
```

Ship condition: all three checker verdicts true **and** no fatal issue **and** the deterministic gates stay silent. Every Section 3 `[Rn]` grant must also carry an immediate `Source:` bibliography key or named source.

The models write and repair Sections 0–5 only. Section 6 is controller-owned
and contains no inferred theorem number: its exact source-backed statement is
appended from `statements.v2.json`. Each package also carries `target.tex` and
`target.json` with separate statement/proof hashes and source spans plus the
deterministic proof-pairing method. Mini, the independent audit, and the S0–S6
export bridge reject a model-added target, an unverified statement or proof
span, a changed target artifact, or any Section 6 drift. On a retry, Mini
validates an existing `target.tex`/`target.json` pair and never silently
overwrites it. The deterministic
Sections 0–5 check detects verbatim target duplication after whitespace
normalization; semantic paraphrases remain an adversarial-checker concern.
The main repo's 46 engineering lessons (the usage-quote ban, parameterized-notation
calibration, dangling references, statement-only grants, the ~3-line sufficiency
calibration, …) are distilled into the three prompts, not into code.

## Quick start

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
export OPENAI_API_KEY=sk-...

.venv/bin/python stage2.py --papers all --dry-run   # see the plan, spend nothing
.venv/bin/python stage2.py --papers all             # run all locally prepared papers
.venv/bin/python audit.py  --papers all --effort high   # independent audit referee
.venv/bin/python compare_audits.py <main-pipeline-audit.json> runs/audit/audit_report.json \
    --label-a pipeline-v2.3 --label-b stage2-min-source-v2    # optional comparison
```

For a new paper, an arXiv ID or arxiv.org link is the only mathematical input:

```bash
.venv/bin/python run.py --arxiv 2604.04891
.venv/bin/python run.py --arxiv https://arxiv.org/abs/2604.04891
```

This prepares the source through upstream Step 5, processes every target in
`mains union hardest`, and runs the independent Mini audit. To enforce exactly
one selected theorem instead:

```bash
.venv/bin/python run.py --arxiv 2604.04891 --target-id stmt-a83f71c209d4
```

Use `--print-plan` to inspect all three subprocess commands without network or
model calls. Paper content lands under ignored `inputs/`; Mini artifacts land
under ignored `runs/`. An API key in `OPENAI_API_KEY` and network access are
still operational requirements, not mathematical inputs.

- All LLM calls are cached under `runs/<id>/cache/`; after an interruption, **re-running the same command does not bill twice**.
- `--papers <paper-id>` runs one locally prepared paper as a smaller trial.
- `--check-model <model>` runs the adversarial checker on a different model than
  author/repair (default: same as `--model`) — useful against same-model blind spots.
- The prompts carry the whole paper, so TPM is the bottleneck: keep `--parallel` at the default 2.

For one solver-bound target, always select it explicitly and enforce the
independent audit gate:

```bash
.venv/bin/python stage2.py --papers <paper-id> --target-id <target-id> \
  --src-runs inputs --out runs
.venv/bin/python audit.py --papers <paper-id> --target-id <target-id> \
  --runs-dir runs --fail-on-package-issues
```

The stage-2 report and audit record bind their decisions to the exact
`problem.md` SHA-256 and frozen target SHA-256. `--fail-on-package-issues` returns nonzero unless exactly
one selected package is self-contained, leak-free, sufficient, free of fatal
issues, deterministic leak spans, and unknown commands, and its hash matches.

## Solver integration

The main CLI treats Mini as the primary target-specific skeleton generator.
After stage 2 and the independent audit pass, this command performs the
restricted-web Section 3 source gate and exports the solver-native bundle:

```bash
PYTHONPATH='Individual Pipeline' python3 -m solver.cli prepare-cleaner-problem \
  --cleaner-runs-dir 'Individual Pipeline/paper_cleaner_mini/runs' \
  --paper-id <paper-id> \
  --target-id <target-id> \
  --packet-file "Prompt Packet/Prompts.md" \
  --output-dir prepared/<paper-id>/<target-id> \
  --run-tag protocol_validation \
  --client openai
```

Use `run-cleaner-solver` to run stage 2, the enforced audit, source gate,
export, and the existing S0-S6 runner in order. Solver options follow `--`:

```bash
PYTHONPATH='Individual Pipeline' python3 -m solver.cli run-cleaner-solver \
  --cleaner-dir 'Individual Pipeline/paper_cleaner_mini' \
  --cleaner-input-root 'Individual Pipeline/paper_cleaner_mini/inputs' \
  --cleaner-work-root 'Individual Pipeline/paper_cleaner_mini/runs' \
  --prepared-dir prepared/<paper-id>/<target-id> \
  --solver-run-dir runs/<run-name>/solver \
  --paper-id <paper-id> \
  --target-id <target-id> \
  --packet-file "Prompt Packet/PromptsWithFullInternet.md" \
  --run-tag protocol_validation \
  --client openai \
  --cleaner-model gpt-5.5 \
  --cleaner-audit-model gpt-5.5 \
  --reasoning-effort high \
  -- --model gpt-5.5 --max-rounds 12 --solver-workers 1
```

The canonical packet marker selects solver browsing automatically:
`Prompts.md` is no-internet, while `PromptsWithFullInternet.md` is
source-supported. The pre-solver source gate always requires restricted web
search when Section 3 is nonempty; it records `NOT_APPLICABLE` and makes no
calls when Section 3 has no grants.

Preparation is idempotent before billing: an existing bundle with the same
package, packet, model, tags, gate decision, and file hashes is reused without
another source-gate call. Any mismatch requires a fresh output directory.

The prepared package is deliberately labeled
`target_scoped_proof_informed`. It is not experimentally identical to the old
full-paper proof-stripped skeleton path: Mini sees the target proof while
choosing prerequisites, then the leak checks prevent that proof from entering
the exported skeleton.

## Layout

```
paper_cleaner_mini/
├── run.py               arXiv ID/URL → upstream Steps 1-5 → Mini → audit
├── stage2.py            main flow: author → gates → checker → repair
├── audit.py             independent calibration audit (same logic and prompts as the main repo's audit.py)
├── audit_gate.py        dependency-free hard-pass predicate shared with tests
├── package_validation.py deterministic target-integrity and Section 3 source gates
├── compare_audits.py    side-by-side comparison of two audit reports
├── minilib.py           all supporting code: config / context / LLM layer / schemas / deterministic checks
├── config.yaml          model parameters, concurrency, cache switch
├── prompts/             s2_author / s2_check / s2_repair / audit_pkg / audit_excl
├── data/latex_std_commands.txt   whitelist of standard LaTeX commands
├── inputs/<paper>/      generated inputs from a completed main-pipeline run (git-ignored):
│   ├── source/flat.tex        the flattened full paper
│   ├── source/meta.json       title / domain baseline
│   ├── index/statements.v2.json  source spans/hashes, target statement + proof, macros, scan whitelist
│   └── roles/selection.json   selection results (mains ∪ hardest = the attack targets)
└── runs/                output (layout-compatible with the main pipeline; contains paper content — do not publish)
    └── <paper>/packages/<target>/stage2/
        ├── problem.md       seven-section problem; Section 6 is controller-owned
        ├── target.tex       exact indexed target statement
        └── target.json      statement/proof hashes, spans, and proof pairing
```

## Fair-comparison conventions vs the main pipeline

- **Same targets**: reuses the main pipeline's selection.json verbatim — no re-selection.
  The variable the experiment isolates is "packaging + verification", not selection.
- **Same referee**: audit.py's prompts / schema / deterministic scans are byte-identical
  to the main repo's; the two runs layouts are mutually compatible, and the main repo's
  audit.py can point `--runs-dir` straight at this folder's `runs/`.
- **One place where mini is judged more strictly**: the Section-3 50-character leak scan.
  The main pipeline whitelists its reviewed external grants; mini has no ExternalDep
  records, so its whitelist is empty.
- **Caveat**: author / checker / referee are all gpt-5.5 (so are the main pipeline's
  a0/a6/a7), so shared model blind spots inflate both sides' scores equally — the
  comparison is valid, the absolute numbers are questionable; spot-check by hand.

## Adding a new paper?

The preferred route is now `python run.py --arxiv <id-or-url>`, which creates
the inputs below automatically.

The four files under `inputs/` are produced by the main pipeline's
step1/step2/step3/step5 (download, parse, index backfill, selection). To add a
paper, run the main repo through step 5 and copy those four files into
`inputs/<arxiv-id>/`, or supply files with the same schema yourself. Mini
deliberately leaves this part out — it is the comparison arm of an experiment,
not a full replacement (for now).

## Diagrams

A visual walkthrough of the architecture and the per-target control flow lives in
[docs/architecture.html](docs/architecture.html) (data flow, control-flow chart,
the three roles' division of labor, deterministic-gate details, experiment evidence).

## Experiment background

Design motivation and judging rules: see the main repo's `docs/stage2-experiment.md`.
Baseline (Stage-1 pipeline, audited 2026-07-05): 13 shipped + 6 excluded; the audit
found 1 package fully clean, 4–6 packages carrying fatal issues, and disputed
false kills among the exclusions.
