---
name: "quality-plan-loop"
description: "Generar planes de calidad iterando planificador↔auditor con límites de convergencia (scope, budgets, stop conditions)."
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
---

# Bounded Plan Review Loop (QPL) — Ciclo de revisión iterativa de planes acotado

> **Autor:** Felipe Gonzalez (2026-08-02)
> **Principio rector:** un plan es "de calidad" cuando un auditor independiente verifica sus supuestos — no cuando el planificador lo declara completo. La calidad se DEMUESTRA, no se declara.
> **Límites de convergencia:** el ciclo es acotado por presupuestos y stop conditions explícitas para evitar bucles infinitos; no existe "convergencia garantizada" a priori.

## Cuándo usar

- Planes de arquitectura/implementación que van a ejecutar agentes (fases, gates, criterios de aceptación).
- Cambios con múltiples dependencias, contratos o restricciones duras (código congelado, dirs read-only).
- Cualquier plan donde un error de diseño costaría horas de ejecución (mejor pagar una breve pasada de auditoría que rehacer implementación).
- NO usar para: tareas triviales, cambios de una línea, o cuando el plan es ejecutable de inmediato sin riesgo.

## Arquitectura del ciclo

```
┌─────────────────────────────────────────────────────────────┐
│             BOUNDED PLAN REVIEW LOOP (QPL)                  │
│                                                             │
│  PLANIFICADOR (Agente planificador) AUDITOR INDEPENDIENTE   │
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
- **Planificador** (agente de planificación en contexto dedicado): produce `PLAN-vN.md`. Corrige SOLO los hallazgos de la última auditoría. Nunca reabre temas ya resueltos.
- **Auditor** (agente auditor independiente, **fresco por iteración**): produce `auditoria-vN.json` con veredicto. Verifica el plan contra el **código real** (no contra lo que el plan afirma).
- **Orquestador (tú, el agente principal)**: crea el contrato, lanza iteraciones, evalúa stop conditions, escala al humano. Es COORDINADOR, no ejecutor del contenido.

## 1. Preflight — Contrato del loop (obligatorio antes de iterar)

Crear `LOOP-CONTROL.md` en el directorio de trabajo con:

### Scope
- **In Scope**: iterar hasta APPROVE o límite de budget; artefactos `PLAN-vN.md` + `auditoria-vN.json` + contrato.
- **Out of Scope (hard stop)**: no reabrir trabajo ya cerrado; no ampliar alcance a features nuevas no pedidas por el auditor; no tocar código congelado/read-only.

### Budgets (límites duros)

| Recurso | Límite sugerido | Regla |
|---|---|---|
| Iteraciones máximas | 3-5 | Al agotarse sin APPROVE → escalar |
| Tamaño del plan | ≤ 20 KB / ~450 líneas | Criterio de concisión: no crecer indefinidamente |
| Tamaño del veredicto | ≤ 6 KB / ~80 líneas JSON | Salidas infladas = señal de ruido |
| Timeout auditor | 15 min / corrida | Evitar cuelgues de contexto saturado |

### Stop conditions (evaluadas en orden, DESPUÉS de cada auditoría)
1. **APPROVE** → fin del loop de revisión de calidad (significa que no restan bloqueos de diseño o inconsistencias detectadas; NO constituye autoridad autónoma para ejecutar mutaciones destructivas sin validación humana/orquestadora).
2. **Iteraciones agotadas** → STOP, escalar con tabla de hallazgos pendientes.
3. **Convergencia estancada**: 2 auditorías consecutivas con los MISMOS hallazgos no resueltos → STOP (problema estructural, no de edición).
4. **Budget de tamaño violado** → STOP, escalar.
5. **Presupuesto de tiempo/tokens excedido** → STOP, escalar.

## 2. Protocolo por iteración (orden fijo)

```
1. Auditor FRESCO (contexto limpio por corrida)
   → prompt con PLAN-vN + auditorías previas + reglas (ver plantilla)
2. Leer auditoria-vN.json (escrito a archivo, no impreso)
3. Evaluar stop conditions 1-5
4. Si REVIEW/REJECT y quedan iteraciones:
   Planificador ← brief con BLOCKs/WARNs de la auditoría vN
   → PLAN-v(N+1).md (verificar ≤ budget, verificar que corrige SOLO los hallazgos)
5. Registrar estado en registro de ejecución
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


