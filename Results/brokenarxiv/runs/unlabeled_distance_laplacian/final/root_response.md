You’re right. Properly tracing the flowchart and executable workflow, it should eventually call S0 again.

The intended two-level behavior is:

1. `SOURCE_LEDGER_REPAIR_NEEDED` first retries the citation layer on the same proof and unchanged \(H_k\).
2. If those citation-only attempts still fail, the controller returns `RERUN_UNCHANGED`.
3. The outer workflow starts a fresh round at S0, still with unchanged \(H_k\).

Evidence:

- The compact flowchart routes citation repair through the assembler to “Next round starts again at S0” (FlowChart.md, lines 52 and 72 in the original workspace).
- The citation layer performs same-proof repair attempts first (`orchestrator.py`, line 655).
- Continued failure becomes `OUTCOME_RERUN_UNCHANGED` (`controller.py`, line 230).
- The outer loop then opens another round, whose first solver call is S0 (`orchestrator.py`, lines 211 and 254).

The prompt wording is ambiguous because it says only `RERUN_CITATION_LAYER_SAME_GUIDANCE`, while the flowchart’s outgoing path continues to a fresh solver round. The packet itself says to pause and reconcile such disagreements.

In our run, I performed repeated citation-only calls but stopped before the outer unchanged rerun. That was incorrect. After the citation repairs remained unsuccessful, I should have launched fresh S0-S6 round 2 with no new guidance item.
