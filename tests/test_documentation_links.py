from __future__ import annotations

import html
import re
import subprocess
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DOCUMENTS = (
    ROOT / "README.md",
    ROOT / "SOURCE_MAP.md",
    ROOT / "CONTRIBUTORS.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "Commands" / "README.md",
    ROOT / "Prompt Packet" / "README.md",
    ROOT / "Prompt Packet" / "FlowChart.md",
    ROOT / "Individual Pipeline" / "paper_cleaner" / "README.md",
    ROOT / "Individual Pipeline" / "paper_cleaner_mini" / "README.md",
    ROOT / "Individual Pipeline" / "paper_cleaner_mini" / "docs" / "architecture.html",
    ROOT / "Individual Pipeline" / "solver" / "README.md",
    ROOT / "Individual Pipeline" / "solver" / "prompts" / "README.md",
    ROOT / "Individual Pipeline" / "citation" / "README.md",
    ROOT / "Individual Pipeline" / "citation" / "prompts" / "README.md",
    ROOT / "Individual Pipeline" / "verifiers" / "README.md",
    ROOT / "Individual Pipeline" / "verifiers" / "SubPipeline_Verifiers.md",
    ROOT / "Individual Pipeline" / "verifiers" / "prompts" / "README.md",
    ROOT / "Inputs" / "README.md",
    ROOT / "Inputs" / "paper_cleaner_input" / "README.md",
    ROOT / "Inputs" / "solver_input" / "README.md",
    ROOT / "Inputs" / "verifier_input" / "README.md",
    ROOT / "Outputs" / "README.md",
    ROOT / "Outputs" / "publishable" / "README.md",
    ROOT / "Results" / "README.md",
    ROOT / "Results" / "brokenarxiv" / "README.md",
    ROOT / "Results" / "brokenarxiv" / "runs" / "problem_38_run_02"
        / "raw_chronological_layout" / "README.md",
)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_TARGET_RE = re.compile(r"(?:href|src|srcset)=\"([^\"]+)\"")
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def prose_only(text: str) -> str:
    """Exclude fenced examples from link and heading checks."""
    lines: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return "\n".join(lines)


def document_anchors(text: str) -> set[str]:
    """Resolve the ATX headings and explicit HTML anchors used in these docs.

    This deliberately is not a full GitHub Markdown renderer. Heading slugs
    cover this repository's plain-text headings, inline formatting, and
    duplicate headings; HTML ids/named anchors are retained verbatim.
    """
    text = prose_only(text)
    anchors = set(re.findall(r'(?:id|name)=[\"\']([^\"\']+)[\"\']', text))
    used: set[str] = set()
    for heading in re.findall(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", text, re.MULTILINE):
        heading = re.sub(r"!?\[([^\]]+)\]\([^)]+\)", r"\1", heading)
        heading = html.unescape(re.sub(r"<[^>]+>", "", heading)).lower()
        slug = re.sub(r"[^\w\s-]", "", heading).replace(" ", "-")
        candidate = slug
        suffix = 0
        while candidate in used:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        used.add(candidate)
        anchors.add(candidate)
    return anchors


class DocumentationLinkTests(unittest.TestCase):
    def test_every_reader_facing_local_link_resolves(self) -> None:
        broken: list[str] = []
        for document in PUBLIC_DOCUMENTS:
            self.assertTrue(document.is_file(), f"missing public document: {document}")
            text = prose_only(document.read_text(encoding="utf-8-sig"))
            targets = MARKDOWN_LINK_RE.findall(text) + HTML_TARGET_RE.findall(text)
            for raw_target in targets:
                target = unquote(raw_target.strip().strip("<>"))
                target = target.split("#", 1)[0].split("?", 1)[0]
                if not target or SCHEME_RE.match(target):
                    continue
                if not (document.parent / target).exists():
                    broken.append(
                        f"{document.relative_to(ROOT)} -> {raw_target}"
                    )

        self.assertEqual(broken, [], f"broken documentation links: {broken}")

    def test_every_reader_facing_local_section_link_resolves(self) -> None:
        broken: list[str] = []
        for document in PUBLIC_DOCUMENTS:
            text = prose_only(document.read_text(encoding="utf-8-sig"))
            for raw in MARKDOWN_LINK_RE.findall(text) + HTML_TARGET_RE.findall(text):
                target = html.unescape(raw.strip().strip("<>"))
                if SCHEME_RE.match(target) or "#" not in target:
                    continue
                path, fragment = target.split("#", 1)
                destination = document.parent / unquote(path.split("?", 1)[0]) if path else document
                fragment = unquote(fragment)
                if not fragment or destination.suffix not in {".md", ".html"}:
                    continue
                if not destination.is_file() or fragment not in document_anchors(
                    destination.read_text(encoding="utf-8-sig")
                ):
                    broken.append(f"{document.relative_to(ROOT)} -> {raw}")
        self.assertEqual(broken, [], f"broken documentation section links: {broken}")

    def test_every_readme_is_included(self) -> None:
        # Ignore private run workspaces, environments, and other Git-ignored files.
        paths = subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT
        ).decode().split("\0")
        readmes = {
            ROOT / path for path in paths
            if Path(path).name == "README.md" and (ROOT / path).is_file()
        }
        self.assertEqual(readmes - set(PUBLIC_DOCUMENTS), set())

    def test_anchor_extraction_ignores_examples_and_handles_duplicates(self) -> None:
        sample = '# A `title`!\n## A title\n```md\n## Hidden\n```\n<a id="explicit"></a>'
        self.assertEqual(document_anchors(sample), {"a-title", "a-title-1", "explicit"})


if __name__ == "__main__":
    unittest.main()
