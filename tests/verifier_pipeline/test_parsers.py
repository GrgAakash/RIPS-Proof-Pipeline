"""Parser coverage for Prompt Packet-style verifier outputs."""

from __future__ import annotations

import unittest

from verifiers.parsers import derive_a_status, parse_a_report, parse_b_report, parse_c_report, parse_composer_a_report


class ParserTests(unittest.TestCase):
    def test_parse_composer_agreement_terms(self) -> None:
        no_majority = "Same controller-verdict signal: **no majority.**\nNon-fillable gaps present? NO"
        majority = "Same controller-verdict signal: majority agree 2 of 3.\nNon-fillable gaps present? NO"
        all_agree = "Same controller-verdict signal: all agree.\nNon-fillable gaps present? NO"
        not_all_agree = "Same controller-verdict signal: not all agree.\nNon-fillable gaps present? NO"

        self.assertEqual(parse_composer_a_report(no_majority, skeleton_ref="s").agreement, "no_majority")
        self.assertEqual(parse_composer_a_report(majority, skeleton_ref="s").implied_status_agreement, "majority_agree")
        self.assertEqual(parse_composer_a_report(all_agree, skeleton_ref="s").agreement, "all_agree")
        self.assertEqual(parse_composer_a_report(not_all_agree, skeleton_ref="s").agreement, "unclear")

    def test_parse_emphasized_labels(self) -> None:
        a_raw = """
**Non-fillable gaps present?** NO
*Fillable-only gaps present?* YES
**Disallowed premises present?** NO
**Omitted case / weaker statement present?** NO
"""
        b_raw = """
- **Weakest point found?** yes
**Weakest point (step + claim, or "None"):** Step 2
**Missing claim, or "None":** Claim X
**Fillable:** yes
**Disallowed premise at the weakest point?** no
"""
        c_raw = """
**Most serious attack (step + claim):** Attack X
**Broke:** no
**If broke, the false claim or failing step:** None
**If unsure, exact check needed to decide:** None
**Disallowed premise at the attacked point?** no
"""
        composer_raw = """
**Non-fillable gaps present?** NO
**Fillable-only gaps present?** NO
**Disallowed premises present?** NO
**Omitted case / weaker statement present?** NO
**Candidate guidance seed, if any:** None
**Implied status agreement:** all agree
"""

        self.assertEqual(parse_a_report(a_raw, run_id="A1", skeleton_ref="s").fillable_only_gaps_present, "YES")
        self.assertEqual(parse_b_report(b_raw, skeleton_ref="s").fillable, "yes")
        self.assertEqual(parse_c_report(c_raw, skeleton_ref="s").broke, "no")
        self.assertEqual(parse_composer_a_report(composer_raw, skeleton_ref="s").implied_status_agreement, "all_agree")

    def test_derive_a_status_all_statuses_from_composer_gold_report(self) -> None:
        cases = {
            "A_VERIFIED": """
Non-fillable gaps present? NO
Fillable-only gaps present? NO
Disallowed premises present? NO
Omitted case / weaker statement present? NO
""",
            "A_ALMOST": """
Non-fillable gaps present? NO
Fillable-only gaps present? YES
Disallowed premises present? NO
Omitted case / weaker statement present? NO
""",
            "A_NOT_VERIFIED": """
Non-fillable gaps present? YES
Fillable-only gaps present? NO
Disallowed premises present? NO
Omitted case / weaker statement present? NO
""",
            "A_INVALID": """
Non-fillable gaps present? NO
Fillable-only gaps present? NO
Disallowed premises present? YES
Omitted case / weaker statement present? NO
""",
            "A_UNCLEAR": """
Non-fillable gaps present? UNCLEAR
Fillable-only gaps present? NO
Disallowed premises present? NO
Omitted case / weaker statement present? NO
""",
        }
        for expected, raw in cases.items():
            with self.subTest(expected=expected):
                self.assertEqual(derive_a_status(parse_composer_a_report(raw, skeleton_ref="s")), expected)

    def test_parse_composer_coupling_fields(self) -> None:
        raw = """
Allowed formal skeleton statements used beyond definitions: [2 + [Lemma 1, Proposition 3]]
Disallowed skeleton statements cited: [1 + [The target theorem]]
Standard-background-heavy? YES
"""
        report = parse_composer_a_report(raw, skeleton_ref="s")
        self.assertEqual(report.allowed_formal_skeleton_statements_used_count, 2)
        self.assertEqual(report.allowed_formal_skeleton_statements_used_list, ["Lemma 1", "Proposition 3"])
        self.assertEqual(report.disallowed_skeleton_statements_cited_count, 1)
        self.assertEqual(report.disallowed_skeleton_statements_cited_list, ["The target theorem"])

    def test_parse_composer_coupling_fields_without_outer_brackets(self) -> None:
        raw = """
Allowed formal skeleton statements used beyond definitions: **0 + []**
Disallowed skeleton statements cited: **0 + []**
"""
        report = parse_composer_a_report(raw, skeleton_ref="s")
        self.assertEqual(report.allowed_formal_skeleton_statements_used_count, 0)
        self.assertEqual(report.allowed_formal_skeleton_statements_used_list, [])
        self.assertEqual(report.disallowed_skeleton_statements_cited_count, 0)
        self.assertEqual(report.disallowed_skeleton_statements_cited_list, [])

    def test_parse_b_and_c_web_source_confirmation(self) -> None:
        self.assertEqual(parse_b_report("9. Web-source confirmation\n\nno web sources used", skeleton_ref="s").web_source_issue, "NO")
        self.assertEqual(parse_c_report("9. Web-source confirmation\n\nUsed a web lookup.", skeleton_ref="s").web_source_issue, "YES")

if __name__ == "__main__":
    unittest.main()
