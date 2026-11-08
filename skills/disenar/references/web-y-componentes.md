# Web y componentes

## Conserva el resultado solicitado

Usa esta referencia para componentes, bloques, páginas o webs completas. Determina qué debe quedar utilizable y en qué entorno: un componente integrable, una página funcional, una aplicación o un prototipo con alcance explícito. Conserva la acción del encargo; auditar no implica modificar el objeto revisado.

Respeta stack, biblioteca elegida, dependencias excluidas y requisitos de originalidad. Un pedido de HTML y CSS sin dependencias puede resolverse directamente con implementación propia. Una biblioteca requerida no se sustituye silenciosamente por otra. Si detectas incompatibilidad, explica el conflicto concreto y resuelve la decisión dependiente; continúa lo que no dependa de ella.

## Descubre lo suficiente para producir

Lee el contexto pertinente: puntos de entrada, componentes vecinos, estilos, tokens, datos, convenciones, rutas y herramientas disponibles. Evita explorar todo el repositorio para un cambio local. Identifica marca y contenido desde evidencia del encargo; no presupongas una marca, fuente, framework o banco habitual.

Si debes seleccionar recursos, compara adecuación funcional, compatibilidad, semántica, estados, personalización, mantenimiento, condiciones de reutilización y coste de integración. Incluye creación original cuando sea razonable. Usa cualquier catálogo como fuente opcional de candidatos. Consulta documentación primaria vigente para las APIs y versiones que vayas a utilizar; termina la investigación cuando permita decidir y construir.

## Define la conducta antes del acabado

Prefiere elementos HTML nativos cuando expresen la acción y el comportamiento requeridos. Para controles personalizados, consulta el patrón pertinente de WAI-ARIA APG y concreta teclado, foco, nombre accesible, roles, estados y cierre. Añadir un rol no implementa su conducta. Los ejemplos de APG requieren comprobar interoperabilidad en el entorno objetivo; no acreditan accesibilidad por copia.

Define entradas, salidas y estados según el alcance. Incluye estados vacío, carga, éxito, error, deshabilitado o selección cuando existan realmente. Aclara qué se conserva al cambiar estado y cómo se recupera una operación fallida. Mantén coherencia entre control visible, acción y resultado.

Para una web completa, completa también contenido, navegación y flujos incluidos en el pedido. No dejes botones aparentes sin comportamiento ni enlaces de relleno como si fueran terminados. Si un prototipo simula un servicio, delimita esa simulación en la entrega. No inventes testimonios, resultados o datos reales para completar el diseño.

## Compón e implementa

Organiza jerarquía, agrupación, ritmo, tipografía y color según tarea, contenido y dirección elegida. Conserva decisiones existentes salvo que el encargo autorice cambiarlas. Distingue normas verificables, convenciones del proyecto y heurísticas; una preferencia estética no obliga a rediseñar una pieza que ya cumple su función.

Construye con contenido real disponible o fixtures representativos identificados como tales. Si el diseño requiere recursos originales, prodúcelos mediante las capacidades disponibles y en el formato pedido. Integra assets con dimensiones, alternativas y condiciones de uso pertinentes.

Expón una interfaz de componente proporcionada: propiedades, eventos, estados y variantes que el consumidor necesite. Evita convertir un caso concreto en un sistema abstracto sin necesidad. Mantén estilos y efectos acotados, libera recursos y preserva contratos de integración. Registrar o publicar en una biblioteca solo forma parte del trabajo cuando el encargo lo incluye.

## Comprueba contenido, espacio e interacción

Prueba dentro del contenedor real, además de los tamaños de pantalla pertinentes. Revisa estrechamiento, ampliación, zoom y cambios de texto sin ocultar información esencial o volver inalcanzables las acciones. Considera teclado, puntero y touch según el uso; conserva foco visible y orden de lectura coherente.

Usa datos adversos plausibles por la misma entrada que utiliza el componente: texto largo y corto, valores faltantes, pluralización, Unicode, números y listas vacías, unitarias o extensas. Apóyate en límites del esquema cuando existan. Decide por campo si corresponde envolver, truncar o mostrar detalle; verifica que la información necesaria siga disponible.

Comprueba las interacciones y los estados afectados. Revisa contraste en pares y fondos concretos, semántica y requisitos de accesibilidad aplicables. Si existe motion, conserva un único productor del artefacto y consulta los criterios de movimiento. Una captura sirve para inspección visual, no demuestra teclado o comportamiento.

## Cierra de manera proporcional

Entrega archivos integrables o ejecutables y las instrucciones mínimas necesarias para usarlos. Para una web, identifica la entrada funcional y los flujos completados. Publica solo si esa acción forma parte del encargo. Una especificación o tokens aislados no completan una pieza funcional pedida.

Ejecuta las comprobaciones pertinentes disponibles y revisa el resultado renderizado cuando puedas. Separa compilación, prueba funcional, inspección visual y dispositivos. Informa evidencia, alcance y pendientes con los estados del contrato; no anuncies cumplimiento global desde un chequeo parcial. Un cambio pequeño requiere comprobaciones focalizadas, sin añadir una batería que solo repita su implementación.

## Procedencia

Síntesis propia informada por la [guía de prácticas ARIA](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/) y las prácticas de exploración y datos adversos de [Emil Kowalski](https://github.com/emilkowalski/skills/tree/2d228630ba1446365f614a108cb8252f1feda202). Consulta [fuentes.md](fuentes.md) para procedencia completa. Ninguna biblioteca citada es una dependencia de esta capacidad.
