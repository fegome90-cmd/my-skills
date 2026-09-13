---
name: learned-structured-review
description: "Use when providing structured feedback on any deliverable — code PRs, documentation, presentations, design specs, architecture decisions — using the BLOCK/WARN/SUGGEST severity framework with numbered issues and concrete fixes."
search_hints: "structured feedback, structured review, BLOCK WARN SUGGEST, code review methodology, revisar, review feedback, PR review, prioritized feedback, numbered issues"
metadata:
  triggers:
    - "structured feedback"
    - "structured review"
    - "revisión estructurada"
    - "BLOCK WARN SUGGEST"
    - "revisar con severidad"
    - "PR review"
    - "code review"
    - "documentation review"
    - "presentation review"
    - "design review"
    - "architecture review"
    - "revisalo como si fuera código"
    - "review with severity"
  role: specialist
  scope: review
version: "1.1.0"
---

# Structured Review Framework (BLOCK/WARN/SUGGEST)

## Context

When reviewing any deliverable — code PRs, documentation, presentation scripts, design specs, architecture decisions — the natural tendency is to give unstructured feedback: pointing out one thing, then another, without prioritizing. The creator doesn't know what's critical vs what's a nice-to-have.

## Problem

Unstructured feedback leads to two failure modes:
- **Everything gets fixed** — wasted effort on low-impact changes
- **Nothing gets fixed** — overwhelmed by unfiltered issues

Both waste time and produce worse outcomes than a structured alternative.

## Solution

Use a severity framework adapted from code review:

| Severity | Meaning | When to Use |
|----------|---------|-------------|
| **🔴 BLOCK** | Must fix | Error, contradiction, security issue, broken functionality, critical missing piece |
| **🟡 WARN** | Should fix | Weak structure, unclear logic, poor naming, missing context, rough transitions |
| **🔵 SUGGEST** | Nice to have | Style preference, minor refactor, future optimization, personal taste |

### Process

1. **Review everything first** — Read the full deliverable before commenting
2. **Assign each finding → numbered issue** — "B1", "W3", "S2" (prefix + sequential)
3. **Pair every issue with a concrete fix** — Never flag without suggesting how to resolve
4. **Group by severity** — Present BLOCK → WARN → SUGGEST in order
5. **Summarize** — Total count per severity, one-line verdict
6. **Offer to apply** — Ask before making changes (unless explicitly requested)

### What to check by review type

| Review Type | Look for |
|-------------|----------|
| **Code PR** | Logic errors, edge cases, naming, test coverage, security, performance |
| **Documentation** | Factual accuracy, completeness, acronyms, tone consistency, audience fit |
| **Presentation scripts** | Flow between slides, transitions, repeated patterns, double-closings, rhythm |
| **Design specs** | Feasibility, consistency with patterns, accessibility, edge cases |
| **Architecture docs** | Assumptions stated? Tradeoffs explicit? Dependencies mapped? |

## Examples

### Code PR review
```
## 🔴 BLOCK
| # | File | Issue | Fix |
|---|------|-------|-----|
| B1 | auth.ts:45 | Missing input validation on userId | Add zod schema or guard clause |
| B2 | db.ts:12 | SQL injection via raw query interpolation | Use parameterized query |

## 🟡 WARN
| # | File | Issue | Fix |
|---|------|-------|-----|
| W1 | handler.ts:88 | Variable name `x` is meaningless | Rename to `retryCount` |
| W2 | test/spec.ts | No edge case test for empty array | Add `it('handles empty array')` |

## 🔵 SUGGEST
| # | File | Issue | Fix |
|---|------|-------|-----|
| S1 | utils.ts | Duplicate helper in two files | Extract to shared module |

Summary: 2 BLOCK, 2 WARN, 1 SUGGEST. Ready after BLOCK fixes.
```

### Presentation script review
```
## 🔴 BLOCK
| # | Slide | Issue | Fix |
|---|-------|-------|-----|
| B1 | 27+28 | Double closing (both say "Thanks") | Keep only one at end |

## 🟡 WARN
| # | Slide | Issue | Fix |
|---|-------|-------|-----|
| W1 | 05 | "But" forced transition | Change to "Now then..." |
| W2 | 12 | MASCC acronym not expanded | Add "(Multinational Association...)" |

## 🔵 SUGGEST
| # | Slide | Issue | Fix |
|---|-------|-------|-----|
| S1 | 03 | Dense paragraph, no breathing room | Add [pause] markers |

Summary: 1 BLOCK, 2 WARN, 1 SUGGEST. Core sound.
```

### Documentation review
```
## 🔴 BLOCK
| # | Section | Issue | Fix |
|---|---------|-------|-----|
| B1 | Quickstart | Installation command is wrong | Change `npm run` to `npx` |

## 🟡 WARN
| # | Section | Issue | Fix |
|---|---------|-------|-----|
| W1 | API Ref | No example for error response | Add 400 response example |

## 🔵 SUGGEST
| # | Section | Issue | Fix |
|---|---------|-------|-----|
| S1 | Overview | Could add a diagram | Link to architecture diagram |

Summary: 1 BLOCK, 1 WARN, 1 SUGGEST.
```

## Activation Signals

- User asks to "revisar" or "review" something (code, doc, script, design)
- User says "revisalo como si fuera código" or similar
- User asks to "mejorar" content with vague criteria
- A multi-file or multi-section deliverable needs consistent review
- PR feedback that should be actionable, not just commentary
- Any scenario where "all issues feel equally important" is the problem

## Relationship to Other Review Skills

This skill provides the **output format** and **severity framework**. Pair it with domain-specific skills in this repo or generic domain analysis:

| If reviewing... | Pair with |
|----------------|-----------|
| Code / Security | `skill-vetting`, `quality-plan-loop`, or repo test suite |
| Architecture / Authority | `authority-flow-audit`, `diagram-auditor` |
| Declarative prose / claims | `learned-accuracy-fallacy-audit` |
| Technical scripts | `scripting-technical-presentations` |
