# WIKI-SCHEMA.md Template

> Copy this to `{WIKI_ROOT}/WIKI-SCHEMA.md` and customize for your domain.
> Replace all `<placeholder>` values with your project-specific names.

## Directory Structure

```
<wiki-root>/
├── METHODOLOGY.md              # General wiki methodology (Karpathy pattern)
├── WIKI-SCHEMA.md              # This file — domain-specific conventions
├── index.md                    # Content catalog (read first on every query)
├── log.md                      # Append-only activity log
│
├── systems/                    # Concrete systems being documented
│   └── <system-name>.md        # One page per system
│
├── patterns/                   # Reusable design patterns
│   └── <pattern-name>.md       # One page per pattern
│
├── concepts/                   # Transversal concepts
│   └── <concept-name>.md       # One page per concept
│
└── references/                 # External sources
    ├── papers/                 # Academic papers, blog posts
    │   └── <paper-name>.md
    └── analyses/               # Technical analyses and reports
        └── <analysis-name>.md
```

## Page Types & Frontmatter

### System Pages (`systems/`)

```yaml
---
type: system
tags: [<domain>, <category>]
sources:
  - "[[path/to/source]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
---
```

### Pattern Pages (`patterns/`)

```yaml
---
type: pattern
tags: [architecture, design-pattern, <category>]
sources:
  - "[[path/to/source]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
---
```

### Concept Pages (`concepts/`)

```yaml
---
type: concept
tags: [concept, <category>]
sources:
  - "[[path/to/source]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
---
```

### Reference Pages (`references/`)

```yaml
---
type: reference
tags: [paper|analysis|report, <category>]
sources:
  - "[[url-or-path]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
---
```

## Cross-Reference Conventions

- Systems link to patterns they implement: `→ [[patterns/<pattern-name>]]`
- Patterns link to concepts they use: `→ [[concepts/<concept-name>]]`
- Concepts link to systems that exemplify them: `→ [[systems/<system-name>]]`
- References link to concepts/patterns they inform
- Use `## See Also` section on every page for navigation

## Naming Conventions

- **Files:** `kebab-case.md`
- **Tags:** `kebab-case`
- **Page titles:** Title Case
- **Cross-refs:** `→ [[page-name]]` (without .md extension)

## Exclusion List

Refs that are intentionally external or templated. Lint skips these.

```yaml
excluded_refs:
  # Template placeholders (arrow-style refs in documentation)
  - "→ [[resources/..."
  - "→ [[path/to/..."
  # External references pointing outside the wiki
  - "AGENTS.md"
  - "MEMORY.md"
  # Add project-specific external refs here
```

## Lint Configuration

```yaml
lint_config:
  staleness_days: 30        # Days before a page is flagged as stale
  orphan_check: true        # Enable orphan page detection
  bidirectionality: false   # Enable bidirectional ref check (expensive)
  max_findings_report: 50   # Stop reporting after N findings per category
```

## Quality Checklist (per page)

- [ ] Frontmatter complete and valid (type, tags, sources, created, updated, status)
- [ ] At least 1 source reference
- [ ] Cross-references to related pages
- [ ] `## See Also` section present
- [ ] Listed in `index.md`
- [ ] Status is not `draft` after review
