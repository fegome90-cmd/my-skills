# MCP Tools Reference

Source: `~/Developer/tmux_fork/src/interfaces/mcp/tools/memory.py` + `messaging.py`
Canonical transport: stdio (auto-detect project from CWD)

## Memory Tools (17)

### Observation CRUD

| Tool | Description | Key Params |
|------|-------------|------------|
| `memory_save` | Save observation | `content`, `type`, `project`, `topic_key`, `title`, `metadata` |
| `memory_search` | FTS5 full-text search | `query`, `limit`, `project`, `max_tokens` |
| `memory_retrieve` | Enhanced multi-signal retrieval | `query`, `limit`, `project`, `type`, `max_tokens` |
| `memory_get` | Get by ID | `id`, `max_tokens` |
| `memory_list` | List recent observations | `limit`, `offset`, `type`, `project`, `max_tokens` |
| `memory_update` | Update existing observation | `id`, `content`, `type`, `project`, `topic_key`, `metadata`, `title` |
| `memory_delete` | Delete by ID | `id`, `project` (ownership check) |

### Context & Stats

| Tool | Description | Key Params |
|------|-------------|------------|
| `memory_context` | Recent session summaries (falls back to all recent) | `limit`, `project`, `max_tokens` |
| `memory_stats` | DB statistics | — |
| `memory_timeline` | Observations in time range | `start` (Unix ms), `end`, `project`, `max_tokens` |

### Sessions

| Tool | Description | Key Params |
|------|-------------|------------|
| `memory_session_start` | Start session (auto-ends previous) | `project`, `directory`, `goal`, `instructions` |
| `memory_session_end` | End active session | `session_id`, `summary` |
| `memory_session_summary` | Save structured session summary | `content`, `project`, `session_id` |

### Utilities

| Tool | Description | Key Params |
|------|-------------|------------|
| `memory_suggest_topic_key` | Suggest stable topic_key for upsert | `title`, `type`, `content` |
| `memory_save_prompt` | Save prompt to dedicated table | `content`, `project`, `session_id`, `role`, `model`, `provider` |
| `memory_capture_passive` | Extract & save Key Learnings from text | `content`, `project`, `session_id`, `source` |
| `memory_merge_projects` | Merge observations/sessions into target project | `from_projects` (comma-separated), `to_project` |

## Messaging Tools (4)

| Tool | Description | Key Params |
|------|-------------|------------|
| `fork_message_send` | Send message to agent | `target` (session:window), `payload`, `from_agent`, `type` |
| `fork_message_receive` | Receive messages for agent | `agent_id`, `limit`, `mark_read` (auto-purge after 5min) |
| `fork_message_broadcast` | Broadcast to all active sessions | `payload`, `from_agent` |
| `fork_message_history` | Message history for agent | `agent_id`, `limit` |

**Message types**: COMMAND, REPLY, HANDOFF, PROGRESS, FILE_TOUCHED, OBSERVATION

## Integration Examples

### Claude Desktop / Cursor
```json
{
  "mcpServers": {
    "fork-memory": {
      "command": "memory",
      "args": ["mcp", "serve"],
      "cwd": "~/Developer/tmux_fork"
    }
  }
}
```

### n8n / HTTP
```json
{
  "mcpServers": {
    "fork-memory": {
      "url": "http://localhost:8765/sse",
      "transport": "sse"
    }
  }
}
```

### OpenClaw (via openclaw.json)
Register as MCP server in gateway config for native tool access.

## Known Issues

- `fork_message_cleanup` is referenced in hybrid dispatch but NOT registered as MCP tool — ghost tool. Use CLI `fork message cleanup` instead.
- SSE/HTTP transports require explicit `project` param (stdio auto-detects from CWD).
