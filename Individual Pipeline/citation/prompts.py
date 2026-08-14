"""Prompt builders for the Citation Generator and Verifier roles."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .constants import FORBIDDEN_PUBLIC_FRAGMENTS
from .models import PromptPacket


def _default_packet_path(filename: str) -> Path:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "Prompt Packet" / filename
        if candidate.is_file():
            return candidate
    return Path("Prompt Packet") / filename


DEFAULT_PACKET_PATH = _default_packet_path("Prompts.md")

_ROLE_ANCHORS = {
    "citation_generator": "You are the Citation Generator.",
    "citation_verifier": "You are the Citation Verifier.",
}

_ROLE_REQUIRED_PLACEHOLDERS = {
    "citation_generator": (
        "[PASTE TARGET THEOREM]",
        "[PASTE CURRENT GUIDANCE LIST, OR WRITE \"None\"]",
        "[PASTE PROPOSED PROOF HERE]",
        "[PASTE SOLVER SOURCE LEDGER, OR WRITE \"None\"]",
        "[PASTE BIBLIOGRAPHY / .BIB / .BBL, OR WRITE \"None\"]",
    ),
    "citation_verifier": (
        "[PASTE TARGET THEOREM]",
        "[PASTE CURRENT GUIDANCE LIST, OR WRITE \"None\"]",
        "[PASTE PROPOSED PROOF HERE]",
        "[PASTE SOURCE LEDGER HERE]",
        "[PASTE BIBLIOGRAPHY / .BIB / .BBL, OR WRITE \"None\"]",
    ),
}

_ALLOWED_BLOCK_RE = re.compile(
    r"\[PASTE EXPLICIT ALLOWED SUPPORTING STATEMENTS.*?explicitly says so\.\]",
    re.DOTALL,
)
_DIVIDER_RE = re.compile(r"(?m)^(?:={16,}|-{16,})\s*$")
_INPUTS_MARKER = "--- INPUTS FOR THIS RUN ---"
_PROVIDED_PACKET_LABEL = "Provided mathematical packet:"


class CitationPromptTemplateError(RuntimeError):
    """Raised when citation prompts cannot be extracted from a prompt packet."""


@dataclass(frozen=True)
class CitationPromptTemplates:
    """Citation prompts extracted from a manual prompt-packet file."""

    prompts: dict[str, str]

    @classmethod
    def from_file(cls, path: str | Path = DEFAULT_PACKET_PATH) -> "CitationPromptTemplates":
        packet_path = Path(path)
        if not packet_path.exists():
            raise CitationPromptTemplateError(f"prompt packet file not found: {packet_path}")
        return cls.from_text(packet_path.read_text(encoding="utf-8"))

    @classmethod
    def from_text(cls, packet_text: str) -> "CitationPromptTemplates":
        return cls(
            prompts={
                role: _extract_prompt(packet_text, role, anchor)
                for role, anchor in _ROLE_ANCHORS.items()
            }
        )

    def build_citation_generator_prompt(
        self,
        *,
        target_theorem: str,
        provided_packet: str,
        allowed_supporting_statements: str,
        guidance: str,
        proof: str,
        solver_source_ledger: str,
        bibliography: str,
    ) -> PromptPacket:
        filled = self._fill(
            "citation_generator",
            allowed_supporting_statements,
            {
                "[PASTE TARGET THEOREM]": target_theorem,
                "[PASTE CURRENT GUIDANCE LIST, OR WRITE \"None\"]": guidance or "None",
                "[PASTE PROPOSED PROOF HERE]": proof,
                "[PASTE SOLVER SOURCE LEDGER, OR WRITE \"None\"]": solver_source_ledger or "None",
                "[PASTE BIBLIOGRAPHY / .BIB / .BBL, OR WRITE \"None\"]": bibliography or "None",
            },
        )
        return _split_packet("citation_generator", filled, provided_packet)

    def build_citation_verifier_prompt(
        self,
        *,
        target_theorem: str,
        provided_packet: str,
        allowed_supporting_statements: str,
        guidance: str,
        proof: str,
        citation_generator_source_ledger: str,
        bibliography: str,
    ) -> PromptPacket:
        filled = self._fill(
            "citation_verifier",
            allowed_supporting_statements,
            {
                "[PASTE TARGET THEOREM]": target_theorem,
                "[PASTE CURRENT GUIDANCE LIST, OR WRITE \"None\"]": guidance or "None",
                "[PASTE PROPOSED PROOF HERE]": proof,
                "[PASTE SOURCE LEDGER HERE]": citation_generator_source_ledger,
                "[PASTE BIBLIOGRAPHY / .BIB / .BBL, OR WRITE \"None\"]": bibliography or "None",
            },
        )
        return _split_packet("citation_verifier", filled, provided_packet)

    def _fill(
        self,
        role: str,
        allowed_supporting_statements: str,
        replacements: dict[str, str],
    ) -> str:
        text = self.prompts[role]
        if _ALLOWED_BLOCK_RE.search(text):
            text = _ALLOWED_BLOCK_RE.sub(lambda _match: allowed_supporting_statements, text)
        for placeholder, value in replacements.items():
            if placeholder not in text:
                raise CitationPromptTemplateError(
                    f"{role}: placeholder missing from packet prompt: {placeholder}"
                )
            text = text.replace(placeholder, value)
        return text


def build_citation_generator_prompt(
    *,
    target_theorem: str,
    provided_packet: str,
    allowed_supporting_statements: str,
    guidance: str,
    proof: str,
    solver_source_ledger: str = "None",
    bibliography: str = "None",
    prompt_templates: CitationPromptTemplates | None = None,
) -> PromptPacket:
    """Build the Citation Generator prompt from public-only material."""

    _assert_public_material(
        "Citation Generator",
        target_theorem,
        provided_packet,
        allowed_supporting_statements,
        guidance,
        proof,
        solver_source_ledger,
        bibliography,
    )
    templates = prompt_templates or CitationPromptTemplates.from_file(DEFAULT_PACKET_PATH)
    return templates.build_citation_generator_prompt(
        target_theorem=target_theorem,
        provided_packet=provided_packet,
        allowed_supporting_statements=allowed_supporting_statements,
        guidance=guidance,
        proof=proof,
        solver_source_ledger=solver_source_ledger,
        bibliography=bibliography,
    )


def build_citation_verifier_prompt(
    *,
    target_theorem: str,
    provided_packet: str,
    allowed_supporting_statements: str,
    guidance: str,
    proof: str,
    citation_generator_source_ledger: str,
    bibliography: str = "None",
    prompt_templates: CitationPromptTemplates | None = None,
) -> PromptPacket:
    """Build the Citation Verifier prompt from public-only material."""

    _assert_public_material(
        "Citation Verifier",
        target_theorem,
        provided_packet,
        allowed_supporting_statements,
        guidance,
        proof,
        citation_generator_source_ledger,
        bibliography,
    )
    templates = prompt_templates or CitationPromptTemplates.from_file(DEFAULT_PACKET_PATH)
    return templates.build_citation_verifier_prompt(
        target_theorem=target_theorem,
        provided_packet=provided_packet,
        allowed_supporting_statements=allowed_supporting_statements,
        guidance=guidance,
        proof=proof,
        citation_generator_source_ledger=citation_generator_source_ledger,
        bibliography=bibliography,
    )


def build_citation_reformat_prompt(role_name: str, required_fields: list[str], previous_response: str) -> PromptPacket:
    """Ask a citation role to re-emit only the machine-parsed summary fields."""

    fields = "\n".join(f"{field}:" for field in required_fields)
    system = """SYSTEM ROLE: Citation Summary Reformatter.

You do not add mathematical content, source claims, citations, or new judgments.
You only reformat the previous response into the exact requested field list.
If a value was absent in the previous response, write UNCLEAR except for candidate guidance,
where you may write None. Return only the field list and values.

Single-choice fields must contain exactly one label. If the previous response combined
multiple labels (for example joined with "/"), select the one consistent with the other
reported fields: MANUAL_REVIEW_FOR_LEAKAGE only if "Possible target-source leakage
encountered" is YES; otherwise SOURCE_LEDGER_REPAIR_NEEDED if the previous response indicates
ledger repair is needed; otherwise the remaining label.
"""
    user = f"""Original role:
{role_name}

Required fields:
{fields}

Previous response:
{previous_response}
"""
    return PromptPacket(role="citation_reformat", system=system, user=user)


def _assert_public_material(role: str, *chunks: str) -> None:
    """Fail fast if proof-blind citation prompts receive private markers."""

    joined = "\n".join(chunks)
    for fragment in FORBIDDEN_PUBLIC_FRAGMENTS:
        if fragment in joined:
            raise RuntimeError(f"{role} prompt contains forbidden private fragment: {fragment}")


def _extract_prompt(packet_text: str, role: str, anchor: str) -> str:
    """Extract a fixed citation prompt from its anchor line to the next divider."""

    start = packet_text.find(anchor)
    if start < 0:
        raise CitationPromptTemplateError(f"{role}: anchor line not found in packet: {anchor!r}")
    divider = _DIVIDER_RE.search(packet_text, start)
    end = divider.start() if divider else len(packet_text)
    prompt = packet_text[start:end].strip() + "\n"
    for placeholder in _ROLE_REQUIRED_PLACEHOLDERS[role]:
        if placeholder not in prompt:
            raise CitationPromptTemplateError(
                f"{role}: expected placeholder not found in extracted prompt: {placeholder}"
            )
    return prompt


def _split_packet(role: str, filled: str, provided_packet: str) -> PromptPacket:
    """Split fixed instructions from run inputs and inline the provided packet."""

    marker_index = filled.find(_INPUTS_MARKER)
    if marker_index >= 0:
        system = filled[:marker_index].rstrip() + "\n"
        user = filled[marker_index:].strip() + "\n"
    else:
        system = filled.rstrip() + "\n"
        user = ""
    user = _inject_provided_packet(user, provided_packet)
    if not user.strip():
        user = "Proceed per the instructions above.\n"
    return PromptPacket(role=role, system=system, user=user)


def _inject_provided_packet(user: str, provided_packet: str) -> str:
    packet = (provided_packet or "None").strip() or "None"
    insertion = f"{_PROVIDED_PACKET_LABEL}\n{packet}\n\n"
    stripped = user.strip()
    if stripped.startswith(_INPUTS_MARKER):
        rest = stripped[len(_INPUTS_MARKER) :].lstrip()
        return f"{_INPUTS_MARKER}\n\n{insertion}{rest}\n"
    if stripped:
        return f"{stripped}\n\n{insertion}"
    return insertion
