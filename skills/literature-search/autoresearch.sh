#!/bin/bash
set -euo pipefail

# Autoresearch benchmark for deduplicate() optimization
# Generates 1000 papers, measures dedup speed, validates correctness

cd "$(dirname "$0")"

uv run python3 benchmark_dedup.py 2>&1
