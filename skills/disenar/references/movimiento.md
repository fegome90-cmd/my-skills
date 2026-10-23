# Movimiento

## Resuelve el encargo

Usa esta referencia para crear o ajustar movimiento, o para revisar sus decisiones técnicas. Conserva la acción solicitada: una auditoría produce hallazgos; una creación o reparación autorizada produce el artefacto. Cuando el movimiento esté integrado en una web, componente o presentación, conserva al productor principal como responsable de la pieza completa.

Identifica el formato de salida, el lugar de reproducción y la editabilidad requerida. Respeta el stack, las bibliotecas elegidas y las restricciones de dependencias. Puedes usar recursos existentes, otras bibliotecas o una implementación original. No exijas un banco de componentes ni añadas una librería para resolver una transición que el entorno ya permite.

## Define qué debe ocurrir

Explica el propósito en una frase: feedback, orientación espacial, cambio de estado, explicación, expresión u otro objetivo del encargo. Registra la frecuencia de exposición como dato conocido o supuesto. Ajusta intensidad, duración y repetición al uso; no conviertas cifras de frecuencia o duración de una receta en umbrales universales.

Para cada secuencia pertinente, determina:

- Disparador y controles disponibles; activación por teclado, puntero, touch o reproducción automática cuando corresponda.
- Estado inicial, estados intermedios relevantes, estado final y salida.
- Qué sucede al repetir, interrumpir, invertir, cancelar o abandonar la interacción.
- Qué contenido y operaciones siguen disponibles durante el movimiento.
- Alternativa con movimiento reducido y representación estática si el formato la necesita.

Mantén esta especificación dentro del trabajo normal; un ajuste pequeño no exige crear documentos separados. Si falta una decisión material, resuelve esa decisión sin detener el trabajo independiente.

## Construye con continuidad

Selecciona técnica y propiedades por el comportamiento requerido. Consulta documentación primaria de la versión real antes de asumir APIs, compatibilidad o aceleración. Reutiliza tokens existentes cuando correspondan; si creas otros, asígnales roles comprensibles dentro del proyecto.

Trata curvas, springs, escalado de pulsación y tiempos sugeridos como puntos de partida. Una explicación narrativa puede necesitar pausas diferentes de una microinteracción. No impongas una estética, proveedor o prohibición general de movimiento por teclado. Conserva la relación espacial pertinente entre disparador y elemento; ajusta el origen según esa relación.

Al interrumpir o invertir, parte del estado visual y lógico vigente. Evita saltos, dobles eventos y acciones ejecutadas dos veces. Define qué ocurre cuando una secuencia recibe otra orden antes de terminar. Conserva un estado final válido tras cancelación, navegación o desmontaje.

Libera listeners, temporizadores y recursos cuando dejen de necesitarse. Coordina animaciones concurrentes para que no escriban la misma propiedad sin una regla clara. Mantén sincronizados apariencia, disponibilidad, foco y semántica: hacer transparente un control no determina por sí solo si debe seguir siendo operable.

## Conserva acceso y control

Consulta la preferencia de movimiento reducido y atiende sus cambios durante la ejecución. Si cambia mientras una animación corre, adapta o detén la secuencia de forma predecible y conserva contenido, foco y estado. La alternativa puede ser instantánea; no exijas conservar movimiento residual.

Distingue capacidades de entrada sin asumir que touch y mouse son excluyentes. Evita depender de hover para contenido esencial. Revisa activación por teclado y devolución del foco cuando proceda. Para contenido automático o repetido, aplica los requisitos pertinentes de pausa, detención y control; identifica la norma y su ámbito antes de afirmar cumplimiento.

## Comprueba lo que cambia en el tiempo

Reproduce la pieza y revisa inicio, desarrollo, llegada y salida. Según el riesgo, prueba activación repetida, reversa, cancelación, navegación y cambios de preferencia. Usa reproducción lenta o inspección temporal para localizar discontinuidades; vuelve a velocidad normal para revisar la entrega.

Si hay un problema de rendimiento, identifica primero la causa probable y registra cuando sea posible el comportamiento bajo la carga y el dispositivo relevantes. No deduzcas fluidez de una propiedad CSS o de una captura. Distingue lectura de código, reproducción observada, perfil temporal y prueba en hardware; la emulación tiene un alcance propio.

## Entrega y declara cobertura

Entrega la fuente y su integración, o el archivo de animación solicitado. Para exportaciones, comprueba reproducción, duración, dimensiones, transparencia y audio cuando sean requisitos. Una captura no sustituye vídeo, ni un vídeo sustituye fuente editable. Si falta el productor requerido, conserva lo útil y declara la salida pendiente.

Resume decisiones materiales y comprobaciones con `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN` o `NOT_APPLICABLE`. Si no pudiste reproducir, dilo; no conviertas intención o lectura estática en verificación temporal.

## Procedencia

Síntesis propia informada por las prácticas de [Emil Kowalski](https://github.com/emilkowalski/skills/tree/2d228630ba1446365f614a108cb8252f1feda202), contrastadas con [Motion: rendimiento](https://motion.dev/docs/performance). Sus recetas son referencias de oficio. Consulta [fuentes.md](fuentes.md) para revisiones, límites y normas aplicables.
