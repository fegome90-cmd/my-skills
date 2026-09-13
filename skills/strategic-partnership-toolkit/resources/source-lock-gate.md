---
name: source-lock-gate
description: Mandatory pre-analysis gate. Forces verbatim source quoting and explicit frame definition before any interpretation. Prevents problem drift.
---

# Source Lock Gate

## Purpose

Lock the problem frame BEFORE any analysis begins. Without this gate, agents silently reinterpret the source material and drift toward a different problem.

## When to use

**Always.** Before Phase 1, before any tool, before any interpretation.

This is not optional. If you skip it, you get the kind of drift where "voice banking for laryngectomy patients" becomes "medical scribe for clinical documentation."

## Method

### Step 1: Quote verbatim

Copy the core proposition from the source material word-for-word. Use blockquote format.

```
> [Exact quote from source]
```

If the source is an email, quote the key sentences. If a meeting, quote the notes. If a document, quote the central thesis.

### Step 2: Define the frame

```
This case IS about:
- [point 1]
- [point 2]
- [point 3]

This case IS NOT about:
- [common misinterpretation 1]
- [common misinterpretation 2]
- [adjacent problem that is NOT this problem]
```

Be explicit about what this is NOT. Most drift comes from conflating adjacent problem types.

### Step 3: Count and name entities

```
Independent entities identified: N

1. [Name] — [One-line description: person/institution/company/community/patient group]
2. [Name] — [One-line description]
3. [Name] — [One-line description]
```

Each entity must be independent. A person is not their employer. An institution is not its representative.

### Step 4: Verify no conflation

Check:
- [ ] No person treated as company
- [ ] No institution treated as person
- [ ] No vendor treated as partner institution
- [ ] No patient group treated as data source

If any conflation exists, split before proceeding.

## Fail conditions

The gate FAILS if any of these are missing:
- No verbatim quote from source
- No explicit "IS / IS NOT" frame
- Entities are conflated
- Frame drift toward a different problem type

When the gate fails: stop, correct, re-lock. Do not proceed with analysis.

## Output format

```
### Source Lock Gate — [date]

**Source:** [what was analyzed]

**Verbatim:**
> [quote]

**Frame:**
- IS about: [list]
- IS NOT about: [list]

**Entities (N):**
1. [Name] — [description]
2. ...

**Conflation check:** [PASS / FAIL — reason]
```

---

*Source Lock Gate v1.0.0 — Strategic Partnership Toolkit*
