---
name: nix-fish-homemanager
description: >
  Comprehensive guide, architectural standards, and workflow reference for managing Fish Shell, Nix Flakes, and Home Manager on macOS (Darwin).
  Trigger: When user asks to edit, configure, troubleshoot, refactor, or manage Fish Shell configs, Nix Flakes, Home Manager modules, macOS Keychain secrets, or environment variables in dotfiles.
license: MIT
search_hints: "nix flakes home manager fish shell macos keychain secrets dotfiles nixpkgs pin troubleshooting debug bugs hang"
metadata:
  author: Felipe Gonzalez
  version: "1.2"
  triggers:
    - "nix flake"
    - "home manager"
    - "fish config"
    - "keychain secret"
    - "dotfiles"
    - "nixpkgs channel"
    - "debug nix"
    - "troubleshoot fish"
    - "nix switch error"
    - "fisher hang"
---

## When to Use

- Adding, editing, or refactoring Nix expressions in `flake.nix`, `fish.nix`, or Home Manager modules.
- Writing Fish functions, aliases, completions, or `conf.d/` hooks on macOS.
- Managing environment variables, secrets, or API tokens without leaking them into `/nix/store`.
- Running dry-run validation builds (`home-manager build`) before applying changes (`home-manager switch`).
- Resolving `$PATH` precedence between Homebrew, Nix profiles, Cargo, Bun, and system binaries.
- Diagnosing, debugging, or troubleshooting failing Nix activations, Fish shell hangs, or update errors (consult [references/troubleshooting-and-known-bugs.md](references/troubleshooting-and-known-bugs.md)).
- Working inside `~/Developer/Gentleman.Dots-nix` or troubleshooting maintenance scripts (`sysup`, `sysdoc`, `dots-update`, `dots-doctor`): **ALWAYS pair and co-invoke with the `dots-maintenance` skill**.

---

## The 4 Golden Architectural Rules

1. **Zero Secrets in `/nix/store`:** Never place API keys, private tokens, or credentials in `.nix` files or `home.file` targets. Always use the dynamic macOS Keychain loader pattern in `fish/conf.d/*.fish`.
   *(See [references/secrets-and-keychain.md](references/secrets-and-keychain.md))*

2. **Prefer Native Modules over Raw Strings:** Use `programs.<name>` (e.g. `programs.starship`, `programs.fish`) instead of raw `home.file` string dumps or imperative shell scripts.
   *(See [references/home-manager-architecture.md](references/home-manager-architecture.md))*

3. **Strict Managed vs. Editable Boundary in Fish:** 
   * `~/.config/fish/config.fish` is **read-only / managed by Nix**.
   * `~/.config/fish/conf.d/*.fish` runs **before** `config.fish` (ideal for secrets and dynamic envs).
   * `~/.config/fish/functions/*.fish` is for **autoloaded modular functions**.
   *(See [references/fish-architecture-macos.md](references/fish-architecture-macos.md))*

4. **Never Switch Without Clean Build Validation:** Always run `home-manager build` to verify that Nix evaluates without errors and derivations are clean before proposing `home-manager switch`.
   *(See [references/verification-and-workflow.md](references/verification-and-workflow.md))*

---

## Troubleshooting & Known Bugs Gate

When debugging failures, unexpected hangs, or activation errors in Nix, Home Manager, or Fish:
**MANDATORY FIRST STEP:** Read [references/troubleshooting-and-known-bugs.md](references/troubleshooting-and-known-bugs.md) before building theories or formulating hypotheses. Check for documented failure modes:
1. **Fisher Stdin Hang (BUG-001):** `fisher update` hanging in non-interactive / headless execution due to unclosed stdin (`< /dev/null` required).
2. **Silent Nix Switch Failures & Auto-Rollback (BUG-002):** `dots-update` / `sysup` hiding stderr and reverting `flake.lock`.
3. **Existing File Collisions (BUG-003):** `checkLinkTargets` aborting on differing unmanaged files.
4. **Activation Script Traps (BUG-004):** Unguarded commands exiting non-zero under `set -euo pipefail`.

> [!IMPORTANT]
> **Cross-Skill Synergy (Dotfiles & System Updates):**
> If the problem touches `~/Developer/Gentleman.Dots-nix` or involves running workstation update commands (`sysup`, `sysdoc`, `dots-update`, `dots-doctor`), **ALWAYS co-invoke the `dots-maintenance` skill** from the very start.
> - `dots-maintenance`: Governs multi-subsystem orchestration (Homebrew, Nix, Bun, uv, Rustup, PNPM, Fisher), PATH precedence audits, and runtime rollback runbooks.
> - `nix-fish-homemanager`: Governs declarative Nix Flakes, Fish shell architecture, activation hooks, and dotfile symlink boundaries.

---

## Decision Gates

| Situation | Action |
| :--- | :--- |
| **Issue in `Gentleman.Dots-nix` or running `sysup`/`sysdoc`** | Load BOTH `nix-fish-homemanager` AND `dots-maintenance` skills together immediately. |
| **Diagnosing hangs or switch errors** | Read [references/troubleshooting-and-known-bugs.md](references/troubleshooting-and-known-bugs.md) first (check Fisher stdin hang, silent switch errors, checkLinkTargets, set -e). |
| **Tool has official Home Manager module** | Use `programs.<tool>` (e.g. `programs.starship`, `programs.git`). Do NOT use `home.file` or `home.packages` for it. |
| **Dotfile without Home Manager module** | Use `home.file.".config/<app>".source = ./path;` for immutable symlinking. |
| **Application requires writable directory** | Use `home.activation.<name>` with `chmod -R u+w` backup/copy pattern. |
| **Handling API Tokens / Secrets** | Store in macOS Keychain (`security add-generic-password`); load via `fish/conf.d/*-keychain.fish`. |
| **Adding a reusable Fish function** | Create `~/.config/fish/functions/<name>.fish` (1 function per file for lazy autoloading). |
| **Testing changes safely** | Run `home-manager build` (dry-run). NEVER run `home-manager switch` without explicit user sign-off. |

---

## Daily Operations & Commands

```bash
# ─── Fish Shell Gates ───
fish_indent -w path/to/script.fish && fish_indent --check path/to/script.fish
fish -n path/to/script.fish

# ─── Nix & Home Manager Evaluation (Dry-Run) ───
# repo path is machine-specific: replace ~/Developer/Gentleman.Dots-nix
# with your own dotfiles checkout (placeholder: ~/Developer/<dots-repo>)
cd ~/Developer/Gentleman.Dots-nix
nix flake check
home-manager build --flake .#gentleman-macos-arm

# ─── Store Leak Audit (3-way gate; canonical snippet in references/verification-and-workflow.md) ───
# grep exit 0 -> BLOCK (leak found) | exit 1 -> CLEAN | exit 2 / missing dir -> GATE ERROR
# Never implement this as `grep ... || echo CLEAN` (masks exit 2 errors).
rm -f result

# ─── Apply Changes (With User Authorization) ───
home-manager switch --flake .#gentleman-macos-arm
```

---

## Output Contract & Quality Gates

When completing any Nix/Fish work unit:
1. **Formatting Gate:** All `.fish` files must exit `0` on `fish_indent --check` and `fish -n`.
2. **Build Gate:** `home-manager build` must succeed with exit code `0`.
3. **Secret Gate:** Derivations in `result/` must contain 0 hardcoded tokens or credentials.
4. **Symlink Integrity:** Profile paths in `~/.local/state/nix/profiles/home-manager/` must point to valid store derivations.

---

## Progressive Disclosure & Deep References

- **Workstation Maintenance & Orchestration:** `dots-maintenance` skill (`~/.gemini/config/skills/dots-maintenance/SKILL.md`) — Multi-subsystem update orchestrator (`sysup`, `sysdoc`, `dots-update`, `dots-doctor`), preflight health audits, and recovery runbooks.
- **Troubleshooting & Known Bugs:** [references/troubleshooting-and-known-bugs.md](references/troubleshooting-and-known-bugs.md) — Canonical registry of edge-case bugs, silent hangs, and activation traps.
- **Nix Flakes Architecture:** [references/nix-and-flakes.md](references/nix-and-flakes.md) — Flake anatomy, inputs, derivations, and locking.
- **Home Manager System:** [references/home-manager-architecture.md](references/home-manager-architecture.md) — Modules, symlinks, profiles, and plugins.
- **Fish Shell Initialization:** [references/fish-architecture-macos.md](references/fish-architecture-macos.md) — Conf.d load order, `$PATH` precedence, and function autoloading.
- **Keychain Secret Management:** [references/secrets-and-keychain.md](references/secrets-and-keychain.md) — Keychain CLI patterns and zero-leak environment exports.
- **Verification Workflow:** [references/verification-and-workflow.md](references/verification-and-workflow.md) — 5-step checklist, dry-run gates, and generation rollbacks.

## Reusable Assets & Templates

- **Flake Skeleton:** [assets/flake-template.nix](assets/flake-template.nix)
- **Fish Home Manager Module:** [assets/fish-module-template.nix](assets/fish-module-template.nix)
- **Keychain Secret Loader:** [assets/keychain-loader-template.fish](assets/keychain-loader-template.fish)
