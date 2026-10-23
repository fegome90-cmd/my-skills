# Seguimiento de pruebas pendientes

Ver [informe de testing](testing-pendientes.md), [resultados históricos normalizados](report.json), [gate](gate.json) y [revisión de los validadores](harness-v2/README.md).

Se produjeron y comprobaron los escenarios de desarrollo pendientes. Navegador e invocación automática siguen sin validar, por lo que el seguimiento conserva INCOMPLETE. Los doce archivos de la skill no cambiaron.

La revisión posterior de `2df99b3` encontró y corrigió tres vías de falso PASS en los validadores de contraste, variantes SVG y PPTX. Siete controles de regresión pasaron de **2 PASS / 5 FAIL** a **7 PASS / 0 FAIL**; los diez grupos offline volvieron a pasar con los scripts corregidos. Son resultados del harness, separados del gate global **INCOMPLETE: 15 PASS, 2 BLOCKED y 3 NOT_RUN**.

Las fuentes, fixtures, deltas y logs originales permanecen en `evidence.zip`. `replay.py` verifica el manifiesto y los hashes y aplica cuatro scripts corregidos únicamente en una extracción temporal. El [resultado actual](harness-v2/replay-results.json) identifica esas versiones. El `replay-results.json` de esta carpeta y los informes normalizados conservan la evidencia histórica del commit base; su antiguo evaluador está preservado en [history/replay-v1.py](harness-v2/history/replay-v1.py).
