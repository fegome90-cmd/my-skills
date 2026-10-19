# Color Theory Foundations

This reference is the sole authority for the 60-30-10 composition heuristic used by this skill.

## Separate source, role, and accessible pair

A source palette supplies candidate colors. A semantic role—such as background, surface, brand fill, text, link, or action—is a design choice made for the interface's purpose. An accessible pair is a particular foreground and background, assessed against the applicable criterion and visual context. A source palette does not assign semantic roles, and a role or attractive harmony does not establish that a text/background pair is accessible.

## 60-30-10 composition heuristic

Use **60% neutral dominant background, 30% secondary surfaces and structure (including headers where appropriate), and 10% accents/actions** as a heuristic for visual weight. It is not a required pixel count, an algorithm, or a validation rule. Adapt it to the interface and its content. Source and brand colors remain source colors until a designer assigns them a role; name derived UI tokens separately.

## Color spaces and their limits

### sRGB and HSL

sRGB is the display encoding used by the engine's HEX inputs and outputs. HSL is a convenient cylindrical representation of sRGB. Legacy HSL harmony rotates hue while retaining HSL lightness and saturation; those coordinates do not preserve perceptual brightness. Use HSL for compatibility and prefer opt-in OKLCH rotations for new harmony work.

### OKLCH

OKLCH is a cylindrical form of OKLab. Its `L` coordinate is perceptual lightness, not WCAG relative luminance `Y`; changing OKLCH lightness does not establish a contrast result. The engine reduces chroma to map out-of-sRGB colors, then quantizes channels to eight-bit HEX. Mapping and quantization can make neighboring steps converge. The requested seed is preserved exactly at scale step `500`; see the implementation for the frozen curve and numeric constants.

Treat generated scales and harmonies as candidates. Measure final rendered foreground/background HEX pairs with `contrast` and assess their semantic and contextual use separately.

### CIELAB data

An external Wada dataset may contain historical LAB values whose reference white and calculation provenance are unspecified. The engine does not use those fields. It exposes no LAB or Delta-E operation.

## WCAG contrast checks

Measure every actual numeric pair with the engine:

```bash
python3 skills/color-theory-engine/scripts/color_engine.py contrast "#3B82F6" "#FFFFFF"
```

The ratio is displayed rounded to two decimal places; threshold flags use the unrounded ratio. Keep the display distinct from the underlying comparison.

- WCAG AA normal text: at least 4.5:1.
- WCAG AA large text: at least 3:1. Large means at least 18 pt regular, or at least 14 pt bold.
- WCAG AAA normal text: at least 7:1.
- WCAG AAA large text: at least 4.5:1.

For WCAG 1.4.11 non-text contrast, 3:1 applies only to visual information required to identify active controls or their states and meaningful parts of icons or graphics needed to understand content, measured against adjacent colors. Decorative content and inactive controls have exceptions. Applicability is a contextual judgment; a numeric ratio or large-text flag alone does not establish non-text conformance. Record the element, state, adjacent color, and criterion when interpreting a measurement.

Color alone does not replace a text label, icon, or other needed identification. Validate each actual pair after its role and context are chosen.
