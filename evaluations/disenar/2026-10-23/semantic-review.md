# Revisión semántica de `disenar`

**Fecha:** 23 de octubre de 2026.  
**Tipo:** revisión de desarrollo con contexto fresco. No es un experimento ciego ni una prueba de activación automática del host.  
**Objeto:** paquete `skills-project/skills/disenar` y resultados de `original-panel/` y `capture-audit/` disponibles en esta carpeta.

La lectura corresponde a la revisión r1, anterior a la corrección documental de `NOTICE.md` anunciada por el coordinador. No atribuye a esta revisión la verificación posterior de una r2.

## Dictamen

**No he identificado fallos materiales en el procedimiento ni incumplimientos materiales de los dos encargos examinados.** El paquete permite seleccionar recursos del proyecto, bibliotecas elegidas u originales y conserva la entrega solicitada como criterio de cierre. No aparece una dependencia funcional del banco personal ni una obligación de alojar, registrar o publicar allí los resultados.

Esta conclusión se refiere a la coherencia del paquete y a la evidencia acotada de estos dos casos. No acredita producción satisfactoria en todos los medios anunciados, calidad visual del panel sin render, accesibilidad integral, instalación en otro host ni acierto de su activación automática.

Durante el cierre, el coordinador comunicó un detalle documental de la revisión examinada: el enlace de Impeccable en `references/fuentes.md` termina en `NOTICE`, mientras que su cotejo del repositorio identifica `NOTICE.md`. La referencia local efectivamente contiene `NOTICE`. Mis intentos de abrir ambos destinos mediante la herramienta web terminaron en `DisabledError`, por lo que **no presento la comprobación del destino como propia**. Es una corrección de trazabilidad comunicada por el coordinador, sin efecto observado sobre la ejecución del procedimiento o del helper. No he modificado ese enlace.

## Alcance y método reales

Leí completos `SKILL.md`, sus nueve referencias, `scripts/contrast.py` y `agents/openai.yaml`. En los dos directorios autorizados leí fuentes, instrucciones de uso, resultados y comprobadores; abrí visualmente `capture-audit/captura.png` e inspeccioné el contenido del ZIP del panel. Los pedidos exactos de ambas pruebas fueron proporcionados por el coordinador durante la revisión, porque los directorios no contenían un registro separado de esos pedidos.

No consulté diagnósticos anteriores, planes de arquitectura ni informes externos de los autores. No inspeccioné la copia del procedimiento citada por los informes bajo `isolated/`, ni otras carpetas del proyecto. La única escritura de esta revisión es este archivo.

Además de la lectura semántica:

- Reejecuté `node verificar.cjs`: **10 pruebas satisfechas, 0 fallos**. Su método es DOM mínimo y reloj simulado.
- Recalculé los diez pares de `original-panel/contraste.json` con el helper actual: coincidencia de ratios y estados en los diez.
- Comprobé que los siete archivos del ZIP coinciden byte por byte con los archivos correspondientes presentes en `original-panel/`.
- Comparé el SHA-256 actual de la captura con `input-hash.json`: coincide. Esto confirma correspondencia con el hash registrado; no constituye una observación independiente del instante anterior a la auditoría.
- Verifiqué dimensiones, modo y las nueve coordenadas de color citadas en el informe: corresponden a un PNG RGB de 1200 × 720 y a los RGB declarados.
- Comprobé la resolución de los enlaces Markdown locales del núcleo y las referencias: ninguno apunta a un recurso local inexistente.
- Ejecuté seis casos focalizados del helper: negro/blanco, colores idénticos, umbral mínimo, rechazo de alfa, rechazo de `NaN` y rechazo de un umbral fuera de rango. Los seis dieron el resultado esperado.

Consulté las fuentes primarias de Slidev y W3C enlazadas por el paquete para contrastar las distinciones de exportación y accesibilidad que podían afectar el dictamen. No ejecuté una exportación de Slidev ni validé todas las afirmaciones de procedencia o licencia de las fuentes históricas.

## Evaluación del sistema

| Dimensión | Evaluación sustentada |
|---|---|
| **Coherencia del alcance** | El núcleo separa crear, refinar, rediseñar, auditar y exportar. Las referencias conservan esa distinción y asignan la responsabilidad al artefacto final, incluyendo movimiento dentro de una web o presentación. No encontré una ruta que convierta sistemáticamente una creación en recomendaciones sin producir la pieza. |
| **Cierre por artefacto** | Web exige archivos utilizables; movimiento exige fuente integrada o archivo reproducible; presentaciones exige formato, notas y editabilidad solicitados; gráfica distingue raster de vector útil; editorial exige la salida final pedida. Las comprobaciones y especificaciones acompañan la entrega. No la sustituyen silenciosamente. |
| **Independencia y portabilidad** | Las referencias operativas son locales y relativas. El helper usa la biblioteca estándar de Python y es opcional para un caso de contraste delimitado. Los repositorios personales aparecen como procedencia, no como imports, rutas privadas obligatorias, catálogo de búsqueda forzosa o destino de publicación. Es portabilidad estructural comprobada por lectura y resolución local, no una instalación verificada en otro host. |
| **Autoridad del encargo** | Stack, biblioteca, originalidad, formato, editabilidad y exclusiones del usuario gobiernan la selección. Un recurso obligatorio incompatible requiere explicar el conflicto; un recurso opcional ausente permite continuar. El paquete subordina las recetas externas a las instrucciones superiores y al pedido, y separa auditoría de modificación. |
| **Proporcionalidad** | El procedimiento permite supuestos reversibles, pide aclaraciones solo para decisiones materiales y rechaza entrevistas, cantidades fijas de propuestas y documentos preliminares para cambios pequeños. La verificación se liga al riesgo y no obliga a repetir una batería sin incertidumbre pendiente. |
| **Capacidades faltantes** | Distingue documentación de herramienta instalada y exportación ejecutada. No promete un productor que el paquete no contiene. Exige terminar la parte posible, declarar qué requisito falta y evitar sustituciones ocultas de formato o editabilidad. |
| **Límites de evidencia** | Separa fuente, cálculo, render, interacción, tiempo y personas. Define estados de comprobación y diferencia esos estados del cierre del encargo. Las cautelas sobre contraste y capturas son consistentes con los resultados examinados. |

La distinción de presentaciones entre `pptx` basado en imágenes y `pptx-editable`, con posibles elementos o láminas rasterizados, está respaldada por la [documentación primaria de Slidev consultada](https://sli.dev/guide/exporting). La referencia exige verificar versión y resultado; no presupone que esa capacidad esté instalada.

El helper calcula luminancia y contraste de dos colores sRGB opacos, valida entradas y compara el valor completo con el umbral antes de mostrar el resultado. No intenta inferir tamaño de texto, composición de transparencias o conformidad global. Su contrato es coherente con el uso observado. La [guía de W3C para contraste](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) respalda la distinción entre umbrales, excepciones y colores de origen frente a píxeles suavizados.

## Contraste con los dos pedidos

### 1. Panel original del taller

**Pedido examinado:** crear desde cero un panel pequeño en HTML, CSS y JavaScript sin dependencias ni bibliotecas; cuatro etapas —Preparar, Explorar, Construir, Compartir—, descripción y avance; tipografía del sistema, fondo claro, texto oscuro y acento verde azulado; selección directa, secuencia, pausa, reinicio y movimiento reducido; fuente funcional y explicación de uso y comprobaciones. Se indicó que no era necesario instalar un navegador, que los archivos debían quedar en `original-panel/` y que no se publicara ni modificara la skill.

Las fuentes implementan esos elementos y controles. La página referencia únicamente CSS y JavaScript locales. La selección cambia el contenido y cancela la reproducción pendiente; pausa conserva el tiempo restante; reinicio vuelve a Preparar; completar el recorrido deja un estado estable y permite repetirlo. La lógica contempla cambios de preferencia de movimiento reducido, ocultación de pestaña y salida de página. Las reglas CSS eliminan transiciones bajo movimiento reducido. La documentación explica que reproducir continúa desde la etapa elegida y que reiniciar permite recorrer las cuatro desde el principio.

El avance representa posición de etapa y así se etiqueta en la interfaz y se explica en el README. No se presenta como progreso real de participantes. Los textos son una propuesta genérica editable, sin datos atribuidos a personas o resultados reales del taller.

Las diez pruebas ejecutadas ejercitan la lógica real de `script.js` en un contexto simulado. Las revisé antes de reejecutarlas: verifican transiciones, cancelación, tiempo restante y estados de salida, además de estructura local. Son útiles para ese alcance. **No prueban disposición visual, aplicación de CSS, comportamiento nativo del teclado, anuncios reales de tecnologías de asistencia ni temporización observada en un motor.** El README identifica exactamente esa diferencia y deja esas comprobaciones bloqueadas o no realizadas.

Por tanto, encuentro **entrega de fuente y cobertura de lógica coherentes con el pedido**, con validación visual e interactiva en navegador pendiente. No considero la falta de esa inspección una demostración de defecto funcional ni una razón para atribuirle una inspección que no ocurrió. Tampoco convierto la regla CSS de movimiento reducido en prueba de su render. Las instrucciones de uso permiten abrir la pieza y continuar la comprobación sin dependencias de producción externas.

### 2. Auditoría de la captura

**Pedido examinado:** auditar visualmente la única imagen disponible de una agenda de talleres; identificar problemas, prioridades y recomendaciones; conservar la imagen; entregar un informe Markdown en `capture-audit/` con alcance y comprobaciones efectivamente posibles; no modificar otros archivos ni publicar.

La inspección de la imagen respalda los hallazgos principales del informe: estados representados por círculos de color sin significado textual visible, acciones y textos secundarios muy tenues, y ausencia de una distinción visual de sección seleccionada. Las recomendaciones priorizan esos problemas y conservan la estructura observable. Las sugerencias sobre contexto temporal y nota inferior se presentan como condicionadas o editoriales, sin inventar horarios ni un propósito obligatorio para la pantalla.

Las muestras de píxeles citadas son reproducibles. El informe no equipara esos pares con los tokens CSS ni con un fallo global de WCAG. También contempla la excepción de controles realmente inactivos y evita inferir si los controles están habilitados. La [guía de W3C sobre uso del color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) sustenta que una alternativa programática por sí sola no resuelve la necesidad de una alternativa visual al significado del color.

La auditoría distingue lo observado de efectos hipotéticos sobre personas, no afirma haber pulsado controles, no deduce `aria-current` de una imagen y no convierte sus dimensiones en viewport CSS. Declara bloqueadas las comprobaciones que requieren aplicación o estructura accesible. Considerar completo el encargo de auditoría estática con esas comprobaciones bloqueadas es coherente: el pedido era un informe sobre la evidencia disponible. El hash actual coincide con el registrado y no se observan alteraciones atribuibles a esta revisión.

## Límites semánticos de activación

Estas son decisiones de pertinencia derivadas de la descripción y el procedimiento, **no resultados observados de un router o del host**.

| Pedido | Decisión semántica esperada | Motivo y alcance |
|---|---|---|
| «Corrige el contraste de este botón» | **Sí corresponde** | Es una corrección visual de un componente. Procede un cambio local, comprobación del par y estados afectados y explicación breve; no requiere rediseñar la página ni producir una auditoría completa. |
| «Corrige esta consulta SQL que duplica filas» | **No corresponde por sí solo** | El objetivo es corregir lógica de datos. La descripción excluye problemas exclusivamente de backend. No aparece un resultado visual que justifique aplicar este procedimiento. |
| «Audita este SKILL.md para saber si está listo» | **No corresponde** | El objeto es la calidad de instrucciones de una skill, no el diseño de una pieza visual. La descripción excluye expresamente esta auditoría. La palabra «audita» no basta para activar el dominio de diseño. |

## Qué permite concluir y qué queda abierto

La revisión respalda la coherencia del procedimiento, su independencia estructural del banco y la correspondencia de los dos resultados con sus encargos. **No quedan correcciones materiales requeridas por esta revisión.** El detalle de `NOTICE` queda identificado como corrección documental comunicada por el coordinador, con el límite de comprobación indicado.

No se han ejercitado aquí: integración en un proyecto existente, biblioteca externa obligatoria, incompatibilidad real de una biblioteca, exportación PPTX o PDF, editabilidad de objetos, animación autónoma exportada, producción gráfica original, impresión física ni resolución de un productor ausente en esos medios. Las referencias contienen instrucciones para esos casos; esta lectura no acredita sus resultados futuros.

Tampoco se ha medido fiabilidad entre ejecuciones, comparación con otro procedimiento, beneficio causal de usar la skill, calidad estética general, pruebas con personas o activación automática. Los dos casos fueron encargos de desarrollo guiados con el procedimiento local indicado. Son evidencia útil de esas rutas de trabajo, con las limitaciones descritas.

## Archivos que sustentan la revisión

- Paquete: `skills-project/skills/disenar/SKILL.md`, `references/*.md`, `scripts/contrast.py` y `agents/openai.yaml`.
- Panel: [fuente HTML](original-panel/index.html), [estilos](original-panel/styles.css), [lógica](original-panel/script.js), [comprobador](original-panel/verificar.cjs), [uso y límites](original-panel/README.md), [resultados guardados](original-panel/resultados-node.txt), [contrastes](original-panel/contraste.json) y [ZIP](original-panel/panel-taller.zip).
- Auditoría: [imagen](capture-audit/captura.png), [informe](capture-audit/informe-auditoria-visual.md), [hash registrado](capture-audit/input-hash.json) y [registro de integridad](capture-audit/source-integrity.json).
