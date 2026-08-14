"""Step 4: dependency extraction (§7, LLM = Agent 1, parallel).

Outputs: graph/dep_graph.json, graph/dropped_edges.json, graph/graph.mmd.
"""
from __future__ import annotations

import asyncio
import json

from .common import RunContext, TaskFailed, Rejected
from .graph_utils import (clean_graph, dedupe_edges, export_mmd,
                          mechanical_edges)
from .gates import g4_deps_failed_rate
from .latex_utils import split_paragraph_chunks
from .llm import call_llm, run_async
from .schemas import (A1Out, DepGraph, Edge, ExternalDep, Meta, Statement,
                      StatementsIndex)
from .step3_fill_index import targeted_fill, targeted_prewarm

STEP = "step4"
NEVER_TRUNCATE = {"definition", "inline-definition"}


# --------------------------------------------------------- §7.2 index truncation rules

def build_statement_index(ctx: RunContext, index: StatementsIndex) -> str:
    """Render the one-line-per-statement index fed to A1, degrading through
    the §7.2 ladder (verbatim -> truncate long texts -> also drop remarks/
    examples) until it fits index_char_cap; definitions are never truncated.
    Reject the paper if even the smallest form overflows."""
    cap = ctx.cfg.limits.index_char_cap
    trunc = ctx.cfg.limits.stmt_trunc_chars

    def render(drop_remarks: bool, truncate: bool) -> str:
        lines = []
        for s in index.statements:
            if drop_remarks and s.env_type in ("remark", "example"):
                continue
            text = s.statement_tex
            if truncate and s.env_type not in NEVER_TRUNCATE and len(text) > trunc:
                text = text[:trunc] + " ...[TRUNCATED]"
            text = text.replace("\n", " ")
            lines.append(f"{s.id} | {s.env_type} | {text}")
        return "\n".join(lines)

    for drop, tr in ((False, False), (False, True), (True, True)):
        out = render(drop, tr)
        if len(out) <= cap:
            if (drop, tr) != (False, False):
                ctx.log_event(event="index_truncated", dropped_remarks=drop)
            return out
    raise Rejected("index_overflow", f"statement index > {cap} chars after ladder")


def build_global_context(index: StatementsIndex, section: str) -> str:
    lines = [f"{g.id} | {g.text_tex}" for g in index.global_context
             if g.scope == "paper" or g.scope == f"section:{section}"]
    return "\n".join(lines) if lines else "(none)"


# ------------------------------------------------------------- single-target call

async def call_a1(ctx: RunContext, t: Statement, stmt_index: str,
                  index: StatementsIndex, field_baseline: str) -> A1Out:
    gc = build_global_context(index, t.section)
    mech = "\n".join(t.mechanical_refs) if t.mechanical_refs else "(none)"
    proof = t.proof_tex if t.proof_tex is not None else "NO PROOF GIVEN IN PAPER"

    if len(proof) <= 100_000:
        return await call_llm(ctx, "a1", {
            "field_baseline": field_baseline, "global_context": gc,
            "statement_index": stmt_index, "target_id": t.id,
            "target_statement": t.statement_tex, "target_proof": proof,
            "mechanical_refs": mech})

    # overly long proof (§7.3): split into <=80k chunks, call A1 once per
    # chunk, and union the results
    ctx.log_event(event="proof_chunked", target=t.id, chars=len(proof))
    chunks = split_paragraph_chunks(proof, 80_000)
    merged: A1Out | None = None
    for ch in chunks:
        out = await call_llm(ctx, "a1", {
            "field_baseline": field_baseline, "global_context": gc,
            "statement_index": stmt_index, "target_id": t.id,
            "target_statement": t.statement_tex, "target_proof": ch,
            "mechanical_refs": mech})
        merged = out if merged is None else _union(merged, out)
    assert merged is not None
    return merged


def _union(a: A1Out, b: A1Out) -> A1Out:
    """Field-wise dedup union of two A1 outputs (used for chunked proofs)."""
    def key_sd(d):
        return d.id

    def merge(xs, ys, key):
        seen, out = set(), []
        for x in list(xs) + list(ys):
            k = key(x)
            if k not in seen:
                seen.add(k)
                out.append(x)
        return out

    return A1Out(
        target_id=a.target_id,
        statement_deps=merge(a.statement_deps, b.statement_deps, key_sd),
        proof_deps=merge(a.proof_deps, b.proof_deps, lambda d: (d.id, d.kind)),
        external_deps=merge(a.external_deps, b.external_deps,
                            lambda d: (d.citation_key, d.usage_quote)),
        unresolved=merge(a.unresolved, b.unresolved, lambda d: d.phrase))


# ------------------------------------------------------------- results -> edges

def edges_from_a1(ctx: RunContext, t: Statement, out: A1Out,
                  index: StatementsIndex) -> tuple[list[Edge], list[ExternalDep]]:
    known = {s.id for s in index.statements} | {g.id for g in index.global_context}
    gc_kind = {g.id: g.kind for g in index.global_context}
    edges: list[Edge] = []

    for d in out.statement_deps:
        if d.id not in known:
            ctx.log_event(event="a1_unknown_id", target=t.id, dep=d.id)
            continue
        kind = "standing" if gc_kind.get(d.id) == "standing-assumption" \
            else "implicit-definition"
        edges.append(Edge.model_validate({
            "from": t.id, "to": d.id, "arises_in": "statement", "kind": kind,
            "evidence": d.evidence, "confidence": d.confidence,
            "source": "agent1"}))
    for d in out.proof_deps:
        if d.id not in known:
            ctx.log_event(event="a1_unknown_id", target=t.id, dep=d.id)
            continue
        edges.append(Edge.model_validate({
            "from": t.id, "to": d.id, "arises_in": "proof", "kind": d.kind,
            "evidence": d.evidence, "confidence": d.confidence,
            "source": "agent1"}))

    exts = [ExternalDep(used_by=t.id, citation_key=d.citation_key,
                        usage_quote=d.usage_quote,
                        stated_in_paper=d.stated_in_paper,
                        statement_tex=d.statement_tex,
                        statement_origin="verbatim-from-paper"
                        if d.stated_in_paper else "")
            for d in out.external_deps]
    return edges, exts


# ------------------------------------------------------------------ main flow

async def _run_async(ctx: RunContext) -> None:
    meta = ctx.read_model("source/meta.json", Meta)
    index = ctx.read_model("index/statements.v2.json", StatementsIndex)
    label_map = ctx.read_json("index/label_map.json")
    frozen_ids = {s.id for s in index.statements} | \
        {g.id for g in index.global_context}
    stmt_index = build_statement_index(ctx, index)
    targets = list(index.statements)

    sem = asyncio.Semaphore(ctx.cfg.llm.parallel)
    ctx.progress(f"dependency extraction: {len(targets)} statements")
    n_done = 0

    async def one(t: Statement):
        nonlocal n_done
        async with sem:
            r = await call_a1(ctx, t, stmt_index, index, meta.field_baseline)
        n_done += 1
        ctx.progress(f"a1 {n_done}/{len(targets)} {t.id} "
                     f"({len(r.proof_deps)} proof deps)")
        return r

    results = await asyncio.gather(*[one(t) for t in targets],
                                   return_exceptions=True)

    a1_by_target: dict[str, A1Out] = {}
    first_wave_failed: list[Statement] = []
    for t, res in zip(targets, results):
        if isinstance(res, BaseException):
            first_wave_failed.append(t)
            ctx.log_event(event="a1_failed", target=t.id, err=repr(res)[:300])
        else:
            a1_by_target[t.id] = res

    # trailing serial retry round: once the parallel flood subsides the TPM
    # window refills, so a target whose 429 retries were exhausted usually
    # recovers in a single serial attempt
    deps_failed: list[str] = []
    for t in first_wave_failed:
        try:
            a1_by_target[t.id] = await call_a1(ctx, t, stmt_index, index,
                                               meta.field_baseline)
            ctx.log_event(event="a1_retry_recovered", target=t.id)
        except Exception as e:
            deps_failed.append(t.id)
            ctx.log_event(event="a1_failed_final", target=t.id,
                          err=repr(e)[:300])

    # §7.6(2): unresolved non-empty -> targeted index-fill -> re-run A1 for
    # that target once. Three phases: (1) pre-warm the a0 cache for every
    # phrase in parallel — the fill prompt depends only on flat text + phrase;
    # (2) merge serially in target order, replaying from cache, so backfilled
    # ids/order_index stay deterministic; (3) re-run A1 in parallel against
    # the fully enriched index.
    index_changed = False
    retry_targets = [t for t in targets
                     if t.id in a1_by_target and a1_by_target[t.id].unresolved]
    seen_ph: set[str] = set()
    phrases = [u.phrase for t in retry_targets
               for u in a1_by_target[t.id].unresolved
               if not (u.phrase in seen_ph or seen_ph.add(u.phrase))]

    async def prewarm(ph: str) -> None:
        async with sem:
            await targeted_prewarm(ctx, ph)

    if phrases:
        ctx.progress(f"targeted fill: pre-warming {len(phrases)} phrases for "
                     f"{len(retry_targets)} targets in parallel")
        await asyncio.gather(*[prewarm(p) for p in phrases])

    rerun_queue: list[Statement] = []
    for t in retry_targets:
        added: list[str] = []
        for u in a1_by_target[t.id].unresolved:
            added += await targeted_fill(ctx, index, u.phrase)
        if added:
            index_changed = True
            rerun_queue.append(t)

    if rerun_queue:
        new_stmt_index = build_statement_index(ctx, index)

        async def rerun_one(t: Statement) -> None:
            try:
                async with sem:
                    a1_by_target[t.id] = await call_a1(
                        ctx, t, new_stmt_index, index, meta.field_baseline)
            except (TaskFailed, Exception) as e:  # keep old result if re-run fails
                ctx.log_event(event="a1_retry_failed", target=t.id,
                              err=repr(e)[:200])
            still = [u.phrase for u in a1_by_target[t.id].unresolved]
            if still:
                ctx.log_event(event="unresolved_kept", target=t.id,
                              phrases=still)

        await asyncio.gather(*[rerun_one(t) for t in rerun_queue])
    if index_changed:
        ctx.write_json("index/statements.v2.json", index)

    # build and clean the graph (§7.6)
    edges: list[Edge] = mechanical_edges(index, label_map)
    externals: list[ExternalDep] = []
    for t in targets:
        out = a1_by_target.get(t.id)
        if out is None:
            continue
        es, xs = edges_from_a1(ctx, t, out, index)
        edges += es
        externals += xs
    edges, dropped = clean_graph(ctx, edges, index, frozen_ids)

    graph = DepGraph(edges=edges, external_deps=externals,
                     deps_failed=deps_failed)
    ctx.write_json("graph/dep_graph.json", graph)
    ctx.write_json("graph/dropped_edges.json", [d for d in dropped])
    export_mmd(ctx, graph)

    degraded = g4_deps_failed_rate(ctx, graph, len(targets))   # G4
    ctx.write_json("graph/g4_degraded.json", {"degraded": degraded})
    unresolved_total = sum(len(o.unresolved) for o in a1_by_target.values())
    ctx.log_event(event="step4_done", edges=len(edges),
                  dropped=len(dropped), failed=len(deps_failed),
                  unresolved=unresolved_total)


def run(ctx: RunContext) -> None:
    ctx.step_name = STEP
    run_async(_run_async(ctx))
