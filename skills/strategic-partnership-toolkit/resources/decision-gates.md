---
name: decision-gates
description: Post-meeting decision gates. Maps specific questions to GO/PAUSE/STOP outcomes. Prevents premature commitment after a single conversation.
---

# Decision Gates

## Purpose

Transform a key meeting (video call, in-person, demo) into structured decision inputs. Every answer maps to a gate: GO (advance), PAUSE (need more info), or STOP (project killer).

## When to use

- After a video call with a potential partner or vendor.
- After a demo that needs evaluation beyond "impressive" vs "not impressive".
- Before advancing from one phase to the next (exploration → due diligence → pilot).

## Core principle

**A good meeting produces answers, not excitement.** Without gates, a good conversation creates false momentum. With gates, the same conversation produces actionable clarity.

## Method

### Step 1: Design questions before the meeting

Write questions aligned to the decision matrix criteria. At least 10-12 questions.

Categories to cover:
1. **Data ownership and portability** — Who owns what? Can we export?
2. **Model training on patient data** — Is our data used to improve their product?
3. **Pricing model** — Per-seat, per-hour, per-patient? Public institution rates?
4. **Legal agreements** — BAA/DPA terms, liability, jurisdiction.
5. **Regulatory compliance** — Certifications, audits, country-specific law history.
6. **References** — Similar implementations in similar settings. Contact info.
7. **Technical specs** — MVP features, API docs, integration complexity, latency.
8. **SLA and support** — Uptime, response time, escalation, clinical-hour support.
9. **Exit strategy** — Data portability, lock-in, migration cost, notice period.
10. **IP ownership** — Who owns co-developed workflows or integrations?
11. **Business continuity** — Financial health, acquisition risk, succession plan.
12. **Consent management** — How is patient consent captured, stored, revoked?

### Step 2: Define gate thresholds per question

For each question, define what constitutes GO, PAUSE, and STOP:

| Question | GO (advance) | PAUSE (need more) | STOP (killer) |
|----------|-------------|-------------------|---------------|
| Q1: Data ownership? | Contractual clause: FALP owns all data | Verbal commitment, draft clause pending | Cave retains data or right to use |

### Step 3: Conduct the meeting with the gate sheet

Use the questions as your meeting guide. Mark answers live.

### Step 4: Tally results

```
GO:    X questions
PAUSE: Y questions
STOP:  Z questions
```

**Decision rule:**
- 0 STOP gates → Proceed to next phase (if GO > PAUSE)
- 1+ STOP gates → Cannot proceed until resolved
- All STOP gates must convert to GO before phase advancement
- PAUSE gates can run in parallel with STOP resolution

### Step 5: Document with evidence

Every answer must have evidence:
- "Verbal commitment in video call 2026-05-29" is acceptable for exploration.
- "Signed BAA received 2026-06-05" is required for due diligence.
- "Approved by ethics committee 2026-06-15" is required for pilot.

## Anti-patterns

1. **Setting all gates to GO.** If nothing can stop the project, the gates are too weak.
2. **Marking "verbal yes" as GO for pilot phase.** Verbal is exploration only.
3. **Fewer than 8 questions.** Too few = blind spots.
4. **No STOP gates.** If there's nothing that kills the project, you're not protecting the institution.
5. **Updating gates after the meeting to match the desired outcome.**

## Output format

```
### Decision Gates (post-meeting: [Meeting description])

| # | Question | GO | PAUSE | STOP | Evidence required |
|---|----------|----|------|------|-------------------|
| G1 | ... | [what answer] | [what answer] | [what answer] | [artifact needed] |

**Summary:** X GO, Y PAUSE, Z STOP
**Decision:** [Cannot proceed until STOP gates G1, G2, G4 resolved.]
```

---

*Decision Gates v1.0.0 — Strategic Partnership Toolkit*
