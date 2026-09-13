---
name: pi-startup-diagnostics
description: Diagnose Pi startup failures caused by conflicting extensions, duplicate tools, package globs, or bridge port collisions. Use when `pi` or `piup` reports `Tool ... conflicts with ...`, `Failed to load extension`, `Port ... in use`, or exits before the interactive session starts.
compatibility: Requires the Pi CLI. Uses POSIX shell commands; `timeout` or `gtimeout` and `lsof` are needed for bounded verification and port inspection.
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
---

# Pi startup diagnostics

Use a tight, bounded loop. Separate the fatal startup error from warnings before changing anything.

## 1. Capture a bounded repro

Run one command at a time. Every probe that can start Pi must have a real timeout; this prevents a bridge or shutdown hook from holding the shell open.

Use `gtimeout` instead of `timeout` when GNU coreutils is installed under the macOS name:

```bash
timeout 10s pi --version 2>&1
timeout 10s pi --help 2>&1
```

For a real startup check, use a non-interactive ephemeral session and skip the skill-registry watcher. This still loads the configured extensions while avoiding unrelated registry work:

```bash
timeout 30s pi --print --no-session --offline --no-tools \
  --no-skill-registry "Respond only OK." 2>&1
```

If neither `timeout` nor `gtimeout` exists, do not run the real startup probe unbounded; report that bounded verification is unavailable. Treat a non-zero exit code or an `Error:` line as failure. An exit code of `0` with no model text is a separate model-output issue, not evidence of an extension startup failure; report it separately. If the command prints the requested response but exits with `124`, startup succeeded but teardown exceeded the limit; report that separately. A notification or extension warning alone is not proof of failure.

## 2. Classify the symptom

- `Tool "X" conflicts with ...` is a fatal duplicate registration. Two loaded extensions expose the same tool name.
- `Failed to load extension "..."` identifies the extension that lost the registration race. The other path in the conflict usually registered first.
- `Port N in use` is normally a separate bridge warning. It means another process owns the listener; it does not explain a duplicate-tool error.

Do not merge these into one hypothesis.

## 3. Find the loading sources

Inspect only the relevant Pi settings and package metadata. Never print `auth.json`, API keys, bearer tokens, or complete environment dumps.

```bash
PI_DIR="${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}"
pi list 2>&1
grep -nE '"source"|"extensions"|"skills"|"!extensions/' \
  "$PI_DIR/settings.json"
```

`pi list` shows the package resources Pi actually sees. The targeted `grep` shows package filters without relying on a line range that can stop at a nested `]`. For duplicate tools, inspect only the exact files named by the error:

```bash
FILE_A='/absolute/path/from-the-error/first-extension.ts'
FILE_B='/absolute/path/from-the-error/second-extension.ts'
grep -nE 'registerTool|TODO_TOOL_NAME|name:' "$FILE_A" "$FILE_B"
```

Do not recursively grep the whole package cache. The exact paths from the error are authoritative; compare the registered tool name and behavior in those files.

For a port warning, identify the listener without killing it:

```bash
lsof -nP -iTCP:N -sTCP:LISTEN
```

Replace `N` with the reported port. Stop or restart a process only with explicit approval and only after confirming it is stale or belongs to the bridge.

## 4. Apply the smallest reversible fix

Keep one canonical implementation of a conflicting tool. Choose it from the user's intended behavior; do not copy the example blindly. Prefer a package-level extension exclusion over editing installed package source. In the observed incident, `gentle-pi` was kept and `agent-stuff/extensions/todos.ts` was excluded:

```json
"extensions": [
  "extensions/*.ts",
  "!extensions/subagent.ts",
  "!extensions/todos.ts"
]
```

Alternative: use a documented feature flag, such as `GENTLE_PI_TODO=0`, when the desired canonical implementation is the other package. Removing a whole package is a larger change and requires confirming that no other extensions or skills depend on it.

Before changing settings, preserve the original file or make a focused diff. Change one loading rule at a time. Do not patch `node_modules` or package cache files to hide a configuration collision.

## 5. Verify the original symptom and the runtime

Re-run both probes:

```bash
timeout 10s pi --help 2>&1
timeout 30s pi --print --no-session --offline --no-tools \
  --no-skill-registry "Respond only OK." 2>&1
```

Use `gtimeout` in place of `timeout` when required. The expected result is exit code `0` and no duplicate-tool `Error:`. Model text is additional evidence, not the startup verdict. A `124` after the requested response means teardown exceeded the limit, not that the extension collision remains. A remaining `Port N in use` line is a separate warning; report it and its listener PID rather than claiming it was fixed.

Report:

1. the two resources that collided;
2. the exact settings rule changed;
3. the bounded commands and exit codes used for verification;
4. any remaining bridge warning and its owner;
5. whether the change was applied or only recommended.
