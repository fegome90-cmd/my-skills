---
name: learned-ssh-agent-vm-bootstrap
description: "Trigger: diagnose a local agent's SSH-to-Linux-VM bootstrap, exact-consumer auth, tunnel health, or protocol/UI reachability before mutation."
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.2.0"
---

## Activation Contract

Load for a desktop or CLI agent that must reach or control an agent runtime on a Linux VM through SSH: wrong user/key, BatchMode failure, non-interactive executable discovery, tunnel/backend health, or protocol/UI reachability. Do not use for generic SSH administration, cloud provisioning/deployment, or standalone WebSocket debugging.

## Hard Rules

- Prove five layers independently: SSH configuration resolution; public-key authentication; remote executable discovery; tunnel/backend health; application protocol and UI state.
- Perform read-only diagnosis before mutation. Mutate only with explicit authorization, a permissions-preserving snapshot, and rollback; change one layer at a time and compare pre/post state.
- Never print environment values, secrets, passwords, tokens, or private-key material. Use `id -un`; discover named executables only with `command -v` and preserve failure status. Quote variables/arrays; never use `eval`, unquoted construction, or a PATH dump.
- Require an independently verified host fingerprint matching `known_hosts` and `StrictHostKeyChecking=yes`. Stop when credentials, passphrase, 2FA, or required interaction is unavailable; never weaken `BatchMode` or host-key checks.

## Decision Gates

| Gate | Continue only when |
| --- | --- |
| Inventory | Actual consumer SSH executable, arguments/config, target, user, `known_hosts`, key paths, and endpoint are known; missing config/key is explicit blocked evidence. |
| Trust/auth | Fingerprint matches; agent accessibility, every effective `IdentityFile`, exact-consumer status, and fresh-auth status are recorded. |
| Transport | Listener ownership and SSH forward target are expected. |
| Protocol | Discovered protocol completes a minimal authenticated exchange and the UI identifies the expected backend. |
| Mutation | Authorization, snapshot, and rollback are present. |

## Execution Steps

1. Before acting, determine the applicable domains and apply the mandatory reference routing below. For cross-domain diagnosis, read **both** references before acting.
2. Follow the read references in order; keep missing evidence or unavailable interaction blocked, use the gates, and never substitute partial-layer success.
3. Use the consumer's local connection configuration/registry and exact SSH argument vector, the selected local `~/.ssh/config` and `~/.ssh/known_hosts` (or the paths actually used), and relevant local application protocol/health documentation only when present and relevant.
4. After authorized changes, rerun every applicable layer and return the output contract.

## Output Contract

Return a per-layer table with columns `layer`, `applicable`, `check`, `exit/status`, `observed evidence`, and `blocked reason`; use one row per layer. Then report `changes`, `rollback`, and `remaining uncertainty`. Mark unavailable interaction or missing evidence as blocked, never successful.

## Resources

- `references/ssh-authentication.md` — **mandatory** before SSH configuration, key, fingerprint, path/stat, or fresh-auth work.
- `references/runtime-transport.md` — **mandatory** before executable discovery, listener/tunnel, HTTP/WebSocket/authenticated protocol, UI/backend identity, or authorized mutation/snapshot/rollback work.
- For cross-domain diagnosis, read **both** references before acting.
