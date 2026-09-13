# Explore Agent Fallback Behavior

When `oracle` subagent type is unavailable (API key invalid, service down), the gate automatically falls back to `explore` subagent type with the same prompt.

## Behavioral Differences

| Aspect | Oracle Agent | Explore Agent |
|--------|--------------|---------------|
| **Response format** | Structured JSON (prose may exist) | More verbose, conversational, may include prose before/after JSON |
| **JSON duplication** | Rare | Often duplicates JSON block in `<answer>` tags + bare code block |
| **Findings schema** | Expected: `object[]` (with id, severity, etc.) | May return: `string[]` instead of `object[]` |
| **Confidence scores** | Numeric 0-1 | May omit or return non-numeric values |
| **Quality** | Structured rigor | Functionally equivalent, may lack structured rigor |

## Schema Normalization (Phase 3)

If `findings` is `string[]` instead of `object[]`, normalize each finding:

```python
{
    "id": "F-NNN",
    "severity": "MEDIUM",  # default for normalized
    "category": "explore_finding",
    "message": <the string>,
    "location": "unknown",
    "recommendation": "Review manually"
}
```

Log a MEDIUM finding: `{id: "F-SCHEMA", severity: "MEDIUM", category: "parse", message: "Agent returned string[] findings — normalized to object[]"}`

## Performance

Explore agents may have different latency characteristics. Default timeout (90s) should suffice, but may adjust if needed.

## Reporting

When fallback occurs, note in Execution Metadata:
```
Fallback Events: oracle → explore for {agent_name}, reason: "API key invalid"
Effective: sdd-gate (2/3 oracle, 1/3 explore)
```
