# Troubleshooting & Known Bugs Registry

Canonical registry of edge-case bugs, silent hangs, activation pitfalls, and failure modes across Nix Flakes, Home Manager, Fish Shell, and orchestration tools (`dots-update` / `sysup`).

**When debugging failures or hangs in this ecosystem, agents MUST consult this registry first before formulating new hypotheses.**

> [!IMPORTANT]
> **Co-Invocation with `dots-maintenance`:**
> If the error or hang occurred while executing `sysup`, `sysdoc`, `dots-update`, `dots-doctor`, or modifying scripts inside `~/Developer/Gentleman.Dots-nix`, you MUST activate the `dots-maintenance` skill (`skills/dots-maintenance/SKILL.md`) alongside this one. `dots-maintenance` owns multi-subsystem orchestration and runtime rollback runbooks, while this skill owns Nix/Fish activation and internal mechanics.

---

## Bug Index

| ID | Component | Symptom | Leading Cause |
|---|---|---|---|
| [BUG-001](#bug-001-fisher-stdin-hang-in-non-tty--headless-environments) | Fisher / Fish | Process hangs indefinitely on `fisher update` | Non-interactive `read` waiting for `EOF` on stdin |
| [BUG-002](#bug-002-silent-nix-switch-failures--destructive-flakelock-rollback) | `dots-update` / Nix | `✖ Nix update returned non-zero code (1)` without details | Redirection to `/dev/null` hides stderr; triggers auto-rollback |
| [BUG-003](#bug-003-existing-file-collision-in-checklinktargets) | Home Manager | `Existing file '...' is in the way of '...'` | Unmanaged file differs from Nix store derivation |
| [BUG-004](#bug-004-activation-hook-abort-under-set--euo-pipefail) | Home Manager Activation | Switch fails midway through custom activation hooks | Unguarded non-zero exit in `home.activation.<name>` |

---

### BUG-001: Fisher Stdin Hang in Non-TTY / Headless Environments

#### Symptom
During `sysup`, automated CI runs, subagent task execution, or background jobs, the update process hangs indefinitely at:
```text
==> Updating Fisher Fish shell plugins...
```
The process consumes 0% CPU and never times out.

#### Stack Trace Signature
Sampling the hanging `fish` process (`sample <PID> 1`) reveals the thread blocked in a system `read`:
```text
fish4exec19exec_process_in_job
  fish8builtins4read4read
    fish_common12read_blocked
      read (in libsystem_kernel.dylib)
```

#### Root Cause
In `~/.config/fish/functions/fisher.fish` (or `fish/functions/fisher.fish` in dotfiles):
```fish
isatty || read --local --null --array stdin && set --append argv $stdin
```
Fisher is designed to accept plugin lists over stdin when piped (e.g. `cat list | fisher install`). If stdin is connected to an open pipe rather than a real TTY (`! isatty`) and nothing writes to that pipe, `read` blocks waiting for `EOF`. In background jobs, subagents, or automated scripts, this causes a permanent deadlock.

#### Remediation & Golden Pattern
Always redirect stdin from `/dev/null` when invoking `fisher` from bash scripts or non-interactive runners:
```bash
# Correct: stdin is immediately closed
fish -c "fisher update" </dev/null

# Inside dots-update:
fish -c "fisher update" </dev/null >/dev/null 2>&1
```

---

### BUG-002: Silent Nix Switch Failures & Destructive `flake.lock` Rollback

#### Symptom
Running `dots-update` or `sysup` outputs:
```text
ℹ  Updating flake inputs in /Users/.../Developer/Gentleman.Dots-nix...
ℹ  Switching Home Manager generation (#gentleman)...
✖  Nix update returned non-zero code (1).
```
No error trace is printed, and inspecting `git diff flake.lock` shows that `flake.lock` was restored to its pre-update revision.

#### Root Cause
In `scripts/dots-update`:
```bash
home-manager switch --flake ".#$FLAKE_TARGET" >/dev/null 2>&1 || nix_err=$?
```
When running without `--verbose`, `dots-update` silences all stdout and stderr. If `home-manager switch` encounters any failure during evaluation, build, or activation:
1. The error details are discarded into `/dev/null`.
2. `nix_err` is set to `1`.
3. The error handler restores `flake.lock.bak` over `flake.lock`, wiping out the newly updated inputs.

#### Remediation & Diagnostic Protocol
Never diagnose Nix failures with bare `dots-update` or `sysup`. Run with explicit verbose logging or execute Home Manager directly:
```bash
# Step 1: Run isolated with full diagnostics
dots-update --only=nix --verbose

# Step 2: Or isolate Home Manager directly
cd ~/Developer/Gentleman.Dots-nix
home-manager switch --flake .#gentleman
```
Inspect the uncensored stderr output to pinpoint the exact failing derivation, missing package, or broken activation hook.

---

### BUG-003: Existing File Collision in `checkLinkTargets`

#### Symptom
`home-manager switch` aborts early with:
```text
Activating checkLinkTargets
Existing file '/Users/<user>/.config/<app>/<file>' is in the way of '/nix/store/...-home-manager-files/...'
```

#### Root Cause
Home Manager manages dotfiles via declarative symlinks pointing to `/nix/store/...`. During the `checkLinkTargets` activation phase:
- If the destination already contains a file whose content is **identical** to the derivation, Home Manager skips it safely (`will be skipped since they are the same`).
- If the file exists and its content **differs** (or is an unmanaged regular file), Home Manager halts execution immediately (`set -e`) to prevent silent data loss.

#### Remediation & Golden Pattern
1. Inspect the differing file against the repo source:
   ```bash
   diff -u ~/.config/<app>/<file> ~/Developer/Gentleman.Dots-nix/<app>/<file>
   ```
2. Move or back up the colliding file:
   ```bash
   mv ~/.config/<app>/<file> ~/.config/<app>/<file>.bak
   ```
3. Re-run `home-manager switch --flake .#gentleman`.

---

### BUG-004: Activation Hook Abort under `set -euo pipefail`

#### Symptom
Home Manager switch succeeds in building derivations, but aborts during activation:
```text
Starting Home Manager activation
...
Activating install<Feature>
# Script exits with code 1
```

#### Root Cause
Home Manager activation scripts generate a monolithic `/nix/store/...-home-manager-generation/activate` script prefixed with:
```bash
set -eu
set -o pipefail
```
Any command in a custom activation hook (`home.activation.<name> = lib.hm.dag.entryAfter [...] '' ... ''`) that returns a non-zero exit code will cause the **entire** activation script to abort immediately. Common pitfalls include:
- `gh extension install` when GitHub auth is expired or rate-limited.
- `grep` returning `1` (no match) inside a pipe with `pipefail` enabled.
- External package installers (`brew install`) when a formula is already tapped or locked.

#### Remediation & Golden Pattern
All side-effecting or external commands in `home.activation` MUST be defensive and explicitly handled:
```nix
# BAD: aborts activation if extension already exists or network drops
gh extension install github/gh-copilot

# GOOD: guarded check or non-zero tolerance
if ! gh extension list 2>/dev/null | grep -q "github/gh-copilot"; then
  gh extension install github/gh-copilot || echo "Warning: copilot extension install skipped"
fi
```
