"""CLI for the standalone mock verifier pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from verifiers.api_smoke import (
    run_api_a1_smoke,
    run_api_cascade,
    run_api_a_stage_smoke,
    run_api_b_smoke,
    run_api_c_smoke,
    run_api_composer_a_smoke,
)
from verifiers.manual_replay import run_manual_replay
from verifiers.orchestrator import run_mock_pipeline
from verifiers.schemas import VerifierInput


def _default_output_root() -> str:
    repo_root = next(
        (
            parent
            for parent in Path(__file__).resolve().parents
            if (parent / "Prompt Packet").is_dir()
            and (parent / "Outputs").is_dir()
        ),
        Path.cwd(),
    )
    return str(repo_root / "Outputs" / "verifier")


DEFAULT_OUTPUT_ROOT = _default_output_root()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m verifiers",
        description="Run the standalone A1/A2/A3 -> Composer A -> B -> C verifier pipeline.",
    )
    sub = parser.add_subparsers(required=True)

    run = sub.add_parser("run-mock")
    run.add_argument("--scenario", default="clean")
    run.add_argument("--run-id")
    run.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    run.add_argument("--target-theorem", required=True)
    run.add_argument("--allowed-supporting-statements")
    run.add_argument("--allowed-statements")
    run.add_argument("--guidance-list", action="append", default=[])
    run.add_argument("--guidance", default=None)
    run.add_argument("--proof-artifact")
    run.add_argument("--proposed-proof")
    run.add_argument("--skeleton-ref", required=True)
    run.set_defaults(func=cmd_run_mock)

    api_a1 = sub.add_parser("run-api-a1-smoke")
    api_a1.add_argument("--run-id")
    api_a1.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    api_a1.add_argument("--target-theorem", required=True)
    api_a1.add_argument("--allowed-supporting-statements")
    api_a1.add_argument("--allowed-statements")
    api_a1.add_argument("--guidance-list", action="append", default=[])
    api_a1.add_argument("--guidance", default=None)
    api_a1.add_argument("--proof-artifact")
    api_a1.add_argument("--proposed-proof")
    api_a1.add_argument("--skeleton-ref", required=True)
    api_a1.set_defaults(func=cmd_run_api_a1_smoke)

    api_a_stage = sub.add_parser("run-api-a-stage")
    api_a_stage.add_argument("--stage", choices=["A1", "A2", "A3"], required=True)
    api_a_stage.add_argument("--run-id")
    api_a_stage.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    api_a_stage.add_argument("--target-theorem", required=True)
    api_a_stage.add_argument("--allowed-supporting-statements")
    api_a_stage.add_argument("--allowed-statements")
    api_a_stage.add_argument("--guidance-list", action="append", default=[])
    api_a_stage.add_argument("--guidance", default=None)
    api_a_stage.add_argument("--proof-artifact")
    api_a_stage.add_argument("--proposed-proof")
    api_a_stage.add_argument("--skeleton-ref", required=True)
    api_a_stage.set_defaults(func=cmd_run_api_a_stage_smoke)

    api_composer = sub.add_parser("run-api-composer-a")
    api_composer.add_argument("--a1", required=True)
    api_composer.add_argument("--a2", required=True)
    api_composer.add_argument("--a3", required=True)
    api_composer.add_argument("--step-id-map", default="None")
    api_composer.add_argument("--skeleton-ref", required=True)
    api_composer.add_argument("--run-id")
    api_composer.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    api_composer.set_defaults(func=cmd_run_api_composer_a_smoke)

    api_b = sub.add_parser("run-api-b")
    _add_proof_input_args(api_b)
    api_b.add_argument("--derived-a-status", required=True, choices=["A_VERIFIED", "A_ALMOST", "A_NOT_VERIFIED", "A_INVALID", "A_UNCLEAR"])
    api_b.set_defaults(func=cmd_run_api_b_smoke)

    api_c = sub.add_parser("run-api-c")
    _add_proof_input_args(api_c)
    api_c.add_argument("--derived-a-status", required=True, choices=["A_VERIFIED", "A_ALMOST", "A_NOT_VERIFIED", "A_INVALID", "A_UNCLEAR"])
    api_c.set_defaults(func=cmd_run_api_c_smoke)

    api_cascade = sub.add_parser("run-api-cascade")
    _add_proof_input_args(api_cascade)
    api_cascade.add_argument("--step-id-map", default="None")
    api_cascade.set_defaults(func=cmd_run_api_cascade)

    manual = sub.add_parser("parse-manual-run")
    manual.add_argument("--a1", required=True)
    manual.add_argument("--a2", required=True)
    manual.add_argument("--a3", required=True)
    manual.add_argument("--composer-a", required=True)
    manual.add_argument("--verifier-b", required=True)
    manual.add_argument("--verifier-c", required=True)
    manual.add_argument("--skeleton-ref", required=True)
    manual.add_argument("--run-id")
    manual.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    manual.set_defaults(func=cmd_parse_manual_run)

    args = parser.parse_args(argv)
    return args.func(args)


def cmd_run_mock(args: argparse.Namespace) -> int:
    inputs = _input_from_args(args)
    summary = run_mock_pipeline(inputs, output_root=args.output_root, scenario=args.scenario, run_id=args.run_id)
    print(json.dumps(summary.to_dict(), indent=2, sort_keys=True))
    return 0


def cmd_run_api_a1_smoke(args: argparse.Namespace) -> int:
    inputs = _input_from_args(args)
    summary = run_api_a1_smoke(inputs, output_root=args.output_root, run_id=args.run_id)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def cmd_run_api_a_stage_smoke(args: argparse.Namespace) -> int:
    inputs = _input_from_args(args)
    summary = run_api_a_stage_smoke(
        inputs,
        stage=args.stage,
        output_root=args.output_root,
        run_id=args.run_id,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def cmd_run_api_composer_a_smoke(args: argparse.Namespace) -> int:
    a_reports = {
        "A1": Path(args.a1).read_text(encoding="utf-8"),
        "A2": Path(args.a2).read_text(encoding="utf-8"),
        "A3": Path(args.a3).read_text(encoding="utf-8"),
    }
    summary = run_api_composer_a_smoke(
        a_reports=a_reports,
        skeleton_ref=args.skeleton_ref,
        step_id_map=_read_arg(args.step_id_map),
        output_root=args.output_root,
        run_id=args.run_id,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def cmd_run_api_b_smoke(args: argparse.Namespace) -> int:
    inputs = _input_from_args(args)
    summary = run_api_b_smoke(
        inputs,
        derived_a_status=args.derived_a_status,
        output_root=args.output_root,
        run_id=args.run_id,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def cmd_run_api_c_smoke(args: argparse.Namespace) -> int:
    inputs = _input_from_args(args)
    summary = run_api_c_smoke(
        inputs,
        derived_a_status=args.derived_a_status,
        output_root=args.output_root,
        run_id=args.run_id,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def cmd_run_api_cascade(args: argparse.Namespace) -> int:
    inputs = _input_from_args(args)
    summary = run_api_cascade(
        inputs,
        output_root=args.output_root,
        run_id=args.run_id,
        step_id_map=_read_arg(args.step_id_map),
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def cmd_parse_manual_run(args: argparse.Namespace) -> int:
    summary = run_manual_replay(
        a1_path=args.a1,
        a2_path=args.a2,
        a3_path=args.a3,
        composer_a_path=args.composer_a,
        verifier_b_path=args.verifier_b,
        verifier_c_path=args.verifier_c,
        skeleton_ref=args.skeleton_ref,
        output_root=args.output_root,
        run_id=args.run_id,
    )
    print(json.dumps(summary.to_dict(), indent=2, sort_keys=True))
    return 0


def _input_from_args(args: argparse.Namespace) -> VerifierInput:
    return VerifierInput(
        target_theorem=_read_arg(args.target_theorem),
        allowed_supporting_statements=_read_arg(args.allowed_supporting_statements or args.allowed_statements or ""),
        guidance_list=[_read_arg(item) for item in args.guidance_list] if args.guidance_list else None,
        guidance=_read_arg(args.guidance) if args.guidance is not None else None,
        proof_artifact=_read_arg(args.proof_artifact) if args.proof_artifact else None,
        proposed_proof=_read_arg(args.proposed_proof) if args.proposed_proof else None,
        skeleton_ref=args.skeleton_ref,
    )


def _add_proof_input_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--run-id")
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--target-theorem", required=True)
    parser.add_argument("--allowed-supporting-statements")
    parser.add_argument("--allowed-statements")
    parser.add_argument("--guidance-list", action="append", default=[])
    parser.add_argument("--guidance", default=None)
    parser.add_argument("--proof-artifact")
    parser.add_argument("--proposed-proof")
    parser.add_argument("--skeleton-ref", required=True)


def _read_arg(value: str) -> str:
    if value.startswith("@"):
        return Path(value[1:]).read_text(encoding="utf-8")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
