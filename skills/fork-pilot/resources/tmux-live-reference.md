# tmux-live Reference

Binary: `~/bin/tmux-live` | Source: `~/.pi/agent/skills/tmux-fork-orchestrator/scripts/tmux-live`

## Pane Lifecycle

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize orchestration session | `tmux-live init` |
| `spawn <name> "cmd"` | Low-level spawn in named pane | `tmux-live spawn dev-1 "python main.py"` |
| `launch <role> <name> @prompt` | Spawn with role model + prompt file | `tmux-live launch explorer exp-1 @/tmp/prompt.txt` |
| `kill <name>` | Kill specific agent | `tmux-live kill exp-1` |
| `stop <name>` | Graceful stop | `tmux-live stop exp-1` |
| `kill-all` | Kill all agents | `tmux-live kill-all` |
| `orphans` | Reap orphan sessions | `tmux-live orphans` |

## Monitoring

| Command | Description |
|---------|-------------|
| `status` | Show all agents and their status |
| `progress <name> <timeout>` | Wait for agent to finish |
| `wait <name> <timeout>` | Alias for progress |
| `wait-all <timeout>` | Wait for all agents |
| `dashboard` | Live agent dashboard (status, tools, tokens) |
| `agents` | List active agents |
| `list` | List panes/agents |
| `events <name>` | Show agent event stream |
| `roles` | List available roles and their models |

## Communication

| Command | Description |
|---------|-------------|
| `send <name> "text"` | Send text to agent's pane |
| `capture <name>` | Capture agent output |
| `response <name> [--full]` | Read agent's .done file |
| `message send <name> "msg"` | Send via message system |
| `attach <name>` | Attach to agent's pane (interactive) |
| `back` | Return from attached pane |

## Pipelines

| Command | Description |
|---------|-------------|
| `chain <file>` | Execute sequential agent pipeline (YAML) |
| `workflow <name>` | Execute named workflow |

## Configuration

| Command | Description |
|---------|-------------|
| `layout` | Manage pane layout |
| `queue` | Task queue management |

## Role → Model Mapping

```
explorer (free)    opencode minimax-m2.5-free
implementer (free) opencode minimax-m2.5-free
explorer           zai glm-5-turbo
implementer        zai glm-5-turbo
verifier           zai glm-5-turbo
architect          zai glm-5.1
analyst            zai glm-5-turbo
```

## Architecture

`tmux-live` is a 73-line dispatcher sourcing 13 lib modules:

| Module | Fns | Purpose |
|--------|-----|---------|
| `core.sh` | 17 | Logging, registration, done helpers |
| `lifecycle.sh` | 7 | WS1 launch lifecycle integration |
| `pane.sh` | 9 | tmux target helpers, layout |
| `queue.sh` | 2 | Lock wrap, drain |
| `kill.sh` | 3 | Kill, stop, kill-all |
| `wait.sh` | 5 | Wait, progress, write-done |
| `spawn.sh` | 8 | Launch, spawn_with_meta, build_pi_cmd |
| `cli.sh` | 9 | CLI dispatch |
| `dashboard.sh` | 1 | Live dashboard |
| `chain.sh` | 2 | Chain, workflow |
| `orphans.sh` | 1+ | Orphan detection/reaping |
| `message.sh` | 1 | Inline messaging |
