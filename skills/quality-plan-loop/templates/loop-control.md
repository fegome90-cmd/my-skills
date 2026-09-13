# Plantilla LOOP-CONTROL.md

> Contrato de convergencia del ciclo de auditorías <ID>

## Scope

### In Scope
- Iterar planificador (GLM-5.2) ↔ auditor (GPT-5.6 Sol fresco) hasta APPROVE.
- Artefactos: `PLAN-<ID>-vN.md`, `auditoria-<ID>-vN.json`, este contrato.

### Out of Scope (hard stop)
- NO reabrir trabajo ya cerrado.
- NO ampliar alcance a features nuevas no pedidas por el auditor.
- NO tocar código congelado / dirs read-only.

## Budgets

| Recurso | Límite | Regla |
|---|---|---|
| Iteraciones máx | 3-5 | Al agotarse → escalar |
| Tamaño plan | ≤ 20 KB / ~450 líneas | No crecer |
| Tamaño veredicto | ≤ 6 KB JSON | No inflar |
| Costo máx | $8-12 | ~$1-2/iter |
| Timeout auditor | 15 min | Sol se cuelga >60% ctx |

## Stop conditions (orden)
1. APPROVE → FIN.
2. Iteraciones agotadas → escalar.
3. 2 auditorías con MISMOS hallazgos → escalar (estructural).
4. Budget tamaño violado → escalar.
5. Costo excedido → escalar.

## Protocolo por iteración
1. Auditor fresco (tab/pane nuevo).
2. Leer veredicto JSON.
3. Evaluar stop conditions.
4. Si REVIEW y quedan iteraciones → planificador produce v(N+1).
5. Registrar memoria + Engram.

## Bitácora

| Iter | Veredicto | BLOCKs nuevos | Decisión |
|---|---|---|---|
| #1 | | | |
