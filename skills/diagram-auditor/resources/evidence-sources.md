# Evidence Sources Protocol

Pluggable adapter interface for external evidence verification during diagram audits.

## Overview

Step 3.1 (Evidence Enrichment) queries external sources to upgrade element tags. Reduces manual verification and provides source-backed evidence.

## Adapter Interface

Each adapter must implement:

```python
class EvidenceAdapter:
    name: str
    priority: int  # lower = checked first
    available: bool  # check before use
    
    def query(self, element_label: str, context: str) -> EvidenceResult:
        """Search for evidence supporting or refuting the element."""
        ...
```

```python
@dataclass
class EvidenceResult:
    found: bool
    source_url: str | None
    doi: str | None
    snippet: str | None
    confidence: float  # 0.0-1.0
    tag_upgrade: str | None  # e.g. "🟠→🟢"
```

## Registered Adapters

Universal local text and code search is the primary default baseline. External MCP adapters (academic search, PubMed, or memory) are optional domain-specific boosters when configured in the environment.

| Adapter | Tools | Priority | When to Use |
|---------|-------|----------|-------------|
| Local Codebase & Docs | `grep_search`, local file inspection | 1 (Default) | Project-specific architecture, code references, and local docs |
| Memory (Optional) | `engram__mem_search`, `memory_recall` | 2 (Optional) | Prior decisions, historical architecture logs if MCP enabled |
| Academic / Domain (Optional) | `pubmed_*`, `papers_*` | 3 (Domain) | External scientific/biomedical claims when domain MCPs present |

## Step 3.1 Procedure

For each element tagged 🟡 INFERRED or 🟠 ASSUMED (skip 🟢 and 🔴):

1. **Extract query terms** from element label + context
2. **Try adapters in priority order** until one returns `found=True`
3. **If found with confidence ≥ 0.7:** upgrade tag
   - 🟠 → 🟢 (confirmed by external source)
   - 🟡 → 🟢 (inference confirmed by evidence)
4. **If found with confidence < 0.7:** upgrade to 🟡 (partial confirmation)
   - 🟠 → 🟡 (assumption partially supported)
5. **If no adapter found evidence:** keep tag, add to grill questions
6. **Record evidence URL/DOI** in element mapping

### Query Construction

```
# For clinical elements
pubmed__pubmed_search_articles(
  query="[element_label] [diagram_context]",
  sources=["pubmed"],
  limit=3
)

# For academic elements
papers__search_papers(
  query="[element_label] [context]",
  sources=["pubmed", "openalex"],
  limit=3
)

# For project-specific
grep_search(query="[element_label]", path=".")
```

### Tag Upgrade Table

| Before | After (conf ≥ 0.7) | After (conf < 0.7) | After (not found) |
|--------|---------------------|---------------------|-------------------|
| 🟢 CONFIRMED | — (skip) | — (skip) | — (skip) |
| 🟡 INFERRED | 🟢 CONFIRMED | 🟢 CONFIRMED | 🟡 INFERRED |
| 🟠 ASSUMED | 🟢 CONFIRMED | 🟡 INFERRED | 🟠 ASSUMED → grill |
| 🔴 FABRICATED | — (skip, never auto-upgrade) | — (skip) | — (skip, remove) |
| ⚪ OUTDATED | — (skip, already corrected) | — (skip) | — (skip) |

## Oncology-Specific Patterns

When auditing oncology diagrams, use MeSH terms:

```python
# TNM staging claims
pubmed__pubmed_search_articles(
  query="TNM staging breast cancer",
  meshTerms=["Breast Neoplasms/pathology", "Neoplasm Staging"],
  limit=3
)

# Treatment protocol claims
pubmed__pubmed_search_articles(
  query="[drug_name] [cancer_type] adjuvant chemotherapy",
  meshTerms=["Antineoplastic Combined Chemotherapy Protocols"],
  limit=3
)

# Nursing care claims
pubmed__pubmed_search_articles(
  query="oncology nursing [procedure_name]",
  meshTerms=["Nursing Process", "Oncologic Nursing"],
  limit=3
)
```

## Evidence Mapping Format (Extended)

```
ELEMENT-XX: [label]
  Tag: [original] → [upgraded]
  Evidence source: [adapter_name]
  Source URL: [url]
  DOI/PMID: [id]
  Confidence: [0.0-1.0]
  Snippet: "[relevant excerpt]"
```

## Graceful Degradation

| Scenario | Behavior |
|----------|----------|
| Adapter unavailable | Skip, try next in priority order |
| All adapters unavailable | Proceed as manual (Step 3 without enrichment), add note |
| Rate limit / timeout | Skip adapter, try next, log warning |
| Evidence conflicts (source A says X, B says Y) | Keep highest-priority result, flag conflict in report |

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|--------------|-----|
| Query too broad ("cancer treatment") | Returns noise, not evidence | Use specific terms from element + context |
| Auto-upgrade 🔴 FABRICATED | Fabricated claims can't be evidence-confirmed | Never auto-upgrade 🔴, always remove |
| Trust single source blindly | One paper ≠ consensus | Require confidence ≥ 0.7 OR 2+ sources |
| Query every element | Wasteful, slow | Only query 🟡/🟠 (skip 🟢) |

---

**Version:** 1.0.0 | **Updated:** 2026-06-02
