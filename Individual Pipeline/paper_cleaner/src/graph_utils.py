"""Graph: build, clean, closure, statistics (§7.6, §8.1, §9.1). Fully deterministic."""
from __future__ import annotations

import re

import networkx as nx

from .common import RunContext, sha256_text
from .latex_utils import scan_refs
from .schemas import (DepGraph, DroppedEdge, Edge, SignalSet, Statement,
                      StatementsIndex)

CONF_RANK = {"high": 2, "medium": 1, "low": 0}


def mechanical_edges(index: StatementsIndex, label_map: dict) -> list[Edge]:
    """§7.6(1): each non-cite mechanical_refs entry -> explicit edge; arises_in
    is decided by where the reference appears (statement vs proof)."""
    edges = []
    for s in index.statements:
        for text, where in ((s.statement_tex, "statement"),
                            (s.proof_tex or "", "proof")):
            for lab in scan_refs(text):
                to = label_map.get(lab)
                if to and to != s.id:
                    edges.append(Edge.model_validate({
                        "from": s.id, "to": to, "arises_in": where,
                        "kind": "explicit", "evidence": f"\\ref{{{lab}}}",
                        "confidence": "high", "source": "parser"}))
    return edges


def dedupe_edges(edges: list[Edge]) -> list[Edge]:
    """Same (from, to, arises_in) -> keep the one with highest confidence (§7.6(3))."""
    best: dict[tuple, Edge] = {}
    for e in edges:
        k = (e.from_, e.to, e.arises_in)
        if k not in best or CONF_RANK[e.confidence] > CONF_RANK[best[k].confidence]:
            best[k] = e
    return list(best.values())


def _first_cycle(g: nx.DiGraph) -> list | None:
    """Deterministic first cycle: iterative DFS over sorted nodes with sorted
    successors. nx.simple_cycles enumerates in an implementation/version-
    dependent order, which made the cycle-break victim — and hence the whole
    dep graph — irreproducible across environments."""
    color: dict = {}                      # 0/absent=white, 1=on stack, 2=done
    for start in sorted(g.nodes):
        if color.get(start):
            continue
        color[start] = 1
        path = [start]
        stack = [(start, iter(sorted(g.successors(start))))]
        while stack:
            node, succ = stack[-1]
            advanced = False
            for v in succ:
                c = color.get(v, 0)
                if c == 1:                # back edge -> cycle found
                    return path[path.index(v):]
                if c == 0:
                    color[v] = 1
                    path.append(v)
                    stack.append((v, iter(sorted(g.successors(v)))))
                    advanced = True
                    break
            if not advanced:
                color[node] = 2
                path.pop()
                stack.pop()
    return None


def clean_graph(ctx: RunContext, edges: list[Edge], index: StatementsIndex,
                frozen_ids: set[str]) -> tuple[list[Edge], list[DroppedEdge]]:
    """§7.6(3)-(6): dedupe, self-loops, forward edges, break cycles.

    frozen_ids: entries that existed when v2 was finalized -- only these participate
    in forward-edge determination; entries appended after v2 (products of targeted
    index-fill, physically located earlier in the text yet with order_index tacked on
    at the tail) are exempt.
    """
    order = {s.id: s.order_index for s in index.statements}
    # appendix-deferred proof exemption: for a statement whose proof is in the
    # appendix, its proof edges pointing to entries "after the statement but before
    # the proof" are legitimate dependencies (the proof is physically located later),
    # not forward edges.
    deferred = {s.id for s in index.statements
                if s.proof_location.startswith("appendix")}
    edges = dedupe_edges(edges)
    edges = [e for e in edges if e.from_ != e.to]              # self-loop
    dropped: list[DroppedEdge] = []

    kept = []
    for e in edges:
        if (e.from_ in order and e.to in order
                and e.from_ in frozen_ids and e.to in frozen_ids
                and order[e.to] > order[e.from_]
                and not (e.arises_in == "proof" and e.from_ in deferred)):
            dropped.append(DroppedEdge(edge=e, reason="forward"))
        else:
            kept.append(e)
    edges = kept

    g = nx.DiGraph()
    for e in edges:
        g.add_edge(e.from_, e.to)
    while True:
        cycle = _first_cycle(g)
        if cycle is None:
            break
        cyc_pairs = set(zip(cycle, cycle[1:] + cycle[:1]))
        cands = [e for e in edges if (e.from_, e.to) in cyc_pairs]
        victim = min(cands, key=lambda e: (CONF_RANK[e.confidence],
                                           len(e.evidence), e.from_, e.to))
        edges.remove(victim)
        g.remove_edge(victim.from_, victim.to)
        dropped.append(DroppedEdge(edge=victim, reason="cycle"))
        ctx.log_event(event="cycle_broken", edge=f"{victim.from_}->{victim.to}")
    return edges, dropped


def build_nx(graph: DepGraph) -> nx.DiGraph:
    g = nx.DiGraph()
    for e in graph.edges:
        g.add_edge(e.from_, e.to, arises_in=e.arises_in, kind=e.kind)
    return g


def export_mmd(ctx: RunContext, graph: DepGraph) -> None:
    lines = ["flowchart TD"]
    for e in graph.edges:
        a = re.sub(r"[^0-9A-Za-z_.-]", "_", e.from_)
        b = re.sub(r"[^0-9A-Za-z_.-]", "_", e.to)
        lines.append(f"    {a} --> {b}")
    ctx.path("graph/graph.mmd").write_text("\n".join(lines) + "\n",
                                           encoding="utf-8")


# --------------------------------------------------------------- §9.1 eligibility

def eligible_ids(index: StatementsIndex, graph: DepGraph, cfg) -> list[str]:
    failed = set(graph.deps_failed)
    out = []
    for s in index.statements:
        if (s.env_type in ("theorem", "lemma", "proposition", "corollary")
                and s.added_by == "parser"
                and s.source_verified
                and bool(s.statement_sha256)
                and bool(s.source_sha256)
                and bool(s.source_file)
                and 0 <= s.source_start < s.source_end
                and s.proof_tex is not None
                and s.proof_source_verified
                and bool(s.proof_sha256)
                and sha256_text(s.proof_tex) == s.proof_sha256
                and bool(s.proof_source_sha256)
                and s.proof_source_file == s.source_file
                and 0 <= s.proof_source_start < s.proof_source_end
                and len(s.proof_tex) >= cfg.pipeline.min_proof_chars
                and not s.uses_figure
                and s.id not in failed):
            out.append(s.id)
    return out


def ineligibility_reason(s: Statement, graph: DepGraph, cfg) -> str | None:
    """reason_code for failing eligibility (§9.1 / §3.8); returns None if eligible."""
    if s.env_type not in ("theorem", "lemma", "proposition", "corollary"):
        return None                      # non-result types are not targets, not written as excluded
    if (s.added_by != "parser" or not s.source_verified
            or not s.statement_sha256 or not s.source_sha256
            or not s.source_file or not (0 <= s.source_start < s.source_end)):
        return "target_source_unverified"
    if s.id in set(graph.deps_failed):
        return "deps_failed"
    if s.uses_figure:
        return "uses_figure"
    if s.proof_tex is None:
        return "no_proof_in_paper"
    if (not s.proof_source_verified or not s.proof_sha256
            or sha256_text(s.proof_tex) != s.proof_sha256
            or not s.proof_source_sha256
            or s.proof_source_file != s.source_file
            or not (0 <= s.proof_source_start < s.proof_source_end)):
        return "proof_source_unverified"
    if len(s.proof_tex) < cfg.pipeline.min_proof_chars:
        return "proof_too_short"
    return None


# --------------------------------------------------------------- §8.1 signals

NAMING_RE = re.compile(r"(?i)main|principal")


def compute_signals(index: StatementsIndex, graph: DepGraph, cfg,
                    intro_text: str) -> dict[str, SignalSet]:
    g = build_nx(graph)
    elig = eligible_ids(index, graph, cfg)
    by_id = index.by_id()

    def used_by(i):
        return g.in_degree(i) if g.has_node(i) else 0

    def closure(i):
        return len(nx.descendants(g, i)) if g.has_node(i) else 0

    def chain(i):
        if not g.has_node(i):
            return 0
        sub = g.subgraph(nx.descendants(g, i) | {i})
        try:
            return nx.dag_longest_path_length(sub)
        except nx.NetworkXUnfeasible:
            return 0

    closures = sorted(closure(i) for i in elig)
    prooflens = sorted(len(by_id[i].proof_tex or "") for i in elig)

    def pct_threshold(vals: list[int], q: float) -> int:
        if not vals:
            return 0
        k = max(0, min(len(vals) - 1, int(round(q * (len(vals) - 1)))))
        return vals[k]

    c_thr = pct_threshold(closures, 0.75)
    p_thr = pct_threshold(prooflens, 0.75)

    out: dict[str, SignalSet] = {}
    for i in elig:
        s = by_id[i]
        # S3 author endorsement: main/principal wording, the Theorem A/B convention, or
        # "the theorem is given a name in the body" -- a named theorem is authorial
        # emphasis (in practice the original regex missed named theorems like
        # "Structure theorem"). Appendix theorems do not count (technical results
        # are often named too).
        s3 = bool(NAMING_RE.search(s.display_name)) or \
            (s.env_type == "theorem" and bool(s.display_name.strip())
             and s.section.isdigit())
        s4 = _intro_references(s, intro_text)
        out[i] = SignalSet(
            S1=used_by(i) == 0,
            S2=closure(i) > 0 and closure(i) >= c_thr,   # percentile >= 0.75 and non-degenerate
            S3=s3, S4=s4,
            S5=len(s.proof_tex or "") >= p_thr,
            S6=s.env_type == "theorem",
            used_by=used_by(i), closure=closure(i), chain=chain(i),
            proof_len=len(s.proof_tex or ""))
    return out


def _intro_references(s: Statement, intro_text: str) -> bool:
    """S4: the introduction explicitly references the statement's source label.

    Note: cannot use the bare "{label}" substring -- the intro text contains the
    statement's own \\label{...} definition site, which would falsely flag every
    labeled statement in section 1.
    """
    if s.latex_label:
        for cmd in ("ref", "cref", "Cref", "autoref", "vref", "eqref"):
            if f"\\{cmd}{{{s.latex_label}}}" in intro_text:
                return True
    return False
