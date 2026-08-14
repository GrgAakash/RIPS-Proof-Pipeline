#!/usr/bin/env bash
set -euo pipefail

: "${OPENAI_API_KEY:?Set OPENAI_API_KEY in the environment}"
: "${ARXIV:?Set ARXIV to an ID or arxiv.org URL}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CODE_ROOT="${REPO_ROOT}/Individual Pipeline"
WORKSPACE_ROOT="${REPO_ROOT}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

cd "${CODE_ROOT}"

"${PYTHON_BIN}" paper_cleaner/run.py \
  --arxiv "${ARXIV}" \
  --config paper_cleaner/config.yaml \
  --runs-dir "${WORKSPACE_ROOT}/Inputs/paper_cleaner_input" \
  --stop-after step5
