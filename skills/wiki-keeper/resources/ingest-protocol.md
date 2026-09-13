# Ingest Protocol — Detailed Guide

Step-by-step process for ingesting a source into the wiki.

## Step 1: Detect Source Type

| Type | Signals | Primary Directory |
|------|---------|-------------------|
| **code** | `.py`, `.ts`, `.js`, `go`, etc. files, repo directory | `systems/` |
| **doc** | `.md`, `.txt`, README files, skill docs | `patterns/` or `concepts/` |
| **config** | `.yaml`, `.json`, `.toml` config files | `systems/` or `concepts/` |
| **paper** | URLs, PDFs, academic references | `references/papers/` |
| **analysis** | Technical writeups, reports | `references/analyses/` |

A single source can produce pages in multiple directories.

## Step 2: Read and Analyze

**Mandatory: Read EVERY relevant file before writing anything.**

### Code Sources
- Identify key interfaces, classes, functions
- Extract architecture patterns (how modules connect)
- Note configuration options and their effects
- Capture error handling patterns
- Look for design decisions embedded in code comments

### Doc Sources
- Extract key takeaways (not summaries — actionable insights)
- Identify patterns and conventions
- Note any rules or constraints
- Flag open questions or ambiguities

### Paper Sources
- Extract methodology
- Key findings and results
- Relevance to wiki domain
- Limitations and caveats

### Config Sources
- Document each field and its purpose
- Note defaults and overrides
- Explain relationships between config sections

## Step 3: Determine Target Pages

Ask:
- Is this a concrete system? → `systems/`
- Is this a reusable pattern? → `patterns/`
- Is this a transversal concept? → `concepts/`
- Is this an external reference? → `references/`

A single source often maps to multiple pages:
- A codebase → system page + pattern pages for design patterns found
- A paper → reference page + concept pages for key ideas

## Step 4: Write the Page

### Structure

```markdown
---
type: <system|pattern|concept|reference>
tags: [primary, secondary]
sources:
  - "[[path/to/source]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
---

# Page Title

Brief description of what this page covers.

## Overview
High-level summary.

## Key Details
<type-specific content>

## Code Examples (if from code source)
```language
// Real code from actual source files
```

## See Also
- → [[related-page-1]]
- → [[related-page-2]]
```

### Rules
- Code snippets MUST come from actual source files — copy-paste, never fabricate
- Include file paths in code snippets for traceability
- Cross-references MUST point to pages that actually exist
- If a related page doesn't exist yet, note it as a TODO — don't create a broken ref

## Step 5: Update Navigation Files

### index.md

Add under the appropriate directory section:
```markdown
- [page-name](path/to/page.md) — One-line summary of what this page covers
```

### log.md

Append at the bottom:
```markdown
## [YYYY-MM-DD] ingest | Source Title
- Created: [[path/to/new-page.md]]
- Updated: [[path/to/existing-page.md]] (added cross-ref)
- Type: code|doc|paper|config
```

## Common Mistakes

1. **Inventing content** — always read the source first
2. **Giant pages** — split into focused pages, use cross-refs
3. **Missing frontmatter** — every page needs it
4. **No See Also** — every page needs navigation
5. **Forgotten index update** — pages not in index are invisible
6. **Processing multiple sources at once** — one at a time for quality
