# Worktrunk Plugin Reference

Source: `devashish2203/herdr-worktrunk` (installed, enabled in `~/.config/herdr/plugins.json`). Wires the `wt` CLI into herdr instead of reimplementing hooks.

## Native vs plugin

- `herdr worktree create/open/remove/list` — built-in, no hook system.
- `wt` via the plugin — hook-driven: setup on create (install deps, copy `.env`, bootstrap services), teardown on remove. Template variables: `{{ branch }}`, `{{ worktree_path }}`.

## Workspace actions (fzf picker)

- Switch / create from default branch: `Enter` switches, typing a new name creates it from the default base. `Alt+Enter` forces the typed name when it fuzzy-matches an existing branch.
- Switch / create from current branch: same picker, new names branch off the current branch.
- Merge, remove, PR shortcuts, live preview, remote-branch inclusion are picker options.

## Open modes

The resulting worktree opens either as a herdr tab or as a native linked-worktree workspace. Confirm the mode with the user when it matters.

## `wt` essentials

- `wt switch <name>` — switch, creating from the default base when missing.
- `wt list` — worktrees and status (source of truth before removal).
- `wt remove` — removes the worktree; deletes the branch only when merged.
- `wt merge` — merges the current branch into the target branch.
- `wt hook`, `wt step`, `wt config` — run or manage individual hooks and configs.

## Hook timing (which hook for what)

- Deps and env files a later step needs → `pre-start` (blocks creation)
- Dev servers, long builds, cache copies → `post-start` (background)
- Formatters, linters, type checks → `pre-commit`
- Tests gating a merge → `pre-merge`
- Cleanup (save artifacts, stop servers) → `pre-remove` / `post-remove`

Derive hook commands from the project itself (`package.json` scripts, `Cargo.toml`) and verify they run before adding them. Test with `wt switch --create test-hooks`.

## `-C` gotcha

`wt step diff --branch beta` from inside another worktree of the same repo already selects beta. Adding `-C ../repo.beta` names it twice and adds nothing. Reach for `-C` only when the repository lookup itself is wrong.

## Provenance

Condensed from upstream `max-sixty/worktrunk` skill (`plugins/worktrunk/skills/worktrunk/SKILL.md`, dual MIT/Apache-2.0): branch-selection rules, hook timing, approval escalation, and config scopes. Agent-handoff patterns (tmux/zellij) and `llm-commits` setup intentionally not carried over — multiplexing belongs to the `herdr` skill.
