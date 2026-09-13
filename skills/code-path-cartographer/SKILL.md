---
name: code-path-cartographer
description: "Map code connectivity, entrypoints, inbound/outbound references, call paths, mini diagrams, and dead candidates without duplicating authority-flow-audit."
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
---

# Code-Path Cartographer v1.0

Map how code connects. Trace entrypoints, resolve references, detect unwired
symbols, and produce connectivity reports. Facts only — no authority verdicts.

## When to Use / When Not to Use

**Use when:**
- Tracing how an entrypoint reaches a specific file or symbol
- Finding all callers/callees of a function, class, or module
- Checking if a symbol is reachable from any known entrypoint
- Generating connectivity diagrams for a module or subsystem
- Scanning for dead/unwired code candidates
- Before an authority-flow-audit — provide connectivity evidence as handoff

**Do NOT use for:**
- Authority/ownership/SSOT verdicts (→ authority-flow-audit)
- Style review, lint, formatting
- Performance profiling, security auditing
- Declaring dead code definitively

## Boundary with authority-flow-audit

| This skill (code-path-cartographer) | authority-flow-audit |
|---|---|
| HOW code connects (reachability, paths) | WHO owns/writes state |
| Facts: connected, unreachable, candidate | Verdicts: authoritative, competing, ambiguous |
| Connectivity graph, entrypoint maps | Pipeline analysis, SSOT verification |
| "Handoff candidates" flagged | Verdicts issued on handoff data |

**Rule:** If a finding looks like an authority concern (double-writer, shadow pipeline, competing writes), flag it as a handoff candidate. Do NOT issue the verdict yourself.

## Modes

| Mode | Flag | Purpose |
|------|------|---------|
| **local-target** | `--mode local-target` | Trace a file/symbol up to entrypoints and down to leaf callees |
| **entrypoint-reachability** | `--mode entrypoint-reachability` | From entrypoints, map everything reachable |
| **dead-candidate-scan** | `--mode dead-candidate-scan` | Find symbols unreachable from any known entrypoint |
| **diagram-only** | `--mode diagram-only` | Generate connectivity diagram, skip full analysis |

Default: `local-target` if a target is specified, `entrypoint-reachability` otherwise.

## Inputs

- Repository path (default: cwd)
- Target file or symbol (for local-target)
- `--depth N` — max traversal depth (default: unlimited for local-target)
- `--include-tests` — include test files in scan (default: exclude)
- `--segment PATH` — Trifecta segment override

## Confidence Model

| Level | Meaning | Allowed language | Forbidden language |
|---|---|---|---|
| **HIGH** | Full static trace, no dynamic dispatch | "is connected", "is reachable" | — |
| **MEDIUM** | Connected but dynamic gap (reflection, plugin registry, string dispatch) | "likely connected", "probable path" | "is connected" |
| **LOW** | Inference only (naming, convention, no code trace) | "may be connected", "candidate" | "is connected", "dead code" |

**Prohibited in ALL levels:** "dead code", "unused", "safe to delete", "orphaned code". Use "dead candidate", "unwired", "unreachable from known entrypoints".

## Procedure Overview

1. **Detect language** from file extensions and project structure
2. **Select adapter** based on language and tool availability (see resources/adapters.md)
3. **Index** the codebase (Trifecta graph index or rg scan)
4. **Execute mode procedure** (load the matching resource file)
5. **Generate report** using resources/report-template.md

## Adapter Priority

See `resources/adapters.md` for full details.

| Priority | Adapter | Languages | Command |
|---|---|---|---|
| 1 | Trifecta graph | Python | `trifecta graph callers/callees/index` |
| 2 | Trifecta AST | Python | `trifecta ast symbols/hover` |
| 3 | rg + git grep | All | `rg`, `git grep` |
| 4 | Trifecta ctx_search | All (semantic) | `trifecta ctx_search` |
| 5 | Neovim headless | LSP-capable | `nvim --headless` (optional) |

## Report Sections

1. Path Summary — what was traced, scope, adapter used
2. Mini Diagram — ASCII connectivity graph
3. Connectivity Table — symbol → callers → callees → confidence
4. Evidence — raw data backing each finding
5. Dead/Unwired Candidates — symbols unreachable from entrypoints
6. Dynamic Dispatch / Uncertainty — paths with MEDIUM or LOW confidence
7. Handoff to Authority Flow Audit — flagged candidates for a-f-a

## Resources Index

| Resource | When to Load |
|----------|-------------|
| `resources/procedure-local-target.md` | `--mode local-target` |
| `resources/procedure-entrypoint-reachability.md` | `--mode entrypoint-reachability` |
| `resources/procedure-dead-candidate-scan.md` | `--mode dead-candidate-scan` |
| `resources/adapters.md` | Before starting (adapter selection) |
| `resources/report-template.md` | Report generation |
| `resources/confidence-model.md` | Before classifying findings |
| `resources/diagram-rules.md` | When generating diagrams |

Max context: SKILL.md (~140 lines) + 1 resource (~200 lines) = ~340 lines.

## Self-Audit

After creating/updating this skill, run:
```bash
# Verify no overlap with authority-flow-audit triggers
grep -c "authoritative\|SSOT\|ownership\|double.writer\|competing" SKILL.md resources/*.md
# Should be 0 in procedure files (only in boundary docs)

# Verify no forbidden language in procedure execution files (excluding definitions in boundary/confidence docs)
grep -rn "dead code\|safe to delete\|unused\|orphaned code" resources/procedure-*.md
# Should be 0

# Line counts
wc -l SKILL.md resources/*.md
```
