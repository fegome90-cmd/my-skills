---
name: skill-import-untrusted
description: "Use when importing an untrusted or unapproved skill from a URL, repository, archive, or unknown disk path; orchestrates vetting via skill-vetting and transactional promotion via skill-onboarding. Do NOT use for approved local skills whose bytes are unchanged."
search_hints: import untrusted skill onboard from URL clone external skill verify provenance repair license preserve attribution transactional promotion staged verification
license: Apache-2.0
metadata:
  author: Felipe Gonzalez
  version: "2.1.6"
  tier: T1
  risk: local-write
  playbook: workflow
  lane: thin-wrapper
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Skill Import (Untrusted) — Thin Routing Wrapper

This skill is a thin routing wrapper that orchestrates the import of unvetted, external, or untrusted skills into the local workspace. It does NOT implement its own verification scripts or transaction engines; instead, it pipes through the two canonical single-source skills:

1. **`skill-vetting`**: Static scan for prompt injection, sensitive files, credentials, and structural signals.
2. **`skill-onboarding`**: The canonical onboarding engine (invariants, pre-frozen fixtures, manifest generation, TOCTOU validation, transactional promotion, and crash recovery).

---

## The 3-Step Import Protocol

### Step 1: Isolation & Vetting (`skill-vetting`)

1. Fetch or unpack the candidate into an isolated staging area outside production paths:
   ```bash
   RUN_ID="import-$(date +%Y%m%d-%H%M%S)"
   mkdir -p "skills/.staging/${RUN_ID}/candidate"
   # Copy or unpack candidate into skills/.staging/${RUN_ID}/candidate/
   ```
2. If unpacking from an archive (zip/tar), verify archive integrity and SHA-256 hash before extraction.
3. Run `skill-vetting` on the candidate directory:
   ```bash
   python3 skills/skill-vetting/scripts/scan.py "skills/.staging/${RUN_ID}/candidate"
   ```
4. Review the scanner report. Treat all scanner alerts as investigable signals (not absolute ground truth). Remediate any detected prompt injection overrides, secret leaks, or suspicious binaries.

### Step 2: Invariant Freeze & Provenance

1. Record upstream provenance, author attribution, and source license.
2. Verify that `candidate/SKILL.md` exists and extract any mandatory negative rules, constraints, or prerequisite commands.
3. Decouple helper resources cleanly into `assets/` and `references/`.

### Step 3: Canonical Onboarding (`skill-onboarding`)

Hand off the verified candidate directory to the canonical `skill-onboarding` engine:

```bash
# Follow the runbook in skills/skill-onboarding/resources/runbook.md
# using scripts in skills/skill-onboarding/scripts/:
# - compile_overlay.py
# - verify_candidate.py
# - txn_manager.py
# - receipt_manager.py
```

All transactional locks, atomic swaps, and crash recovery guarantees are governed exclusively by `skill-onboarding`.
