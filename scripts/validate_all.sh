#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

cd "${PROJECT_ROOT}"
env -u PYTHONPATH uv sync --python 3.11 --frozen
(cd source/A1_2026 && sha256sum --check SHA256SUMS)
env -u PYTHONPATH uv run --frozen python scripts/export_assets.py >/dev/null
git diff --exit-code -- assets
env -u PYTHONPATH uv run --frozen pytest -q
env -u PYTHONPATH uv run --frozen ruff check src tests scripts

for model in right left bimanual; do
  "${SCRIPT_DIR}/open_demo.sh" "${model}" --direct --steps 480
done

echo "ALL VALIDATIONS PASSED"

