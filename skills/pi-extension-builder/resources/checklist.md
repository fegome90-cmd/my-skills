# pi Extension Validation Checklist

Pre-submit checklist for pi extensions. All items MUST pass before deployment.

## Structural Checks

- [ ] File location: `~/.pi/agent/extensions/*.ts` or `~/.pi/agent/extensions/*/index.ts`
- [ ] Imports only from: `@mariozechner/pi-coding-agent`, `@mariozechner/pi-ai`, `@mariozechner/pi-tui`, `@sinclair/typebox`, Node.js built-ins
- [ ] No `require()` — use `import` only
- [ ] Export default factory function: `export default function(pi: ExtensionAPI)`
- [ ] No top-level side effects (code runs inside factory or event handlers)

## Type Safety

- [ ] `npx tsc --noEmit` passes in extensions directory
- [ ] No `any` types without justification (prefer generics or `unknown`)
- [ ] Tool parameters use `Type.Object()` from typebox — never raw objects
- [ ] Event payloads are typed or explicitly `unknown`

## Lifecycle Checks

- [ ] `session_shutdown` handler cleans up ALL resources:
  - [ ] Child processes killed
  - [ ] `setTimeout`/`setInterval` cleared
  - [ ] File handles closed
  - [ ] Temporary files deleted
  - [ ] Event listeners unsubscribed (if `pi.events.on` returns unsub)
- [ ] `session_start` handler reinitializes state (fresh maps, arrays)
- [ ] Process signals (`SIGTERM`, `SIGHUP`, `SIGINT`) handled for cleanup
- [ ] No `session_switch` or `unload` handlers (these events don't exist)

## Init Order Checks

- [ ] Event handlers registered BEFORE any `pi.events.emit()` calls
- [ ] Ready/announce events emitted LAST in factory function
- [ ] `pi.registerTool()` calls can be anywhere (works after startup too)
- [ ] No reliance on specific extension load order (use `pi.events` for coordination)

## Tool Registration Checks

- [ ] Tool name is unique (check `pi.getAllTools()`)
- [ ] `description` starts with what the tool does, includes "When to Use"
- [ ] `promptGuidelines` bullets name the tool explicitly: "Use my_tool when..."
- [ ] `parameters` schema uses `Type.Object()` with descriptions
- [ ] `execute` handles `signal.aborted` gracefully
- [ ] `execute` returns `{ content: [{ type: "text", text: "..." }] }` format
- [ ] Error paths return text content, not thrown exceptions

## Command Registration Checks

- [ ] Command name is short and memorable (`/mycmd`)
- [ ] `description` is one-line
- [ ] `handler` receives `(args: string, ctx: ExtensionCommandContext)`
- [ ] Uses `ctx.ui.notify()` for feedback, not `console.log()`

## Inter-Extension RPC Checks

- [ ] Reply channel format: `{originalChannel}:reply:{requestId}`
- [ ] Reply includes `{ success: true, data }` or `{ success: false, error }`
- [ ] Timeout on reply listeners (prevent memory leaks)
- [ ] Unsubscribe after reply received
- [ ] Ready event emitted AFTER handlers registered

## Child Process Checks

- [ ] `stdio: ["pipe", "pipe", "pipe"]` for capturing output
- [ ] stdout collected via `data` event (JSONL if `pi --mode json`)
- [ ] stderr ignored or logged, not parsed as JSON
- [ ] Process killed on `session_shutdown` (SIGKILL, no grace)
- [ ] Wall-clock timeout prevents hanging processes
- [ ] Temporary files cleaned up on process exit AND on shutdown

## Headless Mode Checks (if applicable)

- [ ] `pi --mode json -p` output parsed line-by-line (JSONL)
- [ ] Empty lines skipped
- [ ] Non-JSON lines treated as failure (strict mode)
- [ ] Assistant text extracted from `message_end` with `role: "assistant"`
- [ ] Fallback: `text_end` event content
- [ ] Requires `turn_end` event for completion validation
- [ ] Exit code 0 alone does NOT mean success

## Error Handling Checks

- [ ] No uncaught exceptions in event handlers (wrap in try/catch)
- [ ] Specific errors caught first (type errors, parse errors)
- [ ] Generic `catch` only as last resort with logging
- [ ] Error messages are actionable (what went wrong + what to do)
- [ ] No silent failures — at minimum log to stderr

## Performance Checks

- [ ] No blocking I/O in event handlers (use async or offload)
- [ ] No unbounded buffers — cap or stream
- [ ] No memory leaks — cleanup on shutdown
- [ ] No busy-wait polling — use events or setTimeout
- [ ] `execFileSync` with timeout if synchronous execution is unavoidable

## Testing

- [ ] `/reload` loads the extension without errors
- [ ] Extension works after `/new` + `/resume` (session lifecycle)
- [ ] Extension works in headless mode: `echo 'test' | pi --mode json -p`
- [ ] Error conditions produce graceful output, not crashes
- [ ] Concurrent operations don't corrupt state
