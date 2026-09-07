# Standalone verifier cascade

This package runs the isolated mathematical review sequence used by the solver:

```text
A1 + A2 + A3 → Composer A → Verifier B → Verifier C
```

It supports deterministic mocks, saved-report replay, individual API-backed
stages, and a full API-backed cascade. It does not replace the integrated
solver controller, exact-target gate, or citation gate.

## Free mock run

From the repository root, after installation:

```bash
python -m verifiers run-mock \
  --scenario clean \
  --target-theorem 'For every integer n, n = n.' \
  --allowed-supporting-statements 'Equality reflexivity is allowed.' \
  --proof-artifact 'For every integer n, n = n by equality reflexivity.' \
  --skeleton-ref 'skeleton.tex#reflexivity'
```

The mock exercises parsing, routing, and artifact creation. It does not verify
an external mathematical claim.

## Command surface

```bash
python -m verifiers --help
```

| Command family | Purpose |
|---|---|
| `run-mock` | Deterministic offline scenarios |
| `run-api-a-stage` | One A-stage review |
| `run-api-composer-a` | Merge A1/A2/A3 evidence |
| `run-api-b` / `run-api-c` | Focused weakest-point and adversarial checks |
| `run-api-cascade` | Full standalone A/Composer/B/C sequence |
| `parse-manual-run` | Parse saved manual reports without API calls |

Set `OPENAI_API_KEY` only for API-backed commands. The regression suite and
mock clients do not require it.

## Output locations

Standalone runs default to:

```text
Outputs/verifier/<verifier-run-id>/
```

Integrated S0-S6 runs place the same role artifacts inside the corresponding
round under `Outputs/<run-name>/solver/<problem-id>/round_NNN/`. The standalone
and integrated directories do not feed into one another.

See [`Outputs/README.md`](../../Outputs/README.md) for artifact interpretation.

## Prompt ownership

Canonical role text lives in the selected file under
[`Prompt Packet/`](../../Prompt%20Packet/README.md). The files under `prompts/`
are generated views checked for drift by the offline suite.

## Interpretation boundary

These verifiers are LLM-based critics, not independent formal proof kernels.
Their reports are evidence for the deterministic controller. Report the exact
terminal status and do not describe a partial or verifier-only result as a
proved theorem.
