---
name: real-world-bug-hunter
description: "Use when you need to find real bugs in CLI tools or SDKs by running actual commands through parallel adversarial agents. Triggers for: bug hunt, hunt bugs, real world testing, adversarial CLI testing, fuzz memory CLI, test the actual CLI, find bugs in memory, stress test memory, parallel bug finding. Also triggers for: cazador de bugs, bug hunt orchestrator. Do NOT use for unit test writing, TDD coaching, code review, or static analysis."
search_hints: bug hunt adversarial CLI testing fuzz parallel agents real world
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.1.0"
  role: orchestrator
  scope: testing
  triggers:
    - "bug hunt"
    - "find bugs in"
    - "real world testing"
    - "adversarial testing"
    - "test the actual CLI"
    - "stress test memory"
    - "hunt bugs"
    - "cazador de bugs"
    - "parallel bug finding"
    - "fuzz memory CLI"
---

# Real-World Bug Hunter

Launches parallel agents that execute real CLI commands against a target project, finding bugs that unit tests miss. Each agent has a distinct testing personality — adversarial inputs, real-world workflows, or isolation boundaries — and findings are consolidated into a severity-rated report.

## Prerequisites

- **tmux-fork-orchestrator**: Required. Provides `tmux-live` (on PATH), envelope contracts, and agent lifecycle management.
- **Memory MCP or CLI**: Required. Provides persistence for hunt sessions and findings.

## When to Use / When Not to Use

| Use | Do NOT Use |
|-----|-----------|
| Finding real bugs in a CLI/SDK product | Writing unit tests |
| Testing actual CLI behavior end-to-end | Static code analysis |
| Stress-testing with adversarial inputs | TDD process coaching |
| Verifying cross-project data isolation | Code style review |
| Validating multi-step workflows | Fixing known bugs (use implementer) |

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--target` | Yes | CLI binary or command to test (e.g., `memory`, `fork`) |
| `--subsystems` | No | Comma-separated subsystems to test. Default: all |
| `--agents` | No | Which agent roles to deploy: `ripper`, `walker`, `sniper`, or `all`. Default: `all` |
| `--project` | No | Project name for memory persistence. Default: `bug-hunt` |
| `--intensity` | No | `quick` (15 min), `standard` (30 min), `deep` (60 min). Default: `standard` |

## Agent Role Mapping

| Bug-hunter role | tmux-live role | Catalog scenarios | Focus |
|----------------|---------------|-------------------|-------|
| ripper | explorer | adversarial, chaos | Malicious inputs, PII, injection, encoding |
| walker | implementer | basic | Multi-step workflows, roundtrips |
| sniper | verifier | adversarial, basic | Cross-project isolation, boundaries |

Note: tmux-live auto-prepends `fork-` to names. Actual session names become `fork-hunt-ripper-<ID>` etc.

## Procedure

### Phase 0: Pre-flight

1. Verify `tmux-live` is on PATH. If not, abort with error.
2. Verify `memory` CLI is available. If not, abort with error.
3. `tmux-live init` with enough slots (3 for full run).

### Phase 1: Plan

1. Determine target CLI and available subsystems from `resources/test-catalog.md`.
2. Select agent roles based on `--agents` parameter.
3. For each agent, select test scenarios from catalog matching its role (see Agent Role Mapping table).
4. Assign a unique session name per agent: `hunt-ripper-<ID>`, `hunt-walker-<ID>`, `hunt-sniper-<ID>`.

### Phase 2: Prepare

1. Record hunt metadata: `memory save "Bug hunt: <target> -- <date>" --type session-summary --project <project> --topic-key "bug-hunt/<target>/<date>"`.
2. For each agent, load `resources/skill-map.md` to determine which skills to resolve.
3. Write agent prompts to `/tmp/hunt-prompt-<role>-<ID>.txt` using `@file` delivery.
   - Prompt includes: role instructions (from resources/agent-*.md), target subsystems from test-catalog, skill resolution queries from skill-map, output format instructions with FORK_START/FORK_END markers.
4. Validate each prompt stays under 5000 chars (allows for agent instructions + scenarios + output format).

### Phase 3: Spawn

1. Spawn ALL agents before monitoring any of them.
2. Use `tmux-live launch <tmux-role> <name> @/tmp/hunt-prompt-<role>-<ID>.txt` (see Agent Role Mapping for tmux-role).
3. Agents use paid models only (never free models for parallel orchestration).
4. Each agent:
   - Resolves skills via `skill-hub` queries from skill-map.
   - Loads `resources/test-catalog.md` for scenario selection.
   - Executes real CLI commands, captures output.
   - Writes findings to `/tmp/hunt-findings-<role>.md` wrapped in `## FORK_START ##` / `## FORK_END ##` markers with the header: Status, Summary, Artifacts, Next, Risks.
5. If spawn fails (non-zero exit): log error, retry once. If retry fails, skip that agent and continue. If 0 agents spawned, abort.

### Phase 4: Monitor

1. Poll via `tmux-live status` and `tmux-live progress <name>`.
2. On agent completion: check output file exists and has content > 200 chars.
3. Failure policies: ripper=CONTINUE, walker=CONTINUE, sniper=CONTINUE.
4. Truncation detection: output < 200 chars → auto-retry with a focused prompt (strip to: role instructions + single failing scenario + output format, target <1500 chars).

### Phase 5: Consolidate

1. Read all `/tmp/hunt-findings-<role>.md` files.
2. Run `scripts/hunt-consolidate <dir>` to merge findings, deduplicate, apply severity classification.
3. Cross-validate: when 2+ agents find same bug independently, mark CONFIRMED.
4. Apply the "Can a real user trigger this?" filter: YES=fix, MAYBE=investigate, NO=report only.
5. Persist consolidated report: `memory save` with type `session-summary`.

### Phase 6: Report

1. Generate report using template from `resources/report-template.md`.
2. Present to user with executive summary, severity breakdown, and reproduction steps.
3. Verdict: PASS (no CRITICAL), PASS WITH WARNINGS (HIGH present but no CRITICAL), FAIL (any CRITICAL). INFO findings do not affect verdict.

### Phase 7: Cleanup

1. `tmux-live kill-all` to close agent panes.
2. Verify cleanup: `tmux-live list` should return empty. If not, kill remaining agents individually.
3. Save final hunt state: `memory save` with topic_key for future reference.
4. If memory save fails, write fallback to `/tmp/hunt-summary-<date>.md`.

## Key Distinctions

| Confusion | Correct |
|-----------|---------|
| "Run unit tests" | This skill runs REAL CLI commands, not test suites |
| "Code review" | This skill tests behavior, not code structure |
| "Debug a known bug" | This skill discovers unknown bugs |
| "Static analysis" | This skill exercises the actual runtime |
| "TDD" | This skill has no test-first cycle — it hunts |

## Resources Index

| Resource | When to Load | Lines |
|----------|-------------|-------|
| `resources/agent-ripper.md` | Phase 2 (spawn ripper) | ~60 |
| `resources/agent-walker.md` | Phase 2 (spawn walker) | ~60 |
| `resources/agent-sniper.md` | Phase 2 (spawn sniper) | ~70 |
| `resources/skill-map.md` | Phase 2 (skill resolution) | ~30 |
| `resources/test-catalog.md` | Phase 1 (planning) + Phase 3 (agent loads) | ~100 |
| `resources/report-template.md` | Phase 6 (reporting) | ~90 |
| `scripts/hunt-consolidate` | Phase 5 (consolidation) | ~110 |
