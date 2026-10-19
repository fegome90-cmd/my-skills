# Patrones de slide

Cada patrón resuelve un tipo de contenido. Elegir el patrón antes de componer evita inventar un layout por slide, y
cambiar de patrón a lo largo del deck señala que cambió el tipo de contenido.

Columnas sobre la grilla de 12 (ver `grilla-y-espacio.md`). Tamaños con los roles de `tipografia.md`.

---

## Portada

- **Objetivo**: nombrar el tema y prometer lo que el público se lleva.
- **Grilla**: 7 + 5 (título a la izquierda, elemento protagonista o índice a la derecha) o 12 centrado.
- **Tipografía**: display para el título; lead para la promesa; etiqueta para autor, fecha e institución.
- **Acento**: en una palabra del título o en el elemento protagonista.
- **Evita**: logotipos de todos los participantes compitiendo; fecha y lugar en el mismo tamaño que el título.

## Índice / agenda

- **Grilla**: lista vertical en 6–8 columnas, o 3–4 tarjetas en fila.
- **Contenido**: 3–6 capítulos numerados (01, 02…) con nombre corto. Funciona como navegación si cada ítem enlaza
  a su slide.
- **Evita**: más de seis capítulos; descripciones largas por ítem.

## Separador de sección

- **Grilla**: 12; número de capítulo grande + nombre.
- **Uso**: decks de más de 10 slides; da una pausa visual. Puede invertir el fondo (única excepción al «un solo
  modo» del deck).

## Afirmación + evidencia (patrón base)

- **Grilla**: 5 + 7 o 7 + 5. El título-afirmación y una frase de apoyo de un lado; la evidencia (gráfico, imagen,
  diagrama, tabla breve) del otro, con más peso.
- **Tipografía**: título + lead + etiqueta para la fuente.
- **Acento**: en el dato de la evidencia del que habla el título.
- **Evita**: repetir en el lead lo que ya dice el gráfico.

## Dato grande

- **Grilla**: 12 o 8 + 4 (dato + contexto).
- **Tipografía**: el número en display (96–144 px), unidad más pequeña al lado, una línea que diga qué significa y
  la fuente en etiqueta.
- **Acento**: el número.
- **Evita**: más de un dato grande por slide (para 2–4 cifras, usa *cifras en fila*).

## Cifras en fila

- **Grilla**: 4 + 4 + 4 o 3 + 3 + 3 + 3.
- **Contenido**: 2–4 cifras con la misma estructura (número, etiqueta corta). `tabular-nums`.
- **Acento**: solo en la cifra que el título destaca.

## Comparación

- **Grilla**: 6 + 6 (dos opciones) o 4 + 4 + 4 (tres carriles).
- **Contenido**: misma estructura en cada carril (mismo orden de filas) para que se compare fila con fila.
- **Acento**: la opción recomendada o el «después». En un antes/después, el «antes» va atenuado y el «después» en
  contraste pleno, y la diferencia también se dice en texto, no solo con color.
- **Evita**: carriles con distinta cantidad de ítems sin explicar por qué.

## Proceso / pasos

- **Grilla**: 3 + 3 + 3 + 3 (horizontal) o lista vertical en 6–8 columnas. Hasta 4–5 pasos; más, divide.
- **Contenido**: número grande (01–04) + verbo + una línea. Los números son el ancla visual.
- **Movimiento**: candidato natural a build progresivo si el presentador explica paso a paso.
- **Acento**: el paso actual o el crítico.

## Cita

- **Grilla**: 12 o 10 centrado con márgenes amplios.
- **Tipografía**: lead grande o título en peso regular; comillas tipográficas; atribución en etiqueta.
- **Evita**: citas de más de unas 30 palabras.

## Imagen protagonista

- **Grilla**: imagen a sangre o en 7–8 columnas; texto en el resto.
- **Contraste**: si el texto va sobre la imagen, pon una capa sólida o un degradado oscuro detrás del texto y
  verifica la captura (el script no mide texto sobre imagen).
- **Evita**: fotos de banco genéricas; la imagen debe mostrar algo del tema.

## Diagrama

- **Grilla**: 8 + 4 (diagrama + leyenda o lectura) o 12.
- **Contenido**: la forma del diagrama debe reflejar la relación real (flujo → flechas en orden; jerarquía → árbol;
  ciclo → círculo). Etiquetas dentro o junto a cada forma, no en una leyenda lejana.
- Si existe la skill `artifact-diagramming`, cárgala.

## Tabla breve

- **Uso**: solo en respaldo o cuando la comparación exacta importa. Máximo 4 columnas y 5–6 filas.
- **Tipografía**: cuerpo o etiqueta según densidad, nunca bajo el mínimo; cifras alineadas a la derecha y
  `tabular-nums`. Sin bordes verticales; líneas horizontales finas.
- **Acento**: la fila o celda de la que habla el título.

## Cierre / decisión

- **Grilla**: 12 o 7 + 5.
- **Contenido**: lo que se pide al público (decisión, siguiente paso, contacto) en una frase, y 2–3 acciones
  concretas como tarjetas numeradas.
- **Evita**: «¿Preguntas?» o «Gracias» como único contenido de la última slide; el cierre es lo que queda proyectado
  durante la conversación.
