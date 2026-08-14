# Standalone Verifier Cascade

This package runs the isolated verifier sequence:

```text
Verifier A1 + A2 + A3
  -> Composer A
  -> Verifier B
  -> Verifier C
  -> Final Checker gate or solver guidance
```

It supports deterministic mocks, saved-report replay, individual API-backed
stages, and a full API-backed cascade. It does not replace the full solver
controller; integrated solver runs invoke the verifier stages in protocol order.

The canonical prompt packet is `../../Prompt Packet/Prompts.md`. Generated
views for the Problem Statement Verifier, A/B/C, Composer A, and Final Checker
live under this package's `prompts/` directory and are checked for drift by the
offline tests.

## Mock run

```bash
python -m verifiers run-mock \
  --scenario clean \
  --target-theorem 'For every integer n, n = n.' \
  --allowed-supporting-statements 'Equality reflexivity is allowed.' \
  --proof-artifact 'For every integer n, n = n by equality reflexivity.' \
  --skeleton-ref 'skeleton.tex#reflexivity'
```

Artifacts default to `Outputs/verifier/`. Optional manual input files belong in
`Inputs/verifier_input/`; both locations are local working surfaces.

This location is used only when the verifier package is invoked directly. A
full S0-S6 run stores its A1/A2/A3, Composer A, B, and C artifacts inside that
run's `Outputs/<run-name>/solver/<problem-id>/round_NNN/` directory. The two
locations do not feed into one another.

## Offline tests

```bash
python -m unittest discover -s tests/verifier_pipeline -p 'test*.py'
```

## API operation

Set `OPENAI_API_KEY` in the environment and use `python -m verifiers --help`
for the available stage and cascade commands. API calls are not required for
the offline regression suite.
