# Public results

We tested **GPT-5.5 xhigh** on ArXivMath and BrokenArXiv, both directly and with
the S0–S6 solver workflow. These are the reported results:

![Reported benchmark scores for direct GPT-5.5 xhigh versus the S0–S6 pipeline; both comparisons use a 0–100% scale.](../docs/benchmark-results.svg)

| Benchmark | Direct model | S0–S6 pipeline | Difference |
|---|---:|---:|---:|
| ArXivMath 04/26 | 63.41% | 69.14% | +5.73 percentage points |
| BrokenArXiv 06/2026 | 69.4% | 90.7% | +21.3 percentage points |

*These are project-reported scores. The two approaches were not given matching
compute budgets.*

## Example runs

Start with the [Cayley's-formula example](../Examples/cayley/README.md) to follow
one complete Codex-subagent run, from its input to the proof and final review.
It is a walkthrough of a known theorem, separate from the benchmarks above.

You can also explore [43 selected BrokenArXiv runs](brokenarxiv/runs/) to see
the inputs, solver prompts, and recorded outputs. These examples stopped at
the solver stage; citation and proof reviews were not run. The
[evaluation notes](brokenarxiv/README.md) explain what is included.

## Paper reproduction

![Paper-reproduction outcomes with and without context, distinguishing automated passes, manual passes, and other outcomes.](../docs/paper-reproduction-results.svg)

We also asked whether paper-specific context helps the solver. **With context**,
it receives background and supporting statements from the paper. **Without
context**, it receives the target and essential definitions, but no supporting
lemmas. The final reports record
**23/31 passes with context (74.2%; 21 automated + 2 manual)** and
**15/31 without context (48.4%; all automated)**. See the
[paper-reproduction results](paper_reproduction/README.md) for the target-by-target
outcomes and links to the papers.

Which targets passed only with context, only without it, in both, or in
neither? The [subject breakdown](paper_reproduction/paired_outcomes.md) compares
the 28 targets we could match between the two reports.

<!-- BEGIN SUBJECT COVERAGE -->

## Subject coverage

The paper-reproduction collection covers **27 unique papers** across
**9 primary arXiv categories**. These counts describe the collection,
not subject-level accuracy.

![Number of unique papers in each primary arXiv subject category.](../docs/paper-subject-coverage.svg)

[Explore all 27 papers and their subjects](paper_reproduction/README.md#subject-coverage).

<!-- END SUBJECT COVERAGE -->

[Project README](../README.md)
