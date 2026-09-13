---
disable-model-invocation: true
name: learned-pr-feedback-resolution
description: "Use when resolving bot review feedback (CodeRabbit, Copilot) on PRs. Provides workflow to categorize issues by severity, create atomic commits per WorkOrder, and document resolution. Do NOT use for human review comments."
search_hints: PR review feedback CodeRabbit Copilot bot comments resolution WorkOrder atomic commits
metadata:
  triggers:
    - "PR"
    - "review"
    - "feedback"
    - "CodeRabbit"
    - "Copilot"
  role: specialist
  scope: implementation
version: 1.0.0
---

# PR Feedback Resolution Workflow

## Why This Matters

Bot reviews (CodeRabbit, Copilot) can generate 10-30+ comments across security vulnerabilities, logic bugs, and style issues. Without a structured approach:
- Critical security issues get buried in noise
- Commits become messy and hard to review
- Easy to miss issues or duplicate work
- No clear progress tracking

This workflow ensures systematic resolution with atomic commits and clear documentation.

## Workflow

### Phase 1: Extract, Verify, and Categorize

**1. Extract bot comments:**
```bash
# Get reviews from bot accounts
gh api repos/<owner>/<repo>/pulls/<pr>/reviews \
  --jq '.[] | select(.user.login | test("coderabbit|copilot|bot"; "i")) | {user: .user.login, state: .state, body: .body}'

# Get individual review comments
gh api repos/<owner>/<repo>/pulls/<pr>/comments \
  --jq '.[] | select(.user.login | test("coderabbit|copilot|bot"; "i")) | {file: .path, line: .line, body: .body}'
```

**2. Verify findings before implementation (CRITICAL):**

> **Rule: Bot feedback ≠ verified defect.** Automated reviewers (CodeRabbit, Copilot) frequently produce false positives, misunderstand architectural intent, or hallucinate non-existent issues.
> - **VERIFIED**: Confirmed genuine defect or risk against code reality → schedule in WorkOrder.
> - **DISMISSED**: False positive, invalid assumption, or harmful rewrite → document dismissal rationale.
> - **QUESTION**: Ambiguous intent → pause and ask the human author.

**3. Categorize verified issues by severity:**

| Priority | Category | Examples | Why First |
|----------|----------|----------|-----------|
| CRITICAL | Security | Command injection, path traversal, XSS, secrets | Blockers for merge |
| HIGH | Logic | Race conditions, null checks, incorrect logic | Affects behavior |
| MEDIUM | Docs | MD lint, outdated examples, confusing docs | Non-blocking |
| LOW | Style | Formatting, naming conventions | Cosmetic only |

### Phase 2: Create WorkOrders

Group related issues into WorkOrders by category. Each WO becomes one atomic commit.

```
WO-001: Security (CRITICAL) - 3 issues
  - cmd-injection in shell.ts
  - path-traversal in file-utils.ts
  - hardcoded secret in config.ts

WO-002: Logic (HIGH) - 4 issues
  - race condition in async-handler.ts
  - missing null check in parser.ts
  - incorrect drift detection in status.ts
  - missing snapshot validation

WO-003: Docs (MEDIUM) - 5 issues
  - MD040 linting in README
  - outdated auth example
  - confusing CLI table
```

### Phase 3: Execute WorkOrders

**Execution order matters:** Security → Logic → Docs → Style

For each WO:
1. Fix all issues in that category
2. Run tests locally
3. Commit atomically
4. Verify CI passes before next WO

```bash
# One commit per WO - this enables easy revert if needed
git add <specific-files-for-wo-001>
git commit -m "fix(security): prevent command injection and path traversal

- Escape shell arguments in shell.ts
- Validate paths in file-utils.ts
- Move secret to env in config.ts"

# After security is committed, move to logic
git add <specific-files-for-wo-002>
git commit -m "fix(logic): race conditions and null checks"
```

**Why atomic commits per WO:**
- Easy to revert if a category introduces bugs
- Clear git history for reviewers
- Each commit is a logical unit
- Bisect-friendly if issues arise later

### Phase 4: Validate Locally

```bash
# Run project-specific test/lint validation before pushing (e.g. npm/bun test, pytest, cargo test)
npm test && npm run lint

# Fix any formatting issues (e.g. prettier, ruff, biome)
npx prettier --write <modified-files>
```

### Phase 5: Proposal & Document Resolution (Gated Push)

Prepare the checklist table for operator review. **Do not push or comment automatically.** Present the result and ask for human confirmation before publishing.

```bash
# Preview commits and status
git status
git log -n <N> --oneline

# Generate checklist markdown proposal:
cat <<'EOF'
## Review Feedback Resolution

| # | File | Issue | Priority | Status | Commit / Rationale |
|---|------|-------|----------|--------|---------------------|
| 1 | shell.ts | Command injection | CRITICAL | Fixed | abc1234 |
| 2 | file-utils.ts | Path traversal | CRITICAL | Fixed | abc1234 |
| 3 | parser.ts | Supposed race condition | HIGH | Dismissed | False positive: single-threaded runtime |
| ... | ... | ... | ... | ... | ... |

All issues resolved or dismissed with rationale.
EOF

# Upon explicit human approval only:
# git push origin <branch>
# gh pr comment <pr> --body "<checklist>"
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Blindly trusting bot comments | Verify against code reality first; dismiss hallucinations |
| Mixing categories in one commit | One commit per WO category |
| Skipping local tests | Always run local tests before commit |
| Pushing without human gate | Always present local validation to operator before `git push` |
| Forgetting to format | Run linter/formatter before push |
| Not documenting dismissal | Record explicit technical rationale for dismissed findings |

## Example: Full Workflow

PR #22 received 13 comments (12 CodeRabbit + 1 Copilot):

```bash
# 1. Extract
gh api repos/owner/repo/pulls/22/comments --jq '.[] | select(.user.login | contains("coderabbit"))'

# 2. Verify against codebase & create plan
#    WO-001: Security (3 issues verified)
#    WO-002: Logic (3 verified, 1 dismissed as false positive)
#    WO-003: Docs (5 issues verified)
#    WO-004: CI fixes (1 issue verified)

# 3. Execute with atomic commits
git commit -m "fix(security): ..."
git commit -m "fix(logic): ..."
git commit -m "fix(docs): ..."
git commit -m "fix(ci): formatting and linter config"

# 4. Validate
npm test && npm run lint

# 5. Hand off to human operator for review & push approval
git status
git log -n 4 --oneline
# Operator confirms -> push & post resolution comment
```

## Quality Checklist

Before marking complete:
- [ ] All CRITICAL issues addressed first
- [ ] Each WO has its own atomic commit
- [ ] Tests pass after each WO
- [ ] CI passes before merge
- [ ] Checklist comment posted on PR

## Learned From

| Attribute | Value |
|-----------|-------|
| Session | 2026-02-27 |
| PR | #22 branch-review |
| Bots | CodeRabbit (12), Copilot (1) |
| Issues | 13 resolved |
| Commits | 7 atomic |
