# Pi CLI Quick Reference

Cheat sheet for invoking pi-coding-agent from OpenClaw.

## Core Commands

```bash
# One-shot print (most common from OpenClaw)
pi -p --no-session --provider zai --model glm-5-turbo "task"

# Interactive session (NOT from OpenClaw)
pi

# Continue previous session
pi --continue
pi --continue --fork <id>

# List sessions
pi --list

# RPC mode (programmatic)
pi --mode rpc --no-session --provider zai --model glm-5-turbo
```

## Key Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `-p` / `--print` | Non-interactive, print output | `pi -p "task"` |
| `--no-session` | Don't persist session | `pi -p --no-session "task"` |
| `--provider` | LLM provider | `--provider zai` |
| `--model` | Model name | `--model glm-5-turbo` |
| `--skill` | Load skill by path | `--skill ~/.pi/agent/skills/autoresearch-gate` |
| `--extension` | Load extension by path | `--extension ~/.pi/agent/extensions/...` |
| `--mode` | Execution mode | `--mode rpc` |
| `--continue` | Resume session | `--continue` |
| `--fork` | Fork from session | `--fork abc123` |
| `--cwd` | Working directory | `--cwd ~/Developer/project` |

## Providers & Models

| Provider | Model | Env Var | Speed | Quality |
|----------|-------|---------|-------|---------|
| zai | glm-5-turbo | `ZAI_API_KEY` | Fast | Good |
| zai | glm-5-pro | `ZAI_API_KEY` | Medium | High |
| openai | gpt-4o | `OPENAI_API_KEY` | Medium | High |
| anthropic | claude-sonnet | `ANTHROPIC_API_KEY` | Medium | High |
| google | gemini-2.5-pro | `GOOGLE_API_KEY` | Medium | High |

## Pi's Built-in Tools

Pi agents have their own tool set (NOT shared with OpenClaw):

| Tool | What it does |
|------|-------------|
| `read` | Read files |
| `bash` | Run shell commands |
| `edit` | Edit files |
| `write` | Write files |
| `search` | Search codebase |
| `browser` | Browse the web |

## Output Modes

| Mode | Flag | Use case |
|------|------|----------|
| Print | `-p` | Get final answer, no interaction |
| RPC | `--mode rpc` | Structured JSON stdin/stdout |
| Interactive | (default) | Full TUI with shortcuts |

## From OpenClaw: Best Practices

### Quick one-shot task
```bash
pi -p --no-session --provider zai --model glm-5-turbo "explain this function"
```

### Experiment with autoresearch
```bash
pi -p --no-session --provider zai --model glm-5-turbo \
  --skill ~/.pi/agent/skills/autoresearch-gate \
  "run baseline: measure X"
```

### Long-running experiment
```bash
exec(background=true):
  pi -p --no-session --provider zai --model glm-5-turbo \
    --skill ~/.pi/agent/skills/autoresearch-create \
    "optimize Y" > /tmp/pi-exp.log 2>&1
```

### Programmatic integration
```bash
echo '{"prompt": "...", "tools": ["read", "bash"]}' | \
  pi --mode rpc --no-session --provider zai --model glm-5-turbo
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `ZAI_API_KEY not set` | Missing env var | Set in shell or pass via `--env` |
| `model not found` | Wrong model name | Check with `pi --models` |
| `skill not found` | Wrong path | Use absolute path to SKILL.md |
| Timeout | Long task | Use `exec(timeout=N)` from OpenClaw |

---

**Version:** 1.0.0 | **Updated:** 2026-06-02
