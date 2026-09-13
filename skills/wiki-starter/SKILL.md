---
name: wiki-starter
description: "Bootstrap a new LLM-maintained wiki from scratch using Karpathy pattern with progressive enrichment. Triggers: create wiki, new wiki, start wiki, bootstrap wiki, init wiki."
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
---

# Wiki Starter v1.0

Bootstrap a new LLM-maintained knowledge base from scratch.
Follows Karpathy's LLM Wiki pattern with proven structural additions.

## When to Use

- Starting a new knowledge base for any domain
- Converting notes/documents into a structured wiki
- Setting up a research wiki for a project/exam/study

## Quick Start

```
create-wiki <domain-name> <path>
```

This creates the full directory skeleton and all starter files.

## Directory Skeleton

```
<wiki-root>/
├── CLAUDE.md              # Schema — LLM instructions (or WIKI-SCHEMA.md)
├── raw/                   # Immutable source documents
│   └── .gitkeep
├── wiki/
│   ├── index.md           # Master catalog (read first on every query)
│   ├── log.md             # Append-only activity log
│   ├── dashboard.md       # Dataview live queries (optional, Obsidian)
│   ├── analytics.md       # Charts visualization (optional, Obsidian)
│   ├── flashcards.md      # Spaced repetition cards (optional, Obsidian)
│   ├── summaries/         # One page per raw source
│   ├── concepts/          # Concept and framework pages
│   ├── entities/          # People, tools, organizations, products
│   ├── syntheses/         # Cross-cutting analyses and comparisons
│   └── journal/           # Research/session journal entries
│       └── template.md
```

## Bootstrap Procedure

Load `resources/bootstrap-procedure.md` for the full step-by-step.

## Core Concepts

### Three Operations

| Operation | Trigger | What Happens |
|-----------|---------|-------------|
| **Ingest** | "ingest raw/file.txt" | Read source → create summary → create/update concepts & entities → cross-link → update index & log |
| **Query** | Ask any question | Search wiki → synthesize answer with citations → optionally create synthesis page |
| **Lint** | "lint" or "health check" | Audit all pages for orphans, contradictions, missing links, incomplete sections, low-confidence claims |

### Frontmatter Standard

Every wiki page uses this frontmatter:

```yaml
---
title: "Page Title"
type: concept | entity | summary | synthesis | journal
tags: [tag1, tag2, tag3]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["raw/filename.txt"]
confidence: high | medium | low
---
```

### Confidence Levels

| Level | Meaning |
|-------|---------|
| **high** | Well-established, multiple corroborating sources, concrete examples |
| **medium** | Supported by sources but limited examples or single-source |
| **low** | Single mention, anecdotal, speculative |

### Linking Rules

- Obsidian-style: `[[concepts/concept-name]]`
- Relative paths from wiki root
- Every page links to at least one other page (no orphans)
- When mentioning a concept with a page, always link it

## Domain Customization

After bootstrap, customize these sections in the schema file:

1. **Purpose** — one-paragraph domain description
2. **Tagging taxonomy** — replace placeholder tags with domain-specific categories
3. **Page types** — add/remove types as needed (e.g., diseases/, treatments/)
4. **Required sections** — define what each page type must contain
5. **Naming conventions** — adjust for domain language (e.g., Spanish terms)

## Enrichment Add-ons (Optional)

These are NOT required for bootstrap but add value over time:

| Add-on | Description | Requires |
|--------|-------------|----------|
| `syntheses/` | Cross-cutting comparisons | 5+ concept pages |
| `journal/` | Research session tracking | Active research workflow |
| `flashcards.md` | Spaced repetition cards | Obsidian + SR plugin |
| `dashboard.md` | Live queries (orphans, confidence, tags) | Obsidian + Dataview |
| `analytics.md` | Visual charts (distribution, wordcloud) | Obsidian + Charts View |
| PubMed integration | Evidence-backed content | PubMed MCP server |
| Confidence tracking | Per-page evidence grading | Defined confidence levels |

## Resources

| Resource | When to Load |
|----------|-------------|
| `resources/bootstrap-procedure.md` | During wiki creation |
| `resources/page-templates.md` | When creating specific page types |
| `resources/lint-checklist.md` | During lint/health check |
| `resources/domain-customization.md` | When tailoring to a specific domain |
