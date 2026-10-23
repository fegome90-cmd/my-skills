# Auditoría y verificación

Lee esta referencia al revisar un diseño o comprobar una entrega. Elige comprobaciones que resuelvan riesgos concretos del encargo. No conviertas cada cambio en una auditoría completa ni repitas pruebas sin una incertidumbre pendiente.

## Fija objeto y alcance

Identifica archivo, revisión, ruta, pantalla, estado o exportación examinados. Aclara el resultado solicitado: una auditoría entrega hallazgos; una corrección entrega el cambio autorizado; una creación entrega el artefacto. En auditoría, conserva las fuentes intactas y escribe el informe aparte. No publiques, registres componentes ni instales dependencias como efectos implícitos de revisar.

Comprueba la vigencia de capturas y resultados previos antes de reutilizarlos. Si el código, los tokens, el contenido o el estado cambiaron, acota qué evidencia sigue siendo válida. Una herramienta disponible no implica una comprobación ejecutada.

## Separa evidencia de interpretación

Distingue lectura de fuente, cálculo, render, inspección visual, interacción y estudio con personas. Identifica el método junto al resultado; no combines sus alcances en una aprobación global.

- Describe como **observación** lo efectivamente visto o medido, con sus condiciones.
- Formula como **inferencia** una explicación apoyada en evidencia, indicando su límite.
- Presenta como **hipótesis** un efecto sobre comprensión, esfuerzo, atención o comportamiento que no se haya observado.
- Marca como **preferencia** un juicio estético o una elección de oficio contextual.

Una captura permite revisar propiedades visibles de ese estado. No prueba teclado, hover, responsividad, animación, accesibilidad integral ni atención ocular. No produzcas mapas de mirada, fijaciones o predicciones de abandono como mediciones. Un mapa de diferencias de píxeles tampoco mide atención humana. Si recorres una tarea con personas ficticias, declara revisión heurística; nunca la presentes como investigación con usuarios reales.

## Registra cobertura y resultado

Para cada comprobación material, conserva: criterio y fuente cuando corresponda, objeto/revisión, método, condiciones, cobertura, resultado y evidencia o motivo de ausencia. Una lista breve basta para cambios acotados.

| Estado | Uso correcto |
|---|---|
| `PASS` | Criterio ejecutado y satisfecho dentro de la cobertura identificada |
| `FAIL` | Criterio ejecutado con evidencia de incumplimiento |
| `BLOCKED` | Un impedimento identificado evita comprobarlo |
| `NOT_RUN` | No se ejecutó; no acredita cumplimiento ni fallo |
| `NOT_APPLICABLE` | No corresponde a este objeto o encargo; explica por qué si no resulta evidente |

Registra también qué quedó fuera: viewports, estados, reglas, motores o dispositivos. Un detector sin findings, un JSON vacío o exit code 0 no prueban que se ejecutaran todas las comprobaciones. Conserva advertencias y cobertura, verifica hallazgos en contexto y distingue falsos positivos de excepciones intencionales. No conviertas puntuaciones editoriales en garantías de usabilidad o conformidad.

## Comprueba el resultado real

Inspecciona el render o archivo exportado cuando la capacidad esté disponible. Revisa contenido, recortes, superposiciones, jerarquía, tipografía, recursos cargados y condiciones de uso pertinentes. Si solo puedes leer el código, declara esa cobertura; no inventes una inspección visual.

Prueba los recorridos afectados y estados relevantes: vacío, carga, éxito, error, deshabilitado, permisos y contenido extremo. En web interactiva, revisa teclado, foco y input aplicable. Distingue viewport emulado, gesto sintetizado, motor del navegador y dispositivo físico. Una imagen móvil no verifica un arrastre en touch.

En motion, observa disparador, secuencia, interrupción, repetición, cancelación y alternativa de movimiento reducido según el encargo. Separa suavidad percibida de rendimiento medido. En exportaciones, revisa formato, contenido, notas, número de páginas o láminas y editabilidad requerida; la extensión del archivo no basta.

## Aplica criterios de accesibilidad con precisión

Selecciona criterios aplicables al medio. Un helper de contraste limitado a colores opacos no cubre transparencia, fondos complejos ni accesibilidad general. Comprueba el par final y su contexto; no redondees un valor insuficiente para aprobarlo.

En web, prueba ampliación de texto y tolerancia a ajustes de espaciado; no declares cumplimiento por elegir `rem` o una interlínea. Distingue foco visible, foco no oculto y apariencia del foco. Consulta [WCAG 2.2](https://www.w3.org/TR/WCAG22/) para nivel, excepciones y condiciones. No anuncies conformidad global con una revisión selectiva.

## Prioriza, corrige y cierra

Ordena hallazgos por impacto en la tarea y alcance solicitado: primero bloqueos y estados engañosos, luego dificultades materiales y finalmente detalles visuales. Explica ubicación, evidencia, efecto observado o hipotético y cambio recomendado. Evita listas extensas de preferencias que oculten problemas importantes.

Cuando corregir esté autorizado, resuelve un lote coherente y repite solo las comprobaciones afectadas y las necesarias para descartar una regresión concreta. Conserva pendientes honestos si una capacidad falta. Distingue estado del encargo —completo, parcial o bloqueado— de estado de sus verificaciones. Entrega el artefacto o informe pedido con evidencia y límites proporcionados.

## Procedencia

Síntesis original informada por [Impeccable: auditoría](https://github.com/pbakaus/impeccable/blob/5cb95eea9c96479f57afe0732a45470d30183326/skill/reference/audit.md) y [cobertura de escaneo](https://github.com/pbakaus/impeccable/blob/5cb95eea9c96479f57afe0732a45470d30183326/crates/detect/tests/regex_only_note.rs). Se preserva la separación de métodos sin adoptar puntuaciones, predicciones humanas ni dependencias de su runtime.
