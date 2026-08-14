"""Tolerant parsers for the labeled-markdown outputs of the S0-S6 protocol roles.

The fixed prompts in both canonical prompt packets mandate
controller-facing fields, preferably as a fenced YAML block and historically as
labeled markdown fields (``failure_output_type:``, ``Fillable: yes/no``,
``Broke: yes / no / unsure``, Composer A's YES/NO summary lines). Real model
output follows those labels but varies in case, punctuation, emphasis marks,
and whether the value sits on the label line or the following line(s). These
parsers extract fields tolerantly and normalize free-text answers into the
canonical values in :mod:`solver.schemas`.

Design rules:

* Never raise on missing fields -- return the conservative default
  (``unclear`` / ``unparseable``) so the deterministic controller can route
  conservatively instead of crashing mid-pipeline.
* When a label appears more than once (e.g. once in a body section and once in
  the final summary), the LAST occurrence wins: every role prompt puts its
  controller-facing summary at the end.
"""

from __future__ import annotations

import re
import textwrap

from solver.io_utils import parse_json_object
from solver.s6_artifacts import split_s6_output
from solver.schemas import (
    BRANCH_LEMMA,
    BranchLemmaCandidate,
    ComposedProofResult,
    ComposerAGoldReport,
    FORBIDDEN_ROUTE,
    FinalCheckerDecision,
    NO,
    NO_USEFUL_GUIDANCE,
    NOT_APPLICABLE,
    ORDINARY_HINT,
    ProblemStatementReport,
    SOLVED,
    SolverFailureOutput,
    SubproblemResult,
    UNCLEAR,
    UNPARSEABLE,
    VerifierBReport,
    VerifierCReport,
    YES,
)


# Protocol sentinel strings (matched case-insensitively).
SETUP_FAILURE_MARKER = "setup failure"
SUBPROBLEM_UNSOLVED_MARKER = "subproblem unsolved"
FINAL_PROOF_NOT_COMPLETED_MARKER = "final proof not completed"
TARGET_SOURCE_LEAKAGE_MARKER = "possible target-source leakage encountered"

_INCOMPLETE_FINAL_PROOF_MARKERS = (
    FINAL_PROOF_NOT_COMPLETED_MARKER,
    "proof attempt (partial",
    "proof cannot be completed",
    "argument cannot be completed",
    "proof is not completed",
    "proof is not complete",
    "cannot be completed from the current packet",
    "blocks at the hardest step",
    "blocked at the",
)

# A line "looks like a label" when, after cleanup, it is short and ends with a
# colon or question mark without an intervening sentence. Used to terminate
# multi-line field values.
_LABEL_LINE_RE = re.compile(r"^[A-Za-z\[][^:?]{0,88}[:?]\s*$")
# Section starts also terminate multi-line values.
_SECTION_LINE_RE = re.compile(r"^(?:#{1,6}\s|\d{1,2}\.\s|[-=]{4,}\s*$|---\s)")
_YAML_FENCE_RE = re.compile(
    r"^[ \t]*```(?:yaml|yml)[ \t]*\r?\n(.*?)^[ \t]*```[ \t]*$",
    re.IGNORECASE | re.DOTALL | re.MULTILINE,
)
_YAML_SCALAR_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_ -]*):(?:\s*(.*))?$")


def _clean_line(raw: str) -> str:
    """Strip list markers, heading hashes, and bold/emphasis from one line."""

    line = raw.strip()
    line = line.lstrip("#>*-• \t")
    line = line.replace("**", "").replace("__", "")
    return line.strip()


def _value_after_label(clean: str, prefix: str) -> str:
    """Given a cleaned line that starts with ``prefix``, return the value part.

    The value is whatever follows the first ``:`` or ``?`` after the prefix
    (label tails such as "... than the target theorem?" are skipped). When no
    punctuation follows, the remainder itself is the value.
    """

    rest = clean[len(prefix):]
    match = re.search(r"[:?]", rest)
    if match:
        return rest[match.end():].strip()
    return rest.strip()


def extract_field(text: str, *prefixes: str) -> str | None:
    """Extract the last occurrence of a labeled field from markdown output.

    ``prefixes`` are case-insensitive label beginnings (e.g. ``"fillable"``,
    ``"does the candidate lemma appear to be weaker"``). If the label line has
    no inline value, subsequent lines are collected until the next label-like
    line or section start. Returns ``None`` when no prefix matches anywhere.
    """

    lines = text.splitlines()
    lowered_prefixes = tuple(prefix.lower().replace("_", " ") for prefix in prefixes)
    best: str | None = None
    for index, raw in enumerate(lines):
        clean = _clean_line(raw)
        lower = clean.lower().replace("_", " ")
        for prefix in lowered_prefixes:
            if not lower.startswith(prefix):
                continue
            value = _value_after_label(clean, prefix)
            if not value:
                value = _collect_following_lines(lines, index + 1)
            best = value
            break
    return best


def _collect_following_lines(lines: list[str], start: int) -> str:
    """Collect a field value that begins on the line(s) after its label."""

    collected: list[str] = []
    for raw in lines[start:]:
        clean = _clean_line(raw)
        if collected and not clean:
            break
        if not clean:
            continue
        if _LABEL_LINE_RE.match(clean) or _SECTION_LINE_RE.match(raw.strip()):
            break
        collected.append(clean)
    return "\n".join(collected).strip()


def _none_to_empty(value: str | None) -> str:
    """Map missing values and the literal answers None / N/A to ''."""

    if value is None:
        return ""
    stripped = value.strip().strip(".")
    if stripped.lower() in {"none", "null", "~", "n/a", "na", "not applicable", ""}:
        return ""
    return value.strip()


def _normalize_yaml_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", key.strip().lower()).strip("_")


def _clean_yaml_scalar(value: str) -> str:
    value = value.strip()
    if value.lower() in {"null", "none", "~"}:
        return ""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _parse_yaml_scalar_map(block: str) -> dict[str, str]:
    """Parse the scalar-only YAML maps required by solver summaries."""

    data: dict[str, str] = {}
    lines = block.splitlines()
    index = 0
    while index < len(lines):
        raw = lines[index]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#") or raw[:1].isspace():
            index += 1
            continue
        match = _YAML_SCALAR_RE.match(raw)
        if match is None:
            index += 1
            continue
        key = _normalize_yaml_key(match.group(1))
        value = (match.group(2) or "").strip()
        if value in {"|", ">"}:
            folded = value == ">"
            collected: list[str] = []
            index += 1
            while index < len(lines):
                next_raw = lines[index]
                if next_raw and not next_raw[:1].isspace() and _YAML_SCALAR_RE.match(next_raw):
                    break
                next_stripped = next_raw.strip()
                if next_stripped and not next_stripped.startswith("#"):
                    collected.append(next_stripped)
                index += 1
            data[key] = (" ".join(collected) if folded else "\n".join(collected)).strip()
            continue
        data[key] = _clean_yaml_scalar(value)
        index += 1
    return data


def extract_yaml_summary(text: str) -> dict[str, str]:
    """Return the last fenced YAML block containing ``failure_output_type``."""

    for match in reversed(list(_YAML_FENCE_RE.finditer(text))):
        data = _parse_yaml_scalar_map(textwrap.dedent(match.group(1)))
        if "failure_output_type" in data:
            return data
    return {}


def _summary_or_field(
    summary: dict[str, str],
    text: str,
    summary_keys: tuple[str, ...],
    *prefixes: str,
) -> str | None:
    for key in summary_keys:
        normalized = _normalize_yaml_key(key)
        if normalized in summary:
            return summary[normalized]
    return extract_field(text, *prefixes)


def normalize_tristate(value: str | None) -> str:
    """Normalize a YES / NO / UNCLEAR style answer."""

    if value is None:
        return UNCLEAR
    lower = value.strip().lower()
    if lower.startswith(("not applicable", "n/a", "na ")) or lower in {"na", "n/a"}:
        return NOT_APPLICABLE
    if lower.startswith("yes"):
        return YES
    if lower.startswith(("unclear", "unsure", "unknown")):
        return UNCLEAR
    if lower.startswith(("no", "none")):
        return NO
    return UNCLEAR


def normalize_broke(value: str | None) -> str:
    """Normalize Verifier C's ``Broke: yes / no / unsure`` answer."""

    if value is None:
        return UNCLEAR
    lower = value.strip().lower()
    if lower.startswith("yes"):
        return "yes"
    if lower.startswith("unsure"):
        return "unsure"
    if lower.startswith("no"):
        return "no"
    return UNCLEAR


def normalize_failure_type(value: str | None) -> str:
    """Normalize a ``failure_output_type`` answer to the canonical constants."""

    if value is None:
        return UNPARSEABLE
    lower = value.strip().lower()
    if not lower:
        return UNPARSEABLE
    lower = lower.replace("**", "").replace("__", "").replace("`", "")
    lower = re.sub(r"[_-]+", " ", lower)
    lower = re.sub(r"\s+", " ", lower).strip(" .;:")
    categories = sum(
        1
        for present in (
            "forbidden" in lower or "obstruction guidance" in lower,
            "branch" in lower or "lemma target" in lower,
            "ordinary hint" in lower,
            "no useful" in lower or "not found" in lower,
        )
        if present
    )
    if "|" in lower or categories >= 2:
        return UNPARSEABLE
    if lower == "solved":
        return SOLVED
    if "forbidden" in lower or "obstruction guidance" in lower:
        return FORBIDDEN_ROUTE
    if "branch" in lower or "lemma target" in lower:
        return BRANCH_LEMMA
    if "ordinary hint" in lower or lower == "hint":
        return ORDINARY_HINT
    if "no useful" in lower or "not found" in lower or lower.startswith("none"):
        return NO_USEFUL_GUIDANCE
    return UNPARSEABLE


def has_setup_failure(text: str) -> bool:
    """Detect the protocol's 'SETUP FAILURE: missing input.' sentinel."""

    return SETUP_FAILURE_MARKER in text.lower()


def has_leakage_marker(text: str) -> bool:
    """Detect the 'Possible target-source leakage encountered.' sentinel."""

    return TARGET_SOURCE_LEAKAGE_MARKER in text.lower()


def has_incomplete_final_proof_marker(text: str) -> bool:
    """Detect S6 outputs that explicitly say the final proof is incomplete."""

    lower = text.lower()
    return any(marker in lower for marker in _INCOMPLETE_FINAL_PROOF_MARKERS)


# ---------------------------------------------------------------------------
# Solver outputs (S1-S5 and S6)
# ---------------------------------------------------------------------------


def parse_branch_lemma(text: str, summary: dict[str, str] | None = None) -> BranchLemmaCandidate:
    """Parse the branch-lemma fields of a solver failure output."""

    summary = summary or {}
    return BranchLemmaCandidate(
        lemma_statement=_none_to_empty(_summary_or_field(
            summary, text, ("candidate_lemma_statement", "lemma_statement"), "candidate lemma statement"
        )),
        why_unblocks=_none_to_empty(_summary_or_field(
            summary, text, ("why_unblocks",), "why this lemma would unblock"
        )),
        where_used=_none_to_empty(_summary_or_field(
            summary, text, ("where_used",), "exact place where the main proof would use it"
        )),
        allowed_inputs=_none_to_empty(_summary_or_field(
            summary, text, ("allowed_inputs",), "allowed inputs for the auxiliary lemma"
        )),
        dependencies=_none_to_empty(_summary_or_field(
            summary, text, ("dependencies",), "dependencies from the skeleton"
        )),
        weaker_than_target=normalize_tristate(
            _summary_or_field(summary, text, ("weaker_than_target",), "does the candidate lemma appear to be weaker")
        ),
        equivalent_or_stronger=normalize_tristate(
            _summary_or_field(
                summary, text, ("equivalent_or_stronger", "lemma_equivalent_or_stronger"),
                "does the candidate lemma appear equivalent"
            )
        ),
        recommended=normalize_tristate(_summary_or_field(
            summary, text, ("recommended", "lemma_recommended"), "recommended mini-pipeline target"
        )),
    )


def parse_solver_failure_output(text: str, source: str) -> SolverFailureOutput:
    """Parse section 3 (failure output and candidate guidance) of S1-S5 / S6."""

    summary = extract_yaml_summary(text)
    raw_failure_type = _summary_or_field(
        summary, text, ("failure_output_type",), "failure_output_type"
    )
    failure_type = normalize_failure_type(raw_failure_type)
    if failure_type == UNPARSEABLE:
        # Legacy fallback applies only when the field is absent. An explicit
        # malformed value (especially a copied menu) remains unparseable.
        if raw_failure_type is None and not (
            SUBPROBLEM_UNSOLVED_MARKER in text.lower()
            or FINAL_PROOF_NOT_COMPLETED_MARKER in text.lower()
        ):
            failure_type = SOLVED
    if failure_type == SOLVED:
        return SolverFailureOutput(source=source, failure_output_type=SOLVED)
    branch = parse_branch_lemma(text, summary) if failure_type == BRANCH_LEMMA else None
    return SolverFailureOutput(
        source=source,
        failure_output_type=failure_type,
        type_detail=_none_to_empty(_summary_or_field(summary, text, ("type",), "type")),
        failed_route=_none_to_empty(_summary_or_field(
            summary, text, ("failed_route",), "failed route or missing step"
        )),
        obstruction=_none_to_empty(_summary_or_field(
            summary, text, ("obstruction",), "obstruction or missing idea"
        )),
        evidence=_none_to_empty(_summary_or_field(summary, text, ("evidence",), "evidence")),
        reuse_value=_none_to_empty(_summary_or_field(
            summary, text, ("reuse_value",), "reuse value"
        )),
        guidance_sentence=_none_to_empty(_summary_or_field(
            summary, text, ("guidance_sentence",), "guidance sentence"
        )),
        branch_lemma=branch,
    )


def parse_subproblem_output(text: str, s_id: str) -> SubproblemResult:
    """Parse one S1-S5 output into a typed result."""

    setup_failure = has_setup_failure(text)
    failure = parse_solver_failure_output(text, s_id)
    unsolved_marker = SUBPROBLEM_UNSOLVED_MARKER in text.lower()
    # A stray 'solved' classification cannot override the explicit protocol
    # marker; trust SUBPROBLEM UNSOLVED when both appear.
    solved = failure.failure_output_type == SOLVED and not unsolved_marker and not setup_failure
    if not solved and failure.failure_output_type == SOLVED:
        failure = SolverFailureOutput(source=s_id, failure_output_type=UNPARSEABLE)
    return SubproblemResult(s_id=s_id, solved=solved, failure=failure, setup_failure=setup_failure)


def extract_final_proof(text: str) -> str:
    """Extract S6's final-proof body, falling back to full text.

    This delegates to the same marker/heading splitter used to write
    ``final_proof.md`` so verifier/final-checker prompts and file artifacts see
    the same candidate proof section.
    """

    return split_s6_output(text).final_proof


def parse_composer_output(text: str) -> ComposedProofResult:
    """Parse one S6 output into a typed composed-proof result."""

    setup_failure = has_setup_failure(text)
    failure = parse_solver_failure_output(text, "S6")
    incomplete_marker = has_incomplete_final_proof_marker(text)
    complete = failure.failure_output_type == SOLVED and not incomplete_marker and not setup_failure
    if not complete and failure.failure_output_type == SOLVED:
        failure = SolverFailureOutput(source="S6", failure_output_type=UNPARSEABLE)
    return ComposedProofResult(
        complete=complete,
        proof_text=extract_final_proof(text) if complete else "",
        failure=None if complete else failure,
        setup_failure=setup_failure,
    )


# ---------------------------------------------------------------------------
# S0 blueprint: subproblem assignment table
# ---------------------------------------------------------------------------

_ASSIGNMENT_SECTION_RE = re.compile(r"(?mi)^#{0,6}\s*(?:6\.\s*)?Subproblem assignment table\s*$")
_ASSIGNMENT_END_RE = re.compile(r"(?m)^#{0,6}\s*(?:7\.\s|Web-source confirmation)")
_S_LABEL_RE = re.compile(r"(?m)^\s*(?:\*\*)?(S[1-5])(?:\*\*)?\s*:\s*")
_SOLVER_ID_RE = re.compile(r"\b(S[1-5])\b", re.IGNORECASE)


def parse_s0_assignments(text: str) -> dict[str, str]:
    """Extract the S1-S5 assignment texts from an S0 blueprint.

    Returns a possibly-partial mapping; the orchestrator substitutes a generic
    pointer to the blueprint for any missing assignment rather than failing the
    round.
    """

    section = text
    heading = _ASSIGNMENT_SECTION_RE.search(text)
    if heading is not None:
        end = _ASSIGNMENT_END_RE.search(text, heading.end())
        section = text[heading.end(): end.start() if end else len(text)]
    assignments: dict[str, str] = {}
    matches = list(_S_LABEL_RE.finditer(section))
    for index, match in enumerate(matches):
        s_id = match.group(1)
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(section)
        body = section[start:end].strip()
        if body and s_id not in assignments:
            assignments[s_id] = body
    return assignments


def parse_s0_key_solver(text: str) -> str | None:
    """Return S0's explicit key-solver designation, if present."""

    value = extract_field(text, "key_solver_id") or ""
    solver_ids = {match.upper() for match in _SOLVER_ID_RE.findall(value)}
    if len(solver_ids) != 1:
        return None
    return solver_ids.pop()


def parse_s0_hardest_solver(text: str) -> str | None:
    """Infer which S1-S5 solver owns S0's hardest predicted step.

    The no-internet prompt asks S0 to emit ``key_solver_id`` explicitly. Older
    and internet-enabled blueprints use ``hardest_step_id`` plus support-graph
    ``suggested_solver`` fields. This parser retains those forms as fallbacks.
    """

    solver = parse_s0_key_solver(text)
    if solver is not None:
        return solver

    for label in ("hardest_step_id", "hardest_step_description"):
        value = extract_field(text, label)
        solver = _first_solver_id(value or "")
        if solver is not None:
            return solver

    hardest = extract_field(text, "hardest_step_id")
    if not hardest:
        return None
    step_id_match = re.search(r"\b[A-Za-z][A-Za-z0-9_-]*\b", hardest)
    if step_id_match is None:
        return None
    step_id = step_id_match.group(0)

    solver = _solver_from_subclaim_block(text, step_id)
    if solver is not None:
        return solver

    for s_id, assignment in parse_s0_assignments(text).items():
        if re.search(rf"(?<![A-Za-z0-9_-]){re.escape(step_id)}(?![A-Za-z0-9_-])", assignment):
            return s_id
    return None


def _first_solver_id(text: str) -> str | None:
    match = _SOLVER_ID_RE.search(text)
    return match.group(1).upper() if match else None


def _solver_from_subclaim_block(text: str, step_id: str) -> str | None:
    pattern = re.compile(
        rf"(?mis)^\s*id\s*:\s*{re.escape(step_id)}\b(?P<body>.*?)(?=^\s*id\s*:|^\s*\d+\.\s|\Z)"
    )
    match = pattern.search(text)
    if match is None:
        return None
    body = match.group("body")
    solver = extract_field(body, "suggested_solver", "suggested solver")
    return _first_solver_id(solver or body)


# ---------------------------------------------------------------------------
# Verifier layer reports
# ---------------------------------------------------------------------------


def parse_problem_statement_report(text: str) -> ProblemStatementReport:
    """Parse the exact-target alignment gate's controller-facing summary."""

    return ProblemStatementReport(
        artifact_role=_none_to_empty(extract_field(text, "artifact role checked")),
        problem_statement_match=normalize_tristate(
            extract_field(text, "problem statement match")
        ),
        actual_statement=_none_to_empty(extract_field(text, "actual statement addressed")),
        mismatch_type=_none_to_empty(extract_field(text, "mismatch type, if any")),
        recommended_action=_none_to_empty(
            extract_field(text, "recommended controller action")
        ),
    )


def parse_composer_a_report(text: str) -> ComposerAGoldReport:
    """Parse Composer A's gold evidence report summary fields."""

    return ComposerAGoldReport(
        non_fillable_gaps=normalize_tristate(extract_field(text, "non-fillable gaps present")),
        fillable_only_gaps=normalize_tristate(extract_field(text, "fillable-only gaps present")),
        disallowed_premises=normalize_tristate(extract_field(text, "disallowed premises present")),
        omitted_case_or_weaker=normalize_tristate(extract_field(text, "omitted case")),
        standard_background_heavy=normalize_tristate(extract_field(text, "standard-background-heavy")),
        web_source_issue=normalize_tristate(extract_field(text, "web-source issue")),
        recurring_issue=normalize_tristate(extract_field(text, "same issue recurring")),
        no_majority="no majority" in text.lower(),
        guidance_seed=_none_to_empty(extract_field(text, "candidate guidance seed")),
    )


def parse_verifier_b_report(text: str) -> VerifierBReport:
    """Parse Verifier B's final summary (weakest point + fillability)."""

    return VerifierBReport(
        weakest_point_found=normalize_tristate(extract_field(text, "weakest point found")),
        weakest_point=_none_to_empty(extract_field(text, "weakest point (")),
        missing_claim=_none_to_empty(extract_field(text, "missing claim")),
        fillable=normalize_tristate(extract_field(text, "fillable")),
        disallowed_premise=normalize_tristate(
            extract_field(text, "disallowed premise at the weakest point")
        ),
    )


def parse_verifier_c_report(text: str) -> VerifierCReport:
    """Parse Verifier C's final summary (adversarial break test)."""

    return VerifierCReport(
        attack=_none_to_empty(extract_field(text, "most serious attack")),
        broke=normalize_broke(extract_field(text, "broke")),
        failing_step=_none_to_empty(extract_field(text, "if broke, the false claim or failing step")),
        check_needed=_none_to_empty(extract_field(text, "if unsure, exact check needed")),
        disallowed_premise=normalize_tristate(
            extract_field(text, "disallowed premise at the attacked point")
        ),
    )


def parse_final_checker_output(text: str) -> FinalCheckerDecision:
    """Parse the Final Checker's strict-JSON verdict (tolerating fences/prose)."""

    return FinalCheckerDecision.from_dict(parse_json_object(text, "Final Checker"))
