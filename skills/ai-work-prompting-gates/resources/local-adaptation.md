# Local Agent Adaptation Pattern

Operational pattern for prompts targeting agents that execute in local shells, worktrees, crons, or CI runners.

---

## 1. Local Execution Scope

Define exact working boundaries before starting:
- **Repository Root:** Determine via `git rev-parse --show-toplevel`.
- **Log Destination:** Designate `$REPO_ROOT/logs/<run_id>.log`.
- **Staging Directory:** Designate `$REPO_ROOT/staging/<run_id>/` or an isolated git worktree.
- **Allowed Path Whitelist:** List the precise files or subdirectories eligible for modification.

---

## 2. Pre-Flight Verification Gate

Run read-only preflight checks before any mutation:
```bash
# 1. Verify working location
pwd
git rev-parse --show-toplevel

# 2. Record clean baseline snapshot
git status --porcelain

# 3. Verify required binaries and dependencies
which node bun git python3
node --version
git --version

# 4. Verify disk space and write permissions
test -w . && echo "CWD writable: OK"
```

**Abort conditions:**
- Working tree contains uncommitted changes on files in scope.
- Any required tool or binary is missing from PATH.
- Missing required environment variables or secrets.

---

## 3. Staging & Isolation Gate

- All file generations, builds, or data transforms must write to `staging/<run_id>/`.
- Do not mutate authoritative tracking branches or active configuration files in-place during test runs.

---

## 4. Promotion Gate

- Run the validation command against the artifacts in `staging/<run_id>/`.
- Validate schema, formatting, and tests.
- Atomically promote verified artifacts to target paths:
  ```bash
  # Atomic promotion example
  cp staging/<run_id>/output.json ./config/output.json
  ```

---

## 5. Rollback Gate

- If any validation check fails (exit code != 0), invoke rollback immediately:
  ```bash
  # Cleanup staging
  rm -rf staging/<run_id>/

  # Rollback tracked changes to baseline
  git checkout -- <modified-files>
  ```
- Emit a structured diagnostic receipt documenting the failure reason, exit code, and captured stderr.

---

## 6. Claim Discipline & Receipt

Conclude every execution with a verifiable execution receipt:
```markdown
### Execution Receipt
- **Run ID:** `run_20260913_191500`
- **Baseline Git Commit:** `a422ee8`
- **Modified Files:** `src/engine.ts`, `tests/engine.test.ts`
- **Validation Run:** `npm test` -> Exit code 0 (24 passed)
- **Observed Artifacts:** `dist/bundle.js` (checksum: `sha256:...`)
- **Residual Risks:** External network calls were mocked; live integration untested.
```
