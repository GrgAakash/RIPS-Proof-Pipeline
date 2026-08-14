"""CLI for the standalone Citation Generator/Verifier gate."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .clients import MockLLMClient, OpenAICompatibleClient
from .constants import DEFAULT_ALLOWED_SUPPORTING_STATEMENTS
from .gate import run_citation_gate
from .prompts import DEFAULT_PACKET_PATH, CitationPromptTemplates


def main(argv: list[str] | None = None) -> int:
    """Run the standalone citation gate CLI."""

    parser = argparse.ArgumentParser(prog="standalone-citation-gate")
    parser.add_argument("--target-file", required=True)
    parser.add_argument("--provided-packet-file", required=True)
    parser.add_argument("--proof-file", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--packet-file",
        default=str(DEFAULT_PACKET_PATH),
        help="Prompt packet to load Citation Generator/Verifier prompts from.",
    )
    parser.add_argument("--allowed-support-file")
    parser.add_argument("--guidance-file")
    parser.add_argument("--solver-source-ledger-file")
    parser.add_argument("--bibliography-file", help="Optional bibliography, .bib, or .bbl text file.")
    parser.add_argument("--client", choices=["mock", "openai"], default="mock")
    parser.add_argument("--model")
    parser.add_argument("--api-base-url", default=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    parser.add_argument("--api-key")
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--web-search", action="store_true", help="Use OpenAI Responses API with the hosted web_search tool.")
    parser.add_argument(
        "--require-web-search",
        action="store_true",
        help="Require the model to call a tool when --web-search is enabled.",
    )
    parser.add_argument(
        "--web-search-context-size",
        choices=["low", "medium", "high"],
        help="Optional hosted web-search context size.",
    )
    parser.add_argument("--mock-citation-scenario", default="all_supported")
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args(argv)

    try:
        client = _make_client(args)
        prompt_templates = CitationPromptTemplates.from_file(args.packet_file)
        decision = run_citation_gate(
            output_dir=Path(args.output_dir),
            target_theorem=_read_text(Path(args.target_file), "target file"),
            provided_packet=_read_text(Path(args.provided_packet_file), "provided packet file"),
            allowed_supporting_statements=_read_optional(
                args.allowed_support_file,
                DEFAULT_ALLOWED_SUPPORTING_STATEMENTS,
                "allowed support file",
            ),
            guidance=_read_optional(args.guidance_file, "None", "guidance file"),
            proof=_read_text(Path(args.proof_file), "proof file"),
            solver_source_ledger=_read_optional(
                args.solver_source_ledger_file,
                "None",
                "solver source ledger file",
            ),
            client=client,
            bibliography=_read_optional(args.bibliography_file, "None", "bibliography file"),
            prompt_templates=prompt_templates,
            metadata={"citation_scenario": args.mock_citation_scenario},
            progress=_print_progress if args.progress else None,
        )
    except (RuntimeError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"{decision.gate_result} verifier_ran={decision.verifier_ran} artifacts={Path(args.output_dir)}")
    return 0


def _make_client(args):
    if args.client == "mock":
        return MockLLMClient(model=args.model or "mock-citation-model")
    return OpenAICompatibleClient(
        model=args.model or os.environ.get("OPENAI_MODEL", "gpt-4.1"),
        base_url=args.api_base_url,
        api_key=(args.api_key or os.environ.get(args.api_key_env)),
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        web_search=args.web_search,
        require_web_search=args.require_web_search,
        web_search_context_size=args.web_search_context_size,
    )


def _read_text(path: Path, label: str) -> str:
    if not path.exists():
        raise RuntimeError(f"{label} does not exist: {path}")
    return path.read_text(encoding="utf-8")


def _read_optional(path_value: str | None, default: str, label: str) -> str:
    return default if not path_value else _read_text(Path(path_value), label)


def _print_progress(message: str) -> None:
    print(message, file=sys.stderr, flush=True)
