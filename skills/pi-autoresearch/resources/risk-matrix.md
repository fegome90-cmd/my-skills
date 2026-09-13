# Risk Matrix Framework

Structured decision framework for the ask-on-risk phase of autoresearch-gate.

## Scoring Format

For each implementation option, score 5 dimensions on a 1-10 scale (1 = low risk, 10 = high risk):

| Dimension | 1 (Best) | 5 (Medium) | 10 (Worst) |
|-----------|----------|------------|-------------|
| **Invasiveness** | No stored data changed | Modifies internal format | Changes public API or DB schema |
| **Re-index** | None needed | Partial (one segment) | Full re-index of all segments |
| **Backward-compat** | Pure addition, no removal | Optional param with default | Breaking change to existing callers |
| **Test surface** | 1-2 new tests | 3-5 new tests | >5 new tests or integration tests |
| **Rollback ease** | Single file revert | Multi-file revert with dependencies | Requires data migration to rollback |

**Total risk score** = sum of 5 dimensions (5-50). Lower is better.

## Decision Tree

```
START: List all options (A, B, C...)

STEP 1: Score each option
  → If only one option: score it anyway. Score > 25 → investigate alternatives.

STEP 2: Compare scores
  → Clear winner (gap ≥ 8 points)? → Choose it.
  → Tie or near-tie (gap < 8)? → Break by: invasiveness → backward-compat → test surface.

STEP 3: Validate choice
  → Does the chosen option solve the WHOLE problem? If partial → can it be extended later?
  → Does it create new dependencies? If yes → are they acceptable?

STEP 4: Record
  → If chosen ≠ lowest-score: document WHY (e.g., "Option B scores lower but doesn't
     solve the full problem, so we accept Option A's higher score")
```

## Risk Patterns

Common risk patterns encountered in autoresearch-gated implementations:

### Pattern 1: Graph Structure Change

**Risk**: Adding a new edge kind (e.g., `owns`) changes edge counts, affects all consumers of graph stats.

**Decision rule**: Prefer implicit traversal (no new edges) over explicit edges. Implicit = zero-invasiveness because it only affects path resolution, not stored data.

**Example**: O-1 class→method gap. Option A (add `owns` edges) scored 28/50. Option C (implicit BFS) scored 8/50.

### Pattern 2: NL Pattern Overlap

**Risk**: A new query classifier pattern matches the same queries as an existing pattern, causing routing ambiguity.

**Decision rule**: New patterns must NOT overlap with existing relational/hub/semantic patterns. If overlap is unavoidable, the more specific pattern wins. Document the priority rule.

**Example**: O-5 `ImpactPredicate`. "who depends on X" overlapped with `_IMPORTER_PATTERNS`. Removed from impact, kept in importers.

### Pattern 3: External Dependency

**Risk**: New feature depends on an external service (LSP daemon, MCP bridge) that may be unavailable.

**Decision rule**: Feature must degrade gracefully. If dependency is unavailable, return `fidelity=degraded` or `unavailable`, never crash.

### Pattern 4: Re-index Cascade

**Risk**: Changing the graph indexing schema requires all segments to be re-indexed.

**Decision rule**: If change only affects query-time behavior (BFS traversal, path resolution), no re-index needed. If change affects what's stored (new edge kinds, new node properties), re-index required.

**Example**: O-1 `traverse_classes` param affects only `find_path` behavior → no re-index.

## Scoring Examples

### Example 1: O-1 Class→Method Path Gap

| Dimension | Option A (owns edges) | Option B (expand at service) | Option C (implicit BFS) |
|-----------|----------------------|------------------------------|------------------------|
| Invasiveness | 7 (adds edges) | 4 (service only) | 1 (no changes) |
| Re-index | 9 (all segments) | 1 (none) | 1 (none) |
| Backward-compat | 6 (new edge kind) | 7 (optional param) | 9 (pure addition) |
| Test surface | 5 (integration tests) | 4 (service tests) | 2 (unit tests) |
| Rollback ease | 7 (data migration) | 4 (multi-file) | 2 (single file) |
| **Total** | **34** | **20** | **15** |

**Decision**: Option C. Gap = 5 vs B, 19 vs A.

### Example 2: O-5 Impact Analysis

| Dimension | Option A (callers-only reuse) | Option B (new reverse BFS) |
|-----------|-------------------------------|---------------------------|
| Invasiveness | 2 (reuse existing) | 4 (new store method) |
| Re-index | 1 (none) | 1 (none) |
| Backward-compat | 8 (overloads callers) | 3 (new API, no breaking) |
| Test surface | 3 (existing tests) | 5 (new tests) |
| Rollback ease | 2 (single file) | 3 (multi-file) |
| **Total** | **16** | **16** |

**Decision**: Tie. Break by invasiveness → Option B (new dedicated API is cleaner than overloading callers).

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|--------------|-----|
| Score only the "obvious" option | No comparison = hidden risk | Always score ≥2 options |
| Skip scoring for "small" changes | Small changes can have large blast radius | Score everything |
| Choose purely by implementer preference | Bias drowns evidence | Follow score + decision tree |
| No documentation of the decision | Future agents repeat the same analysis | Record in engram |