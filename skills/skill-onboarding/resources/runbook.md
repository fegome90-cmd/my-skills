# Transactional Onboarding Runbook (v2.1.5)

Literal-command sequence for a single onboarding run. This resource is the detailed
execution procedure referenced from `SKILL.md` (progressive disclosure): read it only
once classification (`Phase 2`) succeeded and you are about to enter the staged
transactional pipeline.

---

## 1. Bases (mandatory, no relative mixing)

| Base | Meaning | Resolution rule |
|---|---|---|
| `$SKILL_DIR` | Absolute path to THIS skill package root (the directory that contains this `resources/runbook.md`). | Export explicitly or derive as the parent of this file's directory. |
| `$WORKSPACE_ROOT` | Absolute path to your hub/workspace root holding `skills/`, `.atl/skill-registry.md`, and `receipts/`. | Export explicitly. |

Mixing namespaces is prohibited: every internal script MUST be invoked as
`"$SKILL_DIR/scripts/<name>"`; every staging/live artifact is expressed relative to
`$WORKSPACE_ROOT`. The sequence fails closed if either base is unset.

Substitute every `{{TOKEN}}` before executing (editor-side authoring step).

## 2. Preconditions

- [ ] Upstream skill fetched location known (`{{UPSTREAM_PATH}}`).
- [ ] Invariants extracted (Semantic-Lock D1 complete).
- [ ] Fixture battery frozen (see `trigger-testing.md`) ready for the `{{FIXTURES_JSON}}` slot.
- [ ] Compact rules drafted for the `{{COMPACT_RULES_BLOCK}}` slot.
- [ ] Classification decided: `{{TIER}}` / `{{RISK}}` / `{{PLAYBOOK}}`.

## 3. Literal Command Sequence

```bash
# Resolve mandatory bases (fail closed if unset)
export SKILL_DIR="${SKILL_DIR:?SKILL_DIR must point to the installed skill-workflow package root}"
export WORKSPACE_ROOT="${WORKSPACE_ROOT:?WORKSPACE_ROOT must point to the workspace root containing skills/ and .atl/}"
cd "$WORKSPACE_ROOT"
set -euo pipefail

# 1. Fetch preserving dotfiles and generate canonical tree manifest
mkdir -p "skills/.staging/{{RUN_ID}}/candidate"
cp -R "{{UPSTREAM_PATH}}/." "skills/.staging/{{RUN_ID}}/candidate/"
"$SKILL_DIR/scripts/generate_manifest.sh" \
  "skills/.staging/{{RUN_ID}}/candidate" \
  "skills/.staging/{{RUN_ID}}/TREE_MANIFEST"

# 2. Author compact rules (Semantic-Lock output)
cat > "skills/.staging/{{RUN_ID}}/compact_rules.md" <<'RULES_EOF'
{{COMPACT_RULES_BLOCK}}
RULES_EOF

# 3. Freeze the pre-frozen fixture battery (see ../resources/trigger-testing.md)
cat > "skills/.staging/{{RUN_ID}}/fixtures.json" <<'FIXTURES_EOF'
{{FIXTURES_JSON}}
FIXTURES_EOF

# 4. Initialize transaction and freeze base snapshot (before overlay compilation)
python3 "$SKILL_DIR/scripts/txn_manager.py" init \
  "skills/.staging/{{RUN_ID}}" \
  "{{SKILL_NAME}}" \
  ".atl/skill-registry.md" \
  "skills/{{SKILL_NAME}}"

# 5. Compile candidate registry overlay from frozen snapshot
python3 "$SKILL_DIR/scripts/compile_overlay.py" \
  "skills/.staging/{{RUN_ID}}/base/live-registry.md" \
  "skills/.staging/{{RUN_ID}}/compact_rules.md" \
  "{{SKILL_NAME}}" \
  "skills/.staging/{{RUN_ID}}/candidate-registry.md"

# 6. Execute fail-closed verification harness
python3 "$SKILL_DIR/scripts/verify_candidate.py" \
  "skills/.staging/{{RUN_ID}}/candidate" \
  "skills/.staging/{{RUN_ID}}/candidate-registry.md" \
  "skills/.staging/{{RUN_ID}}/fixtures.json" \
  "{{SKILL_NAME}}" \
  "{{RISK}}" \
  "skills/.staging/{{RUN_ID}}/verification_receipt.json"

# 7. Controlled promotion in a single critical section
# Step A: acquire exclusive lock
python3 "$SKILL_DIR/scripts/txn_manager.py" lock

# Step B: TOCTOU integrity validation under lock
python3 "$SKILL_DIR/scripts/txn_manager.py" check_toctou "skills/.staging/{{RUN_ID}}"
python3 "$SKILL_DIR/scripts/txn_manager.py" state "skills/.staging/{{RUN_ID}}" PRECOMMIT

# Step C: backup live state into backup/
mkdir -p "skills/.staging/{{RUN_ID}}/backup"
if [ -d "skills/{{SKILL_NAME}}" ]; then
  mv "skills/{{SKILL_NAME}}" "skills/.staging/{{RUN_ID}}/backup/live-skill"
fi
if [ -f ".atl/skill-registry.md" ]; then
  cp ".atl/skill-registry.md" "skills/.staging/{{RUN_ID}}/backup/live-registry.md"
fi

# Step D: atomic rename of the skill tree
mv "skills/.staging/{{RUN_ID}}/candidate" "skills/{{SKILL_NAME}}"
python3 "$SKILL_DIR/scripts/txn_manager.py" state "skills/.staging/{{RUN_ID}}" SKILL_SWAPPED

# Step E: atomic registry swap via tempfile
cp "skills/.staging/{{RUN_ID}}/candidate-registry.md" ".atl/skill-registry.md.tmp"
mv ".atl/skill-registry.md.tmp" ".atl/skill-registry.md"
python3 "$SKILL_DIR/scripts/txn_manager.py" state "skills/.staging/{{RUN_ID}}" REGISTRY_SWAPPED

# Step F: emit durable receipt through the receipt manager CLI (no PYTHONPATH coupling)
python3 "$SKILL_DIR/scripts/receipt_manager.py" emit \
  --receipt-dir "receipts" \
  --skill-name "{{SKILL_NAME}}" \
  --run-id "{{RUN_ID}}" \
  --status SUCCESS \
  --candidate-tree-digest "$(shasum -a 256 "skills/.staging/{{RUN_ID}}/TREE_MANIFEST" | awk '{print $1}')" \
  --upstream-author "{{UPSTREAM_AUTHOR}}" \
  --upstream-license "{{UPSTREAM_LICENSE}}" \
  --onboarded-by "Felipe Gonzalez" \
  --tier "{{TIER}}" \
  --risk "{{RISK}}" \
  --playbook "{{PLAYBOOK}}" \
  --gates-json "skills/.staging/{{RUN_ID}}/verification_receipt.json"

python3 "$SKILL_DIR/scripts/txn_manager.py" state "skills/.staging/{{RUN_ID}}" COMPLETE

# Step G: release lock
python3 "$SKILL_DIR/scripts/txn_manager.py" unlock
```

## 4. Recovery Contract (truthful, digest-verified)

If any critical-section step fails or a crash interrupts states `PRECOMMIT` (after live backup/mutations begin),
`SKILL_SWAPPED`, or `REGISTRY_SWAPPED`, run:

```bash
python3 "$SKILL_DIR/scripts/txn_manager.py" recover "skills/.staging/{{RUN_ID}}"
```

`recover` restores from `backup/live-*` first, then from `base/live-*` frozen by
`init`, and verifies restored bytes against the recorded baseline digests. It reports
`ROLLED_BACK` ONLY when readback matches exactly; otherwise it marks
`RECOVERY_FAILED` with `intervention_required=true` and exits non-zero. Silent
success is impossible by construction.
