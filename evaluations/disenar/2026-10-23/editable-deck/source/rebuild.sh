#!/usr/bin/env bash
set -euo pipefail

TASK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$TASK_DIR"

RUNTIME_NODE="${CODEX_PRIMARY_RUNTIME_NODE:?Set CODEX_PRIMARY_RUNTIME_NODE}"
RUNTIME_PYTHON="${CODEX_PRIMARY_RUNTIME_PYTHON:?Set CODEX_PRIMARY_RUNTIME_PYTHON}"
RUNTIME_NODE_MODULES="${CODEX_PRIMARY_RUNTIME_NODE_MODULES:?Set CODEX_PRIMARY_RUNTIME_NODE_MODULES}"
PRESENTATIONS_SKILL_DIR="${PRESENTATIONS_SKILL_DIR:-/root/.codex/skills/builtins/presentations}"
OUTPUT_NAME="${1:-plan-talleres-2027-reconstruido.pptx}"
export TMPDIR="$TASK_DIR/build/tmp"
export XDG_CACHE_HOME="$TASK_DIR/build/cache"
mkdir -p "$TMPDIR" "$XDG_CACHE_HOME" "$TASK_DIR/output" "$TASK_DIR/checks" "$TASK_DIR/renders"
if [[ ! -e "$TASK_DIR/source/node_modules" ]]; then
  ln -s "$RUNTIME_NODE_MODULES" "$TASK_DIR/source/node_modules"
fi
if [[ -e "$TASK_DIR/output/$OUTPUT_NAME" ]]; then
  printf 'Output already exists: %s\n' "$OUTPUT_NAME" >&2
  exit 1
fi

"$RUNTIME_NODE" source/create_deck.mjs "$OUTPUT_NAME"
"$RUNTIME_PYTHON" -B source/capture_validator.py checks/package-integrity.json -- "$RUNTIME_PYTHON" -B "$PRESENTATIONS_SKILL_DIR/container_tools/inspect_presentation_package_integrity.py" build/candidate.pptx --fail-on-findings
"$RUNTIME_PYTHON" -B source/capture_validator.py checks/layout-geometry.json -- "$RUNTIME_PYTHON" -B "$PRESENTATIONS_SKILL_DIR/container_tools/inspect_presentation_layout_geometry.py" build/candidate.pptx --fail-on-findings --expected-slide-size-emu 12192000,6858000 --expected-slide-count 8 --approved-font-family 'Nimbus Sans' --require-uniform-font-family --validate-bullet-geometry --validate-heading-fit
"$RUNTIME_PYTHON" -B source/validate_deck.py
cp build/candidate.pptx "output/$OUTPUT_NAME"
"$RUNTIME_NODE" source/render_final.mjs "$OUTPUT_NAME"
"$RUNTIME_NODE" source/verify_native_edit.mjs "$OUTPUT_NAME"
"$RUNTIME_PYTHON" -B source/validate_deck.py "output/$OUTPUT_NAME"
