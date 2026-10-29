---
name: typography-selection-pairing
description: "Elige y empareja tipografías: separa la voz expresiva (titulares) del motor de lectura (UI y cuerpo), verifica propiedades técnicas relevantes al idioma, contenido y despliegue, y valida el emparejamiento en 3 niveles con la prueba MEGATYPOS. Use when choosing fonts, pairing typefaces or checking whether a font suits a UI, editorial or clinical interface."
license: MIT
metadata:
  author: 'Felipe Gonzalez'
---

# Typography Selection & Pairing

## Objective

Seleccionar y emparejar familias tipográficas combinando expresividad de marca (*Font Follows Feeling*) con legibilidad funcional (*Font Follows Function*, formulado por Oliver Schöndorfer). Verifica las propiedades técnicas que requiere el uso local y fundamenta las afirmaciones sobre cada fuente con evidencia de sus fuentes primarias; usa la estrategia de 3 niveles de combinación (Canon de Massimo Vignelli, Superfamilias y prueba *MEGATYPOS*) cuando sea pertinente.

## Inputs and Preconditions

- **Keywords del Proyecto**: Atributos emocionales (personalidad/tono) y estructurales (densidad de interfaz, lectura larga, tablas de datos), provenientes de `PRODUCT.md` o `design-system/01-art-direction.md`.
- **Idioma y Contenido**: Idiomas soportados y glifos realmente usados (ej. español con tildes, diéresis y `ñ`), presencia de cifras financieras/clínicas o bloques de código.
- **Restricciones de Plataforma**: Presupuesto de carga web, preferencia por fuentes open-source (Google Fonts / Fontshare) o licencias comerciales definidas en `STACK.md`.

## Workflow

### Fase 1: Bifurcación Semántica y Funcional (Feeling vs. Function)

Separa la decisión tipográfica en dos roles con criterios distintos:

1. **Font Follows Feeling (Voz Expresiva - Display y Titulares `H1`-`H2`)**:
   - Traduce las keywords emocionales de la dirección de arte en rasgos morfológicos:
     - *Autoridad Editorial / Tradición*: Serif de alto contraste o transicional (*Instrument Serif*, *Playfair Display*, *Newsreader*, *Fraunces*).
     - *Precisión Técnica / Modernidad*: Sans Geométrica o Neo-Grotesca con detalles incisivos (*Space Grotesk*, *Plus Jakarta Sans*, *Syne*, *Cabinet Grotesk*).
     - *Calidez Humana / Cercanía*: Sans o Serif Humanista de trazo orgánico (*Lora*, *Source Serif 4*, *Outfit*, *General Sans*).
2. **Font Follows Function (Motor de Lectura - Body, UI Controls y Data `H3`-`Caption`)**:
   - Para texto corrido y controles, considera legibilidad y desambiguación de glifos según los idiomas, tamaños y tareas del producto. La altura de `x`, contraformas abiertas y distinción de `1Il`/`0O` son criterios a comprobar cuando sean relevantes; no presumas que una familia los cumple sin evidencia.

### Fase 2: Verificación Técnica Contextual

Verifica los requisitos locales de cada fuente seleccionada usando evidencia de sus fuentes primarias (por ejemplo, página oficial de la familia, repositorio del distribuidor/fundidor, archivos de fuente y texto de licencia). Registra la fuente/version consultada; si no hay evidencia disponible, marca la propiedad como no verificada, no como aprobada.

1. **Pesos y estilos requeridos**: Comprueba que los archivos/familia elegidos incluyan los pesos reales que necesita el diseño y que no se simulen grosores o cursivas cuando la distinción auténtica sea necesaria. No exijas una lista fija de pesos o cursiva si el sistema no los usa.
2. **Cobertura de idioma y glifos requeridos**: Comprueba los caracteres que realmente necesita el producto (por ejemplo, `á, é, í, ó, ú, ñ, Ñ, ü, ¿, ¡` y símbolos monetarios/matemáticos cuando apliquen). No infieras cobertura por el nombre de un subconjunto como `Latin Extended`.
3. **Números tabulares**: Comprueba `tabular-nums` / `tnum` solo para datos que necesiten alineación vertical de cifras, como ciertas tablas, precios, signos vitales, contadores o dashboards. Si no aplica, indícalo como no requerido.
4. **Formato y fuente variable**: El soporte Variable Font y WOFF2 es opcional; prefiérelo si es apropiado para navegador, rendimiento, presupuesto y pesos/ejes requeridos. Verifica los archivos y ejes usados; no conviertas un peso de archivo o número de archivos universal en requisito.
5. **Licencia de uso**: Comprueba la licencia aplicable a la distribución, plataforma y uso local de la fuente. Registra evidencia y condiciones pertinentes; no afirmes licencia abierta o comercial verificada sin una fuente consultable.

### Fase 3: Estrategia de Emparejamiento en 3 Niveles y Prueba MEGATYPOS

Limita el sistema a **máximo 2 familias** (más 1 `Monospace` opcional para código/datos técnicos) eligiendo uno de estos 3 niveles de complejidad cuando aplique (consulta `references/font-catalog-and-pairings.md` para candidatos, no propiedades ya verificadas):

| Nivel | Estrategia | Regla de Construcción | Nivel de Riesgo | Ejemplo Recomendado |
| :--- | :--- | :--- | :--- | :--- |
| **Nivel 1** | **Monofuente (Canon de Massimo Vignelli)** | 1 sola familia hiper-versátil en todo el sistema; la jerarquía se logra variando peso, tamaño, *tracking* y opacidad | Bajo si cubre los roles requeridos | *Inter*, *Plus Jakarta Sans*, *IBM Plex Sans*, *Geist* |
| **Nivel 2** | **Superfamilia Tipográfica** | Combinar variantes Sans y Serif (o Mono) de una misma superfamilia si sus rasgos sirven al brief | Depende de los roles y archivos disponibles | *IBM Plex Sans + Serif + Mono*, *Source Sans 3 + Source Serif 4*, *Instrument Serif + Sans* |
| **Nivel 3** | **Headline Anchor Font + Prueba MEGATYPOS** | Fuente expresiva en Display (`H1-H2`) + fuente funcional en UI/Body (`H3-Body`), comparadas morfológicamente | Requiere validación de la combinación | *Fraunces* (Display) + *Plus Jakarta Sans* (Body); *Space Grotesk* + *Inter* |

#### Cómo ejecutar la Prueba Morfológica MEGATYPOS (Nivel 3)

Cuando combines dos familias de distintos autores (prueba de palabra muestra; antes de citar autoría, verifícala en una fuente confiable):

1. Escribe la palabra **`MEGATYPOS`** (en mayúsculas) y **`megatypos`** (en minúsculas) al mismo tamaño (`48px`) con ambas fuentes lado a lado.
2. **Compara el Esqueleto de Mayúsculas (`M`, `E`, `G`, `O`, `S`)**: Busca contraste deliberado de estilo (ej. Serif transicional vs. Sans geométrica) y coherencia en proporción ancho/alto, salvo que una diferencia extrema sea una decisión editorial intencional.
3. **Compara Altura-x y Aberturas en Minúsculas** (`e`, `g`, `a`, `y`, `p`, `o`, `s`): Si ambas fuentes pueden coexistir en la misma línea o bloque cercano, evalúa si sus alturas-x son compatibles o pueden normalizarse en CSS con `size-adjust`. Evita el conflicto de casi-igualdad si no es una decisión deliberada.

## Missing or Conflicting Information

- Si el usuario pide una fuente decorativa o de bajo contraste para cuerpo de texto largo o tablas de datos, explica el costo posible para legibilidad y propone reservarla para `H1`/`H2` si encaja, con una fuente más legible para cuerpo.
- Si no se especifica presupuesto de licencias, trata las fuentes abiertas como una preferencia/candidatura posible; verifica la licencia de cada fuente elegida y ofrece alternativas pertinentes sin asumir permisos.

## Output Contract

Entrega una especificación de **Selección y Emparejamiento Tipográfico** (`design-system/02-typography-selection.md`) que contenga:

1. **Tabla de Asignación por Rol**: `Display/Headline` (*Feeling*), `Body/UI` (*Function*) y `Monospace/Data` (si aplica), justificando cada elección.
2. **Matriz de Requisitos Locales**: Pesos/estilos requeridos, glifos/idiomas requeridos, función tabular cuando los datos necesiten alineación, formato/ejes si aplican y licencia. Marca cada elemento como verificado con referencia a su fuente, no requerido o no verificado.
3. **Validación de Emparejamiento**: Nivel 1, 2 o 3 cuando aplique; en nivel 3, análisis de proporciones, contraste estilístico y compatibilidad de `x-height` con MEGATYPOS.
4. **Configuración CSS de Carga y Features OpenType**: Reglas `font-family` con *fallback stack* métrico. Activa `font-variant-numeric: tabular-nums` solo para datos que requieran alineación y features adicionales solo cuando la fuente seleccionada las soporte.

## Common Mistakes

- **Mezclar dos fuentes de la misma categoría sin contraste**: Emparejar *Inter* en titulares con *Helvetica* o *DM Sans* en cuerpo puede generar disonancia sin aportar jerarquía.
- **Aplicar `tabular-nums` indiscriminadamente**: Úsalo solo cuando el contenido numérico necesite alineación; documenta la decisión.
- **Elegir formato o ejes sin comprobarlos**: Variable WOFF2 puede ser una buena opción cuando convenga, pero no sustituye verificar los pesos, características y carga local necesarios.

## Verification

- [ ] Se separó explícitamente el rol *Font Follows Feeling* (Display) del rol *Font Follows Function* (Body/UI).
- [ ] Los pesos/estilos y glifos requeridos localmente se comprobaron con fuentes citadas; los no comprobados se marcan no verificados.
- [ ] `tabular-nums` se evaluó solo si hay datos que requieren cifras alineadas; si no, se indica que no es necesario.
- [ ] La selección de variable/estática se justifica por el contexto; cualquier uso declarado se apoya en archivos y fuentes consultadas.
- [ ] La licencia de cada fuente seleccionada se verifica con evidencia citada, o se marca no verificada.
- [ ] El sistema utiliza como máximo 2 familias principales (más 1 Monospace opcional) y explica el nivel de combinación aplicado.
