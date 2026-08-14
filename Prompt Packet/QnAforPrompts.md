# QnA for Prompts

## Decision Controller and Guidance Generation

### Question

If we do not make the Decision Controller an LLM agent in the automation, then how can it see Verifier B's report and form a good forward-looking guidance item?

Also, right now we do not have the Decision Controller implemented as non-LLM code, so where did the `if` statement logic come from? Was that made up for now?

### Answer

Right now, the Decision Controller is only a prompt-level role: an LLM or human follows the rules written in `Prompts.md` and `FlowChart.md`. There is not yet deterministic controller code.

The `if` statement was a proposed implementation sketch, not existing code. It was written by translating the current prompt rule into automation-style pseudocode.

The relevant current rule is:

```text
If B's weakest point is fillable: no, or B records a disallowed premise at the weakest point,
output RERUN_SOLVER_WITH_GUIDANCE, source = B, unless the guidance budget is exhausted.
```

That naturally becomes:

```python
if B.fillable == "no" or B.disallowed_premise == "yes":
    return RERUN_SOLVER_WITH_GUIDANCE(source="B")
```

If the Decision Controller is later automated as non-LLM code, it should not invent new mathematics. Instead, Verifier B must output enough structured information for the controller to transform B's finding into a solver-facing hint.

The intended split is:

```text
Verifier B = LLM math critic
  outputs structured fields:
    weakest_point
    missing_claim
    fillable
    disallowed_premise

Decision Controller = deterministic code
  reads those fields
  applies the routing rule
  wraps the missing_claim into one standalone guidance item

Prompt/Packet Packager = deterministic code
  appends that guidance item exactly to the next Solver prompt
```

For example, if B says:

```text
Fillable: no
Missing claim: existence of jointly measurable parameterized disintegration with respect to the (U^t)-marginal
Disallowed premise at the weakest point? no
```

then a deterministic controller could produce:

```text
Establish the jointly measurable parameterized disintegration needed with respect to the
(U^t)-marginal. Make explicit the standard Borel hypotheses, the marginal being
disintegrated over, and the required measurability in t.
```

This is not new mathematical judgment by the controller. It is a templated rewrite of B's `Missing claim` field.

So the current status is:

```text
Current system: Decision Controller is still prompt-level.
Pseudocode: proposed future automation logic.
Reason it is valid: it directly mirrors the written prompt rule.
Needed improvement: make B/C final summaries machine-readable, preferably JSON or YAML.
```

## Mathematical Guidance in Verifier Prompts

### Question

Should the additional mathematical guidance list be included in every prompt for all the verifiers?

### Answer

Yes. The guidance list should be included in every verifier prompt, because the verifier must judge the proof in the same mathematical environment that the Solver had. If the Solver was allowed to use guidance item `H_i`, then A, B, C, and the Final Checker need to know that `H_i` was an allowed input rather than treating it as an unstated outside premise.

The important distinction is:

```text
Verifiers may see and use the existing guidance list as allowed context.
Verifiers should not create or append new guidance items themselves.
```

This means the guidance list should be present in:

```text
Solver prompt
Verifier A1/A2/A3 prompts
Composer A inputs
Verifier B prompt
Verifier C prompt
Final Checker prompt
Controller / packager record
```

But the power to append a new guidance item belongs only to the controller path:

```text
A / B / C identifies a blocking mathematical issue.
Decision Controller chooses the source issue and produces exactly one standalone guidance item.
Prompt/Packet Packager appends that item to the next Solver prompt.
```

So the answer is not "put guidance generation ability into every verifier." The answer is "put the existing guidance list into every verifier prompt, but keep guidance generation centralized."

Why this matters:

```text
Without the guidance list:
  A verifier might falsely reject a proof for using a hint that was actually allowed.

With guidance generation inside every verifier:
  Multiple agents could produce competing hints, leaking diagnoses across roles and breaking
  the one-guidance-item-per-round rule.

With the current intended split:
  All verifiers know the allowed guidance context, but only the controller route appends one
  new item when the proof must be rerun.
```

So the clean design is:

```text
Every verifier sees H_k.
No verifier independently appends to H_k.
The Decision Controller decides whether one new item should be appended.
The Prompt/Packet Packager carries H_{k+1} into the next Solver/verifier packet.
```

## Which Roles Should Be LLMs vs Code in Automation

### Question

When we automate this workflow, which agents should still be LLMs, and which parts should become code?

### Answer

The practical split should be:

```text
Use LLMs for mathematical judgment.
Use code for routing, packet assembly, logging, budgets, and mechanical checks.
```

Recommended automation design:

```text
LLM roles:
  Solver
  Verifier A1
  Verifier A2
  Verifier A3
  Verifier B
  Verifier C
  Final Checker

Code roles:
  Prompt/Packet Packager
  Decision Controller, once verifier outputs are structured enough
  Guidance-list manager
  Controller log writer
  Guidance-budget checker
  Hard-gate checker for setup/web/skeleton-leakage issues
  Basic Controller Audit checks
```

Borderline roles:

```text
Composer A:
  Keep as LLM for now, because it merges three mathematical audit reports and must preserve
  disagreements carefully.

  Later, it can partly become code if A1/A2/A3 produce strict JSON/YAML artifact reports.
  Even then, an LLM may still be useful for summarizing disagreements and producing a readable
  gold Verifier A evidence report.

Decision Controller:
  Can be an LLM now, because the reports are still prose-heavy.

  In the final automation, it should ideally be deterministic code. It should not re-check the
  proof or make new mathematical judgments. It should read structured fields from A/Composer,
  B, C, and Final Checker, then apply the decision tree exactly.

Controller Audit:
  Can be code for mechanical checks once the controller output is structured.

  An LLM audit is useful while the protocol is still changing, because it can catch confusing
  prose mismatches that code would not understand.
```

The reason Solver, A, B, C, and Final Checker should remain LLMs is that they require proof search or proof criticism:

```text
Solver:
  constructs a proof.

Verifier A1/A2/A3:
  independently audit the whole proof for gaps, disallowed premises, false steps, and scope.

Verifier B:
  identifies the single weakest point and decides whether it is fillable.

Verifier C:
  adversarially tries to break the proof.

Final Checker:
  uses privileged gold/source access to make the final mathematical correctness decision.
```

The reason the controller-style pieces should become code is that they should be exact, repeatable, and not creative:

```text
Decision Controller code should answer questions like:
  Did A verify or fail?
  Should B run next?
  Did B say fillable: no?
  Did C say broke: yes?
  Is the guidance budget already 10?
  Should the Final Checker run?
  Is the final status ACCEPTED, REJECTED_FINAL_CHECK, RERUN_SOLVER_WITH_GUIDANCE, or STOPPED_BUDGET?
```

So the long-term clean architecture is:

```text
LLM math agents produce structured reports.
Code reads those reports and moves the workflow forward.
Only LLMs do math judgment.
Only code mutates workflow state.
```

For now, because the current reports are still partly prose, the Decision Controller can remain an LLM/manual role. But the prompts should keep moving toward machine-readable final summaries so that the controller can later become code without changing the mathematical protocol.
