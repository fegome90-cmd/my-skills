---
disable-model-invocation: true
name: claude-md-optimizer
description: "Use when creating or optimizing CLAUDE.md files for Claude Code based on expert research and anti-patterns, detecting project type and applying templates. Do NOT use for general skill creation or prompt templates outside Claude Code."
search_hints: CLAUDE.md optimize anti-patterns templates project-type progressive disclosure Claude Code
---

## Overview

Generates optimized CLAUDE.md files by:
1. Detecting project type from key files (pyproject.toml, package.json, tsconfig.json)
2. Analyzing existing CLAUDE.md against anti-patterns
3. Applying expert best practices from research
4. Presenting proposal for user confirmation

## When to Use

- Creating new CLAUDE.md for a project
- Optimizing existing CLAUDE.md against anti-patterns
- Updating CLAUDE.md after major architectural changes

## When NOT to Use

- General skill authoring or onboarding → use `skill-onboarding` or `template-skill`
- Prompt engineering for commands/agents → use `prompt-doctor` or `ai-work-prompting-gates`
- Repository-wide documentation not governed by CLAUDE.md guidelines

## Process

### Step 1: Detect Project Type

Read these files in order (first match wins):
1. `pyproject.toml` → Check for FP indicators ('fp', 'clean-arch', 'domain/')
2. `tsconfig.json` + `src/domain/` → TypeScript + Clean Architecture
3. `package.json` → Check for framework (next, react, vue)
4. `requirements.txt` / `environment.yml` → Data Science

**If detection fails:** Present menu to user:
```
🔍 No pude determinar el tipo de proyecto automáticamente.

Archivos encontrados:
  - [list files]

¿Podrías ayudarme identificando el tipo de proyecto?

1) Python Backend (FP + Clean Architecture)
2) Python Backend (estándar/django/fastapi)
3) TypeScript Backend (Clean Architecture)
4) Web App (Next.js/React/Vue)
5) Data Science/ML
6) Otro (describir)
```

### Step 2: Analyze Existing CLAUDE.md

If CLAUDE.md exists, check for anti-patterns:
- File length exceeding conciseness heuristic (~60-150 lines without progressive disclosure)
- Code style guidelines (should use linters)
- Verbose command documentation (should use npm/task runner scripts)
- Long narrative paragraphs
- Task-specific instructions (not universal)

### Step 3: Generate Optimized Version

Load template from `resources/template-*.md` based on detected type and customize with:
- Detected tech stack
- Commands from package.json/pyproject.toml scripts
- Architecture patterns from codebase structure
- References to existing docs (README.md, ARCHITECTURE.md, PRP.md)

### Step 4: Present and Confirm

Show proposal and ask: "¿Aplicar estos cambios? (y/n)"

## Resources

- `resources/anti-patterns.md` - Known anti-patterns from research
- `resources/best-practices.md` - Expert recommendations
- `resources/template-*.md` - Project-type templates

## Anti-Patterns to Avoid

❌ Code style guidelines → Use linters (ESLint, Prettier, ruff)
❌ Unfocused monoliths (>150 lines without seams) → Use progressive disclosure
❌ Verbose commands → Create npm/py scripts
❌ Long paragraphs → Use bullets
❌ Negative-only constraints → Always provide alternatives
❌ Embedded documentation → Reference file paths

## Best Practices

✅ Aim for conciseness (~60-150 lines heuristic; prefer semantic clarity over strict counting)
✅ Progressive disclosure → External docs
✅ Simple commands → npm/py scripts
✅ Bullets > paragraphs
✅ Pointers to files, not copies
✅ Living document → Iterate based on friction

## Quick Reference

### File Detection

| Type | Key Files | Indicators |
|------|-----------|------------|
| python-fp | pyproject.toml | 'fp', 'clean-arch', 'src/domain/' |
| typescript-clean | tsconfig.json | 'src/domain/', 'src/infrastructure/' |
| web-standard | package.json | 'next', 'react', 'vue', 'vite' |
| data-science | requirements.txt | 'pandas', 'scikit-learn', 'jupyter' |

### Template Selection

```bash
# Python + FP
resources/template-python-fp.md

# TypeScript + Clean Architecture
resources/template-typescript-clean.md
```
