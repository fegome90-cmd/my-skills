# Revisión de desarrollo de `disenar`

Esta carpeta conserva la evidencia de creación del paquete, separada de las instrucciones que consume el agente. El objetivo es disponer de un método de diseño portable que use recursos del proyecto, bibliotecas elegidas u originales sin depender de un banco, marca o framework.

## Fuente y arquitectura

La [skill](../../../skills/disenar/SKILL.md) reúne un contrato común, seis módulos por entregable, fundamentos, selección de recursos, procedencia y un helper de contraste. Se eligió una entrada común con referencias locales; una alternativa de especialistas distribuibles resolvía sus referencias mediante generación, pero añadía distribución y versionado que este uso aún no exige. Ambas admiten independencia del banco. Esta decisión documental no demuestra una ventaja de calidad, velocidad o consumo de contexto.

El inventario de [r2](candidate-r2.json) fija doce archivos. Se conserva [r1](candidate-r1.json) y el [diff](r1-to-r2.patch): la única diferencia es corregir el enlace de atribución de Impeccable a `NOTICE.md`. Raíz, referencias operativas, helper y metadatos no cambiaron; los resultados de comportamiento de r1 siguen aplicando a esos mismos bytes. Se repitieron las comprobaciones estructurales afectadas sobre r2.

## Qué se ejecutó

| Comprobación | Evidencia | Alcance |
|---|---|---|
| Estructura | [Inspector r2](candidate-lint-r2.json) | `OK`, sin findings locales; no prueba conducta ni activación |
| Copia aislada | [Resolución local](package-isolation-r2.json) | Doce archivos y catorce enlaces locales; sin bancos privados obligatorios |
| Procedencia | [Integridad de fuentes](provenance-check.json) | 20 archivos de Emil y 25 de Impeccable coinciden con sus Git blob SHA; no es prueba de sus runtimes |
| Contraste | [Doce invocaciones CLI](contrast-cli-results.json) | Límites 4,5:1, valores inválidos y códigos de salida; solo colores sRGB opacos |
| Componente original | [Panel](original-panel/README.md) | HTML/CSS/JS propio, diez pruebas de lógica con DOM y reloj simulados; navegador pendiente |
| Biblioteca elegida | [Landing](external-library/index.html) y [preservación](external-preservation.json) | Pico CSS y tema conservados; HTML sin nuevas dependencias; no se recomienda Pico como dependencia nueva |
| Cambio mínimo | [Diff exacto](minimal-change/root-check.json) | Únicamente color del texto; dos pares de contraste comprobados |
| Presentación | [PPTX](editable-deck/output/plan-talleres-2027.pptx) y [comprobaciones](editable-deck/output/COMPROBACIONES.md) | Ocho láminas/notas, objetos nativos, prueba de edición, render y reconstrucción; sin abrir PowerPoint |
| Auditoría de imagen | [Informe](capture-audit/informe-auditoria-visual.md) e [integridad](capture-audit/source-integrity.json) | Observaciones y cálculos sobre la captura; fuente intacta, sin extrapolar interacción ni atención humana |
| Revisión semántica | [Revisión con contexto fresco](semantic-review.md) | Núcleo y referencias completos; panel y auditoría; no revisión independiente de todas las rutas |
| Cierre técnico | [Caso](technical-case.json), [reporte](technical-report.json), [resultado](technical-gate.json) | Verificación de desarrollo; el helper comprueba registros y hashes, no la verdad de un juicio |

La evidencia editorial adicional y los casos no ejecutados se detallan en [observaciones de aceptación](acceptance-observations.json). El [plan original](acceptance-plan-original.json) permanece sin reescribir sus estados históricos. Los [pedidos](forward-prompts.json) y sus desviaciones se conservan aparte.

## Límites e incidencias

Se usaron contextos nuevos con el procedimiento indicado explícitamente. Las ejecuciones comparten modelo, filesystem y herramientas. No fue una evaluación ciega, una comparación con baseline ni una demostración causal de mejora. La revisión semántica identifica su propio alcance y atribuye las comprobaciones recibidas de otros revisores.

El navegador no estuvo disponible: su descarga oficial falló. La lógica simulada del panel no prueba render, teclado nativo, reflujo, lector de pantalla ni tiempo real de animación. Los casos que no se ejecutaron conservan `NOT_RUN`; una fuente válida no convierte todas las salidas posibles en verificadas.

El finalizador integrado de presentaciones falló con `spawnSync EPERM`; se ejecutaron directamente los validadores. Un registro de integridad quedó inicialmente vacío: se corrigió con captura atómica de comando, salida y exit code, y se volvió a ejecutar solo ese validador. Un PDF complementario del deck falló por un módulo de fuente ausente y no formaba parte de ese pedido. Se mantienen los límites en su informe.

La escritura en el registro interno del host fue rechazada automáticamente por la protección de `/root/.codex`. No se intentó eludirla. Esta rama contiene fuente versionada, no una instalación automática. No se modificaron los repositorios de componentes. Las piezas de prueba se conservan como evidencia en esta rama y no se desplegaron como productos. Véase [alcance de permisos](permission-scope.json).

Los informes de las ejecuciones conservan algunas rutas absolutas del entorno en que ocurrieron; son trazas de evidencia, no dependencias de la skill. Las fuentes y salidas relevantes están preservadas aquí para inspección.

## Repetición de comprobaciones acotadas

Desde la raíz del repositorio, con Python 3:

```sh
python3 evaluations/disenar/2026-10-23/check-contrast.py --skill skills/disenar --output /tmp/disenar-contrast-results.json
```

Para la lógica del panel, con Node:

```sh
node evaluations/disenar/2026-10-23/original-panel/verificar.cjs
```

Los generadores de documentos declaran su entorno en sus carpetas. Tener su fuente no implica disponer de esos productores en otro host. Las pruebas no requieren instalar el paquete en el registro de skills.
