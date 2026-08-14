from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPONENT_ROOT = ROOT / "Individual Pipeline"


class StandaloneSolverBundleTests(unittest.TestCase):
    def test_standalone_verifier_output_stays_at_repository_root(self) -> None:
        from verifiers.cli import DEFAULT_OUTPUT_ROOT

        self.assertEqual(Path(DEFAULT_OUTPUT_ROOT), ROOT / "Outputs" / "verifier")

    def test_flat_solver_package_has_no_open_problem_subpackage(self) -> None:
        solver_dir = COMPONENT_ROOT / "solver"
        citation_dir = COMPONENT_ROOT / "citation"
        verifiers_dir = COMPONENT_ROOT / "verifiers"
        self.assertTrue((solver_dir / "orchestrator.py").is_file())
        self.assertTrue((solver_dir / "llm.py").is_file())
        self.assertTrue((citation_dir / "gate.py").is_file())
        self.assertTrue((verifiers_dir / "orchestrator.py").is_file())
        self.assertTrue((verifiers_dir / "prompts" / "verifier_a.md").is_file())
        self.assertFalse((solver_dir / "citation").exists())
        self.assertFalse((solver_dir / "open_problem").exists())
        self.assertFalse((COMPONENT_ROOT / "src").exists())

    def test_no_web_mock_run_reaches_a_terminal_state(self) -> None:
        completed = self._run_mock("Prompts.md")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("status:", completed.stdout)

    def test_source_supported_mock_run_reaches_a_terminal_state(self) -> None:
        completed = self._run_mock("PromptsWithFullInternet.md", "--web-search")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("status:", completed.stdout)

    def test_mock_run_persists_problem_statement_verifier_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            problem = temp_root / "problem"
            problem.mkdir()
            (problem / "target.md").write_text("Prove that 1 + 1 = 2.\n", encoding="utf-8")
            (problem / "skeleton.md").write_text(
                "Use the usual arithmetic axioms.\n", encoding="utf-8"
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "solver",
                    "run-open-problem",
                    "--problem-dir",
                    str(problem),
                    "--run-dir",
                    str(temp_root / "runs"),
                    "--packet-file",
                    str(ROOT / "Prompt Packet" / "Prompts.md"),
                    "--client",
                    "mock",
                    "--max-rounds",
                    "1",
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(COMPONENT_ROOT)},
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            round_dir = temp_root / "runs" / "problem" / "round_001"
            self.assertTrue((round_dir / "problem_statement_verifier.md").is_file())
            self.assertTrue(
                (round_dir / "parsed" / "problem_statement_verifier.json").is_file()
            )

    def test_standalone_verifier_mock_reaches_final_checker_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "verifiers",
                    "run-mock",
                    "--scenario",
                    "clean",
                    "--run-id",
                    "bundle-smoke",
                    "--output-root",
                    tmp,
                    "--target-theorem",
                    "For every integer n, n = n.",
                    "--allowed-supporting-statements",
                    "Equality reflexivity is allowed.",
                    "--proof-artifact",
                    "For every integer n, n = n by equality reflexivity.",
                    "--skeleton-ref",
                    "skeleton.tex#reflexivity",
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(COMPONENT_ROOT)},
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("FINAL_CHECKER_GATE", completed.stdout)

    def _run_mock(self, packet_name: str, *extra: str) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            problem = temp_root / "problem"
            problem.mkdir()
            (problem / "target.md").write_text(
                "Prove that 1 + 1 = 2.\n", encoding="utf-8"
            )
            (problem / "skeleton.md").write_text(
                "Use the usual arithmetic axioms.\n", encoding="utf-8"
            )
            env = os.environ.copy()
            env["PYTHONPATH"] = str(COMPONENT_ROOT)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "solver",
                    "run-open-problem",
                    "--problem-dir",
                    str(problem),
                    "--run-dir",
                    str(temp_root / "runs"),
                    "--packet-file",
                    str(ROOT / "Prompt Packet" / packet_name),
                    "--client",
                    "mock",
                    "--max-rounds",
                    "1",
                    "--max-branch-depth",
                    "0",
                    "--max-branches",
                    "0",
                    *extra,
                ],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            return completed


if __name__ == "__main__":
    unittest.main()
