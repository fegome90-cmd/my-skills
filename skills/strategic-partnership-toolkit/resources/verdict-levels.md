---
name: verdict-levels
description: Four-level verdict system replacing binary PASS/FAIL. Separates structural, methodological, factual, and institutional assessment.
---

# Verdict Levels

## Purpose

Replace binary PASS/FAIL with a four-dimensional verdict that honestly reflects the state of analysis. Prevents a single "PASS" from masking critical gaps in evidence, governance, or institutional alignment.

## The problem with binary PASS/FAIL

A binary PASS implies readiness. But an analysis can have:
- Sound methodology (PASS-worthy)
- Insufficient evidence (FAIL-worthy)
- No institutional alignment (unassessed)

The binary collapses these into one misleading signal.

## The four levels

| Level | Question it answers | PASS means | FAIL means |
|-------|--------------------|-----------|-----------|
| **Structural** | Is the decision framework sound? | Logic, architecture, criteria are well-designed. | Framework has holes or contradictions. |
| **Methodological** | Were the right tools applied correctly? | Analysis tools used properly, outputs consistent. | Tools misapplied, inconsistent, or skipped. |
| **Factual** | Are all claims verified with evidence? | Every claim traces to a source. Evidence is sufficient for the phase. | Claims exist without evidence. Sources missing or weak. |
| **Institutional** | Are all stakeholders aligned and approvals obtained? | Decision makers informed, approvals in place, timeline agreed. | Institution hasn't been engaged or hasn't approved. |

## Possible verdicts per level

- **PASS** — Fully met
- **PARTIAL PASS** — Mostly met, specific gaps documented
- **FAIL** — Not met, action required
- **NOT YET ASSESSED** — Not evaluated (different from FAIL)

**Important:** NOT YET ASSESSED ≠ PASS. It means we don't know. Treating NYA as PASS is the most common error.

## Scoring guide

| Situation | Structural | Methodological | Factual | Institutional |
|-----------|-----------|---------------|---------|---------------|
| First analysis from email | PASS | PARTIAL | FAIL | NYA |
| After video call + documents | PASS | PASS | PARTIAL | NYA |
| After due diligence complete | PASS | PASS | PASS | NYA |
| After committee approval | PASS | PASS | PASS | PASS |
| Analysis with logic errors | FAIL | — | — | — |
| Analysis with unverifiable claims | PASS | PARTIAL | FAIL | — |

## Rules

1. **PASS Factual requires the claim ledger to be clean.** Every claim either verified or explicitly marked as hypothesis.
2. **PASS Institutional requires documented approvals**, not verbal promises.
3. **PARTIAL PASS Methodological** is acceptable if gaps are documented and bounded.
4. **NOT YET ASSESSED is honest.** Use it when the institution simply hasn't been involved yet.
5. **No overall "PASS" composite.** Report each level separately. A composite average hides the weakest link.

## Integration with decision matrix

The verdict levels should align with the decision matrix:

| Matrix state | Expected verdict levels |
|-------------|------------------------|
| Exploración viable | Structural: PASS, Methodological: PARTIAL, Factual: PARTIAL, Institutional: NYA |
| Due diligence complete | Structural: PASS, Methodological: PASS, Factual: PASS, Institutional: NYA |
| Pilot ready | All four: PASS |

If the verdict levels don't match the phase expectations, the phase is not ready.

## Output format

```
### Verdict by Level

| Dimension | Verdict | Justification |
|-----------|---------|---------------|
| Structural | [PASS/PARTIAL/FAIL/NYA] | [1-2 sentences] |
| Methodological | [...] | [...] |
| Factual | [...] | [...] |
| Institutional | [...] | [...] |

### Comparison with previous version
[Table showing what changed and why]
```

---

*Verdict Levels v1.0.0 — Strategic Partnership Toolkit*
