"""Prompt assembly and stage runners for optional API-backed verifier calls."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from verifiers.api_client import ApiVerifierResult, call_openai_verifier
from verifiers.api_config import ApiConfig
from verifiers.schemas import VerifierInput


ApiCall = Callable[[str], ApiVerifierResult]

PROMPT_DIR = Path(__file__).resolve().parent / "prompts"
TEXT_SKELETON_SUFFIXES = {".tex", ".txt", ".md"}
INPUTS_MARKER = "--- INPUTS FOR THIS RUN ---"


def run_verifier_a_api(
    inputs: VerifierInput,
    *,
    run_id: str,
    config: ApiConfig,
    api_call: ApiCall | None = None,
) -> ApiVerifierResult:
    prompt = build_verifier_a_prompt(inputs, run_id=run_id)
    if api_call is None:
        return call_openai_verifier(prompt, config=config)
    return api_call(prompt)


def run_verifier_a1_api(
    inputs: VerifierInput,
    *,
    config: ApiConfig,
    api_call: ApiCall | None = None,
) -> ApiVerifierResult:
    return run_verifier_a_api(inputs, run_id="A1", config=config, api_call=api_call)


def build_verifier_a_prompt(inputs: VerifierInput, *, run_id: str) -> str:
    template = _read_prompt_template("verifier_a.md")
    return build_proof_verifier_prompt(template=template, inputs=inputs, run_id=run_id)


def build_verifier_b_prompt(inputs: VerifierInput) -> str:
    template = _read_prompt_template("verifier_b.md")
    return build_proof_verifier_prompt(template=template, inputs=inputs, run_id="B")


def build_verifier_c_prompt(inputs: VerifierInput) -> str:
    template = _read_prompt_template("verifier_c.md")
    return build_proof_verifier_prompt(template=template, inputs=inputs, run_id="C")


def build_proof_verifier_prompt(*, template: str, inputs: VerifierInput, run_id: str) -> str:
    guidance = "\n".join(f"- {item}" for item in inputs.guidance_list) if inputs.guidance_list else "None"
    skeleton_text = read_skeleton_text_if_available(inputs.skeleton_ref)
    return f"""{template}

--- CONCRETE INPUT PACKAGE FOR API RUN ---
Verifier run id:
{run_id}

Skeleton reference:
{inputs.skeleton_ref}

Cleaned skeleton text, if available:
{skeleton_text}

Target theorem:
{inputs.target_theorem}

Allowed supporting statements:
{inputs.allowed_supporting_statements}

Additional mathematical guidance:
{guidance}

Proposed proof artifact P_k:
{inputs.proof_artifact}
"""


def run_verifier_b_api(
    inputs: VerifierInput,
    *,
    config: ApiConfig,
    api_call: ApiCall | None = None,
) -> ApiVerifierResult:
    prompt = build_verifier_b_prompt(inputs)
    if api_call is None:
        return call_openai_verifier(prompt, config=config)
    return api_call(prompt)


def run_verifier_c_api(
    inputs: VerifierInput,
    *,
    config: ApiConfig,
    api_call: ApiCall | None = None,
) -> ApiVerifierResult:
    prompt = build_verifier_c_prompt(inputs)
    if api_call is None:
        return call_openai_verifier(prompt, config=config)
    return api_call(prompt)


def run_composer_a_api(
    *,
    a_reports: dict[str, str],
    config: ApiConfig,
    step_id_map: str = "None",
    api_call: ApiCall | None = None,
) -> ApiVerifierResult:
    prompt = build_composer_a_prompt(a_reports=a_reports, step_id_map=step_id_map)
    if api_call is None:
        return call_openai_verifier(prompt, config=config)
    return api_call(prompt)


def build_composer_a_prompt(*, a_reports: dict[str, str], step_id_map: str = "None") -> str:
    template = _read_prompt_template("composer_a.md")
    report_blocks = "\n\n".join(
        f"--- {name} REPORT ---\n{raw.strip()}" for name, raw in sorted(a_reports.items())
    )
    return f"""{template}

--- CONCRETE INPUT PACKAGE FOR API RUN ---
Step-ID map:
{step_id_map or "None"}

Verifier A reports:
{report_blocks}
"""


def read_skeleton_text_if_available(skeleton_ref: str) -> str:
    """Embed local text skeletons while preserving abstract skeleton references."""
    path_text = skeleton_ref.split("#", 1)[0].strip()
    if not path_text:
        return "Not embedded; skeleton_ref is empty."

    path = Path(path_text)
    if path.suffix.lower() not in TEXT_SKELETON_SUFFIXES:
        return "Not embedded; skeleton_ref does not point to a supported text skeleton file."

    if not path.is_file():
        return "Not embedded; skeleton_ref is not a local readable file."

    return path.read_text(encoding="utf-8-sig")


def _read_prompt_template(filename: str) -> str:
    """Read only fixed instructions; concrete inputs are appended by code."""

    text = (PROMPT_DIR / filename).read_text(encoding="utf-8-sig")
    index = text.find(INPUTS_MARKER)
    if index >= 0:
        text = text[:index]
    return text.strip()
