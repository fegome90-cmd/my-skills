# Real-World Examples

Examples from building a 27-page orchestration wiki. Your domain will differ — the process stays the same.

## Example: Init

Creating a new wiki for an orchestration system:

```
User: "I want a wiki for my orchestration tools"
→ mkdir -p wiki/{systems,patterns,concepts,references/papers,references/analyses}
→ Copy WIKI-SCHEMA.md template, customize domain tags
→ Create index.md with empty sections
→ Create log.md
→ git init && git add -A && git commit -m "wiki init"
```

Result: Empty wiki ready for ingestion.

## Example: Ingest (Code Source)

Ingesting a codebase with multiple interconnected systems:

```
User: "Ingest the gentle-ai codebase"
→ Read all .py files in the repo
→ Identified 3 systems: prompt-engine, safety-layer, response-formatting
→ Created systems/gentle-ai.md with:
  - Architecture overview with real code snippets
  - Interface definitions copied from source
  - Configuration options from actual config files
→ Extracted 2 patterns → patterns/rule-engine.md, patterns/progressive-disclosure.md
→ Updated index.md with 3 new entries
→ Updated log.md: ## [2026-03-15] ingest | gentle-ai codebase
```

**What worked:**
- Reading every file first (not skimming)
- One source at a time
- Splitting into system + pattern pages instead of one mega-page
- Real code snippets with file paths for traceability

**What didn't work:**
- Trying to ingest 2 sources in one pass (rushed, missed details)
- Writing before reading (invented a pattern that didn't exist in the code)

## Example: Lint

Running a health check on a 27-page wiki:

```
Results:
- 14 pages missing frontmatter → added frontmatter to all
- 1 page missing ## See Also → added with 3 cross-refs
- 3 orphan pages → added inbound links from related pages
- 2 broken cross-refs (from a rename) → updated references
- 0 contradictions found
- Status: all pages active after review
```

**Key learning:** Most issues were from early pages created before the schema was formalized. Running lint after establishing conventions catches these quickly.

## Example: Query

```
User: "How do the memory systems interact?"
→ Read index.md → find systems/dual-memory.md, systems/engram-memory.md, systems/trifecta-context.md
→ Read all three pages
→ Synthesize: Engram handles decisions (what/why), Trifecta handles code (how/code), dual-memory bridges them
→ Cite: → [[systems/dual-memory]], → [[systems/engram-memory]], → [[systems/trifecta-context]]
→ Answer is good enough to file back? Not this time — already well-documented.
```

**When to file back:** If the query reveals a gap (no page covers the answer) or synthesizes new insight (connecting dots across pages), create a new page.

## Example: Log Entry Format

```markdown
## [2026-03-15] ingest | gentle-ai codebase
- Created: systems/gentle-ai.md
- Created: patterns/rule-engine.md
- Created: patterns/progressive-disclosure.md
- Updated: index.md (3 entries)
- Type: code
- Pages touched: 3

## [2026-03-15] lint | full health check
- Fixed: 14 missing frontmatters
- Fixed: 1 missing See Also
- Fixed: 3 orphan pages
- Fixed: 2 broken refs
- Status: all clear
```

## Example: Large Ingest with Sub-Agent (Paperclip Wiki, 39 pages)

Ingesting ~125 markdown files from two sources (internal docs + community docs):

```
User: "Create a wiki from the Paperclip docs"
→ Phase 1: Spawn sub-agent with 15min timeout
→ Sub-agent read 20 internal docs from ~/Developer/paperclip/doc/
→ Created 19 pages (systems/, patterns/, concepts/, references/)
→ Lint: 100% clean

User: "Now ingest the community docs too"
→ Phase 2: Clone aronprins/paperclip-docs (~65 files, 12.5k lines)
→ Spawn sub-agent — timed out twice (A7 anti-pattern!)
→ Fell back to manual ingestion: read in batches, wrote pages directly
→ Created 13 new pages (guides/, concepts/, references/)
→ Updated 6 existing pages with new content from community docs
→ Lint: found 8 false-positive orphans (A8 anti-pattern)
→ Fixed by adding short-form refs to WIKI-SCHEMA excluded_refs
→ Final: 39 pages, 100% clean
```

**What worked:**
- Cloning the community docs repo locally instead of fetching each URL
- Reading source files in batches of 5 for efficiency
- Writing each page immediately to disk (not buffering)
- Manual fallback when sub-agents failed on large tasks

**What didn't work:**
- Relying on sub-agents for 65+ file ingests (timed out 2x)
- Lint scripts that didn't handle `[[dir/basename]]` ref format (40 false positives)
- Not updating index.md immediately after creating pages (pages became invisible)
