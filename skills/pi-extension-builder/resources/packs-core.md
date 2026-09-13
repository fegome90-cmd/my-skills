# pi Extension Packs — Core Patterns (6-7)\n\nIntermediate patterns for proxying, side effects, and inter-extension communication.\nFor packs 1-5, load .\n
For packs 1-5, load `resources/packs-essential.md`. For 8-10, load `resources/packs-hooks.md`.

## Pack 6: MCP Bridge — External Process + Tool Proxy

**Source**: `n8n-mcp-bridge.ts` (410 lines)
**When**: Proxying LLM tool calls to ANY MCP server over stdio.

```typescript
import { spawn, type ChildProcessWithoutNullStreams } from "node:child_process";
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

// Configure for YOUR MCP server
const MCP_BIN = process.env.MCP_SERVER_BIN || "my-mcp-server";

type Pending = { resolve: (v: any) => void; reject: (e: Error) => void };

export default function (pi: ExtensionAPI) {
  let proc: ChildProcessWithoutNullStreams | null = null;
  let nextId = 1;
  let stdoutBuffer = "";
  const pending = new Map<number, Pending & { timer: NodeJS.Timeout }>();
  let initialized = false;

  function attachHandlers(child: ChildProcessWithoutNullStreams) {
    child.stdout.on("data", (chunk: Buffer) => {
      stdoutBuffer += chunk.toString("utf8");
      // CORRECT buffer pattern: indexOf + while loop, NOT split
      let idx = stdoutBuffer.indexOf("\n");
      while (idx >= 0) {
        const line = stdoutBuffer.slice(0, idx).trim();
        stdoutBuffer = stdoutBuffer.slice(idx + 1);
        if (line) handleMessage(line);
        idx = stdoutBuffer.indexOf("\n");
      }
    });

    child.on("exit", () => {
      for (const w of pending.values()) {
        w.reject(new Error("MCP process exited"));
        clearTimeout(w.timer);
      }
      pending.clear();
      resetState();
    });
  }

  function handleMessage(line: string) {
    let msg: any;
    try { msg = JSON.parse(line); } catch { return; }
    if (typeof msg.id === "number" && pending.has(msg.id)) {
      const w = pending.get(msg.id)!;
      pending.delete(msg.id);
      clearTimeout(w.timer);
      if (msg.error) w.reject(new Error(msg.error.message || "Unknown MCP error"));
      else w.resolve(msg.result);
    }
  }

  async function ensureProcess(): Promise<ChildProcessWithoutNullStreams> {
    if (proc) return proc;
    const child = spawn(MCP_BIN, {  // configure MCP_BIN above or via env: process.env.MCP_SERVER_BIN
      stdio: ["pipe", "pipe", "pipe"],
    });
    child.stderr.on("data", () => { /* silence — MCP stdio must stay clean */ });
    attachHandlers(child);
    proc = child;
    return child;
  }

  async function rpc(method: string, params: Record<string, unknown> = {}): Promise<any> {
    const child = await ensureProcess();
    const id = nextId++;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => { pending.delete(id); reject(new Error(`MCP timeout: ${method}`)); }, 15_000);
      pending.set(id, { resolve, reject, timer });
      child.stdin.write(JSON.stringify({ jsonrpc: "2.0", id, method, params }) + "\n");
    });
  }

  async function ensureInitialized() {
    if (initialized) return;
    await rpc("initialize", {
      protocolVersion: "2024-11-05",
      capabilities: {},
      clientInfo: { name: "pi-mcp-bridge", version: "0.1.0" },
    });
    initialized = true;
  }

  // Register tool proxy
  pi.registerTool({
    name: "my_mcp_tool",
    label: "MCP Tool",
    description: "Proxy to MCP server",
    parameters: { type: "object", properties: { query: { type: "string" } }, required: ["query"] } as const,
    async execute(_id, params) {
      try {
        await ensureInitialized();
        const result = await rpc("tools/call", { name: "search", arguments: params });
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      } catch (err: any) {
        return { content: [{ type: "text", text: `MCP error: ${err.message}` }], isError: true };
      }
    },
  });

  function resetState() { proc = null; stdoutBuffer = ""; pending.clear(); initialized = false; }

  pi.on("session_shutdown", async () => {
    proc?.kill("SIGTERM");
    resetState();
  });
}
```

**Key rules**: Buffer management uses `indexOf("\n")` + while loop — NOT `split("\n")`. MCP requires `initialize` handshake before tool calls. Reset state on process exit. Use `isError: true` for error results.

---

## Pack 7: Turn Hook — Side Effects Per Turn

**Source**: `git-guard.ts` (45 lines)
**When**: Running side effects at turn boundaries — before each turn, after each turn, on agent completion.

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  let turnCount = 0;

  // Available turn events:
  // turn_start  → BEFORE the agent processes a turn
  // turn_end    → AFTER a complete turn (including tool calls)
  // agent_end   → when agent finishes ALL turns

  pi.on("session_start", async (_event, ctx) => {
    turnCount = 0;
    // Example: check environment at session start
    // const { stdout } = await pi.exec("git", ["status", "--porcelain"]);
    // if (stdout.trim() && ctx.hasUI) ctx.ui.notify(`Dirty: ${lines} changes`, "warning");
  });

  pi.on("turn_start", async () => {
    turnCount++;
    // Example: checkpoint before each turn
    // await pi.exec("git", ["stash", "create", "-m", `checkpoint-${turnCount}`]);
  });

  pi.on("turn_end", async () => {
    // Example: log turn completion
    // console.error(`[myext] Turn ${turnCount} done`);
  });

  pi.on("agent_end", async () => {
    // Example: notify user when agent finishes all turns
    // if (ctx?.hasUI) ctx.ui.notify(`Done: ${turnCount} turns`, "info");
    turnCount = 0;
  });
}
```

**Key rules**: `pi.exec()` is pi's built-in exec (NOT `child_process.exec`). Returns `{ stdout, stderr }`. Use `ctx.hasUI` before UI calls. `turn_start` → `turn_end` is one cycle (may include tool calls). `agent_end` fires after ALL turns complete.
