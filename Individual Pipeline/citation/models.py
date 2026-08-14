"""Typed records for the Citation Generator/Verifier gate."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class PromptPacket:
    """Complete prompt payload for one role call."""

    role: str
    system: str
    user: str


@dataclass(frozen=True)
class LLMResponse:
    """Normalized completion payload returned by citation clients."""

    text: str
    model: str


@dataclass(frozen=True)
class CitationGeneratorReport:
    """Controller-facing summary parsed from the Citation Generator output."""

    source_ledger_complete: str
    internet_used: str
    possible_target_source_leakage: str
    unsupported_or_unclear_sources_present: str
    suspicious_standard_background_claims_present: str
    external_sources_checked: str
    recommended_next_step: str
    parse_status: str = "OK"
    missing_fields: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CitationVerifierReport:
    """Controller-facing summary parsed from the Citation Verifier output."""

    citation_gate_result: str
    source_ledger_present: str
    missing_source_entries_present: str
    disallowed_sources_present: str
    overstrengthened_or_misquoted_sources_present: str
    suspicious_standard_background_claims_present: str
    external_source_issue_present: str
    citation_only_repair_needed: str
    substantive_source_issue_present: str
    candidate_guidance_seed: str
    parse_status: str = "OK"
    missing_fields: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CitationGateDecision:
    """Terminal decision for one citation gate run."""

    gate_result: str
    reason: str
    verifier_ran: bool
    candidate_guidance_seed: str | None
    generator_report: CitationGeneratorReport
    verifier_report: CitationVerifierReport | None = None

    def to_dict(self) -> dict:
        return asdict(self)
