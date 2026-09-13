---
name: decision-matrix-weighted
description: Weighted decision matrix with multi-state scoring for partnership evaluation. Separates exploration, due diligence, and pilot phases. Prevents binary PASS/FAIL traps.
---

# Weighted Decision Matrix

## Purpose

Replace binary PASS/FAIL with a structured, weighted, multi-state decision matrix. Prevents the common trap of giving a single "PASS" to an opportunity that is only viable in early phases and dangerous in later ones.

## When to use

- Any partnership or pilot opportunity that involves patient data, institutional resources, or external vendors.
- When the previous analysis used a binary verdict and needs upgrade.
- Before a decision memo: the matrix feeds into the memo with honest scores per phase.

## Core principle

**Different phases have different risk profiles.** An opportunity that scores 4/5 in exploration may score 1/5 in pilot. The matrix must show this honestly.

## Method

### Step 1: Define criteria

Use 5-8 criteria. Recommended defaults for health/institutional partnerships:

| # | Criterion | Weight | Why |
|---|-----------|--------|-----|
| 1 | Clinical value | 4-5 | Does this solve a real problem? |
| 2 | Technical feasibility | 3-4 | Can we actually do this? |
| 3 | Legal risk | 3-4 | Regulatory exposure |
| 4 | Ethical risk | 3-4 | Patient protection, sensitive data |
| 5 | Operational cost | 2-3 | Can we afford it? |
| 6 | External dependency | 2-3 | Vendor lock-in, uptime |
| 7 | Institutional opportunity | 2-3 | Timing, positioning |

**Weight sum target:** 20-26 range. Clinical value and legal/ethical risk should carry the most weight.

Customize criteria for context (e.g., add "scalability" for tech partnerships, "publishability" for academic).

### Step 2: Define evaluation states

Always separate at least three:

| State | Definition | No patient data? | Contractual commitment? |
|-------|-----------|-------------------|------------------------|
| **Exploración estratégica** | Desktop review, email exchange, meetings | ✅ Yes | ❌ No |
| **Due diligence pre-paciente** | Legal review, BAA, data flow design, vendor audit | ✅ Yes | ⚠️ Conditional |
| **Piloto clínico** | Actual pilot with real patients/data | ❌ No | ✅ Required |

Add intermediate states if needed (e.g., "MVP técnico sin pacientes").

### Step 3: Score each cell

- Scale: 1 (very unfavorable) to 5 (very favorable)
- Score = weight × raw score
- Add evidence note to every cell — no score without justification

### Step 4: Calculate totals per state

Sum weighted scores, normalize to /5:

| State | Raw sum | Weighted | Normalized (/5) | Level |
|-------|---------|----------|-----------------|-------|
| Exploración | 25/35 | 103/175 | 2.94 | ⚠️ Proceed with caution |
| Due Diligence | 17/35 | 71/175 | 2.03 | 🔴 Insufficient |
| Piloto clínico | 13/35 | 53/175 | 1.51 | 🔴 Very insufficient |

**Thresholds (guideline):**
- ≥ 3.5: Favorable
- 2.5-3.4: Conditional — proceed with caution
- 1.5-2.4: Insufficient — major gaps
- < 1.5: Very insufficient — high risk

### Step 5: Interpret honestly

- If exploration scores well but pilot scores poorly → the opportunity is real but premature.
- If all states score poorly → the opportunity is not viable at any phase.
- If pilot scores well but exploration poorly → someone is skipping steps (red flag).

## Anti-patterns to avoid

1. **Binary PASS/FAIL.** Always use weighted multi-state. Binary hides the phase reality.
2. **Scoring without evidence.** Every cell needs a source note.
3. **Averaging away the extremes.** Don't use a single "average" — the worst state matters most.
4. **Inflating exploration scores.** Exploration is cheap and low-risk. Of course it scores well. The meaningful test is pilot readiness.
5. **Changing weights to justify a preferred outcome.** Set weights before scoring, not after.

## Output format

See `output-templates.md` — Tool 3.5 (Decision Matrix Template).

---

*Decision Matrix v1.0.0 — Strategic Partnership Toolkit*
