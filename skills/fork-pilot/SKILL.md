---
name: fork-pilot
description: "Lightweight wrapper to use tmux_fork as orchestrator from OpenClaw. PicoClaw coordinates, fork agents execute."
license: MIT
metadata:
  author: Felipe Gonzalez & PicoClaw
  version: "2.1.0"
  openclaw:
    requires:
      bins: ["tmux-live", "fork"]
    emoji: "🦞"
when: "When orchestrating parallel agents, delegating work to fork, launching multi-agent exploration, or coordinating tmux_fork tasks from OpenClaw."
examples:
  - "usa fork para explorar el codebase en paralelo"
  - "lanza 3 agentes para investigar X"
  - "fork pilot research sobre Y"
  - "delega la implementación a fork agents"
---

# Fork Pilot — Orchestrator Mode

## Role Split

| Who | Does |
|-----|------|
| **PicoClaw (you)** | Plan, delegate, monitor, consolidate. **NEVER execute** implementation. |
| **fork agents** | Read, write, test, explore. They execute everything. |

## Skill Path (Full Orchestration Protocol)

```
~/.pi/agent/skills/tmux-fork-orchestrator/SKILL.md
```

For 10-phase protocol, load this file. For quick operations, use the references below.

## Resources (Progressive Disclosure)

| File | What | When |
|------|------|------|
| `resources/fork-cli-reference.md` | fork CLI commands (message, task, poll, adapter, template, doctor) | Need `fork` subcommands |
| `resources/tmux-live-reference.md` | tmux-live commands (25 total) | Need tmux-live operations |
| `resources/memory-cli-reference.md` | memory CLI commands (30+ total) | Need observation/session/workspace |
| `resources/mcp-tools-reference.md` | 21 MCP tools (17 memory + 4 messaging) | Need MCP integration |

## OpenClaw Execution Bridge

**You (PicoClaw) run outside tmux.** All tmux-live commands must go through `tmux send-keys`.
Never call `tmux-live` directly from `exec` — it detects `TMUX` env var and exits.

```bash
# Canonical pattern: send command, wait, capture output
SESSION="openclaw"
tmux send-keys -t $SESSION '<command>' Enter
sleep <N>
tmux capture-pane -t $SESSION -p -S -20
```

**Session name**: Always use `openclaw`. Create if missing:
```bash
tmux has-session -t openclaw 2>/dev/null || tmux new-session -d -s openclaw
```

**Note**: `tmux-live wait`, `tmux-live status`, `tmux-live response`, and `tmux-live kill-all` work from exec because they only read files/pipes — they don't need `TMUX` env.

## Orchestration Workflow

### Phase 0: Pre-flight
**MANDATORY before every orchestration.** Prevents pane accumulation and zombie panes.

```bash
SESSION="openclaw"
tmux has-session -t $SESSION 2>/dev/null || tmux new-session -d -s $SESSION
# Kill dead panes from previous runs
tmux list-panes -t $SESSION -F "#{pane_index} #{pane_dead}" | grep '1$' | awk '{print $1}' | \
  tac | while read idx; do tmux kill-pane -t "$SESSION:$idx" 2>/dev/null; done
# Clean stale files
rm -f /tmp/fork-live-done/*.done /tmp/fork-live-registry/fork-*.pane 2>/dev/null
```

### Phase 1: Plan
- Decompose task into subtasks
- Write prompt files to `/tmp/fork-prompt-*.txt` (see template below)
- Assign roles and models
- **Calculate timeouts** (see guidance below)

### Phase 2: Delegate (via send-keys)
```bash
SESSION="openclaw"
tmux send-keys -t $SESSION 'cd "${PROJECT_ROOT:-.}" && tmux-live init 2>&1' Enter
sleep 2
tmux send-keys -t $SESSION 'tmux-live launch <role> <name> @/tmp/fork-prompt-<name>.txt' Enter
sleep 5
# Verify agents are alive
tmux list-panes -t $SESSION -F "#{pane_index} alive=#{pane_dead} cmd=#{pane_current_command}"
```

### Phase 3: Monitor
```bash
tmux-live wait <name> <timeout> 2>&1
tmux-live status 2>&1
```

### Phase 4: Consolidate
```bash
tmux-live response <name> --full 2>&1
```

### Phase 5: Verify (optional)
```bash
tmux send-keys -t $SESSION 'tmux-live launch verifier verify-1 @/tmp/fork-prompt-verify.txt' Enter; sleep 5
tmux-live wait verify-1 180 2>&1
tmux-live response verify-1 --full 2>&1
```

### Phase 6: Cleanup
```bash
tmux-live kill-all 2>&1
tmux-live orphans 2>&1
tmux kill-session -t openclaw 2>/dev/null  # Optional
```

## Timeout Guidance

| Task Type | Min Timeout | Notes |
|-----------|-------------|-------|
| Read/explore only | 60-120s | Single file reads |
| Edit 1-2 files | 120-180s | Small surgical changes |
| Edit 3-5 files | 180-300s | Multiple coordinated edits |
| Full implementation | 300-600s | New code, tests, iterations |
| Analysis/report | 120-240s | Reading + synthesizing |

**Rule**: When in doubt, use 300s. `pi` with `glm-5-turbo` needs time for thinking + tool calls.

## Detecting Failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| `tmux-live: Not in tmux` | Called from exec directly | Use `tmux send-keys` bridge |
| Pane dead at 0s | Stale session / zombie panes | Phase 0 pre-flight or `kill-session` + recreate |
| Agent timeout | Still working, needs more time | Retry `wait` with higher timeout |
| No done file | Agent crashed (OOM, provider) | Check `/tmp/fork-live-sessions/` |
| Rate limit 429 | Provider throttled | Use free model for explorers |

## Prompt Template
See `resources/prompt-template.md` — structure: Role, Task, Context, Deliverable, Constraints.

## Role → Model Assignment

| Role | Model | Cost |
|------|-------|------|
| explorer (free) | `opencode/minimax-m2.5-free` | free |
| implementer (free) | `opencode/minimax-m2.5-free` | free |
| explorer (paid) | `zai/glm-5-turbo` | paid |
| implementer (paid) | `zai/glm-5-turbo` | paid |
| verifier | `zai/glm-5-turbo` | paid |
| architect | `zai/glm-5.1` | paid |
| analyst | `zai/glm-5-turbo` | paid |

**P11**: Paid only for 2+ concurrent agents.

## Task Lifecycle & Messaging
See `resources/fork-cli-reference.md` for `fork task`, `fork message`, and `fork poll` commands.

## Common Patterns

### Parallel Exploration
```bash
SESSION="openclaw"
# Phase 0: pre-flight (see above)
tmux send-keys -t $SESSION 'tmux-live launch explorer exp-1 @prompt1.txt' Enter; sleep 5
tmux send-keys -t $SESSION 'tmux-live launch explorer exp-2 @prompt2.txt' Enter; sleep 5
tmux-live wait exp-1 180 2>&1; tmux-live wait exp-2 180 2>&1
tmux-live response exp-1 --full 2>&1; tmux-live response exp-2 --full 2>&1
```

### Implement + Verify
```bash
tmux send-keys -t $SESSION 'tmux-live launch implementer dev-1 @prompt.txt' Enter; sleep 5
tmux-live wait dev-1 300 2>&1; tmux-live response dev-1 --full 2>&1
tmux send-keys -t $SESSION 'tmux-live launch verifier verify-1 @verify.txt' Enter; sleep 5
tmux-live wait verify-1 180 2>&1; tmux-live response verify-1 --full 2>&1
```

### Pipeline (Chain)
```bash
tmux send-keys -t $SESSION 'tmux-live chain /tmp/pipeline.yaml' Enter; sleep 5
tmux-live wait-all 300 2>&1
```

## Decision Tree

```
Need to orchestrate?
├─ Single task <30s → PicoClaw executes directly (no fork)
├─ 2-3 related tasks → Sequential delegation
├─ 3+ independent tasks → Full orchestration (preflight → init → launch → monitor → consolidate)
└─ Unknown codebase → 2 explorers first, then plan based on results
```

## Health & Recovery
```bash
fork doctor status && tmux-live kill-all 2>&1 && tmux-live orphans 2>&1
```