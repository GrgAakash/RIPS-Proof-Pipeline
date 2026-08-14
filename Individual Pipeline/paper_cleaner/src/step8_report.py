"""Step 8: human-readable artifacts (visualization + A5 selection rationale). Modifies no machine artifact.

Output (idempotent regeneration):
  graph/dep_graph.html            interactive dependency graph (vis-network, CDN)
  report/dashboard.html           pipeline funnel / signals / verification-result dashboard
  packages/SELECTION_RATIONALE.md A5 English selection rationale + deterministic signal appendix

A5 is a pure human-readable-document writer: its failure does not fail the paper, it falls back to a purely deterministic appendix.
"""
from __future__ import annotations

import html
import json

from .common import RunContext, TaskFailed
from .llm import call_llm, run_async
from .schemas import (DepGraph, Manifest, Meta, Roles, Selection,
                      StatementsIndex)

STEP = "step8"

ENV_COLOR = {
    "theorem": "#6366f1", "lemma": "#10b981", "proposition": "#06b6d4",
    "corollary": "#8b5cf6", "definition": "#ec4899",
    "inline-definition": "#f9a8d4", "assumption": "#f59e0b",
    "equation": "#94a3b8", "remark": "#d1d5db", "example": "#d1d5db",
}


def _esc(s: str, n: int = 0) -> str:
    if n:
        s = s[:n] + ("…" if len(s) > n else "")
    return html.escape(s, quote=True)


# ------------------------------------------------------- dependency graph HTML

GRAPH_TMPL = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>__TITLE__ — dependency graph</title>
<script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
<style>
 body{margin:0;font-family:system-ui,-apple-system,sans-serif;background:#0f172a;color:#e2e8f0}
 #bar{padding:10px 18px;background:#1e293b;display:flex;gap:18px;align-items:baseline;flex-wrap:wrap}
 #bar h1{font-size:15px;margin:0;font-weight:600}
 #bar .sub{color:#94a3b8;font-size:12px}
 .lg{display:inline-flex;align-items:center;gap:5px;font-size:11px;color:#cbd5e1}
 .dot{width:10px;height:10px;border-radius:50%;display:inline-block}
 #net{width:100vw;height:calc(100vh - 46px)}
</style></head><body>
<div id="bar"><h1>__TITLE__</h1><span class="sub">__SUBTITLE__</span>__LEGEND__</div>
<div id="net"></div>
<script>
 const nodes = new vis.DataSet(__NODES__);
 const edges = new vis.DataSet(__EDGES__);
 const net = new vis.Network(document.getElementById('net'), {nodes, edges}, {
   physics: {barnesHut: {gravitationalConstant: -5000, springLength: 130,
             avoidOverlap: 0.4}, stabilization: {iterations: 250}},
   nodes: {font: {color: '#e2e8f0', size: 13}, borderWidth: 1.5},
   edges: {arrows: {to: {enabled: true, scaleFactor: 0.55}},
           smooth: {type: 'continuous'}, width: 1.2},
   interaction: {hover: true, tooltipDelay: 120}
 });
 net.once('stabilizationIterationsDone', () => net.setOptions({physics: false}));
</script></body></html>
"""


def _graph_html(ctx: RunContext, index: StatementsIndex, graph: DepGraph,
                sel: Selection, emitted: set[str], meta: Meta) -> None:
    m_set, h_set = set(sel.mains), set(sel.hardest)
    nodes, node_ids = [], set()
    for s in index.statements:
        label = s.id
        marks = ""
        if s.id in m_set:
            marks += " ★"
        if s.id in h_set:
            marks += " ⚡"
        if s.id in emitted:
            marks += " ✓"
        tip = (f"<b>{_esc(s.id)}</b><br>{_esc(s.env_type)}"
               + (f" — {_esc(s.display_name)}" if s.display_name else "")
               + f"<br>section {_esc(s.section)}<br><i>"
               + _esc(s.statement_tex, 260) + "</i>")
        node = {"id": s.id, "label": label + marks, "title": tip,
                "color": {"background": ENV_COLOR.get(s.env_type, "#64748b"),
                          "border": "#334155"},
                "value": max(6, min(40, len(s.proof_tex or "") // 150))}
        if s.id in m_set or s.id in h_set:
            node["borderWidth"] = 4
            node["color"]["border"] = ("#a855f7" if s.id in m_set and s.id in h_set
                                       else "#f59e0b" if s.id in m_set
                                       else "#ef4444")
        nodes.append(node)
        node_ids.add(s.id)
    # gc ids always pass the edge endpoint filter below, but a gc node is
    # only drawn when some edge actually references it (used_gc)
    for g in index.global_context:
        node_ids.add(g.id)
    used_gc = {e.to for e in graph.edges if e.to.startswith("gc-")}
    for g in index.global_context:
        if g.id in used_gc:
            nodes.append({"id": g.id, "label": g.id, "shape": "box",
                          "title": "<b>global context</b><br><i>"
                                   + _esc(g.text_tex, 200) + "</i>",
                          "color": {"background": "#475569",
                                    "border": "#334155"},
                          "font": {"size": 10}})
    edges = []
    for e in graph.edges:
        if e.from_ not in node_ids or e.to not in node_ids:
            continue
        edges.append({"from": e.from_, "to": e.to,
                      "color": {"color": "#60a5fa" if e.arises_in == "statement"
                                else "#64748b", "opacity": 0.7},
                      "dashes": e.source == "agent4-patch",
                      "title": f"{e.arises_in} / {e.kind} / {e.source}"})

    legend = "".join(
        f'<span class="lg"><span class="dot" style="background:{c}"></span>{k}</span>'
        for k, c in ENV_COLOR.items() if any(
            s.env_type == k for s in index.statements))
    legend += ('<span class="lg">★ main</span><span class="lg">⚡ hardest</span>'
               '<span class="lg">✓ emitted</span>'
               '<span class="lg">— proof dep</span>'
               '<span class="lg" style="color:#60a5fa">— statement dep</span>'
               '<span class="lg">┄ verify-repair edge</span>')
    out = (GRAPH_TMPL
           .replace("__TITLE__", _esc(ctx.paper_id))
           .replace("__SUBTITLE__", _esc(meta.title, 110))
           .replace("__LEGEND__", legend)
           .replace("__NODES__", json.dumps(nodes, ensure_ascii=False))
           .replace("__EDGES__", json.dumps(edges, ensure_ascii=False)))
    p = ctx.path("graph/dep_graph.html")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(out, encoding="utf-8")


# ----------------------------------------------- data-loss warning aggregation

# Events that mean "material was dropped or a step degraded" — the difference
# between "the paper has nothing there" and "the pipeline lost it" lives in
# these lines of logs/run.jsonl, so surface them instead of leaving them buried.
LOSS_EVENTS = (
    "flatten_missing_input", "a0_section_failed", "a0_drop_unlocated",
    "a0_drop_too_short", "a0_drop_proof_fragment", "md_stmt_unmatched",
    "label_collision", "unknown_label",
    "targeted_fill_failed", "ext_host_removed", "g3_unknown_commands",
    "a2_failed", "a5_failed", "verify_iter_cap", "g5_leak_scan_hit",
    "gate_g4_degraded", "a3_ext_no_consensus",
)

_SAMPLE_KEYS = ("name", "text", "quote", "header", "label", "section", "cmds",
                "sample", "detail", "err", "target", "host", "phrase")


def _ev_sample(ev: dict) -> str:
    for k in _SAMPLE_KEYS:
        if ev.get(k):
            return str(ev[k])[:90]
    return ""


def loss_summary(ctx: RunContext) -> list[dict]:
    """Aggregate loss/degradation warnings (cumulative across reruns) plus the
    still-unresolved orphan proofs and deps_failed targets."""
    counts: dict[str, list] = {}
    p = ctx.path("logs/run.jsonl")
    if p.exists():
        for ln in p.read_text(encoding="utf-8").splitlines():
            try:
                ev = json.loads(ln)
            except json.JSONDecodeError:
                continue
            name = ev.get("event")
            if name in LOSS_EVENTS:
                counts.setdefault(name, []).append(ev)
    rows = [{"event": k, "count": len(v),
             "samples": [s for s in (_ev_sample(e) for e in v[:3]) if s]}
            for k, v in sorted(counts.items())]
    if ctx.path("index/orphan_proofs.json").exists():
        orph = ctx.read_json("index/orphan_proofs.json")
        if orph:
            rows.append({
                "event": "orphan_proof_unresolved", "count": len(orph),
                "samples": [str(o.get("of_text") or o.get("body", ""))[:90]
                            for o in orph[:3]]})
    if ctx.path("graph/dep_graph.json").exists():
        failed = ctx.read_json("graph/dep_graph.json").get("deps_failed", [])
        if failed:
            rows.append({"event": "deps_failed", "count": len(failed),
                         "samples": failed[:3]})
    return rows


# ------------------------------------------------------------ dashboard HTML

DASH_CSS = """
 body{margin:0;font-family:system-ui,-apple-system,sans-serif;background:#f1f5f9;color:#0f172a}
 .wrap{max-width:1100px;margin:0 auto;padding:26px 20px 60px}
 h1{font-size:20px;margin:0 0 2px} .sub{color:#64748b;font-size:13px;margin-bottom:20px}
 .cards{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}
 .card{background:#fff;border-radius:10px;padding:14px 20px;box-shadow:0 1px 3px rgba(0,0,0,.08);min-width:110px}
 .card .n{font-size:26px;font-weight:700} .card .t{font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:.04em}
 .arrow{align-self:center;color:#94a3b8;font-size:18px}
 table{border-collapse:collapse;width:100%;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.08);font-size:13px}
 th{background:#1e293b;color:#e2e8f0;padding:8px 10px;text-align:left;font-weight:600;font-size:11.5px;text-transform:uppercase;letter-spacing:.03em}
 td{padding:8px 10px;border-top:1px solid #e2e8f0;vertical-align:top}
 tr:hover td{background:#f8fafc}
 .chip{display:inline-block;padding:2px 9px;border-radius:999px;font-size:11px;font-weight:600}
 .ok{background:#dcfce7;color:#166534} .bad{background:#fee2e2;color:#991b1b}
 .main{background:#fef3c7;color:#92400e} .hard{background:#fee2e2;color:#b91c1c}
 .both{background:#f3e8ff;color:#7e22ce} .bf{background:#e0f2fe;color:#075985}
 .sig{font-family:ui-monospace,monospace;letter-spacing:2px}
 .sig b{color:#4f46e5} .sig span{color:#cbd5e1}
 .bar{height:9px;border-radius:5px;background:linear-gradient(90deg,#6366f1,#a855f7)}
 .barbg{background:#e2e8f0;border-radius:5px;width:180px;display:inline-block;vertical-align:middle}
 .reason{color:#991b1b;font-size:12px} .note{color:#64748b;font-size:12px;margin-top:6px}
 h2{font-size:15px;margin:26px 0 10px} a{color:#4f46e5;text-decoration:none} a:hover{text-decoration:underline}
 .links{margin-top:22px;font-size:13.5px;display:flex;gap:22px}
"""


def _sig_str(sg) -> str:
    return "".join(
        (f"<b>{name}</b>" if getattr(sg, name) else "<span>·</span>")
        for name in ("S1", "S2", "S3", "S4", "S5", "S6"))


def _dashboard_html(ctx: RunContext, index: StatementsIndex, sel: Selection,
                    manifest: Manifest, excluded: list[dict],
                    meta: Meta) -> None:
    by_id = index.by_id()
    m_set, h_set = set(sel.mains), set(sel.hardest)
    targets = list(dict.fromkeys(sel.mains + sel.hardest))
    emitted = {p.target_id for p in manifest.packages}
    exc_by = {e["target_id"]: e for e in excluded}
    n_proofed = sum(1 for s in index.statements
                    if len(s.proof_tex or "") >= ctx.cfg.pipeline.min_proof_chars)
    diff_rank = {t: i + 1 for i, t in enumerate(
        sorted(sel.difficulty, key=lambda t: sel.difficulty[t], reverse=True))}

    def funnel_card(n, t):
        return f'<div class="card"><div class="n">{n}</div><div class="t">{t}</div></div>'

    funnel = '<div class="cards">' + '<div class="arrow">→</div>'.join([
        funnel_card(len(index.statements), "statements indexed"),
        funnel_card(n_proofed, "with usable proof"),
        funnel_card(f"{len(targets)}", f"targets ({len(sel.mains)} main / "
                    f"{len(sel.hardest)} hardest)"),
        funnel_card(len(emitted), "problems emitted"),
    ]) + '</div>'

    rows = []
    for t in targets:
        s = by_id.get(t)
        if s is None:
            continue
        sg = sel.signals.get(t)
        sel_as = ("main+hardest" if t in m_set and t in h_set else
                  "hardest" if t in h_set else "main")
        cls = {"main": "main", "hardest": "hard", "main+hardest": "both"}[sel_as]
        chip = f'<span class="chip {cls}">{sel_as}</span>'
        if t in sel.backfilled:
            chip += ' <span class="chip bf">backfilled</span>'
        if t in emitted:
            out = '<span class="chip ok">EMITTED</span>'
        elif t in exc_by:
            e = exc_by[t]
            out = (f'<span class="chip bad">{_esc(e["reason_code"])}</span>'
                   f'<div class="reason">{_esc(str(e.get("detail", "")), 140)}</div>')
        else:
            out = '<span class="chip bad">not packaged</span>'
        name = f" <i>{_esc(s.display_name, 40)}</i>" if s.display_name else ""
        rows.append(
            f"<tr><td><b>{_esc(t)}</b>{name}</td>"
            f"<td>{chip}</td>"
            f"<td class='sig'>{_sig_str(sg) if sg else ''}</td>"
            f"<td>{sg.used_by if sg else ''}/{sg.closure if sg else ''}"
            f"/{sg.chain if sg else ''}</td>"
            f"<td>{sg.proof_len if sg else ''}</td>"
            f"<td>#{diff_rank.get(t, '–')} ({sel.difficulty.get(t, '–')})</td>"
            f"<td>{out}</td></tr>")

    top_diff = sorted(sel.difficulty, key=lambda t: sel.difficulty[t],
                      reverse=True)[:8]
    mx = max((sel.difficulty[t] for t in top_diff), default=1) or 1
    dbars = "".join(
        f"<tr><td><b>{_esc(t)}</b></td>"
        f"<td><span class='barbg'><span class='bar' style='width:{int(180 * sel.difficulty[t] / mx)}px'></span></span>"
        f" {sel.difficulty[t]}</td>"
        f"<td>{'⚡' if t in h_set else ''}{'★' if t in m_set else ''}</td></tr>"
        for t in top_diff)

    exc_rows = "".join(
        f"<tr><td><b>{_esc(e['target_id'])}</b></td>"
        f"<td><span class='chip bad'>{_esc(e['reason_code'])}</span></td>"
        f"<td class='reason'>{_esc(str(e.get('detail', '')), 220)}</td></tr>"
        for e in excluded)

    loss = loss_summary(ctx)
    loss_rows = "".join(
        f"<tr><td><b>{_esc(r['event'])}</b></td><td>{r['count']}</td>"
        f"<td class='reason'>{_esc(' ; '.join(r['samples']), 260)}</td></tr>"
        for r in loss)

    out = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{_esc(ctx.paper_id)} — dashboard</title>
<style>{DASH_CSS}</style></head><body><div class="wrap">
<h1>{_esc(ctx.paper_id)} — Paper Cleaner dashboard</h1>
<div class="sub">{_esc(meta.title, 140)} &nbsp;·&nbsp; {_esc(meta.paper_date)}
 &nbsp;·&nbsp; baseline: {_esc(meta.field_baseline, 90)}</div>
{funnel}
<h2>Selected targets</h2>
<table><tr><th>target</th><th>selected as</th><th>signals S1–S6</th>
<th>used_by/closure/chain</th><th>proof chars</th><th>difficulty</th>
<th>outcome</th></tr>{''.join(rows)}</table>
<div class="note">S1 sink · S2 closure-percentile · S3 named-theorem ·
 S4 previewed in abstract/intro · S5 long proof · S6 env=theorem ·
 difficulty = rank-points(proof len + closure + chain) + A2-hardest bonus</div>
<h2>Difficulty ranking (top {len(top_diff)})</h2>
<table><tr><th>statement</th><th>score</th><th></th></tr>{dbars}</table>
<h2>Exclusions ({len(excluded)})</h2>
<table><tr><th>target</th><th>reason</th><th>detail</th></tr>
{exc_rows or '<tr><td colspan=3>(none)</td></tr>'}</table>
<h2>Pipeline warnings — data-loss &amp; degradation signals</h2>
<table><tr><th>event</th><th>count</th><th>samples</th></tr>
{loss_rows or '<tr><td colspan=3>(none — no loss signals logged)</td></tr>'}</table>
<div class="note">Counts are cumulative over logs/run.jsonl (reruns append).
 These distinguish "the paper does not contain it" from "the pipeline dropped
 it": e.g. flatten_missing_input = an \\input file was absent from the source;
 a0_section_failed = a whole section's index-fill call failed.</div>
<div class="links"><a href="../graph/dep_graph.html">→ interactive dependency graph</a>
<a href="../packages/SELECTION_RATIONALE.md">→ selection rationale (A5)</a>
<a href="../manifest.json">→ manifest.json</a></div>
</div></body></html>"""
    p = ctx.path("report/dashboard.html")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(out, encoding="utf-8")


# ------------------------------------------ A5 selection rationale (English md)

def _rationale_payload(ctx: RunContext, index: StatementsIndex,
                       sel: Selection, manifest: Manifest,
                       excluded: list[dict], roles: Roles) -> list[dict]:
    by_id = index.by_id()
    emitted = {p.target_id for p in manifest.packages}
    exc_by = {e["target_id"]: e for e in excluded}
    m_set, h_set = set(sel.mains), set(sel.hardest)
    diff_rank = {t: i + 1 for i, t in enumerate(
        sorted(sel.difficulty, key=lambda t: sel.difficulty[t], reverse=True))}
    nominee_why = {n.id: n.why for n in sel.llm_nominees}
    payload = []
    for t in dict.fromkeys(sel.mains + sel.hardest):
        s = by_id.get(t)
        if s is None:
            continue
        sg = sel.signals.get(t)
        role = roles.roles.get(t)
        if t in emitted:
            status = "emitted"
        elif t in exc_by:
            status = (f"excluded ({exc_by[t]['reason_code']}: "
                      f"{str(exc_by[t].get('detail', ''))[:160]})")
        else:
            status = "not packaged"
        payload.append({
            "id": t,
            "env": s.env_type,
            "display_name": s.display_name,
            "selected_as": ("main+hardest" if t in m_set and t in h_set
                            else "hardest" if t in h_set else "main"),
            "backfilled": t in sel.backfilled,
            "signals": {k: getattr(sg, k) for k in
                        ("S1", "S2", "S3", "S4", "S5", "S6")} if sg else {},
            "graph": {"used_by": sg.used_by, "closure": sg.closure,
                      "chain": sg.chain, "proof_chars": sg.proof_len}
                     if sg else {},
            "difficulty_rank": diff_rank.get(t),
            "a2_nomination_why": nominee_why.get(t, ""),
            "a2_role": role.role if role else "unknown",
            "status": status,
            "statement_excerpt": (s.statement_tex or "")[:350],
        })
    return payload


def _signal_appendix(sel: Selection, payload: list[dict]) -> str:
    lines = ["", "---", "", "## Appendix — deterministic signal table", "",
             "| target | selected as | S1–S6 | used_by | closure | chain | "
             "proof chars | difficulty rank | outcome |",
             "|---|---|---|---|---|---|---|---|---|"]
    for p in payload:
        sig = "".join(k if v else "·" for k, v in p["signals"].items()) \
            .replace("S", "")
        g = p["graph"]
        lines.append(
            f"| {p['id']} | {p['selected_as']}"
            f"{' (backfilled)' if p['backfilled'] else ''} | `{sig or '—'}` "
            f"| {g.get('used_by', '')} | {g.get('closure', '')} "
            f"| {g.get('chain', '')} | {g.get('proof_chars', '')} "
            f"| #{p['difficulty_rank']} | {p['status'].split(' (')[0]} |")
    lines += ["",
              "Signal glossary: **S1** dependency-graph sink · **S2** "
              "dependency-closure size ≥ 75th percentile · **S3** named "
              "theorem in the main body · **S4** previewed in abstract/"
              "introduction · **S5** proof length ≥ 75th percentile · "
              "**S6** stated as `theorem`. Difficulty score = rank points "
              "over (proof length, dependency closure, chain depth) + a "
              "bonus when agent A2 independently nominated the proof as "
              "technically hardest.", ""]
    return "\n".join(lines)


async def _rationale_md(ctx: RunContext, index: StatementsIndex,
                        sel: Selection, manifest: Manifest,
                        excluded: list[dict], roles: Roles,
                        meta: Meta) -> None:
    payload = _rationale_payload(ctx, index, sel, manifest, excluded, roles)
    abstract = ""
    try:
        from .step5_select_mains import _abstract_and_intro
        abstract, _ = _abstract_and_intro(ctx, meta)
    except Exception:
        pass

    body = ""
    try:
        out = await call_llm(ctx, "a5", {
            "paper_title": meta.title,
            "paper_id": ctx.paper_id,
            "field_baseline": meta.field_baseline,
            "abstract": abstract[:2500],
            "storyline": roles.storyline[:2500],
            "targets_json": json.dumps(payload, ensure_ascii=False, indent=1),
        })
        body = out.markdown.strip()
    except (TaskFailed, Exception) as e:      # a human-readable document does not block the pipeline
        ctx.log_event(event="a5_failed", err=repr(e)[:250])
        body = ("*(automatic fallback: the A5 writing agent failed; "
                "the deterministic appendix below is authoritative)*")

    head = (f"# Problem Selection Rationale — {ctx.paper_id}\n\n"
            f"**{meta.title}**\n\n"
            f"*Generated by Paper Cleaner v2.3 — agent A5 prose over "
            f"deterministic selection signals. Emitted problems: "
            f"{len(manifest.packages)} / {len(payload)} targets.*\n\n")
    md = head + body + "\n" + _signal_appendix(sel, payload)
    p = ctx.path("packages/SELECTION_RATIONALE.md")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(md, encoding="utf-8")
    ctx.log_event(event="rationale_written", chars=len(md))


# ------------------------------------------------------------------ main flow

async def _run_async(ctx: RunContext) -> None:
    meta = ctx.read_model("source/meta.json", Meta)
    index = ctx.read_model("index/statements.v2.json", StatementsIndex)
    graph = ctx.read_model("graph/dep_graph.json", DepGraph)
    sel = ctx.read_model("roles/selection.json", Selection)
    roles = ctx.read_model("roles/roles.json", Roles)
    manifest = ctx.read_model("manifest.json", Manifest)
    excluded = (ctx.read_json("excluded.json")
                if ctx.path("excluded.json").exists() else [])
    emitted = {p.target_id for p in manifest.packages}

    _graph_html(ctx, index, graph, sel, emitted, meta)
    _dashboard_html(ctx, index, sel, manifest, excluded, meta)
    await _rationale_md(ctx, index, sel, manifest, excluded, roles, meta)
    ctx.log_event(event="step8_done", emitted=len(emitted),
                  targets=len(dict.fromkeys(sel.mains + sel.hardest)))


def run(ctx: RunContext) -> None:
    ctx.step_name = STEP
    run_async(_run_async(ctx))
