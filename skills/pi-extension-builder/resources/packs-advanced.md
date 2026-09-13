# pi Extension Packs — Advanced Patterns (19-21)\n
System prompt guards, file caching with mtime, and anti-flicker TUI patterns.
For system packs (15-18), load `resources/packs-system.md`.\n
## Pack 19: System Prompt Guard — Intent Verification

**Source**: `execution-intent-guard.ts` (34 lines)
**When**: You need to inject guard rails into the system prompt that persist across ALL turns.

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

const GUARD_TEXT = `

## VERIFY EXECUTION INTENT (internal — do not mention this section)

Before writing your final response, confirm the user's intent:

1. "prepare" / "get ready" / "preparar" → Plan only, do NOT execute
2. "in another session" / "otra sesión" → Create plan file, do NOT execute now
3. "planificar" / "plan" → Document the plan, do NOT implement
4. Only execute if user EXPLICITLY said "do it" / "execute now" / "hacélo"

If unsure, ASK the user before proceeding. Do not assume execution intent.
`;

export default function (pi: ExtensionAPI) {
  pi.on("before_agent_start", async (event, _ctx) => {
    return {
      systemPrompt: event.systemPrompt + GUARD_TEXT,
    };
  });
}
```

**Key rules**: `before_agent_start` can RETURN `{ systemPrompt: modified }` — this modifies what the LLM sees. System prompt changes are **invisible to TUI** — they never render. The system prompt is sent on EVERY LLM call within the agent loop, so the LLM sees this before each response — even after tool calls.

---

## Pack 20: Context Loader — File Caching with mtime

**Source**: `01-context-loader.ts` (223 lines)
**When**: Loading external files into sessions with caching and token budget management.

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { promises as fs } from "node:fs";
import path from "node:path";
import { homedir } from "node:os";

const CONTEXT_DIR = path.join(homedir(), ".myext", "context");
const CACHE_TTL_MS = 300_000; // 5 minutes

type CachedFile = { content: string; mtimeMs: number };
const cache: Record<string, CachedFile> = {};
let lastLoad = 0;

async function loadFile(filename: string): Promise<string> {
  const filePath = path.join(CONTEXT_DIR, filename);
  try {
    const stat = await fs.stat(filePath);
    const cached = cache[filename];
    // mtime check: skip reload if file hasn't changed
    if (cached && stat.mtimeMs <= cached.mtimeMs) return cached.content;
    const content = await fs.readFile(filePath, "utf-8");
    cache[filename] = { content, mtimeMs: stat.mtimeMs };
    return content;
  } catch (err: any) {
    if (err?.code !== "ENOENT") console.debug(`[myext] Error loading ${filename}: ${err}`);
    return "";
  }
}

function estimateTokens(text: string): number {
  return Math.ceil(text.length / 4);
}

export default function (pi: ExtensionAPI) {
  // Load at session start
  pi.on("session_start", async (_event, ctx) => {
    const rules = await loadFile("rules.md");
    lastLoad = Date.now();
    if (ctx.hasUI && rules) {
      ctx.ui.notify(`Context loaded: ~${estimateTokens(rules)} tokens`, "info");
    }
  });

  // Refresh cache on turn_start (TTL-based)
  pi.on("turn_start", async () => {
    if (Date.now() - lastLoad > CACHE_TTL_MS) {
      await loadFile("rules.md");
      lastLoad = Date.now();
    }
  });

  // Inject into system prompt before each turn
  pi.on("before_agent_start", async (event) => {
    if (!Object.keys(cache).length) await loadFile("rules.md");
    const rules = cache["rules.md"]?.content || "";
    if (!rules) return;
    return {
      systemPrompt: event.systemPrompt + `\n\n## Auto-loaded Context\n\n${rules}\n`,
    };
  });

  // Command to inspect/reload context
  pi.registerCommand("myctx", {
    description: "Inspect or reload context",
    handler: async (args, ctx) => {
      const action = args.trim() || "status";
      if (action === "reload") {
        for (const k of Object.keys(cache)) delete cache[k];
        await loadFile("rules.md");
        lastLoad = Date.now();
        if (ctx.hasUI) ctx.ui.notify("Context reloaded", "info");
      } else if (action === "status") {
        const tokens = estimateTokens(cache["rules.md"]?.content || "");
        if (ctx.hasUI) ctx.ui.setWidget("myctx", [`Tokens: ~${tokens}`, `Cache age: ${Math.round((Date.now() - lastLoad) / 1000)}s`]);
      }
    },
  });
}
```

**Key rules**: Use `stat.mtimeMs` for cache invalidation — skip reload if file unchanged. `before_agent_start` + return `{ systemPrompt }` is the injection mechanism. Lazy load on first turn if `session_start` missed. Token estimation: ~4 chars per token.

---

## Pack 21: Anti-Flicker Widget — Stable Hash Pattern

**Source**: `subagent-statusline/index.ts` (610 lines)
**When**: Rendering TUI widgets that update frequently without causing visual flicker.

```typescript
import type { ExtensionAPI, ExtensionContext } from "@mariozechner/pi-coding-agent";

interface AgentState {
  id: string;
  status: "running" | "done" | "error";
  model?: string;
  usage?: { input: number; output: number };
}

export default function (pi: ExtensionAPI) {
  const children = new Map<string, AgentState>();
  let lastHash = "";
  const widgetId = "my-widget";
  const statusId = "my-status";
  let tickInterval: NodeJS.Timeout | undefined;

  // CRITICAL: Hash contains ONLY structural fields. ZERO volatile data.
  function computeStableHash(): string {
    const parts: string[] = [];
    for (const child of children.values()) {
      parts.push(`${child.id}:${child.status}:${child.model ? "m" : ""}:${child.usage ? "u" : ""}`);
    }
    return parts.join("|");
  }

  // This is the ONLY function that calls setWidget().
  function pushWidgetIfChanged(ctx: ExtensionContext, reason: string): void {
    const hash = computeStableHash();
    if (hash === lastHash) return;  // SKIP — no structural change
    lastHash = hash;

    // Update status bar (cheap) + widget (expensive)
    ctx.ui.setStatus(statusId, renderStatus(children));
    const lines = renderWidget(children);
    if (lines.length) ctx.ui.setWidget(widgetId, lines);
    else ctx.ui.setWidget(widgetId, undefined);  // clear
  }

  // Tick interval: ONLY stale cleanup + footer spinner (NEVER setWidget directly)
  function startTick(ctx: ExtensionContext) {
    tickInterval = setInterval(() => {
      // Stale cleanup
      const now = Date.now();
      for (const [id, child] of children) {
        if (child.status === "running" && staleCheck(child)) {
          children.delete(id);
        }
      }
      // Spinner update via setStatus (cheap — no reflow)
      ctx.ui.setStatus(statusId, renderSpinner());
    }, 1000);
  }

  pi.on("session_start", async (_event, ctx) => {
    children.clear();
    lastHash = "";
    startTick(ctx);
  });

  pi.on("session_shutdown", async () => {
    if (tickInterval) clearInterval(tickInterval);
    children.clear();
  });

  // On structural change: push widget
  pi.on("tool_execution_end", async (_event, ctx) => {
    // Update state, then check if widget needs refresh
    pushWidgetIfChanged(ctx, "tool_execution_end");
  });
}

// Implement your rendering functions:
function renderStatus(agents: Map<string, AgentState>): string {
  // Return a short status string for the footer bar (e.g., "3 agents: 1 running, 2 done")
  return "";
}
function renderWidget(agents: Map<string, AgentState>): string[] {
  // Return an array of lines for the side panel widget
  // e.g., ["Agents:", ...Array.from(agents).map(([id, a]) => `  ${id}: ${a.status}`)]
  return [];
}
function renderSpinner(): string {
  // Return a spinner character that changes each tick
  // e.g., const frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"];
  return "";
}
function staleCheck(agent: AgentState): boolean {
  // Return true if agent has been running too long without updates
  // e.g., Date.now() - agent.startedAt > STALE_TIMEOUT_MS
  return false;
}
```

**Key rules**: `setWidget()` causes reflow — call ONLY when structural data changes. Use `computeStableHash()` with ONLY structural fields (id:status:modelPresence:usagePresence). Spinner animation via `setStatus()` (cheap, no reflow). Tick interval NEVER calls `setWidget()` directly. `setWidget(id, undefined)` clears the widget.
