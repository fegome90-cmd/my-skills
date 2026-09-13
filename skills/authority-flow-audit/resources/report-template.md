# Report Template

## Required Report Structure

Every audit produced with this skill MUST follow this structure exactly.
Do not add sections, reorder, or omit sections. Use "N/A" for inapplicable fields.

---

```markdown
# Authority-Flow Audit Report

**Mode:** repo-audit | change-audit
**Scope:** [repository path or change identifier]
**Date:** [YYYY-MM-DD]
**Auditor:** [agent name or "automated"]

---

## 1. Verdict

[One sentence. One of:]
- HEALTHY: No authority conflicts, pipelines are single-source, SSOTs verified.
- NEEDS ATTENTION: Minor conflicts or ambiguities detected, no data loss risk.
- CRITICAL ISSUES FOUND: Double writers, race conditions, or authority vacuums exist.

[Brief justification — 2-3 lines maximum.]

---

## 2. Surface Inventory

| # | Surface | Type | File:Lines | Calls | Called By |
|---|---------|------|------------|-------|-----------|
| 1 | [name] | [type] | [path:range] | [outbound] | [inbound] |
| 2 | ... | ... | ... | ... | ... |

Types: function | method | cli | script | api | job | hook | daemon | handler | importer | test-fixture

**Change-audit delta markers:** Prefix each item with [NEW] [MODIFIED] [UNCHANGED-AFFECTED] [BASELINE]

---

## 3. Authority Table

| Surface | Type | Primary Action | Inputs | State Reads | State Writes | Artifacts Produced | Side Effects | Authority | Competes With | Pipeline Affected | Risk | Confidence | Evidence Class | Proposed Decision |
|---------|------|---------------|--------|-------------|-------------|-------------------|-------------|-----------|--------------|------------------|------|------------|----------------|------------------|
| [name] | [type] | [one line] | [consumes] | [reads] | [writes] | [outputs] | [external effects] | [auth class] | [surface or "none"] | [pipeline name] | [severity] | [high/medium/low] | [direct-write/call-chain/inferred/docs-only] | [keep/delegate/remove/investigate] |

Authority values: authoritative | delegated | reader-only | evidence | competing | legacy | ambiguous

**Change-audit delta markers:** Prefix each row with [NEW] [MODIFIED] [UNCHANGED-AFFECTED] [BASELINE]

---

## 4. Pipelines Detected

For each output artifact or state mutation:

### Pipeline: [artifact/state name]

| Path | Entry Point | Steps | Active | Authority | Notes |
|------|------------|-------|--------|-----------|-------|
| Official | [entry surface] | [surfaces in order] | yes/no | [surface name] | [notes] |
| [Alternative] | [entry surface] | [surfaces in order] | yes/no | [surface name] | [notes] |

Pipeline type: single-pipeline | official+tolerated | competing | orphaned | shadow

**Change-audit delta markers:** Prefix each pipeline/path with [NEW] [MODIFIED] [UNCHANGED-AFFECTED] [BASELINE]

---

## 5. Duplications and Conflicts

| # | Conflict Type | Surfaces Involved | State/Artifact | Evidence | Severity | Confidence | Evidence Class |
|---|--------------|------------------|---------------|----------|----------|------------|----------------|
| 1 | [type] | [surface names] | [contested] | [file:line refs] | [severity] | [high/medium/low] | [direct-write/call-chain/inferred/docs-only] |

Conflict types: double-writer | bypass | hidden-delegation | evidence-as-authority | ssot-violation | dangling-mutation | lifecycle-escape | pipeline-drift

**Change-audit delta markers:** Prefix each item with [NEW] [MODIFIED] [UNCHANGED-AFFECTED] [BASELINE]

---

## 6. Side Effects and Contention Points

| # | Side Effect | Triggering Surface | Target | Concurrent With | Coordination | Severity | Confidence | Evidence Class |
|---|-------------|-------------------|--------|----------------|-------------|----------|------------|----------------|
| 1 | [description] | [surface] | [file/table/queue] | [other surfaces] | [mechanism or "none"] | [severity] | [high/medium/low] | [direct-write/call-chain/inferred/docs-only] |

**Change-audit delta markers:** Prefix each item with [NEW] [MODIFIED] [UNCHANGED-AFFECTED] [BASELINE]

---

## 7. Proposed Official Entrypoints

For each output artifact that needs a single authority:

| Artifact/State | Proposed Authority | Current Authority | Rationale |
|---------------|-------------------|------------------|-----------|
| [name] | [surface name] | [current or "none/ambiguous"] | [why this surface should own it] |

**Change-audit delta markers:** Prefix each item with [NEW] [MODIFIED] [UNCHANGED-AFFECTED] [BASELINE]

---

## 8. Surfaces That Must Not Mutate Official State

| Surface | Currently Mutates | Should Be | Required Change |
|---------|------------------|-----------|----------------|
| [name] | [what it writes] | reader-only / delegated | [specific action needed] |

**Change-audit delta markers:** Prefix each item with [NEW] [MODIFIED] [UNCHANGED-AFFECTED] [BASELINE]

---

## 9. Prioritized Risks

| Priority | Risk | Severity | Impact | Effort to Fix | Depends On | Confidence | Evidence Class |
|----------|------|----------|--------|---------------|------------|------------|----------------|
| 1 | [description] | CRITICAL/HIGH/MEDIUM/LOW/INFO | [what breaks] | [S/M/L] | [prerequisites] | [high/medium/low] | [direct-write/call-chain/inferred/docs-only] |
| 2 | ... | ... | ... | ... | ... | ... | ... |

---

## 10. Recommended Intervention Order

1. **[Action]** — [why first, what it unblocks]
2. **[Action]** — [why second]
3. ...

- Each action references specific surfaces and artifacts
- Each action has a clear completion criterion
- Ordering reflects dependency chain (fix authority before removing duplicates)

---

## 11. Uncertainties and Evidence Gaps

| # | Uncertainty | What Cannot Be Determined | What Would Resolve It |
|---|------------|--------------------------|----------------------|
| 1 | [description] | [why evidence is insufficient] | [what tool/access/data would clarify] |

Common uncertainties:
- Runtime behavior only visible in production logs
- Scripts executed outside version control
- Manual database operations not tracked in code
- External service behavior not documented
- Race conditions only under specific load patterns

---

## 12. Authority Map (Optional)

Visual/text map showing which surface owns which artifact.

| Artifact | Owner Surface | Competing Writers | Pipeline Type |
|----------|--------------|-------------------|---------------|
| [artifact name] | [surface name] | [list or "none"] | [single-pipeline/official+tolerated/competing/orphaned/shadow] |

---

## 13. Pipeline Map (Optional)

For each output artifact, list all paths from entrypoint to write.

| Artifact | Path Name | Entrypoint → ... → Writer | Active | Authority |
|----------|-----------|---------------------------|--------|-----------|
| [artifact] | [path name] | [surface1] → [surface2] → [writer] | [yes/no] | [surface name] |

---

## Appendix: Methodology

- [ ] Phase 1: Surface Discovery — [tools used, files scanned]
- [ ] Phase 2: State Mapping — [state categories examined]
- [ ] Phase 3: Authority Assignment — [classification method]
- [ ] Phase 4: Pipeline Detection — [tracing method]
- [ ] Phase 5: Conflict Analysis — [heuristics applied]
- [ ] Phase 6: Report Generation — [template version]
```

---

## Confidence Levels

- **high**: grep-confirmed write operation or direct call chain visible in code
- **medium**: call chain partially traced or naming convention suggests pattern
- **low**: inferred from docs/naming only, no code evidence

## Evidence Classes

- **direct-write**: surface writes to target via confirmed grep (.save, .write, INSERT, UPDATE)
- **call-chain**: surface calls writer through intermediate functions, chain traced
- **inferred**: pattern suspected from structure/naming but not fully traced
- **docs-only**: claim exists only in documentation, not verified in code
