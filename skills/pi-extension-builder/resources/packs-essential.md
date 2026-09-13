# pi Extension Packs — Core



---

## Pack 1: Minimal Handler — Starting Point

**When**: Every extension starts here. Provides the skeleton with proper lifecycle cleanup.

```typescript
/**
 * my-extension.ts — One-line description
 */
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  const timers: NodeJS.Timeout[] = [];
  const unsubscribers: (() => void)[] = [];

  pi.on("session_start", async (_event, ctx) => {
    // Reinitialize state here (fires on /new, /resume, /fork)
  });

  // THIS IS THE ONLY CLEANUP HOOK. No "unload" or "session_switch" event exists.
  pi.on("session_shutdown", async (_event, _ctx) => {
    for (const t of timers) clearInterval(t);
    for (const u of unsubscribers) u();
  });

  // Catch process signals for cleanup outside pi lifecycle
  for (const sig of ["SIGTERM", "SIGHUP", "SIGINT"] as const) {
    process.on(sig, () => {
      for (const t of timers) clearInterval(t);
    });
  }
}
```

**Key rules**: `session_shutdown` fires on quit/reload/new/resume/fork. It is the ONLY cleanup event. Always handle SIGTERM/SIGHUP/SIGINT for out-of-band exits.

---

## Pack 2: Tool Registration — LLM-Callable Function

**When**: Exposing a function for the LLM to call during agent execution.

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";
import { StringEnum } from "@mariozechner/pi-ai";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "my_tool",
    label: "My Tool",
    description: `What this tool does.

## When to Use
- Condition 1
- Condition 2`,
    promptGuidelines: [
      "Use my_tool when the user asks to do X",
    ],
    parameters: Type.Object({
      action: StringEnum(["list", "add"] as const),
      text: Type.Optional(Type.String({ description: "Optional text" })),
    }),
    async execute(_toolCallId, params, signal, onUpdate, ctx) {
      // signal: AbortSignal — check signal.aborted or add listener
      // onUpdate: stream intermediate results to UI
      // ctx: ExtensionContext (ui, cwd, hasUI, etc.)

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
        // Return error as text, DO NOT throw
        return { content: [{ type: "text", text: `Error: ${err.message}` }] };
      }
    },
  });
}
```

**Key rules**: `promptGuidelines` bullets are flat — each MUST name the tool. Error paths return text content, never throw. `signal` supports `addEventListener("abort", ...)`. Works during load AND after startup.

---

## Pack 3: Command Registration — Slash Command

**When**: Adding `/mycmd` commands for the user.

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import type { AutocompleteItem } from "@mariozechner/pi-tui";

export default function (pi: ExtensionAPI) {
  pi.registerCommand("mycmd", {
    description: "One-line description",
    getArgumentCompletions(prefix: string): AutocompleteItem[] | null {
      return [{ value: "opt1", label: "Option 1" }];
    },
    handler: async (args: string, ctx) => {
      // ctx: ExtensionCommandContext (extends ExtensionContext)
      // ctx.waitForIdle(), ctx.newSession(), ctx.fork(), ctx.reload()
      if (ctx.hasUI) {
        ctx.ui.notify(`Result: ${args}`, "info");
      } else {
        console.log(`Result: ${args}`);
      }
    },
  });
}
```

**Key rules**: Multiple extensions can register same command name → auto-renamed to `/cmd:1`, `/cmd:2`. Use `ctx.hasUI` before calling UI methods. `args` is the raw string after the command name.

---

## Pack 4: Provider Registration — Custom Model Provider

**Source**: `openrouter.ts` (80 lines)
**When**: Adding a custom model provider (proxy, local model, alternative API).

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerProvider("my-provider", {
    baseUrl: "https://api.example.com/v1",
    apiKey: "!cat ~/.pi/agent/auth.json | jq -r '.myProvider.key'",
    api: "openai-completions",  // or "anthropic"
    headers: {
      "X-Custom-Header": "value",
    },
    models: [
      {
        id: "model-id",
        name: "Display Name",
        reasoning: true,            // supports chain-of-thought
        input: ["text", "image"],   // supported input types
        contextWindow: 131072,
        maxTokens: 16384,
        cost: { input: 0.3, output: 1.1, cacheRead: 0, cacheWrite: 0 },  // optional
      },
    ],
  });
}
```

**Key rules**: `apiKey` starting with `!` executes as shell command. Registration happens in factory function (no event needed). Optional `cost` per model.

---

## Pack 5: Tool Guard — Policy Enforcement Hook

**Source**: `tool-guard.ts` (296 lines)
**When**: Auditing, blocking, or transforming LLM tool calls based on policy.

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { isToolCallEventType } from "@mariozechner/pi-coding-agent";
import { appendFile, mkdir } from "node:fs/promises";
import { dirname } from "node:path";

// --- Policy types (implement your own policy format) ---
interface Policy {
  mode: "audit" | "enforce";
  failClosed?: boolean;
  blockedTools: string[];
  blockedCommands: string[];
  blockedPaths: string[];
  blockedPatterns: string[];
  allowedCommands?: string[];
  auditLog?: string;
}

// --- Policy helpers (implement your own loading logic) ---
const DEFAULT_POLICY: Policy = { mode: "audit", blockedTools: [], blockedCommands: [], blockedPaths: [], blockedPatterns: [] };
function loadPolicy(): Promise<Policy> { /* Load from JSON file, return DEFAULT_POLICY on error */ return Promise.resolve({ ...DEFAULT_POLICY }); }
function checkCommand(cmd: string, policy: Policy): { policy: string; matched: string } | null { /* Match against blockedCommands, blockedPatterns, allowedCommands */ return null; }
function isBlockedPath(path: string, blocked: string[]): boolean { /* Check if path starts with any blocked prefix */ return false; }
async function auditLog(entry: object): Promise<void> { /* Write to audit log file */ }

export default function (pi: ExtensionAPI) {
  let policy: Policy = { ...DEFAULT_POLICY };

  pi.on("session_start", async () => { policy = await loadPolicy(); });

  pi.on("tool_call", async (event, _ctx) => {
    try {
      const { toolName, toolCallId } = event;

      if (policy.blockedTools.includes(toolName)) {
        if (policy.mode === "enforce") return { block: true, reason: `Tool "${toolName}" blocked by policy` };
        await auditLog({ toolName, toolCallId, action: "audited" });
      }

      if (isToolCallEventType("bash", event)) {
        const command: string = event.input.command;
        const hit = checkCommand(command, policy);
        if (hit) {
          if (policy.mode === "enforce") return { block: true, reason: `Command blocked: ${hit.matched}` };
          await auditLog({ toolName: "bash", toolCallId, action: "audited", policy: hit.policy });
        }
      }

      if (isToolCallEventType("read", event) || isToolCallEventType("write", event) || isToolCallEventType("edit", event)) {
        const path: string = event.input.path;
        if (isBlockedPath(path, policy.blockedPaths)) {
          if (policy.mode === "enforce") return { block: true, reason: `Path blocked: ${path}` };
        }
      }

      return undefined;  // allow the tool call
    } catch (error) {
      // Tool guard errors must never crash pi
      if (policy.failClosed) return { block: true, reason: `Tool guard error: ${error}` };
      return undefined;  // fail-open: log but allow
    }
  });
}
```

**Key rules**: Return `{ block: true, reason }` to block — NOT `event.block()`. Use `isToolCallEventType("bash", event)` for type narrowing. Wrap the ENTIRE handler in try/catch with fail-closed/fail-open based on `policy.failClosed`. Helper functions are stubs — implement your own policy loading and command matching.

---

