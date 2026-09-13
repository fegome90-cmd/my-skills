# Audit of `disk-cleanup-macos-safe` v1.0.0

## Verdict

**Good intent, unsafe for autonomous execution.** The original skill correctly recognizes irreversible data loss and introduces backup and confirmation, but several checks are technically wrong or too weak. It should remain audit-only until the critical findings are fixed and pressure-tested.

## Critical findings

1. **Linked worktrees can bypass the guard.** The check `[ -d "$path/.git" ]` misses linked worktrees because Git normally stores `.git` as a file there.
2. **The backup path is buggy.** `BACKUP="~/Developer/..."` prevents tilde expansion and may create a literal relative `~` path.
3. **“Remote exists” does not mean recoverable.** A clean status does not detect unpushed branches, local-only commits, stashes, dirty submodules, or local LFS state.
4. **HITL is underspecified.** Choosing “Trash or rm” does not show exact canonical paths, byte estimates, backup proof, command arguments, or blast radius. Approval can be reused after the plan changes.
5. **No path-boundary or race protection.** Empty variables, traversal, symlinks, mount changes, or path replacement between review and execution can redirect deletion.
6. **Docker procedure is overbroad.** `docker stop $(docker ps -q)` can stop unrelated workloads. `system prune -a --volumes -f` removes more than database volumes, while `-f` bypasses Docker’s own prompt.
7. **PostgreSQL verification is inadequate.** `grep CREATE TABLE` does not validate a custom-format dump and is not a restore test.
8. **`/private/tmp` is not globally safe.** It can contain active sockets, locks, worktrees, outputs, or user data. Only exact inactive candidates should be considered.
9. **Trash is not immediate reclamation.** Moving data to Trash on the same volume does not free its blocks until Trash is emptied.
10. **Session anecdotes are encoded as universal rules.** Statements about path naming, automatic Docker.raw compaction, fixed APFS release amounts, and “zero data loss” are not stable safety guarantees.

## High-priority redesign

Adopt a two-phase transaction:

- **Phase A:** read-only inventory and immutable deletion manifest.
- **Phase B:** per-plan approval, precondition revalidation, one-target-at-a-time execution, and postcondition verification.

Approval must bind to exact targets and arguments. Any changed path, inode, size, classification, backup, or command requires new approval. Never use sticky approvals for destructive tools.

## Structural recommendations

- Keep the main `SKILL.md` focused on policy and decision gates.
- Move behavioral tests to `tests/pressure-scenarios.md`.
- Later, encode path validation and manifest generation in a read-only helper script; mechanical safety checks should not depend only on prose.
- Validate frontmatter with `skills-ref validate` before deployment.
- Remove or relocate the single-session evidence section to a case study.

## Status of the attached v2 draft

The draft fixes the documented logic and adds 20 pressure scenarios. It has been statically checked for YAML validity and structure, but it has **not** yet been behaviorally validated with independent agent runs on macOS. Treat it as a deployment candidate, not a proven safety control.
