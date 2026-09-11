#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

if [[ ! -x "${PROJECT_ROOT}/.venv/bin/python" ]]; then
  "${SCRIPT_DIR}/setup.sh"
fi

MODEL="${1:-right}"
if [[ $# -gt 0 ]]; then
  shift
fi

exec env -u PYTHONPATH uv run --project "${PROJECT_ROOT}" --frozen \
  onerobotics-a1-pybullet "${MODEL}" "$@"

