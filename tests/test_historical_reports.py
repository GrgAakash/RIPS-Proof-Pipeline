"""Validate the final-branch report tables, not the correctness of the proofs."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "Results" / "paper_reproduction"
PAPER_LINK = re.compile(r"\[(\d{4}\.\d{4,5})\]\(https://arxiv\.org/abs/\1\)")


def target_rows(text: str) -> list[list[str]]:
    rows = []
    in_runs = False
    for line in text.splitlines():
        if line == "## Target records":
            in_runs = True
        elif line.startswith("## "):
            in_runs = False
        elif in_runs and line.startswith("| "):
            cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line)[1:-1]]
            if cells[0] not in {"run", "paper"}:
                rows.append(cells)
    return rows


class HistoricalReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(
            (ROOT / "tests" / "fixtures" / "paper_report_snapshot.json").read_text()
        )

    def test_all_final_source_fields_are_preserved(self) -> None:
        for entry in self.manifest["source_reports"]:
            with self.subTest(report=entry["file"]):
                rows = target_rows((REPORTS / entry["file"]).read_text())
                self.assertEqual(len(rows), entry["records"])
                paper_column = entry["paper_column"]
                for row in rows:
                    self.assertEqual(len(row), entry["column_count"],
                                     "unescaped pipe or missing column")
                    paper_link = PAPER_LINK.fullmatch(row[paper_column])
                    self.assertIsNotNone(paper_link)
                    row[paper_column] = paper_link.group(1)
                # Canonical representation of every original field, in source order.
                digest = hashlib.sha256(json.dumps(
                    rows, ensure_ascii=False, separators=(",", ":")
                ).encode()).hexdigest()
                self.assertEqual(digest, entry["source_rows_sha256"])
                self.assertEqual(len({row[paper_column] for row in rows}),
                                 entry["distinct_paper_ids"])

    def test_aggregate_counts_and_rates_match_target_rows(self) -> None:
        for entry in self.manifest["source_reports"]:
            with self.subTest(report=entry["file"]):
                text = (REPORTS / entry["file"]).read_text()
                rows = target_rows(text)
                counts = Counter(row[entry["outcome_column"]].strip("`") for row in rows)
                self.assertEqual(dict(counts), entry["outcomes"])
                declared = dict((key, int(value)) for key, value in re.findall(
                    r"^- `([^`]+)`: (\d+)$", text, re.MULTILINE
                ))
                self.assertEqual(declared, dict(counts))
                strict = counts["accepted_final_checker"]
                manual = counts["accepted_manual_final_checker"]
                rate = 100 * (strict + manual) / len(rows)
                summary = f'| {len(rows)} | {strict} | {manual} | {rate:.1f}% |'
                self.assertIn(summary, text)

    def test_summary_counts_match_the_reports(self) -> None:
        text = (REPORTS / "README.md").read_text()
        for entry in self.manifest["source_reports"]:
            counts = entry["outcomes"]
            strict = counts["accepted_final_checker"]
            manual = counts.get("accepted_manual_final_checker", 0)
            rate = 100 * (strict + manual) / entry["records"]
            summary = (
                f']({entry["file"]}) | {entry["records"]} | '
                f'{strict} | {manual} | {rate:.1f}% |'
            )
            self.assertIn(summary, text)

    def test_each_paper_target_is_counted_once(self) -> None:
        for entry in self.manifest["source_reports"]:
            with self.subTest(report=entry["file"]):
                rows = target_rows((REPORTS / entry["file"]).read_text())
                keys = [(row[entry["paper_column"]], row[entry["target_column"]])
                        for row in rows]
                self.assertTrue(all(paper and target for paper, target in keys))
                self.assertEqual(len(keys), len(set(keys)), "duplicate target counted")

    def test_counted_passes_have_a_final_checker_pass(self) -> None:
        for entry in self.manifest["source_reports"]:
            with self.subTest(report=entry["file"]):
                rows = target_rows((REPORTS / entry["file"]).read_text())
                for row in rows:
                    outcome = row[entry["outcome_column"]].strip("`")
                    if outcome in {"accepted_final_checker", "accepted_manual_final_checker"}:
                        self.assertEqual(row[entry["checker_column"]], "PASS")

    def test_front_page_paper_totals_match_final_reports(self) -> None:
        for path in (ROOT / "README.md", ROOT / "Results" / "README.md"):
            with self.subTest(document=path):
                text = path.read_text()
                for entry in self.manifest["source_reports"]:
                    counts = entry["outcomes"]
                    passes = counts["accepted_final_checker"] + counts.get(
                        "accepted_manual_final_checker", 0
                    )
                    self.assertIn(f'{passes}/{entry["records"]}', text)
                    self.assertIn(f'{100 * passes / entry["records"]:.1f}%', text)

    def test_benchmark_tables_stay_in_sync(self) -> None:
        rows = []
        for path in (ROOT / "README.md", ROOT / "Results" / "README.md"):
            rows.append(re.findall(r"^\| (?:ArXivMath|BrokenArXiv) .*\|$",
                                   path.read_text(), re.MULTILINE))
        self.assertEqual(len(rows[0]), 2)
        self.assertEqual(rows[0], rows[1])


if __name__ == "__main__":
    unittest.main()
