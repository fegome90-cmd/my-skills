# Markdown Quality Gate (shared)

> Apply when a skill gains a `resources/`, `references/`, `scripts/`, or
> `templates/` directory. Mechanical checks — no linter dependency.
> Run before registering the skill.

This snippet is the SINGLE source of truth for markdown quality across skill
onboarding. Other structure-teaching skills reference it with one line instead
of copying the rules (no drift).

## Gate condition

Only run these checks when the skill has a non-trivial directory layout. A flat
single-file `SKILL.md` needs none of this — skip the gate.

## Checks (stateful — no markdownlint required)

### 1. Every fenced code block declares a language

A bare opening fence (backticks with no language token) fails markdownlint MD040
and renders unstyled. Closing fences are legitimately bare, so a plain
`grep '^```$'` is wrong — it false-flags every closer. Use a stateful check that
tracks open/close:

```bash
awk '
  /^```/ {
    if (!inblock) {                                  # opening fence
      if ($0 ~ /^```[ \t]*$/) print FILENAME ":" FNR ": MD040 bare opening fence"
      inblock = 1
    } else { inblock = 0 }                           # closing fence — always OK
    next
  }
' SKILL.md resources/*.md
```

Output must be empty. (If `markdownlint` is installed, run it too for extra
signal — but the awk above is the contract.)

### 2. Heading hierarchy has no skipped levels

Walk headings top-down. Each heading level may increase by at most 1 (a `##`
must not jump to `####` without a `###` between them).

```bash
grep -nE '^#{1,6} ' SKILL.md resources/*.md
```

### 3. Internal references resolve

Every backtick-quoted path you point agents to (e.g. `resources/foo.md`) must
exist on disk. Extract each ` `path/to/file` ` token and `test -f` it — this is
the one check that needs judgment, not just grep.

## What this gate is NOT

- Not a style enforcer (line length, table pipe spacing) — those are cosmetic.
- Not a full linter — the three checks above catch mechanical defects only.
- Not a substitute for reading the file.
