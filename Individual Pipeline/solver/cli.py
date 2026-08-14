"""Command line interface for the standalone S0-S6 solver distribution."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from .agent_calls import INTERNET_ENABLED_ROLES, AgentCaller
from .cleaner_bridge import (
    export_solver_bundle,
    load_cleaner_package,
    packet_internet_mode,
    reuse_prepared_solver_bundle,
    sha256_text,
)
from citation.constants import CITATION_INTERNET_ENABLED_ROLES
from citation.prompts import CitationPromptTemplates
from .config import (
    DEFAULT_API_KEY_FILE,
    extract_api_key_from_text,
    optional_int_env,
    optional_set_env,
    ordered_api_key_env_names,
)
from .controller import ControllerConfig
from .io_utils import write_json
from .llm import MockLLMClient, OpenAICompatibleClient, WEB_SEARCH_FORBIDDEN_ROLES
from .mock import ScriptedMockClient
from .orchestrator import OpenProblemOrchestrator, OpenRunConfig, ProblemInputs
from .prompt_loader import DEFAULT_PACKET_PATH, PacketPrompts
from .run_store import OpenRunStore
from .skeleton_source_gate import (
    INTERNET_ROLES,
    MockSkeletonSourceClient,
    SkeletonSourcePromptTemplates,
    run_skeleton_source_gate,
)


CLASSIFICATION_TAGS = (
    "paper_original_result",
    "cited_prior_result",
    "protocol_validation",
)

# These gold-blind or privileged roles must never receive a browsing tool,
# even when a process-wide environment override is present.
def main(argv: list[str] | None = None) -> int:
    """Run one of the standalone solver commands."""

    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="integrated-math-solver",
        description="Run the S0-S6 mathematical solver with or without solver web search.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    _add_open_problem_parser(subparsers)
    _add_prepare_parser(subparsers)
    _add_integrated_parser(subparsers)
    return parser


def _add_open_problem_parser(subparsers) -> None:
    command = subparsers.add_parser(
        "run-open-problem",
        help="Run the S0-S6 solver and deterministic Decision Controller.",
    )
    command.add_argument("--problem-dir", required=True)
    command.add_argument("--run-dir", default="open_runs")
    command.add_argument(
        "--packet-file",
        default=str(DEFAULT_PACKET_PATH),
    )
    command.add_argument("--client", default="api", choices=["mock", "api", "openai"])
    command.add_argument("--mock-scenario", default="solved_round1")
    command.add_argument("--model")
    command.add_argument("--s0-model")
    for index in range(1, 6):
        command.add_argument(f"--s{index}-model")
    command.add_argument("--s6-model")
    command.add_argument("--citation-model")
    command.add_argument("--key-solver-model")
    command.add_argument("--key-solver-id", choices=["S1", "S2", "S3", "S4", "S5"])
    command.add_argument("--verifier-model")
    command.add_argument("--verifier-a-model")
    command.add_argument("--composer-a-model")
    command.add_argument("--verifier-b-model")
    command.add_argument("--verifier-c-model")
    command.add_argument("--checker-model")
    command.add_argument("--api-base-url")
    command.add_argument("--api-surface", choices=["auto", "chat", "responses"])
    command.add_argument("--api-key")
    command.add_argument("--api-key-env", default="OPENAI_API_KEY")
    command.add_argument("--api-key-file")
    command.add_argument("--reasoning-effort")
    command.add_argument("--s0-reasoning-effort")
    command.add_argument("--key-solver-reasoning-effort")
    command.add_argument("--s6-reasoning-effort")
    command.add_argument("--citation-reasoning-effort")
    command.add_argument("--verifier-a-reasoning-effort")
    command.add_argument("--composer-a-reasoning-effort")
    command.add_argument("--verifier-b-reasoning-effort")
    command.add_argument("--verifier-c-reasoning-effort")
    command.add_argument("--checker-reasoning-effort")
    command.add_argument("--temperature", type=float, default=0.0)
    command.add_argument("--input-price", type=float)
    command.add_argument("--output-price", type=float)
    command.add_argument("--max-rounds", type=int, default=12)
    command.add_argument("--citation-max-attempts", type=int, default=2)
    command.add_argument(
        "--citation-web-search-context-size",
        choices=["low", "medium", "high"],
        default="medium",
    )
    command.add_argument(
        "--mock-citation-scenario",
        default="all_supported",
        choices=[
            "all_supported",
            "target_source_leakage",
            "source_ledger_repair_needed",
            "blocking_source_issue",
            "malformed_summary_routes_unclear",
        ],
    )
    command.add_argument("--solver-workers", type=int, default=5)
    command.add_argument("--solver-delay-seconds", type=float, default=0.0)
    command.add_argument("--pre-round-delay-seconds", type=float, default=0.0)
    command.add_argument("--retry-max-attempts", type=int, default=8)
    command.add_argument("--max-guidance", type=int, default=10)
    command.add_argument("--max-branch-depth", type=int, default=1)
    command.add_argument("--max-branches", type=int, default=3)
    command.add_argument("--max-no-guidance-rounds", type=int, default=1)
    command.add_argument("--no-verifiers", action="store_true")
    command.add_argument("--web-search", action="store_true")
    command.add_argument("--resume", action="store_true")
    command.add_argument("--progress", action="store_true")
    command.set_defaults(func=cmd_run_open_problem)


def _add_prepare_parser(subparsers) -> None:
    command = subparsers.add_parser(
        "prepare-cleaner-problem",
        help="Source-audit and export one Paper Cleaner Mini package.",
    )
    command.add_argument("--cleaner-runs-dir", required=True)
    command.add_argument("--paper-id", required=True)
    command.add_argument("--target-id", required=True)
    command.add_argument("--packet-file", required=True)
    command.add_argument("--output-dir", required=True)
    command.add_argument("--run-tag", required=True, choices=CLASSIFICATION_TAGS)
    command.add_argument("--source-audit-model")
    command.add_argument(
        "--source-web-search-context-size",
        choices=["low", "medium", "high"],
        default="medium",
    )
    command.add_argument("--include-private-final-checker", action="store_true")
    _add_common_client_arguments(command, api_surface="responses", reasoning_effort="high")
    command.add_argument("--mock-source-scenario", default="all_supported")
    command.add_argument("--progress", action="store_true")
    command.set_defaults(func=cmd_prepare_cleaner_problem)


def _add_integrated_parser(subparsers) -> None:
    command = subparsers.add_parser(
        "run-cleaner-solver",
        help="Run Paper Cleaner Mini, hard gates, export, and then S0-S6.",
    )
    command.add_argument(
        "--cleaner-dir",
        default=str(Path(__file__).resolve().parent.parent / "paper_cleaner_mini"),
    )
    command.add_argument("--cleaner-input-root", required=True)
    command.add_argument("--cleaner-work-root", required=True)
    command.add_argument("--prepared-dir", required=True)
    command.add_argument("--solver-run-dir", required=True)
    command.add_argument("--paper-id", required=True)
    command.add_argument("--target-id", required=True)
    command.add_argument("--packet-file", required=True)
    command.add_argument("--run-tag", required=True, choices=CLASSIFICATION_TAGS)
    command.add_argument("--cleaner-model", default="auto")
    command.add_argument("--cleaner-check-model", default="")
    command.add_argument("--cleaner-audit-model", default="auto")
    command.add_argument("--source-audit-model")
    command.add_argument("--cleaner-effort", default="high", choices=["low", "medium", "high"])
    command.add_argument("--cleaner-parallel", type=int, default=2)
    command.add_argument("--cleaner-max-repairs", type=int, default=2)
    command.add_argument(
        "--source-web-search-context-size",
        choices=["low", "medium", "high"],
        default="medium",
    )
    command.add_argument("--include-private-final-checker", action="store_true")
    _add_common_client_arguments(command, reasoning_effort="high")
    command.add_argument("--mock-source-scenario", default="all_supported")
    command.add_argument("--progress", action="store_true")
    command.add_argument("solver_args", nargs=argparse.REMAINDER)
    command.set_defaults(func=cmd_run_cleaner_solver)


def _add_common_client_arguments(
    parser: argparse.ArgumentParser,
    *,
    api_surface: str | None = None,
    reasoning_effort: str | None = None,
) -> None:
    parser.add_argument("--client", default="openai", choices=["mock", "api", "openai"])
    parser.add_argument("--api-base-url")
    parser.add_argument("--api-surface", default=api_surface, choices=["auto", "chat", "responses"])
    parser.add_argument("--api-key")
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY")
    parser.add_argument("--api-key-file")
    parser.add_argument("--reasoning-effort", default=reasoning_effort)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--retry-max-attempts", type=int, default=8)


def cmd_run_open_problem(args: argparse.Namespace) -> int:
    """Run the S0-S6 pipeline to a terminal state."""

    packet_mode = packet_internet_mode(args.packet_file)
    if packet_mode == "none" and args.web_search:
        raise RuntimeError("Prompts.md forbids solver web search; remove --web-search")
    if packet_mode == "source_supported" and not args.web_search:
        raise RuntimeError(
            "the selected packet requires source-supported solver web search; add --web-search"
        )

    problem = ProblemInputs.load(args.problem_dir)
    prompts = PacketPrompts.from_file(args.packet_file)
    citation_prompts = CitationPromptTemplates.from_file(args.packet_file)
    store = OpenRunStore(Path(args.run_dir) / problem.problem_id)
    if store.state_path.exists() and not args.resume:
        raise RuntimeError(
            f"run state already exists at {store.state_path}; pass --resume "
            "to continue or use a fresh --run-dir"
        )

    if args.client == "mock":
        shared = ScriptedMockClient(scenario=args.mock_scenario)
        solver_client = citation_client = verifier_client = checker_client = shared
        s0_client = s6_client = key_solver_client = None
        verifier_a_client = composer_a_client = verifier_b_client = verifier_c_client = None
        subproblem_clients = {}
    else:
        solver_web_roles = INTERNET_ENABLED_ROLES if args.web_search else frozenset()
        solver_client = _make_client(
            args,
            model=args.model,
            temperature=args.temperature,
            web_search_roles=solver_web_roles,
        )
        citation_args = argparse.Namespace(**vars(args))
        citation_args.api_surface = "responses"
        citation_client = _make_client(
            citation_args,
            model=args.citation_model or args.verifier_model or args.model,
            temperature=args.temperature,
            reasoning_effort=(
                args.citation_reasoning_effort
                if args.citation_reasoning_effort is not None
                else _USE_ARGS_REASONING
            ),
            web_search_roles=CITATION_INTERNET_ENABLED_ROLES,
            web_search_context_size=args.citation_web_search_context_size,
        )
        s0_client = _optional_role_client(
            args,
            model=args.s0_model,
            effort=args.s0_reasoning_effort,
            web_search_roles=solver_web_roles,
        )
        s6_client = _optional_role_client(
            args,
            model=args.s6_model,
            effort=args.s6_reasoning_effort,
            web_search_roles=solver_web_roles,
        )
        key_solver_client = _optional_role_client(
            args,
            model=args.key_solver_model,
            effort=args.key_solver_reasoning_effort,
            web_search_roles=solver_web_roles,
        )
        subproblem_clients = {
            s_id: _make_client(
                args,
                model=getattr(args, f"{s_id.lower()}_model"),
                temperature=args.temperature,
                web_search_roles=solver_web_roles,
            )
            for s_id in ("S1", "S2", "S3", "S4", "S5")
            if getattr(args, f"{s_id.lower()}_model")
        }
        verifier_client = (
            _make_client(args, model=args.verifier_model, temperature=args.temperature)
            if args.verifier_model
            else None
        )
        verifier_a_client = _optional_role_client(
            args,
            model=args.verifier_a_model or args.verifier_model,
            effort=args.verifier_a_reasoning_effort,
        )
        composer_a_client = _optional_role_client(
            args,
            model=args.composer_a_model or args.verifier_model,
            effort=args.composer_a_reasoning_effort,
        )
        verifier_b_client = _optional_role_client(
            args,
            model=args.verifier_b_model or args.verifier_model,
            effort=args.verifier_b_reasoning_effort,
        )
        verifier_c_client = _optional_role_client(
            args,
            model=args.verifier_c_model or args.verifier_model,
            effort=args.verifier_c_reasoning_effort,
        )
        checker_client = _optional_role_client(
            args,
            model=args.checker_model,
            effort=args.checker_reasoning_effort,
        )

    caller = AgentCaller(
        prompts=prompts,
        solver_client=solver_client,
        s0_client=s0_client,
        subproblem_clients=subproblem_clients,
        key_solver_client=key_solver_client,
        s6_client=s6_client,
        citation_client=citation_client,
        citation_prompts=citation_prompts,
        verifier_client=verifier_client,
        verifier_a_client=verifier_a_client,
        composer_a_client=composer_a_client,
        verifier_b_client=verifier_b_client,
        verifier_c_client=verifier_c_client,
        checker_client=checker_client,
        progress=_print_progress if args.progress else None,
        base_metadata={
            "pipeline": "main",
            "depth": 0,
            "citation_scenario": args.mock_citation_scenario,
        },
    )
    write_json(
        store.root / "run_config.json",
        _run_config_snapshot(
            args,
            solver_client=solver_client,
            s0_client=s0_client,
            subproblem_clients=subproblem_clients,
            key_solver_client=key_solver_client,
            s6_client=s6_client,
            citation_client=citation_client,
            verifier_client=verifier_client,
            verifier_a_client=verifier_a_client,
            composer_a_client=composer_a_client,
            verifier_b_client=verifier_b_client,
            verifier_c_client=verifier_c_client,
            checker_client=checker_client,
        ),
    )
    orchestrator = OpenProblemOrchestrator(
        problem=problem,
        caller=caller,
        store=store,
        config=OpenRunConfig(
            max_rounds=args.max_rounds,
            run_verifiers=not args.no_verifiers,
            solver_workers=args.solver_workers,
            solver_delay_seconds=args.solver_delay_seconds,
            pre_round_delay_seconds=args.pre_round_delay_seconds,
            citation_max_attempts=args.citation_max_attempts,
            key_solver_id=args.key_solver_id,
        ),
        controller_config=ControllerConfig(
            max_guidance=args.max_guidance,
            max_branch_depth=args.max_branch_depth,
            max_total_branches=args.max_branches,
            max_no_guidance_rounds=args.max_no_guidance_rounds,
        ),
        progress=_print_progress if args.progress else None,
    )
    state = orchestrator.run()
    print(f"status: {state.status}")
    print(f"rounds: {state.round_index}")
    print(f"guidance items: {len(state.guidance)}")
    for index, item in enumerate(state.guidance, start=1):
        print(f"  {index}. {item}")
    if state.final_proof_round is not None:
        proof_path = str(store.round_dir(state.final_proof_round) / "S6.md")
        if proof_path.startswith("\\\\?\\"):
            proof_path = proof_path[4:]
        print(f"final proof: {proof_path}")
    if state.stop_reason:
        print(f"stop reason: {state.stop_reason}")
    return 0


def _optional_role_client(
    args: argparse.Namespace,
    *,
    model: str | None,
    effort: str | None,
    web_search_roles=frozenset(),
):
    if not model and not effort:
        return None
    return _make_client(
        args,
        model=model,
        temperature=args.temperature,
        reasoning_effort=effort,
        web_search_roles=web_search_roles,
    )


def cmd_prepare_cleaner_problem(args: argparse.Namespace) -> int:
    solver_input = _prepare_cleaner_problem(
        args,
        cleaner_runs_dir=Path(args.cleaner_runs_dir),
        output_dir=Path(args.output_dir),
    )
    print(f"solver input: {solver_input}")
    return 0


def _prepare_cleaner_problem(
    args: argparse.Namespace,
    *,
    cleaner_runs_dir: Path,
    output_dir: Path,
) -> Path:
    packet_internet_mode(args.packet_file, required=True)
    package = load_cleaner_package(cleaner_runs_dir, args.paper_id, args.target_id)
    source_model = (
        MockSkeletonSourceClient.model
        if args.client == "mock"
        else args.source_audit_model or package.audit_model or "gpt-5.5"
    )
    existing = reuse_prepared_solver_bundle(
        package=package,
        output_dir=output_dir,
        packet_path=args.packet_file,
        classification_tag=args.run_tag,
        source_audit_model=source_model,
        include_private_final_checker=args.include_private_final_checker,
    )
    if existing is not None:
        return existing

    templates = SkeletonSourcePromptTemplates.from_file(args.packet_file)
    if args.client == "mock":
        source_client = MockSkeletonSourceClient(args.mock_source_scenario)
    else:
        source_args = argparse.Namespace(**vars(args))
        source_args.api_surface = "responses"
        source_client = _make_client(
            source_args,
            model=source_model,
            temperature=args.temperature,
            reasoning_effort=args.reasoning_effort,
            web_search_roles=INTERNET_ROLES,
            require_web_search_roles=INTERNET_ROLES,
            web_search_context_size=args.source_web_search_context_size,
            max_attempts=args.retry_max_attempts,
        )
    source_gate_dir = cleaner_runs_dir / args.paper_id / "source_gate" / args.target_id
    decision = run_skeleton_source_gate(
        output_dir=source_gate_dir,
        target=package.sections.target,
        section3=package.sections.section3,
        bibliography=package.bibliography,
        templates=templates,
        client=source_client,
        progress=_print_progress if args.progress else None,
    )
    if decision.gate_result not in {"GOOD_TO_GO", "NOT_APPLICABLE"}:
        raise RuntimeError(
            f"skeleton source gate stopped with {decision.gate_result}; "
            f"artifacts: {source_gate_dir}"
        )
    return export_solver_bundle(
        package=package,
        output_dir=output_dir,
        packet_path=args.packet_file,
        classification_tag=args.run_tag,
        source_gate_decision=decision,
        source_gate_dir=source_gate_dir,
        source_audit_model=source_model,
        include_private_final_checker=args.include_private_final_checker,
    )


def cmd_run_cleaner_solver(args: argparse.Namespace) -> int:
    """Run one cleaner target through hard gates and then S0-S6."""

    cleaner_dir = Path(args.cleaner_dir).resolve()
    input_root = Path(args.cleaner_input_root).resolve()
    work_root = Path(args.cleaner_work_root).resolve()
    prepared_dir = Path(args.prepared_dir).resolve()
    packet_file = Path(args.packet_file).resolve()
    if not (cleaner_dir / "stage2.py").exists() or not (cleaner_dir / "audit.py").exists():
        raise RuntimeError(f"invalid Paper Cleaner Mini directory: {cleaner_dir}")
    if args.include_private_final_checker:
        _preflight_private_final_checker(input_root, args.paper_id, args.target_id)

    cleaner_env = os.environ.copy()
    resolved_key = _resolve_api_key(args)
    if resolved_key:
        cleaner_env["OPENAI_API_KEY"] = resolved_key
    stage2_cmd = [
        sys.executable,
        str(cleaner_dir / "stage2.py"),
        "--papers", args.paper_id,
        "--target-id", args.target_id,
        "--src-runs", str(input_root),
        "--out", str(work_root),
        "--config", str(cleaner_dir / "config.yaml"),
        "--model", args.cleaner_model,
        "--effort", args.cleaner_effort,
        "--parallel", str(args.cleaner_parallel),
        "--max-repairs", str(args.cleaner_max_repairs),
    ]
    if args.cleaner_check_model:
        stage2_cmd.extend(["--check-model", args.cleaner_check_model])
    _run_checked(stage2_cmd, cleaner_dir, env=cleaner_env)

    audit_cmd = [
        sys.executable,
        str(cleaner_dir / "audit.py"),
        "--papers", args.paper_id,
        "--target-id", args.target_id,
        "--runs-dir", str(work_root),
        "--config", str(cleaner_dir / "config.yaml"),
        "--model", args.cleaner_audit_model,
        "--effort", args.cleaner_effort,
        "--parallel", str(args.cleaner_parallel),
        "--fail-on-package-issues",
    ]
    _run_checked(audit_cmd, cleaner_dir, env=cleaner_env)

    solver_input = _prepare_cleaner_problem(
        args,
        cleaner_runs_dir=work_root,
        output_dir=prepared_dir,
    )
    mode = packet_internet_mode(packet_file, required=True)
    forwarded = list(args.solver_args)
    if forwarded and forwarded[0] == "--":
        forwarded = forwarded[1:]
    _reject_forwarded_solver_overrides(forwarded)
    solver_argv = [
        "run-open-problem",
        "--problem-dir", str(solver_input),
        "--run-dir", str(Path(args.solver_run_dir).resolve()),
        "--packet-file", str(packet_file),
        "--client", args.client,
        "--reasoning-effort", args.reasoning_effort,
        "--retry-max-attempts", str(args.retry_max_attempts),
    ]
    if args.api_base_url:
        solver_argv.extend(["--api-base-url", args.api_base_url])
    if args.api_key:
        solver_argv.extend(["--api-key", args.api_key])
    if args.api_key_env:
        solver_argv.extend(["--api-key-env", args.api_key_env])
    if args.api_key_file:
        solver_argv.extend(["--api-key-file", args.api_key_file])
    if mode == "source_supported":
        solver_argv.extend(["--api-surface", "responses", "--web-search"])
    if args.progress:
        solver_argv.append("--progress")
    solver_argv.extend(forwarded)
    result = main(solver_argv)
    if result != 0:
        raise RuntimeError(f"run-open-problem failed with exit code {result}")
    return 0


def _run_checked(command: list[str], cwd: Path, *, env: dict[str, str] | None = None) -> None:
    completed = subprocess.run(command, cwd=cwd, env=env, check=False)
    if completed.returncode != 0:
        raise RuntimeError(
            f"pipeline stage failed with exit code {completed.returncode}: {command[1]}"
        )


def _preflight_private_final_checker(
    input_root: Path, paper_id: str, target_id: str
) -> None:
    """Fail before paid cleaner stages when requested gold material is absent."""

    index_path = input_root / paper_id / "index" / "statements.v2.json"
    if not index_path.is_file():
        raise RuntimeError(
            "private Final Checker requested but the prepared statement index "
            f"does not exist: {index_path}"
        )
    index = json.loads(index_path.read_text(encoding="utf-8"))
    targets = [
        item for item in index.get("statements", []) if item.get("id") == target_id
    ]
    if len(targets) != 1:
        raise RuntimeError(
            f"private Final Checker requested but target {target_id!r} is missing or "
            "duplicated in the prepared statement index"
        )
    if not str(targets[0].get("proof_tex") or "").strip():
        raise RuntimeError(
            "private Final Checker requested but the selected target has no "
            "extractable proof; set INCLUDE_PRIVATE_FINAL_CHECKER=0 to run the "
            "public cascade without gold material"
        )
    target = targets[0]
    meta_path = input_root / paper_id / "source" / "meta.json"
    if not meta_path.is_file():
        raise RuntimeError("prepared paper metadata is missing; target source cannot be verified")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    source_name = "flat.md" if meta.get("source_type") == "ocr" else "flat.tex"
    source_path = input_root / paper_id / "source" / source_name
    if not source_path.is_file():
        raise RuntimeError("prepared paper source is missing; target source cannot be verified")
    source = source_path.read_text(encoding="utf-8")
    statement = str(target.get("statement_tex") or "")
    start, end = target.get("source_start", -1), target.get("source_end", -1)
    source_ok = (target.get("added_by") == "parser"
                 and target.get("source_verified") is True
                 and target.get("source_file") == f"source/{source_name}"
                 and isinstance(start, int) and isinstance(end, int)
                 and 0 <= start < end <= len(source)
                 and bool(statement)
                 and sha256_text(statement) == target.get("statement_sha256")
                 and sha256_text(source[start:end]) == target.get("source_sha256")
                 and statement in source[start:end])
    if not source_ok:
        raise RuntimeError(
            "private Final Checker requested but the selected target is not "
            "backed by a valid source span and hashes"
        )
    proof = str(target.get("proof_tex") or "")
    proof_start = target.get("proof_source_start", -1)
    proof_end = target.get("proof_source_end", -1)
    proof_ok = (
        target.get("proof_source_verified") is True
        and target.get("proof_pairing") in {
            "explicit-label", "explicit-heading-label", "adjacent",
            "explicit-label-recovery",
        }
        and target.get("proof_source_file") == f"source/{source_name}"
        and isinstance(proof_start, int)
        and isinstance(proof_end, int)
        and 0 <= proof_start < proof_end <= len(source)
        and bool(proof)
        and sha256_text(proof) == target.get("proof_sha256")
        and sha256_text(source[proof_start:proof_end])
            == target.get("proof_source_sha256")
        and proof in source[proof_start:proof_end]
    )
    if not proof_ok:
        raise RuntimeError(
            "private Final Checker requested but the reference proof is not "
            "backed by a valid source span, hashes, and deterministic pairing"
        )


def _reject_forwarded_solver_overrides(arguments: list[str]) -> None:
    reserved = {
        "--problem-dir",
        "--run-dir",
        "--packet-file",
        "--client",
        "--web-search",
        "--api-surface",
        "--api-base-url",
        "--api-key",
        "--api-key-env",
        "--api-key-file",
    }
    for argument in arguments:
        name = argument.split("=", 1)[0]
        if name in reserved:
            raise RuntimeError(
                f"{name} is controlled by run-cleaner-solver and cannot be forwarded"
            )


_USE_ARGS_REASONING = object()


def _make_client(
    args: argparse.Namespace,
    *,
    model: str | None = None,
    temperature: float = 0.0,
    reasoning_effort=_USE_ARGS_REASONING,
    web_search_roles=frozenset(),
    require_web_search_roles=frozenset(),
    web_search_context_size: str | None = None,
    max_attempts: int | None = None,
):
    selected_model = model if model is not None else getattr(args, "model", None)
    if args.client == "mock":
        return MockLLMClient(model=selected_model or "mock-mvp-model")
    if reasoning_effort is _USE_ARGS_REASONING:
        selected_reasoning_effort = (
            getattr(args, "reasoning_effort", None)
            or os.environ.get("DEEPSEEK_REASONING_EFFORT")
            or os.environ.get("OPENAI_REASONING_EFFORT")
            or None
        )
    else:
        selected_reasoning_effort = reasoning_effort
    selected_max_attempts = (
        max_attempts
        if max_attempts is not None
        else getattr(args, "retry_max_attempts", None)
    )
    effective_web_search_roles = set(web_search_roles) | optional_set_env(
        "OPENAI_WEB_SEARCH_ROLES"
    )
    effective_required_web_search_roles = set(
        require_web_search_roles
    ) | optional_set_env("OPENAI_REQUIRE_WEB_SEARCH_ROLES")
    forbidden = WEB_SEARCH_FORBIDDEN_ROLES & (
        effective_web_search_roles | effective_required_web_search_roles
    )
    if forbidden:
        names = ", ".join(sorted(forbidden))
        raise RuntimeError(
            "web search is forbidden for verifier/checker roles; remove these roles "
            f"from OPENAI_WEB_SEARCH_ROLES/OPENAI_REQUIRE_WEB_SEARCH_ROLES: {names}"
        )

    kwargs: dict = {
        "model": selected_model or os.environ.get("OPENAI_MODEL", "gpt-4.1"),
        "base_url": args.api_base_url
        or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "api_key": _resolve_api_key(args),
        "temperature": temperature,
        "max_tokens": optional_int_env("OPENAI_MAX_TOKENS"),
        "api_surface": getattr(args, "api_surface", None)
        or os.environ.get("OPENAI_API_SURFACE", "auto"),
        "thinking": os.environ.get("DEEPSEEK_THINKING") or None,
        "reasoning_effort": selected_reasoning_effort,
        "json_response_roles": optional_set_env("OPENAI_JSON_RESPONSE_ROLES"),
        "web_search_roles": effective_web_search_roles,
        "require_web_search_roles": effective_required_web_search_roles,
        "web_search_context_size": web_search_context_size
        or os.environ.get("OPENAI_WEB_SEARCH_CONTEXT_SIZE")
        or None,
        "input_price_per_1m": getattr(args, "input_price", None),
        "output_price_per_1m": getattr(args, "output_price", None),
    }
    if selected_max_attempts is not None:
        kwargs["max_attempts"] = selected_max_attempts
    return OpenAICompatibleClient(**kwargs)


def _resolve_api_key(args: argparse.Namespace) -> str | None:
    explicit_key = getattr(args, "api_key", None)
    if explicit_key:
        return explicit_key.strip()
    for env_name in ordered_api_key_env_names(getattr(args, "api_key_env", None)):
        value = os.environ.get(env_name)
        if value:
            return value.strip()
    explicit_key_file = getattr(args, "api_key_file", None)
    if explicit_key_file:
        key_file = Path(explicit_key_file)
        if not key_file.exists():
            raise RuntimeError(f"API key file does not exist: {key_file}")
    else:
        key_file = DEFAULT_API_KEY_FILE if DEFAULT_API_KEY_FILE.exists() else None
    if key_file is None:
        return None
    token = extract_api_key_from_text(key_file.read_text(encoding="utf-8").strip())
    if token is not None:
        return token
    raise RuntimeError(f"API key file does not contain a recognizable key: {key_file}")


def _run_config_snapshot(args: argparse.Namespace, **clients) -> dict:
    solver_client = clients["solver_client"]
    subproblem_clients = clients["subproblem_clients"]

    def model_for(*names: str) -> str:
        for name in names:
            client = clients.get(name)
            if client is not None:
                return client.model
        return solver_client.model

    all_clients = [solver_client]
    all_clients.extend(client for client in clients.values() if hasattr(client, "model"))
    all_clients.extend(subproblem_clients.values())
    effective_web_roles = sorted(
        {
            role
            for client in all_clients
            for role in getattr(client, "web_search_roles", set())
        }
    )
    effective_required_web_roles = sorted(
        {
            role
            for client in all_clients
            for role in getattr(client, "require_web_search_roles", set())
        }
    )

    return {
        "problem_dir": args.problem_dir,
        "run_dir": args.run_dir,
        "packet_file": args.packet_file,
        "packet_mode": packet_internet_mode(args.packet_file),
        "client": args.client,
        "api_base_url": args.api_base_url
        or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "api_surface": args.api_surface
        or os.environ.get("OPENAI_API_SURFACE", "auto"),
        "web_search": bool(args.web_search),
        "effective_web_search_roles": effective_web_roles,
        "effective_required_web_search_roles": effective_required_web_roles,
        "citation_web_search": True,
        "citation_web_search_context_size": args.citation_web_search_context_size,
        "role_models": {
            "s0": model_for("s0_client"),
            **{
                s_id.lower(): subproblem_clients.get(s_id, solver_client).model
                for s_id in ("S1", "S2", "S3", "S4", "S5")
            },
            "key_solver": clients["key_solver_client"].model
            if clients["key_solver_client"]
            else None,
            "s6": model_for("s6_client"),
            "citation_generator": model_for("citation_client"),
            "citation_verifier": model_for("citation_client"),
            "problem_statement_verifier": model_for("verifier_client"),
            "verifier_a": model_for("verifier_a_client", "verifier_client"),
            "composer_a": model_for("composer_a_client", "verifier_client"),
            "verifier_b": model_for("verifier_b_client", "verifier_client"),
            "verifier_c": model_for("verifier_c_client", "verifier_client"),
            "final_checker": model_for("checker_client"),
        },
        "requested_models": {
            "default": args.model,
            "s0": args.s0_model,
            **{f"s{index}": getattr(args, f"s{index}_model") for index in range(1, 6)},
            "key_solver": args.key_solver_model,
            "s6": args.s6_model,
            "citation": args.citation_model,
            "verifier": args.verifier_model,
            "verifier_a": args.verifier_a_model,
            "composer_a": args.composer_a_model,
            "verifier_b": args.verifier_b_model,
            "verifier_c": args.verifier_c_model,
            "checker": args.checker_model,
        },
        "reasoning_efforts": {
            "default": args.reasoning_effort,
            "s0": args.s0_reasoning_effort,
            "key_solver": args.key_solver_reasoning_effort,
            "s6": args.s6_reasoning_effort,
            "citation": args.citation_reasoning_effort,
            "verifier_a": args.verifier_a_reasoning_effort,
            "composer_a": args.composer_a_reasoning_effort,
            "verifier_b": args.verifier_b_reasoning_effort,
            "verifier_c": args.verifier_c_reasoning_effort,
            "checker": args.checker_reasoning_effort,
        },
        "loop": {
            "max_rounds": args.max_rounds,
            "max_guidance": args.max_guidance,
            "max_branch_depth": args.max_branch_depth,
            "max_branches": args.max_branches,
            "max_no_guidance_rounds": args.max_no_guidance_rounds,
            "solver_workers": args.solver_workers,
            "solver_delay_seconds": args.solver_delay_seconds,
            "pre_round_delay_seconds": args.pre_round_delay_seconds,
            "citation_max_attempts": args.citation_max_attempts,
            "run_verifiers": not args.no_verifiers,
            "key_solver_id": args.key_solver_id,
            "retry_max_attempts": args.retry_max_attempts,
        },
    }


def _print_progress(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
