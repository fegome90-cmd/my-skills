---
name: disenar-slides
description: Diseña, compone y revisa slides de calidad para decks web (React/HTML con CSS) con criterios explícitos de tipografía, color, grilla, espacio, jerarquía y movimiento mínimo, y deja evidencia medida con un script de Playwright. Úsala siempre que haya que crear una presentación o un deck, agregar o rediseñar una slide, mejorar el aspecto de una presentación existente, elegir fuentes, paleta, tamaños o layout para slides, ordenar la jerarquía entre títulos y texto, decidir animaciones de entrada o transiciones entre slides, o auditar un deck antes de proyectarlo, aunque el pedido no diga «diseño» (por ejemplo «arma la presentación de X», «esta slide se ve recargada», «haz que el deck se vea profesional»). Es agnóstica de marca; en el repo presentaciones-falp aplica el perfil FALP por defecto.
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
  origin: "fegome90-cmd/presentaciones-falp · .claude/skills/disenar-slides"
---

# Diseñar slides

Una slide no es una página web pequeña ni un documento: se lee de lejos, durante pocos segundos, mientras alguien
habla. Casi todas las decisiones de esta skill salen de esa condición: textos más grandes y cortos, una sola idea y
un solo foco por slide, contraste con margen para el proyector, y movimiento que solo orienta.

Las reglas tienen fuente y nivel de evidencia en [`references/fuentes.md`](references/fuentes.md). Las que vienen de
WCAG son requisitos; el resto son heurísticas de oficio con valores de partida. Cuando un valor no encaje con el
contenido, ajústalo y dilo; no lo cumplas a ciegas ni lo presentes como ley.

## Alcance

- **Sí**: decks web en React/HTML con CSS (por ejemplo, el repo presentaciones-falp: Next/vinext, `app/presentaciones/<slug>/`).
- **No**: `.pptx`, Google Slides o PDF como formato de origen. Si te piden eso, usa la skill correspondiente
  (`pptx`, `google-workspace`) y, si sirve, toma de aquí solo los criterios.

## Antes de empezar: el perfil de marca

Las reglas generales no fijan colores ni fuentes; los toma un **perfil**. En el repo presentaciones-falp el perfil por defecto es FALP:
lee [`perfiles/falp.md`](perfiles/falp.md) antes de escribir CSS. Si el deck es para otra marca o no tiene marca,
define un perfil nuevo con la plantilla del final de ese archivo (tokens con rol y descripción de uso) en vez de
dispersar valores sueltos por el código.

## Flujo

Sigue las etapas en orden. Cada una tiene una salida concreta; no pases a componer sin el guion.

### 1. Brief

Averigua (del pedido, del contenido o preguntando) y escribe en 5–6 líneas:

- **Audiencia y objetivo**: quién mira y qué debe decidir, entender o recordar al final.
- **Contexto de lectura**: proyector en sala iluminada, pantalla grande, notebook compartido o lectura posterior en
  móvil. Cambia el tamaño mínimo, el contraste y si conviene fondo claro u oscuro.
- **Duración y cantidad de slides**: como orientación, 1–2 minutos por slide de contenido.
- **Perfil de marca**.

Si falta algo que cambia el diseño (por ejemplo, si se proyecta), pregunta. Lo demás, asúmelo y decláralo.

### 2. Guion de títulos

Escribe primero la lista de slides **solo con sus títulos**, antes de cualquier diseño.

- Cada título es una **afirmación** completa («La lista de espera bajó 30 % con triage telefónico»), no un tema
  («Resultados»). Así la slide tiene una idea y el público la recibe aunque no lea el resto.
- **Prueba de los títulos**: leídos en orden, deben contar la historia completa. Si un título no aporta o repite,
  la slide sobra o se fusiona.
- Una idea por slide. Si una slide necesita dos títulos, son dos slides.

### 3. Patrón por slide

Asigna a cada slide un patrón de [`references/patrones.md`](references/patrones.md) (portada, sección, afirmación +
evidencia, dato grande, comparación, proceso, cita, imagen, diagrama, cierre). Varía los patrones a lo largo del deck
con propósito: el cambio de patrón señala un cambio de tipo de contenido. No repitas el mismo patrón más de tres
veces seguidas salvo que la serie sea intencional (por ejemplo, los pasos de un proceso).

### 4. Composición

Compón cada slide con estas referencias, en este orden, porque cada decisión condiciona la siguiente:

1. [`references/grilla-y-espacio.md`](references/grilla-y-espacio.md): lienzo, márgenes seguros, 12 columnas,
   ritmo de 8 y espacio vacío.
2. [`references/jerarquia.md`](references/jerarquia.md): niveles de texto, punto focal, presupuesto de palabras.
3. [`references/tipografia.md`](references/tipografia.md): escala para proyección, pares, interlineado, tracking.
4. [`references/color.md`](references/color.md): roles 60-30-10, un acento por slide, contraste con margen.

Escribe valores como tokens del perfil (variables CSS), nunca números sueltos repetidos en cada slide.

### 5. Movimiento

Lee [`references/movimiento.md`](references/movimiento.md). Por defecto, la slide entra con un fundido y un
desplazamiento corto, y nada más. Agrega un build progresivo solo cuando el orden de aparición es parte del
argumento.

### 6. Revisión

1. Levanta el deck (en presentaciones-falp, `npm run dev`; un HTML suelto se abre con `file://`) y ejecuta el script de
   revisión (ruta relativa a esta skill):

   ```bash
   node <ruta-de-la-skill>/scripts/revisar-slides.mjs \
     --url http://localhost:5173/presentaciones/<slug> --slides 0-7 \
     --out evidencia/slides/<fecha>-<slug>
   ```

   Captura cada slide a 1920×1080 y 1366×768 (y 390×844 si el perfil lo pide), y mide tamaño mínimo de texto,
   contraste, desbordes, largo de línea, niveles tipográficos, palabras por slide y animaciones (también con
   `prefers-reduced-motion`). Las opciones están en el encabezado del script. `evidencia/` no se versiona.
2. Mira las capturas tú mismo: el script no ve equilibrio, alineación óptica ni si el punto focal es el correcto.
   Haz la **prueba de entrecerrar los ojos** sobre cada captura (o mírala reducida): lo primero que se distingue
   tiene que ser lo más importante de la slide.
3. Recorre [`references/checklist.md`](references/checklist.md).
4. Corrige y vuelve a medir. Si algo no se pudo medir (texto sobre una imagen, por ejemplo), declara que
   quedó **sin medir** en vez de darlo por bueno.

## Entrega

Al terminar, informa en este formato:

```markdown
## Deck: <título>
- Perfil: <FALP | otro> · Slides: <n> · Contexto de lectura: <…>
- Guion de títulos: <lista numerada>
- Revisión automática: <errores / advertencias por slide, o "sin hallazgos">
- Sin medir: <lo que el script no pudo comprobar y por qué>
- Decisiones fuera de las reglas: <valor, motivo>
```

## Skills complementarias

Úsalas si están disponibles; esta skill no depende de ellas.

| Necesidad | Skill |
|---|---|
| Gráficos de datos dentro de una slide | `dataviz` (antes de escribir el gráfico) |
| Diagramas de proceso o arquitectura | `artifact-diagramming` |
| Auditoría de accesibilidad pedida explícitamente | `design:accessibility-review` |
| Crítica de diseño de una slide o captura | `design:design-critique` |
| Revisar textos, botones y microcopia | `design:ux-copy` |
| Guion, notas del orador y estructura del argumento | `scripting-technical-presentations` (este repo de skills) |
| Generar o analizar una paleta para un perfil nuevo | `color-theory-engine` (este repo de skills) |

## Convenciones del repo presentaciones-falp

Aplican solo cuando trabajas en [presentaciones-falp](https://github.com/fegome90-cmd/presentaciones-falp).

- Cada deck vive en `app/presentaciones/<slug>/` y se registra en `lib/presentations.ts`. La navegación usa
  fragmentos numéricos (`#0` portada, `#1…#n` slides) con `useNumericDeckHash`.
- Los tokens de marca y movimiento se generan en `registry/falp/themes/falp.css` desde
  `scripts/build-registry.mjs`. No edites el archivo generado: agrega tokens en el script y regenera.
- Las animaciones FALP viven en `registry/falp/themes/falp-motion.css` (única fuente de `@keyframes`).
- Valida con `npm test` (compila y corre `tests/*.test.mjs`) antes de entregar.
