"""Check target matching and report accounting, not mathematical correctness."""
from collections import Counter
import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("paired_results", ROOT / "docs/build_paired_results.py")
paired = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = paired
SPEC.loader.exec_module(paired)


class PairedResultsTests(unittest.TestCase):
    def test_counts_and_excluded_rows_reconcile(self):
        pairs, with_unmatched, without_unmatched, _, _ = paired.analysis()
        self.assertEqual(Counter(map(paired.outcome_of, pairs)),
                         {"With only": 9, "Without only": 2, "Both": 12, "Neither": 5})
        self.assertEqual(len(pairs), 28)
        self.assertEqual((len(with_unmatched), len(without_unmatched)), (3, 3))
        for side, unmatched in ((0, with_unmatched), (1, without_unmatched)):
            records = [pair[side] for pair in pairs] + unmatched
            self.assertEqual(len(records), 31)
            self.assertEqual(len({record.key for record in records}), 31)
            filename = "report.md" if side == 0 else "report_without_lemma.md"
            self.assertEqual(set(records), set(paired.read_records(
                ROOT / "Results/paper_reproduction" / filename)))

    def test_primary_subject_counts(self):
        _, _, _, fields, _ = paired.analysis()
        expected = {
            "math.CO": (3, 2, 4, 0), "math.CA": (2, 0, 4, 0),
            "math.AG": (2, 0, 0, 2), "math.PR": (0, 0, 2, 1),
            "math.AC": (1, 0, 1, 0), "math.ST": (0, 0, 1, 1),
            "math.NT": (0, 0, 0, 1), "math.OC": (1, 0, 0, 0),
        }
        self.assertEqual({field: tuple(counts[key] for key in paired.OUTCOMES)
                          for field, counts in fields.items()}, expected)

    def test_only_documented_alias_is_matched(self):
        pairs, with_unmatched, without_unmatched, _, _ = paired.analysis()
        renamed = [(a.key, b.key) for a, b in pairs if a.key != b.key]
        self.assertEqual(renamed, [(("2607.05330", "proposition-2"),
                                    ("2607.05330", "proposition-2.1"))])
        self.assertEqual({r.key for r in with_unmatched}, {
            ("2606.15432", "corollary-6.8"), ("2607.03305", "corollary-2.5"),
            ("2607.04347", "proposition-2.5")})
        self.assertEqual({r.key for r in without_unmatched}, {
            ("2606.15432", "corollary-6.4"), ("2607.03305", "corollary-2.2"),
            ("2607.04347", "proposition-2.2")})

    def test_matching_never_uses_row_order_or_paper_alone(self):
        a = paired.Record("2601.12345", "theorem-1", "blocked_setup", "")
        b = paired.Record(a.paper, "theorem-2", "accepted_final_checker", "")
        self.assertEqual(paired.pair_records([a], [b]), ([], [a], [b]))
        folder = ROOT / "Results/paper_reproduction"
        with_records = paired.read_records(folder / "report.md")
        without_records = paired.read_records(folder / "report_without_lemma.md")
        self.assertEqual(paired.pair_records(with_records, without_records),
                         paired.pair_records(with_records[::-1], without_records[::-1]))

    def test_duplicate_and_unsupported_alias_are_rejected(self):
        record = paired.Record("2607.05330", "proposition-2.1", "accepted_final_checker", "")
        with self.assertRaisesRegex(ValueError, "missing its report evidence"):
            paired.pair_records([], [record])
        with self.assertRaisesRegex(ValueError, "Duplicate target"):
            paired.pair_records([record, record], [])
        alias = paired.Record(record.paper, record.target, record.outcome, paired.ALIAS_EVIDENCE)
        canonical = paired.Record(record.paper, "proposition-2", record.outcome, "")
        with self.assertRaisesRegex(ValueError, "alias collision"):
            paired.pair_records([], [alias, canonical])

    def test_manual_passes_remain_identifiable(self):
        pairs, *_ = paired.analysis()
        manual = [(a.key, paired.outcome_of((a, b))) for a, b in pairs
                  if a.outcome == "accepted_manual_final_checker"]
        self.assertEqual(manual, [(("2607.04347", "theorem-1.7"), "Both"),
                                  (("2607.06477", "theorem-b"), "With only")])

    def test_without_only_cases_are_cleaner_blocks_not_solver_rejections(self):
        pairs, *_ = paired.analysis()
        cases = [a for a, b in pairs if paired.outcome_of((a, b)) == "Without only"]
        self.assertEqual({r.key for r in cases}, {
            ("2607.06275", "lemma-10.5"), ("2607.06275", "theorem-5.1")})
        self.assertTrue(all(r.outcome == "blocked_cleaner_disputed" for r in cases))

    def test_generated_page_is_current(self):
        self.assertEqual((ROOT / paired.DESTINATION).read_text(), paired.render())

    def test_readme_summary_matches_paired_counts(self):
        pairs, *_ = paired.analysis()
        counts = Counter(map(paired.outcome_of, pairs))
        text = (ROOT / "Results/paper_reproduction/README.md").read_text()
        self.assertIn(f"**{len(pairs)} matched target records**", text)
        for key, phrase in (("With only", "only with context"),
                            ("Without only", "only without context"),
                            ("Both", "in both"), ("Neither", "in neither")):
            self.assertIn(f"**{counts[key]} {phrase}**", text)


if __name__ == "__main__":
    unittest.main()
