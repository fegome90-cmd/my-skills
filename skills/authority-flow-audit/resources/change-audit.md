# change-audit Procedure v2.1 (Delta-First)

change-audit compares before/after a change to detect authority shifts, new conflicts,
or broken pipelines. It does NOT re-audit the entire repo.

---

## Contract

Every change-audit MUST address all 8 dimensions of the Mandatory Checklist below.
The report MUST use delta markers (NEW/MODIFIED/UNCHANGED-AFFECTED/BASELINE).
The report MUST include confidence and evidence_class for every finding.

## Mandatory Checklist

For each item, mark: **CLEAR** | **FLAGGED** | **UNCERTAIN**

| # | Dimension | What to Check |
|---|-----------|--------------|
| 1 | New writers on owned state | Does the change introduce a surface that writes to state already owned by another surface? |
| 2 | New entrypoints to pipelines | Does the change add a new entrypoint (CLI, script, endpoint) that reaches an existing writer? |
| 3 | Evidence-as-authority risk | Does any new surface read from logs/reports/metrics to make state decisions? |
| 4 | New side effects | Does a modified surface add side effects not present in the version it replaces? |
| 5 | Validation strength change | Does the change weaken or strengthen validation before a write? |
| 6 | Legacy path status | Are deprecated/legacy paths removed, or do they remain alive alongside new ones? |
| 7 | Authority expansion | Does a surface gain write access to additional artifacts it did not write before? |
| 8 | Pipeline type transition | Does any pipeline change type? (single→competing, official→shadow, etc.) |

All 8 items must appear in the report, even if CLEAR.

## Step 1: Identify Change Surfaces

Extract from diff/PR/handoff:
- **New surfaces:** functions, scripts, hooks, jobs, daemons added
- **Removed surfaces:** surfaces deleted or renamed
- **Modified surfaces:** surfaces with changed write targets, side effects, or validation
- **Unchanged-affected:** surfaces not in the diff but that share state with changed surfaces

For each, record: name, type, file:line, what it writes to.

## Step 2: Delta Against Authority

For each new or modified surface, apply core heuristics (H1-H5):

| Heuristic | Delta Question |
|-----------|---------------|
| H1: Multiple entrypoints | Does the change add another entrypoint to an existing mutation? |
| H2: Bypass | Does a new script/CLI skip the official pipeline? |
| H3: Lifecycle conflict | Does a new hook/job mutate state the official pipeline also mutates? |
| H4: Double writer | Does a new surface write to the same file/table as an existing one? |
| H5: Evidence-as-authority | Does any surface now read from evidence to decide writes? |

Each finding must include:
- **confidence**: high | medium | low
- **evidence_class**: direct-write | call-chain | inferred | docs-only

## Step 3: Pipeline Impact Analysis

For each artifact touched by the change:

| Artifact | Pipeline Type Before | Pipeline Type After | Delta |
|----------|---------------------|---------------------|-------|
| [name] | single-pipeline | competing | [what changed] |

- Was the pipeline single-source before? Is it still?
- Was a new code path added for an existing output?
- Was a legacy path removed or left alive?
- Does the change extend a surface's authority to new artifacts?

## Step 4: Generate Delta Report

Use the same 11-section template as repo-audit, with these modifications:

### Delta Markers
Items in sections 2-8 MUST be prefixed with:
- **[NEW]** — surface/artifact/pipeline did not exist before this change
- **[MODIFIED]** — changed write targets, side effects, or authority classification
- **[UNCHANGED-AFFECTED]** — existing surface affected by changes elsewhere
- **[BASELINE]** — pre-change state shown for comparison

### Baseline Comparison Table

Include after section 3 (Authority Table):

| Surface | Authority Before | Authority After | Delta Trigger | Confidence | Evidence Class |
|---------|-----------------|----------------|---------------|-----------|---------------|
| [name] | authoritative | competing | new writer added | high | direct-write |

### Checklist Summary

Include before section 9 (Prioritized Risks):

| # | Dimension | Status | Details |
|---|-----------|--------|---------|
| 1 | New writers on owned state | CLEAR/FLAGGED/UNCERTAIN | [finding if not CLEAR] |
| 2-8 | ... | ... | ... |
