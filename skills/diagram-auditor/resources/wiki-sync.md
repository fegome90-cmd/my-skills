# Wiki Sync Protocol

Persist audit results to the wiki for durability and cross-reference integrity.

## Overview

After Step 5 (single audit) or Step B4 (batch rollup), sync results to the wiki. This makes audit state survive beyond memory and catches orphan references.

## Step 5.5: Wiki Sync (Single Diagram)

### 5.5.1: Update Diagram Page Frontmatter

Add or update audit metadata in the diagram's wiki page:

```yaml
---
audit_state: audited
audit_date: 2026-06-02
audit_verdict: PASS
audit_elements: 12
audit_confirmed: 10
audit_inferred: 2
audit_assumed: 0
audit_fabricated: 0
audit_version: 1.4.0
---
```

### 5.5.2: Append Audit Log Entry

```markdown
## Audit Log

### 2026-06-02 — PASS
- **Elements:** 12 (🟢10 🟡2 🟠0 🔴0 ⚪0)
- **Evidence sources:** PubMed (2 verified), Papers (1 verified)
- **Key findings:** 2 elements upgraded 🟡→🟢 via PubMed evidence
- **Actions:** Labels updated, no structural changes
```

### 5.5.3: Orphan Detection

After removing 🔴 FABRICATED elements, check if any wiki pages reference the removed element:

```
wiki_search(query="[removed_element_label]")
```

If found → flag as orphan reference in audit report. Wiki-keeper can clean up.

## Step B5.5: Wiki Sync (Batch)

After batch rollup (Step B4):

1. **Update each diagram page** individually using Step 5.5.1 and 5.5.2
2. **Create/update batch summary page** at `wiki/diagram-audits/YYYY-MM-DD.md`:
   ```markdown
   # Batch Audit — 2026-06-02
   
   **Diagrams:** N audited
   **Overall:** PASS=N PASS-WARN=N FAIL=N
   
   ## Individual Results
   | Diagram | Verdict | Elements | Key Issue |
   |---------|---------|----------|-----------|
   
   ## Cross-Diagram Issues
   | Issue | Severity | Diagrams |
   |-------|----------|----------|
   ```
3. **Run wiki lint** if available:
   ```
   Read wiki-keeper skill → execute lint checklist
   Check for orphan references from removed elements
   ```

## Integration with wiki-keeper

After wiki sync, the wiki-keeper lint cycle will automatically:
- Detect stale `audit_state: needs-review` pages
- Verify frontmatter consistency
- Catch orphan references from removed elements

No special trigger needed — just ensure wiki pages are updated.

## Graceful Degradation

| Scenario | Behavior |
|----------|----------|
| Wiki tools unavailable | Skip wiki sync, persist to engram only, add note to report |
| Page doesn't exist | Create with audit metadata + audit log |
| Page exists but no frontmatter | Add frontmatter block with audit fields |
| Batch creates 10+ pages | Spread writes, don't overwhelm wiki |

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|--------------|-----|
| Overwrite entire page | Destroys non-audit content | Only update frontmatter + append audit log |
| Skip wiki sync for FAIL | FAIL diagrams need wiki tracking most | Always sync, mark clearly |
| Create audit pages outside wiki | Orphan metadata | Write to wiki directory only |
| No audit_version field | Can't detect stale audits | Always include skill version |

---

**Version:** 1.0.0 | **Updated:** 2026-06-02
