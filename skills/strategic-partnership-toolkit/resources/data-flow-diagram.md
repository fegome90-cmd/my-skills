---
name: data-flow-diagram
description: Mandatory data lifecycle diagram before any protocol involving patient or sensitive data. Maps every node from capture to deletion with access, storage, and revocation protocols.
---

# Data Flow Diagram

## Purpose

Map the complete data lifecycle before any protocol that involves patient data, voice biometrics, or sensitive institutional information. This is a prerequisite, not an optional analysis step.

## When to use

- **Always** before writing any pilot protocol that involves patient data.
- Before signing a BAA/DPA with a vendor.
- When a partner proposes cloud processing of sensitive data.
- When voice, video, or biometric data is involved.

## Core principle

**No protocol without a data flow.** If you can't draw the data lifecycle, you can't protect the patient. Every unaddressed node is a liability.

## Method

### Step 1: Map the linear flow

```
[PATIENT] → [CAPTURE] → [UPLOAD] → [PROCESSING] → [STORAGE] → [ACCESS] → [DELETION]
```

### Step 2: Detail each node

For every node, answer all six questions:

| Question | Description |
|----------|-------------|
| **WHO** | Who operates this node? Name the role, not just "the system" |
| **WHERE** | Physical or geographic location. Is it Chile? US? EU? Cloud provider? |
| **HOW** | Technology and transmission method. TLS version? End-to-end encryption? |
| **DURATION** | How long does data persist at this node? Buffer time? Retention policy? |
| **REVOCATION** | What happens if the patient revokes consent at this node? |
| **AUDIT** | Is there an access log? Who can see it? |

### Step 3: Identify gaps

Common gaps that must be flagged:

1. **Server location unknown** — Can't evaluate regulatory compliance without this.
2. **Retention policy undefined** — Data accumulation risk.
3. **Consent module not implemented** — Can't handle revocation.
4. **Access logs not described** — Can't audit who saw what.
5. **Encryption gaps** — No E2E, no encryption at rest, or outdated protocols.
6. **Vendor employee access** — Can the vendor's staff see patient data?
7. **Sub-processor chain** — Does the vendor use third parties we don't know about?

### Step 4: Define revocation protocol

Patient consent revocation must have a concrete protocol:

```
Revocation trigger → [who is notified] → [which nodes are affected] → 
[what data is deleted] → [confirmation to whom] → [retention of audit log only]
```

**Critical:** Even after deletion, audit logs may need to be retained for legal reasons. This is acceptable if clearly documented and separated from patient data.

### Step 5: Verify against regulation

Cross-reference the data flow with applicable regulation:

| Regulation | Relevant for | Key requirement |
|-----------|-------------|-----------------|
| Chile Ley 19.628 | All personal data | Consent, purpose limitation, data subject rights |
| Chile Ley 21.719 (new) | Health data specifically | Enhanced consent, DPO, data minimization |
| HIPAA (if US processing) | Health data transmitted to US | BAA required |
| GDPR (if EU processing) | EU data subjects | Right to erasure, DPO, DPIA |

## Anti-patterns

1. **"Data is encrypted" without specifying where and how.** "Encrypted" is meaningless without details.
2. **Assuming data stays in Chile.** Most cloud ASR providers process in US/EU. Verify.
3. **No revocation protocol.** If the patient revokes and you don't have a protocol, you're non-compliant.
4. **Vendor says "we're compliant" without evidence.** Demand audit reports, certifications, or third-party assessments.
5. **Skipping this step for a "small pilot."** The risk per-patient is the same regardless of pilot size.

## Output format

```
### Data Flow Diagram

[ASCII art of the flow]

| Node | WHO | WHERE | HOW | DURATION | REVOCATION | AUDIT |
|------|-----|-------|-----|----------|-----------|-------|
| CAPTURE | ... | ... | ... | ... | ... | ... |

### Gaps Identified
1. [gap description] — [severity: CRITICAL/HIGH/MEDIUM]
2. ...

### Revocation Protocol
[step-by-step]
```

---

*Data Flow Diagram v1.0.0 — Strategic Partnership Toolkit*
