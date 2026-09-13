
> **Prerequisite:** Complete `resources/source-evidence-ledger.md` before this tool. Every claim must trace to a source class.
---
name: strategic-situation-assessment
description: Use this skill when analyzing a strategic signal such as an email, meeting note, partner proposal, institutional opportunity, negotiation cue, or ambiguous stakeholder message. The skill extracts actors, incentives, implied deadlines, assumptions, risks, options, and the next recommended move.
---

# Strategic Situation Assessment

## Purpose

Convert ambiguous strategic inputs into a clear decision frame.

This skill is especially useful when the input contains:
- A partner message.
- A meeting summary.
- A possible institutional opportunity.
- A politically sensitive proposal.
- A weak signal with an implicit deadline.
- A collaboration that may become operational.

Do not produce generic business advice. The output must help the user decide what to do next.

## Required inputs

Ask for missing information only if it is truly blocking. Otherwise proceed with assumptions clearly marked.

Minimum useful input:
- Original message, note, or situation.
- Known actors.
- Desired outcome, if available.
- Constraints, if available.

## Method

1. Identify the strategic signal.
   - What is explicitly being said?
   - What is implied but not said?
   - What opportunity is being created?
   - What pressure or deadline is hidden in the message?

2. Map actors and incentives.
   - Who benefits if this advances?
   - Who carries operational burden?
   - Who can block it?
   - Who gains reputation, data, access, legitimacy, evidence, or visibility?

3. Separate facts from interpretation.
   Use three categories:
   - Verified facts.
   - Reasonable inferences.
   - Speculative hypotheses.

4. Identify the clock.
   - Is there an explicit deadline?
   - Is there an implicit presentation, funding, pilot, partner, political, or reputational clock?
   - What becomes harder if no action happens soon?

5. Detect strategic risks.
   - Overcommitment.
   - Institutional misalignment.
   - Ethical or legal exposure.
   - Data governance gaps.
   - Dependency on external partner.
   - Unclear ownership.
   - Public claims ahead of evidence.

6. Define options.
   Produce at least three:
   - Conservative option.
   - Focused fast option.
   - Ambitious option.

7. Recommend one next move.
   It must be narrow, realistic, and owned by a specific role.

## Output format

### Veredicto

State the strategic reading in 2–4 sentences.

### Qué está explícito

List the direct facts from the input.

### Qué está implícito

List reasonable inferences. Mark confidence as High / Medium / Low.

### Actores e incentivos

Use a table with:
Actor | Likely interest | What they need | Risk if ignored

### Reloj estratégico

Explain the timeline pressure and what must exist before the next milestone.

### Riesgos principales

Prioritize by probability × severity × exposure.

### Opciones

Conservative / Focused fast / Ambitious.

### Recomendación

One recommended move, with owner, next artifact, and boundary.

### Frase útil para responder

Provide a short draft phrase that preserves optionality and avoids overcommitment.

## Quality gates

Before finalizing, verify:
- No claim is treated as fact unless present in the input.
- The recommendation does not overcommit the institution.
- The output names the implied deadline if one exists.
- The next step is operational, not motivational.
- The answer separates opportunity from proof.
