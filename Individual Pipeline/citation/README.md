# Citation gate

The citation package validates the source claims used by an assembled proof.
It runs after S6 and the exact-target check, and before the A/B/C mathematical
verifier cascade.

## Responsibilities

| Component | Responsibility |
|---|---|
| Citation Generator | Build a source ledger from the proof and supplied bibliography |
| Citation Verifier | Check that ledger using restricted source search |
| Deterministic gate | Parse the report, enforce the decision contract, and persist evidence |

Verifier A does not run until the Citation Verifier returns `GOOD_TO_GO`.
Citation clearance supports the provenance of imported results; it does not
establish that the proof itself is mathematically correct.

## Runtime artifacts

Integrated runs write:

```text
Outputs/<run-name>/solver/<problem-id>/round_NNN/citation_gate/
  citation_generator.md
  citation_verifier.md
  citation_gate_summary.json
```

Only stages actually reached are present. This package contains executable
code and generated prompt views, not the reports from a particular run.

## Modules

| Module | Responsibility |
|---|---|
| `gate.py` | stage execution, retry boundary, persistence, and decision |
| `prompts.py` | public-only prompt assembly |
| `parsers.py` | structured report parsing |
| `models.py` | typed reports and decisions |
| `clients.py` | deterministic offline responses |
| `constants.py` | public/private path and content guardrails |

## Prompt ownership

The canonical role text lives under
[`Prompt Packet/`](../../Prompt%20Packet/README.md). Files in `prompts/` are
generated review views:

```bash
python prompt_sync.py --write
python prompt_sync.py --check
```

## Privacy boundary

Citation prompts may contain the public theorem packet, assembled proof, and
bibliographic material. They must not contain private gold proofs, private
source bundles, API keys, or Final Checker reasoning.
