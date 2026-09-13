---
name: prompt-doctor
description: "Use when creating, repairing, or auditing pi prompt templates. Covers frontmatter validation, YAML quoting rules, discovery debugging, and progressive disclosure. Triggers for prompt creation, prompt not appearing, /command missing, frontmatter error, YAML parse error. Do NOT use for skill creation (use skill-create) or general documentation."
search_hints: prompt template frontmatter YAML quoting discovery autocomplete command repair audit
metadata:
  triggers:
    - "prompt not appearing"
    - "create prompt"
    - "repair prompt"
    - "frontmatter error"
    - "/command not found"
    - "prompt audit"
  role: specialist
  scope: implementation
version: "1.0.0"
---

# Prompt Doctor

Create, repair, and audit pi prompt templates. Covers frontmatter validation, YAML quoting, discovery debugging, and content quality.

## When to Use / When Not to Use

| Use | Don't Use |
|-----|-----------|
| Create new `/command` prompts | Create skills (use `skill-create`) |
| Fix prompts not appearing in TUI | General documentation |
| Audit existing prompts for quality | Write extension code |
| Validate frontmatter YAML | Debug pi internals |

## Three Modes

| Mode | Trigger | Output |
|------|---------|--------|
| **create** | User wants a new `/command` | Valid, registered prompt file |
| **repair** | Prompt doesn't appear or throws error | Fixed prompt with root cause |
| **audit** | Batch check all prompts | Health report with pass/fail per file |

## Quick Reference

### Prompt Locations (auto-discovered)

| Location | Scope | Discovery |
|----------|-------|-----------|
| `~/.pi/agent/prompts/*.md` | Global | Automatic |
| `.pi/prompts/*.md` | Project | Automatic |
| `prompts/` array in settings | Configured | Automatic |
| Subdirectories of above | — | **NOT automatic** |

Discovery is **non-recursive**. Files in subdirectories are invisible unless added to settings.

### Frontmatter Format

```yaml
---
description: "One-line description. Always quote if it contains : or special chars."
argument-hint: "[optional] [args] — quote if contains brackets"
---
```

Required: `description` field. Everything else is optional.

### The #1 Bug: Unquoted Colons

YAML treats unquoted `:` as key-value separator. Pi silently skips prompts that fail to parse.

```yaml
# BROKEN — YAML sees "Phase 2 & 3" as key, "Save Context..." as value
description: Phase 2 & 3: Save Context

# FIXED — quoted string
description: "Phase 2 & 3: Save Context"
```

## Procedures

For detailed step-by-step procedures, see [resources/procedures.md](resources/procedures.md).

For the complete frontmatter spec and quoting rules, see [resources/frontmatter-reference.md](resources/frontmatter-reference.md).

For common bugs and diagnosis, see [resources/known-issues.md](resources/known-issues.md).

## Resources Index

| Resource | Purpose | Lines |
|----------|---------|-------|
| [procedures.md](resources/procedures.md) | Create/repair/audit step-by-step | ~150 |
| [frontmatter-reference.md](resources/frontmatter-reference.md) | YAML spec, quoting, validation | ~80 |
| [known-issues.md](resources/known-issues.md) | Common bugs, diagnosis, fixes | ~60 |

## Key Distinctions

| Confusion | Clarification |
|-----------|---------------|
| Prompt vs Skill | Prompts = `/command` templates, no code. Skills = full capability packages with scripts/resources. |
| `imports/` prompts | Subdirectory files are NOT discovered. They're reference material, not commands. |
| `description` quoting | Always quote if contains `:`, `#`, `[`, `]`, `{`, `}`, `&`, `*`. Safe to always quote. |
| Silent failure | Pi catches YAML parse errors silently — prompt disappears without warning. |
| `$ARGUMENTS` vs `$@` | Both expand to all args. Use `$1`, `$2` for positional. `${@:N}` for slicing. |
