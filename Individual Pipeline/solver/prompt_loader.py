"""Load the fixed role prompts from the prompt packet and fill placeholders.

The selected canonical prompt packet is the source of truth for every role:
``Prompt Packet/Prompts.md`` for no-internet solvers or
``Prompt Packet/PromptsWithFullInternet.md`` for source-supported solvers.
Each fixed prompt is extracted at runtime, anchored on its unique
``You are ...`` opening line and ending at the next divider line (a full line of
``=`` or ``-``), matching the packet's own Prompt Assembler rule that packets
begin at the "You are ..." line and that controller-only text above it must not
be pasted into any model chat.

The prompt text is reproduced byte-identically except that:

* bracketed ``[PASTE ...]`` placeholders are replaced with run values, and
* because API calls cannot attach files, the cleaned skeleton is inlined into
  the user message under an explicit ``ATTACHED CLEANED SKELETON`` label for
  the roles that receive it.

Each filled prompt is split into a ``PromptPacket`` at the literal
``--- INPUTS FOR THIS RUN ---`` line: the fixed instructions become the system
message and the inputs section becomes the user message.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from solver.packet import PromptPacket


class PromptLoaderError(RuntimeError):
    """Raised when a fixed prompt cannot be extracted or filled from the packet."""


def _default_packet_path(filename: str) -> Path:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "Prompt Packet" / filename
        if candidate.is_file():
            return candidate
    return Path("Prompt Packet") / filename


DEFAULT_PACKET_PATH = _default_packet_path("PromptsWithFullInternet.md")

# Unique opening line per role. Extraction is anchored on these so packet
# reorganization that keeps the fixed prompts intact does not break loading.
ROLE_ANCHORS: dict[str, str] = {
    "s0": "You are S0, the Blueprint Solver.",
    "subproblem": "You are [PASTE S-ID: S1 / S2 / S3 / S4 / S5], a Subproblem Solver.",
    "s6": "You are S6, the Composer Solver.",
    "problem_statement_verifier": "You are the Problem Statement Verifier.",
    "verifier_a": "You are one independent Verifier A run, a strict mathematical referee.",
    "verifier_b": "You are Verifier B.",
    "verifier_c": "You are Verifier C.",
    "composer_a": "You are Composer A.",
    "final_checker": "You are the Final Checker, a privileged mathematical referee.",
}

# Placeholders each extracted prompt must contain; a missing one means the
# packet was edited in a way this loader no longer understands -> fail loudly.
ROLE_REQUIRED_PLACEHOLDERS: dict[str, tuple[str, ...]] = {
    "s0": ("[PASTE TARGET THEOREM]", '[PASTE CURRENT GUIDANCE LIST, OR WRITE "None"]'),
    "subproblem": (
        "[PASTE S-ID: S1 / S2 / S3 / S4 / S5]",
        "[PASTE TARGET THEOREM]",
        '[PASTE CURRENT GUIDANCE LIST, OR WRITE "None"]',
        "[PASTE S0 BLUEPRINT HERE]",
        "[PASTE THIS S-SOLVER ASSIGNMENT HERE]",
    ),
    "s6": (
        "[PASTE TARGET THEOREM]",
        '[PASTE CURRENT GUIDANCE LIST, OR WRITE "None"]',
        "[PASTE S0 BLUEPRINT HERE]",
        "[PASTE S1-S5 OUTPUTS HERE]",
    ),
    "problem_statement_verifier": (
        "[PASTE TARGET THEOREM]",
        "[PASTE ROLE]",
        "[PASTE AGENT OUTPUT HERE]",
    ),
    "verifier_a": (
        "[PASTE TARGET THEOREM]",
        '[PASTE CURRENT GUIDANCE LIST, OR WRITE "None"]',
        "[PASTE PROPOSED PROOF HERE]",
        "[PASTE SOURCE LEDGER HERE]",
        "[PASTE CITATION VERIFIER REPORT HERE]",
    ),
    "verifier_b": (
        "[PASTE TARGET THEOREM]",
        '[PASTE CURRENT GUIDANCE LIST, OR WRITE "None"]',
        "[PASTE PROPOSED PROOF HERE]",
        "[PASTE SOURCE LEDGER HERE]",
        "[PASTE CITATION VERIFIER REPORT HERE]",
    ),
    "verifier_c": (
        "[PASTE TARGET THEOREM]",
        '[PASTE CURRENT GUIDANCE LIST, OR WRITE "None"]',
        "[PASTE PROPOSED PROOF HERE]",
        "[PASTE SOURCE LEDGER HERE]",
        "[PASTE CITATION VERIFIER REPORT HERE]",
    ),
    "composer_a": ("[PASTE A1, A2, A3, ...]",),
    "final_checker": (
        "[PASTE TARGET THEOREM]",
        "[PASTE PUBLIC PREFIX, OR NOTE IT IS THE ATTACHED SKELETON PDF OR TEX FILE]",
        "[PASTE CANDIDATE SOLVER PROOF]",
        "[PASTE PRIVATE GOLD PROOF]",
        '[PASTE OR WRITE "Not provided"]',
        '[PASTE CURRENT GUIDANCE LIST, OR WRITE "None"]',
    ),
}

# The multi-line allowed-supporting-statements placeholder block. The whole
# bracketed region (which embeds the default rule) is replaced with the run's
# allowed-support text.
_ALLOWED_BLOCK_RE = re.compile(
    r"\[PASTE EXPLICIT ALLOWED SUPPORTING STATEMENTS.*?explicitly says so\.\]",
    re.DOTALL,
)

# The packet's default allowed-support rule, used when a run supplies none.
DEFAULT_ALLOWED_SUPPORT = """Definitions, notation, and assumptions needed to state or parse the target theorem are allowed.
All formal statements appearing textually before the target theorem are allowed unless listed in Exclusions.
Formal statements appearing textually after the target theorem are not allowed unless listed in Later-but-upstream inclusions.
No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

Later-but-upstream inclusions:
None.

Exclusions:
None.

Unclear:
None.

This list or rule is authoritative for this run. Packet order controls allowedness only because this default rule explicitly says so."""

# Divider lines that terminate a fixed prompt in the packet.
_DIVIDER_RE = re.compile(r"(?m)^(?:={16,}|-{16,})\s*$")
# The line splitting fixed instructions (system) from run inputs (user).
_INPUTS_MARKER = "--- INPUTS FOR THIS RUN ---"

_SKELETON_LABEL = "--- ATTACHED CLEANED SKELETON (inlined for this API run) ---"


def render_guidance(guidance: list[str]) -> str:
    """Render the cumulative guidance list the way the packet expects."""

    items = [item.strip() for item in guidance if item.strip()]
    if not items:
        return "None"
    return "\n\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


@dataclass(frozen=True)
class PacketPrompts:
    """Fixed role prompts extracted from one prompt-packet file."""

    prompts: dict[str, str]

    @property
    def requires_key_solver_first(self) -> bool:
        """Whether this packet's S0 contract enables the key-first schedule."""

        return re.search(
            r"(?mi)^\s*key_solver_id\s*:", self.prompts["s0"]
        ) is not None

    @classmethod
    def from_text(cls, packet_text: str) -> "PacketPrompts":
        prompts: dict[str, str] = {}
        for role, anchor in ROLE_ANCHORS.items():
            prompts[role] = _extract_prompt(packet_text, role, anchor)
        return cls(prompts=prompts)

    @classmethod
    def from_file(cls, path: str | Path = DEFAULT_PACKET_PATH) -> "PacketPrompts":
        packet_path = Path(path)
        if not packet_path.exists():
            raise PromptLoaderError(f"prompt packet file not found: {packet_path}")
        return cls.from_text(packet_path.read_text(encoding="utf-8"))

    # --- packet builders, one per role -----------------------------------

    def build_s0(
        self,
        target: str,
        guidance: list[str],
        skeleton: str,
        allowed_support: str | None = None,
    ) -> PromptPacket:
        filled = self._fill(
            "s0",
            allowed_support,
            {
                "[PASTE TARGET THEOREM]": target,
                '[PASTE CURRENT GUIDANCE LIST, OR WRITE "None"]': render_guidance(guidance),
            },
        )
        return _split_packet("s0", filled, skeleton)

    def build_subproblem(
        self,
        s_id: str,
        target: str,
        guidance: list[str],
        blueprint: str,
        assignment: str,
        skeleton: str,
        allowed_support: str | None = None,
    ) -> PromptPacket:
        filled = self._fill(
            "subproblem",
            allowed_support,
            {
                "[PASTE S-ID: S1 / S2 / S3 / S4 / S5]": s_id,
                "[PASTE TARGET THEOREM]": target,
                '[PASTE CURRENT GUIDANCE LIST, OR WRITE "None"]': render_guidance(guidance),
                "[PASTE S0 BLUEPRINT HERE]": blueprint,
                "[PASTE THIS S-SOLVER ASSIGNMENT HERE]": assignment,
            },
        )
        return _split_packet("subproblem", filled, skeleton)

    def build_s6(
        self,
        target: str,
        guidance: list[str],
        blueprint: str,
        subproblem_outputs: str,
        skeleton: str,
        allowed_support: str | None = None,
    ) -> PromptPacket:
        filled = self._fill(
            "s6",
            allowed_support,
            {
                "[PASTE TARGET THEOREM]": target,
                '[PASTE CURRENT GUIDANCE LIST, OR WRITE "None"]': render_guidance(guidance),
                "[PASTE S0 BLUEPRINT HERE]": blueprint,
                "[PASTE S1-S5 OUTPUTS HERE]": subproblem_outputs,
            },
        )
        return _split_packet("s6", filled, skeleton)

    def build_verifier(
        self,
        stage: str,
        target: str,
        guidance: list[str],
        proof_artifact: str,
        skeleton: str,
        allowed_support: str | None = None,
        source_ledger: str | None = None,
        citation_report: str | None = None,
    ) -> PromptPacket:
        """Build one Verifier A/B/C packet.

        ``source_ledger`` and ``citation_report`` are supplied by the mandatory
        post-S6 citation gate. The honest defaults remain for isolated prompt
        tests and explicitly bypassed legacy callers.
        """

        if stage not in {"verifier_a", "verifier_b", "verifier_c"}:
            raise PromptLoaderError(f"unknown verifier stage: {stage}")
        filled = self._fill(
            stage,
            allowed_support,
            {
                "[PASTE TARGET THEOREM]": target,
                '[PASTE CURRENT GUIDANCE LIST, OR WRITE "None"]': render_guidance(guidance),
                "[PASTE PROPOSED PROOF HERE]": proof_artifact,
                "[PASTE SOURCE LEDGER HERE]": source_ledger or "Not provided for this run.",
                "[PASTE CITATION VERIFIER REPORT HERE]": citation_report
                or "Not provided for this run.",
            },
        )
        return _split_packet(stage, filled, skeleton)

    def build_problem_statement_verifier(
        self,
        target: str,
        artifact_role: str,
        agent_output: str,
        skeleton: str,
    ) -> PromptPacket:
        """Build the mandatory exact-target alignment check for an S6 proof."""

        filled = self._fill(
            "problem_statement_verifier",
            None,
            {
                "[PASTE TARGET THEOREM]": target,
                "[PASTE ROLE]": artifact_role,
                "[PASTE AGENT OUTPUT HERE]": agent_output,
            },
        )
        return _split_packet("problem_statement_verifier", filled, skeleton)

    def build_composer_a(self, verifier_a_reports: list[str]) -> PromptPacket:
        joined = "\n\n".join(
            f"### Verifier A report {index}\n\n{report.strip()}"
            for index, report in enumerate(verifier_a_reports, start=1)
        )
        filled = self._fill(
            "composer_a",
            None,
            {
                '[PASTE OR WRITE "None"]': "None",
                "[PASTE A1, A2, A3, ...]": joined,
            },
        )
        # Composer A sees only the Verifier A reports -- no skeleton, target, or proof.
        return _split_packet("composer_a", filled, skeleton=None)

    def build_final_checker(
        self,
        target: str,
        skeleton: str,
        candidate_proof: str,
        gold_proof: str,
        full_source: str | None,
        guidance: list[str],
    ) -> PromptPacket:
        filled = self._fill(
            "final_checker",
            None,
            {
                "[PASTE TARGET THEOREM]": target,
                "[PASTE PUBLIC PREFIX, OR NOTE IT IS THE ATTACHED SKELETON PDF OR TEX FILE]": skeleton,
                "[PASTE CANDIDATE SOLVER PROOF]": candidate_proof,
                "[PASTE PRIVATE GOLD PROOF]": gold_proof,
                '[PASTE OR WRITE "Not provided"]': full_source or "Not provided",
                '[PASTE CURRENT GUIDANCE LIST, OR WRITE "None"]': render_guidance(guidance),
            },
        )
        # The skeleton is already inlined through the public-prefix placeholder.
        return _split_packet("final_checker", filled, skeleton=None)

    # --- internals ---------------------------------------------------------

    def _fill(
        self,
        role: str,
        allowed_support: str | None,
        replacements: dict[str, str],
    ) -> str:
        text = self.prompts[role]
        if _ALLOWED_BLOCK_RE.search(text):
            text = _ALLOWED_BLOCK_RE.sub(
                lambda _match: allowed_support or DEFAULT_ALLOWED_SUPPORT, text
            )
        for placeholder, value in replacements.items():
            if placeholder not in text:
                raise PromptLoaderError(f"{role}: placeholder missing from packet prompt: {placeholder}")
            text = text.replace(placeholder, value)
        return text


def _extract_prompt(packet_text: str, role: str, anchor: str) -> str:
    """Extract one fixed prompt: from its anchor line to the next divider line."""

    start = packet_text.find(anchor)
    if start < 0:
        raise PromptLoaderError(f"{role}: anchor line not found in packet: {anchor!r}")
    divider = _DIVIDER_RE.search(packet_text, start)
    end = divider.start() if divider else len(packet_text)
    prompt = packet_text[start:end].strip() + "\n"
    for placeholder in ROLE_REQUIRED_PLACEHOLDERS[role]:
        if placeholder not in prompt:
            raise PromptLoaderError(
                f"{role}: expected placeholder not found in extracted prompt: {placeholder}"
            )
    return prompt


def _split_packet(role: str, filled: str, skeleton: str | None) -> PromptPacket:
    """Split a filled prompt into system/user at the INPUTS marker.

    The fixed instructions become the system message; the run inputs (and the
    inlined skeleton, when supplied) become the user message. Prompts without
    an inputs marker are sent entirely as the system message with the skeleton
    (if any) as the user message.
    """

    marker_index = filled.find(_INPUTS_MARKER)
    if marker_index >= 0:
        system = filled[:marker_index].rstrip() + "\n"
        user = filled[marker_index:].strip() + "\n"
    else:
        system = filled.rstrip() + "\n"
        user = ""
    if skeleton is not None:
        user = f"{user}\n{_SKELETON_LABEL}\n{skeleton.strip()}\n"
    if not user.strip():
        user = "Proceed per the instructions above.\n"
    return PromptPacket(role=role, system=system, user=user)
