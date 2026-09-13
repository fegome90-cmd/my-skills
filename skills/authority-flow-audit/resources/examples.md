# Worked Examples

## Example 1: repo-audit — CLI + API + Jobs Writing to Same DB

**Scenario:** A Python project has a CLI tool, a FastAPI backend, and Celery jobs
that all write to a PostgreSQL database. The user suspects conflicting data.

**Trigger:** "audit this repo for who writes what to the database"

### What the audit produces:

**Verdict:** CRITICAL ISSUES FOUND — Three surfaces write to `reports` table
without coordination.

**Authority Table (key columns):**

| Surface | Type | State Writes | Authority | Competes With | Risk | Confidence | Evidence Class | Proposed Decision |
|---------|------|-------------|-----------|--------------|------|------------|----------------|------------------|
| `POST /reports` | api | reports table | authoritative | none | low | high | direct-write | keep |
| `generate_report` CLI | cli | reports.status, reports.data | competing | POST /reports | critical | high | direct-write | delegate |
| `celery.compute_report` | job | reports.data, reports.computed_at | competing | POST /reports | critical | high | direct-write | delegate |

**Pipeline for `reports.data`:**

1. Official: `POST /reports` → `ReportService.create()` → validates → `db.save()`
2. Shadow: `generate_report` → reads config → computes → `db.execute(UPDATE)` (no validation)
3. Shadow: `celery.compute_report` → reads queue → computes → `db.execute(UPDATE)` (no validation)

**Duplications and Conflicts:**

| # | Conflict Type | Surfaces Involved | State/Artifact | Evidence | Severity | Confidence | Evidence Class |
|---|--------------|------------------|---------------|----------|----------|------------|----------------|
| 1 | double-writer | POST /reports, generate_report CLI | reports.data | api.py:45, cli.py:112 | critical | high | direct-write |
| 2 | double-writer | POST /reports, celery.compute_report | reports.data | api.py:45, tasks.py:78 | critical | high | direct-write |
| 3 | ssot-violation | generate_report CLI, celery.compute_report | reports.status | cli.py:115, tasks.py:82 | high | high | direct-write |

**Why confidence=high, evidence_class=direct-write:** All three surfaces contain
grep-confirmed `db.execute(UPDATE ...)` or `session.commit()` calls targeting the
`reports` table directly. No intermediate abstraction layer — each surface owns
its SQL.

**Side Effects:**

| # | Side Effect | Triggering Surface | Target | Concurrent With | Coordination | Severity | Confidence | Evidence Class |
|---|-------------|-------------------|--------|----------------|-------------|----------|------------|----------------|
| 1 | Status race condition | generate_report CLI | reports.status | celery.compute_report | none | high | high | direct-write |

**Recommended intervention:**

1. Make `ReportService.create()` the sole authority for `reports` table
2. Refactor CLI to call `ReportService.create()` via Python import (not raw SQL)
3. Refactor Celery job to use task result pattern instead of direct DB write
4. Add database-level check constraint on status transitions

---

## Example 2: change-audit — PR Adding a Pre-commit Hook

**Scenario:** An agent submitted a PR adding a `pre-commit` hook to auto-format
generated reports. The user wants to know if this conflicts with the existing
report generation pipeline.

**Trigger:** "audit this PR for authority conflicts"

### What the audit produces:

**Verdict:** NEEDS ATTENTION — The new hook writes to the same directory as the
official pipeline but with different formatting rules.

**Change analysis with delta markers:**

| Surface | Type | Writes To | Authority | Delta Marker |
|---------|------|-----------|-----------|--------------|
| `hooks/pre-commit-format-reports` | hook | `output/*.md` | competing | [NEW] |
| `ReportGen.generate()` | method | `output/*.md` | authoritative | [BASELINE] |

**Authority Table:**

| Surface | Type | Primary Action | Artifacts Produced | Authority | Competes With | Risk | Confidence | Evidence Class | Proposed Decision |
|---------|------|---------------|-------------------|-----------|--------------|------|------------|----------------|------------------|
| `ReportGen.generate()` | method | Generate formatted markdown | output/*.md | authoritative | none | low | high | direct-write | keep |
| `hooks/pre-commit-format-reports` | hook | Format markdown on pre-commit | output/*.md | competing | ReportGen.generate | medium | medium | call-chain | investigate |

**Conflict detected (confidence: medium, evidence_class: call-chain):**

- [BASELINE] pipeline: `make reports` → `ReportGen.generate()` → writes formatted markdown
- [NEW] hook: pre-commit → `prettier --write output/*.md` → reformats with different rules
- Both surfaces write to `output/*.md` with different formatting opinions

**[NEW] Duplications and Conflicts entry:**

| # | Conflict Type | Surfaces Involved | State/Artifact | Evidence | Severity | Confidence | Evidence Class |
|---|--------------|------------------|---------------|----------|----------|------------|----------------|
| 1 | double-writer | ReportGen.generate, pre-commit-format-reports | output/*.md | generator.py:89, hooks/pre-commit:12 | medium | medium | call-chain |

**[NEW] Side Effects entry:**

| # | Side Effect | Triggering Surface | Target | Concurrent With | Coordination | Severity | Confidence | Evidence Class |
|---|-------------|-------------------|--------|----------------|-------------|----------|------------|----------------|
| 1 | Formatting thrash | pre-commit-format-reports | output/*.md | ReportGen.generate | none | medium | medium | call-chain |

**Why confidence=medium, evidence_class=call-chain:** The hook calls `prettier`
through the pre-commit framework (chain: git hook → pre-commit runner → prettier).
The write to `output/*.md` is confirmed via `prettier --write` but the trigger
path depends on pre-commit configuration, not direct code invocation.

**[NEW] Prioritized Risk:**

| Priority | Risk | Severity | Confidence | Evidence Class |
|----------|------|----------|------------|----------------|
| 1 | Formatting thrash between hook and pipeline | MEDIUM | medium | call-chain |

**Recommended resolution:**

1. Decide which formatter is authoritative (pipeline's or prettier's)
2. If pipeline: remove prettier from hook, make hook validate-only
3. If prettier: remove formatting logic from pipeline, let hook be the formatter
