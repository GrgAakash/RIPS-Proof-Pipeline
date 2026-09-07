# Paper Cleaner Mini

Paper Cleaner Mini turns one selected theorem into the public packet consumed
by S0-S6. It is the repository's current packaging path.

**Mini is the second cleaner stage, not a smaller replacement for Paper
Cleaner.** Paper Cleaner first processes the whole paper through Step 5 and
selects source-backed target IDs. Mini then handles one of those targets at a
time:

```text
whole-paper index + selected target
    -> Mini author/check/repair
    -> independent Mini audit
    -> source-checked solver bundle
    -> S0-S6
```

Paper Cleaner determines **what theorem is being attempted**. Mini determines
**what context the solver is allowed to use for that theorem**. See the
[whole-paper cleaner guide](../paper_cleaner/README.md#paper-cleaner-versus-paper-cleaner-mini)
for the side-by-side boundary and the retained legacy Steps 6-8.

Mini receives the full paper and a source-backed target selected by Paper
Cleaner. An author model chooses the necessary context, a checker challenges
the draft, and a repair model addresses concrete failures. Code—not a
model—owns the target statement and the decision to ship or exclude the
package.

> [!IMPORTANT]
> Mini is `target_scoped_proof_informed`: its authoring roles can inspect the
> target's source proof while deciding which prerequisites belong in the
> packet. Checks look for proof leakage in the exported solver input; they do
> not guarantee that all indirect hints are absent. A Mini package is not
> experimentally equivalent to a proof-blind full-paper skeleton.

## Run it

From the repository root, after installing `.[pipeline]`:

```bash
export OPENAI_API_KEY='...'
ARXIV=2604.04891 ./Commands/run_mini_from_arxiv.sh
```

This prepares the paper through upstream Step 5, runs Mini on every selected
main or hardest target, and performs the independent Mini audit. Inputs go to
`Inputs/paper_cleaner_input/`; Mini outputs go to `Outputs/mini/`. Both are
ignored by Git.

To process one selected target, run from this component directory:

```bash
python run.py \
  --arxiv 2604.04891 \
  --target-id stmt-a83f71c209d4
```

Inspect the subprocess commands without downloading a paper or calling a
model:

```bash
python run.py --arxiv 2604.04891 --print-plan
```

## What happens to one target

1. The author writes Sections 0-5 of `problem.md` from the full paper.
2. The controller appends the frozen source statement as Section 6.
3. Deterministic checks reject structural errors, target drift, unknown macros,
   obvious proof leakage, or malformed Section 3 grants.
4. The checker reviews self-containment, sufficiency, and leakage.
5. If the checker finds a repairable problem, the repair role revises Sections
   0-5 and the checks run again.
6. A separate audit rechecks the finished package and its hashes.

The default repair budget is two rounds. A package that still fails is listed
in `excluded.json`; it is not silently promoted to solver input.

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

The stage report and independent audit bind their decisions to the exact
package and target hashes. A passing model opinion cannot override a failed
deterministic check.

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

`--fail-on-package-issues` is the useful automation boundary: it succeeds only
when the selected package passes the independent audit and matches the recorded
hashes.

## Hand the package to S0-S6

The supported end-to-end commands are documented in
[Commands/README.md](../../Commands/README.md). The integrated
`run-cleaner-solver` route performs, in order:

1. Mini author/check/repair;
2. independent package audit;
3. restricted source verification for Section 3 grants;
4. deterministic solver-bundle export;
5. S0-S6 and the downstream evidence gates.

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

The prompts can contain the full paper, so API calls may be large. Run
`--print-plan`, verify the model and output directories, and start with one
target. Compatible calls are cached, but provider telemetry—not the cache—is
the billing record.

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
