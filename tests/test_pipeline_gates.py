from __future__ import annotations

import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
COMPONENT_ROOT = ROOT / "Individual Pipeline"
if str(COMPONENT_ROOT) not in sys.path:
    sys.path.insert(0, str(COMPONENT_ROOT))

from citation.prompts import (
    CitationPromptTemplates,
    build_citation_generator_prompt,
)

from solver.cleaner_bridge import (
    CleanerPackage,
    CleanerSections,
    export_solver_bundle,
    sha256_text,
)
from solver.controller import (
    ControllerConfig,
    route_after_problem_statement_verifier,
)
from solver.report_parsers import parse_problem_statement_report
from solver.schemas import (
    OUTCOME_RERUN_UNCHANGED,
    OUTCOME_RUN_NEXT_STAGE,
    PipelineState,
)
from solver.cli import _make_client, _preflight_private_final_checker
from solver.skeleton_source_gate import (
    SkeletonSourceGateDecision,
    _generator_gate,
    _verifier_gate,
)


def _generator_item() -> dict[str, str]:
    return {
        "grant_id": "R1",
        "source_status": "VERIFIED",
        "source_identifier": "source-key",
        "exact_statement_checked": "YES",
        "hypotheses_checked": "YES",
        "source_location": "Theorem 1",
        "url_or_reference_checked": "https://example.invalid/source",
    }


def _verifier_item() -> dict[str, str]:
    return {
        "grant_id": "R1",
        "verdict": "VERIFIED",
        "source_identifier": "source-key",
        "exact_location_checked": "Theorem 1",
        "explanation": "The statement and hypotheses match.",
    }


class SkeletonSourceDecisionTests(unittest.TestCase):
    def test_generator_requires_clear_complete_approval(self) -> None:
        summary = {
            "possible_target_source_leakage": "NO",
            "unsupported_or_unclear_grants": "NO",
            "recommended_next_step": "PROCEED_TO_SKELETON_SOURCE_VERIFIER",
        }
        self.assertIsNone(_generator_gate(["R1"], ["R1"], [_generator_item()], summary))

        unclear = dict(summary)
        unclear.pop("possible_target_source_leakage")
        self.assertEqual(
            _generator_gate(["R1"], ["R1"], [_generator_item()], unclear)[0],
            "UNCLEAR",
        )
        self.assertEqual(
            _generator_gate(["R1"], [], [], summary)[0],
            "UNCLEAR",
        )

    def test_verifier_good_to_go_requires_all_negative_issue_fields(self) -> None:
        summary = {
            "possible_target_source_leakage": "NO",
            "missing_grants": "NO",
            "source_location_issues": "NO",
            "hypothesis_mismatches": "NO",
            "unsupported_or_unclear_grants": "NO",
            "gate_result": "GOOD_TO_GO",
        }
        self.assertEqual(
            _verifier_gate(["R1"], ["R1"], [_verifier_item()], summary)[0],
            "GOOD_TO_GO",
        )

        unclear = dict(summary)
        unclear["hypothesis_mismatches"] = "UNCLEAR"
        self.assertEqual(
            _verifier_gate(["R1"], ["R1"], [_verifier_item()], unclear)[0],
            "UNCLEAR",
        )
        blocked = dict(summary)
        blocked["source_location_issues"] = "YES"
        self.assertEqual(
            _verifier_gate(["R1"], ["R1"], [_verifier_item()], blocked)[0],
            "BLOCKING_SOURCE_ISSUE",
        )


class CleanerBridgeExportTests(unittest.TestCase):
    def test_export_solver_bundle_keeps_private_material_out_by_default(self) -> None:
        problem_text = "synthetic audited cleaner problem"
        package = CleanerPackage(
            paper_id="paper-1",
            target_id="theorem-1",
            problem_path=Path("problem.md"),
            problem_text=problem_text,
            problem_sha256=sha256_text(problem_text),
            sections=CleanerSections(
                skeleton="## 0. Macro definitions\nNone\n\n## 1. Notation and conventions\nNone",
                target="**Theorem 1.** For every integer n, n = n.",
                section3="",
                section5="**Lemma 1.** Equality is reflexive.",
            ),
            bibliography="",
            target_proof="Private proof text.",
            full_source="Private full source.",
            stage2_report={},
            audit_record={
                "audit": {
                    "self_contained": True,
                    "leak_free": True,
                    "sufficient": True,
                    "issues": [],
                }
            },
            audit_model="mock-auditor",
            cleaner_models={"author": "mock-author"},
            target_statement_sha256=sha256_text(
                "For every integer n, n = n."),
            target_proof_sha256=sha256_text("Private proof text."),
        )
        decision = SkeletonSourceGateDecision(
            gate_result="NOT_APPLICABLE",
            reason="Section 3 contains no external grants.",
            expected_grant_ids=[],
            generator_grant_ids=[],
            verifier_grant_ids=[],
            verifier_ran=False,
            generator_summary={},
        )
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            gate_dir = temp_root / "source_gate"
            gate_dir.mkdir()
            (gate_dir / "skeleton_source_gate_decision.json").write_text(
                json.dumps(decision.to_dict(), indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            output = export_solver_bundle(
                package=package,
                output_dir=temp_root / "prepared",
                packet_path=ROOT / "Prompt Packet" / "Prompts.md",
                classification_tag="protocol_validation",
                source_gate_decision=decision,
                source_gate_dir=gate_dir,
                source_audit_model="mock-source-auditor",
            )

            self.assertTrue((output / "target.md").is_file())
            self.assertTrue((output / "skeleton.md").is_file())
            self.assertTrue((output / "allowed_support.md").is_file())
            self.assertFalse((output / "private").exists())
            manifest = json.loads((output / "setup_manifest.json").read_text())
            self.assertFalse(manifest["private_final_checker_material"])
            self.assertEqual(manifest["solver_internet_mode"], "none")


class ProblemStatementGateTests(unittest.TestCase):
    def test_match_continues_and_mismatch_reruns_without_guidance(self) -> None:
        state = PipelineState(problem_id="toy")
        config = ControllerConfig()
        matching = parse_problem_statement_report(
            """Artifact role checked: Solver proof
Problem statement match? YES
Actual statement addressed: Exact target.
Mismatch type, if any: none
Recommended controller action: continue
"""
        )
        mismatch = parse_problem_statement_report(
            """Artifact role checked: Solver proof
Problem statement match? NO
Actual statement addressed: A special case.
Mismatch type, if any: special case only
Recommended controller action: rerun Solver with exact target
"""
        )
        self.assertEqual(
            route_after_problem_statement_verifier(matching, state, config).outcome,
            OUTCOME_RUN_NEXT_STAGE,
        )
        self.assertEqual(
            route_after_problem_statement_verifier(mismatch, state, config).outcome,
            OUTCOME_RERUN_UNCHANGED,
        )


class RuntimeSafetyTests(unittest.TestCase):
    def test_citation_builder_defaults_to_canonical_packet(self) -> None:
        values = {
            "target_theorem": "Target",
            "provided_packet": "Public packet",
            "allowed_supporting_statements": "Allowed facts",
            "guidance": "None",
            "proof": "Candidate proof",
            "solver_source_ledger": "None",
            "bibliography": "None",
        }
        default = build_citation_generator_prompt(**values)
        canonical = build_citation_generator_prompt(
            **values,
            prompt_templates=CitationPromptTemplates.from_file(
                ROOT / "Prompt Packet" / "Prompts.md"
            ),
        )
        self.assertEqual(default, canonical)

    def test_environment_cannot_enable_web_for_verifier_roles(self) -> None:
        args = Namespace(
            client="openai",
            model="mock-model",
            api_base_url=None,
            api_key=None,
            api_key_env="OPENAI_API_KEY",
            api_key_file=None,
            api_surface="responses",
            reasoning_effort=None,
            retry_max_attempts=1,
            input_price=None,
            output_price=None,
        )
        with patch.dict(
            "os.environ", {"OPENAI_WEB_SEARCH_ROLES": "verifier_a"}, clear=False
        ):
            with self.assertRaisesRegex(RuntimeError, "web search is forbidden"):
                _make_client(args)

    def test_private_checker_preflight_rejects_missing_proof_before_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            index_path = root / "paper-1" / "index" / "statements.v2.json"
            index_path.parent.mkdir(parents=True)
            index_path.write_text(
                json.dumps(
                    {
                        "statements": [
                            {"id": "theorem-1", "proof_tex": ""},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuntimeError, "no extractable proof"):
                _preflight_private_final_checker(root, "paper-1", "theorem-1")


if __name__ == "__main__":
    unittest.main()
