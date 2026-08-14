"""Step 3: index completion (§6, LLM = Agent 0).

Output: index/statements.v2.json (v1 + new statements + proof-link completion).
Also exports targeted_fill(): the targeted index-fill of §7.6(2) / §10.3(4)
reuses the same merge logic.
"""
from __future__ import annotations

import asyncio
import re

from .common import RunContext, sha256_text
from .latex_utils import split_paragraph_chunks
from .llm import call_llm, run_async
from .schemas import (A0Out, GlobalItem, Meta, Statement, StatementsIndex)
from .step2_parse import ENV_ALIASES, resolve_hint
from .target_integrity import context_statement_id

STEP = "step3"

CANONICAL_ENVS = {"theorem", "lemma", "proposition", "corollary", "definition",
                  "inline-definition", "assumption", "remark", "example",
                  "equation"}
EXTRA_ALIASES = dict(ENV_ALIASES, claim="proposition", notation="inline-definition")


def _normalize_env(env_type: str) -> str:
    e = (env_type or "").strip().lower()
    if e in CANONICAL_ENVS:
        return e
    return EXTRA_ALIASES.get(e, "inline-definition")


def _norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------- merge logic §6.3

def _locate(flat: str, after_text: str, text_tex: str) -> int:
    """Anchor position of a new A0 statement in flat; -1 = unlocatable (discard)."""
    if after_text:
        p = flat.find(after_text)
        if p >= 0:
            return p + len(after_text)
    probe = text_tex[:50].strip()
    if probe:
        p = flat.find(probe)
        if p >= 0:
            return p
    probe2 = _norm_ws(text_tex)[:40]
    if probe2:                                   # lenient: retry after collapsing whitespace
        p = _norm_ws(flat).find(probe2)
        if p >= 0:
            # scale the position from normalized text back to raw text — an
            # estimate is fine, the anchor only drives relative ordering
            return int(p * len(flat) / max(1, len(_norm_ws(flat))))
    return -1


def _is_duplicate(text_tex: str, index: StatementsIndex) -> bool:
    """Bidirectional-containment dedup (§6.3 item 2)."""
    t = _norm_ws(text_tex)
    if not t:
        return True
    for s in index.statements:
        e = _norm_ws(s.statement_tex)
        if t in e or e in t:
            return True
    for g in index.global_context:
        e = _norm_ws(g.text_tex)
        if t in e or e in t:
            return True
    return False


def _is_proof_fragment(text_tex: str, index: StatementsIndex) -> bool:
    """Candidate text sits inside some statement's proof body -> an A0
    mis-extraction, not a definition (the typical failure mode of targeted
    index-fill treating a proof sentence as an inline definition)."""
    t = _norm_ws(text_tex)
    if not t:
        return False
    for s in index.statements:
        if s.proof_tex and t in _norm_ws(s.proof_tex):
            return True
    return False


def _next_gc_seq(index: StatementsIndex) -> int:
    mx = 0
    for g in index.global_context:
        mo = re.match(r"gc-(\d+)$", g.id)
        if mo:
            mx = max(mx, int(mo.group(1)))
    return mx + 1


def merge_a0(ctx: RunContext, index: StatementsIndex, out: A0Out, flat: str,
             section_id: str, added_by: str = "agent0") -> list[str]:
    """Merge one A0 output into index (in place); returns the new statement ids.

    order_index initially holds the anchor position as a placeholder;
    _finalize_order turns it into a real rank (append mode shifts it to max+1
    instead, see targeted_fill).
    """
    from .latex_utils import section_of, section_positions
    marks = section_positions(flat)
    new_ids: list[str] = []
    for ns in out.new_statements:
        if len(ns.text_tex.strip()) < 20:            # junk-statement lower bound (better to omit than to err)
            ctx.log_event(event="a0_drop_too_short", text=ns.text_tex[:40])
            continue
        anchor = _locate(flat, ns.after_text, ns.text_tex)
        if anchor < 0:
            ctx.log_event(event="a0_drop_unlocated", text=ns.text_tex[:80])
            continue
        if _is_duplicate(ns.text_tex, index):
            ctx.log_event(event="a0_drop_duplicate", text=ns.text_tex[:60])
            continue
        if _is_proof_fragment(ns.text_tex, index):
            # Repair-first policy: pure definition/notation material living in
            # proof prose is admissible — papers introduce coupling variables
            # and shorthand mid-proof (2606.19639's $x_t^\infty$, "the spaces
            # are Polish"), and refusing them structurally killed those
            # targets. Deductive claims from proofs stay rejected; result-type
            # grants from the target's own proof are additionally filtered at
            # assembly by grants_from_target.
            defgrade = ((ns.kind or "").strip().lower()
                        in ("notation", "standing-assumption")
                        or (ns.env_type or "").strip().lower()
                        in ("inline-definition", "definition"))
            if not defgrade:
                ctx.log_event(event="a0_drop_proof_fragment",
                              text=ns.text_tex[:60])
                continue
            ctx.log_event(event="proof_prose_definition_admitted",
                          text=ns.text_tex[:80])
        item_section = (section_of(anchor, marks)
                        if section_id == "targeted" else section_id)
        kind = (ns.kind or "").strip().lower()
        if kind in ("notation", "standing-assumption"):
            scope = ns.scope.strip() if re.fullmatch(
                r"paper|section:[0-9A-Za-z]+", ns.scope.strip() or "") else "paper"
            gid = f"gc-{_next_gc_seq(index)}"
            index.global_context.append(GlobalItem(
                id=gid, kind=kind, scope=scope, text_tex=ns.text_tex,
                added_by=added_by))
            new_ids.append(gid)
            continue
        env = _normalize_env(ns.env_type)
        sid = context_statement_id(
            paper_id=index.paper_id, added_by=added_by, env_type=env,
            statement_tex=ns.text_tex,
            used_ids={statement.id for statement in index.statements})
        st = Statement(id=sid, env_type=env, latex_label="",
                       display_name="", section=item_section,
                       order_index=10 ** 9 + anchor,   # placeholder, reordered in finalize
                       statement_tex=ns.text_tex, proof_tex=None,
                       proof_location="omitted", mechanical_refs=[],
                       uses_figure="[FIGURE-" in ns.text_tex, added_by=added_by)
        index.statements.append(st)
        new_ids.append(sid)
    return new_ids


def _resolve_proof_links(ctx: RunContext, index: StatementsIndex, out: A0Out,
                         label_map: dict, flat: str,
                         source_file: str) -> None:
    """Recover only source proofs whose own heading has an explicit label."""
    p_orph = ctx.path("index/orphan_proofs.json")
    if not p_orph.exists():
        return
    orphans = ctx.read_json("index/orphan_proofs.json")
    remaining = list(orphans)
    for link in out.proof_links:
        probe = link.proof_first_30_chars.strip()
        if not probe:
            continue
        hit = next((o for o in remaining
                    if _norm_ws(o["body"]).startswith(_norm_ws(probe)[:25])), None)
        if hit is None:
            continue
        # The model may locate an orphan by its opening text, but it cannot
        # choose the owner. Ownership comes only from the proof's source
        # heading, which must contain an unambiguous explicit label.
        target = resolve_hint(hit.get("of_text", ""),
                              index.statements, label_map)
        if target is None or target.proof_tex is not None:
            continue
        start, end = hit.get("pos", -1), hit.get("end", -1)
        if not isinstance(start, int) or not isinstance(end, int) \
                or not (0 <= start < end <= len(flat)):
            continue
        source_slice = flat[start:end]
        if hit["body"] not in source_slice:
            continue
        target.proof_tex = hit["body"]
        target.proof_location = (f"appendix:{hit['section']}"
                                 if str(hit["section"]).isalpha() else "inline")
        target.proof_sha256 = sha256_text(hit["body"])
        target.proof_source_file = source_file
        target.proof_source_start = start
        target.proof_source_end = end
        target.proof_source_sha256 = sha256_text(source_slice)
        target.proof_source_verified = True
        target.proof_pairing = "explicit-label-recovery"
        if "[FIGURE-" in hit["body"]:
            target.uses_figure = True
        remaining.remove(hit)
        ctx.log_event(event="proof_link_resolved", target=target.id)
    ctx.write_json("index/orphan_proofs.json", remaining)


def _finalize_order(index: StatementsIndex, flat: str) -> None:
    """Recompute order_index once (§6.3 item 5); frozen thereafter.

    Existing statements are located by a monotonic scan through flat in their
    original order; new statements reuse the anchor kept in the placeholder.
    """
    pos_map: dict[str, int] = {}
    cursor = 0
    for s in sorted(index.statements, key=lambda x: x.order_index):
        if s.order_index >= 10 ** 9:                 # new statement: restore the anchor
            pos_map[s.id] = s.order_index - 10 ** 9
            continue
        probe = s.statement_tex[:40]
        p = flat.find(probe, cursor) if probe else -1
        if p < 0:
            p = flat.find(probe) if probe else -1
        if p < 0:
            p = cursor
        pos_map[s.id] = p
        cursor = max(cursor, p)
    index.statements.sort(key=lambda s: (pos_map[s.id], s.id))
    for oi, s in enumerate(index.statements):
        s.order_index = oi


# ------------------------------------------------------------------ main flow

def _sections_of(flat: str, meta: Meta) -> list[tuple[str, str]]:
    """[(section_id, text)]; section 0 = from after \\begin{document} up to the first section."""
    from .latex_utils import section_positions
    body_start = flat.find("\\begin{document}")
    start = body_start if body_start >= 0 else 0
    marks = section_positions(flat)
    marks = [(p, sid) for p, sid in marks if p >= start]
    out = []
    if not marks:
        return [("0", flat[start:])]
    if marks[0][0] > start:
        out.append(("0", flat[start:marks[0][0]]))
    for i, (p, sid) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(flat)
        out.append((sid, flat[p:end]))
    return out


def _already_extracted_lines(index: StatementsIndex, sec: str) -> str:
    lines = [f"{s.id} | {s.env_type} | {s.statement_tex[:80]}"
             for s in index.statements if s.section == sec]
    return "\n".join(lines) if lines else "(nothing)"


async def _run_async(ctx: RunContext) -> None:
    meta = ctx.read_model("source/meta.json", Meta)
    flat = ctx.path("source/flat.md" if meta.source_type == "ocr"
                    else "source/flat.tex").read_text(encoding="utf-8")
    source_file = ("source/flat.md" if meta.source_type == "ocr"
                   else "source/flat.tex")
    index = ctx.read_model("index/statements.v1.json", StatementsIndex)
    label_map = ctx.read_json("index/label_map.json")
    cap = ctx.cfg.limits.section_chunk_chars

    jobs = []
    for sec, text in _sections_of(flat, meta):
        for chunk in split_paragraph_chunks(text, cap):
            jobs.append((sec, chunk))

    sem = asyncio.Semaphore(ctx.cfg.llm.parallel)
    STANDING_SIGNAL = re.compile(r"(?i)\bthroughout\b|\bwe (assume|suppose)\b")
    NOTATION_SIGNAL = re.compile(r"(?i)\bwe (write|denote)\b|\bstands? for\b")
    ctx.progress(f"index fill: {len(jobs)} section chunks")
    n_done = 0

    async def one(sec: str, chunk: str):
        nonlocal n_done
        async with sem:
            out = await call_llm(ctx, "a0", {
                "section_id": sec, "section_latex": chunk,
                "already_extracted": _already_extracted_lines(index, sec),
                "extra_instruction": ""})
            # deterministic re-extraction trigger: the chunk carries a literal
            # signal for a global-convention kind that A0's output lacks ->
            # retry once with a hint. Judged per kind separately, to hedge
            # against extraction variance.
            kinds = {(ns.kind or "").strip().lower() for ns in out.new_statements}
            need = (("standing-assumption" not in kinds
                     and STANDING_SIGNAL.search(chunk))
                    or ("notation" not in kinds and NOTATION_SIGNAL.search(chunk)))
            if need:
                retry = await call_llm(ctx, "a0", {
                    "section_id": sec, "section_latex": chunk,
                    "already_extracted": _already_extracted_lines(index, sec),
                    "extra_instruction":
                        "This section appears to introduce global conventions. "
                        "Sentences like \"Throughout this paper, we assume "
                        "...\" are STANDING ASSUMPTIONS; sentences like \"We "
                        "write X for ...\" are NOTATION. Extract every one "
                        "you can find."})
                out.new_statements.extend(retry.new_statements)
                out.proof_links.extend(retry.proof_links)
            n_done += 1
            ctx.progress(f"a0 {n_done}/{len(jobs)} section {sec} "
                         f"(+{len(out.new_statements)} candidates)")
            return out

    results = await asyncio.gather(*[one(s, c) for s, c in jobs],
                                   return_exceptions=True)
    for (sec, _chunk), res in zip(jobs, results):
        if isinstance(res, BaseException):        # skip this section and log a warning
            ctx.log_event(event="a0_section_failed", section=sec,
                          err=repr(res)[:300], level="warning")
            continue
        merge_a0(ctx, index, res, flat, sec)
        _resolve_proof_links(ctx, index, res, label_map, flat, source_file)

    _deterministic_gc_fallback(ctx, index, flat)
    _finalize_order(index, flat)
    ctx.write_json("index/statements.v2.json", index)
    ctx.log_event(event="step3_done", statements=len(index.statements),
                  global_context=len(index.global_context))


THROUGHOUT_RE = re.compile(r"\bThroughout\b[^.]{10,350}\.")


def _deterministic_gc_fallback(ctx: RunContext, index: StatementsIndex,
                               flat: str) -> None:
    """Last, purely deterministic line of defense for global conventions.

    A "Throughout ..." sentence in the source is the strongest literal signal
    of a standing assumption; capture it verbatim whenever A0 (even with the
    hinted retry) missed it — gpt-4.1 at temp=0 still varies across calls, so
    the retry hedge is not 100%. The costs are asymmetric: over-capture is
    ~free (gc is verbatim source text, at worst one throwaway sentence gets
    granted), while under-capture means a package missing a standing
    assumption. "Throughout the proof ..." sentences inside proofs are skipped."""
    from .schemas import GlobalItem
    for mo in THROUGHOUT_RE.finditer(flat):
        sent = _norm_ws(mo.group(0))
        if _is_proof_fragment(sent, index):
            continue
        key = sent[:60].casefold()
        if any(key in _norm_ws(g.text_tex).casefold()
               or _norm_ws(g.text_tex).casefold()[:60] in sent.casefold()
               for g in index.global_context):
            continue
        gid = f"gc-{_next_gc_seq(index)}"
        index.global_context.append(GlobalItem(
            id=gid, kind="standing-assumption", scope="paper",
            text_tex=mo.group(0).strip(), added_by="agent0"))
        ctx.log_event(event="gc_deterministic_fallback", id=gid,
                      text=sent[:80])


def run(ctx: RunContext) -> None:
    ctx.step_name = STEP
    run_async(_run_async(ctx))


# --------------------------------------------- targeted index-fill (§7.6(2) / §10.3(4))

def _pseudo_section(ctx: RunContext, flat: str, phrase: str) -> str:
    """Grep flat for the paragraphs containing phrase (±1 neighbor) and stitch
    them into a pseudo-section. Empty string when the phrase greps nothing."""
    paras = re.split(r"\n\s*\n", flat)
    hits = [i for i, p in enumerate(paras) if phrase and phrase in p]
    if not hits:
        norm_phrase = _norm_ws(phrase)
        hits = [i for i, p in enumerate(paras) if norm_phrase in _norm_ws(p)]
    if not hits:
        return ""
    if len(hits) > 3:
        # a high-frequency symbol (e.g. \Gamma) hits a great many paragraphs
        # and the pseudo-section would get truncated arbitrarily; prefer the
        # definitional paragraphs (phrase followed closely by a defining verb
        # or :=)
        defpat = re.compile(
            re.escape(phrase) + r"[^.\n]{0,60}?(?:denotes?|stands?\s+for|"
            r"is\s+(?:the|an?|defined)|:=|\\coloneqq|we\s+(?:write|denote|"
            r"define|say))")
        dhits = [i for i in hits if defpat.search(paras[i])]
        if dhits:
            hits = dhits
    keep = sorted({j for i in hits for j in (i - 1, i, i + 1)
                   if 0 <= j < len(paras)})
    return "\n\n".join(paras[j] for j in keep)[
        :ctx.cfg.limits.section_chunk_chars]


def _read_flat(ctx: RunContext) -> str:
    meta = ctx.read_model("source/meta.json", Meta)
    return ctx.path("source/flat.md" if meta.source_type == "ocr"
                    else "source/flat.tex").read_text(encoding="utf-8")


async def _targeted_a0(ctx: RunContext, pseudo: str, phrase: str) -> A0Out:
    return await call_llm(ctx, "a0", {
        "section_id": "targeted", "section_latex": pseudo,
        "already_extracted": "(nothing)",
        "extra_instruction":
            f'Pay special attention to where "{phrase}" is introduced.'})


async def targeted_prewarm(ctx: RunContext, phrase: str) -> None:
    """Cache pre-warmer so callers can parallelize fill batches: runs only the
    A0 call — its prompt depends on flat text + phrase alone, never on index
    state — and a subsequent serial targeted_fill replays it from cache.
    No index mutation, no merge logging; errors are swallowed here and
    surface in the serial pass, which retries live and logs properly."""
    pseudo = _pseudo_section(ctx, _read_flat(ctx), phrase)
    if not pseudo:
        return
    try:
        await _targeted_a0(ctx, pseudo, phrase)
    except Exception:
        pass


async def targeted_fill(ctx: RunContext, index: StatementsIndex, phrase: str,
                        added_by: str = "agent0") -> list[str]:
    """Grep flat for the paragraphs containing phrase (±1 neighbor), stitch
    them into a pseudo-section, and run A0 on it.

    New statements are appended to index in place with order_index shifted to
    max+1 — existing entries are never reordered once v2 is frozen. Returns
    the new statement ids; the caller writes index back to statements.v2.json.
    """
    flat = _read_flat(ctx)
    pseudo = _pseudo_section(ctx, flat, phrase)
    if not pseudo:
        return []

    try:
        out = await _targeted_a0(ctx, pseudo, phrase)
    except Exception as e:
        ctx.log_event(event="targeted_fill_failed", phrase=phrase[:80],
                      err=repr(e)[:200])
        return []

    new_ids = merge_a0(ctx, index, out, flat, "targeted", added_by=added_by)
    # append mode: order_index shifts to the tail; existing statements are
    # never reordered (§3.2 convention)
    nxt = max((s.order_index for s in index.statements
               if s.order_index < 10 ** 9), default=-1) + 1
    for s in index.statements:
        if s.order_index >= 10 ** 9:
            s.order_index = nxt
            nxt += 1
    return new_ids
