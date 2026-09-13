# Procedure: entrypoint-reachability

From all known entrypoints, map everything reachable in the codebase.

## Inputs

- `--scope`: limit to specific entrypoint types (cli|api|script|job)
- `--include-tests`: include test entrypoints (default: exclude)
- `--depth N`: max depth from each entrypoint

## Step 1: Discover Entrypoints

Scan the codebase for entrypoint patterns (language-aware):

```bash
# CLI
rg "func main\(\)" --type go
rg "argparse|click|typer|@command" --type py
rg "commander|yargs|sys\.argv" --type js

# API
rg "@app\.route|@router|handler|controller" --type py
rg "@app\.(get|post|put|delete)|@router\." --type ts

# Scripts
rg "if __name__" --type py
find . -name "*.sh" -not -path "*/node_modules/*" -not -path "*/.git/*"

# Jobs / CI
find . -name "*.yml" -path "*workflows*" -o -name "*.yaml" -path "*.github*"
rg "cron|schedule|@periodic_task" --type py
```

For each entrypoint found, record: file:line, type, symbol name.

## Step 2: BFS/DFS from Each Entrypoint

For each discovered entrypoint, walk the call graph depth-first:

1. Start at entrypoint symbol
2. For each callee, record: file:line, symbol, dispatch type, confidence
3. Mark symbol as REACHABLE
4. Recurse into callees until leaf or depth limit
5. Track which entrypoint reached each symbol (multi-entrypoint signal)

## Step 3: Build Reachability Set

Maintain a set of all reachable symbols:
```
REACHABLE = {symbol: [entrypoints_that_reach_it, confidence]}
```

## Step 4: Diff Against Full Symbol Set

1. Get all defined symbols in the codebase (adapter-dependent)
2. Subtract REACHABLE set
3. Remaining symbols = **unwired candidates**

Filter out:
- Test-only symbols (unless `--include-tests`)
- Type definitions, constants, enums (usually pulled by reference, not call)
- `__init__`, `__all__`, module-level docstrings

## Step 5: Classify Unwired Candidates

For each unwired candidate:

| Signal | Classification |
|--------|---------------|
| Only referenced in comments/docs | candidate:documentation-only |
| Referenced in config/string but no import | candidate:dynamic-dispatch |
| Imported but never called | candidate:imported-uncalled |
| No references found at all | candidate:no-references |
| Exported but no external consumers | candidate:exported-no-consumers |

**Never classify using prohibited terms** (see resources/confidence-model.md).

## Step 6: Generate Report

Use report-template.md. Include:
- Entrypoint inventory (count by type)
- Reachability coverage (% of symbols reached)
- Unwired candidates table with classification
- Multi-entrypoint overlap map (symbols reached by 2+ entrypoints)
- Handoff candidates for authority-flow-audit
