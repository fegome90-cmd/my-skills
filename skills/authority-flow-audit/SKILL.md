---
name: authority-flow-audit
description: "Use when auditing repository architecture for authority, data flow, competing pipelines, duplicate side effects, bottlenecks, and false SSOTs. Triggers for ownership analysis, responsibility mapping, pipeline conflict detection, SSOT verification, lifecycle analysis, double-writer detection, and side effect auditing. Supports repo-audit (full repo inspection) and change-audit (PR/diff/handoff review) modes. Also triggers for 'audit this repo', 'who owns X', 'what writes to Y', 'is this really the SSOT', 'authority analysis', 'flow audit', 'responsibility map', 'pipeline conflict', 'double writer', 'side effect audit'. Do NOT use for style review, lint, formatting, clean code cosmetics, or general code review."
search_hints: authority flow audit responsibility ownership SSOT pipeline conflict side-effect lifecycle entrypoint writer reader mutation bottleneck data-flow control-flow authority-vs-evidence repo-audit change-audit
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "2.1.0"
  role: specialist
  scope: architecture
  triggers:
    - "authority"
    - "flow audit"
    - "responsibility map"
    - "SSOT"
    - "pipeline conflict"
    - "double writer"
    - "side effect"
    - "lifecycle"
    - "who writes"
    - "who owns"
    - "entrypoint"
    - "repo audit"
    - "change audit"
    - "bottleneck"
---

# Authority-Flow Audit v2.1

Audit the real operational structure of a software system. Map what each surface does,
what it reads, what it writes, who it competes with, and whether it holds genuine
authority or merely provides evidence.

## When to Use / When Not to Use

**Use when:**
- Auditing a repo's actual architecture (docs may lie, code does not)
- Reviewing an agent's work on a repo (plan, diff, PR, handoff)
- Investigating who owns a piece of state or an artifact
- Checking if a supposed SSOT is actually single-source
- Detecting competing pipelines for the same output
- Before merging a PR that touches lifecycle, state, or pipeline code

**Do NOT use for:** Style review, lint, clean code analysis, general code review,
proposing features, refactoring, performance profiling, security auditing.

## Modes

| Mode | Flag | Scope |
|------|------|-------|
| **repo-audit** | `--mode repo-audit` | Full repository architectural inspection (tier-based) |
| **change-audit** | `--mode change-audit` | Specific change: PR, diff, patch, handoff (delta-first) |

Default: `repo-audit` unless the user specifies a PR, diff, or agent output.

## Inputs

**repo-audit:** Repository path. Optional: `--scope cli,jobs,api` and `--focus pipelines,side-effects`.
**change-audit:** Repository path + change identifier (PR number, diff file, commit range).

## Hard Invariants (Non-Negotiable)

These rules cannot be overridden. They apply regardless of mode, tier, or context.

1. **Evidence is not authority.** Logs, reports, metrics, test results do not own state.
2. **SSOT requires proof, not assumption.** Single-writer must be verified by code trace.
3. **Authority claims need code evidence.** Naming conventions are not evidence.
4. **No vague decisions.** Proposed decisions must be: keep / delegate / remove / investigate.
5. **Uncertainties must be explicit.** Unknowns go in section 11, not hidden in findings.

## Red Flags (Immediate Flag)

These trigger regardless of tier or severity. If detected, flag immediately:

1. Two surfaces write to same file without coordination — race condition
2. A hook mutates state the official pipeline also mutates — double execution
3. A wrapper reimplements logic it should delegate — hidden authority
4. Evidence used as basis for state decision — false authority
5. Pipeline has no identifiable authoritative surface — authority vacuum
6. State read from one source, written to another — split-brain

## Procedure — repo-audit (Tier-Based)

### Tier 1: Structural Scan

Catalog authority-critical surfaces only. Do NOT scan every function.

**Tier 1 surfaces (always catalog):** Entrypoints (CLI, API, scripts), writers
(functions that save/write/update/create), jobs, hooks, daemons, event handlers.

**Tier 2 surfaces (catalog if between entrypoint and write):** Wrappers, decorators,
transformers, importers that modify data before a write.

**Tier 3 surfaces (skip unless scoped):** Pure readers, helpers, test fixtures.

Record: file:line, type, writes-to, callers, callees.

**Load `resources/procedure.md`** for search patterns and classification tables.

**Tier 1 exit criteria:** If all pipelines are single-source, no competing writers,
and SSOTs verified → generate report. Stop here.

### Tier 2: Authority + Pipeline Analysis

Escalate from Tier 1 if any of:
- Multiple writers detected for same artifact
- Authority classification returns `ambiguous`
- Unofficial paths found alongside official ones
- Evidence-as-authority suspected

**Load `resources/judgment.md`** for confidence and evidence classification.
**Load `resources/heuristics-core.md`** for H1-H5 detection patterns.

Classify every finding with confidence (high/medium/low) and evidence_class
(direct-write/call-chain/inferred/docs-only).

**Tier 2 exit criteria:** If conflicts are resolved or low-confidence → generate report.
If competing pipelines or authority vacuums remain → escalate.

### Tier 3: Deep Conflict Analysis

Escalate from Tier 2 if any of:
- Competing pipelines detected (2+ active paths, no authority)
- Lifecycle conflicts (hooks/jobs vs official pipeline)
- Authority vacuum on critical state
- Tier 2 findings with CRITICAL/HIGH severity + high confidence

**Load `resources/heuristics-extended.md`** for H6-H13 patterns.
Deep-trace all conflicting paths with full call chains.

### Report Generation

**Load `resources/report-template.md`** for the mandatory 11-section structure
(+ 2 optional sections: authority map, pipeline map).
**Load `resources/judgment.md`** for the risk priority matrix.

## Procedure — change-audit (Delta-First)

**Load `resources/change-audit.md`** for the full hardened procedure.

Core principle: compare before/after the change across 8 mandatory dimensions.
Every finding gets confidence + evidence_class. Report uses delta markers:
NEW / MODIFIED / UNCHANGED-AFFECTED / BASELINE.

## Resources Index

| Resource | Lines | When to Load | Obligatory? |
|----------|-------|--------------|-------------|
| `resources/INDEX.md` | ~70 | Before starting — navigation map | Optional |
| `resources/procedure.md` | ~160 | Tier 1-2: search patterns, authority table, pipeline types | repo-audit |
| `resources/change-audit.md` | ~130 | Every change-audit | change-audit |
| `resources/judgment.md` | ~90 | Tier 2+: severity, confidence, evidence, escalation | Yes |
| `resources/heuristics-core.md` | ~100 | Tier 2: 5 highest-frequency patterns | Tier 2+ |
| `resources/heuristics-extended.md` | ~155 | Tier 3: 8 additional patterns | Tier 3 |
| `resources/report-template.md` | ~190 | Report generation | Yes |
| `resources/examples.md` | ~110 | Before starting — worked examples | Optional |
| `resources/learned.md` | ~150 | Post-creation lessons | Maintenance |
| `resources/activation-test.md` | ~55 | Skill trigger testing | Maintenance |

Max context per load: **SKILL.md (~195 lines) + 1 resource (~190 lines) = ~385 lines**

## Key Distinctions

| Confuse | With | Rule |
|---------|------|------|
| Authority | Evidence | Authority writes state; evidence describes state |
| Owner | Helper | Owner decides what state becomes; helper executes for owner |
| Official pipeline | Tolerated pipeline | Official = designated; tolerated = legacy convenience |
| Reader | Writer | Reader has zero mutation paths; writer has at least one |
| Direct mutation | Derived side effect | Direct = intentional write; derived = consequence of another action |
| Innocuous duplication | Dangerous duplication | Innocuous = read-only overlap; dangerous = competing writes |
| Legitimate bottleneck | Accidental coupling | Legitimate = by design; accidental = could parallelize |
| High severity | High confidence | Severity = impact; confidence = evidence strength. Both needed to act |
