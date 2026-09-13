# Autoresearch: Optimize deduplicate() in literature-search scoring engine

## Objective

Optimize the `deduplicate()` function in `resources/scoring.py` to handle large paper sets (1000+) efficiently, while maintaining correctness and stdlib-only constraint.

## Metrics

- **Primary**: `dedup_µs` (µs, lower is better) — time to deduplicate 1000 papers with mixed DOI/PMID/title scenarios
- **Secondary**: `throughput_papers_s` (papers/second, higher is better) — throughput metric derived from primary

## How to Run

```bash
./autoresearch.sh
```

Outputs `METRIC dedup_µs=<value>`.

Checks script (runs automatically after each pass):

```bash
./autoresearch.checks.sh
```

## Files in Scope

| File | Purpose |
|------|---------|
| `resources/scoring.py` | `deduplicate()` function — target of optimization |
| `resources/tests/test_scoring.py` | 56 tests — must always pass |

## Off Limits

- `SKILL.md` — skill documentation, not code
- All other `resources/*.md` files — documentation only
- `.gitignore` — not relevant

## Constraints

1. **Stdlib only** — no external dependencies (no numpy, no pandas, no rapidfuzz)
2. **56 tests must pass** — `uv run pytest resources/tests/ -v`
3. **mypy must pass** — `uv run mypy resources/scoring.py`
4. **interface stability** — function signature `deduplicate(papers: list[dict], threshold: float = 0.95) -> tuple[list[dict], list[dict]]` must NOT change
5. **Return format stability** — unique list + log list with kept_index, removed_index, reason, detail fields

## Dedup Algorithm (current)

Current implementation uses:
1. DOI hash table (O(1) dedup by DOI)
2. PMID hash table (O(1) dedup by PMID)
3. Title similarity via `difflib.SequenceMatcher` — O(n*m) per comparison, O(n²) total worst case

The bottleneck is step 3: when a paper has no DOI/PMID, it compares against ALL previously seen papers using SequenceMatcher (expensive string matching).

## What's Been Tried

| # | Idea | Result | Verdict |
|---|------|--------|---------|
| 1 | Replace `papers.index(prev)` with indexed tuples | within noise | ❌ discard — `list.index()` is C-level |
| 2 | Length pre-filter: skip SequenceMatcher when max possible ratio < threshold | **432,665µs (-84.3%) — 6.4x** | ✅ **keep — 144x noise floor** |
| 3 | Cache `.lower()`/`len()` in tuples + exact match short-circuit | 422,717µs — ~2.3% gain | ✅ keep — 2.0x noise floor |
| 4 | Word-set pre-filter: skip SequenceMatcher when 0 shared words | **213,829µs (-92.3%) — 12.9x total** | ✅ **keep — 11.6x noise floor** |

### Results Summary

| Metric | Before (baseline) | After (best) | Improvement |
|--------|------------------|-------------|-------------|
| dedup_µs (1000 papers) | 2,759,358 µs | 213,829 µs | **12.9x faster** |
| throughput | 362 papers/s | 4,676 papers/s | +1192% |
| 50-paper search | ~138,000 µs | ~10,700 µs | imperceptible |

## Active Optimizations in Code

- `_titles_can_match_len(len_a, len_b, threshold)` — length-based pre-filter
- Word-set pre-filter via `frozenset.intersection()` — 0 shared words → skip SequenceMatcher
- Exact match short-circuit before SequenceMatcher
- Cached `.lower()`, `len()`, `frozenset(words)` in tuple entries
