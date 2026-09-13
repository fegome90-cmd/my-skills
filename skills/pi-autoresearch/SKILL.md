---
name: pi-autoresearch
description: "Autonomous research loops using pi-coding-agent with metric-gated experimentation. Invoke pi agents from OpenClaw, measure baselines, validate changes, and persist only proven improvements."
when: "When Felipe asks to run autoresearch, optimize something with experiments, invoke pi agents, or do hypothesis-driven development"
examples:
  - "Corre autoresearch para optimizar X"
  - "Invoca pi con autoresearch"
  - "Mide baseline antes de implementar"
  - "Experimenta con pi para mejorar Y"
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
  openclaw:
    requires:
      bins: [pi]
    emoji: "🔬"
---

# Pi Autoresearch

Run autonomous research loops using **pi-coding-agent** from OpenClaw. Metric-gated: baseline → risk assessment → implement → validate → persist. No unmeasured changes.

## Quick Reference

```bash
# One-shot invocation (fire and forget)
pi -p --no-session --provider zai --model glm-5-turbo "task description"

# With autoresearch skill
pi -p --no-session --provider zai --model glm-5-turbo \
  --skill ~/.pi/agent/skills/autoresearch-create \
  "optimize Papers MCP cache hit rate for oncology wiki"

# RPC mode (programmatic stdin/stdout)
pi --mode rpc --no-session --provider zai --model glm-5-turbo

# With specific model override
pi -p --no-session --provider zai --model glm-5-turbo \
  --model glm-5-pro "complex reasoning task"
```

## Architecture

```
OpenClaw (orchestrator)
  │
  ├── exec(bash) ──→ pi CLI ──→ pi-agent (GLM-5)
  │                            ├── autoresearch skill
  │                            ├── autoresearch-gate skill
  │                            └── target codebase
  │
  ├── papers__* MCP ──→ multi-platform search
  ├── pubmed__* MCP ──→ biomedical search + fulltext
  └── engram ──→ decisions, baselines, lessons
```

## When to Use

| Use This | Don't Use This |
|----------|----------------|
| Optimize a measurable metric (latency, coverage, hit rate) | Creative exploration without target metric |
| Validate a code change with before/after evidence | Post-commit build/lint checks |
| Choose between implementations via risk scoring | General debugging |
| Cross-repo optimization experiments | One-off tasks without iteration need |

## Modes

| Mode | Trigger | Produces |
|------|---------|----------|
| **one-shot** | Quick task, no experiment loop | pi output, no metrics |
| **research** | `autoresearch-create` skill | Experiment loop with metrics |
| **gate** | `autoresearch-gate` skill | Metric-gated implementation |
| **validate** | Gate Phase 1-2 only | Baseline report + gap analysis |

## The 5-Phase Gate Procedure

See `resources/gate-procedure.md` for full details.

### Phase 1: Baseline
```bash
# Initialize + measure current state
pi -p --no-session --provider zai --model glm-5-turbo \
  --skill ~/.pi/agent/skills/autoresearch-gate \
  "run baseline: measure current Papers MCP cache hit rate for oncology wiki queries"
```

### Phase 2: Risk Assessment
Score implementation options using risk matrix (see `resources/risk-matrix.md`).

### Phase 3: Implement + Validate
```bash
pi -p --no-session --provider zai --model glm-5-turbo \
  --skill ~/.pi/agent/skills/autoresearch-gate \
  "implement O-1: add semantic caching to Papers MCP queries, then validate against baseline"
```

### Phase 4: Persist
Log result, commit with structured message, save lesson to engram.

### Phase 5: Next
Return to Phase 1 for next opportunity.

## Pi Invocation Patterns

### One-shot (most common from OpenClaw)
```bash
pi -p --no-session --provider zai --model glm-5-turbo "describe the extension API in pi-coding-agent"
```

### With Extensions
```bash
pi -p --no-session --provider zai --model glm-5-turbo \
  --extension ~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/extensions/pi-autoresearch \
  "run experiment"
```

### With Skills
```bash
pi -p --no-session --provider zai --model glm-5-turbo \
  --skill ~/.pi/agent/skills/autoresearch-gate \
  "implement opportunity O-3"
```

### RPC (programmatic)
```bash
echo '{"prompt": "analyze this code", "tools": ["read", "bash"]}' | \
  pi --mode rpc --no-session --provider zai --model glm-5-turbo
```

### Background (long experiments)
```bash
pi -p --no-session --provider zai --model glm-5-turbo \
  --skill ~/.pi/agent/skills/autoresearch-create \
  "optimize context pack coverage for Go repos" \
  > "${TMPDIR:-/tmp}/pi-experiment.log" 2>&1 &
```

## Available Pi Skills

| Skill | Path | Purpose |
|-------|------|---------|
| autoresearch-create | `~/.pi/agent/skills/autoresearch-create` | Setup experiment loop (interactive prompts → autoresearch.md + loop) |
| autoresearch-gate | `~/.pi/agent/skills/autoresearch-gate` | Metric-gated implementation (baseline → risk → implement → validate) |
| autoresearch-finalize | `~/.pi/agent/skills/autoresearch-finalize` | Convert noisy branch into clean 1-branch-per-change PRs |
| autoresearch-hooks | `~/.pi/agent/skills/autoresearch-hooks` | before.sh/after.sh per iteration |

## Provider Configuration

| Provider | Model | Env Var | Notes |
|----------|-------|---------|-------|
| zai | glm-5-turbo | `ZAI_API_KEY` | Default for autoresearch — fast, cheap |
| zai | glm-5-pro | `ZAI_API_KEY` | Complex reasoning |
| openai | gpt-4o | `OPENAI_API_KEY` | Fallback |
| anthropic | claude-sonnet | `ANTHROPIC_API_KEY` | High quality |

## Integration with Papers MCP

When running autoresearch on search/bibliography tasks, use Papers MCP tools from OpenClaw side:

```bash
# OpenClaw measures baseline
papers__search_papers(query="...", sources=["pubmed","openalex"], limit=10)
# Record: cache_hit_rate = 0.3, unique_repos_found = 5

# Pi agent implements optimization
pi -p --no-session --provider zai --model glm-5-turbo \
  "improve search query construction for oncology terms in the wiki pipeline"

# OpenClaw validates against baseline
papers__search_papers(query="...", sources=["pubmed","openalex"], limit=10)
# Record: cache_hit_rate = 0.7, unique_repos_found = 12 → PASS
```

## Persistence

| Storage | What | Survives |
|---------|------|----------|
| `autoresearch.jsonl` | Experiment runs with metrics + ASI | Restarts, context resets |
| `autoresearch.md` | Living document: objective, dead ends, wins | Restarts |
| `autoresearch.ideas.md` | Hypothesis backlog | Restarts |
| Engram | Decisions, baselines, lessons | Cross-session |

## Limitations

- `pi -p --no-session` gives only final output, no real-time feedback
- Pi has its own tool set (read, bash, edit) — does NOT share OpenClaw tools
- Without TTY, no shortcuts or dashboard
- For long loops, use `exec(background=true)` or spawn subagent

## Resources

| File | Purpose |
|------|---------|
| `resources/gate-procedure.md` | Full 5-phase procedure with rollback protocol |
| `resources/risk-matrix.md` | Option scoring framework (1-10 × 5 dimensions) |
| `resources/experiment-template.md` | Hypothesis-prediction-result format |
| `resources/pi-quickref.md` | Pi CLI commands, modes, flags cheat sheet |
| `resources/opportunity-validation.md` | Implement + validate mode details |

## Wiki Reference

- `vault/orchestration-wiki/pi_systems/` — Full pi documentation wiki
- Key pages: `pi_extensions.md`, `pi_invocation.md`, `pi_autoresearch.md`, `pi_providers_models.md`

---

**Version:** 1.0.0 | **Updated:** 2026-06-02 | **Source:** pi-mono-docs vault + autoresearch-gate skill + Papers MCP
