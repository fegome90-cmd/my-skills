# memory CLI Reference

Canonical backend: `memory-mcp` (21 MCP tools). CLI is fallback/debug only.

## Core Observations

| Command | Description | Example |
|---------|-------------|---------|
| `save` | Save observation | `memory save "Fixed race" --type bugfix --project api` |
| `search` | FTS5 search | `memory search "auth middleware" --limit 10` |
| `retrieve` | Enhanced multi-signal retrieval | `memory retrieve "concurrent writes"` |
| `list` | List recent observations | `memory list --type decision --limit 20` |
| `get <id>` | Get by ID (prefix match) | `memory get abc12345` |
| `update <id>` | Update observation | `memory update abc12345 "New content"` |
| `delete <id>` | Delete observation | `memory delete abc12345` |
| `diff <ref1> <ref2>` | Compare between refs | `memory diff main HEAD` |
| `context` | Recent session summaries | `memory context` |
| `cleanup` | Clean old observations | `memory cleanup` |
| `health` | DB health check | `memory health` |
| `stats` | DB statistics | `memory stats` |
| `query` | Structured event filtering | `memory query --type decision --after 2026-01-01` |

## Project Management

| Command | Description |
|---------|-------------|
| `project merge` | Merge/consolidate projects |

## Sessions

| Command | Description |
|---------|-------------|
| `session start` | Start session (`--project`, `--goal`) |
| `session end` | End active session |
| `session list` | List sessions |

## Compact / Context Recovery

| Command | Description |
|---------|-------------|
| `compact` | Context-window recovery (save-summary, recover) |

## Workflow

| Command | Description |
|---------|-------------|
| `workflow outline` | Create workflow plan |
| `workflow execute` | Execute workflow tasks |
| `workflow verify` | Verify execution |
| `workflow ship` | Ship workflow |
| `workflow status` | Workflow status |

## Workspace (Git Worktree)

| Command | Description |
|---------|-------------|
| `workspace create` | Create workspace |
| `workspace list` | List workspaces |
| `workspace remove` | Remove workspace |
| `workspace detect` | Detect from CWD |
| `workspace enter` | Enter workspace |
| `workspace merge` | Merge workspace branch |
| `workspace config` | Show/edit configuration |

## Launch Lifecycle (10-state FSM)

| Command | Transition |
|---------|-----------|
| `launch request` | → RESERVED |
| `launch confirm-spawning` | RESERVED → SPAWNING |
| `launch confirm-active` | SPAWNING → ACTIVE |
| `launch mark-failed` | → FAILED |
| `launch begin-termination` | ACTIVE → TERMINATING |
| `launch confirm-terminated` | TERMINATING → TERMINATED |
| `launch status` | Query status |
| `launch list-active` | List in-flight |
| `launch summary` | Counts by status |
| `launch list-quarantined` | List quarantined |

## FPEL (Frozen Proposal Evidence Loop)

| Command | Description |
|---------|-------------|
| `fpel freeze` | Create immutable snapshot |
| `fpel check` | Run checks (writes evidence only) |
| `fpel seal` | Validate invariants, create sealed PASS |
| `fpel status` | Authorization status |

## Prompt Management

| Command | Description |
|---------|-------------|
| `prompt save` | Save prompt (auto-indexed FTS) |
| `prompt search` | FTS5 BM25 search |
| `prompt list` | List recent prompts |
| `prompt stats` | Counts by model/provider |

## Export / Sync

| Command | Description |
|---------|-------------|
| `export obsidian` | Export to Obsidian vault |
| `import obsidian` | Import from Obsidian vault |
| `sync export` | Git-based sync |
| `sync import` | Git-based sync |
| `sync status` | Git-based sync |

## MCP Server

| Command | Description |
|---------|-------------|
| `mcp serve` | Start MCP server (stdio) |
| `mcp start` | Start MCP server (background) |
| `mcp stop` | Stop MCP server |
| `mcp status` | MCP server status |

## TUI

| Command | Description |
|---------|-------------|
| `tui` | Interactive observation browser |
