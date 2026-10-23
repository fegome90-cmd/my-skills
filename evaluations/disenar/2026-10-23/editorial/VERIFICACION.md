# Verificación del manual del taller de ideas

## Estado del encargo

**Completo.** Se produjeron el PDF final y la fuente editable DOCX solicitados. La exportación terminó correctamente y no hay requisitos de producción pendientes.

| Entregable | Tamaño | SHA-256 |
|---|---:|---|
| `manual_taller_de_ideas.pdf` | 84 521 bytes | `96769ca511e105bc88f8f1e2a61e06060be5996188016d37c36c19485fbda64b` |
| `manual_taller_de_ideas.docx` | 39 538 bytes | `052d8a6bf789cab52c6ce6c2781bb2fdf6a96505c9d56fe8023c4dd1aebe9217` |

## Contenido y diseño

El documento tiene cuatro páginas A4 verticales. Usa texto negro, reglas grises y una sola familia tipográfica, DejaVu Sans. El texto de lectura tiene 11,5 pt. Los márgenes del cuerpo son de 20 mm a izquierda y derecha y de 18 mm arriba y abajo. El pie numerado queda a 9 mm del borde inferior.

| Página | Contenido |
|---|---|
| 1 | Objetivo, pregunta compartida, papel y lápices, preparación del espacio y propósito. |
| 2 | Ideas individuales, puesta en común sin interrupciones y agrupación de temas. |
| 3 | Comparación con el propósito, selección de una idea, prototipo sencillo y registro de ajustes. |
| 4 | Aprendizajes, siguiente paso, persona responsable, fecha y siete líneas para notas manuscritas. |

El manual no incorpora marca, estadísticas, resultados atribuidos a estudios ni fuentes externas. La redacción desarrolla las instrucciones del encargo con lenguaje cotidiano.

Se siguió el procedimiento local `disenar/SKILL.md` y sus referencias de editorial e impresión, dirección y fundamentos, y auditoría y verificación. Se consultaron también las instrucciones de producción y revisión de documentos y PDF disponibles en el entorno.

## Producción ejecutada

- Fuente DOCX: python-docx 1.2.0, con texto, estilos de párrafo, bordes de párrafo y campos de página nativos.
- Exportación: LibreOfficeDev 26.8.0.0.alpha0, mediante el productor disponible `render_docx.py`.
- Render para inspección: Poppler, a 135 ppp; cuatro imágenes de 1117 × 1579 píxeles.
- Comprobación estructural: PyMuPDF, inspección OOXML, python-docx y Pillow.

No se instalaron dependencias ni se publicaron archivos. Las salidas de producción, las copias de prueba y la evidencia se guardaron exclusivamente en el directorio autorizado para este encargo. No se modificó la skill ni se hicieron cambios en servicios externos.

## Comprobaciones y cobertura

| Criterio | Método y cobertura real | Estado |
|---|---|---|
| Cuatro páginas A4 verticales | Apertura del PDF con PyMuPDF. Las cuatro páginas miden 210,01 × 297,00 mm, con rotación 0. La diferencia de 0,01 mm respecto al ancho nominal procede de la unidad de medida del documento y está dentro de la tolerancia declarada de 0,1 mm. | PASS |
| Texto íntegro y en orden | Comparación de todos los párrafos del DOCX por etapa con el texto extraído de la página correspondiente del PDF. Se normalizaron espacios y se excluyó el pie. Coincidencia en las cuatro páginas. | PASS |
| Fuentes incluidas | Se extrajeron los siete subconjuntos de fuente referenciados en el PDF. Todos contienen un programa TrueType; corresponden a DejaVu Sans regular y negrita. | PASS |
| Escala de grises digital | Comparación de los canales RGB de todos los píxeles de las cuatro imágenes. Diferencia máxima entre canales: 0. | PASS |
| Geometría de impresión | Medición de las cajas de texto y los trazos del PDF. Distancias mínimas a los bordes: izquierda 20,00 mm, superior 17,99 mm, derecha 19,96 mm e inferior 9,00 mm. Se satisface el mínimo de revisión elegido de 8 mm. | PASS |
| DOCX con contenido nativo | Apertura con python-docx e inspección OOXML: 87 párrafos del cuerpo y 88 nodos de texto; sin archivos de imagen, sin dibujos rasterizados y sin protección de edición. Se mantienen estilos de título y encabezado. | PASS |
| Zona para notas | Conteo de siete líneas distintas bajo el rótulo Notas en la página 4, de unos 170 mm de ancho y con separación de 8,63–8,64 mm. Los trazos PDF coincidentes se agruparon para contar las líneas visibles. | PASS |
| Edición y guardado | Se modificaron en una copia un título de paso y una respuesta manuscrita vacía, se guardó y se volvió a abrir el DOCX. Los dos cambios permanecen. El hash del original no cambió. | PASS |
| Reexportación de la copia editada | LibreOffice exportó la copia de prueba. Los dos cambios aparecen en el texto del PDF y la copia conserva cuatro páginas. Se inspeccionó además la imagen de la primera página modificada. | PASS |
| Composición visual final | Se abrieron e inspeccionaron las cuatro imágenes completas tras la última exportación. Se revisaron recortes, superposiciones, glifos, jerarquía, espacio entre bloques, pies y zonas de escritura. Una segunda revisión independiente también cubrió las cuatro páginas y no observó defectos materiales. | PASS |
| Impresión en papel | No se imprimieron hojas ni se probó un modelo concreto de impresora. La revisión de área imprimible es digital. | NOT_RUN |
| Edición en Microsoft Word | No se abrió la interfaz de Word. La edición probada fue con python-docx y la reexportación con LibreOffice. | NOT_RUN |
| Accesibilidad integral | No se auditó de forma integral el etiquetado ni se utilizó un lector de pantalla. La apariencia y la estructura no se presentan como prueba de conformidad. | NOT_RUN |

## Correcciones realizadas durante la revisión

En la primera exportación se detectó una línea azul heredada del estilo de título de la plantilla. Se eliminó del estilo, se volvió a exportar y se confirmó su ausencia en el render final. También se ajustaron los tabuladores del pie para alinear la numeración a la derecha y se añadió separación entre el campo de fecha y el párrafo de cierre.

El primer recuento automático de líneas de notas contó dos veces los trazos coincidentes que emite el exportador. La comprobación se corrigió para agrupar coordenadas idénticas; las imágenes muestran siete líneas, no catorce. No fue necesario modificar el área de notas.

## Evidencia y alcance

- `qa/render/page-1.png` a `page-4.png`: render final revisado.
- `qa/verificacion_digital.json`: ocho comprobaciones automatizadas y sus medidas.
- `qa/verificacion_final.json`: registro consolidado de diez comprobaciones satisfactorias y tres no realizadas.
- `qa/editabilidad/prueba_edicion.docx`: copia con dos cambios representativos.
- `qa/editabilidad/render/prueba_edicion.pdf`: exportación de esa copia.
- `qa/editabilidad/exportacion.log`: salida del productor durante la prueba de edición.
- `produccion.py`: código de autoría del DOCX.
- `verificar.py`: comprobaciones automatizadas y preparación de la copia de edición.

Las comprobaciones descritas acreditan estos archivos y las versiones de los productores usadas. La paginación del DOCX puede recomponerse al modificar contenido o al abrirlo en otro editor sin la misma fuente. El PDF final conserva la composición verificada. Para imprimirlo, utilizar A4 vertical a tamaño real o 100 %.
