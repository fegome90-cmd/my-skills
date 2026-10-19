# Changelog

## 2.0.0

- **Breaking API error contract:** invalid library inputs now raise `ValueError` instead of returning error dictionaries or strings; the CLI writes a JSON error to stderr, leaves stdout empty, and exits 1. Help remains a successful exit.
- Added the portable CLI commands `scale` and `wada`, OKLCH harmonies, and five-step monochromatic harmony while preserving legacy HSL harmony output.
- Added the eleven-step OKLCH scale with the input color anchored exactly at `500`.
- Kept the public `ContrastResult` export and the existing five-field contrast result, including `passes_AAA_large`; threshold flags continue to use the unrounded ratio.
- Wada data is no longer implicitly located or bundled. Queries require an explicit external dataset path, and this package makes no dataset-license claim.
- Added self-contained tests with fictional synthetic Wada records; no canonical Wada catalog or workspace output is included.
