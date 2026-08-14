#!/usr/bin/env python3
"""Independent calibration audit — fully automated, no human step.

Re-checks the pipeline's own quality claims with (a) a deterministic full-text
leak scan and (b) an independent, stronger LLM that — unlike the pipeline's
a4a/a4b/a4c checkers — reads the FULL SOURCE PAPER while auditing:

  * every shipped package: is it really self-contained / leak-free /
    sufficient?  (audit_pkg)
  * every exclusion: was the drop justified, or a text-matching false kill
    when the paper does introduce the flagged items?  (audit_excl)

Outputs <runs-dir>/audit/audit_report.json + audit_report.md with per-item
verdicts and aggregate error-rate metrics for the pipeline's checkers.

    python audit.py --papers all
    python audit.py --papers 2604.04891,2606.19639 --model gpt-5.2

LLM responses are cached in each paper's runs/<id>/cache/ (audit_pkg-*.json),
so reruns are free and resumable. Requires OPENAI_API_KEY.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

from src.common import RunContext, load_config, now_iso, sha256_text
from src.gates import g3_macro_residue
from src.llm import call_llm, get_client, run_async
from src.schemas import DepGraph, Manifest, Meta, StatementsIndex
from src.step7_verify import ship_leak_spans
from src.target_integrity import (frozen_target_artifact_issues,
                                  proof_source_issues,
                                  statement_source_issues,
                                  target_identity_issues)

# Strongest-first; "auto" picks the first one the account actually serves.
# Must be a DIFFERENT model from the pipeline's a4a/a4b/a4c tier (gpt-4.1 /
# o4-mini), otherwise the audit inherits the same blind spots. Plain flagship
# ids only — -pro/-codex/-chat/-mini variants differ in API surface or tier.
MODEL_PREFERENCE = ("gpt-5.5", "gpt-5.4", "gpt-5.2", "gpt-5.1", "gpt-5",
                    "o3")

MAX_OUT = {"audit_pkg": 30000, "audit_excl": 16000}
FLAT_CAP = 600_000          # chars of source paper passed to the auditor


async def pick_model(provider: str, requested: str) -> str:
    if requested and requested != "auto":
        return requested
    client = get_client(provider)
    page = await client.models.list()
    have = {m.id for m in page.data}
    for m in MODEL_PREFERENCE:
        if m in have:
            return m
    # fall back: any gpt-5*/o3* the account serves, newest name first
    cand = sorted((m for m in have
                   if m.startswith(("gpt-5", "o3"))), reverse=True)
    if cand:
        return cand[0]
    raise SystemExit(f"no audit-grade model available; account serves: "
                     f"{sorted(have)[:20]} ...")


def _flat_source(ctx: RunContext, meta: Meta) -> str:
    p = ctx.path("source/flat.md" if meta.source_type == "ocr"
                 else "source/flat.tex")
    return p.read_text(encoding="utf-8")


async def audit_paper(cfg, runs_dir: str, pid: str, model: str,
                      sem: asyncio.Semaphore) -> dict:
    ctx = RunContext(pid, cfg, runs_dir)
    ctx.step_name = "audit"
    meta = ctx.read_model("source/meta.json", Meta)
    index = ctx.read_model("index/statements.v2.json", StatementsIndex)
    by_id = index.by_id()
    flat = _flat_source(ctx, meta)
    manifest = (ctx.read_model("manifest.json", Manifest)
                if ctx.path("manifest.json").exists() else Manifest(paper_id=pid))
    excluded = (ctx.read_json("excluded.json")
                if ctx.path("excluded.json").exists() else [])
    graph = (ctx.read_model("graph/dep_graph.json", DepGraph)
             if ctx.path("graph/dep_graph.json").exists() else DepGraph())

    out: dict = {"paper_id": pid, "title": meta.title,
                 "packages": [], "exclusions": []}

    async def one_pkg(entry):
        problem_md = ctx.path(entry.path).read_text(encoding="utf-8")
        target = by_id[entry.target_id]
        assembly = ctx.read_json(
            f"packages/{entry.target_id}/{entry.policy}/assembly.json")
        report = ctx.read_json(
            f"packages/{entry.target_id}/{entry.policy}/report.json")
        problem_sha = sha256_text(problem_md)
        claimed_sha = (report.get("problem_sha256")
                       or report.get("input_hashes", {}).get("problem", ""))
        hash_matches = bool(claimed_sha) and claimed_sha == problem_sha
        det_spans = ship_leak_spans(index, graph, target, problem_md,
                                    assembly)
        unknown_cmds, _ = g3_macro_residue(ctx, problem_md,
                                           index.macros_tex, flat)
        source_file = ("source/flat.md" if meta.source_type == "ocr"
                       else "source/flat.tex")
        target_issues = statement_source_issues(
            target, flat_source=flat, expected_source_file=source_file)
        target_issues.extend(proof_source_issues(
            target, flat_source=flat, expected_source_file=source_file))
        target_issues.extend(target_identity_issues(problem_md, target))
        target_tex = ctx.path(
            f"packages/{entry.target_id}/{entry.policy}/target.tex")
        target_json = ctx.path(
            f"packages/{entry.target_id}/{entry.policy}/target.json")
        if not target_tex.exists() or not target_json.exists():
            target_issues.append("frozen target artifacts are missing")
        else:
            try:
                target_record = ctx.read_json(
                    f"packages/{entry.target_id}/{entry.policy}/target.json")
            except (OSError, ValueError, TypeError) as exc:
                target_issues.append(f"target.json is unreadable: {exc}")
            else:
                target_issues.extend(frozen_target_artifact_issues(
                    target, target_tex=target_tex.read_text(encoding="utf-8"),
                    record=target_record))
        claims = (f"self_contained={report.get('self_contained')}, "
                  f"leak_clean={report.get('leak_clean')}, "
                  f"sufficient={report.get('sufficiency')}, "
                  f"verify_iterations={report.get('iterations')}, "
                  f"baseline_assumed={report.get('baseline_assumed')}")
        async with sem:
            llm = await call_llm(ctx, "audit_pkg", {
                "paper_title": meta.title, "flat_source": flat[:FLAT_CAP],
                "problem_md": problem_md, "pipeline_claims": claims,
                "field_baseline": meta.field_baseline}, model=model)
        audit_row = llm.model_dump()
        audit_row["issues"].extend({
            "kind": "other", "quote": target.statement_tex[:300],
            "explanation": issue, "severity": "fatal",
            "fix_hint": "regenerate and freeze the target from its exact source span",
        } for issue in target_issues)
        audit_pass = (
            bool(llm.self_contained)
            and bool(llm.leak_free)
            and bool(llm.sufficient)
            and not det_spans
            and not unknown_cmds
            and not target_issues
            and hash_matches
            and not any(issue.get("severity") == "fatal"
                        for issue in audit_row["issues"])
        )
        rec = {"target_id": entry.target_id, "policy": entry.policy,
               "pipeline_claims": claims,
               "problem_sha256": problem_sha,
               "claimed_problem_sha256": claimed_sha,
               "hash_matches": hash_matches,
               "det_leak_spans": [s[:200] for s in det_spans[:5]],
               "det_unknown_commands": unknown_cmds[:10],
               "det_target_issues": target_issues,
               "audit_pass": audit_pass,
               "audit": audit_row}
        print(f"  [pkg ] {pid}/{entry.target_id}: "
              f"sc={llm.self_contained} leak_free={llm.leak_free} "
              f"suff={llm.sufficient} issues="
              f"{sum(1 for i in llm.issues if i.severity == 'fatal')} fatal"
              f"/{len(llm.issues)} | det_scan={len(det_spans)} hits "
              f"target_integrity={len(target_issues)} issues",
              flush=True)
        return rec

    async def one_excl(exc):
        target = by_id.get(exc["target_id"])
        async with sem:
            llm = await call_llm(ctx, "audit_excl", {
                "paper_title": meta.title, "flat_source": flat[:FLAT_CAP],
                "target_id": exc["target_id"],
                "target_statement": target.statement_tex if target else "",
                "target_proof": (target.proof_tex or "")[:20000] if target else "",
                "reason_code": exc["reason_code"],
                "detail": exc.get("detail", ""),
                "field_baseline": meta.field_baseline}, model=model)
        rec = {"target_id": exc["target_id"], "policy": exc.get("policy", ""),
               "reason_code": exc["reason_code"],
               "detail": exc.get("detail", ""), "audit": llm.model_dump()}
        print(f"  [excl] {pid}/{exc['target_id']} ({exc['reason_code']}): "
              f"justified={llm.exclusion_justified} "
              f"paper_resolves_it={llm.paper_resolves_it}", flush=True)
        return rec

    pkg_jobs = [one_pkg(e) for e in manifest.packages]
    exc_jobs = [one_excl(e) for e in excluded]
    results = await asyncio.gather(*pkg_jobs, *exc_jobs)
    out["packages"] = results[:len(pkg_jobs)]
    out["exclusions"] = results[len(pkg_jobs):]
    return out


def _metrics(papers: list[dict]) -> dict:
    pkgs = [p for pp in papers for p in pp["packages"]]
    excl = [e for pp in papers for e in pp["exclusions"]]
    return {
        "packages_audited": len(pkgs),
        "pkg_not_self_contained": sum(
            1 for p in pkgs if not p["audit"]["self_contained"]),
        "pkg_leak_flagged": sum(1 for p in pkgs if not p["audit"]["leak_free"]),
        "pkg_insufficient": sum(1 for p in pkgs if not p["audit"]["sufficient"]),
        "pkg_with_fatal_issues": sum(
            1 for p in pkgs if any(i["severity"] == "fatal"
                                   for i in p["audit"]["issues"])),
        "pkg_det_leak_scan_hits": sum(
            1 for p in pkgs if p["det_leak_spans"]),
        "pkg_target_integrity_failures": sum(
            1 for p in pkgs if p["det_target_issues"]),
        "pkg_hash_mismatch": sum(
            1 for p in pkgs if not p["hash_matches"]),
        "pkg_not_ready": sum(
            1 for p in pkgs if not p["audit_pass"]),
        "exclusions_audited": len(excl),
        "exclusions_disputed": sum(
            1 for e in excl if not e["audit"]["exclusion_justified"]),
        "exclusions_paper_resolves": sum(
            1 for e in excl if e["audit"]["paper_resolves_it"]),
    }


def _markdown(model: str, papers: list[dict], metrics: dict) -> str:
    L = [f"# Calibration audit report", "",
         f"*independent auditor model: `{model}` · generated {now_iso()} · "
         f"fully automated (audit.py)*", "",
         "## Aggregate metrics", ""]
    L += [f"- **{k}**: {v}" for k, v in metrics.items()]
    L += ["", "## Shipped packages — pipeline claims vs auditor", "",
          "| paper | target | pipeline | auditor sc/leak-free/suff | fatal "
          "issues | det scan | hash | ready | confidence |",
          "|---|---|---|---|---|---|---|---|---|"]
    for pp in papers:
        for p in pp["packages"]:
            a = p["audit"]
            fatals = [i for i in a["issues"] if i["severity"] == "fatal"]
            L.append(
                f"| {pp['paper_id']} | {p['target_id']} | all-clean | "
                f"{a['self_contained']}/{a['leak_free']}/{a['sufficient']} | "
                f"{len(fatals)} | {len(p['det_leak_spans'])} hits | "
                f"{p['hash_matches']} | {p['audit_pass']} | {a['confidence']} |")
    L += ["", "### Fatal issues detail", ""]
    any_fatal = False
    for pp in papers:
        for p in pp["packages"]:
            for i in p["audit"]["issues"]:
                if i["severity"] == "fatal":
                    any_fatal = True
                    L.append(f"- **{pp['paper_id']}/{p['target_id']}** "
                             f"[{i['kind']}] {i['quote'][:160]} — "
                             f"{i['explanation'][:300]}")
    if not any_fatal:
        L.append("(none)")
    L += ["", "## Exclusions — was the drop justified?", "",
          "| paper | target | reason | justified | paper resolves it | "
          "confidence |", "|---|---|---|---|---|---|"]
    for pp in papers:
        for e in pp["exclusions"]:
            a = e["audit"]
            L.append(f"| {pp['paper_id']} | {e['target_id']} | "
                     f"{e['reason_code']} | {a['exclusion_justified']} | "
                     f"{a['paper_resolves_it']} | {a['confidence']} |")
    L += ["", "### Disputed exclusions detail", ""]
    any_disp = False
    for pp in papers:
        for e in pp["exclusions"]:
            a = e["audit"]
            if not a["exclusion_justified"]:
                any_disp = True
                L.append(f"- **{pp['paper_id']}/{e['target_id']}** "
                         f"(dropped for: {e['detail'][:120]}) — "
                         f"{a['verdict'][:400]}")
                if a["where_in_paper"]:
                    L.append(f"  - paper introduces it at: "
                             f"“{a['where_in_paper'][:300]}”")
    if not any_disp:
        L.append("(none — every audited exclusion was justified)")
    L += ["", "### Package summaries", ""]
    for pp in papers:
        for p in pp["packages"]:
            L.append(f"- **{pp['paper_id']}/{p['target_id']}** — "
                     f"{p['audit']['summary']}")
    return "\n".join(L) + "\n"


async def _main_async(args) -> int:
    cfg = load_config(args.config)
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set", file=sys.stderr)
        return 3
    cfg.llm.reasoning.reasoning_effort = args.effort
    cfg.llm.max_output_tokens.update(MAX_OUT)

    runs = Path(args.runs_dir)
    if args.papers == "all":
        pids = sorted(d.name for d in runs.iterdir()
                      if (d / "manifest.json").exists())
    else:
        pids = [p.strip() for p in args.papers.split(",") if p.strip()]
    if not pids:
        print("no papers to audit", file=sys.stderr)
        return 1

    model = await pick_model(cfg.provider, args.model)
    n_pkgs = n_excl = 0
    for pid in pids:
        d = runs / pid
        if (d / "manifest.json").exists():
            n_pkgs += len(json.loads((d / "manifest.json")
                                     .read_text("utf-8")).get("packages", []))
        if (d / "excluded.json").exists():
            n_excl += len(json.loads((d / "excluded.json").read_text("utf-8")))
    print(f"auditor model: {model} (effort={args.effort}) — "
          f"{n_pkgs} packages + {n_excl} exclusions across "
          f"{len(pids)} papers", flush=True)

    sem = asyncio.Semaphore(args.parallel)
    papers = []
    for pid in pids:                        # serial across papers, parallel within
        print(f"[{now_iso()}] auditing {pid} ...", flush=True)
        papers.append(await audit_paper(cfg, args.runs_dir, pid, model, sem))

    metrics = _metrics(papers)
    out_dir = runs / "audit"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "audit_report.json").write_text(json.dumps(
        {"model": model, "generated_at": now_iso(), "metrics": metrics,
         "papers": papers}, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "audit_report.md").write_text(
        _markdown(model, papers, metrics), encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    print(f"report: {out_dir}/audit_report.md")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="independent calibration audit")
    ap.add_argument("--papers", default="all",
                    help='"all" or comma-separated paper ids')
    ap.add_argument("--runs-dir", default="runs")
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--model", default="auto",
                    help='auditor model id, or "auto" (strongest available)')
    ap.add_argument("--effort", default="high",
                    choices=["low", "medium", "high"])
    ap.add_argument("--parallel", type=int, default=2,
                    help="concurrent audit calls (inputs are whole papers — keep low for TPM)")
    return run_async(_main_async(ap.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
