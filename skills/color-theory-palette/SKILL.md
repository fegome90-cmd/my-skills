---
name: color-theory-palette
description: "Crea desde cero el sistema de color de una interfaz: color base a partir de keywords, armonía, regla 60-30-10, rampas 100-900 (+150), temas claro/oscuro y verificación de contraste WCAG 2.2 con script incluido. Use when choosing colors, building a palette or color ramps, or defining light/dark themes. Para auditar un diseño ya terminado, usa una skill de auditoría de accesibilidad si está disponible."
license: MIT
metadata:
  author: 'Felipe Gonzalez'
---

# Color Theory, Perceptual Ramps & UX Psychophysics

## Objective

Diseñar y auditar sistemas de color completos que traduzcan la identidad emocional de un proyecto en paletas armónicas, rampas matemáticas (`100-900` + `150`), distribución espacial `60-30-10` y temas Light/Dark que respeten la psicofísica de la visión humana (principios de *The UX Book* de Rex Hartson y Pardha Pyla) y los estándares de accesibilidad WCAG 2.2 (SC 1.4.1, 1.4.3 y 1.4.11).

## Inputs and Preconditions

- **Keywords y Arquetipo**: Atributos emocionales y estructurales del proyecto (provenientes de `PRODUCT.md` o `design-system/01-art-direction.md`).
- **Color de Marca Existente (Opcional)**: Hexadecimal, HSB u OKLCH inicial si el producto ya tiene identidad visual.
- **Polaridad de Tema**: Light Mode, Dark Mode o sistema Dual-Theme adaptable (definido en `STACK.md`).

## Workflow

### Fase 1: Flujo Determinista en 3 Pasos hacia el Color Base y Armonía

1. **Paso 1 - De Keywords a Matiz Base (`Hue` en el círculo de 360°)**:
   - Asocia la psicología funcional del dominio a un rango de matiz primario:
     - *Azul (`205° - 235°`)*: Confianza clínica, banca, infraestructura, productividad.
     - *Verde / Esmeralda / Salvia (`135° - 165°`)*: Salud, finanzas positivas, sostenibilidad, calma.
     - *Violeta / Índigo (`250° - 280°`)*: IA, creatividad, profundidad cognitiva, lujo moderno.
     - *Ámbar / Naranja / Terracota (`15° - 42°`)*: Energía, hospitalidad, gastronomía, calidez táctil.
     - *Rojo / Carmesí (`345° - 12°`)*: Urgencia, pasión editorial, entretenimiento de alto impacto.
2. **Paso 2 - Modulación Perceptual HSB / OKLCH (Tint, Tone, Shade)**:
   - Nunca trabajes en RGB/HEX a ciegas; manipula **HSB** (*Hue, Saturation, Brightness*) u **OKLCH** (*Lightness, Chroma, Hue*):
     - **Tint (Matiz + Blanco)**: Subir `B` al `95-100%` y bajar `S` al `5-20%` -> Superficies de fondo suaves y badges.
     - **Tone (Matiz + Gris)**: Mantener `B` en `50-80%` y reducir `S` al `15-45%` -> Estados secundarios, bordes y superficies sofisticadas.
     - **Shade (Matiz + Negro)**: Reducir `B` al `10-35%` y subir `S` al `70-95%` -> Textos oscuros tintados y fondos en Dark Mode.
3. **Paso 3 - Selección de uno de los 5 Esquemas de Armonía Cromática**:
   - **Monocromático**: 1 solo `Hue` modulando `S` y `B` (+ neutrales tintados). Máxima sobriedad para dashboards y lectura.
   - **Analogo (`Hue ± 20° a 35°`)**: Armónico y orgánico; excelente para bienestar, naturaleza y superficies graduales.
   - **Complementario (`Hue` + `Hue + 180°`)**: Máximo contraste para separar marca de llamadas a la acción (cuidando la cromoestereopsis).
   - **Split-Complementary (`Hue` + `Hue + 150°` + `Hue + 210°`)**: Alto contraste visual sin la tensión óptica del complementario directo.
   - **Triadico (`Hue` + `Hue + 120°` + `Hue + 240°`)**: Vibrante para categorización de datos y gráficos (manteniendo 1 dominante y 2 subordinados).

### Fase 2: Regla 60-30-10 y Construcción Matemática de Rampas (100-900 + Comodín 150)

1. **Presupuesto Espacial 60-30-10**:
   - **60% Dominante (Neutrales Tintados de Superficie)**: Fondos de página, contenedores base y espacio negativo. **Prohibido usar grises muertos puros (`S = 0%`)**: inyecta siempre `2% - 8%` de saturación del `Hue` primario en la rampa de grises (frios o cálidos) para unificar la atmósfera.
   - **30% Secundario (Estructura y Elevación)**: Tarjetas secundarias, barras laterales, cabeceras, bordes y tipografía principal/secundaria.
   - **10% Acento (Foco de Acción)**: reservado estrictamente para el CTA primario, indicadores activos y puntos focales críticos. Si el color de acento supera el 10% del viewport, deja de ser un acento y se vuelve ruido.
2. **Construcción de la Rampa `100-900` + Comodín `150` (Opacidad Escalonada / Curva HSB)**:
   - Coloca el color base verificado en el paso **`500`** (o `600` si necesitas mayor contraste sobre texto blanco) y genera la escala completa mezclando sobre blanco (`100-400`) y sobre oscuro tintado (`600-900`) o aplicando esta progresión determinista:

| Paso | Rol Semántico en el Sistema | Mezcla / Opacidad sobre Base `500` | Rango HSB Orientativo (`S` / `B`) | Uso Principal en Light y Dark Mode |
| :--- | :--- | :--- | :--- | :--- |
| **`100`** | Fondo sutil / Canvas | `10%` Base + `90%` Blanco (`#FFF`) | `S: 4-10%`, `B: 98-99%` | Fondo de página o de alerta suave en Light Mode; texto primario en Dark Mode |
| **`150`** | **Comodín de Superficie (Hover/Card)** | `16%` Base + `84%` Blanco (`#FFF`) | `S: 8-16%`, `B: 95-97%` | **Paso crítico**: diferencia una tarjeta secundaria o estado `hover` sobre un fondo `100` sin saltar bruscamente a `200` |
| **`200`** | Borde sutil / Chip | `25%` Base + `75%` Blanco | `S: 15-25%`, `B: 90-94%` | Bordes de divisores, fondos de *badges* y estado `active` suave |
| **`300`** | Borde interactivo | `45%` Base + `55%` Blanco | `S: 30-45%`, `B: 82-88%` | Bordes de inputs, iconos deshabilitados, texto secundario en Dark Mode |
| **`400`** | Acento suave / Dark CTA | `70%` Base + `30%` Blanco | `S: 55-75%`, `B: 72-82%` | Color interactivo primario en **Dark Mode** (desaturado para no vibrar) |
| **`500`** | **Color Base (Ancla)** | `100%` Color Base | `S: 75-90%`, `B: 55-70%` | Identidad de marca, gráficos y acento base |
| **`600`** | **CTA Primario Light Mode** | `82%` Base + `18%` Negro (`#000`) | `S: 80-95%`, `B: 45-58%` | Botones primarios y enlaces en **Light Mode** (objetivo `>= 4.5:1` con texto blanco, **nunca asumido**: en matices claros —amarillo, cian, verde— el `600` suele quedar entre `2.3:1` y `3.4:1`; verifica con `scripts/contrast_check.py` y baja a `700/800` o usa texto oscuro) |
| **`700`** | Estado Hover de CTA | `64%` Base + `36%` Negro | `S: 82-95%`, `B: 35-45%` | Hover de botón primario, texto de acento sobre fondos `100`/`150` |
| **`800`** | Superficie elevada Dark | `42%` Base + `58%` Negro | `S: 75-90%`, `B: 20-30%` | Tarjetas y modales elevados en **Dark Mode**; texto principal en Light Mode |
| **`900`** | Fondo profundo / Tinta | `22%` Base + `78%` Negro | `S: 70-85%`, `B: 8-16%` | Canvas base en **Dark Mode**; titulares de máximo contraste en Light Mode |

3. **Verificación Calculada de la Rampa (obligatoria)**:
   - Los porcentajes de mezcla son un punto de partida, no una garantía: el contraste real depende de la luminancia del matiz. Ejecuta:
     - `python3 scripts/contrast_check.py ramp <HEX_base>` -> rampa completa con ratios contra blanco y contra `900`, e indica el primer paso apto para CTA con texto blanco.
     - `python3 scripts/contrast_check.py pair <fg> <bg>` -> ratio de cualquier par texto/fondo y umbrales WCAG que cumple.
   - Usa como CTA de Light Mode el paso que el script marque, aunque no sea el `600`.
   - Calcula el contraste sobre el HEX cuantizado que realmente se emite; el ratio mostrado con dos decimales es solo informativo y el redondeo no cambia el veredicto ni la selección del CTA.

### Fase 3: Salvaguardas Psicofísicas de UX y Accesibilidad (WCAG 2.2)

1. **Principio Grayscale-First (práctica estándar de UX: la jerarquía no debe depender del color)**:
   - Diseña y verifica primero la jerarquía completa en **escala de grises (solo luminancia)**. El color solo puede reforzar una jerarquía que ya funciona por contraste acromático.
2. **Prevención de Cromoestereopsis y Fatiga Foveal**:
   - **Nunca coloques rojo saturado junto o sobre azul saturado** (ni magenta sobre cian/verde puro): la lente del ojo humano enfoca las longitudes de onda largas (rojo) y cortas (azul) en planos distintos de la retina, produciendo una ilusión de vibración 3D (*chromostereopsis*) que causa fatiga visual inmediata.
   - **Evita usar azul puro saturado (`Hue 240°`) para texto fino o detalles pequeños**: los conos S (sensibles al azul) son una minoría (aprox. 5-10% de los conos) y están ausentes en el centro de la fóvea.
3. **Prohibición de Negro Puro (`#000000`) con Blanco Puro (`#FFFFFF`) en Dark Mode**:
   - Un contraste extremo `21:1` de `#FFFFFF` sobre `#000000` provoca **halación** (el texto blanco parece sangrar sobre el fondo negro, especialmente en usuarios con astigmatismo). Usa fondos oscuros tintados (`900` = `#0B0F17` a `#12161F`) y texto blanco suavizado (`100` = `#F1F5F9` o `rgba(255,255,255,0.90)`).
   - En **Dark Mode**, la elevación de superficies no se logra con sombras negras (que son invisibles sobre fondo oscuro), sino **aumentando la luminancia de la superficie** a medida que se acerca al usuario (`Canvas = 900`, `Card = 850/800`, `Modal/Dropdown = 750`) y reduciendo un `10-15%` la saturación de los acentos (`paso 400` en lugar de `600`).
4. **Redundancia Semántica (WCAG 2.2 SC 1.4.1) y Ratios de Contraste (SC 1.4.3 / 1.4.11)**:
   - **Nunca comuniques un estado (`Success`, `Warning`, `Danger`, `Info`) solo mediante color**: acompáñalo siempre de un **icono distintivo + etiqueta textual o patrón** para el ~8% de usuarios con deficiencia de visión cromática (deuteranopía, protanopía, tritanopía).
   - **Texto normal (`< 24px` o `< 18.66px bold`)**: Contraste mínimo **`4.5:1`** (AA) / **`7:1`** (AAA).
   - **Texto grande (`>= 24px` o `>= 18.66px bold`) y componentes UI / bordes de inputs / iconos (SC 1.4.11)**: Contraste mínimo **`3:1`**.

## Missing or Conflicting Information

- Si el usuario entrega un color corporativo claro o pastel (ej. amarillo `#FACC15` o cian `#38BDF8`) y pide usarlo en botones con texto blanco, **no apliques texto blanco ilegible**: muestra el calculo de contraste fallido (`< 2.5:1`) y ofrece dos soluciones: (a) usar texto oscuro (`paso 900`) sobre el botón `400/500`, o (b) usar el `paso 600/700` oscurecido si el texto debe ser blanco.

## Output Contract

Entrega una especificación del **Sistema de Color** (`design-system/04-color-system.md`) que incluya:

1. **Justificación Cromática y Armonía**: Mapeo de keywords -> `Hue` base, esquema de armonía elegido y presupuesto `60-30-10`.
2. **Tablas Completas de Rampas (`100-900` + `150`)**: Valores en `HEX` y `OKLCH`/`HSL` para:
   - Rampa `Primary` (y `Secondary`/`Accent` si aplica).
   - Rampa `Neutral` (tintada con `2%-8%` de saturación del matiz base).
   - Rampas Semánticas (`Success`, `Warning`, `Danger`, `Info`).
3. **Mapeo Dual-Theme (Light Mode vs. Dark Mode)**: Tabla de asignación semántica (`--surface-canvas`, `--surface-card`, `--surface-elevated`, `--text-primary`, `--text-secondary`, `--border-subtle`, `--action-primary`) para ambos modos.
4. **Matriz de Auditoría Psicofísica y WCAG**: Ratios de contraste verificados para los pares texto/fondo y validación contra cromoestereopsis, halación y daltonismo.

## Common Mistakes

- **Omitir el comodín `150`**: Sin el paso `150`, las tarjetas o filas en `hover` sobre un fondo `100` se ven demasiado oscuras si saltan al paso `200`, o invisibles si se quedan en `100`.
- **Grises puros `#808080` junto a colores ricos**: Ensucian la paleta; tinta siempre los neutrales con el ángulo `Hue` de la marca.
- **Invertir literalmente la rampa en Dark Mode**: Poner el color `600` saturado sobre un fondo `900` pierde contraste y vibra; en Dark Mode los acentos interactivos suben al paso `400` (más luminoso y menos saturado).

## Verification

- [ ] Se construyeron las rampas completas `100-900` incluyendo el paso comodín `150` y neutrales tintados (`S: 2%-8%`).
- [ ] El presupuesto espacial respeta la proporción `60% Neutrales - 30% Estructura - 10% Acento`.
- [ ] Los ratios de contraste se calcularon con `scripts/contrast_check.py` (no estimados a ojo) y el paso de CTA es el que el script valida.
- [ ] Prueba del helper (stdlib): desde este directorio, `python3 -B -m unittest discover -s tests -p 'test_*.py' -v`.
- [ ] Todos los pares de texto normal cumplen `>= 4.5:1` (WCAG 1.4.3) y los bordes/controles interactivos cumplen `>= 3:1` (WCAG 1.4.11).
- [ ] Se verificó la ausencia de cromoestereopsis (rojo/azul saturados adyacentes), se evito `#000000` + `#FFFFFF` puros en Dark Mode y cada color semántico incluye redundancia de icono/etiqueta (WCAG 1.4.1).
