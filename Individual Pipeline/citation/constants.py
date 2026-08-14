"""Constants for the Citation Generator/Verifier gate."""

YES_NO_UNCLEAR = {"YES", "NO", "UNCLEAR"}
GENERATOR_NEXT_STEPS = {
    "PROCEED_TO_CITATION_VERIFIER",
    "MANUAL_REVIEW_FOR_LEAKAGE",
    "SOURCE_LEDGER_REPAIR_NEEDED",
    "UNCLEAR",
}
CITATION_GATE_RESULTS = {
    "GOOD_TO_GO",
    "SOURCE_LEDGER_REPAIR_NEEDED",
    "BLOCKING_SOURCE_ISSUE",
    "LEAKAGE_RISK",
    "UNCLEAR",
}
CITATION_INTERNET_ENABLED_ROLES = frozenset({"citation_generator", "citation_verifier"})
FORBIDDEN_PUBLIC_FRAGMENTS = (
    "/private/",
    "\\private\\",
    "private/gold",
    "private\\gold",
    "PRIVATE GOLD",
    "SOURCE_PROOF_SENTINEL",
)
DEFAULT_ALLOWED_SUPPORTING_STATEMENTS = """Definitions, notation, and assumptions needed to state or parse the target theorem are allowed.
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
