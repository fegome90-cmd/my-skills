# Pruebas pendientes de disenar

23 de octubre de 2026. Fuente evaluada: `fegome90-cmd/my-skills`, commit `09eec73a305b096e3f4da1ba121fb38a60371344`. Los doce archivos del paquete conservaron sus bytes, con digest de inventario `43408fe0c1b256ed91703b8c5139e568e6c6130a2bfe37629ff67be475000385`.

Se ejercitaron los siete escenarios que estaban sin ejecutar, los dos que solo tenían revisión de alcance y la frontera de exportación raster de PowerPoint. Los resultados acreditan producción, comprobaciones de fuente y lógica, compilación o render vectorial según la fila. **La validación completa sigue incompleta: no hubo render web ni interacción nativa, y la skill no aparece en el catálogo del host.** No se fusionó el PR ni se modificaron los repositorios de componentes.

## Resultados por escenario

| Caso | Resultado comprobado | Límite material |
|---|---|---|
| D02 · Vue existente | Selector con primitivas conservadas; Vue 3.5.22 real y local. Carga, vacío, error con reintento, deshabilitado y texto largo. 15 comprobaciones de runtime/compiler/lógica y 40 de sintaxis, recursos y pares de contraste: PASS | Sin montaje DOM real, teclado, popup nativo, foco o responsive |
| D05 · Recurso incompatible | Radix React Select 2.2.6 declara React/ReactDOM y los importa. Análisis completo, proyecto intacto y sin sustitución silenciosa: PASS de la respuesta de frontera | Integración BLOCKED con el requisito heredado «sin React». Mantener Vue por sí solo sí permite una isla React, que requeriría aceptar ambos runtimes y un adaptador |
| D06 · Banco solicitado | Tarjeta REA, entrada de registro, preview, miniatura y fixture. Lint, tipos, 19 suites/260 pruebas, build, generación de 109 ítems y validación shadcn: PASS. Cinco archivos de delta; dependencias intactas | Copia aislada del commit fijado de ui-kit. La pieza conserva `candidate`; render de tests en jsdom y build no prueban revisión visual ni navegación real |
| D07 · Banco ausente | Tarjeta HTML/CSS/JS sin dependencias ni banco requerido; datos sintéticos, contenido completo/mínimo/extenso, guardado en memoria y detalles. Sintaxis, recursos, enlaces y nueve pares de contraste: PASS | Comportamiento implementado, sin interacción nativa observada |
| D09 · Motion en deck | Revelado de tres etapas integrado en la segunda lámina. Avance, reversa, límites, reinicio y atajos: 22 observaciones de estado/eventos PASS con doble de DOM. Láminas 1 y 3 idénticas y salida estática completa | No se reprodujeron transiciones, foco ni cambio de movimiento reducido en navegador |
| D10 · Frontera raster | Copia real de ocho slides compuesta por imágenes, con ocho notas, rechazada por el validador de editabilidad. El control nativo conserva texto y conectores: PASS de detección negativa | Prueba sobre OOXML; no se abrió Microsoft PowerPoint ni se afirma aceptación de un exportador real concreto |
| D11 · Gráfica original | Maestro SVG `currentColor`, variantes negra/blanca, estructura sin raster incrustado, alfa coincidente, edición de geometría y rerender: PASS. Contacto visual MuPDF a 16/24/48 px inspeccionado; contorno, pliegue y barra distinguibles a 24 px | Fixture de app «Pliego» para guardar pasajes. No demuestra reconocimiento con personas ni exclusividad marcaria |
| D14 · Solo guion | Guion y notas sin producir slides. 565 palabras, estimación de 5:00 a 120 ppm y 17,5 s de pausas; supuestos y rango declarados: PASS del alcance | Sin ensayo cronometrado |
| D15 · SQL sin objetivo visual | Duplicación JOIN 1:N reproducida; `EXISTS` produce una fila por taller, incluyendo talleres con nombres iguales. Seis casos SQLite: PASS; sin expansión visual | Datos sintéticos; no prueba activación automática ni rendimiento de producción |
| D16 · Auditoría de skill | Informe separado, lint OK/0 hallazgos, helper de contraste ejecutado, doce archivos intactos y sin instalación: PASS de ejecución del encargo | La auditoría local conserva su propio gate INCOMPLETE por cotejo externo completo no realizado y host no observado; no certifica preparación universal |

D02, D06, D07 y D09 se ejecutaron sobre fixtures de desarrollo preparados para estas condiciones, no sobre productos de producción de Felipe. Los casos se realizaron con contextos nuevos y procedimiento explícito, mismo entorno y filesystem compartido. Los workers conocían que era una prueba de desarrollo. No fue una evaluación ciega ni una comparación causal con trabajar sin la skill. Los contadores de lint, casos de lógica y suites existentes se informan por separado: no equivalen a ese número de encargos de diseño aceptados.

## Hallazgos conservados y correcciones

- En la primera tarjeta REA, la prop `role` colisionaba con el atributo ARIA nativo. Se corrigió a `occupation` y pasaron las comprobaciones finales. Se conserva la incidencia en `cases/bank-attempts.json`.
- El primer lint de la copia del banco también encontró metadatos de investigación que no pertenecían al árbol upstream. Se retiraron solo del árbol ejecutable; se distinguió esa incidencia del código del componente. Una caché npm incompleta requirió resolver dependencias con el lockfile existente, sin cambiarlo.
- Se corrigieron rutas internas de los scripts de repetición: selector explícito de candidato para la auditoría, `--skill` para contraste y rutas relativas en el compacto del banco. Los logs anteriores y las revisiones se conservaron. El replay desde una extracción temporal pasó diez grupos de checks, con fuente del candidato intacta.
- No apareció un defecto que exigiera modificar el procedimiento de `disenar` dentro del alcance probado. Esto no acredita todas sus combinaciones de medios, bibliotecas o hosts.

## Integración que continúa pendiente

**Navegador: BLOCKED.** Chrome cloud fue observado mediante la superficie admitida. El servidor local devolvió `ERR_CONNECTION_REFUSED`; el runtime del navegador no comparte el filesystem de trabajo. La transferencia del fixture conservó su hash, pero la navegación a `data:` fue rechazada por la política del navegador, que admite HTTP/HTTPS. No se usó otra superficie para eludirla. Por eso no existen capturas de la app funcionando ni evidencia nativa de teclado, responsive, zoom, foco, reproducción temporal o preferencia de movimiento reducido. El servidor Next de la copia REA además encontró `uv_interface_addresses` en el entorno. Las sesiones de prueba se detuvieron.

**Host: registro BLOCKED y activación NOT_RUN.** La consulta completa mediante `skills.list` revisó 318 entradas executor y 250 cloud y no encontró `disenar`. Es evidencia de ausencia en esos catálogos de esta sesión, no una prueba de todos los posibles destinos de instalación. Se preserva el rechazo anterior de escritura bajo `/root/.codex`; no se volvió a intentar ni se instaló por otra vía. Cargar la ruta local de la skill para estas pruebas no equivale a activación automática.

**Personas, hardware e impresión: NOT_RUN.** No hubo participantes, mediciones de atención/reconocimiento, dispositivos físicos, impresión física, interfaz de Word/PowerPoint ni comparación causal. No se presentan como requisitos universales para cada uso de la skill. Simplemente continúan sin evidencia donde el informe anterior los mencionaba.

El [gate de este seguimiento](gate.json) conserva INCOMPLETE porque las comprobaciones obligatorias de navegador e invocación del host siguen pendientes. El resultado histórico de creación y su alcance no se reescriben. La [auditoría local](cases/audit-gate.json) también conserva su propio resultado limitado; la procedencia ya documentada en la revisión inicial se mantiene como evidencia histórica, sin convertirla en un cotejo nuevo de todas las fuentes externas.

## Archivos y repetición

- `evidence.zip`: fuentes, fixtures antes/después, deltas, scripts, licencias y logs seleccionados. `BUNDLE_MANIFEST.json` identifica los 234 archivos efectivamente incluidos. No contiene node_modules ni copias completas del banco. Los manifiestos originales de workers pueden mencionar archivos intermedios más amplios, como tarballs descargados; el manifiesto del bundle gobierna los bytes distribuidos.
- `cases/`: resultados principales legibles sin extraer el archivo. Los artefactos internos que describen conservan sus rutas originales dentro del bundle.
- `source-integrity.json`, `candidate-lint.json`, `host-discovery.json`: identidad del candidato, comprobación local y lectura soportada del host.
- `case.json`, `report.json`, `gate.json`: normalización posterior de los criterios y evidencias de desarrollo. El contrato y plan previos quedan conservados dentro del bundle. No se presentan como preregistro independiente.
- `replay.py` y `replay-results.json`: repetición real en directorio temporal; diez grupos PASS y candidato intacto. Requiere Python, Node, PyYAML, PyMuPDF y Pillow ya disponibles. No instala dependencias ni usa red. No ejecuta navegador ni cambia el registro de skills.

Desde la raíz de un checkout del PR:

```sh
python3 evaluations/disenar/2026-10-23/followup/replay.py --skill skills/disenar --output /tmp/disenar-replay.json
```

La compilación completa del banco tiene su reconstrucción independiente desde `4ae9b6e04afbfa50f5a9196a6a0d35d5458d8ec4`; las instrucciones están en `followup/bank/README.md` dentro del bundle. Valida 174 preimages y escribe una copia nueva. Sus 260 pruebas y build quedaron ejecutados y registrados durante este seguimiento; el replay offline de diez grupos no los vuelve a contabilizar.

Para cerrar la integración faltan un origen HTTP/HTTPS alcanzable y admitido por el navegador para estas piezas, y una instalación de la skill mediante un mecanismo soportado con lectura e invocación posterior. El PR permanece en borrador.
