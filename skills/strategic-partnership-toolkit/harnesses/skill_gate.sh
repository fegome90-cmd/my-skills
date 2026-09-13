#!/usr/bin/env bash
#
# skill_gate.sh - Minimal portable validator for skill mini-harness outputs.
#
# It validates a plain text block between:
# <!-- skillgate:start -->
# <!-- skillgate:end -->
#
# The script is intentionally read-only: it validates structure, not truth.
#
# Usage:
#   skill_gate.sh template
#   skill_gate.sh check <output.md>
#   skill_gate.sh version

set -euo pipefail

readonly VERSION='0.1.1'
readonly STATUS_PASS='PASS'
readonly STATUS_LIMITED='PASS_WITH_LIMITATIONS'
readonly STATUS_FAIL='FAIL_PRELIMINARY_ONLY'

REQUIRED_STAGES=(
  'intake'
  'analysis'
  'output'
  'self_audit'
  'handoff'
)

failures=0

usage() {
  cat <<'EOF'
Usage:
  skill_gate.sh template
  skill_gate.sh check <output.md>
  skill_gate.sh version

Expected block:

<!-- skillgate:start -->
skill: my-skill-name
status: PASS_WITH_LIMITATIONS
stage:intake: COMPLETE
stage:analysis: COMPLETE
stage:output: COMPLETE
stage:self_audit: COMPLETE
stage:handoff: COMPLETE
source_ledger: PRESENT
claims: PRESENT
audit_result: PASS_WITH_LIMITATIONS
next_step_owner: project lead
next_step_artifact: one-page memo
next_step_boundary: no patient action before governance review
limitations: conference date unverified
<!-- skillgate:end -->
EOF
}

die() {
  printf 'ERROR: %s\n' "$1" >&2
  exit "${2:-2}"
}

template() {
  cat <<'EOF'
<!-- skillgate:start -->
skill: my-skill-name
status: PASS_WITH_LIMITATIONS
stage:intake: COMPLETE
stage:analysis: COMPLETE
stage:output: COMPLETE
stage:self_audit: COMPLETE
stage:handoff: COMPLETE
source_ledger: PRESENT
claims: PRESENT
audit_result: PASS_WITH_LIMITATIONS
next_step_owner: project lead
next_step_artifact: one-page memo
next_step_boundary: no patient action before governance review
limitations: conference date unverified
<!-- skillgate:end -->
EOF
}

extract_block() {
  local file="$1"
  local in_block=0
  local block_count=0
  local line=''

  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ "$line" == '<!-- skillgate:start -->' ]]; then
      (( block_count += 1 )) || true
      if [[ "$block_count" -gt 1 ]]; then
        die 'Multiple skillgate blocks found — only one allowed per file' 4
      fi
      in_block=1
      continue
    fi

    if [[ "$line" == '<!-- skillgate:end -->' ]]; then
      in_block=0
      continue
    fi

    if [[ "$in_block" -eq 1 ]]; then
      printf '%s\n' "$line"
    fi
  done <"$file"

  if [[ "$block_count" -eq 0 ]]; then
    return 1
  fi

  return 0
}

value_for_key() {
  local block="$1"
  local key="$2"
  local line=''

  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ "$line" =~ ^"${key}": ]]; then
      printf '%s\n' "${line#"${key}":}"
      return 0
    fi
  done <<<"$block"

  return 1
}

value_is_nonempty() {
  local block="$1"
  local key="$2"
  local value=''

  value="$(value_for_key "$block" "$key")" || return 1
  [[ "$value" =~ [^[:space:]] ]]
}

line_exists() {
  local block="$1"
  local wanted="$2"
  local line=''

  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ "$line" == "$wanted" ]] && return 0
  done <<<"$block"

  return 1
}

record_gate() {
  local name="$1"
  local ok="$2"
  local detail="$3"

  if [[ "$ok" -eq 0 ]]; then
    printf 'PASS %s %s\n' "$name" "$detail"
  else
    printf 'FAIL %s %s\n' "$name" "$detail"
    (( failures += 1 )) || true
  fi
}

check_stage() {
  local block="$1"
  local stage="$2"
  local expected="stage:${stage}: COMPLETE"

  if line_exists "$block" "$expected"; then
    record_gate "stage:${stage}" 0 'complete'
  else
    record_gate "stage:${stage}" 1 'missing or not COMPLETE'
  fi
}

check_status() {
  local block="$1"
  local status=''

  status="$(value_for_key "$block" 'status')" || {
    record_gate 'status' 1 'missing'
    return
  }

  # Trim whitespace.
  status="${status#"${status%%[![:space:]]*}"}"
  status="${status%"${status##*[![:space:]]}"}"

  case "$status" in
    "$STATUS_PASS"|"$STATUS_LIMITED")
      record_gate 'status' 0 "$status"
      ;;
    "$STATUS_FAIL")
      record_gate 'status' 1 'FAIL_PRELIMINARY_ONLY blocks final use'
      ;;
    *)
      record_gate 'status' 1 "invalid value: $status"
      ;;
  esac
}

check_audit_result() {
  local block="$1"
  local result=''

  result="$(value_for_key "$block" 'audit_result')" || {
    record_gate 'audit_result' 1 'missing'
    return
  }

  result="${result#"${result%%[![:space:]]*}"}"
  result="${result%"${result##*[![:space:]]}"}"

  case "$result" in
    "$STATUS_PASS"|"$STATUS_LIMITED")
      record_gate 'audit_result' 0 "$result"
      ;;
    "$STATUS_FAIL")
      record_gate 'audit_result' 1 'FAIL_PRELIMINARY_ONLY — output must be marked preliminary'
      ;;
    *)
      record_gate 'audit_result' 1 "invalid value: $result"
      ;;
  esac
}

check_required_key() {
  local block="$1"
  local key="$2"

  if value_is_nonempty "$block" "$key"; then
    record_gate "$key" 0 'present'
  else
    record_gate "$key" 1 'missing or empty'
  fi
}

check_literal_key_value() {
  local block="$1"
  local key="$2"
  local expected="$3"
  local line="${key}: ${expected}"

  if line_exists "$block" "$line"; then
    record_gate "$key" 0 "$expected"
  else
    record_gate "$key" 1 "expected '${line}'"
  fi
}

check_file() {
  local file="$1"
  local block=''

  [[ -r "$file" ]] || die "Cannot read output file: $file" 2

  block="$(extract_block "$file")" || die 'Missing skillgate block markers' 3
  [[ -n "$block" ]] || die 'Empty skillgate block' 3

  check_required_key "$block" 'skill'
  check_status "$block"

  local stage=''
  for stage in "${REQUIRED_STAGES[@]}"; do
    check_stage "$block" "$stage"
  done

  check_literal_key_value "$block" 'source_ledger' 'PRESENT'
  check_literal_key_value "$block" 'claims' 'PRESENT'
  check_audit_result "$block"
  check_required_key "$block" 'next_step_owner'
  check_required_key "$block" 'next_step_artifact'
  check_required_key "$block" 'next_step_boundary'
  check_required_key "$block" 'limitations'

  if [[ "$failures" -eq 0 ]]; then
    printf 'RESULT PASS\n'
    return 0
  fi

  printf 'RESULT FAIL failures=%s\n' "$failures"
  return 1
}

main() {
  local command="${1:-}"

  case "$command" in
    template)
      template
      ;;
    check)
      [[ $# -eq 2 ]] || die 'Usage: skill_gate.sh check <output.md>' 2
      check_file "$2"
      ;;
    version)
      printf '%s\n' "$VERSION"
      ;;
    -h|--help|help|'')
      usage
      ;;
    *)
      usage >&2
      die "Unknown command: $command" 2
      ;;
  esac
}

main "$@"
