---
name: ai-work-prompting-gates
description: "Use when authoring or reviewing agent prompts that need gated execution over repos, local files, runners, or pipelines. Establishes audience separation, executable gates (discovery, staging, rollback, validation), and strict claim discipline (no PASS without evidence)."
search_hints: prompting gates agent workflow L2 gated workflow runtime discovery staging promotion rollback claim discipline lifecycle crash-safety authority vs evidence
metadata:
  status: reference-only
  tier: D1-method-note
  authority: non-normative
---

# AI Work Prompting Gates

Lightweight prompting standard and checklist for agent-driven execution. Designed for authoring and auditing robust agent prompts operating on local files, repositories, runners, and automated pipelines.

> [!NOTE] Non-Normative Reference Guide
> This skill is a **reference-only method note** (`tier: D1-method-note`, non-normative). It does not compete with or override binding system execution contracts (such as the D1 Agent Execution Contract). It provides a practical architectural blueprint and checklist for prompt authors.

## When This Skill Applies

- Authoring or auditing prompts for agents that will inspect or mutate code, configurations, or repositories.
- The prompt mixes conversational advice for human/ChatGPT with operational commands for local agent execution.
- Quality gates say "validate" or "verify" without specifying a command, exit code, or expected artifact.
- The agent is permitted to declare "PASS", "stable", or "production-ready" without verifiable evidence.

Do **not** use for simple informational chat prompts, non-executing drafting tasks, or trivial L0/L1 conversational instructions.

## Core Conceptual Model

### Prompt Taxonomy

| Level | Pattern | Typical Use Case |
|---|---|---|
| **L0 Raw** | Freeform text instructions | Brainstorming, general questions, zero execution |
| **L1 Structured** | Ordered steps with explicit output format | Documentation drafts, simple code formatting |
| **L2 Gated Workflow** | **Phases + Executable Gates + Artifact Receipts** | **Default for autonomous/local agents, runners, scripts, tools** |
| **L3 Multi-Role** | Explicit roles, adversarial reviews, provenance chains | Complex multi-model audits, security-critical migrations |

### Audience Separation Rule

| Audience | Belongs in Prompt | Must NOT Appear in Prompt |
|---|---|---|
| **Prompt Analyst** | Evaluation criteria, trade-offs, method rationale | Low-level execution steps for local agents |
| **Local Agent / Executor** | Bounded scope, CLI commands, gates, exit criteria | Generic LLM advice, conversational meta-rules |
| **Repo / Runtime** | Code, tests, migrations, schemas, scripts | Unenforced governance assertions |
| **Library / SSOT** | Source documents, authorities, status metadata | Ephemeral runtime assumptions |

> **The Separation Rule:** If an instruction exists only to keep a conversational assistant from hallucinating, it does not belong in the operational prompt of an automated agent.

## Procedure: Authoring & Auditing Gated Prompts

### Phase 1: Audience & Scope Boundary
1. Identify the single intended recipient (human, subagent, CLI runner).
2. Define explicit boundaries:
   - **Allowed:** exact directories, files, or command categories.
   - **Forbidden:** destructive operations, out-of-scope files.
   - **Out of Scope:** related tasks that should not be touched in this turn.

### Phase 2: Authority & Runtime Preflight
1. Define the decision owner vs. the execution agent.
2. Formulate the Runtime Discovery Gate: verify tools, binaries, versions, and current git baseline before applying changes.
3. Fail-closed on missing secrets or invalid environments.

### Phase 3: Lifecycle, Staging & Rollback
1. Require staging for intermediate mutations (`staging/<run_id>/` or branch/worktree).
2. Specify atomic promotion: promote only after all verification gates return exit code 0.
3. Define the rollback procedure on failure.

### Phase 4: Executable Validation & Claim Discipline
1. Replace vague directives ("Make sure it works") with concrete executable gates:
   - Specific command (e.g. `pytest tests/test_parser.py -q`)
   - Expected exit code (e.g. `0`)
   - Expected artifact or stdout signature
2. Enforce Claim Discipline: prohibit claiming "PASS" or "stable" without citing the exact command, exit code, and generated artifact.
3. Mandate reporting of residual risks and unverified assumptions.

## L2 Gated Prompting Skeleton

```markdown
# TASK — Single bounded executable task
# CONTEXT — Minimal context strictly for THIS agent
# SCOPE — Allowed / Forbidden / Out of scope
# AUTHORITY GATE — Execution owner, decision owner, authoritative source vs evidence surfaces
# RUNTIME DISCOVERY GATE — Tool existence, versions, paths, clean baseline
# SECRET HANDLING GATE — Fail closed, never log secrets
# OWNERSHIP GATE — Single process/agent per mutated surface
# LIFECYCLE / CRASH-SAFETY GATE — Initial -> In Progress -> Promoted / Failed / Rolled Back + Staging
# VALIDATION GATE — Deterministic command, exit code 0, artifact assertion
# DEGRADATION / REGRESSION GATE — Before/after metrics comparison
# OBSERVABILITY GATE — run_id, timestamps, logs, execution receipt
# CLAIM DISCIPLINE GATE — No PASS without proof; enumerate residual risks
# DELIVERABLES — File changes, commands run, receipts, open questions
```

For the complete verbatim template, see `resources/l2-template.md`.

## Canonical Anti-Patterns

| Anti-Pattern | Root Cause | Correction |
|---|---|---|
| **Gate without mechanism** | "Make sure it's valid and safe" | Specify command, exit code 0, and artifact assertion. |
| **Audience mixing** | LLM advice mixed with shell commands | Separate analyst guidance from agent execution tasks. |
| **Strong claim without proof** | "All systems verified and stable" | Enforce Claim Discipline: cite evidence + residual risks. |
| **Implicit direct staging** | Modifying live configs in-place | Isolate changes in staging; promote atomically on PASS. |

For expanded explanations and examples, see `resources/anti-patterns.md`.

## Local Agent Execution Pattern

When targeting agents operating on a local workstation or runner:
1. Preflight git status, current directory, and tool binaries.
2. Isolate mutations in `staging/<run_id>/`.
3. Validate staging outputs before promoting.
4. Auto-rollback on test failure.
5. Emit execution receipts with run_id, diffs, and residual risks.

See `resources/local-adaptation.md` for complete bash snippets.

## Pre-Dispatch Prompt Checklist

Before dispatching an agent prompt, verify:
- [ ] Single intended recipient declared (no audience mixing)?
- [ ] Allowed, forbidden, and out-of-scope boundaries explicit?
- [ ] Decision owner vs execution agent identified?
- [ ] Runtime discovery / preflight commands specified?
- [ ] Staging and rollback paths defined for mutating operations?
- [ ] Every gate specifies an executable command, expected exit code, and artifact assertion?
- [ ] Claim discipline enforced (no PASS/stable claims without proof)?
- [ ] Residual risks and unverified assumptions required in final output?
