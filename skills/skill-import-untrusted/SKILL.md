---
# Advisory frontmatter: portable consumers are only required to parse `name` and
# `description`. Every other field is safe-to-ignore metadata (see resources/frontmatter-guide.md).
name: skill-import-untrusted
description: "Use when importing an untrusted or unapproved skill from a URL, repository, archive, or unknown disk path; verify provenance, license, secrets, invariants, and promote transactionally. Do NOT use for an approved local skill whose bytes are unchanged."
search_hints: import untrusted skill onboard from URL clone external skill verify provenance repair license preserve attribution transactional promotion staged verification
license: Apache-2.0
metadata:
  author: Felipe Gonzalez
  version: "2.1.6"
  tier: T2
  risk: local-write
  playbook: workflow
  replaces: skill-workflow
  lane: hardened-import
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Skill Workflow v2.1.5 (Hardened Onboarding Engine)

Transactional, provenance-safe, evidence-backed workflow for importing, standardizing,
refactoring, and verifying agent skills into the local ecosystem. Filesystem + POSIX
shell + python3 is the true interface; every step below runs identically regardless of
the agent harness driving it.

---

## Path Bases

All commands separate two explicit bases. Mixing relative namespaces is prohibited.

- `SKILL_DIR` — absolute path to THIS package root (directory containing this file).
  Every internal script is invoked as `"$SKILL_DIR/scripts/<script>"`.
- `WORKSPACE_ROOT` — absolute path to the hub workspace root holding `skills/`,
  `.atl/skill-registry.md`, and `receipts/`. Staging lives at
  `$WORKSPACE_ROOT/skills/.staging/{run-id}/`.

---

## When to Use

**Use for:** importing/onboarding an external skill; provenance/license/attribution
repair during onboarding; refactoring a skill while preserving negative rules;
candidate verification against a staged registry; registry collision checks;
transactional promotion under lock.

**Do NOT use for:** creating a brand-new skill from scratch (`skill-creator`);
general questions that only literally mention "install skill"; casual edits to another
skill's internal workflow unrelated to onboarding.

---

## Resource Map

| Phase | When needed | Resource |
|---|---|---|
| Fetch & Classify | Provenance digest, tiers, risk, security scan | [resources/analysis-checklist.md](resources/analysis-checklist.md) |
| Normalize | Two-tier frontmatter schema and field rules | [resources/frontmatter-guide.md](resources/frontmatter-guide.md) |
| Semantic-Lock | Invariant extraction and decoupling patterns | [resources/refactor-patterns.md](resources/refactor-patterns.md) |
| Freeze fixtures | Intent fixture design and deterministic Judge B rules | [resources/trigger-testing.md](resources/trigger-testing.md) |
| Quality gate | Mechanical markdown checks before registration | [resources/markdown-quality.md](resources/markdown-quality.md) |
| Execute pipeline | The literal transactional runbook (commands below) | [resources/runbook.md](resources/runbook.md) |

---

## Critical Patterns

### Pattern 0: Staging, Dotfile Preservation & Canonical Manifest
Never edit skills in-place or write directly to live production directories before verification:
1. Work exclusively inside an isolated staging sandbox on the same filesystem:
   `$WORKSPACE_ROOT/skills/.staging/{run-id}/candidate/`.
2. Preserve **all** files including dotfiles during fetch:
   ```bash
   cp -R /path/to/upstream-skill/. skills/.staging/{run-id}/candidate/
   ```
3. Generate the canonical **Tree Manifest & Digest** across all files, dotfiles,
   symlinks, and file modes using the single canonical implementation:
   ```bash
   "$SKILL_DIR/scripts/generate_manifest.sh" skills/.staging/{run-id}/candidate skills/.staging/{run-id}/TREE_MANIFEST
   ```
   No other algorithm may produce a `TREE_MANIFEST` (single manifest contract).
4. Record source repository/commit, upstream author, and upstream license.
5. Preserve the upstream license verbatim (e.g. `MIT`, `GPL`, `Apache-2.0`, `Unlicense`). **Never perform license washing.**

### Pattern 1: Multi-Axis Classification
Classify the skill across three explicit axes:
- **Complexity Tier:** `T0` (Utility) | `T1` (Specialist) | `T2` (Workflow) | `T3` (Orchestrator).
- **Capability Risk:** `read-only` | `local-write` | `git-mutating` | `network-external` | `elevated-exec`.
- **Playbook Tag:** `debug` | `testing` | `architecture` | `governance` | `workflow` | `data`.

### Pattern 2: Semantic-Lock (Invariants & Pre-Frozen Fixtures)
Before modifying or refactoring `SKILL.md`:
1. **Extract ALL Invariants (D1):** Capture every non-negotiable negative rule, security boundary, and prerequisite into `## Critical Patterns`. Do not cap or compress rules to satisfy arbitrary line counts (semantic completeness outranks token budgets).
2. **Pre-Freeze Verification Fixtures:**
   - 2–3 positive user intent queries.
   - 1 paraphrase query.
   - 1 near-miss negative query (that MUST NOT trigger this skill).
   - 1 neighboring-skill confusion query.
   - 1 smoke behavioral command/property check for executable skills.
3. **Decouple Cleanly:** Code templates go to `assets/`, local technical guides go to `references/` (local relative markdown links for dependencies; external URLs permitted for provenance citations).

### Pattern 3: Least Privilege & Schema Normalization
- Enforce least-privilege `allowed-tools` (e.g. `Read, Glob, Grep` for T0/T1 reading skills; add `Write, Bash` only when required).
- Frontmatter follows the two-tier contract of [resources/frontmatter-guide.md](resources/frontmatter-guide.md): `name` + `description` are the universal core; everything else is advisory.

### Pattern 4: Frozen Snapshot Overlay & TOCTOU Guard
Verification MUST run against the candidate registry overlay before modifying live files:
1. **Freeze Snapshot:** Initialize transaction and freeze live registry and live skill baseline:
   ```bash
   python3 "$SKILL_DIR/scripts/txn_manager.py" init skills/.staging/{run-id} <skill-name> .atl/skill-registry.md skills/<skill-name>
   ```
2. **Compile Candidate Overlay:** Compile $\text{LIVE BASE SNAPSHOT} \setminus \text{OLD ENTRY} \cup \text{CANDIDATE}$:
   ```bash
   python3 "$SKILL_DIR/scripts/compile_overlay.py" skills/.staging/{run-id}/base/live-registry.md skills/.staging/{run-id}/compact_rules.md <skill-name> skills/.staging/{run-id}/candidate-registry.md
   ```
3. **Fail-Closed Verification Harness:** Execute `"$SKILL_DIR/scripts/verify_candidate.py"` (Judge A exact lookup, Judge B deterministic frozen-fixture battery, capability-aware smoke test).

### Pattern 5: Controlled Promotion under Lock with Compensating Rollback
Staging layout on the same filesystem:

```
skills/.staging/{run-id}/
├── candidate/             # Isolated candidate skill tree
├── compact_rules.md       # Pre-digested compact rules block
├── candidate-registry.md  # Compiled overlay (Live Base Snapshot + Delta)
├── base/                  # Frozen snapshot before overlay compilation
│   ├── live-registry.md   # Exact baseline registry
│   └── live-skill/        # Exact baseline skill tree
├── backup/                # Pre-commit backup storage (isolated from candidate)
│   ├── live-skill/        # Snapshot of live skill before swap
│   └── live-registry.md   # Exact snapshot of .atl/skill-registry.md
├── txn_state.json         # Transaction state journal (INIT -> PRECOMMIT -> SKILL_SWAPPED -> REGISTRY_SWAPPED -> COMPLETE)
└── TREE_MANIFEST          # Canonical tree digest
```

**Single Critical-Section Promotion Protocol:**
```text
ACQUIRE EXCLUSIVE LOCK (.atl/.promotion.lock)
        ↓
DUAL TOCTOU CHECK (verify current live registry & skill tree match base snapshot)
        ↓
BACKUP LIVE STATE TO backup/
        ↓
ATOMIC SWAP SKILL TREE (mv candidate -> skills/<name>) [State: SKILL_SWAPPED]
        ↓
ATOMIC SWAP REGISTRY (.tmp -> .atl/skill-registry.md) [State: REGISTRY_SWAPPED]
        ↓
EXACT READBACK VALIDATION
        ↓
EMIT DURABLE RECEIPT (via receipt_manager.py CLI) [State: COMPLETE]
        ↓
RELEASE EXCLUSIVE LOCK
```

If any step fails inside the critical section, recovery claims success ONLY after verified
byte-level restoration: `python3 "$SKILL_DIR/scripts/txn_manager.py" recover
skills/.staging/{run-id}` restores from `backup/live-*` then `base/live-*` and verifies
digest readback; otherwise it emits `RECOVERY_FAILED` + intervention-required and exits non-zero.

---

## Execution Runbook

The literal command sequence (bases resolution → fetch → manifest → fixtures → txn init
→ overlay → verify → locked promotion → receipt CLI → unlock) lives in
[resources/runbook.md](resources/runbook.md). Invoke it only after Phase classification
is complete and both bases above resolve. The sequence is smoke-tested verbatim by the
engineering suite and fails closed on unset bases.

---

## Production-Readiness Gates (Hardened Lane — added per FULL_ANTIDRIFT audit)

This lane is read-only safe only after these gates PASS with `exit_code: 0` evidence:

1. **Secret Quarantine — explicit evidence:** `verify_candidate.py` Gate 1 must be proven via `evidence_matrix` entry showing 0 sensitive files found (e.g. `SENSITIVE_PATTERNS` scan over candidate tree). A bare `preflight: PASS` without a dedicated `secret_quarantine` artifact is `DEGRADED` → fail.
2. **TOCTOU Guard — explicit evidence:** `txn_manager.py check_toctou` must be recorded as a separate evidence entry with `exit_code: 0` and digest match against `base/live-registry.md` + `base/live-skill/`. A receipt stating `TOCTOU: N/A` is invalid.
3. **Atomic Promotion — explicit evidence:** `receipt_manager.py emit` must record `SKILL_SWAPPED` + `REGISTRY_SWAPPED` via temp `.tmp → mv` with readback digest; if recover path was taken, `txn_manager.py recover` must show `ROLLED_BACK` with byte-level digest verification.
4. **Discovery Reconciliation (new):** After promotion, prove the promoted skill is discoverable where it matters:
   ```bash
   skill-hub "<skill-name>"                          # expect managed entry with correct Source/Path, not "No results"
   skill-hub --cards "<realistic user intent query>" # expect promotion without trigger collision
   ```
   If either returns `No results` or promotes a colliding skill, return `status: degraded` with `residual_risks: ["discovery not reconciled"]`. Skill-hub may return `exit 0` with `No results` — validate content, not code.
5. **Source Authenticity (beyond provenance):** Record upstream URL/commit verification where applicable; provenance registration alone does not prove authenticity.

## Done Criteria

- [ ] Upstream license and author attribution preserved without license washing.
- [ ] Tier (`T0`–`T3`), Capability Risk, and Playbook assigned.
- [ ] Canonical `TREE_MANIFEST` and `TREE_DIGEST` generated by `generate_manifest.sh` with dotfiles and modes preserved.
- [ ] Semantic Lock complete: all invariants preserved; code decoupled to `assets/` and docs to `references/`.
- [ ] Frontmatter normalized to the two-tier schema with least-privilege `allowed-tools`.
- [ ] Frozen snapshot base compiled into overlay via `compile_overlay.py`.
- [ ] `verify_candidate.py` PASSes every frozen fixture (deterministic Judge B) and the capability-aware smoke test — with explicit secret-quarantine evidence.
- [ ] TOCTOU Guard and Atomic Promotion proven as separate evidence entries (not `N/A`).
- [ ] Promotion executed inside an exclusive lock critical section (`lock -> check_toctou -> swap -> receipt -> unlock`).
- [ ] Execution receipt generated at `receipts/onboarding-{skill}-{run-id}.md` (for both PASS and FAIL) plus discovery reconciliation (`skill-hub`/`--cards`) evidence.
- [ ] Source authenticity recorded where applicable (URL/commit), not just provenance string.
