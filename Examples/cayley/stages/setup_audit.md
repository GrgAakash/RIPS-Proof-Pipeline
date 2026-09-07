# Step A2 Skeleton Leakage and Target-Integrity Audit

Verdict: PASS

## Scope

Audited only the packet-allowed files:

- `../private/cayleyProof.tex` as source reference only.
- `../public_input/target.md`.
- `../public_input/skeleton.md`.
- `../public_input/skeleton.tex`.
- `../public_input/allowed_support.md`.
- `../setup/target_record.json`.

No repairs were made to the input files.

## SHA-256 Hashes

- `target.md`: `b6a909b89d6b8eef4bc29f3d4cd685d782f1af75f11332ea6e80ccbb53924bfb`
- `skeleton.md`: `5084f4251a845115720809d7a677567d518ea29daf08ca675ccb7574afeaf737`
- `skeleton.tex`: `5c1323fb27341e5d764cdf6c29d9434e6f8dacdad5bd3162b0d7fd6ce6dea338`
- `allowed_support.md`: `5b2cec066a94a891c6ed23b3c39758f199f80f0d5956556b86eff46daae3ea58`

## Individual Checks

- Target integrity: PASS. `target.md` matches the source theorem body after stripping surrounding whitespace. Its hash also matches `target_record.json`.
- Source record integrity: PASS. The computed source SHA-256 of `cayleyProof.tex` matches `target_record.json`.
- Solver-facing skeleton self-containment: PASS. `skeleton.md` supplies the needed domain convention, notation, finite probability convention, associated directed graph definition, and cyclic-vertex definition.
- Hypotheses and domain: PASS. The packet retains `n` as a positive integer, so `n=1` is included and the well-defined domain is `n >= 1`.
- No proof leakage: PASS. `skeleton.md` contains no proof paragraphs, sketches, derivations, proof-strategy hints, or randomized-procedure details from the source proof.
- Formal source statements: PASS. The non-definition mathematical statements visible in the skeleton are explicitly marked excluded, and `allowed_support.md` independently states that no formal paper statements, the target statement, tree counts, graph-tree correspondences, or height-distribution statements are granted as support.
- Permitted vs excluded distinction: PASS. `skeleton.md` separates notation/conventions/definitions from exclusions, and `allowed_support.md` gives a matching allowed/not-granted boundary. A statement appearing in the excluded list is not treated as an available premise.
- TeX counterpart: PASS. `skeleton.tex` is consistent with the public skeleton and target packet. Its theorem-numbering presentation has been adjusted so the target display no longer renders as a numbered theorem such as `Theorem 0.1`; this resolves the presentation concern without changing the target text or support boundary.

## Concrete Blockers

None.
