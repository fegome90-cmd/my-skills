
> **Prerequisite:** Complete `resources/source-evidence-ledger.md` before this tool. Every claim must trace to a source class.
---
name: risk-governance-review
description: Use this skill when reviewing ethical, clinical, institutional, privacy, data, legal, reputational, or vendor risks in a health, AI, voice, ASR, patient-data, research, or pilot collaboration.
---

# Risk Governance Review

## Purpose

Identify what can go wrong before enthusiasm becomes institutional exposure.

This skill is designed for health and AI projects involving patients, voice, speech, data, third-party tools, or external partners.

## Core principle

Evidence is not authority. A demo, email, deck, or partner promise does not authorize clinical use, data sharing, public claims, or patient recruitment.

## Required inputs

Useful inputs:
- Project description.
- Technology/vendor.
- Patient/user group.
- Data types involved.
- Current stage.
- Proposed next action.
- Institutional context.

If details are missing, assume a conservative risk posture and mark unknowns.

## Method

1. Classify data sensitivity.
   Consider:
   - Voice recordings.
   - Speech impairment samples.
   - Personal identifiers.
   - Clinical condition.
   - Oncology status.
   - Contact details.
   - Images, notes, transcripts.
   - Cross-border transfer.

2. Identify use stage.
   - Internal exploration.
   - Demo with synthetic data.
   - Staff-only test.
   - Patient feasibility pilot.
   - Research study.
   - Clinical workflow.
   - Public communication.

3. Identify authority needed.
   Match stage to approvals:
   - Clinical owner.
   - Ethics/research committee.
   - Data protection/privacy.
   - IT/security.
   - Legal/procurement.
   - Communications.
   - Patient representative, when appropriate.

4. Identify risk categories.
   - Patient vulnerability.
   - Consent clarity.
   - Data storage and access.
   - Vendor dependency.
   - Model output failure.
   - Misrecognition or miscommunication.
   - Emotional harm.
   - Public overclaiming.
   - Cross-border data transfer.
   - Unclear responsibility if tool fails.

5. Define mitigations.
   Each high risk must have:
   - Preventive control.
   - Detection method.
   - Escalation owner.
   - Stop condition.

6. Define permitted next step.
   Recommend the safest useful next action.

## Output format

### Veredicto de riesgo

Low / Moderate / High / Not enough information.

### Etapa real del proyecto

State the current stage and what is not yet authorized.

### Datos involucrados

Table:
Data type | Sensitivity | Who accesses | Storage/transfer concern | Required control

### Riesgos priorizados

Table:
Risk | Probability | Severity | Exposure | Mitigation | Stop condition

### Autoridades necesarias

Table:
Authority | Why needed | Before what action

### Lo permitido ahora

Actions that are safe with current authority.

### Lo no permitido todavía

Actions that require approval first.

### Próximo control mínimo

One governance artifact or meeting to create next.

## Quality gates

Before finalizing, verify:
- Patient data is not treated as ordinary product telemetry.
- Voice is treated as sensitive biometric/identity-linked material when applicable.
- The output distinguishes demo, pilot, research, and clinical deployment.
- No public claim is recommended before approval.
- Every high-risk item has a stop condition.
