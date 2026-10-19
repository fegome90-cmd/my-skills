# Checklist de revisión

Recorre la lista sobre las capturas y el informe del script. La columna «Cómo» dice si lo mide el script (**auto**)
o si hay que mirarlo (**ojo**). Lo que no se pudo verificar se reporta como «sin medir».

## Deck

| # | Criterio | Cómo |
|---|---|---|
| D1 | Leídos solos y en orden, los títulos cuentan la historia completa | ojo |
| D2 | Un solo modo (claro u oscuro), salvo separadores deliberados | ojo |
| D3 | Máximo dos familias tipográficas y tres pesos en todo el deck | auto (familias) + ojo |
| D4 | Los mismos roles se ven iguales en todas las slides | ojo |
| D5 | Todos los valores salen de tokens del perfil; no hay colores, tamaños ni duraciones sueltos repetidos | revisión de código |
| D6 | Navegación por teclado (→ ← Inicio Fin) y foco visible en los controles | ojo |

## Slide

| # | Criterio | Umbral de partida | Cómo |
|---|---|---|---|
| S1 | Título es una afirmación, máximo 2 líneas | — | ojo |
| S2 | Un solo punto focal; pasa la prueba de entrecerrar los ojos | — | ojo |
| S3 | Ningún texto bajo el mínimo | 1/60 del alto (18 px a 1080); 12 px en móvil vertical | auto |
| S4 | Contraste de texto | WCAG 4,5:1 normal, 3:1 grande; objetivo 7:1 | auto (fondos sólidos y degradados) |
| S5 | Máximo tres tamaños de texto (más etiqueta) | ≤ 4 tamaños distintos | auto |
| S6 | Palabras visibles | aviso sobre 60 | auto |
| S7 | Largo de línea del cuerpo | ≤ ~60 caracteres | auto (estimado) |
| S8 | Nada se desborda ni se corta; nada sale del área segura | — | auto (desbordes) + ojo (márgenes) |
| S9 | Máximo cuatro bloques por fila | — | ojo |
| S10 | Distancia entre grupos claramente mayor que dentro del grupo | — | ojo |
| S11 | El acento aparece en un solo lugar | — | ojo |
| S12 | El color no es la única señal de ningún estado o categoría | — | ojo |
| S13 | Texto sobre imagen tiene capa de protección | — | ojo (el script lo marca «sin medir») |
| S14 | Alineación a un eje; alineación óptica de números e iconos | — | ojo |

## Movimiento

| # | Criterio | Cómo |
|---|---|---|
| M1 | Solo `opacity` y `transform` animan en entradas; sin `transition: all` | auto (animaciones) + código |
| M2 | Ninguna animación supera 400 ms ni es infinita | auto |
| M3 | Con `prefers-reduced-motion` no queda desplazamiento, pero sí fundido | auto |
| M4 | Elementos no interactivos no reaccionan al hover | ojo |
| M5 | Diez avances rápidos seguidos no se sienten lentos | ojo |

## Viewports

- Siempre 1920×1080 y 1366×768.
- Si el perfil es responsivo (FALP), también 1024×600 y 390×844 (`--viewports` del script).
