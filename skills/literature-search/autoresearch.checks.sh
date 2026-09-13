#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Running 56 tests ==="
uv run pytest resources/tests/ -q 2>&1 | tail -5

echo ""
echo "=== mypy check ==="
uv run mypy resources/scoring.py 2>&1 | tail -3
