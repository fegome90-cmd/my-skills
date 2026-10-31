---
name: design-art-direction
description: "Define la dirección de arte a partir del brief: keywords, arquetipo estético, semilla narrativa, foco visual cuando aplique, motivos de rima pertinentes, materialidad opcional y 3 variantes A/B/C. Use when the user asks for visual style, art direction, moodboard, hero concept or the creative concept of a web, app or brand."
license: MIT
metadata:
  author: 'Felipe Gonzalez'
---

# Design Art Direction & Creative Concept

## Objective

Establecer una dirección de arte coherente, memorable y con intención narrativa antes de abrir el lienzo o escribir CSS. Este proceso transforma atributos abstractos de marca en un sistema visual concreto mediante arquetipos estéticos, una Semilla Narrativa, un foco visual cuando el alcance lo requiera, Rima Visual cuando la sustente el brief y profundidad táctil controlada.

## Inputs and Preconditions

- **Contexto del Proyecto**: Nombre del producto/marca, industria, audiencia objetivo y problema que resuelve (proveniente de `PRODUCT.md` si existe).
- **Entregable Esperado**: Especificación de Dirección de Arte (`design-system/01-art-direction.md` y sección correspondiente en `DESIGN.md`), concepto de Hero Section si está en alcance, o directrices de moodboard/stylescape.
- **Restricciones Existentes (Opcional)**: Activos de marca previos (logo, fotografía, restricciones regulatorias o de rendimiento en `STACK.md`).

## Workflow

### Fase 1: Extracción de Keywords y Selección del Arquetipo Estético

1. **Definir el Par de Keywords Fundacionales**:
   - Extrae de `PRODUCT.md` o del brief **3 keywords emocionales** (cómo debe *sentirse* el producto: ej. *sereno, confiable, artesanal*) y **3 keywords estructurales** (cómo debe *funcionar*: ej. *denso en datos, modular, instantáneo*).
2. **Seleccionar el Arquetipo Estético Primario (y un acento secundario opcional)**:
   - Evalúa el proyecto frente a los **6 Arquetipos Estéticos de Dirección de Arte** (consulta `references/archetypes-and-trends.md` para detalles extendidos):

| Arquetipo Estético | Referente Conceptual | Filosofía Visual | Superficies y Luz | Tipografía y Layout | Casos de Uso Ideales |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Minimalismo Industrial** | Diseño industrial de producto ("menos, pero mejor") | Reducción radical, claridad absoluta, el producto físico o digital es el héroe | Luz de estudio difusa, blancos puros/grises anodizados, cristal sutil | Neo-grotesca neutra, grillas simétricas amplias, 50%+ espacio negativo | Hardware, SaaS flagship, productividad, salud clínica |
| **2. Precisión de Alta Ingeniería** | Consolas de telemetría e ingeniería de alto rendimiento | Rendimiento extremo, telemetría, computación avanzada y autoridad técnica | Modo oscuro profundo (carbono/obsidiana), acentos luminosos de alta energía | Sans geométrica/técnica + Monospace tabular para métricas, Bento Grids | IA, infraestructura cloud, devtools, fintech cuantitativa |
| **3. Calidez Orgánica y Accesible** | Editorial de estilo de vida y hospitalidad | Hospitalidad, tactilidad humana, optimismo cotidiano y cercanía | Tonos crema, terracota, salvia; sombras cálidas y texturas de papel/lino | Serif humanista/orgánica en titulares + Sans amable en UI, bordes suaves | Bienestar, consumo consciente, educación, gastronomía |
| **4. Editorial Audaz de Alto Contraste** | Revistas de moda y dirección fotográfica | Expresión dramática, dirección de moda, presencia escultórica e impacto | Contrastes marcados, fotografía de estudio con iluminación direccional | Didone/Display de alto contraste + Sans minimalista, asimetría controlada | Moda, cultura, medios digitales, portfolios creativos |
| **5. Deconstrucción Conceptual** | Diseño post-industrial con metadatos expuestos | Transparencia industrial, metadatos expuestos ("SPEC"), ironía culta | Fondos crudos (hormigón/papel técnico), bordes de 1px visibles, etiquetas | Neo-grotesca pesada (Helvetica/Inter) + Monospace de etiquetas técnicas | Streetwear, Web3, estudios de diseño, lanzamientos experimentales |
| **6. Escala Cinemática e Inmersiva** | Lenguaje de cine de gran formato | Arquitectura monumental, tensión temporal, gravedad física y realismo | Paletas desaturadas (acero, ámbar, azul nocturno), profundidad atmosférica | Sans geométrica con *tracking* expandido en mayúsculas, encuadres panorámicos | Entretenimiento, arquitectura, movilidad, narrativa interactiva |

### Fase 2: La Semilla Narrativa de Sanderson y el Foco Visual

Aplicando el principio de construcción de mundos de Brandon Sanderson (*"empieza por un elemento extraordinario y deriva las leyes del sistema desde él"*):

1. **Declarar la Semilla Narrativa**: Formula en **una sola oración** qué hace único al universo visual del producto o interfaz (ej. *"Un laboratorio óptico donde cada tarjeta de datos actúa como una lente refractiva sobre papel milimetrado oscuro"*), si esa formulación es pertinente al encargo.
2. **Designar el foco visual cuando esté en alcance**:
   - Si el brief incluye una página con Hero, elige **exactamente 1 protagonista visual** para esa sección:
     - *Opción A*: Tipografía Escultórica / Titular Masivo.
     - *Opción B*: Visualización / Artefacto de Producto Interactivo en vivo.
     - *Opción C*: Pieza Fotográfica / Ilustración / 3D de dirección de arte.
   - **Regla de Exclusión**: Si la tipografía es el foco, los gráficos de acompañamiento deben subordinarse. Si una pieza visual o demo interactiva es la protagonista, el titular debe ser conciso y limpio sin competir con efectos decorativos.
   - Si el brief es una pantalla de producto o UI sin Hero, no inventes uno: define el foco de la tarea/interfaz solo si el encargo necesita esa decisión.

### Fase 3: Rima Visual (Visual Rhyming) cuando el brief lo sustente

Aplica la **Rima Visual** cuando una repetición de ángulos, curvaturas, proporciones o detalles estructurales entre elementos distintos refuerce la identidad del encargo:

1. **Explorar rimas pertinentes con la tipografía, el logo o componentes existentes**:
   - Si la fuente de titulares tiene terminales afiladas o cortes diagonales de `15°`, considera repetir ese corte o radio en contenedores destacados, divisores o badges.
   - Si la tipografía tiene curvas superelípticas suaves (*squircle*), considera radios continuos equivalentes en botones, tarjetas y avatares.
2. Cuando haya rasgos de identidad o formas que justifiquen la relación, documenta hasta 2 motivos concretos y dónde se repiten. No fuerces una rima entre logo/tipo y componentes si no se desprende del brief; indica que no aplica y por qué.

### Fase 4: Profundidad Táctil Opcional y Exploración Divergente

1. **Presupuesto de Textura y Profundidad (Opcional, Máximo 2 Capas)**:
   - **Por defecto: 0 capas** en UI de producto, dashboards y herramientas clínicas o de uso intensivo. Grano y *glassmorphism* son opciones, no requisitos; úsalos solo si el brief/arquetipo lo justifica y cada capa cumple una función (separar planos o dar materialidad a la marca) sin dañar lectura, contraste o rendimiento.
   - Si una o dos capas se justifican, descríbelas con la razón de uso; no hay un mínimo requerido:
     - *Capa 1 (Micro-textura de superficie)*: Grano analógico sutil (`SVG feTurbulence` con `opacity: 0.025` a `0.04` y `mix-blend-mode: overlay`) o patrón geométrico de baja opacidad.
     - *Capa 2 (Materialidad óptica)*: *Glassmorphism* funcional (`backdrop-filter: blur(12px) saturate(140%)`) con borde especular superior/izquierdo de `1px solid rgba(255,255,255,0.12)` e iluminación direccional consistente desde el cénit superior.
2. **Iteración del Productor Musical (3 Variaciones Divergentes)**:
   - Antes de cerrar la dirección de arte, plantea mentalmente o en boceto **3 mezclas del mismo contenido** (como un productor musical que prueba una versión acústica, una sinfónica y una electrónica):
     - *Mezcla A (Contenida/Clásica)*: 80% convención del sector, 20% carácter.
     - *Mezcla B (Equilibrada/Recomendada)*: Equilibrio óptimo entre usabilidad y personalidad distintiva.
     - *Mezcla C (Vanguardia/Experimental)*: Lleva el arquetipo y la semilla narrativa al límite expresivo.

## Missing or Conflicting Information

- Si el usuario no especifica industria, audiencia o tono emocional, **no inventes un estilo genérico**: ofrece 2 o 3 opciones contrastadas basadas en los 6 arquetipos y pregunta cuál resuena mejor antes de fijar la dirección definitiva.
- Si el usuario pide combinar arquetipos opuestos al mismo nivel (ej. *Minimalismo Industrial* + *Editorial Audaz* + *Deconstrucción* al 33% cada uno), advierte del riesgo de fragmentación visual y propone una jerarquía **80% Arquetipo Primario + 20% Acento Secundario**.

## Output Contract

Entrega una especificación estructurada de **Dirección de Arte** (`design-system/01-art-direction.md`) ajustada al alcance, que incluya:

1. **Matriz de Identidad**: 3 Keywords Emocionales + 3 Keywords Estructurales + Arquetipo Primario (y Secundario si aplica).
2. **Semilla Narrativa y foco visual**: Declaración en 1 frase si es pertinente; define un protagonista único solo si un Hero está en alcance, sin imponer Hero a una pantalla de producto.
3. **Rima Visual, si aplica**: Motivos morfológicos concretos respaldados por el brief; si no hay una relación pertinente, indícalo sin inventarla.
4. **Materialidad, si aplica**: Cero, una o dos capas, con parámetros y razón para cada capa usada; explica si no se necesita ninguna.
5. **Tres Direcciones de Mezcla (A/B/C)**: Breve comparativa de las 3 variaciones del productor musical con una recomendación fundamentada.

## Common Mistakes

- **Síndrome de "Todo es Protagonista"**: Si un Hero está en alcance, evitar que titular, fondo, tarjetas y CTAs compitan por el mismo protagonismo.
- **Incongruencia de Rima Visual**: Usar una tipografía brutalista cuadrada con botones tipo píldora (`border-radius: 9999px`) e iconos redondeados infantiles sin justificación semántica.
- **Ruido o Glassmorphism Ilegible**: Aplicar efectos de superficie sobre texto denso sin comprobar lectura y contraste.

## Verification

- [ ] Se definieron keywords conectadas con el brief y un Arquetipo Estético claro.
- [ ] La semilla responde al encargo; se define un protagonista único solo cuando el Hero está en alcance.
- [ ] Los motivos de Rima Visual, si se usan, se justifican con el brief; una ausencia pertinente se declara en vez de inventar conexiones.
- [ ] Se justifican individualmente las capas de materialidad usadas (0–2); cero capas es válido y no requiere parámetros ficticios.
