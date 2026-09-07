"""Rebuild the paired report comparison from local records; no model calls."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = Path("Results/paper_reproduction/paired_outcomes.md")
PASS_STATUSES = {"accepted_final_checker", "accepted_manual_final_checker"}
OUTCOMES = ("With only", "Without only", "Both", "Neither")
# A report explicitly identifies this renumbering. Do not infer aliases from
# row order, similar labels, or a shared paper/run-folder name.
ALIASES = {("2607.05330", "proposition-2.1"): "proposition-2"}
ALIAS_EVIDENCE = "the current arXiv v2 displays the target as Proposition 2"


@dataclass(frozen=True)
class Record:
    paper: str
    target: str
    outcome: str
    notes: str

    @property
    def key(self) -> tuple[str, str]:
        return self.paper, self.target


def read_records(path: Path) -> list[Record]:
    section = path.read_text().split("## Target records\n", 1)[1].split("\n## ", 1)[0]
    rows = [[cell.strip() for cell in re.split(r"(?<!\\)\|", line)[1:-1]]
            for line in section.splitlines() if line.startswith("| ")]
    header = rows[0]
    records = []
    for row in rows[1:]:
        if len(row) != len(header):
            raise ValueError(f"Malformed target row in {path}")
        fields = dict(zip(header, row))
        paper = re.fullmatch(r"\[(\d{4}\.\d{4,5})\]\(https://arxiv\.org/abs/\1\)",
                             fields["paper"])
        if paper is None:
            raise ValueError(f"Invalid paper identifier in {path}")
        outcome = fields["outcome"].strip("`")
        if outcome in PASS_STATUSES and fields["final checker"] != "PASS":
            raise ValueError("A counted pass must have a Final Checker PASS")
        records.append(Record(paper.group(1),
                              fields.get("target statement", fields.get("target", "")),
                              outcome, fields.get("what happened", fields.get("warnings", ""))))
    if not records or any(not record.target for record in records):
        raise ValueError("Empty target report or target label")
    return records


def pair_records(with_context: list[Record], without_context: list[Record]):
    def index(records, allow_alias=False):
        result = {}
        for record in records:
            key = record.key
            if allow_alias and key in ALIASES:
                if ALIAS_EVIDENCE not in record.notes:
                    raise ValueError("Renumbered target is missing its report evidence")
                key = record.paper, ALIASES[key]
            if key in result:
                raise ValueError(f"Duplicate target or alias collision: {key}")
            result[key] = record
        return result

    with_index, without_index = index(with_context), index(without_context, True)
    shared = with_index.keys() & without_index.keys()
    pairs = [(with_index[key], without_index[key]) for key in sorted(shared)]
    unmatched_with = [with_index[key] for key in sorted(with_index.keys() - shared)]
    unmatched_without = [without_index[key] for key in sorted(without_index.keys() - shared)]
    return pairs, unmatched_with, unmatched_without


def outcome_of(pair: tuple[Record, Record]) -> str:
    passed = tuple(record.outcome in PASS_STATUSES for record in pair)
    return {(True, False): "With only", (False, True): "Without only",
            (True, True): "Both", (False, False): "Neither"}[passed]


def analysis(root: Path = ROOT):
    folder = root / "Results/paper_reproduction"
    pairs, unmatched_with, unmatched_without = pair_records(
        read_records(folder / "report.md"), read_records(folder / "report_without_lemma.md"))
    metadata = json.loads((folder / "subjects.json").read_text())
    categories = {paper["arxiv_id"]: paper["primary_category"] for paper in metadata["papers"]}
    fields = defaultdict(Counter)
    for pair in pairs:
        fields[categories[pair[0].paper]][outcome_of(pair)] += 1
    return pairs, unmatched_with, unmatched_without, fields, metadata["category_names"]


def render(root: Path = ROOT) -> str:
    pairs, unmatched_with, unmatched_without, fields, names = analysis(root)
    total = Counter(outcome_of(pair) for pair in pairs)
    exact = sum(a.key == b.key for a, b in pairs)
    lines = [
        "# With vs. without context: which targets passed?", "",
        f"Across **{len(pairs)} matched target records**, **{total['With only']} passed only with context**,",
        f"**{total['Without only']} only without context**, **{total['Both']} in both**, and **{total['Neither']} in neither**.", "",
        "[With context](README.md#what-does-context-mean) supplies paper-specific background and",
        "supporting statements; without context supplies only the target and essential",
        "definitions, notation, and assumptions.", "",
        "## Breakdown by subject", "",
        "Counts are **targets, not papers**, grouped by the paper’s primary arXiv category.",
        "“With only” and “Without only” mean a recorded pass in that setup but not the other.", "",
        "| Subject | With only | Without only | Both | Neither | Paired targets |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for category in sorted(fields, key=lambda key: (-sum(fields[key].values()), names[key])):
        counts = fields[category]
        lines.append(f"| {names[category]} | " + " | ".join(str(counts[key]) for key in OUTCOMES)
                     + f" | {sum(counts.values())} |")
    lines += [
        "| **Total** | " + " | ".join(f"**{total[key]}**" for key in OUTCOMES)
        + f" | **{len(pairs)}** |", "",
        "**The surprising case:** both without-context-only passes are from the same",
        "[combinatorics paper](https://arxiv.org/abs/2607.06275): Lemma 10.5 and Theorem 5.1.",
        "Their with-context runs stopped at the cleaner, before solving. This is a",
        "workflow difference—not evidence that removing context improved the solver.", "",
        "**How to read this:** “Neither” means neither run recorded a pass; no-pass",
        "outcomes include setup blocks, protocol stops, incomplete attempts, and API",
        "timeouts, not just rejected proofs. Passes include two manual Final Checker",
        "passes in the with-context setup (one in “With only,” one in “Both”). These",
        "are model-based checks, not formal verification. Small subject samples and",
        "different run/checking conditions do not establish a causal effect of context.", "",
        f"The comparison matches {exact} records by paper ID and target label, plus one",
        "explicitly documented renumbering. Three rows from each report remain unpaired",
        "because their target labels disagree; they are **excluded, not counted as failures**.",
        "The full reports still contain 31 records per setup. Mathematical Finance has",
        "no paired target because its sole target is among those unresolved labels.", "",
        "<details>", "<summary>Check all matched targets and recorded statuses</summary>", "",
        "| Paper | Target (with / without, if different) | With-context status | Without-context status | Group |",
        "|---|---|---|---|---|",
    ]
    for a, b in pairs:
        target = a.target if a.target == b.target else f"{a.target} / {b.target}"
        lines.append(f"| [{a.paper}](https://arxiv.org/abs/{a.paper}) | {target} | "
                     f"`{a.outcome}` | `{b.outcome}` | {outcome_of((a, b))} |")
    lines += ["", "</details>", "", "<details>",
              "<summary>See the renumbering and unpaired records</summary>", "",
              "For `2607.05330`, the without-context report explicitly identifies",
              "`proposition-2.1` as Proposition 2 in arXiv v2; it is paired with",
              "`proposition-2` in the with-context report. No other aliases are assumed.", "",
              "| Setup | Paper | Unpaired target | Recorded status |",
              "|---|---|---|---|"]
    for label, records in (("With context", unmatched_with), ("Without context", unmatched_without)):
        for record in records:
            lines.append(f"| {label} | [{record.paper}](https://arxiv.org/abs/{record.paper}) | "
                         f"{record.target} | `{record.outcome}` |")
    lines += ["", "In particular, the without-context `2607.04347` Proposition 2.2 record",
              "reports a target-naming/input error; it cannot safely be treated as the",
              "with-context Proposition 2.5 result. The other two label discrepancies",
              "also need statement-level confirmation before inclusion.", "", "</details>", "",
              "[With-context report](report.md#target-records) ·",
              "[Without-context report](report_without_lemma.md#target-records) ·",
              "[Subject metadata](subjects.json) · [All paper results](README.md)", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path, expected = ROOT / DESTINATION, render()
    if args.write:
        path.write_text(expected)
        print(f"Updated {DESTINATION}")
    elif not path.exists() or path.read_text() != expected:
        print(f"Stale paired comparison: {DESTINATION}; run with --write")
        return 1
    else:
        print("Paired comparison is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
