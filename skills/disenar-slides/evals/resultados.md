# Resultados de evaluación

## Iteración 1 · 2026-10-19

Tres casos de `evals.json`, cada uno ejecutado con la skill y sin ella (agentes independientes), y calificados con
`scripts/revisar-slides.mjs` a 1920×1080 y 1366×768 más chequeos de código (12 por deck).

| Caso | Con skill | Sin skill | Qué falló sin skill |
|---|---|---|---|
| 1 · Deck FALP para el comité de calidad | 12/12 | 7/12 | Contenido cortado a 1366×768 (lienzo fijo sin escalar), 8 tamaños de texto en una slide, 82 palabras en otra, texto de 17 px, desplazamientos con movimiento reducido |
| 2 · Rediseñar una slide recargada | 12/12 | 10/12 | Cifra principal con contraste 2,36:1; 5 tamaños de texto |
| 3 · Charla en meetup, sala oscura | 12/12 | 11/12 | 5 tamaños de texto |

Total: 100 % con skill, 78 % sin skill.

Límites de esta medición:

- Las ejecuciones con skill podían correr el script de revisión y corregirse; las de referencia no. Parte de la
  diferencia viene de eso.
- A 1920×1080 ambas versiones se ven bien; las diferencias aparecen en otros viewports, contraste y detalle.
- Sin datos de tiempo ni tokens: un límite de API interrumpió las ejecuciones y se retomaron.
- Una sola ejecución por configuración; no hay varianza.

Cambio derivado: el selector por defecto del script tomaba la primera slide oculta en decks que marcan todos los
`<article>` con `data-slide`. Corregido: ahora prueba cada selector en orden y usa el primer elemento visible.
