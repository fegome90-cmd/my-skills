---
name: actor-separation-checkpoint
description: Mandatory checkpoint during Phase 1. Forces explicit separation of all entities and flags conflation risks. Runs after source lock gate.
---

# Actor Separation Checkpoint

## Purpose

Ensure every entity in the analysis is treated as independent. Prevents the common error of treating a person as their employer, or conflating multiple organizations into a single "partner."

## When to use

After the source lock gate. Before any tool that analyzes stakeholders or relationships.

## Method

### Step 1: List all entities

```
Entity | Nature | Legal status | Decision authority | Relationship to others
-------|--------|-------------|-------------------|---------------------
Richard Cave | Person (SLT) | Individual | Personal initiative (not institutional) | Bridges CDLI/UCL and ElevenLabs
CDLI/UCL | Academic institution | University (UK) | Governing board | Employs Richard (partially)
ElevenLabs | Commercial company (US) | Corporation | Corporate leadership | Richard is Impact Partner (not employee)
FALP | Clinical institution (Chile) | Foundation | Board of directors | Potential recipient
Patients | Vulnerable population | Protected class under Ley 21.719 | Consent right | End users
```

### Step 2: Check for role splits

If a single entity serves multiple roles, document the split:
- Richard is: (a) researcher, (b) Impact Partner, (c) bridge person. These are different roles with different incentives.

### Step 3: Flag single points of failure

```
⚠️ SPOF: All partnership flows pass through Richard personally (email approvals,
licence distribution, ASR coordination). If Richard leaves CDLI or loses interest,
the partnership has no institutional backup.
```

### Step 4: Verify relationships

- Who employs whom?
- Who pays whom?
- Who is legally liable for what?
- Who owns what (data, IP, models)?

If any relationship is ambiguous, mark as [AMBIGUOUS — clarify with source].

## Anti-patterns

1. **"Cave" as entity.** "Cave" is a person. "Cave's company" does not exist. Use Richard Cave (person), CDLI (institution), ElevenLabs (vendor).
2. **"The partner" as singular.** When multiple entities are involved, "the partner" hides the real structure.
3. **Institution ≠ representative.** Richard's enthusiasm ≠ CDLI institutional commitment.

## Output format

```
### Actor Separation Checkpoint

**Entities identified:** N

| Entity | Nature | Status | Authority | Key risk |
|--------|--------|--------|-----------|----------|

**SPOFs:** [list]

**Ambiguities:** [list or "none"]

**Check:** [PASS / FAIL — reason]
```

---

*Actor Separation Checkpoint v1.0.0 — Strategic Partnership Toolkit*
