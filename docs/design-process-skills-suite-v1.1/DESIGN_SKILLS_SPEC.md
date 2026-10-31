# Especificación de la suite de skills de diseño v1.1

## 1. Propósito y límites

La suite reúne ocho skills portables para coordinar y resolver tareas de dirección visual, tipografía, color, layout, tokens/componentes y motion/handoff. Portabilidad describe el formato de conocimiento y procedimiento, no garantiza compatibilidad universal con cualquier agente o harness. No se requieren dependencias de runtime ni herramientas particulares; las capacidades disponibles se descubren en el entorno de uso.

El orquestador coordina alcance, dependencias y handoff. No sustituye ni duplica reglas de especialistas, no es propietario de los documentos o decisiones del proyecto y no crea una autoridad de revisión paralela. El proyecto conserva la autoridad de sus fuentes canónicas; el harness anfitrión conserva sus propios procesos y gates.

## 2. Modos, autoridad y alcance

Seleccionar el modo mínimo que cubre la solicitud. El número de dimensiones o nodos no escala automáticamente el trabajo.

| Modo | Condición | Contrato de trabajo y escritura |
|---|---|---|
| **Greenfield** | Intención explícita de crear desde cero; alcance y decisiones necesarias claros o resueltos. Un repositorio nuevo no basta. | Planificar solo las fases solicitadas o pertinentes. Ofrecer scaffolding si es útil y autorizado; no implica crear todos los artefactos ni ejecutar todos los tests. |
| **Subgraph** | Se solicitan o implican fases acotadas. | Consultar prerequisitos relevantes, declarar dependencias y fases omitidas. No generar fases ni documentos ajenos al alcance. |
| **Ligero** | Ajuste acotado de una o pocas dimensiones existentes. | Consultar fuentes relevantes y derivar al especialista. No crear ni exigir los cuatro documentos rectores, ni crear un `DESIGN.md` faltante. |
| **Auditoría** | Solicitud explícita de inspección/informe. | Inspeccionar y reportar hallazgos, cobertura, evidencia y límites. Es read-only; un hallazgo no autoriza corregirlo. |
| **Refactorización** | Autorización explícita para cambiar estructura/contenido y alcance de escritura claro. | Modificar únicamente superficies autorizadas, respetando fuentes y ownership. Una auditoría o mejora inferida no concede permiso. |

En proyectos existentes, identificar la raíz/índice, fuentes rectoras pertinentes, responsables, restricciones y capacidades existentes. Respetar la autoridad de esas fuentes, señalar conflictos y no sobrescribirlas ni cambiar stack, herramientas o dependencias por inferencia. La presencia de un manifiesto no equivale a autorización. Si una ambigüedad de autoridad o permiso cambia el trabajo, detener solo ese trabajo afectado y pedir decisión.

Enrutar solo los dominios solicitados. Si falta una capacidad o especialista, continuar el trabajo independiente, marcar su dominio `NotReviewed` y bloquear únicamente resultados dependientes. No instalar un reemplazo ni atribuir verificación a una capacidad ausente.

## 3. Cobertura, evidencia y verificación

Son dimensiones distintas. Para cada dominio/gate pertinente informar responsable, fuente, cobertura, método, evidencia observada y estado de verificación. No existe obligación de completar ocho gates ni de producir ocho `PASS`.

- **Cobertura:** `Reviewed`, `NotReviewed` o `NotApplicable` (con motivo). Una etapa omitida nunca es aprobación.
- **Verificación:** `Verified`, `Failed` o `NotVerified`, siempre con método/evidencia. La inspección estática no demuestra comportamiento; sin navegador, la conducta visual es `NotVerified`.
- Para `NotApplicable`, explicar su relación con el alcance y dejar verificación como `—`. No convertir instrucciones, fixtures, inspección o resultados parciales en prueba de conducta de un agente ni en aprobación global.
- Las verificaciones de accesibilidad, estados, contenido/i18n y rendimiento se seleccionan por contenido, plataforma, locales, alcance y evidencia. No afirmar FPS/GPU, conformidad WCAG, renderizado ni conducta de modelo sin la prueba correspondiente.

## 4. Paquete de entregables y rutas canónicas

Los entregables son condicionales a modo, contexto, fase solicitada y autorización; no son prerrequisitos universales. Las plantillas de workspace son punto de partida y deben adaptarse al layout y ownership existentes.

Desde la raíz del proyecto, los posibles documentos rectores son `PRODUCT.md`, `STACK.md`, `CONTEXT.md` y `DESIGN.md`. Son opcionales: un modo ligero, subgrafo o auditoría no los exige ni los crea automáticamente. Las notas de fases solo se generan para trabajo incluido en alcance:

```text
<project-root>/
├── PRODUCT.md                         # opcional: intención, usuarios y contexto
├── STACK.md                           # opcional: decisiones técnicas del proyecto
├── CONTEXT.md                         # opcional: vocabulario del proyecto
├── DESIGN.md                          # opcional: índice conciso, no SSOT automática
└── design-system/
    ├── 01-art-direction.md
    ├── 02-typography-selection.md
    ├── 03-typography-scales.md
    ├── 04-color-system.md
    ├── 05-layout-and-hierarchy.md
    ├── 06-tokens-and-components.md
    ├── 07-motion-and-handoff.md
    ├── tokens/
    │   ├── design-tokens.json
    │   └── theme.css
    └── components/
        └── CRD-<ComponentName>.md
```

Crear solo archivos solicitados/autorizados y aplicables; eliminar secciones fuera de alcance en vez de insinuar que se completaron. Las rutas son relativas a la raíz del proyecto, no a la skill: tokens siempre bajo `design-system/tokens/`, CRD bajo `design-system/components/`. Si un `DESIGN.md` está autorizado, sus enlaces usan esas mismas rutas. No sustituir el índice o layout canónico de un proyecto.

## 5. Skills, ownership y fundamentos

Los nombres `G0`–`G7` identifican comprobaciones posibles, no una cadena universal ni gates que siempre deban ejecutarse. El especialista es responsable de los juicios de su dominio; el orquestador informa cobertura y dependencias sin duplicar sus criterios detallados.

| Nodo | Skill y responsabilidad | Fundamentos conservados | Salida posible / condición |
|---|---|---|---|
| **G0** | `design-process-orchestrator`: alcance, modos, coordinación y consolidación. | Prompt Graph Engineering (Sandeco Macedo), lenguaje ubicuo de Domain-Driven Design y prevención de drift. | Plan/handoff del trabajo solicitado; no hay cuatro archivos obligatorios. |
| **G1** | `design-art-direction`: concepto y dirección visual conectados al brief. | Arquetipos, semilla y “Star of the Show” de Brandon Sanderson; *Visual Rhyming* cuando el brief lo sustente; variaciones divergentes. | `design-system/01-art-direction.md` si está en alcance. Hero y protagonista solo si el encargo incluye Hero. Materialidad: 0–2 capas justificadas, sin mínimo. |
| **G2** | `typography-selection-pairing`: voz de display y función de lectura. | “Font Follows Feeling / Function” (Oliver Schöndorfer), canon de emparejamiento de Massimo Vignelli y prueba MEGATYPOS. | `design-system/02-typography-selection.md` si se solicita selección/emparejamiento. Glifos, pesos, licencia y features se verifican según necesidad local; `tabular-nums` solo si se alinean datos. Variable WOFF2 es opcional/preferible cuando convenga. |
| **G3** | `typography-scales-microtype`: escalas, espaciado y microtipografía. | Escalas modulares/armónicas; triada de letter-spacing (Chris Misterek), medida/legibilidad (Matthew Butterick), WCAG 2.2 SC 1.4.4 y 1.4.12 cuando aplican. | `design-system/03-typography-scales.md` si está en alcance. Escalas, `rem`/`clamp()` y line-height son decisiones/recomendaciones contextuales, no evidencia de conformidad. Probar overrides aplicables y redimensionado; no inferir cumplimiento de valores por defecto. |
| **G4** | `color-theory-palette`: armonía, rampas, temas y pares de contraste. | HSB/OKLCH como medios posibles, grayscale-first, psicofísica de UX (Rex Hartson y Pardha Pyla), WCAG 2.2 SC 1.4.1, 1.4.3 y 1.4.11. | `design-system/04-color-system.md` y helper si están en alcance. Porcentajes/rampas son punto de partida; verificar el HEX emitido y cada par aplicable, sin redondear un fallo hacia PASS. |
| **G5** | `layout-grid-hierarchy`: espacio, estructura y jerarquía. | Gestalt (sistematizada por William Lidwell), Squint Test y catálogo de 25 patrones; 12-8-4/8pt como presets adaptables (la rejilla 12-8-4 se relaciona con convención de Material Design). | `design-system/05-layout-and-hierarchy.md` si está en alcance. Elegir grilla, breakpoints y patrones según contenido/tarea/dispositivo; un foco dominante y acompañantes subordinados, sin Hero o layout obligatorio. |
| **G6** | `design-tokens-components`: arquitectura local de tokens y contratos de componentes. | DTCG Format Module 2025.10; convenciones locales Brand/Alias/Mapped; radios concéntricos condicionales; properties/slots y CRD. | `design-system/06-tokens-and-components.md`, `design-system/tokens/design-tokens.json` y CRD solo cuando se pidan. El ejemplo apunta al DTCG Format Module 2025.10, que **no es estándar W3C**. Brand/Alias/Mapped y `$extensions.mode` son convenciones locales. Si se da JSON, normalizar `color` con componentes sRGB 0–1 y `dimension` como `{ "value": número, "unit": "px" }`; las referencias de tokens son strings. No afirmar validación de schema sin validarla. |
| **G7** | `ui-motion-and-handoff`: movimiento, interacción, estados y handoff. | Principios de motion de Emil Kowalski; affordances/ciclo de interacción de Hartson y Pyla; Widget-First, destilación anti-slop y señal/ruido de Lidwell. | `design-system/07-motion-and-handoff.md` si se solicita handoff. Declarar propiedades por interacción; `transform`/`opacity` son preferidas para movimiento espacial, con excepciones justificadas. `prefers-reduced-motion` neutraliza desplazamiento y escala espacial; conservar feedback no espacial cuando proceda. |

## 6. Topología de referencia

Para una iniciativa Greenfield explícita y completa, la topología orientativa conserva esta secuencia: contexto/alcance → dirección de arte → selección tipográfica, color y layout según lo pedido → tokens/componentes cuando se necesiten → motion/handoff cuando se necesite. La selección tipográfica precede a la escala si la tarea depende de una fuente elegida; declarar otras dependencias reales.

Esta secuencia no obliga a ejecutar las ocho skills: los nodos independientes pueden trabajarse como subgrafo. Una auditoría es solo lectura; una refactorización requiere autorización expresa. El orquestador compacta y consolida el handoff, pero la fuente rectora del proyecto y el ownership del especialista se mantienen.

## 7. Accesibilidad y precisión normativa

Identificar nivel y criterio exactos si se citan. WCAG 2.2 SC 2.4.7 Focus Visible y SC 2.4.11 Focus Not Obscured (Minimum) son AA; SC 2.4.13 Focus Appearance es AAA. Un outline visible por sí solo no demuestra todos esos criterios. SC 2.5.8 Target Size (Minimum) es AA y su regla general de 24×24 CSS px tiene excepciones normativas (spacing, equivalent, inline, user-agent control y essential); no imponer el tamaño sin evaluar excepciones. 44×44 corresponde a SC 2.5.5 Target Size (Enhanced), AAA, y puede ser recomendación de comodidad, no requisito AA.

Las pruebas concretas dependen de los componentes/plataformas en alcance. Por ejemplo, SC 1.4.12 se verifica con los cuatro overrides simultáneos (line-height 1.5, espaciado entre párrafos 2em, letter-spacing 0.12em y word-spacing 0.16em) y ausencia de pérdida; un line-height inicial no es prueba. Para SC 1.4.4 se comprueba el redimensionado/zoom aplicable (incluido 200% cuando corresponda), no la unidad CSS aislada.

## 8. Cobertura declarada de fixtures y límites de evidencia

El fixture congelado describe **nueve familias**: cinco casos de intención por cada una de las ocho skills (dos directos, una paráfrasis, un near-miss y una confusión con skill vecina: 40 casos declarados en total) más nueve escenarios de orquestación. Los cuatro casos de regresión de la interfaz pública del helper de color son una familia separada de comandos/casos de prueba, no evidencia de conducta del LLM.

Los fixtures declaran entradas y propiedades esperadas; por sí solos no prueban ejecución, routing, ausencia de colisiones, comportamiento del agente ni aprobación. Informar por separado cobertura estructural, ejecución de regresiones, evaluación de comportamiento, verificación visual y validación de formato. No decir “PASS” para un fixture que solo está declarado ni convertir un resultado de un tipo en otro.

## 9. Conservación de intención y referencias

La suite conserva sus marcos teóricos, autores atribuidos y catálogo de 25 patrones como herramientas de trabajo; sus valores, proporciones, geometrías, presets y preferencias estéticas se aplican con contexto y no se elevan a reglas universales ni evidencia por sí solos. Las referencias comparativas y documentos de contexto informan el análisis, no son autoridad estética, política pública universal ni permiso para alterar fuentes del proyecto. La autoría declarada por el propietario y su elección explícita de MIT constan en [PROVENANCE.md](PROVENANCE.md) y en los avisos LICENSE del paquete y de cada skill. Esto no autentica externamente el origen ni concede autorización operativa al agente para instalar, incorporar o publicar.
