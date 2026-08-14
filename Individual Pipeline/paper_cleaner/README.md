# Paper Cleaner v2.3

**In one sentence: give it an arXiv math paper, and it automatically turns the paper's most important theorems into standalone "exam problems" — each problem ships with every definition, notation convention, and known result its proof needs, never leaks the proof itself, and is delivered only after passing three independent automated checks.**

Each generated problem (a `problem.md` file) can be handed directly to a human or an AI: "prove this theorem." The recipient does not need the original paper — everything required is already in the problem — and nowhere in the problem is there a chance to "copy the answer."

The pipeline runs with no human in the loop. When it is not confident in a problem's quality, it prefers shipping nothing over shipping a broken problem — and every dropped problem has its reason recorded, so it can be traced afterwards.

---

## Contents

- [What does this project do?](#what-does-this-project-do)
- [How does it work? (8 steps)](#how-does-it-work-8-steps)
- [What you need before running](#what-you-need-before-running)
- [Quick start: five commands to process your first paper](#quick-start-five-commands-to-process-your-first-paper)
- [Three input modes](#three-input-modes)
- [Reading the results: a complete guide to the output files](#reading-the-results-a-complete-guide-to-the-output-files)
- [Resuming and saving money](#resuming-and-saving-money)
- [Common configuration (config.yaml)](#common-configuration-configyaml)
- [Running the tests](#running-the-tests)
- [FAQ](#faq)
- [Source layout](#source-layout)
- [Glossary](#glossary)
- [Further reading (for developers)](#further-reading-for-developers)

---

## What does this project do?

**The background problem.** A theorem in a math paper is almost never "standalone": its statement uses notation defined in Section 2, its proof relies on two lemmas from Section 3 and a paper-wide assumption from Section 1, and it cites a classical result from another paper. If you cut out just the theorem text and send it to someone, they cannot even get started; if you hand over the whole paper, the proof sits right after the theorem — you have shipped the answer along with the question.

**This project's solution.** For every selected theorem, three things happen automatically:

1. **Collect**: follow the "what does this theorem's proof use?" dependency relation and gather everything required — definitions, notation conventions, standing assumptions, lemmas (statement only, never the proof), and results from external references. (This "bring along whatever is needed" set is called the **dependency closure**.)
2. **Sweep for leaks**: make sure the packaged material contains no sentence that gives away the proof idea (phrases like "immediate from Lemma 3.2" must never appear).
3. **Acceptance-check**: three independent LLM inspectors review the problem in turn — **self-containment** (is every symbol and concept explained inside the problem?), **leak prevention** (does it smuggle in the answer?), **sufficiency** (compared against the paper's original proof, are all required tools provided?). Any issue triggers an automatic repair and re-review, up to the configured number of rounds (`max_verify_iters`, default 5); problems that cannot be fixed are dropped, with the reason recorded.

**Output.** Each paper yields several "problem packages", the core of each being a `problem.md` file — a self-contained Markdown document that anyone (human or AI) can start working on without the original paper. Typical use: building an evaluation set for theorem-proving ability.

**Selection policy.** By default each paper gets **5 main theorems** (the paper's core results, nominated by an LLM and cross-confirmed by programmatic signals) plus **2 hardest theorems** (chosen by a purely programmatic difficulty score; may overlap with the mains). So one paper yields at most 5–7 problems — usually fewer, because problems that fail the triple verification are removed.

---

## How does it work? (8 steps)

One run = the 8 steps below, executed in order. You never intervene manually — knowing them only helps you read the outputs and logs:

| Step | Name | What it does (plain language) | Who does the work |
|---|---|---|---|
| 1 | Fetch source | Download the paper's LaTeX source from arXiv (the author's original files); PDFs without source go through OCR | Code |
| 2 | Parse structure | Read the LaTeX and find every theorem, lemma, definition, assumption, and their proofs; assign opaque source-backed IDs and record exact source spans/hashes | Code |
| 3 | Backfill the index | Have an LLM add what the parser cannot see: informal definitions written in prose, notation declarations like "throughout, X denotes …" | LLM (A0) |
| 4 | Extract dependencies | For each statement, ask an LLM: "which other statements in the index does its statement/proof use?" — the answers form a **dependency graph** | LLM (A1), parallel |
| 5 | Select main theorems | An LLM nominates "the most important theorems of this paper"; code cross-confirms with objective signals (appears in the abstract? proof length? dependency size? …); the hardest few are additionally chosen by difficulty score | LLM (A2) + code |
| 6 | Package | For each selected theorem, walk the dependency graph to collect its dependency closure and assemble a problem draft; results cited from external papers are rewritten by an LLM into directly usable statements | Code + LLM (A3) |
| 7 | Triple verification | Three inspectors (A4a self-containment / A4b leak scan / A4c sufficiency) review each problem in turn, with automatic repairs for a bounded number of rounds; unfixable → drop the problem and record why | LLM (A4) × 3 |
| 8 | Report | Generate the human-facing material: batch overview page, per-paper dashboard, interactive dependency graph, and a selection rationale document | Code + LLM (A5) |

**One important design principle**: LLM output is only allowed to influence four kinds of things (non-target context entries, dependency-graph edges, verification verdicts, main-theorem nominations); every control-flow branch is decided by programmatic rules. A model-added statement can support a package but can never become its target.

### Target identity and immutability

The cleaner deliberately does **not** emulate LaTeX theorem counters. Papers can share counters between theorem types, reset counters, or use custom numbering, so a structural parser must not invent labels such as “Theorem 4.1.” Every parsed statement instead receives an opaque deterministic ID such as `stmt-a83f71c209d4`, derived from its source label when available and otherwise from its exact source text. Paper theorem numbers are not stored in the new index and are neither IDs, graph edges, target-selection inputs, nor public target headings.

Only a deterministic parser entry with a valid source file, exact source span, statement hash, and source-slice hash is target-eligible. Its reference proof must separately have an exact source span, proof hash, source-slice hash, and a deterministic pairing method; an unresolved titled proof is orphaned instead of attached by adjacency. For each package the controller writes the exact statement to `target.tex`, records statement and proof provenance in `target.json`, and owns Section 6 of `problem.md`. Models may write or repair Sections 0–5 only. Packaging, verification, the independent audit, and the S0–S6 export bridge all reject missing hashes, changed source slices, altered target artifacts, or any Section 6 text that differs from the frozen statement. Deterministic duplication checks reject an exact whitespace-normalized copy of the target outside Section 6; semantic paraphrases remain an LLM-audit responsibility. If statement or proof extraction cannot be verified, the target is excluded rather than reconstructed.

---

## What you need before running

1. **A macOS or Linux machine** with **Python 3.11 or newer**. Check: run `python3 --version` in a terminal; any `Python 3.11.x` or above is fine.
2. **An OpenAI API key** (a secret of the form `sk-...`, obtained at [platform.openai.com](https://platform.openai.com)). The pipeline calls OpenAI models (o4-mini, gpt-4.1, gpt-5.5 — see `models.*` in `config.yaml`) and **bills by actual usage**: one paper typically triggers a hundred to several hundred model calls (three measured papers: 381 / 149 / 124 calls), and cost grows with paper length and verification rounds. For your first run, try one short paper.
3. **Network access** to arxiv.org (paper downloads) and api.openai.com (model calls).
4. (Optional) Only needed for the **local-PDF route**: install the OCR tool [nougat](https://github.com/facebookresearch/nougat) (command `nougat`) or MinerU (command `magic-pdf`). If you only process arXiv papers, skip this — nearly all arXiv papers come with LaTeX source and never touch OCR.

---

## Quick start: five commands to process your first paper

In a terminal, inside this project directory:

```bash
# ① Create an isolated Python environment (one-time)
#    A venv is a "virtual environment": everything this project installs goes
#    into the .venv folder and never touches your system Python.
python3 -m venv .venv

# ② Install the dependencies (one-time)
.venv/bin/pip install -r requirements.txt

# ③ Set your API key (repeat in every new terminal window)
#    The key lives only in this terminal's environment variables; the program
#    never writes it to any file.
export OPENAI_API_KEY=sk-your-key-here

# ④ Process one paper (replace the id with the arXiv id you want)
.venv/bin/python run.py --arxiv 2604.04891

# ⑤ When it finishes, open the overview page in a browser
open runs/index.html
```

**What you will see while it runs**: live progress on the terminal (stderr) — each step's start/end and duration, one line per real LLM call (task name, model, duration, token counts; cache hits are silent), the `a0 12/40` / `a1 17/76` completion counters in steps 3–4, per-package draft sizes in step 6, per-round `gaps/miss/leaks` counts in step 7, and the final `✓ shipped` / `✗ excluded` verdicts. At the end it prints `[time] 2604.04891: ok` plus a one-line JSON summary. `ok` means the paper completed; for `rejected` / `failed` see the [FAQ](#faq). Set `PAPER_CLEANER_PROGRESS=0` to silence progress output.

**If the run gets interrupted** (network drop, Ctrl-C, laptop sleep): just **re-run the exact command from step ④**. The program remembers each step's completion state, finished steps are skipped automatically, and every paid LLM call is cached — **you will not be billed twice**. Details in [Resuming and saving money](#resuming-and-saving-money).

> **Windows users**: in step ③ use `set OPENAI_API_KEY=sk-...` (cmd) or `$env:OPENAI_API_KEY="sk-..."` (PowerShell), and replace `.venv/bin/` with `.venv\Scripts\`. The project is primarily tested on macOS/Linux.

---

## Three input modes

```bash
# Mode 1: a single arXiv paper (most common)
.venv/bin/python run.py --arxiv 2506.12345

# Prepare only the source/index/selection consumed by Paper Cleaner Mini
.venv/bin/python run.py --arxiv 2506.12345 --stop-after step5 \
    --runs-dir ../paper_cleaner_mini/inputs

# Mode 2: batch (papers.txt has one arXiv id per line; lines starting with '#' are comments)
.venv/bin/python run.py --ids papers.txt

# Mode 3: a local PDF (requires nougat or magic-pdf; see item 4 of "What you need")
.venv/bin/python run.py --pdf ./local.pdf --paper-id mypaper1
```

Notes:

- **Batch mode** processes papers serially (LLM calls within a single paper run in parallel). Papers are fully independent: one failure does not affect the others, and all results are summarized into `runs/summary.json` at the end.
- `--paper-id` is the name you give a PDF; it determines the output directory (`runs/mypaper1/`).
- Optional flags: `--config PATH` (default `config.yaml`), `--runs-dir PATH` (output root, default `runs`).
- **Exit codes**: `0` everything succeeded; `2` some papers were rejected or failed (the rest still produced output); `3` configuration error, exits immediately.

---

## Reading the results: a complete guide to the output files

All output lives under `runs/`, one subdirectory per paper: `runs/<paper-id>/`.

### First stop: the four human-facing pages

| File | What it is |
|---|---|
| `runs/index.html` | **Batch overview**: one row per paper — title, how many theorems were selected, ship rate, and links to the three pages below |
| `runs/<id>/report/dashboard.html` | The paper's **dashboard**: the problem funnel (how many selected → how many survived), selection signals, difficulty ranking, and every dropped problem with its reason |
| `runs/<id>/graph/dep_graph.html` | **Interactive dependency graph**: the reference relations between all theorems/lemmas/definitions in the paper; drag and zoom |
| `runs/<id>/packages/SELECTION_RATIONALE.md` | The **selection rationale**: why these theorems were chosen, what makes each problem good and where its difficulty lies, why the dropped ones deserved dropping — with the objective signal table attached |

### The actual product: manifest plus authenticated packages

Downstream programs should load the manifest and the complete selected package directory; the target authentication files are part of the package, not disposable intermediates:

1. **`runs/<id>/manifest.json`** — the problem list. Each element of the `packages` array is one problem:

   | Field | Meaning |
   |---|---|
   | `target_id` | opaque source-backed statement identifier, e.g. `stmt-a83f71c209d4` |
   | `selected_as` | why it was selected: `main` (main theorem) / `hardest` / `main+hardest` (both) |
   | `path` | relative path to the problem file (the problem.md below) |
   | `self_contained` / `leak_clean` | an entry appears in the manifest only if both are `true` (passed the self-containment and leak checks) |
   | `proof_chars` | length in characters of the theorem's proof in the original paper — a rough difficulty proxy |
   | `topo_rank` | the theorem's topological rank in the dependency graph (larger = deeper dependency chain) |
   | `role` / `env_type` / `policy` | theorem role, environment type (theorem/proposition/…), and packaging policy (default `dep-closure`) |

   The `stats` block at the end records: how many statements this paper indexed, how many dependency edges, how many problems were attempted, and how many survived.

2. **`runs/<id>/packages/<target-id>/<policy>/`** — the seven-section `problem.md` plus `target.tex` and `target.json`, which freeze and authenticate the target:

   | Section | Content | How the solver uses it |
   |---|---|---|
   | YAML front matter | paper id, target theorem, domain baseline, and other metadata | machine-readable |
   | `## 0. Macro definitions` | LaTeX macro definitions | makes the formulas render correctly |
   | `## 1. Notation and conventions` | notation and paper-wide conventions | read before starting |
   | `## 2. Standing assumptions` | paper-wide assumptions | hold by default; cite freely |
   | `## 3. Known external results` | results from other papers (already rewritten as complete statements) | **may be used without proof** |
   | `## 4. Definitions` | every definition used | concept lookup |
   | `## 5. Available results` | in-paper lemmas/propositions (statements only) | **may be used without proof** |
   | `## 6. Target` | **the immutable statement to prove** | inserted by the controller and checked against `target.tex`/`target.json` |

   The problem opens with explicit "exam rules": use only the material in Sections 1–5 plus graduate-level common knowledge of the field, cite nothing outside the provided list, and state which given result each step uses.

### The honesty ledger: excluded.json

`runs/<id>/excluded.json` records **every dropped problem** and why. It is the receipt for this system's "ship nothing rather than ship a broken problem" principle. Common `reason_code` values:

| reason_code | Plain-language meaning |
|---|---|
| `self_containment_unresolvable` | after all repair rounds, some symbol/concept still has no definition inside the problem — dropped |
| `sufficiency_unresolvable` | compared against the original proof, a required tool is missing and could not be supplied — dropped |
| `external_dep_unstatable` | an external-reference result the proof depends on could not be rewritten into a rigorous statement — dropped |
| `deps_failed` | step 4 could not extract reliable dependencies for it (e.g. network retries exhausted) |
| `package_build_error` | the packaging step itself errored |
| `target_source_unverified` | the selected statement lacks an exact, hash-verified source span |
| `target_integrity_failed` | Section 6 or a frozen target artifact drifted from the indexed source statement |

**Zero problems can be the correct outcome — but the exclusions themselves need calibration.** In one measured batch: `2604.04891` shipped 6/6, `2606.16585` shipped 2/4, `2606.19639` shipped 0/4, and `excluded.json` recorded exactly which symbol each drop was stuck on. However, the first independent calibration audit in 2026-07 (`audit.py`, which re-checks every verdict against the full original paper using a stronger independent model) found that 5 of the 6 exclusions were false kills ("the paper does define this — the text matching just failed to find it"), and 6 of the 8 shipped packages were also flagged by the auditor. Conclusion: an exclusion can just as well be a pipeline defect as a property of the paper. **After each batch, run `python audit.py --papers all`** and read the audit report (`runs/audit/audit_report.md`).

### Full directory map

```text
runs/
├── index.html                  ← batch overview (start browsing here)
├── summary.json                batch summary: which papers were ok / rejected / failed
└── <paper-id>/
    ├── manifest.json           ★ problem list (for downstream programs)
    ├── packages/
    │   ├── SELECTION_RATIONALE.md   selection rationale (for humans)
    │   └── <target-id>/<policy>/
    │       ├── problem.md      ★ the problem itself (final version)
    │       ├── target.tex      ★ exact frozen target statement
    │       ├── target.json     ★ statement/proof spans, hashes, and pairing provenance
    │       ├── problem.iter1.md    draft snapshot before verification round 1 (for debugging diffs)
    │       ├── report.json     detailed record of the triple verification
    │       └── assembly.json   which statements were packaged, and why
    ├── excluded.json           dropped problems + reasons
    ├── status.json             per-step completion state (what resuming relies on)
    ├── report/dashboard.html   dashboard
    ├── graph/                  dependency graph (dep_graph.html interactive / .json data)
    ├── source/                 downloaded paper source (flat.tex = the flattened full text)
    ├── index/                  statement index (statements.v2.json = all theorems/definitions)
    ├── roles/                  selection results (selection.json: who was chosen and why)
    ├── cache/                  LLM call cache (the key to cheap re-runs — do not delete by hand)
    └── logs/run.jsonl          structured log (one event per line; look here when something breaks)
```

The manifest and each complete ★ package are the formal products consumed downstream; `graph/roles/cache/logs` are ordinary intermediates. Source/index evidence remains necessary when independently re-authenticating a target.

> ⚠️ **Warning**: `runs/` contains the full text of third-party papers and raw API responses. It is excluded by `.gitignore` — **do not commit it to git, let alone publish it**. The whole directory can be deleted at any time; the only cost is paying to regenerate it.

---

## Resuming and saving money

The pipeline remembers progress at two levels, so re-running the same command is always safe:

1. **Step level**: `status.json` records each step's completion state and an "input fingerprint" (a hash of the input files + the relevant config + the prompts). Completed steps whose fingerprints are unchanged are skipped outright.
2. **Call level**: every LLM call result is cached under `cache/`. Even when a step must re-run, its unchanged calls hit the cache — **no double billing**.

Practical consequences:

- **Edited `config.yaml` or a prompt in `prompts/`?** Just re-run the original command — only the affected steps recompute; upstream steps are reused as-is.
- **Want to force a paper to run completely from scratch?** Delete the entire `runs/<paper-id>/` directory and re-run (this re-incurs the full cost).
- **The right way to control cost**: validate your configuration on a single paper before launching a batch, and leave `llm.parallel` at the default 8 — the bottleneck is your OpenAI account's per-minute token quota (TPM, e.g. 200k/min); blindly raising the parallelism only produces a flood of rate-limit retries, not more speed.

---

## Common configuration (config.yaml)

Edit the config and simply re-run; affected steps recompute automatically. The most frequently touched settings:

| Setting | Default | What it does |
|---|---|---|
| `pipeline.max_main_theorems` / `min_main_theorems` | 5 / 5 | how many main theorems per paper (when consensus falls short, deterministically backfilled up the signal ladder to the minimum) |
| `pipeline.hardest_theorems` | 2 | how many extra "hardest theorems" to select (may overlap with the mains) |
| `pipeline.max_verify_iters` | 5 | maximum repair rounds of the triple verification (more rounds = more cost, but fewer false drops) |
| `pipeline.min_proof_chars` | 300 | theorems whose proof is shorter than this many characters are not eligible for selection (too easy) |
| `models.*` | o4-mini / gpt-4.1 / gpt-5.5 | which model each LLM role uses: reasoning-heavy roles (dependency extraction A1, checks A4a/A4c, …) use the reasoning model o4-mini; mechanical extraction/scanning roles (leak scan A4b, …) use gpt-4.1; audit-tier roles (index backfill A0, repairer A6, appeal judge A7) use gpt-5.5 |
| `llm.parallel` | 8 | concurrent LLM calls within one paper (see the cost guide above — don't blindly raise it) |
| `llm.cache` | true | LLM call cache switch (turning it off forfeits "free re-runs" — basically never turn it off) |
| `ocr.engine` | nougat | which OCR engine the PDF route uses (`nougat` or `mineru`) |
| `provider` | openai | set to `azure` for Azure OpenAI (also requires the matching environment variables, see design doc §11.3) |

For the full set of fields, read [config.yaml](config.yaml) itself — every line is commented.

---

## Running the tests

```bash
# Without an API key: offline parts only (parsing, graph algorithms, etc. — free)
.venv/bin/pytest tests/ -q

# With an API key: the full suite (includes LLM stages and fault injection; costs a little)
OPENAI_API_KEY=sk-... .venv/bin/pytest tests/ -q
```

The test "paper" is a hand-built mini paper, `tests/fixtures/mini_paper.tex`, whose ground truth (which statements, which dependency edges) is known by construction (`mini_paper_truth.json`) — so the assertions check exact results, not "roughly right". LLM call caches land in `tests/_runs/`, so repeated full-suite runs cost almost nothing.

---

## FAQ

**Q: `config error: OPENAI_API_KEY ...`, or model calls keep failing?**
No API key set, or the key is invalid / out of credit. Go back to step ③ of the quick start; remember that every new terminal needs a fresh `export`.

**Q: A paper's status is `rejected` — what does that mean?**
The system **refused it by rule**; the program did not break. The reason is in `reject_reason` inside `runs/<id>/status.json`. Common values: `ocr_quality` (PDF recognition below the quality bar), `ocr_unavailable` (no OCR tool installed), `no_formal_statements` (the paper has no formal theorem environments), `no_main_theorem` (no qualified main theorem could be selected), `download_error` (arXiv download failed).

**Q: And `failed`?**
A program exception. Check the last lines of `runs/<id>/logs/run.jsonl` (one JSON event per line; the `"event": "exception"` line carries the full error). In batch mode, a single `failed` paper does not affect the others.

**Q: A theorem produced no problem?**
Check `runs/<id>/excluded.json` — every dropped problem has a `reason_code` and details; `report/dashboard.html` visualizes the same. This is by design: problems that cannot be fixed are not delivered.

**Q: Very slow, or lots of 429 retries in the log?**
You are hitting your OpenAI account's TPM cap. This is normal: the program backs off and retries as the server instructs, and after the parallel burst it makes one serial catch-up pass. Do **not** raise `llm.parallel` — that only makes it worse. To actually go faster, raise your account's TPM quota in the OpenAI console.

**Q: Does re-running the same paper charge twice?**
No. Step-level + call-level double caching; see [Resuming and saving money](#resuming-and-saving-money).

**Q: Can the problems be fed directly to an AI?**
Yes. `problem.md` is itself a complete, self-contained prompt — the task and rules are stated at the top; no extra wrapper needed.

**Q: The `--pdf` route reports `ocr_unavailable`?**
The machine has no `nougat` or `magic-pdf` command. Install one of them and make sure `ocr.engine` in `config.yaml` matches.

---

## Source layout

```text
paper_cleaner/
├── run.py                 Orchestrator: runs the 8 steps in order; handles resuming and batch summary
├── audit.py               Independent calibration audit: a stronger independent model, with the
│                          original paper in hand, re-checks every shipped package (self-containment /
│                          leaks / sufficiency) and every exclusion (false kill?);
│                          writes runs/audit/audit_report.md
├── config.yaml            All configuration (models, concurrency, selection counts, verification rounds…)
├── requirements.txt       Python dependencies
├── papers.txt             Example input for batch mode (one arXiv id per line)
├── prompts/               One prompt template per LLM role
│   ├── a0.txt             index backfill           ├── a3_ext.txt  external-result statement
│   ├── a1.txt             dependency extraction    ├── a3_cmp.txt  external-result comparison
│   ├── a2.txt             main-theorem nomination  ├── a4a/a4b/a4c.txt  triple verification
│   ├── a5.txt             selection rationale      └── audit_pkg/audit_excl.txt  audit
├── src/
│   ├── step1_get_source.py … step8_report.py   the 8 steps, one module each
│   ├── common.py          config / context / state machine
│   ├── llm.py             LLM call layer (cache, rate-limit retries, structured outputs)
│   ├── latex_utils.py     LaTeX handling (macro expansion, reference scanning)
│   ├── graph_utils.py     dependency-graph algorithms (closure, cycle breaking)
│   ├── target_integrity.py opaque IDs, source-span/hash checks, immutable Section 6
│   ├── gates.py           programmatic decision rules
│   └── schemas.py         all JSON data-structure definitions
├── tests/                 pytest suite + the hand-built mini paper
├── data/                  whitelist of standard LaTeX commands
├── docs/
│   ├── engineering-plan.md        the original v2.2 design spec and historical baseline
│   └── implementation-notes.md    implementation deviations + field-tested rule fixes (maintainer notes)
└── runs/                  output directory (git-ignored; safe to delete anytime)
```

---

## Glossary

| Term | Meaning |
|---|---|
| **arXiv** | the preprint server where most math/physics/CS papers appear first; every paper has a unique id (e.g. `2604.04891`) |
| **LaTeX** | the typesetting language of academic papers; arXiv usually provides a paper's LaTeX source, which is far easier to parse than the PDF |
| **LLM** | large language model (this project uses o4-mini, gpt-4.1, gpt-5.5), called through the OpenAI API and billed by usage |
| **API key** | the credential for calling OpenAI, of the form `sk-...`; treat it like a wallet password and never commit it to the repo |
| **TPM** | tokens per minute — OpenAI's per-account usage cap; the real throughput bottleneck of this pipeline |
| **venv (virtual environment)** | Python's isolation sandbox; the project's dependencies live inside `.venv/` without touching the system |
| **dependency closure** | starting from the target theorem, follow "A uses B, B uses C" all the way down — the complete set of prerequisite material |
| **target ID** | opaque `stmt-...` identifier derived from source evidence; it never contains or depends on a theorem number |
| **self-contained** | the problem document depends on no outside material: every symbol and concept is defined within the document |
| **leak** | any content in the problem that reveals the proof idea or the derivation of the conclusion; leak prevention = guaranteeing the solver cannot "copy the answer" |
| **OCR** | optical character recognition — turning PDF images back into text/formulas; only used on the local-PDF route |
| **structured outputs** | forcing the LLM to answer only in a pre-declared JSON schema, eliminating format-parsing errors |
