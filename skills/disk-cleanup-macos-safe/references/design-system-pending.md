# Design System — Redesign PENDING (implement when v4 is stable)

**Status:** Deferred. The v4 script ships with the original flat CSS. This document
captures the **"Diagnostic Console"** redesign (design-principles + color-theory-engine,
WCAG AA-validated) so it can be reapplied once v4 reaches a stable release.

**Created:** 2026-07-16 (applied briefly to v3 script, then deferred for v4)

---

## Design direction

**"Diagnostic Console"** — *Utility & Function + Precision & Density*.
References: GitHub, Linear, Raycast, macOS Activity Monitor.
Context: read-only storage report for a developer diagnosing a disk. Data-heavy,
evidence-first, precision over chrome.

| Decision | Choice | Why |
|----------|--------|-----|
| Foundation | Cool slate/neutral, monochrome | Structure in gray; color only for meaning |
| Accent | ONE cyan/teal (#4dd0e1 dark / #0e7490 light) | Actionable data + highlight, never decorative |
| Depth | Borders-only (flat) | Developer tool; 1px borders, no heavy shadows (Linear) |
| Radius | 6px system | Technical, consistent |
| Typography | System sans for UI, monospace for data | "This is data" |
| Modes | Dark-first, clean light fallback | Dev on dark Mac; reporte técnico premium |
| Grid | 4px strict, symmetrical padding | Craft |
| Color-for-meaning | Status (ok/warn/err) + accent only | Anti-pattern: decorative color |

---

## WCAG AA-validated palette (verified with color_engine.py contrast)

Every pair below passed AA (≥4.5:1 normal text). Validated against the REAL badge
backgrounds (status text on its own 10% tint, not on plain surface — the honest check).

### Dark theme (`--bg #0b0e14`, `--surface #11151d`)
| Token | Hex | Ratio | Context |
|-------|-----|-------|---------|
| `--fg` | `#e6e9ef` | 15.88 (AAA) | primary text on bg |
| `--fg-secondary` | `#aab2c0` | 9.05 (AAA) | body on bg |
| `--fg-muted` | `#888fa0` | 5.96 (AA) | labels/hints (bumped from #6b7384=4.06✗) |
| `--fg-faint` | `#646c7a` | 3.65 | footer/decorative (non-essential) |
| `--accent` | `#4dd0e1` | 10.51 (AAA) | on bg |
| `--ok` | `#5dbb74` | 6.55 | badge text on its 10% tint |
| `--warn` | `#e0a84a` | 7.27 | badge text on its 10% tint |
| `--err` | `#e06c6c` | 5.04 | badge text on its 10% tint |

### Light theme (`--bg #f6f7f9`, `--surface #fff`)
| Token | Hex | Ratio | Note |
|-------|-----|-------|------|
| `--fg` | `#0f172a` | 16.65 (AAA) | |
| `--fg-secondary` | `#475569` | 7.07 (AAA) | |
| `--fg-muted` | `#5b6577` | 5.48 (AA) | bumped from #94a3b8=2.39✗ |
| `--accent` | `#0e7490` | 5.00 (AA) | bumped from #0891b2=3.43✗ |
| `--ok` | `#166534` | 6.14 | badge on tint (bumped from #16a34a) |
| `--warn` | `#854d0e` | 5.97 | badge on tint (bumped from #ca8a04) |
| `--err` | `#b91c1c` | 5.50 | badge on tint (bumped from #dc2626) |

**Re-validation command** (when reapplying):
```bash
CE="./scripts/color_engine.py" # Or path to color-theory-engine
python3 "$CE" contrast "#888fa0" "#0b0e14"   # fg-muted dark
# status badges: validate on computed tint bg = 0.10*status + 0.90*surface
```

---

## CSS tokens (design system)

Full `:root` + `@media (prefers-color-scheme: light)` block is in git history / the
v3-era script. Key tokens: `--font-sans`, `--font-mono` (`ui-monospace, SF Mono`),
`--bg/surface/surface-2`, `--border/border-strong`, `--fg/fg-secondary/fg-muted/fg-faint`,
`--accent/accent-dim`, `--ok/warn/err`, `--r:6px`. Classes: `.wrap`, `.masthead`,
`.tag`, `.sub`, `.mono`, `.eyebrow`, `.notice`, `.grid`, `.stat` (`.label`/`.value`),
`section`+`h2`, `.hint`, table density, `.empty`, `.status`(`.ok`/`.warn`/`.err`),
`.chart`, svg `.bar`/`.chart-label`/`.chart-value`, `.next`, `footer`.

Craft principles: 4px grid spacing, symmetrical padding, borders-only depth (no shadows),
mono for all data (bytes/paths/inodes/commands), status badges with 10% tint bg.

---

## Body structure (map to v4's 7 sections when reapplying)

v4 body `<h2>` sections (must all be preserved when reapplying):
1. Volume capacity views (NEW in v4)
2. Largest measured directories (was "Largest attributed")
3. Per-device attribution (NEW in v4)
4. Cache candidates
5. Large-item candidates (was "Large-file")
6. Native command evidence
7. Required next step

Reapply pattern: wrap each section in `<section>`, use `.chart` card for charts,
`.stat` cards for the meta grid (Generated/Tool version/Accounting gap → adapt to v4's
capacity views), `.status` badges for command exit codes, `.next` box for required step.

---

## Re-application method (debugged — follow exactly)

1. **edit tool is broken this session for absolute paths** → use `write` for a temp
   Python replacement script, or `bash + python`.
2. **`read` shows phantom indentation**: the f-string body of `return f"""..."""` is
   at column 0 in the real file, but `read` rendered it with 4-space indent → exact-string
   matching fails. **Use anchor-based replacement** (`src.index("<style>")` …
   `src.index("</style>")`, and `<body>` … `</body></html>"""`), not exact block match.
3. **f-string braces**: CSS is pure style (no interpolations) → double every `{`→`{{`
   and `}`→`}}` so the surrounding f-string emits literal braces. Body has
   interpolations (`{html.escape(...)}`) → leave single.
4. **Closing `"""`**: if NEW_BODY is delimited with `"""..."""`, the trailing `"""`
   that closes the target's `return f"""` gets swallowed → SyntaxError (f-string runs
   to EOF). **Delimit NEW_BODY with triple-SINGLE-quote `'''...'''`** so the literal
   `"""` at the end is preserved.
5. `command_rows` status badges: compute `_status`/`_scls` before the append; emit
   `<span class="status {_scls}">`; `exit`/`unavailable` → `err`, `timeout` → `warn`,
   `ok` → `ok`.

**Validate after reapply:** `python3 -c "import ast; ast.parse(open(SCRIPT).read())"`
(syntax, no bytecode), then regenerate the report and grep for `class="masthead"` /
`status (ok|warn|err)`.

---

## Why deferred

v4 is a net gain in **observability** (System/Data volume modeling, Foundation capacity
probe, per-dir confidence, scope dedup, mdutil-tied Spotlight) — the core purpose of the
v3+ skill. Reapplying the design system on the *draft* v4 would risk the 2 new sections
and churn. Plan: lock v4 to stable (run the 13 unit tests + macOS fixture validation),
then reapply this design system in one deliberate pass.
