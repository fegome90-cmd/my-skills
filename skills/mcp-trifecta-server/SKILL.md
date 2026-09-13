---
name: mcp-trifecta-server
description: "Use when creating or running a custom Trifecta MCP server that exposes context-pack search, ctx get, or PCC operations over Model Context Protocol."
homepage: https://github.com/modelcontextprotocol/specification
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "0.1.0"
---

# Trifecta MCP Server

## Overview

Custom MCP server for Trifecta Programming Context Calling (PCC) operations. Exposes Context Pack search and retrieval via Model Context Protocol (JSON-RPC 2.0 over stdio).

**Architecture:**
- **Mock Mode** (default): Demo service with sample data
- **Real Mode** (opt-in): Uses Trifecta Python API via uv runner (requires `TRIFECTA_DOPE_DIR`)

**Exposes:**
- `ctx_search` - Search Context Pack for relevant chunks
- `ctx_get` - Retrieve specific chunks by ID with progressive disclosure

## Requirements

### Required Tools

1. **Python 3.8+** - For MCP server
   ```bash
   python3 --version  # Must be 3.8+
   ```

2. **Trifecta Source** (Real Mode only)
   ```bash
   export TRIFECTA_DOPE_DIR="${TRIFECTA_DOPE_DIR:-$HOME/Developer/agent_h/trifecta_dope}"
   ```

3. **Built Context Pack** (Real Mode only)
   ```bash
   cd ~/Developer/examen_grado
   trifecta ctx build --segment .
   ```

**⚠️ IMPORTANT:** Real Mode requires executable `trifecta` command with appropriate permissions.

## Installation

### Step 1: Verify Prerequisites

```bash
# Check Python version
python3 --version  # Must be 3.8+

# Check Trifecta CLI (for real mode only)
cd ~/Developer/agent_h/trifecta_dope
uv sync

# Check Context Pack (for real mode only)
cd ~/Developer/examen_grado
ls -la _ctx/context_pack.json
```

### Step 2: Start MCP Server

```bash
# Mock mode (default)
cd ~/Developer/examen_grado/mcp-servers/trifecta
MCP_TRIFECTA_MODE=mock python3 server.py

# Real mode (requires TRIFECTA_DOPE_DIR)
export TRIFECTA_DOPE_DIR="${TRIFECTA_DOPE_DIR:-$HOME/Developer/agent_h/trifecta_dope}"
cd ~/Developer/examen_grado/mcp-servers/trifecta
python3 server.py
```

**Expected output:** Server starts and waits for JSON-RPC requests on stdin.

## MCP Tools

### ctx_search

Search Context Pack for relevant chunks.

```json
{
  "query": "string (required, 3-500 chars)",
  "k": "integer (optional, 1-100, default 5)",
  "filters": "object (optional, only 'segment' allowed in real mode)",
  "segment": "string (optional, defaults to cwd)"
}
```

**Response (Mock Mode):**
```json
{
  "query": "telemetry",
  "k": 5,
  "hits": [
    {
      "id": "demo:abc123",
      "score": 1.0,
      "title_path": ["demo", "overview"],
      "preview": "Demo chunk for query: telemetry"
    }
  ],
  "total": 1
}
```

**Response (Real Mode):**
```json
{
  "query": "telemetry",
  "k": 5,
  "hits": [
    {
      "id": "prime:a1b2c3",
      "score": 1.5,
      "title_path": ["telemetry", "overview"],
      "preview": "El sistema de telemetría T8..."
    }
  ],
  "total": 5
}
```

### ctx_get

Retrieve specific chunks from Context Pack.

```json
{
  "ids": ["string[] (required, 1-50 items)"],
  "mode": "string (optional, enum: raw|excerpt|skeleton, default excerpt)",
  "segment": "string (optional, defaults to cwd)"
}
```

**Response (Mock Mode):**
```json
{
  "ids": ["demo:abc123"],
  "mode": "excerpt",
  "chunks": [
    {
      "id": "demo:abc123",
      "doc": "prime",
      "title_path": ["demo", "overview"],
      "text": "Demo chunk content for testing. Mock implementation for demonstration purposes.",
      "char_count": 100,
      "token_est": 25
    }
  ],
  "total_tokens": 25
}
```

**Response (Real Mode):**
```json
{
  "ids": ["prime:a1b2c3"],
  "mode": "excerpt",
  "chunks": [
    {
      "id": "prime:a1b2c3",
      "doc": "prime",
      "title_path": ["telemetry", "overview"],
      "text": "El sistema de telemetría T8 proporciona observabilidad integrada...",
      "char_count": 1234,
      "token_est": 308
    }
  ],
  "total_tokens": 308,
  "stop_reason": "complete",
  "chunks_returned": 1,
  "chars_returned_total": 250
}
```

## Architecture

### Dual Mode System

**Mock Mode (Default):**
- ✅ No external dependencies
- ✅ Works immediately without Trifecta CLI
- ✅ Sample data for testing
- ✅ Ideal for development and MCP client validation

**Real Mode (Opt-in):**
- ⚠️ Requires Trifecta CLI
- ⚠️ Requires Context Pack (`_ctx/context_pack.json`)
- ⚠️ Uses Trifecta CLI as SSOT (via imports)
- ✅ Access to real Trifecta Context Packs
- ✅ Production-ready

### Mode Selection

**Via command-line args:**
```bash
# Mock mode (default)
python3 server.py

# Real mode
python3 server.py --mode=real

# Real mode with custom segment
python3 server.py --mode=real --segment ~/Developer/examen_grado
```

**Via environment variable:**
```bash
# Mock mode
export MCP_TRIFECTA_MODE=mock

# Real mode
export MCP_TRIFECTA_MODE=real

# Then run server
python3 server.py
```

**Priority:** Command-line args override environment variable.

## Security & Hardening

### Input Validation

- Query length: 3-500 characters
- k range: 1-100 results
- IDs count: 1-50 chunks
- Mode validation: raw, excerpt, skeleton only

### PII Sanitization

The server automatically sanitizes output content:

- Email addresses: `user@example.com` → `***@***.***`
- API keys: `api_key: abc123` → `***REDACTED***`
- Secrets: `secret: xyz` → `***REDACTED***`

### Error Handling

All errors are explicit with JSON-RPC error codes:

- `-32700`: Invalid JSON
- `-32601`: Unknown method/tool
- `-32602`: Invalid params (validation error)
- `-32603`: Internal server error

**No silent failures** - all errors return explicit messages.

### Path Validation

- All paths resolved relative to segment root
- No arbitrary file access
- Path traversal protection enabled

## Troubleshooting

### Server fails to start

**Error:** `Failed to import Trifecta modules: No module named 'src'`

**Solution:** Use Mock mode (default) or ensure Trifecta CLI path is correct:
```bash
# Use mock mode (works without Trifecta)
python3 server.py

# Ensure Trifecta is installed
cd ~/Developer/agent_h/trifecta_dope
uv sync
```

**Error:** `Context Pack not found: _ctx/context_pack.json`

**Solution:** Build Context Pack first (Real Mode only):
```bash
cd ~/Developer/examen_grado
trifecta ctx build --segment .
```

### Validation errors

**Error:** `Query must be at least 3 characters`

**Solution:** Provide longer query string.

**Error:** `k too large (max 100)`

**Solution:** Reduce k parameter to ≤ 100.

### Mode selection issues

**Error:** `WARNING: Could not import Trifecta modules: ImportError...`
`WARNING: Falling back to MOCK ContextService (mode: mock)`

**Solution:** This is expected behavior when Trifecta CLI is not available. Server will use Mock mode.

### MCP client connection issues

**Error:** `Connection refused` or `timeout`

**Solution:**
- Verify server is running
- Check stdio/stderr are properly connected
- Ensure no firewall blocking

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|----------|
| `MCP_TRIFECTA_MODE` | Mode selection (mock|real) | `mock` |
| `TRIFECTA_DOPE_DIR` | Path to Trifecta source (real mode only) | None |

**Note:** Real mode requires `TRIFECTA_DOPE_DIR` to be set.

**Example:**
```bash
export TRIFECTA_DOPE_DIR="${TRIFECTA_DOPE_DIR:-$HOME/Developer/agent_h/trifecta_dope}"
```

## Development

### Testing Server

```bash
cd ~/Developer/examen_grado/mcp-servers/trifecta

# Full smoke test (mock + real)
python3 scripts/smoke_mcp_full.py

# Runner-only smoke test
bash scripts/smoke_real_runner.sh

# Manual tests (Mock mode)
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python3 server.py

# Manual tests (Real mode - requires TRIFECTA_DOPE_DIR)
export TRIFECTA_DOPE_DIR="${TRIFECTA_DOPE_DIR:-$HOME/Developer/agent_h/trifecta_dope}"
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"ctx_search","arguments":{"query":"telemetry"}}}' | python3 server.py
```

### Adding New Tools

To add a new MCP tool:

1. Add handler method: `def _new_tool_handler(self, arguments):`
2. Register in `handle_tools_call()`: `elif name == "new_tool":`
3. Add schema in `handle_tools_list()`
4. Add validation if needed

Example:
```python
def _new_tool_handler(self, arguments):
    """Handle new_tool tool."""
    # ... implementation ...
    return {"result": "data"}

# In handle_tools_call:
elif name == "new_tool":
    result = self._new_tool_handler(arguments)

# In handle_tools_list:
{
  "name": "new_tool",
  "description": "Description of new tool",
  "inputSchema": {
    "type": "object",
    "properties": {...},
    "required": [...]
  }
}
```

## MCP Protocol Compliance

This server implements **Model Context Protocol (MCP) 2024-11-05**:

- ✅ JSON-RPC 2.0 over stdio
- ✅ `initialize` handshake
- ✅ `tools/list` with schema
- ✅ `tools/call` with validation
- ✅ Explicit error codes
- ✅ Content array in responses
- ✅ PII sanitization
- ✅ Mock mode for fallback

## Resources

- **MCP Documentation:** `docs/research/mcp/MCP-PROTOCOL-CHEATSHEET-2026-03.md`
- **MCP Security:** `docs/research/mcp/MCP-SECURITY-PLAYBOOK-2026-03.md`
- **MCP Integration:** `docs/research/mcp/MCP-CLIENT-INTEGRATION-MATRIX-2026-03.md`
- **Trifecta Research:** `docs/research/trifecta/`

## License

Same as Trifecta (see `agent_h/trifecta_dope/LICENSE`).

## Version

- **Version:** 0.1.0
- **Protocol:** 2024-11-05
- **Python:** 3.8+
- **Author:** PicoClaw 🦞
