# Bootstrap Procedure

Step-by-step guide to create a new wiki from scratch.

## Step 1: Create Directory Skeleton

```bash
mkdir -p <wiki-root>/{raw,wiki/{summaries,concepts,entities,syntheses,journal}}
touch <wiki-root>/raw/.gitkeep
```

## Step 2: Create Schema File (CLAUDE.md or WIKI-SCHEMA.md)

Copy the template from page-templates.md and customize:

1. **Purpose section** — describe the domain in one paragraph
2. **Directory layout** — match the skeleton you created
3. **Page types** — define which types exist (default: concept, entity, summary, synthesis, journal)
4. **Required sections per type** — what each page must contain
5. **Tagging taxonomy** — domain-specific categories (3-8 tags each)
6. **Confidence levels** — use defaults or customize
7. **Workflows** — ingest, query, lint (copy from SKILL.md)
8. **Rules** — never modify raw/, always update index + log, etc.

## Step 3: Create Starter Files

### wiki/index.md

```markdown
# <Domain> Wiki — Index

> Created: YYYY-MM-DD
> Total: 0 pages

## Concepts

| Page | Summary |
|------|---------|
<!-- Auto-populated during ingest -->

## Entities

| Page | Summary |
|------|---------|

## Summaries

| Page | Source |
|------|--------|
```

### wiki/log.md

```markdown
# Activity Log

| Date | Action | Pages | Details |
|------|--------|-------|---------|
```

### wiki/journal/template.md

```markdown
---
title: "Journal Entry — YYYY-MM-DD"
type: journal
tags: [journal]
date: YYYY-MM-DD
concepts_used: []
result: ""
---

# Journal Entry — YYYY-MM-DD

## Setup
<!-- What were you investigating? What sources/pages informed you? -->

## Process
<!-- Steps taken, decisions made, why. Link concept pages. -->

## Result
<!-- Outcome, what you learned. -->

## What Went Well
-

## What Could Improve
-
```

## Step 4: Drop First Sources

Add initial documents to `raw/`:
- Text files, transcripts, articles, notes
- PDFs (if the LLM can read them)
- These are **immutable** — never modify after adding

## Step 5: First Ingest

```
ingest raw/first-source.txt
```

The LLM will:
1. Read the source completely
2. Create `wiki/summaries/<slug>.md`
3. Identify concepts and entities
4. Create/update concept and entity pages
5. Cross-link everything bidirectionally
6. Update index and log

## Step 6: Customize Domain

After first ingest, refine:
- Adjust tags based on what emerged from the source
- Add domain-specific page types if needed
- Update schema with learned naming conventions
- Define minimum content standards (like CONTENIDO-MINIMO.md)

## Step 7: Iterate

Repeat ingest for each source. Query to explore. Lint periodically.

## Bootstrap Checklist

- [ ] Directory skeleton created
- [ ] Schema file written with domain purpose
- [ ] Tagging taxonomy defined
- [ ] index.md created
- [ ] log.md created
- [ ] journal/template.md created
- [ ] First source dropped in raw/
- [ ] First ingest completed
- [ ] Cross-links verified
- [ ] Domain customization done
