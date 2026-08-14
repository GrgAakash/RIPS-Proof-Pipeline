"""Deterministic splitter for S6 composer output into per-section artifacts.

S6 returns one response containing the final proof, the Source Ledger, the
completion checklist, and the web-source confirmation. Downstream tools (the
citation gate in particular) need those sections as separate files, e.g.::

    --proof-file round_xxx/final_proof.md
    --solver-source-ledger-file round_xxx/source_ledger.md

The prompt contract asks S6 to wrap each section in exact HTML-comment
markers (``<!-- BEGIN_SOURCE_LEDGER --> ... <!-- END_SOURCE_LEDGER -->``).
Marker extraction is tried first; when a marker pair is missing (older runs
predate the markers), extraction falls back to the known section headings in
their Markdown, plain-numbered, bold, and LaTeX ``\\section*{...}`` forms.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


# Every heading S6 is allowed to emit, used both for locating sections and for
# finding where the previous section ends. Section numbers differ between the
# no-internet and internet prompt packets, so matching is by name only.
_ALL_SECTION_NAMES = (
    "Composition map",
    "Final proof",
    "Composer failure output and candidate guidance",
    "Source Ledger",
    "Completion checklist",
    "Web-source confirmation",
    "LaTeX artifact",
)


def _heading_pattern(name: str) -> str:
    """One section heading in Markdown, numbered, bold, or LaTeX form."""

    escaped = re.escape(name)
    number = r"(?:\d{1,2}[.)]\s*)?"
    return (
        rf"^(?:#{{1,6}}\s*)?\*{{0,2}}{number}{escaped}\*{{0,2}}\s*:?\s*$"
        rf"|^\\(?:sub)?section\*?\{{\s*{number}{escaped}\s*\}}\s*$"
    )


_SECTION_RES = {
    name: re.compile(_heading_pattern(name), re.IGNORECASE | re.MULTILINE)
    for name in _ALL_SECTION_NAMES
}
# Transcript separators (manual runs save whole conversations) also end a section.
_BOUNDARY_RE = re.compile(
    "|".join(_heading_pattern(name) for name in _ALL_SECTION_NAMES)
    + r"|^##\s+(?:User|Assistant)\b.*$"
    + r"|^---\s*INPUTS\b.*$",
    re.IGNORECASE | re.MULTILINE,
)


def _extract_marked(text: str, marker: str) -> str | None:
    match = re.search(
        rf"<!--\s*BEGIN_{marker}\s*-->(.*?)<!--\s*END_{marker}\s*-->",
        text,
        re.DOTALL,
    )
    if match is None:
        return None
    return match.group(1).strip() or None


def _extract_by_heading(text: str, name: str) -> str | None:
    heading = _SECTION_RES[name].search(text)
    if heading is None:
        return None
    start = heading.end()
    following = _BOUNDARY_RE.search(text, start)
    end = following.start() if following else len(text)
    return text[start:end].strip() or None


def _extract_section(text: str, marker: str, heading_name: str) -> str | None:
    marked = _extract_marked(text, marker)
    if marked is not None:
        return marked
    return _extract_by_heading(text, heading_name)


_TEX_FENCE_RE = re.compile(r"```(?:latex|tex)\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
_TEX_DOC_RE = re.compile(r"\\documentclass.*?\\end\{document\}", re.DOTALL)


def _extract_tex(text: str) -> str | None:
    """A compilable LaTeX document embedded in the S6 response, if any."""

    for match in _TEX_FENCE_RE.finditer(text):
        body = match.group(1).strip()
        if "\\documentclass" in body:
            return body
    document = _TEX_DOC_RE.search(text)
    if document:
        return document.group(0).strip()
    return None


@dataclass(frozen=True)
class S6Artifacts:
    """Sections of one S6 response, split for downstream file-level consumers."""

    final_proof: str
    source_ledger: str | None
    completion_checklist: str | None
    web_source_confirmation: str | None
    final_proof_tex: str | None


def split_s6_output(text: str) -> S6Artifacts:
    """Split an S6 response into its artifact sections.

    Marker pairs win; known headings are the fallback. The final proof falls
    back to the full response (mirroring ``report_parsers.extract_final_proof``)
    so a proof file always exists; the other sections stay ``None`` when absent.
    """

    final_proof = _extract_section(text, "FINAL_PROOF", "Final proof")
    return S6Artifacts(
        final_proof=final_proof if final_proof else text.strip(),
        source_ledger=_extract_section(text, "SOURCE_LEDGER", "Source Ledger"),
        completion_checklist=_extract_section(
            text, "COMPLETION_CHECKLIST", "Completion checklist"
        ),
        web_source_confirmation=_extract_section(
            text, "WEB_SOURCE_CONFIRMATION", "Web-source confirmation"
        ),
        final_proof_tex=_extract_tex(text),
    )


def derive_s6_artifact_files(text: str) -> dict[str, str]:
    """Map artifact filename -> content for one S6 response.

    Only sections that were actually found are included, except the final
    proof, which always is (full-text fallback).
    """

    artifacts = split_s6_output(text)
    files = {"final_proof.md": artifacts.final_proof}
    if artifacts.final_proof_tex is not None:
        files["final_proof.tex"] = artifacts.final_proof_tex
    if artifacts.source_ledger is not None:
        files["source_ledger.md"] = artifacts.source_ledger
    if artifacts.completion_checklist is not None:
        files["completion_checklist.md"] = artifacts.completion_checklist
    if artifacts.web_source_confirmation is not None:
        files["web_source_confirmation.md"] = artifacts.web_source_confirmation
    return files


def write_s6_artifacts(text: str, directory: Path) -> dict[str, Path]:
    """Write the derived artifact files next to ``S6.md``; returns the paths."""

    directory.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for name, content in derive_s6_artifact_files(text).items():
        path = directory / name
        path.write_text(content.rstrip() + "\n", encoding="utf-8")
        written[name] = path
    return written
