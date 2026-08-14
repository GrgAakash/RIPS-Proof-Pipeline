#!/usr/bin/env python3
"""Orchestrator (§11.1, §1.1, §1.2).

    python run.py --ids papers.txt --config config.yaml
    python run.py --arxiv 2506.12345
    python run.py --pdf ./local.pdf --paper-id mypaper1
    python run.py --arxiv 2506.12345 --stop-after step5
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import traceback
from pathlib import Path

from src.common import (Config, ConfigError, Rejected, RunContext, Status,
                        StepTimer, load_config, now_iso, step_input_hash)
from src import (step1_get_source, step2_parse, step3_fill_index, step4_deps,
                 step5_select_mains, step6_package, step7_verify,
                 step8_report)

# Per-step input_hash declaration: (name, module, input files, config fields,
# prompt templates). Deliberately lists only "upstream-stable" files —
# intermediates appended/rewritten by later steps (statements.v2, dep_graph,
# problem.md) stay out of the hash, so already-completed steps cannot
# invalidate themselves on a checkpoint-resume.
STEPS = [
    ("step1", step1_get_source, [], ["ocr"], []),
    ("step2", step2_parse,
     ["source/flat.tex", "source/flat.md", "source/macros.tex",
      "source/meta.json"], [], []),
    ("step3", step3_fill_index,
     ["index/statements.v1.json"],
     ["limits.section_chunk_chars", "models.a0"], ["a0"]),
    ("step4", step4_deps,
     ["index/statements.v1.json", "index/label_map.json", "source/meta.json"],
     ["limits", "models.a1"], ["a1", "a0"]),
    ("step5", step5_select_mains,
     ["index/statements.v1.json", "graph/dropped_edges.json",
      "source/meta.json"],
     ["pipeline.max_main_theorems", "pipeline.min_main_theorems",
      "pipeline.hardest_theorems", "pipeline.min_proof_chars", "models.a2"],
     ["a2"]),
    ("step6", step6_package,
     ["roles/selection.json", "index/label_map.json", "source/meta.json"],
     ["pipeline", "models.a3_ext"], ["a3_ext", "a3_cmp"]),
    ("step7", step7_verify,
     ["roles/selection.json", "source/meta.json"],
     ["pipeline.max_verify_iters", "pipeline.repair_agent",
      "pipeline.final_gate", "pipeline.appeal",
      "models.a4a", "models.a4b", "models.a4c", "models.a6", "models.a7"],
     ["a4a", "a4b", "a4c", "a6", "a7"]),
    ("step8", step8_report,                     # human-readable products: visualization + A5 rationale
     ["roles/selection.json", "roles/roles.json", "manifest.json",
      "excluded.json", "source/meta.json"],
     ["models.a5"], ["a5"]),
]

# Step-local revisions invalidate persisted status hashes when deterministic
# implementation changes alter an artifact without changing its file inputs.
STEP_HASH_REVISIONS = {
    "step2": "source-backed-opaque-ids-frozen-target-v5",
}


def process_paper(pid: str, cfg: Config, runs_dir: str,
                  arxiv_id: str | None = None,
                  pdf_path: str | None = None,
                  stop_after: str = "step8") -> tuple[str, str | None]:
    """Return (final_state, reason). Paper-level exception boundary (§11.1)."""
    ctx = RunContext(pid, cfg, runs_dir)
    st = Status(ctx)
    step_names = [name for name, *_ in STEPS]
    if stop_after not in step_names:
        raise ValueError(
            f"unknown stop step {stop_after!r}; expected one of {step_names}"
        )
    # No whole-paper short-circuit: per-step input_hash skipping is enough.
    # After a prompt/config change, rerunning the same batch recomputes only
    # the affected steps.
    for name, mod, files, cfg_keys, prompts in STEPS:
        h = step_input_hash(ctx, files, cfg_keys, prompts)
        if name in STEP_HASH_REVISIONS:
            h += f":{STEP_HASH_REVISIONS[name]}"
        if name == "step1":
            h += f":{arxiv_id or pdf_path}"
        if st.done(name, h):
            ctx.step_name = name
            ctx.progress("skipped (input hash unchanged)")
            if name == stop_after:
                break
            continue
        try:
            timer = StepTimer()
            ctx.step_name = name
            ctx.progress("started")
            if name == "step1":
                mod.run(ctx, arxiv_id=arxiv_id, pdf_path=pdf_path)
            else:
                mod.run(ctx)
            ctx.step_name = name
            ctx.progress(f"done in {timer.ms() / 1000:.0f}s")
            st.mark_done(name, h)
            if name == stop_after:
                break
        except Rejected as e:                   # rule-based rejection
            ctx.log_event(event="rejected", step=name, reason=e.reason,
                          detail=e.detail[:300])
            st.finalize("rejected", e.reason)
            return "rejected", e.reason
        except Exception as e:                  # program error
            ctx.log_event(event="exception", step=name, err=repr(e)[:500],
                          tb=traceback.format_exc()[-2000:])
            st.finalize("failed", repr(e)[:200])
            return "failed", repr(e)[:200]
    if stop_after == step_names[-1]:
        st.finalize("ok")
        return "ok", None

    # Successful source preparation is distinct from a complete legacy run.
    # Do not downgrade an existing complete run when its cache is reused.
    st.data["prepared_through"] = stop_after
    if st.data.get("final_state") != "ok":
        st.data["final_state"] = "prepared"
        st.data["reject_reason"] = None
    st.save()
    return "prepared", None


def write_batch_index(runs_dir: str, pids: list[str]) -> None:
    """runs/index.html: batch overview page (purely deterministic, links to each paper's dashboard)."""
    import html as _h
    rows = []
    for pid in pids:
        d = Path(runs_dir) / pid
        try:
            meta = json.loads((d / "source/meta.json").read_text("utf-8"))
        except Exception:
            meta = {}
        try:
            man = json.loads((d / "manifest.json").read_text("utf-8"))
            emitted = len(man.get("packages", []))
            attempted = man.get("stats", {}).get("targets_attempted", 0)
        except Exception:
            emitted, attempted = 0, 0
        try:
            sel = json.loads((d / "roles/selection.json").read_text("utf-8"))
            mains, hardest = sel.get("mains", []), sel.get("hardest", [])
        except Exception:
            mains, hardest = [], []
        ok = "background:#dcfce7;color:#166534" if emitted else \
             "background:#fee2e2;color:#991b1b"
        rows.append(
            f"<tr><td><b>{_h.escape(pid)}</b><br>"
            f"<span style='color:#64748b;font-size:12px'>"
            f"{_h.escape(str(meta.get('title', ''))[:90])}</span></td>"
            f"<td>{len(mains)} main / {len(hardest)} hardest</td>"
            f"<td><span style='padding:2px 10px;border-radius:999px;"
            f"font-weight:600;{ok}'>{emitted}/{attempted}</span></td>"
            f"<td><a href='{pid}/report/dashboard.html'>dashboard</a> · "
            f"<a href='{pid}/graph/dep_graph.html'>graph</a> · "
            f"<a href='{pid}/packages/SELECTION_RATIONALE.md'>rationale</a>"
            f"</td></tr>")
    out = ("<!DOCTYPE html><html><head><meta charset='utf-8'>"
           "<title>Paper Cleaner — batch overview</title><style>"
           "body{font-family:system-ui,sans-serif;background:#f1f5f9;"
           "color:#0f172a;margin:0}.w{max-width:900px;margin:0 auto;"
           "padding:30px 20px}h1{font-size:20px}"
           "table{border-collapse:collapse;width:100%;background:#fff;"
           "border-radius:10px;overflow:hidden;font-size:13.5px;"
           "box-shadow:0 1px 3px rgba(0,0,0,.08)}"
           "th{background:#1e293b;color:#e2e8f0;padding:9px 12px;"
           "text-align:left;font-size:12px}"
           "td{padding:10px 12px;border-top:1px solid #e2e8f0}"
           "a{color:#4f46e5;text-decoration:none}</style></head><body>"
           "<div class='w'><h1>Paper Cleaner — batch overview</h1>"
           "<table><tr><th>paper</th><th>selection</th>"
           "<th>emitted/attempted</th><th>reports</th></tr>"
           + "".join(rows) + "</table></div></body></html>")
    Path(runs_dir, "index.html").write_text(out, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Paper Cleaner v2.3 pipeline")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--ids", help="batch: file with one arXiv id per line")
    g.add_argument("--arxiv", help="single arXiv id")
    g.add_argument("--pdf", help="local PDF path")
    ap.add_argument("--paper-id", help="paper id for --pdf route")
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--runs-dir", default="runs")
    ap.add_argument(
        "--stop-after",
        choices=[name for name, *_ in STEPS],
        default="step8",
        help="Stop after this step. step5 prepares inputs for Paper Cleaner Mini.",
    )
    args = ap.parse_args()

    try:
        cfg = load_config(args.config)
        if args.pdf and not args.paper_id:
            raise ConfigError("--pdf requires --paper-id")
        # fail fast on missing credentials — otherwise the first failure
        # surfaces mid-run at step 3's first LLM call
        if cfg.provider == "openai" and not os.environ.get("OPENAI_API_KEY"):
            raise ConfigError("OPENAI_API_KEY is not set "
                              "(export OPENAI_API_KEY=... before running)")
        if cfg.provider == "azure":
            need = [v for v in ("AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT",
                                "OPENAI_API_VERSION")
                    if not os.environ.get(v)]
            if need:
                raise ConfigError(f"provider=azure requires env vars: "
                                  f"{', '.join(need)}")
    except ConfigError as e:
        print(f"config error: {e}", file=sys.stderr)
        return 3                                 # config error: exit at startup

    papers: list[tuple[str, str | None, str | None]] = []
    if args.ids:
        for line in Path(args.ids).read_text(encoding="utf-8").splitlines():
            aid = line.strip()
            if aid and not aid.startswith("#"):
                papers.append((aid.replace("/", "-"), aid, None))
    elif args.arxiv:
        papers.append((args.arxiv.replace("/", "-"), args.arxiv, None))
    else:
        papers.append((args.paper_id, None, args.pdf))

    summary = {"ok": [], "rejected": [], "failed": [], "degraded": [],
               "finished_at": ""}
    if args.stop_after != "step8":
        summary["prepared"] = []
    for pid, aid, pdf in papers:                 # serial across papers; parallel within a paper
        print(f"[{now_iso()}] processing {pid} ...", flush=True)
        try:
            state, reason = process_paper(pid, cfg, args.runs_dir,
                                          arxiv_id=aid, pdf_path=pdf,
                                          stop_after=args.stop_after)
        except Exception as e:                   # fallback: a single paper does not drag down the batch
            state, reason = "failed", repr(e)[:200]
        if state == "ok":
            summary["ok"].append(pid)
        elif state == "prepared":
            summary["prepared"].append(pid)
        elif state == "rejected":
            summary["rejected"].append({"id": pid, "reason": reason})
        else:
            summary["failed"].append({"id": pid, "reason": reason})
        gpath = Path(args.runs_dir) / pid / "graph/g4_degraded.json"
        if gpath.exists() and json.loads(gpath.read_text()).get("degraded"):
            summary["degraded"].append(pid)
        print(f"[{now_iso()}] {pid}: {state}"
              + (f" ({reason})" if reason else ""), flush=True)

    summary["finished_at"] = now_iso()
    out = Path(args.runs_dir) / "summary.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    if args.stop_after == "step8":
        try:
            write_batch_index(args.runs_dir, [p for p, _, _ in papers])
        except Exception as e:                   # human-readable products do not affect the exit code
            print(f"batch index generation failed: {e}", file=sys.stderr)
    display_keys = ("ok", "prepared", "rejected", "failed")
    print(json.dumps({k: summary[k] for k in display_keys if k in summary},
                     ensure_ascii=False))
    return 0 if not summary["rejected"] and not summary["failed"] else 2


if __name__ == "__main__":
    sys.exit(main())
