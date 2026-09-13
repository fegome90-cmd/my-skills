---
name: paper-writer-cli
description: "Use when Felipe wants to audit, review, create, or improve scientific documents (forms, manuscripts, protocols) using the paper-writer CLI pipeline. Treats documents like code: chunk, audit, fix, merge."
when: "When Felipe mentions paper-writer, auditing a form/manuscript, reviewing a scientific document, CIIC, formulario, protocolo de investigación, or wants to use the paper-writer CLI for document quality assurance."
examples:
  - "Audita el formulario CIIC"
  - "Revisa el manuscrito con paper-writer"
  - "Corre el pipeline de auditoría"
  - "Genera un protocolo con paper-writer"
  - "Pasa el formulario por el CLI"
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
  openclaw:
    requires:
      bins: ["uv"]
    emoji: "🔬"
---

# Paper-Writer CLI — Scientific Document Pipeline

Use the full paper-writer CLI to audit, create, or improve scientific documents. Treat every section like a code file in a PR review.

## Location

- **CLI repo**: `${PAPER_WRITER_PATH:-$HOME/Developer/paper-writer}`
- **Run with**: `cd "${PAPER_WRITER_PATH:-$HOME/Developer/paper-writer}" && uv run python -m cli.paper.main <command>`
- **Shortcut alias**: `PAPER="cd \"${PAPER_WRITER_PATH:-$HOME/Developer/paper-writer}\" && uv run python -m cli.paper.main"`
- **Project root**: Always pass `-C "${PAPER_WRITER_PATH:-$HOME/Developer/paper-writer}"` if running from outside the repo

## Pre-flight Check

**Before ANY mode, run doctor.** Abort if critical tools missing.

```bash
PAPER doctor
```

Expected: pandoc ✅, tectonic ✅, vale ✅, pdftotext ✅. Warnings (bibtex-tidy) are non-blocking.

If `doctor` fails → install missing dependency or abort with clear message to Felipe.

## Working Directory

**Never use `/tmp/`.** Use workspace-relative paths:

```
apps/pae-wizard/outputs/<project-name>/
├── source/           # Converted markdown
├── chunks/           # Split sections
├── reviews/          # Batch review files
├── corrected/        # Fixed chunks
├── audit/            # Consolidated report
└── output/           # Final rendered files
```

Each phase creates its subdirectory. If it exists from a prior run, confirm with Felipe before overwriting.

## Modes

| Mode | When | Entry Phase |
|------|------|-------------|
| **Audit** | Review existing document (DOCX/MD) | Phase 1 |
| **Create** | Build new document from research | Phase C1 |
| **Fix** | Apply corrections from audit report | Phase F1 |

---

## AUDIT MODE

### Phase 1: Convert & Discover

```bash
# Convert DOCX to clean markdown
pandoc "input.docx" -t markdown -o <project>/source/converted.md

# Or use existing markdown
cp /path/to/document.md <project>/source/converted.md
```

Read full document to identify section boundaries.

### Phase 2: Global Audit

Run ALL applicable audits on the full document:

```bash
PAPER audit prose <project>/source/converted.md --output terminal
PAPER audit writing-quality <project>/source/converted.md --output terminal
PAPER audit claims <project>/source/converted.md --output terminal
PAPER audit ethics <project>/source/converted.md --output terminal
PAPER audit citations <project>/source/converted.md --output terminal
PAPER audit tables <project>/source/converted.md --output terminal
PAPER audit reporting <project>/source/converted.md --output terminal
PAPER gate method <project>/source/converted.md
PAPER lint style
```

Skip if not applicable:
- `audit factuality` — requires `--evidence` (screened_evidence.json)
- `audit quality-appraisal` — requires `--evidence`
- `audit code-health` — requires Trifecta MCP graph

### Phase 3: Detect Document Type & Split

Read the source document and classify: **Research Form**, **Manuscript (IMRAD)**, **Case Report**, **Systematic Review**, **Study Protocol**, or **Custom**.

Classification heuristics (read `resources/section-splits.md` for full taxonomy):
- Has PICOT + variables table + cronograma → **Research Form** (20 chunks)
- Has IMRAD sections (Intro/Methods/Results/Discussion) → **Manuscript** (10 chunks)
- Has PROSPERO registration + search strategy → **Systematic Review** (12 chunks)
- Has single patient timeline + differential diagnosis → **Case Report** (6 chunks)
- Has randomization + DSMB + arms → **Study Protocol** (14 chunks)
- **Custom**: Ask Felipe for chunk boundaries, or split at `## ` headings

Create `<project>/chunks/` directory. Each chunk gets:

```yaml
---
section: N
section_name: "Section Title"
source: "Document Name"
audit_status: pending
known_issues: []
---
```

**Conversion rules:**
- Remove pandoc table artifacts (`+----+`, `|====`)
- Convert to proper markdown tables
- Keep citation markers `[N]` exactly as-is
- Keep bold as `**bold**`
- Convert ASCII Gantt to markdown table

### Phase 4: Bibliography Verification

Most error-prone section. Verify EVERY reference.

```bash
PAPER audit citations <file> --output json
```

Cross-check DOIs:
```bash
curl -s "https://api.crossref.org/works/{DOI}" | python3 -m json.tool
```

**Known error patterns:**
- Wrong DOI (points to different paper or erratum)
- Fabricated co-author names
- Duplicate reference numbering
- Missing DOI for papers that have one
- Placeholder author fields (`[Autor]`)
- Wrong article numbers
- Conference abstracts with wrong first author

After verification → renumber sequentially → mark each ref ✅/⚠️.

### Phase 4b: Zotero Integration (ONLY if Felipe requests)

```bash
PAPER zotero search <query>
PAPER zotero create items.json --collection <KEY>
PAPER zotero collections
```

**Gotchas:**
- `conferencePaper` type does NOT accept `publicationTitle` — use `conferenceName`
- POST to `/collections/{key}/items` may fail — use PATCH on each item's `collections` field
- Always have Crossref as fallback if Zotero API fails

### Phase 5: Section-by-Section Review

For each chunk (like a code review):
1. Read the chunk
2. Cross-reference with Phase 2 audit findings
3. Check internal consistency (citations ↔ bibliography, PICOT ↔ objectives, variables ↔ instruments)
4. Flag issues as TODO comments in the markdown
5. Update `audit_status`: pending → reviewed | corrected

Save findings per batch (3-4 sections per batch file). Naming: `batch{N}-review.md` (N starts at 1).
```
<project>/reviews/batch1-review.md
```

### Phase 5b: Cross-Section Consistency

After all chunks reviewed, check:
- Temporalidad mismatches (PICOT T vs Design timeline)
- Variable ↔ Instrument alignment
- Hypothesis ↔ Objective scope alignment
- Inclusion/exclusion ↔ Population definition
- Data retention mentioned in both Ethics AND Procedures
- Same treatment thresholds across sections

### Phase 6: Generate Corrected Document

1. Create `<project>/corrected/` with fixed chunks
2. Merge into single markdown
3. Re-run full audit suite (Phase 2) to verify fixes
4. Render:

```bash
# DOCX output
pandoc corrected.md -o <project>/output/corrected.docx

# PDF output
pandoc corrected.md -o <project>/output/corrected.pdf
```

### Error Handling

| Scenario | Action |
|----------|--------|
| `PAPER doctor` fails | Abort. Install missing dep or ask Felipe. |
| pandoc fails on DOCX | Try `--from docx` explicitly. If malformed, open with LibreOffice → save → retry. |
| `audit citations` timeout | Retry once. If fails, verify top-5 refs manually via Crossref curl. |
| Zotero API 401 | Check key expiry. Fall back to Crossref-only verification. |
| Zotero POST fails | Use PATCH on each item's `collections` field instead. |
| `gate method` false positives | Form layouts trigger STROBE items — flag as N/A, not failures. |
| Concurrent audit of 2 documents | Use separate project directories (never share `chunks/`). |

### Phase 7: Consolidated Report

Write `<project>/audit/CONSOLIDATED-REPORT.md` with:
- Executive summary (findings by severity)
- Findings table (ID, section, issue, proposed fix)
- Findings by section (totals)
- Citation renumbering impact
- Cross-section consistency issues
- Priority tiers (ethics → factual → methodological → completeness)

---

## CREATE MODE

### Phase C1: Project Init

```bash
PAPER init <project-name>
```

### Phase C2: Literature Search

**Step 1 — MCP PubMed (primary for biomedical):**
```bash
# MeSH vocabulary lookup first
PAPER mesh <term>

# Structured search with MeSH, filters, date ranges
pubmed__pubmed_search_articles --query "..." --mesh-terms [...] --date-range ...
pubmed__pubmed_fetch_articles --pmids [...]
pubmed__pubmed_fetch_fulltext --pmcids [...]
pubmed__pubmed_convert_ids --ids [...] --idtype doi
```

**Step 2 — CLI Semantic Scholar (secondary, for citation chaining):**
```bash
PAPER search <query> --max-results 50
PAPER screen <search-results>
PAPER chain <screened-set> --depth 2
PAPER export-bib <screened-set> --format bibtex
```

**Step 3 — Verify all DOIs via Crossref:**
```bash
curl -s "https://api.crossref.org/works/{DOI}" | python3 -m json.tool
```

**Step 4 — Zotero import (if requested):**
```bash
PAPER zotero create items.json --collection <KEY>
```

### Phase C3: Outline & Section Drafting

```bash
PAPER draft outline --sections <list>
```

Then draft section by section (each becomes a chunk):
```bash
PAPER draft <section-name> --references bib/
```

For each drafted section:
1. Verify all claims have citations
2. Cross-check statistics against source papers (PMIDs)
3. Run `PAPER audit prose <section>` for quality
4. Run `PAPER audit writing-quality <section>` for AI patterns

### Phase C4: Full Assembly & Audit

Merge all drafted sections → single document → switch to **Audit Mode** (Phases 1-7).

### Phase C5: Render & Export

```bash
PAPER render --format docx --csl styles/csl/vancouver.csl
PAPER verify  # full verification (requires pipeline stage: rendered)
```

Final output → `apps/pae-wizard/outputs/`.

---

## FIX MODE

### Phase F1: Parse Audit Report

Read `<project>/audit/CONSOLIDATED-REPORT.md` and extract:
- All 🔴 Critical findings (must fix)
- All 🟡 Warning findings (should fix)
- Priority order: ethics → citations → methodology → completeness

### Phase F2: Apply Fixes per Section

For each chunk with findings:
1. Read original chunk from `chunks/`
2. Check for existing corrected version in `audit/corrected/` — if none exists, create fix from scratch
3. Apply fixes listed in consolidated report
4. Write fixed version to `corrected/`
5. Update chunk frontmatter `audit_status: corrected`

**Fix order:**
1. Ethics section first (consent, committee, disclosure)
2. Bibliography (renumbering, wrong authors/DOIs)
3. Cross-section consistency (temporalidad, variable↔instrument)
4. Methodology (overfitting, scope, design consistency)
5. Formatting (word counts, placeholders)

### Phase F3: Merge & Re-audit

1. Merge corrected chunks → single markdown
2. Re-run full Phase 2 audit suite
3. Verify all 🔴 findings resolved
4. Accept remaining 🟡 as known issues or fix if trivial
5. Render final document

---

## CLI COMMAND REFERENCE

| Command | Purpose | Input | Use When |
|---------|---------|-------|----------|
| `init` | Create project | name | Starting new project |
| `search` | Literature search | query | Finding papers |
| `chain` | Citation chaining | screened set | Expanding corpus |
| `screen` | Screen results | search results | Filtering evidence |
| `export-bib` | Export BibTeX | screened set | Building bibliography |
| `draft` | Draft sections | outline | Writing |
| `protocol` | Reproducibility protocol | project state | Documentation |
| `lint` | Lint bib/style | project state | Before submission |
| `check` | Citation-ref consistency | project state | Before submission |
| `audit prose` | Prose quality | .md/.tex | Global audit |
| `audit claims` | Claim detection | .md/.tex | Global audit |
| `audit writing-quality` | AI writing patterns | .md/.tex | Global audit |
| `audit ethics` | AI disclosure | .md/.tex | Global audit |
| `audit citations` | Verify refs | .md/.tex | Bibliography |
| `audit tables` | Required tables/figures | .md/.tex | Global audit |
| `audit reporting` | Reporting checklists | project state | Method check |
| `audit factuality` | Claim-evidence | file + --evidence | When evidence available |
| `audit quality-appraisal` | Study quality | file + --evidence | When evidence available |
| `audit code-health` | Dead code | project state | Code projects |
| `gate` | Method gates | file | Method check |
| `import` | Import resources | file | Zotero, bib |
| `render` | Final output | project state + --csl | Submission |
| `trace` | Trace code structure | project state | Code projects |
| `graph-overview` | Trifecta graph health | project state | Debugging |
| `zotero` | Zotero ops | query/json | Reference management |
| `verify` | Full verification | project state | Final check |
| `doctor` | Env check | — | Troubleshooting |
| `thesaurus` | MeSH/DeCS normalization | term | Biomedical terms |
| `mesh` | MeSH import/lookup | term | Biomedical vocabulary |

---

## Severity Classification

| Level | Label | Action |
|-------|-------|--------|
| 🔴 | Critical/Major | Must fix before submission |
| 🟡 | Warning/Minor | Should fix |
| 🟢 | Info/Pass | OK or informational |

## Priority Tiers (for fixes)

1. **Ethics blockers** — consent order, committee, disclosure, retention, data protection
2. **Citation/factual correctness** — wrong authors, DOIs, renumbering errors
3. **Methodological rigor** — overfitting, scope mismatches, design inconsistencies
4. **Completeness/formatting** — placeholders, word counts, page limits
5. **Improvements** — scoring algorithms, qualitative detail, distress protocols

---

## Decision Rules

1. **Pre-flight check first** — `PAPER doctor` before any mode
2. **Workspace-relative paths** — never `/tmp/`
3. **Always run Phase 2 global audit before splitting** — catches systemic issues early
4. **Bibliography verification is NEVER optional** — highest error rate section
5. **Cross-section consistency is a separate pass** — don't rely on per-section review alone
6. **Re-audit after fixes** — every correction can introduce new issues
7. **Preserve citation markers exactly** during conversion — `[N]` format throughout
8. **MCP PubMed is primary for biomedical verification** — Crossref as fallback
9. **Zotero is optional unless Felipe requests it** — Crossref is the ground truth
10. **Detect document type before splitting** — don't assume Research Form

---

## Output Location

All outputs go to `${PAPER_WRITER_OUTPUT_DIR:-outputs/}` (or `apps/pae-wizard/outputs/` within the target workspace).
