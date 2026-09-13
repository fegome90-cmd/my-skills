---
disable-model-invocation: true
name: learned-progressive-disclosure
description: "Use when refactoring large skills (>300 lines) into orchestrator + resources/ pattern. Reduces context bloat by loading detailed instructions only when needed. Do NOT use for simple single-purpose skills."
search_hints: progressive disclosure skill structure orchestrator resources refactoring phases variants
metadata:
  triggers:
    - "progressive"
    - "disclosure"
    - "skill"
    - "structure"
    - "orchestrator"
  role: specialist
  scope: implementation
version: 1.0.0
---

# Progressive Disclosure for Skills

## Context
When a skill becomes too large, it contaminates the LLM context and becomes harder to maintain. Skills with multiple phases or variants are especially prone to bloat.

## Problem
- Monolithic instruction files load unnecessary context and crowd out active reasoning
- Multi-phase skills require different instructions at different execution phases
- Mixing orchestration with low-level details creates high maintenance burden
- Temporary workspace scratchpads and untracked runtime state pollute skill directories

## Solution

### Structure

```text
skills/<skill-name>/
├── SKILL.md           # Orchestrator (concise entry point, ideally ~100-200 lines)
├── resources/         # Detailed instructions and reference materials
│   ├── phase-1.md
│   ├── phase-2.md
│   └── variant-a.md
└── scripts/           # Optional small executable helpers
```

### SKILL.md (Orchestrator)

Contains only:
- Frontmatter (name, description for triggering)
- Index/table of contents pointing to resources/
- Entry point instructions
- When to load which resource

```markdown
---
name: my-workflow
description: "Multi-phase workflow. Triggers on X, Y, Z."
---

# My Workflow

## Phases

| Phase | Resource | When to Load |
|-------|----------|--------------|
| Init | resources/init.md | Starting fresh |
| Execute | resources/execute.md | After init |
| Cleanup | resources/cleanup.md | After execute |

## Entry Point
1. Determine current phase from context
2. Read corresponding resource
3. Execute instructions
4. Advance to next phase
```

### resources/ (Details)

Each file ~100-200 lines with:
- Specific instructions for that phase/variant
- Tools to use
- Output format
- Validation checklist

### Directory Hygiene

**DO NOT** leave runtime garbage or temporary session state in the skill package:
```text
❌ skills/my-skill/
   ├── SKILL.md
   ├── .DS_Store / *.swp / *~ # NO - editor/OS noise
   ├── workspace/             # NO - temporary agent scratchpads go to /tmp or scratch
   ├── __pycache__/ / *.pyc   # NO - runtime build artifacts
   └── audit-run-*/           # NO - transient run logs belong in gitignore
```

**Allowed package structure:**
```text
✅ skills/my-skill/
   ├── SKILL.md               # Entry point and index
   ├── resources/             # Deep reference materials and templates
   ├── scripts/               # Optional small executable helpers
   ├── tests/                 # Optional verification test suite
   └── evals/                 # Optional evaluation datasets/fixtures (when needed)
```

## Example

**Before (monolithic 500 lines):**
```markdown
# reviewctl-workflow

## Phase 1: Init
[100 lines of init instructions]

## Phase 2: Explore
[150 lines of explore instructions]

## Phase 3: Plan
[100 lines of plan instructions]

...
```

**After (progressive disclosure):**
```text
reviewctl-workflow/
├── SKILL.md (~150 lines - index + entry)
└── resources/
    ├── init.md (~100 lines)
    ├── explore.md (~150 lines)
    └── plan.md (~100 lines)
```

Context loaded: ~300 lines max (orchestrator + 1 resource)

## Activation Signals

- Skill exceeds ~250-300 lines without clear internal separation
- Skill has 3+ distinct execution phases
- Skill has distinct variants (e.g., by language, by framework, by toolchain)
- Skill mixes high-level orchestration with low-level reference detail

## Quality Checklist

- [ ] SKILL.md acts as a concise entry point and index (semantic clarity wins over strict line counting)
- [ ] Each resource file is focused on a single topic, phase, or variant
- [ ] Index table in SKILL.md points to all resources
- [ ] No temporary workspace scratchpads, cache files, or runtime logs in the package
- [ ] Resources are independently loadable and self-contained
- [ ] Markdown quality gate passed (see `skills/skill-onboarding/resources/markdown-quality.md`)

## Learned From

| Attribute | Value |
|-----------|-------|
| Session | 2026-02-28 |
| Context | Creating rctl-workflow skill system |
| Issue | Single skill would be ~1000 lines |
| Solution | Orchestrator + resources/ |
| Evidence | `.pi/plan/rctl-workflow-architecture.md` |
