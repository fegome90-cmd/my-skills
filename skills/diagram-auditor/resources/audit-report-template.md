# Audit Report Template

## Report Structure

```markdown
# Diagram Audit Report

**Diagram:** [name]
**Date:** [YYYY-MM-DD]
**Elements audited:** N
**Verdict:** [PASS / PASS-WITH-WARNINGS / FAIL / SYNTAX-FAIL]

## Summary
| Tag | Count | Percentage |
|-----|-------|-----------|
| 🟢 CONFIRMED | X | X% |
| 🟡 INFERRED | X | X% |
| 🟠 ASSUMED | X | X% |
| 🔴 FABRICATED | X | X% |
| ⚪ OUTDATED | X | X% |

**DRAFT check:** {N}/{total} ({X}%) elements 🟡 or worse → {DRAFT if >50% | OK}

## Findings

### 🔴 FABRICATED (must fix)
- ELEMENT-XX: [what's wrong] → [suggested fix]

### 🟠 ASSUMED (flag for confirmation)
- ELEMENT-XX: [what's assumed] → [question to ask]

### 🟡 INFERRED (verify when possible)
- ELEMENT-XX: [what's inferred] → [source of inference]

### ⚪ OUTDATED (replace)
- ELEMENT-XX: [old info] → [corrected info]

## Questions for Stakeholders
1. [Specific question about ELEMENT-XX]
2. [Specific question about flow/role]

## Delivery Readiness
- [ ] All 🔴 elements resolved
- [ ] All ⚪ elements corrected
- [ ] All 🟠 elements confirmed or replaced with TBD
- [ ] All 🟡 elements flagged for future verification
- [ ] Diagram legend includes confidence levels
```

## Evidence Mapping Format

For each element in Step 3:

```
ELEMENT-XX: [label]
  Tag: [🟢/🟡/🟠/🔴/⚪]
  Source: [who said it / where it came from]
  Confidence: [high/medium/low]
  Action: [keep / flag / replace / remove]
  Correction: [if applicable]
```

## Memory Persistence Format

After report generation, persist audit state:

```
memory_save(
  type: "pattern",
  topic_key: "audit/diagram-{sanitized-name}",
  content: "**What**: Audit of {diagram-name} — verdict: {verdict}, elements: {N}
**Why**: Track diagram validation state across sessions
**Where**: skills/diagram-auditor
**Learned**: tags: confirmed={N} inferred={N} assumed={N} fabricated={N} outdated={N} source={mermaid|embedded|prose|svg} syntax_valid={true|false|null} version=1.2.0"
)
```

If memory tools unavailable → skip persistence, add note to report: "Audit state not persisted (memory tools unavailable)."
