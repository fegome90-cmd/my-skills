# fork CLI Reference

## fork run

Run a command in a forked terminal.
```bash
fork run "command"
fork run "pytest tests/ > /tmp/results.log 2>&1"
```

## fork message — Inter-Agent Messaging

| Command | Description | Example |
|---------|-------------|---------|
| `send` | Point-to-point message | `fork message send dev:1 "Fix auth bug"` |
| `broadcast` | Send to ALL agents | `fork message broadcast "Deploy in 5 min"` |
| `receive` | Poll inbox (supports watch mode) | `fork message receive dev:1 --watch --json` |
| `history` | Full message log | `fork message history dev:1 --limit 50` |
| `cleanup` | Purge expired messages | `fork message cleanup --max-age 300` |
| `send-to-pane` | Bridge SQLite msg → tmux pane | `fork message send-to-pane %5 "Hello"` |

**Message types**: COMMAND, REPLY, HANDOFF, PROGRESS, FILE_TOUCHED, OBSERVATION

## fork task — Task Management

| Command | Transition | Description |
|---------|-----------|-------------|
| `create` | → PENDING | Create new task |
| `submit-plan` | PENDING → PLANNING | Submit plan for review |
| `approve` | PLANNING → APPROVED | Approve plan |
| `reject` | PLANNING → PENDING | Reject plan (back to pending) |
| `start` | APPROVED → IN_PROGRESS | Begin execution |
| `complete` | IN_PROGRESS → COMPLETED | Mark done |
| `update` | — | Update task fields |
| `delete` | any → DELETED | Soft-delete |
| `assign` | — | Assign to agent via inbox |
| `list` | — | List all tasks |

## fork poll — Autonomous Polling

| Command | Description |
|---------|-------------|
| `start` | Start polling loop (Ctrl+C to stop) |
| `status` | Show active/recent poll runs |
| `cancel <run-id>` | Cancel active poll |
| `list-tasks` | APPROVED tasks awaiting execution |

## fork adapter — Terminal Multiplexer Abstraction

| Command | Description |
|---------|-------------|
| `detect` | Auto-detect active multiplexer |
| `spawn "cmd"` | Spawn command in new pane |
| `kill <pane-id>` | Kill pane by ID |
| `alive <pane-id>` | Check if pane is alive |
| `title <pane-id> "name"` | Set pane title |

## fork template — Agent Template Management

| Command | Description |
|---------|-------------|
| `list` | List all templates |
| `show <name>` | Show template details |
| `save --name <n> --model <m>` | Create/update template |
| `delete <name>` | Delete template |
| `toggle <name>` | Enable/disable |
| `discover --project .` | Scan for .md agent definitions |
| `resolve-role <role>` | Resolve role config → JSON |
| `team create <name>` | Create agent team |
| `team list` | List teams |
| `team delete <name>` | Delete team |

## fork doctor — Diagnostics

| Command | Description |
|---------|-------------|
| `status` | Full health check |
| `reconcile` | Fix orphan sessions |
| `cleanup-orphans` | Remove orphan data |
