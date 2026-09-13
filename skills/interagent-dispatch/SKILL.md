---
disable-model-invocation: true
name: interagent-dispatch
description: "Structure typed execution contracts and return receipts when dispatching subagents or delegating tasks. Triggers: subagent dispatch, task delegation, worker contracts."
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
---

# Interagent Dispatch Contract

Assemble typed execution contracts and structured return receipts for subagent dispatch and cross-agent delegation.

## When to Use

- Dispatching a subagent via `invoke_subagent`, CLI, or background worker
- Delegating bounded tasks across agent boundaries
- Structuring parallel agent work without shared-state collision
- Enforcing deterministic `result_receipt` returns instead of unstructured chat replies

## Dispatch Protocol (5 Steps)

1. **Classify task profile:** Identify the smallest sufficient profile (`BASIC`, `CONTROLLED`, `GOVERNED`, `FULL_ANTIDRIFT`).
2. **Freeze inputs and authority:** Record baseline commits, absolute paths, and define the single authority entrypoint.
3. **Assemble contract payload:** Load the matching template from [resources/templates.md](resources/templates.md).
4. **Dispatch worker:** Send the contract payload to the subagent.
5. **Parse and validate receipt:** Verify the worker returned the structured YAML or JSON receipt defined in [resources/receipt-schemas.md](resources/receipt-schemas.md).

## Profile Selection Matrix

| Profile | Substantive Scope | Typical Triggers | Context Load |
|---|---|---|---|
| `BASIC` | Task + Scope + Bounded Verification | Typo fix, single-file reading, simple lookup | Minimal (~50 tokens) |
| `CONTROLLED` | + Pre-flight Discovery + Hard Stops + Secret Gate | Script edit, local test run, single-component fix | Lean (~200 tokens) |
| `GOVERNED` | + Staging + Rollback + Candidate Freeze + Envelopes | Multi-file mutation, shared runtime config, DB schema | Structured (~450 tokens) |
| `FULL_ANTIDRIFT` | + Evidence Integrity + Anti-Drift Taxonomy + BMCC | Benchmark, adversarial audit, long-horizon multi-step | Full (~800 tokens) |

**Dynamic Escalation Rule:** Start at the lowest sufficient profile. Escalate immediately (`BASIC → CONTROLLED → GOVERNED → FULL_ANTIDRIFT`) when persistent state, secrets, or human decisions emerge. Maintain profile stability throughout execution; retain or escalate the assigned profile strictly.

## Invariant Rules for Dispatchers

- **Positive Scope:** Specify allowed targets explicitly (`Operate exclusively inside <path>`). Frame boundaries with affirmative constraints.
- **Fail-Closed Hard Stops:** Every unexpected failure, missing dependency, or scope ambiguity must trigger immediate stop and return `status: blocked` or `status: failed`. Escalate directly upon blocker encounter.
- **Evidence vs Authority:** The worker generates evidence (`command`, `exit_code`, `diff`). The orchestrator holds decision authority.
- **Mandatory Typed Return:** The worker must conclude execution with the standard `result_receipt` YAML or JSON receipt.

## Format Modes (Markdown vs Compact JSON)

Choose payload format by transport:
- **Markdown Mode:** Default for interactive chat and subagent prompts where visual inspection matters.
- **JSON (A2A RPC) Mode:** High-efficiency transport for programmatic pipes, API workers, and tight token budgets. Guarantees 0-ambiguity machine parsing with `JSON.parse()`.

## Resources

- [resources/templates.md](resources/templates.md) — Ready-to-copy dispatch templates (Markdown & JSON) for all 4 profiles.
- [resources/receipt-schemas.md](resources/receipt-schemas.md) — Typed JSON and YAML receipt schemas and validation rules.

