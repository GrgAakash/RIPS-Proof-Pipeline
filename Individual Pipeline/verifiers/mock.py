"""Deterministic mock outputs for the standalone verifier pipeline."""

from __future__ import annotations

from verifiers.schemas import AReport


A_RUN_IDS = ("A1", "A2", "A3")


def make_a_output(run_id: str, scenario: str) -> str:
    if scenario == "disallowed_premise":
        return _a_report(run_id, disallowed="YES", seed="Do not cite the target theorem or an equivalent downstream statement.", marker="MOCK_DISALLOWED")
    if scenario == "disallowed_premise_no_seed":
        return _a_report(run_id, disallowed="YES", seed="None", marker="MOCK_DISALLOWED_NO_SEED")
    if scenario == "no_majority" and run_id == "A3":
        return _a_report(run_id, non_fillable="YES", seed="None", marker="MOCK_NO_MAJORITY")
    if scenario == "guidance_seed":
        return _a_report(run_id, non_fillable="YES", seed="Prove the missing compactness step from the allowed hypotheses.")
    if scenario == "non_fillable_no_seed":
        return _a_report(run_id, non_fillable="YES", seed="None")
    if scenario == "fillable_only":
        return _a_report(run_id, fillable="YES", seed="None")
    if scenario == "ordinary_disagreement" and run_id == "A3":
        return _a_report(run_id, fillable="YES", seed="None", marker="MOCK_ORDINARY_DISAGREEMENT")
    if scenario == "web_a":
        return _a_report(run_id, web_source_issue="YES", marker="MOCK_WEB_A")
    return _a_report(run_id)


def compose_a_output(a_reports: list[AReport], step_map: str | None = None) -> str:
    """Compose A reports without accepting proof/skeleton/target inputs."""

    del step_map  # currently unused, but kept for the prompt's optional input.
    disallowed = any(report.disallowed_premises_present == "YES" for report in a_reports)
    non_fillable = any(report.non_fillable_gaps_present == "YES" for report in a_reports)
    fillable = any(report.fillable_only_gaps_present == "YES" for report in a_reports) and not non_fillable
    omitted = any(report.omitted_case_or_weaker_statement_present == "YES" for report in a_reports)
    web_source_issue = any(report.web_source_issue == "YES" for report in a_reports)
    seed = next((report.candidate_guidance_seed for report in a_reports if report.candidate_guidance_seed != "None"), "None")
    no_majority = any("MOCK_NO_MAJORITY" in report.raw_text for report in a_reports)
    majority = any("MOCK_ORDINARY_DISAGREEMENT" in report.raw_text for report in a_reports)
    agreement = "no majority" if no_majority else "majority agree (2 of 3)" if majority else "all agree"
    same_issue = "UNCLEAR" if no_majority else "YES"
    return _composer_report(
        non_fillable="YES" if non_fillable else "NO",
        fillable="YES" if fillable else "NO",
        disallowed="YES" if disallowed else "NO",
        omitted="YES" if omitted else "NO",
        web_source_issue="YES" if web_source_issue else "NO",
        seed=seed,
        agreement=agreement,
        same_issue=same_issue,
    )


def make_b_output(scenario: str) -> str:
    if scenario in {"b_unfillable", "b_fillable", "web_b"}:
        fillable = "yes" if scenario == "b_fillable" else "no"
        web_confirmation = "Used a web lookup for context." if scenario == "web_b" else "no web sources used"
        return """1. Weakest point

Step 2 needs a missing compactness claim.

2. Why this is the weakest point

This is the first load-bearing transition in the mock proof that is not justified by the supplied materials.

3. Weakest point location

inside [KEY STEP]

4. Source status of the vulnerable claim

unsupported

5. Issue type

unjustified existence

6. What must be proved to close it (the missing claim)

Every minimizing sequence has a convergent subsequence under the stated hypotheses.

7. Fillable?

fillable: no - the mock report treats the needed compactness claim as genuinely missing.

8. Disallowed-premise check

Empty.

9. Web-source confirmation

{web_confirmation}

Final summary format:
Weakest point found? yes
Weakest point (step + claim, or "None"): Step 2 needs a missing compactness claim.
Weakest point location (inside key step / outside key step / blueprint / S1-S5 / no key step / unclear / not applicable): inside key step
Source status: unsupported
Missing claim, or "None": Every minimizing sequence has a convergent subsequence under the stated hypotheses.
Fillable: {fillable}
Disallowed premise at the weakest point? no
""".format(fillable=fillable, web_confirmation=web_confirmation)
    return """1. Weakest point

No weakest point found.

2. Why this is the weakest point

No non-routine vulnerable point is flagged in this mock report.

3. Weakest point location

unclear / not applicable

4. Source status of the vulnerable claim

standard background

5. Issue type

other

6. What must be proved to close it (the missing claim)

None.

7. Fillable?

fillable: not applicable - no weakest point is found.

8. Disallowed-premise check

Empty.

9. Web-source confirmation

no web sources used

Final summary format:
Weakest point found? no
Weakest point (step + claim, or "None"): None
Weakest point location (inside key step / outside key step / blueprint / S1-S5 / no key step / unclear / not applicable): not applicable
Source status: standard background
Missing claim, or "None": None
Fillable: not applicable
Disallowed premise at the weakest point? no
"""


def make_c_output(scenario: str) -> str:
    if scenario == "c_broke":
        broke = "yes"
        failing = "The asserted inequality is false in the boundary case."
        unsure = "None"
    elif scenario == "c_unsure":
        broke = "unsure"
        failing = "None"
        unsure = "Check whether the limiting interchange is justified by the allowed hypotheses."
    elif scenario == "web_c":
        broke = "no"
        failing = "None"
        unsure = "None"
    else:
        broke = "no"
        failing = "None"
        unsure = "None"
    web_confirmation = "Used a web lookup for context." if scenario == "web_c" else "no web sources used"
    return f"""1. Most serious possible failure point

Attack the key limiting step.

2. Exact location

The mock attack is located at the key limiting transition.

3. Attack location

inside [KEY STEP]

4. Source status of the vulnerable claim

standard background

5. Why the proof could fail there

The mock attack checks whether the proof's limiting step is justified by the allowed hypotheses.

6. Did it break?

broke: {broke} - see the final summary fields for the concrete result.

7. Disallowed-premise check

Empty.

8. Three most delicate points

1. Key limiting transition: check whether the limiting interchange is justified.
2. Boundary case: check whether the stated inequality remains valid.
3. Source status: check whether the needed fact is allowed or standard.

9. Web-source confirmation

{web_confirmation}

Final summary format:
Most serious attack (step + claim): Attack the key limiting step.
Attack location (inside key step / outside key step / blueprint / S1-S5 / no key step / unclear / not applicable): inside key step
Broke: {broke}
If broke, the false claim or failing step: {failing}
If unsure, exact check needed to decide: {unsure}
Source status: standard background
Disallowed premise at the attacked point? no
"""


def _a_report(
    run_id: str,
    *,
    non_fillable: str = "NO",
    fillable: str = "NO",
    disallowed: str = "NO",
    omitted: str = "NO",
    web_source_issue: str = "NO",
    seed: str = "None",
    marker: str = "",
) -> str:
    gap_line = (
        "Mock missing claim for this A run."
        if non_fillable == "YES" or fillable == "YES"
        else "Empty."
    )
    gap_fillability = (
        f"Mock missing claim for this A run.; fillable: {'no' if non_fillable == 'YES' else 'yes'}"
        if non_fillable == "YES" or fillable == "YES"
        else "Empty."
    )
    disallowed_line = "Mock disallowed premise cited by the proof." if disallowed == "YES" else "Empty."
    scope_line = "Mock omitted case or weaker-statement issue." if omitted == "YES" else "The full target statement is established in this mock report."
    return f"""1. Target restatement

Mock target theorem restatement for verifier run {run_id}.

2. Step ledger

1. JUSTIFIED: mock step justified from allowed materials.
2. {'GAP: ' + gap_line if gap_line != 'Empty.' else 'JUSTIFIED: mock final step justified from allowed materials.'}

3. Unfilled gaps

{gap_fillability}

4. Disallowed-premise check

{disallowed_line}

5. Scope check

{scope_line}

6. Coupling inventory

* Definitions/notation/assumptions from the cleaned skeleton PDF or TeX file actually used: [0 + []].
* Allowed formal skeleton statements used beyond definitions/notation/assumptions (statements in the Allowed list, appearing before the target): [0 + []].
* Disallowed skeleton statements cited (the target itself, anything equivalent to / stronger than / downstream of it, or anything appearing after it): [0 + []].
* Standard-background facts the core argument relies on: [mock standard background].
* Is the core argument carried mainly by standard background? yes, this mock fixture marks the route standard-background-heavy.

7. Blueprint and subproof consistency

Not applicable.

8. Web-source confirmation

no web sources used

9. Controller-facing summary

Non-fillable gaps present? {non_fillable}
Fillable-only gaps present? {fillable}
Disallowed premises present? {disallowed}
Omitted case / weaker statement present? {omitted}
Allowed formal skeleton statements used beyond definitions: [0 + []]
Disallowed skeleton statements cited: [0 + []]
Standard-background-heavy? YES
Blueprint present? N/A
[KEY STEP] present? N/A
Blueprint smuggling issue? N/A
Final proof follows blueprint? N/A
Web-source issue? {web_source_issue}
Candidate guidance seed, if any: {seed}
{marker}
Verifier run: {run_id}
"""


def _composer_report(
    *,
    non_fillable: str,
    fillable: str,
    disallowed: str,
    omitted: str,
    web_source_issue: str,
    seed: str,
    agreement: str,
    same_issue: str,
) -> str:
    gap_union = "Mock missing claim from at least one A report." if non_fillable == "YES" else "Empty."
    disallowed_union = "Mock disallowed premise from at least one A report." if disallowed == "YES" else "Empty."
    scope_check = "Mock omitted case or weaker-statement issue." if omitted == "YES" else "full"
    return f"""1. Gold step status

1. ALL-ACCEPTED: every mock report that addressed this step marked it justified.
2. {'CHALLENGED: at least one mock report raised a gap or concern here.' if non_fillable == 'YES' or disallowed == 'YES' or omitted == 'YES' else 'ALL-ACCEPTED: every mock report that addressed this step marked it justified.'}

2. Gold unfilled gaps (union)

{gap_union}

3. Gold disallowed premises (union)

{disallowed_union}

4. Gold scope check

{scope_check}

5. Gold coupling inventory

* allowed formal skeleton statements used beyond definitions/notation/assumptions: [0 + []].
* disallowed skeleton statements cited: [0 + []].
* standard-background-heavy? yes.

6. Disagreement map

* step/gap disagreement: {'present' if agreement == 'no majority' else 'none surfaced'}.
* fillability disagreement: none surfaced.
* disallowed-premise disagreement: {'present' if disallowed == 'YES' else 'none surfaced'}.
* scope disagreement: {'present' if omitted == 'YES' else 'none surfaced'}.
* coupling-count disagreement: none surfaced.

Same controller-verdict signal: {agreement}. Mock composer merged only A reports.
Implied status agreement: {agreement}

7. Web-source roll-up

Empty.

8. Gold Verifier A evidence report for the Decision Controller

Non-fillable gaps present? {non_fillable}
Fillable-only gaps present? {fillable}
Disallowed premises present? {disallowed}
Omitted case / weaker statement present? {omitted}
Allowed formal skeleton statements used beyond definitions: [0 + []]
Disallowed skeleton statements cited: [0 + []]
Standard-background-heavy? YES
Web-source issue? {web_source_issue}
Same issue recurring across reports? {same_issue}
Candidate guidance seed, if any: {seed}
"""
