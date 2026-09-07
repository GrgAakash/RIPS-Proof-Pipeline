# BrokenArXiv S0-S6 artifacts

This collection preserves prompts and outputs for **43 selected solver-only
S0-S6 runs** from the June 2026 BrokenArXiv evaluation. The runs were executed
on July 20-21, 2026.

> [!WARNING]
> These are model-behavior and usage artifacts, **not verified proofs**. The
> citation gate, A/B/C verifier cascade, and private Final Checker did not run.
> No solved/unsolved or mathematical-correctness rate should be inferred from
> this export alone.

## Snapshot

| Runs | Sessions | Recorded stage outputs | Recorded tokens | Token-equivalent estimate |
|---:|---:|---:|---:|---:|
| 43 | 668 | 662 | 17,497,323 | $158.62 |

All sessions used `GPT-5.5`. Reasoning effort was `xhigh` for 640 sessions and
`high` for 28 sessions; the `high` sessions belong to `problem_10` and
`unlabeled_distance_laplacian`.

Twelve sessions lack usage telemetry, so the recorded token total is a lower
bound. Six sessions have no recorded final assistant output.

The usage totals and model settings above are historical accounting figures.
This export contains prompt/output Markdown, not the original per-session
usage telemetry or aggregation script. The cost arithmetic below is
reproducible from the stated totals; those totals cannot be independently
recomputed from this public export alone.

## What is preserved

For each exported run, the collection retains the available:

- input request and target;
- role prompts actually sent;
- role outputs actually recorded;
- round and branch hierarchy;
- parent/root response when present;
- historical attempts, separated from the 43-run aggregate.

The saved prompts beside each output are the most direct evidence of what a
particular session was asked to do. This repository does not retroactively run
the newer citation or verifier gates over these historical artifacts.

## Cost calculation

| Token category | Tokens |
|---|---:|
| Input | 12,826,989 |
| Cached input | 10,138,496 |
| Uncached input | 2,688,493 |
| Output | 4,670,334 |
| Reasoning output, included in output | 430,988 |
| **Total recorded** | **17,497,323** |

| Token category | GPT-5.5 credits per million | Evaluation dollars per million |
|---|---:|---:|
| Uncached input | 125 | $5.00 |
| Cached input | 12.5 | $0.50 |
| Output | 750 | $30.00 |

```text
cost = (2,688,493 / 1M × $5.00)
     + (10,138,496 / 1M × $0.50)
     + (4,670,334 / 1M × $30.00)
     = $158.621733
     = $158.62 rounded ($3.69 per run)
```

Rate-card reference: [OpenAI ChatGPT and Codex pricing](https://learn.chatgpt.com/docs/pricing#what-are-tokens-and-credits).
The dollar figure uses the evaluation conversion of 25 credits per dollar. It
is a token-equivalent estimate, not an invoice amount published by the rate
card.

## Round-budget irregularities

The stated `max_guidance_rounds = 3` was not mechanically enforced across the
preserved batch:

- most runs used at most three total main rounds;
- `problem_40_run_01` used four;
- `problem_06` received two guidance items before its final rerun.

The totals therefore describe actual recorded usage, not an equal-budget
benchmark comparison.

## Directory layout

```text
runs/problem_NN/
  input/
    request.md
    target.md
  round_NNN/
    prompts/
    outputs/
  final/root_response.md          when recorded
  historical_attempts/           excluded from the 43-run totals
```

Duplicate labels `38` and `40` are preserved as `_run_01` and `_run_02`.
Executed branches remain nested beneath the stage that requested them. For
`problem_38_run_02`, the canonical parent/branch hierarchy is primary; its
`raw_chronological_layout/` folder preserves the original recovery grouping.

## How to inspect one run

1. Start with `input/target.md` and `input/request.md`.
2. Read `round_001/prompts/S0.md` before its corresponding output.
3. Follow later rounds in numerical order.
4. Treat branch directories as subordinate proof attempts, not main rounds.
5. Read `final/root_response.md` only as the parent model's conclusion, not as
   independent mathematical verification.

## Interpretation limits

- The 43 runs are the preserved selected set; this README does not claim that
  they form a balanced sample of all mathematical problem types.
- Model self-reports and root responses are not correctness labels.
- Missing telemetry is not zero usage.
- Historical attempts are useful provenance but are excluded from the headline
  totals.
- Comparisons with later pipeline versions must account for changes in prompts,
  source checking, verifier gates, and round enforcement.
