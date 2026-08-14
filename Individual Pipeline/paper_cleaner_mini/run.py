#!/usr/bin/env python3
"""Run Paper Cleaner Mini from one arXiv ID or arxiv.org URL."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


MINI_DIR = Path(__file__).resolve().parent
REPO_ROOT = MINI_DIR.parent
MODERN_ARXIV_ID = re.compile(r"^[0-9]{4}\.[0-9]{4,5}(?:v[0-9]+)?$")
LEGACY_ARXIV_ID = re.compile(r"^[a-z0-9.-]+/[0-9]{7}(?:v[0-9]+)?$")
ARXIV_HOSTS = {"arxiv.org", "www.arxiv.org", "export.arxiv.org"}


class MiniRunError(RuntimeError):
    """Raised when an arXiv-first Mini stage cannot continue."""


def normalize_arxiv_reference(value: str) -> str:
    """Return a validated arXiv ID from an ID, prefix, abstract URL, or PDF URL."""

    candidate = value.strip()
    if not candidate:
        raise MiniRunError("arXiv reference is empty")
    if candidate.lower().startswith("arxiv:"):
        candidate = candidate.split(":", 1)[1].strip()
    if candidate.lower().startswith(("arxiv.org/", "www.arxiv.org/")):
        candidate = "https://" + candidate

    parsed = urlparse(candidate)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() not in ARXIV_HOSTS:
            raise MiniRunError("only arxiv.org links are accepted")
        parts = [part for part in parsed.path.split("/") if part]
        if parts and parts[0].lower() in {"abs", "pdf", "html"}:
            parts = parts[1:]
        candidate = "/".join(parts)

    candidate = candidate.split("?", 1)[0].split("#", 1)[0].strip("/")
    if candidate.lower().endswith(".pdf"):
        candidate = candidate[:-4]
    candidate = candidate.lower()
    if not (MODERN_ARXIV_ID.fullmatch(candidate) or LEGACY_ARXIV_ID.fullmatch(candidate)):
        raise MiniRunError(
            f"invalid arXiv reference {value!r}; expected an ID such as "
            "2604.04891 or an arxiv.org/abs/... link"
        )
    return candidate


def paper_id_for(arxiv_id: str) -> str:
    """Map an arXiv ID to the directory convention used by Paper Cleaner."""

    return arxiv_id.replace("/", "-")


def _paths(args: argparse.Namespace) -> dict[str, Path]:
    return {
        "upstream": args.upstream_cleaner_dir.resolve(),
        "upstream_config": args.upstream_config.resolve(),
        "inputs": args.input_root.resolve(),
        "output": args.out.resolve(),
        "mini_config": args.config.resolve(),
    }


def build_commands(args: argparse.Namespace, arxiv_id: str, paper_id: str) -> list[tuple[str, Path, list[str]]]:
    """Build the three subprocess calls without executing or shell-quoting them."""

    paths = _paths(args)
    upstream_script = paths["upstream"] / "run.py"
    stage2_script = MINI_DIR / "stage2.py"
    audit_script = MINI_DIR / "audit.py"
    for script in (upstream_script, stage2_script, audit_script):
        if not script.is_file():
            raise MiniRunError(f"required pipeline script does not exist: {script}")

    upstream = [
        sys.executable,
        str(upstream_script),
        "--arxiv", arxiv_id,
        "--config", str(paths["upstream_config"]),
        "--runs-dir", str(paths["inputs"]),
        "--stop-after", "step5",
    ]
    stage2 = [
        sys.executable,
        str(stage2_script),
        "--papers", paper_id,
        "--src-runs", str(paths["inputs"]),
        "--out", str(paths["output"]),
        "--config", str(paths["mini_config"]),
        "--model", args.model,
        "--effort", args.effort,
        "--parallel", str(args.parallel),
        "--max-repairs", str(args.max_repairs),
    ]
    if args.check_model:
        stage2.extend(["--check-model", args.check_model])
    if args.target_id:
        stage2.extend(["--target-id", args.target_id])

    audit = [
        sys.executable,
        str(audit_script),
        "--papers", paper_id,
        "--runs-dir", str(paths["output"]),
        "--config", str(paths["mini_config"]),
        "--model", args.audit_model,
        "--effort", args.effort,
        "--parallel", str(args.parallel),
    ]
    if args.target_id:
        audit.extend(["--target-id", args.target_id, "--fail-on-package-issues"])

    return [
        ("prepare arXiv source through Step 5", paths["upstream"], upstream),
        ("run Mini author/check/repair", MINI_DIR, stage2),
        ("run independent Mini audit", MINI_DIR, audit),
    ]


def _run_checked(label: str, cwd: Path, command: list[str]) -> None:
    print(f"[mini] {label}", flush=True)
    completed = subprocess.run(command, cwd=cwd, check=False)
    if completed.returncode:
        raise MiniRunError(
            f"{label} failed with exit code {completed.returncode}"
        )


def _read_json(path: Path, description: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MiniRunError(f"cannot read {description} at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise MiniRunError(f"{description} must be a JSON object: {path}")
    return value


def _selected_targets(input_root: Path, paper_id: str) -> list[str]:
    selection = _read_json(
        input_root / paper_id / "roles" / "selection.json",
        "upstream theorem selection",
    )
    targets = []
    for key in ("mains", "hardest"):
        values = selection.get(key, [])
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            raise MiniRunError(f"selection field {key!r} must be a list of target IDs")
        targets.extend(values)
    return list(dict.fromkeys(targets))


def _verify_outputs(output_root: Path, paper_id: str, target_id: str) -> tuple[int, Path]:
    manifest_path = output_root / paper_id / "manifest.json"
    manifest = _read_json(manifest_path, "Mini manifest")
    packages = manifest.get("packages", [])
    if not isinstance(packages, list):
        raise MiniRunError(f"Mini manifest packages must be a list: {manifest_path}")
    if target_id:
        packages = [item for item in packages if item.get("target_id") == target_id]
    if not packages:
        raise MiniRunError(
            "Mini shipped no package for the requested scope; inspect "
            f"{output_root / paper_id / 'excluded.json'}"
        )

    audit_path = output_root / "audit" / "audit_report.json"
    audit = _read_json(audit_path, "independent audit report")
    metrics = audit.get("metrics", {})
    if not isinstance(metrics, dict):
        raise MiniRunError(f"audit metrics must be an object: {audit_path}")
    if metrics.get("pkg_not_ready", 0):
        raise MiniRunError(
            "one or more Mini packages failed the independent audit; inspect "
            f"{audit_path}"
        )
    if metrics.get("packages_audited") != len(packages):
        raise MiniRunError(
            "independent audit package count does not match the Mini manifest"
        )
    return len(packages), manifest_path.parent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download one arXiv paper, prepare it through Step 5, and run Paper Cleaner Mini."
    )
    parser.add_argument(
        "--arxiv",
        required=True,
        help="arXiv ID or arxiv.org abstract/PDF URL",
    )
    parser.add_argument("--target-id", default="", help="Process one selected target; default: all mains and hardest.")
    parser.add_argument("--upstream-cleaner-dir", type=Path, default=REPO_ROOT / "paper_cleaner")
    parser.add_argument("--upstream-config", type=Path, default=REPO_ROOT / "paper_cleaner" / "config.yaml")
    parser.add_argument("--input-root", type=Path, default=MINI_DIR / "inputs")
    parser.add_argument("--out", type=Path, default=MINI_DIR / "runs")
    parser.add_argument("--config", type=Path, default=MINI_DIR / "config.yaml")
    parser.add_argument("--model", default="auto", help="Mini author/repair model")
    parser.add_argument("--check-model", default="", help="Mini checker model; default: author model")
    parser.add_argument("--audit-model", default="auto", help="Independent Mini auditor model")
    parser.add_argument("--effort", default="high", choices=["low", "medium", "high"])
    parser.add_argument("--parallel", type=int, default=2)
    parser.add_argument("--max-repairs", type=int, default=2)
    parser.add_argument("--print-plan", action="store_true", help="Print subprocess commands without running them")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        arxiv_id = normalize_arxiv_reference(args.arxiv)
        paper_id = paper_id_for(arxiv_id)
        commands = build_commands(args, arxiv_id, paper_id)
        if args.print_plan:
            for label, cwd, command in commands:
                print(f"# {label} (cwd={cwd})")
                print(shlex.join(command))
            return 0

        first_label, first_cwd, first_command = commands[0]
        _run_checked(first_label, first_cwd, first_command)
        selected = _selected_targets(_paths(args)["inputs"], paper_id)
        if not selected:
            raise MiniRunError("the upstream cleaner selected no main or hard theorem")
        if args.target_id and args.target_id not in selected:
            raise MiniRunError(
                f"target {args.target_id!r} was not selected; available targets: "
                + ", ".join(selected)
            )
        print(f"[mini] selected targets: {', '.join(selected)}", flush=True)

        for label, cwd, command in commands[1:]:
            _run_checked(label, cwd, command)
        count, artifact_dir = _verify_outputs(
            _paths(args)["output"], paper_id, args.target_id
        )
        print(f"[mini] complete: paper={paper_id} audited_packages={count}")
        print(f"[mini] artifacts: {artifact_dir}")
        return 0
    except (MiniRunError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
