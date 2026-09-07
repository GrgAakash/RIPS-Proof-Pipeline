# Standalone verifier cascade

This package runs the proof reviewers. Three A agents review the same proof
separately, Composer A combines their findings, B looks for its weakest point,
and C tries to break it:

```text
A1 + A2 + A3 → Composer A → Verifier B → Verifier C
```

You can try fixed mock responses, replay saved reports, or run individual
reviews and the full sequence through the API. The standalone commands do not
run the integrated solver's controller, statement check, or citation check.

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

The mock checks that reports are read and files are saved correctly. Its
responses are fixed; it does not test a real proof.

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

These are language-model reviews, not formal verification. Report which checks
ran and what they found; a partial review or standalone verifier run is not a
complete pipeline result.
