# tmux Plan Auditor v2

Multi-agent orchestrator for technical auditing of implementation plans. Uses parallel background processes for fast execution, domain-aware rule filtering, and JSON v2 handoff.

---

## Features

- **Fast Mode (default)**: 4 agents run as parallel background processes (~1.3s per run)
- **Interactive Mode** (`--interactive`): Agents run in tmux windows for live debugging
- **Domain Detection**: Automatically classifies plans as `tui-rich`, `web-api`, `cli`, or `generic` and filters rules accordingly
- **Rule Caching**: Rules are cached at module level to avoid redundant file reads
- **Confidence Scoring**: Each finding includes a confidence score (0.0-1.0); low-confidence findings (<0.3) are filtered out
- **Workflow Layers**: Specialized rule sets per workflow (`feature`, `bugfix`, `refactor`, `security`)
- **Package Manager Detection**: Auto-detects bun, yarn, or pnpm from lock files
- **Payload Validation**: Agent outputs are validated before handoff construction
- **Test Suite**: 21 unit tests covering domain detection, rule loading, handoff validation, and static command detection

---

## Architecture

```text
tmux-plan-auditor/
├── scripts/
│   ├── run_tmux_plan_audit.sh      # Orchestrator (entry point)
│   └── detect_domain.py            # Standalone domain detection
├── resources/
│   ├── agents/                     # Agent implementations (Python)
│   │   ├── base_agent.py           # Core: domain detection, rule engine, CLI
│   │   ├── logic_agent.py          # Ambiguity and scope issues
│   │   ├── code_quality_agent.py   # Refactor risks and code smells
│   │   ├── silent_failure_agent.py # Observability and error handling
│   │   └── testing_static_agent.py # Quality gates and static checks
│   ├── rules/                      # Detection rules (YAML)
│   │   ├── default.yaml            # Base rules (per-agent namespaces)
│   │   ├── bugfix.yaml             # Regression-focused rules
│   │   ├── refactor.yaml           # Simplicity-focused rules
│   │   └── security.yaml           # Hardening-focused rules
│   └── handoff_builder.py          # Result aggregation v2
└── tests/
    ├── conftest.py                 # Shared fixtures
    ├── test_detect_domain.py       # Domain detection tests
    ├── test_loader.py              # Rule loading and caching tests
    ├── test_handoff_builder.py     # Payload validation tests
    └── test_static_commands.py     # Stack detection tests
```

---

## Prerequisites

- **Python 3.10+**
- **Bash 5.x**
- **tmux** (optional — only required for `--interactive` mode)

---

## Usage

### Fast mode (default)

```bash
bash scripts/run_tmux_plan_audit.sh path/to/plan.md
```

Completes in ~1.3s. No tmux required.

### Interactive mode (debugging)

```bash
bash scripts/run_tmux_plan_audit.sh path/to/plan.md --interactive
```

Agents run in tmux windows. Attach with `tmux attach -t plan-audit-<run-id>`.

### Workflow-specific audit

```bash
bash scripts/run_tmux_plan_audit.sh path/to/plan.md -w security
bash scripts/run_tmux_plan_audit.sh path/to/plan.md -w refactor
```

### Configuration

```bash
export AUDITOR_AGENT_TIMEOUT=600   # Agent timeout in seconds (default: 300)
export AUDITOR_AUTO_CLEANUP=true   # Auto-cleanup in interactive mode (default: true)
export AUDITOR_INTERACTIVE=true    # Force interactive mode (alternative to --interactive)
export AUDITOR_PROJECT_ROOT=/path  # Project root for rule overrides and static checks
export AUDITOR_PLAN_DOMAIN=cli     # Force domain (tui-rich|web-api|cli|generic)
export AUDITOR_WORKFLOW=bugfix     # Force workflow (feature|bugfix|refactor|security)
```

---

## Domain Detection

The auditor automatically classifies plan content into one of four domains:

| Domain | Keywords | Example |
|--------|----------|---------|
| `tui-rich` | Rich, Textual, Textualize | Terminal UI plans |
| `web-api` | FastAPI, Flask, Express.js, endpoint | API/HTTP plans |
| `cli` | CLI, terminal, Typer, Click | Command-line tool plans |
| `generic` | (no keywords matched) | Any other plan |

Domain filtering prevents irrelevant findings (e.g., HTTP recommendations for CLI plans). Override with `AUDITOR_PLAN_DOMAIN` or `--interactive` for full rule evaluation.

---

## Rule Customization

Create `.pi/auditor-rules.yaml` in your project root to override default rules. Merge order:

1. `default.yaml` (skill defaults)
2. `workflow.yaml` (workflow-specific rules)
3. `.pi/auditor-rules.yaml` (project overrides)

Rules support an `applies_to` field for domain scoping:

```yaml
silent_failure:
  rules:
    - pattern: "\\bstatus\\b|\\berror\\b"
      severity: Media
      title: "Observability needed"
      risk: "late incident detection"
      recommendation: "Add error checklist and structured logs."
      applies_to: ["web-api"]
```

---

## Output (handoff.json v2)

```json
{
  "schema_version": "2.0",
  "plan_domain": "tui-rich",
  "execution_summary": {
    "total_duration_ms": 1337,
    "overall_confidence": 0.98,
    "agents_completed": 4,
    "agents_failed": 0
  },
  "findings": [...],
  "deduplicated_patch_candidates": [...]
}
```

---

## Testing

```bash
cd skills/tmux-plan-auditor
python3 -m pytest tests/ -v
```

21 tests covering domain detection, rule loading/caching, payload validation, and stack detection.

---

## License

MIT
