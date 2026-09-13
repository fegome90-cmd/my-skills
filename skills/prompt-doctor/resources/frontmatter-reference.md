# Frontmatter Reference

Complete spec for pi prompt template frontmatter. Based on pi source code (`prompt-templates.js` + `frontmatter.js`).

## Parser Behavior

Pi uses the `yaml` npm package to parse frontmatter. The parser:

1. Checks if content starts with `---`
2. Finds the next `\n---` after position 3
3. Extracts the text between as YAML
4. Parses with `yaml.parse()`
5. Returns `{ frontmatter, body }` where body is everything after the second `---`

If parsing fails, `loadTemplateFromFile` catches the error silently and returns `null`. The prompt is **silently excluded** from autocomplete — no warning, no error message.

## Required Fields

| Field | Required | Type | Max Length |
|-------|----------|------|-----------|
| `description` | YES | string | ~120 chars practical (TUI display) |

## Optional Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `argument-hint` | Shows arg syntax in autocomplete | `"[feature\|bugfix] <description>"` |
| (any other key) | Ignored by pi | — |

## Quoting Rules (CRITICAL)

**Rule: Always wrap string values in double quotes if they contain ANY of these characters:**

| Char | Why it breaks | Example |
|------|--------------|---------|
| `:` | YAML interprets as key-value separator | `description: Phase 1: Plan` |
| `#` | YAML comment | `description: Fix bug #123` |
| `[` `]` | YAML flow sequence | `argument-hint: [--phase init]` |
| `{` `}` | YAML flow mapping | `description: Use {json} format` |
| `&` `*` | YAML anchor/alias | `description: Find & fix` |
| `!` | YAML tag | `description: Don't! use` |
| `>` `\|` | YAML folded/literal | Avoid as values — use `">"` if needed |

**Safe practice: Always quote `description` and `argument-hint`. No downside.**

```yaml
# ALWAYS SAFE
description: "Any text here: with colons, [brackets], & ampersands"

# RISKY — only safe if NO special chars
description: Simple text without special characters
```

## What NOT to Do

```yaml
# BROKEN: Multiline YAML — causes truncation in downstream systems
description: >
  This is a long description
  that wraps across lines

# BROKEN: Bare colon
description: Phase 1: Planning

# BROKEN: Bare brackets
argument-hint: [--phase init|plan]

# BROKEN: Missing description
---
# My Prompt
body content
---
```

## Template Expansion Variables

Inside the body (not frontmatter), these variables expand:

| Variable | Expands To |
|----------|-----------|
| `$ARGUMENTS` | All arguments joined by space |
| `$@` | Same as `$ARGUMENTS` |
| `$1`, `$2`, ... | Positional argument |
| `${@:N}` | Args from Nth position (1-indexed) |
| `${@:N:L}` | L args starting from Nth |

## Validation Script

One-liner to test any prompt file against pi's actual parser:

```bash
node -e "
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const piBin = execSync('which pi', { encoding: 'utf-8' }).trim();
const realPi = fs.realpathSync(piBin);
const fmPath = path.resolve(path.dirname(realPi), '../utils/frontmatter.js');
const { parseFrontmatter } = await import(fmPath);
const content = fs.readFileSync(process.argv[1], 'utf-8');
try {
  const { frontmatter, body } = parseFrontmatter(content);
  console.log('PASS');
  console.log('description:', frontmatter.description || '(empty)');
  console.log('body length:', body.length, 'chars');
} catch(e) {
  console.log('FAIL:', e.message);
}
" /path/to/prompt.md
```
