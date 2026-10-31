---
name: typography-scales-microtype
description: "Calcula escalas tipográficas (modulares o armónicas, con clamp() fluido) y microtipografía en CSS y Figma: interletrado, interlineado, medida de línea, alineación y jerarquía por contraste. Incluye comprobaciones pertinentes de WCAG 2.2 (1.4.4 y 1.4.12), sin inferir conformidad de los valores iniciales. Use when creating a type scale or setting font sizes, line-height, letter-spacing or fluid typography."
license: MIT
metadata:
  author: 'Felipe Gonzalez'
---

# Typography Scales & Micro-Typography

## Objective

Construir escalas tipográficas multi-dispositivo y parametrizar las propiedades micro-tipográficas (`line-height`, `letter-spacing`, `max-width` en `ch`, alineación, jerarquía por opacidad y variables en Figma/CSS), con valores iniciales adaptados al contenido, densidad y preferencias. Cuando aplique, comprobar el redimensionado y el espaciado real frente a WCAG 2.2 SC 1.4.4 Resize Text y SC 1.4.12 Text Spacing; las recetas por sí solas no demuestran conformidad.

## Inputs and Preconditions

- **Familias Tipográficas**: Fuentes `Display`, `Sans/Body` y `Mono` previamente definidas (o provenientes de `typography-selection-pairing` / `design-system/02-typography-selection.md`).
- **Contexto de Densidad**:
  - *Marketing / Editorial*: puede beneficiarse de mayor contraste entre titulares (`H1`) y cuerpo (`Body`).
  - *Product UI / Dashboard / Clínico*: puede requerir compresión controlada y alta densidad informativa sin perder jerarquía.
- **Dispositivos y preferencias**: Viewports relevantes, tamaño de texto del usuario, zoom y restricciones de contenido/plataforma si se conocen. Los tamaños de ejemplo no son breakpoints obligatorios.

## Workflow

### Fase 1: Cálculo de la Escala Tipográfica Multi-Modo

Elige una escala que responda al proyecto y al contenido; los tamaños y progresiones siguientes son recetas de partida que puedes adaptar. Para CSS web, `rem` y `clamp()` con componente en `rem` suelen facilitar que los tamaños respondan a preferencias de texto; elegir esas unidades no demuestra por sí solo cumplimiento.

1. **Arquitectura A - Escala Clásica Multi-Modo (un punto de partida posible)**:
   - La tabla siguiente ilustra una combinación Desktop (`1.25x`) y Mobile (`1.20x`) basada en `16px (1rem)`. Adáptala en lugar de tratarla como estándar para todo proyecto:

| Token Semántico | Rol en UI | Desktop (`1.25x`) | Mobile (`1.20x`) | `clamp()` Fluido (ejemplo `375px -> 1280px`) | `line-height` (inicial) | `letter-spacing` (inicial) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `--text-display` | Display / impacto, si aplica | `60px` (`3.75rem`) | `40px` (`2.50rem`) | `clamp(2.5rem, 1.98rem + 2.21vw, 3.75rem)` | `1.08` (`64px` / `44px`) | `-0.03em` |
| `--text-h1` | Título principal | `48px` (`3.00rem`) | `32px` (`2.00rem`) | `clamp(2rem, 1.59rem + 1.77vw, 3rem)` | `1.15` (`56px` / `36px`) | `-0.02em` |
| `--text-h2` | Título de sección | `36px` (`2.25rem`) | `28px` (`1.75rem`) | `clamp(1.75rem, 1.54rem + 0.88vw, 2.25rem)` | `1.20` (`44px` / `36px`) | `-0.015em` |
| `--text-h3` | Subtítulo / card | `28px` (`1.75rem`) | `24px` (`1.50rem`) | `clamp(1.5rem, 1.4rem + 0.44vw, 1.75rem)` | `1.28` (`36px` / `32px`) | `-0.01em` |
| `--text-h4` | Encabezado de grupo | `24px` (`1.50rem`) | `20px` (`1.25rem`) | `clamp(1.25rem, 1.15rem + 0.44vw, 1.5rem)` | `1.33` (`32px` / `28px`) | `-0.005em` |
| `--text-h5` | Subencabezado | `20px` (`1.25rem`) | `18px` (`1.125rem`) | `clamp(1.125rem, 1.07rem + 0.22vw, 1.25rem)` | `1.40` (`28px` / `24px`) | `0em` |
| `--text-body-lg` | Lead / intro | `18px` (`1.125rem`) | `16px` (`1.00rem`) | `clamp(1rem, 0.95rem + 0.22vw, 1.125rem)` | `1.55` (`28px` / `24px`) | `0em` |
| `--text-body` | Cuerpo estándar | `16px` (`1.00rem`) | `16px` (`1.00rem`) | `1rem` | `1.50` (`24px`) | `0em` |
| `--text-body-sm` | UI secundaria / tablas | `14px` (`0.875rem`) | `14px` (`0.875rem`) | `0.875rem` | `1.43` (`20px`) | `+0.005em` |
| `--text-caption` | Metadatos / badges | `12px` (`0.75rem`) | `12px` (`0.75rem`) | `0.75rem` | `1.33` (`16px`) | `+0.02em` |
| `--text-overline` | Eyebrow (`UPPERCASE`), si aporta información | `12px` (`0.75rem`) | `12px` (`0.75rem`) | `0.75rem` | `1.33` (`16px`) | `+0.08em` |

2. **Arquitectura B - Escala Armónica por Raíces de la Proporción Áurea (`phi = 1.618`)**:
   - Si encaja con un proyecto editorial o de marca, puedes probar desktop `sqrt(phi) = 1.272` y mobile `cuberoot(phi) = 1.174` como progresiones iniciales, no como una elección universal. Los tamaños de `references/scales-and-css-recipes.md` son aproximaciones con ajuste óptico, no redondeos exactos a una cuadrícula de `4px`; conserva los tamaños legibles de cuerpo y caption.
   - Consulta las tablas y fórmulas de interpolación `clamp()` en `references/scales-and-css-recipes.md`.

### Fase 2: Parametrización Micro-tipográfica en CSS

Usa estas pautas ópticas como valores de partida y adáptalas al tipo, tamaño, idioma y contenido:

1. **Letter-spacing (heurística tipográfica)**:
   - **Titulares grandes (`> 24px`)**: prueba *tracking* negativo (`-0.01em` a `-0.03em`) si mejora la forma de la fuente.
   - **Cuerpo (`14px - 18px`)**: el valor neutro (`0em`) es un punto de partida; comprueba la legibilidad.
   - **Mayúsculas / Overlines / Badges**: el *tracking* positivo (`+0.05em` a `+0.10em`) puede ayudar, pero no es obligatorio. Usa etiquetas solo si aportan información (categoría, estado, unidad), no en cada sección por defecto.
2. **Ratio inverso de `line-height` (pauta inicial)**:
   - Prueba valores menores para tipos grandes y mayores para texto corrido según tipografía y uso. Como rangos de partida, considera `1.05`–`1.15` para Display/H1, `1.20`–`1.30` para H2/H3 y `1.50`–`1.60` para Body. En particular, `1.5`–`1.6` para Body es una recomendación, no una prueba ni garantía de conformidad con SC 1.4.12.
3. **Medida de línea**:
   - `50ch`–`75ch` en desktop y `35ch`–`50ch` en mobile pueden servir como rangos orientativos para lectura. Ajusta `max-width` al contenido y al layout; titulares y otros bloques pueden necesitar otra medida.
   - `text-wrap: balance` en titulares y `text-wrap: pretty` en párrafos son opciones a probar.
4. **Alineación centrada**:
   - El centrado puede servir para titulares, subtítulos cortos o llamadas a la acción. Para bloques largos, compara alineación centrada con `start` y elige según legibilidad y patrón de lectura; tres líneas no es un umbral universal.
5. **Jerarquía por contraste (no solo tamaño)**:
   - Si el sistema usa niveles de luminancia, define tokens con colores efectivos y comprueba contraste pertinente. Valores ilustrativos: `--text-primary` `100%` (o `92%` en Dark Mode), `--text-secondary` `68%–75%`, `--text-muted` `48%–56%`; los porcentajes no garantizan por sí mismos una relación de contraste.

### Fase 3: Arquitectura de Variables Tipográficas en Figma y Código

1. **Alias de Familias (`base-font`)**: Los tokens alias como `font/family/sans`, `font/family/display` y `font/family/mono` pueden desacoplar componentes del nombre literal de una fuente.
2. **Vertical Trim (`Cap Height to Baseline` / `text-box-trim`)**: Si el proyecto y la herramienta lo admiten, evalúa *Vertical Trim* en Figma y `text-box-trim: trim-both; text-box-edge: cap alphabetic;` en CSS para ajustar cajas de texto.
3. **Paridad de Altura-x (`size-adjust`)**: Si el fallback difiere de la fuente web y el proyecto lo necesita, evalúa `size-adjust` en `@font-face`.

## Missing or Conflicting Information

- Si el usuario solicita texto pequeño para contenido legible, explica los posibles efectos sobre la legibilidad en el contexto y propone alternativas; no presentes `12px` como umbral normativo universal.
- Si el usuario pide tamaños en `px`, explica que `rem` o `clamp()` con componente `rem` suelen facilitar adaptación a preferencias, pero `px` no constituye automáticamente una violación de SC 1.4.4. Comprueba el comportamiento real de redimensionado/zoom aplicable en lugar de inferir conformidad por unidad CSS.

## Output Contract

Entrega una especificación de **Escala Tipográfica y Micro-tipografía** (`design-system/03-typography-scales.md`) que incluya, según el alcance:

1. **Tabla de Escala Tipográfica**: Tokens pertinentes con Desktop, Mobile, `clamp()`, `line-height`, `letter-spacing` y `font-weight` cuando correspondan; identifica valores como iniciales o decisiones contextualizadas.
2. **Bloque CSS de Variables y Clases**: Código de ejemplo con unidades y propiedades elegidas para el proyecto, y cualquier pauta de medida o jerarquía aplicada.
3. **Guía de Configuración en Figma**, si corresponde: Mapeo de colecciones multi-modo y opciones de Vertical Trim pertinentes.
4. **Checklist de Accesibilidad Tipográfica**: Qué se comprobó de SC 1.4.4 y/o 1.4.12, con resultado/evidencia; si no se ejecutaron pruebas, indícalo explícitamente.

## Common Mistakes

- **Usar solo `vw` en el término fluido de `clamp()` sin revisar preferencias**: Considera un término en `rem` para facilitar la respuesta al tamaño base. La unidad elegida no prueba por sí misma SC 1.4.4.
- **Aplicar el mismo `line-height: 1.5` a un H1 grande sin comprobar la composición**: Puede crear demasiado espacio entre líneas; ajusta al contenido y a la fuente.
- **Párrafos excesivamente anchos**: Una medida de lectura como `65ch` puede ser un punto de partida, pero adáptala a viewport, fuente y contenido.

## Verification

- [ ] Se registran unidades y escala elegidas para el contexto; `rem`/`clamp()` se consideran recomendaciones, no evidencia de conformidad.
- [ ] Los valores de letter-spacing, line-height y medida se adaptan al uso; `line-height: 1.5`–`1.6` no se toma como prueba de SC 1.4.12.
- [ ] Cuando aplica SC 1.4.12, se prueban simultáneamente los cuatro overrides (`line-height: 1.5`, espaciado entre párrafos `2em`, `letter-spacing: 0.12em`, `word-spacing: 0.16em`) y se comprueba en el renderizado que no se pierda contenido ni función. `min-height` puede ayudar, pero no basta; sin renderizador/evidencia del producto, el resultado es `NOT VERIFIED` y no se declara conformidad global.
- [ ] Cuando aplica SC 1.4.4, se comprueba el redimensionado/zoom al 200% en el producto pertinente y que el contenido no se pierda; no se infiere resultado solo de usar `rem` o `px`.
- [ ] Los checks no ejecutados quedan identificados como no verificados, no como conformes.
