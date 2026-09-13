# Procedure: dead-candidate-scan

Find symbols that are unreachable from any known entrypoint. Lighter weight
than entrypoint-reachability — skips the full reachability map and focuses
on the gap.

## Inputs

- `--include-tests`: include test files (default: exclude)
- `--min-confidence`: filter candidates below threshold (default: LOW)

## Step 1: Build Symbol Inventory

Collect all defined symbols using the best available adapter:

| Adapter | Command | Languages |
|---------|---------|-----------|
| Trifecta AST | `trifecta ast symbols sym://python/mod\|type/all` | Python |
| rg + AST | `rg "^(def |class |func |export )" --type-add` | All |

For non-Python, use rg patterns:
```bash
# Go
rg "func [A-Z]" --type go
rg "type [A-Z]" --type go

# TypeScript/JavaScript
rg "export (function|class|const|interface|type) " --type ts
rg "export default" --type ts

# Python (if no Trifecta)
rg "^(def |class ) " --type py
```

## Step 2: Reference Scan

For each symbol, check if it appears in any import, call, or reference:

```bash
# Symbol referenced anywhere
rg "<symbol_name>" --type <lang> -l
```

Count references. Distinguish:
- **Import references:** `import X`, `from Y import X`, `require("X")`
- **Call references:** `X()`, `X.method()`, `new X()`
- **Type references:** `: X`, `<X>`, `as X`
- **String references:** `"X"` in config, registry, plugin lists

## Step 3: Entrypoint Filter

Remove symbols that are entrypoints themselves (they're self-justifying).

Remove symbols reachable via dynamic dispatch patterns:
- Plugin registries: `registry["name"] = plugin_class`
- Factory patterns: `getattr(module, class_name)`
- Config-driven: string references in YAML/JSON/TOML
- Reflection: `inspect`, `getattr`, `importlib`

Mark these as `candidate:dynamic-dispatch` (LOW confidence unwired).

## Step 4: Confidence Assignment

| Evidence | Confidence |
|----------|-----------|
| Zero references anywhere | HIGH (likely unwired) |
| Only in comments, docs, or tests | HIGH |
| Imported but never called | MEDIUM |
| Referenced in config strings only | LOW (may be dynamic) |
| Referenced in plugin registry pattern | LOW |

## Step 5: Output

Generate candidate list sorted by confidence (HIGH first):

```
## Dead/Unwired Candidates (N found)

| Symbol | File | Confidence | Why | References |
|--------|------|-----------|-----|-----------|
| `_old_parser` | src/legacy/parser.py:42 | HIGH | No references found | 0 |
| `BatchProcessorV1` | src/batch/v1.py:15 | HIGH | Only in comments | 2 (doc) |
| `handle_webhook_v2` | src/api/hooks.py:88 | MEDIUM | Imported, never called | 1 (import) |
| `PluginMirror` | src/plugins/mirror.py:5 | LOW | String ref in config | 1 (config) |
```

## Step 6: Handoff Check

Scan candidates for patterns that authority-flow-audit should investigate:
- Multiple symbols with similar names (possible stale duplication)
- Symbols in files that also contain active writers
- Candidates in lifecycle-sensitive paths (hooks, jobs, middleware)

If any found → add to Handoff section.
