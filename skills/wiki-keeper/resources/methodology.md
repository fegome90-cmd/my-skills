# Wiki Methodology

> Based on [Karpathy's llm-wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
> Adapted as a generic, domain-agnostic wiki methodology.

## Core Idea

A persistent, compounding knowledge base. The LLM **incrementally builds and maintains** structured markdown — not re-deriving everything on every query. Over time, cross-references accumulate, contradictions get flagged, and the wiki becomes a first-class project artifact.

## Three Layers

1. **Raw Sources** — Code, docs, papers, logs, configs. Read but never modified by the LLM.
2. **The Wiki** — LLM-generated structured markdown. System pages, pattern pages, concept pages, cross-references.
3. **The Schema** — `WIKI-SCHEMA.md` + `METHODOLOGY.md`. Conventions, templates, workflows.

## Three Workflows

### Ingest
Drop a source and request processing:
1. LLM reads the source thoroughly
2. Discusses key takeaways
3. Writes structured page(s) into the wiki
4. Updates `index.md` with new entries
5. Updates cross-references across existing pages
6. Appends entry to `log.md`

A single source may touch multiple pages. Process one source at a time for quality.

### Query
Ask questions against the wiki. The LLM searches relevant pages, synthesizes with citations. **Good answers get filed back** as new pages — explorations compound over time.

### Lint
Periodic health-check to maintain quality:
- Contradictions between pages
- Stale claims superseded by newer sources
- Orphan pages with no inbound links
- Missing cross-references
- Code examples that don't match actual source
- Incomplete frontmatter or missing `## See Also` sections

#### Two-Phase Lint Workflow

```
DETECT → CLASSIFY → VALIDATE → FIX → VERIFY
```

1. **Detect** — Run all automated lint checks
2. **Classify** — Categorize each finding as `SCRIPT_BUG | TEMPLATE_PLACEHOLDER | REAL_DEBT`
3. **Validate** — Spot-check 5 random findings by hand. If >50% are false positives, fix the lint script first
4. **Fix** — Address only `REAL_DEBT` items (fix scripts for `SCRIPT_BUG`, update exclusion list for `TEMPLATE_PLACEHOLDER`)
5. **Verify** — Re-run all checks to confirm no regressions

See → [[resources/anti-patterns]] for common pitfalls and → [[resources/lint-checklist]] for full checklist.

#### Incremental Improvement

Each improvement (new check, schema change, debt fix) must be independently verifiable. **After any change, re-run all existing checks** — this is the regression gate. Never batch multiple improvements without intermediate verification.

## Navigation Files

- **`index.md`** — Content catalog. Every page listed with link + one-line summary. Organized by directory. Updated on every ingest.
- **`log.md`** — Append-only chronological record. Format: `## [YYYY-MM-DD] ingest | Source Title`. Machine-parseable with grep.

## Key Principles

- The wiki is a **persistent, compounding artifact** — it grows smarter over time.
- **Human curates sources, directs analysis.** LLM does bookkeeping and synthesis.
- **Git gives version history** for free — every change is tracked.
- **Code examples reference actual source paths**, never invented.
- **One source at a time** — quality over throughput.
- **Read before write** — extract real content from sources.
