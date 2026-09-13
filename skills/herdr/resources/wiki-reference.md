# Herdr Wiki Reference (OPTIONAL)

> This file is an OPT-IN index. Do NOT read it by default.
> Load it only when you need to clarify a Herdr concept, flag, or behavior
> that the operational SKILL.md does not cover.

## What this is

A persistent LLM Wiki about Herdr lives in the shared vault at
`~/.llm-wiki/wiki/` (topic: `herdr`). It holds synthesized pages plus captured
source material: install flows, the socket API, configuration, keybindings,
agent automation, plugin lists, and comparisons vs tmux/Zellij.

This file tells you how to reach the right page on demand, WITHOUT copying
any of that content into the skill (which would bloat every agent's context).

## How to access (pick one)

### A) pi-llm-wiki extension active (preferred)

Query the vault directly — it returns ranked links or page previews:

- `wiki_recall "herdr socket api"` — semantic recall
- `wiki_search "keybindings"` — registry search
- then `read` the matched page path

### B) Extension NOT active (sub-agents, other harnesses)

The pages are plain Markdown files. Read them directly:

```text
read ~/.llm-wiki/wiki/<category>/<page>.md
```

## Page map (high-value Herdr pages)

Organized as the wiki's own `entities/herdr` index presents them.

### Entry point

- `entities/herdr` — Canonical overview + full page index

### Getting started

- `concepts/install` — Script, Homebrew, mise, Nix, manual
- `syntheses/quick-start-cheat-sheet` — Productive in 5 minutes
- `concepts/concepts` — Session, Workspace, Tab, Pane, Agent, Modes

### Core

- `concepts/keybindings` — Prefix mode, mouse, copy mode, prefix-free
- `concepts/configuration` — config.toml, themes, UI, sound, sidebar
- `concepts/session-state` — Persistence, restore, handoff, agent resume
- `concepts/remote-work` — SSH, thin client, phone workflow

### UI

- `concepts/sidebar` — Agent panel, spaces panel, layout tokens
- `concepts/themes` — Built-in themes, auto-switch, color overrides

### Agent layer

- `concepts/agents` — Detection, state, integrations, rollups
- `concepts/integrations` — Per-agent install (Pi, Claude, Codex, etc.)
- `concepts/agent-automation` — Orchestrate from scripts
- `concepts/agent-skill` — Teach agents to control Herdr
- `concepts/plugins` — Install, author, marketplace
- `syntheses/popular-plugins` — Curated list of 150+ plugins

### API / advanced

- `concepts/socket-api` — Raw JSON protocol
- `concepts/cli-reference` — Full command reference
- `concepts/worktrees` — Git worktree integration

### Comparisons & reference

- `syntheses/compare` — vs tmux, Zellij, Warp, cmux, Solo
- `syntheses/herdr-vs-tmux` — Detailed comparison
- `analyses/troubleshooting` — Common issues

## Recommended query terms

| If you need to clarify... | Query / read |
|---|---|
| a command or flag | `cli-reference` or `socket-api` |
| why a lifecycle state (idle/done/blocked) behaves oddly | `agents` or `agent-automation` |
| a keybinding | `keybindings` |
| config.toml options | `configuration` |
| plugin behavior | `plugins` / `popular-plugins` |
| tmux parity / migration | `herdr-vs-tmux` / `compare` |
| an error | `troubleshooting` |

## Notes

- The wiki is a living artifact and may be enriched over time; the page
  names above are stable handles.
- This pointer is a LOCAL ADDITION to the upstream Herdr skill and does not
  alter its operational contract or the `HERDR_ENV=1` safety guardrail.
