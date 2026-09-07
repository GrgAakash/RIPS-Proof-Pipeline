# With context

[Compare setups](README.md) · [Without context](report_without_lemma.md)

The solver receives the target and a cleaner-prepared packet of paper-specific
background and permitted supporting statements, but not the target's proof.

| Unique targets | Automated passes | Manual passes | Total pass rate |
|---:|---:|---:|---:|
| 31 | 21 | 2 | 74.2% |

The total includes 21 automated Final Checker passes and 2 manual passes.
The automated-only rate is **67.7% (21/31)**.

Each paper–target pair is counted once. Setup failures remain in the denominator.

<details>
<summary>Target-by-target results — 31 records</summary>

## Outcome counts

- `accepted_final_checker`: 21
- `accepted_manual_final_checker`: 2
- `blocked_cleaner`: 1
- `blocked_cleaner_disputed`: 2
- `blocked_setup`: 3
- `cleaner_only`: 1
- `incomplete`: 1

## Target records

| paper | target statement | run used for this theorem | run owner | outcome | final checker | what happened |
|---|---|---|---|---|---|---|
| [2603.19491](https://arxiv.org/abs/2603.19491) | lemma-3.2 | 2603.19491_lemma-3.2 | agurung | `blocked_setup` | not run | The run stopped during setup, before the cleaner or solver could process the theorem. |
| [2604.07183](https://arxiv.org/abs/2604.07183) | theorem-3.1 | 2604.07183_theorem-3.1_no_internet_20260714_163330 | mkagalwala | `accepted_final_checker` | PASS | top folder is `2604.07813`; inner metadata uses `2604.07183` |
| [2604.25023](https://arxiv.org/abs/2604.25023) | proposition-3.4 | 2604.25023_proposition-3.4 | agurung | `blocked_cleaner` | not run | The cleaner blocked this theorem, so it did not reach the solver. |
| [2605.04912](https://arxiv.org/abs/2605.04912) | theorem-25 | 2605.04912_theorem-4.2_no_internet_CHAT6 | aaltyyeva | `accepted_final_checker` | PASS | The run-folder name says theorem 4.2, but the corrected target name is theorem 25. |
| [2605.07617](https://arxiv.org/abs/2605.07617) | lemma-6.13 | 2605.07617_lemma-6.7 | agurung | `blocked_setup` | not run | The run-folder name says lemma 6.7, but the corrected target is lemma 6.13. The run stopped during setup. |
| [2605.19979](https://arxiv.org/abs/2605.19979) | theorem-3.7 | 2605.19979_theorem-3.3 | agurung | `accepted_final_checker` | PASS | The run-folder name says theorem 3.3, but the corrected target name is theorem 3.7. |
| [2605.31583](https://arxiv.org/abs/2605.31583) | lemma-4.1 | 2605.31583_lemma-4.1_no_internet_002 | aaltyyeva | `accepted_final_checker` | PASS | The first run was incomplete. The second run passed, so only the second result is used. |
| [2605.31583](https://arxiv.org/abs/2605.31583) | lemma-4.3 | 2605.31583_lemma-4.2_no_internet_001 | aaltyyeva | `blocked_setup` | not run | This is a different lemma from lemma 4.1. The run-folder name says lemma 4.2, but the corrected target is lemma 4.3. Its only run stopped during setup. |
| [2606.02299](https://arxiv.org/abs/2606.02299) | theorem-1 | 2606.02299_theorem-1.1_no_internet_001 | aaltyyeva | `accepted_final_checker` | PASS |  |
| [2606.02847](https://arxiv.org/abs/2606.02847) | theorem-1 | 2606.02847_theorem-1.1_no_internet_001 | aaltyyeva | `accepted_final_checker` | PASS |  |
| [2606.07143](https://arxiv.org/abs/2606.07143) | theorem-3.2 | 2606.07143_theorem-3.2_no_internet_CHAT7_retry1 | aaltyyeva | `accepted_final_checker` | PASS | The first run was blocked by the cleaner. The rerun passed, so only the rerun result is used. |
| [2606.15249](https://arxiv.org/abs/2606.15249) | lemma-8 | 2606.15249_lemma-3.6 | agurung | `accepted_final_checker` | PASS | The run-folder name says lemma 3.6, but the corrected target name is lemma 8. |
| [2606.15297](https://arxiv.org/abs/2606.15297) | theorem-3.1 | 2606.15297_theorem-3.1_no_internet_001 | aaltyyeva | `accepted_final_checker` | PASS |  |
| [2606.15432](https://arxiv.org/abs/2606.15432) | corollary-6.8 | 2606.15432_corollary-6.4_no_internet_20260714_161020 | mkagalwala | `cleaner_only` | not run | The run folders say corollary 6.4, but the corrected target is corollary 6.8. It was run twice; neither run reached the solver, so only the later run is used. |
| [2606.15670](https://arxiv.org/abs/2606.15670) | theorem-1.2 | 2606.15670_theorem-1.1_no_internet_CHAT4 | aaltyyeva | `accepted_final_checker` | PASS |  |
| [2607.03305](https://arxiv.org/abs/2607.03305) | corollary-2.5 | 2607.03305_corollary-2.2_no_internet_20260714_151917 | mkagalwala | `accepted_final_checker` | PASS | The run folders say corollary 2.2, but the corrected target is corollary 2.5. The earlier run stopped before the solver; the later run passed. |
| [2607.03856](https://arxiv.org/abs/2607.03856) | lemma-2.6 | 2607.03856_lemma-2.4 | agurung | `accepted_final_checker` | PASS |  |
| [2607.04347](https://arxiv.org/abs/2607.04347) | proposition-2.5 | 2607.04347_proposition-2.2 | agurung | `accepted_final_checker` | PASS |  |
| [2607.04347](https://arxiv.org/abs/2607.04347) | theorem-1.7 | 2607.04347_theorem-1.7 | agurung | `accepted_manual_final_checker` | PASS | A manual Codex-subagent final check passed. This is a different target from proposition 2.5 in the same paper. |
| [2607.04798](https://arxiv.org/abs/2607.04798) | theorem-3.1 | 2607.04798_theorem-3.1 | agurung | `accepted_final_checker` | PASS |  |
| [2607.04831](https://arxiv.org/abs/2607.04831) | lemma-4.3 | 2607.04831_lemma-4.3 | agurung | `accepted_final_checker` | PASS |  |
| [2607.05330](https://arxiv.org/abs/2607.05330) | proposition-2 | 2607.05330_proposition-2.1 | agurung | `accepted_final_checker` | PASS |  |
| [2607.05374](https://arxiv.org/abs/2607.05374) | lemma-6 | 2607.05374_lemma-3.1 | agurung | `accepted_final_checker` | PASS |  |
| [2607.06275](https://arxiv.org/abs/2607.06275) | lemma-10.4 | 2607.06275_lemma-10.3_no_internet | mkagalwala | `accepted_final_checker` | PASS |  |
| [2607.06275](https://arxiv.org/abs/2607.06275) | lemma-10.5 | 2607.06275_lemma-10.4_no_internet | mkagalwala | `blocked_cleaner_disputed` | not run | The cleaner blocked this lemma because of a `\defn` macro issue. A later audit said the block was not justified. |
| [2607.06275](https://arxiv.org/abs/2607.06275) | theorem-5.1 | 2607.06275_theorem-5.1_no_internet | mkagalwala | `blocked_cleaner_disputed` | not run | The cleaner blocked this theorem. A later audit said the block was not justified and reported `leak_clean: false`. |
| [2607.06477](https://arxiv.org/abs/2607.06477) | theorem-b | 2607.06477_theorem-b | agurung | `accepted_manual_final_checker` | PASS | manual Codex-subagent pass |
| [2607.07617](https://arxiv.org/abs/2607.07617) | theorem-6.4 | 2607.07617_theorem-6.3_no_internet_20260716_104413 | mkagalwala | `incomplete` | not run | The solver started proving a supporting lemma, but that proof did not finish. No final decision was produced. |
| [2607.08871](https://arxiv.org/abs/2607.08871) | theorem-2.5 | 2607.08871_theorem-2.2 | agurung | `accepted_final_checker` | PASS |  |
| [2607.09222](https://arxiv.org/abs/2607.09222) | lemma-10 | 2607.09222_lemma-3.7_no_internet_20260714_163330 | mkagalwala | `accepted_final_checker` | PASS |  |
| [2607.09440](https://arxiv.org/abs/2607.09440) | lemma-5 | 2607.09440_lemma-0.1 | agurung | `accepted_final_checker` | PASS |  |

</details>
