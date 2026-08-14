"""Tests that mock verifier outputs keep the Prompt Packet report skeletons."""

from __future__ import annotations

import unittest

from verifiers.mock import compose_a_output, make_a_output, make_b_output, make_c_output
from verifiers.parsers import parse_a_report


class MockPromptFormatTests(unittest.TestCase):
    def assert_contains_in_order(self, text: str, headings: list[str]) -> None:
        cursor = 0
        for heading in headings:
            index = text.find(heading, cursor)
            self.assertNotEqual(index, -1, f"Missing heading: {heading}")
            cursor = index + len(heading)

    def test_mock_verifier_a_output_uses_prompt_sections(self) -> None:
        raw = make_a_output("A1", "clean")
        self.assert_contains_in_order(
            raw,
            [
                "1. Target restatement",
                "2. Step ledger",
                "3. Unfilled gaps",
                "4. Disallowed-premise check",
                "5. Scope check",
                "6. Coupling inventory",
                "7. Blueprint and subproof consistency",
                "8. Web-source confirmation",
                "9. Controller-facing summary",
            ],
        )

    def test_mock_composer_a_output_uses_prompt_sections(self) -> None:
        reports = [
            parse_a_report(make_a_output(run_id, "clean"), run_id=run_id, skeleton_ref="skeleton")
            for run_id in ("A1", "A2", "A3")
        ]
        raw = compose_a_output(reports)
        self.assert_contains_in_order(
            raw,
            [
                "1. Gold step status",
                "2. Gold unfilled gaps (union)",
                "3. Gold disallowed premises (union)",
                "4. Gold scope check",
                "5. Gold coupling inventory",
                "6. Disagreement map",
                "7. Web-source roll-up",
                "8. Gold Verifier A evidence report for the Decision Controller",
            ],
        )

    def test_mock_verifier_b_output_uses_prompt_sections(self) -> None:
        raw = make_b_output("b_unfillable")
        self.assert_contains_in_order(
            raw,
            [
                "1. Weakest point",
                "2. Why this is the weakest point",
                "3. Weakest point location",
                "4. Source status of the vulnerable claim",
                "5. Issue type",
                "6. What must be proved to close it (the missing claim)",
                "7. Fillable?",
                "8. Disallowed-premise check",
                "9. Web-source confirmation",
                "Final summary format:",
            ],
        )

    def test_mock_verifier_c_output_uses_prompt_sections(self) -> None:
        raw = make_c_output("c_unsure")
        self.assert_contains_in_order(
            raw,
            [
                "1. Most serious possible failure point",
                "2. Exact location",
                "3. Attack location",
                "4. Source status of the vulnerable claim",
                "5. Why the proof could fail there",
                "6. Did it break?",
                "7. Disallowed-premise check",
                "8. Three most delicate points",
                "9. Web-source confirmation",
                "Final summary format:",
            ],
        )


if __name__ == "__main__":
    unittest.main()
