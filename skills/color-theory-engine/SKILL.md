---
name: color-theory-engine
description: Use when choosing color roles, generating color harmonies or tonal scales, querying Wada Sanzo palettes, or measuring WCAG contrast for interface colors.
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "2.0.0"
---

# Color Theory Engine

Use this skill to choose and measure interface color candidates. The CLI performs numeric color operations; the agent chooses semantic roles and evaluates interface context.

## Workflow

1. **Choose the intended role.** Decide whether a candidate is for a background, surface, brand fill, text, link, action, or status. Consult [`patterns/color-patterns.json`](patterns/color-patterns.json) as candidate-selection guidance; it does not generate semantic tokens or guarantee contrast. Read [Color Theory Foundations](reference/color-theory-foundations.md) for composition, color-space limits, and WCAG interpretation.
2. **Optionally consult a source palette.** When historical colors are useful, query [Wada Sanzo Palettes](reference/wada-sanzo-palettes.md) before generation or validation. Source colors do not assign interface roles or establish accessible pairs.
3. **Generate candidates.** Use `harmony` for color relationships or `scale` for tonal candidates. Existing harmony calls default to legacy HSL; use `--space oklch` for OKLCH rotations. `monochromatic` returns five steps from the canonical OKLCH scale.
4. **Measure final pairs.** Run `contrast` for every numeric foreground/background pair actually used. Select roles and decide criterion applicability separately; a numeric result cannot decide whether non-text contrast applies to an element or state.

## CLI

Run from the repository root and quote HEX arguments:

```bash
python3 skills/color-theory-engine/scripts/color_engine.py --help
python3 skills/color-theory-engine/scripts/color_engine.py harmony "#3B82F6" triadic --space oklch
python3 skills/color-theory-engine/scripts/color_engine.py harmony "#3B82F6" monochromatic
python3 skills/color-theory-engine/scripts/color_engine.py scale "#3B82F6"
python3 skills/color-theory-engine/scripts/color_engine.py contrast "#414141" "#FFFFFF"
python3 skills/color-theory-engine/scripts/color_engine.py wada --id 7 --dataset "$WADA_DATASET"
python3 skills/color-theory-engine/scripts/color_engine.py wada --name blue --dataset "$WADA_DATASET"
```

Supported signatures:

```text
contrast <foreground> <background>
harmony <base_hex> <complementary|analogous|triadic|monochromatic> [--space <hsl|oklch>]
scale <base_hex>
wada (--id <palette_id> | --name <color_name> [<additional_name_word> ...]) [--exact] --dataset <path>
```

HEX accepts three or six RGB digits with at most one leading `#`; alpha is unsupported. Contrast results include `ratio`, `passes_AA_normal`, `passes_AA_large`, `passes_AAA_normal`, and `passes_AAA_large`. The ratio is displayed to two decimals while all flags compare the unrounded ratio. Invalid library inputs raise `ValueError`; CLI errors are JSON on stderr, with stdout empty and exit status 1. `--help` exits successfully.

Wada data is not bundled and there is no implicit dataset path. Provide a compatible external dataset with `--dataset PATH`; the user is responsible for obtaining data they are entitled to use. Name matching is case-insensitive and returns exact matches first, followed by all substring matches in dataset order. `--exact` restricts matching to exact names. See [Wada Sanzo Palettes](reference/wada-sanzo-palettes.md) for the external input shape and query contract.

## Output limits

The scale has eleven keys from `50` through `950`, preserves the normalized seed exactly at `500`, and uses OKLCH for generated steps. Gamut mapping reduces chroma where needed; eight-bit quantization can collapse neighboring steps. OKLCH lightness is not WCAG relative luminance. Measure the final emitted HEX pairs instead of inferring contrast from color-space coordinates.

The engine does not recommend semantic roles automatically and does not expose LAB or Delta-E calculations. Wada historical LAB values, if present in an external dataset, are not used by the engine and have unspecified reference white/provenance. For WCAG thresholds, text sizing, contrast rounding, and non-text context, use [Color Theory Foundations](reference/color-theory-foundations.md).
