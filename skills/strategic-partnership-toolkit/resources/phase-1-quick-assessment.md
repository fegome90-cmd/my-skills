---
name: phase-1-quick-assessment
description: Always load first. Classifies the strategic signal, selects the right tool sequence, and maps tools to resource files.
---

# Phase 1: Quick Assessment

**Always start here.** Load this first for any strategic signal.

## Purpose

Determine what tool sequence to use, produce an initial strategic reading, and map to exact resource files.

## Process

### 0. Context discovery (before classification)

Before classifying the signal, check whether the user already has:
- wiki pages or profiles for the actors,
- prior analysis or meeting notes,
- org charts or CRM notes,
- hidden stakeholders not visible in the primary source.

If those materials exist, read them first.
If the user says they exist but does not provide them, stop and ask for them before proceeding.

### 1. Source lock + actor separation

Before scoring or sequencing any opportunity:
- pass the **Source Lock Gate** (`source-lock-gate.md`)
- pass the **Actor Separation Checkpoint** (`actor-separation-checkpoint.md`)

If entities are conflated, do not continue to Phase 2.

### 2. Receive the signal

The user provides:
- Original message, note, or situation description
- Known actors (people/organizations involved)
- Desired outcome (if known)
- Constraints (if known)

If details are missing, list them as evidence gaps. Do not invent actors, approvals, deadlines, or commitments.

### 3. Classify the signal

Determine the signal type and auto-select the tool sequence:

| Signal type | Description | Sequence | Files to load |
|-------------|-------------|----------|---------------|
| **Partner outreach** | Email/message from external partner | PRE → 1 → 2 → 3 → 4 → 6 | `source-lock-gate.md`, `actor-separation-checkpoint.md`, `strategic-situation-assessment.md`, `stakeholder-power-map.md`, `pilot-readiness-map.md`, `risk-governance-review.md`, `decision-memo-writer.md` |
| **Internal proposal** | Idea or request from inside institution | PRE → 2 → 3 → 4 → 6 | `source-lock-gate.md`, `actor-separation-checkpoint.md`, `stakeholder-power-map.md`, `pilot-readiness-map.md`, `risk-governance-review.md`, `decision-memo-writer.md` |
| **Opportunity window** | Time-limited chance (conference, funding) | PRE → 1 → 5 → 3 → 6 | `source-lock-gate.md`, `actor-separation-checkpoint.md`, `strategic-situation-assessment.md`, `conference-readiness-map.md`, `pilot-readiness-map.md`, `decision-memo-writer.md` |
| **Risk event** | Something went wrong or might | PRE → 4 → 2 → 6 | `source-lock-gate.md`, `actor-separation-checkpoint.md`, `risk-governance-review.md`, `stakeholder-power-map.md`, `decision-memo-writer.md` |
| **Decision pending** | Choice needs to be made soon | PRE → 1 → 2 → 6 | `source-lock-gate.md`, `actor-separation-checkpoint.md`, `strategic-situation-assessment.md`, `stakeholder-power-map.md`, `decision-memo-writer.md` |
| **Political misalignment** | Stakeholders misaligned | PRE → 2 → 6 | `source-lock-gate.md`, `actor-separation-checkpoint.md`, `stakeholder-power-map.md`, `decision-memo-writer.md` |

### 4. Produce initial reading

Output this structure:

```
## Strategic Reading

**Signal type:** [type]
**Context discovery:** [done / pending]
**Prerequisites:** [source lock PASS/FAIL, actor separation PASS/FAIL]
**Primary actor:** [who sent/initiated]
**Opportunity:** [what's being offered/implied]
**Clock:** [deadline or pressure, explicit or implicit]
**Key uncertainty:** [what we don't know that matters most]
**Recommended sequence:** [tool numbers in order]
**Files to load:** [exact resource filenames from table above]

## Quick Facts vs Inferences

| Category | Item | Confidence |
|----------|------|------------|
| Verified fact | ... | High |
| Reasonable inference | ... | Medium |
| Speculative | ... | Low |

## Recommended next step

One concrete action.
```

### 5. Ask user before proceeding

Before loading Phase 2 tools, confirm:
- Is this reading correct?
- Which tools should I run?
- Any constraints I should know about?

Then load the mapped resource files and proceed with each tool's method.

---

*Phase 1 of Strategic Partnership Toolkit v1.5.1*
