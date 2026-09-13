# disk-cleanup-macos-safe v4 draft

This draft extends the safety-focused cleanup protocol with a macOS-native observability layer that distinguishes APFS/System/Data capacity, per-device allocation, measurement coverage, packages, cloud residency, native tool ownership, and diagnostic trends.

## Contents

- `SKILL.md` — policy, staged workflow, HITL contract, and deployment gate.
- `references/macos-storage-observability.md` — detailed measurement and interpretation reference.
- `scripts/macos_storage_audit.py` — read-only local audit and HTML/SVG report generator.
- `scripts/macos_resource_probe.swift` — read-only Foundation metadata probe for volume capacity and selected items.
- `tests/test_audit_logic.py` — portable logic tests.
- `tests/pressure-scenarios.md` — 46 behavioral safety scenarios.
- `tests/synthetic-report.html` — synthetic report render.
- `audits/` — versioned audit history:
  - `AUDIT.md`, `AUDIT-v2.md`, `AUDIT-v3.md` — early drafts.
  - `AUDIT-v4.md` — web-grounded audit, decisions, and remaining limitations.
  - `AUDIT-v5.md` — field-tested gaps from a real cleanup session, with proposed (unapplied) patches to `SKILL.md`.
- `v3-to-v4.patch` — full change set from v3.

## Run on macOS

```bash
python3 scripts/macos_storage_audit.py
```

Bounded deeper analysis:

```bash
python3 scripts/macos_storage_audit.py \
  --scope "$HOME/Developer" \
  --scope "$HOME/Library" \
  --deep-activity \
  --activity-file-limit 10000 \
  --large-gib 1
```

Growth comparison:

```bash
python3 scripts/macos_storage_audit.py \
  --baseline /path/to/prior/summary.json
```

Critically full startup disk:

```bash
python3 scripts/macos_storage_audit.py \
  --output /Volumes/External/macos-storage-audit
```

## Safety properties

The helpers contain no cleanup, move, prune, snapshot-removal, Trash-emptying, or privilege-escalation operation. Raw command output is bounded and marked when truncated. Low-space mode skips deep and optional scans. The report directory is protected evidence.

## Status

Portable logic tests, Python compilation, Swift syntax parsing, static destructive-command scanning, YAML parsing, and synthetic rendering are included in verification. This remains a draft until exercised on supported macOS versions and tested with independent RED/GREEN agent pressure scenarios.
