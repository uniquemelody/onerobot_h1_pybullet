#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

if ! command -v uv >/dev/null 2>&1; then
  echo "错误：未找到 uv。请先安装 uv：https://docs.astral.sh/uv/" >&2
  exit 1
fi

env -u PYTHONPATH uv sync --project "${PROJECT_ROOT}" --python 3.11 --frozen
echo "安装完成。运行：${PROJECT_ROOT}/scripts/open_demo.sh right"

