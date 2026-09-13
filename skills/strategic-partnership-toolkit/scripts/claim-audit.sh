#!/usr/bin/env bash
# claim-audit.sh — Audit a claim ledger markdown file
# Strategic Partnership Toolkit v1.5.1
#
# Usage:
#   claim-audit.sh <file>              # audit a claim ledger
#   claim-audit.sh <file> --json       # JSON output
#   claim-audit.sh <file> --strict     # fail if any claim lacks source
#
# Exit codes:
#   0 = PASS (all claims sourced, thresholds met)
#   1 = FAIL (thresholds breached or structural issues)
#   2 = ERROR (file not found, parse error)

set -euo pipefail

# --- Config ---
VERIFIED_RE="✅|VERIFIED|verificado|confirmed|CONFIRMED"
PARTIAL_RE="⚠️|PARTIAL|parcial|partial|inferred|INFERRED|inferido"
DISCARDED_RE="❌|DISCARDED|DESCARTADO|descartado|eliminado"
WEAK_RE="🟡|WEAK|HIPÓTESIS|hipótesis|débil|weak|HYPOTHESIS"
JSON_OUTPUT=false
STRICT_MODE=false

# --- Args ---
if [[ $# -lt 1 ]]; then
  echo "Usage: claim-audit.sh <file> [--json] [--strict]" >&2
  exit 2
fi

FILE="$1"
shift
while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) JSON_OUTPUT=true ;;
    --strict) STRICT_MODE=true ;;
  esac
  shift
done

if [[ ! -f "$FILE" ]]; then
  echo "ERROR: File not found: $FILE" >&2
  exit 2
fi

# --- Counters ---
VERIFIED=0; PARTIAL=0; DISCARDED=0; WEAK=0; UNSOURCED=0; TOTAL=0
declare -A UNSOURCED_CLAIMS

# --- Parse ---
while IFS= read -r line; do
  # Match claim rows: lines with status symbols
  if echo "$line" | grep -qE "\|.*\|.*\|"; then
    # Skip header rows
    echo "$line" | grep -qiE "^(#|\|.*claim.*\||.*afirmación.*\||.*estado.*status)" && continue

    TOTAL=$((TOTAL + 1))
    claim_id="C$TOTAL"
    claim_text=$(echo "$line" | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $2}')

    if echo "$line" | grep -qE "$VERIFIED_RE"; then
      VERIFIED=$((VERIFIED + 1))
      tag="✅ VERIFIED"
    elif echo "$line" | grep -qE "$PARTIAL_RE"; then
      PARTIAL=$((PARTIAL + 1))
      tag="⚠️ PARTIAL"
    elif echo "$line" | grep -qE "$DISCARDED_RE"; then
      DISCARDED=$((DISCARDED + 1))
      tag="❌ DISCARDED"
    elif echo "$line" | grep -qE "$WEAK_RE"; then
      WEAK=$((WEAK + 1))
      tag="🟡 WEAK"
    else
      # Unrecognized status
      WEAK=$((WEAK + 1))
      tag="? UNKNOWN"
    fi

    # Check for source/evidence column
    # A well-formed claim row should have at least 4 pipe-separated columns:
    # | # | Claim | Status | Source |
    col_count=$(echo "$line" | tr -cd '|' | wc -c | tr -d ' ')
    if [[ $col_count -lt 3 ]]; then
      UNSOURCED=$((UNSOURCED + 1))
      UNSOURCED_CLAIMS["$claim_id"]="$claim_text"
    fi
  fi
done < "$FILE"

# If no claims found via table parsing, try numbered list format
if [[ $TOTAL -eq 0 ]]; then
  while IFS= read -r line; do
    if echo "$line" | grep -qE "^[0-9]+\.\s|^[0-9]+\)\s|^- \*\*C[0-9]+|^- \*\*[0-9]+"; then
      TOTAL=$((TOTAL + 1))
      if echo "$line" | grep -qE "$VERIFIED_RE"; then
        VERIFIED=$((VERIFIED + 1))
      elif echo "$line" | grep -qE "$PARTIAL_RE"; then
        PARTIAL=$((PARTIAL + 1))
      elif echo "$line" | grep -qE "$DISCARDED_RE"; then
        DISCARDED=$((DISCARDED + 1))
      else
        WEAK=$((WEAK + 1))
      fi
    fi
  done < "$FILE"
fi

# --- Thresholds ---
# From diagram-auditor pattern:
# FAIL if ≥20% fabricated/discarded (in analysis context: discarded without source = risk)
# DRAFT if >50% partial+weak (unconfirmed majority)
DRAFT_PCT=0
FAIL_PCT=0
if [[ $TOTAL -gt 0 ]]; then
  UNCONFIRMED=$((PARTIAL + WEAK + UNSOURCED))
  DRAFT_PCT=$((UNCONFIRMED * 100 / TOTAL))
  FAIL_PCT=$((DISCARDED * 100 / TOTAL))
fi

# --- Verdict ---
VERDICT="PASS"
if [[ $DRAFT_PCT -gt 50 ]]; then
  VERDICT="DRAFT"
fi
if [[ $FAIL_PCT -ge 20 ]] || [[ $DISCARDED -gt 0 && $TOTAL -gt 0 ]]; then
  # In analysis context: any discarded claim without source is a flag
  # Only FAIL if ≥20% or in strict mode
  if [[ $FAIL_PCT -ge 20 ]]; then
    VERDICT="FAIL"
  fi
fi
if [[ $UNSOURCED -gt 0 ]] && $STRICT_MODE; then
  VERDICT="FAIL"
fi

# --- Output ---
if $JSON_OUTPUT; then
  cat << EOF
{
  "file": "$FILE",
  "total_claims": $TOTAL,
  "verified": $VERIFIED,
  "partial": $PARTIAL,
  "discarded": $DISCARDED,
  "weak": $WEAK,
  "unsourced": $UNSOURCED,
  "unconfirmed_pct": $DRAFT_PCT,
  "discarded_pct": $FAIL_PCT,
  "verdict": "$VERDICT"
}
EOF
else
  echo "════════════════════════════════════════"
  echo " Claim Audit: $(basename "$FILE")"
  echo "════════════════════════════════════════"
  echo
  echo "  Claims found:   $TOTAL"
  echo "  ✅ Verified:     $VERIFIED"
  echo "  ⚠️  Partial:     $PARTIAL"
  echo "  ❌ Discarded:    $DISCARDED"
  echo "  🟡 Weak:         $WEAK"
  echo "  ⚠️  Unsourced:   $UNSOURCED"
  echo
  echo "  Unconfirmed:    ${UNCONFIRMED:-0}/$TOTAL ($DRAFT_PCT%)"
  echo "  Discarded:      $DISCARDED/$TOTAL ($FAIL_PCT%)"
  echo
  echo "  Thresholds:"
  echo "    DRAFT  = >50% unconfirmed ${DRAFT_PCT}% → $([ $DRAFT_PCT -gt 50 ] && echo 'TRIGGERED' || echo 'ok')"
  echo "    FAIL   = ≥20% discarded  ${FAIL_PCT}% → $([ $FAIL_PCT -ge 20 ] && echo 'TRIGGERED' || echo 'ok')"
  echo
  if [[ $UNSOURCED -gt 0 ]]; then
    echo "  ⚠️  Claims without source column:"
    for id in "${!UNSOURCED_CLAIMS[@]}"; do
      echo "    $id: ${UNSOURCED_CLAIMS[$id]}"
    done
    echo
  fi
  echo "════════════════════════════════════════"
  if [[ "$VERDICT" == "PASS" ]]; then
    echo " VERDICT: ✅ PASS — all claims within thresholds"
  elif [[ "$VERDICT" == "DRAFT" ]]; then
    echo " VERDICT: ⚠️  DRAFT — majority unconfirmed, not decision-ready"
  elif [[ "$VERDICT" == "FAIL" ]]; then
    echo " VERDICT: ❌ FAIL — thresholds breached"
  fi
  echo "════════════════════════════════════════"
fi

# --- Exit code ---
[[ "$VERDICT" == "PASS" ]] && exit 0 || exit 1
