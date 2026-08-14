from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
COMPONENT_ROOT = ROOT / "Individual Pipeline"
if str(COMPONENT_ROOT) not in sys.path:
    sys.path.insert(0, str(COMPONENT_ROOT))

if importlib.util.find_spec("networkx") is None:
    raise unittest.SkipTest(
        "target-integrity tests require the optional [pipeline] dependencies"
    )

from paper_cleaner.src.common import sha256_text
from paper_cleaner.src.graph_utils import eligible_ids, ineligibility_reason
from paper_cleaner.src.schemas import DepGraph, Meta, Statement
from paper_cleaner.src.step2_parse import RawEnv, build_index, resolve_hint
from paper_cleaner.src.target_integrity import (
    canonical_target_section,
    canonicalize_target_section,
    frozen_target_artifact_issues,
    proof_source_issues,
    source_statement_id,
    statement_source_issues,
    target_identity_issues,
)
from solver.cleaner_bridge import CleanerBridgeError, load_cleaner_package


MINI = COMPONENT_ROOT / "paper_cleaner_mini"
if str(MINI) not in sys.path:
    sys.path.insert(0, str(MINI))

from package_validation import (  # noqa: E402
    canonicalize_target_section as mini_canonicalize_target_section,
    frozen_target_artifact_issues as mini_frozen_target_artifact_issues,
    proof_source_issues as mini_proof_source_issues,
    statement_source_issues as mini_statement_source_issues,
    target_identity_issues as mini_target_identity_issues,
)
from stage2 import (EDITABLE_HEADINGS, HEADINGS,  # noqa: E402
                    freeze_or_validate_target_artifacts, structure_missing)


class _Ctx:
    def __init__(self, root: Path, paper_id: str = "paper") -> None:
        self.root = root
        self.paper_id = paper_id
        self.events: list[dict] = []

    def path(self, rel: str) -> Path:
        return self.root / rel

    def log_event(self, **event) -> None:
        self.events.append(event)

    def read_json(self, rel: str):
        return json.loads(self.path(rel).read_text(encoding="utf-8"))

    def write_json(self, rel: str, value) -> None:
        path = self.path(rel)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")


class StatementIdentityTests(unittest.TestCase):
    def test_id_never_uses_number_or_source_order(self) -> None:
        first = source_statement_id(
            paper_id="p", env_type="theorem", statement_tex="Exact text.",
            latex_label="thm:main", used_ids=set())
        renamed_number = source_statement_id(
            paper_id="p", env_type="theorem", statement_tex="Exact text.",
            latex_label="thm:main", used_ids=set())
        self.assertEqual(first, renamed_number)
        self.assertRegex(first, r"^stmt-[0-9a-f]{12}$")
        self.assertNotIn("4.1", first)

    def test_parser_does_not_synthesize_numbers(self) -> None:
        tex = "AAA exact first BBB exact second CCC"
        envs = [
            RawEnv("theorem", False, 0, 15, "exact first", "", "4", "thm:a"),
            RawEnv("lemma", False, 16, 32, "exact second", "", "4", "lem:b"),
        ]
        with tempfile.TemporaryDirectory() as tmp, patch(
                "paper_cleaner.src.step2_parse._extract_latex",
                return_value=(envs, [])):
            ctx = _Ctx(Path(tmp))
            index, _ = build_index(
                ctx, tex, Meta(paper_id="paper", source_type="latex"))
        self.assertTrue(all("number" not in statement.model_dump()
                            for statement in index.statements))
        self.assertTrue(all(statement.id.startswith("stmt-")
                            for statement in index.statements))
        self.assertFalse(any(event.get("event") == "number_synthetic"
                             for event in ctx.events))

    def test_shared_latex_counter_never_enters_identity(self) -> None:
        tex = r"""
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\begin{document}
\section{Main}
\begin{theorem}\label{thm:first}
Exact first result.
\end{theorem}
\begin{proof}First proof is sufficiently long.\end{proof}
\begin{lemma}
Exact second result.
\end{lemma}
\begin{proof}[Proof of Lemma 1.2]Second proof is sufficiently long.\end{proof}
\end{document}
"""
        with tempfile.TemporaryDirectory() as tmp:
            ctx = _Ctx(Path(tmp))
            index, _ = build_index(
                ctx, tex, Meta(paper_id="paper", source_type="latex"))
        results = [statement for statement in index.statements
                   if statement.env_type in {"theorem", "lemma"}]
        self.assertEqual(len(results), 2)
        self.assertTrue(all("number" not in statement.model_dump()
                            for statement in results))
        self.assertTrue(all(statement.source_verified for statement in results))
        self.assertTrue(results[0].proof_tex)
        self.assertTrue(results[0].proof_source_verified)
        self.assertEqual(results[0].proof_pairing, "adjacent")
        self.assertEqual(sha256_text(results[0].proof_tex),
                         results[0].proof_sha256)
        self.assertIsNone(results[1].proof_tex)
        self.assertTrue(all(statement.id.startswith("stmt-") for statement in results))

    def test_printed_number_cannot_pair_a_proof(self) -> None:
        statement = Statement(
            id="stmt-a", env_type="lemma",
            statement_tex="Exact text")
        self.assertIsNone(resolve_hint(
            "Proof of Lemma 4.2", [statement], {}))
        self.assertIs(statement, resolve_hint(
            r"Proof of Lemma~\ref{lem:a}", [statement], {"lem:a": "stmt-a"}))

    def test_unresolved_explicit_proof_title_never_falls_back_to_adjacency(self) -> None:
        tex = r"""
\begin{theorem}\label{thm:a}Statement A.\end{theorem}
\begin{proof}[Proof of Theorem 2.3]Proof belonging elsewhere.\end{proof}
"""
        with tempfile.TemporaryDirectory() as tmp:
            index, extras = build_index(
                _Ctx(Path(tmp)), tex, Meta(paper_id="paper", source_type="latex"))
        theorem = next(s for s in index.statements if s.env_type == "theorem")
        self.assertIsNone(theorem.proof_tex)
        self.assertEqual(len(extras["orphan_proofs"]), 1)

    def test_ocr_statement_and_proof_use_the_markdown_source(self) -> None:
        markdown = (
            "**Theorem 1.** Exact OCR target.\n\n"
            "**Proof.** Exact OCR proof. ∎\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            index, extras = build_index(
                _Ctx(Path(tmp)), markdown,
                Meta(paper_id="paper", source_type="ocr"))

        theorem = next(s for s in index.statements if s.env_type == "theorem")
        self.assertEqual(extras["orphan_proofs"], [])
        self.assertEqual(theorem.source_file, "source/flat.md")
        self.assertTrue(theorem.source_verified)
        self.assertEqual(theorem.proof_source_file, "source/flat.md")
        self.assertTrue(theorem.proof_source_verified)
        self.assertEqual(theorem.proof_pairing, "adjacent")

    def test_duplicate_label_ids_are_stable_under_source_reordering(self) -> None:
        def ids(tex: str) -> dict[str, str]:
            with tempfile.TemporaryDirectory() as tmp:
                index, _ = build_index(
                    _Ctx(Path(tmp)), tex,
                    Meta(paper_id="paper", source_type="latex"))
            return {statement.statement_tex: statement.id
                    for statement in index.statements}

        first = (
            r"\begin{theorem}\label{dup}A.\end{theorem}"
            r"\begin{theorem}\label{dup}B.\end{theorem}"
        )
        second = (
            r"\begin{theorem}\label{dup}B.\end{theorem}"
            r"\begin{theorem}\label{dup}A.\end{theorem}"
        )
        self.assertEqual(ids(first), ids(second))


class TargetEligibilityTests(unittest.TestCase):
    def _cfg(self):
        return SimpleNamespace(pipeline=SimpleNamespace(min_proof_chars=5))

    def test_model_added_statement_cannot_be_a_target(self) -> None:
        target = Statement(
            id="ctx-a", env_type="theorem", statement_tex="Claim",
            proof_tex="proof long enough", added_by="agent0")
        index = SimpleNamespace(statements=[target])
        self.assertEqual(eligible_ids(index, DepGraph(), self._cfg()), [])
        self.assertEqual(ineligibility_reason(target, DepGraph(), self._cfg()),
                         "target_source_unverified")

    def test_source_backed_statement_is_eligible(self) -> None:
        target = Statement(
            id="stmt-a", env_type="theorem", statement_tex="Claim",
            statement_sha256=sha256_text("Claim"), source_verified=True,
            source_file="source/flat.tex", source_start=0, source_end=6,
            source_sha256=sha256_text("source"), proof_tex="proof long enough",
            proof_sha256=sha256_text("proof long enough"),
            proof_source_file="source/flat.tex", proof_source_start=7,
            proof_source_end=17, proof_source_sha256=sha256_text("proof slice"),
            proof_source_verified=True, proof_pairing="adjacent")
        index = SimpleNamespace(statements=[target])
        self.assertEqual(eligible_ids(index, DepGraph(), self._cfg()), ["stmt-a"])


class FrozenTargetTests(unittest.TestCase):
    def _statement(self, flat: str) -> Statement:
        statement_text = "For every $x$, $x=x$."
        start = flat.index("\\begin{theorem}")
        end = flat.index("\\end{theorem}") + len("\\end{theorem}")
        return Statement(
            id="stmt-a", env_type="theorem", statement_tex=statement_text,
            statement_sha256=sha256_text(statement_text),
            source_file="source/flat.tex", source_start=start, source_end=end,
            source_sha256=sha256_text(flat[start:end]), source_verified=True,
            added_by="parser")

    def test_source_span_and_hash_are_required(self) -> None:
        flat = "before\\begin{theorem}For every $x$, $x=x$.\\end{theorem}after"
        statement = self._statement(flat)
        self.assertEqual(statement_source_issues(
            statement, flat_source=flat,
            expected_source_file="source/flat.tex"), [])
        statement.statement_tex = "For some $x$, $x=x$."
        self.assertIn("statement text does not match its recorded hash",
                      statement_source_issues(
                          statement, flat_source=flat,
                          expected_source_file="source/flat.tex"))

    def test_controller_discards_model_target(self) -> None:
        frozen = "For every $x$, $x=x$."
        raw = "## 0. Macro definitions\nnone\n\n## 6. Target\n\nA stronger invented claim.\n"
        expected = canonical_target_section(frozen)
        body = canonicalize_target_section(raw, statement_tex=frozen)
        self.assertTrue(body.endswith(expected))
        self.assertNotIn("invented", body)

        mini_body = mini_canonicalize_target_section(raw, statement_tex=frozen)
        self.assertTrue(mini_body.endswith(expected))
        self.assertNotIn("invented", mini_body)

    def test_model_only_needs_editable_sections_and_cannot_insert_target_early(self) -> None:
        editable = "\n\n".join(f"{heading}\ncontent" for heading in EDITABLE_HEADINGS)
        self.assertEqual(structure_missing(editable), [])
        early = editable.replace(
            EDITABLE_HEADINGS[-1], f"{HEADINGS[-1]}\nimprovised\n\n{EDITABLE_HEADINGS[-1]}")
        self.assertIn(HEADINGS[-1], structure_missing(early))
        inside_section_five = editable + f"\n\n{HEADINGS[-1]}\nimprovised\n"
        self.assertIn(HEADINGS[-1], structure_missing(inside_section_five))

    def test_audits_reject_target_drift_and_invalid_hash(self) -> None:
        flat = "before\\begin{theorem}For every $x$, $x=x$.\\end{theorem}after"
        statement = self._statement(flat)
        good = canonical_target_section(statement.statement_tex)
        self.assertEqual(target_identity_issues(good, statement), [])
        bad = good.replace("every", "some")
        self.assertTrue(target_identity_issues(bad, statement))
        self.assertTrue(mini_target_identity_issues(
            bad, statement_tex=statement.statement_tex,
            statement_sha256=statement.statement_sha256))
        self.assertTrue(mini_target_identity_issues(
            good, statement_tex=statement.statement_tex,
            statement_sha256="0" * 64))

    def test_main_and_mini_source_checks_agree(self) -> None:
        flat = "before\\begin{theorem}For every $x$, $x=x$.\\end{theorem}after"
        statement = self._statement(flat)
        main = statement_source_issues(
            statement, flat_source=flat, expected_source_file="source/flat.tex")
        mini = mini_statement_source_issues(
            added_by=statement.added_by,
            source_verified=statement.source_verified,
            source_file=statement.source_file,
            source_start=statement.source_start,
            source_end=statement.source_end,
            source_sha256=statement.source_sha256,
            statement_tex=statement.statement_tex,
            statement_sha256=statement.statement_sha256,
            flat_source=flat,
            expected_source_file="source/flat.tex",
        )
        self.assertEqual(main, mini)

        proof_flat = flat + "\\begin{proof}Reference proof.\\end{proof}"
        proof_start = proof_flat.index("\\begin{proof}")
        proof_end = len(proof_flat)
        statement.proof_tex = "Reference proof."
        statement.proof_sha256 = sha256_text(statement.proof_tex)
        statement.proof_source_file = "source/flat.tex"
        statement.proof_source_start = proof_start
        statement.proof_source_end = proof_end
        statement.proof_source_sha256 = sha256_text(
            proof_flat[proof_start:proof_end])
        statement.proof_source_verified = True
        statement.proof_pairing = "adjacent"
        main_proof = proof_source_issues(
            statement, flat_source=proof_flat,
            expected_source_file="source/flat.tex")
        mini_proof = mini_proof_source_issues(
            proof_tex=statement.proof_tex,
            proof_sha256=statement.proof_sha256,
            proof_source_file=statement.proof_source_file,
            proof_source_start=statement.proof_source_start,
            proof_source_end=statement.proof_source_end,
            proof_source_sha256=statement.proof_source_sha256,
            proof_source_verified=statement.proof_source_verified,
            proof_pairing=statement.proof_pairing,
            flat_source=proof_flat,
            expected_source_file="source/flat.tex",
        )
        self.assertEqual(main_proof, mini_proof)

    def test_strict_target_record_policy_matches_mini(self) -> None:
        flat = "before\\begin{theorem}For every $x$, $x=x$.\\end{theorem}after"
        statement = self._statement(flat)
        expected = {
            "target_id": statement.id,
            "statement_sha256": statement.statement_sha256,
            "source_file": statement.source_file,
            "source_start": statement.source_start,
            "source_end": statement.source_end,
            "source_sha256": statement.source_sha256,
            "proof_sha256": "", "proof_source_file": "",
            "proof_source_start": -1, "proof_source_end": -1,
            "proof_source_sha256": "", "proof_source_verified": False,
            "proof_pairing": "",
        }
        extended = {**expected, "paper_id": "paper"}
        self.assertTrue(frozen_target_artifact_issues(
            statement, target_tex=statement.statement_tex, record=extended))
        self.assertTrue(mini_frozen_target_artifact_issues(
            target_tex=statement.statement_tex,
            statement_tex=statement.statement_tex,
            record=extended, expected_record=expected))
        self.assertTrue(frozen_target_artifact_issues(
            statement, target_tex=statement.statement_tex, record=[]))

    def test_mini_reuses_but_never_overwrites_frozen_target_artifacts(self) -> None:
        flat = "before\\begin{theorem}For every $x$, $x=x$.\\end{theorem}after"
        statement = self._statement(flat)
        expected = {
            "target_id": statement.id,
            "statement_sha256": statement.statement_sha256,
            "source_file": statement.source_file,
            "source_start": statement.source_start,
            "source_end": statement.source_end,
            "source_sha256": statement.source_sha256,
            "proof_sha256": "", "proof_source_file": "",
            "proof_source_start": -1, "proof_source_end": -1,
            "proof_source_sha256": "", "proof_source_verified": False,
            "proof_pairing": "",
        }
        with tempfile.TemporaryDirectory() as tmp:
            ctx = _Ctx(Path(tmp))
            pdir = ctx.path(f"packages/{statement.id}/stage2")
            pdir.mkdir(parents=True)
            self.assertEqual(freeze_or_validate_target_artifacts(
                ctx, pdir, statement, expected), [])
            (pdir / "target.tex").write_text("Tampered target.", encoding="utf-8")

            issues = freeze_or_validate_target_artifacts(
                ctx, pdir, statement, expected)

            self.assertTrue(issues)
            self.assertEqual((pdir / "target.tex").read_text(encoding="utf-8"),
                             "Tampered target.")

    def test_target_cannot_be_duplicated_as_available_support(self) -> None:
        flat = "before\\begin{theorem}For every $x$, $x=x$.\\end{theorem}after"
        statement = self._statement(flat)
        bad = ("## 5. Available results (statements only; may be used without proof)\n\n"
               + statement.statement_tex + "\n\n"
               + canonical_target_section(statement.statement_tex))
        self.assertTrue(any("outside controller-owned Section 6" in issue
                            for issue in target_identity_issues(bad, statement)))
        self.assertTrue(mini_target_identity_issues(
            bad, statement_tex=statement.statement_tex,
            statement_sha256=statement.statement_sha256))


class CleanerBridgeIntegrityTests(unittest.TestCase):
    def _write_package(self, root: Path) -> tuple[Path, str]:
        paper = root / "paper"
        package = paper / "packages" / "stmt-a" / "stage2"
        package.mkdir(parents=True)
        source = (r"before\begin{theorem}Exact target.\end{theorem}"
                  r"\begin{proof}Private proof.\end{proof}after")
        statement_text = "Exact target."
        start = source.index(r"\begin{theorem}")
        end = source.index(r"\end{theorem}") + len(r"\end{theorem}")
        statement_sha = sha256_text(statement_text)
        source_sha = sha256_text(source[start:end])
        proof_text = "Private proof."
        proof_start = source.index(r"\begin{proof}")
        proof_end = source.index(r"\end{proof}") + len(r"\end{proof}")
        proof_sha = sha256_text(proof_text)
        proof_source_sha = sha256_text(source[proof_start:proof_end])
        problem = """---
paper_id: paper
target_id: stmt-a
---

## 0. Macro definitions
none

## 1. Notation and conventions
none

## 2. Standing assumptions
none

## 3. Known external results (may be used without proof)
none

## 4. Definitions
none

## 5. Available results (statements only; may be used without proof)
none

## 6. Target

**Target statement.**

Exact target.
"""
        problem_sha = sha256_text(problem)
        (package / "problem.md").write_text(problem, encoding="utf-8")
        (package / "target.tex").write_text(statement_text, encoding="utf-8")
        target_record = {
            "target_id": "stmt-a", "statement_sha256": statement_sha,
            "source_file": "source/flat.tex", "source_start": start,
            "source_end": end, "source_sha256": source_sha,
            "proof_sha256": proof_sha,
            "proof_source_file": "source/flat.tex",
            "proof_source_start": proof_start,
            "proof_source_end": proof_end,
            "proof_source_sha256": proof_source_sha,
            "proof_source_verified": True,
            "proof_pairing": "adjacent",
        }
        (package / "target.json").write_text(
            json.dumps(target_record), encoding="utf-8")
        (package / "report.json").write_text(json.dumps({
            "problem_sha256": problem_sha,
            "input_hashes": {"target": statement_sha,
                             "reference_proof": proof_sha},
        }), encoding="utf-8")
        (paper / "manifest.json").write_text(json.dumps({
            "packages": [{"target_id": "stmt-a",
                          "path": "packages/stmt-a/stage2/problem.md"}]
        }), encoding="utf-8")
        (paper / "index").mkdir()
        (paper / "index" / "statements.v2.json").write_text(
            json.dumps({"schema_version": 2, "statements": [{
                "id": "stmt-a", "env_type": "theorem",
                "statement_tex": statement_text,
                "statement_sha256": statement_sha,
                "source_file": "source/flat.tex", "source_start": start,
                "source_end": end, "source_sha256": source_sha,
                "source_verified": True, "added_by": "parser",
                "proof_tex": proof_text, "proof_sha256": proof_sha,
                "proof_source_file": "source/flat.tex",
                "proof_source_start": proof_start,
                "proof_source_end": proof_end,
                "proof_source_sha256": proof_source_sha,
                "proof_source_verified": True,
                "proof_pairing": "adjacent",
            }]}), encoding="utf-8")
        (paper / "source").mkdir()
        (paper / "source" / "flat.tex").write_text(source, encoding="utf-8")
        (paper / "source" / "meta.json").write_text(
            '{"paper_id":"paper","source_type":"latex"}', encoding="utf-8")
        (root / "audit").mkdir()
        (root / "audit" / "audit_report.json").write_text(
            json.dumps({
                "model": "audit", "papers": [{"paper_id": "paper", "packages": [{
                    "target_id": "stmt-a", "audit_pass": True,
                    "problem_sha256": problem_sha, "hash_matches": True,
                    "det_target_issues": [], "audit": {"issues": []},
                }]}]}), encoding="utf-8")
        return package, statement_sha

    def test_bridge_requires_and_propagates_frozen_target_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, statement_sha = self._write_package(root)
            loaded = load_cleaner_package(root, "paper", "stmt-a")
            self.assertEqual(loaded.target_statement_sha256, statement_sha)
            self.assertEqual(loaded.sections.target,
                             "**Target statement.**\n\nExact target.")

    def test_bridge_rejects_tampered_target_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package, _ = self._write_package(root)
            (package / "target.tex").write_text("Improvised target.",
                                                 encoding="utf-8")
            with self.assertRaisesRegex(CleanerBridgeError,
                                        "frozen target artifacts"):
                load_cleaner_package(root, "paper", "stmt-a")

    def test_bridge_rejects_tampered_reference_proof(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_package(root)
            index_path = root / "paper" / "index" / "statements.v2.json"
            index = json.loads(index_path.read_text(encoding="utf-8"))
            index["statements"][0]["proof_tex"] = "Different proof."
            index_path.write_text(json.dumps(index), encoding="utf-8")
            with self.assertRaisesRegex(CleanerBridgeError,
                                        "source span, hashes"):
                load_cleaner_package(root, "paper", "stmt-a")

    def test_bridge_rejects_old_index_with_actionable_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_package(root)
            index_path = root / "paper" / "index" / "statements.v2.json"
            index = json.loads(index_path.read_text(encoding="utf-8"))
            index.pop("schema_version")
            index_path.write_text(json.dumps(index), encoding="utf-8")
            with self.assertRaisesRegex(CleanerBridgeError,
                                        "stale statement index; rerun"):
                load_cleaner_package(root, "paper", "stmt-a")


if __name__ == "__main__":
    unittest.main()
