# pi Extension Templates

Copy-paste templates for common extension patterns. Each template is self-contained.

## Template 1: Minimal Event Handler

For extensions that react to events without registering tools or commands.

```typescript
/**
 * my-extension.ts — One-line description
 */
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  let intervals: NodeJS.Timeout[] = [];
  let unsubscribers: (() => void)[] = [];

  pi.on("session_start", async (event, ctx) => {
    // Reinitialize state after session switch
  });

  pi.on("session_shutdown", async (event, ctx) => {
    for (const i of intervals) clearInterval(i);
    for (const u of unsubscribers) u();
    intervals = [];
    unsubscribers = [];
  });

  for (const sig of ["SIGTERM", "SIGHUP", "SIGINT"] as const) {
    process.on(sig, () => {
      for (const i of intervals) clearInterval(i);
    });
  }
}
```

## Template 2: Tool Registration

For extensions that register LLM-callable tools.

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "my_tool",
    label: "My Tool",
    description: `What this tool does.

## When to Use
- Condition 1
- Condition 2

## Parameters
- **param1**: Description (required)
- **param2**: Description (optional)`,
    parameters: Type.Object({
      param1: Type.String({ description: "Required parameter" }),
      param2: Type.Optional(Type.String({ description: "Optional parameter" })),
    }),
    async execute(_toolCallId, params, signal, _onUpdate, _ctx) {
      if (signal?.aborted) {
        return { content: [{ type: "text", text: "Cancelled" }] };
      }
      try {
        const result = await doWork(params);
        return {
          content: [{ type: "text", text: `Done: ${result}` }],
          details: { result },
        };
      } catch (err: any) {
        return { content: [{ type: "text", text: `Error: ${err.message}` }] };
      }
    },
  });
}
```

**Key rules:**
- `promptGuidelines` bullets are flat — MUST name the tool: "Use my_tool when..."
- `signal` supports `addEventListener("abort", ...)` for cancellation
- Error paths return text content, not thrown exceptions

## Template 3: Command Registration

```typescript
import type { AutocompleteItem } from "@mariozechner/pi-tui";

pi.registerCommand("mycmd", {
  description: "What this command does",
  getArgumentCompletions(prefix: string): AutocompleteItem[] | null {
    return [{ value: "opt1", label: "Option 1" }];
  },
  handler: async (args: string, ctx) => {
    ctx.ui.notify(`Result: ${args}`, "info");
  },
});
```

Multiple extensions registering same command name → `/cmd:1`, `/cmd:2`.

## Template 4: Inter-Extension RPC

```typescript
import { randomUUID } from "node:crypto";
const PROTOCOL_VERSION = 1;

// Consumer side: call an RPC
function rpcCall(pi: ExtensionAPI, channel: string, params: object, timeoutMs: number) {
  const requestId = randomUUID();
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { unsub(); reject(new Error(`${channel} timeout`)); }, timeoutMs);
    const unsub = pi.events.on(`${channel}:reply:${requestId}`, (raw) => {
      unsub(); clearTimeout(timer);
      if (raw.success) resolve(raw.data);
      else reject(new Error(raw.error));
    });
    pi.events.emit(channel, { requestId, ...params });
  });
}

// Provider side: handle RPC
pi.events.on("myext:rpc:ping", (payload) => {
  const { requestId } = payload;
  pi.events.emit(`myext:rpc:ping:reply:${requestId}`, {
    data: { version: PROTOCOL_VERSION },
  });
});

// Announce availability AFTER handlers registered
pi.events.emit("myext:ready");
```

**Critical:** Reply channel = `{originalChannel}:reply:{requestId}`. Register handlers BEFORE emitting ready.

## Extension Naming Convention

| Prefix | Purpose |
|--------|---------|
| `00-` | Foundation (memory bridges, core services) |
| `01-` | Context loaders |
| `02-` | Context enhancers |
| `03-` | Service adapters (RPC bridges) |
| No prefix | User extensions |

## Testing Extensions

```bash
# Hot reload
/reload

# Headless test
echo 'test' | pi --mode json -p 2>/dev/null | head -5

# Type check
cd ~/.pi/agent/extensions && npx tsc --noEmit
```
