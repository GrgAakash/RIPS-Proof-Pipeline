# Solver Inputs

Each integrated run exports an audited public bundle here. Users who want to
skip the cleaners may also create a hand-authored problem directory and pass it
to `python -m solver run-open-problem`.

## Files

```text
<problem-name>/
  target.md
  skeleton.md                 # or skeleton.tex
  allowed_support.md          # strongly recommended
  guidance.md                 # optional
  bibliography.bib            # optional; .bbl or .md also accepted
  private/
    gold_proof.md              # optional; Final Checker only
    source.md                  # optional; Final Checker only
```

`target.md` and one of `skeleton.md` or `skeleton.tex` are required. The
directory name becomes the problem identifier used in the output path.

### `target.md`

Write the exact theorem statement, including all hypotheses, quantifiers, and
scope. Do not paraphrase it, strengthen it, weaken it, or include its proof.

### `skeleton.md`

Provide the public information from which the proof may be reconstructed. For
paper-reproduction work, use these headings in this order:

```text
## 0. Macro definitions
## 1. Notation and conventions
## 2. Standing assumptions
## 3. Known external results (may be used without proof)
## 4. Definitions
## 5. Available results (statements only; may be used without proof)
```

The skeleton must be self-contained. Define paper-specific notation; state
assumptions explicitly; give every imported result at the needed generality;
and identify a source for every Section 3 result. Section 5 may contain only
statements of earlier results. It must not contain the target proof, a proof
outline, hidden hints derived from that proof, or a premise equivalent to or
stronger than the target.

### `allowed_support.md`

List exactly what may be used without proof. A useful structure is:

```text
Definitions, notation, conventions, and standing assumptions in Sections 1,
2, and 4 are allowed.

Section 3 results [R1], [R2], ... are allowed exactly as written and subject to
source verification.

The named prior results in Section 5 are allowed exactly as written.

The target is not an allowed premise. No equivalent, stronger, or logically
downstream statement may be used as a premise.
```

If this file is absent, the prompt packet's default support rule applies. An
explicit file is safer for a public or auditable run.

### Optional files

- `guidance.md`: one complete guidance item per non-empty line. Leave it empty
  for the first attempt. Guidance is solver-visible, so never place a gold-proof
  excerpt or private verifier reasoning here.
- `bibliography.bib`, `bibliography.bbl`, or `bibliography.md`: source records
  used by the citation gate. Only the first matching filename is loaded.
- `private/gold_proof.md` and `private/source.md`: enable the privileged Final
  Checker. They are never intended for S0-S6 prompts. Keep them local and do
  not commit them.

An integrated cleaner export also contains `setup_manifest.json`, hashes, and
source-gate records. These prove that its public packet passed the repository's
setup gates. A hand-authored directory has no such provenance and must not be
described as cleaner-audited or source-gated.

## Run

From the repository root, perform a free structural smoke test first:

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

The mock confirms that the directory can be loaded and the orchestration can
reach a terminal state; it does not validate the mathematics or source
provenance. See the root `README.md` for real no-internet and
source-supported commands.
