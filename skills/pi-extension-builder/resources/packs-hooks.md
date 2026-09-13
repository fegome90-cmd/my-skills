# pi Extension Packs — Hooks & RPC (8-10)\n
Session-level hooks and inter-extension communication patterns.
For packs 1-5, load `resources/packs-essential.md`. For 6-7, load `resources/packs-core.md`.\n
## Pack 8: Session Name — First-Message Hook

**Source**: `auto-session-name.ts` (29 lines)
**When**: Reacting to the first user message in a session.

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  let named = false;

  pi.on("session_start", async () => { named = false; });

  pi.on("agent_end", async (event) => {
    if (named) return;
    const userMsg = event.messages.find((m) => m.role === "user");
    if (!userMsg) return;

    // Handle both string and array content (multimodal messages)
    const text = typeof userMsg.content === "string"
      ? userMsg.content
      : userMsg.content
          .filter((b): b is { type: "text"; text: string } => b.type === "text")
          .map((b) => b.text)
          .join(" ");

    if (text) {
      pi.setSessionName(text.slice(0, 60).replace(/\n/g, " ").trim());
      named = true;
    }
  });
}
```

**Key rules**: `agent_end` fires after each turn. Use a `named` flag for single-execution. Content can be `string` or `ContentBlock[]` — handle both. `pi.setSessionName()` sets the display name.

---

## Pack 9: Periodic Check — Background Version Check

**Source**: `auto-update.ts` (73 lines)
**When**: Periodic background checks (version, health, config sync).

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { execSync } from "node:child_process";
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

const CHECK_INTERVAL = 24 * 60 * 60 * 1000; // 24 hours
const STAMP_FILE = join(homedir(), ".pi", "agent", ".update-check");

function readStamp(): number {
  try { return Number(readFileSync(STAMP_FILE, "utf8").trim()) || 0; } catch { return 0; }
}

function writeStamp() {
  try { writeFileSync(STAMP_FILE, String(Date.now())); } catch {}
}

function isNewer(latest: string, current: string): boolean {
  const a = latest.split(".").map(Number);
  const b = current.split(".").map(Number);
  for (let i = 0; i < 3; i++) {
    if ((a[i] ?? 0) > (b[i] ?? 0)) return true;
    if ((a[i] ?? 0) < (b[i] ?? 0)) return false;
  }
  return false;
}

// Implement your own version detection
function getCurrentVersion(): string | null { return null; }

export default function (pi: ExtensionAPI) {
  pi.on("session_start", async (_event, ctx) => {
    // Non-blocking: defer with setTimeout to not delay startup
    setTimeout(async () => {
      try {
        if (Date.now() - readStamp() < CHECK_INTERVAL) return;
        writeStamp();

        const latest = execSync("npm view my-pkg version", {  // replace my-pkg with your package
          encoding: "utf8", timeout: 8000,
        }).trim();

        const current = getCurrentVersion();
        if (!current || !latest || !isNewer(latest, current)) return;

        if (ctx.hasUI) {
          ctx.ui.notify(`Update: ${current} → ${latest}`, "info");
        } else {
          console.log(`Update available: ${current} → ${latest}`);
        }
      } catch { /* network error — ignore */ }
    }, 2000);
  });
}
```

**Key rules**: Use `setTimeout` to defer — don't block session startup. Stamp file rate-limits checks. `execSync` with timeout for network. `isNewer` does semver comparison.

---

## Pack 10: Inter-Extension RPC — Request/Reply

**When**: Communicating between extensions via the event bus.

```typescript
import { randomUUID } from "node:crypto";
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

// --- Provider side (handles RPC calls) ---
const unsubscribers: (() => void)[] = [];

function registerHandlers(pi: ExtensionAPI) {
  // Clean up previous handlers first (idempotent registration)
  unregisterHandlers();

  unsubscribers.push(
    pi.events.on("myext:rpc:ping", (payload) => {
      const { requestId } = payload;
      pi.events.emit(`myext:rpc:ping:reply:${requestId}`, {
        success: true,
        data: { version: 1 },
      });
    }),
  );

  unsubscribers.push(
    pi.events.on("myext:rpc:action", (payload) => {
      const { requestId, ...params } = payload;
      // Handle action...
      pi.events.emit(`myext:rpc:action:reply:${requestId}`, {
        success: true,
        data: { result: "done" },
      });
    }),
  );
}

function unregisterHandlers() {
  for (const u of unsubscribers) u();
  unsubscribers.length = 0;
}

// --- Consumer side (calls RPC) ---
function rpcCall(pi: ExtensionAPI, channel: string, params: object, timeoutMs = 5_000) {
  const requestId = randomUUID();
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      unsub();
      reject(new Error(`${channel} timeout after ${timeoutMs}ms`));
    }, timeoutMs);

    const unsub = pi.events.on(`${channel}:reply:${requestId}`, (raw) => {
      unsub();
      clearTimeout(timer);
      if (raw.success) resolve(raw.data);
      else reject(new Error(raw.error));
    });

    pi.events.emit(channel, { requestId, ...params });
  });
}

// --- Lifecycle ---
export default function (pi: ExtensionAPI) {
  pi.on("session_start", async () => {
    registerHandlers(pi);
    // Emit ready AFTER handlers registered
    pi.events.emit("myext:ready");
  });

  pi.on("session_shutdown", async () => {
    unregisterHandlers();
  });
}
```

**Key rules**: Reply channel = `{channel}:reply:{requestId}`. Reply format: `{ success, data }` or `{ success: false, error }`. Unsubscribe on reply AND on timeout. Register BEFORE emitting ready.
