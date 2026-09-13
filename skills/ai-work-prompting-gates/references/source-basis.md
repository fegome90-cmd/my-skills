id: ai-work-prompting-gates-0.2
title: AI Work Prompting Gates · v0.2
version: "0.2"
type: method-note
project: ai-work-wiki
authority: PROPOSED
status: draft
document_tier: D1
migration_state: source-backed
canonical:
  control_plane: wiki
  content: editable-source
  pdf_generation: on-demand
artifact:
  kind: none
  role: no-release-artifact-required
relationships:
  governed_by:
    - ai-work-wiki-schema
  source_basis:
    relationship_resolution: non_governing_references_until_ids_resolve
    non_governing_references:
      - name: QUALITY-GATES-MINIMUM.md
        file_id: file_000000002a3c720eb3875642a50f8ece
        role: quality-gate-source
        resolution_status: filename_and_file_id_only_no_frontmatter_id_observed
      - name: pre-task-gates-exploration.md
        file_id: file_000000007328720e9943a69a7392fa63
        role: pre-task-gate-gap-analysis
        resolution_status: filename_and_file_id_reference
      - name: 11-proto-agentic-map.md
        file_id: file_00000000b6e4720ea374bc1e2de2ae79
        role: prompt-level-taxonomy
        resolution_status: filename_and_file_id_only_no_frontmatter_id_observed
      - name: AI Engineering.pdf
        file_id: file_00000000cca4720e9459760247cfc29a
        role: general-prompt-engineering-reference
        resolution_status: pdf-reference_not_formal_wiki_relation
freshness:
  depends_on_external_state: false
audit:
  baseline_status: reviewed
  baseline_result: pass_as_draft_blocked_for_promotion
  reviewed_at: 2026-08-13
  findings_open:
    - PG-20260813-001-tests-artifact-missing
    - PG-20260813-002-promotion-path-undecided
  findings_resolved:
    - PG-20260813-REL-uses-unresolved-converted-to-source-basis
    - PG-20260813-AUDIT-section-added
    - PG-20260813-GRAPHIFY-example-marked-non-authoritative
    - PG-20260813-LANG-policy-added
    - PG-20260813-AC-updated
lifecycle:
  promotion_state: not_promoted
  promotion_blockers:
    - executable_prompt_lint_not_created
    - target_library_path_not_decided
tags:
  - ai-work
  - prompting
  - gates
  - agent-workflows
  - draft

---

# AI Work Prompting Gates · v0.2

## Estado

Draft propuesto v0.2. Este documento no está activo ni promovido como norma de Library. Define un estándar de prompting con gates para tareas ejecutadas por agentes, especialmente cuando el agente opera sobre repositorios, archivos locales, automatizaciones, scripts, runners o pipelines.

No instala, ejecuta ni modifica ningún agente. No reemplaza métodos activos. No promueve componentes de Library. No convierte un prompt en enforcement real por sí mismo.

## Resultado de auditoría v0.2

Veredicto: PASS_AS_DRAFT / BLOCKED_FOR_PROMOTION.

Este documento puede usarse como borrador de trabajo y como plantilla local de prompting, pero no debe promocionarse como estándar canónico hasta cerrar los blockers de promoción.

## Propósito

Crear una plantilla mínima para prompts de agentes que reduzca tres fallas frecuentes:
1. Mezcla de audiencias: instrucciones para ChatGPT, para un agente local, para un repo o para una Library terminan dentro del mismo prompt.
2. Gates declarativos sin verificación: el prompt dice PASS, FAIL_ABORT o validar, pero no exige comando, archivo, exit code, artifact o evidencia reproducible.
3. Claims más fuertes que la evidencia: el agente declara "listo", "estable", "cerrado" o "seguro" sin demostrarlo.

Este documento convierte el prompting en un workflow L2: fases + gates + artifacts + validación, salvo que la tarea requiera explícitamente multi-rol, provenance pesada o investigación compleja.

## Principios

1. Separar audiencia antes de escribir el prompt
2. No mezclar autoridad, evidencia y ejecución
3. Preferir gates ejecutables sobre self-enforcement
4. Nivel de prompting por defecto: L0 Raw, L1 Structured, L2 Gated workflow (default para agentes locales), L3 Multi-role

## Plantilla base para prompts L2 gated workflow

# TASK
<Describe una tarea única, ejecutable y acotada.>

# CONTEXT
<Incluye solo contexto necesario para el agente. No incluyas reglas destinadas a ChatGPT si el destinatario es otro agente.>

# SCOPE
Allowed:
- <rutas, archivos, comandos, sistemas permitidos>
Forbidden:
- <rutas, archivos, comandos, sistemas prohibidos>
Out of scope:
- <trabajo que no debe hacer aunque parezca relacionado>

# AUTHORITY GATE
Before acting, identify:
- execution owner:
- decision owner:
- authoritative state/source:
- non-authoritative evidence surfaces:
Fail if authority is ambiguous or duplicated.

# RUNTIME DISCOVERY GATE
Verify before implementation:
- required binaries exist
- versions are captured
- required directories exist
- read/write permissions are valid
- required environment variables/secrets are present
- current baseline/state is recorded

# SECRET HANDLING GATE
Secrets must not be hardcoded, printed, committed, or written to logs. Fail closed if a required secret is missing.

# OWNERSHIP GATE
Exactly one component owns each state transition or output surface.

# LIFECYCLE / CRASH-SAFETY GATE
Define states: initial, in_progress, promoted/done, failed, rolled_back. Define lock/lease, stale lock policy, staging location, atomic promotion, rollback path.

# VALIDATION GATE
Define PASS in exact terms. Each PASS condition must map to evidence. Required: reproducible command(s), expected exit code(s), generated artifact(s), at least one boundary/failure case.

# DEGRADATION / REGRESSION GATE
Compare before/after. Block promotion if degradation exceeds threshold.

# OBSERVABILITY GATE
Each run/change must leave: run_id, started_at/finished_at, exit code, logs, summary artifact, before/after stats, diagnostic artifact.

# CLAIM DISCIPLINE GATE
The agent must not claim: stable, complete, closed, safe, production-ready, PASS unless the required evidence exists.

# DELIVERABLES
Return: plan summary, files changed, commands run, evidence artifacts, PASS/FAIL per gate, residual risks, decisions required.

## Adaptación para agente local del ordenador
Incluye LOCAL EXECUTION SCOPE, LOCAL PRE-FLIGHT GATE, STAGING GATE, PROMOTION GATE, ROLLBACK GATE, FINAL REPORT.

## Gate mapping rápido, Anti-patrones (4), Mini-checklist (9), Ejemplo aplicado Graphify
Ver fuente completa para detalles.
