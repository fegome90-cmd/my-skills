# Ejemplo real: PLAN-W1 (wiki-validate, 2026-08-02)

## Trayectoria
| Iter | Auditor | Veredicto | Hallazgos | → |
|---|---|---|---|---|
| #1 | Sol | REVIEW | 9 | v2 |
| #2 | Sol | REVIEW | 6 BLOCKs + 4 WARNs | v3 |
| #3 | Sol | REVIEW | 2 BLOCKs + 4 WARNs | v4 |
| #4 | Sol (fresco) | REVIEW | 4 BLOCKs + 1 WARN | v5 |
| #5 | Sol (fresco) | REVIEW | 1 BLOCK (G7) | v6 |
| #6 | Sol (fresco) | APPROVE | 0 | ✅ |

## Datos clave
- Convergencia en 6 iteraciones (presupuesto 3 en el loop final — se usaron 2/3).
- Costo ≈ $8 total; plan final 19.8 KB.
- Gates: 7, todos con comandos exactos (runner, pytest, git diff, find, snapshot).
- Restricciones: src/ congelado (diff ∅ vs 77d0ff9), vault/ read-only, target sample-w1/.

## Lecciones confirmadas
1. Auditor fresco por iteración es OBLIGATORIO (Sol se cuelga con contexto >60%).
2. Escribir a archivo + responder solo ruta.
3. Verificar contra código real (ledger.py, ast_parser.py, runner.py).
4. Gates con comandos exactos desde la v1 evitan 2-3 iteraciones.
5. "Sé quirúrgico" en iteraciones avanzadas acelera APPROVE.
6. Los agentes herdr se pierden si el workspace colapsa → recrear con mismo patrón.

## Artefactos
`~/Developer/wiki-library/tools/wiki-validate/w1-audit-pack/` (README + 6 planes + 6 veredictos + contrato).
