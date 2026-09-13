# Judgment Framework

Severity criteria, confidence levels, evidence classes, escalation rules, and risk priority matrix for authority-flow-audit findings.

## Severity Criteria

| Level | Definition |
|-------|-----------|
| CRITICAL | Competing pipelines write to the same target with no coordination; data loss or corruption is probable. |
| HIGH | Unofficial write path bypasses the authority owner; no guard rails prevent divergent state. |
| MEDIUM | Ambiguous authority with multiple plausible owners; no clear SSOT enforced in code. |
| LOW | Documentation claims authority but code does not enforce it; drift risk exists. |
| INFO | Authority is clear and enforced; finding is purely observational (good pattern). |

## Confidence Levels

| Level | Definition |
|-------|-----------|
| high | grep-confirmed write operation or direct call chain visible in code. |
| medium | call chain partially traced or naming convention suggests pattern. |
| low | inferred from docs/naming only, no code evidence. |

## Evidence Classes

| Class | Definition |
|-------|-----------|
| direct-write | Surface writes to target via confirmed grep (.save, .write, INSERT, UPDATE). |
| call-chain | Surface calls writer through intermediate functions, chain traced. |
| inferred | Pattern suspected from structure/naming but not fully traced. |
| docs-only | Claim exists only in documentation, not verified in code. |

## Escalation Rules

**Tier 1 (self-contained, report inline):**
- Single pipeline owns the target with no competing writers.
- SSOT is proven by grep: only one write path reaches the target.
- Findings are LOW/INFO severity.
- No lifecycle conflicts or cross-module side effects detected.

**Tier 2 (flag to user, await decision):**
- Multiple writers found reaching the same target.
- Authority is ambiguous: two or more modules claim ownership.
- Unofficial or undocumented write paths exist alongside the canonical one.
- Evidence class is call-chain or inferred (not direct-write confirmed).
- Findings are MEDIUM severity with medium or low confidence.

**Tier 3 (stop and escalate immediately):**
- Competing pipelines with no coordination mechanism.
- Lifecycle conflicts: one pipeline creates, another mutates, a third deletes.
- Authority vacuum: no module claims ownership of a critical write target.
- Findings are CRITICAL or HIGH severity.
- Evidence class is direct-write for competing paths (confirmed, not suspected).

## Risk Priority Matrix

Combines severity and confidence into an action priority.

| | Confidence: high | Confidence: medium | Confidence: low |
|---|---|---|---|
| **CRITICAL** | P1: Block and escalate. Competing writes confirmed in code. | P1: Escalate with trace request. Pattern strongly suspected. | P2: Flag and trace. Competing writes possible but unconfirmed. |
| **HIGH** | P1: Block and escalate. Unofficial path confirmed. | P2: Flag and investigate. Unofficial path likely but needs tracing. | P3: Note and monitor. Unofficial path suspected from docs only. |
| **MEDIUM** | P2: Flag for review. Ambiguous authority confirmed. | P3: Note for next cycle. Ambiguous authority suspected. | P4: Informational. Weak signal, document only. |
| **LOW** | P3: Note for review. Doc/code drift confirmed. | P4: Informational. Possible drift. | P5: Dismiss or defer. Insufficient signal. |
| **INFO** | P4: Informational. Good pattern observed. | P5: Dismiss. No action needed. | P5: Dismiss. No action needed. |

**Action meanings:**
- P1: Present finding immediately, recommend blocking action (guard rail, deduplication, owner assignment).
- P2: Include in report with recommendation, do not block current work.
- P3: Include as note, no immediate action required.
- P4: Record for awareness, useful for future audits.
- P5: Skip or defer, noise below actionable threshold.
