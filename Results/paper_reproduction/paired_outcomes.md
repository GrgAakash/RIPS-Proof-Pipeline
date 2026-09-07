# With vs. without context: which targets passed?

Across **28 matched target records**, **9 passed only with context**,
**2 only without context**, **12 in both**, and **5 in neither**.

[With context](README.md#what-does-context-mean) supplies paper-specific background and
supporting statements; without context supplies only the target and essential
definitions, notation, and assumptions.

## Breakdown by subject

Counts are **targets, not papers**, grouped by the paper’s primary arXiv category.
“With only” and “Without only” mean a recorded pass in that setup but not the other.

| Subject | With only | Without only | Both | Neither | Paired targets |
|---|---:|---:|---:|---:|---:|
| Combinatorics | 3 | 2 | 4 | 0 | 9 |
| Classical Analysis and ODEs | 2 | 0 | 4 | 0 | 6 |
| Algebraic Geometry | 2 | 0 | 0 | 2 | 4 |
| Probability | 0 | 0 | 2 | 1 | 3 |
| Commutative Algebra | 1 | 0 | 1 | 0 | 2 |
| Statistics Theory | 0 | 0 | 1 | 1 | 2 |
| Number Theory | 0 | 0 | 0 | 1 | 1 |
| Optimization and Control | 1 | 0 | 0 | 0 | 1 |
| **Total** | **9** | **2** | **12** | **5** | **28** |

**The surprising case:** both without-context-only passes are from the same
[combinatorics paper](https://arxiv.org/abs/2607.06275): Lemma 10.5 and Theorem 5.1.
Their with-context runs stopped at the cleaner, before solving. This is a
workflow difference—not evidence that removing context improved the solver.

**How to read this:** “Neither” means neither run recorded a pass; no-pass
outcomes include setup blocks, protocol stops, incomplete attempts, and API
timeouts, not just rejected proofs. Passes include two manual Final Checker
passes in the with-context setup (one in “With only,” one in “Both”). These
are model-based checks, not formal verification. Small subject samples and
different run/checking conditions do not establish a causal effect of context.

The comparison matches 27 records by paper ID and target label, plus one
explicitly documented renumbering. Three rows from each report remain unpaired
because their target labels disagree; they are **excluded, not counted as failures**.
The full reports still contain 31 records per setup. Mathematical Finance has
no paired target because its sole target is among those unresolved labels.

<details>
<summary>Check all matched targets and recorded statuses</summary>

| Paper | Target (with / without, if different) | With-context status | Without-context status | Group |
|---|---|---|---|---|
| [2603.19491](https://arxiv.org/abs/2603.19491) | lemma-3.2 | `blocked_setup` | `stopped_max_rounds` | Neither |
| [2604.07183](https://arxiv.org/abs/2604.07183) | theorem-3.1 | `accepted_final_checker` | `accepted_final_checker` | Both |
| [2604.25023](https://arxiv.org/abs/2604.25023) | proposition-3.4 | `blocked_cleaner` | `stopped_max_rounds` | Neither |
| [2605.04912](https://arxiv.org/abs/2605.04912) | theorem-25 | `accepted_final_checker` | `accepted_final_checker` | Both |
| [2605.07617](https://arxiv.org/abs/2605.07617) | lemma-6.13 | `blocked_setup` | `stopped_max_rounds` | Neither |
| [2605.19979](https://arxiv.org/abs/2605.19979) | theorem-3.7 | `accepted_final_checker` | `stopped_max_rounds` | With only |
| [2605.31583](https://arxiv.org/abs/2605.31583) | lemma-4.1 | `accepted_final_checker` | `accepted_final_checker` | Both |
| [2605.31583](https://arxiv.org/abs/2605.31583) | lemma-4.3 | `blocked_setup` | `stopped_max_rounds` | Neither |
| [2606.02299](https://arxiv.org/abs/2606.02299) | theorem-1 | `accepted_final_checker` | `needs_human_review` | With only |
| [2606.02847](https://arxiv.org/abs/2606.02847) | theorem-1 | `accepted_final_checker` | `stopped_max_rounds` | With only |
| [2606.07143](https://arxiv.org/abs/2606.07143) | theorem-3.2 | `accepted_final_checker` | `accepted_final_checker` | Both |
| [2606.15249](https://arxiv.org/abs/2606.15249) | lemma-8 | `accepted_final_checker` | `accepted_final_checker` | Both |
| [2606.15297](https://arxiv.org/abs/2606.15297) | theorem-3.1 | `accepted_final_checker` | `accepted_final_checker` | Both |
| [2606.15670](https://arxiv.org/abs/2606.15670) | theorem-1.2 | `accepted_final_checker` | `accepted_final_checker` | Both |
| [2607.03856](https://arxiv.org/abs/2607.03856) | lemma-2.6 | `accepted_final_checker` | `accepted_final_checker` | Both |
| [2607.04347](https://arxiv.org/abs/2607.04347) | theorem-1.7 | `accepted_manual_final_checker` | `accepted_final_checker` | Both |
| [2607.04798](https://arxiv.org/abs/2607.04798) | theorem-3.1 | `accepted_final_checker` | `api_response_stall` | With only |
| [2607.04831](https://arxiv.org/abs/2607.04831) | lemma-4.3 | `accepted_final_checker` | `accepted_final_checker` | Both |
| [2607.05330](https://arxiv.org/abs/2607.05330) | proposition-2 / proposition-2.1 | `accepted_final_checker` | `accepted_final_checker` | Both |
| [2607.05374](https://arxiv.org/abs/2607.05374) | lemma-6 | `accepted_final_checker` | `accepted_final_checker` | Both |
| [2607.06275](https://arxiv.org/abs/2607.06275) | lemma-10.4 | `accepted_final_checker` | `stopped_max_rounds` | With only |
| [2607.06275](https://arxiv.org/abs/2607.06275) | lemma-10.5 | `blocked_cleaner_disputed` | `accepted_final_checker` | Without only |
| [2607.06275](https://arxiv.org/abs/2607.06275) | theorem-5.1 | `blocked_cleaner_disputed` | `accepted_final_checker` | Without only |
| [2607.06477](https://arxiv.org/abs/2607.06477) | theorem-b | `accepted_manual_final_checker` | `needs_human_review` | With only |
| [2607.07617](https://arxiv.org/abs/2607.07617) | theorem-6.4 | `incomplete` | `api_response_stall` | Neither |
| [2607.08871](https://arxiv.org/abs/2607.08871) | theorem-2.5 | `accepted_final_checker` | `stopped_max_rounds` | With only |
| [2607.09222](https://arxiv.org/abs/2607.09222) | lemma-10 | `accepted_final_checker` | `needs_human_review` | With only |
| [2607.09440](https://arxiv.org/abs/2607.09440) | lemma-5 | `accepted_final_checker` | `stopped_max_rounds` | With only |

</details>

<details>
<summary>See the renumbering and unpaired records</summary>

For `2607.05330`, the without-context report explicitly identifies
`proposition-2.1` as Proposition 2 in arXiv v2; it is paired with
`proposition-2` in the with-context report. No other aliases are assumed.

| Setup | Paper | Unpaired target | Recorded status |
|---|---|---|---|
| With context | [2606.15432](https://arxiv.org/abs/2606.15432) | corollary-6.8 | `cleaner_only` |
| With context | [2607.03305](https://arxiv.org/abs/2607.03305) | corollary-2.5 | `accepted_final_checker` |
| With context | [2607.04347](https://arxiv.org/abs/2607.04347) | proposition-2.5 | `accepted_final_checker` |
| Without context | [2606.15432](https://arxiv.org/abs/2606.15432) | corollary-6.4 | `needs_human_review` |
| Without context | [2607.03305](https://arxiv.org/abs/2607.03305) | corollary-2.2 | `accepted_final_checker` |
| Without context | [2607.04347](https://arxiv.org/abs/2607.04347) | proposition-2.2 | `blocked_setup` |

In particular, the without-context `2607.04347` Proposition 2.2 record
reports a target-naming/input error; it cannot safely be treated as the
with-context Proposition 2.5 result. The other two label discrepancies
also need statement-level confirmation before inclusion.

</details>

[With-context report](report.md#target-records) ·
[Without-context report](report_without_lemma.md#target-records) ·
[Subject metadata](subjects.json) · [All paper results](README.md)
