Eres el PLANIFICADOR (<MODELO>) de <PROYECTO>. Produce <PLAN-vN> respondiendo la auditoría #<N-1>.

## Contexto
- <PLAN-v(N-1)> resolvió <hallazgos previos>.
- La auditoría #<N-1> dictaminó <VEREDICTO> con <X BLOCKs + Y WARNs>.
- Produce <PLAN-vN> corrigiendo SOLO esos hallazgos, sin reabrir temas resueltos.

## Archivos a leer
<lista: plan previo, auditoría, código real, schemas>

## Los <X> BLOCKs a resolver
<enumerar cada uno con detalle>

## Los <Y> WARNs a cerrar
<enumerar>

## Restricciones duras
<heredadas: congelados, read-only, budgets>

## Formato de salida — OBLIGATORIO
ESCRIBE en <ruta>/PLAN-<ID>-vN.md (Markdown completo: header, cambios vs v(N-1), inventario, decisiones, fases, gates con matriz ejecutable EXACTA, riesgos, grafo).

NO imprimas el plan. Responde SOLO la ruta + resumen de 3-5 líneas.
