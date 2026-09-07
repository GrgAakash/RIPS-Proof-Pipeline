# Without context

[Compare setups](README.md) · [With context](report.md)

The solver receives the target and the definitions, notation, and assumptions
needed to read it, but no supplied supporting lemmas or source proof. Any
additional lemmas must be established by the solver, including through branches.

| Unique targets | Automated passes | Manual passes | Total pass rate |
|---:|---:|---:|---:|
| 31 | 15 | 0 | 48.4% |

These are the reported GPT-5.5 baseline outcomes. Supplementary GPT-5.6 SOL
results appear only in the detailed notes and do not count as baseline passes.

Each paper–target pair is counted once. Setup failures remain in the denominator.

<details>
<summary>Target-by-target results — 31 records</summary>

## Outcome counts

- `accepted_final_checker`: 15
- `api_response_stall`: 2
- `blocked_setup`: 1
- `needs_human_review`: 4
- `stopped_max_rounds`: 9

## Target records

| run | tested date | paper | target | run owner | outcome | final checker | warnings |
|---|---|---|---|---|---|---|---|
| repro_2603.19491_lemma-3.2 | 2026-08-04 | [2603.19491](https://arxiv.org/abs/2603.19491) | lemma-3.2 | Zhida | `stopped_max_rounds` | not run | 3 rounds `forbidden_route`; guidance disputes the target statement (missing `q^lambda` in both Hecke congruences; level formula gives `N=3` where `eta(2z)` precludes `Gamma_0(3)` invariance) |
| repro_2604.07183_theorem-3.1 | 2026-08-04 | [2604.07183](https://arxiv.org/abs/2604.07183) | theorem-3.1 | Zhida | `accepted_final_checker` | PASS |  |
| repro_2604.25023_proposition-3.4 | 2026-08-04 | [2604.25023](https://arxiv.org/abs/2604.25023) | proposition-3.4 | Zhida | `stopped_max_rounds` | not run | 3 rounds `forbidden_route`; round 3 opened a branch lemma that exhausted its own 3 rounds; parent ended `no_useful_guidance` |
| 2605.04912_theorem-25 | 2026-08-12 | [2605.04912](https://arxiv.org/abs/2605.04912) | theorem-25 | Zhida | `accepted_final_checker` | PASS | passed in 1 round; 0 hints; corrected re-run of the mismatch-labelled `repro_2605.04912_theorem-4.2` target |
| 2605.07617_lemma-6.13 | 2026-08-12 | [2605.07617](https://arxiv.org/abs/2605.07617) | lemma-6.13 | Zhida | `stopped_max_rounds` | not run | 3 rounds `forbidden_route`; 3 hints; corrected re-run of the mismatch-labelled `lemma-6.7` target; guidance repeatedly disputes the target as stated (parameter-closedness of `T_1` under the ordered-tuple definition requires an ordering convention absent from the statement) |
| 2605.19979_theorem-3.7 | 2026-08-12 | [2605.19979](https://arxiv.org/abs/2605.19979) | theorem-3.7 | Zhida | `stopped_max_rounds` | not run | 3 rounds `forbidden_route`; 3 hints; corrected re-run of the mismatch-labelled `repro_2605.19979_theorem-3.3` target; every attempted survivor/cancellation involution for the alternating-permutation identity was rejected by the verifiers |
| 2605.31583_lemma-4.1 | 2026-08-05 | [2605.31583](https://arxiv.org/abs/2605.31583) | lemma-4.1 | agurung | `accepted_final_checker` | PASS | passed in 1 round; 0 hints |
| 2605.31583_lemma-4.3 | 2026-08-12 | [2605.31583](https://arxiv.org/abs/2605.31583) | lemma-4.3 | Zhida | `stopped_max_rounds` | not run | 3 rounds `forbidden_route`; 3 hints; corrected re-run of the mismatch-labelled `lemma-4.2` target; guidance asserts the lemma as stated is false — the exponent `A X_S - A^2 n/2` is not the Gaussian likelihood-ratio normalization for the `n x n` submatrix model (the paper's own definition uses `A^2 n^2/2`) |
| 2606.02299_theorem-1 | 2026-08-12 | [2606.02299](https://arxiv.org/abs/2606.02299) | theorem-1 | Zhida | `needs_human_review` | not run (protocol gate) | 2 rounds; 0 hints; corrected re-run of the mismatch-labelled `theorem-1.1` target; citation layer repeatedly requested source-ledger repair without producing a guidance item; complete candidate proofs were composed in both rounds |
| 2606.02847_theorem-1 | 2026-08-12 | [2606.02847](https://arxiv.org/abs/2606.02847) | theorem-1 | Zhida | `stopped_max_rounds` | not run | 3 rounds; 2 hints; corrected re-run of the mismatch-labelled `theorem-1.1` target; a branch investigation disproved a candidate auxiliary lemma, and round 3 ended `no_useful_guidance` |
| 2606.07143_theorem-3.2 | 2026-08-05 | [2606.07143](https://arxiv.org/abs/2606.07143) | theorem-3.2 | agurung | `accepted_final_checker` | PASS | passed in 2 rounds; 1 hint |
| 2606.15249_lemma-8 | 2026-08-12 | [2606.15249](https://arxiv.org/abs/2606.15249) | lemma-8 | Zhida | `accepted_final_checker` | PASS | passed in 1 round; 0 hints; corrected re-run of the mismatch-labelled `lemma-3.6` target; Final Checker notes the accepted proof is a valid alternative that avoids the gold proof's geodesic argument |
| 2606.15297_theorem-3.1 | 2026-08-05 | [2606.15297](https://arxiv.org/abs/2606.15297) | theorem-3.1 | agurung | `accepted_final_checker` | PASS | passed in 1 round; 0 hints |
| 2606.15432_corollary-6.4 | 2026-08-05 | [2606.15432](https://arxiv.org/abs/2606.15432) | corollary-6.4 | agurung | `needs_human_review` | not run (protocol gate) | 2 rounds; 0 hints; citation layer repeatedly requested source-ledger repair without producing a guidance item |
| 2607.05374_lemma-6 | 2026-08-13 | [2607.05374](https://arxiv.org/abs/2607.05374) | lemma-6 | aziza | `accepted_final_checker` | PASS | corrected mismatch target; passed in round 3 with 2 guidance items; 0 branches |
| 2607.06275_lemma-10.5 | 2026-08-13 | [2607.06275](https://arxiv.org/abs/2607.06275) | lemma-10.5 | aziza | `accepted_final_checker` | PASS | corrected mismatch target; passed in round 1 with 0 guidance items; 0 branches |
| 2607.06275_lemma-10.4 | 2026-08-13 | [2607.06275](https://arxiv.org/abs/2607.06275) | lemma-10.4 | aziza | `stopped_max_rounds` | not run by baseline | corrected mismatch target; GPT-5.5 xhigh stopped after 3 rounds; supplementary GPT-5.6 SOL rerun yielded a Final Checker PASS in round 2 with 1 guidance item; the SOL result is not counted as a baseline pass; 0 branches |
| 2607.06275_theorem-5.1 | 2026-08-04 | [2607.06275](https://arxiv.org/abs/2607.06275) | theorem-5.1 | mkagalwala | `accepted_final_checker` | PASS | passed in 1 round |
| 2607.06477_theorem-b | 2026-08-04 | [2607.06477](https://arxiv.org/abs/2607.06477) | theorem-b | mkagalwala | `needs_human_review` | not run | blocked at citation gate after 2 rounds |
| 2607.07617_theorem-6.4 | 2026-08-13 | [2607.07617](https://arxiv.org/abs/2607.07617) | theorem-6.4 | aziza | `api_response_stall` | not run | corrected mismatch target; GPT-5.5 xhigh reached round 3 with 2 guidance items and 3 branches, including a nested determinant-identity branch; repeated resume attempts ended on API read timeouts, so the run was concluded without a mathematical verdict |
| 2607.08871_theorem-2.5 | 2026-08-13 | [2607.08871](https://arxiv.org/abs/2607.08871) | theorem-2.5 | aziza | `stopped_max_rounds` | not run by baseline | corrected mismatch target; GPT-5.5 xhigh stopped after 3 rounds with 2 branches; supplementary GPT-5.6 SOL opened 2 branches and completed S0 plus four sub-solvers after resume, but the remaining API response timed out; the SOL attempt was concluded without changing the baseline outcome |
| 2607.09222_lemma-10 | 2026-08-13 | [2607.09222](https://arxiv.org/abs/2607.09222) | lemma-10 | aziza | `needs_human_review` | not run (protocol gate) | corrected mismatch target; GPT-5.5 stopped after 3 rounds; GPT-5.6 SOL reached repeated citation-ledger repair and stopped for human review after round 2; 0 branches |
| 2607.09440_lemma-5 | 2026-08-13 | [2607.09440](https://arxiv.org/abs/2607.09440) | lemma-5 | aziza | `stopped_max_rounds` | not run | corrected mismatch target; both GPT-5.5 and GPT-5.6 SOL stopped after 3 rounds on the unsupported colimit/Čech-totalization interchange; 0 branches in either attempt |
| 2606.15670_theorem-1.2 | 2026-08-12 | [2606.15670](https://arxiv.org/abs/2606.15670) | theorem-1.2 | Zhida | `accepted_final_checker` | PASS | passed in 1 round; 0 hints; corrected re-run of the mismatch-labelled `theorem-1.1` target (the paper's shared theorem counter makes the result Theorem 1.2) |
| 2607.03305_corollary-2.2_no_internet_20260714_151917 | 2026-08-04 | [2607.03305](https://arxiv.org/abs/2607.03305) | corollary-2.2 | Aziza | `accepted_final_checker` | PASS | separate fresh reproduction passed in 1 round |
| 2607.03856_lemma-2.6 | 2026-08-13 | [2607.03856](https://arxiv.org/abs/2607.03856) | lemma-2.6 | aziza | `accepted_final_checker` | PASS | corrected mismatch target; passed in round 1 with 0 guidance items; 0 branches |
| 2607.04347_proposition-2.2 | 2026-08-05 | [2607.04347](https://arxiv.org/abs/2607.04347) | proposition-2.2 | Aziza | `blocked_setup` | not run | rounds N/A; supplied ZIP explicitly names `2607.04347_proposition-2.2.md`, but the corresponding paper statement is Lemma 2.2 and no Proposition 2.2 exists; recorded as a skeleton-generator target-naming/input error, with prior corrective solver attempts disregarded |
| 2607.04347_theorem-1.7 | 2026-08-05 | [2607.04347](https://arxiv.org/abs/2607.04347) | theorem-1.7 | Aziza | `accepted_final_checker` | PASS | passed in 1 round; citation gate `GOOD_TO_GO` |
| 2607.04798_theorem-3.1 | 2026-08-05 | [2607.04798](https://arxiv.org/abs/2607.04798) | theorem-3.1 | Aziza | `api_response_stall` | not run | rounds N/A; repeated attempts with two valid API keys, two workers, and saved-state and fresh-output runs stalled while reading S0/S6 API responses; one attempt completed S0 and all five perspectives before timing out ahead of synthesis; not a mathematical verdict or input failure |
| 2607.04831_lemma-4.3 | 2026-08-05 | [2607.04831](https://arxiv.org/abs/2607.04831) | lemma-4.3 | Aziza | `accepted_final_checker` | PASS | passed in 3 rounds; citation gate `GOOD_TO_GO`; round 3 supplied the missing standard formulation and closure facts for linearly bounded filtrations |
| 2607.05330_proposition-2.1 | 2026-08-05 | [2607.05330](https://arxiv.org/abs/2607.05330) | proposition-2.1 | Aziza | `accepted_final_checker` | PASS | passed in 1 round; citation gate `GOOD_TO_GO`; the current arXiv v2 displays the target as Proposition 2 |

</details>
