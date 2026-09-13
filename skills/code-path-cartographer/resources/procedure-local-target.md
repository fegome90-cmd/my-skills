# Procedure: local-target

Trace a specific file or symbol: who calls it (upstream to entrypoints) and
what it calls (downstream to leaf callees).

## Inputs

- `target`: file path or symbol name (required)
- `--depth N`: max traversal levels (default: unlimited)
- `--include-tests`: include test callers (default: exclude)

## Step 1: Resolve Target

1. If target is a file → extract exported symbols (load adapters.md)
2. If target is a symbol → locate its definition
3. If ambiguous (multiple defs) → list all, ask user to pick

## Step 2: Upstream Trace (Callers)

Starting from the target symbol, walk backward:

```
target_symbol
  ← caller_1 (file:line, confidence)
    ← caller_1a (file:line, confidence)
    ← ENTRYPOINT (type: cli|api|main)
  ← caller_2 (file:line, confidence)
    ← ENTRYPOINT (type: api)
  ← NO CALLERS FOUND → flag as unwired candidate
```

**Stop conditions:**
- Reach an entrypoint (cli main, api route, script, job)
- Hit `--depth` limit
- No more callers found

**For each edge, record:**
- Source file:line
- Symbol name
- Confidence (HIGH/MEDIUM/LOW per confidence-model.md)
- Dispatch type (static / dynamic / inferred)

## Step 3: Downstream Trace (Callees)

Starting from the target symbol, walk forward:

```
target_symbol
  → callee_1 (file:line, type: local|external|stdlib)
    → callee_1a (file:line)
    → callee_1b (file:line, external lib)
  → callee_2 (file:line, type: local)
```

**Stop conditions:**
- Reach leaf function (no further callees)
- Hit external library boundary
- Hit `--depth` limit

## Step 4: Cross-Reference

Check if upstream entrypoints also appear as callees of the target
(circular dependency signal). Flag if found.

## Step 5: Entry Detection

For each path, classify the terminal node:

| Pattern | Type |
|---------|------|
| `func main()`, `package main` | entrypoint:cli |
| `@app.route`, `@router`, `handler` | entrypoint:api |
| `__main__`, `if __name__` | entrypoint:script |
| `*.sh`, `Makefile target` | entrypoint:script |
| Cron, CI workflow, job config | entrypoint:job |
| None found | unwired |

## Step 6: Generate Report

Use report-template.md. Include:
- Upstream tree with confidence per edge
- Downstream tree with type per edge
- Entry detection results
- Any circular dependency signals
- Handoff candidates if patterns match authority-flow-audit scope
