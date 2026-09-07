# Solver input contract

Each integrated run exports an audited solver bundle under this workspace.
Users may also create a hand-authored theorem packet and pass it to
`python -m solver run-open-problem`.

> [!IMPORTANT]
> A hand-authored packet bypasses cleaner provenance, independent package
> audit, and the pre-solver source gate. Its terminal status covers only the
> stages that actually ran.

## Minimal packet

```text
<problem-name>/
  target.md
  skeleton.md                 # or skeleton.tex
  allowed_support.md          # strongly recommended
  guidance.md                 # optional
  bibliography.bib            # optional; .bbl or .md also accepted
  private/                     # optional; never commit
    gold_proof.md
    source.md
```

Provide `target.md` and one public skeleton. If both skeleton filenames exist,
the loader uses `skeleton.md` and ignores `skeleton.tex`. The directory name
becomes the problem identifier in the output path; integrated exports use a
nested directory named `solver_input`.

## `target.md`

Copy the exact theorem statement, including every hypothesis, quantifier, and
scope condition. Do not paraphrase, strengthen, weaken, or include its proof.

## Public skeleton

For paper-reproduction work, use these headings in this order:

```text
## 0. Macro definitions
## 1. Notation and conventions
## 2. Standing assumptions
## 3. Known external results (may be used without proof)
## 4. Definitions
## 5. Available results (statements only; may be used without proof)
```

The skeleton should define paper-specific notation, state assumptions, and give
each permitted imported result at the required generality. Every Section 3
grant needs an identifiable source. Section 5 may contain statements of prior
in-paper results, never their proofs.

Do not include:

- the target's proof or proof outline;
- a premise equivalent to or stronger than the target;
- hidden hints extracted from the reference proof;
- an external result without enough information to source-check it.

## `allowed_support.md`

State the premise boundary explicitly. A useful pattern is:

```text
Definitions, notation, conventions, and standing assumptions in Sections 1,
2, and 4 are allowed.

Section 3 results [R1], [R2], ... are allowed exactly as written and subject to
source verification.

The named prior results in Section 5 are allowed exactly as written.

The target is not an allowed premise. No equivalent, stronger, or logically
downstream statement may be used as a premise.
```

If this file is absent, the selected prompt packet's default support rule
applies. An explicit file is safer for a public or auditable run.

## Optional files

- `guidance.md`: one complete guidance item per non-empty line. Leave it empty
  for the first attempt. Never put gold-proof text or private verifier reasoning
  here.
- `bibliography.bib`, `.bbl`, or `.md`: source records used by the citation
  gate. Only the first recognized filename is loaded.
- `private/gold_proof.md` and `private/source.md`: privileged Final Checker
  inputs. They are isolated from S0-S6 and must remain untracked.

Integrated cleaner exports also contain `setup_manifest.json`, file hashes,
audit records, and source-gate evidence. Preserve those files with the packet.

## Validate without paid calls

From the repository root:

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

The mock confirms that the packet loads and the orchestrator reaches a terminal
state. It does not validate the mathematics, citations, or source provenance.

For real API-backed options, run `python -m solver run-open-problem --help` and
read the [root workflow guide](../../README.md#run-a-hand-authored-solver-packet).
