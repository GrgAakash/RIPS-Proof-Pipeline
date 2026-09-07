# Citation gate

This package checks the results a proof relies on: where they come from,
whether they say what the proof needs, and whether the solver was allowed to
use them. It runs after S6 and the statement check, before the A/B/C proof reviews.

## Responsibilities

| Component | Responsibility |
|---|---|
| Citation Generator | List the proof's sources and how each is used |
| Citation Verifier | Check those entries, looking up sources where permitted |
| Gate code | Read the report, save the result, and decide whether review can continue |

Verifier A does not run until the Citation Verifier returns `GOOD_TO_GO`.
This means the source checks passed, not that the mathematics has been verified.

## Runtime artifacts

Integrated runs write:

```text
Outputs/<run-name>/solver/<problem-id>/round_NNN/citation_gate/
  citation_gate_summary.json
  attempt_001/
    citation_generator_prompt.json
    citation_generator_output.md
    citation_verifier_prompt.json
    citation_verifier_output.md
    citation_gate_decision.json
```

A report appears only if that stage ran. Retries use `attempt_002/` and so on;
start with `citation_gate_summary.json` to find the final attempt. Open the
run's output directory for results; this component directory contains the code
and prompt copies.

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

Edit role prompts in [Prompt Packet/](../../Prompt%20Packet/README.md), then
regenerate the reference copies in `prompts/`:

```bash
python prompt_sync.py --write
python prompt_sync.py --check
```

## Privacy boundary

Citation reviewers receive the solver's input, candidate proof, and bibliography.
Keep reference proofs, private source files, API keys, and private Final Checker
reasoning out of their prompts.
