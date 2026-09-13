---
name: claim-ledger
description: Systematic claim tracking with evidence classification. Prevents leakage of descartado inferences into final conclusions.
---

# Claim Ledger

## Purpose

Track every factual claim made during analysis. Classify each claim by verification status. Ensure that claims killed by evidence do not leak into conclusions.

## The problem: inference leakage

During analysis, you naturally generate hypotheses. Some get confirmed, some get discarded. Without a ledger, discarded inferences can silently persist in the final recommendation — creating a false sense of evidence.

## Claim classification

| Status | Symbol | Meaning | When to use |
|--------|--------|---------|-------------|
| **Verified** | ✅ | Evidence exists and supports the claim. Source is cited. | Fact is confirmed with traceable source. |
| **Partial** | ⚠️ | Some evidence exists but is incomplete or unverified. | Claim is plausible but needs confirmation. |
| **Discarded** | ❌ | Evidence contradicts the claim or no evidence exists after search. | The analysis explored this and ruled it out. |
| **Weak hypothesis** | 🟡 | No evidence for or against. Interesting but untested. | Worth noting but must not be treated as fact. |

## Rules

1. **Every claim gets one status.** No "verified-ish." Choose the most honest classification.
2. **Discarded claims must be explained.** Why was it discarded? What evidence killed it?
3. **Weak hypotheses must not appear in conclusions.** They go in a "hypotheses for exploration" section only.
4. **Verified claims require a source.** No verified claim without a citation or document reference.
5. **Ledger must be auditable.** Anyone should be able to retrace why each claim has its status.

## Method

### Step 1: Extract all claims

During or after analysis, list every factual assertion made:
- Direct quotes from input materials
- Inferences drawn from context
- Assumptions made for analysis
- Statistical claims (percentages, rates, sample sizes)
- Capability claims ("technology works for X")
- Compliance claims ("vendor is compliant with Y")

### Step 2: Classify each claim

For each claim, determine:
- Is there direct evidence? → ✅ Verified
- Is there partial evidence? → ⚠️ Partial
- Was it searched and not found? → ❌ Discarded
- Was it never checked? → 🟡 Weak hypothesis

### Step 3: Check for leakage

Search the entire analysis output for any reference to discarded claims. Flag:
- Recommendations that depend on discarded claims
- Risk assessments that assume discarded capabilities
- Stakeholder messages based on discarded assumptions

### Step 4: Generate summary

```
Total claims: N
- Verified: X (Y%)
- Partial: X (Y%)
- Discarded: X (Y%)
- Weak hypotheses: X (Y%)

Factual verdict: [PASS if >70% verified, PARTIAL if 40-70%, FAIL if <40%]
```

## Anti-patterns

1. **"Verified" without a source.** This is the most common error.
2. **Leaving discarded claims in the text.** If you evaluated something and ruled it out, remove it from conclusions.
3. **Promoting weak hypotheses to partial without evidence.** "Interesting" ≠ "plausible."
4. **Too few claims.** If your ledger has fewer than 10 claims for a complex partnership, you're not being granular enough.

## Output format

```
### Claim Ledger

| # | Claim | Status | Source / Evidence Required | Notes |
|---|-------|--------|---------------------------|-------|
| C1 | "..." | ✅ | [citation] | |
| C2 | "..." | ❌ | [why discarded] | |
| C3 | "..." | 🟡 | [what would verify this] | |

**Summary:** X verified, Y partial, Z discarded, W hypotheses
```

---

*Claim Ledger v1.0.0 — Strategic Partnership Toolkit*
