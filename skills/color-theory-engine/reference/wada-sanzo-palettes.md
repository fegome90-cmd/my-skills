# Wada Sanzo Palettes

Wada Sanzo combinations are an **optional external source-palette reference**. They provide historical context and candidate colors; they do not assign UI roles or establish accessible text/background pairs. Keep source values distinct from derived interface tokens.

## External data and use

No Wada dataset is included, fetched, or selected implicitly by this package. Supply a compatible JSON dataset explicitly with `--dataset PATH` for every query. The user must obtain data they are entitled to use; this package makes no claim about the dataset's license or provenance. Do not treat example fixture data in `tests/fixtures/` as historical Wada data.

The reader expects a non-empty JSON array. Each record has `name` (string), `hex` (three- or six-digit RGB HEX), `rgb` (three integer channels from 0 to 255), `swatch` (integer), and `combinations` (a non-empty list of positive integer palette IDs). Any additional dataset fields are ignored. Dataset order and original HEX spelling are preserved in query results.

Set a path you control, then pass it explicitly:

```bash
WADA_DATASET=/path/to/your/authorized-dataset.json
python3 skills/color-theory-engine/scripts/color_engine.py wada --id 7 --dataset "$WADA_DATASET"
python3 skills/color-theory-engine/scripts/color_engine.py wada --name "blue" --dataset "$WADA_DATASET"
python3 skills/color-theory-engine/scripts/color_engine.py wada --name "blue" --exact --dataset "$WADA_DATASET"
```

The path above is a placeholder, not a bundled file. Without a dataset, the command returns a clear JSON error on stderr, leaves stdout empty, and exits 1.

## Query behavior

- `wada --id N` returns the matching palette's ID, color count, and colors in dataset order; unknown IDs are errors.
- `wada --name WORDS...` performs case-insensitive matching. Exact names appear first, followed by all substring matches in dataset order.
- `--exact` restricts a name search to exact matches and is valid only with `--name`.
- A name result includes each match and its palette memberships; membership results preserve dataset order.
- Successful CLI output is JSON on stdout. Invalid or missing data is JSON on stderr with exit status 1.

A historical source palette remains a set of source colors, not a role assignment or accessibility verdict. For composition, color-space limits, and WCAG context, see [Color Theory Foundations](color-theory-foundations.md).
