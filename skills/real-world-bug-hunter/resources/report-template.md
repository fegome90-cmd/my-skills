# Bug Hunt Report Template

Every bug hunt produces a structured report using this template. The consolidator (`scripts/hunt-consolidate`) aggregates individual agent findings into a unified report.

## Report Structure

```markdown
# Bug Hunt Report — <project> — <date>

## Executive Summary
- Agents deployed: <ripper, walker, sniper>
- Subsystems tested: <list>
- Total findings: X (Y CRITICAL, Z HIGH, W MEDIUM, V LOW, U INFO)
- Verdict: PASS | PASS WITH WARNINGS | FAIL

## Severity Definitions
| Severity | Meaning | Action Required |
|----------|---------|----------------|
| CRITICAL | Data loss, security breach, corruption in normal usage | Fix immediately, blocks release |
| HIGH | Silent failure, wrong output, crash in common scenario | Fix before next release |
| MEDIUM | Poor error handling, edge case failure, recoverable | Fix in current sprint |
| LOW | Cosmetic, theoretical-only, requires contrived input | Backlog |
| INFO | Observation, improvement suggestion, not a bug | Optional |

## The "Can a Real User Trigger This?" Filter
Every finding classified by user impact:
- YES — Normal user, normal usage → Fix it
- MAYBE — Power user, unusual but valid input → Investigate
- NO — Malicious/contrived scenario only → Report only

## Findings by Severity

### CRITICAL
| ID | Title | Subsystem | Agent | User Trigger? | Command | Expected | Actual |
|----|-------|-----------|-------|---------------|---------|----------|--------|
| C1 | ... | ... | ripper | YES | `memory ...` | ... | ... |

### HIGH
| ID | Title | Subsystem | Agent | User Trigger? | Command | Expected | Actual |
|----|-------|-----------|-------|---------------|---------|----------|--------|

### MEDIUM
(same table format)

### LOW
(same table format)

### INFO
(same table format)

## Findings by Subsystem
Grouped by subsystem for developers:
### <subsystem-name>
- <ID>: <title> — <severity>

## Agent Coverage Matrix
| Subsystem | Ripper | Walker | Sniper | Coverage |
|-----------|--------|--------|--------|----------|
| CRUD | ✓ | ✓ | ✓ | Full |
| ... | ... | ... | ... | ... |

## Reproduction Instructions
For each CRITICAL and HIGH finding, detailed steps:
### <ID>: <title>
1. Setup: `memory session start -p test-hunt`
2. Trigger: `memory save "api_key=EXAMPLE_KEY_REDACTED" -p test-hunt`
3. Verify: `memory search "api_key" -l 5`
4. Expected: content redacted
5. Actual: plaintext API key stored

## Recommendations
Priority-ordered fix recommendations with estimated impact.
```

## Severity Classification Rules

- **CRITICAL**: Any finding where real user data is lost, corrupted, or exposed. Any security vulnerability exploitable without special access.
- **HIGH**: Any finding where CLI silently produces wrong output, crashes, or fails to perform its documented function under normal usage.
- **MEDIUM**: Any finding where error handling is poor (raw tracebacks, misleading messages), or where edge cases fail but normal usage works.
- **LOW**: Cosmetic issues, theoretical vulnerabilities requiring contrived input, or inconsistencies that don't affect functionality.
- **INFO**: Patterns worth noting, improvement suggestions, architectural observations that aren't bugs.

## Cross-Validation Rules

When 2+ agents independently find the same bug:
- Mark as **CONFIRMED** with confidence HIGH
- Note which agents found it independently

When only 1 agent finds a bug:
- Mark as **UNCONFIRMED** with confidence MEDIUM
- Verify with a separate reproduction attempt
