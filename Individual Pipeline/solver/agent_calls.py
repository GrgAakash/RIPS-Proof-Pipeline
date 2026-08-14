"""Thin role-call wrappers for the open-problem workflow.

One method per LLM role. Each builds its packet via
:class:`~solver.prompt_loader.PacketPrompts`, invokes
the configured client with routing metadata (role, pipeline id, round, S-id),
and returns the raw response text. All parsing lives in ``report_parsers.py``;
all routing lives in ``controller.py``.

Client trust classes mirror the protocol:

* ``solver_client``   -- default client for S0, S1-S5, S6 (internet-permitted
  roles in the manual protocol; plain completions here). Optional per-solver
  clients can override this default for expensive/key roles.
* ``citation_client`` -- Citation Generator and Citation Verifier. These roles
  may browse only for restricted source checking in both packet modes.
* ``verifier_client`` -- Verifier A1/A2/A3, Composer A, Verifier B, Verifier C
  (gold-blind; must never receive gold material).
* ``checker_client``  -- the privileged Final Checker only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from solver.io_utils import parse_json_object
from solver.llm import LLMClient
from solver.prompt_loader import (
    DEFAULT_ALLOWED_SUPPORT,
    PacketPrompts,
    render_guidance,
)
from citation.gate import run_citation_gate
from citation.models import CitationGateDecision
from citation.prompts import CitationPromptTemplates
from solver.packet import PromptPacket


# Roles the packet permits to browse in source-supported mode (Operating Rule
# 2): S0, S1-S5, and S6. "Proof Verifiers, Composer A, Decision Controller,
# Controller Audit, and Final Checker still do not browse." The reformatter is
# mechanical and gets no tools either. Pass this set as the client's
# web_search_roles so the hosted web_search tool is attached to exactly these
# prompt roles and no others.
INTERNET_ENABLED_ROLES = frozenset({"s0", "subproblem", "s6"})

# Deterministic reformatter prompt used when a solver output's section 3 cannot
# be parsed. This is mechanical field extraction, not new mathematics.
_REFORMAT_SYSTEM = """SYSTEM ROLE: Output reformatter.

You are given one solver output from a mathematical proof pipeline. Extract its
"Solver failure output and candidate guidance" (or "Composer failure output and
candidate guidance") section into strict JSON. Do not add, remove, or reinterpret
mathematical content. Copy field values verbatim from the output.

Return exactly one JSON object and nothing else, with these keys:
{"failure_output_type": "solved | forbidden-route / obstruction guidance | branch lemma target | ordinary hint request | no useful guidance item found",
 "type": "...", "failed_route": "...", "obstruction": "...", "evidence": "...",
 "reuse_value": "...", "guidance_sentence": "...",
 "candidate_lemma_statement": "...", "lemma_equivalent_or_stronger": "YES | NO | UNCLEAR",
 "lemma_recommended": "YES | NO | UNCLEAR"}

Use "" for fields the output does not contain.
"""


@dataclass
class AgentCaller:
    """Bundle of prompt templates + per-trust-class clients + call plumbing."""

    prompts: PacketPrompts
    solver_client: LLMClient
    s0_client: LLMClient | None = None
    subproblem_clients: dict[str, LLMClient] = field(default_factory=dict)
    key_solver_client: LLMClient | None = None
    s6_client: LLMClient | None = None
    citation_client: LLMClient | None = None
    citation_prompts: CitationPromptTemplates | None = None
    verifier_client: LLMClient | None = None
    verifier_a_client: LLMClient | None = None
    composer_a_client: LLMClient | None = None
    verifier_b_client: LLMClient | None = None
    verifier_c_client: LLMClient | None = None
    checker_client: LLMClient | None = None
    progress: Callable[[str], None] | None = None
    base_metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._citation: LLMClient = self.citation_client or self.solver_client
        self._verifier: LLMClient = self.verifier_client or self.solver_client
        self._checker: LLMClient = self.checker_client or self.solver_client
        if self.citation_prompts is None:
            self.citation_prompts = CitationPromptTemplates.from_file()

    # --- solver roles ------------------------------------------------------

    def call_s0(
        self,
        target: str,
        guidance: list[str],
        skeleton: str,
        allowed_support: str | None,
        round_index: int,
    ) -> str:
        packet = self.prompts.build_s0(target, guidance, skeleton, allowed_support)
        return self._complete(self.s0_client or self.solver_client, packet, round_index)

    def call_subproblem(
        self,
        s_id: str,
        target: str,
        guidance: list[str],
        blueprint: str,
        assignment: str,
        skeleton: str,
        allowed_support: str | None,
        round_index: int,
        use_key_model: bool = False,
    ) -> str:
        packet = self.prompts.build_subproblem(
            s_id, target, guidance, blueprint, assignment, skeleton, allowed_support
        )
        client = self._subproblem_client(s_id, use_key_model=use_key_model)
        return self._complete(client, packet, round_index, s_id=s_id)

    def call_s6(
        self,
        target: str,
        guidance: list[str],
        blueprint: str,
        subproblem_outputs: str,
        skeleton: str,
        allowed_support: str | None,
        round_index: int,
    ) -> str:
        packet = self.prompts.build_s6(
            target, guidance, blueprint, subproblem_outputs, skeleton, allowed_support
        )
        return self._complete(self.s6_client or self.solver_client, packet, round_index)

    # --- citation gate ----------------------------------------------------

    def call_problem_statement_verifier(
        self,
        *,
        target: str,
        artifact_role: str,
        agent_output: str,
        skeleton: str,
        round_index: int,
    ) -> str:
        """Check that the composed proof addresses the exact target theorem."""

        packet = self.prompts.build_problem_statement_verifier(
            target, artifact_role, agent_output, skeleton
        )
        return self._complete(self._verifier, packet, round_index)

    def call_citation_gate(
        self,
        *,
        output_dir: Path,
        target: str,
        provided_packet: str,
        allowed_support: str | None,
        guidance: list[str],
        proof: str,
        solver_source_ledger: str,
        bibliography: str | None,
        round_index: int,
        attempt: int,
    ) -> CitationGateDecision:
        """Run Citation Generator -> Citation Verifier with public material."""

        return run_citation_gate(
            output_dir=output_dir,
            target_theorem=target,
            provided_packet=provided_packet,
            allowed_supporting_statements=allowed_support or DEFAULT_ALLOWED_SUPPORT,
            guidance=render_guidance(guidance),
            proof=proof,
            solver_source_ledger=solver_source_ledger or "None",
            bibliography=bibliography or "None",
            client=self._citation,
            prompt_templates=self.citation_prompts,
            metadata={
                **self.base_metadata,
                "round": round_index,
                "citation_attempt": attempt,
            },
            progress=self.progress,
        )

    # --- verifier roles ----------------------------------------------------

    def call_verifier_a(
        self,
        run_label: str,
        target: str,
        guidance: list[str],
        proof_artifact: str,
        skeleton: str,
        allowed_support: str | None,
        round_index: int,
        source_ledger: str,
        citation_report: str,
    ) -> str:
        packet = self.prompts.build_verifier(
            "verifier_a",
            target,
            guidance,
            proof_artifact,
            skeleton,
            allowed_support,
            source_ledger,
            citation_report,
        )
        return self._complete(self.verifier_a_client or self._verifier, packet, round_index, s_id=run_label)

    def call_composer_a(self, verifier_a_reports: list[str], round_index: int) -> str:
        packet = self.prompts.build_composer_a(verifier_a_reports)
        return self._complete(self.composer_a_client or self._verifier, packet, round_index)

    def call_verifier_b(
        self,
        target: str,
        guidance: list[str],
        proof_artifact: str,
        skeleton: str,
        allowed_support: str | None,
        round_index: int,
        source_ledger: str,
        citation_report: str,
    ) -> str:
        packet = self.prompts.build_verifier(
            "verifier_b",
            target,
            guidance,
            proof_artifact,
            skeleton,
            allowed_support,
            source_ledger,
            citation_report,
        )
        return self._complete(self.verifier_b_client or self._verifier, packet, round_index)

    def call_verifier_c(
        self,
        target: str,
        guidance: list[str],
        proof_artifact: str,
        skeleton: str,
        allowed_support: str | None,
        round_index: int,
        source_ledger: str,
        citation_report: str,
    ) -> str:
        packet = self.prompts.build_verifier(
            "verifier_c",
            target,
            guidance,
            proof_artifact,
            skeleton,
            allowed_support,
            source_ledger,
            citation_report,
        )
        return self._complete(self.verifier_c_client or self._verifier, packet, round_index)

    # --- privileged role ---------------------------------------------------

    def call_final_checker(
        self,
        target: str,
        skeleton: str,
        candidate_proof: str,
        gold_proof: str,
        full_source: str | None,
        guidance: list[str],
        round_index: int,
    ) -> str:
        packet = self.prompts.build_final_checker(
            target, skeleton, candidate_proof, gold_proof, full_source, guidance
        )
        return self._complete(self._checker, packet, round_index)

    # --- mechanical reformatter ---------------------------------------------

    def reformat_failure_output(self, raw_output: str, round_index: int) -> dict | None:
        """One retry to convert an unparseable section 3 into strict JSON.

        Returns the parsed JSON object, or ``None`` when even the reformatted
        response is unusable (the caller then routes as no-useful-guidance).
        """

        packet = PromptPacket(role="reformatter", system=_REFORMAT_SYSTEM, user=raw_output)
        text = self._complete(self.solver_client, packet, round_index)
        try:
            return parse_json_object(text, "Reformatter")
        except Exception:  # noqa: BLE001 - any parse failure degrades gracefully
            return None

    # --- internals -----------------------------------------------------------

    def _subproblem_client(self, s_id: str, use_key_model: bool = False) -> LLMClient:
        """Return the client for one S1-S5 call.

        Explicit per-S clients win. The key-solver client is a dynamic fallback
        selected by S0's hardest-step prediction.
        """

        explicit = self.subproblem_clients.get(s_id.upper())
        if explicit is not None:
            return explicit
        if use_key_model and self.key_solver_client is not None:
            return self.key_solver_client
        return self.solver_client

    def _complete(
        self,
        client: LLMClient,
        packet: PromptPacket,
        round_index: int,
        s_id: str | None = None,
    ) -> str:
        metadata = dict(self.base_metadata)
        metadata["role"] = packet.role
        metadata["round"] = round_index
        if s_id is not None:
            metadata["s_id"] = s_id
        self._emit(f"[{metadata.get('pipeline', 'main')}] round={round_index} call={packet.role}"
                   + (f" ({s_id})" if s_id else "") + f" model={client.model}")
        response = client.complete(packet, metadata)
        self._emit(
            f"[{metadata.get('pipeline', 'main')}] round={round_index} done={packet.role}"
            + (f" ({s_id})" if s_id else "")
            + f" chars={len(response.text)}"
        )
        return response.text

    def _emit(self, message: str) -> None:
        if self.progress is not None:
            self.progress(message)
