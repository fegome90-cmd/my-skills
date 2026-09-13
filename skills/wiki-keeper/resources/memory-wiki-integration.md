# OpenClaw memory-wiki — Integration Guide

Use `openclaw wiki ingest + lint` as a complementary validation layer for our
Karpathy-style wiki. wiki-keeper remains the owner. memory-wiki adds capabilities
we don't have natively (contradiction detection, claim health, staleness scoring).

## Setup (DONE)

- Plugin: `memory-wiki` enabled, v2026.4.15
- Mode: `isolated` (own vault, no dependency on memory-core)
- CLI: `openclaw wiki` available at `/opt/homebrew/bin/openclaw`

## Script

**`scripts/wiki-memory-wiki-lint.sh`** — one-stop bridge between our wiki and openclaw.

```bash
# Full pipeline (ingest → lint → report → cleanup)
./scripts/wiki-memory-wiki-lint.sh --full

# Watch mode (ingest → lint, keep sources for re-linting)
./scripts/wiki-memory-wiki-lint.sh --watch

# Cleanup only (remove ingested sources, recompile)
./scripts/wiki-memory-wiki-lint.sh --cleanup

# Custom wiki root
./scripts/wiki-memory-wiki-lint.sh path/to/other/wiki --full
```

**Performance:** ~5s per page (openclaw startup overhead). 39 pages ≈ 3-4 min.
Use `--watch` to ingest once and lint multiple times without re-ingesting.

## Integration with wiki-keeper Lint Checklist

Add as **Phase 1.5** (optional) in the wiki-keeper lint workflow:

1. Run wiki-keeper automated checks (frontmatter, see-also, index, orphans, refs, status)
2. **Run `wiki-memory-wiki-lint.sh --full`** for contradiction detection + claim health
3. Classify findings (REAL_DEBT / SCRIPT_BUG / TEMPLATE_PLACEHOLDER)
4. Fix real issues using wiki-keeper methodology
5. Run wiki-keeper manual checks (contradictions, stale claims, code snippets)

memory-wiki's automated contradiction detection augments the manual check (Phase 8)
in the lint checklist.

## Pipeline Detail

### How it works

1. **Ingest:** Copies each `.md` into `~/.openclaw/wiki/main/sources/` with wrapped frontmatter
   - Excludes: `index.md`, `log.md`, `WIKI-SCHEMA.md`, `METHODOLOGY.md`, `.openclaw-wiki/`
   - Idempotent: re-ingesting the same file overwrites without duplicates
2. **Lint:** `openclaw wiki lint --json` analyzes the ingested copies
3. **Report:** Structured output with severity, category, and classification guide
4. **Cleanup:** `rm -rf ~/.openclaw/wiki/main/sources/ && openclaw wiki compile`

### Lint output categories

| Category | What it detects | Our action |
|----------|----------------|------------|
| `links` | Broken wikilinks between ingested pages | Fix ref or classify as TEMPLATE_PLACEHOLDER |
| `structure` | Schema/structure issues | Usually SCRIPT_BUG (different taxonomy) |
| `provenance` | Missing source attribution | Add `sources:` to frontmatter |
| `contradictions` | Competing claims across pages | REAL_DEBT — fix the wiki page |
| `open-questions` | Unresolved claims | Review and resolve or mark intentional |
| `quality` | Low-confidence pages | Review content freshness |

### Important: taxonomy mismatch

memory-wiki expects its own vault layout (`entities/`, `concepts/`, `syntheses/`).
Our wiki uses `systems/`, `patterns/`, `concepts/`, `references/` — different taxonomy.

**Impact:** Cross-directory links like `[[patterns/rule-engine]]` may be reported as
broken even when valid in our wiki. These should be classified as `SCRIPT_BUG` or
`TEMPLATE_PLACEHOLDER`.

## Commands Reference

```bash
# Status check
openclaw wiki status

# Health check
openclaw wiki doctor

# Lint (the key command for us)
openclaw wiki lint --json

# Search wiki content
openclaw wiki search "<query>"

# Read a page
openclaw wiki get <page-id>

# Compile digests
openclaw wiki compile
```

## What NOT to do

- Don't use `wiki init` on our vault (it has its own layout)
- Don't use `wiki apply` to edit our pages (use wiki-keeper instead)
- Don't use `wiki ingest` as primary ingest method (use wiki-keeper methodology)
- Don't enable bridge mode (we don't want memory-wiki importing from LanceDB into our wiki)
- Don't let memory-wiki manage our schema (frontmatter, cross-refs)

## What TO use it for

- `wiki lint --json` — contradiction detection, staleness, claim health
- `wiki search` — alternative search when wiki-keeper's grep isn't enough
- `wiki doctor` — periodic health check
- `wiki compile` — machine-readable digests of our content

## Known Limitations

- Taxonomy mismatch: our `systems/`, `patterns/`, `references/` vs memory-wiki's expected layout
- ~5s per page ingest overhead (openclaw startup)
- Contradiction detection works best with structured claims frontmatter (which we don't use yet)
- Broken link reports may include false positives due to different cross-ref conventions
