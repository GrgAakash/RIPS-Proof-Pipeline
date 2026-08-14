"""Routing and run-storage tests for the standalone mock verifier pipeline."""

from __future__ import annotations

import inspect
import json
import tempfile
import unittest
from pathlib import Path

from verifiers.mock import compose_a_output
from verifiers.orchestrator import _route_after_c, run_mock_pipeline
from verifiers.schemas import CReport, VerifierInput


ROOT = Path(__file__).resolve().parents[2]
_TEMP_DIR = tempfile.TemporaryDirectory()
unittest.addModuleCleanup(_TEMP_DIR.cleanup)
TMP_ROOT = Path(_TEMP_DIR.name)


def _test_output_root(name: str) -> Path:
    path = TMP_ROOT / "_unit_tests" / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def good_input() -> VerifierInput:
    return VerifierInput(
        target_theorem="Target theorem text",
        allowed_supporting_statements="Definitions and allowed statements",
        guidance_list=[],
        proof_artifact="Candidate proof text",
        skeleton_ref="skeleton.tex#theorem-1",
    )


class OrchestratorTests(unittest.TestCase):
    def run_scenario(self, scenario: str):
        tmp = _test_output_root(scenario)
        summary = run_mock_pipeline(good_input(), output_root=tmp, scenario=scenario, run_id=f"run_{scenario}")
        summary_path = tmp / f"run_{scenario}" / "summary.json"
        self.assertTrue(summary_path.exists())
        stored = json.loads(summary_path.read_text(encoding="utf-8"))
        self.assertEqual(stored["status"], summary.status)
        self.assertEqual(stored["protocol_next_step"], summary.protocol_next_step)
        return summary

    def test_inputs_json_uses_new_input_package_names(self) -> None:
        tmp = _test_output_root("inputs_shape")
        run_mock_pipeline(good_input(), output_root=tmp, scenario="clean", run_id="inputs_shape")
        inputs = json.loads((tmp / "inputs_shape" / "inputs.json").read_text(encoding="utf-8"))
        self.assertEqual(inputs["guidance_list"], [])
        self.assertEqual(inputs["proof_artifact"], "Candidate proof text")
        self.assertEqual(inputs["allowed_supporting_statements"], "Definitions and allowed statements")
        self.assertNotIn("proposed_proof", inputs)
        self.assertNotIn("allowed_statements", inputs)

    def test_legacy_input_alias_maps_proposed_proof_to_proof_artifact(self) -> None:
        legacy = VerifierInput(
            target_theorem="Target theorem text",
            allowed_statements="Definitions and allowed statements",
            guidance="Keep the proof local.",
            proposed_proof="Legacy candidate proof",
            skeleton_ref="skeleton.tex#theorem-1",
        )
        tmp = _test_output_root("legacy_inputs")
        run_mock_pipeline(legacy, output_root=tmp, scenario="clean", run_id="legacy_inputs")
        inputs = json.loads((tmp / "legacy_inputs" / "inputs.json").read_text(encoding="utf-8"))
        self.assertEqual(inputs["proof_artifact"], "Legacy candidate proof")
        self.assertEqual(inputs["guidance_list"], ["Keep the proof local."])

    def test_clean_cascade_runs_b_and_c_then_goes_to_final_checker_gate(self) -> None:
        summary = self.run_scenario("clean")
        self.assertEqual(summary.status, "COMPLETED_C_CLEAN")
        self.assertEqual(summary.derived_a_status, "A_VERIFIED")
        self.assertEqual(summary.protocol_next_step, "FINAL_CHECKER_GATE")
        self.assertEqual(summary.current_cascade_action, "CASCADE_CLEAR")
        self.assertTrue(summary.b_ran)
        self.assertTrue(summary.c_ran)

    def test_disallowed_premise_ends_current_cascade_and_reruns_solver_from_s0(self) -> None:
        summary = self.run_scenario("disallowed_premise")
        self.assertEqual(summary.status, "STOPPED_DISALLOWED_PREMISE")
        self.assertEqual(summary.protocol_action, "RERUN_SOLVER_WITH_GUIDANCE")
        self.assertEqual(summary.protocol_source, "A")
        self.assertEqual(summary.protocol_next_step, "FRESH_MULTI_SOLVER_RUN_FROM_S0")
        self.assertEqual(summary.rerun_starts_at, "S0_BLUEPRINT")
        self.assertEqual(summary.current_cascade_action, "END_CURRENT_VERIFIER_CASCADE")
        self.assertFalse(summary.b_ran)
        self.assertFalse(summary.c_ran)

    def test_disallowed_premise_without_guidance_seed_still_reruns_solver_from_s0(self) -> None:
        summary = self.run_scenario("disallowed_premise_no_seed")
        self.assertEqual(summary.status, "STOPPED_DISALLOWED_PREMISE")
        self.assertEqual(summary.protocol_action, "RERUN_SOLVER_WITH_GUIDANCE")
        self.assertEqual(summary.protocol_source, "A")
        self.assertEqual(summary.protocol_next_step, "FRESH_MULTI_SOLVER_RUN_FROM_S0")
        self.assertEqual(summary.rerun_starts_at, "S0_BLUEPRINT")
        self.assertEqual(summary.current_cascade_action, "END_CURRENT_VERIFIER_CASCADE")
        self.assertEqual(
            summary.candidate_guidance_seed,
            "Remove the disallowed premise and prove the needed claim using only allowed supporting statements.",
        )
        self.assertFalse(summary.b_ran)
        self.assertFalse(summary.c_ran)


    def test_no_majority_ends_current_cascade_for_math_gap_adjudication(self) -> None:
        summary = self.run_scenario("no_majority")
        self.assertEqual(summary.status, "STOPPED_NO_MAJORITY")
        self.assertEqual(summary.protocol_action, "HUMAN_ADJUDICATION_REQUIRED")
        self.assertEqual(summary.protocol_source, "A")
        self.assertEqual(summary.protocol_next_step, "MATH_GAP_ADJUDICATION")
        self.assertIsNone(summary.rerun_starts_at)
        self.assertIsNone(summary.candidate_guidance_seed)
        self.assertFalse(summary.b_ran)
        self.assertFalse(summary.c_ran)

    def test_ordinary_disagreement_does_not_trigger_no_majority_stop(self) -> None:
        summary = self.run_scenario("ordinary_disagreement")
        self.assertNotEqual(summary.status, "STOPPED_NO_MAJORITY")
        self.assertTrue(summary.b_ran)
        self.assertTrue(summary.c_ran)

    def test_guidance_seed_ends_current_cascade_and_reruns_solver_from_s0(self) -> None:
        tmp = _test_output_root("guidance_seed")
        summary = run_mock_pipeline(good_input(), output_root=tmp, scenario="guidance_seed", run_id="run_guidance_seed")
        handoff_path = tmp / "run_guidance_seed" / "next_guidance.json"
        self.assertEqual(summary.status, "STOPPED_GUIDANCE_SEED")
        self.assertEqual(summary.derived_a_status, "A_NOT_VERIFIED")
        self.assertEqual(summary.protocol_action, "RERUN_SOLVER_WITH_GUIDANCE")
        self.assertEqual(summary.protocol_source, "A")
        self.assertEqual(summary.protocol_next_step, "FRESH_MULTI_SOLVER_RUN_FROM_S0")
        self.assertEqual(summary.rerun_starts_at, "S0_BLUEPRINT")
        self.assertIn("compactness", summary.candidate_guidance_seed)
        self.assertFalse(summary.b_ran)
        self.assertFalse(summary.c_ran)
        handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
        self.assertEqual(handoff["guidance_list"], [summary.candidate_guidance_seed])
        self.assertEqual(handoff["protocol_next_step"], "FRESH_MULTI_SOLVER_RUN_FROM_S0")
        self.assertEqual(handoff["rerun_starts_at"], "S0_BLUEPRINT")

    def test_non_fillable_gap_without_guidance_seed_continues_to_b_and_c_but_does_not_auto_accept(self) -> None:
        summary = self.run_scenario("non_fillable_no_seed")
        self.assertEqual(summary.status, "COMPLETED_C_CLEAN")
        self.assertEqual(summary.derived_a_status, "A_NOT_VERIFIED")
        self.assertEqual(summary.protocol_action, "HUMAN_ADJUDICATION_REQUIRED")
        self.assertEqual(summary.protocol_source, "A")
        self.assertEqual(summary.protocol_next_step, "MATH_GAP_ADJUDICATION")
        self.assertEqual(summary.current_cascade_action, "END_CURRENT_VERIFIER_CASCADE")
        self.assertTrue(summary.b_ran)
        self.assertTrue(summary.c_ran)

    def test_b_unfillable_ends_current_cascade_and_reruns_solver_from_s0_with_b_guidance(self) -> None:
        summary = self.run_scenario("b_unfillable")
        self.assertEqual(summary.status, "STOPPED_AFTER_B")
        self.assertEqual(summary.protocol_action, "RERUN_SOLVER_WITH_GUIDANCE")
        self.assertEqual(summary.protocol_source, "B")
        self.assertEqual(summary.protocol_next_step, "FRESH_MULTI_SOLVER_RUN_FROM_S0")
        self.assertEqual(summary.rerun_starts_at, "S0_BLUEPRINT")
        self.assertEqual(summary.current_cascade_action, "END_CURRENT_VERIFIER_CASCADE")
        self.assertIn("minimizing sequence", summary.candidate_guidance_seed)
        self.assertTrue(summary.b_ran)
        self.assertFalse(summary.c_ran)

    def test_b_fillable_yes_continues_to_c(self) -> None:
        summary = self.run_scenario("b_fillable")
        self.assertEqual(summary.status, "COMPLETED_C_CLEAN")
        self.assertTrue(summary.b_ran)
        self.assertTrue(summary.c_ran)

    def test_a_unclear_with_clean_c_goes_to_math_gap_adjudication_not_final_checker_gate(self) -> None:
        summary = _route_after_c(
            "skeleton.tex#theorem-1",
            CReport(skeleton_ref="skeleton.tex#theorem-1", raw_text="Broke: no", broke="no"),
            "A_UNCLEAR",
        )
        self.assertEqual(summary.status, "COMPLETED_C_CLEAN")
        self.assertEqual(summary.derived_a_status, "A_UNCLEAR")
        self.assertEqual(summary.protocol_action, "HUMAN_ADJUDICATION_REQUIRED")
        self.assertEqual(summary.protocol_source, "A")
        self.assertEqual(summary.protocol_next_step, "MATH_GAP_ADJUDICATION")
        self.assertEqual(summary.current_cascade_action, "END_CURRENT_VERIFIER_CASCADE")

    def test_c_broke_yes_ends_current_cascade_and_reruns_solver_from_s0_with_c_guidance(self) -> None:
        summary = self.run_scenario("c_broke")
        self.assertEqual(summary.status, "COMPLETED_C_BROKE")
        self.assertEqual(summary.protocol_action, "RERUN_SOLVER_WITH_GUIDANCE")
        self.assertEqual(summary.protocol_source, "C")
        self.assertEqual(summary.protocol_next_step, "FRESH_MULTI_SOLVER_RUN_FROM_S0")
        self.assertEqual(summary.rerun_starts_at, "S0_BLUEPRINT")
        self.assertEqual(summary.current_cascade_action, "END_CURRENT_VERIFIER_CASCADE")
        self.assertIn("boundary case", summary.candidate_guidance_seed)
        self.assertTrue(summary.b_ran)
        self.assertTrue(summary.c_ran)

    def test_c_broke_unsure_routes_to_math_gap_adjudication(self) -> None:
        summary = self.run_scenario("c_unsure")
        self.assertEqual(summary.status, "COMPLETED_C_UNSURE")
        self.assertEqual(summary.protocol_action, "HUMAN_ADJUDICATION_REQUIRED")
        self.assertEqual(summary.protocol_source, "C")
        self.assertEqual(summary.protocol_next_step, "MATH_GAP_ADJUDICATION")
        self.assertEqual(summary.current_cascade_action, "END_CURRENT_VERIFIER_CASCADE")
        self.assertIn("limiting interchange", summary.candidate_guidance_seed)
        self.assertTrue(summary.b_ran)
        self.assertTrue(summary.c_ran)

    def test_web_contamination_stops_the_cascade(self) -> None:
        for scenario, b_ran, c_ran in (("web_a", False, False), ("web_b", True, False), ("web_c", True, True)):
            with self.subTest(scenario=scenario):
                summary = self.run_scenario(scenario)
                self.assertEqual(summary.status, "STOPPED_WEB_CONTAMINATION")
                self.assertEqual(summary.protocol_action, "VOID_OR_MANUAL_REVIEW")
                self.assertEqual(summary.protocol_next_step, "WEB_CONTAMINATION_REVIEW")
                self.assertEqual(summary.current_cascade_action, "END_CURRENT_VERIFIER_CASCADE")
                self.assertEqual(summary.b_ran, b_ran)
                self.assertEqual(summary.c_ran, c_ran)

    def test_clean_c_with_low_coupling_metadata_routes_to_provenance_adjudication(self) -> None:
        inputs = VerifierInput(
            target_theorem="Target theorem text",
            allowed_supporting_statements="Definitions and allowed statements",
            guidance_list=[],
            proof_artifact="Candidate proof text",
            skeleton_ref="skeleton.tex#theorem-1",
            run_metadata={
                "run_tags": ["paper_original_result"],
                "allowed_proof_skeleton_coupling": "LOW",
            },
        )
        tmp = _test_output_root("low_coupling")
        summary = run_mock_pipeline(inputs, output_root=tmp, scenario="clean", run_id="low_coupling")
        self.assertEqual(summary.status, "COMPLETED_C_CLEAN_LOW_COUPLING")
        self.assertEqual(summary.protocol_action, "HUMAN_ADJUDICATION_REQUIRED")
        self.assertEqual(summary.protocol_next_step, "COUPLING_PROVENANCE_ADJUDICATION")
        self.assertEqual(summary.current_cascade_action, "CASCADE_CLEAR_WITH_PROVENANCE_BLOCK")

    def test_setup_failure_is_not_a_proof_verdict(self) -> None:
        missing = VerifierInput(
            target_theorem="",
            allowed_supporting_statements="Definitions and allowed statements",
            guidance_list=[],
            proof_artifact="Candidate proof text",
            skeleton_ref="",
        )
        tmp = _test_output_root("setup_failure")
        summary = run_mock_pipeline(missing, output_root=tmp, scenario="clean", run_id="setup_failure")
        self.assertEqual(summary.status, "SETUP_FAILURE")
        self.assertEqual(summary.stopped_stage, "setup")
        self.assertEqual(summary.protocol_action, "FIX_INPUT")
        self.assertEqual(summary.protocol_next_step, "FIX_INPUT_AND_RERUN")
        self.assertIn("target_theorem", summary.missing_inputs)
        self.assertIn("skeleton_ref", summary.missing_inputs)
        self.assertFalse(summary.b_ran)
        self.assertFalse(summary.c_ran)

    def test_composer_a_signature_enforces_blindness(self) -> None:
        params = set(inspect.signature(compose_a_output).parameters)
        self.assertEqual(params, {"a_reports", "step_map"})
        self.assertTrue({"proof", "skeleton", "target_theorem", "allowed_statements"}.isdisjoint(params))


if __name__ == "__main__":
    unittest.main()
