# Learned Lessons (v1.0 → v1.2)

Patterns discovered during the creation, auditing, and hardening of this skill.
These apply to any skill creation or curation process, not just authority-flow audits.

---

## L1: Frontmatter Description Must Be Single-Line Quoted String

The skill-hub registration pipeline (`register_skill.py`) cannot parse YAML multiline
scalars (`>` folded or `|` literal). It extracts the indicator character literally,
producing `">"` as the description in the hub entry and manifest.

**Symptom:** Manifest description = `">"`, hub entry has no readable description,
`audit_skill_hub.py` reports "suspect description: truncated_or_empty".

**Fix:** Always use single-line quoted strings:
```yaml
# BAD — causes truncation
description: >
  Long description here.

# GOOD — always works
description: "Use when X. Also triggers for Y. Do NOT use for Z."
```

This applies to ALL skills registered via the indexing pipeline.

---

## L2: Description Lives in 3 Places — Expect Drift

After registration, a skill's description exists in:
1. SKILL.md YAML frontmatter (source of truth)
2. Hub entry `.md` file in `~/.trifecta/segments/skills-hub/` (extracted copy)
3. Manifest JSON in `_ctx/skills_manifest.json` (extracted copy)

If you manually edit the hub entry without re-registering, or change SKILL.md
without re-running `register_skill.py`, the three copies drift apart.

**Mitigation:** Always re-register after any frontmatter change. Verify with
`audit_skill_hub.py` and check manifest entry directly.

---

## L3: Content Coherence Is a Separate Check From Structure

A skill can pass all progressive disclosure checks (line counts, context budget,
directory hygiene) while having its SKILL.md describe resources incorrectly.

Example: SKILL.md says core heuristics are "double writer, bypass, hidden delegation,
evidence-as-authority, SSOT violation" but the actual file contains H1-H5 that don't
match this list.

**Fix:** Add a content coherence check after progressive disclosure:
- Grep H-titles from each resource
- Compare against SKILL.md's description of what each resource contains
- Mismatch = block registration

---

## L4: Change-Audit Is Not Repo-Audit-Lite

When a skill supports two modes, the secondary mode cannot be defined as "same
procedure but with less input." Change-audit needs its own procedure because:

- It works on deltas, not full inventories
- It needs before/after comparison logic
- Its output must mark items as NEW / MODIFIED / UNCHANGED-AFFECTED
- It asks different questions (was this single-source before? is it still?)

Generic procedures shared between modes produce generic output. Each mode that
produces different output needs its own procedure resource.

---

## L5: Discovery Must Be Prioritized, Not Exhaustive

"Catalog every executable surface" is the wrong starting instruction for repos with
hundreds of functions. It produces noise: pure readers, helpers, display functions,
test fixtures — none of which affect authority.

The correct approach is tiered:
- **Tier 1** (always): Entrypoints, writers, jobs, hooks, daemons
- **Tier 2** (if affects mutation): Wrappers, transformers, importers
- **Tier 3** (skip unless scoped): Pure readers, helpers, test fixtures

This is analogous to the "triage before diagnosis" pattern in debugging.

---

## L6: Overlapping Heuristics Produce Ambiguous Findings

When two heuristics can produce the same finding from different angles, the audit
produces duplicates or the auditor wastes time classifying which heuristic applies.

Example: H4 "wrapper reimplements instead of delegating" and H11 "surface appears
delegated but has hidden side effects" — both target wrappers that don't behave as
advertised. The fix is consolidation: one heuristic covers both manifestations.

**Rule:** If two heuristics share the same detection trigger (same grep pattern, same
surface type), they should be one heuristic with subsections, not two separate entries.

---

## L7: Context Budget Is Largest Single Resource, Not Sum

The correct calculation for context budget is:
```
SKILL.md lines + max(resource lines)
```
NOT the sum of all resources. Progressive disclosure means only one resource is loaded
at a time. Using the total sum overestimates context consumption by 3-5x.

---

## L8: Self-Auditability Is a Quality Gate

If a skill analyzes structure, authority, or flows, it should be applicable to itself.
If it produces nonsensical output when self-applied, the skill has a design problem.

This is not required for all skills (a TDD coaching skill doesn't need to self-test),
but for any skill that produces structured analysis of code/systems, self-auditability
is a strong signal of operational completeness.

---

## L9: Progressive Disclosure Is Meta-Auditable

The progressive disclosure checklist can be applied to ANY skill, not just the one
being created. It is itself a reusable quality gate:

1. SKILL.md < 200 lines
2. Each resource < 250 lines
3. Index table points to all resources
4. No evals/workspace in skill directory
5. Resources independently loadable
6. No circular references
7. Context budget ~300 lines

This checklist should be a standard step in the skill-creation pipeline, not an
afterthought.

---

## L10: The Skill-Creation Pipeline Is Itself a Reusable Artifact

The 7-phase workflow used to create this skill (design → write → progressive disclosure
→ registration → hub audit → self-audit → delivery) was extracted into a reusable
prompt at `~/.pi/agent/prompts/skill-create.md`. Any pi agent can follow it to produce
skills with the same quality level.
