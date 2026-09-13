# Papers MCP Protocol

## Overview

Native MCP tools for multi-platform academic search. Replaces manual curl/web_fetch to external APIs with structured tool calls.

**Tools available:** `papers__search_papers`, `papers__advanced_search`, `papers__fetch_paper`, `papers__fetch_latest`, `papers__list_categories`, `papers__smart_cache_search`, `papers__trend_analysis`, `papers__manage_cache`

## When to Use Papers MCP vs PubMed MCP vs web_search

| Scenario | Use |
|----------|-----|
| Biomedical + MeSH + PMC fulltext | **PubMed MCP** (`pubmed__*`) — primary for medical literature |
| Multi-platform discovery (OpenAlex, Semantic Scholar, bioRxiv, medRxiv, arXiv) | **Papers MCP** (`papers__*`) |
| General web surfacing, news, blogs | **web_search** |
| One specific paper by ID | `papers__fetch_paper` (multi-platform) or `pubmed__pubmed_fetch_articles` (PMID only) |
| Trend analysis over time | `papers__trend_analysis` |
| Check if we already found something | `papers__smart_cache_search` |
| DOI/PMID conversion | `pubmed__pubmed_convert_ids` |

## Search Strategy (Replaces Search Protocol Layers)

### Layer 1: Broad Discovery

```
papers__search_papers(
  query="[population] [intervention/outcome]",
  sources=["pubmed", "openalex", "semantic-scholar"],
  limit=20,
  field="all",
  sortBy="relevance"
)
```

### Layer 2: Targeted with Filters

```
papers__search_papers(
  query="[specific query]",
  sources=["pubmed"],
  categories=["oncology"],
  sortBy="date",
  sortOrder="desc",
  limit=10
)
```

### Layer 2.5: Deduplication

The MCP returns results with `id` (source-specific) and `doi`. Deduplicate by DOI first, then by title.

### Layer 3: Advanced Queries (Boolean)

```
papers__advanced_search(
  query="[population] AND [intervention] AND [outcome]",
  field="abstract",
  sources=["pubmed", "openalex"],
  fuzzyMatch=true,
  limit=10
)
```

### Layer 4: Full Metadata & Fulltext

```python
# Get detailed metadata
papers__fetch_paper(id="31488084", source="pubmed")

# Get fulltext (PMC only — use PubMed MCP for this)
pubmed__pubmed_fetch_fulltext(pmids=["31488084"])
```

### Layer 5: Snowball (Forward/Backward)

```
# Find related/citing papers (PubMed MCP)
pubmed__pubmed_find_related(pmid="31488084", relationship="similar")
pubmed__pubmed_find_related(pmid="31488084", relationship="cited_by")
pubmed__pubmed_find_related(pmid="31488084", relationship="references")
```

## Integration with Ranking (Phase 3)

### Extract from Papers MCP result

Each `papers__search_papers` result includes:

```json
{
  "id": "31488084",
  "title": "...",
  "authors": ["Author A", "Author B"],
  "abstract": "...",
  "published": "2025-06-02T...",
  "source": "pubmed",
  "doi": "10.xxxx/xxxxx",
  "url": "https://pubmed.ncbi.nlm.nih.gov/31488084/",
  "pdfUrl": "https://...",  // if open access
  "fullTextAvailable": true,
  "categories": ["oncology"]
}
```

**Mapping to ranking criteria:**

| Papers MCP field | Ranking use |
|-------------------|-------------|
| `abstract` | Population/intervention/outcome relevance (A, B, C) |
| `authors` | COI check (D sub-score) |
| `published` | Recency bias |
| `doi` | Citation verification gate |
| `source` | Source quality (pubmed > preprint) |
| `fullTextAvailable` | Fulltext availability for synthesis |
| `categories` | Topic alignment |

### Enriching with PubMed MCP

For Tier 1 candidates, cross-reference:

```
pubmed__pubmed_fetch_articles(pmids=["31488084"])  → full metadata, MeSH, grants
pubmed__pubmed_fetch_fulltext(pmids=["31488084"])    → structured JATS fulltext
```

## Cache Strategy

### Smart Cache (Semantic Search)

After initial searches, the MCP caches results. Use `papers__smart_cache_search` to find related papers across sessions without re-querying:

```
papers__smart_cache_search(
  query="breast cancer chemotherapy toxicity nursing",
  similarityThreshold=0.7,
  maxResults=10
)
```

### Cache Management

```
papers__manage_cache(action="stats")          # hit rate, size
papers__manage_cache(action="list", pattern="*breast*")  # specific entries
papers__manage_cache(action="clear")         # reset
```

## Trend Analysis

For literature matrix coverage or detecting emerging topics:

```
papers__trend_analysis(
  topic="immunotherapy nursing care",
  sources=["pubmed", "openalex"],
  period="year",
  granularity="month",
  limit=50
)
```

Returns growth rates, peak periods, keyword analysis.

## Source Selection Guide

| Source | Strengths | Limitations |
|--------|-----------|-------------|
| **pubmed** | Biomedical, MeSH, PMC links | Biomedical only |
| **openalex** | Broad coverage, author affiliations, concepts | No fulltext |
| **semantic-scholar** | Citation counts, recommendations, embeddings | Can rate-limit |
| **bioRxiv** | Biology preprints (latest) | Not peer-reviewed |
| **medRxiv** | Medical preprints (latest) | Not peer-reviewed |
| **arXiv** | Physics/CS preprints | Not biomedical |
| **crossref** | DOI metadata, retractions | Metadata only |
| **google-scholar** | Comprehensive citations | Rate-limited, less structured |

## Practical Example: Oncology Nursing Query

```python
# Step 1: Broad search across platforms
papers__search_papers(
  query="oncology nursing care plan chemotherapy management",
  sources=["pubmed", "openalex", "semantic-scholar"],
  limit=15,
  sortBy="relevance"
)

# Step 2: Filter to oncology category on PubMed
papers__search_papers(
  query="breast cancer adjuvant chemotherapy toxicity management nursing",
  sources=["pubmed"],
  categories=["oncology"],
  limit=10,
  sortBy="date",
  sortOrder="desc"
)

# Step 3: Boolean advanced search
papers__advanced_search(
  query="breast cancer AND (chemotherapy OR neoadjuvant) AND (toxicity OR adverse effects) AND (nursing OR management)",
  field="abstract",
  sources=["pubmed"],
  limit=10
)

# Step 4: Get full metadata for top papers
papers__fetch_paper(id="31488084", source="pubmed")
pubmed__pubmed_fetch_articles(pmids=["31488084", "39551558"])

# Step 5: Fulltext for synthesis
pubmed__pubmed_fetch_fulltext(pmids=["31488084"])

# Step 6: Snowball
pubmed__pubmed_find_related(pmid="31488084", relationship="cited_by", maxResults=10)

# Step 7: Cache check for future sessions
papers__smart_cache_search(query="oncology chemotherapy toxicity nursing")
```

## Replaces in search-protocol.md

| Old method | New MCP method |
|------------|----------------|
| `curl Semantic Scholar API` | `papers__search_papers(sources=["semantic-scholar"])` |
| `curl OpenAlex API` | `papers__search_papers(sources=["openalex"])` |
| `curl CrossRef API` | `papers__fetch_paper(source="crossref")` |
| `web_fetch pmc.ncbi.nlm.nih.gov` | `pubmed__pubmed_fetch_fulltext` |
| Manual dedup by script | `papers__search_papers` handles per-source; dedup by DOI in agent |
| `web_fetch` journal PDFs | `papers__search_papers` returns `pdfUrl` when available |

**Still use web_search** for general discovery, news, blog posts, and when MCP sources don't cover a niche.

---

**Version:** 1.0.0 | **Updated:** 2026-06-02 | **Source:** Papers MCP + PubMed MCP tools
