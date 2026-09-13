# Analysis & Classification Checklist (v2.1-R2)

Validation checklist for Phase 1 (Fetch & Freeze) and Phase 2 (Classify).

---

## 1. Provenance & Canonical Tree Digest

- [ ] `SKILL.md` exists at the root of the source.
- [ ] Source URI and commit/version are captured.
- [ ] **Canonical Tree Manifest Generated:** via the single canonical implementation
      `$SKILL_DIR/scripts/generate_manifest.sh` (contract: includes regular files,
      dotfiles, symlinks with targets, file modes, sizes, and per-file SHA-256;
      deterministic ordering; emits `TREE_DIGEST`). No ad-hoc `find`-based or filtered
      pseudo-manifest may substitute for it — any divergent algorithm is a contract violation.
- [ ] **License Check:** Upstream license (`MIT`, `GPL`, `Apache-2.0`, `Unlicense`, etc.) is identified and preserved verbatim.
  - ⚠️ **Zero License Washing:** Never overwrite external licenses with a default license.
- [ ] **Author Attribution:** Upstream author is recorded (`metadata.author`); local adopter is set (`metadata.onboarded_by`).

---

## 2. Multi-Axis Classification

### A. Complexity Tier
- [ ] **`T0` (Utility):** Single-purpose tool wrapper, formatting, basic command execution.
- [ ] **`T1` (Specialist Guide):** Idiomatic language rules, testing patterns, framework best practices.
- [ ] **`T2` (Multi-Step Workflow):** State-machine lifecycle, checklists, multi-phase procedures.
- [ ] **`T3` (Orchestration Engine):** Multi-agent loops, supervisor models, gate contracts.

### B. Capability Risk
- [ ] `read-only` (information retrieval, linting, docs)
- [ ] `local-write` (creates/edits local files within workspace)
- [ ] `git-mutating` (commits, branches, worktrees)
- [ ] `network-external` (API calls, web downloads, database queries)
- [ ] `elevated-exec` (system daemons, root commands, package installs)

### C. Playbook Tag
- [ ] `debug` | `testing` | `architecture` | `governance` | `workflow` | `data`

---

## 3. Security & Safety Scan

- [ ] No hardcoded API keys, bearer tokens, or secrets.
- [ ] No dangerous `eval()` or `exec()` on unsanitized inputs.
- [ ] No unbounded shell commands without explicit timeouts or path guards.
- [ ] Tool access strictly scoped to least-privilege (e.g. no blanket `Bash, Write` for read-only skills).

---

## 4. Directory Structure Standards

```
skill-name/
├── SKILL.md              # Required entrypoint (Critical Patterns + Orchestration)
├── assets/               # Optional: templates, code fixtures, schemas
├── references/           # Optional: local markdown technical guides + provenance URLs
├── resources/            # Optional: sub-phase guides
└── scripts/              # Optional: standalone executable helpers
```

### Artifacts That MUST NOT Exist
- [ ] `.git/` directory
- [ ] `evals/` or benchmark workspace dumps
- [ ] `*.log`, `*.tmp`, `.DS_Store`
