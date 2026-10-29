---
name: ui-motion-and-handoff
description: "Especifica el movimiento de interfaz (curvas, resortes, duraciones, preferencia por transform/opacity y excepciones contextuales, prefers-reduced-motion), los estados de interacción y recuperación, el flujo widget-first, la poda anti-AI-slop y el contrato de entrega a desarrollo con accesibilidad WCAG 2.2. Use when designing UI animations, polishing AI-generated UI or preparing a developer handoff spec. Para una auditoría WCAG completa, usa una skill de auditoría de accesibilidad si está disponible."
license: MIT
metadata:
  author: 'Felipe Gonzalez'
---

# UI Motion Physics, Anti-Slop Distillation & Developer Handoff

## Objective

Especificar y auditar la capa final de ingeniería de interfaz: las propiedades y costos de renderizado del movimiento (principios de Emil Kowalski sobre curvas *cubic-bezier*, resortes físicos y composición), el Ciclo de Interacción y los 5 roles de *Affordance* (formulados por Rex Hartson y Pardha Pyla en *The UX Book*), el flujo de construcción *Widget-First*, la pasada de destilación contra *AI Slop* (maximizar la relación Señal-Ruido de William Lidwell) y el contrato de *Developer Handoff* y accesibilidad WCAG 2.2 (SC 2.3.3, 2.5.7, 2.5.8 y 4.1.2). No se infiere rendimiento, FPS ni uso de GPU sin medición.

## Inputs and Preconditions

- **Componentes y Layouts**: Estructura de pantalla y tokens provenientes de las fases anteriores o del código/prototipo a auditar.
- **Stack de Ejecución**: Motor de estilos y animación definido en `STACK.md` (CSS nativo, Tailwind, Motion/Framer Motion, SwiftUI, etc.).

## Workflow

### Fase 1: Física del Movimiento y Micro-Interacciones (Principios de Emil Kowalski)

El movimiento en una interfaz no es decoración; explica de dónde viene un elemento, a dónde va y confirma la acción del usuario:

1. **Selección de Curva según la Intención Física (evita `linear` para desplazamientos espaciales)**:
   - **Elementos que entran a la pantalla (`Enter` / `Ease-Out`)**: Deben arrancar con velocidad instantánea y frenar suavemente con fricción:
     - `--ease-out-quart`: `cubic-bezier(0.165, 0.84, 0.44, 1)` o `--ease-out-expo`: `cubic-bezier(0.16, 1, 0.3, 1)`.
   - **Elementos que se mueven o cambian de tamaño dentro de la pantalla (`Move / Morph` / `Ease-In-Out`)**:
     - `--ease-in-out`: `cubic-bezier(0.65, 0, 0.35, 1)`.
   - **Elementos que salen de la pantalla (`Exit`)**: `150ms - 180ms` con `ease-in` suave o `ease-out` rápido (las salidas pueden ser más rápidas que las entradas para no bloquear al usuario).
   - **Interacciones dirigidas por gestos o física real (`Springs`)**: Usa resortes sin rebote exagerado (`stiffness: 300-400, damping: 28-35, mass: 1` o amortiguamiento crítico $\zeta \approx 0.85 - 1.0`) para que la interfaz responda a la velocidad del gesto sin oscilar como un juguete.
2. **Presupuesto de Duración por Frecuencia de Uso**:
   - **Micro-feedback (`hover`, `active`, `toggle`, `button press`)**: `100ms - 160ms` (por ejemplo, `transform: scale(0.98)` en `:active`).
   - **Transiciones de componentes (`dropdown`, `tooltip`, `popover`, `toast`)**: `160ms - 220ms` (origen de escala `transform-origin` anclado al botón que lo abrió, empezando en `scale(0.95)` y nunca desde `scale(0)`).
   - **Transiciones de contenedores grandes (`drawer`, `modal`, `page view`)**: `240ms - 320ms`. **Regla**: Ninguna animación de interfaz productiva debe superar los **`350ms`**; si un usuario ejecuta una acción 50 veces al día, una animación de `600ms` se percibe como lentitud del sistema.
3. **Propiedades de Movimiento y Accesibilidad Vestibular (WCAG 2.2 SC 2.3.3)**:
   - **Prefiere `transform` (`translate3d`, `scale`, `rotate`) y `opacity` para movimiento espacial**. `background-color` y `box-shadow` pueden usarse como transiciones explícitas de feedback si aportan claridad; `clip-path` y `filter` son excepciones moderadas que requieren justificación y comprobación en el contexto objetivo.
   - Evita `transition: all`. No animes `width`, `height`, `top`, `left`, `margin` o `padding` por defecto: pueden provocar recálculos de layout. Declara las propiedades por interacción; no afirmes `60fps`, aceleración por GPU ni rendimiento mejorado sin medición representativa.
   - **Soporte de `@media (prefers-reduced-motion: reduce)`**: Cancela desplazamientos y escalas espaciales, incluido `scale()` de presión del botón. Conserva feedback no espacial apropiado, como cambios explícitos de color/sombra u opacidad; las reglas de opacity del popover deben eliminar su transform espacial.

### Fase 2: El Ciclo de Interacción de Hartson & Pyla y Flujo Widget-First

1. **Los 5 Roles de Affordance (Rex Hartson & Pardha Pyla)**:
   Toda acción del usuario atraviesa un ciclo cognitivo y físico que requiere estas **5 affordances**:
   - **1. Cognitive Affordance**: El diseño visual comunica claramente *qué es* el control antes de tocarlo (un botón parece presionable, un input parece editable).
   - **2. Physical Affordance**: El control es físicamente fácil de alcanzar y activar. Como criterio general de WCAG 2.2 SC 2.5.8 (AA), comprueba objetivo de `24x24px` CSS o las excepciones normativas aplicables (spacing, equivalent, inline, user-agent control y essential); no impongas 24x24 sin considerar excepciones. `44x44px` puede recomendarse por comodidad en mobile y corresponde a SC 2.5.5 (AAA), no a AA. Toda acción de arrastrar `drag-and-drop` debe tener una alternativa de clic simple por WCAG 2.2 SC 2.5.7.
   - **3. Sensory Affordance**: El control es perceptible visualmente y por lectores de pantalla (contraste, `aria-label`, `:focus-visible`).
   - **4. Functional Affordance**: El control ejecuta una función con propósito real para la tarea del usuario.
   - **5. Feedback & Recovery States**: Ninguna vista está terminada si solo existe el *Happy Path*. Debes diseñar explícitamente:
     - `Empty State` (Estado vacío con explicación y CTA de primer paso).
     - `Loading / Skeleton State` (Preservando las dimensiones exactas para `CLS = 0`).
     - `Partial / Truncated Data State` (Qué ocurre si un nombre tiene 80 caracteres o un número tiene 12 dígitos).
     - `Error & Recovery State` (Mensaje en lenguaje humano junto al campo afectado indicando qué ocurrió y cómo resolverlo sin perder los datos ingresados).
2. **Método de Generación "Widget-First" (4 Variaciones antes de ensamblar la Página)**:
   - Cuando diseñes una pantalla compleja con IA o en código, **no generes la página entera de un golpe** (eso produce componentes genéricos y superficiales).
   - Selecciona primero el **Widget Ancla** más importante de la vista (ej. la tarjeta de triaje clínico, el selector de precios o el panel de telemetría), explora **4 variaciones estructurales de ese widget aislado**, elige el ganador y construye el resto de la página alrededor de su gramática visual.

### Fase 3: Pasada de Destilación contra "AI Slop" y Contrato de Developer Handoff

1. **Protocolo de Destilación Anti-Slop (*Signal-to-Noise Ratio* de William Lidwell)**:
   Antes de entregar una interfaz, ejecuta esta poda sistemática cuando sea pertinente al brief y contexto:
   - [ ] **Gradientes Violeta-Cian genéricos y Orbes Flotantes sin función**: Evalúa si son decoraciones estereotipadas sin función; no los elimines si responden a una intención justificada.
   - [ ] **Cajas dentro de Cajas dentro de Cajas**: Si una tarjeta tiene borde, sombra, fondo gris y dentro otra sub-caja con borde para mostrar 2 datos, evalúa eliminar el contenedor intermedio y usar espaciado (`16px -> 32px`).
   - [ ] **Regla del 10% de Resaltado (*Highlighting*, William Lidwell)**: Si más del 10% de la pantalla está en negrita, con badges de colores, iconos parpadeantes o bordes de acento, evalúa la jerarquía; es una heurística, no un límite universal.
   - [ ] **Ornamento Tipográfico de Plantilla**: Revisa eyebrows en mayúsculas sobre cada sección, numeración `01 / 02 / 03` decorativa o énfasis cromático/cursivo sin función.
   - [ ] **Glassmorphism o Grano sin Función**: Evalúa si separan planos o expresan la marca definida en la dirección de arte.
   - [ ] **Copy Genérico**: Reemplaza el texto de relleno por lenguaje concreto y verificable del dominio (`CONTEXT.md`).
2. **Especificación de Developer Handoff y Semántica HTML/A11y (WCAG 2.2 SC 4.1.2)**:
   - **Distinción estricta `<button>` vs. `<a>`**:
     - Si cambia la URL, navega a otra página o ancla del documento → **`<a href="...">`** (permite *Cmd+Click / Abrir en nueva pestaña*).
     - Si ejecuta una acción en la vista actual (enviar formulario, abrir modal, filtrar, borrar, alternar tema) → **`<button type="button|submit">`** (nunca `<div onClick>`).
   - **Orden Lógico de Lectura por Bandas (`DOM Order === Visual Band Order`)**:
     - Anota el recorrido de `Tab` y lector de pantalla siguiendo bandas horizontales de izquierda a derecha y de arriba hacia abajo (`1 -> 2 -> 3`). Evita alterar con `order` de CSS o `position: absolute` la secuencia sin que el DOM coincida.
   - **Foco**: Distingue SC 2.4.7 Focus Visible y SC 2.4.11 Focus Not Obscured (Minimum), ambos AA, de SC 2.4.13 Focus Appearance (AAA). Comprueba el ocultamiento por contenido del autor cuando aplique; un outline aislado no demuestra por sí solo conformidad.

## Missing or Conflicting Information

- Si el usuario solicita animaciones complejas de entrada escalonada (*stagger*) en un dashboard operativo de uso intensivo, advierte que en herramientas de uso frecuente las animaciones de entrada repetitivas ralentizan el flujo de trabajo y recomienda reservar el movimiento para transiciones de estado funcionales (`< 200ms`).

## Output Contract

Entrega una especificación de **Motion, Anti-Slop y Developer Handoff** (`design-system/07-motion-and-handoff.md`) que incluya:

1. **Tabla de Tokens de Movimiento**: Curvas `--ease-out`, `--ease-in-out`, parámetros de `spring`, duraciones (`120ms`, `200ms`, `280ms`) y bloque CSS `@media (prefers-reduced-motion: reduce)`.
2. **Matriz de Estados del Ciclo de Interacción**: Especificación visual y funcional de `Default`, `Hover`, `Active`, `Focus-Visible`, `Disabled`, `Empty`, `Loading (Skeleton)` y `Error Recovery`.
3. **Reporte de Destilación Anti-Slop**: Lista de elementos decorativos o contenedores redundantes revisados y decisiones para maximizar la relación señal-ruido según el brief.
4. **Contrato Semántico y de Accesibilidad (Handoff)**: Mapa de etiquetas HTML (`<header>`, `<main>`, `<nav>`, `<section>`, `<button>` vs `<a>`), orden de tabulación, propiedades de movimiento por interacción y manejo de movimiento reducido. Verificar áreas táctiles según SC 2.5.8 y sus excepciones; 44x44 pertenece a SC 2.5.5 AAA. Separar los criterios de foco 2.4.7/2.4.11 AA de 2.4.13 AAA.

## Common Mistakes

- **Usar `transition: all 0.3s ease`**: Puede animar propiedades no previstas, incluidas propiedades de layout; declara propiedades explícitas y apropiadas para la interacción.
- **Escalar modales o popovers desde `scale(0)`**: Un elemento que crece desde `0` parece saltar desde la nada; inicia siempre desde `scale(0.95)` o `scale(0.96)` combinado con `opacity: 0 -> 1`.
- **Ocultar `outline: none` en `:focus` sin proporcionar `:focus-visible`**: Deja sin señal visual a los usuarios de teclado.

## Verification

- [ ] Para cada interacción se declaran las propiedades animadas: `transform`/`opacity` son preferidas para movimiento espacial; `background-color` y `box-shadow` pueden usarse como transiciones de feedback explícitas y `clip-path`/`filter` requieren justificación contextual. Evitar `transition: all`; no afirmar FPS/GPU sin medición.
- [ ] Bajo `prefers-reduced-motion` se cancelan traslación y escala espacial, incluido el estado `:active` del botón, y se conserva feedback no espacial apropiado.
- [ ] Se especificaron los 5 roles de affordance y los estados de recuperación (`Empty`, `Loading`, `Truncated`, `Error`) de Hartson & Pyla.
- [ ] Se ejecutó el checklist de destilación contra *AI Slop* según el brief, sin tratar porcentajes o preferencias estéticas como veto universal.
- [ ] Cada elemento interactivo especifica si es `<button>` o `<a>`, aplica el criterio de target size de 2.5.8 con sus excepciones y respeta el orden lógico de lectura en el DOM.
- [ ] Los checks de foco distinguen SC 2.4.7/2.4.11 (AA) de SC 2.4.13 (AAA); no se declara conformidad por un outline aislado.
