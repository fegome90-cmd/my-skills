---
disable-model-invocation: true
name: wiki-keeper
description: "Fachada y router del pipeline decomposed F0-F7 (wiki-pipeline-orchestrator). Enruta triggers (create wiki, maintain wiki, lint wiki, ingest into wiki, wiki keeper, wiki health) a la fase correspondiente y sirve como indice de referencia para el Wiki Registry y Resources compartidos."
search_hints: wiki knowledge base documentation lint ingest karpathy create maintain health check fachada router orchestrator pipeline decomposed
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "2.0.0"
  triggers:
    - "create wiki"
    - "maintain wiki"
    - "lint wiki"
    - "ingest into wiki"
    - "wiki keeper"
    - "wiki health"
  role: fachada
  scope: documentation
---

# Wiki Keeper (Fachada / Router)

> **v2.0.0 — Skill fachada.** Enruta triggers historicos de wiki (`create wiki`, `maintain wiki`, `lint wiki`, `ingest into wiki`, `wiki keeper`, `wiki health`) al orquestador [`wiki-pipeline-orchestrator`](../wiki-pipeline-orchestrator/) y a las skills de fase F0–F7 del pipeline decomposed. Mantiene el [Wiki Registry](#wiki-registry-active-wikis) y la tabla de [Resources](#resources) como indice de referencia compartido.

---

## Cuando usar esta skill

- Enrutar cualquier comando de ciclo de vida de wiki al orquestador o fase especializada.
- Consultar el [Wiki Registry](#wiki-registry-active-wikis) para resolver la ubicacion y alcance de las wikis del workspace.
- Acceder a los [Resources](#resources) compartidos (plantillas, metodologia, schema, checklist de lint).

## Cuando delegar a otra skill

- **Ejecutar fases del pipeline:** Carga [`wiki-pipeline-orchestrator`](../wiki-pipeline-orchestrator/) o la skill de fase correspondiente (`wiki-f0-intake` ... `wiki-f7-lint`).
- **Integrar y escribir paginas:** Carga F5 ([`wiki-f5-integrate`](../wiki-f5-integrate/)).
- **Extraer atomics desde fuentes:** Carga F3 ([`wiki-f3-extract`](../wiki-f3-extract/)).
- **Promocion transaccional de lotes:** Ejecuta el runner operacional ([`batch_runner.py`](../../scripts/batch_runner.py) / [`wiki_batch_caller.py`](../../scripts/wiki_batch_caller.py)).

---

## Trigger Routing (fachada)

Enruta cada trigger al orquestador o a la fase correspondiente segun el contrato del pipeline decomposed:

| Trigger | Skill delegada | Fase / Comando |
|---------|----------------|----------------|
| `create wiki` | `wiki-pipeline-orchestrator` | `start` (inicia nuevo `run_id`, fase F0 intake) |
| `maintain wiki` | `wiki-pipeline-orchestrator` | `start` / `resume {run_id}` |
| `ingest into wiki` | `wiki-pipeline-orchestrator` → F0 (`wiki-f0-intake`) | intake — inicia nuevo `run_id` |
| `lint wiki` | `wiki-pipeline-orchestrator` → F7 (`wiki-f7-lint`) | lint-promoter (gate G7) |
| `wiki keeper` | esta skill (fachada) | consulta de referencia a Wiki Registry / Resources |
| `wiki health` | `wiki-pipeline-orchestrator` → F7 (`wiki-f7-lint`) + G9 | health check y diagnostico de observabilidad |

### Reglas de Enrutamiento:

1. **Delegacion via orquestador:** Toda transicion de estado y handoff se gestiona a traves del orquestador del pipeline; los estados observables se preservan en `vault/.runs/{run_id}/handoffs/inbox/{new,in_process,completed,failed}/`.
2. **Respuesta guia:** Ante cualquier trigger de ejecucion, responde indicando la skill delegada y el comando correspondiente sin ejecutar logica inline.
3. **Reanudacion determinista:** Para reanudar un run en estado `awaiting-human` (gate G4), ejecuta `wiki-pipeline-orchestrator resume {run_id}` preservando el identificador del lote.

---

## Protocolos Removidos (Migracion v1.7.0 → v2.0.0)

Las siguientes secciones del antiguo monolito v1.7.0 migraron a fases dedicadas del pipeline decomposed. Si un agente solicita invocarlas, responde con la guia de delegacion:

| Protocolo removido (v1.7.0) | Migrado a | Mensaje guia |
|------------------------------|-----------|--------------|
| `wiki-keeper capture-from-web` | F0 intake + F1 search (`wiki-f0-intake`, `wiki-f1-search`) | "Capture-from-web fue removido de wiki-keeper. Usa `wiki-pipeline-orchestrator start` con el source; F0+F1 se encargan." |
| `wiki-keeper extract` | F3 extract (`wiki-f3-extract`) | "Extract fue removido. Usa `wiki-pipeline-orchestrator` → F3 para extraer atomics en `vault/.runs/{run_id}/atomics/`." |
| `wiki-keeper ingest` | F0+F5 (`wiki-f0-intake`, `wiki-f5-integrate`) | "Ingest fue removido. Inicia un run con `wiki-pipeline-orchestrator start` (F0 intake); F5 integra." |
| `wiki-keeper lint` | F7 lint (`wiki-f7-lint`) | "Lint fue removido. Usa `wiki-pipeline-orchestrator` → F7 (gate G7)." |
| `wiki-keeper eval-loop` | validador constitution + CI | "Eval loop fue removido. La validacion corre via `wiki-constitution-validate` en pre-commit/CI sobre los 4 archivos constitution + 3 fixtures." |

---

## Wiki Registry (Active Wikis)

> ⚠️ **DEPRECADO como SSOT (2026-08-16):** el registro canónico es ahora **`WIKIS.md` v2** (root del workspace) — fuente única de rutas, dominios, keywords y estado para las 9 wikis W0–W8 (incluye OpenClaw nativa W0, constitución-ai W7 y pi-llm-wiki W8). Esta tabla se conserva como referencia histórica (conteos 2026-08-07/15) y NO se actualiza; ante cualquier divergencia gana `WIKIS.md` v2. Ver también skill `wiki-reader` (capa de lectura read-only con progressive disclosure).

> ℹ️ **Reference-only** — Índice consultado por skills F0–F7 como Single Source of Truth (SSOT) de wikis en el workspace.

| # | Wiki | Root Path | Pages | Scope | Keywords | Schema | Last Audit |
|---|------|-----------|-------|-------|----------|--------|------------|
| W1 | Wiki Oncológica | `~/Developer/examen_grado/vault/wiki/` | 124 | Enfermedades, tratamientos, conceptos oncológicos (FALP) | cancer, tumor, TNM, quimio, radio, FALP, oncológico | WIKI-SCHEMA.md | 2026-08-11 (108/124 PMID) |
| W2 | Wiki Orquestación | `~/Developer/examen_grado/vault/orchestration-wiki/` | 75 | Patrones de agentes, sistemas, conceptos, pi_systems | orquestación, patterns, CLOOP, handoff, agents, runner | WIKI-SCHEMA.md | 2026-08-15 |
| W3 | ~~Paperclip Wiki~~ | `~/Developer/examen_grado/vault/paperclip-wiki/` | 43 | **ARCHIVED** — integracion paperclip historica | paperclip, integración | WIKI-SCHEMA.md | — |
| W4 | TQT App Wiki | `~/Developer/tqt_app/docs/wiki/` | 129 | Voice banking, guias FALP, arquitectura, diseno clinico | tqt, voice banking, VB, voice cloning, FALP flujo, care phases | WIKI-SCHEMA.md | 2026-08-07 |
| W5 | Constitución AI | `~/Developer/constitucion-ai/constitution/` | 1 | Marco normativo agentico (13 leyes, anexos, glosario) | constitución, leyes, agentic constitution, normativa | (single file) | — |
| W6 | Wiki Library (multi) | `~/Developer/wiki-library/` | 5 wikis | Indice maestro + sub-wikis tematicas (altas-capacidades, oncologia, etc.) | wiki-library, altas-capacidades, research-methodology | WIKI-SCHEMA.md | 2026-08-07 |

### Reglas del Registry:
1. **Resolucion de topico:** Consultar la columna Keywords y TOOLS.md para mapear el dominio antes de iniciar un run.
2. **Alta de wiki:** Agregar la fila correspondiente en este registro y en `WIKIS.md`.
3. **Baja o archivo:** Marcar la wiki como ARCHIVED sin eliminar el historial.
4. **Referencias cruzadas:** Utilizar la sintaxis `[[wiki-name:page-name]]` para enlazar entidades entre wikis.
5. **Aislamiento externo:** W4, W5 y W6 son de solo lectura dentro del workspace `examen_grado` salvo autorizacion expresa.

---

## Resources

> ℹ️ **Reference-only** — Indice de plantillas, metodologias y checklists consumidos por las skills de fase F0–F7 via `[[wiki-keeper:resources/<file>]]`.

| Recurso | Descripcion y Proposito |
|---------|-------------------------|
| → [[resources/methodology]] | Patron Karpathy, arquitectura de 3 capas y flujos de trabajo. |
| → [[resources/schema-template]] | Plantilla reutilizable para `WIKI-SCHEMA.md`. |
| → [[resources/ingest-protocol]] | Especificacion de ingesta estructurada por tipo de fuente. |
| → [[resources/lint-checklist]] | Checklist exhaustivo de reglas y severidades para fase F7. |
| → [[resources/examples]] | Ejemplos de referencia reales extraidos de wikis operativas. |
| → [[resources/entity-templates]] | Plantillas estandarizadas de frontmatter por tipo de entidad. |
| → [[resources/anti-patterns]] | Catalogo de antipatrones de mantenimiento (A1–A6). |
| → [[resources/core-protocols]] | Convenciones de inicializacion, consultas y schemas. |
| → [[resources/memory-wiki-integration]] | Capa de validacion de memoria persistente. |

---

## Pipeline reference (delegacion)

La ejecucion completa reside en el pipeline decomposed F0–F7 y en el motor operacional transaccional:

- **Orquestador (F0–F7):** [`wiki-pipeline-orchestrator`](../wiki-pipeline-orchestrator/SKILL.md) — Gestiona las transiciones del FSM, gates G0–G9 y suspension en G4 (`awaiting-human`).
- **Motor Transaccional (ADR 0003):** [`scripts/batch_runner.py`](../../scripts/batch_runner.py) / [`scripts/wiki_batch_caller.py`](../../scripts/wiki_batch_caller.py) — Ejecuta concurrencia segura con `batch.lock` (flock), verificacion CAS con SHA-256 tree digests, aislamiento estricto de Git y gobernanza de promocion (`shadow` $\rightarrow$ `supervised` $\rightarrow$ `automatic`).
- **Skills de Fase:**
  [`wiki-f0-intake`](../wiki-f0-intake/SKILL.md) ·
  [`wiki-f1-search`](../wiki-f1-search/SKILL.md) ·
  [`wiki-f2-verify`](../wiki-f2-verify/SKILL.md) ·
  [`wiki-f3-extract`](../wiki-f3-extract/SKILL.md) ·
  [`wiki-f4-review`](../wiki-f4-review/SKILL.md) ·
  [`wiki-f5-integrate`](../wiki-f5-integrate/SKILL.md) ·
  [`wiki-f6-audit`](../wiki-f6-audit/SKILL.md) ·
  [`wiki-f7-lint`](../wiki-f7-lint/SKILL.md).
- **Constitution:** [`wiki-pipeline-orchestrator/constitution/`](../wiki-pipeline-orchestrator/constitution/) (`00-priority.md`, `01-states.md`, `02-taxonomy.md`, `03-permissions.md`).
- **Staging Aislado:** `vault/.runs/{run_id}/` — Area efimera donde se ensamblan los borradores y handoffs antes de la promocion transaccional.
