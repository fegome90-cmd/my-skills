---
name: starship-prompt
description: >
  Comprehensive guide and architecture reference for designing, customizing, and styling the Starship cross-shell prompt (via starship.toml or Home Manager programs.starship).
  Trigger: When user asks to customize, design, style, troubleshoot, or configure Starship prompt, terminal statusline, Powerline segments, palette colors, or Starship modules in Fish, Zsh, Bash, Nu, or Nix.
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0"
---

## When to Use

- Designing or modifying shell prompts in Fish, Zsh, Bash, Nushell, or PowerShell.
- Configuring Powerline / Chevron / Capsule styles with Nerd Font glyphs (``, ``, ``).
- Setting up custom themes, palettes (Catppuccin Mocha, Gruvbox, Tokyo Night, Gentleman), or directory substitutions.
- Migrating Starship configuration to Home Manager (`programs.starship.settings`).
- Debugging slow prompt performance, missing glyphs, or unrendered modules.

---

## Critical Patterns & Architecture

### 1. The Format Contract
Starship constructs prompts by interpolating active modules specified in `format` and `right_format`:

```toml
format = """
$directory\
$git_branch\
$git_status\
$fill\
$cmd_duration\
\n$character"""
```

* **Line breaks**: Use `\n` or `$line_break` to separate header lines from the active typing line.
* **Right alignment**: Use `$fill` in `format` or use `right_format` for native right-side status.
* **Conditionality**: Modules only render if their activation criteria are met (e.g. `$git_branch` only renders inside a git repository).

---

### 2. Powerline Segment Transition Math
To seamlessly connect two colored background segments without visual gaps or misaligned colors:

$$\text{Transition Glyph: } [\text{}](\text{fg:Background\_A bg:Background\_B})$$

```toml
# Example: Red OS segment transitioning to Peach Directory segment
[](red)$os$username[](bg:peach fg:red)$directory[](bg:yellow fg:peach)$git_branch
```

---

### 3. Declarative Home Manager Integration (Nix) & Ownership Preflight

Before proposing or applying any edit to `~/.config/starship.toml`, execute this mandatory ownership preflight:

```bash
# Preflight check: verify if config is owned by Nix / Home Manager
if [ -L ~/.config/starship.toml ]; then
  echo "BLOCK: ~/.config/starship.toml is a symlink -> $(readlink ~/.config/starship.toml)" >&2
  echo "Managed by Nix/Home Manager. Do NOT edit directly. Edit the source .nix module instead." >&2
  exit 1
fi
```

Never edit `~/.config/starship.toml` imperatively when managed by Nix. Declare the configuration inside `starship.nix`:

```nix
{ config, pkgs, lib, ... }:
{
  programs.starship = {
    enable = true;
    enableFishIntegration = true;
    enableZshIntegration = true;
    settings = {
      "$schema" = "https://starship.rs/config-schema.json";
      format = lib.concatStrings [
        "$directory"
        "$git_branch"
        "$fill"
        "$cmd_duration"
        "\n$character"
      ];
      palette = "catppuccin_mocha";
      # Module attrsets map 1:1 to TOML tables
      directory = {
        truncation_length = 3;
        truncate_to_repo = true;
      };
    };
  };
}
```

---

## Decision Gates

| Situation | Action |
| :--- | :--- |
| **Managing via Nix / Home Manager** | Run `test -L ~/.config/starship.toml` preflight. Write settings to `starship.nix` in `programs.starship.settings`; validate with `home-manager build`. |
| **Managing via standalone dotfiles** | Run `test -L ~/.config/starship.toml` preflight to confirm it is NOT a Nix symlink. Edit `~/.config/starship.toml` directly; validate with `starship print-config`. |
| **Maximalist context / High contrast** | Choose **Connected Powerline (``)** with colored background blocks. |
| **Minimalist / Low distraction** | Choose **2-Line Minimal** or **1-Line Inline** with transparent backgrounds and bold foreground colors. |
| **Terminal lacks Nerd Fonts** | Use `starship preset no-nerd-font` or standard Unicode symbols (`➜`, `λ`). |

---

## Layout Archetypes

| Archetype | Characteristics | Best For |
| :--- | :--- | :--- |
| **Connected Powerline (``)** | High-contrast colored blocks with sharp arrow transitions | Maximalist info dashboards, full context |
| **Floating Pills (` ... `)** | Individual rounded bubble tags per module with whitespace | Clean modern aesthetic |
| **2-Line Minimalist** | Context on top (directory, git, duration), clean cursor on line 2 | High productivity, zero screen clutter |
| **1-Line Inline** | Everything on a single line (`~/repo on main ❯ `) | Compact terminal windows and side panels |

---

## Commands & Diagnostics

```bash
# Preview and debug active modules in current directory
starship explain

# Inspect compiled TOML output
starship print-config

# Test a single module output directly
starship module directory
starship module git_branch

# Test official built-in presets
starship preset catppuccin-powerline
starship preset nerd-font-symbols
starship preset bracketed-segments

# Validate Home Manager build (if using Nix)
home-manager build --flake .#<profile>
```

---

## Output Contract & Verification

Before finalizing prompt changes:
1. Verify syntax and configuration compilation: `starship print-config > /dev/null`.
2. Inspect rendered modules: `starship explain`.
3. If using Nix, verify build passes: `home-manager build --flake .#<profile>`.

---

## Resources

- **Templates**: See [assets/](assets/) for `minimal.toml`, `powerline-catppuccin.toml`, and `nix-home-manager-module.nix`.
- **Module Reference**: See [references/modules-reference.md](references/modules-reference.md) for module keys and variables.
- **Glyphs & Presets**: See [references/presets-and-glyphs.md](references/presets-and-glyphs.md) for Powerline Unicode symbols and transitions.
