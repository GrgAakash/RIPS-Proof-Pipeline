"""Offline tests for API verifier scaffolding.

These tests mock the API call. They must not spend API credits.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from verifiers.api_client import ApiVerifierResult
from verifiers.api_config import ApiConfig, load_api_config
from verifiers.api_runners import build_composer_a_prompt, build_verifier_a_prompt, build_verifier_b_prompt, build_verifier_c_prompt
from verifiers.api_smoke import (
    run_api_a1_smoke,
    run_api_a_stage_smoke,
    run_api_b_smoke,
    run_api_c_smoke,
    run_api_cascade,
    run_api_composer_a_smoke,
)
from verifiers.schemas import VerifierInput


ROOT = Path(__file__).resolve().parents[2]
_TEMP_DIR = tempfile.TemporaryDirectory()
unittest.addModuleCleanup(_TEMP_DIR.cleanup)
TMP_ROOT = Path(_TEMP_DIR.name)


def good_input() -> VerifierInput:
    return VerifierInput(
        target_theorem="For every integer n, n = n.",
        allowed_supporting_statements="Definitions and equality reflexivity are allowed.",
        guidance_list=[],
        proof_artifact="S0: prove reflexivity. S6: For any integer n, n = n by equality reflexivity.",
        skeleton_ref="toy-skeleton.tex#reflexivity",
    )


def fake_a1_output() -> str:
    return """1. Target restatement

For every integer n, n = n.

2. Step ledger

1. JUSTIFIED: equality reflexivity gives n = n.

3. Unfilled gaps

Empty.

4. Disallowed-premise check

Empty.

5. Scope check

The full target statement is established.

6. Coupling inventory

* Definitions/notation/assumptions from the cleaned skeleton PDF or TeX file actually used: [0 + []].
* Allowed formal skeleton statements used beyond definitions: [0 + []]
* Disallowed skeleton statements cited: [0 + []]
* Standard-background facts the core argument relies on: [equality reflexivity].
* Is the core argument carried mainly by standard background? yes.

7. Blueprint and subproof consistency

Not applicable.

8. Web-source confirmation

no web sources used

9. Controller-facing summary

Non-fillable gaps present? NO
Fillable-only gaps present? NO
Disallowed premises present? NO
Omitted case / weaker statement present? NO
Allowed formal skeleton statements used beyond definitions: [0 + []]
Disallowed skeleton statements cited: [0 + []]
Standard-background-heavy? YES
Blueprint present? N/A
[KEY STEP] present? N/A
Blueprint smuggling issue? N/A
Final proof follows blueprint? N/A
Web-source issue? NO
Candidate guidance seed, if any: None
"""


def fake_composer_a_output() -> str:
    return """1. Gold step status

Step 1: ALL-ACCEPTED.

2. Gold unfilled gaps (union)

Empty.

3. Gold disallowed premises (union)

Empty.

4. Gold scope check

full

5. Gold coupling inventory

Allowed formal skeleton statements used beyond definitions: [0 + []]
Disallowed skeleton statements cited: [0 + []]
Standard-background-heavy? YES

6. Disagreement map

No material disagreement.
Implied status agreement: all agree

7. Web-source roll-up

Empty.

8. Gold Verifier A evidence report for the Decision Controller

Non-fillable gaps present? NO
Fillable-only gaps present? NO
Disallowed premises present? NO
Omitted case / weaker statement present? NO
Allowed formal skeleton statements used beyond definitions: [0 + []]
Disallowed skeleton statements cited: [0 + []]
Standard-background-heavy? YES
Web-source issue? NO
Same issue recurring across reports? NO
Candidate guidance seed, if any: None
"""


def fake_composer_a_guidance_output() -> str:
    return """1. Gold step status

Step 6: CHALLENGED by A2.

2. Gold unfilled gaps (union)

Step 6 uniform asymptotic gap. Gold fillability: fillable: yes.

3. Gold disallowed premises (union)

Empty.

4. Gold scope check

Optimality needs the Step 6 fill.

5. Gold coupling inventory

Allowed formal skeleton statements used beyond definitions: 0 + []
Disallowed skeleton statements cited: 0 + []
Standard-background-heavy? YES

6. Disagreement map

Implied status agreement: majority agree (2 of 3)

7. Web-source roll-up

Empty.

8. Gold Verifier A evidence report for the Decision Controller

Non-fillable gaps present? NO
Fillable-only gaps present? YES
Disallowed premises present? NO
Omitted case / weaker statement present? YES
Allowed formal skeleton statements used beyond definitions: 0 + []
Disallowed skeleton statements cited: 0 + []
Standard-background-heavy? YES
Web-source issue? NO
Same issue recurring across reports? NO
Candidate guidance seed, if any: Make Step 6 uniform asymptotic control explicit.
"""


def fake_b_unfillable_output() -> str:
    return """1. Weakest point

Step 6 sharpness uniform asymptotic.

2. Why this is the weakest point

It blocks optimality.

3. Weakest point location

inside [KEY STEP]

4. Source status of the vulnerable claim

standard background; unsupported.

5. Issue type

unjustified inequality.

6. What must be proved to close it (the missing claim)

Uniform summable Taylor remainder.

7. Fillable?

fillable: no

8. Disallowed-premise check

Empty.

9. Web-source confirmation

no web sources used

Final summary format:

Weakest point found? yes
Weakest point (step + claim, or "None"): Step 6 sharpness uniform asymptotic
Weakest point location (inside key step / outside key step / blueprint / S1-S5 / no key step / unclear / not applicable): inside key step
Source status: unsupported
Missing claim, or "None": Uniform summable Taylor remainder.
Fillable: no
Disallowed premise at the weakest point? no
"""


def fake_b_fillable_output() -> str:
    return fake_b_unfillable_output().replace("fillable: no", "fillable: yes").replace("Fillable: no", "Fillable: yes")


def fake_c_broke_output() -> str:
    return """1. Most serious possible failure point

Step 6 boundary case.

2. Exact location

The cutoff limit.

3. Attack location

inside [KEY STEP]

4. Source status of the vulnerable claim

unsupported.

5. Why the proof could fail there

The limit exchange is not justified.

6. Did it break?

broke: yes - the cutoff limit fails as written.

7. Disallowed-premise check

Empty.

8. Three most delicate points

Cutoff, asymptotic, denominator positivity.

9. Web-source confirmation

no web sources used

Final summary format:

Most serious attack (step + claim): Step 6 boundary case
Attack location (inside key step / outside key step / blueprint / S1-S5 / no key step / unclear / not applicable): inside key step
Broke: yes
If broke, the false claim or failing step: the cutoff limit fails as written.
If unsure, exact check needed to decide: None
Source status: unsupported
Disallowed premise at the attacked point? no
"""


def fake_c_clean_output() -> str:
    return fake_c_broke_output().replace("broke: yes - the cutoff limit fails as written.", "broke: no - the proof is robust.").replace("Broke: yes", "Broke: no").replace("the cutoff limit fails as written.", "None")


class ApiSmokeTests(unittest.TestCase):
    def test_load_api_config_requires_key_unless_dry_run(self) -> None:
        with patch.dict(os.environ, {"OPENAI_API_KEY": "", "OPENAI_VERIFIER_DRY_RUN": ""}, clear=False):
            with self.assertRaises(RuntimeError):
                load_api_config(require_api_key=True)

        with patch.dict(os.environ, {"OPENAI_API_KEY": "", "OPENAI_VERIFIER_DRY_RUN": "1"}, clear=False):
            config = load_api_config(require_api_key=True)
            self.assertTrue(config.dry_run)
            self.assertFalse(config.api_key_present)

    def test_load_api_config_reads_optional_reasoning_effort(self) -> None:
        with patch.dict(
            os.environ,
            {
                "OPENAI_API_KEY": "test-key",
                "OPENAI_VERIFIER_REASONING_EFFORT": "low",
            },
            clear=False,
        ):
            config = load_api_config(require_api_key=True)
            self.assertEqual(config.reasoning_effort, "low")

    def test_build_verifier_a_prompt_contains_input_package(self) -> None:
        prompt = build_verifier_a_prompt(good_input(), run_id="A1")
        self.assertIn("Verifier run id:\nA1", prompt)
        self.assertIn("For every integer n, n = n.", prompt)
        self.assertIn("Allowed supporting statements:", prompt)
        self.assertIn("Proposed proof artifact P_k:", prompt)
        self.assertNotIn("[PASTE TARGET THEOREM]", prompt)
        self.assertNotIn("--- INPUTS FOR THIS RUN ---", prompt)

    def test_build_verifier_a_prompt_embeds_local_text_skeleton(self) -> None:
        skeleton_dir = TMP_ROOT / "api_prompt"
        skeleton_dir.mkdir(parents=True, exist_ok=True)
        skeleton_path = skeleton_dir / "mini_skeleton.tex"
        skeleton_path.write_text("\\begin{thm}Mini theorem.\\end{thm}\n", encoding="utf-8")

        inputs = VerifierInput(
            target_theorem="Mini theorem.",
            allowed_supporting_statements="Definitions only.",
            guidance_list=[],
            proof_artifact="S0: mini. S6: proof.",
            skeleton_ref=str(skeleton_path),
        )
        prompt = build_verifier_a_prompt(inputs, run_id="A1")

        self.assertIn("Cleaned skeleton text, if available:", prompt)
        self.assertIn("\\begin{thm}Mini theorem.\\end{thm}", prompt)

    def test_build_composer_a_prompt_is_blind_to_proof_inputs(self) -> None:
        prompt = build_composer_a_prompt(
            a_reports={"A1": "A1 says clean.", "A2": "A2 says gap.", "A3": "A3 says clean."}
        )
        self.assertIn("--- A1 REPORT ---", prompt)
        self.assertIn("A2 says gap.", prompt)
        self.assertNotIn("Target theorem:", prompt)
        self.assertNotIn("Proposed proof artifact P_k:", prompt)
        self.assertNotIn("[PASTE A1, A2, A3, ...]", prompt)

    def test_build_b_and_c_prompts_are_stage_isolated(self) -> None:
        b_prompt = build_verifier_b_prompt(good_input())
        c_prompt = build_verifier_c_prompt(good_input())
        self.assertIn("You are Verifier B", b_prompt)
        self.assertIn("You are Verifier C", c_prompt)
        self.assertNotIn("You are Verifier C", b_prompt)
        self.assertNotIn("Final Checker", c_prompt)

    def test_api_a1_smoke_with_mocked_api_call_writes_artifacts(self) -> None:
        output_root = TMP_ROOT / "api_a1_smoke"
        output_root.mkdir(parents=True, exist_ok=True)
        config = ApiConfig(model="mock-model", api_key_present=True)

        def fake_api_call(prompt: str) -> ApiVerifierResult:
            self.assertIn("Verifier run id:\nA1", prompt)
            return ApiVerifierResult(
                raw_text=fake_a1_output(),
                model="mock-model",
                usage={"input_tokens": 10, "output_tokens": 20},
                latency_ms=7,
            )

        summary = run_api_a1_smoke(
            good_input(),
            output_root=output_root,
            run_id="mocked_a1",
            config=config,
            api_call=fake_api_call,
        )

        self.assertEqual(summary["status"], "API_A1_SMOKE_PARSED")
        run_dir = output_root / "mocked_a1"
        self.assertTrue((run_dir / "inputs.json").exists())
        self.assertTrue((run_dir / "raw" / "verifier_a1.md").exists())
        self.assertTrue((run_dir / "parsed" / "verifier_a1.json").exists())
        self.assertTrue((run_dir / "parsed" / "api_verifier_a1_call.json").exists())

        parsed = json.loads((run_dir / "parsed" / "verifier_a1.json").read_text(encoding="utf-8"))
        self.assertEqual(parsed["non_fillable_gaps_present"], "NO")
        self.assertEqual(parsed["web_source_issue"], "NO")

    def test_api_a_stage_smoke_supports_a2_artifacts(self) -> None:
        output_root = TMP_ROOT / "api_a_stage_smoke"
        output_root.mkdir(parents=True, exist_ok=True)
        config = ApiConfig(model="mock-model", api_key_present=True)

        def fake_api_call(prompt: str) -> ApiVerifierResult:
            self.assertIn("Verifier run id:\nA2", prompt)
            return ApiVerifierResult(
                raw_text=fake_a1_output(),
                model="mock-model",
                usage={"input_tokens": 11, "output_tokens": 21},
                latency_ms=8,
            )

        summary = run_api_a_stage_smoke(
            good_input(),
            stage="A2",
            output_root=output_root,
            run_id="mocked_a2",
            config=config,
            api_call=fake_api_call,
        )

        self.assertEqual(summary["status"], "API_A2_SMOKE_PARSED")
        self.assertEqual(summary["stage"], "verifier_a2")
        run_dir = output_root / "mocked_a2"
        self.assertTrue((run_dir / "raw" / "verifier_a2.md").exists())
        self.assertTrue((run_dir / "parsed" / "verifier_a2.json").exists())
        self.assertTrue((run_dir / "parsed" / "api_verifier_a2_call.json").exists())

    def test_api_a_stage_model_setup_failure_is_not_parsed_as_verdict(self) -> None:
        output_root = TMP_ROOT / "api_a_stage_model_setup_failure"
        output_root.mkdir(parents=True, exist_ok=True)
        config = ApiConfig(model="mock-model", api_key_present=True)

        def fake_api_call(prompt: str) -> ApiVerifierResult:
            return ApiVerifierResult(
                raw_text="SETUP FAILURE: missing input.\n\nWeb-source confirmation: no web sources used.",
                model="mock-model",
                usage={"input_tokens": 12, "output_tokens": 22},
                latency_ms=9,
            )

        summary = run_api_a_stage_smoke(
            good_input(),
            stage="A2",
            output_root=output_root,
            run_id="model_setup_failure",
            config=config,
            api_call=fake_api_call,
        )

        self.assertEqual(summary["status"], "API_A2_MODEL_SETUP_FAILURE")
        self.assertEqual(summary["protocol_action"], "FIX_INPUT")
        run_dir = output_root / "model_setup_failure"
        self.assertTrue((run_dir / "raw" / "verifier_a2.md").exists())
        self.assertFalse((run_dir / "parsed" / "verifier_a2.json").exists())

    def test_api_a_stage_empty_output_is_call_failure(self) -> None:
        output_root = TMP_ROOT / "api_a_stage_empty_output"
        output_root.mkdir(parents=True, exist_ok=True)
        config = ApiConfig(model="mock-model", api_key_present=True)

        summary = run_api_a_stage_smoke(
            good_input(),
            stage="A1",
            output_root=output_root,
            run_id="empty_output",
            config=config,
            api_call=lambda prompt: ApiVerifierResult("", "mock-model", {"output_tokens": 3000}, 9),
        )

        self.assertEqual(summary["status"], "API_A1_EMPTY_OUTPUT")
        self.assertFalse((output_root / "empty_output" / "parsed" / "verifier_a1.json").exists())

    def test_api_composer_a_smoke_with_mocked_api_call_writes_artifacts(self) -> None:
        output_root = TMP_ROOT / "api_composer_a_smoke"
        output_root.mkdir(parents=True, exist_ok=True)
        config = ApiConfig(model="mock-model", api_key_present=True)

        def fake_api_call(prompt: str) -> ApiVerifierResult:
            self.assertIn("--- A1 REPORT ---", prompt)
            self.assertIn("--- A2 REPORT ---", prompt)
            self.assertIn("--- A3 REPORT ---", prompt)
            self.assertNotIn("Proposed proof artifact P_k:", prompt)
            return ApiVerifierResult(
                raw_text=fake_composer_a_output(),
                model="mock-model",
                usage={"input_tokens": 31, "output_tokens": 41},
                latency_ms=10,
            )

        summary = run_api_composer_a_smoke(
            a_reports={"A1": "a1", "A2": "a2", "A3": "a3"},
            skeleton_ref="toy-skeleton.tex",
            output_root=output_root,
            run_id="mocked_composer_a",
            config=config,
            api_call=fake_api_call,
        )

        self.assertEqual(summary["status"], "API_COMPOSER_A_SMOKE_PARSED")
        self.assertEqual(summary["derived_a_status"], "A_VERIFIED")
        run_dir = output_root / "mocked_composer_a"
        self.assertTrue((run_dir / "raw" / "composer_a.md").exists())
        self.assertTrue((run_dir / "parsed" / "composer_a.json").exists())
        self.assertTrue((run_dir / "parsed" / "api_composer_a_call.json").exists())

    def test_api_composer_a_smoke_writes_next_guidance_handoff(self) -> None:
        output_root = TMP_ROOT / "api_composer_a_guidance"
        output_root.mkdir(parents=True, exist_ok=True)
        config = ApiConfig(model="mock-model", api_key_present=True)

        def fake_api_call(prompt: str) -> ApiVerifierResult:
            return ApiVerifierResult(
                raw_text=fake_composer_a_guidance_output(),
                model="mock-model",
                usage={"input_tokens": 32, "output_tokens": 42},
                latency_ms=11,
            )

        summary = run_api_composer_a_smoke(
            a_reports={"A1": "a1", "A2": "a2", "A3": "a3"},
            skeleton_ref="toy-skeleton.tex",
            output_root=output_root,
            run_id="mocked_composer_a_guidance",
            config=config,
            api_call=fake_api_call,
        )

        self.assertEqual(summary["cascade_route_status"], "STOPPED_GUIDANCE_SEED")
        run_dir = output_root / "mocked_composer_a_guidance"
        handoff = json.loads((run_dir / "next_guidance.json").read_text(encoding="utf-8"))
        self.assertEqual(handoff["guidance_list"], ["Make Step 6 uniform asymptotic control explicit."])
        self.assertEqual(handoff["protocol_next_step"], "FRESH_MULTI_SOLVER_RUN_FROM_S0")
        self.assertEqual(handoff["rerun_starts_at"], "S0_BLUEPRINT")

    def test_api_b_unfillable_writes_next_guidance_handoff(self) -> None:
        output_root = TMP_ROOT / "api_b_unfillable"
        output_root.mkdir(parents=True, exist_ok=True)
        config = ApiConfig(model="mock-model", api_key_present=True)

        summary = run_api_b_smoke(
            good_input(),
            derived_a_status="A_VERIFIED",
            output_root=output_root,
            run_id="mocked_b_unfillable",
            config=config,
            api_call=lambda prompt: ApiVerifierResult(fake_b_unfillable_output(), "mock-model", {}, 12),
        )

        self.assertEqual(summary["cascade_route_status"], "STOPPED_AFTER_B")
        handoff = json.loads((output_root / "mocked_b_unfillable" / "next_guidance.json").read_text(encoding="utf-8"))
        self.assertEqual(handoff["guidance_list"], ["Uniform summable Taylor remainder."])

    def test_api_b_fillable_continues_to_c(self) -> None:
        output_root = TMP_ROOT / "api_b_fillable"
        output_root.mkdir(parents=True, exist_ok=True)
        config = ApiConfig(model="mock-model", api_key_present=True)

        summary = run_api_b_smoke(
            good_input(),
            derived_a_status="A_VERIFIED",
            output_root=output_root,
            run_id="mocked_b_fillable",
            config=config,
            api_call=lambda prompt: ApiVerifierResult(fake_b_fillable_output(), "mock-model", {}, 13),
        )

        self.assertEqual(summary["cascade_route_status"], "CONTINUE_TO_C")
        self.assertFalse((output_root / "mocked_b_fillable" / "next_guidance.json").exists())

    def test_api_c_broke_writes_next_guidance_handoff(self) -> None:
        output_root = TMP_ROOT / "api_c_broke"
        output_root.mkdir(parents=True, exist_ok=True)
        config = ApiConfig(model="mock-model", api_key_present=True)

        summary = run_api_c_smoke(
            good_input(),
            derived_a_status="A_VERIFIED",
            output_root=output_root,
            run_id="mocked_c_broke",
            config=config,
            api_call=lambda prompt: ApiVerifierResult(fake_c_broke_output(), "mock-model", {}, 14),
        )

        self.assertEqual(summary["cascade_route_status"], "COMPLETED_C_BROKE")
        handoff = json.loads((output_root / "mocked_c_broke" / "next_guidance.json").read_text(encoding="utf-8"))
        self.assertEqual(handoff["guidance_list"], ["the cutoff limit fails as written."])

    def test_api_c_clean_hands_off_to_final_checker_gate(self) -> None:
        output_root = TMP_ROOT / "api_c_clean"
        output_root.mkdir(parents=True, exist_ok=True)
        config = ApiConfig(model="mock-model", api_key_present=True)

        summary = run_api_c_smoke(
            good_input(),
            derived_a_status="A_VERIFIED",
            output_root=output_root,
            run_id="mocked_c_clean",
            config=config,
            api_call=lambda prompt: ApiVerifierResult(fake_c_clean_output(), "mock-model", {}, 15),
        )

        self.assertEqual(summary["cascade_route_status"], "COMPLETED_C_CLEAN")
        self.assertEqual(summary["protocol_next_step"], "FINAL_CHECKER_GATE")
        self.assertFalse((output_root / "mocked_c_clean" / "next_guidance.json").exists())

    def test_api_a1_setup_failure_does_not_call_api(self) -> None:
        output_root = TMP_ROOT / "api_a1_setup_failure"
        output_root.mkdir(parents=True, exist_ok=True)
        config = ApiConfig(model="mock-model", api_key_present=True)

        def forbidden_api_call(prompt: str) -> ApiVerifierResult:
            raise AssertionError("API call should not run when setup inputs are missing")

        summary = run_api_a1_smoke(
            VerifierInput(
                target_theorem="",
                allowed_supporting_statements="Allowed.",
                proof_artifact="Proof.",
                skeleton_ref="toy",
            ),
            output_root=output_root,
            run_id="setup_failure",
            config=config,
            api_call=forbidden_api_call,
        )

        self.assertEqual(summary["status"], "API_A1_SETUP_FAILURE")
        self.assertFalse(summary["api_call_made"])
        self.assertIn("target_theorem", summary["missing_inputs"])

    def test_api_cascade_clean_runs_through_c(self) -> None:
        output_root = TMP_ROOT / "api_cascade_clean"
        output_root.mkdir(parents=True, exist_ok=True)
        config = ApiConfig(model="mock-model", api_key_present=True)
        responses = [
            fake_a1_output(),
            fake_a1_output(),
            fake_a1_output(),
            fake_composer_a_output(),
            fake_b_fillable_output(),
            fake_c_clean_output(),
        ]

        def fake_api_call(prompt: str) -> ApiVerifierResult:
            return ApiVerifierResult(responses.pop(0), "mock-model", {}, 1)

        summary = run_api_cascade(
            good_input(),
            output_root=output_root,
            run_id="mocked_cascade_clean",
            config=config,
            api_call=fake_api_call,
        )

        self.assertEqual(summary["status"], "COMPLETED_C_CLEAN")
        self.assertEqual(summary["protocol_next_step"], "FINAL_CHECKER_GATE")
        self.assertEqual(len(summary["stage_summaries"]), 6)
        self.assertEqual(responses, [])
        run_dir = output_root / "mocked_cascade_clean"
        self.assertTrue((run_dir / "summary.json").exists())
        self.assertTrue((run_dir / "stages" / "a1" / "raw" / "verifier_a1.md").exists())
        self.assertTrue((run_dir / "stages" / "composer_a" / "raw" / "composer_a.md").exists())
        self.assertTrue((run_dir / "stages" / "verifier_c" / "raw" / "verifier_c.md").exists())

    def test_api_cascade_stops_after_composer_guidance(self) -> None:
        output_root = TMP_ROOT / "api_cascade_guidance"
        output_root.mkdir(parents=True, exist_ok=True)
        config = ApiConfig(model="mock-model", api_key_present=True)
        responses = [
            fake_a1_output(),
            fake_a1_output(),
            fake_a1_output(),
            fake_composer_a_guidance_output(),
            fake_b_fillable_output(),
        ]

        def fake_api_call(prompt: str) -> ApiVerifierResult:
            return ApiVerifierResult(responses.pop(0), "mock-model", {}, 1)

        summary = run_api_cascade(
            good_input(),
            output_root=output_root,
            run_id="mocked_cascade_guidance",
            config=config,
            api_call=fake_api_call,
        )

        self.assertEqual(summary["status"], "STOPPED_GUIDANCE_SEED")
        self.assertEqual(summary["protocol_next_step"], "FRESH_MULTI_SOLVER_RUN_FROM_S0")
        self.assertEqual(len(summary["stage_summaries"]), 4)
        self.assertEqual(len(responses), 1)
        run_dir = output_root / "mocked_cascade_guidance"
        handoff = json.loads((run_dir / "next_guidance.json").read_text(encoding="utf-8"))
        self.assertEqual(handoff["guidance_list"], ["Make Step 6 uniform asymptotic control explicit."])
        self.assertFalse((run_dir / "stages" / "verifier_b").exists())


if __name__ == "__main__":
    unittest.main()
