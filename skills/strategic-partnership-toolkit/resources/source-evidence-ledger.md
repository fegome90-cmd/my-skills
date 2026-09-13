---
name: source-evidence-ledger
description: Use this resource before any strategic recommendation. Prevents treating interpretation, assumptions, partner signals, or user impressions as verified facts.
---

# Source Evidence Ledger

## Purpose

Prevent the agent from treating interpretation, assumptions, partner signals, or user impressions as verified facts.

## Source classes

### A. Primary source

Direct material provided by the user.

Examples:
- Email from partner.
- Uploaded deck.
- Meeting transcript.
- Internal memo.
- Official document shared by a stakeholder.

### B. Public verification source

External public material used to verify facts.

Examples:
- Official institution website.
- Conference page.
- Academic publication.
- Company documentation.
- Regulatory or legal source.

### C. Internal interpretation

User's interpretation of institutional dynamics or strategic meaning.

Examples:
- "He is implying we need to move quickly."
- "This person has informal power."
- "The institution may prefer a conservative pilot."

These may be strategically valuable but must not be presented as public facts.

### D. Agent inference

Reasoned conclusion produced by the agent.

Examples:
- "There is an implicit deadline."
- "The best next move is a narrow pilot."
- "This creates a conference-readiness clock."

Must be labeled as inference.

### E. Unknown / evidence gap

Something important that is not yet supported.

Examples:
- conference name, date, approval pathway, patient eligibility, legal requirements, vendor data handling, institutional owner.

## Ledger table

Use this table:

| ID | Claim or input | Source class | Source detail | Confidence | Used for | Limitation |
|---|---|---|---|---|---|---|
| S1 | | Primary/Public/Internal/Inference/Unknown | | High/Medium/Low | | |

## Evidence rules

1. A source can support only what it actually says.
2. A source cannot authorize action unless it is an authority source.
3. A partner email can show interest, but not institutional approval.
4. A deck can support what was presented, but not prove clinical effectiveness.
5. A meeting memory can guide strategy, but should be marked as internal interpretation.
6. A public website can verify affiliation or event details, but not private intent.
7. Clinical or patient-facing action requires governance, not just strategic enthusiasm.

## Required source comparison

Before final output, create this table:

| Final claim | Source IDs | Fully supported? | Adjustment needed |
|---|---|---|---|
| | | Yes/Partially/No | |

## Unsupported claim handling

If a claim is unsupported:
- remove it,
- weaken it,
- mark it as hypothesis,
- or request verification.

Do not leave unsupported claims in the final memo.

---

*Resource for Strategic Partnership Toolkit v1.5.1*
