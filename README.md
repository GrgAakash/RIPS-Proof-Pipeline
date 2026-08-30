# Proof Pipeline

A standalone, proof-oriented pipeline for reconstructing a theorem from a
mathematical paper. It prepares an arXiv source, exports a solver-safe theorem
packet, runs the S0-S6 proof workflow, checks citations, and routes the result
through an isolated verifier cascade.

This repository is the clean normal proof-reproduction system. Historical
runs, cached papers, private proof material, and the experimental open-problem
pipeline are intentionally kept elsewhere.

## Project provenance

This repository is a cleaned public release of the collaborative RIPS-LA 2026
project sponsored by OpenAI. Development occurred in an earlier shared
repository, so the commit history here does not represent the full team's
contributions. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for the complete project
team and mentorship.

## Pipeline

```text
paper source
  -> paper cleaner and target selection
  -> audited solver packet
  -> S0 blueprint
  -> S1-S5 proof modules
  -> S6 candidate proof
  -> Problem Statement Verifier
  -> citation gate
  -> Verifier A1/A2/A3 -> Composer A -> Verifier B -> Verifier C
  -> optional private Final Checker
  -> reader-facing proof package
```

The solver supports two prompt packets:

- `Prompt Packet/Prompts.md`: S0-S6 work without hosted web search.
- `Prompt Packet/PromptsWithFullInternet.md`: S0-S6 may use hosted web search.

In both modes, source validation and the post-proof citation gate may use
restricted web search. A verifier acceptance is not automatically a private
Final Checker acceptance; the terminal status records which gates actually ran.

## Repository layout

```text
Individual Pipeline/    implementation components grouped in one container
  solver/               S0-S6 orchestration, branching, and proof assembly
  citation/             post-S6 Citation Generator and Citation Verifier gate
  verifiers/            isolated A1/A2/A3, Composer A, B, and C tools
  paper_cleaner/         upstream arXiv preparation and target selection
  paper_cleaner_mini/    one-target cleaner, repair, and audit workflow
Prompt Packet/           canonical role prompts and workflow map
Commands/                reusable shell entry points
tests/                   offline solver and verifier regression tests
Inputs/                  local generated inputs; ignored by Git
Outputs/                 local run artifacts; ignored by Git
run_pipeline.py          integrated cleaner-to-solver entry point
```

The canonical packets are the only prompt files edited by hand. Generated
role-specific views live under `Individual Pipeline/solver/prompts/`,
`Individual Pipeline/citation/prompts/`, and
`Individual Pipeline/verifiers/prompts/`. The standalone verifier utility
loads its generated views at runtime; the integrated pipeline loads the
selected canonical packet. After changing a canonical packet, run:

```bash
python prompt_sync.py --write
python prompt_sync.py --check
```

## Install

Python 3.9 or newer is required.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[pipeline]'
```

Keep `OPENAI_API_KEY` in the environment. Never place credentials, private
papers, or private proofs in tracked files.

### API key resolution

An explicit `--api-key` wins. Otherwise the CLI checks the name supplied by
`--api-key-env`, then `DEEPSEEK_API_KEY`, then `OPENAI_API_KEY`, and finally
the ignored local `API_key.md` compatibility file. Environment variables are
preferred; keys are never written into run configuration artifacts.

## Use with Codex subagents

Current Codex clients can delegate independent work to
[subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
For this repository, use Codex as the operator around the checked-in runtime:
subagents may inspect inputs and audit outputs, while the Python controller owns
the ordered S0-S6 run, routing, persistence, and verifier gates. Do not ask a
second set of Codex agents to duplicate a solver round already being run by the
Python controller.

Open the repository in Codex and adapt this prompt:

```text
Operate the proof pipeline in this repository.

Run mode: <full pipeline or solver-only>
Input: <paper ID and target ID, or solver-input directory>
Prompt mode: <no-internet or full-internet>
Run name: <name>

Use the selected canonical prompt packet and follow its S0-S6 execution order.
Use read-only subagents for two independent preflight checks: one must validate
the input files and exact target statement; the other must check the selected
prompt mode, privacy boundary, and output location. Wait for both and resolve
any blocking finding before running the pipeline.

The checked-in Python runtime is the authoritative orchestrator. Do not manually
re-run S0-S6 or the verifier cascade in a second orchestration layer. Before any
paid API call, show me the exact command, model, solver web mode, private Final
Checker setting, and output directory, then wait for approval.

After the run reaches a terminal status, use separate read-only subagents to
audit (1) the terminal controller status and gates that actually ran and (2) the
proof, citation, and verifier artifacts. Wait for both, then report the exact
status, artifact paths, and unresolved gates. Never describe a candidate,
partial, or verifier-only result as privately checked or proved.
```

Codex subagents share the parent session's permissions and consume additional
tokens. Keep their assignments bounded and avoid parallel edits to the same
files. The repository does not currently expose Codex subagents as an alternate
backend for its internal model calls; `--solver-workers` controls the runtime's
own parallel S1-S5 API calls.

## Prepare a paper

```bash
export OPENAI_API_KEY='...'
ARXIV=2606.16585 ./Commands/prepare_paper_input.sh
```

The prepared paper is written to `Inputs/paper_cleaner_input/<paper-id>/`.
Inspect its `roles/selection.json`, then select one opaque target identifier
(`stmt-...`). These IDs are source-backed and intentionally do not contain a
possibly misparsed theorem number.

## Run the full pipeline

Closed-book S0-S6 run:

```bash
PAPER_ID=2606.16585 \
TARGET_ID=stmt-a83f71c209d4 \
RUN_NAME=2606.16585_stmt-a83f71c209d4_no_internet \
  ./Commands/run_no_internet.sh
```

Internet-enabled S0-S6 run:

```bash
PAPER_ID=2606.16585 \
TARGET_ID=stmt-a83f71c209d4 \
RUN_NAME=2606.16585_stmt-a83f71c209d4_full_internet \
  ./Commands/run_full_internet.sh
```

Common overrides include `MODEL`, `SOLVER_WORKERS`, `MAX_ROUNDS`,
`MAX_BRANCH_DEPTH`, `MAX_BRANCHES`, `CITATION_MODEL`, and
`CITATION_MAX_ATTEMPTS`. See [Commands/README.md](Commands/README.md).

The shipped run scripts enable the private Final Checker by default. This
copies the selected target's gold proof and full paper source into the ignored
`Inputs/solver_input/<run-name>/solver_input/private/` directory. Set
`INCLUDE_PRIVATE_FINAL_CHECKER=0` to omit that material and finish with a
cascade-only status when the public verifier cascade clears.

## Run only the solver pipeline

To skip both cleaners and supply an existing theorem packet directly, create a
directory under `Inputs/solver_input/`. A practical input packet is:

```text
Inputs/solver_input/my_problem/
  target.md             exact theorem to prove
  skeleton.md           public definitions, assumptions, and granted results
  allowed_support.md     explicit boundary on premises the solver may use
  guidance.md            optional; one prior guidance item per non-empty line
  bibliography.bib       optional; needed when the packet uses cited sources
```

`target.md` must contain the exact target, without a proof or a stronger
replacement. `skeleton.md` should use Sections 0-5 of the cleaner format:

```text
## 0. Macro definitions
## 1. Notation and conventions
## 2. Standing assumptions
## 3. Known external results (may be used without proof)
## 4. Definitions
## 5. Available results (statements only; may be used without proof)
```

State imported results completely, identify their sources, and include only
statements that may be used without proof. Do not include the target's proof,
proof outline, or result equivalent to or stronger than the target. See
[Inputs/solver_input/README.md](Inputs/solver_input/README.md) for the complete
file contract.

Smoke-test the packet without paid API calls:

```bash
python -m solver run-open-problem \
  --problem-dir Inputs/solver_input/my_problem \
  --run-dir Outputs/solver_only_mock \
  --packet-file 'Prompt Packet/Prompts.md' \
  --client mock \
  --max-rounds 1 \
  --max-branch-depth 0 \
  --max-branches 0
```

Then run the no-internet solver with a supported model:

```bash
export OPENAI_MODEL='your-supported-model'
python -m solver run-open-problem \
  --problem-dir Inputs/solver_input/my_problem \
  --run-dir Outputs/solver_only \
  --packet-file 'Prompt Packet/Prompts.md' \
  --client openai \
  --api-surface responses \
  --model "$OPENAI_MODEL" \
  --reasoning-effort high \
  --solver-workers 5 \
  --max-rounds 3 \
  --progress
```

For source-supported solver browsing, select
`Prompt Packet/PromptsWithFullInternet.md` and add `--web-search`. Do not mix
`--web-search` with `Prompts.md`.

The direct solver command still runs the Problem Statement Verifier, citation
gate, and A/B/C cascade by default; it skips only the cleaner and package-audit
stages. Add `--no-verifiers` only for debugging: the exact-target and citation
gates still run, and the result cannot receive ordinary cascade acceptance.
Because a hand-authored packet bypasses cleaner, independent package audit, and
the pre-solver source gate, its terminal status covers only the stages that
actually ran.

## Find the result

For `RUN_NAME=my_run`, inspect:

```text
Inputs/solver_input/my_run/       exact solver-ready input
Outputs/my_run/cleaner/           cleaner and audit records
Outputs/my_run/solver/            solver state and round artifacts
```

For a completed S6 proof, the round records `candidate_final_proof.md`,
`final_proof.md`, `source_ledger.md`, and `problem_statement_verifier.md`. If
the Problem Statement Verifier clears the target, it also records
`citation_gate/`. Runs with accepted branch proofs also produce
`PROOF_GUIDE.md`, `proof_registry.json`, and
`proof_modules/`. `final_proof.tex` is produced only when S6 supplies a TeX
artifact or the optional `pandoc` executable is available.

### Integrated versus standalone verifier output

The repository has two verifier execution paths with separate output locations:

| Execution path | Started by | Verifier output location |
|---|---|---|
| Full S0-S6 pipeline | `Commands/run_no_internet.sh` or `Commands/run_full_internet.sh` | Inside `Outputs/<run-name>/solver/<problem-id>/round_NNN/` |
| Standalone verifier utility | `python -m verifiers ...` | `Outputs/verifier/<verifier-run-id>/` by default |

`Outputs/verifier/` is not an extra stage of the full S0-S6 pipeline. It is an
optional scratch location used only when A1/A2/A3, Composer A, B, and C are run
independently for a mock, replay, or focused verifier check. The integrated
pipeline does not read from that folder, and the folder may be absent until a
standalone verifier command creates it.

Ordinary inputs and outputs stay ignored. Only deliberately reviewed material
belongs in `Outputs/publishable/`.

## Offline verification

After installing the documented `.[pipeline]` dependencies, the bundled tests
do not call paid APIs:

```bash
PYTHONPATH='Individual Pipeline' python -m unittest discover -s tests -p 'test*.py'
```

For a quick standalone verifier check:

```bash
python -m verifiers run-mock \
  --scenario clean \
  --target-theorem 'For every integer n, n = n.' \
  --allowed-supporting-statements 'Equality reflexivity is allowed.' \
  --proof-artifact 'For every integer n, n = n by equality reflexivity.' \
  --skeleton-ref 'skeleton.tex#reflexivity'
```

This command writes to `Outputs/verifier/` by default. It does not modify or
continue an integrated run under `Outputs/<run-name>/`.

## Scope and safety

- This repository reproduces proofs of results supplied by a source paper.
- The experimental professor-supplied open-problem workflow is not included.
- Generated outputs are evidence packages, not automatic publication claims.
- Candidate, partial, verifier-accepted, and private-checker-accepted are
  distinct statuses and must not be presented interchangeably.
- API jobs are never required for offline tests and should be launched only
  intentionally.
- Do not commit generated inputs, raw runs, private gold material, or secrets.
