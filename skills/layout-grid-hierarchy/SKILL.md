---
name: layout-grid-hierarchy
description: "Diseña la estructura espacial de una pantalla según su contenido: selecciona una grilla, espaciado, catálogo de 25 patrones de layout, jerarquía visual y squint test contextual. Use when designing a page layout, grids and spacing, visual hierarchy, bento grids, or adapting desktop layouts to mobile."
license: MIT
metadata:
  author: 'Felipe Gonzalez'
---

# Layout, Adaptive Grid & Visual Hierarchy

## Objective

Estructurar el espacio, las rejillas y la jerarquía visual a partir del contenido, tarea, dispositivos y densidad del proyecto. La rejilla `12-8-4`, el sistema espacial de `8pt`, los breakpoints y los patrones de este documento son presets para elegir y adaptar, no requisitos universales. El catálogo de **25 patrones** y las leyes perceptuales de la Gestalt (sistematizadas en *Universal Principles of Design* de William Lidwell) sirven como recursos de diseño; usa el *Squint Test* como heurística cuando sea pertinente.

## Inputs and Preconditions

- **Inventario de Contenido**: Bloques funcionales, secciones o componentes que debe alojar la pantalla (provenientes de `PRODUCT.md` o del wireframe/prompt).
- **Dispositivos Objetivo**: Viewports y plataformas pertinentes al encargo; los rangos Desktop/Tablet/Mobile de los ejemplos son puntos de partida, no breakpoints obligatorios.
- **Nivel de Densidad**: Considera el tipo, volumen y prioridad de contenido; no presupongas porcentajes fijos de espacio negativo ni densidad.

## Workflow

### Fase 1: Selección de Grilla y Sistema Espacial

1. **Elige columnas, breakpoint, gutter, márgenes y contenedor según el contenido y los dispositivos**. La siguiente configuración es un ejemplo inicial 12-8-4, que puede ser útil si coincide con el proyecto; adapta sus valores o usa otra estructura:

| Dispositivo (ejemplo) | Breakpoint de ejemplo | Columnas del preset | Gutter de ejemplo | Margen lateral de ejemplo | Contenedor máximo de ejemplo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Desktop** | `>= 1024px` (`1280px+`) | 12 | `24px` (o `32px` editorial) | `64px - 120px` (`auto` centrado) | `1200px - 1280px` (`100%` en algunos dashboards) |
| **Tablet** | `768px - 1023px` | 8 | `20px` (o `16px`) | `32px - 40px` | Fluido (`100% - 2*margin`) |
| **Mobile** | `< 768px` (`375px` base) | 4 | `16px` | `16px - 20px` | Fluido (`100% - 2*margin`) |

2. **Espaciado y agrupación**:
   - La escala `8pt` y pasos finos de `4px` son opciones para un sistema consistente, no una condición para todo layout. Adapta medidas y unidades al contenido y plataforma.
   - Cuando la proximidad espacial exprese pertenencia a un grupo, usa separación interna menor que la separación externa como una heurística perceptual. Los rangos siguientes son ejemplos adaptables, no mínimos/múltiplos requeridos:
     - *Micro* (átomos dentro de una tarjeta): `8px - 16px`.
     - *Meso* (entre tarjetas o encabezado de sección y su grilla): `32px - 48px`.
     - *Macro* (entre secciones): `96px - 128px`.
3. **Tokens de espaciado**:
   - Si el proyecto usa tokens semánticos multi-modo, ajusta sus valores por contexto. Como punto de partida opcional: `--space-section-y` `104px` Desktop / `64px` Mobile; `--space-group-gap` `32px` / `20px`; `--space-card-padding` `24px` / `16px`.

### Fase 2: Selección de Patrones de Layout

Asigna a cada sección el patrón que responda al volumen y prioridad de su contenido (consulta los 25 patrones de `references/layout-patterns-25.md`). Los spans y colapsos del catálogo suponen la rejilla de referencia 12-8-4: ajústalos a la grilla elegida y valida el flujo para las vistas pertinentes.

- **1 columna en la grilla de referencia**:
  - *1. Hero Centrado Focal* (titular + subtítulo + CTA + artefacto inferior), si la página y el encargo incluyen un Hero.
  - *2. Columna Editorial Estrecha* (`65ch` orientativo para artículos, términos o narrativa).
  - *3. Banner Full-Bleed de Impacto* (ancho `100vw`, cuando el contenido lo pida).
  - *4. Flujo Vertical Paso a Paso (Timeline/Stepper)*.
  - *5. Contenedor Focal de Tarea Única* (Login, Checkout, Onboarding modal).
- **2 columnas en la grilla de referencia (`6+6`, `7+5` o `8+4` en Desktop; apilado en algunos Mobile)**:
  - *6. Split Hero Asimétrico (`7+5` o `6+6`)* (propuesta de valor + producto/visual), si aplica.
  - *7. Zig-Zag Alternado de Features* (invierte texto/imagen si ayuda a mantener interés).
  - *8. Sticky Narrative Scroll (`5+7`)* (si la interacción y contenido justifican `position: sticky`).
  - *9. Comparativa Lado a Lado (`6+6`)* (Antes/Después, Plan Pro vs. Free, Con vs. Sin).
  - *10. Sidebar + Workspace (`3+9` o `280px + 1fr`)* (aplicaciones o documentación).
- **3 columnas en la grilla de referencia (`4+4+4` o asimétrica)**:
  - *11. Tríada de Valor* (3 beneficios o pasos, solo si el contenido se agrupa así).
  - *12. Matriz de Precios con Destacado Central (`4+4+4`)*.
  - *13. Bento Grid Asimétrico de 3 Celdas (`8+4` arriba + `4+8` abajo)*.
  - *14. Feed Editorial con Destacado (`6+3+3`)*.
  - *15. Panel de Trabajo en 3 Bandas (`Lista + Detalle + Inspector`)*.
- **4 columnas en la grilla de referencia (`3+3+3+3`)**:
  - *16. Banda de KPIs / Métricas*.
  - *17. Catálogo / Galería de Activos*.
  - *18. Bento Grid Modular de 4 Columnas* (celdas `1x1`, `2x1`, `1x2` y `2x2`).
  - *19. Matriz de Equipo / Testimonios*.
  - *20. Mega-Footer Estructurado en 4 Pilares*.
- **5+ columnas en la grilla de referencia (alta densidad)**:
  - *21. Cinta de Logos de Confianza*.
  - *22. Matriz de Integraciones / Iconografía Técnica*.
  - *23. Tabla de Datos / Heatmap de Alta Densidad*.
  - *24. Tablero Kanban Multi-Etapa*.
  - *25. Galería Masonry / Mosaico Denso*.

### Fase 3: Jerarquía Visual y Squint Test

1. Si la tarea requiere ordenar fijaciones, puede ser útil considerar estas tres preguntas: ¿dónde estoy y qué puedo hacer?, ¿por qué me importa y cuáles son las opciones?, ¿cuál es el siguiente paso? Adapta las bandas al contenido y flujo; no exijas un Hero, una cronología o un CTA si no corresponde.
2. **Jerarquía en tres niveles**:
   - **Nivel 1 (Primario / Dominante)**: un único foco dominante por vista. Puede haber un segundo elemento destacado, como un botón de acción, siempre subordinado visualmente al foco; no cuenta como segundo dominante.
   - **Nivel 2 (Secundario / Escaneable)**: encabezados de sección, títulos de tarjetas, navegación principal y controles secundarios, según el layout.
   - **Nivel 3 (Terciario / Contextual)**: cuerpo de texto, metadatos, fechas, notas al pie y bordes divisorios sutiles.
3. **El Squint Test (heurística de desenfoque)**:
   - Cuando se pueda observar el layout, entrecierra los ojos o usa como exploración `filter: blur(6px) grayscale(100%)`:
     - ¿Se distinguen los grupos funcionales y su jerarquía?
     - ¿Hay un punto focal dominante y los elementos de apoyo permanecen subordinados?
   - Una recomendación o simulación mental no es una inspección visual; marca como no comprobado aquello que no se haya observado.

## Missing or Conflicting Information

- Si el usuario pide 5 o 6 tarjetas anchas de texto en una fila, estima el ancho útil con el viewport, contenido y grilla reales. Si se dificulta la lectura, compara alternativas como Bento Grid, menos columnas o apilado; no presupongas que una única estructura es siempre correcta.

## Output Contract

Entrega una especificación de **Layout, Rejilla y Jerarquía Visual** (`design-system/05-layout-and-hierarchy.md`) adaptada al alcance, que incluya:

1. **Grilla y espaciado seleccionados**: Columnas, breakpoints, *gutters*, márgenes y tokens `--space-*` solo si son pertinentes; indica qué valores son presets o decisiones del proyecto.
2. **Mapa de Arquitectura por Sección**: Patrón del catálogo para cada sección cuando sea útil, distribución de *spans* según la grilla realmente elegida y reglas de colapso cuando aplique.
3. **Matriz de Jerarquía**: Elementos relevantes de niveles 1, 2 y 3 por vista; un foco dominante y acompañantes subordinados.
4. **Código CSS Grid / Flexbox y Squint Test**, si forman parte del encargo; distingue código propuesto de inspección ejecutada.

## Common Mistakes

- **Perder la agrupación cuando se usa proximidad**: Si el espacio expresa grupos, evita que la separación interna sea igual o mayor que la separación entre esos grupos sin una razón de contenido.
- **Usar bordes como sustituto automático del espaciado**: Evalúa el espacio negativo y la estructura antes de añadir divisores; no hay una receta fija de `16px -> 32px -> 104px`.
- **Varios focos dominantes en competencia**: Mantén un foco dominante y subordina acompañantes según la tarea; el número de CTAs depende del flujo y no determina por sí solo la jerarquía.

## Verification

- [ ] La grilla, breakpoints y espaciado se seleccionaron según el contenido y los dispositivos; no se requiere el preset 12-8-4, 8pt ni valores concretos.
- [ ] Los patrones del catálogo usados se adaptan a la grilla elegida y su colapso se comprueba solo cuando aplica.
- [ ] La jerarquía establece un foco dominante único; elementos acompañantes de nivel alto están claramente subordinados.
- [ ] El Squint Test y verificaciones visuales solo se marcan realizados si hubo inspección; en otro caso se declaran no verificados.
