---
name: pi-extension-builder
description: "Use when creating, auditing, or refactoring pi coding agent TypeScript extensions. Covers extension factory functions, pi.registerTool, pi.registerCommand, pi.events event bus, lifecycle hooks (session_start, session_shutdown), ExtensionAPI, ExtensionContext, child_process spawning, JSONL output parsing, and extension testing. Also triggers for pi extension, pi plugin, pi tool registration, pi event handler, pi lifecycle, pi extension debug, pi --mode json. Do NOT use for MCP server development, general TypeScript development, or skill authoring (use template-skill or skill-onboarding)."
search_hints: pi extension registerTool registerCommand pi.events lifecycle session_start session_shutdown ExtensionAPI child_process JSONL tool-guard pi-tasks subagent extension scaffold TypeScript pack footer header provider TUI
metadata:
  triggers:
    - "create pi extension"
    - "pi extension"
    - "pi plugin"
    - "register pi tool"
    - "pi registerTool"
    - "pi registerCommand"
    - "pi events"
    - "pi lifecycle"
    - "pi event bus"
    - "extension scaffold"
    - "pi --mode json"
    - "extension audit"
    - "extension refactor"
    - "pi extension debug"
    - "pi extension pack"
    - "pi footer extension"
    - "pi header extension"
    - "pi provider extension"
  role: specialist
  scope: implementation
version: "2.0.0"
---

# pi Extension Builder

Design, implement, and audit TypeScript extensions for the pi coding agent. 21 verified packs extracted from real production extensions.

## Procedure

### Phase 1: Design — Load API + Select Packs

Load `resources/api-surface.md` for complete API reference.
Load `resources/packs-essential.md` and `resources/packs-core.md` for essential and core packs.

1. Determine extension style from pack table below
2. Map event subscriptions from API reference
3. Design state: init on `session_start`, cleanup on `session_shutdown`
4. Design init order: handlers BEFORE `pi.events.emit`

**Critical**: `session_shutdown` is the ONLY cleanup hook. No `unload` or `session_switch` event.

### Phase 2: Implement — Use Packs + Templates

Load `resources/packs-hooks.md`, `resources/packs-tui.md`, `resources/packs-system.md`, and `resources/packs-advanced.md` for hooks, TUI, system, and advanced packs.
Load `resources/templates.md` for copy-paste skeletons.
Load `resources/advanced-patterns.md` for JSONL parser, context injection, idempotent listeners.

1. Copy the pack skeleton that matches your extension type
2. Fill in domain-specific logic
3. Wire cleanup into `session_shutdown`

### Phase 3: Validate

Load `resources/checklist.md` (60+ items).

1. `npx tsc --noEmit` — type check
2. `/reload` — hot reload test
3. `/new` + `/resume` — lifecycle test
4. Force errors — graceful degradation test

## Pack Index — Organized by Creation Frequency

Every extension needs Pack 1. Most extensions use 2-3 packs combined.

| Need | Pack | Resource | Source |
|------|------|----------|--------|
| **START HERE** — any extension | Pack 1: Minimal Handler | `packs-essential.md` | — |
| Expose a function to the LLM | Pack 2: Tool Registration | `packs-essential.md` | — |
| Add a `/slash` command | Pack 3: Command Registration | `packs-essential.md` | — |
| Add a custom model provider | Pack 4: Provider | `packs-essential.md` | `openrouter.ts` |
| Block or audit LLM tool calls | Pack 5: Tool Guard | `packs-essential.md` | `tool-guard.ts` |
| Proxy tools to MCP server | Pack 6: MCP Bridge | `packs-core.md` | `n8n-mcp-bridge.ts` |
| Side effects per agent turn | Pack 7: Turn Hook | `packs-core.md` | `git-guard.ts` |
| React to first user message | Pack 8: Session Name | `packs-hooks.md` | `auto-session-name.ts` |
| Periodic background check | Pack 9: Periodic Check | `packs-hooks.md` | `auto-update.ts` |
| Talk to other extensions | Pack 10: Inter-Extension RPC | `packs-hooks.md` | `pi-tasks` pattern |
| Custom footer status bar | Pack 11: Footer | `packs-tui.md` | `custom-footer.ts` |
| Custom header display | Pack 12: Header | `packs-tui.md` | `compact-header.ts` |
| Session management + events | Pack 13: Session Hub | `packs-tui.md` | `context-session-hub.ts` |
| Persist across compaction | Pack 14: Compaction Hook | `packs-tui.md` | `00-compact-memory-bridge.ts` |
| Extension > 300 lines | Pack 15: Multi-File Package | `packs-system.md` | `subagent-statusline/` |
| Inject context into turns | Pack 16: System Prompt Injection | `packs-system.md` | `context-loader.ts` |
| Temporary UI panel | Pack 17: TUI Widget | `packs-system.md` | `n8n-mcp-helper.ts` |
| Spawn headless pi processes | Pack 18: Process Manager | `packs-system.md` | `pi-tasks` pattern |
| Inject guard rails into system prompt | Pack 19: Prompt Guard | `packs-advanced.md` | `execution-intent-guard.ts` |
| Load files with mtime caching | Pack 20: Context Loader | `packs-advanced.md` | `01-context-loader.ts` |
| Anti-flicker TUI widgets | Pack 21: Anti-Flicker Widget | `packs-advanced.md` | `subagent-statusline/index.ts` |

## Key Distinctions

| Confuse | With | Rule |
|---------|------|------|
| `pi.on()` | `pi.events.on()` | `pi.on` = pi lifecycle. `pi.events.on` = inter-extension bus |
| `session_shutdown` | `session_switch` | `session_switch` does NOT exist |
| `ExtensionAPI` | `ExtensionContext` | API = static methods. Context = per-call state (ui, cwd) |
| Tool `execute` return | Command `handler` return | Tool → `{ content, details }`. Command → void |
| `pi.exec()` | `child_process.spawn()` | `pi.exec` = pi built-in. `spawn` = Node.js built-in |
| `--mode json` | `--mode json -p` | `-p` reads from stdin. Without `-p`, interactive |
| `{ block: true }` | `event.block()` | Return `{ block: true, reason }` from `tool_call`. No `.block()` method |

## Resources

| Resource | Lines | Phase | Content |
|----------|-------|-------|---------|
| `api-surface.md` | ~230 | 1: Design | Full API reference (registerTool, registerCommand, pi.on, ctx) |
| `packs-essential.md` | ~244 | 1: Design | Packs 1-5: Minimal, Tool, Command, Provider, Tool Guard |
| `packs-core.md` | ~166 | 1: Design | Packs 6-7: MCP Bridge, Turn Hook |
| `packs-hooks.md` | ~181 | 2: Implement | Packs 8-10: Session Name, Periodic Check, RPC |
| `packs-tui.md` | ~246 | 2: Implement | Packs 11-14: Footer, Header, Session Hub, Compaction |
| `packs-system.md` | ~239 | 2: Implement | Packs 15-18: Multi-File, Prompt Injection, Widget, Process Manager |
| `packs-advanced.md` | ~211 | 2: Implement | Packs 19-21: Prompt Guard, File Cache, Anti-Flicker Widget |
| `templates.md` | ~160 | 2: Implement | Copy-paste skeletons |
| `advanced-patterns.md` | ~245 | 2: Implement | JSONL parser, context injection, idempotent listeners |
| `checklist.md` | ~105 | 3: Validate | 60+ validation items |
