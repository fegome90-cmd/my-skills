# Activation Test — Trigger Validation

Test cases for validating that this skill activates correctly and does not activate
for wrong contexts. Use when testing skill discoverability and triggering accuracy.

---

## Must Activate (Should Trigger This Skill)

These phrases MUST cause the skill to be loaded:

1. "audit this repo for who writes to the database"
2. "who owns the report generation pipeline"
3. "is the users table really single-source"
4. "check for double writers on the config file"
5. "map the authority for all state mutations"
6. "what surfaces compete for the same output"
7. "audit this PR for authority conflicts"
8. "find competing pipelines for report generation"
9. "lifecycle audit — are hooks mutating state outside the pipeline"
10. "side effect audit for the sync module"
11. "responsibility map for this service"
12. "flow audit — trace who reads and writes the orders table"
13. "verify SSOT for the notification queue"
14. "change-audit this diff for new writers"

## Must NOT Activate (Should NOT Trigger This Skill)

These phrases describe different tasks that have their own skills:

1. "code review this PR" → use `code-review`
2. "clean up the code style" → use `refactor-clean`
3. "lint the codebase" → use project lint tools
4. "fix the formatting" → use `refactor-clean`
5. "performance optimization for slow queries" → use `db-performance`
6. "security audit for vulnerabilities" → use `security-auditor`
7. "improve test coverage" → use `test-coverage`
8. "refactor this module" → use `refactor-clean` or architecture skill
9. "naming conventions review" → use `code-review`
10. "architecture proposal for new feature" → use `architecture-designer`
11. "general code quality review" → use `code-review`
12. "check for code smells" → use `code-review`

## Borderline Cases (Context-Dependent)

| Phrase | Activate? | Condition |
|--------|-----------|-----------|
| "architecture review" | Only if asking about ownership/pipelines | If asking about general patterns → no |
| "dependency analysis" | Only if asking about who writes what | If asking about package deps → no |
| "technical debt" | Only if about structural drift between docs/code | If about style debt → no |
| "review this service" | Only if asking about its authority boundaries | If general code review → no |
| "check for race conditions" | Only if about competing writers on shared state | If about threading bugs → use `debug-helper` |
| "is this the right design" | No — this is architecture proposal | Use `architecture-designer` instead |
| "audit the build pipeline" | Only if asking about state mutation ownership | If asking about CI performance → no |
