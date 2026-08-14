"""Step 6: packaging (§9, program + restricted LLM sub-call A3-ext).

Output: packages/<target_id>/<policy>/problem.md (draft) + assembly.json (assembly trace).
assemble() is reused by Step 7 (reassembly after dropping blocks / adding edges).
"""
from __future__ import annotations

import asyncio
import re
import shutil

import networkx as nx

from .common import RunContext, TaskFailed, sha256_text
from .gates import _norm_ws, g3_macro_residue
from .graph_utils import build_nx, eligible_ids, ineligibility_reason
from .llm import call_llm, run_async
from .schemas import (DepGraph, ExternalDep, Meta, Selection, Statement,
                      StatementsIndex)
from .target_integrity import (canonical_target_section,
                               canonicalize_target_section,
                               frozen_target_record,
                               proof_source_issues,
                               statement_source_issues)

STEP = "step6"

DEF_TYPES = {"definition", "inline-definition", "assumption"}
RESULT_TYPES = {"theorem", "lemma", "proposition", "corollary", "equation"}
ENV_DISPLAY = {
    "theorem": "Theorem", "lemma": "Lemma", "proposition": "Proposition",
    "corollary": "Corollary", "definition": "Definition",
    "inline-definition": "Definition", "assumption": "Assumption",
    "equation": "Equation", "remark": "Remark", "example": "Example",
}


class PackageExcluded(Exception):
    def __init__(self, reason_code: str, detail: str = ""):
        super().__init__(f"{reason_code}: {detail}")
        self.reason_code = reason_code
        self.detail = detail


def _sec_key(s: str):
    """Section sort key: numeric body sections before appendix letters."""
    return (0, int(s)) if s.isdigit() else (1, s)


def grants_from_target(cands: list[Statement],
                       target: Statement) -> set[str]:
    """Entries that must never be granted for THIS target: positioned after
    the target and textually contained in the target's own proof or statement.

    Two legitimate capture paths produce such entries — labeled equations
    nested in the target's env (its own conclusions) and labeled equations
    inside its appendix proof (pulled into the closure by the
    appendix-deferred exemption). Granting either hands the solver the
    answer (a calibration target was once granted its own
    Eqs 3.5/3.6 plus its Appendix-D estimates as "available results").
    Entries positioned BEFORE the target are body material and always safe —
    a proof restating an earlier definition must not un-grant it.
    NOTE: definition-grade STATEMENTS get no exemption — the first
    repair-first audit showed a "Definition" carrying the target proof's
    coupling construction is a proof step, not language (2606.19639).
    Pure notation and standing assumptions admitted from proof prose reach
    the owner through the gc channel instead, which this filter never
    touches — that split keeps the rescue without the leak.
    """
    tproof = _norm_ws(target.proof_tex or "")
    tstmt = _norm_ws(target.statement_tex)
    out = set()
    for s in cands:
        if s.order_index <= target.order_index or s.id == target.id:
            continue
        t = _norm_ws(s.statement_tex)
        if t and (t in tproof or t in tstmt):
            out.add(s.id)
    return out


# ------------------------------------------------- §9.3 external-result decision tree

CITE_MARKER_RE = re.compile(
    r"\[[^\]]{1,60}\]|\\cite[tp]?\*?(?:\[[^\]]*\])*\{[^}]*\}")


def _usage_quote_usable(quote: str) -> bool:
    """A usage quote can stand in for the cited result if, after stripping
    citation markers, it still carries math ($...$) or >=8 words of prose."""
    stripped = CITE_MARKER_RE.sub(" ", quote)
    if re.search(r"\$[^$]+\$", stripped):
        return True
    return len(re.findall(r"[A-Za-z][A-Za-z'-]*", stripped)) >= 8


def _context_paragraph(flat: str, quote: str) -> str:
    if quote:
        paras = re.split(r"\n\s*\n", flat)
        for p in paras:
            if quote[:60] in p:
                return p[:4000]
    return quote


def _ext_memo_key(ext: ExternalDep, forbid_usage_quote: bool = False) -> str:
    # fq=1 entries are keyed separately: the same dep may legitimately resolve
    # via usage-quote for one target's closure and need a real statement for
    # another (its own) target
    suffix = "|fq=1" if forbid_usage_quote else ""
    return sha256_text(
        f"{ext.used_by}|{ext.citation_key}|{ext.usage_quote}{suffix}")[:24]


async def resolve_external(ctx: RunContext, ext: ExternalDep,
                           index: StatementsIndex, flat: str,
                           forbid_usage_quote: bool = False) -> ExternalDep | None:
    """Three-level decision tree; returns None on total failure (caller handles per §9.3(4)).

    Results are memoized to disk keyed by (used_by, cite, quote): the dual-generation
    protocol of §9.3(3) is one-shot — if every reassembly in the verification loop
    re-samples the statement text, problem.md drifts each round, the a4 cache is fully
    invalidated, and verification never converges (empirically the root cause of results
    flip-flopping between batches)."""
    memo_path = "graph/resolved_externals.json"
    memo = getattr(ctx, "_ext_memo", None)
    if memo is None:
        memo = (ctx.read_json(memo_path)
                if ctx.path(memo_path).exists() else {})
        ctx._ext_memo = memo
    mk = _ext_memo_key(ext, forbid_usage_quote)
    if mk in memo:
        hit = memo[mk]
        if hit is None:
            return None
        ext.statement_tex = hit["statement_tex"]
        ext.statement_origin = hit["statement_origin"]
        return ext

    resolved = await _resolve_external_fresh(ctx, ext, index, flat,
                                             forbid_usage_quote)
    memo[mk] = (None if resolved is None else
                {"statement_tex": resolved.statement_tex,
                 "statement_origin": resolved.statement_origin,
                 "usage_quote": ext.usage_quote[:120]})
    ctx.write_json(memo_path, memo)
    return resolved


async def _resolve_external_fresh(ctx: RunContext, ext: ExternalDep,
                                  index: StatementsIndex, flat: str,
                                  forbid_usage_quote: bool = False
                                  ) -> ExternalDep | None:
    if ext.stated_in_paper and ext.statement_tex.strip():
        ext.statement_origin = "verbatim-from-paper"
        return ext
    # Branch 1' (deterministic): the citation marker sits inside the body of an
    # already-indexed statement itself (e.g. "Proposition 1.1 (Foo's theorem)
    # ... ; see \cite{Foo64}") — that statement is the paper's exact statement of
    # the cited result, so grant it verbatim, zero LLM.
    if ext.citation_key:
        host = index.by_id().get(ext.used_by)
        if host and re.search(
                r"\\cite[tp]?\*?(?:\[[^\]]*\])*\{[^}]*"
                + re.escape(ext.citation_key), host.statement_tex):
            ext.statement_tex = host.statement_tex
            ext.statement_origin = "verbatim-from-paper"
            return ext
    # usage-quote stand-in — forbidden for the target's own deps: their quote
    # is a sentence of the target's proof, so shipping it as the grant both
    # fails self-containment (no hypotheses/conclusion) and leaks the proof
    # move (calibration-audit finding: Sion-minimax / "follows the structure
    # of the proof of Theorem 8" grants). Those fall through to the a3_ext
    # dual generation, which states the result properly or rejects it.
    if not forbid_usage_quote and _usage_quote_usable(ext.usage_quote):
        ext.statement_tex = ('As invoked in the source: "'
                             + ext.usage_quote.strip() + '"')
        ext.statement_origin = "usage-quote"
        return ext
    raw_bib = next((c.raw_bib for c in index.citations
                    if c.key == ext.citation_key), "")
    base_vars = {"citation_key": ext.citation_key or "(uncited)",
                 "raw_bib": raw_bib[:2000],
                 "usage_quote": ext.usage_quote,
                 "context_paragraph": _context_paragraph(flat, ext.usage_quote)}
    try:
        # Two independent generations: cache off, differing nonce at prompt tail (§9.3(3))
        g1 = await call_llm(ctx, "a3_ext", dict(base_vars, nonce="nonce: alpha-1"),
                            use_cache=False)
        g2 = await call_llm(ctx, "a3_ext", dict(base_vars, nonce="nonce: beta-2"),
                            use_cache=False)
        cmp_ = await call_llm(ctx, "a3_cmp", {
            "usage_quote": ext.usage_quote, "stmt_a": g1.statement,
            "stmt_b": g2.statement})
        if cmp_.equivalent and g1.statement.strip():
            ext.statement_tex = g1.statement
            ext.statement_origin = "llm-agreed"
            return ext
        # Repair-first: temp-0 generations still vary in FORM, and a single
        # disagreement used to be a terminal external_dep_unstatable (killed
        # Hoeffding's lemma on 2510.03923). One tiebreaker generation; any
        # 2-of-3 agreement endorses the statement.
        g3 = await call_llm(ctx, "a3_ext",
                            dict(base_vars, nonce="nonce: gamma-3"),
                            use_cache=False)
        if g3.statement.strip():
            for cand in (g1, g2):
                if not cand.statement.strip():
                    continue
                cmp2 = await call_llm(ctx, "a3_cmp", {
                    "usage_quote": ext.usage_quote,
                    "stmt_a": cand.statement, "stmt_b": g3.statement})
                if cmp2.equivalent:
                    ctx.log_event(event="a3_ext_tiebreak_agreed",
                                  key=ext.citation_key or "(uncited)")
                    ext.statement_tex = cand.statement
                    ext.statement_origin = "llm-agreed"
                    return ext
        ctx.log_event(event="a3_ext_no_consensus",
                      key=ext.citation_key or "(uncited)",
                      quote=ext.usage_quote[:80])
    except (TaskFailed, Exception) as e:
        ctx.log_event(event="a3_ext_failed", key=ext.citation_key,
                      err=repr(e)[:200])
    return None


# ------------------------------------------------------- §9.2 assembly algorithm

TEMPLATE_HEAD = """---
paper_id: {paper_id}
target_id: {target_id}
policy: {policy}
field_baseline: {field_baseline}
statements_version: {sha}
---

# Task: prove the target theorem

Provide a complete and rigorous proof of the **Target** in Section 6.

Ground rules:
- You may freely use, without proof, everything in Sections 1-5.
- You may use standard {field_baseline} knowledge.
- Do not cite external literature beyond the results listed in Section 3.
- Write the proof in LaTeX-flavored Markdown; state where each given
  result is used.
- If the problem is ill-posed or under-specified, say so explicitly and
  identify what is missing, instead of guessing.

## 0. Macro definitions
```latex
{macros_tex}
```
"""


def _render_stmt(s: Statement) -> str:
    head = ENV_DISPLAY.get(s.env_type, s.env_type.capitalize())
    disp = f" ({s.display_name})" if s.display_name else ""
    if s.env_type == "equation":
        body = f"$$\n{s.statement_tex}\n$$"
        return f"<!-- b:{s.id} -->\n**{head}{disp}.**\n{body}\n<!-- e:{s.id} -->"
    return (f"<!-- b:{s.id} -->\n**{head}{disp}.** "
            f"{s.statement_tex}\n<!-- e:{s.id} -->")


async def assemble(ctx: RunContext, index: StatementsIndex, graph: DepGraph,
                   target: Statement, policy: str,
                   removed: set[str] | None = None) -> tuple[str, dict]:
    """§9.2 assembly. Returns (problem_md, info). Raises PackageExcluded on failure.

    removed: block ids dropped by Step 7 for leaks (no longer enter assembly within
    the scope of this package).
    """
    removed = removed or set()
    by_id = index.by_id()
    gc_ids = {g.id for g in index.global_context}
    g = build_nx(graph)

    # 1. need_def: transitive closure along arises_in=statement edges
    g_stmt = nx.DiGraph()
    for e in graph.edges:
        if e.arises_in == "statement":
            g_stmt.add_edge(e.from_, e.to)
    need_def = set(nx.descendants(g_stmt, target.id)) if g_stmt.has_node(
        target.id) else set()

    # dep closure (transitive closure of proof_deps ∪ statement_deps)
    closure = set(nx.descendants(g, target.id)) if g.has_node(target.id) else set()

    # 2. avail
    if policy == "full-prior":
        avail = {s.id for s in index.statements
                 if s.order_index < target.order_index
                 and s.env_type in RESULT_TYPES | DEF_TYPES}
    elif policy == "dep-closure":
        avail = set(closure)
    elif policy == "minimal":
        avail = set(need_def)
    else:
        raise PackageExcluded("package_build_error", f"unknown policy {policy}")
    avail.discard(target.id)

    # 3. defs — under dep-closure, widened to ALL definition-kind entries
    #    (definition / inline-definition / assumption) preceding the target:
    #    definitions are just language, so the superset hedges against A1
    #    having missed a definition edge
    pool = (need_def | avail) - removed
    defs_ids = {i for i in pool
                if i in by_id and by_id[i].env_type in DEF_TYPES}
    if policy == "dep-closure":
        defs_ids |= {s.id for s in index.statements
                     if s.env_type in DEF_TYPES
                     and s.order_index < target.order_index
                     and s.id not in removed}
    defs = sorted((by_id[i] for i in defs_ids), key=lambda s: s.order_index)

    # 4. res: the rest of avail; remark/example never enter
    res_ids = {i for i in (avail - removed)
               if i in by_id and by_id[i].env_type in RESULT_TYPES
               and i not in defs_ids}
    res = sorted((by_id[i] for i in res_ids), key=lambda s: s.order_index)

    # 4b. never grant the target's own material (conclusions / proof-internal
    # labeled equations) — see grants_from_target
    own = grants_from_target(defs + res, target)
    if own:
        ctx.log_event(event="grant_from_target_dropped", target=target.id,
                      ids=sorted(own)[:10], n=len(own))
        defs = [s for s in defs if s.id not in own]
        res = [s for s in res if s.id not in own]

    # 5. gcs: scope rule ∪ gc pointed to by repair edges. A theorem statement may
    # reference notation formally introduced only later (statement in §3, mechanism
    # in §5), which the scope rule misses; the gc edges Step 7 adds must actually take
    # effect, otherwise even a ladder that hits a gc still can't assemble it in
    # (an ineffective-repair infinite loop)
    gc_edge_ids = {e.to for e in graph.edges
                   if e.to in gc_ids
                   and (e.from_ == target.id or e.from_ in closure)}
    tkey = _sec_key(target.section or "0")
    gcs = [gitem for gitem in index.global_context
           if gitem.id not in removed
           and (gitem.id in gc_edge_ids
                or gitem.scope == "paper"
                or (gitem.scope.startswith("section:")
                    and _sec_key(gitem.scope.split(":", 1)[1]) <= tkey))]

    # 6. ext: used_by ∈ {T} ∪ closure, goes through the §9.3 decision tree
    meta = ctx.read_model("source/meta.json", Meta)
    flat = ctx.path("source/flat.md" if meta.source_type == "ocr"
                    else "source/flat.tex").read_text(encoding="utf-8")
    scope_ids = {target.id} | closure
    exts: list[tuple[str, ExternalDep]] = []
    seen_ext = set()
    ext_n = 0
    for ext in graph.external_deps:
        if ext.used_by not in scope_ids:
            continue
        dedup_key = (ext.citation_key, ext.usage_quote[:80])
        if dedup_key in seen_ext:
            continue
        seen_ext.add(dedup_key)
        resolved = await resolve_external(
            ctx, ext.model_copy(), index, flat,
            forbid_usage_quote=ext.used_by == target.id)
        if resolved is None:
            # §9.3(4): needed by the target itself or by the statement chain
            # (need_def) → abandon the whole target; a host that enters the closure
            # only via proof edges is an optional granted block → drop the host.
            # (The old rule counted every "closure member" as essential, so an
            # uncited external carried by an appendix index-fill entry would kill
            # the main theorem by association.)
            essential = ext.used_by == target.id or ext.used_by in need_def
            if essential:
                raise PackageExcluded(
                    "external_dep_unstatable",
                    f"cite={ext.citation_key or '(uncited)'} "
                    f"used_by={ext.used_by}")
            res = [s for s in res if s.id != ext.used_by]
            defs = [s for s in defs if s.id != ext.used_by]
            ctx.log_event(event="ext_host_removed", host=ext.used_by)
            continue
        ext_n += 1
        exts.append((f"ext-R{ext_n}", resolved))

    # 7. fill the template verbatim
    sha = sha256_text(
        ctx.path("index/statements.v2.json").read_text(encoding="utf-8"))[:16]
    parts = [TEMPLATE_HEAD.format(
        paper_id=ctx.paper_id, target_id=target.id, policy=policy,
        field_baseline=meta.field_baseline, sha=sha,
        macros_tex=index.macros_tex.strip() or "% (no macros)")]

    parts.append("\n## 1. Notation and conventions\n")
    notation = [x for x in gcs if x.kind == "notation"]
    parts += [f"<!-- b:{x.id} -->\n{x.text_tex}\n<!-- e:{x.id} -->\n"
              for x in notation] or ["(none)\n"]

    parts.append("\n## 2. Standing assumptions\n")
    standing = [x for x in gcs if x.kind == "standing-assumption"]
    parts += [f"<!-- b:{x.id} -->\n{x.text_tex}\n<!-- e:{x.id} -->\n"
              for x in standing] or ["(none)\n"]

    parts.append("\n## 3. Known external results (may be used without proof)\n")
    if exts:
        for bid, x in exts:
            key = x.citation_key or "uncited"
            parts.append(f"<!-- b:{bid} -->\n**[{bid.replace('ext-', '')}]** "
                         f"(as invoked for [{key}]) {x.statement_tex}\n"
                         f"<!-- e:{bid} -->\n")
    else:
        parts.append("(none)\n")

    parts.append("\n## 4. Definitions\n")
    parts += [_render_stmt(s) + "\n" for s in defs] or ["(none)\n"]

    parts.append("\n## 5. Available results (statements only; may be used "
                 "without proof)\n")
    parts += [_render_stmt(s) + "\n" for s in res] or ["(none)\n"]

    parts.append("\n" + canonical_target_section(target.statement_tex))

    problem_md = "\n".join(parts)
    info = {
        "target_id": target.id, "policy": policy,
        "target_statement_sha256": target.statement_sha256,
        "need_def": sorted(need_def), "closure": sorted(closure),
        "defs": [s.id for s in defs], "res": [s.id for s in res],
        "ext_blocks": [b for b, _ in exts],
        "gcs": [x.id for x in gcs],
        "closure_size": {"definitions": len(defs), "results": len(res),
                         "external": len(exts)},
        "removed": sorted(removed),
    }
    return problem_md, info


# ---------------------------------------------- G3 + §9.4 + persistence wrapper

LABEL_RE = re.compile(r"\\label\{([^}]*)\}")


def _strip_dup_labels(problem_md: str) -> str:
    """Strip dead duplicate \\labels that the source paper itself introduced.

    Empirically one paper reused \\label{1.1} twice, so 4a reported duplicate-
    label ambiguity every round until the target died. A later duplicate label
    with no reference inside the package is dead — strip it; keep referenced
    duplicates (that ambiguity is real, let verification adjudicate it)."""
    from .latex_utils import scan_refs
    referenced = set(scan_refs(problem_md))
    seen: set[str] = set()

    def _sub(m: re.Match) -> str:
        lab = m.group(1)
        if lab in seen and lab not in referenced:
            return ""
        seen.add(lab)
        return m.group(0)

    return LABEL_RE.sub(_sub, problem_md)


async def build_package(ctx: RunContext, index: StatementsIndex,
                        graph: DepGraph, target: Statement, policy: str,
                        removed: set[str] | None = None) -> tuple[str, dict]:
    """assemble + G3 macro-residue gate + §9.4 automatic downgrade on the size cap."""
    meta = ctx.read_model("source/meta.json", Meta)
    flat = ctx.path("source/flat.md" if meta.source_type == "ocr"
                    else "source/flat.tex").read_text(encoding="utf-8")
    source_file = ("source/flat.md" if meta.source_type == "ocr"
                   else "source/flat.tex")
    source_issues = statement_source_issues(
        target, flat_source=flat, expected_source_file=source_file)
    if source_issues:
        raise PackageExcluded("target_source_unverified", "; ".join(source_issues))
    proof_issues = proof_source_issues(
        target, flat_source=flat, expected_source_file=source_file)
    if proof_issues:
        raise PackageExcluded("proof_source_unverified", "; ".join(proof_issues))
    downgraded = False
    active_policy = policy

    problem_md, info = await assemble(ctx, index, graph, target,
                                      active_policy, removed)
    if len(problem_md) > ctx.cfg.pipeline.package_char_cap:
        if active_policy == "full-prior":                       # §9.4 automatic downgrade
            active_policy, downgraded = "dep-closure", True
            problem_md, info = await assemble(ctx, index, graph, target,
                                              active_policy, removed)
        if len(problem_md) > ctx.cfg.pipeline.package_char_cap:
            raise PackageExcluded("package_build_error",
                                  f"oversize: {len(problem_md)} chars")

    # G3: macro residue
    unknown, addendum = g3_macro_residue(ctx, problem_md, index.macros_tex, flat)
    if addendum:                                # collect the missed definitions and reassemble once
        index.macros_tex = index.macros_tex.rstrip() + "\n" + addendum + "\n"
        macros_path = ctx.path("source/macros.tex")
        macros_path.write_text(index.macros_tex, encoding="utf-8")
        ctx.log_event(event="g3_macros_appended", cmds=addendum[:200])
        problem_md, info = await assemble(ctx, index, graph, target,
                                          active_policy, removed)
        unknown, _ = g3_macro_residue(ctx, problem_md, index.macros_tex, flat)
    if unknown:
        if meta.source_type == "ocr":           # typical symptom of an OCR-hallucinated command
            raise PackageExcluded("package_build_error",
                                  f"undefined_command:{unknown[0]}")
        ctx.log_event(event="g3_unknown_commands", cmds=unknown,
                      level="warning")

    info["policy_downgraded"] = downgraded
    info["effective_policy"] = active_policy
    problem_md = _strip_dup_labels(problem_md)
    problem_md = canonicalize_target_section(
        problem_md, statement_tex=target.statement_tex)
    return problem_md, info


# ------------------------------------------------------------------ main flow

async def _run_async(ctx: RunContext) -> None:
    index = ctx.read_model("index/statements.v2.json", StatementsIndex)
    graph = ctx.read_model("graph/dep_graph.json", DepGraph)
    selection = ctx.read_model("roles/selection.json", Selection)
    by_id = index.by_id()

    # A step6 rerun = redo all packaging for this round: clear the previous round's
    # excluded records and package directories. After selection changes, a leftover
    # old target directory would get verified in passing by step7 (which enumerates
    # by disk) and mixed into the manifest (step6/7 are the only two writers). Only
    # delete subdirectories — human-readable artifacts like SELECTION_RATIONALE.md
    # under the packages/ root are managed by step8
    if ctx.path("excluded.json").exists():
        ctx.path("excluded.json").unlink()
    pkg_root = ctx.path("packages")
    if pkg_root.exists():
        for child in pkg_root.iterdir():
            if child.is_dir():
                shutil.rmtree(child)

    if ctx.cfg.pipeline.granularity == "per-node":
        targets = eligible_ids(index, graph, ctx.cfg)
        for s in index.statements:              # would-be targets that fail eligibility → excluded
            reason = ineligibility_reason(s, graph, ctx.cfg)
            if reason:
                ctx.add_excluded(s.id, "", reason)
    else:
        # mains ∪ hardest (dedup, order-preserving, mains first) — a hardest
        # theorem may coincide with a main theorem
        targets = list(dict.fromkeys(
            list(selection.mains) + list(selection.hardest)))

    ctx.progress(f"packaging {len(targets)} targets × "
                 f"{len(ctx.cfg.pipeline.policies)} policies")
    for tid in targets:
        target = by_id[tid]
        for policy in ctx.cfg.pipeline.policies:
            pkg_dir = ctx.path(f"packages/{tid}/{policy}")
            pkg_dir.mkdir(parents=True, exist_ok=True)
            try:
                problem_md, info = await build_package(
                    ctx, index, graph, target, policy)
            except PackageExcluded as e:
                ctx.add_excluded(tid, policy, e.reason_code, e.detail)
                continue
            except Exception as e:              # packaging-program exception
                ctx.add_excluded(tid, policy, "package_build_error",
                                 repr(e)[:300])
                continue
            (pkg_dir / "problem.md").write_text(problem_md, encoding="utf-8")
            (pkg_dir / "target.tex").write_text(target.statement_tex,
                                                  encoding="utf-8")
            ctx.write_json(f"packages/{tid}/{policy}/target.json",
                           frozen_target_record(target))
            ctx.write_json(f"packages/{tid}/{policy}/assembly.json", info)
            ctx.log_event(event="package_drafted", target=tid, policy=policy,
                          chars=len(problem_md))
            cs = info.get("closure_size", {})
            ctx.progress(f"drafted {tid}/{policy}: {len(problem_md)} chars, "
                         f"{cs.get('definitions', '?')} defs / "
                         f"{cs.get('results', '?')} results / "
                         f"{cs.get('external', '?')} ext")


def run(ctx: RunContext) -> None:
    ctx.step_name = STEP
    run_async(_run_async(ctx))
