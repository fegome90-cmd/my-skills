---
name: falp-strategic-analysis-harness
description: >
  Force the agent to use the complete strategic skill chain, audit itself,
  compare output against sources, and produce a defensible final deliverable.
  Use for FALP/UCL/ElevenLabs collaboration, Impact Partner decisions,
  ASR/voice banking pilot planning, conference-readiness, and partner negotiation review.
scope: private
---

# FALP Strategic Analysis Harness

## Purpose

Force the agent to use the complete strategic skill chain, audit itself, compare output against sources, and produce a defensible final deliverable.

This harness should be used for:

- FALP / UCL / ElevenLabs collaboration analysis.
- Impact Partner decision.
- ASR / voice banking pilot planning.
- Chilean Spanish impaired speech strategy.
- Conference-readiness planning.
- Institutional stakeholder alignment.
- Partner negotiation review.

## Invocation

When the user provides a strategic input, run:

1. Context discovery — collect existing profiles, org notes, and prior decisions.
2. Source lock gate (`resources/source-lock-gate.md`) + actor separation checkpoint (`resources/actor-separation-checkpoint.md`).
3. Source ledger (`resources/source-evidence-ledger.md`).
4. Strategic situation assessment (`resources/strategic-situation-assessment.md`).
5. Stakeholder power map (`resources/stakeholder-power-map.md`).
6. Pilot readiness map (`resources/pilot-readiness-map.md`).
7. Risk and governance review (`resources/risk-governance-review.md`).
8. Conference readiness map (`resources/conference-readiness-map.md`).
9. Decision memo writer (`resources/decision-memo-writer.md`).
10. Grill assumptions with the user before final output when the user is available.
11. Audit checklist (`resources/strategic-analysis-audit-checklist.md`).
12. Source comparison and claim verification.
13. Final deliverable.

## Non-negotiable rule

The final deliverable is not allowed until the audit (Phase 7) and source comparison (Phase 8) have been completed.

## Execution contract

### Step 1 — Intake

Restate the task in one paragraph.

Identify:
- decision context,
- source material,
- known actors,
- timeline,
- intended output.

Then perform context discovery:
- existing profiles/wiki/CRM/org-chart notes,
- prior analysis or meeting notes,
- key actors omitted from the primary source.

If the user says those sources exist but does not provide them, stop and request them before continuing.

### Step 2 — Source lock + actor separation

Before the ledger, complete:
- Source Lock Gate (`resources/source-lock-gate.md`)
- Actor Separation Checkpoint (`resources/actor-separation-checkpoint.md`)

Do not continue if people, institutions, and vendors are still conflated.

### Step 3 — Source ledger

Create source ledger using `resources/source-evidence-ledger.md`.

Minimum required fields:
- Source ID.
- Claim/input.
- Source class (Primary/Public/Internal/Inference/Unknown/Context user-provided).
- Confidence.
- Limitation.

### Step 4 — Run the core analysis skills

Run each skill in order. Do not merge phases.

Each phase must produce a compact but explicit output.

### Step 5 — Synthesis

Create a synthesis that connects:
- strategic signal,
- stakeholder reality,
- pilot path,
- governance boundary,
- conference clock,
- decision ask.

### Step 6 — Grill assumptions

Before the audit, ask the user to validate the major hypotheses when the user is available.

Capture:
- which hypotheses were confirmed,
- which were corrected,
- which remained unresolved.

If the user is not available, mark the unresolved assumptions explicitly in the audit as a limitation.

### Step 7 — Audit

Use `resources/strategic-analysis-audit-checklist.md`.

The audit must explicitly state:
- Pass,
- Pass with limitations,
- or Fail — preliminary only.

### Step 8 — Source comparison

Create a final claim verification table:

| Claim | Support | Source IDs | Confidence | Action |
|---|---|---|---|---|

Actions: Keep / Weaken / Reframe as hypothesis / Remove / Verify before use.

### Step 9 — Final deliverable

Produce final deliverable only after Step 8.

The final deliverable must include:

1. Executive verdict.
2. Strategic interpretation.
3. Recommended next move.
4. Pilot minimum viable path.
5. Governance and ethics requirements.
6. Stakeholder engagement sequence.
7. Conference-readiness path.
8. Decision memo summary.
9. Claims safe to say now.
10. Claims not safe to say yet.
11. Open questions.
12. Next 14 days.

## Output modes

| Mode | When to use | Primary output |
|------|-------------|----------------|
| **A — Full strategic report** | Deep analysis | All 12 sections above |
| **B — Decision memo** | For leadership | Sections 1, 3, 5, 8, 12 |
| **C — Email response** | Replying to partner | Sections 1, 3, 9, 10, 11 |
| **D — Pilot plan** | Operationalizing | Sections 4, 5, 6, 9, 10, 12 |
| **E — Conference brief** | Preparing presentation | Sections 1, 2, 7, 9, 10, 12 |

## Fail-closed policy

If any of the following are unresolved, do not produce an overconfident final answer:

- missing source ledger,
- missing governance path,
- missing consent path for patient involvement,
- unverified conference,
- unclear institutional owner,
- unsupported public claims,
- vendor/data handling unknown,
- no risk stop conditions,
- no stakeholder sequence.

Instead output:

```
"Preliminary only — not ready for institutional decision"

Missing:
- [evidence gap 1]
- [missing approval 2]

Safest next step:
- [one action]
```

## Final quality standard

The output should be good enough to hand to a senior institutional stakeholder after human review.

It must not read like:
- generic consulting,
- sales copy,
- startup hype,
- technical fantasy,
- or emotional overreach.

It must read like:
- serious institutional strategy,
- clinically aware,
- ethically bounded,
- operationally realistic,
- evidence-disciplined.

*Harness for Strategic Partnership Toolkit v1.5.1*
