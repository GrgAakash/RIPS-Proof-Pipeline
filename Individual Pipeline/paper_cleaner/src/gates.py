"""Automated quality gates (§12). G2 lives inline in step1 (OCR sampling);
the rest are implemented here."""
from __future__ import annotations

import re

from .common import Rejected, RunContext
from .schemas import DepGraph, StatementsIndex


def g1_min_statements(ctx: RunContext, index: StatementsIndex) -> None:
    """G1: require at least one theorem-like result.

    A raw count threshold rejects valid short notes (2607.05330 has one
    theorem and one proposition).  The pipeline needs a proof target, not an
    arbitrary minimum number of environments.  Keep short papers auditable
    with a warning, but reject only when no theorem-like result was parsed.
    """
    theorem_like = [statement for statement in index.statements
                    if statement.env_type in {
                        "theorem", "lemma", "proposition", "corollary"
                    }]
    if not theorem_like:
        raise Rejected("no_formal_statements",
                       f"no theorem-like statements parsed "
                       f"({len(index.statements)} total environments)")
    if len(index.statements) < 5:
        ctx.log_event(event="gate_g1_short_paper",
                      statements=len(index.statements),
                      theorem_like=len(theorem_like), level="warning")


def g4_deps_failed_rate(ctx: RunContext, graph: DepGraph, n_targets: int) -> bool:
    """G4: deps_failed ratio > 0.3 -> do not block, mark summary as degraded."""
    if n_targets == 0:
        return False
    rate = len(graph.deps_failed) / n_targets
    degraded = rate > 0.3
    if degraded:
        ctx.log_event(event="gate_g4_degraded", rate=round(rate, 3))
    return degraded


CMD_RE = re.compile(r"\\([A-Za-z@]+)")


def load_std_commands(ctx: RunContext) -> set[str]:
    p = ctx.data_dir / "latex_std_commands.txt"
    return {ln.strip() for ln in p.read_text(encoding="utf-8").splitlines()
            if ln.strip()}


def g3_macro_residue(ctx: RunContext, problem_md: str, macros_tex: str,
                     flat_source: str) -> tuple[list[str], str]:
    """G3: check each \\cmd in problem.md against the std-command whitelist
    ∪ the names defined in macros.tex.

    Returns (list of unmatched commands, recovered definitions appended to macros.tex).
    The caller decides warning / excluded per route (§12 table).
    """
    std = load_std_commands(ctx)
    defined = set(re.findall(
        r"\\(?:newcommand|renewcommand|providecommand|def|DeclareMathOperator)\*?"
        r"\s*\{?\\([A-Za-z@]+)\}?", macros_tex))
    unknown, appended = [], []
    for cmd in sorted(set(CMD_RE.findall(problem_md))):
        if cmd in std or cmd in defined or len(cmd) == 1:
            continue
        # search the flat.tex preamble once more for the definition
        # (recovers a \def that slipped past collect_macros)
        mo = re.search(
            r"\\(?:newcommand|renewcommand|providecommand|def|DeclareMathOperator)"
            r"\*?\s*\{?\\" + re.escape(cmd) + r"(?![A-Za-z@]).*", flat_source)
        if mo:
            appended.append(mo.group(0))
            defined.add(cmd)
        else:
            unknown.append(cmd)
    return unknown, "\n".join(appended)


def g5_invariants(ctx: RunContext, problem_md: str, proof_tex: str,
                  self_contained: bool, leak_clean: bool) -> None:
    """G5: factory invariant assertions; failure = program bug -> paper failed."""
    assert self_contained and leak_clean, "G5: report flags not clean"
    probe = proof_tex[:200]
    if probe:
        assert probe not in problem_md, "G5: target proof prefix leaked into problem.md"


_WS_RE = re.compile(r"\s+")


def _norm_ws(s: str) -> str:
    return _WS_RE.sub(" ", s).strip()


def g5_leak_scan(problem_md: str, proof_tex: str,
                 allowed_texts: list[str] | tuple = (),
                 min_len: int = 120, stride: int = 20,
                 max_span: int = 1200) -> list[str]:
    """Deterministic full-text leak scan (G5 upgrade over the 200-char probe).

    Slides windows of min_len normalized chars from the target proof over the
    normalized problem.md; a matching window is extended to its maximal shared
    span. A span fully contained in some allowed text (the target statement,
    a granted block's own source text, macros) is legitimate presence, not a
    leak — the same mere-presence principle as the a4b guard. Detection floor:
    overlaps shorter than min_len + stride - 1 normalized chars may be missed.
    Returns the leaked spans (normalized), empty = clean.
    """
    hay = _norm_ws(problem_md)
    needle = _norm_ws(proof_tex)
    if len(needle) < min_len:
        return []
    allowed = [_norm_ws(a) for a in allowed_texts if a and a.strip()]
    spans: list[str] = []
    i, n = 0, len(needle)
    while i + min_len <= n:
        window = needle[i:i + min_len]
        if window in hay:
            j = i + min_len
            while j < min(n, i + max_span) and needle[i:j + 1] in hay:
                j += 1
            frag = needle[i:j]
            # strip boundary whitespace before the containment check: allowed
            # texts are _norm_ws-stripped, so a single shared boundary space
            # (block marker vs next proof word) would defeat coverage and
            # false-flag a granted block's own text (seen on 2510.03923)
            probe = frag.strip()
            if probe and not any(probe in a for a in allowed):
                spans.append(frag)
            i = j
        else:
            i += stride
    return spans


def g6_no_main(ctx: RunContext, mains: list[str]) -> None:
    """G6: fallback ladder exhausted with still no main theorem -> rejected no_main_theorem."""
    if not mains:
        raise Rejected("no_main_theorem", "fallback ladder exhausted")
