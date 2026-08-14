#!/usr/bin/env python3
"""Side-by-side comparison of two audit_report.json files produced by the
same judge (audit.py) over two pipelines' outputs.

    python compare_audits.py runs/audit/audit_report.json \\
        runs_stage2/audit/audit_report.json \\
        --label-a pipeline-v2.3 --label-b stage2-min-source-v2
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def index_report(rep: dict) -> tuple[dict, dict]:
    pkgs, excl = {}, {}
    for pp in rep["papers"]:
        for p in pp["packages"]:
            pkgs[(pp["paper_id"], p["target_id"])] = p
        for e in pp["exclusions"]:
            excl[(pp["paper_id"], e["target_id"])] = e
    return pkgs, excl


def all_clean(p: dict) -> bool:
    a = p["audit"]
    return (a["self_contained"] and a["leak_free"] and a["sufficient"]
            and not any(i["severity"] == "fatal" for i in a["issues"]))


def n_fatal(p: dict) -> int:
    return sum(1 for i in p["audit"]["issues"] if i["severity"] == "fatal")


def cell(key, pkgs, excl) -> str:
    if key in pkgs:
        p, a = pkgs[key], pkgs[key]["audit"]
        b = lambda v: "✓" if v else "✗"
        return (f"shipped · sc={b(a['self_contained'])} "
                f"lf={b(a['leak_free'])} suff={b(a['sufficient'])} · "
                f"{n_fatal(p)} fatal · det {len(p['det_leak_spans'])}")
    if key in excl:
        e, a = excl[key], excl[key]["audit"]
        b = lambda v: "✓" if v else "✗"
        return (f"excluded[{e['reason_code']}] · "
                f"justified={b(a['exclusion_justified'])} "
                f"paper_resolves={b(a['paper_resolves_it'])}")
    return "—"


def aggregate(pkgs: dict, excl: dict) -> dict:
    return {
        "packages shipped": len(pkgs),
        "all-clean packages (sc∧lf∧suff∧0 fatal)":
            sum(1 for p in pkgs.values() if all_clean(p)),
        "packages with fatal issues":
            sum(1 for p in pkgs.values() if n_fatal(p)),
        "total fatal issues": sum(n_fatal(p) for p in pkgs.values()),
        "det leak-scan hits":
            sum(1 for p in pkgs.values() if p["det_leak_spans"]),
        "exclusions": len(excl),
        "exclusions disputed by auditor":
            sum(1 for e in excl.values()
                if not e["audit"]["exclusion_justified"]),
        "exclusions the paper resolves (false kills)":
            sum(1 for e in excl.values()
                if e["audit"]["paper_resolves_it"]),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="compare two audit reports")
    ap.add_argument("baseline")
    ap.add_argument("candidate")
    ap.add_argument("--label-a", default="baseline")
    ap.add_argument("--label-b", default="candidate")
    ap.add_argument("--out", default="",
                    help="output md (default: comparison.md next to candidate)")
    args = ap.parse_args()

    ra, rb = load(args.baseline), load(args.candidate)
    pa, ea = index_report(ra)
    pb, eb = index_report(rb)
    A, B = args.label_a, args.label_b

    L = ["# Audit comparison", "",
         f"*judge: `{ra['model']}` vs `{rb['model']}` · "
         f"A = {A} ({ra['generated_at']}) · "
         f"B = {B} ({rb['generated_at']})*", "",
         "## Aggregate", "",
         f"| metric | {A} | {B} |", "|---|---|---|"]
    agg_a, agg_b = aggregate(pa, ea), aggregate(pb, eb)
    for k in agg_a:
        L.append(f"| {k} | {agg_a[k]} | {agg_b[k]} |")

    L += ["", "## Per target", "",
          f"| paper | target | {A} | {B} |", "|---|---|---|---|"]
    keys = sorted(set(pa) | set(ea) | set(pb) | set(eb))
    for key in keys:
        L.append(f"| {key[0]} | {key[1]} | {cell(key, pa, ea)} | "
                 f"{cell(key, pb, eb)} |")

    wins = [k for k in keys if k in pb and all_clean(pb[k])
            and not (k in pa and all_clean(pa[k]))]
    losses = [k for k in keys if k in pa and all_clean(pa[k])
              and not (k in pb and all_clean(pb[k]))]
    L += ["", "## Verdict deltas", "",
          f"- all-clean in {B} but not in {A}: "
          + (", ".join(f"{p}/{t}" for p, t in wins) or "(none)"),
          f"- all-clean in {A} but not in {B}: "
          + (", ".join(f"{p}/{t}" for p, t in losses) or "(none)")]

    L += ["", f"## Fatal issues in {B} (detail)", ""]
    any_f = False
    for (pid, tid), p in sorted(pb.items()):
        for i in p["audit"]["issues"]:
            if i["severity"] == "fatal":
                any_f = True
                L.append(f"- **{pid}/{tid}** [{i['kind']}] "
                         f"{i['quote'][:140]} — {i['explanation'][:220]}")
    if not any_f:
        L.append("(none)")

    md = "\n".join(L) + "\n"
    out = Path(args.out) if args.out else (
        Path(args.candidate).parent / "comparison.md")
    out.write_text(md, encoding="utf-8")
    print(md)
    print(f"written: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
