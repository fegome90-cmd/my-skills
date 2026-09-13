# Lint Checklist

Audit wiki health. Fix what you can, report what needs human judgment.

## Checks

### 1. Index Completeness
- [ ] Every page in `wiki/` appears in `index.md`
- [ ] No pages listed in index that don't exist on disk
- [ ] Page counts in index header match actual file counts

### 2. Orphan Detection
- [ ] Every page has at least one inbound link from another page
- [ ] No page exists that no other page references
- [ ] Flag orphans — decide: link from relevant page, or delete

### 3. Frontmatter Validation
- [ ] Every page has valid YAML frontmatter
- [ ] Required fields present: title, type, tags, created, updated, confidence
- [ ] `sources` field references actual files in `raw/`
- [ ] `updated` date is not older than `created`
- [ ] Tags match the defined taxonomy

### 4. Cross-Link Integrity
- [ ] All `[[wiki/path]]` links point to existing pages
- [ ] No broken links (link target doesn't exist)
- [ ] Bidirectional links: if A links to B, B should reference A
- [ ] No self-references

### 5. Content Completeness
- [ ] Each page type has all required sections
- [ ] No empty sections (except intentional placeholders)
- [ ] No placeholder text left from templates

### 6. Confidence Audit
- [ ] Low-confidence pages identified
- [ ] Low-confidence pages have notes explaining why
- [ ] Suggestions for sources that could raise confidence

### 7. Contradiction Detection
- [ ] Same concept described differently across pages
- [ ] Conflicting claims flagged with page references
- [ ] Outdated information (pages not updated after new sources ingested)

### 8. Log Consistency
- [ ] Every page creation/update logged in `log.md`
- [ ] Log entries have timestamps
- [ ] No log entries for pages that don't exist

### 9. Naming Convention
- [ ] All filenames lowercase with hyphens
- [ ] No spaces or special characters in filenames
- [ ] Filename matches title slug

### 10. Raw Directory Integrity
- [ ] All `sources` references point to existing files in `raw/`
- [ ] No files in `raw/` have been modified (immutable rule)
- [ ] No raw files without at least one summary page

## Scoring

| Check | Weight | Status |
|-------|--------|--------|
| Index completeness | 15% | |
| Orphan detection | 15% | |
| Frontmatter | 10% | |
| Cross-links | 15% | |
| Content | 15% | |
| Confidence | 10% | |
| Contradictions | 10% | |
| Other | 10% | |

**Pass threshold:** 80% overall, no critical check failed.

## Critical Checks (must pass)
- Index completeness
- Cross-link integrity (no broken links)
- Raw immutability

## Auto-Fixable
- Add missing pages to index
- Fix filename casing
- Add missing `updated` timestamps
- Remove self-references

## Needs Human Judgment
- Orphan pages (keep or delete?)
- Contradictions (which version is correct?)
- Confidence disputes
- Tag taxonomy changes
