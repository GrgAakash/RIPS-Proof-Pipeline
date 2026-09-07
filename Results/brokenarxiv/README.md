# BrokenArXiv example runs

Explore **43 selected runs** from the June 2026 BrokenArXiv evaluation. Each
folder shows the problem, prompts sent to the S0–S6 solvers, and their recorded
responses. The runs took place on July 20-21, 2026.

These are solver-only examples. The citation checks, A/B/C reviewers, and
private Final Checker were not run, so this collection alone does not tell us
which proofs are correct or establish a success rate.

## Snapshot

| Runs | Sessions | Recorded stage outputs | Recorded tokens | Token-equivalent estimate |
|---:|---:|---:|---:|---:|
| 43 | 668 | 662 | 17,497,323 | $158.62 |

All sessions used `GPT-5.5`. Reasoning effort was `xhigh` for 640 sessions and
`high` for 28 sessions; the `high` sessions belong to `problem_10` and
`unlabeled_distance_laplacian`.

Twelve sessions lack usage telemetry, so the recorded token total is a lower
bound. Six sessions have no recorded final assistant output.

These usage totals come from the original accounting records. The export
contains prompts and responses, but not the per-session usage logs or counting
script. You can check the cost arithmetic below, but cannot rebuild the token
totals from these files alone.

## What is preserved

Each run includes the files that were available:

- input request and target;
- role prompts actually sent;
- role outputs actually recorded;
- rounds and nested lemma attempts;
- parent/root response when present;
- earlier attempts, kept separate from the 43-run totals.

Read the prompt beside an output to see what that solver was asked to do.
These are the original records; the newer review stages have not been applied
to them.

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

The runs did not all follow the stated `max_guidance_rounds = 3` limit:

- most runs used at most three total main rounds;
- `problem_40_run_01` used four;
- `problem_06` received two guidance items before its final rerun.

The totals reflect what was actually run, not a comparison with equal budgets.

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

Problems `38` and `40` each have two runs, named `_run_01` and `_run_02`.
Lemma attempts sit under the stage that requested them. For
`problem_38_run_02`, follow that parent/branch layout; the
`raw_chronological_layout/` folder also retains the original recovery grouping.

## How to inspect one run

1. Start with `input/target.md` and `input/request.md`.
2. Read `round_001/prompts/S0.md` before its corresponding output.
3. Follow later rounds in numerical order.
4. Open branch directories for the separate lemmas attempted within a round.
5. Read `final/root_response.md` for the parent model's conclusion. It is not
   an independent proof review.

## Interpretation limits

The 43 selected runs are examples, not a balanced sample of mathematical
subjects. Earlier attempts are excluded from the totals, and missing usage
records are not counted as zero. When comparing with later versions, account
for changes in prompts, source checks, proof reviews, and round limits.
