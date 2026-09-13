#!/usr/bin/env bash
# tmux Plan Auditor - Orchestrator v2
# Runs 4 agents in parallel via tmux, produces handoff.json v2
set -euo pipefail
umask 077

# Configuration
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESOURCES_DIR="${SKILL_DIR}/resources"
DEFAULT_TIMEOUT="${AUDITOR_AGENT_TIMEOUT:-300}"  # 5 minutes default
AUTO_CLEANUP="${AUDITOR_AUTO_CLEANUP:-true}"

# Arguments
PLAN_PATH=""
BASE_SESSION="plan-audit"
RUN_ID="plan-audit-$(date +%Y%m%d-%H%M%S)-$$-$RANDOM"
WORKFLOW="feature"
INTERACTIVE_MODE="${AUDITOR_INTERACTIVE:-false}"

while [[ $# -gt 0 ]]; do
  case $1 in
    -p|--plan)
      PLAN_PATH="$2"
      shift 2
      ;;
    -s|--session)
      BASE_SESSION="$2"
      shift 2
      ;;
    -w|--workflow)
      WORKFLOW="$2"
      shift 2
      ;;
    -i|--interactive)
      INTERACTIVE_MODE="true"
      shift
      ;;
    *)
      if [[ -z "$PLAN_PATH" ]]; then
        PLAN_PATH="$1"
      elif [[ "$BASE_SESSION" == "plan-audit" ]]; then
        BASE_SESSION="$1"
      else
        RUN_ID="$1"
      fi
      shift
      ;;
  esac
done

SESSION_TARGET="${BASE_SESSION}-${RUN_ID}"

# Validation
if [[ -z "$PLAN_PATH" ]]; then
  echo "Usage: $0 [-w workflow] [-s session] <PLAN_PATH>"
  echo "Workflows: feature (default), bugfix, refactor, security"
  exit 1
fi

# Capture the caller project root before switching directories.
PROJECT_ROOT="$(pwd)"
export AUDITOR_PROJECT_ROOT="$PROJECT_ROOT"

# Validate plan path — reject paths with shell metacharacters BEFORE resolution
case "$PLAN_PATH" in
  *\'*|*\"*|*\`*|*\$*|*\(*|*\)*|*\{*|*\}*|*\[*|*\]*|*\&*|*\;*|*\|*|*\<*|*\>*)
    echo "Error: Plan path contains shell metacharacters: $PLAN_PATH" >&2
    exit 2
    ;;
esac

# Resolve plan path against the caller project root
PLAN_PATH="$(python3 -c 'from pathlib import Path; import sys; project_root = Path(sys.argv[1]); plan_arg = Path(sys.argv[2]).expanduser(); print((plan_arg if plan_arg.is_absolute() else (project_root / plan_arg)).resolve())' "$PROJECT_ROOT" "$PLAN_PATH")"

if [[ ! -f "$PLAN_PATH" ]]; then
  echo "Error: Plan not found: $PLAN_PATH"
  exit 1
fi


# Detect plan domain (preserve if already set)
if [[ -z "${AUDITOR_PLAN_DOMAIN:-}" ]]; then
  AUDITOR_PLAN_DOMAIN=$(python3 "${SKILL_DIR}/scripts/detect_domain.py" "$PLAN_PATH")
fi
export AUDITOR_PLAN_DOMAIN

# Validate domain — fall back to auto-detect if invalid
case "$AUDITOR_PLAN_DOMAIN" in
  tui-rich|web-api|cli|generic) ;;
  *)
    AUDITOR_PLAN_DOMAIN=$(python3 "${SKILL_DIR}/scripts/detect_domain.py" "$PLAN_PATH")
    export AUDITOR_PLAN_DOMAIN
    ;;
esac

if [[ "$INTERACTIVE_MODE" == "true" ]] && ! command -v tmux >/dev/null 2>&1; then
  echo "Error: tmux is required for interactive mode but not installed" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required but not installed"
  exit 1
fi

# Validate workflow
case "$WORKFLOW" in
  feature|bugfix|refactor|security) ;;
  *)
    echo "Error: Invalid workflow '$WORKFLOW'. Must be: feature, bugfix, refactor, security" >&2
    exit 2
    ;;
esac
export AUDITOR_WORKFLOW="$WORKFLOW"

# Setup run directory (absolute path based on current working directory)
RUN_DIR="$(pwd)/_ctx/review_runs/${RUN_ID}"
mkdir -p "$RUN_DIR"

echo "=== tmux Plan Auditor v2 ==="
echo "Plan: $PLAN_PATH"
echo "Workflow: $WORKFLOW"
echo "Domain: $AUDITOR_PLAN_DOMAIN"
echo "Run ID: $RUN_ID"
echo "Timeout: ${DEFAULT_TIMEOUT}s"
echo "Run dir: $RUN_DIR"
echo "Mode: $([ "$INTERACTIVE_MODE" = "true" ] && echo "interactive (tmux)" || echo "fast (background)")"
echo ""

AGENTS=("logic" "code_quality" "silent_failure" "testing_static")

if [[ "$INTERACTIVE_MODE" == "true" ]]; then
  SESSION_TARGET="${BASE_SESSION}-${RUN_ID}"

  TMUX= tmux kill-session -t "$SESSION_TARGET" 2>/dev/null || true
  TMUX= tmux new-session -d -s "$SESSION_TARGET" -n orchestrator "echo 'Auditor session: $SESSION_TARGET'; exec bash"

  _cleanup_tmux() {
    TMUX= tmux kill-session -t "$SESSION_TARGET" 2>/dev/null || true
  }
  trap _cleanup_tmux EXIT INT TERM

  for _ in $(seq 1 20); do
    if TMUX= tmux has-session -t "$SESSION_TARGET" 2>/dev/null; then
      break
    fi
    sleep 0.05
  done

  for agent in "${AGENTS[@]}"; do
    json_out="${RUN_DIR}/agent-${agent//_/-}.json"
    txt_out="${RUN_DIR}/agent-${agent//_/-}.txt"

    TMUX= tmux new-window -t "$SESSION_TARGET" -n "agent-${agent}" \
      "cd '${SKILL_DIR}' && PYTHONPATH='${SKILL_DIR}' python3 -m resources.agents.${agent}_agent '${PLAN_PATH}' '${json_out}' '${txt_out}'; exec bash"
  done
else
  AGENT_PIDS=()

  _cleanup_bg() {
    for pid in "${AGENT_PIDS[@]}"; do
      kill "$pid" 2>/dev/null || true
    done
  }
  trap _cleanup_bg EXIT INT TERM

  for agent in "${AGENTS[@]}"; do
    agent_module="resources.agents.${agent}_agent"
    json_out="${RUN_DIR}/agent-${agent//_/-}.json"
    txt_out="${RUN_DIR}/agent-${agent//_/-}.txt"

    (
      cd "$SKILL_DIR"
      PYTHONPATH="$SKILL_DIR" python3 -m "$agent_module" \
        "$PLAN_PATH" "$json_out" "$txt_out" 2>"${txt_out}.err"
    ) &
    AGENT_PIDS+=($!)
  done
fi

# Wait for agents with polling
wait_for_agents() {
  local timeout=$1
  local elapsed=0
  local pending=()

  while [[ $elapsed -lt $timeout ]]; do
    pending=()
    for agent in "${AGENTS[@]}"; do
      json_out="${RUN_DIR}/agent-${agent//_/-}.json"
      if [[ ! -f "$json_out" ]]; then
        pending+=("$agent")
      elif ! python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$json_out" 2>/dev/null; then
        pending+=("$agent")
      fi
    done

    if [[ ${#pending[@]} -eq 0 ]]; then
      echo "All agents completed after ${elapsed}s"
      return 0
    fi

    echo "Waiting for: ${pending[*]} (${elapsed}s/${timeout}s)"
    sleep 1
    elapsed=$((elapsed + 1))
  done

  echo "Timeout reached. Pending agents: ${pending[*]}"
  return 1
}

echo "Waiting for agents..."
set +e
wait_for_agents "$DEFAULT_TIMEOUT"
WAIT_STATUS=$?
set -e

if [[ "$INTERACTIVE_MODE" != "true" ]]; then
  for pid in "${AGENT_PIDS[@]}"; do
    wait "$pid" 2>/dev/null || true
  done
  # Clean up .err files from background agents
  rm -f "${RUN_DIR}"/*.err
fi

# Build handoff
echo ""
echo "Building handoff.json..."

CLEANUP_FLAG="false"
if [[ "$AUTO_CLEANUP" == "true" && $WAIT_STATUS -eq 0 ]]; then
  CLEANUP_FLAG="true"
fi

if [[ "$INTERACTIVE_MODE" == "true" ]]; then
  HANDOFF_SESSION="$SESSION_TARGET"
else
  HANDOFF_SESSION="$RUN_ID"
fi
cd "$SKILL_DIR" || { echo "Error: Cannot access $SKILL_DIR" >&2; exit 1; }
PYTHONPATH="$SKILL_DIR" python3 "${RESOURCES_DIR}/handoff_builder.py" "$RUN_DIR" "$RUN_ID" "$HANDOFF_SESSION" "$PLAN_PATH" "$CLEANUP_FLAG" "$AUDITOR_PLAN_DOMAIN"

if [[ "$INTERACTIVE_MODE" == "true" && "$AUTO_CLEANUP" == "true" && $WAIT_STATUS -eq 0 ]]; then
  echo "Auto-cleanup: killing tmux session '$SESSION_TARGET'"
  trap - EXIT INT TERM
fi

# Generate summary
cat > "${RUN_DIR}/summary.md" <<EOS
# tmux Plan Auditor v2

- **Run ID:** ${RUN_ID}
- **Plan:** ${PLAN_PATH}
- **Run dir:** ${RUN_DIR}
- **Timeout:** ${DEFAULT_TIMEOUT}s
- **Mode:** $([ "$INTERACTIVE_MODE" = "true" ] && echo "interactive (tmux)" || echo "fast (background)")
- **Auto-cleanup:** ${AUTO_CLEANUP}

## Outputs

- [handoff.json](./handoff.json) - Main handoff file
- [patch-confirmation-template.json](./patch-confirmation-template.json) - User decisions template

## Agent outputs

- [agent-logic.json](./agent-logic.json)
- [agent-code-quality.json](./agent-code-quality.json)
- [agent-silent-failure.json](./agent-silent-failure.json)
- [agent-testing-static.json](./agent-testing-static.json)
EOS

if [[ "$INTERACTIVE_MODE" == "true" ]]; then
  cat >> "${RUN_DIR}/summary.md" <<EOS

## Manual attach

\`\`\`bash
tmux attach -t ${SESSION_TARGET}
\`\`\`
EOS
fi

echo ""
echo "=== Complete ==="
echo "Handoff: ${RUN_DIR}/handoff.json"
echo "Summary: ${RUN_DIR}/summary.md"

if [[ $WAIT_STATUS -ne 0 ]]; then
  echo "WARNING: Some agents timed out"
  exit 1
fi
