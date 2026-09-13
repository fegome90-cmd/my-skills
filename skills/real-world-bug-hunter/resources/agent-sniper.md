# Agent Sniper — Isolation & Boundary Testing

Audits data boundaries. Ensures one project's commands cannot see, modify, or corrupt another project's data — the kind of bug that only surfaces in multi-tenant real-world usage.

## What It Targets

- Cross-project data leaks in `search`, `list`, `export`, and `recover`
- Project-scoped CRUD isolation (create/read/update/delete stays within scope)
- Session project boundaries (compact/recover respects project context)
- Sync watermark integrity per project (no cross-contamination of sync state)
- Workspace isolation (workspaces in project A invisible to project B)
- Metadata cross-contamination (tags, timestamps, authors don't bleed between projects)
- No-project vs with-project behavior (commands without `--project` don't access scoped data)
- CWD auto-detection vs explicit `--project` (both enforce the same boundary)

## Test Procedure

1. **Resolve skills** — Run skill-hub queries (see Skill Resolution below)
2. **Create test fixtures** — Set up 2+ projects with distinct, identifiable data (different content strings, unique tags)
3. **For each project-scoped command:**
   - Execute from project A, verify results contain only project A data
   - Verify project B data is absent from output
   - Verify project B's DB state is unchanged
4. **Check 3 leakage vectors:**
   - Query results (search/list output)
   - Export output (exported files contain only scoped data)
   - Session context (compact/recover doesn't pull cross-project memories)
5. **Boundary edge cases:**
   - Run without `--project` — verify no scoped data appears
   - Run with explicit `--project` from wrong CWD — verify CWD doesn't override explicit scope
   - Run with `--project` pointing to non-existent project — verify clean error, no partial data leak

## Isolation Verification Matrix

| Command | Scope Method | What to Check for Leakage |
|---------|-------------|---------------------------|
| `memory save` | `--project` or CWD | Row stored under correct project ID only |
| `memory list` | `--project` or CWD | Results exclude other projects' entries |
| `memory search` | `--project` or CWD | FTS query cannot match other projects' content |
| `memory export` | `--project` or CWD | Export file contains zero bytes from other projects |
| `memory recover` | `--project` or CWD | Recovered context excludes other projects' memories |
| `sync push/pull` | `--project` or CWD | Sync watermark scoped, no cross-project sync |
| `workspace *` | `--project` or CWD | Workspace CRUD contained to one project |

## Expected Findings Format

```
[SNIPER-002] HIGH
Leakage vector: search query results
Source project: proj-alpha
Target project: proj-beta
Data leaked:    3 memory entries from proj-beta appeared in proj-alpha search
Reproduce:      1. memory save "secret-beta-data" -p proj-beta
                2. memory search "secret" -p proj-alpha
                3. Results include proj-beta entries — should be empty
Expected:       zero results (query scoped to proj-alpha only)
Actual:         proj-beta entries visible in proj-alpha search output
```

Fields per finding: ID, severity, leakage vector, source project, target project, data that leaked, reproduction steps.

## Skill Resolution (runtime)

Run these skill-hub queries before testing:

- `"authority flow audit boundaries"`
- `"database verification integrity"`
- `"SQL local database workflows"`

## Output Format

Wrap ALL findings in `## FORK_START ##` / `## FORK_END ##` markers. Include the header:
```
## FORK_START ##
## Status: success|partial|blocked
## Summary: <1-3 sentences>
## Artifacts: /tmp/hunt-findings-sniper.md
## Next: none
## Risks: <risks found or None>

[findings here]

## FORK_END ##
```
