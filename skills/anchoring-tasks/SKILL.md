---
name: anchoring-tasks
description: Use when executing a task with an ANCHOR.yaml or explicit intent/done_when/not_doing boundaries, or when the user asks to anchor execution against scope drift or overengineering.
license: MIT
metadata:
  author: "Felipe Gonzalez"
  version: "0.3-rc1"
---

# Anchoring Tasks v0.3-rc1

## Purpose

Preserve the current task envelope while leaving implementation autonomous.

**Core rule:** choose the smallest sufficient solution that satisfies `done_when`. Anchor constrains task meaning and boundaries; it is not a plan, spec, path allowlist, or implementation recipe.

Anchor never grants authority to violate higher-priority instructions, safety constraints, or repository contracts.

## Anchor contract

Use exactly three task fields:

```yaml
intent: What this task is trying to achieve.
done_when:
  - Observable completion condition.
not_doing:
  - Explicitly excluded expansion.
```

If `intent` or `done_when` is missing or empty, or `not_doing` is missing, do not invent the missing contract. Ask for repair before consequential work.

## Critical Patterns

1. **Read before act.** Read the current Anchor before consequential work.
2. **No self-amendment.** Never weaken or reinterpret the Anchor to fit your solution. Only an explicit authorized revision from the human or higher authority may change it.
3. **`not_doing` wins.** Explicit exclusions override convenience, inferred future needs, and implementation preference.
4. **Implementation stays autonomous.** More files, tests, helpers, or reversible internal changes are not scope drift by themselves when they directly satisfy `done_when`.
5. **Evidence before PASS.** Every `done_when` criterion needs fresh evidence.

## Start

Before consequential work, emit only:

```text
ANCHOR START
intent: <one sentence>
path: <step> → <step> → <step if needed>
boundary: <relevant exclusion | none>
```

The path is a sanity check, not a technical plan. Then execute.

## During execution

Before adding a component, service, runtime, registry, persistence layer, dependency, control file, validator, deployment mechanism, or abstraction, ask:

> Can `done_when` be satisfied without this?

If yes, omit it and continue. If no, proceed only when the addition remains inside `intent` and `not_doing`.

If a necessary change crosses `not_doing`, changes `intent`, creates a new requirement, or materially enlarges responsibility, emit:

```text
ANCHOR ESCALATION
need: <what became necessary>
evidence: <why done_when cannot be met inside the envelope>
smallest_expansion: <minimum boundary change>
AWAITING_USER
```

Stop only the affected expansion. After an authorized revision, re-read the Anchor and emit a fresh `ANCHOR START` before continuing consequential work.

## End

When work stops, emit:

```text
ANCHOR END
result: PASS | FAIL | BLOCKED
done_when:
- PASS | FAIL — <criterion>: <fresh evidence>
scope_drift: none | <brief deviation>
```

`PASS` requires every criterion to pass with fresh evidence. Prefer existing tests, checks, or direct observation. Do not invent verification infrastructure merely to satisfy Anchor.

## Anti-no-op

Do not claim the skill was applied unless START precedes consequential work and END evaluates the current Anchor. Escalation is observable only when a real boundary crossing is blocked rather than silently accepted.

## Anti-Ferrari

Complexity must be necessary for `done_when` or materially reduce present risk. Anchor itself stays passive: no parser, schema, CLI, daemon, registry, lifecycle, lock, or state machine until repeated observed failures prove necessity.
