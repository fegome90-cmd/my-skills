# Known Issues and Diagnosis

Common bugs encountered in pi prompt templates, with diagnosis and fixes.

## Issue 1: Prompt Silently Missing from Autocomplete

**Symptom:** File exists in `~/.pi/agent/prompts/` but `/name` doesn't appear in TUI autocomplete.

**Root Cause:** YAML frontmatter parse error. Pi's `loadTemplateFromFile` catches parse errors silently (returns `null`).

**Diagnosis:**
```bash
node -e "
const { parseFrontmatter } = await import('/opt/homebrew/lib/node_modules/@mariozechner/pi-coding-agent/dist/utils/frontmatter.js');
const fs = await import('fs');
const content = fs.readFileSync('<path>', 'utf-8');
try { parseFrontmatter(content); console.log('PASS'); }
catch(e) { console.log('FAIL:', e.message); }
"
```

**Common causes:**
1. Unquoted `:` in description → "Nested mappings are not allowed"
2. Unquoted `[` in argument-hint → "Unexpected flow-seq-start"
3. Missing second `---` → parser treats entire file as frontmatter
4. BOM (byte order mark) → file doesn't start with `---`

**Fix:** Quote the offending value or add missing `---`.

## Issue 2: File in Subdirectory Not Discovered

**Symptom:** Prompt file is in `~/.pi/agent/prompts/imports/` but doesn't appear.

**Root Cause:** Pi discovery is non-recursive. Only top-level `*.md` files in prompts directories are auto-discovered.

**Fix:** Move file to top-level `prompts/` directory, or add the subdirectory to `settings.json`:
```json
{ "prompts": ["~/.pi/agent/prompts/imports"] }
```

**Note:** Adding a directory registers ALL `.md` files in it as commands.

## Issue 3: PROMPT_MIGRATION_TRACKER Appears as Command

**Symptom:** `/PROMPT_MIGRATION_TRACKER` appears in autocomplete.

**Root Cause:** Any `.md` file in the prompts directory becomes a command, including non-prompt documentation files.

**Fix:** Move tracking documents to a subdirectory (non-recursive discovery excludes them) or rename to non-`.md` extension.

## Issue 4: Description Shows as `">"` or `"|"`

**Symptom:** In skill-hub manifest or autocomplete, description shows as literal `">"` or `"|"`.

**Root Cause:** YAML multiline operators (`>` folded, `|` literal) used in frontmatter.

**Fix:** Use a single-line quoted string instead:
```yaml
description: "One-line description that is clear and concise"
```

## Issue 5: Arguments Not Expanding

**Symptom:** `$ARGUMENTS` or `$1` appears literally in expanded prompt.

**Root Cause:** Variables only expand when the prompt is invoked with `/name args`. They don't expand when loaded as a skill or via `--prompt-template`.

**Fix:** Ensure the prompt is invoked as `/name args` from the TUI editor.

## Issue 6: Prompt Content is Empty After Expansion

**Symptom:** Prompt loads but agent receives no instructions.

**Root Cause:** Missing body — content between frontmatter `---` and end of file is empty.

**Fix:** Verify file structure:
```
---
description: "..."
---

# Prompt body starts here after a blank line
```

The blank line after `---` is important. Without it, content may be included in frontmatter parsing.
