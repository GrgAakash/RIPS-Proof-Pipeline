#!/usr/bin/env bash
set -euo pipefail

: "${OPENAI_API_KEY:?Set OPENAI_API_KEY in the environment}"
: "${ARXIV:?Set ARXIV to an ID or arxiv.org URL}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CODE_ROOT="${REPO_ROOT}/Individual Pipeline"
WORKSPACE_ROOT="${REPO_ROOT}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
MODEL="${MODEL:-gpt-5.5}"

cd "${CODE_ROOT}"

"${PYTHON_BIN}" paper_cleaner_mini/run.py \
  --arxiv "${ARXIV}" \
  --input-root "${WORKSPACE_ROOT}/Inputs/paper_cleaner_input" \
  --out "${WORKSPACE_ROOT}/Outputs/mini" \
  --model "${MODEL}" \
  --audit-model "${MODEL}" \
  --effort high \
  --parallel 2
