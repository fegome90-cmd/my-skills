# Gate Report Template

## Structure

The gate report follows this exact structure. Fill in `{placeholders}` from aggregation results.

---

```markdown
### SDD Gate Result

| Metric | Value |
|--------|-------|
| Change | {change-name} |
| Findings Reported | {total_findings} |
| Findings Discarded | {total_discarded} |
| Verification Rate | {reported / (reported + discarded) * 100}% |
| Agents Completed | {completed}/{dispatched} |
| Quorum | {valid}/{total} agents valid |
| Gate Decision | **{PASS | REVIEW | BLOCK | INCONCLUSIVE}** |

---

### Findings by Severity

#### CRITICAL ({count})
| ID | Category | Message | Location | Evidence | Recommendation |
|----|----------|---------|----------|----------|----------------|
| F-NNN | {category} | {message} | {location} | {evidence_quote} | {recommendation} |

#### HIGH ({count})
| ID | Category | Message | Location | Evidence | Recommendation |
|----|----------|---------|----------|----------|----------------|
| F-NNN | {category} | {message} | {location} | {evidence_quote} | {recommendation} |

#### MEDIUM ({count})
| ID | Category | Message | Location | Evidence | Recommendation |
|----|----------|---------|----------|----------|----------------|
| F-NNN | {category} | {message} | {location} | {evidence_quote} | {recommendation} |

#### LOW ({count})
| ID | Category | Message | Location | Evidence | Recommendation |
|----|----------|---------|----------|----------|----------------|
| F-NNN | {category} | {message} | {location} | {evidence_quote} | {recommendation} |

---

### Findings by Agent

| Agent | Findings | Discarded | Confidence | State |
|-------|----------|-----------|------------|-------|
| sdd-structure | {n} | {n} | {0.0-1.0} | {completed | timed_out | parse_failed} |
| sdd-design | {n} | {n} | {0.0-1.0} | {completed | timed_out | parse_failed} |
| sdd-risk | {n} | {n} | {0.0-1.0} | {completed | timed_out | parse_failed} |

---

### Recommended Actions

1. {Top finding — severity-first — with recommendation}
2. {Second finding — with recommendation}
3. {Third finding — with recommendation}

---

### Gate Decision

{PASS → "All clear. Proceed to sdd-tasks or sdd-apply."}
{REVIEW → "High-severity findings require attention. Fix before proceeding."}
{BLOCK → "Critical issues or >2 high findings. Must resolve before implementation."}
{INCONCLUSIVE → "Insufficient agent coverage. Re-run with longer timeout or different preset."}

Options:
1. **Fix issues** — Update artifacts, re-run gate
2. **Get details** — Ask about specific findings
3. **Proceed anyway** — Acknowledge risks (not recommended for BLOCK)
4. **Re-run** — With longer timeout or explore agents (for INCONCLUSIVE)

---

### Execution Metadata

| Agent | State | Duration | Parse Status | Findings | Discarded |
|-------|-------|----------|-------------|----------|-----------|
| sdd-structure | {state} | {duration_ms}ms | {ok | partial | failed} | {n} | {n} |
| sdd-design | {state} | {duration_ms}ms | {ok | partial | failed} | {n} | {n} |
| sdd-risk | {state} | {duration_ms}ms | {ok | partial | failed} | {n} | {n} |

**Artifacts Retrieved**: spec={yes/no}, design={yes/no}, tasks={yes/no}
**Fallback Events**: {oracle→explore fallback count, or "none"}
**Prompt Injection**: {sanitized patterns count, or "none detected"}
```

---

## Degraded Mode Details

When an agent times out or returns invalid/unparseable JSON, include this section in the report:

```markdown
### Degraded Agent Details

| Agent | Issue | Raw Preview | Action Taken |
|-------|-------|-------------|-------------|
| {agent_name} | {timeout/parse_failed} | {first 500 chars} | {synthetic F-000 created, excluded from stats} |
```

**Downgrade rules**:
- If `sdd-structure` or `sdd-risk` agent fails → downgrade overall recommendation by one level (PASS→REVIEW, REVIEW→BLOCK)
- If `sdd-design` agent fails → note reduced coverage, no automatic downgrade
- All degraded agents still count toward quorum check (2/3 agents must be valid)