# Comprobaciones del plan de talleres 2027

## Estado del encargo

**Completo**, con los límites de comprobación descritos abajo. Se entrega un PPTX de exactamente ocho diapositivas, con notas en las ocho, texto y diagrama nativos y fuente reproducible en el entorno utilizado.

La dirección visual es sobria: formato 16:9, una familia tipográfica, fondo claro en las láminas de contenido y fondo oscuro en apertura y cierre. La fuente es Nimbus Sans. No se incorporaron estadísticas, resultados, marcas, imágenes ni recursos externos. El material conserva el carácter sintético del encargo.

## Alcance de la comprobación

| Criterio | Método y cobertura | Estado | Evidencia o límite |
|---|---|---|---|
| Ocho diapositivas, en el orden solicitado | Lectura del paquete OOXML y contraste con el contenido del encargo | PASS | Ocho partes de diapositivas y el contenido exigido en cada una |
| Texto como objetos editables | Inspección de los objetos nativos del PPTX | PASS | 38 formas con texto; cero imágenes y cero referencias de rasterización |
| Diagrama editable | Inspección de la tercera diapositiva | PASS | Tres rectángulos nativos y dos conectores nativos, asociados a los extremos de sus nodos |
| Edición de objeto después de importar | Importación del PPTX con Artifact Tool, cambio del texto y posición de un nodo en una copia, reexportación y lectura OOXML | PASS | El texto cambió a «Diagnóstico (comprobación)» y la posición horizontal pasó de 88 a 104 px. La entrega original no cambió |
| Notas en las ocho láminas | Lectura de las ocho partes de notas del PPTX | PASS | Notas no vacías, guía de exposición y transición en cada una |
| Guía para unos cinco minutos | Suma de los tiempos sugeridos en la fuente | PASS | 300 segundos en total. 556 palabras de texto hablado, además de tiempos y transiciones |
| Integridad del paquete | Ejecución directa del validador del host con captura completa | PASS | Código de salida 0, stderr vacío y cero hallazgos. Registro JSON con comando, stdout, stderr e informe. Solo cubre estructura y relaciones del paquete |
| Conteo, tamaño, geometría y fuentes codificadas | Ejecución directa del validador de geometría del host | PASS | Ocho láminas, 1280 × 720 px, Nimbus Sans, cero hallazgos y cero advertencias |
| Render de la entrega | Reimportación del PPTX final y exportación a PNG mediante Artifact Tool 2.8.99 | PASS | Ocho PNG a 1280 × 720 px |
| Inspección visual | Revisión individual de las ocho imágenes a tamaño completo | PASS | Contenido visible, sin recortes ni superposiciones imprevistas observadas. Diagrama y flechas legibles |
| Fuente reproducible | Ejecución completa de `source/rebuild.sh` sobre un nuevo nombre de salida | PASS | Retorno 0. Textos y notas coinciden; las ocho imágenes resultantes tienen los mismos SHA-256. Los bytes del ZIP PPTX pueden variar entre generaciones |
| Edición y reproducción en Microsoft PowerPoint | No se abrió la aplicación | NOT_RUN | La prueba de edición utilizó Artifact Tool; no se probó la interfaz de PowerPoint |
| Sustitución de fuentes en otros equipos | No se ejecutó en otro sistema | NOT_RUN | Un equipo sin Nimbus Sans podría sustituir la fuente |
| Exposición cronometrada ante personas | No se realizó ensayo ni sesión real | NOT_RUN | Cinco minutos es una estimación de guion, no una medición |
| Finalizador integrado de Presentations | Se intentó usar sin modificarlo | BLOCKED | Su llamada `spawnSync` informó `EPERM`, aunque el proceso devolvió un reporte estructural PASS. Los mismos validadores se ejecutaron directamente y pasaron |
| Exportación complementaria a PDF | Se intentó después de los ocho PNG | BLOCKED | Faltaba el módulo `#standard-fonts/Helvetica`. El PDF no se pidió y no se entrega |
| Publicación o modificación de servicios | Fuera del alcance | NOT_APPLICABLE | No se publicó ni se utilizó un servicio externo |

## Evidencia guardada

- `checks/package-integrity.json`: registro válido de 1585 bytes de la ejecución estructural directa, con comando, código de salida, stdout, stderr e informe interpretado.
- `checks/capture-empty-stdout.json`: prueba aislada del capturador ante una orden sin salida. Guarda BLOCKED y el capturador termina con código 2, sin dejar un JSON vacío.
- `checks/layout-geometry.json`: geometría, conteo y fuentes codificadas.
- `checks/content-editability.json`: contenido, notas y objetos nativos.
- `checks/editability-readback.json`: lectura de la copia modificada.
- `checks/reproducibility.json`: reconstrucción y comparación de textos, notas y renders.
- `renders/slide-01.png` a `renders/slide-08.png`: imágenes inspeccionadas.
- `source/`: fuente principal, notas, scripts de generación y comprobación.

Todos los archivos de trabajo y entrega se guardaron dentro de la carpeta autorizada `editable-deck`. No se modificó la skill ni sus referencias.

## Corrección del registro estructural

Se detectó que el registro anterior de integridad estaba vacío. Se repitió únicamente ese validador sobre el PPTX entregado y se capturó su ejecución en un JSON válido. El resultado fue PASS. Se sustituyeron las redirecciones directas de `rebuild.sh` por un capturador que conserva tanto el resultado como los fallos o salidas vacías, y se actualizó el ZIP de fuente.

El flujo completo de reconstrucción documentado arriba se ejecutó antes de esta corrección del capturador. En esta revisión solo se repitió el validador estructural y se probó el caso de salida vacía del capturador. No se volvió a generar ni renderizar el deck. El SHA-256 del PPTX se mantuvo idéntico. Los límites anteriores sobre PowerPoint, fuentes, ensayo, finalizador y PDF permanecen sin cambios.

## Archivo entregado

PPTX: `output/plan-talleres-2027.pptx`

SHA-256: `ce9132ac283d42b76ffeca5f3e2385d98d823d3f47dcc72bc7584bf3e600a389`
