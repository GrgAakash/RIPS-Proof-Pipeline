"""Step 5: main-theorem extraction (§8). Program signals + LLM nomination + deterministic consensus.

Output: roles/selection.json (the sole source of Step 6 targets), roles/roles.json (pure metadata).
"""
from __future__ import annotations

from .common import RunContext, TaskFailed
from .gates import g6_no_main
from .graph_utils import compute_signals, eligible_ids
from .latex_utils import extract_env_block
from .llm import call_llm, run_async
from .schemas import (A2Out, DepGraph, Meta, Nominee, RejectedTarget,
                      RoleEntry, Roles, Selection, SignalSet, StatementsIndex)
from .step3_fill_index import _sections_of
from .step4_deps import build_statement_index

STEP = "step5"


def _abstract_and_intro(ctx: RunContext, meta: Meta) -> tuple[str, str]:
    flat = ctx.path("source/flat.md" if meta.source_type == "ocr"
                    else "source/flat.tex").read_text(encoding="utf-8")
    blk = extract_env_block(flat, "abstract")
    abstract = blk[2] if blk else ""
    secs = dict(_sections_of(flat, meta))
    intro = secs.get("1", secs.get("0", ""))
    return abstract[:20_000], intro[:60_000]


def _consensus(ctx: RunContext, elig: list[str], signals: dict[str, SignalSet],
               a2: A2Out | None, cap: int) -> tuple[list[str], str, list[RejectedTarget]]:
    """§8.3 consensus + §8.4 fallback ladder. Returns (mains, selector, rejected)."""
    L_det = [t for t in elig
             if signals[t].S1 and (signals[t].S3 or signals[t].S4)]

    rejected: list[RejectedTarget] = []
    if a2 is not None:
        nominated = [m.id for m in a2.main_results if m.id in elig]
        mains = [t for t in nominated
                 if t in L_det or signals[t].S3 or signals[t].S4 or signals[t].S2]
        for t in elig:
            if t not in nominated:
                rejected.append(RejectedTarget(id=t, reason="not_nominated"))
            elif t not in mains:
                rejected.append(RejectedTarget(id=t, reason="no_confirming_signal"))
        if mains:
            if len(mains) > cap:
                ranked = sorted(mains, key=lambda t: (
                    signals[t].S4, signals[t].S3, signals[t].S2,
                    signals[t].S5, signals[t].S6), reverse=True)
                cut = set(ranked[cap:])
                for t in mains:
                    if t in cut:
                        rejected.append(RejectedTarget(id=t, reason="over_cap"))
                mains = [t for t in ranked[:cap]]
            return mains, "consensus", rejected

    # §8.4 fallback ladder (A2 failed or consensus is empty)
    rejected = [r for r in rejected if r.reason != "no_confirming_signal"] \
        if a2 is None else rejected
    if L_det:
        mains = sorted(L_det, key=lambda t: (signals[t].S4, signals[t].S2),
                       reverse=True)[:min(2, len(L_det))]
        return mains, "fallback-1", rejected
    sinks = [t for t in elig if signals[t].S1]
    if sinks:
        mains = sorted(sinks, key=lambda t: signals[t].closure,
                       reverse=True)[:2]
        return mains, "fallback-2", rejected
    if elig:
        mains = sorted(elig, key=lambda t: signals[t].proof_len,
                       reverse=True)[:1]
        return mains, "fallback-3", rejected
    return [], "fallback-3", rejected


def _difficulty(elig: list[str], signals: dict[str, SignalSet],
                a2: A2Out | None, order: dict[str, int],
                n_hardest: int) -> tuple[list[str], dict[str, int]]:
    """Hardest theorem: deterministic difficulty score = sum of rank points over
    three proxy metrics (proof length, dependency closure, chain depth), with A2's
    hardest nomination as a fixed-value bonus (the LLM can only add points, not veto,
    same philosophy as the main-theorem consensus). Returns (top-N ids by descending
    score, score table over all eligible)."""
    if not elig or n_hardest <= 0:
        return [], {}
    n = len(elig)

    def rank_points(metric) -> dict[str, int]:
        ordered = sorted(elig, key=metric, reverse=True)
        return {t: n - i for i, t in enumerate(ordered)}

    p_proof = rank_points(lambda t: signals[t].proof_len)
    p_clo = rank_points(lambda t: signals[t].closure)
    p_chain = rank_points(lambda t: signals[t].chain)
    a2_hard = set(a2.hardest) if a2 is not None else set()
    # bonus ≈ half the field: enough to lift a mid-ranked nominee, never
    # enough to overturn the three deterministic metrics on its own
    bonus = (n + 1) // 2
    score = {t: p_proof[t] + p_clo[t] + p_chain[t]
             + (bonus if t in a2_hard else 0) for t in elig}
    ranked = sorted(elig, key=lambda t: (score[t], signals[t].proof_len,
                                         -order.get(t, 0)), reverse=True)
    return ranked[:n_hardest], score


def _backfill(ctx: RunContext, mains: list[str], elig: list[str],
              signals: dict[str, SignalSet], a2: A2Out | None,
              sections: dict[str, str], order: dict[str, int],
              min_mains: int, cap: int) -> list[str]:
    """Deterministic backfill: when mains fall short of min_main_theorems, fill up
    the ladder (take all if eligible is insufficient). Order: (1) A2-nominated but
    unendorsed, by nomination order; (2) the remaining eligible, sorted by
    (S3, S4, S2, S5, S6, main-body section first, whole-document order)."""
    want = min(min_mains, len(elig), cap)
    if len(mains) >= want:
        return []
    picked = list(mains)
    backfilled: list[str] = []

    def add(t: str):
        if t not in picked and len(picked) < want:
            picked.append(t)
            backfilled.append(t)

    if a2 is not None:                        # (1) nomination order takes priority
        for m in a2.main_results:
            if m.id in elig:
                add(m.id)

    def score(t: str):                        # (2) signal ladder
        s = signals[t]
        in_main_body = sections.get(t, "").isdigit()
        return (s.S3, s.S4, s.S2, s.S5, s.S6, in_main_body, -order.get(t, 0))

    for t in sorted(elig, key=score, reverse=True):
        add(t)
    mains += backfilled
    if backfilled:
        ctx.log_event(event="mains_backfilled", added=backfilled)
    return backfilled


async def _run_async(ctx: RunContext) -> None:
    meta = ctx.read_model("source/meta.json", Meta)
    index = ctx.read_model("index/statements.v2.json", StatementsIndex)
    graph = ctx.read_model("graph/dep_graph.json", DepGraph)

    abstract, intro = _abstract_and_intro(ctx, meta)
    # S4's preview scan covers abstract + intro (a name-drop in the abstract
    # is the strongest author signal)
    signals = compute_signals(index, graph, ctx.cfg,
                              abstract + "\n\n" + intro)
    elig = [i for i in eligible_ids(index, graph, ctx.cfg)]
    elig.sort(key=lambda i: index.by_id()[i].order_index)

    graph_stats = "\n".join(
        f"{i} | used_by={signals[i].used_by} | closure={signals[i].closure} | "
        f"chain={signals[i].chain} | S3={signals[i].S3} | S4={signals[i].S4}"
        for i in elig) or "(no eligible statements)"

    a2: A2Out | None = None
    if elig:
        try:
            a2 = await call_llm(ctx, "a2", {
                "abstract": abstract, "introduction": intro,
                "statement_index": build_statement_index(ctx, index),
                "graph_stats": graph_stats})
        except (TaskFailed, Exception) as e:       # §8.5: whole-step failure goes to fallback
            ctx.log_event(event="a2_failed", err=repr(e)[:300])
            a2 = None

    mains, selector, rejected = _consensus(
        ctx, elig, signals, a2, ctx.cfg.pipeline.max_main_theorems)

    by_id = index.by_id()
    sections = {i: by_id[i].section for i in elig}
    order = {i: by_id[i].order_index for i in elig}
    backfilled = _backfill(ctx, mains, elig, signals, a2, sections, order,
                           ctx.cfg.pipeline.min_main_theorems,
                           ctx.cfg.pipeline.max_main_theorems)
    rejected = [r for r in rejected if r.id not in set(backfilled)]
    g6_no_main(ctx, mains)                          # G6

    hardest, difficulty = _difficulty(elig, signals, a2, order,
                                      ctx.cfg.pipeline.hardest_theorems)
    if hardest:
        ctx.log_event(event="hardest_selected", hardest=hardest,
                      overlap=[t for t in hardest if t in set(mains)])

    selection = Selection(
        mains=mains, hardest=hardest, difficulty=difficulty,
        selector=selector, signals=signals,
        llm_nominees=[Nominee(id=m.id, why=m.why)
                      for m in (a2.main_results if a2 else [])],
        rejected=rejected, backfilled=backfilled)
    ctx.write_json("roles/selection.json", selection)

    if a2 is not None:
        roles = Roles(
            roles={r.id: RoleEntry(role=r.role, signals=r.signals,
                                   rationale=r.rationale) for r in a2.roles},
            storyline=a2.storyline, anomalies=a2.anomalies)
    else:
        roles = Roles(roles={i: RoleEntry(role="unknown") for i in elig},
                      storyline="", anomalies=[])
    ctx.write_json("roles/roles.json", roles)
    ctx.log_event(event="step5_done", mains=mains, selector=selector)


def run(ctx: RunContext) -> None:
    ctx.step_name = STEP
    run_async(_run_async(ctx))
