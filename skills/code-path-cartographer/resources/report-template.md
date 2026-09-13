# Report Template

Mandatory structure for all code-path-cartographer reports.

---

## 1. Path Summary

```
Mode: <local-target | entrypoint-reachability | dead-candidate-scan | diagram-only>
Target: <file or symbol, or "full scan">
Scope: <depth, include-tests, segment>
Adapter: <which adapter was used>
Symbols scanned: <count>
Time: <duration estimate>
```

## 2. Mini Diagram

ASCII connectivity graph. Follow diagram-rules.md.

```
[CLI main] ──→ [Router.dispatch] ──→ [AuthMiddleware.check]
                                       ├─→ [UserService.validate] ──→ [DB.query]
                                       └─→ [Logger.warn]

? [LegacyParser.parse] (no callers found)
```

Legend:
- `[Name]` — symbol
- `──→` — HIGH confidence call
- `-→` — MEDIUM confidence call (dynamic)
- `? [Name]` — unwired candidate
- `~` prefix — LOW confidence / inferred

## 3. Connectivity Table

| Symbol | File:Line | Callers | Callees | Confidence |
|--------|-----------|---------|---------|-----------|
| `AuthService.login` | src/auth.py:42 | `Router.dispatch`, `CLI.login` | `DB.query`, `Hash.verify` | HIGH |
| `PluginLoader.load` | src/plugins.py:15 | `main` (config ref) | `importlib.import_module` | MEDIUM |

## 4. Evidence

Raw data backing each finding. One entry per notable finding.

```
### Finding: AuthService.login is reachable from 2 entrypoints

- CLI path: main() → CLI.login() → AuthService.login() [HIGH, static call]
- API path: app.route("/login") → Router.dispatch() → AuthMiddleware → AuthService.login() [HIGH, static call]
- Adapter: trifecta graph callers
```

## 5. Dead/Unwired Candidates

| Symbol | File | Confidence | Classification | References |
|--------|------|-----------|---------------|-----------|
| `_old_parser` | src/legacy.py:42 | HIGH | no-references | 0 |
| `handle_v2` | src/hooks.py:88 | MEDIUM | imported-uncalled | 1 |

**Total unwired candidates:** N (HIGH: X, MEDIUM: Y, LOW: Z)

## 6. Dynamic Dispatch / Uncertainty

Paths with MEDIUM or LOW confidence. Explain the gap.

```
### PluginLoader.load → actual plugin classes

Dispatch: plugin_registry[name] (string-keyed dict)
Confidence: LOW — cannot statically determine which plugins are registered
Mitigation: scan config files for plugin names, cross-reference with class definitions
```

## 7. Handoff to Authority Flow Audit

Candidates that authority-flow-audit should investigate. Only flag, never verdict.

```
### Candidate: DB.query called from 3 entrypoints

- CLI.main → DB.query (direct)
- API.handler → DB.query (via middleware)
- Job.cleanup → DB.query (scheduled)

Why flagged: Multiple entrypoints write to same surface. Authority-flow-audit
should determine if writes are coordinated or competing.

Evidence: [paste raw callers output]
```

---

**End of report.**
