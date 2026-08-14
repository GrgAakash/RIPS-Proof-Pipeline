"""Step 7: verification loop (§10, LLM = Agent 4 x3 checks).

For each draft package: a4c sufficiency (dep-closure/minimal only) -> a4a
self-contained -> a4b leak; deterministic edge-patch for gap/missing
(§10.3/§10.6), leak block drop (§10.5), reassembly after edge-patch;
ship on convergence, otherwise excluded. Aggregate into manifest.json.
"""
from __future__ import annotations

import asyncio
import re

from .common import RunContext, sha256_text
from .gates import g5_invariants, g5_leak_scan
from .llm import call_llm, run_async
from .common import TaskFailed
from .schemas import (A4aGap, A4cMissing, A6Fix, DepGraph, Edge, ExternalDep,
                      GlobalItem, Manifest, Meta, PkgEntry, Report,
                      ClosureSize, Roles, Selection, Statement,
                      StatementsIndex)
from .step3_fill_index import targeted_fill
from .step6_package import PackageExcluded, build_package
from .target_integrity import (frozen_target_artifact_issues,
                               proof_source_issues,
                               statement_source_issues,
                               target_identity_issues)

STEP = "step7"

BLOCK_B_RE = re.compile(r"<!-- b:([^ ]+) -->")


def _norm_ws(s: str) -> str:
    # Curly-quote folding: LLM output often smartens ASCII quotes into curly
    # ones; fold both sides before any comparison or substring search
    s = (s.replace("’", "'").replace("‘", "'")
          .replace("“", '"').replace("”", '"'))
    return re.sub(r"\s+", " ", s).strip()


def _authoritative_text(index: StatementsIndex, bid: str) -> str | None:
    """Authoritative source text (statement / gc) for the entry at block id; ext blocks return None (conservative)."""
    s = index.by_id().get(bid)
    if s is not None:
        return s.statement_tex
    g = index.gc_by_id().get(bid)
    if g is not None:
        return g.text_tex
    return None


class _Unrepairable(Exception):
    def __init__(self, reason_code: str, detail: str = ""):
        self.reason_code = reason_code
        self.detail = detail


SEC3_RE = re.compile(r"## 3\. Known external results.*?(?=\n## \d)", re.DOTALL)


def ship_leak_spans(index: StatementsIndex, graph: DepGraph,
                    target: Statement, problem_md: str,
                    assembly: dict) -> list[str]:
    """Deterministic pre-ship leak scan (G5 upgrade).

    Full problem.md vs the whole target proof at the default floor; the
    external-grants section additionally at a 50-char floor — a verbatim proof
    span inside a grant is the usage-quote leak class the calibration audit
    caught (grants quoting "Thus Sion's minimax theorem applies..." straight
    from the target's proof). Granted blocks' own source texts are legitimate
    presence, EXCEPT usage-quote grants: their text IS a proof sentence, so
    they never whitelist anything.
    """
    stmt_grade = [x.statement_tex for x in graph.external_deps
                  if x.statement_origin != "usage-quote"]
    allowed = [target.statement_tex, index.macros_tex] + stmt_grade
    allowed += [_authoritative_text(index, bid) or "" for bid in
                (assembly.get("defs", []) + assembly.get("res", [])
                 + assembly.get("gcs", []))]
    spans = g5_leak_scan(problem_md, target.proof_tex or "", allowed)
    m = SEC3_RE.search(problem_md)
    if m:
        spans += g5_leak_spans_dedup(
            g5_leak_scan(m.group(0), target.proof_tex or "", stmt_grade,
                         min_len=50, stride=10), spans)
    return spans


def g5_leak_spans_dedup(new: list[str], seen: list[str]) -> list[str]:
    return [s for s in new if not any(s in t or t in s for t in seen)]


# ------------------------------------------------------- §10.3 gap -> edge-patch

def _find_block_of(problem_md: str, quote: str) -> str | None:
    """Locate quote -> expand outward to the nearest block marker pair; returns None if not inside any block."""
    pos = problem_md.find(quote)
    if pos < 0:
        norm = re.sub(r"\s+", " ", quote).strip()
        flat = re.sub(r"\s+", " ", problem_md)
        p2 = flat.find(norm)
        if p2 < 0:
            return None
        pos = min(len(problem_md) - 1, p2)          # approximate location is enough to find the block
    last_b, last_id = None, None
    for m in BLOCK_B_RE.finditer(problem_md, 0, pos + 1):
        last_b, last_id = m.start(), m.group(1)
    if last_id is None:
        return None
    end_marker = f"<!-- e:{last_id} -->"
    end_pos = problem_md.find(end_marker, last_b)
    if end_pos < 0 or pos > end_pos + len(end_marker):
        return None                                  # quote is outside blocks (template/Target)
    return last_id


DEF_POOL = {"definition", "inline-definition", "assumption"}
RESULT_POOL = {"theorem", "lemma", "proposition", "corollary", "equation"}

# a parametrized-notation instance: a macro head with a short subscript
# parameter, e.g. \mathbb{Z}_K, \tX_n, \ell_{p}
_PARAM_NOTATION_RE = re.compile(
    r"(\\[A-Za-z]+\{[A-Za-z]\}|\\[A-Za-z]{2,})\s*_\s*"
    r"(?:\{[^{}]{1,12}\}|[A-Za-z0-9])")


def _parametrized_defined(gap_text: str, problem_md: str) -> bool:
    """The gap is an instance of parametrized notation whose general
    definition — same head, any parameter, followed by a defining `:=` —
    already sits in the package text (\\mathbb{Z}_K flagged while
    \\mathbb{Z}_n:=\\{0,...,n-1\\} is granted). The checker tier keeps
    missing this identification, and the audits certified the resulting
    exclusions as false kills."""
    m = _PARAM_NOTATION_RE.search(gap_text)
    if m:
        head = m.group(1)
        pat = re.compile(
            re.escape(head) + r"\s*_\s*(?:\{[^{}]{1,12}\}|[A-Za-z0-9])\s*"
            r"(?::=|\\coloneqq|\\triangleq)")
        if pat.search(problem_md):
            return True
    # bracket-family convention: gap mentions [F] while the package grants
    # the paper's generic [n]:={1,...,n} definition
    if re.search(r"\[[A-Za-z]\]", gap_text) and re.search(
            r"\[[A-Za-z]\]\s*(?::=|\\coloneqq)", problem_md):
        return True
    return False

_PTR_STOP = re.compile(
    r"(?i)\b(?:see|in|of|the|a|an|for|details?|we|refer|to|appendix|"
    r"appendices|proof|proofs|section|and|is|are|given|deferred|it|this|"
    r"below|above|full|complete)\b")


def _is_self_pointer(text: str, target: Statement,
                     label_map: dict) -> bool:
    """A dangling pointer to where the target's own proof lives ("see
    Appendix~\\ref{app:proofs}" on a statement whose proof IS in the
    appendix) is not a gap — the pointed-at content is exactly what the
    solver must produce. Repair-first: classify benign instead of dying on
    self_containment_unresolvable in a calibration run.

    Conservative: any resolvable statement reference, or meaningful residue
    beyond pointer boilerplate, keeps it a real gap.
    """
    if not target.proof_location.startswith("appendix"):
        return False
    if not re.search(r"(?i)appendix", text):
        return False
    from .latex_utils import scan_refs
    if any(lab in label_map for lab in scan_refs(text)):
        return False                        # points at an indexed statement
    residue = re.sub(r"\\[A-Za-z]+(?:\[[^\]]*\])?(?:\{[^}]*\})*", " ", text)
    residue = _PTR_STOP.sub(" ", residue)
    residue = re.sub(r"[^A-Za-z]", "", residue)
    return len(residue) <= 6


def _bound_pat(probe: str, flags: int = 0) -> re.Pattern:
    """Boundary-aware substring pattern for probe: require a word boundary
    when it starts/ends with a letter (LaTeX command-name boundaries likewise:
    \\Gamma is not a prefix of \\Gamma_t)."""
    return re.compile(
        (r"(?<![A-Za-z\\])" if probe[:1].isalpha() else "")
        + re.escape(probe)
        + (r"(?![A-Za-z_])" if probe[-1:].isalpha() else ""), flags)


def _search_items(index: StatementsIndex, g: str, casefold: bool,
                  pool: set[str], with_gc: bool,
                  exclude: set[str]) -> list[str]:
    """Substring search over statement_tex / gc.text_tex, returning matched ids.

    pool is partitioned by gap type: a term/symbol gap can only be filled by a
    definition-type entry -- matching a lemma that "uses" the term is a false hit
    (when the real definition is missing it would block the level-4 index-fill).
    exclude: entries already in the package cannot be the solution to a gap.
    remark/example are never candidates.
    """
    probe = _norm_ws(g)
    if not probe:
        return []

    # Boundary-aware matching: "\Gamma" must not match "\Gamma_t" (the definition
    # of Γ_t does not define Γ), "balanced" must not match "unbalanced". For math
    # fragments, fall back to a fully space-stripped comparison
    # (space differences like "O(d y_k | x_k)" <-> "O(dy_k|x_k)").
    flags = re.IGNORECASE if casefold else 0
    pat = _bound_pat(probe, flags)
    mathy = bool(re.search(r"[\\|_^(]", probe))
    pat_ns = _bound_pat(probe.replace(" ", ""), flags)

    def _match(text: str) -> bool:
        hay = _norm_ws(text)
        if pat.search(hay):
            return True
        return mathy and bool(pat_ns.search(hay.replace(" ", "")))

    hits = []
    for s in index.statements:
        if s.env_type not in pool or s.id in exclude:
            continue
        if _match(s.statement_tex):
            hits.append(s.id)
    if with_gc:
        for gc in index.global_context:
            if gc.id in exclude:
                continue
            if _match(gc.text_tex):
                hits.append(gc.id)
    return hits


def _pick_hit(index: StatementsIndex, hits: list[str], target: Statement) -> str | None:
    """Disambiguate multiple ladder hits: prefer the earliest entry before the
    target (a definition normally precedes its use), then gc entries; entries
    after the target qualify only if added by index-fill (physically earlier
    in the text, their order_index merely appended at the tail)."""
    if not hits:
        return None
    if len(hits) == 1:
        return hits[0]
    order = {s.id: s.order_index for s in index.statements}
    gc_hits = [h for h in hits if h not in order]
    stmt_hits = sorted(
        [h for h in hits if h in order
         and (order[h] < target.order_index or order[h] > target.order_index
              and index.by_id()[h].added_by != "parser")],
        key=lambda h: order[h])
    prior = [h for h in stmt_hits if order[h] < target.order_index]
    if prior:
        return prior[0]
    if gc_hits:
        return gc_hits[0]
    return stmt_hits[0] if stmt_hits else None


# Numbered references: the number group must start with an uppercase letter/digit
# ("Theorem 4.2" / "Lemma B.1"), otherwise narrative like "the theorem states"
# would be misjudged as a numbered reference. Environment words list case variants
# explicitly -- IGNORECASE would also disable the [A-Z0-9] of the number group
NUMBERED_RE = re.compile(
    r"([Tt]heorem|[Ll]emma|[Pp]roposition|[Cc]orollary|[Dd]efinition|"
    r"[Aa]ssumption)\s+([A-Z0-9][A-Za-z0-9.]*)")
EQNUM_RE = re.compile(r"\((\d+(?:\.\d+)+[a-z]?)\)")

# Named results like "Portmanteau theorem" / "Euler's pentagonal number theorem"
NAME_KEY_RE = re.compile(
    r"\b([A-Za-z][A-Za-z'’\-]*(?:[ -][A-Za-z'’\-]+){0,5}[ -]"
    r"(?:theorem|lemma|identity|formula|inequality|principle|law|criterion|"
    r"rule|equation|estimate|bound|property)s?)\b", re.IGNORECASE)

# Wording that refers to the paper's internal context ("the proof of the
# same theorem") can never be classified as baseline knowledge
ANAPHORIC_RE = re.compile(
    r"\b(?:the\s+(?:proofs?|arguments?|previous|preceding|same|above|"
    r"foregoing|earlier|first|second|third|last)\b"
    r"|this\s+(?:paper|section|chapter|proof))", re.IGNORECASE)

MATHY_RE = re.compile(r"[\\${}^_=<>|~#&]")

STOP_WORDS = {"the", "a", "an", "of", "for", "and", "are", "is", "that",
              "with", "all", "any", "by", "in", "on", "to", "we", "assume",
              "assumption", "suppose", "holds", "have", "has", "let"}


def _name_key(text: str) -> str | None:
    """Extract a named-result short name from gap text (comparison/search is much more robust than a full quote)."""
    mo = NAME_KEY_RE.search(text)
    if not mo:
        return None
    key = re.sub(r"^(?:(?:by|via|using|from|applying|apply|per|with|the|an?)"
                 r"\s+)+", "", mo.group(1).strip(),
                 flags=re.IGNORECASE).replace("’", "'")
    return key if len(key) >= 8 else None


def _content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z\-]{2,}", text.casefold())
            if w not in STOP_WORDS}


def _baseline_assumable(text: str) -> str | None:
    """For a result/term gap whose ladder (including targeted index-fill) is
    entirely empty: if it is a natural-language concept phrase that does not
    refer to the paper's internal numbering/context -> classify as domain
    baseline knowledge (§4.3), non-blocking.

    Rationale: not finding it anywhere via targeted index-fill = the paper never
    states/defines it, and the author treats it as reader consensus;
    field_baseline always contains "the paper's own subject area". Bare symbols,
    numbered references, and "the same/previous ..." anaphora never apply (they
    must be resolved inside the paper). Returns the normalized short name
    (recorded in the log and report), or None when it cannot be classified."""
    from .latex_utils import REF_CMD_RE
    if REF_CMD_RE.search(text) or NUMBERED_RE.search(text) \
            or EQNUM_RE.search(text) or ANAPHORIC_RE.search(text):
        return None
    cand = _name_key(text) or _norm_ws(text).rstrip(".:;,")
    if len(cand) > 90 or MATHY_RE.search(cand):
        return None
    if len([w for w in re.findall(r"[A-Za-z][A-Za-z'’\-]{2,}", cand)]) < 2:
        return None
    return cand


DEFINE_OPS = ("=", "\\coloneqq", "\\triangleq", "\\doteq")


def _defining_equation(index: StatementsIndex, g: str, present: set[str],
                       target: Statement) -> str | None:
    """Symbol/notation gap level 3.5: g appears on the left of the first defining
    operator (= / := / \\coloneqq ...) on some line of an equation entry -> that
    equation defines g ("\\Theta_t := ..."). In formulas that use the symbol it
    sits on the right and won't match; take the first in document order
    (definition precedes use). Mismatches are caught by the next 4a re-check."""
    key = _norm_ws(g)
    if not key:
        return None
    pat = _bound_pat(key)
    for s in index.statements:
        if s.env_type != "equation" or s.id in present or s.id == target.id:
            continue
        for line in s.statement_tex.splitlines():
            ln = _norm_ws(line)
            ops = [p for p in (ln.find(op) for op in DEFINE_OPS) if p > 0]
            if ops and pat.search(ln[:min(ops)]):
                return s.id
    return None


def _token_overlap_hit(index: StatementsIndex, g: str,
                       present: set[str]) -> str | None:
    """standing gap level 3.6: content-word overlap ratio >= 0.6 with some
    assumption/gc. The pool is tiny (assumption + gc), substring matching is not
    immune to rewording, so bag-of-words is the fallback
    ("the spaces are Polish by assumption" <-> "X, Y are Polish spaces")."""
    words = _content_words(g)
    if len(words) < 2:
        return None
    cands = [(s.id, s.statement_tex) for s in index.statements
             if s.env_type == "assumption" and s.id not in present]
    cands += [(x.id, x.text_tex) for x in index.global_context
              if x.id not in present]
    best, best_r = None, 0.0
    for cid, text in cands:
        tw = set(re.findall(r"[a-z][a-z\-]{2,}", text.casefold()))
        r = len(words & tw) / len(words)
        if r > best_r:
            best, best_r = cid, r
    return best if best_r >= 0.6 else None


def _math_fragments(text: str) -> list[str]:
    """Cut display-equation fragments out of a 4c quote (lines >=25 chars
    containing a \\command and =), for verbatim comparison against the
    statements of later theorems/equations."""
    frags = []
    for line in text.splitlines():
        ln = line.strip()
        if len(ln) >= 25 and "\\" in ln and "=" in ln:
            frags.append(ln.rstrip(".,;"))
    return frags


def _best_new(index: StatementsIndex, new_ids: list[str], g: str,
              nk: str | None) -> str | None:
    """Direct match against level-4 index-fill products: pick the best of the new
    entries A0 just extracted for this gap by content-word overlap, bypassing the
    pool partition -- a known identity the paper restates in prose is often
    extracted as an inline-definition, and a search of the result pool would never
    hit it."""
    words = _content_words(nk or g)
    if not words:
        return None
    by = index.by_id()
    best, best_n = None, 0
    for nid in new_ids:
        s = by.get(nid)
        if s is None:
            continue
        hay = (s.statement_tex + " " + (s.display_name or "")).casefold()
        n = sum(1 for w in words if w in hay)
        if n > best_n:
            best, best_n = nid, n
    return best if best_n >= max(1, len(words) // 2) else None


def _short_symbol_hit(index: StatementsIndex, g: str, present: set[str],
                      target: Statement) -> str | None:
    """Defining-occurrence search for bare symbols (≤2 chars). Substring
    search over-matches catastrophically for single letters, so instead look
    for a DEFINING occurrence — "$K$ denotes", "let $I$ be", "$I:=[0,1]$" —
    restricted to definition-grade entries, gc items and equation entries.
    Yield lever: atomic notation like I/K/F previously had NO resolution
    path at all (label lookup only) and killed 3/5 targets of 2510.03923."""
    e = re.escape(g)
    pats = [
        re.compile(r"\$\{?" + e + r"\}?\$\s*(?:denotes?|stands?\s+for|"
                   r"is\s+(?:the|an?|defined)|:?=|\\coloneqq)"),
        re.compile(r"\$\{?" + e + r"\}?\s*(?::=|\\coloneqq|=)"),
        re.compile(r"(?<![A-Za-z\\}])" + e + r"\s*(?::=|\\coloneqq)"),
        re.compile(r"(?:[Ll]et|[Dd]enoted?\s+by|[Ww]e\s+write|[Ww]rite)\s+"
                   r"\$\{?" + e + r"\}?\$"),
    ]
    cands: list[tuple[int, str]] = []
    for gitem in index.global_context:            # conventions first
        if gitem.id not in present and \
                any(p.search(gitem.text_tex) for p in pats):
            cands.append((-1, gitem.id))
    for s in index.statements:
        if s.id in present or s.id == target.id:
            continue
        if s.env_type not in DEF_POOL and s.env_type != "equation":
            continue
        if any(p.search(s.statement_tex) for p in pats):
            cands.append((s.order_index, s.id))
    return min(cands)[1] if cands else None


async def _match_gap(ctx: RunContext, index: StatementsIndex, label_map: dict,
                     target: Statement, g: str, where: str,
                     kind: str = "implicit-definition",
                     arises_in: str = "statement",
                     present: set[str] | None = None) -> Edge | str | None:
    """The level 1-4 matching of §10.3; returns an edge on success, None on
    failure. May append index entries in place.

    present: entries already in the current package -- excluded from candidates
    (an edge to an entry already in the package is a no-op, and would also block
    the level-4 targeted index-fill).
    """
    present = present or set()
    if kind == "implicit-result":
        pool, with_gc = RESULT_POOL, False
    elif kind == "standing":
        pool, with_gc = {"assumption"}, True
    else:
        pool, with_gc = DEF_POOL, True

    # Atomic-symbol route. a4a reports these as "I", "K", or "I (the domain
    # of ...)" / "T_{\tW} (the linear operator ...)": a head symbol, possibly
    # with a parenthetical description. Substring search over-matches for
    # such heads, so the routes are label lookup, defining-occurrence search,
    # and dollar-wrapped targeted index-fill; a longer gap text falls through
    # to the normal ladder if the head route finds nothing.
    gs_full = g.strip()
    mo_head = re.match(
        r"^\$?\{?(?P<h>[A-Za-z](?:_(?:\{[^}]{1,12}\}|[A-Za-z0-9]))?)\}?\$?"
        r"\s*(?:\(|$)", gs_full)
    if mo_head:
        head = mo_head.group("h")
        cand = label_map.get(head)
        if cand and cand in present:
            return "PRESENT"
        if cand and cand != target.id:
            return Edge.model_validate({
                "from": target.id, "to": cand, "arises_in": arises_in,
                "kind": kind, "evidence": where[:500],
                "confidence": "medium", "source": "agent4-patch"})
        hit = _short_symbol_hit(index, head, present, target)
        if hit is None:
            probes = [f"${head}$"] + ([head] if len(head) > 2 else [])
            for pr in probes:
                try:
                    new_ids = await targeted_fill(ctx, index, pr,
                                                  added_by="agent4-patch")
                except Exception as e:
                    ctx.log_event(event="targeted_fill_failed", phrase=pr,
                                  err=repr(e)[:150])
                    new_ids = []
                if new_ids:
                    hit = (_short_symbol_hit(index, head, present, target)
                           or _best_new(index, new_ids, gs_full, None))
                if hit:
                    break
        if hit and hit in present:
            return "PRESENT"
        if hit and hit != target.id:
            return Edge.model_validate({
                "from": target.id, "to": hit, "arises_in": arises_in,
                "kind": kind, "evidence": where[:500],
                "confidence": "medium", "source": "agent4-patch"})
        if len(gs_full) <= 2:
            return None            # nothing else to try for a bare letter

    def search(cf: bool, probe: str | None = None):
        return _pick_hit(index, _search_items(index, probe or g, cf, pool,
                                              with_gc, present), target)

    from .latex_utils import scan_refs
    for lab in scan_refs(g) + scan_refs(where):       # 0 gap text carries its own \ref
        cand = label_map.get(lab)
        if cand and cand == target.id:
            continue
        if cand and cand in present:
            return "PRESENT"       # the named block is already in the package: mere-reference false positive
        if cand:
            return Edge.model_validate({
                "from": target.id, "to": cand, "arises_in": arises_in,
                "kind": kind, "evidence": where[:500],
                "confidence": "high", "source": "agent4-patch"})

    nk = _name_key(g)
    hit = search(False)                                               # 1 exact
    if hit is None and nk and nk != g.strip():                        # 1.5 name key
        hit = search(False, nk) or search(True, nk)
    if hit is None and " " not in g.strip():                          # 2 label
        cand = label_map.get(g.strip())
        hit = cand if cand and cand not in present else None
    if hit is None and "$" not in g and "\\" not in g:                # 3 casefold
        hit = search(True)
    if hit is None and kind == "implicit-definition":                 # 3.5 defining equation
        hit = _defining_equation(index, g, present, target)
    if hit is None and kind == "standing":                            # 3.6 token overlap
        hit = _token_overlap_hit(index, g, present)
    if hit is None:                                                   # 4 targeted index-fill
        new_ids = await targeted_fill(ctx, index, nk or g,
                                      added_by="agent4-patch")
        if new_ids:
            ctx.write_json("index/statements.v2.json", index)
            hit = search(False)
            if hit is None and nk:
                hit = search(False, nk) or search(True, nk)
            if hit is None:
                hit = _best_new(index, new_ids, g, nk)
    if hit is None or hit == target.id:
        return None
    return Edge.model_validate({
        "from": target.id, "to": hit, "arises_in": arises_in, "kind": kind,
        "evidence": where[:500], "confidence": "medium",
        "source": "agent4-patch"})


# Anaphora like "the last expression" / "the previous display" = the proof's own previous step
INTERNAL_ANAPHORA_RE = re.compile(
    r"\b(?:the|this)\s+(?:last|previous|preceding|above|foregoing)\s+"
    r"(?:expression|display(?:ed)?(?:\s+equation)?|equation|computation|"
    r"calculation|identity|line|step|estimate)", re.IGNORECASE)


def _looks_like_reference(invoked_as: str) -> bool:
    """Classify a 4c missing item: a real reference (blocking, needs an edge)
    vs. a derivation step of the proof itself (over-reported by 4c, ignore).
    A reference = \\ref, numbering like "Lemma 4.2", equation numbering like
    "(2.1)", or a short noun phrase without derivation notation. Long display
    equations with = / a math environment, and internal anaphora like "the last
    expression", are what the proof itself is going to derive, not a prerequisite
    tool."""
    from .latex_utils import REF_CMD_RE
    if REF_CMD_RE.search(invoked_as) or NUMBERED_RE.search(invoked_as) \
            or EQNUM_RE.search(invoked_as):
        return True
    if INTERNAL_ANAPHORA_RE.search(invoked_as):
        return False
    s = invoked_as.strip()
    return len(s) <= 60 and "=" not in s and "\\begin" not in s \
        and "\\sum" not in s and "\\int" not in s


async def _match_missing(ctx: RunContext, index: StatementsIndex,
                         label_map: dict, target: Statement, m: A4cMissing,
                         present: set[str] | None = None
                         ) -> Edge | str | None:
    """§10.6: direct pick by source label, otherwise reuse the §10.3 ladder.

    present holds entries that are "already in the package ∪ already pointed to by
    an edge". A direct pick that hits a present member = the tool named by 4c is
    actually already granted (its statement is in the package) -> return the
    "PRESENT" sentinel, and the caller treats it as non-blocking (same class of
    false positive as 4b mere-presence); other direct-pick candidates skip the
    no-op and keep looking for an alternative solution."""
    from .latex_utils import scan_refs
    present = present or set()
    seen_present = False

    def _ok(hit: str | None) -> bool:
        nonlocal seen_present
        if hit and hit in present:
            seen_present = True
        return bool(hit) and hit != target.id and hit not in present

    for lab in scan_refs(m.invoked_as):          # invoked_as often contains raw \ref{...}
        hit = label_map.get(lab)
        if _ok(hit):
            return Edge.model_validate({
                "from": target.id, "to": hit, "arises_in": "proof",
                "kind": "implicit-result", "evidence": m.invoked_as[:500],
                "confidence": "medium", "source": "agent4-patch"})
    # A printed theorem/equation number is evidence that the phrase is
    # paper-local, but it is not sufficient to choose a graph node. Continue
    # through the text/source matching ladder and exclude if no unique
    # source-backed match can be established.
    if seen_present:
        return "PRESENT"
    if m.kind == "result":
        # direct math-fragment match: a display equation embedded in the 4c
        # quote is often verbatim the statement of a later theorem/equation
        for frag in _math_fragments(m.invoked_as):
            hits = _search_items(index, frag, False,
                                 RESULT_POOL, False, present | {target.id})
            hit = _pick_hit(index, hits, target)
            if _ok(hit):
                return Edge.model_validate({
                    "from": target.id, "to": hit, "arises_in": "proof",
                    "kind": "implicit-result", "evidence": m.invoked_as[:500],
                    "confidence": "medium", "source": "agent4-patch"})
    kind = {"result": "implicit-result", "definition": "implicit-definition",
            "assumption": "standing"}.get(m.kind, "implicit-result")
    return await _match_gap(ctx, index, label_map, target, m.invoked_as,
                            m.invoked_as, kind=kind, arises_in="proof",
                            present=present)


async def _repair_with_a6(ctx: RunContext, index: StatementsIndex,
                          graph: DepGraph, target: Statement,
                          problem_md: str, unres_gaps: list[str],
                          unres_miss: list[str], flat: str,
                          paper_title: str, field_baseline: str) -> int:
    """A6 last-resort repair: an audit-tier model with the FULL PAPER supplies
    quoted or synthesized material for the ladder's leftovers, instead of the
    package dying on the spot. A6 only PROPOSES — every merged item goes
    through the normal a4 re-verification, grants_from_target, and the ship
    leak scan. Deterministic guards here: nothing whose text lies inside the
    target's own proof, no synthesized results, no fake "quotes", no
    duplicates. Returns the number of merged entries."""
    items = list(dict.fromkeys(unres_gaps + unres_miss))
    try:
        out = await call_llm(ctx, "a6", {
            "paper_title": paper_title,
            "flat_source": flat[:600_000],
            "problem_md": problem_md,
            "target_id": target.id,
            "target_proof": (target.proof_tex or "")[:60_000],
            "unresolved_items": "\n".join(f"- {x}" for x in items),
            "field_baseline": field_baseline})
    except (TaskFailed, Exception) as e:
        ctx.log_event(event="a6_failed", target=target.id, err=repr(e)[:200])
        return 0
    merged = _merge_repair_fixes(ctx, index, graph, target, out.fixes, flat,
                                 tag="a6")
    ctx.progress(f"A6 repair {target.id}: {merged}/{len(items)} items merged")
    return merged


def _merge_repair_fixes(ctx: RunContext, index: StatementsIndex,
                        graph: DepGraph, target: Statement,
                        fixes: list, flat: str, tag: str = "a6") -> int:
    """Guarded merge shared by the A6 repairer and the A7 appeal judge.
    Every proposal passes the same deterministic guards: nothing whose text
    lies inside the target's own proof, no synthesized results, no fake
    "quotes", duplicates become edge grants to the existing entry. Returns
    the number of material changes (new entries + granted edges)."""
    from .step3_fill_index import _is_duplicate, _next_gc_seq
    from .target_integrity import context_statement_id
    tproof = _norm_ws(target.proof_tex or "")
    flat_norm = _norm_ws(flat)
    merged = 0
    for fx in fixes:
        txt = fx.text_tex.strip()
        if getattr(fx, "action", "quote") == "unfixable" or not txt:
            ctx.log_event(event=f"{tag}_unfixable", target=target.id,
                          item=fx.item[:80], note=fx.note[:150])
            continue
        if getattr(fx, "action", "quote") == "synthesized" \
                and fx.kind == "result":
            ctx.log_event(event=f"{tag}_rejected_synth_result",
                          target=target.id, item=fx.item[:80])
            continue
        tn = _norm_ws(txt)
        if tn and tn in tproof:
            ctx.log_event(event=f"{tag}_rejected_own_proof",
                          target=target.id, item=fx.item[:80])
            continue
        if getattr(fx, "action", "quote") == "quote" and fx.kind == "result" \
                and tn not in flat_norm:
            ctx.log_event(event=f"{tag}_rejected_fake_quote",
                          target=target.id, item=fx.item[:80])
            continue
        if _is_duplicate(txt, index):
            # The repair material already exists in the index — the actual
            # defect is that the package never granted it. Convert the
            # would-be skip into an edge grant so assembly pulls the existing
            # entry in (the patch-round audit showed dup-skips false-killing
            # packages whose fix was already indexed but not packaged).
            dup_id = ""
            for s in index.statements:
                e = _norm_ws(s.statement_tex)
                if tn and (tn in e or e in tn):
                    dup_id = s.id
                    break
            if not dup_id:
                for g in index.global_context:   # edges to gc ids are valid (assembly honors them)
                    e = _norm_ws(g.text_tex)
                    if tn and (tn in e or e in tn):
                        dup_id = g.id
                        break
            if dup_id and _append_edges(graph, [Edge.model_validate({
                    "from": target.id, "to": dup_id, "arises_in": "proof",
                    "kind": ("implicit-result" if fx.kind == "result"
                             else "implicit-definition"),
                    "evidence": fx.item[:500], "confidence": "medium",
                    "source": "agent4-patch"})]):
                ctx.log_event(event=f"{tag}_duplicate_granted",
                              target=target.id, id=dup_id, item=fx.item[:80])
                merged += 1
            else:
                ctx.log_event(event=f"{tag}_duplicate_skipped",
                              target=target.id, item=fx.item[:80],
                              detail="gc match or edge already present")
            continue
        if fx.kind in ("notation", "assumption"):
            new_id = f"gc-{_next_gc_seq(index)}"
            index.global_context.append(GlobalItem(
                id=new_id,
                kind="notation" if fx.kind == "notation"
                else "standing-assumption",
                scope="paper", text_tex=txt, added_by="agent4-patch"))
        else:
            env = ("inline-definition" if fx.kind == "definition"
                   else "proposition")
            sid = context_statement_id(
                paper_id=index.paper_id, added_by="agent4-patch",
                env_type=env, statement_tex=txt,
                used_ids={statement.id for statement in index.statements})
            index.statements.append(Statement(
                id=sid, env_type=env, latex_label="",
                display_name="", section=tag,
                order_index=max((s.order_index
                                 for s in index.statements), default=-1) + 1,
                statement_tex=txt, proof_tex=None, proof_location="omitted",
                mechanical_refs=[], uses_figure=False,
                added_by="agent4-patch"))
            new_id = sid
        _append_edges(graph, [Edge.model_validate({
            "from": target.id, "to": new_id, "arises_in": "proof",
            "kind": ("implicit-result" if fx.kind == "result"
                     else "implicit-definition"),
            "evidence": fx.item[:500], "confidence": "medium",
            "source": "agent4-patch"})])
        ctx.log_event(event=f"{tag}_fix_merged", target=target.id, id=new_id,
                      kind=fx.kind, action=getattr(fx, "action", "quote"),
                      item=fx.item[:80])
        merged += 1
    if merged:
        ctx.write_json("index/statements.v2.json", index)
    return merged


async def _appeal_review(ctx: RunContext, index: StatementsIndex,
                         graph: DepGraph, target: Statement,
                         problem_md: str, blocking: list[str], flat: str,
                         paper_title: str, field_baseline: str
                         ) -> tuple[list[str], int, list[str]]:
    """Option-2 appeal court: before an exclusion is written, an audit-tier
    judge with the FULL PAPER reviews every blocking item once per package.
    Returns (resolved_item_texts, merged_material_count, upheld_item_texts).
    resolved = the file/baseline already covers it (caller marks baseline_ok);
    merged   = paper material granted through the shared A6 guards (caller
    reassembles and re-verifies); upheld = the kill stands, recorded on the
    exclusion. Judge unavailable -> everything upheld (the old kill path)."""
    try:
        out = await call_llm(ctx, "a7", {
            "paper_title": paper_title,
            "flat_source": flat[:600_000],
            "problem_md": problem_md,
            "target_id": target.id,
            "target_proof": (target.proof_tex or "")[:60_000],
            "blocking_items": "\n".join(f"- {x}" for x in blocking),
            "field_baseline": field_baseline})
    except (TaskFailed, Exception) as e:
        ctx.log_event(event="a7_failed", target=target.id, err=repr(e)[:200])
        return [], 0, list(blocking)
    resolved: list[str] = []
    upheld: list[str] = []
    grant_fixes = []
    for v in out.items:
        if v.verdict == "resolved_in_file":
            resolved.append(v.item)
            ctx.log_event(event="appeal_overturned", target=target.id,
                          how="resolved_in_file", item=v.item[:80],
                          evidence=v.evidence[:200])
        elif v.verdict == "grant_from_paper" and v.fix_text_tex.strip():
            grant_fixes.append(A6Fix(item=v.item, action="quote",
                                     kind=v.fix_kind,
                                     text_tex=v.fix_text_tex, note=v.note))
        else:
            upheld.append(v.item)
            ctx.log_event(event="appeal_upheld", target=target.id,
                          item=v.item[:80], note=v.note[:150])
    merged = 0
    if grant_fixes:
        merged = _merge_repair_fixes(ctx, index, graph, target, grant_fixes,
                                     flat, tag="a7")
        # grants that every guard rejected stay blocking
        if not merged:
            upheld += [f.item for f in grant_fixes]
    ctx.progress(f"{target.id} appeal: {len(resolved)} resolved-in-file, "
                 f"{merged} granted, {len(upheld)} upheld")
    return resolved, merged, upheld


def _append_edges(graph: DepGraph, new_edges: list[Edge]) -> int:
    existing = {(e.from_, e.to, e.arises_in) for e in graph.edges}
    n = 0
    for e in new_edges:
        k = (e.from_, e.to, e.arises_in)
        if k not in existing:
            graph.edges.append(e)
            existing.add(k)
            n += 1
    return n


# --------------------------------------------------------------- single-package verification

async def _verify_package(ctx: RunContext, index: StatementsIndex,
                          graph: DepGraph, target: Statement, policy: str,
                          field_baseline: str, flat: str,
                          source_file: str,
                          paper_title: str = "") -> Report | None:
    pkg = f"packages/{target.id}/{policy}"
    problem_md = ctx.path(f"{pkg}/problem.md").read_text(encoding="utf-8")
    assembly = ctx.read_json(f"{pkg}/assembly.json")
    integrity_issues = statement_source_issues(
        target, flat_source=flat, expected_source_file=source_file)
    integrity_issues.extend(proof_source_issues(
        target, flat_source=flat, expected_source_file=source_file))
    target_tex_path = ctx.path(f"{pkg}/target.tex")
    target_json_path = ctx.path(f"{pkg}/target.json")
    if not target_tex_path.exists() or not target_json_path.exists():
        integrity_issues.append("frozen target artifacts are missing")
    else:
        try:
            target_record = ctx.read_json(f"{pkg}/target.json")
        except (OSError, ValueError, TypeError) as exc:
            integrity_issues.append(f"target.json is unreadable: {exc}")
        else:
            integrity_issues.extend(frozen_target_artifact_issues(
                target,
                target_tex=target_tex_path.read_text(encoding="utf-8"),
                record=target_record))
    integrity_issues.extend(target_identity_issues(problem_md, target))
    if integrity_issues:
        ctx.add_excluded(target.id, policy, "target_integrity_failed",
                         "; ".join(integrity_issues)[:900])
        return None
    removed: set[str] = set(assembly.get("removed", []))
    need_def = set(assembly.get("need_def", []))
    policy_downgraded = bool(assembly.get("policy_downgraded", False))
    run_4c = policy in ("dep-closure", "minimal")

    report = Report(target_id=target.id, policy=policy,
                    policy_downgraded=policy_downgraded)
    prev_ambiguities: set[str] = set()
    label_map = ctx.read_json("index/label_map.json")

    last_gaps: list[A4aGap] = []
    last_miss: list[A4cMissing] = []
    baseline_ok: set[str] = set()      # gaps already classified as baseline knowledge / already in the package (across iterations)
    tried_ext: set[tuple] = set()      # missing items already converted to external grants (do not re-append)
    passed = False
    iter_capped = False
    tried_a6 = False
    tried_appeal = False
    appeal_upheld_items: list[str] = []
    final_gate_done = False
    final_gate_clean = False               # True only when the gate ran and found nothing
    pending_gate_gaps: list[A4aGap] = []   # gate findings handed to the next iteration's ladder

    async def _run_final_gate(cur_problem_md: str) -> list[A4aGap]:
        """Audit-tier self-containment re-check on the final file, once per
        package. Every ship path must pass through here — the calibration
        audits showed the gate-bypassed pass paths ship the packages with the
        most fatal findings. Findings never kill the package directly: they
        go through the normal repair machinery. Unavailable gate -> ship."""
        nonlocal final_gate_done, final_gate_clean
        if not ctx.cfg.pipeline.final_gate or final_gate_done:
            return []
        final_gate_done = True
        gate_model = ctx.cfg.models.for_task("a6")
        try:
            fg = await call_llm(ctx, "a4a", {
                "problem_md": cur_problem_md,
                "field_baseline": field_baseline}, model=gate_model)
        except (TaskFailed, Exception) as e:
            # the gate is an extra safety net — unavailable must not
            # block shipping
            ctx.log_event(event="final_gate_failed",
                          target=target.id, err=repr(e)[:200])
            return []
        fg_gaps = [x for x in fg.gaps
                   if _norm_ws(x.text) not in baseline_ok]
        final_gate_clean = not fg_gaps
        ctx.log_event(event="final_gate", target=target.id,
                      policy=policy, model=gate_model,
                      gaps=len(fg_gaps), raw=len(fg.gaps))
        ctx.progress(f"{target.id}/{policy} final gate "
                     f"({gate_model}): {len(fg_gaps)} gaps")
        return fg_gaps

    for it in range(1, ctx.cfg.pipeline.max_verify_iters + 1):
        report.iterations = it
        ctx.path(f"{pkg}/problem.iter{it}.md").write_text(problem_md,
                                                          encoding="utf-8")
        a4c_out = None
        if run_4c:
            a4c_out = await call_llm(ctx, "a4c", {
                "target_proof_tex": target.proof_tex or "",
                "problem_md": problem_md, "field_baseline": field_baseline})
        a4a_out = await call_llm(ctx, "a4a", {
            "problem_md": problem_md, "field_baseline": field_baseline})
        a4b_out = await call_llm(ctx, "a4b", {"problem_md": problem_md})
        ctx.progress(f"{target.id}/{policy} iter {it}: "
                     f"gaps={len(a4a_out.gaps)} "
                     f"miss={len(a4c_out.missing) if a4c_out else '-'} "
                     f"leaks={len(a4b_out.leaks)}")

        # 4c missing classification: only "real reference" missing items block
        # shipping and drive edge-patching; display equations the proof derives
        # itself (long equations/constructions) are 4c over-reporting, ignored and logged.
        miss_all = list(a4c_out.missing) if a4c_out else []
        miss = []
        for m in miss_all:
            if _norm_ws(m.invoked_as) in baseline_ok:
                continue                           # already classified as baseline knowledge in a previous iteration
            if _looks_like_reference(m.invoked_as):
                miss.append(m)
            else:
                ctx.log_event(event="a4c_internal_step_ignored",
                              target=target.id, quote=m.invoked_as[:80])
        raw_gap_n = len(a4a_out.gaps)
        gaps = [g for g in a4a_out.gaps
                if _norm_ws(g.text) not in baseline_ok]
        if pending_gate_gaps:                     # gate findings from the previous iteration join the ladder
            seen_g = {_norm_ws(g.text) for g in gaps}
            gaps += [g for g in pending_gate_gaps
                     if _norm_ws(g.text) not in seen_g]
            pending_gate_gaps = []
        bad_leaks = [l for l in a4b_out.leaks if l.severity in ("fatal", "hint")]
        report.gaps_history.append([g.text for g in gaps])
        last_gaps, last_miss = gaps, miss

        # Classify leaks first: outside-block (template/Target area, a 4b false
        # positive) and "mere presence" (the quote falls entirely inside an
        # entry's authoritative source text = treating a granted prerequisite
        # result as a leak, which the prompt explicitly forbids) both do not
        # count as real leaks, do not participate in the pass decision, and do
        # not trigger a drop.
        real_leaks: list[tuple] = []
        for leak in bad_leaks:
            bid = _find_block_of(problem_md, leak.quote)
            if bid is None:
                ctx.log_event(event="leak_outside_blocks",
                              quote=leak.quote[:80])
                continue
            auth = _authoritative_text(index, bid)
            if auth and _norm_ws(leak.quote) in _norm_ws(auth):
                ctx.log_event(event="leak_mere_presence_ignored",
                              block=bid, quote=leak.quote[:80])
                continue
            real_leaks.append((leak, bid))

        # The sufficient/self_contained booleans no longer veto on their own:
        # when all missing/gaps are absorbed by the classifier (internal
        # derivation / baseline knowledge), the classifier's conclusion overrides
        # the LLM's overall judgment (same philosophy as the 4b mere-presence guard)
        ok_4c = (not run_4c) or not miss
        ok_4a = not gaps and (a4a_out.self_contained or len(gaps) < raw_gap_n)
        ok_4b = not real_leaks
        if ok_4c and ok_4a and ok_4b:
            # Stage-1 ship gate: the calibration audits measured a consistent
            # detection gap between the cheap checker tier and the audit tier.
            # Findings do not kill the package: they feed the normal repair
            # machinery below (ladder + A6) for one more round.
            fg_gaps = await _run_final_gate(problem_md)
            if not fg_gaps:
                report.self_contained = True
                report.leak_clean = True
                report.sufficiency = True if run_4c else None
                passed = True
                break
            gaps = fg_gaps          # hand to the repair machinery this iter
            report.gaps_history.append([g.text for g in fg_gaps])

        material = False       # graph/blocks actually changed -> must reassemble and re-verify
        classified = False     # merely classified appeals as benign -> package unchanged, can pass in place
        unres_gaps: list[str] = []
        try:
            # §10.5 leak block drop
            for leak, bid in real_leaks:
                if bid in need_def:
                    raise _Unrepairable("leak_in_required_context",
                                        f"block {bid}")
                if bid not in removed:
                    removed.add(bid)
                    report.removed_blocks.append(bid)
                    material = True

            # present = actual entries in the current package. (Do not merge in
            # "already pointed to by an edge" -- edges from the previous batch
            # would make the ladder permanently skip legitimate candidates,
            # empirically poisoning cross-batch reruns.)
            present = set(assembly.get("defs", []) + assembly.get("res", [])
                          + assembly.get("gcs", []))

            # §10.6 missing -> edge-patch; a result/definition missing item whose
            # ladder is entirely empty, if it is a pure concept phrase -> baseline
            # knowledge, non-blocking (an assumption must be resolved inside the
            # paper); a math-form result missing item -> convert to a §9.3
            # cite-less external grant (a3_ext states it or rejects it, rejection
            # = external_dep_unstatable terminal state)
            unres_miss = []
            for m in miss:
                if _is_self_pointer(m.invoked_as, target, label_map):
                    baseline_ok.add(_norm_ws(m.invoked_as))
                    ctx.log_event(event="self_pointer_ignored",
                                  target=target.id, quote=m.invoked_as[:80])
                    classified = True
                    continue
                e = await _match_missing(ctx, index, label_map, target, m,
                                         present=present)
                if isinstance(e, Edge):
                    if _append_edges(graph, [e]):
                        material = True
                    continue
                if e == "PRESENT":               # the named tool is already in the package
                    baseline_ok.add(_norm_ws(m.invoked_as))
                    ctx.log_event(event="a4c_present_ignored",
                                  target=target.id, quote=m.invoked_as[:120])
                    classified = True
                    continue
                cand = (_baseline_assumable(m.invoked_as)
                        if m.kind != "assumption" else None)
                if cand:
                    baseline_ok.add(_norm_ws(m.invoked_as))
                    report.baseline_assumed.append(cand)
                    ctx.log_event(event="a4c_baseline_assumed",
                                  target=target.id, name=cand,
                                  quote=m.invoked_as[:120])
                    classified = True
                elif m.kind == "result" and len(m.invoked_as) <= 300 \
                        and (target.id, _norm_ws(m.invoked_as)[:80]) \
                        not in tried_ext:
                    tried_ext.add((target.id, _norm_ws(m.invoked_as)[:80]))
                    graph.external_deps.append(ExternalDep(
                        used_by=target.id, citation_key="",
                        usage_quote=m.invoked_as[:300]))
                    ctx.log_event(event="a4c_missing_to_external",
                                  target=target.id, quote=m.invoked_as[:120])
                    material = True
                else:
                    unres_miss.append(m.invoked_as)

            # §10.3 gap -> edge-patch; ambiguity two-iteration rule
            cur_amb = set()
            for gp in gaps:
                if _is_self_pointer(gp.text, target, label_map):
                    baseline_ok.add(_norm_ws(gp.text))
                    ctx.log_event(event="self_pointer_ignored",
                                  target=target.id, quote=gp.text[:80])
                    classified = True
                    continue
                if gp.kind in ("symbol", "term") \
                        and _parametrized_defined(gp.text, problem_md):
                    baseline_ok.add(_norm_ws(gp.text))
                    ctx.log_event(event="gap_parametrized_present",
                                  target=target.id, quote=gp.text[:80])
                    classified = True
                    continue
                if gp.kind == "ambiguity":
                    if gp.text in prev_ambiguities:
                        # repeat after a repair round: no longer an instant
                        # kill — it rides unres_gaps into the appeal court
                        # (A6 already had its shot; tried_a6 guards a rerun)
                        ctx.log_event(event="ambiguity_repeated",
                                      target=target.id, quote=gp.text[:120])
                        cur_amb.add(gp.text)
                        unres_gaps.append(gp.text)
                        continue
                    # Cheap-tier ambiguity gets audit-tier arbitration: if the
                    # ship gate (same question, stronger model) judges the
                    # file clean, the ambiguity is noise — the audits showed
                    # first-seen-ambiguity insta-kills were false kills.
                    if not final_gate_done:
                        fgj = await _run_final_gate(problem_md)
                        if fgj:                # real audit-tier findings: next iteration's ladder
                            pending_gate_gaps = fgj
                            report.gaps_history.append([g.text for g in fgj])
                    if final_gate_clean:
                        baseline_ok.add(_norm_ws(gp.text))
                        ctx.log_event(event="ambiguity_overruled_by_gate",
                                      target=target.id, quote=gp.text[:120])
                        classified = True
                        continue
                    cur_amb.add(gp.text)
                    unres_gaps.append(gp.text)   # A6 gets a disambiguation shot; detail no longer empty
                    continue
                gap_kind = ("implicit-result" if gp.kind == "result"
                            else "implicit-definition")
                e = await _match_gap(ctx, index, label_map, target,
                                     gp.text, gp.where, kind=gap_kind,
                                     present=present)
                if isinstance(e, Edge):
                    if _append_edges(graph, [e]):
                        material = True
                    continue
                if e == "PRESENT":               # the block the \ref points to is already in the package
                    baseline_ok.add(_norm_ws(gp.text))
                    ctx.log_event(event="gap_present_ignored",
                                  target=target.id, quote=gp.text[:120])
                    classified = True
                    continue
                # A term/result concept phrase whose ladder is entirely empty ->
                # baseline knowledge (a symbol is the paper's own notation, whose
                # definition must be found inside the paper, so it does not apply)
                cand = (_baseline_assumable(gp.text)
                        if gp.kind in ("term", "result") else None)
                if cand:
                    baseline_ok.add(_norm_ws(gp.text))
                    report.baseline_assumed.append(cand)
                    ctx.log_event(event="gap_baseline_assumed",
                                  target=target.id, name=cand,
                                  quote=gp.text[:120])
                    classified = True
                else:
                    unres_gaps.append(gp.text)
            prev_ambiguities = cur_amb
        except _Unrepairable as u:
            ctx.add_excluded(target.id, policy, u.reason_code, u.detail)
            return None

        # Excluded details record only genuinely blocking items — appeals
        # classified as benign do not count as unresolved
        last_miss = [m for m in miss if m.invoked_as in unres_miss]
        last_gaps = [g for g in gaps if g.text in unres_gaps]

        # A6 last resort: the ladder is out of moves but unresolved items
        # remain — before excluding, let the audit-tier repairer supply the
        # missing material from the paper (once per package)
        if not material and ctx.cfg.pipeline.repair_agent and not tried_a6 \
                and (unres_miss or unres_gaps):
            tried_a6 = True
            if await _repair_with_a6(ctx, index, graph, target, problem_md,
                                     unres_gaps, unres_miss, flat,
                                     paper_title, field_baseline):
                material = True

        if not material:
            if not unres_miss and not unres_gaps and not real_leaks \
                    and not cur_amb and not pending_gate_gaps:
                # All appeals classified as benign (baseline / already in package
                # / internal derivation) and the package unchanged: re-verifying
                # would only cache-hit the same output and get filtered again ->
                # pass in place, do not burn an iteration. This ship path must
                # clear the final gate too (the Stage-1 audit caught both
                # gate-bypassed packages with fatal findings); gate gaps go to
                # the next iteration's ladder via pending_gate_gaps.
                fg_gaps = await _run_final_gate(problem_md)
                if fg_gaps:
                    pending_gate_gaps = fg_gaps
                    report.gaps_history.append([g.text for g in fg_gaps])
                    continue
                report.self_contained = True
                report.leak_clean = True
                report.sufficiency = True if run_4c else None
                passed = True
                if classified:
                    ctx.log_event(event="verify_pass_by_classification",
                                  target=target.id, iter=it)
                break
            if pending_gate_gaps and not unres_miss and not unres_gaps \
                    and not real_leaks and not cur_amb:
                continue      # gate findings queued: give them their iteration
            # Option-2 appeal court: before the exclusion is written, an
            # audit-tier judge with the full paper reviews the blocking
            # items once per package. Overturned-in-place ships (through
            # the gate); granted material re-enters the repair loop;
            # upheld items stamp the exclusion record.
            if ctx.cfg.pipeline.appeal and not tried_appeal \
                    and (unres_gaps or unres_miss or cur_amb):
                tried_appeal = True
                blocking = list(dict.fromkeys(
                    unres_gaps + unres_miss + sorted(cur_amb)))
                resolved, n_merged, upheld = await _appeal_review(
                    ctx, index, graph, target, problem_md, blocking, flat,
                    paper_title, field_baseline)
                appeal_upheld_items = upheld
                for t in resolved:
                    baseline_ok.add(_norm_ws(t))
                if n_merged:
                    material = True          # rebuild + re-verify below
                elif resolved and not upheld:
                    # fully overturned in place — still must clear the gate
                    fg_gaps = await _run_final_gate(problem_md)
                    if fg_gaps:
                        pending_gate_gaps = fg_gaps
                        report.gaps_history.append([g.text for g in fg_gaps])
                        continue
                    report.self_contained = True
                    report.leak_clean = True
                    report.sufficiency = True if run_4c else None
                    passed = True
                    ctx.log_event(event="appeal_shipped", target=target.id,
                                  policy=policy, resolved=len(resolved))
                    break
            if not material:
                ctx.log_event(event="verify_unrepairable", target=target.id,
                              policy=policy, iter=it)
                break

        # Write back the graph (source=agent4-patch is already on the edges), reassemble
        ctx.write_json("graph/dep_graph.json", graph)
        try:
            problem_md, assembly = await build_package(
                ctx, index, graph, target, policy, removed=removed)
        except PackageExcluded as e:
            ctx.add_excluded(target.id, policy, e.reason_code, e.detail)
            return None
        need_def = set(assembly.get("need_def", []))
        policy_downgraded = policy_downgraded or assembly.get(
            "policy_downgraded", False)
        ctx.path(f"{pkg}/problem.md").write_text(problem_md, encoding="utf-8")
        ctx.write_json(f"{pkg}/assembly.json",
                       dict(assembly, removed=sorted(removed)))
    else:
        # fell off the iteration cap while the final round was still making
        # material repairs — a different situation from "no repair possible"
        # (verify_unrepairable): raising max_verify_iters might converge this one
        iter_capped = True
        ctx.log_event(event="verify_iter_cap", target=target.id, policy=policy,
                      iters=ctx.cfg.pipeline.max_verify_iters)

    if not passed:
        # reason comes from the last iteration's unpassed items (§10.1):
        # 4c still failing -> sufficiency, otherwise self-containment
        if run_4c and last_miss:
            reason = "sufficiency_unresolvable"
            detail = "; ".join(m.invoked_as for m in last_miss[:3])[:300]
        else:
            reason = "self_containment_unresolvable"
            detail = "; ".join(g.text for g in last_gaps[:3])[:300]
        if iter_capped:
            detail = (f"hit max_verify_iters="
                      f"{ctx.cfg.pipeline.max_verify_iters} while still "
                      f"repairing; " + detail)[:300]
        if appeal_upheld_items:
            detail = ("[appeal upheld] " + detail)[:300]
        ctx.add_excluded(target.id, policy, reason,
                         detail or f"{report.iterations} iters")
        return None

    # Ship: deterministic full-text leak scan first — a verbatim proof span in
    # the final problem.md that no granted block's own source text covers is a
    # leak a4b missed; per "better fewer than wrong", exclude instead of ship
    integrity_issues = target_identity_issues(problem_md, target)
    if not target_tex_path.exists() or not target_json_path.exists():
        integrity_issues.append("frozen target artifacts are missing")
    else:
        try:
            target_record = ctx.read_json(f"{pkg}/target.json")
        except (OSError, ValueError, TypeError) as exc:
            integrity_issues.append(f"target.json is unreadable: {exc}")
        else:
            integrity_issues.extend(frozen_target_artifact_issues(
                target,
                target_tex=target_tex_path.read_text(encoding="utf-8"),
                record=target_record))
    if integrity_issues:
        ctx.add_excluded(target.id, policy, "target_integrity_failed",
                         "; ".join(integrity_issues)[:900])
        return None
    leak_spans = ship_leak_spans(index, graph, target, problem_md, assembly)
    if leak_spans:
        ctx.log_event(event="g5_leak_scan_hit", target=target.id,
                      policy=policy, spans=len(leak_spans),
                      sample=leak_spans[0][:160])
        ctx.add_excluded(target.id, policy, "leak_scan_overlap",
                         leak_spans[0][:300])
        return None

    # G5 + write report to disk
    g5_invariants(ctx, problem_md, target.proof_tex or "",
                  report.self_contained, report.leak_clean)
    report.policy_downgraded = policy_downgraded
    cs = assembly.get("closure_size", {})
    report.closure_size = ClosureSize(**cs) if cs else ClosureSize()
    report.input_hashes = {
        "statements": sha256_text(
            ctx.path("index/statements.v2.json").read_text(encoding="utf-8"))[:16],
        "graph": sha256_text(
            ctx.path("graph/dep_graph.json").read_text(encoding="utf-8"))[:16],
        "problem": sha256_text(problem_md),
        "target": target.statement_sha256,
        "reference_proof": target.proof_sha256}
    ctx.write_json(f"{pkg}/report.json", report)
    ctx.log_event(event="package_passed", target=target.id, policy=policy,
                  iters=report.iterations)
    ctx.progress(f"✓ shipped {target.id}/{policy} "
                 f"({report.iterations} iters)")
    return report


# ------------------------------------------------------------------ main flow

async def _run_async(ctx: RunContext) -> None:
    meta = ctx.read_model("source/meta.json", Meta)
    index = ctx.read_model("index/statements.v2.json", StatementsIndex)
    graph = ctx.read_model("graph/dep_graph.json", DepGraph)
    selection = ctx.read_model("roles/selection.json", Selection)
    roles = ctx.read_model("roles/roles.json", Roles)
    by_id = index.by_id()
    flat = ctx.path("source/flat.md" if meta.source_type == "ocr"
                    else "source/flat.tex").read_text(encoding="utf-8")
    source_file = ("source/flat.md" if meta.source_type == "ocr"
                   else "source/flat.tex")

    jobs = []
    for tdir in sorted(ctx.path("packages").iterdir()) \
            if ctx.path("packages").exists() else []:
        if not tdir.is_dir():
            continue
        for pdir in sorted(tdir.iterdir()):
            if (pdir / "problem.md").exists():
                jobs.append((tdir.name, pdir.name))

    # A step7-only rerun re-adjudicates every drafted package: drop stale
    # excluded entries for the (target, policy) pairs about to be verified,
    # otherwise they duplicate/contradict this run's verdicts (step6 clears
    # the whole file, but only on ITS rerun)
    excl_path = ctx.path("excluded.json")
    if excl_path.exists() and jobs:
        job_set = set(jobs)
        items = ctx.read_json("excluded.json")
        kept = [e for e in items
                if (e["target_id"], e.get("policy", "")) not in job_set]
        if len(kept) != len(items):
            ctx.write_json("excluded.json", kept)
            ctx.log_event(event="stale_exclusions_cleared",
                          n=len(items) - len(kept))

    # Verification prompts are the heaviest in the pipeline (whole problem.md,
    # plus the full proof for 4c), so cap concurrent packages at parallel//3
    # to keep the token flood under the account TPM ceiling.
    ctx.progress(f"verifying {len(jobs)} packages "
                 f"(≤{ctx.cfg.pipeline.max_verify_iters} iters each)")
    sem = asyncio.Semaphore(max(1, ctx.cfg.llm.parallel // 3))

    async def one(tid: str, policy: str):
        async with sem:
            try:
                return await _verify_package(ctx, index, graph, by_id[tid],
                                             policy, meta.field_baseline,
                                             flat, source_file, meta.title)
            except Exception as e:
                ctx.add_excluded(tid, policy, "self_containment_unresolvable",
                                 f"verify error: {repr(e)[:300]}")
                return None

    reports = await asyncio.gather(*[one(t, p) for t, p in jobs])

    # manifest aggregation (only includes those that passed verification)
    m_set, h_set = set(selection.mains), set(selection.hardest)
    entries = []
    for (tid, policy), rep in zip(jobs, reports):
        if rep is None:
            continue
        s = by_id[tid]
        role = roles.roles.get(tid)
        sel_as = ("main+hardest" if tid in m_set and tid in h_set
                  else "hardest" if tid in h_set else "main")
        entries.append(PkgEntry(
            target_id=tid, env_type=s.env_type,
            role=role.role if role else "unknown", selected_as=sel_as,
            policy=policy,
            path=f"packages/{tid}/{policy}/problem.md",
            topo_rank=s.order_index, proof_chars=len(s.proof_tex or ""),
            self_contained=True, leak_clean=True))

    excl_path = ctx.path("excluded.json")
    excluded = ctx.read_json("excluded.json") if excl_path.exists() else []
    attempted = {(t, p) for t, p in jobs} | \
        {(e["target_id"], e.get("policy", "")) for e in excluded}
    manifest = Manifest(
        paper_id=ctx.paper_id, paper_date=meta.paper_date,
        packages=entries,
        stats={"statements": len(index.statements),
               "edges": len(graph.edges),
               "targets_attempted": len(attempted),
               "targets_emitted": len(entries)})
    ctx.write_json("manifest.json", manifest)
    ctx.log_event(event="step7_done", emitted=len(entries),
                  attempted=len(jobs))


def run(ctx: RunContext) -> None:
    ctx.step_name = STEP
    run_async(_run_async(ctx))
