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
The configuration usually resides in a `.nix` file (e.g., `starship.nix`) under the user's dotfiles repository, using the `home.file.".config/starship.toml".text` attribute.

### 2. Nix-Specific Escaping (CRITICAL)
When writing Starship's `${module}` variables inside a Nix multiline string (`''`), you MUST escape the `${` sequence using `''${`.
- **Incorrect:** `format = "${custom.gpu_usage}"` (Nix tries to evaluate it).
- **Correct:** `format = "''${custom.gpu_usage}"` (Nix renders it as `${custom.gpu_usage}`).

### 3. Apple Silicon Modules
Use these optimized `ioreg` commands for hardware monitoring without sudo:
- **GPU Usage:** `ioreg -n AppleDeviceManagementHIDEventService -r -l | grep -m 1 "DeviceUtilization" | awk '{print $NF}'`
- **RAM Usage:** Use Starship's native `$memory_usage` with `format = "$symbol[$percentage]($style) "`.

### 4. Deployment
After modifying the Nix file, apply changes using:
```bash
home-manager switch --flake .
```

## Best Practices
- **Palettes:** Use a `let...in` block in the Nix file to define colors, then reference them in the TOML string using `${palette.color}`.
- **Custom Modules:** Always add descriptive comments to `custom` modules to explain the data source.
- **Git Status:** Prefer descriptive labels over bare icons for better user learning curves (e.g., `! modified:N`).
