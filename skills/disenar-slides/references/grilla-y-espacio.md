# Grilla y espacio

El espacio decide qué se agrupa con qué antes de que se lea una palabra. Una grilla y una escala de espaciado
eliminan las distancias arbitrarias, que son lo que hace que una slide se vea «armada a mano».

## 1. Lienzo

Elige uno de dos modos según el contexto de lectura del brief y escríbelo en el código:

| Modo | Cuándo | Cómo |
|---|---|---|
| **Lienzo fijo escalado** | Proyección y pantalla completa; la slide debe verse idéntica en cualquier pantalla. | Escenario `aspect-ratio: 16 / 9` con `container-type: size`; tamaños en `cqh`/`cqw` o en px de un lienzo de 1920×1080 escalado con `transform: scale()`. |
| **Slide responsiva** | El deck también se consulta en notebook y móvil (caso FALP). | Grilla CSS con `clamp()`; las columnas se reorganizan con breakpoints. Verificar 1920×1080, 1366×768, 1024×600 y 390 px. |

La referencia de medidas de este documento es **1920×1080**. Para otro tamaño, escala proporcionalmente a la
altura (1366×768 ≈ ×0,71).

## 2. Márgenes seguros

- Horizontal: **5–6 % del ancho** (96–120 px a 1920). Vertical: **6–9 % del alto** (64–96 px a 1080).
- Nada con contenido toca el borde salvo imágenes a sangre deliberadas. Los proyectores y algunas pantallas
  recortan los bordes, y el texto pegado al borde se percibe como un error.
- El encabezado y el pie del deck (logo, progreso, navegación) viven en franjas propias y no invaden el área de
  contenido.

## 3. Grilla de 12 columnas

12 se divide en 2, 3, 4 y 6, así que cubre todos los repartos útiles de una slide.

- A 1920: márgenes 120 px, medianil (gutter) 24–32 px.
- CSS: `grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: var(--gutter);` y cada bloque con
  `grid-column: span N`.

Repartos de partida:

| Reparto | Uso |
|---|---|
| 12 | Portada, afirmación sola, cita, dato grande |
| 7 + 5 · 5 + 7 | Texto + visual (el lado de mayor peso lleva el contenido principal) |
| 8 + 4 | Contenido + nota lateral o fuente |
| 6 + 6 | Comparación de dos opciones equivalentes |
| 4 + 4 + 4 | Tres carriles paralelos |
| 3 + 3 + 3 + 3 | Cuatro pasos o cifras |

**Máximo cuatro bloques por fila.** Más divisiones en una slide (no en una tabla) bajan los textos por debajo del
tamaño mínimo o fragmentan la atención. Si hay cinco o más elementos, agrúpalos o divide la slide.

En modo responsivo: 12 → 8 → 4 columnas. A 4 columnas casi todo se apila en una sola; dos columnas solo para grillas
compactas de iconos o cifras.

## 4. Ritmo de 8

Escala de espaciado: **8 · 16 · 24 · 32 · 48 · 64 · 96 · 128** (px a 1920). Se permite 4 para ajustes internos
de componentes pequeños.

Regla de proximidad (agrupación por distancia):

| Relación | Distancia de partida | Ejemplo |
|---|---|---|
| Dentro de un grupo | 1× (16–24) | Título de tarjeta → su texto |
| Entre grupos cercanos | 2× (32–48) | Título de slide → cuerpo; tarjeta → tarjeta |
| Entre zonas de la slide | 4× o más (64–128) | Bloque de contenido → nota al pie |

La distancia entre grupos debe ser **claramente mayor** que la distancia dentro del grupo. Si son parecidas, el ojo
no sabe qué va con qué. Los valores de la tabla son de partida (Misterek usa 16 → 32 en web); lo obligatorio es la
diferencia.

## 5. Espacio vacío

- Como orientación, entre un **30 y un 50 % del área útil** queda sin contenido. Si una slide está llena de borde a
  borde, sobra contenido, no falta espacio: divide la slide o mueve detalle a la nota del orador.
- El espacio vacío también tiene peso: un bloque pequeño con mucho aire alrededor puede equilibrar uno grande.

## 6. Alineación

- Un solo eje izquierdo para título, cuerpo y fuente dentro de la misma columna. Cada eje extra es ruido.
- Centra solo slides de un único bloque corto (portada, cita, dato grande, sección). El texto de más de dos líneas
  se alinea a la izquierda: el centrado obliga a buscar el inicio de cada línea.
- Alineación óptica: un número grande, un icono o una comilla pueden necesitar un desplazamiento de unos pocos px
  para *verse* alineados con el texto de abajo. Ajústalo mirando la captura, no las cajas.
- Las filas de tarjetas comparten la línea superior y la línea base del título, aunque el contenido tenga distinto
  largo (diseña para el texto más largo y el más corto).

## 7. Equilibrio

Una slide equilibrada no parece inclinarse hacia un lado. Tres formas válidas:

- **Simétrico**: un bloque centrado. Estable y formal; úsalo con moderación.
- **Asimétrico**: más masa a un lado compensada con aire o con un acento en el otro.
- **Diagonal**: texto pesado arriba a la izquierda compensado por un visual abajo a la derecha.

Comprueba el equilibrio en la captura reducida, no en el código.
