# BrokenArXiv S0-S6 Results

Prompts and outputs for **43 selected solver-only S0-S6 runs** from the June
2026 BrokenArXiv evaluation, executed on July 20-21, 2026.

All 668 sessions used **GPT-5.5**. Reasoning effort was `xhigh` for 640
sessions and `high` for 28 sessions; the `high` sessions were the runs for
`problem_10` and `unlabeled_distance_laplacian`.

| Runs | Sessions | Stage outputs | Recorded tokens | Estimated cost |
|---:|---:|---:|---:|---:|
| 43 | 668 | 662 | 17,497,323 | $158.62 |

## Cost calculation

| Token category | Tokens |
|---|---:|
| Input | 12,826,989 |
| Cached input | 10,138,496 |
| Uncached input | 2,688,493 |
| Output | 4,670,334 |
| Reasoning output (included in output) | 430,988 |
| Total | 17,497,323 |

| Token category | GPT-5.5 credits per million | Evaluation dollars per million |
|---|---:|---:|
| Uncached input | 125 | $5.00 |
| Cached input | 12.5 | $0.50 |
| Output | 750 | $30.00 |

```text
cost = (2,688,493 / 1M x $5.00)
     + (10,138,496 / 1M x $0.50)
     + (4,670,334 / 1M x $30.00)
     = $158.621733
     = $158.62 rounded ($3.69 per run)
```

Formula and rate-card source: [OpenAI ChatGPT and Codex pricing](https://learn.chatgpt.com/docs/pricing#what-are-tokens-and-credits).
The dollar column uses the evaluation conversion of 25 credits per dollar; it
is a token-equivalent estimate, not an invoice conversion published by the rate
card. Twelve sessions lack usage telemetry, so the recorded total is a minimum.

These are solver outputs, not verified proofs: the citation gate, verifier
cascade, and private Final Checker did not run.

## Round limits

The stated `max_guidance_rounds = 3` was not mechanically enforced. Most runs
used at most three total main rounds, but `problem_40_run_01` used four.
`problem_06` also received two guidance items before its final rerun. The totals
therefore reflect actual usage rather than an equal-budget benchmark.

## Layout

```text
runs/problem_NN/
  input/                     request and target
  round_NNN/                 prompts and outputs
  final/root_response.md     parent response, when present
  historical_attempts/       excluded from the 43-run totals
```

Duplicate labels `38` and `40` are preserved as `_run_01` and `_run_02`.
Executed branches remain nested beneath their requesting stages. Six stage
outputs are empty because no final assistant message was recorded.
