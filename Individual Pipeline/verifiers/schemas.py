"""Typed records for the standalone verifier mock pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

TriState = Literal["YES", "NO", "UNCLEAR"]
Agreement = Literal["all_agree", "majority_agree", "no_majority", "unclear"]
DerivedAStatus = Literal["A_VERIFIED", "A_ALMOST", "A_NOT_VERIFIED", "A_INVALID", "A_UNCLEAR"]
PipelineStatus = Literal[
    "SETUP_FAILURE",
    "STOPPED_DISALLOWED_PREMISE",
    "STOPPED_NO_MAJORITY",
    "STOPPED_WEB_CONTAMINATION",
    "STOPPED_GUIDANCE_SEED",
    "STOPPED_AFTER_B",
    "COMPLETED_C_BROKE",
    "COMPLETED_C_CLEAN",
    "COMPLETED_C_CLEAN_LOW_COUPLING",
    "COMPLETED_C_UNSURE",
]


@dataclass(frozen=True, init=False)
class VerifierInput:
    target_theorem: str
    allowed_supporting_statements: str
    guidance_list: list[str]
    proof_artifact: str
    skeleton_ref: str
    run_metadata: dict[str, Any] = field(default_factory=dict)

    def __init__(
        self,
        target_theorem: str = "",
        allowed_supporting_statements: str | None = None,
        guidance_list: list[str] | str | None = None,
        proof_artifact: str | None = None,
        skeleton_ref: str = "",
        run_metadata: dict[str, Any] | None = None,
        *,
        allowed_statements: str | None = None,
        guidance: str | None = None,
        proposed_proof: str | None = None,
    ) -> None:
        if allowed_supporting_statements is None:
            allowed_supporting_statements = allowed_statements or ""
        if proof_artifact is None:
            proof_artifact = proposed_proof or ""
        if guidance_list is None:
            guidance_list = _guidance_to_list(guidance)
        elif isinstance(guidance_list, str):
            guidance_list = _guidance_to_list(guidance_list)

        object.__setattr__(self, "target_theorem", target_theorem)
        object.__setattr__(self, "allowed_supporting_statements", allowed_supporting_statements)
        object.__setattr__(self, "guidance_list", list(guidance_list))
        object.__setattr__(self, "proof_artifact", proof_artifact)
        object.__setattr__(self, "skeleton_ref", skeleton_ref)
        object.__setattr__(self, "run_metadata", dict(run_metadata or {}))

    def missing_fields(self) -> list[str]:
        missing: list[str] = []
        required = {
            "target_theorem": self.target_theorem,
            "allowed_supporting_statements": self.allowed_supporting_statements,
            "proof_artifact": self.proof_artifact,
            "skeleton_ref": self.skeleton_ref,
        }
        for field_name, value in required.items():
            if not str(value).strip():
                missing.append(field_name)
        return missing

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class AReport:
    run_id: str
    skeleton_ref: str
    raw_text: str
    non_fillable_gaps_present: TriState = "UNCLEAR"
    fillable_only_gaps_present: TriState = "UNCLEAR"
    disallowed_premises_present: TriState = "UNCLEAR"
    omitted_case_or_weaker_statement_present: TriState = "UNCLEAR"
    allowed_formal_skeleton_statements_used: str = ""
    disallowed_skeleton_statements_cited: str = ""
    standard_background_heavy: TriState = "UNCLEAR"
    web_source_issue: TriState = "UNCLEAR"
    candidate_guidance_seed: str = "None"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ComposerAReport:
    skeleton_ref: str
    raw_text: str
    non_fillable_gaps_present: TriState = "UNCLEAR"
    fillable_only_gaps_present: TriState = "UNCLEAR"
    disallowed_premises_present: TriState = "UNCLEAR"
    omitted_case_or_weaker_statement_present: TriState = "UNCLEAR"
    allowed_formal_skeleton_statements_used: str = ""
    allowed_formal_skeleton_statements_used_count: int | None = None
    allowed_formal_skeleton_statements_used_list: list[str] = field(default_factory=list)
    disallowed_skeleton_statements_cited: str = ""
    disallowed_skeleton_statements_cited_count: int | None = None
    disallowed_skeleton_statements_cited_list: list[str] = field(default_factory=list)
    standard_background_heavy: TriState = "UNCLEAR"
    web_source_issue: TriState = "UNCLEAR"
    same_issue_recurring_across_reports: TriState = "UNCLEAR"
    candidate_guidance_seed: str = "None"
    implied_status_agreement: Agreement = "unclear"

    def to_dict(self) -> dict:
        data = asdict(self)
        data["agreement"] = self.implied_status_agreement
        return data

    @property
    def agreement(self) -> Agreement:
        return self.implied_status_agreement


@dataclass(frozen=True)
class BReport:
    skeleton_ref: str
    raw_text: str
    weakest_point_found: Literal["yes", "no", "unclear"] = "unclear"
    weakest_point: str = ""
    fillable: Literal["yes", "no", "not applicable", "unclear"] = "unclear"
    weakest_point_location: str = ""
    source_status: str = ""
    missing_claim: str = ""
    disallowed_premise_at_weakest_point: Literal["yes", "no", "not applicable", "unclear"] = "unclear"
    web_source_issue: TriState = "UNCLEAR"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CReport:
    skeleton_ref: str
    raw_text: str
    most_serious_attack: str = ""
    attack_location: str = ""
    source_status: str = ""
    broke: Literal["yes", "no", "unsure", "unclear"] = "unclear"
    failing_step: str = ""
    exact_check_needed: str = ""
    disallowed_premise_at_attacked_point: Literal["yes", "no", "unclear"] = "unclear"
    web_source_issue: TriState = "UNCLEAR"

    def to_dict(self) -> dict:
        return asdict(self)


def _guidance_to_list(value: str | None) -> list[str]:
    if value is None:
        return []
    cleaned = value.strip()
    if not cleaned or cleaned.lower().strip(" .") in {"none", "n/a", "not applicable"}:
        return []
    return [cleaned]


@dataclass(frozen=True)
class PipelineSummary:
    status: PipelineStatus
    skeleton_ref: str
    stopped_stage: str
    derived_a_status: DerivedAStatus = "A_UNCLEAR"
    protocol_action: str | None = None
    protocol_source: str | None = None
    protocol_next_step: str | None = None
    rerun_starts_at: str | None = None
    current_cascade_action: str | None = None
    candidate_guidance_seed: str | None = None
    b_ran: bool = False
    c_ran: bool = False
    missing_inputs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
