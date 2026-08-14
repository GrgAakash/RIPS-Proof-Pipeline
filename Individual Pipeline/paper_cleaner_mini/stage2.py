#!/usr/bin/env python3
"""Mini theorem-problem pipeline: three strong-model roles with the full
paper in hand, replacing the main repo's graph pipeline (steps 3-7).

Per target (same targets the main pipeline attempted — selection.json
mains ∪ hardest, bundled under inputs/):

    author (full paper, target proof marked forbidden)  -> problem.md body
    deterministic gate: structure, macro closure, verbatim-proof leak scan
    checker (full paper, adversarial)                   -> issues + verdicts
    repair (full paper)                                 -> revised body
    ... up to --max-repairs rounds; ship iff the checker passes AND the
    deterministic gate is silent; otherwise excluded.json with reason.

Output layout matches the main pipeline, so either repo's audit.py can
judge the result:

    python stage2.py --papers all
    python audit.py --papers all --effort high
    python compare_audits.py <baseline audit json> runs/audit/audit_report.json
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import shutil
import sys
import traceback
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

from minilib import (DepGraph, Manifest, Meta, PkgEntry, RunContext,
                     Selection, Statement, StatementsIndex, TaskFailed,
                     _norm_ws, atomic_write_text, call_llm, load_config,
                     load_std_commands,
                     now_iso, pick_model, run_async, sha256_text,
                     ship_leak_spans, CMD_RE, DEFINED_RE)
from package_validation import (canonicalize_target_section,
                                frozen_target_artifact_issues,
                                frozen_target_record,
                                proof_source_issues,
                                section3_source_issues,
                                statement_source_issues,
                                target_identity_issues)

STEP = "s2"
FLAT_CAP = 600_000
PROOF_CAP = 100_000
MAX_OUT = {"s2_author": 40000, "s2_check": 30000, "s2_repair": 40000}

HEADINGS = [
    "## 0. Macro definitions",
    "## 1. Notation and conventions",
    "## 2. Standing assumptions",
    "## 3. Known external results (may be used without proof)",
    "## 4. Definitions",
    "## 5. Available results (statements only; may be used without proof)",
    "## 6. Target",
]
EDITABLE_HEADINGS = HEADINGS[:-1]

# Same header the main pipeline ships (its step6 TEMPLATE_HEAD) minus
# Section 0, which the author writes — the audit judges identical rules.
HEAD_TMPL = """---
paper_id: {paper_id}
target_id: {target_id}
policy: stage2
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

"""

DEF_POOL = {"definition", "inline-definition", "assumption"}
EXT_RE = re.compile(r"\*\*\[R\d+\]\*\*")


# ------------------------------------------------------------ LLM schemas

class _LLM(BaseModel):
    model_config = ConfigDict(extra="forbid")


class S2AuthorOut(_LLM):
    problem_md: str


class S2Issue(_LLM):
    kind: Literal["undefined-symbol", "undefined-term", "missing-result",
                  "leak", "other"]
    quote: str
    explanation: str
    severity: Literal["fatal", "minor"]
    fix_hint: str


class S2CheckOut(_LLM):
    issues: list[S2Issue]
    self_contained: bool
    leak_free: bool
    sufficient: bool
    summary: str


class S2RepairOut(_LLM):
    problem_md: str
    unfixed: list[str]


# ------------------------------------------------- deterministic checks

def normalize_body(raw: str) -> Optional[str]:
    """Cut author/repair output down to the editable body (from Section 0)."""
    i = raw.find(HEADINGS[0])
    if i < 0:
        return None
    return raw[i:].strip() + "\n"


def structure_missing(body: str) -> list[str]:
    """Editable headings that are absent, duplicated, or out of order."""
    pos, bad = -1, []
    for h in EDITABLE_HEADINGS:
        hits = [match.start() for match in re.finditer(
            rf"(?m)^{re.escape(h)}\s*$", body)]
        i = hits[0] if hits else -1
        if len(hits) != 1 or i < pos:
            bad.append(h)
        else:
            pos = i
    # Models own Sections 0-5 only. Any Section 6 occurrence is rejected and
    # retried instead of silently truncating later content.
    if re.search(rf"(?m)^{re.escape(HEADINGS[-1])}\s*$", body):
        bad.append(HEADINGS[-1])
    return bad


def macro_closure_missing(body: str, std: set[str]) -> list[str]:
    """Commands used in the file but neither standard LaTeX nor defined in
    the file's own Section 0 — standalone renderability, stricter than the
    main pipeline's g3 (which accepts paper-side definitions)."""
    defined = set(DEFINED_RE.findall(body))
    return sorted({c for c in CMD_RE.findall(body)
                   if c not in std and c not in defined and len(c) > 1})


def detect_blocks(index: StatementsIndex, body: str) -> dict:
    """Which index blocks the author quoted verbatim (normalized substring).
    Feeds the same det-scan whitelist rule the main pipeline uses: a
    granted block's own source text is legitimate presence, not a leak."""
    hay = _norm_ws(body)
    defs, res, gcs = [], [], []
    for s in index.statements:
        t = _norm_ws(s.statement_tex)
        if t and t in hay:
            (defs if s.env_type in DEF_POOL else res).append(s.id)
    for g in index.global_context:
        t = _norm_ws(g.text_tex)
        if t and t in hay:
            gcs.append(g.id)
    return {"defs": defs, "res": res, "gcs": gcs}


def det_issues(index: StatementsIndex, target: Statement, md: str,
               body: str, std: set[str], assembly: dict) -> list[dict]:
    """Deterministic pre-ship gate, same functions the audit runs."""
    issues = target_identity_issues(
        body,
        statement_tex=target.statement_tex,
        statement_sha256=target.statement_sha256,
    )
    for s in ship_leak_spans(index, DepGraph(), target, md, assembly)[:6]:
        issues.append({
            "kind": "leak", "quote": s[:300],
            "explanation": "verbatim span from the target's own proof found "
                           "in the file (deterministic scan)",
            "severity": "fatal",
            "fix_hint": "delete or rewrite; if this text is a granted "
                        "block's own statement, quote it verbatim from the "
                        "paper (outside the proof) instead"})
    for cmd in macro_closure_missing(body, std)[:10]:
        issues.append({
            "kind": "undefined-symbol", "quote": "\\" + cmd,
            "explanation": "LaTeX command used but neither standard nor "
                           "defined in Section 0",
            "severity": "fatal",
            "fix_hint": "copy its definition from the paper's preamble into "
                        "the Section 0 latex block"})
    issues.extend(section3_source_issues(
        body, [citation.key for citation in index.citations]
    ))
    return issues


def freeze_or_validate_target_artifacts(
    ctx: RunContext,
    pdir: Path,
    target: Statement,
    target_record: dict,
) -> list[str]:
    """Create target artifacts once, or reject any later mismatch."""

    target_tex_path = pdir / "target.tex"
    target_json_rel = f"packages/{target.id}/stage2/target.json"
    target_json_path = ctx.path(target_json_rel)
    have_tex = target_tex_path.exists()
    have_json = target_json_path.exists()
    if not have_tex and not have_json:
        atomic_write_text(target_tex_path, target.statement_tex)
        ctx.write_json(target_json_rel, target_record)
        return []
    if not have_tex or not have_json:
        return ["frozen target artifacts are incomplete"]
    try:
        record = ctx.read_json(target_json_rel)
        target_tex = target_tex_path.read_text(encoding="utf-8")
    except (OSError, ValueError, TypeError) as exc:
        return [f"frozen target artifacts are unreadable: {exc}"]
    return frozen_target_artifact_issues(
        target_tex=target_tex,
        statement_tex=target.statement_tex,
        record=record,
        expected_record=target_record,
    )


# ------------------------------------------------------------ per target

async def do_target(ctx: RunContext, meta: Meta, index: StatementsIndex,
                    flat: str, sha: str, target: Statement, selected_as: str,
                    models: dict, sem: asyncio.Semaphore, std: set[str],
                    max_repairs: int, tally: dict):
    tid = target.id
    pdir = ctx.path(f"packages/{tid}/stage2")
    pdir.mkdir(parents=True, exist_ok=True)
    source_file = ("source/flat.md" if meta.source_type == "ocr"
                   else "source/flat.tex")
    source_issues = statement_source_issues(
        added_by=target.added_by,
        source_verified=target.source_verified,
        source_file=target.source_file,
        source_start=target.source_start,
        source_end=target.source_end,
        source_sha256=target.source_sha256,
        statement_tex=target.statement_tex,
        statement_sha256=target.statement_sha256,
        flat_source=flat,
        expected_source_file=source_file,
    )
    if source_issues:
        return ("excluded", {"target_id": tid, "policy": "stage2",
                             "reason_code": "target_source_unverified",
                             "detail": "; ".join(source_issues)[:900]})
    if not (target.proof_tex or "").strip():
        return ("excluded", {"target_id": tid, "policy": "stage2",
                             "reason_code": "no_proof_in_paper",
                             "detail": "target has no proof in the paper"})
    proof_issues = proof_source_issues(
        proof_tex=target.proof_tex or "",
        proof_sha256=target.proof_sha256,
        proof_source_file=target.proof_source_file,
        proof_source_start=target.proof_source_start,
        proof_source_end=target.proof_source_end,
        proof_source_sha256=target.proof_source_sha256,
        proof_source_verified=target.proof_source_verified,
        proof_pairing=target.proof_pairing,
        flat_source=flat,
        expected_source_file=source_file,
    )
    if proof_issues:
        return ("excluded", {"target_id": tid, "policy": "stage2",
                             "reason_code": "proof_source_unverified",
                             "detail": "; ".join(proof_issues)[:900]})
    target_record = frozen_target_record(
        target_id=target.id,
        statement_sha256=target.statement_sha256,
        source_file=target.source_file,
        source_start=target.source_start,
        source_end=target.source_end,
        source_sha256=target.source_sha256,
        proof_sha256=target.proof_sha256,
        proof_source_file=target.proof_source_file,
        proof_source_start=target.proof_source_start,
        proof_source_end=target.proof_source_end,
        proof_source_sha256=target.proof_source_sha256,
        proof_source_verified=target.proof_source_verified,
        proof_pairing=target.proof_pairing,
    )
    artifact_issues = freeze_or_validate_target_artifacts(
        ctx, pdir, target, target_record)
    if artifact_issues:
        return ("excluded", {"target_id": tid, "policy": "stage2",
                             "reason_code": "target_integrity_failed",
                             "detail": "; ".join(artifact_issues)[:900]})

    head = HEAD_TMPL.format(paper_id=ctx.paper_id, target_id=tid,
                            field_baseline=meta.field_baseline, sha=sha)
    common = {"paper_title": meta.title, "flat_source": flat[:FLAT_CAP],
              "target_id": tid, "field_baseline": meta.field_baseline,
              "target_proof": (target.proof_tex or "")[:PROOF_CAP],
              "bibliography": bibliography_text(index)}

    async def ask(task, extra, schema):
        m = models["check"] if task == "s2_check" else models["gen"]
        async with sem:
            obj = await call_llm(ctx, task, {**common, **extra},
                                 schema=schema, model=m)
        u = getattr(obj, "_usage_log", None)
        if u:
            tally["calls"] += 1
            for k, kk in (("in", "in_tok"), ("out", "out_tok"),
                          ("reason", "reasoning_tok")):
                tally[k] += u.get(kk, 0)
        else:
            tally["cached"] += 1
        return obj

    async def structured_body(task, extra, schema):
        """Call author/repair; one corrective retry if headings break."""
        note = ""
        for _ in range(2):
            out = await ask(task, {**extra, "format_note": note}, schema)
            body = normalize_body(out.problem_md)
            bad = structure_missing(body) if body else EDITABLE_HEADINGS
            if not bad:
                body = canonicalize_target_section(
                    body,
                    statement_tex=target.statement_tex,
                )
                return body, out
            note = ("PREVIOUS ATTEMPT REJECTED: these exact headings were "
                    f"missing or out of order: {bad}. Reproduce ALL six "
                    "headings, in order, exactly as specified.")
        return None, None

    body, _ = await structured_body(
        "s2_author", {"target_statement": target.statement_tex,
                      "macros_tex": index.macros_tex}, S2AuthorOut)
    if body is None:
        return ("excluded", {"target_id": tid, "policy": "stage2",
                             "reason_code": "package_build_error",
                             "detail": "author output missing required "
                                       "section headings after retry"})

    unfixed: list[str] = []
    chk, det, assembly, md = None, [], {}, ""
    for rnd in range(max_repairs + 1):
        md = head + body
        assembly = detect_blocks(index, body)
        # The target is never an available grant of any kind.
        for key in ("defs", "res", "gcs"):
            assembly[key] = [block_id for block_id in assembly[key]
                             if block_id != tid]
        det = det_issues(index, target, md, body, std, assembly)
        artifact_issues = frozen_target_artifact_issues(
            target_tex=(pdir / "target.tex").read_text(encoding="utf-8"),
            statement_tex=target.statement_tex,
            record=ctx.read_json(f"packages/{tid}/stage2/target.json"),
            expected_record=target_record)
        det.extend({
            "kind": "other", "quote": target.statement_tex[:300],
            "explanation": issue, "severity": "fatal",
            "fix_hint": "restore target artifacts from the source-backed index",
        } for issue in artifact_issues)
        chk = await ask("s2_check", {"problem_md": md}, S2CheckOut)
        fatals = [i for i in chk.issues if i.severity == "fatal"]
        if (chk.self_contained and chk.leak_free and chk.sufficient
                and not fatals and not det):
            problem_sha = sha256_text(md)
            assembly.update(target_id=tid, policy="stage2", ext_blocks=[],
                            closure_size={
                                "definitions": len(assembly["defs"]),
                                "results": len(assembly["res"]),
                                "external": len(EXT_RE.findall(body))})
            (pdir / "problem.md").write_text(md, encoding="utf-8")
            ctx.write_json(f"packages/{tid}/stage2/assembly.json", assembly)
            ctx.write_json(f"packages/{tid}/stage2/report.json", {
                "target_id": tid, "policy": "stage2", "iterations": rnd + 1,
                "self_contained": True, "leak_clean": True,
                "sufficiency": True, "gaps_history": [], "removed_blocks": [],
                "policy_downgraded": False, "baseline_assumed": [],
                "closure_size": assembly["closure_size"],
                "problem_sha256": problem_sha,
                "input_hashes": {"statements": sha, "problem": problem_sha,
                                 "target": target.statement_sha256,
                                 "reference_proof": target.proof_sha256}})
            ctx.progress(f"✓ shipped {tid} (round {rnd + 1})")
            return ("shipped", PkgEntry(
                target_id=tid, env_type=target.env_type,
                selected_as=selected_as,
                policy="stage2", path=f"packages/{tid}/stage2/problem.md",
                proof_chars=len(target.proof_tex or "")))
        ctx.progress(f"{tid} round {rnd + 1}: {len(fatals)} fatal + "
                     f"{len(det)} det | sc={chk.self_contained} "
                     f"leak={chk.leak_free} suff={chk.sufficient}")
        if rnd == max_repairs:
            break
        (pdir / f"problem.iter{rnd + 1}.md").write_text(md, encoding="utf-8")
        findings = json.dumps([i.model_dump() for i in fatals] + det,
                              ensure_ascii=False, indent=1)
        new_body, rep = await structured_body(
            "s2_repair", {"problem_md": md, "findings": findings},
            S2RepairOut)
        if new_body is None:
            break
        body, unfixed = new_body, list(rep.unfixed)

    # ----- exclusion: keep the last state on disk for post-mortems
    (pdir / "problem.md").write_text(md, encoding="utf-8")
    ctx.write_json(f"packages/{tid}/stage2/report.json", {
        "target_id": tid, "policy": "stage2",
        "iterations": max_repairs + 1,
        "self_contained": chk.self_contained, "leak_clean": chk.leak_free,
        "sufficiency": chk.sufficient,
        "problem_sha256": sha256_text(md),
        "unfixed": unfixed[:20]})
    fatals = [i for i in chk.issues if i.severity == "fatal"]
    leak_bad = (not chk.leak_free or any(i.kind == "leak" for i in fatals)
                or any(d["kind"] == "leak" for d in det))
    sc_bad = (not chk.self_contained
              or any(i.kind in ("undefined-symbol", "undefined-term")
                     for i in fatals)
              or any(d["kind"] == "undefined-symbol" for d in det))
    reason = ("leak_in_required_context" if leak_bad else
              "self_containment_unresolvable" if sc_bad else
              "sufficiency_unresolvable")
    items = ([i.quote[:120] for i in fatals]
             + [d["quote"][:120] for d in det] + unfixed[:5])
    detail = "; ".join(items)[:900] or chk.summary[:400]
    ctx.progress(f"✗ excluded {tid} [{reason}]")
    return ("excluded", {"target_id": tid, "policy": "stage2",
                         "reason_code": reason, "detail": detail})


# ------------------------------------------------------------- per paper

def bootstrap(src_runs: Path, out_runs: Path, pid: str) -> None:
    """Copy the required input artifacts of a finished main-pipeline run
    (bundled under inputs/ by default)."""
    src, dst = src_runs / pid, out_runs / pid
    need = ["source/meta.json", "index/statements.v2.json",
            "roles/selection.json"]
    flat = next((f for f in ("source/flat.tex", "source/flat.md")
                 if (src / f).exists()), None)
    missing = [n for n in need if not (src / n).exists()]
    if flat is None or missing:
        raise SystemExit(f"{pid}: inputs incomplete under {src} "
                         f"(missing {missing or ['flat source']})")
    try:
        raw_index = json.loads((src / "index/statements.v2.json").read_text(
            encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"{pid}: cannot read prepared statement index: {exc}")
    if not isinstance(raw_index, dict) or raw_index.get("schema_version") != 2:
        raise SystemExit(
            f"{pid}: stale statement index; rerun Paper Cleaner Step 2/3 "
            "to create source/proof provenance schema version 2"
        )
    for rel in need + [flat]:
        d = dst / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        if (not d.exists()
                or (src / rel).stat().st_mtime > d.stat().st_mtime):
            shutil.copy2(src / rel, d)


def targets_of(sel: Selection) -> list[tuple[str, str]]:
    """(target_id, selected_as) in main-pipeline order: mains ∪ hardest."""
    ordered = list(dict.fromkeys([*sel.mains, *sel.hardest]))
    return [(t, "main+hardest" if t in sel.mains and t in sel.hardest
             else "main" if t in sel.mains else "hardest")
            for t in ordered]


def bibliography_text(index: StatementsIndex) -> str:
    """Render indexed bibliography entries with stable citation-key labels."""

    entries = []
    for citation in index.citations:
        raw = citation.raw_bib.strip()
        if raw:
            entries.append(f"% citation_key: {citation.key}\n{raw}")
    return "\n\n".join(entries) or "None supplied"


async def run_paper(cfg, src_runs: Path, out_runs: Path, pid: str,
                    models: dict, args) -> dict:
    bootstrap(src_runs, out_runs, pid)
    ctx = RunContext(pid, cfg, out_runs)
    ctx.step_name = STEP
    meta = ctx.read_model("source/meta.json", Meta)
    index = ctx.read_model("index/statements.v2.json", StatementsIndex)
    sel = ctx.read_model("roles/selection.json", Selection)
    raw_index = ctx.path("index/statements.v2.json").read_text("utf-8")
    sha = sha256_text(raw_index)[:16]
    flat_rel = ("source/flat.md" if meta.source_type == "ocr"
                else "source/flat.tex")
    # Keep the complete source for deterministic span/hash verification. Only
    # the model-facing binding is capped inside ``do_target``.
    flat = ctx.path(flat_rel).read_text(encoding="utf-8")
    std = load_std_commands(ctx)
    by_id = index.by_id()
    plan = [(t, s) for t, s in targets_of(sel) if t in by_id]
    if args.target_id:
        plan = [(t, s) for t, s in plan if t == args.target_id]
        if not plan:
            raise SystemExit(
                f"{pid}: target {args.target_id!r} is not selected in roles/selection.json"
            )

    if args.dry_run:
        print(f"[{pid}] {meta.title[:70]}")
        for tid, s_as in plan:
            st = by_id[tid]
            print(f"  {tid:<22} {s_as:<14} {st.env_type:<12} "
                  f"proof={len(st.proof_tex or '')} chars")
        return {"targets": len(plan)}

    # Preserve selected targets' frozen target.tex/target.json across retries.
    # Unselected directories are stale and must not survive a full-paper run.
    packages_root = ctx.path("packages")
    packages_root.mkdir(parents=True, exist_ok=True)
    if not args.target_id:
        planned_ids = {target_id for target_id, _ in plan}
        for child in packages_root.iterdir():
            if child.is_dir() and child.name not in planned_ids:
                shutil.rmtree(child)

    tally = {"calls": 0, "cached": 0, "in": 0, "out": 0, "reason": 0}
    sem = asyncio.Semaphore(args.parallel)

    async def guarded(tid, s_as):
        try:
            return await do_target(ctx, meta, index, flat, sha, by_id[tid],
                                   s_as, models, sem, std, args.max_repairs,
                                   tally)
        except TaskFailed as e:
            ctx.log_event(event="s2_task_failed", target=tid,
                          detail=str(e)[:300])
            return ("excluded", {"target_id": tid, "policy": "stage2",
                                 "reason_code": "package_build_error",
                                 "detail": f"llm task failed: {e}"[:300]})
        except Exception as e:                     # keep the batch alive
            ctx.log_event(event="s2_exception", target=tid,
                          detail=traceback.format_exc()[-1500:])
            print(f"  !! {pid}/{tid} crashed: {e!r}", file=sys.stderr,
                  flush=True)
            return ("excluded", {"target_id": tid, "policy": "stage2",
                                 "reason_code": "package_build_error",
                                 "detail": repr(e)[:300]})

    results = await asyncio.gather(*(guarded(t, s) for t, s in plan))
    shipped = [r[1] for r in results if r[0] == "shipped"]
    excluded = [r[1] for r in results if r[0] == "excluded"]

    manifest = Manifest(paper_id=pid, paper_date=meta.paper_date,
                        pipeline_version="stage2-min-source-v2", packages=shipped,
                        stats={"statements": len(index.statements),
                               "attempted": len(plan),
                               "shipped": len(shipped),
                               "excluded": len(excluded)})
    ctx.write_json("manifest.json", manifest)
    ctx.write_json("excluded.json", excluded)
    print(f"[{now_iso()}] {pid}: {len(shipped)}/{len(plan)} shipped, "
          f"{len(excluded)} excluded | live calls={tally['calls']} "
          f"cached={tally['cached']} in={tally['in']} out={tally['out']} "
          f"(reasoning {tally['reason']})", flush=True)
    return {"shipped": len(shipped), "excluded": len(excluded), **tally}


# ------------------------------------------------------------------ main

async def _main_async(args) -> int:
    cfg = load_config(args.config)
    cfg.llm.reasoning.reasoning_effort = args.effort
    cfg.llm.max_output_tokens.update(MAX_OUT)
    src_runs, out_runs = Path(args.src_runs), Path(args.out)

    if args.papers == "all":
        pids = sorted(d.name for d in src_runs.iterdir()
                      if (d / "roles/selection.json").exists())
    else:
        pids = [p.strip() for p in args.papers.split(",") if p.strip()]
    if not pids:
        print("no papers to process", file=sys.stderr)
        return 1
    if args.target_id and len(pids) != 1:
        print("--target-id requires exactly one paper id", file=sys.stderr)
        return 1

    if args.dry_run:
        for pid in pids:
            await run_paper(cfg, src_runs, out_runs, pid,
                            {"gen": "dry", "check": "dry"}, args)
        return 0

    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set", file=sys.stderr)
        return 3
    gen_model = await pick_model(cfg.provider, args.model)
    check_model = (await pick_model(cfg.provider, args.check_model)
                   if args.check_model else gen_model)
    models = {"gen": gen_model, "check": check_model}
    print(f"stage2 models: gen={gen_model} check={check_model} "
          f"(effort={args.effort}, parallel={args.parallel}, "
          f"max_repairs={args.max_repairs}) — papers: {', '.join(pids)}",
          flush=True)

    summary = {}
    for pid in pids:                 # serial across papers (TPM headroom)
        print(f"[{now_iso()}] stage2 {pid} ...", flush=True)
        summary[pid] = await run_paper(cfg, src_runs, out_runs, pid,
                                       models, args)
    (out_runs / "stage2_summary.json").write_text(json.dumps(
        {"models": models, "effort": args.effort, "generated_at": now_iso(),
         "papers": summary}, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"next: python audit.py --runs-dir {args.out} --papers all "
          f"--effort high")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="mini pipeline (author/check/repair, full paper)")
    ap.add_argument("--papers", default="all",
                    help='"all" or comma-separated paper ids')
    ap.add_argument("--src-runs", default="inputs",
                    help="input artifacts dir (bundled: inputs/)")
    ap.add_argument("--out", default="runs")
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--model", default="auto",
                    help='model for author/repair, or "auto" (strongest)')
    ap.add_argument("--check-model", default="",
                    help="cross-model checker (default: same as --model)")
    ap.add_argument("--effort", default="high",
                    choices=["low", "medium", "high"])
    ap.add_argument("--parallel", type=int, default=2,
                    help="concurrent LLM calls (whole-paper inputs; TPM!)")
    ap.add_argument("--max-repairs", type=int, default=2)
    ap.add_argument("--target-id", default="",
                    help="Process exactly one selected target id.")
    ap.add_argument("--dry-run", action="store_true",
                    help="bootstrap + print the target plan, no LLM calls")
    return run_async(_main_async(ap.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
