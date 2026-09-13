---
name: herdr-worktrunk
description: "Trigger: worktrunk, herdr worktree, isolated worktree, wt switch, worktree hooks. Manage isolated git worktrees through herdr worktree commands and the worktrunk plugin with lifecycle hooks."
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0"
---

## Activation Contract

Use when the user explicitly asks for isolated worktree work via herdr: create, switch, list, merge, or remove git worktrees, or run worktrunk lifecycle hooks. The `herdr` skill owns panes and agents; this skill owns worktree topology. Do not activate merely because parallel work is possible.

## Hard Rules

- Prefer `herdr worktree` for plain open-as-tab workspaces; prefer `wt` when setup/teardown hooks must run.
- Never remove a worktree with uncommitted changes without explicit user approval; check `wt list` status first.
- Parse branch and path from JSON output; never invent worktree paths.
- A branch argument already selects its worktree; do not layer `-C <path>` on top of it (`-C` fixes repo lookup, never worktree selection).
- When `wt` blocks on hook approval in a non-interactive session, stop and escalate to the user; never pass `--yes` on their behalf.
- Keep writes single-threaded per worktree unless isolated branches are explicitly approved.

## Decision Gates

| Situation | Action |
| --- | --- |
| Setup/teardown hooks needed (deps, `.env`) | Use `wt` via the worktrunk plugin, not native commands |
| Open an existing worktree as a tab | `herdr worktree open --path <path>` |
| Finish and integrate work | `wt merge` from the worktree, then remove it |
| Native vs hooks unclear | Ask which one before acting |
| Editing `~/.config/worktrunk/config.toml` | Propose first, preserve structure; never install tools unasked |
| Editing `<repo>/.config/wt.toml` | Edit proactively (versioned); warn before destructive or network-piped commands |

## Execution Steps

1. Inspect state: `herdr worktree list` or `wt list`.
2. Create or switch: `herdr worktree create --branch <name> --base <ref>` or `wt switch <name>`.
3. Work inside the returned worktree path; commit there, never in the main checkout.
4. Merge with `wt merge`; remove with `herdr worktree remove` (`--force` only with approval).
5. Verify with `wt list` that the worktree is gone and the branch state is as expected.

## Output Contract

Return: worktree path and branch created, switched, merged, or removed; hook results when `wt` ran; `wt list` verification; residual risks such as unmerged branches.

## References

- `references/worktrunk-plugin.md` — plugin actions, lifecycle hooks, and template variables.
