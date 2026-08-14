#!/usr/bin/env python3
"""Independent calibration audit — same judge as the main repo's audit.py,
ported onto minilib (identical prompts, schemas and deterministic scans).

Re-checks quality claims with (a) a deterministic full-text leak scan and
(b) an independent, stronger LLM that reads the FULL SOURCE PAPER:

  * every shipped package: really self-contained / leak-free / sufficient?
  * every exclusion: justified, or a false kill the paper resolves?

Outputs <runs-dir>/audit/audit_report.json + audit_report.md.

    python audit.py --papers all
    python audit.py --papers 2604.04891 --model gpt-5.5 --effort high

LLM responses cache in each paper's <runs-dir>/<id>/cache/, so reruns are
free and resumable. Requires OPENAI_API_KEY.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

from audit_gate import package_audit_pass
from minilib import (AuditExclOut, AuditPkgOut, DepGraph, Manifest, Meta,
                     RunContext, StatementsIndex, call_llm,
                     g3_macro_residue, load_config, now_iso, pick_model,
                     run_async, sha256_text, ship_leak_spans)
from package_validation import (frozen_target_artifact_issues,
                                frozen_target_record,
                                proof_source_issues,
                                statement_source_issues,
                                target_identity_issues)

MAX_OUT = {"audit_pkg": 30000, "audit_excl": 16000}
FLAT_CAP = 600_000          # chars of source paper passed to the auditor


def _flat_source(ctx: RunContext, meta: Meta) -> str:
    p = ctx.path("source/flat.md" if meta.source_type == "ocr"
                 else "source/flat.tex")
    return p.read_text(encoding="utf-8")


async def audit_paper(cfg, runs_dir: str, pid: str, model: str,
                      sem: asyncio.Semaphore, target_id: str = "") -> dict:
    ctx = RunContext(pid, cfg, runs_dir)
    ctx.step_name = "audit"
    meta = ctx.read_model("source/meta.json", Meta)
    index = ctx.read_model("index/statements.v2.json", StatementsIndex)
    by_id = index.by_id()
    flat = _flat_source(ctx, meta)
    manifest = (ctx.read_model("manifest.json", Manifest)
                if ctx.path("manifest.json").exists()
                else Manifest(paper_id=pid))
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
        claims = (f"self_contained={report.get('self_contained')}, "
                  f"leak_clean={report.get('leak_clean')}, "
                  f"sufficient={report.get('sufficiency')}, "
                  f"verify_iterations={report.get('iterations')}, "
                  f"baseline_assumed={report.get('baseline_assumed')}")
        async with sem:
            llm = await call_llm(ctx, "audit_pkg", {
                "paper_title": meta.title, "flat_source": flat[:FLAT_CAP],
                "problem_md": problem_md, "pipeline_claims": claims,
                "field_baseline": meta.field_baseline},
                schema=AuditPkgOut, model=model)
        identity_issues = target_identity_issues(
            problem_md,
            statement_tex=target.statement_tex,
            statement_sha256=target.statement_sha256,
        )
        source_file = ("source/flat.md" if meta.source_type == "ocr"
                       else "source/flat.tex")
        for issue in statement_source_issues(
                added_by=target.added_by,
                source_verified=target.source_verified,
                source_file=target.source_file,
                source_start=target.source_start,
                source_end=target.source_end,
                source_sha256=target.source_sha256,
                statement_tex=target.statement_tex,
                statement_sha256=target.statement_sha256,
                flat_source=flat,
                expected_source_file=source_file):
            identity_issues.append({
                "kind": "other", "quote": target.statement_tex[:300],
                "explanation": issue, "severity": "fatal",
                "fix_hint": "regenerate the target from the deterministic source parser"})
        for issue in proof_source_issues(
                proof_tex=target.proof_tex or "",
                proof_sha256=target.proof_sha256,
                proof_source_file=target.proof_source_file,
                proof_source_start=target.proof_source_start,
                proof_source_end=target.proof_source_end,
                proof_source_sha256=target.proof_source_sha256,
                proof_source_verified=target.proof_source_verified,
                proof_pairing=target.proof_pairing,
                flat_source=flat,
                expected_source_file=source_file):
            identity_issues.append({
                "kind": "other", "quote": (target.proof_tex or "")[:300],
                "explanation": issue, "severity": "fatal",
                "fix_hint": "reparse and source-authenticate the reference proof"})
        target_tex_path = ctx.path(
            f"packages/{entry.target_id}/{entry.policy}/target.tex")
        target_json_path = ctx.path(
            f"packages/{entry.target_id}/{entry.policy}/target.json")
        if not target_tex_path.exists() or not target_json_path.exists():
            artifact_issues = ["frozen target artifacts are missing"]
        else:
            try:
                target_record = ctx.read_json(
                    f"packages/{entry.target_id}/{entry.policy}/target.json")
            except (OSError, ValueError, TypeError) as exc:
                artifact_issues = [f"target.json is unreadable: {exc}"]
            else:
                artifact_issues = frozen_target_artifact_issues(
                    target_tex=target_tex_path.read_text(encoding="utf-8"),
                    statement_tex=target.statement_tex,
                    record=target_record,
                    expected_record=frozen_target_record(
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
                        proof_pairing=target.proof_pairing))
        for issue in artifact_issues:
            identity_issues.append({
                "kind": "other", "quote": target.statement_tex[:300],
                "explanation": issue, "severity": "fatal",
                "fix_hint": "restore target.tex and target.json from the source-backed index"})
        issue_rows = [issue.model_dump() for issue in llm.issues]
        issue_rows.extend(identity_issues)
        audit_pass = package_audit_pass(
            self_contained=llm.self_contained,
            leak_free=llm.leak_free,
            sufficient=llm.sufficient,
            issues=issue_rows,
            det_leak_spans=det_spans,
            unknown_commands=unknown_cmds,
            hash_matches=hash_matches,
        )
        rec = {"target_id": entry.target_id, "policy": entry.policy,
               "pipeline_claims": claims,
               "problem_sha256": problem_sha,
               "claimed_problem_sha256": claimed_sha,
               "hash_matches": hash_matches,
               "det_leak_spans": [s[:200] for s in det_spans[:5]],
               "det_unknown_commands": unknown_cmds[:10],
               "det_target_issues": identity_issues,
               "audit_pass": audit_pass,
               "audit": llm.model_dump()}
        print(f"  [pkg ] {pid}/{entry.target_id}: "
              f"sc={llm.self_contained} leak_free={llm.leak_free} "
              f"suff={llm.sufficient} issues="
              f"{sum(1 for i in llm.issues if i.severity == 'fatal')} fatal"
              f"/{len(llm.issues)} | det_scan={len(det_spans)} hits "
              f"target_identity={len(identity_issues)} issues "
              f"ready={audit_pass}",
              flush=True)
        return rec

    async def one_excl(exc):
        target = by_id.get(exc["target_id"])
        async with sem:
            llm = await call_llm(ctx, "audit_excl", {
                "paper_title": meta.title, "flat_source": flat[:FLAT_CAP],
                "target_id": exc["target_id"],
                "target_statement": target.statement_tex if target else "",
                "target_proof":
                    (target.proof_tex or "")[:20000] if target else "",
                "reason_code": exc["reason_code"],
                "detail": exc.get("detail", ""),
                "field_baseline": meta.field_baseline},
                schema=AuditExclOut, model=model)
        rec = {"target_id": exc["target_id"],
               "policy": exc.get("policy", ""),
               "reason_code": exc["reason_code"],
               "detail": exc.get("detail", ""), "audit": llm.model_dump()}
        print(f"  [excl] {pid}/{exc['target_id']} ({exc['reason_code']}): "
              f"justified={llm.exclusion_justified} "
              f"paper_resolves_it={llm.paper_resolves_it}", flush=True)
        return rec

    package_entries = [e for e in manifest.packages
                       if not target_id or e.target_id == target_id]
    exclusion_entries = [e for e in excluded
                         if not target_id or e.get("target_id") == target_id]
    pkg_jobs = [one_pkg(e) for e in package_entries]
    exc_jobs = [one_excl(e) for e in exclusion_entries]
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
        "pkg_leak_flagged": sum(
            1 for p in pkgs if not p["audit"]["leak_free"]),
        "pkg_insufficient": sum(
            1 for p in pkgs if not p["audit"]["sufficient"]),
        "pkg_with_fatal_issues": sum(
            1 for p in pkgs if any(i["severity"] == "fatal"
                                   for i in p["audit"]["issues"])),
        "pkg_det_leak_scan_hits": sum(
            1 for p in pkgs if p["det_leak_spans"]),
        "pkg_unknown_commands": sum(
            1 for p in pkgs if p["det_unknown_commands"]),
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
         f"fully automated (audit.py, mini)*", "",
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
    if args.target_id and len(pids) != 1:
        print("--target-id requires exactly one paper id", file=sys.stderr)
        return 1

    model = await pick_model(cfg.provider, args.model)
    n_pkgs = n_excl = 0
    for pid in pids:
        d = runs / pid
        if (d / "manifest.json").exists():
            packages = json.loads(
                (d / "manifest.json").read_text("utf-8")).get("packages", [])
            n_pkgs += sum(1 for package in packages
                          if not args.target_id
                          or package.get("target_id") == args.target_id)
        if (d / "excluded.json").exists():
            exclusions = json.loads((d / "excluded.json").read_text("utf-8"))
            n_excl += sum(1 for exclusion in exclusions
                          if not args.target_id
                          or exclusion.get("target_id") == args.target_id)
    print(f"auditor model: {model} (effort={args.effort}) — "
          f"{n_pkgs} packages + {n_excl} exclusions across "
          f"{len(pids)} papers", flush=True)

    sem = asyncio.Semaphore(args.parallel)
    papers = []
    for pid in pids:              # serial across papers, parallel within
        print(f"[{now_iso()}] auditing {pid} ...", flush=True)
        papers.append(await audit_paper(
            cfg, args.runs_dir, pid, model, sem, target_id=args.target_id
        ))

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
    if args.fail_on_package_issues:
        if metrics["packages_audited"] != 1 or metrics["pkg_not_ready"]:
            print("selected package did not pass the enforced audit gate", file=sys.stderr)
            return 2
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="independent calibration audit (mini)")
    ap.add_argument("--papers", default="all",
                    help='"all" or comma-separated paper ids')
    ap.add_argument("--runs-dir", default="runs")
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--model", default="auto",
                    help='auditor model id, or "auto" (strongest available)')
    ap.add_argument("--effort", default="high",
                    choices=["low", "medium", "high"])
    ap.add_argument("--parallel", type=int, default=2,
                    help="concurrent audit calls (whole-paper inputs)")
    ap.add_argument("--target-id", default="",
                    help="Audit exactly one target id.")
    ap.add_argument("--fail-on-package-issues", action="store_true",
                    help="Return exit code 2 unless one selected package passes.")
    return run_async(_main_async(ap.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
