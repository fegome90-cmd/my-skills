---
name: design-tokens-components
description: "Crea la arquitectura de tokens y componentes de un sistema: convención local Brand/Alias/Mapped, ejemplos JSON con objetivo DTCG Format Module 2025.10, descripciones de uso para agentes, radios concéntricos, 5 propiedades de componente y fichas CRD. Use when structuring design tokens or Figma variables, defining component properties or slots, or evaluating nested border radii. Para auditar un sistema existente o sincronizarlo con Figma, prefiere las skills de auditoría o sincronización si están disponibles."
license: MIT
metadata:
  author: 'Felipe Gonzalez'
---

# Design Tokens Architecture & Flexible Components

## Objective

Arquitectar y auditar sistemas de tokens y componentes reutilizables en Figma y código usando el formato del DTCG (*Design Tokens Community Group*) cuando corresponda. El ejemplo JSON toma como objetivo el **DTCG Format Module 2025.10**, que no es un estándar W3C; la cascada en **3 colecciones (`Brand -> Alias -> Mapped`)** y `$extensions.mode` son convenciones locales, no requisitos DTCG. Evaluar radios concéntricos con $R_{\text{ext}} = R_{\text{int}} + p$ solo si el inset uniforme y la intención geométrica lo justifican; aplicar las **5 propiedades de componentes** (incluyendo *Slots*) con **98% de invariancia responsiva** y documentar cada pieza mediante *Component Reference Documents* (`CRD`) con reglas semánticas de 1 línea legibles por humanos y agentes de IA. No afirmar compatibilidad o validación de schema sin validación específica.

## Inputs and Preconditions

- **Fundamentos del Sistema**: Escalas tipográficas, rampas de color (`100-900` + `150`) y tokens espaciales (`8pt` + *Jumper*) definidos en las fases previas o en `DESIGN.md`.
- **Entorno de Destino**: Variables de Figma, CSS Custom Properties, JSON con el formato DTCG (la referencia de esta skill usa como objetivo 2025.10), Tailwind CSS v4 `@theme` o Style Dictionary (según `STACK.md`).
- **Inventario de Componentes**: Átomos, moleculas u organismos a especificar (botones, inputs, cards, modales, tablas, navegación).

## Workflow

### Fase 1: El Árbol de Variables en 3 Colecciones (`Brand -> Alias -> Mapped`) — convención local

Para evitar tanto la rigidez de usar hexadecimales directos como el caos de miles de tokens hiper-específicos inmanejables, estructura esta arquitectura local en **3 niveles**. DTCG no exige esos nombres ni esa cantidad de colecciones:

| Nivel | Nombre de Colección | Función Exacta | Visibilidad en Librería | Ejemplo de Token |
| :--- | :--- | :--- | :--- | :--- |
| **Nivel 1** | **Brand (Primitivos)** | Inventario bruto de valores matemáticos sin contexto de uso (rampas `100-900`, escala `px/rem`) | **Oculto** (*Hide from publishing* en Figma; variables privadas en código) | `brand/blue/600` (`#2563EB`), `brand/space/16` (`16px`) |
| **Nivel 2** | **Alias ( Puentes Semánticos)** | Traduce el primitivo a un rol de marca o categoría transversal antes de tocar superficies concretas | Interno del Design System (puente para rebranding instantáneo en 1 clic) | `alias/primary/default` → `brand/blue/600`, `alias/neutral/surface` → `brand/slate/100` |
| **Nivel 3** | **Mapped (Tokens de Interfaz / Modo)** | Tokens finales consumidos por los componentes; los modos Light/Dark y Desktop/Mobile, cuando se usan, son una convención del proyecto | **Público** (Única colección que los diseñadores y agentes IA pueden asignar a componentes) | `surface/card/default`, `text/primary`, `action/primary/bg`, `space/card/padding` |

1. **Regla Semántica de 1 Línea para Agentes IA (`$description`)**:
   - Cada token de la colección `Mapped` debe incluir en su campo `Description` de Figma y `$description` en JSON una **oración imperativa de 1 línea** que indique *dónde usarlo y dónde NO usarlo* (ej. `"Fondo de tarjetas elevadas nivel 1; no usar para el canvas general de la página ni para modales"`). Esto elimina alucinaciones cuando un agente genera UI vía Figma MCP o CSS.
2. **Criterio de Excepción para Component-Level Tokens (4to Nivel Condicional)**:
   - **No crees tokens por componente por defecto** (`button-primary-bg`, `card-header-bg`) si el componente simplemente sigue las reglas de `Mapped`.
   - **Crea un Component-Level Token ÚNICAMENTE cuando** el componente requiere romper la lógica de inversión automática entre Light Mode y Dark Mode (ej. un `Tooltip` oscuro que permanece oscuro en ambos modos, o un `Primary Button` cuyo texto debe mantenerse blanco en Dark Mode aunque `--text-primary` se invierta).
3. **Frontera Estricta: Variables vs. Styles Compuestos**:
   - **Variables (Tokens Atómicos)**: Almacenan un único valor atómico (un color, una dimensión de espaciado/radio, un string de fuente).
   - **Styles (Compuestos)**: Se usan para propiedades multi-valor que combinan varios tokens o vectores: **Typography Styles** (que agrupan `font-family` + `font-size` + `line-height` + `letter-spacing`), **Effect Styles** (`box-shadow` multi-capa + `backdrop-filter`), **Layout Grids** y **Gradientes**.

`$extensions.mode` es una convención de proyecto en el ejemplo, no un mecanismo universal de modos definido por DTCG.

### Fase 2: Geometría de Radios Concentricos y las 5 Propiedades de Componentes

1. **Relación de Radios para Inset Uniforme (heurística geométrica contextual)**:
   - Si un elemento con borde redondeado (ej. un botón o imagen con radio interno $R_{\text{int}}$) va dentro de un contenedor padre con inset uniforme $p$ y la intención es conservar un paralelismo concéntrico, considera:
     $$R_{\text{ext}} = R_{\text{int}} + p$$
   - *Ejemplo*: Con $R_{\text{int}} = 8\text{px}$ (`--radius-sm`) e inset uniforme $p = 16\text{px}$ (`--space-micro`), la relación da $R_{\text{ext}} = 8 + 16 = 24\text{px}$ (`--radius-xl`). Comprueba los valores efectivos y la geometría resultante.
   - No es una regla universal para cualquier borde anidado. Con insets no uniformes, radios asimétricos, clipping u otra intención visual, evalúa los lados/condiciones pertinentes o elige una geometría distinta; no declares satisfecha la ecuación si los valores no cuadran.
2. **Arquitectura de Componentes con las 5 Propiedades (Anti-Explosión de Variantes)**:
   - Antes de multiplicar la matriz de variantes en Figma o las props en React/Vue, aplica cada propiedad para su propósito exacto:
     1. **Variants**: *Solo* para cambios estructurales o de estado visual que alteran múltiples tokens simultáneamente (`intent: primary | secondary | danger`, `size: sm | md | lg`, `state: default | hover | focus | disabled`).
     2. **Boolean Property**: Para mostrar/ocultar sub-elementos opcionales (`hasIconLeft`, `hasBadge`, `isDismissible`) en lugar de duplicar variantes *With Icon / Without Icon*.
     3. **Text Property**: Para inyectar cadenas de texto (`label`, `helperText`, `placeholder`).
     4. **Instance Swap**: Para intercambiar átomos del mismo contrato (ej. cambiar el icono `Lucide/Check` por `Lucide/ArrowRight`).
     5. **Slots (Propiedad de Ranura / `children`)**: En contenedores compuestos (`Modal`, `Card`, `Accordion`, `Drawer`), **prohibido meter 20 variantes de contenido fijo**. Define una sub-capa de tipo **Slot** con Auto Layout para inyectar cualquier contenido hijo manteniendo intacto el marco, el *padding* y la geometría elegida.
3. **Regla del 98% de Invariancia Responsiva**:
   - Un componente bien construido con `Auto Layout` (`flexbox`/`grid`), restricciones `Fill container` / `Hug contents` y vinculado a variables `Mapped` (incluyendo *Jumper variables*) **no necesita una variante `.Mobile` y otra `.Desktop`**. El **98% de los componentes** deben adaptarse solos al cambiar el ancho de su columna y el modo de variables de la página; reserva variantes responsivas explícitas solo para el **2% de estructuras que cambian de topología** (ej. una barra de navegación superior que se transforma en un *Bottom Sheet* o *Drawer*).

### Fase 3: Component Reference Documents (CRD) y Gobernanza Anti-Drift

Para cada componente clave del sistema, redacta o actualiza su **Component Reference Document (`CRD-<ComponentName>.md`)** y ejecuta el **Protocolo de Auditoría en 4 Pasos** antes de fusionar cambios:

1. **Auditoría de Primitivos**: Cero valores hexadecimales o `px` mágicos; todo apunta a `Mapped`.
2. **Auditoría de Geometría**: Verificación de la rejilla `8pt`/`4pt` y de la relación $R_{\text{ext}} = R_{\text{int}} + p$ solo si aplica al inset uniforme e intención elegidos.
3. **Auditoría de Estados**: Presencia de `default`, `hover`, `active`, `focus-visible`, `disabled`, `loading` y `error`.
4. **Sincronización de Documentación**: Actualización del `CRD` y del índice en `DESIGN.md` (< 150 líneas).

## Missing or Conflicting Information

- Si el usuario pide crear variantes separadas para cada combinación de icono, texto y modo oscuro (ej. `Button / Primary / Dark / With Left Icon / Mobile`), explica cómo las 5 propiedades de componentes + variables `Mapped` reducen una matriz de 96 variantes a **12 variantes limpias** y entrega la estructura optimizada.
- Si no se ha elegido la versión DTCG para el proyecto, declara que 2025.10 es solo el objetivo del ejemplo. No afirmes compatibilidad de formato o schema sin ejecutar una validación correspondiente.

## Output Contract

Las rutas de salida siguientes son relativas a la raíz del proyecto (`PROJECT-ROOT`).

Entrega una especificación de **Design Tokens y Arquitectura de Componentes** (`design-system/06-tokens-and-components.md`, `design-system/tokens/design-tokens.json` y `design-system/components/CRD-*.md`) que contenga:

1. **Árbol de Tokens en 3 Colecciones (`Brand -> Alias -> Mapped`)**: Si se entrega JSON, nombrar la versión objetivo del DTCG Format Module; la referencia usa 2025.10. Normalizar los valores `color` y `dimension` según ese formato. Las tres colecciones y `$extensions.mode` son convenciones locales, no requisitos DTCG. No afirmar conformidad de schema sin validación específica. Incluir CSS Custom Properties y `$description` de 1 línea en cada token `Mapped`.
2. **Tabla de Radios**: Pares verificados de $(R_{\text{int}}, p, R_{\text{ext}})$ para tarjetas, modales, grupos de botones e inputs cuando la relación concéntrica y el inset uniforme correspondan.
3. **Contratos de Componentes (`CRD`)**: Especificación de propiedades (`Variants`, `Booleans`, `Text`, `Instance Swap`, `Slots`), anatomía interna, tokens asignados y comportamiento responsivo (98% invariante).

## Common Mistakes

- **Publicar la colección `Brand` a los consumidores del sistema**: Si los diseñadores o agentes IA ven `brand/blue/500`, lo usarán directamente en lugar de `action/primary/bg`, rompiendo el Dark Mode y los futuros rebrandings.
- **Declarar cumplida una relación geométrica sin comprobar los valores**: Si aplica la relación para un inset uniforme, comprueba la suma con los valores efectivos; no universalices la fórmula para otras geometrías.
- **Duplicar componentes para Mobile y Desktop**: Multiplica por dos el costo de mantenimiento cuando bastaba con usar `Fill container` y variables *Jumper*.

## Verification

- [ ] La arquitectura local de tokens separa `Brand` (oculto), `Alias` (puente) y `Mapped` (público con modos y `$description` de 1 línea), sin atribuir esta convención a DTCG.
- [ ] Si se declara DTCG, el ejemplo identifica la versión objetivo (2025.10 aquí) y emplea la representación correspondiente para `color` y `dimension`; `$extensions.mode` permanece identificado como convención local. No se afirma validación de schema sin hacerla.
- [ ] Cuando se usa la relación de radios para un inset uniforme, los valores concretos cuadran con la intención geométrica; no se generaliza como requisito universal.
- [ ] Los componentes utilizan `Booleans`, `Instance Swap` y `Slots` para evitar la explosión de variantes y consideran la invariancia responsiva según el contexto.
- [ ] Cada componente especificado cuenta con su ficha `CRD` completa y trazable a `design-system/tokens/design-tokens.json` (ruta relativa a `PROJECT-ROOT`).
