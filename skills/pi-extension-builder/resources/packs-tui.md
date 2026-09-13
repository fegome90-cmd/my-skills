# pi Extension Packs — Advanced

Advanced patterns for TUI, sessions, compaction, multi-file packages, and prompt injection.
Each pack is verified against the real source code.

---

## Pack 11: Footer Status Bar — Custom Footer Rendering

**Source**: `custom-footer.ts` (96 lines)
**When**: Displaying live status in the pi footer bar.

```typescript
import type { AssistantMessage } from "@mariozechner/pi-ai";
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { truncateToWidth } from "@mariozechner/pi-tui";

export default function (pi: ExtensionAPI) {
  let sessionStart = Date.now();

  function fmt(n: number): string {
    if (n < 1000) return `${n}`;
    return `${(n / 1000).toFixed(1)}k`;
  }

  pi.on("session_start", async (_event, ctx) => {
    sessionStart = Date.now();
    if (!ctx.hasUI) return;

    ctx.ui.setFooter((tui, theme, footerData) => {
      // Subscribe to git branch changes for re-render
      const unsub = footerData.onBranchChange(() => tui.requestRender());
      // Periodic re-render for elapsed time
      const timer = setInterval(() => tui.requestRender(), 30_000);

      return {
        // Called when extension should clean up
        dispose() { unsub(); clearInterval(timer); },
        // Called when footer data changes (not commonly used)
        invalidate() {},
        // Render footer content — returns array of strings, one per line
        render(width: number): string[] {
          // Access session data
          let input = 0, output = 0, cost = 0;
          for (const e of ctx.sessionManager.getBranch()) {
            if (e.type === "message" && e.message.role === "assistant") {
              const m = e.message as AssistantMessage;
              input += m.usage.input;
              output += m.usage.output;
              cost += m.usage.cost.total;
            }
          }

          // Access context usage
          const usage = ctx.getContextUsage();
          const pct = usage?.percent ?? 0;
          const pctColor = pct > 75 ? "error" : pct > 50 ? "warning" : "success";

          // Theme API: theme.fg(colorName, text)
          const stats = theme.fg("accent", `${fmt(input)}/${fmt(output)}`)
            + theme.fg("warning", ` $${cost.toFixed(2)}`)
            + theme.fg(pctColor, ` ${pct.toFixed(0)}%`);

          const branch = footerData.getGitBranch();
          const branchStr = branch ? theme.fg("accent", `⎇ ${branch}`) : "";

          const left = [stats, branchStr].filter(Boolean).join(theme.fg("dim", " | "));
          return [truncateToWidth(left, width)];
        },
      };
    });
  });

  pi.on("session_switch", async (event) => {
    if (event.reason === "new") sessionStart = Date.now();
  });
}
```

**Key rules**: `setFooter()` returns `dispose`/`invalidate`/`render` object. `dispose()` fires when extension unloads — clean up timers and subscriptions there. `truncateToWidth()` ensures text fits terminal width. `footerData.onBranchChange()` triggers re-render on git branch changes.

---

## Pack 12: Header Display — Custom Header Rendering

**Source**: `compact-header.ts` (69 lines)
**When**: Displaying custom content in the pi header (keybindings, status info).

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { VERSION } from "@mariozechner/pi-coding-agent";
import { truncateToWidth, visibleWidth } from "@mariozechner/pi-tui";

export default function (pi: ExtensionAPI) {
  pi.on("session_start", async (_event, ctx) => {
    if (!ctx.hasUI) return;

    ctx.ui.setHeader((_tui, theme) => ({
      render(width: number): string[] {
        const d = (s: string) => theme.fg("dim", s);
        const a = (s: string) => theme.fg("accent", s);

        // Access registered commands
        const cmds = pi.getCommands();
        const prompts = cmds
          .filter(c => c.source === "prompt")
          .map(c => `/${c.name}`).join("  ");

        const model = ctx.model ? `${ctx.model.id}` : "no model";
        const thinking = pi.getThinkingLevel();
        const provider = ctx.model?.provider ?? "";

        // Build tabular layout
        const lines: string[] = [""];
        lines.push(d("version") + "  " + a(`v${VERSION}  ${provider}`));
        lines.push(d("model") + "    " + a(model));
        lines.push(d("think") + "    " + a(thinking));
        if (prompts) lines.push(d("prompts") + "  " + a(truncateToWidth(prompts, width - 12)));
        lines.push(d("─".repeat(width)));

        return lines;
      },
      invalidate() {},
    }));
  });
}
```

**Key rules**: Same pattern as `setFooter()` — returns `render`/`invalidate`. `pi.getCommands()` returns registered commands with source info. `VERSION` from pi package. `visibleWidth()` measures actual display width (handles ANSI escapes).

---

## Pack 13: Session Hub — Event-Driven Session Management

**Source**: `context-session-hub.ts` (1419 lines)
**When**: Managing sessions with custom events, commands, and inter-extension coordination.

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

// Implement your own persistence functions
async function saveCheckpoint(args: string): Promise<{ name: string; path: string }> { return { name: args, path: "" }; }
async function listSessions(): Promise<{ name: string; path: string }[]> { return []; }
async function restoreState(_previousFile?: string): Promise<void> {}

export default function (pi: ExtensionAPI) {
  // Emit custom events for other extensions to consume
  // Use namespace prefixes to avoid collisions
  function emitRestore(sessionId: string, entries: any[]) {
    pi.events.emit("session-restore:start", { sessionId, entries });
  }

  function emitRestored(meta: { name: string; path: string }) {
    pi.events.emit("session-restore:done", meta);
  }

  // Register commands for session management
  pi.registerCommand("checkpoint", {
    description: "Save session state as checkpoint",
    handler: async (args, ctx) => {
      const meta = await saveCheckpoint(args);
      emitRestored(meta);
      if (ctx.hasUI) {
        ctx.ui.notify(`Checkpoint saved: ${meta.name}`, "info");
      }
    },
  });

  pi.registerCommand("sessions", {
    description: "List saved sessions",
    handler: async (_args, ctx) => {
      const sessions = await listSessions();
      if (ctx.hasUI) {
        ctx.ui.setWidget("sessions-list", [
          "Sessions:",
          ...sessions.map(s => `  ${s.name} — ${s.path}`),
        ]);
      }
    },
  });

  // React to session lifecycle
  pi.on("session_start", async (event, ctx) => {
    if (event.reason === "resume") {
      // event.previousSessionFile contains the old session path
      await restoreState(event.previousSessionFile);
    }
  });
}
```

**Key rules**: Use `pi.events` for inter-extension communication — namespace your events. `session_start` with `reason: "resume"` provides `previousSessionFile`. Commands and events can coordinate: command saves, event notifies.

---

## Pack 14: Compaction Hook — Persist State Across Compaction

**Source**: `00-compact-memory-bridge.ts` (1244 lines)
**When**: Customizing compaction behavior or persisting critical state across compaction.

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  const state: Map<string, string> = new Map();

  // BEFORE compaction: persist critical state
  pi.on("session_before_compact", async (event, _ctx) => {
    // Can customize compaction content:
    // event.compaction = { custom: "preserve this text" }
    // Can cancel: event.cancel() (use sparingly)

    // Save critical state to persistent storage
    await persistToMemory(state);
  });

  // AFTER compaction: verify and restore
  pi.on("session_compact", async (event, _ctx) => {
    // event.compactionEntry = the compaction data that was saved
    // Verify critical context survived compaction
    const recovered = await recoverFromMemory();
    if (recovered) state.set("recovered", "true");
  });

  // Track file operations from tool results for state
  pi.on("tool_result", async (event) => {
    // event.toolName — the name of the tool that produced this result
    // event.input — the tool's input parameters
    if (["edit", "write"].includes(event.toolName)) {
      const path = event.input?.path;
      if (path) {
        // Track modified files for state persistence
      }
    }
  });

  // ALSO persist on shutdown (belt and suspenders)
  pi.on("session_shutdown", async () => {
    await persistToMemory(state);
  });
}
```

**Key rules**: `session_before_compact` is the ONLY chance to influence what gets preserved. `session_compact` fires after compaction completes. Always persist on shutdown too — compaction is not guaranteed. Track tool results for file-aware state.

---

