---
name: dots-maintenance
description: >
  Comprehensive guide and execution protocol for maintaining, diagnosing, updating, and rolling back the Gentleman.Dots-nix workstation ecosystem across Nix Flakes, Home Manager, Homebrew, Bun, uv, Rustup, PNPM, and Fisher.
  Trigger: When user asks to update packages, run system maintenance, check health, diagnose PATH precedence or shadowed binaries, fix broken symlinks, rollback home-manager generations, or use dots-update, dots-doctor, sysup, sysdoc.
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0"
---

## When to Use

- Updating workstation tools, runtimes, and dependencies across all package managers in a single pass.
- Running preflight health audits to detect `$PATH` precedence issues, shadowed binaries, or stale symlinks.
- Previewing updates safely via `--dry-run` or targeting specific subsystems (`--only=bun,uv`, `--skip=brew`).
- Diagnosing or resolving runtime upgrade errors (e.g. `bun upgrade`, `uv self update`, `rustup update`).
- Rolling back broken Home Manager generations, restoring `flake.lock`, or recovering standalone runtimes.
- Extending or modifying the update engine (`scripts/dots-update`) or diagnostic engine (`scripts/dots-doctor`).
- Diagnosing failed updates or hangs during `sysup` / `dots-update` (always co-invoke `nix-fish-homemanager` for Nix/Fish activation traps and Fisher bugs).

---

## The 4 Core Architectural Principles

1. **Strict Subsystem Isolation (Failure Resilient):**
   Updates are executed in sequential, isolated phases across 7 subsystems: **Homebrew**, **Nix Flakes**, **Bun**, **uv**, **Rustup**, **PNPM**, and **Fisher**. A transient network failure or error in one subsystem MUST NEVER abort or corrupt the others.

2. **Self-Updaters Live Outside `/nix/store`:**
   Runtimes managed via standalone self-update commands (`bun upgrade`, `uv self update`, `rustup update`) maintain their own binaries in user-writable directories (`~/.bun/bin`, `~/.local/bin`, `~/.cargo/bin`) to avoid `/nix/store` immutability permission errors (`EACCES`). Declarative packages declared in `flake.nix` are managed deterministically via Flake inputs.

3. **Preflight Health & Shadowing Gates (`sysdoc`):**
   Before running major updates or troubleshooting CLI behavior, run `dots-doctor` (`sysdoc`) to audit the 6 origin tiers (`Nix`, `Homebrew`, `Bun`, `Cargo`, `Local`, `System`) and verify that Nix profiles precede Homebrew in `$PATH`.

4. **Non-Blocking Shell Cadence (<10ms):**
   Interactive shell reminders inspect `~/.cache/dots-update/last_run.json` using local epoch math without network I/O. Reminders trigger only after 7 days elapsed without adding startup latency.

---

## Subsystem Matrix & Ownership

| Subsystem | Managed Scope | Update Command | Fallback / Rollback |
|---|---|---|---|
| **Nix Flakes** | Declarative CLI tools, shells, fonts | `nix flake update && home-manager switch` | Activate `/nix/store/<hash>-.../activate` |
| **Homebrew** | macOS casks, window managers (`nehir`), daemons | `brew update && brew upgrade` | `brew install <pkg>@<ver>` |
| **Bun** | JavaScript/TypeScript fast runtime | `bun upgrade` | Inspect official installer script before running |
| **uv** | Python toolchains & virtualenvs | `uv self update` | Inspect official installer script before running |
| **Rustup** | Rust toolchains & `cargo` | `rustup update` | `rustup default stable` |
| **PNPM** | Global Node CLI packages | `pnpm update -g` | `pnpm setup` |
| **Fisher** | Fish shell plugins & themes | `fisher update` | Reinstall via `fish.nix` declarative plugin |

> [!IMPORTANT]
> **Fisher Non-Interactive Invocation (BUG-001):**
> When invoking `fisher update` from background processes, CI, or subshells without a TTY, always close stdin (`fish -c "fisher update" </dev/null`). Unclosed pipes trigger Fisher's stdin ingestion loop (`isatty || read ...`) and cause indefinite execution hangs (see [BUG-001](../nix-fish-homemanager/references/troubleshooting-and-known-bugs.md#bug-001-fisher-stdin-hang-in-non-tty--headless-environments)).

---

## Daily Operations & Commands

### 1. Quick Ergonomic Aliases
```bash
# Health check & diagnostic sanity check
sysdoc

# Preview all update actions without making changes
sysup-dry

# Perform complete system update across all 7 layers
sysup

# Machine-readable health diagnostic in JSON
dots-doctor --json | jq .summary
```

### 2. Granular Updates & Filters
```bash
# Update only Bun and uv
dots-update --only=bun,uv

# Update everything except Homebrew
dots-update --skip=brew

# Update without pruning package manager caches
dots-update --no-cleanup

# Verbose debugging output
dots-update --verbose
```

### 3. Preflight Health Verification
```bash
# Inspect shadowed binaries
dots-doctor --json | jq .shadowed_binaries

# Inspect broken symlinks in ~/.config and dotfiles
dots-doctor --json | jq .broken_symlinks

# Inspect active Home Manager generation and path
dots-doctor --json | jq .home_manager
```

---

## Emergency Rollback Runbook

### Scenario A: Declarative Nix Configuration Error
```bash
# 1. List previous Home Manager generations
home-manager generations

# 2. Activate the last known healthy generation
/nix/store/<hash>-home-manager-generation/activate
```

### Scenario B: Incompatible Upstream Flake Input
```bash
# 1. Revert flake.lock to the recorded baseline commit (never blind HEAD~1)
cd ~/Developer/Gentleman.Dots-nix
# Identify baseline commit from git log:
git log -n 5 --oneline flake.lock
# Restore the exact known-good commit:
git checkout <recorded-good-commit> -- flake.lock

# 2. Re-switch Home Manager
home-manager switch --flake .#gentleman
```

### Scenario C: Corrupted Standalone Runtime (Bun / uv)
> [!WARNING]
> Security Risk: Never pipe untrusted remote shell scripts directly to `bash` or `sh` without inspecting the file contents or verifying cryptographic signatures. Download to a local file, inspect, and execute explicitly:

```bash
# Download and inspect before execution
curl -fsSL https://bun.sh/install -o /tmp/bun-install.sh
# Review /tmp/bun-install.sh before running:
bash /tmp/bun-install.sh

curl -LsSf https://astral.sh/uv/install.sh -o /tmp/uv-install.sh
# Review /tmp/uv-install.sh before running:
sh /tmp/uv-install.sh
```

### Scenario D: Broken Toolchain Package Manager (Rustup / PNPM)
```bash
# Restore Rust toolchains
rustup default stable

# Repair PNPM global directory configuration
pnpm setup
```

---

## Resources & Documentation

- **Full Maintenance Runbook**: See [references/runbook.md](references/runbook.md).
- **Nix & Fish Architecture & Bug Registry**: See `nix-fish-homemanager` skill (`../nix-fish-homemanager/SKILL.md`) for declarative patterns and its canonical bug registry ([references/troubleshooting-and-known-bugs.md](../nix-fish-homemanager/references/troubleshooting-and-known-bugs.md)) for known activation traps and Fisher/Nix hangs.
