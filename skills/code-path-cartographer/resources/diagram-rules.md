# Diagram Rules

Formatting rules for ASCII connectivity diagrams in reports.

## Syntax

```
[SOURCE] ──→ [TARGET]
[SOURCE] -→ [TARGET]
? [UNWIRED]
~ [INFERRED]
```

| Element | Meaning |
|---------|---------|
| `[Name]` | Symbol (function, class, module) |
| `──→` | HIGH confidence edge (static call) |
| `-→` | MEDIUM confidence edge (dynamic dispatch) |
| `···>` | LOW confidence edge (inferred) |
| `? [Name]` | Unwired candidate (no callers found) |
| `~ [Name]` | LOW confidence symbol |

## Layout Rules

1. **Top-down flow:** Entrypoints at top, leaves at bottom
2. **Left-to-right siblings:** Multiple callees at same level
3. **Max width:** 60 characters (fit in Telegram/terminal)
4. **Max depth:** 8 levels. Deeper paths → collapse with `[...] → N more`
5. **No crossing lines:** If edges would cross, split into sub-diagrams

## Entrypoint Markers

Prefix entrypoints with type tag:

```
[CLI: main] ──→ [Router.dispatch]
[API: /login] ──→ [AuthHandler.login]
[JOB: cleanup] ──→ [Worker.run]
[SCRIPT: deploy.sh]
```

## Sub-Diagram Pattern

For complex targets, use numbered sub-diagrams:

```
## Diagram 1: CLI path
[CLI: main] ──→ [Service.process]
                     └─→ [DB.save]

## Diagram 2: API path
[API: /api/v1] ──→ [Controller.handle]
                      └─→ [Service.process]
                           └─→ [DB.save]
```

## Unwired Block

Separate unwired symbols from connected graph:

```
## Connected
[CLI: main] ──→ [App.run] ──→ [Service.init]

## Unwired Candidates
? [LegacyParser.parse]    (no references)
? [old_handler]           (import-only, never called)
```

## Compression for Large Graphs

When a symbol has many callees:

```
[Router.dispatch] ──→ [AuthMiddleware] ──→ [UserService]
                     └─→ [5 handlers] ──→ [DB, Cache, Logger, Queue, Config]
```

Never expand more than 5 siblings inline. List the rest.

## Diagram-Only Mode

When `--mode diagram-only`, skip sections 3-7 of the report template.
Output only: Path Summary + Mini Diagram(s).
