# Core Protocols

Init, query, and schema conventions for wiki-keeper.

## Init Protocol

Create a new wiki from scratch:

1. Create directory: `mkdir -p <WIKI_ROOT>/{systems,patterns,concepts,references/papers,references/analyses}`
2. Copy `resources/schema-template.md` → `{WIKI_ROOT}/WIKI-SCHEMA.md`
3. Copy `resources/methodology.md` → `{WIKI_ROOT}/METHODOLOGY.md`
4. Create `index.md` with section headers for each directory
5. Create `log.md` with header: `# Activity Log\n\nAppend-only chronological record.\n`
6. Commit to git

## Query Protocol

1. Read `index.md` to find relevant pages
2. Read candidate pages in full
3. Synthesize answer with `→ [[page]]` citations
4. If the answer is new/valuable, file it back as a new page

## Schema Conventions

### Page Types

| Type | Directory | Tags |
|------|-----------|------|
| `system` | `systems/` | `[domain, specific]` |
| `pattern` | `patterns/` | `[architecture, design-pattern]` |
| `concept` | `concepts/` | `[concept, domain]` |
| `reference` | `references/` | `[paper\|analysis, domain]` |
| `entity` | `entities/` | `[person\|tool\|decision\|meeting\|concept-external]` |

### Frontmatter Template

```yaml
---
type: system|pattern|concept|reference
tags: [primary, secondary]
sources:
  - "[[path/to/source]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active  # active | stale | needs-review | archived | deprecated
---
```

### Status Lifecycle

| Transition | Trigger |
|-----------|---------|
| active → stale | 30 days without update |
| stale → needs-review | Manual review flagged |
| needs-review → active | Content updated |
| any → archived | Manual archival |
| any → deprecated | Manual deprecation |

### Entity Pages (Optional)

Create `entities/` for typed knowledge about people, tools, decisions, meetings, and external concepts.

**Entity Types:** person, tool, decision, meeting, concept-external

**Entity Frontmatter:**
```yaml
---
type: entity
entity-type: person|tool|decision|meeting|concept-external
tags: [primary, secondary]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
# Per entity-type: person (role, org), tool (url, version),
# decision (decision-date, deciders, outcome), meeting (date, participants, action-items),
# concept-external (source-url, domain)
---
```

### Conventions

- Files: `kebab-case.md`
- Cross-refs: `→ [[page-name]]` (supports both `[[basename]]` and `[[path/basename]]` formats)
- Navigation: `## See Also` section on every page
- Naming: Title Case for page titles
- **Exclusion list:** External refs and template placeholders belong in `WIKI-SCHEMA.md` under `excluded_refs:` and are ignored by lint

See → [[resources/entity-templates]] for full per-entity templates and → [[resources/schema-template]] for the full WIKI-SCHEMA template.
