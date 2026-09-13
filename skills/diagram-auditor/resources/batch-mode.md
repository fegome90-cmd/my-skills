# Batch Audit Mode

Audit multiple diagrams in a single session with cross-diagram consistency analysis.

## When to Use

- Thesis/project with 5+ clinical flowcharts
- Wiki with multiple diagrams needing validation pass
- Sprint review of diagram deliverables

## Invocation Pattern

```
audit --batch "<glob-pattern>" --output-dir audits/
```

Example:
```
audit --batch "vault/wiki/diseases/*.md" --output-dir audits/
audit --batch "docs/diagrams/*.mmd" --output-dir audits/
```

## Procedure

### Step B1: Discover

1. Expand glob pattern → list of diagram sources
2. Classify each source type (`.mmd`, `.svg`, `.html`, `.md` with embedded, prose)
3. Skip non-diagram files (log skipped count)

### Step B2: Individual Audit

For each diagram, run Steps 0–4 of the standard audit process.

**Parallelization:** If using subagents, spawn one per diagram. Otherwise sequential.

### Step B3: Cross-Diagram Consistency

Check across ALL audited diagrams:

| Check | What | Severity |
|-------|------|----------|
| **Role alias conflict** | Same entity labeled differently across diagrams | 🔴 HIGH |
| **Orphan reference** | Diagram A references Diagram B role not found in B | 🟠 MEDIUM |
| **Terminology drift** | Same concept with different terms across diagrams | 🟡 LOW |
| **Broken cross-refs** | Diagram references a non-existent diagram | 🔴 HIGH |
| **Inconsistent verdict** | Same role 🟢 in one diagram, 🔴 in another | 🟠 MEDIUM |

#### Role Alias Conflict Detection

```
# Pseudocode
roles_by_diagram = {diagram: [role_labels]}
for role in union(all_roles):
    diagrams_with_role = [d for d in roles_by_diagram if role in d]
    if len(diagrams_with_role) > 1:
        labels = [roles_by_diagram[d][role] for d in diagrams_with_role]
        unique_labels = set(labels)
        if len(unique_labels) > 1:
            flag("ROLE_ALIAS_CONFLICT", role, unique_labels, diagrams_with_role)
```

Example conflict: "Nutricionista" in Diagram A, "Equipo Nutricional" in Diagram B → flag for stakeholder.

### Step B4: Summary Rollup

Produce aggregate report:

```markdown
# Batch Audit Summary

**Diagrams audited:** N
**Date:** YYYY-MM-DD
**Overall verdict:** [PASS / PASS-WITH-WARNINGS / FAIL]

## Individual Verdicts
| Diagram | Type | Elements | Verdict | Key Issue |
|---------|------|----------|---------|-----------|
| cancer-mama | Mermaid | 12 | PASS | — |
| nutrition-referral | SVG | 8 | PASS-WITH-WARNINGS | 2 🟡 |
| surgical-staging | Mermaid | 15 | FAIL | 3 🔴 |

## Cross-Diagram Issues
| Check | Severity | Details |
|-------|----------|---------|
| Role alias conflict | 🔴 | "Nutricionista" vs "Equipo Nutricional" in 2 diagrams |
| Terminology drift | 🟡 | "TNM staging" vs "estadificación TNM" |

## Statistics
- Total elements audited: N
- 🟢: N (X%) | 🟡: N (X%) | 🟠: N (X%) | 🔴: N (X%) | ⚪: N (X%)
- Consistency issues: N
```

### Step B5: Persist

Persist batch result:
```
memory_save(
  type: "pattern",
  topic_key: "audit/batch-{date}",
  content: "Batch audit of N diagrams. Verdicts: PASS=N PASS-WARN=N FAIL=N. Cross-issues: N."
)
```

## Wiki Integration

After batch audit, update wiki log with summary entry. Flagged diagrams get `status: needs-review` in frontmatter.

## Edge Cases

| Case | Behavior |
|------|----------|
| Empty glob match | Report 0 diagrams, suggest pattern |
| Mix of types (SVG + Mermaid) | Process each with appropriate Step 0 |
| One diagram SYNTAX-FAIL | Skip content audit, include in summary |
| All diagrams PASS | Report "All clear", persist, move on |
| >50% FAIL | Stop batch, report blocker, do not continue |

---

**Version:** 1.0.0 | **Updated:** 2026-06-02
