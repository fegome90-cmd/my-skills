#!/usr/bin/env python3
"""
Trifecta MCP Server (stdio) - v0.1.0 - JSON-RPC 2.0
- tools/list, tools/call - Tools: ctx_search, ctx_get
- Security: strict validation, output caps, timeouts, redact secrets/PII, logs to stderr only
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

# Configuration constants
MAX_QUERY_LEN = 500
MIN_QUERY_LEN = 3
MAX_K = 100
MIN_K = 1
DEFAULT_K = 5
MAX_IDS = 50
MAX_ID_LEN = 256
SUBPROCESS_TIMEOUT_S = 20
MAX_STDOUT_CHARS = 200_000
MAX_STDERR_CHARS = 20_000

# Environment variable for Trifecta CLI command
# Examples: TRIFECTA_CMD="trifecta"
# Examples: TRIFECTA_CMD="uv run trifecta"
TRIFECTA_CMD_ENV = "TRIFECTA_CMD"


# Redaction patterns (basic but useful)
_RE_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_RE_OPENAI_KEY = re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")
_RE_GITHUB_TOKEN = re.compile(r"\bghp_[A-Za-z0-9]{30,}\b|\bgithub_pat_[A-Za-z0-9_]{20,}\b")
_RE_AWS_ACCESS = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
_RE_PRIVATE_KEY = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
_RE_GENERIC_SECRET = re.compile(r"\b(?:api[_-]?key|token|secret|passwd|password)\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{8,}['\"]?", re.IGNORECASE)


def log(msg: str, **kwargs) -> None:
    """Log message to stderr only."""
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    safe = msg.replace("\n", "\\n")

    extra_fields = []
    for key, value in kwargs.items():
        if value is not None:
            if isinstance(value, str):
                value = value.replace("\n", "\\n")[:200]  # Truncate for logs
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        safe = f"{safe} {' '.join(extra_fields)}"

    sys.stderr.write(f"[trifecta-mcp-server] {ts} {safe}\n")
    sys.stderr.flush()


def redact_text(s: str) -> str:
    """Redact sensitive patterns from text."""
    if not s:
        return s

    s = _RE_PRIVATE_KEY.sub("[REDACTED_PRIVATE_KEY]", s)
    s = _RE_OPENAI_KEY.sub("[REDACTED_OPENAI_KEY]", s)
    s = _RE_GITHUB_TOKEN.sub("[REDACTED_GITHUB_TOKEN]", s)
    s = _RE_AWS_ACCESS.sub("[REDACTED_AWS_ACCESS_KEY]", s)
    s = _RE_EMAIL.sub("[REDACTED_EMAIL]", s)
    s = _RE_GENERIC_SECRET.sub("[REDACTED_SECRET_KV]", s)

    return s


def cap_text(s: str, limit: int) -> Tuple[str, bool]:
    """Cap text at limit and return truncation status."""
    if len(s) <= limit:
        return s, False
    return s[:limit] + "\n[TRUNCATED]", True


# JSON-RPC helpers
def jsonrpc_error(_id: JsonRpcId, code: int, message: str, data: Optional[JSON] = None) -> JSON:
    """Create JSON-RPC error response."""
    err: JSON = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    return {"jsonrpc": "2.0", "id": _id, "error": err}


def jsonrpc_result(_id: JsonRpcId, result: JSON) -> JSON:
    """Create JSON-RPC result response."""
    return {"jsonrpc": "2.0", "id": _id, "result": result}


def is_valid_id(v: Any) -> bool:
    """Check if value is a valid JSON-RPC ID."""
    return v is None or isinstance(v, (str, int))


def ensure_object(v: Any) -> Dict[str, Any]:
    """Ensure value is a JSON object."""
    if not isinstance(v, dict):
        raise ValueError("Expected object")
    return v


# Type aliases
JSON = Dict[str, Any]
JsonRpcId = Union[str, int, None]


# Trifecta CLI Adapter (SSOT)
@dataclass
class TrifectaCliAdapter:
    """Adapter to call Trifecta CLI as subprocess SSOT."""
    cmd: List[str]

    @staticmethod
    def from_env() -> "TrifectaCliAdapter":
        """Create adapter from TRIFECTA_CMD environment variable."""
        raw = os.environ.get(TRIFECTA_CMD_ENV, "").strip()

        if raw:
            # Naive split (good enough if user keeps it simple)
            parts = raw.split()
        else:
            parts = ["trifecta"]

        return TrifectaCliAdapter(cmd=parts)

    def _run_json(self, args: List[str], stdin_text: Optional[str] = None) -> Any:
        """Run Trifecta CLI command and parse JSON output."""
        import shlex

        full_cmd = self.cmd + args
        cmd_str = " ".join(shlex.quote(arg) for arg in full_cmd)

        log(f"CLI run: {cmd_str[:100]}{' ...' if len(cmd_str) > 100 else ''}")

        try:
            proc = subprocess.run(
                full_cmd,
                input=stdin_text,
                text=True,
                capture_output=True,
                timeout=SUBPROCESS_TIMEOUT_S,
                check=False,
            )
        except FileNotFoundError:
            raise RuntimeError(f"Trifecta command not found. Set {TRIFECTA_CMD_ENV} (e.g. 'uv run trifecta').")
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Trifecta CLI timed out after {SUBPROCESS_TIMEOUT_S}s.")

        stdout = proc.stdout or ""
        stderr = proc.stderr or ""

        stdout = redact_text(stdout)
        stderr = redact_text(stderr)

        stdout, _ = cap_text(stdout, MAX_STDOUT_CHARS)
        stderr, _ = cap_text(stderr, MAX_STDERR_CHARS)

        if proc.returncode != 0:
            raise RuntimeError(f"Trifecta CLI error (rc={proc.returncode}). stderr={stderr.strip()[:500]}")

        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            raise RuntimeError("Trifecta CLI did not return valid JSON. Ensure '--json' is supported and enabled.")

    def ctx_search(self, query: str, k: int, filters: Optional[Dict[str, Any]] = None) -> Any:
        """Execute ctx_search via Trifecta CLI."""
        # NOTE: Adjust args to your real Trifecta CLI
        # This assumes: trifecta ctx search --json --k {k} --query {query}
        args = ["ctx", "search", "--json", "--k", str(k), "--query", query]

        # Filters allowlist (example)
        if filters:
            # Only allow 'segment' as demo; extend carefully if needed
            if "segment" in filters:
                args += ["--segment", str(filters["segment"])]
            unknown = set(filters.keys()) - {"segment"}
            if unknown:
                raise ValueError(f"Unknown filters: {sorted(list(unknown))}")

        return self._run_json(args)

    def ctx_get(self, ids: List[str], mode: str) -> Any:
        """Execute ctx_get via Trifecta CLI."""
        # NOTE: Adjust args to your real Trifecta CLI
        # This assumes: trifecta ctx get --json --mode {mode} --id {id1} --id {id2} ...
        args = ["ctx", "get", "--json", "--mode", mode]

        for _id in ids:
            args += ["--id", _id]

        return self._run_json(args)


# Mock Context Service for fallback
class MockContextService:
    """Mock ContextService for demo/testing."""

    def __init__(self, root: Optional[Path] = None):
        self._pack = {
            "schema_version": 1,
            "segment": "demo",
            "digest": "Demo Context Pack for testing",
            "chunks": [
                {
                    "id": "demo:abc123",
                    "doc": "prime",
                    "title_path": ["demo", "overview"],
                    "text": "Demo chunk content for testing. This is a mock implementation.",
                    "char_count": 100,
                    "token_est": 25,
                    "source_path": "_ctx/prime_demo.md"
                },
                {
                    "id": "demo:def456",
                    "doc": "skill",
                    "title_path": ["demo", "rules"],
                    "text": "Demo skill content for testing. Mock implementation for demonstration purposes.",
                    "char_count": 150,
                    "token_est": 38,
                    "source_path": "_ctx/skill_demo.md"
                }
            ]
        }

    def search(self, query: str, k: int, filters=None):
        """Mock search."""
        from dataclasses import dataclass

        @dataclass
        class SearchHit:
            id: str
            score: float
            title_path: List[str]
            preview: str

        @dataclass
        class SearchResult:
            hits: List[SearchHit]

        return SearchResult(
            hits=[
                SearchHit(
                    id="demo:abc123",
                    score=1.0,
                    title_path=["demo", "overview"],
                    preview=f"Demo chunk for query: {query}"
                )
            ]
        )

    def get(self, ids, mode):
        """Mock get."""
        from dataclasses import dataclass

        @dataclass
        class Chunk:
            id: str
            doc: str
            title_path: List[str]
            text: str
            char_count: int
            token_est: int
            source_path: str

        @dataclass
        class GetResult:
            chunks: List[Chunk]
            total_tokens: int
            stop_reason: str
            chunks_returned: int
            chars_returned_total: int

        chunks = []
        for chunk_id in ids:
            for chunk in self._pack["chunks"]:
                if chunk["id"] == chunk_id:
                    chunks.append(Chunk(**chunk))
                    break

        return GetResult(
            chunks=chunks,
            total_tokens=sum(c["token_est"] for c in chunks),
            stop_reason="complete",
            chunks_returned=len(chunks),
            chars_returned_total=sum(c["char_count"] for c in chunks)
        )


# Tool specs
def tool_specs() -> List[JSON]:
    """Return list of available MCP tools."""
    return [
        {
            "name": "ctx_search",
            "description": "Search Trifecta Context Packs for relevant chunks.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "minLength": MIN_QUERY_LEN,
                        "maxLength": MAX_QUERY_LEN
                    },
                    "k": {
                        "type": "integer",
                        "minimum": MIN_K,
                        "maximum": MAX_K,
                        "default": DEFAULT_K
                    },
                    "filters": {
                        "type": "object",
                        "additionalProperties": True
                    },
                    "segment": {
                        "type": "string",
                        "description": "Segment path (optional, defaults to cwd)"
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        },
        {
            "name": "ctx_get",
            "description": "Retrieve chunks by ID with progressive disclosure modes.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ids": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "maxLength": MAX_ID_LEN
                        },
                        "minItems": 1,
                        "maxItems": MAX_IDS
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["raw", "excerpt", "skeleton"],
                        "default": "excerpt"
                    },
                    "segment": {
                        "type": "string",
                        "description": "Segment path (optional, defaults to cwd)"
                    }
                },
                "required": ["ids"],
                "additionalProperties": False
            }
        }
    ]


# Validation functions
def validate_ctx_search(args: Dict[str, Any]) -> Tuple[str, int, Optional[Dict[str, Any]]]:
    """Validate ctx_search arguments."""
    query = args.get("query", "")
    if not isinstance(query, str):
        raise ValueError("query must be a string")

    query = query.strip()
    if len(query) < MIN_QUERY_LEN:
        raise ValueError(f"query must be at least {MIN_QUERY_LEN} chars")
    if len(query) > MAX_QUERY_LEN:
        raise ValueError(f"query must be <= {MAX_QUERY_LEN} chars")

    k = args.get("k", DEFAULT_K)
    if isinstance(k, bool) or not isinstance(k, int):
        raise ValueError("k must be an integer")
    if not (MIN_K <= k <= MAX_K):
        raise ValueError(f"k must be between {MIN_K} and {MAX_K}")

    filters = args.get("filters")
    if filters is not None and not isinstance(filters, dict):
        raise ValueError("filters must be an object")

    return query, k, filters


def validate_ctx_get(args: Dict[str, Any]) -> Tuple[List[str], str]:
    """Validate ctx_get arguments."""
    ids = args.get("ids")
    if not isinstance(ids, list) or not ids:
        raise ValueError("ids must be a non-empty array")

    if len(ids) > MAX_IDS:
        raise ValueError(f"ids max length is {MAX_IDS}")

    norm: List[str] = []
    for v in ids:
        if not isinstance(v, str):
            raise ValueError("each id must be a string")
        v = v.strip()
        if not v:
            raise ValueError("id must not be empty")
        if len(v) > MAX_ID_LEN:
            raise ValueError(f"id too long (>{MAX_ID_LEN})")
        norm.append(v)

    mode = args.get("mode", "excerpt")
    if mode not in ("raw", "excerpt", "skeleton"):
        raise ValueError(f"mode must be one of raw|excerpt|skeleton")

    return norm, mode


def to_tool_result(payload: Any, truncated: bool = False, is_error: bool = False, mock: bool = False) -> JSON:
    """Convert payload to MCP tool result format."""
    text = json.dumps(payload, ensure_ascii=False)
    text = redact_text(text)
    text, was_trunc = cap_text(text, MAX_STDOUT_CHARS)

    meta = {"truncated": truncated or was_trunc}

    if mock:
        meta["mock"] = True

    return {
        "content": [{"type": "text", "text": text}],
        "isError": bool(is_error),
        "_meta": meta,
    }


# MCP server core
def handle_request(adapter: TrifectaCliAdapter, mock_service, req: JSON) -> Optional[JSON]:
    """Handle MCP JSON-RPC request."""
    # Validate envelope
    if req.get("jsonrpc") != "2.0":
        return jsonrpc_error(
            req.get("id") if is_valid_id(req.get("id")) else None,
            -32600,
            "Invalid Request: jsonrpc must be '2.0'"
        )

    _id = req.get("id")
    if not is_valid_id(_id):
        return jsonrpc_error(
            None,
            -32600,
            "Invalid Request: id must be string|int|null"
        )

    method = req.get("method")
    if not isinstance(method, str):
        return jsonrpc_error(
            _id,
            -32600,
            "Invalid Request: method must be a string"
        )

    params = req.get("params")

    # Try to use real adapter, fall back to mock on error
    try:
        log(f"Request: {method}", id=_id, mode="real")

        if method == "initialize":
            return jsonrpc_result(
                _id,
                {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {
                        "name": "trifecta-mcp-server",
                        "version": "0.1.0",
                        "author": "PicoClaw",
                        "mcp_trifecta_mode": "real"
                    },
                    "capabilities": {
                        "tools": {}
                    }
                }
            )

        elif method == "tools/list":
            return jsonrpc_result(_id, {"tools": tool_specs()})

        elif method == "tools/call":
            p = ensure_object(params)
            name = p.get("name")
            arguments = p.get("arguments", {})

            if not isinstance(name, str) or not name:
                return jsonrpc_error(_id, -32602, "Invalid params: name is required")

            if not isinstance(arguments, dict):
                return jsonrpc_error(_id, -32602, "Invalid params: arguments must be an object")

            if name == "ctx_search":
                query, k, filters = validate_ctx_search(arguments)
                data = adapter.ctx_search(query=query, k=k, filters=filters)
                return jsonrpc_result(_id, to_tool_result(data))
            elif name == "ctx_get":
                ids, mode = validate_ctx_get(arguments)
                data = adapter.ctx_get(ids=ids, mode=mode)
                return jsonrpc_result(_id, to_tool_result(data))
            else:
                return jsonrpc_error(
                    _id,
                    -32601,
                    f"Method not found: unknown tool '{name}'",
                    data={"available_tools": ["ctx_search", "ctx_get"]}
                )

        elif method == "shutdown":
            return jsonrpc_result(_id, {"ok": True})

        else:
            return jsonrpc_error(
                _id,
                -32601,
                f"Method not found: {method}",
                data={"available_methods": ["initialize", "tools/list", "tools/call", "shutdown"]}
            )

    except (ValueError, RuntimeError) as exc:
        # Invalid params or CLI errors: return as tool result with isError=true
        return jsonrpc_result(_id, to_tool_result({"error": str(exc)}, is_error=True, mock=False))
    except Exception as exc:
        msg = redact_text(str(exc))
        return jsonrpc_error(_id, -32603, "Internal error", data={"message": msg})


def main() -> int:
    """Entry point for MCP server."""
    try:
        # Initialize CLI adapter
        adapter = TrifectaCliAdapter.from_env()

        # Initialize mock service for fallback
        mock_service = MockContextService()

        # Check if adapter can work (try to run --help)
        try:
            adapter._run_json(["--help"])
            log("Real mode: Trifecta CLI is accessible")
        except (FileNotFoundError, RuntimeError):
            log("Falling back to mock mode (Trifecta CLI not available)", mode="mock")

        # Read JSON-RPC requests from stdin
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            # Parse JSON
            try:
                req = json.loads(line)
                if not isinstance(req, dict):
                    resp = jsonrpc_error(None, -32700, "Invalid Request: body must be an object")
                else:
                    resp = handle_request(adapter, mock_service, req)
            except json.JSONDecodeError:
                resp = jsonrpc_error(None, -32700, "Parse error: invalid JSON")
            except Exception as exc:
                resp = jsonrpc_error(None, -32603, "Internal error", data={"message": redact_text(str(exc))})

            if resp is not None:
                sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
                sys.stdout.flush()

            # Exit on shutdown notification pattern (optional)
            if isinstance(req, dict) and req.get("method") == "shutdown":
                break

        return 0

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as exc:
        error_resp = {
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,
                "message": f"Server initialization failed: {exc}"
            }
        }
        sys.stdout.write(json.dumps(error_resp, ensure_ascii=False) + "\n")
        sys.stdout.flush()
        sys.exit(1)


if __name__ == "__main__":
    raise SystemExit(main())
