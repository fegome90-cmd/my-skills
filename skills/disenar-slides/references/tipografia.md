# Tipografía para slides

En una slide la tipografía hace casi todo el trabajo de jerarquía. Se lee a varios metros y por pocos segundos, así
que los tamaños son mucho mayores que en web y los textos mucho más cortos.

## 1. Escala para proyección

Medidas a 1920×1080. Usa **una razón** para generar la escala; **1,333 (cuarta justa)** da saltos claros con pocos
niveles, que es lo que necesita una slide. Usa 1,25 (tercera mayor) solo en slides densas de consulta (respaldo,
anexos).

| Rol | Tamaño de partida | Peso | Interlineado | Uso |
|---|---|---|---|---|
| Display | 96–144 px | 700–800 | 0,95–1,05 | Dato grande, portada, sección |
| Título | 56–72 px | 700–800 | 1,05–1,15 | Afirmación de la slide |
| Subtítulo / lead | 32–40 px | 400–500 | 1,25–1,35 | Una frase de apoyo |
| Cuerpo | 28–32 px | 400–500 | 1,35–1,45 | Viñetas, textos de tarjeta |
| Etiqueta / fuente | 20–24 px | 500–700 | 1,3 | Eyebrow, notas, citas de fuente |

**Mínimo absoluto: 18 px a 1080 de alto** (1/60 de la altura). Por debajo no se lee proyectado; si un texto
«necesita» ser más chico, no va en la slide (va en la nota del orador o en una slide de respaldo). El script de
revisión marca cualquier texto bajo ese umbral. En la versión móvil vertical de una slide responsiva (que no se
proyecta) el piso es 12 px.

Implementación: define la escala como tokens (`--text-display`, `--text-title`, `--text-lead`, `--text-body`,
`--text-label`) y úsalos en todas las slides. En slides responsivas, escribe cada token con
`clamp(mínimo, valor-fluido, máximo)` donde el máximo es el valor de la tabla y el mínimo respeta el umbral de
legibilidad del viewport más chico que se proyecta.

## 2. Niveles por slide

**Máximo tres tamaños de texto por slide** más una etiqueta. Cuatro o más tamaños hacen que ninguno mande. Si
parece necesitar más, hay dos ideas en la slide.

## 3. Largo de línea

- Cuerpo: **35–60 caracteres por línea** (`max-width: 30–34ch`). Es más corto que en web (50–75) porque el lector
  está lejos y lee en ráfagas.
- Título: **máximo 2 líneas** (unos 40 caracteres por línea). Si no cabe en dos, la afirmación es demasiado larga:
  reescríbela.
- Evita viudas (una palabra sola en la última línea del título): `text-wrap: balance` en títulos y
  `text-wrap: pretty` en párrafos.

## 4. Combinación de familias

Tres niveles de madurez (Misterek, OKF-137/151):

1. **Una familia** variando peso y tamaño. Segura, siempre válida.
2. **Superfamilia**: sans + serif + mono del mismo autor (DM, Source, Roboto, IBM Plex). Contraste sin choque;
   comprueba igual la altura de x y el ancho.
3. **Fuente ancla del titular**: elige primero la fuente del título (define la personalidad) y luego una de cuerpo
   con **contraste claro de estructura o ancho** (por ejemplo serif condensada + sans ancha).

Reglas:

- Máximo **dos familias** por deck (más una mono para código o datos si hace falta).
- Nunca dos familias casi iguales (Georgia + Times): parece un error, no una decisión.
- Máximo **tres pesos** en todo el deck.
- Fuentes display o script solo en textos breves (unas 7–10 palabras).
- Las fuentes deben estar alojadas localmente o con licencia clara; documenta cuál y de dónde sale.

## 5. Ajustes finos

- **Tracking**: titulares grandes, ligeramente negativo (−0,01 a −0,03 em según la familia). Cuerpo, sin tocar.
  MAYÚSCULAS y etiquetas: positivo (+0,06 a +0,12 em), porque las mayúsculas sin espacio extra se apelmazan.
- **Cifras**: `font-variant-numeric: tabular-nums` en tablas, contadores y cifras que se comparan; numeración de
  secuencias con dos dígitos (01, 02…) cuando el perfil lo usa.
- **Énfasis**: color de acento o peso, uno solo a la vez. Sin subrayado (se confunde con enlace) y sin cursiva en
  textos proyectados largos.
- **Mayúsculas**: solo para etiquetas cortas. Un título en mayúsculas se lee más lento.
- **Comillas y signos**: tipográficos («», “”, —, …) y en el idioma del deck.
- **Jerarquía por opacidad** (100 / 87 / 70 / 60 %): úsala solo después de comprobar el contraste del color
  resultante sobre el fondo real (ver `color.md`). Es una referencia histórica de Material Design, no una garantía
  de legibilidad.
