# Grill Phase — Interactive Stakeholder Interrogation

**When:** Step 4.5, after audit report, before Step 5 (Fix or Flag).
**Trigger:** Stakeholder (user) is present in the session and the audit has non-🟢 elements.

## Purpose

Resolve as many questions as possible *in the moment* by interrogating the stakeholder. Each answer can reclasify elements from 🟡/🟠 to 🟢, potentially upgrading the verdict from FAIL to PASS-WITH-WARNINGS or PASS.

## Protocol

### Phase A: Prioritize Questions

From the audit report's "Questions for Stakeholders" section, order by impact:

1. **🔴 FABRICATED** questions first — these block delivery
2. **🟠 ASSUMED** questions second — these can trigger DRAFT labeling
3. **🟡 INFERRED** questions third — these improve confidence
4. **⚪ OUTDATED** questions last — these are usually quick corrections

### Phase B: Ask Relentlessly

For each question, follow this pattern:

```
FOR EACH unresolved element (priority order):

  1. STATE the element and its current classification
     "ELEMENT-05 is classified as 🟠 ASSUMED. The label 'Equipo Nutricional' has no evidence."

  2. ASK a specific, answerable question
     "¿Existe un equipo nutricional formal en la organización? Si sí, ¿quién lo integra?"

  3. PROVIDE your recommended answer (based on context/patterns)
     "My recommendation: Hospital nutrition processes typically have a nutritionist
      and a treating physician. A formal 'committee' is less common. Consider
      replacing with 'Nutricionista + Médico tratante revisan caso'."

  4. WAIT for the stakeholder's answer. Do NOT proceed until answered.

  5. RECLASSIFY based on the answer:
     - Clear confirmation → 🟢 CONFIRMED
     - Partial answer → 🟡 INFERRED (with updated source)
     - "I don't know" → keep current tag or downgrade to 🟠 ASSUMED
     - Correction → ⚪ OUTDATED, then apply correction → 🟢 CONFIRMED

  6. BRANCH on dependent questions
     If the answer to this question affects other elements, update those too.
     Example: If "Equipo Nutricional" is confirmed → all elements referencing
     that team get upgraded. If denied → all referencing elements get downgraded.

  7. RECALCULATE verdict after each reclassification
     Stop early if verdict reaches PASS (all elements 🟢).
```

### Phase C: If Stakeholder Explores Codebase

If a question can be answered by exploring the codebase or existing documentation, **explore it** instead of asking. Per the grill-me principle: don't ask what you can verify yourself.

Actions that count as verification:
- Reading official domain/system documentation in the project
- Checking prior stakeholder communications in memory
- Searching for the role/process in project wiki or docs

### Phase D: Close Grill

After all questions are resolved or the stakeholder can't answer more:

1. Show updated tag distribution (before → after)
2. Show updated verdict
3. List any remaining unresolved elements
4. Proceed to Step 5 (Fix or Flag) with the updated classifications

## Example Grill Interaction

```
AGENT: The audit found 10 elements. 6 need resolution. Starting with 🔴/🟠...

ELEMENT-05 is 🟠 ASSUMED: "Equipo Nutricional" reviews the plan.
No evidence this team exists in the verified domain specs.
Question: ¿Existe un equipo nutricional formal?
My recommendation: Replace with "Nutricionista revisa con médico tratante".

USER: Sí, hay un equipo. Lo conforman la nutricionista y el médico de cabecera.

AGENT: → Reclassified ELEMENT-05: 🟠 → 🟢 CONFIRMED.
   Updated role: "Nutricionista + Médico de cabecera"
   Also updating ELEMENT-07 (references same team): 🟡 → 🟢 CONFIRMED.
   Verdict: FAIL → still FAIL (2 🟡 remain, but improving)...

[continues with next question]
```

## Skip Conditions

Do NOT run the grill phase if:
- All elements are already 🟢 → verdict is PASS, nothing to grill
- No stakeholder present → go directly to Step 5
- Quick audit (≤5 elements) → unless specifically requested
- User explicitly says "skip grill" or "just flag them"
