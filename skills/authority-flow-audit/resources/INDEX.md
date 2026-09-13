# Package Index — authority-flow-audit v2.1

Navigation map for this skill. Load this file first to orient before starting any audit.

---

## File Map

| File | Purpose | Obligatory? | Lines | Loaded When |
|------|---------|-------------|-------|-------------|
| `SKILL.md` | Orchestrator, modes, hard invariants, tier execution, red flags | Always | ~170 | Every invocation |
| `resources/INDEX.md` | This file — navigation and loading guide | Reference | ~60 | Before starting |
| `resources/procedure.md` | repo-audit: search patterns, state categories, authority table, pipeline types | repo-audit | ~155 | Tier 1-3 |
| `resources/change-audit.md` | change-audit: delta-first with 8-dimension mandatory checklist | change-audit | ~95 | Every change-audit |
| `resources/judgment.md` | Severity, confidence, evidence_class, escalation rules, risk matrix | Tier 2+ | ~90 | When findings exist |
| `resources/heuristics-core.md` | 5 highest-frequency detection patterns (H1-H5) | Tier 2+ | ~100 | Tier 2 escalation |
| `resources/heuristics-extended.md` | 8 additional patterns for deep analysis (H6-H13) | Tier 3 | ~155 | Tier 3 escalation |
| `resources/report-template.md` | Mandatory 11-section report + 2 optional (authority-map, pipeline-map) | Yes | ~190 | Report generation |
| `resources/examples.md` | 2 worked examples with confidence/evidence_class | Reference | ~115 | Before starting |
| `resources/learned.md` | 10 lessons from building this skill | Maintenance | ~150 | Post-creation only |
| `resources/activation-test.md` | Trigger phrase validation and edge cases | Maintenance | ~55 | Skill testing only |

## Loading Order by Mode

### repo-audit

```
1. SKILL.md           (always)
2. INDEX.md           (optional — orientation)
3. examples.md        (optional — before starting)
4. procedure.md       (Tier 1 — structural scan)
5. judgment.md        (Tier 2 — authority + severity)
6. heuristics-core.md (Tier 2 — core patterns)
7. heuristics-extended.md (Tier 3 only — if escalating)
8. report-template.md (Tier 2-3 — report generation)
```

### change-audit

```
1. SKILL.md           (always)
2. change-audit.md    (always — full contract)
3. judgment.md        (always — confidence assessment)
4. heuristics-core.md (always — core patterns against delta)
5. report-template.md (always — report with delta markers)
```

## Which Questions Each File Answers

| Question | File |
|----------|------|
| What is this skill for? | SKILL.md — "When to Use" |
| What are the hard rules I cannot skip? | SKILL.md — "Hard Invariants" |
| What are the red flags that stop everything? | SKILL.md — "Red Flags" |
| How do I discover surfaces? | procedure.md — Tier 1 |
| How do I classify authority? | procedure.md — Phase 3 |
| What patterns am I looking for? | heuristics-core.md + heuristics-extended.md |
| How do I judge severity and confidence? | judgment.md |
| When do I escalate to deeper analysis? | judgment.md — Escalation Rules |
| How do I audit a PR/diff specifically? | change-audit.md |
| What must the report contain? | report-template.md |
| What are the optional report sections? | report-template.md — sections 12-13 |
| Does this phrase trigger the skill? | activation-test.md |
