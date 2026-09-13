# Lint Checklist

Complete wiki health-check. Run automated checks first, then manual review.

## Output Classification

All lint findings MUST be classified before reporting or fixing:

| Category | Meaning | Action |
|----------|---------|--------|
| `SCRIPT_BUG` | Detection logic is wrong | Fix the lint script first |
| `TEMPLATE_PLACEHOLDER` | Intentional template ref | Add to `excluded_refs:` in WIKI-SCHEMA |
| `REAL_DEBT` | Actual wiki issue | Fix the wiki page |

**Format:** `SEVERITY \| CATEGORY \| FILE \| DETAIL`

## Validation Step

**Before any fix pass, spot-check 5 random findings by hand.** Lint output is hypothesis, not diagnosis. If >50% of spot-checked items are false positives, stop and fix the lint script first.

## Automated Checks

### 0.5. Memory-Wiki Validation (Optional)
- **Severity:** Warning
- **Prerequisite:** `openclaw` CLI installed (`npm i -g openclaw`)
- **Command:**
  ```bash
  ./scripts/wiki-memory-wiki-lint.sh --full
  ```
- **What it adds:** Contradiction detection, claim health scoring, provenance gaps —
  capabilities beyond wiki-keeper's native checks. See `memory-wiki-integration.md`
  for details.
- **Classification:** Classify findings as `REAL_DEBT`, `SCRIPT_BUG`, or
  `TEMPLATE_PLACEHOLDER` before acting on them. Spot-check 5 random findings.
- **Catches:** Cross-page contradictions, stale claims, low-confidence pages.
- **Note:** ~3-4 min for 39 pages. Use `--watch` to avoid re-ingesting on each run.

### 1. Frontmatter Present
- **Severity:** Critical
- **Command:**
  ```bash
  find "$WIKI_ROOT" -name "*.md" \
    ! -name "index.md" ! -name "log.md" ! -name "WIKI-SCHEMA.md" ! -name "METHODOLOGY.md" \
    -exec sh -c 'head -1 "$1" | grep -q "^---" || echo "NO FRONTMATTER: $1"' _ {} \;
  ```
- **Fix:** Add frontmatter block with type, tags, sources, created, updated, status.
- **Catches:** Pages created in a hurry without metadata.

### 2. Frontmatter Fields Complete
- **Severity:** Critical
- **Command:**
  ```bash
  for f in $(find "$WIKI_ROOT" -name "*.md" ! -name "index.md" ! -name "log.md" ! -name "WIKI-SCHEMA.md" ! -name "METHODOLOGY.md"); do
    for field in "type:" "tags:" "sources:" "created:" "updated:" "status:"; do
      sed -n '1,/^---$/p' "$f" | head -n -1 | grep -q "$field" || echo "MISSING $field in $f"
    done
  done
  ```
- **Fix:** Add missing fields with appropriate values.
- **Catches:** Partially filled frontmatter.

### 3. See Also Section
- **Severity:** Medium
- **Command:**
  ```bash
  find "$WIKI_ROOT" -name "*.md" \
    ! -name "index.md" ! -name "log.md" ! -name "WIKI-SCHEMA.md" ! -name "METHODOLOGY.md" \
    -exec sh -c 'grep -q "^## See Also" "$1" || echo "NO SEE ALSO: $1"' _ {} \;
  ```
- **Fix:** Add `## See Also` with links to related pages.
- **Catches:** Pages without navigation anchors.

### 4. Index Completeness
- **Severity:** Medium
- **Command:**
  ```bash
  for f in $(find "$WIKI_ROOT" -name "*.md" ! -name "index.md" ! -name "log.md" ! -name "WIKI-SCHEMA.md" ! -name "METHODOLOGY.md"); do
    basename=$(basename "$f" .md)
    grep -q "$basename" "$WIKI_ROOT/index.md" || echo "NOT IN INDEX: $f"
  done
  ```
- **Fix:** Add entry to index.md under the correct directory section.
- **Catches:** Pages that exist but aren't discoverable.

### 5. Orphan Pages
- **Severity:** Low
- **Command:**
  ```bash
  for f in $(find "$WIKI_ROOT" -name "*.md" ! -name "index.md" ! -name "log.md" ! -name "WIKI-SCHEMA.md" ! -name "METHODOLOGY.md"); do
    basename=$(basename "$f" .md)
    count=$(grep -r "\[\[${basename}\]\]" "$WIKI_ROOT" --include="*.md" | grep -v "^$f:" | grep -v "index.md" | wc -l | tr -d ' ')
    [ "$count" -eq 0 ] && echo "ORPHAN: $f"
  done
  ```
- **Note:** Also checks `[[path/${basename}]]` format via basename match.
- **Fix:** Add cross-references from related pages, or merge into another page.
- **Catches:** Isolated pages that no other page links to.

### 6. Broken Cross-References
- **Severity:** Critical
- **Command:**
  ```bash
  grep -roh "\[\[[^]]*\]\]" "$WIKI_ROOT" --include="*.md" | sort -u | while read ref; do
    target=$(echo "$ref" | tr -d '[][')
    # Handle both [[basename]] and [[path/basename]] formats
    basename=$(basename "$target")
    # Skip excluded refs (defined in WIKI-SCHEMA.md excluded_refs:)
    find "$WIKI_ROOT" -name "${basename}.md" | grep -q . || echo "BROKEN: $ref"
  done
  ```
- **Note:** Checks both `[[basename]]` and `[[path/basename]]` formats. Excludes refs listed in WIKI-SCHEMA `excluded_refs:`.
- **Fix:** Update the reference to point to an existing page, or create the missing page.
- **Catches:** Stale links from renames or typos.

### 7. Invalid Status Values
- **Severity:** Low
- **Command:**
  ```bash
  grep -rn "^status:" "$WIKI_ROOT" --include="*.md" | grep -v "active\|stale\|needs-review\|archived\|deprecated"
  ```
- **Fix:** Correct to one of: active, stale, needs-review, archived, deprecated.
- **Catches:** Typos in status fields.

## Manual Checks

### 8. Contradictions Between Pages
- **Severity:** Critical
- **How:** Read overlapping pages and compare claims.
- **Fix:** Update the stale page, add a note about the correction.

### 9. Stale Claims vs Source
- **Severity:** High
- **How:** Pick claims from wiki pages and verify against actual source files.
- **Fix:** Update wiki to match reality.

### 10. Code Snippet Accuracy
- **Severity:** High
- **How:** Spot-check 3-5 code snippets against the referenced source files.
- **Fix:** Replace fabricated snippets with actual code.

### 11. Cross-Reference Bidirectionality
- **Severity:** Low
- **How:** If page A links to B, check if B links back to A (or references A in See Also).
- **Fix:** Add the reverse link where it makes sense.

### 12. Staleness Detection
- **Severity:** Warning
- **Threshold:** Read `staleness_days` from WIKI-SCHEMA `lint_config:` section (default: 30)
- **Command:**
  ```bash
  STALE_DAYS=$(sed -n 's/^.*staleness_days:[[:space:]]*//p' "$WIKI_ROOT/WIKI-SCHEMA.md" | head -1)
  STALE_DAYS=${STALE_DAYS:-30}
  CUTOFF=$(date -v-${STALE_DAYS}d +%Y-%m-%d 2>/dev/null || date -d "$STALE_DAYS days ago" +%Y-%m-%d)
  grep -rn "^updated:" "$WIKI_ROOT" --include="*.md" | while IFS=: read file line; do
    date=$(echo "$line" | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}')
    [ -n "$date" ] && [ "$date" \< "$CUTOFF" ] && echo "STALE ($date): $file"
  done
  ```
- **Fix:** Review page content; set `status: needs-review` if outdated.
- **Catches:** Pages that haven't been touched in 30+ days.

## Running the Full Lint

```bash
WIKI_ROOT="/path/to/wiki"
echo "=== Wiki Lint $(date +%Y-%m-%d) ==="
echo ""

echo "--- Frontmatter ---"
# Check 1 & 2 here

echo "--- See Also ---"
# Check 3 here

echo "--- Index ---"
# Check 4 here

echo "--- Orphans ---"
# Check 5 here

echo "--- Broken Refs ---"
# Check 6 here

echo "--- Status ---"
# Check 7 here

echo ""
echo "=== Manual checks needed: contradictions, stale claims, code accuracy, bidirectionality ==="
```
