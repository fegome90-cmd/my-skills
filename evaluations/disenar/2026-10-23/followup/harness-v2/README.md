# Revisión y corrección de los validadores

23 de octubre de 2026. Base revisada: [`2df99b33479881af531bfae44e6f9dbfe3629ed2`](https://github.com/fegome90-cmd/my-skills/commit/2df99b33479881af531bfae44e6f9dbfe3629ed2).

**Las tres vías de falso PASS reproducidas quedaron corregidas.** Los siete controles dirigidos pasan y los diez grupos offline vuelven a pasar. El gate global continúa **INCOMPLETE: 15 PASS, 2 BLOCKED y 3 NOT_RUN**: esta revisión mejora la fiabilidad de los verificadores, sin ampliar la evidencia a navegador, activación del host, personas, impresión física o Office UI.

Los doce archivos de `skills/disenar` conservan sus bytes. El sistema sigue alojado en `my-skills`, con bancos y bibliotecas opcionales. No se modificaron los repositorios de componentes ni el archivo histórico `evidence.zip`.

## Defectos reproducidos y reparaciones

| Hallazgo | Contraejemplo al verificador original | Corrección y alcance |
|---|---|---|
| P2 · Contraste | Un par con ratio 1 frente a un umbral 4,5 escribía FAIL, pero el proceso salía con código 0. El replay lo contaba como PASS. | `checks-contrast.py` devuelve 1 cuando existe cualquier fallo. Los 21 pares declarados actuales pasan; no se encontró un defecto de contraste en esos pares. |
| P2 · Frontera de editabilidad PPTX | El probe aceptaba cualquier salida no cero. Sustituir el validador por un `RuntimeError` producía PASS. Además, el control nativo fallaba al intentar guardar un informe en una carpeta ausente. | El validador crea la carpeta de resultados. El probe ejecuta primero el control nativo con el mismo validador y exige PASS, salida 0 y hash correcto. Para la copia raster exige salida 1 y rechazo estructurado `NATIVE_TEXT_MISSING`, con hash y slide correctos. Un crash general o exclusivo del raster falla. |
| P3 · Color de variantes SVG | Cambiar el color de la variante blanca a negro mantenía PASS: el verificador comprobaba estructura y alfa, pero no el color solicitado. | `produce_verify.py` compara el atributo `fill` del path con expectativas separadas: `currentColor`, `#000000` y `#ffffff`. El control defectuoso se rechaza. Las variantes originalmente distribuidas eran correctas. |

El rechazo histórico del PPTX raster ocurrió por falta de texto nativo. El defecto estaba en que la prueba también aceptaba errores operativos ajenos a ese requisito. Las reparaciones no convierten la inspección OOXML en una prueba de edición mediante Microsoft PowerPoint, ni la comprobación SVG en reconocimiento humano o compatibilidad CSS de navegador.

Los cambios de los cuatro scripts están en [changes.patch](changes.patch). El evaluador principal [replay.py](../replay.py) utiliza [overrides.json](overrides.json) para aplicarlos exclusivamente a su copia temporal.

## Controles de regresión ejecutados

El [contrato](contract.json) y el [script de controles](test_oracles.py) son los mismos en ambas ejecuciones; sus hashes constan en los dos resultados. Se fijaron para estos defectos durante la revisión de desarrollo. No son una evaluación ciega ni una estimación causal de la eficacia de la skill.

| Control | Original | Corregido |
|---|---:|---:|
| Contraste válido | PASS | PASS |
| Contraste inválido debe fallar el proceso | FAIL | PASS |
| SVG con variantes correctas | PASS | PASS |
| SVG blanco sustituido por negro debe rechazarse | FAIL | PASS |
| PPTX nativo aceptado y raster rechazado por el motivo previsto | FAIL | PASS |
| Validador PPTX averiado no debe aprobar el probe | FAIL | PASS |
| Crash solo para el raster no debe contar como rechazo semántico | FAIL | PASS |
| **Total** | **2 PASS / 5 FAIL** | **7 PASS / 0 FAIL** |

Los cinco FAIL iniciales corresponden a controles del verificador; no son cinco diseños de usuario fallidos. Véanse [controls-before.json](controls-before.json) y [controls-after.json](controls-after.json), con comandos, salidas y excepciones.

Además se ejecutaron los diez grupos del [replay original](history/replay-audit-v1.json) y los diez del replay corregido, ambos con resultado PASS. La diferencia se hace visible al introducir los defectos deliberados. El [replay corregido](replay-results.json) identifica el evaluador, el ZIP y los cuatro reemplazos y registra `candidate_unchanged: true`. No repite las 260 pruebas del banco: esas conservan sus logs e instrucciones de reconstrucción anteriores.

## Lo que sostiene la evidencia anterior

La lectura del seguimiento y su evidencia confirmó los siguientes alcances:

- **Vue:** las 15 observaciones combinan runtime, compilador, lógica, conservación de primitivas y comprobaciones de fuente. Las 40 comprobaciones estáticas incluyen sintaxis, importaciones, recursos y pares de contraste. Ninguno de esos contadores sustituye el montaje, foco y teclado nativos.
- **REA:** los logs registran 19 suites y 260 pruebas del banco. La pieza nueva recibe invariantes del registro y render de humo de previews/miniaturas; no incorpora pruebas nuevas de interacción específicas de la tarjeta. La corrección `role` → `occupation` es coherente en la pieza y los fixtures. Se cotejaron los cinco archivos del delta y las fuentes upstream de las pruebas en `ui-kit` commit `4ae9b6e04afbfa50f5a9196a6a0d35d5458d8ec4`.
- **Movimiento:** las 22 observaciones ejercitan el script real con un doble de DOM. Conservan el alcance de estados y eventos; no prueban transiciones reproducidas por un navegador.
- **Gráfica:** las variantes originales y su rasterización eran correctas. La revisión visual a 24 px se limita al render disponible y a la observación registrada; no acredita reconocimiento con personas.
- **Contrato y archivos:** se cotejaron las referencias de artefactos del informe, los 234 archivos del bundle y los doce archivos del candidato. La normalización posterior de casos permanece declarada como tal.

La revisión aplicó skills-manager y las pautas de pstack para probar comportamiento y corregir causas. Hubo revisión paralela de desarrollo y una lectura posterior de las reparaciones; los agentes compartían modelo y filesystem. El [dictamen posterior](review/report.md) fija hashes de las fuentes, registra los límites y no afirma haber repetido las suites que ya ejecutó el coordinador. Su exploración CSS adicional tiene un [resumen conservado](review/probes/svg-style-probe.json); no produjo un contraejemplo material en MuPDF.

## Conservación y lectura histórica

El [registro de preservación](preservation.json) identifica los doce archivos del candidato y el ZIP. Su SHA256 es `2840abdc017586e6eff6e285cc6fb8697da189f341e181d1a01b0946a9a78ff5`.

Los archivos `../report.json`, `../gate.json`, `../replay-results.json` y `../cases/` siguen describiendo el seguimiento histórico de `2df99b3`. Se mantuvieron sus bytes y sus estados. El `replay.py` de aquel commit está conservado en [history/replay-v1.py](history/replay-v1.py), con SHA256 `28c5ab8bfefae518d174f9ed497cced39978ddf4827becb98d5acae8fd9649a3`. Ese es el evaluador cuyo hash figura en el informe histórico; el `../replay.py` actual corresponde a la revisión corregida.

El replay actual verifica el manifiesto del ZIP, coteja los hashes originales y corregidos y restringe las sustituciones a su extracción temporal. Los scripts corregidos se publican como texto separado para que el diff sea revisable. El archivo ZIP no se vuelve a empaquetar y la fuente de la skill no recibe estos cambios del evaluador.

## Repetición

Desde la raíz de un checkout de esta rama, con Python, Node, PyYAML, PyMuPDF y Pillow ya disponibles:

```sh
python3 evaluations/disenar/2026-10-23/followup/harness-v2/test_oracles.py --revision original --output /tmp/disenar-controls-before.json
python3 evaluations/disenar/2026-10-23/followup/harness-v2/test_oracles.py --revision fixed --output /tmp/disenar-controls-after.json
python3 evaluations/disenar/2026-10-23/followup/replay.py --skill skills/disenar --output /tmp/disenar-replay-v2.json
```

La primera invocación sale con código 1 por los cinco controles que exponen los defectos anteriores. Las otras dos salen con código 0. No se instala nada ni se usa red. La ejecución verificada usa Python ordinario, con aserciones activas, y rutas de salida fuera del candidato. No se afirma compatibilidad con modos que eliminen aserciones ni protección frente a elegir deliberadamente una salida dentro de la fuente.

## Pendientes para cerrar la integración

1. Un origen HTTP/HTTPS alcanzable y admitido por el navegador para observar render, teclado, foco, responsive, zoom, movimiento reducido y reproducción temporal en las piezas existentes.
2. Instalación mediante un mecanismo soportado, lectura posterior del registro y casos de invocación del host que distingan uso explícito de activación automática.

La evaluación global conserva dos BLOCKED —navegador y registro— y tres NOT_RUN —activación, resultados con personas e impresión/Office—. Los dos últimos no se convierten en requisitos universales para todo encargo; continúan sin evidencia para las afirmaciones que dependerían de ellos. El PR permanece en borrador.
