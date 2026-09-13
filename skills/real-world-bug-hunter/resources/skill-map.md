# Skill Resolution Map

Each agent resolves relevant skills before testing. This map tells agents which `skill-hub` queries to run based on what they are testing. Resolve skills at the start of your phase; load them before writing test code.

## Per-Subsystem Skill Resolution

| Subsystem | skill-hub query | Expected skills |
|-----------|-----------------|-----------------|
| CRUD | `security adversarial testing` | security-auditor, secure-coding |
| CRUD | `secure coding input validation` | secure-coding |
| PII / Privacy | `PII redaction privacy data leak` | security-testing-guide, secure-coding |
| Search / List | `FTS query special characters SQL injection` | sql-queries, secure-coding |
| Sessions | `CLI integration testing workflow` | cli-explorer, bash-scripting |
| Sync | `authority flow audit` | authority-flow-audit |
| Sync | `database state integrity verification` | sqlite-ops, db-performance |
| Compact / Recovery | `database verification state consistency` | sqlite-ops, sql-local-database-workflows |
| Export | `cross project data isolation authority` | authority-flow-audit |
| Workspace | `chaos engineering stress test` | chaos-engineer |
| Workspace | `SQLite concurrent access patterns` | sqlite-ops |

## Cross-Cutting Skills

All agents should resolve these regardless of subsystem:

| Query | Expected skill | Purpose |
|-------|---------------|---------|
| `systematic debugging root cause` | debug-helper | Structured failure analysis |
| `error classification patterns` | error-tracer | Deep error investigation and stack trace correlation |
| `judgment day evaluation severity` | (severity framework) | Consistent HIGH/MEDIUM/LOW classification |
| `verification loop quality gate` | verification-loop | Final pass validation |
