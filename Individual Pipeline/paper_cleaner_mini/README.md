# Paper Cleaner Mini

Paper Cleaner Mini prepares the context a solver needs for one theorem:
definitions, assumptions, and supporting results, with their proofs removed.

It runs **after Paper Cleaner**, which reads the whole paper and selects the
targets through Step 5. Mini handles one selected theorem at a time:

```text
whole-paper index + selected target
    -> Mini author/check/repair
    -> independent Mini audit
    -> source-checked solver bundle
    -> S0-S6
```

Paper Cleaner chooses **which theorem to attempt**; Mini chooses **what context
the solver can use**. See the
[whole-paper cleaner guide](../paper_cleaner/README.md#paper-cleaner-versus-paper-cleaner-mini)
for a side-by-side comparison and the older Steps 6–8.

An author model drafts the context, a checker reviews it, and a repair model
fixes any problems. Code keeps the target statement unchanged and decides
whether the package passes.

Mini can read the original proof while choosing context; the solver cannot.
The finished input is checked for proof leakage, though these checks cannot
rule out every indirect hint. This is the `target_scoped_proof_informed` setup,
not preparation done without seeing the proof.

## Run it

From the repository root, after installing `.[pipeline]`:

```bash
export OPENAI_API_KEY='...'
ARXIV=2604.04891 ./Commands/run_mini_from_arxiv.sh
```

This runs Paper Cleaner through Step 5, prepares every selected main or hardest
target with Mini, and runs a separate audit. Inputs go to
`Inputs/paper_cleaner_input/`; Mini outputs go to `Outputs/mini/`. Both are
ignored by Git.

To process one selected target, run from this component directory:

```bash
python run.py \
  --arxiv 2604.04891 \
  --target-id stmt-a83f71c209d4
```

Replace the example target ID with one from the paper's `roles/selection.json`.

Inspect the subprocess commands without downloading a paper or calling a
model:

```bash
python run.py --arxiv 2604.04891 --print-plan
```

## What happens to one target

1. The author writes Sections 0-5 of `problem.md` from the full paper.
2. The controller appends the frozen source statement as Section 6.
3. Code checks the structure, target, macros, proof leakage, and Section 3 sources.
4. The checker looks for missing context and leaked proof material.
5. If the checker finds a repairable problem, the repair role revises Sections
   0-5 and the checks run again.
6. A separate audit rechecks the finished package and its hashes.

Mini allows two repair rounds by default. A package that still fails goes into
`excluded.json` rather than to the solver.

The models cannot edit `target.tex`, `target.json`, or Section 6. On a retry,
Mini validates those frozen artifacts rather than replacing them.

## Inputs and outputs

Prepared input for one paper is:

```text
inputs/<paper-id>/
  source/flat.tex
  source/meta.json
  index/statements.v2.json
  roles/selection.json
```

The package for one target is written under:

```text
runs/<paper-id>/packages/<target-id>/stage2/
  problem.md
  target.tex
  target.json
```

`problem.md` has seven sections:

| Section | Contents |
|---:|---|
| 0 | required LaTeX macros |
| 1 | notation and conventions |
| 2 | standing assumptions |
| 3 | external results, each with an immediate source label |
| 4 | definitions |
| 5 | permitted results from the same paper, without their proofs |
| 6 | the exact target statement, inserted by code |

The stage report and separate audit record which exact files they checked,
using file hashes. A model's approval cannot override a failed code check.

## Run from existing prepared inputs

From `Individual Pipeline/paper_cleaner_mini/`:

```bash
# List planned targets without model calls
python stage2.py --papers all --dry-run

# Build all selected targets already present under inputs/
python stage2.py --papers all

# Audit the resulting packages
python audit.py --papers all --effort high
```

For one target with a nonzero exit code on any audit failure:

```bash
python stage2.py \
  --papers <paper-id> \
  --target-id <target-id> \
  --src-runs inputs \
  --out runs

python audit.py \
  --papers <paper-id> \
  --target-id <target-id> \
  --runs-dir runs \
  --fail-on-package-issues
```

Use `--fail-on-package-issues` in scripts: the command succeeds only if the
selected package passes the audit and matches its recorded hashes.

## Hand the package to S0-S6

Use the [command guide](../../Commands/README.md) to run the full workflow.
The `run-cleaner-solver` command runs these steps in order:

1. prepare, check, and repair the Mini packet;
2. audit the finished packet separately;
3. check sources for the external results in Section 3;
4. export the solver's input files;
5. run S0-S6, then the statement, source, and proof reviews.

The exported public bundle contains:

```text
target.md
skeleton.md
allowed_support.md
guidance.md
bibliography.bib          optional
setup_manifest.json
```

Private gold proof and full-source files are excluded unless the caller
explicitly enables the private Final Checker.

## Cost and privacy

- `--model` selects the author and repair model.
- `--check-model` can use a different checker model.
- `--audit-model` selects the independent auditor.
- `--parallel` controls whole-paper concurrency; the default is 2.
- `--max-repairs` controls the bounded repair loop; the default is 2.

The prompts can contain the full paper, so API calls may be large. Use
`--print-plan` to check the settings, and start with one target. Cached calls
can be reused; check the provider's usage records for actual costs.

Do not publish `inputs/`, `runs/`, or `Outputs/mini/` wholesale. They can
contain paper text, reference proofs, raw model responses, and audit material.

## Files in this component

| Path | Purpose |
|---|---|
| `run.py` | arXiv input, upstream preparation, Mini, and audit wrapper |
| `stage2.py` | author/check/repair loop |
| `audit.py` | independent package and exclusion audit |
| `audit_gate.py` | hard-pass predicate used by commands and tests |
| `package_validation.py` | target, structure, macro, and Section 3 checks |
| `minilib.py` | configuration, schemas, caching, and model-call support |
| `compare_audits.py` | compare two audit reports |
| `config.yaml` | model and runtime settings |
| `prompts/` | author, checker, repair, and audit prompts |

The component also includes a [control-flow walkthrough](docs/architecture.html)
to open locally in a browser (GitHub displays HTML source, not a live page).
For source preparation and target selection, see
[Paper Cleaner](../paper_cleaner/README.md).
