---
name: ai-work-prompting-gates
description: "Use when authoring or reviewing agent prompts that need gated execution over repos, local files, runners or pipelines — especially when you need audience separation, executable gates (runtime discovery, staging/promotion/rollback, lifecycle/crash-safety) or to prevent PASS/stable/safe claims without evidence."
search_hints: prompting gates agent workflow L2 gated workflow runtime discovery staging promotion rollback claim discipline lifecycle crash-safety authority vs evidence
---

# AI Work Prompting Gates

Lightweight, searchable prompting standard for agent work. Optimized for `skill-hub` discoverability and governed card promotion — guidance checklist, not transactional enforcement. For crash-safe transactional enforcement, see the hardened variant.

> Source: `ai-work-prompting-gates-0.2` (method-note D1, PROPOSED/draft, audit 2026-08-13 PASS_AS_DRAFT/BLOCKED_FOR_PROMOTION). Only `ai-work-wiki-schema` is treated as governed; other references stay as source basis until IDs resolve.

## When This Skill Applies

- You need to write or audit an agent prompt that will operate on a repository, local files, scripts, runners or pipelines
- The prompt currently mixes ChatGPT consulting instructions with local-agent execution steps
- Gates say PASS/validate but don't name a command, exit code, or artifact
- The agent would be allowed to claim stable/safe/complete without showing logs or snapshots

Do **not** use for a plain ChatGPT answer with no tool execution, or for a trivial L0/L1 note/template with no state mutation.

## Current Contract You MUST Respect

### Searchable vs renderable

| State | Meaning | Cause |
|---|---|---|
| Searchable | `skill-hub "ai-work-prompting-gates"` finds it | Hub entry exists and sync indexed it |
| Renderable | `skill-hub --cards "gated workflow prompting for local agent automation"` promotes it | Description + source/path are complete enough for a governed card |

Do not assume both surfaces agree — searchable does not guarantee renderable.

### Authority rules

- Do not hand-edit `skills_manifest.json` or `_ctx/context_pack.json` — they are downstream runtime state.
- The operator flow is: **source SKILL.md → managed hub entry → sync → verify**.
- If you change name/description, refresh the hub entry via the managed helper, do not patch the manifest.

## Workflow Overview

| Level | Use | When |
|---|---|---|
| L0 Raw | Texto simple | Mensajes sin ejecución |
| L1 Structured | Pasos + output | Revisión simple sin riesgo |
| **L2 Gated workflow** | **Fases + gates + artifacts** | **Default para agentes locales: automatizaciones, scripts, runners, auditorías** |
| L3 Multi-role | Roles + provenance | Investigación compleja / adversarial |

Default for local agents: **L2**.

### Audience separation at a glance

| Audience | Receives | Must NOT receive |
|---|---|---|
| ChatGPT consultor | Encuadre, método, criterios de revisión | Instrucciones operativas del agente local |
| Agente local | Tarea ejecutable, rutas, comandos, gates, artifacts | Correcciones a ChatGPT |
| Repo/backend | Contratos de estado, scripts, tests, rollback | Governance sin enforcement |
| Library | Fuente, estado, autoridad, relaciones, auditoría | Suposiciones de runtime no verificadas |

> Rule: if a line exists only to prevent a ChatGPT mistake, it does not belong in the local-agent prompt.

## Recommended Flow

### Phase 1: Fetch

Copy the source prompt or method note into your working area. Identify the canonical `SKILL.md` you will deliver.

### Phase 2: Analyze

Validate: `SKILL.md` exists + YAML frontmatter valid, `name` is lowercase-hyphenated, `description` is specific and action-oriented (starts `Use when...`), no secrets or junk artifacts, not so bloated it needs extraction.

### Phase 3: Refactor

If too large: keep `SKILL.md` as orchestration entrypoint; move deep gate details into `resources/` or `references/`.

### Phase 4: Agnosticize

Neutralize vendor/harness-specific branding when it reduces reuse. Keep real constraints accurate — do not genericize away security or scope limits.

### Phase 5: Optimize Frontmatter for Search AND Cards

- `description` states when to use + when NOT to use, concrete enough to survive card promotion
- `search_hints` include realistic synonyms a user would type
- No placeholder like "Helper skill"

### Phase 6: Register via Skill Onboarding

Register or refresh the skill entry following the canonical onboarding workflow (see `skills/skill-onboarding`):

```bash
# Verify skill discovery and frontmatter validity
skill-hub "<skill-name>"
```

What it does: validates frontmatter → ensures canonical source directory placement → verifies exact-name discovery and card promotion.

### Phase 7: Verify Search (exact-name first)

```bash
skill-hub "ai-work-prompting-gates"
```

Proves searchable on the default path. Check `Source` + `Path` in the result — ensure it points to the intended runtime copy.

### Phase 8: Verify Cards (realistic query only)

```bash
skill-hub --cards "gated workflow prompting for local agent automation"
```

Do not use a vague query and conclude registration is broken. Cards require meaningful metadata — if description is empty/truncated to `>`, you'll be searchable but not renderable (fix source → re-register → sync).

## L2 Gated Template (Concise)

```markdown
# TASK — single bounded executable task
# CONTEXT — only context for THIS agent
# SCOPE — Allowed / Forbidden / Out of scope
# AUTHORITY GATE — execution owner, decision owner, authoritative source, evidence surfaces
# RUNTIME DISCOVERY GATE — binaries, versions, dirs, permissions, secrets, baseline (with command outputs)
# SECRET HANDLING GATE — fail closed if missing, never log
# OWNERSHIP GATE — one owner per state surface
# LIFECYCLE GATE — initial/in_progress/promoted/failed/rolled_back + lock/lease + staging + rollback
# VALIDATION GATE — PASS in exact terms → evidence (commands, exit codes, artifacts, boundary case)
# DEGRADATION GATE — before/after thresholds
# OBSERVABILITY GATE — run_id, timestamps, exit code, logs, stats, diagnostic artifact
# CLAIM DISCIPLINE GATE — never claim PASS/stable/safe without evidence; per claim report evidence + residual risk
# DELIVERABLES — summary, files changed, commands run, artifacts, PASS/FAIL per gate, risks, decisions
```

See `resources/l2-template.md` for the full expanded template and `resources/anti-patterns.md` for the 4 canonical anti-patterns with corrections.

## Local Adaptation Snippet

> When the agent runs locally (cron, runner, worktree): scope to explicit repo/log/config paths, pre-flight `pwd → git root → clean/dirty → binaries with absolute paths → versions → scheduler → config → secrets → disk → permissions`, write every run to `staging/<run_id>/` first, promote only after validation PASS with snapshot + before/after stats, rollback restores all coupled artifacts.

## Anti-Patterns (at a glance)

| Anti-pattern | Correction |
|---|---|
| Gate without mechanism ("Validate everything") | `Run <command>. PASS only if exit code = 0 and <artifact> contains <condition>.` |
| Audience mixing | Split: `[ChatGPT analyst] Treat as local automation...` vs `[Local agent] Implement runner with gates...` |
| Strong claim without evidence ("System is stable") | `Observed PASS: <command> <exit> <artifact>. Not proven: crash recovery under power loss. Residual: <risk>.` |
| Implicit staging ("Generate the graph") | `Generate into staging/<run_id>. Promote only after validation PASS.` |

## Mini-Checklist Before Sending a Prompt

- [ ] Real recipient declared?
- [ ] Allowed/forbidden/out-of-scope clear?
- [ ] Single authority for go/no-go?
- [ ] Logs/tests treated as evidence not authority?
- [ ] Every gate has concrete evidence (or marked weak/self-enforced)?
- [ ] Staging exists if persistent state is written?
- [ ] Rollback exists if promotion/mutation happens?
- [ ] Crash-safety specified or declared as residual risk?
- [ ] PASS without evidence prohibited?

## Common Mistakes

- Assuming `skill-hub --cards` is the registration check (exact-name search is).
- Assuming searchable → renderable (cards need complete description/source/path).
- Hand-editing manifest/catalog instead of re-running the managed helper.
- Verifying cards with a query no real user would type.
- Overwriting an unmanaged hub entry without checking ownership.
- Keeping a vague description that blocks safe card promotion.

## Done Criteria

You are done only when: source SKILL.md valid, skill lives in intended root, managed hub entry refreshed, `skill-hub "ai-work-prompting-gates"` finds it, and if cards were in scope that `skill-hub --cards` promotes it under a realistic query, with manifest count consistent.

## Governance Note
 
This skill provides the lightweight specification and execution gates for prompt engineering in automated and agentic workflows. For multi-role adversarial reviews, combine with `learned-structured-review` and `learned-accuracy-fallacy-audit`.
