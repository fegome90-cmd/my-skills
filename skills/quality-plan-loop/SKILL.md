---
name: "quality-plan-loop"
description: "Generar planes de calidad iterando planificador↔auditor con límites de convergencia (scope, budgets, stop conditions)."
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
---

# Quality Plan Loop (QPL) — Generar planes de calidad con convergencia garantizada

> **Autor:** Felipe Gonzalez & PicoClaw (2026-08-02)
> **Proveniencia:** ciclo real planificador↔auditor que convergió PLAN-CIERRE-0B (8 iters → APPROVE) y PLAN-W1 (6 iters → APPROVE, 2/3 del presupuesto).
> **Principio rector:** un plan es "de calidad" cuando un auditor independiente lo aprueba — no cuando el planificador lo declara completo. La calidad se DEMUESTRA, no se declara.

## Cuándo usar

- Planes de arquitectura/implementación que van a ejecutar agentes (fases, gates, criterios de aceptación).
- Cambios con múltiples dependencias, contratos o restricciones duras (código congelado, dirs read-only).
- Cualquier plan donde un error de diseño costaría horas de ejecución (mejor pagar ~$1-2 de auditoría que rehacer implementación).
- NO usar para: tareas triviales, cambios de una línea, o cuando el plan es ejecutable de inmediato sin riesgo.

## Arquitectura del ciclo

```
┌─────────────────────────────────────────────────────────────┐
│                 QUALITY PLAN LOOP (QPL)                      │
│                                                             │
│  PLANIFICADOR (GLM-5.2)          AUDITOR (GPT-5.6 Sol)      │
│  ┌──────────────────┐            ┌──────────────────────┐   │
│  │ Lee hallazgos    │            │ Lee plan vN          │   │
│  │ Escribe PLAN-vN  │  ──►       │ Verifica vs código   │   │
│  │ (≤ budget)       │  prompt    │ real (no solo texto) │   │
│  └──────────────────┘            │ Escribe JSON veredicto│  │
│         ▲                        └──────────────────────┘   │
│         │  REVIEW/REJECT (hallazgos)                        │
│         └───────────────────────────────────────────────────│
│                                                             │
│  CONTRATO: LOOP-CONTROL.md (scope, budgets, stop conditions)│
│  ⛔ APPROVE → FIN · ⛔ stop condition → ESCALAR a humano     │
└─────────────────────────────────────────────────────────────┘
```

**Roles:**
- **Planificador** (GLM-5.2 vía herdr/opencode, pane dedicado): produce `PLAN-vN.md`. Corrige SOLO los hallazgos de la última auditoría. Nunca reabre temas ya resueltos.
- **Auditor** (GPT-5.6 Sol vía pi, **fresco por iteración**): produce `auditoria-vN.json` con veredicto. Verifica el plan contra el **código real** (no contra lo que el plan afirma).
- **Orquestador (tú, el agente principal)**: crea el contrato, lanza iteraciones, evalúa stop conditions, escala al humano. Es COORDINADOR, no ejecutor del contenido.

## 1. Preflight — Contrato del loop (obligatorio antes de iterar)

Crear `LOOP-CONTROL.md` en el directorio de trabajo con:

### Scope
- **In Scope**: iterar hasta APPROVE; artefactos `PLAN-vN.md` + `auditoria-vN.json` + contrato.
- **Out of Scope (hard stop)**: no reabrir trabajo ya cerrado; no ampliar alcance a features nuevas no pedidas por el auditor; no tocar código congelado/read-only.

### Budgets (límites duros, estilo gentle-ai SDD)

| Recurso | Límite sugerido | Regla |
|---|---|---|
| Iteraciones máximas | 3-5 | Al agotarse sin APPROVE → escalar |
| Tamaño del plan | ≤ 20 KB / ~450 líneas | Criterio sdd-propose: no crecer indefinidamente |
| Tamaño del veredicto | ≤ 6 KB / ~80 líneas JSON | Salidas infladas = señal de ruido |
| Costo máx | $8-12 por loop | ~$1-2 Sol + ~$0.1 GLM por iteración |
| Timeout auditor | 15 min / prompt | Sol con contexto >60% se cuelga |

### Stop conditions (evaluadas en orden, DESPUÉS de cada auditoría)
1. **APPROVE** → fin del loop, autorizada la ejecución del plan.
2. **Iteraciones agotadas** → STOP, escalar con tabla de hallazgos pendientes.
3. **Convergencia estancada**: 2 auditorías consecutivas con los MISMOS hallazgos no resueltos → STOP (problema estructural, no de edición).
4. **Budget de tamaño violado** → STOP, escalar.
5. **Costo excedido** → STOP, escalar.

## 2. Protocolo por iteración (orden fijo)

```
1. Auditor FRESCO (tab/pane nuevo, pi + gpt-5.6-sol)
   → prompt con PLAN-vN + auditorías previas + reglas (ver plantilla)
2. Leer auditoria-vN.json (escrito a archivo, no impreso)
3. Evaluar stop conditions 1-5
4. Si REVIEW/REJECT y quedan iteraciones:
   Planificador (GLM-5.2) ← brief con BLOCKs/WARNs de la auditoría vN
   → PLAN-v(N+1).md (verificar ≤ budget, verificar que corrige SOLO los hallazgos)
5. Registrar en memoria diaria + Engram (trayectoria + lección)
```

## 3. Reglas de oro (lecciones validadas en producción)

1. **Auditor fresco por iteración**: nunca reutilices el agente auditor de la iteración anterior (contexto >60% → se cuelga/encola). Tab y pane nuevos cada vez.
2. **Escribir a archivo, no imprimir**: pedir al agente que ESCRIBA el JSON/plan a archivo y responda SOLO la ruta. La UI de terminal intercala texto con salida.
3. **Verificar contra el código real**: el auditor debe leer `src/` (ledger.py, parser, runner) y comprobar las afirmaciones del plan. Un plan que afirma cosas falsas del código es REJECT automático.
4. **Comandos EXACTOS en los gates**: cada gate de cierre debe nombrar el comando/test que lo demuestra (`PYTHONPATH=src python3 -m ...`, `pytest -q tests/...`, `git diff --exit-code <commit> -- src/`). Un gate sin comando no es verificable.
5. **Quirúrgico en iteraciones avanzadas**: a partir de la 3ª iteración, pedir al auditor "sé quirúrgico: solo hallazgos que bloqueen ejecución o verificabilidad; no inventes hallazgos marginales". Esto acelera la convergencia.
6. **Trazabilidad de severidades**: cada versión del plan debe registrar el conteo CORRECTO de BLOCKs/WARNs previos y su estado (los auditores pueden discrepar en conteos — el planificador reconcilia).
7. **Nunca reabrir lo resuelto**: la vN+1 corrige solo los hallazgos de la vN. Reabrir temas cerrados = loop infinito.
8. **Panes herdr se pierden**: si el workspace colapsa (tabs cerrados), los agentes desaparecen. Recrear con el mismo patrón: `herdr tab create --cwd <dir> --label <x> --no-focus` → `herdr agent start <name> --kind opencode|pi --pane <ID> -- --model <...>`.

## 4. Formatos de artefactos

### PLAN-vN.md (estructura mínima)
```
# PLAN-<ID>-vN — <título>
> Base: <commit/versión> · Objetivo · Restricciones
## Cambios vs v(N-1) (respuesta a la auditoría #N — X BLOCKs + Y WARNs)
## Inventario / estado verificado
## ⚑ Decisiones (D1..Dn)
## Fases (P1..Pn) con comandos y criterios
## ⚑ Gate de cierre — matriz ejecutable (G1..Gn)
## Riesgos · Grafo de dependencias
```

### auditoria-vN.json (estructura mínima)
```json
{
  "veredicto": "APPROVE|REVIEW|REJECT",
  "resumen": "",
  "bloques_previos_resueltos": { "id": true|false },
  "warns_previos_resueltos": { "id": true|false },
  "regresiones_iteraciones_previas": [],
  "problemas_nuevos": [],
  "gate_cierre_ok": true|false,
  "veredicto_final": ""
}
```

## 5. Comandos operativos (herdr)

```bash
# Auditor fresco (por iteración)
herdr tab create --cwd <DIR> --label auditor-<id>-v<N> --no-focus
herdr agent start auditor-<id>-v<N> --kind pi --pane <PANE> --timeout 120000 -- --provider openai-codex --model gpt-5.6-sol
herdr agent prompt auditor-<id>-v<N> "$(cat /tmp/prompt.md)" --wait --timeout 900000

# Planificador
herdr agent start planner-<id>-v<N> --kind opencode --pane <PANE> --timeout 120000 -- --model zai-coding-plan/glm-5.2
herdr agent prompt planner-<id>-v<N> "$(cat /tmp/brief.md)" --wait --timeout 600000
```

## 6. Cierre

- Al APPROVE: actualizar bitácora del contrato, guardar memoria diaria + Engram, entregar `audit-pack/` (copia de todos los planes + veredictos + README índice) para revisión humana.
- La ejecución del plan aprobado es fase SEPARADA (W1-P1..Pn) — el loop solo garantiza la CALIDAD del plan, no su implementación.

## Ver también
- SDD gentle-ai: `~/Developer/gentle-ai/internal/assets/skills/sdd-propose/SKILL.md` (scope/budget)
- Wiki orquestación: `vault/orchestration-wiki/systems/tmux-plan-auditor.md` (auditoría paralela)
- Ejemplo real: `~/Developer/wiki-library/tools/wiki-validate/w1-audit-pack/`
