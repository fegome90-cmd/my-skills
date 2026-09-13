---
disable-model-invocation: true
name: starship-nix-manager
description: Use when managing Starship prompt configurations deployed via Nix/Home Manager. Handles Nix escaping, Apple Silicon modules, and deployment workflows. Do NOT use for standalone Starship configs or non-Nix environments.
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0"
---

# Starship Nix Manager

Manage Starship prompts within a Nix/Home Manager environment.

## Workflow

### 1. Locate Configuration
The configuration may reside in Home Manager via `programs.starship` (idiomatic module, where `settings` is structured attribute set) or via `home.file.".config/starship.toml".text` in `.nix` dotfiles. Prefer `programs.starship.settings` where possible; if raw TOML multiline text in Nix is used, escaping rules below apply.

### 2. Nix-Specific Escaping (CRITICAL for raw text)
When writing Starship's `${module}` variables inside a Nix multiline string (`''`), you MUST escape the `${` sequence using `''${`.
- **Incorrect:** `format = "${custom.gpu_usage}"` (Nix tries to evaluate it).
- **Correct:** `format = "''${custom.gpu_usage}"` (Nix renders it as `${custom.gpu_usage}`).

### 3. Apple Silicon Modules
Use these optimized `ioreg` commands for hardware monitoring without sudo:
- **GPU Usage:** `ioreg -n AppleDeviceManagementHIDEventService -r -l | grep -m 1 "DeviceUtilization" | awk '{print $NF}'`
- **RAM Usage:** Use Starship's native `$memory_usage` with `format = "$symbol[$percentage]($style) "`.

### 4. Deployment (Build First, Sign-off, then Switch)
Never run `switch` directly without build verification. Validate the Nix flake first:
```bash
# 1. Build and verify flake evaluation without activating
home-manager build --flake .

# 2. Inspect generated result symlink and diff if needed
# 3. Request user confirmation before activation

# 4. Activate only upon explicit user sign-off
home-manager switch --flake .
```

## Best Practices
- **Idiomatic Module:** Align with `nix-fish-homemanager`: prefer `programs.starship` module options over arbitrary file overrides.
- **Palettes:** Use a `let...in` block in the Nix file to define colors, then reference them in the configuration.
- **Custom Modules:** Always add descriptive comments to `custom` modules to explain the data source.
- **Git Status:** Prefer descriptive labels over bare icons for better user learning curves (e.g., `! modified:N`).
