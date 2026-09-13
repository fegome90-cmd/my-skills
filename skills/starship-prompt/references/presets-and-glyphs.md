# Powerline Glyphs & Preset Patterns

## 1. Essential Powerline / Nerd Font Glyphs

| Glyph | Unicode | Description | Visual Role |
| :--- | :--- | :--- | :--- |
| `` | `\uE0B6` | Left Rounded Semi-circle | Opening capsule cap |
| `` | `\uE0B4` | Right Rounded Semi-circle | Closing capsule cap |
| `` | `\uE0B0` | Right Solid Arrow / Chevron | Standard segment connector |
| `` | `\uE0B2` | Left Solid Arrow / Chevron | Right-prompt segment connector |
| `` | `\uE0B1` | Right Thin Chevron | Inner-block sub-separator |
| `` | `\uE0B3` | Left Thin Chevron | Inner-block right sub-separator |
| `󰀵` | `\uF0035` | Apple MacOS Logo | OS indicator |
| `` | `\uF07C` | Folder Icon | Directory indicator |
| `` | `\uF418` | Git Branch Icon | Git branch |
| `` | `\uF43A` | Clock Icon | System time |
| `` | `\uEAF4` | Timer / Stopwatch | Command execution duration |
| `❯` | `\u276F` | Modern Powerline Prompt | Character input symbol |

---

## 2. Powerline Transition Formula

To connect Segment A (Background = `$bg_A`) to Segment B (Background = `$bg_B`):

```text
[Segment A Content](bg:$bg_A fg:$fg_A)[](fg:$bg_A bg:$bg_B)[Segment B Content](bg:$bg_B fg:$fg_B)
```

* **Opening Cap:** `[](fg:$bg_1 bg:none)`
* **Closing Cap:** `[](fg:$bg_last bg:none)` or `[](fg:$bg_last bg:none)`

---

## 3. Official Starship Presets Reference

Starship includes built-in presets that can be applied with `starship preset <name>`:
- `catppuccin-powerline`: Connected Powerline rainbow using Catppuccin Mocha/Frappe/Latte.
- `gruvbox-rainbow`: Gruvbox warm retro powerline blocks.
- `nerd-font-symbols`: Maximalist icons for all toolchains and systems.
- `no-nerd-font`: Pure ASCII / standard Unicode prompt without special font requirements.
- `bracketed-segments`: Clean bracketed `[path] [branch] [node]` minimalist style.
- `plain-text`: Pure text prompt with minimal footprint.
- `pastel-powerline`: Soft pastel gradient powerline capsules.
- `tokyo-night`: Tokyo night color scheme integration.
