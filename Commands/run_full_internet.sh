#!/usr/bin/env bash
set -euo pipefail

: "${OPENAI_API_KEY:?Set OPENAI_API_KEY in the environment}"
: "${PAPER_ID:?Set PAPER_ID}"
: "${TARGET_ID:?Set TARGET_ID}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CODE_ROOT="${REPO_ROOT}"
PYTHONPATH_ROOT="${REPO_ROOT}/Individual Pipeline"
PIPELINE_ENTRY="${REPO_ROOT}/run_pipeline.py"
WORKSPACE_ROOT="${REPO_ROOT}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
MODEL="${MODEL:-gpt-5.5}"
CITATION_MODEL="${CITATION_MODEL:-${MODEL}}"
CITATION_MAX_ATTEMPTS="${CITATION_MAX_ATTEMPTS:-2}"
CITATION_WEB_SEARCH_CONTEXT_SIZE="${CITATION_WEB_SEARCH_CONTEXT_SIZE:-medium}"
RUN_NAME="${RUN_NAME:-${PAPER_ID}_${TARGET_ID}_full_internet}"
RUN_TAG="${RUN_TAG:-paper_original_result}"
SOLVER_WORKERS="${SOLVER_WORKERS:-2}"
SOLVER_DELAY_SECONDS="${SOLVER_DELAY_SECONDS:-0}"
MAX_ROUNDS="${MAX_ROUNDS:-3}"
MAX_BRANCH_DEPTH="${MAX_BRANCH_DEPTH:-2}"
MAX_BRANCHES="${MAX_BRANCHES:-3}"
INCLUDE_PRIVATE_FINAL_CHECKER="${INCLUDE_PRIVATE_FINAL_CHECKER:-1}"
PAPER_INPUT_ROOT="${WORKSPACE_ROOT}/Inputs/paper_cleaner_input"
SOLVER_INPUT_ROOT="${WORKSPACE_ROOT}/Inputs/solver_input/${RUN_NAME}"
OUTPUT_ROOT="${WORKSPACE_ROOT}/Outputs/${RUN_NAME}"

PRIVATE_FINAL_CHECKER_ARGS=()
case "${INCLUDE_PRIVATE_FINAL_CHECKER}" in
  1|true|TRUE|yes|YES) PRIVATE_FINAL_CHECKER_ARGS=(--include-private-final-checker) ;;
  0|false|FALSE|no|NO) ;;
  *) echo "INCLUDE_PRIVATE_FINAL_CHECKER must be 1/0, true/false, or yes/no" >&2; exit 2 ;;
esac

cd "${CODE_ROOT}"

PYTHONPATH="${PYTHONPATH_ROOT}${PYTHONPATH:+:${PYTHONPATH}}" \
"${PYTHON_BIN}" "${PIPELINE_ENTRY}" \
  --cleaner-input-root "${PAPER_INPUT_ROOT}" \
  --cleaner-work-root "${OUTPUT_ROOT}/cleaner" \
  --prepared-dir "${SOLVER_INPUT_ROOT}" \
  --solver-run-dir "${OUTPUT_ROOT}/solver" \
  --paper-id "${PAPER_ID}" \
  --target-id "${TARGET_ID}" \
  --packet-file "Prompt Packet/PromptsWithFullInternet.md" \
  --run-tag "${RUN_TAG}" \
  --client openai \
  --cleaner-model "${MODEL}" \
  --cleaner-check-model "${MODEL}" \
  --cleaner-audit-model "${MODEL}" \
  --source-audit-model "${MODEL}" \
  --cleaner-effort high \
  --cleaner-parallel 1 \
  --source-web-search-context-size medium \
  --reasoning-effort high \
  --retry-max-attempts 8 \
  --progress \
  "${PRIVATE_FINAL_CHECKER_ARGS[@]}" \
  -- \
  --model "${MODEL}" \
  --citation-model "${CITATION_MODEL}" \
  --citation-max-attempts "${CITATION_MAX_ATTEMPTS}" \
  --citation-web-search-context-size "${CITATION_WEB_SEARCH_CONTEXT_SIZE}" \
  --solver-workers "${SOLVER_WORKERS}" \
  --solver-delay-seconds "${SOLVER_DELAY_SECONDS}" \
  --max-rounds "${MAX_ROUNDS}" \
  --max-branch-depth "${MAX_BRANCH_DEPTH}" \
  --max-branches "${MAX_BRANCHES}"
