"""Integrity checks for the archived manual run, not a new mathematical verdict."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import unittest
from pathlib import Path

from citation.parsers import parse_citation_generator_report, parse_citation_verifier_report
from solver.report_parsers import (
    parse_composer_a_report, parse_composer_output, parse_problem_statement_report,
    parse_s0_key_solver, parse_subproblem_output, parse_verifier_b_report,
    parse_verifier_c_report,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "Examples" / "cayley"


class CayleyExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((EXAMPLE / "manifest.json").read_text())

    def report(self, name):
        return (EXAMPLE / "stages" / (name + ".md")).read_text()

    def test_exported_artifacts_match_recorded_hashes(self):
        for relative, expected in self.manifest["files_sha256"].items():
            with self.subTest(path=relative):
                path = EXAMPLE / relative
                self.assertTrue(path.is_file())
                self.assertTrue(path.resolve().is_relative_to(EXAMPLE.resolve()))
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)

    def test_input_hashes_match_independent_setup_audit(self):
        audit = self.report("setup_audit")
        self.assertIn("Verdict: PASS", audit)
        for name in ("target.md", "skeleton.md", "skeleton.tex", "allowed_support.md"):
            expected = re.search(r"`" + re.escape(name) + r"`: `([a-f0-9]{64})`", audit)
            self.assertIsNotNone(expected)
            actual = hashlib.sha256((EXAMPLE / "input" / name).read_bytes()).hexdigest()
            self.assertEqual(actual, expected.group(1))

    def test_manual_execution_boundary_and_key_first_trace(self):
        m = self.manifest
        self.assertEqual(m["execution_mode"], "manual_codex_subagents")
        self.assertEqual(m["role_model"], "gpt-5.5")
        self.assertEqual(m["role_reasoning_effort"], "xhigh")
        self.assertFalse(m["runtime_executed"])
        self.assertFalse(m["api_runner_used"])
        self.assertEqual((m["solver_rounds"], m["guidance_items"], m["branches"]), (1, 0, 0))
        trace = json.loads((EXAMPLE / "dispatches.json").read_text())
        self.assertEqual(trace["fork_turns"], "none")
        roles = [r["role"] for r in trace["roles"]]
        self.assertEqual(len(roles), len(set(roles)))
        key = parse_s0_key_solver(self.report("S0"))
        self.assertEqual(key, m["key_solver_id"])
        for role in ("S1", "S2", "S4", "S5"):
            self.assertLess(roles.index(key), roles.index(role))
        self.assertLess(roles.index("citation_verifier"), roles.index("A1"))
        for role in ("A1", "A2", "A3"):
            entry = next(r for r in trace["roles"] if r["role"] == role)
            self.assertEqual(entry["packet"], "packets/verifier_a.md")
            self.assertLess(roles.index(role), roles.index("composer_a"))

    def test_solver_completion_and_target_gate(self):
        for role in ("S1", "S2", "S3", "S4", "S5"):
            parsed = parse_subproblem_output(self.report(role), role)
            self.assertTrue(parsed.solved)
            self.assertFalse(parsed.setup_failure)
        self.assertTrue(parse_composer_output(self.report("S6")).complete)
        self.assertEqual(parse_problem_statement_report(self.report("problem_statement")).problem_statement_match, "yes")

    def test_recorded_citation_gates(self):
        cg = parse_citation_generator_report(self.report("citation_generator"))
        cv = parse_citation_verifier_report(self.report("citation_verifier"))
        self.assertEqual(cg.parse_status, "OK")
        self.assertEqual(cg.possible_target_source_leakage, "NO")
        self.assertEqual(cg.recommended_next_step, "PROCEED_TO_CITATION_VERIFIER")
        self.assertEqual(cv.parse_status, "OK")
        self.assertEqual(cv.citation_gate_result, "GOOD_TO_GO")

    def test_recorded_mathematical_and_terminal_gates(self):
        a = parse_composer_a_report(self.report("composer_a"))
        self.assertEqual(a.non_fillable_gaps, "no")
        self.assertEqual(a.disallowed_premises, "no")
        self.assertEqual(a.omitted_case_or_weaker, "no")
        b = parse_verifier_b_report(self.report("verifier_b"))
        self.assertTrue(b.weakest_point_found == "no" or (b.weakest_point_found == "yes" and b.fillable == "yes"))
        self.assertEqual(b.weakest_point_found, "no")
        self.assertEqual(b.disallowed_premise, "not_applicable")
        self.assertIn("8. Disallowed-premise check\n\nNone.", self.report("verifier_b"))
        c = parse_verifier_c_report(self.report("verifier_c"))
        self.assertEqual(c.broke, "no")
        self.assertEqual(c.disallowed_premise, "no")
        final = json.loads((EXAMPLE / "stages" / "final_checker_public.json").read_text())
        self.assertEqual(final["decision"], "PASS")
        self.assertNotIn("private_rationale", final)
        self.assertRegex(self.report("decision"), r"Outcome:\s*ACCEPTED\b")
        self.assertIn("CONTROLLER ROUTING VALID", self.report("controller_audit"))
        self.assertEqual(self.manifest["status"], "accepted_manual_final_checker")

    def test_no_private_source_or_checker_packet_exported(self):
        self.assertFalse(self.manifest["private_inputs_published"])
        forbidden = {"private", "source.tar", "cayleyProof.tex", "gold_proof.tex", "final_checker.md"}
        for path in EXAMPLE.rglob("*"):
            self.assertFalse(forbidden.intersection(path.relative_to(EXAMPLE).parts))
        for packet in (EXAMPLE / "packets").glob("*.md"):
            self.assertNotRegex(packet.read_text(), r"\[PASTE\b")

    def test_finite_check_is_explicitly_bounded(self):
        data = json.loads((EXAMPLE / "finite_check.json").read_text())
        self.assertIn("not a proof", data["scope"])
        self.assertEqual([r["n"] for r in data["rows"]], list(range(1, 7)))
        for row in data["rows"]:
            n = row["n"]
            self.assertEqual(row["all_functions"], n ** n)
            self.assertEqual(row["one_cyclic_vertex"], n ** (n-1))

    def test_public_text_has_no_local_home_paths(self):
        for path in EXAMPLE.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".json", ".tex", ".svg", ".py"}:
                with self.subTest(path=str(path.relative_to(EXAMPLE))):
                    self.assertNotRegex(path.read_text(), r"/(?:Users|home)/")

    def test_small_case_script_reproduces_saved_counts(self):
        spec = importlib.util.spec_from_file_location("cayley_small_cases", EXAMPLE / "check_small_cases.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        saved = json.loads((EXAMPLE / "finite_check.json").read_text())
        self.assertEqual(module.counts(), saved["rows"])


if __name__ == "__main__":
    unittest.main()
