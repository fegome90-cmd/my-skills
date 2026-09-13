# Frontmatter Standardization Guide (v2.1.5, TWO-TIER)

Guide for writing `SKILL.md` YAML frontmatter that works identically across every
agent harness. The contract is explicitly two-tier.

---

## 1. Two-Tier Schema

### Tier 1 — CORE (the universal contract)

Only these two fields are required to be parsed by any consumer:

```yaml
---
name: {skill-name}
description: >
  {Concise, high-signal summary of capabilities}.
  Trigger: {Explicit keywords, user phrases, and scenarios that activate this skill}.
---
```

### Tier 2 — ADVISORY (safe-to-ignore everywhere)

The following fields are **advisory metadata**. Consumers that do not understand them
MUST safely ignore them; dropping them never breaks skill discovery or execution.
This ignore-safety is a proven property of this codebase: no runtime script parses
YAML frontmatter at all (all checks are plain substring probes), so advisory fields
cannot influence routing or verification behavior.

```yaml
license: {upstream-license-preserved}
metadata:
  author: {upstream-author}
  onboarded_by: {your-name-or-organization}
  upstream_version: "{version}"
  tier: {T0|T1|T2|T3}
  risk: {read-only|local-write|git-mutating|network-external|elevated-exec}
  playbook: {debug|testing|architecture|governance|workflow|data}
allowed-tools: {comma-separated-least-privilege-tools}
```

---

## 2. Field Rules & Constraints

### `name` (CORE, Required)
- Lowercase alphanumeric with hyphens only (`^[a-z0-9-]+$`).
- Maximum 64 characters.
- No vendor prefixes naming a specific harness.

### `description` (CORE, Required)
- Routing surface for discovery: state capability + explicit trigger scenarios,
  including when the skill must NOT be used. This field IS the procedure summary
  replacement: keep it high-signal, not a logline.
- Do NOT include redundant keywords in the body; search agents read the frontmatter description.

### `license` (ADVISORY)
- Carry over the upstream license verbatim (`MIT`, `Apache-2.0`, `GPL-3.0`, `BSD-3-Clause`, `Unlicense`).
- **Never perform license washing.**

### `metadata` (ADVISORY)
- `author`: Original author or organization.
- `onboarded_by`: Local adopter / maintainer.
- `tier`: Complexity ceiling (`T0`–`T3`).
- `risk`: Capability risk tier (`read-only`, `local-write`, etc.).
- `playbook`: Operational domain tag.

### `allowed-tools` (ADVISORY)
- Document intent as least privilege; every harness maps or ignores tool names on its own:
  - Reading / analysis skills: `Read, Glob, Grep`
  - Code generation / editing skills: `Read, Edit, Write, Glob, Grep`
  - Execution / CLI skills: `Read, Edit, Write, Glob, Grep, Bash`
- Do not list tools your steps do not actually execute. Harness-dispatch-only tools
  belong here only if a documented step relies on them.

---

## 3. Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Correct Approach |
|---|---|---|
| Treating advisory fields as load-bearing | Portable consumers may ignore them; nothing in this runtime parses YAML. | Keep core guarantees in `name`/`description`; treat the rest as documentation. |
| Hardcoding `license: Apache-2.0` on external code | License violation and legal drift. | Preserve upstream license string verbatim. |
| Vague description (`"Helper skill"`) | Blocks safe card promotion on hub card rendering. | State specific problem, input, output, and explicit triggers. |
| Adding a `## Keywords` section in body | Wastes context window; indexing uses frontmatter. | Put search hints and triggers into the YAML block. |
