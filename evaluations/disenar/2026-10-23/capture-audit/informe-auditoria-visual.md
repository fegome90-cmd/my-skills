# Auditoría visual de «Agenda de talleres»

**Fecha de revisión:** 23 de octubre de 2026.  
**Estado del encargo:** completo como auditoría de una captura estática.  
**Objeto:** [captura.png](sandbox:/workspace/scratch/cbc1d7005c48/research/final-validation/capture-audit/captura.png), PNG RGB de 1200 × 720 píxeles.  
**Resultado:** informe de problemas observables y recomendaciones; no se ha corregido ni publicado la interfaz.

## 1. Conclusión y prioridades

Priorizaría **hacer comprensibles los estados y devolver legibilidad a las acciones**. La columna «ESTADO» muestra únicamente puntos de color, sin indicar qué significan. «Crear taller» y los cuatro «Ver» tienen una apariencia muy tenue; los pares de píxeles examinados presentan contrastes de aproximadamente 1,45:1 y 1,70:1, respectivamente. Esto justifica revisar su presentación, aunque la captura no permite determinar si son controles habilitados o deshabilitados.

La composición tiene una base aprovechable: el título se distingue del resto, las cuatro filas están alineadas y separadas, los nombres de las actividades y las fechas son legibles y no se observan recortes ni superposiciones en este encuadre. Recomiendo conservar esa estructura y actuar sobre significado, contraste y orientación.

| Prioridad | Cambio recomendado | Motivo |
|---|---|---|
| **P1 — primero** | Añadir el nombre real de cada estado junto a su indicador. | La información visible depende exclusivamente de distinguir e interpretar colores. |
| **P1 — primero** | Reforzar «Crear taller» y «Ver» cuando estén disponibles; distinguir con claridad cualquier estado deshabilitado real. | Las acciones son mucho más tenues que el contenido que permiten gestionar. |
| **P2 — después** | Aumentar el contraste de cabeceras, subtítulo y cualquier texto informativo que se conserve. | La jerarquía secundaria está demasiado debilitada en la imagen. |
| **P2 — después** | Señalar la sección activa en la navegación. | Ninguna opción se distingue como ubicación actual. |
| **P2 — condicionado al uso** | Aclarar el contexto temporal y mostrar hora o duración si esta pantalla debe permitir organizar la asistencia. | Actualmente solo se ven día y mes. |
| **P3 — ajuste de contenido** | Revisar o retirar «Próximamente: más opciones para tu equipo». | No concreta una novedad, fecha ni acción útil en esta pantalla. |

Estas prioridades son un juicio de diseño sobre la tarea representada. No se han observado bloqueos funcionales, tiempos de ejecución, abandonos ni comportamiento de personas.

## 2. Alcance y evidencia disponible

La única evidencia del producto es la imagen indicada. Se realizó una inspección visual completa del encuadre y una lectura de sus píxeles para comprobar dimensiones, colores y algunos pares de contraste. No se dispone de URL, aplicación ejecutable, HTML, CSS, diseño editable, árbol de accesibilidad, datos originales ni otras capturas.

El archivo representa una interfaz con la marca «AULA», cuatro opciones laterales, el título «Agenda de talleres», un control aparente «Crear taller» y una tabla de cuatro actividades. La fecha de captura, el dispositivo, la escala del sistema, el zoom del navegador y la vigencia respecto a una aplicación actual son desconocidos. Los 1200 × 720 píxeles describen **el archivo**, no acreditan un viewport CSS de ese tamaño.

Se aplicó el procedimiento local [disenar/SKILL.md](sandbox:/workspace/scratch/cbc1d7005c48/research/final-validation/isolated/disenar/SKILL.md), con estas referencias pertinentes:

- [Dirección y fundamentos](sandbox:/workspace/scratch/cbc1d7005c48/research/final-validation/isolated/disenar/references/direccion-y-fundamentos.md): jerarquía, tipografía, composición y uso del color.
- [Web y componentes](sandbox:/workspace/scratch/cbc1d7005c48/research/final-validation/isolated/disenar/references/web-y-componentes.md): distinguir presentación visible de comportamiento e implementación.
- [Auditoría y verificación](sandbox:/workspace/scratch/cbc1d7005c48/research/final-validation/isolated/disenar/references/auditoria-y-verificacion.md): alcance, evidencia, prioridades y estados de comprobación.

**Convención del informe:** «observación» describe lo visto o calculado; «inferencia» expresa una interpretación; los posibles efectos sobre usuarios se presentan como hipótesis. Las recomendaciones no son cambios ejecutados.

## 3. Hallazgos y cambios recomendados

### H1. Los estados carecen de significado textual visible — P1

**Observación.** Bajo «ESTADO» aparecen cuatro círculos de la misma forma: verde, naranja, verde y rosado/rojo, en ese orden. No se ve una etiqueta, leyenda u otra señal visible que explique su significado. Los centros aproximados se encuentran en x = 945, con y = 235, 317, 399 y 481.

**Inferencia y límite.** La cabecera sugiere que los colores representan estados de los talleres. No puede deducirse si significan confirmación, disponibilidad, progreso o incidencia. Tampoco puede saberse si existe texto accesible o una explicación al interactuar. Una alternativa programática, por sí sola, no resolvería la ausencia de una alternativa visual al color descrita por el criterio 1.4.1 de WCAG.[1]

**Cambio recomendado.** Mostrar el nombre real de cada estado junto al círculo o en una etiqueta. Conservar el color como refuerzo. No asignar automáticamente «confirmado», «pendiente» o «cancelado» a estos colores: el vocabulario debe proceder del producto. Si se incorporan iconos, acompañarlos de texto cuando su significado no sea inequívoco.

**Cierre verificable.** Una nueva captura debe permitir identificar el estado de cada fila leyendo su etiqueta, sin depender de reconocer el color. La comprobación con lector de pantalla requerirá la implementación.

### H2. Las acciones parecen poco disponibles por su presentación — P1

**Observación.** El control «Crear taller», en la esquina superior derecha, tiene fondo azul claro y texto apenas más oscuro. Los cuatro «Ver», a la derecha de las filas, son pequeños y muy claros sobre blanco. Su contraste muestreado es considerablemente inferior al de los nombres de actividades.

**Inferencia.** La apariencia puede sugerir controles deshabilitados. **No se ha comprobado que lo estén ni que fallen al pulsarlos.** La posible dificultad para localizar o reconocer las acciones es una hipótesis de usabilidad, no un resultado de prueba con personas.

**Cambio recomendado.** Si «Crear taller» está habilitado, darle una presentación primaria clara dentro de la paleta existente: fondo oscuro y texto claro, por ejemplo. Para el detalle de cada fila, usar un enlace o botón secundario legible; «Ver detalles» sería una etiqueta visible más explícita. La relación de cada acción con su taller debe mantenerse clara, también al definir su nombre accesible en la implementación.

Si un control está realmente deshabilitado, mantener una apariencia coherente con ese estado y explicar el requisito para habilitarlo cuando sea necesario para avanzar. No debe declararse un incumplimiento normativo de contraste de un componente inactivo solo por esta imagen: el criterio de contraste incluye una excepción para componentes realmente inactivos.[2]

**Cierre verificable.** Revisar visualmente los estados habilitado y deshabilitado reales; después comprobar activación, destino, teclado y foco en la aplicación. La captura actual solo permite valorar la presentación.

### H3. Cabeceras y textos secundarios excesivamente tenues — P2

**Observación.** «ACTIVIDAD», «FECHA» y «ESTADO» presentan poca diferencia de luminosidad respecto al fondo blanco. El subtítulo y la nota inferior también se ven muy claros sobre el fondo gris. En los pares muestreados, los valores oscilan entre 1,58:1 y 2,19:1; el detalle está en la sección 4.

**Cambio recomendado.** Oscurecer los textos informativos secundarios y mantener la jerarquía mediante tamaño, peso y espaciado. Una cabecera debe seguir siendo reconocible sin competir con el título. No hace falta aumentar el contraste de todos los elementos decorativos: las líneas separadoras ya ayudan a agrupar las filas en este encuadre, y su suavidad no constituye por sí sola un fallo.

**Cierre verificable.** Medir los colores definidos y compuestos sobre el fondo real de la aplicación. Revisar los textos al tamaño efectivo de presentación; aquí no se han recuperado tamaños ni pesos CSS.

### H4. La navegación no señala una ubicación actual — P2

**Observación.** «Resumen», «Talleres», «Participantes» e «Informes» comparten una presentación similar. No se aprecia un fondo, marcador, peso u otro tratamiento que identifique una opción seleccionada.

**Inferencia.** «Talleres» parece corresponder al contenido mostrado, pero esa relación no acredita la ruta real de navegación.

**Cambio recomendado.** Marcar la sección que corresponda con un tratamiento visible y coherente: por ejemplo, un fondo de selección más un indicador o cambio de peso. Complementarlo con el estado programático apropiado al implementar. No puede concluirse que actualmente falte `aria-current` a partir de la imagen.

**Cierre verificable.** Una captura del estado seleccionado permitirá revisar la orientación visual. La semántica deberá comprobarse por separado.

### H5. El contexto temporal es limitado — P2, condicionado al propósito

**Observación.** Las fechas son «24 oct», «25 oct», «27 oct» y «29 oct». No se ve año, hora, duración ni un encabezado de período. Las cuatro fechas aparecen en orden ascendente dentro de octubre.

**Interpretación.** Día y mes pueden bastar para un listado breve de próximas actividades. Si la tarea es planificar la asistencia o detectar solapamientos, la información visible puede ser insuficiente. No puede saberse si los datos restantes aparecen al abrir el detalle.

**Cambio recomendado.** Aclarar el período cuando exista ambigüedad, mediante un encabezado o fechas completas. Mostrar hora y duración si son necesarias para la decisión que debe tomarse en esta pantalla. Incorporar zona horaria solo si el contexto de uso lo requiere. No inventar horarios ni asociar las fechas al año de esta auditoría.

**Cierre verificable.** Confirmar la tarea principal y comprobar que el listado o su detalle ofrece la información temporal necesaria. La ausencia visible de datos está comprobada; su obligatoriedad no.

### H6. La nota inferior aporta poca información concreta — P3

**Observación.** «Próximamente: más opciones para tu equipo» es el único contenido al pie. No especifica qué llegará ni cuándo, y presenta un contraste muy bajo.

**Recomendación editorial.** Retirarla si es texto provisional o sustituirla por una información concreta y verificable cuando exista. Si debe conservarse como información del producto, hacerla legible. No añadir anuncios o fechas sin respaldo.

## 4. Medición acotada de contraste

### Método y límites

Se leyeron los valores RGB del archivo con Pillow. En regiones delimitadas de texto oscuro sobre fondos claros se tomó **el píxel más oscuro observado dentro de los trazos** y se comparó con el fondo uniforme próximo. Esto evita elegir deliberadamente un borde más claro por el suavizado. Para la navegación se tomó el color claro repetido en el interior de los caracteres sobre el fondo oscuro.

Los pares se calcularon ejecutando el helper local `disenar/scripts/contrast.py` con `--threshold 4.5`. El resultado corresponde a **dos colores sRGB opacos y uniformes**. No recupera tokens CSS, opacidades originales, fuente, escala de captura ni estados interactivos. Los valores de la tabla se redondean solo para mostrarlos; el helper comparó los valores completos.

Se usa 4,5:1 como referencia de texto de tamaño normal. WCAG contempla 3:1 para texto grande y excepciones, incluido el contenido de controles inactivos. Su documentación indica que para evaluar una interfaz deben consultarse los colores del agente de usuario o los estilos, pues el suavizado puede alterar los píxeles del texto.[2] Por tanto, los estados siguientes son **resultados de pares de colores de la captura, no dictámenes de conformidad de la aplicación**.

| Zona examinada | Color de trazo observado | Fondo | Ratio | Comparación del par con 4,5:1 |
|---|---|---|---:|---|
| «Crear taller» | `#A0B9C5` | `#CADCE4` | 1,45:1 | `FAIL` |
| Los cuatro «Ver» | `#C1C7CD` | `#FFFFFF` | 1,70:1 | `FAIL` |
| Las tres cabeceras | `#B0B7C0` | `#FFFFFF` | 2,02:1 | `FAIL` |
| Subtítulo | `#9DA8B5` | `#F1F4F8` | 2,19:1 | `FAIL` |
| Nota inferior | `#BEC5CE` | `#F1F4F8` | 1,58:1 | `FAIL` |
| Título | `#163548` | `#F1F4F8` | 11,63:1 | `PASS` |
| Nombre de la primera actividad | `#18394B` | `#FFFFFF` | 12,17:1 | `PASS` |
| Fecha de la primera fila | `#374E5E` | `#FFFFFF` | 8,70:1 | `PASS` |
| «Talleres», navegación | `#A4BDCA` | `#102939` | 7,66:1 | `PASS` |

**Muestras reproducibles.** Coordenadas en píxeles desde la esquina superior izquierda del archivo: subtítulo (487, 94); cabecera «ACTIVIDAD» (308, 171); primer «Ver» (1037, 232); «Crear taller» (1039, 54); nota inferior (270, 636). Fondos de referencia: página (270, 120), tarjeta (300, 200), botón (1030, 40) y barra lateral (5, 5).

### Opciones de color para una corrección posterior

Estas propuestas conservan la familia de azules existente. Se calcularon sus pares, pero **no se aplicaron ni se inspeccionaron en un nuevo render**.

| Uso propuesto | Texto | Fondo | Ratio calculado | Estado del cálculo |
|---|---|---|---:|---|
| Acción primaria habilitada | `#FFFFFF` | `#163548` | 12,83:1 | `PASS` frente a 4,5:1 |
| Acción de detalle sobre la tarjeta | `#18394B` | `#FFFFFF` | 12,17:1 | `PASS` frente a 4,5:1 |
| Texto secundario sobre la página | `#4F6472` | `#F1F4F8` | 5,60:1 | `PASS` frente a 4,5:1 |

Son puntos de partida que requieren revisar el resultado real, incluyendo estados, tamaño y posibles transparencias. No constituyen una nueva identidad visual aprobada.

## 5. Registro de comprobaciones efectivamente realizadas

| Comprobación / criterio | Método y cobertura | Estado | Evidencia o límite |
|---|---|---|---|
| Archivo legible e identificable | Apertura del PNG y lectura de metadatos | `PASS` | RGB, 1200 × 720; imagen inspeccionada. |
| Fuente conservada | Comparación de SHA-256 antes y después de producir el informe | `PASS` | Mismo hash indicado al final de esta sección. |
| Ausencia de recortes y superposiciones visibles | Inspección del encuadre completo y sus cuatro filas | `PASS` | No se observaron en la captura; no cubre contenido fuera de ella. |
| Estado comprensible mediante información visual adicional al color | Inspección de las cuatro celdas y del resto del encuadre; referencia [1] | `FAIL` | Solo círculos de color; no hay etiquetas o explicación visibles. |
| Identificación visual de la sección activa | Revisión heurística de las cuatro opciones laterales | `FAIL` | Ninguna se diferencia como seleccionada. No es un dictamen normativo. |
| Contraste de pares muestreados frente a 4,5:1 | Lectura de píxeles y helper local | `FAIL` | Cinco grupos por debajo del umbral; véase tabla. No implica fallo global de WCAG. |
| Contraste de los tres pares propuestos | Cálculo de colores opacos | `PASS` | Solo cálculo; falta aplicación y revisión visual del resultado. |
| Colores CSS, tamaño efectivo y excepciones normativas | Requeriría estilos y estados reales | `BLOCKED` | Solo está disponible la captura. |
| Funcionamiento de crear y abrir detalles; permisos y estado deshabilitado | Requeriría aplicación ejecutable | `BLOCKED` | No se han pulsado controles ni recorrido tareas. |
| Teclado, foco, semántica, lector de pantalla y tamaño real de objetivos de interacción | Requeriría interfaz y estructura accesible | `BLOCKED` | Los píxeles visibles no determinan área clicable ni comportamiento. |
| Reflujo, móvil, ampliación y ajustes de espaciado | Requeriría otros estados o la interfaz renderizable | `BLOCKED` | Una sola imagen; reducirla o ampliarla no sería probar responsividad. |
| Vigencia frente al producto actual | Requeriría origen o versión del producto | `BLOCKED` | No se conoce cuándo ni cómo se obtuvo la captura. |
| Usabilidad con personas, atención o comprensión real | No se realizó estudio | `NOT_RUN` | Las hipótesis de efecto no son mediciones humanas. |
| Rendimiento y tiempos de respuesta | No se ejecutó medición | `NOT_RUN` | No hay entorno operativo examinado. |
| Animación, exportación editable y publicación | Fuera del objeto y de la autorización | `NOT_APPLICABLE` | El entregable solicitado es este informe de una imagen estática. |

**Identificador de la imagen revisada y conservada:** SHA-256 `83bb261d3a5c5f90f7d47c5ed26a8a27344f2d4f74b67cc0535ff74216c81dd9`.

Los `BLOCKED` delimitan comprobaciones que no permite esta evidencia; no convierten la auditoría visual solicitada en un encargo incompleto. Tampoco los `PASS` parciales acreditan accesibilidad o usabilidad globales.

## 6. Secuencia recomendada para corregir y comprobar

1. Definir los nombres reales de los estados y mostrarlos en cada fila. Aclarar cuáles acciones están disponibles y cuáles, si procede, requieren una condición previa.
2. Ajustar contraste de acciones y textos secundarios conservando la estructura, y marcar la sección activa.
3. Confirmar la información temporal necesaria para organizar los talleres y revisar la nota inferior.
4. Inspeccionar un nuevo render para comprobar los cambios visibles. Con la aplicación disponible, añadir verificaciones de estilos, teclado, foco, semántica, destinos y comportamiento en los tamaños de pantalla pertinentes.

No se recomienda incorporar filtros, búsquedas o paginación solo por esta captura de cuatro registros: no hay evidencia suficiente de un problema de volumen. Tampoco se necesita rehacer la composición para resolver los hallazgos principales.

## 7. Fuentes de criterio

Las observaciones de contenido, composición y color proceden de la captura y de los cálculos descritos. Los criterios de auditoría proceden de las referencias locales indicadas en la sección 2. Para delimitar el alcance de accesibilidad se consultaron estas fuentes oficiales de W3C:

1. [Understanding SC 1.4.1: Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html). Criterio sobre información visual adicional al color.
2. [Understanding SC 1.4.3: Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Umbrales, excepciones y cautelas sobre el suavizado y los colores de origen.

Las recomendaciones sobre navegación, contexto temporal y nota inferior son juicios heurísticos y editoriales identificados como tales; no se presentan como resultados de investigación con usuarios.
