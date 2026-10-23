# Revisión de las correcciones del harness — PASS acotado

## Identidad y dictamen

**Base exacta:** `2df99b33479881af531bfae44e6f9dbfe3629ed2`.

**Dictamen: PASS para las tres correcciones solicitadas.** No identifiqué un falso PASS material residual en los caminos corregidos bajo la ejecución ordinaria de Python registrada. Los siete controles conservados muestran **2 PASS / 5 FAIL** en el código original y **7 PASS / 0 FAIL** en el código corregido. La repetición integrada conserva **10 PASS / 0 FAIL** y `candidate_unchanged: true`.

La revisión corresponde a los bytes de los archivos enumerados al final, preparados como overlay fuera del archivo histórico. Es una revisión de desarrollo: mismo modelo y filesystem compartidos, sin ceguera ni estimación causal. Se revisaron código, patch, manifiestos, resultados y hashes. No se volvió a ejecutar el replay ni la suite de siete controles. Solo se ejecutó el productor SVG en copias aisladas para un control válido y dos exploraciones de un posible override de CSS.

## Resultado por corrección

| Frontera | Código revisado y evidencia | Resultado |
|---|---|---|
| Contraste | `checks-contrast.py:25` propaga cualquier fila FAIL al código de salida 1. El control negativo registrado conserva ratio 1, umbral 4,5 y estado FAIL; cambia únicamente su salida de 0 a 1. El control válido conserva 12 y 9 pares sin fallos. | PASS. Se cierra el desacoplamiento entre el JSON de fallo y el resultado del proceso. |
| Variantes SVG | `produce_verify.py:50` fija expectativas separadas para maestro `currentColor`, negro `#000000` y blanco `#ffffff`, y las coteja con el atributo del path leído del SVG. El control que cambia la variante blanca a negra falla en esa comparación, con ambos valores en el error. El control normal pasa. | PASS para los atributos y artefactos que produce este generador. La comprobación ya no depende únicamente del canal alfa. |
| Frontera PPTX | `validate_deck.py:37` emite un rechazo estructurado `NATIVE_TEXT_MISSING`, con SHA256 y slide, cuando no existen runs de texto. `validate_deck.py:85` prepara la carpeta del informe. `pptx_raster_probe.py:66` ejecuta el control nativo con el mismo validador, y exige exit 0, PASS y el hash correcto; luego exige exit 1, FAIL, código semántico, hash y slide correctos para el raster. | PASS. Tanto un validador roto como un error operativo exclusivo del raster dejan de satisfacer la prueba negativa. |

Las excepciones operativas del validador ya no producen un PASS del probe: el fallo del control positivo corta el proceso; un crash en el raster sin JSON semántico provoca fallo al interpretar ese resultado. La prueba no confunde ahora cualquier salida no cero con un rechazo por editabilidad.

## Controles, independencia y trazabilidad

Los dos informes de controles registran el mismo SHA256 del contrato (`83dd1e8…`) y del script de pruebas (`2a7295e…`), y estos coinciden con los archivos revisados. Sus siete identificadores coinciden con los siete del contrato. Las expectativas conocidas —ratio 1, colores solicitados y presencia de texto nativo— son apropiadas para regresiones de estos defectos. El uso de mutaciones de fuente para introducir defectos es transparente; no constituye una evaluación general de productores desconocidos ni un conjunto de prueba independiente del desarrollo.

Los controles prueban la desaparición de los falsos PASS originales y la conservación de casos válidos. No son una prueba exhaustiva de todos los colores, formas SVG, variantes OOXML, condiciones de entorno ni fallos posibles. No se observó que la documentación los elevara a ese alcance.

La verificación paralela de aislamiento comprobó lo siguiente mediante lecturas y hashes:

- El `evidence.zip` original y la copia de integración coinciden con SHA256 `2840abdc017586e6eff6e285cc6fb8697da189f341e181d1a01b0946a9a78ff5`, también coincidente con la descarga base64 conservada.
- Los 234 archivos del manifiesto del ZIP coinciden con sus hashes.
- Los doce archivos de `skills/disenar` coinciden con `source-integrity.json`, la copia de integración y los Git blob SHA guardados de la base.
- Los 26 archivos históricos cotejados con los registros de descarga conservan sus bytes, incluidos el informe, el gate y el replay original.
- `harness-v2/history/replay-v1.py` conserva el replay original, con SHA256 `28c5ab8bfefae518d174f9ed497cced39978ddf4827becb98d5acae8fd9649a3`.
- Los cuatro `original_sha256` coinciden con sus miembros del ZIP, y los cuatro `replacement_sha256` con los scripts corregidos revisados.
- `replay.py` escribe las sustituciones solo en `TemporaryDirectory`, tras comprobar el manifiesto, los bytes originales, los reemplazos y la contención de rutas resueltas. No escribe el ZIP ni el candidato.
- La repetición corregida registra el hash del evaluador y los cuatro hashes de reemplazo que coinciden con este dictamen.

Los hashes antes/después muestran identidad de contenido del contrato y de las pruebas; por sí solos no certifican de forma independiente su cronología. La afirmación de revisión de desarrollo, sin ceguera ni causalidad, es la adecuada.

## Exploración SVG sin hallazgo material

Se sospechó que un atributo `style="fill:#000000"` podría anular `fill="#ffffff"` y dejar pasar una variante visualmente negra. Se probaron dos posiciones del atributo `style` en copias aisladas del productor, conservando el productor normal como control.

Las tres ejecuciones terminaron con PASS. Sin embargo, **las dos mutaciones también produjeron 131 píxeles completamente opacos de RGB (255, 255, 255) a 24 px**, igual que el control. Por tanto, no se obtuvo la condición defectuosa supuesta en el renderer disponible, MuPDF/PyMuPDF 1.26.6. Esto no es un contraejemplo a la corrección examinada y no se presenta como validación de CSS en navegador. El método y sus límites permanecen declarados.

Artefactos y stdout/stderr conservados exclusivamente en `reviewer-fixes/probes/`; resumen en `probes/svg-style-probe.json`. No se modificaron el overlay, el bundle ni el candidato.

## Observaciones sin efecto sobre este PASS

1. **Documentación del overlay pendiente al momento de la primera lectura.** `README.md` y `testing-pendientes.md` todavía contenían la versión histórica, sin explicar el nuevo `harness-v2/replay-results.json`, los controles 2/5 → 7/0 ni los reemplazos. Es una tarea documental para publicación, no un defecto de las cuatro reparaciones. Este informe no adjudica PASS a una actualización documental posterior.
2. **Atribución de controles mejorable.** El informe de controles registra hashes del archivo, contrato y test, pero no los cuatro hashes de scripts corregidos que ejecutó. El replay sí los registra. Añadirlos a futuras salidas haría la atribución de los controles más autónoma; los hashes actuales están fijados abajo.
3. **Ruta de salida del replay.** Existe un límite heredado: la comprobación `candidate_unchanged` precede a escribir `args.output`. Elegir deliberadamente una salida dentro del candidato podría modificarlo después de la comprobación. El comando documentado y el run revisado escriben fuera del candidato; no invalida su preservación observada.
4. **Entorno de ejecución.** Las comprobaciones existentes usan `assert`; el PASS revisado corresponde a la invocación ordinaria registrada, sin modos de optimización que eliminen aserciones. No se ensayaron esos modos ni se afirma compatibilidad con ellos.

Navegador, registro e invocación del host, resultados humanos, impresión física y Office UI conservan sus límites BLOCKED/NOT_RUN. Estos cambios no alteran el gate global INCOMPLETE ni convierten simulación o inspección de paquetes en interacción nativa.

## SHA256 de los bytes revisados

Prefijo: `publish/evaluations/disenar/2026-10-23/followup/`.

| Archivo | SHA256 |
|---|---|
| `replay.py` | `b7d77fbc35e7ccbd94579246bb054ed8c14be827207404f03944f9a31e4d756c` |
| `harness-v2/checks-contrast.py` | `b30db21bad7d0330fd2e75e684c9294915b77b1a718c82054be2f260ec13583d` |
| `harness-v2/produce_verify.py` | `eab267cdafc0b827f6595b6efff3128f2a31cf573f2430cc8ae487122c78fa0e` |
| `harness-v2/validate_deck.py` | `c3d83937d146a6fb8a613a36096548242c355d3e335efbe73bc256fc16f216fc` |
| `harness-v2/pptx_raster_probe.py` | `efff4e000bc0f74995411ef1814867af50d28b8e5bc844b6cd9fe44dc3264721` |
| `harness-v2/overrides.json` | `0f370029bb1f4754f7ef451689bc84c68eed5a14210d98e72c73d2a97661166f` |
| `harness-v2/contract.json` | `83dd1e8b09d24b4d49b8952823ff4aa96f4fe4dfd8bc3144152f109b289930fb` |
| `harness-v2/changes.patch` | `dd9e9b4e672c25cc3206d76346e42a8e39f2fb629a11a27dd12a9d5ee818b60c` |
| `harness-v2/test_oracles.py` | `2a7295e21e6f5c9e80687434e4ebf2972c8190a7488ea6fcc1e43b3b60e862f8` |
| `harness-v2/controls-before.json` | `bd9e3e5c8899900aadab739710ce229ae2d8e5586f942ed59adff3f56e8ec50e` |
| `harness-v2/controls-after.json` | `8318aa2fca717bfdeeaa44530fd38eb8a8833b4278a7127659c290e52af33dc9` |
| `harness-v2/replay-results.json` | `f33c936044ab51feccec972cda694e57017de8d3d0206e2e240b8d2417259774` |

SHA256 del resumen de probes: `22cf121b844aba9399c3311123d8d60b49879b72e1e37af8ca4be1a3d1ee3e38`.

No se usaron red, instalaciones ni GitHub. No se cambiaron archivos de fuente fuera de las copias de probe autorizadas.
