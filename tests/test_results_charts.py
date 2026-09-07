"""Offline checks for the README figures and the reported data they display."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "results_charts", ROOT / "docs/build_results_charts.py"
)
charts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(charts)
NS = {"svg": "http://www.w3.org/2000/svg"}


class ResultsChartTests(unittest.TestCase):
    def test_generated_figures_are_current(self) -> None:
        for name, expected in charts.figures().items():
            with self.subTest(figure=name):
                self.assertEqual((ROOT / "docs" / name).read_text(), expected,
                                 "Run docs/build_results_charts.py --write")

    def test_figures_have_accessible_descriptions_and_theme_support(self) -> None:
        for content in charts.figures().values():
            root = ET.fromstring(content)
            self.assertEqual(root.attrib["role"], "img")
            self.assertEqual(root.attrib["aria-labelledby"], "title desc")
            self.assertTrue(root.find("svg:title", NS).text)
            self.assertTrue(root.find("svg:desc", NS).text)
            self.assertIn("prefers-color-scheme: dark", content)
            self.assertIsNone(root.find(".//svg:script", NS))

    def test_benchmark_bars_encode_reported_percentages_from_zero(self) -> None:
        root = ET.fromstring(charts.benchmark_chart())
        bars = [node for node in root.findall("svg:rect", NS)
                if node.attrib.get("height") != "16.000"
                and node.attrib.get("class") in {"direct", "pipeline"}]
        expected = [float(value.rstrip("%"))
                    for row in charts.benchmark_data() for value in row[1:3]]
        self.assertEqual(len(bars), len(expected))
        for bar, score in zip(bars, expected):
            self.assertAlmostEqual(float(bar.attrib["height"]) / 210 * 100,
                                   score, places=3)
            self.assertAlmostEqual(float(bar.attrib["y"]) +
                                   float(bar.attrib["height"]), 340, places=3)

    def test_paper_segments_match_target_record_counts(self) -> None:
        root = ET.fromstring(charts.paper_chart())
        for index, (_, total, automated, manual) in enumerate(charts.paper_data()):
            y = 180 + 126 * index
            segments = [node for node in root.findall("svg:rect", NS)
                        if float(node.attrib["y"]) == y]
            expected = [count for count in (automated, manual, total - automated - manual)
                        if count]
            self.assertEqual(len(segments), len(expected))
            for node, count in zip(segments, expected):
                self.assertAlmostEqual(float(node.attrib["width"]) / 584 * total,
                                       count, places=3)
            self.assertAlmostEqual(sum(float(node.attrib["width"]) for node in segments),
                                   584, places=3)
        self.assertIn('fill="url(#manual)"', charts.paper_chart())

    def test_benchmark_reader_rejects_inconsistent_differences(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Results").mkdir()
            (root / "Results/README.md").write_text(
                "| ArXivMath 04/26 | 63.41% | 69.14% | +99 percentage points |\n"
                "| BrokenArXiv 06/2026 | 69.4% | 90.7% | +21.3 percentage points |\n"
            )
            with self.assertRaisesRegex(ValueError, "difference disagrees"):
                charts.benchmark_data(root)

    def test_subject_metadata_covers_exactly_the_papers_in_both_reports(self) -> None:
        papers = charts.subject_metadata()["papers"]
        ids = [paper["arxiv_id"] for paper in papers]
        self.assertEqual(len(ids), len(set(ids)), "Do not count a paper twice")
        for report in ("report.md", "report_without_lemma.md"):
            text = (ROOT / "Results/paper_reproduction" / report).read_text()
            expected = set(re.findall(r"https://arxiv.org/abs/(\d{4}\.\d{4,5})", text))
            self.assertEqual(set(ids), expected)

    def test_subject_classifications_have_traceable_metadata(self) -> None:
        metadata = charts.subject_metadata()
        self.assertEqual(metadata["classification_field"], "arxiv:primary_category")
        self.assertEqual(metadata["source"], "https://export.arxiv.org/api/query")
        self.assertRegex(metadata["checked_on"], r"^\d{4}-\d{2}-\d{2}$")
        used = set()
        for paper in metadata["papers"]:
            self.assertTrue(paper["title"])
            self.assertRegex(paper["metadata_version"],
                             "^" + re.escape(paper["arxiv_id"]) + r"v[1-9]\d*$")
            primary = paper["primary_category"]
            self.assertIn(primary, paper["categories"])
            self.assertIn(primary, metadata["category_names"])
            used.add(primary)
        self.assertEqual(used, set(metadata["category_names"]))

    def test_subject_bars_count_unique_papers_not_targets_or_cross_lists(self) -> None:
        metadata = charts.subject_metadata()
        rows = charts.subject_counts()
        self.assertEqual(sum(row[2] for row in rows), len(metadata["papers"]))
        expected = {code: sum(paper["primary_category"] == code
                              for paper in metadata["papers"])
                    for code in metadata["category_names"]}
        self.assertEqual({code: count for code, _, count in rows}, expected)
        root = ET.fromstring(charts.subject_chart())
        bars = [node for node in root.findall("svg:rect", NS)
                if node.attrib.get("class") == "coverage"]
        self.assertEqual(len(bars), len(rows))
        maximum = max(row[2] for row in rows)
        for bar, (_, name, count) in zip(bars, rows):
            self.assertEqual(float(bar.attrib["x"]), 330)
            self.assertAlmostEqual(float(bar.attrib["width"]) / 246 * maximum,
                                   count, places=3)
            self.assertIn(name, charts.subject_chart())

    def test_generated_subject_lists_are_current(self) -> None:
        for path, content in charts.subject_readmes().items():
            self.assertEqual(path.read_text(), content)
        section = charts.subject_section()
        rows = charts.table_rows(section)[1:]
        papers = charts.subject_metadata()["papers"]
        self.assertEqual(len(rows), len(papers))
        for row, paper in zip(rows, papers):
            self.assertIn(paper["arxiv_id"], row[0])
            self.assertIn(paper["primary_category"], row[2])

    def test_subject_reader_rejects_duplicate_papers(self) -> None:
        metadata = charts.subject_metadata()
        metadata["papers"].append(metadata["papers"][0])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "Results/paper_reproduction"
            folder.mkdir(parents=True)
            (folder / "subjects.json").write_text(json.dumps(metadata))
            with self.assertRaisesRegex(ValueError, "unique"):
                charts.subject_counts(root)


if __name__ == "__main__":
    unittest.main()
