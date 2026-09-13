# Procedure: repo-audit Tier-Based Reference

Search patterns, state categories, authority classifications, and pipeline type
definitions. Used during Tier 1-3 execution.

Load `resources/judgment.md` alongside this file for confidence/evidence classification.

---

## Tier 1: Structural Scan — Prioritized Discovery

Discovery follows priority order. Start with Tier 1 surfaces and expand only if escalation criteria are met (see judgment.md).

### Tier 1: Authority-Critical Surfaces (always catalog)

These surfaces directly affect state ownership and pipeline authority.

```
1. CLI entry points:     grep -rn "argparse\|click\|typer\|commander\|@command\|sys.argv"
2. API endpoints:        grep -rn "@app.route\|@router\|handler\|controller\|lambda"
3. Scripts:              find . -name "*.sh" -o -name "*.py" | grep -E "scripts|bin|tools"
4. Jobs/cron:            find . -name "crontab" -o -name "*.cron" | grep -rn "celery\|rq\|github actions"
5. Hooks:                grep -rn "pre-commit\|post-receive\|lifecycle\|useEffect\|componentDidMount"
6. Daemons/workers:      grep -rn "daemon\|worker\|subscriber\|consumer\|listener"
7. Event handlers:       grep -rn "on_event\|handle_\|subscribe\|dispatch\|emit"
8. State writers:        grep -rn "\.save(\|\.write(\|\.update(\|\.create(\|INSERT\|UPDATE\|PUT\|POST"
```

Surface types: `cli | api | script | job | hook | daemon | handler | writer`

For each Tier 1 surface record:
- File path and line range
- Surface type
- What state it writes to (primary signal for authority)
- What calls it (inbound entrypoints)
- What it calls (outbound dependencies)

### Tier 2: Mutation-Affecting Surfaces (catalog if they sit between entrypoint and write)

```
9. Wrappers/decorators:  grep -rn "def.*wrapper\|@decorator\|def.*proxy"
10. Transformers:        functions that modify data before passing to a writer
11. Importers/loaders:   grep -rn "def.*import\|def.*load\|def.*parse" (narrow to IO functions)
```

Catalog Tier 2 surfaces only if:
- They sit in the call path between a Tier 1 entrypoint and a state write
- They add validation, transformation, or side effects that differ from the writer
- They could be called independently of the Tier 1 surface

### Tier 3: Skip Unless Explicitly Scoped

- Pure reader functions (compute + return, no side effects)
- Test fixtures and mocks (unless they write to production state)
- Display/formatting functions
- Utility helpers with no mutation path

Catalog Tier 3 only if `--scope` explicitly includes them, or if a Tier 1/2 surface
contains calls to Tier 3 functions that perform hidden side effects.

---

## Phase 2: State and Artifact Categories

### State Categories

| Category | Examples |
|----------|---------|
| Files | config files, data files, cache files, lock files, temp files |
| Database | tables, rows, columns, materialized views |
| Queues | message queues, task queues, event buses |
| Sockets | unix sockets, TCP sockets, IPC channels |
| Environment | env vars, runtime config, feature flags |
| Process state | memory, pid files, shared memory segments |
| External services | third-party APIs, SaaS stores, managed services |

### Artifact Categories

| Category | Examples |
|----------|---------|
| Generated files | reports, build artifacts, dist output |
| Logs and traces | application logs, audit trails, distributed traces |
| Metrics | monitoring data, dashboards, alerts |
| Deployed artifacts | containers, packages, bundles |
| State snapshots | backups, checkpoints, savepoints |

### Per-Surface Fields

| Field | Question |
|-------|----------|
| reads | What state/artifacts does this surface consume? |
| writes | What state/artifacts does this surface produce or mutate? |
| side_effects | What external effects does it cause (network, disk, process)? |

---

## Phase 3: Authority Classification

Authority is determined by four factors:
1. Who creates the state (first writer)
2. Who is the canonical updater (primary writer)
3. Who other surfaces expect to be the source of truth
4. Whether multiple writers compete without coordination

### Classifications

| Classification | Definition |
|---------------|------------|
| **authoritative** | Designated creator/owner of this state |
| **delegated** | Writes on behalf of the authoritative surface |
| **reader-only** | Reads but never mutates |
| **evidence** | Produces diagnostic/observational output only |
| **competing** | Writes to state owned by another surface |
| **legacy** | Was authoritative but has been superseded |
| **ambiguous** | Authority cannot be determined from code alone |

### Authority vs Evidence

Evidence surfaces produce observations about state: logs, reports, metrics, test results.
They describe what happened but do not own the state they describe.

Authority surfaces create, mutate, or govern state. If an authority surface disagrees
with all evidence surfaces, the authority surface wins by definition.

Tests for authority:
- If you delete this surface's output, does the system break? (authority signal)
- If you delete this surface's output, does observability decrease? (evidence signal)
- Does any other surface read this output to make state decisions? (potential false authority)

---

## Phase 4: Pipeline Types

For each artifact or state mutation, answer:
1. How many distinct code paths can produce or mutate it?
2. Are any paths unofficial (scripts, CLI, direct DB access)?
3. Do any paths bypass validation or lifecycle hooks?
4. Are there legacy paths still alive alongside new ones?

### Classification

| Type | Pattern |
|------|---------|
| **single-pipeline** | One authoritative path, no alternatives |
| **official+tolerated** | One official path, one or more legacy/convenience paths |
| **competing** | Two or more active paths with no clear authority |
| **orphaned** | Path exists but no surface activates it (dead code) |
| **shadow** | Unofficial path that circumvents the official one |

### Pipeline Tracing Method

1. Start from the artifact/state
2. Grep for all write operations that produce or mutate it
3. For each write operation, trace backward to the entrypoint
4. Map the full path: entrypoint → intermediate surfaces → write operation
5. Compare paths for: validation differences, side effect differences, trigger conditions
