"""All pydantic models, corresponding one-to-one with plan §3.

Two kinds of models:
- Data-file models (the schema for JSON on disk) -- plain pydantic, defaults allowed;
- LLM output models (used with response_format) -- must satisfy the OpenAI Structured
  Outputs constraints: extra="forbid" (-> additionalProperties:false) and all fields required.
  Hence LLM models set no defaults and avoid dict[str, X] (strict mode does
  not support arbitrary keys).
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------- Data-file models

class Meta(BaseModel):
    paper_id: str
    title: str = ""
    paper_date: str = ""
    primary_category: str = ""
    categories: list[str] = Field(default_factory=list)   # primary + secondary categories (cross-list)
    field_baseline: str = ""
    source_type: Literal["latex", "ocr"] = "latex"


class GlobalItem(BaseModel):
    id: str
    kind: Literal["notation", "standing-assumption"]
    scope: str = "paper"  # paper | section:<n>
    text_tex: str
    added_by: Literal["parser", "agent0", "agent4-patch"] = "parser"


ENV_TYPES = (
    "theorem", "lemma", "proposition", "corollary", "definition",
    "inline-definition", "assumption", "remark", "example", "equation",
)


class Statement(BaseModel):
    id: str
    env_type: str
    latex_label: str = ""
    display_name: str = ""
    section: str = ""
    order_index: int = 0
    statement_tex: str
    statement_sha256: str = ""
    source_file: str = ""
    source_start: int = -1
    source_end: int = -1
    source_sha256: str = ""
    source_verified: bool = False
    proof_tex: Optional[str] = None
    proof_location: str = "omitted"  # inline | appendix:<X> | omitted | external
    proof_sha256: str = ""
    proof_source_file: str = ""
    proof_source_start: int = -1
    proof_source_end: int = -1
    proof_source_sha256: str = ""
    proof_source_verified: bool = False
    proof_pairing: str = ""
    mechanical_refs: list[str] = Field(default_factory=list)
    uses_figure: bool = False
    added_by: Literal["parser", "agent0", "agent4-patch"] = "parser"


class Citation(BaseModel):
    key: str
    raw_bib: str


class StatementsIndex(BaseModel):
    schema_version: Literal[2]
    paper_id: str
    macros_tex: str = ""
    global_context: list[GlobalItem] = Field(default_factory=list)
    statements: list[Statement] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)

    def by_id(self) -> dict[str, Statement]:
        return {s.id: s for s in self.statements}

    def gc_by_id(self) -> dict[str, GlobalItem]:
        return {g.id: g for g in self.global_context}


class Edge(BaseModel):
    from_: str = Field(alias="from")
    to: str
    arises_in: Literal["statement", "proof"]
    kind: Literal["explicit", "implicit-definition", "implicit-result", "standing"]
    evidence: str = ""
    confidence: Literal["high", "medium", "low"] = "high"
    source: Literal["parser", "agent1", "agent4-patch"] = "parser"

    model_config = ConfigDict(populate_by_name=True)


class ExternalDep(BaseModel):
    used_by: str
    citation_key: str = ""
    usage_quote: str = ""
    stated_in_paper: bool = False
    statement_tex: str = ""
    statement_origin: str = ""  # verbatim-from-paper | usage-quote | llm-agreed


class DroppedEdge(BaseModel):
    edge: Edge
    reason: str  # forward | cycle


class DepGraph(BaseModel):
    edges: list[Edge] = Field(default_factory=list)
    external_deps: list[ExternalDep] = Field(default_factory=list)
    deps_failed: list[str] = Field(default_factory=list)


class SignalSet(BaseModel):
    S1: bool = False
    S2: bool = False
    S3: bool = False
    S4: bool = False
    S5: bool = False
    S6: bool = False
    used_by: int = 0
    closure: int = 0
    chain: int = 0
    proof_len: int = 0


class Nominee(BaseModel):
    id: str
    why: str = ""


class RejectedTarget(BaseModel):
    id: str
    reason: Literal["not_nominated", "no_confirming_signal", "over_cap"]


class Selection(BaseModel):
    mains: list[str] = Field(default_factory=list)
    hardest: list[str] = Field(default_factory=list)      # hardest theorems (may overlap with mains)
    difficulty: dict[str, int] = Field(default_factory=dict)  # difficulty scores for all eligible
    selector: Literal["consensus", "fallback-1", "fallback-2", "fallback-3"] = "consensus"
    signals: dict[str, SignalSet] = Field(default_factory=dict)
    llm_nominees: list[Nominee] = Field(default_factory=list)
    rejected: list[RejectedTarget] = Field(default_factory=list)
    backfilled: list[str] = Field(default_factory=list)   # the portion backfilled by min_main_theorems


class RoleEntry(BaseModel):
    role: str = "unknown"
    signals: list[str] = Field(default_factory=list)
    rationale: str = ""


class Roles(BaseModel):
    roles: dict[str, RoleEntry] = Field(default_factory=dict)
    storyline: str = ""
    anomalies: list[str] = Field(default_factory=list)


class ClosureSize(BaseModel):
    definitions: int = 0
    results: int = 0
    external: int = 0


class Report(BaseModel):
    target_id: str
    policy: str
    iterations: int = 0
    self_contained: bool = False
    leak_clean: bool = False
    gaps_history: list[list[str]] = Field(default_factory=list)
    removed_blocks: list[str] = Field(default_factory=list)
    policy_downgraded: bool = False
    sufficiency: Optional[bool] = None
    baseline_assumed: list[str] = Field(default_factory=list)
    closure_size: ClosureSize = Field(default_factory=ClosureSize)
    input_hashes: dict[str, str] = Field(default_factory=dict)


class PkgEntry(BaseModel):
    target_id: str
    env_type: str
    role: str = "unknown"
    selected_as: str = "main"   # main | hardest | main+hardest
    policy: str
    path: str
    topo_rank: int = 0
    proof_chars: int = 0
    self_contained: bool = True
    leak_clean: bool = True


class Manifest(BaseModel):
    paper_id: str
    paper_date: str = ""
    pipeline_version: str = "2.3"
    packages: list[PkgEntry] = Field(default_factory=list)
    stats: dict[str, int] = Field(default_factory=dict)


EXCLUDED_REASONS = (
    "no_proof_in_paper", "proof_too_short", "uses_figure", "deps_failed",
    "target_source_unverified", "proof_source_unverified",
    "target_integrity_failed",
    "external_dep_unstatable", "self_containment_unresolvable",
    "sufficiency_unresolvable", "leak_in_required_context",
    "package_build_error", "leak_scan_overlap",
)


class ExcludedEntry(BaseModel):
    target_id: str
    policy: str = ""
    reason_code: str
    detail: str = ""


# ------------------------------------------------------------- LLM output models
# All extra="forbid" + no defaults (strict mode requires every field).
# NOTE: keep these models free of docstrings and Field descriptions — pydantic
# embeds both in the JSON schema that ships with every API request, so adding
# one silently changes the prompts.

class _LLM(BaseModel):
    model_config = ConfigDict(extra="forbid")


class A0NewStatement(_LLM):
    env_type: str
    kind: str
    scope: str
    text_tex: str
    after_text: str


class A0ProofLink(_LLM):
    proof_first_30_chars: str
    belongs_to_hint: str


class A0Out(_LLM):
    new_statements: list[A0NewStatement]
    proof_links: list[A0ProofLink]


class A1Dep(_LLM):
    id: str
    evidence: str
    confidence: Literal["high", "medium", "low"]


class A1ProofDep(_LLM):
    id: str
    kind: Literal["explicit", "implicit-definition", "implicit-result", "standing"]
    evidence: str
    confidence: Literal["high", "medium", "low"]


class A1ExternalDep(_LLM):
    citation_key: str
    usage_quote: str
    stated_in_paper: bool
    statement_tex: str


class A1Unresolved(_LLM):
    phrase: str
    note: str


class A1Out(_LLM):
    target_id: str
    statement_deps: list[A1Dep]
    proof_deps: list[A1ProofDep]
    external_deps: list[A1ExternalDep]
    unresolved: list[A1Unresolved]


class A2Main(_LLM):
    id: str
    why: str


class A2Role(_LLM):
    id: str
    role: Literal["main-result", "key-proposition", "technical-lemma",
                  "corollary", "remark-level"]
    signals: list[str]
    rationale: str


class A2Out(_LLM):
    main_results: list[A2Main]
    hardest: list[str]           # ids of the technically hardest-to-prove results (2-3)
    roles: list[A2Role]
    storyline: str
    anomalies: list[str]


class A3ExtOut(_LLM):
    statement: str


class A3CmpOut(_LLM):
    equivalent: bool


class A4aGap(_LLM):
    kind: Literal["symbol", "term", "result", "ambiguity"]
    text: str
    where: str


class A4aOut(_LLM):
    gaps: list[A4aGap]
    self_contained: bool


class A4bLeak(_LLM):
    quote: str
    why: str
    severity: Literal["fatal", "hint", "mild"]


class A4bOut(_LLM):
    leaks: list[A4bLeak]
    clean: bool


class A4cMissing(_LLM):
    invoked_as: str
    kind: Literal["result", "definition", "assumption"]


class A4cOut(_LLM):
    missing: list[A4cMissing]
    sufficient: bool


class A5Out(_LLM):
    markdown: str                # body of the English selection-rationale document (markdown)


class A6Fix(_LLM):
    item: str                    # the unresolved gap text (echoed)
    action: Literal["quote", "synthesized", "unfixable"]
    kind: Literal["notation", "definition", "assumption", "result"]
    text_tex: str                # verbatim passage / synthesized statement
    note: str


class A6Out(_LLM):
    fixes: list[A6Fix]


class A7Item(_LLM):
    item: str                    # the blocking item text (echoed)
    verdict: Literal["resolved_in_file", "grant_from_paper", "uphold"]
    evidence: str                # quote from the problem file / the paper
    fix_kind: Literal["notation", "definition", "assumption", "result"]
    fix_text_tex: str            # verbatim paper passage for grant_from_paper
    note: str


class A7Out(_LLM):
    items: list[A7Item]


# --- audit.py (independent-model calibration audit; not part of the pipeline)

class AuditIssue(_LLM):
    kind: Literal["undefined-symbol", "undefined-term", "missing-result",
                  "leak", "other"]
    quote: str
    explanation: str
    severity: Literal["fatal", "minor"]


class AuditPkgOut(_LLM):
    issues: list[AuditIssue]
    self_contained: bool
    leak_free: bool
    sufficient: bool
    confidence: Literal["high", "medium", "low"]
    summary: str


class AuditExclOut(_LLM):
    exclusion_justified: bool
    paper_resolves_it: bool
    where_in_paper: str
    verdict: str
    confidence: Literal["high", "medium", "low"]


TASK_SCHEMAS = {
    "a0": A0Out, "a1": A1Out, "a2": A2Out, "a3_ext": A3ExtOut,
    "a3_cmp": A3CmpOut, "a4a": A4aOut, "a4b": A4bOut, "a4c": A4cOut,
    "a5": A5Out, "a6": A6Out, "a7": A7Out,
    "audit_pkg": AuditPkgOut, "audit_excl": AuditExclOut,
}
