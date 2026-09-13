# pi Extension API Surface

Complete API reference for pi extension development.
Source: `pi --version` docs at `/opt/homebrew/lib/node_modules/@mariozechner/pi-coding-agent/docs/extensions.md`

## Extension Factory

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

// Synchronous
export default function (pi: ExtensionAPI) { /* ... */ }

// Asynchronous (pi waits for factory to resolve before startup)
export default async function (pi: ExtensionAPI) { /* ... */ }
```

## pi.registerTool(definition)

Register an LLM-callable tool. Works during load and after startup.

```typescript
import { Type } from "@sinclair/typebox";
import { StringEnum } from "@mariozechner/pi-ai";

pi.registerTool({
  name: "my_tool",                    // unique tool name
  label: "My Tool",                    // display label
  description: "What this tool does",  // LLM reads this
  promptSnippet: "One-line summary",   // optional: appears in Available tools
  promptGuidelines: [                  // optional: appended to Guidelines section
    "Use my_tool when the user asks to..."
  ],
  parameters: Type.Object({            // typebox schema
    action: StringEnum(["list", "add"] as const),
    text: Type.Optional(Type.String()),
  }),
  prepareArguments(args) {             // optional: compat shim before validation
    return args;
  },
  async execute(toolCallId, params, signal, onUpdate, ctx) {
    // signal: AbortSignal for cancellation
    // onUpdate: stream progress to UI
    // ctx: ExtensionContext (ui, cwd, sessionManager, etc.)
    onUpdate?.({ content: [{ type: "text", text: "Working..." }] });
    return {
      content: [{ type: "text", text: "Done" }],
      details: { result: "..." },  // optional structured data
    };
  },
  renderCall(args, theme, context) { /* optional custom render */ },
  renderResult(result, options, theme, context) { /* optional custom render */ },
});
```

**Key rules:**
- `promptGuidelines` bullets are appended flat with NO tool name prefix. Each bullet MUST name the tool: "Use my_tool when..."
- `signal` supports `signal.addEventListener("abort", ...)` for cancellation
- `onUpdate` allows streaming intermediate results

## pi.registerCommand(name, options)

Register a slash command. Multiple extensions can register same name → `/cmd:1`, `/cmd:2`.

```typescript
import type { AutocompleteItem } from "@mariozechner/pi-tui";

pi.registerCommand("mycmd", {
  description: "What this command does",
  getArgumentCompletions(prefix: string): AutocompleteItem[] | null {
    return [{ value: "opt1", label: "Option 1" }];
  },
  handler: async (args: string, ctx: ExtensionCommandContext) => {
    ctx.ui.notify("Done", "info");
  },
});
```

## pi.on(event, handler) — Lifecycle Events

```typescript
// Session lifecycle
pi.on("session_start", async (event, ctx) => { });
// event: { reason: "new" | "resume" | "fork", previousSessionFile? }

pi.on("session_before_switch", async (event, ctx) => { });
// event.cancel() to prevent switch

pi.on("session_shutdown", async (event, ctx) => { });
// event: { reason: "quit" | "reload" | "new" | "resume" | "fork", targetSessionFile? }
// THIS IS THE ONLY CLEANUP HOOK. No "unload" event exists.

pi.on("session_before_fork", async (event, ctx) => { });
pi.on("session_before_compact", async (event, ctx) => { });
// event.cancel() to prevent compaction
// event.compaction = { custom: "..." } to customize compaction

pi.on("session_compact", async (event, ctx) => { });
// event.compactionEntry = saved compaction data

// Agent lifecycle
pi.on("before_agent_start", async (event, ctx) => { });
// event.prompt, event.images, event.systemPrompt
// Can inject messages: event.messages.push(...)
// Can MODIFY system prompt: return { systemPrompt: event.systemPrompt + appended }
// System prompt changes are INVISIBLE to TUI — never render

pi.on("agent_start", async (event, ctx) => { });
pi.on("agent_end", async (event, ctx) => { });

// Turn lifecycle
pi.on("turn_start", async (event, ctx) => { });
pi.on("turn_end", async (event, ctx) => { });

// Message lifecycle
pi.on("message_start", async (event, ctx) => { });
pi.on("message_update", async (event, ctx) => { });
pi.on("message_end", async (event, ctx) => { });

// Tool lifecycle
pi.on("tool_call", async (event, ctx) => { });
// Can BLOCK the call: event.block()

pi.on("tool_result", async (event, ctx) => { });
// Can MODIFY the result

pi.on("tool_execution_start", async (event, ctx) => { });
pi.on("tool_execution_update", async (event, ctx) => { });
pi.on("tool_execution_end", async (event, ctx) => { });

// Provider
pi.on("context", async (event, ctx) => { });
// Can modify messages array
pi.on("before_provider_request", async (event, ctx) => { });
pi.on("after_provider_response", async (event, ctx) => { });

// User input
pi.on("user_bash", async (event, ctx) => { });
pi.on("input", async (event, ctx) => { });

// Model
pi.on("model_select", async (event, ctx) => { });
```

## pi.events — Inter-Extension Event Bus

```typescript
// Shared event bus for communication between extensions
pi.events.on("my:event", (data) => { /* handle */ });
pi.events.emit("my:event", { /* payload */ });

// RPC pattern (request-reply with scoped channel):
function rpcCall(channel, params, timeoutMs) {
  const requestId = crypto.randomUUID();
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { unsub(); reject(new Error("timeout")); }, timeoutMs);
    const unsub = pi.events.on(`${channel}:reply:${requestId}`, (raw) => {
      unsub(); clearTimeout(timer);
      if (raw.success) resolve(raw.data);
      else reject(new Error(raw.error));
    });
    pi.events.emit(channel, { requestId, ...params });
  });
}
```

## ExtensionContext (ctx)

Available in tool execute, command handler, and most event handlers.

```typescript
ctx.ui              // UI operations: notify, select, confirm, input
ctx.hasUI           // boolean: false in headless mode
ctx.cwd             // current working directory
ctx.sessionManager  // session operations: getEntries, etc.
ctx.modelRegistry   // model information
ctx.model           // current model
ctx.signal          // AbortSignal
ctx.isIdle()        // check if agent is idle
ctx.abort()         // abort current operation
ctx.hasPendingMessages()
ctx.shutdown()      // trigger shutdown
ctx.getContextUsage() // context window usage info
ctx.compact()       // trigger compaction
ctx.getSystemPrompt() // read current system prompt
```

## ExtensionCommandContext (extends ctx)

```typescript
ctx.waitForIdle()
ctx.newSession(options?)
ctx.fork(entryId, options?)
ctx.navigateTree(targetId, options?)
ctx.switchSession(sessionPath, options?)
ctx.reload()
```

## Available Imports

```typescript
import type { ExtensionAPI, ExtensionContext } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";
import { StringEnum } from "@mariozechner/pi-ai";
import { Container, Text } from "@mariozechner/pi-tui";  // TUI components
```

## Extension Locations

| Location | Purpose |
|----------|---------|
| `~/.pi/agent/extensions/*.ts` | User extensions (auto-loaded) |
| `~/.pi/agent/extensions/*/index.ts` | Package extensions |
| `/opt/homebrew/lib/node_modules/@tintinweb/pi-*/dist/` | NPM-installed extensions |

## Headless Mode: `pi --mode json -p`

```bash
echo 'prompt' | pi --mode json -p
```

Output: **JSONL stream** (one JSON per line) to stdout. Noise to stderr.

Event sequence: `session` → `agent_start` → `turn_start` → `message_start/end` (user) → `message_start/update/end` (assistant) → `turn_end` → (repeat if tools) → agent implicitly ends after last turn.

Extract assistant text from: `message_end` with `role: "assistant"` → `content[n].text`.
Fallback: `message_update` with `assistantMessageEvent.type: "text_end"` → `content` field.

Exit code: 0 on success (even if response is empty). Non-zero on infrastructure failure.
