# Procedures: Create, Repair, Audit

Three modes with dedicated procedures. Each produces different output.

## Mode 1: Create

### Step 1: Determine Location

| Scope | Path |
|-------|------|
| Global (all projects) | `~/.pi/agent/prompts/<name>.md` |
| Project-specific | `.pi/prompts/<name>.md` |

Name becomes the `/command`. Use lowercase, hyphens for separators. Colons (`:`) are allowed for namespacing (e.g. `tf:spawn.md` → `/tf:spawn`).

### Step 2: Write Frontmatter

```yaml
---
description: "Always quoted. Describe what the prompt does and when to use it."
argument-hint: "[optional] describe arguments — quote if special chars"
---
```

Rules:
- `description` is the ONLY required field
- ALWAYS wrap `description` in double quotes
- ALWAYS wrap `argument-hint` in double quotes if it contains `[`, `]`, or `:`
- Keep description under 120 characters for best TUI display
- Do NOT use YAML multiline (`>` or `|`) — causes truncation in skill-hub

### Step 3: Write Body

Structure:

```markdown
# Prompt Title

1-2 sentences: what this prompt makes the agent do.

## Context / Inputs

$ARGUMENTS or $1, $2 for positional args.

## Procedure

Numbered steps the agent should follow.

## Rules

Operational constraints.

## Output Format

Expected output structure or envelope.
```

### Step 4: Validate

```bash
# Parse test — use pi's own parser dynamically resolved from PATH
node -e "
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const piBin = execSync('which pi', { encoding: 'utf-8' }).trim();
const realPi = fs.realpathSync(piBin);
const fmPath = path.resolve(path.dirname(realPi), '../utils/frontmatter.js');
const { parseFrontmatter } = await import(fmPath);
const content = fs.readFileSync('<path>', 'utf-8');
try {
  const { frontmatter, body } = parseFrontmatter(content);
  console.log('PASS: description=[' + frontmatter.description + ']');
} catch(e) {
  console.log('FAIL: ' + e.message);
}
"
```

### Step 5: Verify in TUI

Restart pi or reload templates. Type `/` in editor — prompt should appear in autocomplete.

## Mode 2: Repair

### Step 1: Diagnose

Run the validation script from `frontmatter-reference.md` on the broken file. Common failures:

| Symptom | Likely Cause | Check |
|---------|-------------|-------|
| Prompt not in autocomplete | YAML parse error | Run parseFrontmatter on file |
| Prompt in autocomplete but wrong description | Unquoted special chars | Check for bare `:`, `#`, `[` |
| Prompt loads but content is empty | Missing body after `---` | Verify second `---` exists |
| `PROMPT_MIGRATION_TRACKER` appears as command | Non-prompt `.md` in prompts dir | Move to subdirectory or rename |

### Step 2: Fix Frontmatter

The most common fix — add quotes:

```yaml
# Before (broken)
description: Phase 5.5 & 5.7: Validation Gate

# After (fixed)
description: "Phase 5.5 & 5.7: Validation Gate"
```

### Step 3: Fix Body

Check for:
- Missing second `---` closing frontmatter
- Content starts with `#` heading after blank line
- No BOM or invisible characters (check with `xxd | head -5`)
- Body is not empty

### Step 4: Validate and Verify

Same as Create Steps 4-5.

## Mode 3: Audit

### Step 1: Batch Validate

```bash
node -e "
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const piBin = execSync('which pi', { encoding: 'utf-8' }).trim();
const realPi = fs.realpathSync(piBin);
const fmPath = path.resolve(path.dirname(realPi), '../utils/frontmatter.js');
const { parseFrontmatter } = await import(fmPath);
const dir = '<prompts-dir>/';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.md'));
let pass = 0, fail = 0;
for (const name of files) {
  try {
    const content = fs.readFileSync(path.join(dir, name), 'utf-8');
    const { frontmatter, body } = parseFrontmatter(content);
    const desc = frontmatter.description || '(no description)';
    console.log('PASS: /' + name.replace('.md','') + ' [' + desc.slice(0,60) + ']');
    pass++;
  } catch(e) {
    console.log('FAIL: /' + name.replace('.md','') + ' — ' + e.message.split('\n')[0]);
    fail++;
  }
}
console.log('\nResult: ' + pass + ' PASS, ' + fail + ' FAIL');
" 2>&1
```

### Step 2: Check Content Quality

For each prompt that passes parsing:

| Check | Criteria |
|-------|----------|
| Has description | `frontmatter.description` is non-empty |
| Has body | `body.length > 50` characters |
| Uses arguments | References `$ARGUMENTS` or `$1` (if prompt takes args) |
| Self-contained | No references to files that don't exist |
| No dead imports | No references to `imports/` subdirectory files |
| Under budget | Body < 800 lines (context window concern) |

### Step 3: Report

```
## Prompt Audit Report

### Parse Results
- PASS: N files
- FAIL: N files (list each with error)

### Quality Issues
- [list issues with severity and fix]

### Recommendations
- [actions: quote frontmatter, remove dead refs, split oversized prompts]
```
