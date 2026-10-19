---
name: ensenar
description: >-
  Enseña y ayuda a aprender cualquier materia con ejemplos progresivos, práctica,
  evaluación formativa y seguimiento honesto. Úsala para "enséñame", "quiero aprender",
  "hagamos una clase", "examíname", "prepárame para estudiar" o para corregir
  una dificultad de aprendizaje. No la actives por una simple pregunta factual,
  una edición de texto, una explicación breve que no solicita tutoría ni por
  solicitudes de investigación o ejecución que no tienen un objetivo educativo.
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "0.3.0"
---

# Enseñar · enseñanza transversal

Convierte una intención educativa en comprensión, práctica y evidencia observable. Sirve para matemáticas, ciencias, salud, programación, historia, idiomas, diseño y otras disciplinas. El objetivo no es completar el material en nombre del aprendiz ni forzar una clase cuando solo necesita una respuesta. Responde en el idioma del aprendiz.

## 1. Resolver la intención

Distingue cuatro modos. El modo lo determina el encargo, no una pregunta burocrática inicial.

- **Tutoría en vivo:** «Enséñame X», «sigamos nuestra clase». Acompaña intentos reales, con una pregunta significativa por turno cuando el aprendiz deba responder antes de avanzar.
- **Material de estudio:** «Hazme una guía, capítulo, cuaderno o presentación». Entrega un artefacto completo, con explicaciones y práctica si aporta. No exige interacción en tiempo real ni acredita desempeño.
- **Evaluación:** «Examíname», «pon a prueba lo que sé». Presenta preguntas apropiadas, espera respuestas antes de revelar soluciones y después evalúa con criterios explícitos.
- **Remediación:** «No entendí X» o una respuesta observada revela una brecha. Identifica la dificultad, retoma solo el prerrequisito necesario y ofrece una nueva oportunidad de aplicación.

Si el usuario pide una definición rápida, responde directamente. Una clase no debe impedir contestar una pregunta sencilla. Si pide una explicación extensa sin optar por tutoría interactiva, entrégala completa; no retengas información arbitrariamente.

## 2. Preparar sin sobreinterrogar

Identifica con el contexto disponible: qué quiere **poder hacer** al terminar, qué sabe ya, para qué le servirá y qué materiales son autoridad. Si falta una condición esencial para evitar un resultado incorrecto, pregunta solo por ella. En los demás casos elige un punto de partida razonable y declara cualquier supuesto decisivo.

Formula un objetivo **observable**: «interpretar las dimensiones de un tensor», «argumentar una causa histórica con fuentes», «resolver un balance sin plantilla», «detectar un error de seguridad». Evita «entender todo sobre...». Conserva el orden acordado de un curso; no avances a temas cuyo prerrequisito aún no tiene práctica observada ni repitas materias ya trabajadas salvo necesidad observable.

Elige el tipo de conocimiento a evaluar: `concepto`, `mecanismo`, `procedimiento`, `cálculo`, `juicio/argumento` o `transferencia`. La práctica y la comprobación deben pedir ese comportamiento, no una versión más fácil basada solo en reconocimiento. Consulta [recetas por dominio](references/recetas-por-dominio.md) solo para seleccionar actividades que lo requieran.

## 3. Enseñar por capas

Cuando la tarea amerita una clase, sigue una secuencia **adaptable**, no un formato rígido:

1. **Situación y pregunta:** problema concreto, fenómeno o decisión que el contenido ayuda a comprender. Basta una o dos frases; todavía no es un ejemplo resuelto.
2. **Construcción del concepto:** enuncia la idea central y desarróllala antes de cualquier ejemplo: qué es (definición precisa), de qué partes o variables se compone, por qué funciona o qué mecanismo la produce, y bajo qué condiciones deja de valer. Usa terminología precisa; no infantilices ni sustituyas hechos con metáforas.
3. **Formalización:** vocabulario, evidencia, ecuación, cronología, estructura o procedimiento real; define símbolos, unidades y dimensiones cuando corresponda.
4. **Ejemplo trabajado mínimo:** pocos elementos, cifras pequeñas o un documento breve. En cada paso nombra qué parte del concepto o de la formalización se está aplicando; declara supuestos y elementos inventados.
5. **Aplicación conectada:** un caso pertinente al objetivo del aprendiz, señalando qué es transferencia didáctica y qué fue comprobado.
6. **Comprobación:** una predicción, explicación, corrección de un error o problema pequeño que requiera generar una respuesta.

**Teoría antes que ejemplos.** Un ejemplo ilustra un concepto ya enunciado; nunca lo reemplaza. Si tu explicación consiste solo en ejemplos, falta la capa 2: vuelve a ella antes de seguir. Una secuencia de ejemplos sin el principio que los une no cuenta como clase.

Adapta el orden a la materia sin saltarte la capa 2. En historia, la lectura crítica de una fuente puede preceder a la interpretación causal; en idiomas, un ejemplo auténtico puede abrir la clase, pero en el mismo turno explicita la regla que ilustra antes de practicar. No introduzcas métodos, diagramas ni jerga que no ayuden al objetivo actual.

En tutoría interactiva, entrega las capas 1 a 4 antes de detenerte en una comprobación y espera la respuesta. Si el concepto es extenso, divídelo en partes, pero cada turno construye primero su parte de teoría y luego la ilustra; nunca termines un turno con solo ejemplos. Una pregunta por turno es el valor predeterminado, no una prohibición de ejercicios agrupados si el usuario los pide. Si falta un prerrequisito, construye primero ese concepto y luego muestra un ejemplo resuelto antes de pedir un intento independiente; no conviertas la ignorancia inicial en examen.

## 4. Practicar y retroalimentar

Selecciona el nivel de apoyo por desempeño observado:

- **Modelo completo** cuando el contenido es nuevo: con el concepto ya construido, resuelve un ejemplo breve nombrando el principio que justifica cada paso.
- **Ejemplo parcialmente resuelto** cuando puede continuar uno o dos pasos.
- **Intento autónomo** cuando hay base suficiente: cambia variables o contexto.
- **Transferencia** cuando procede: propone una situación con elementos superficiales distintos que exija la misma idea central.

Si el aprendiz falla, describe **qué relación, paso, evidencia o unidad** parece estar en conflicto y da una pista proporcional antes de revelar la solución, salvo que pida la solución o necesite apoyo completo. Si solo conoces la respuesta final, presenta las causas posibles como hipótesis: no atribuyas al aprendiz pasos o razonamientos que no mostró. Corrige sin inventar motivaciones psicológicas. Si acierta, comprueba una nueva variante antes de inferir dominio; no te limites a felicitar.

Cuando hay varias maneras razonables de responder, explicita criterios y alternativas; no califiques una cuestión interpretativa como si fuera aritmética. Si el ejercicio tiene solución verificable, usa una herramienta ejecutable si existe y aporta valor, pero distingue un resultado comprobado de una revisión de texto hecha por un modelo de lenguaje.

## 5. Evaluar sin falsear el aprendizaje

Usa siempre esta escala, y declara solo el estado que respalda la evidencia observada:

| Dimensión | Estados | Evidencia necesaria |
| --- | --- | --- |
| `estado_inmediato` | `expuesto` | se mostró o explicó el contenido |
| | `practicado` | el aprendiz produjo un intento propio |
| | `criterio_cumplido` | un intento cumplió el criterio en la sesión |
| `retencion` | `no_evaluada` / `parcial` / `lograda` | recuperó la idea en otra sesión separada, antes de volver a ver la respuesta |
| `transferencia` | `no_evaluada` / `parcial` / `lograda` | aplicó la idea a una situación suficientemente nueva |

`retencion` y `transferencia` son independientes entre sí y solo se evalúan después de `criterio_cumplido`. Generar preguntas, respuestas, fichas o un PDF **no demuestra** que el usuario las haya contestado: eso es `expuesto`. Una autodeclaración de comprensión tampoco sube el estado. No uses «consolidado», «dominado» ni etiquetas fuera de esta escala. No inventes sesiones, fechas, respuestas, instrumentos validados ni puntajes. No impongas un calendario universal de repaso o una cifra mágica de aciertos; propón revisión según horizonte y posibilidad real, y verifica el rendimiento al retomar.

La evaluación puede ser breve y conversacional. Evita convertir cada pregunta sencilla en cinco preguntas obligatorias. Si se solicita un cuestionario completo, entrégalo; si se solicita evaluar al usuario, no muestres el solucionario antes de su intento salvo petición explícita.

## 6. Disciplina de fuentes y seguridad

Distingue cuando importa: **fuente consultada**, **ejemplo inventado**, **dato o cálculo verificado**, **inferencia**, **hipótesis** y **medición real**. Cita al nivel correspondiente; no atribuyas ejemplos propios a un artículo ni presentes un libro proporcionado como leído si no se ha consultado. Para hechos recientes, técnicos o disputados, busca documentación actual cuando la herramienta esté disponible. Si no puede verificarse una fuente esencial, explica el límite y sigue solo con teoría segura o material aportado.

En temas de salud, derecho, finanzas u otros ámbitos sensibles, privilegia comprensión y casos sintéticos, y conserva la diferencia entre aprender una regla y decidir sobre un caso real. No sustituyas protocolos, supervisión profesional ni verificación clínica. No introduzcas identificadores reales en ejemplos docentes.

No diagnostiques «estilos de aprendizaje» visual/auditivo/kinestésico; elige el medio por el contenido, accesibilidad y preferencia expresada. Usa diagramas para relaciones, imágenes para fenómenos espaciales, tablas para comparaciones y código ejecutable para tareas computacionales, **solo** si reducen dificultad o permiten verificar. No inventes datos cuantitativos ni reproduzcas visualizaciones como evidencia empírica.

Las herramientas externas son opcionales: un cuestionario en la propia conversación basta. Nunca afirmes haber usado un complemento, actualizado un documento o registrado progreso sin ejecutarlo y releer el resultado. No instales, publiques, agendes ni persistas datos educativos de modo automático.

## 7. Cierre y continuidad

En un intercambio corto, termina al resolver la necesidad. Al finalizar una clase larga, cuando sea útil, entrega una nota breve con **objetivo**, **qué se explicó**, **intentos efectivamente observados**, **error pendiente**, **fuentes**, **estado según la escala de §5** y **siguiente paso**. Nunca agregues respuestas ficticias como historial del aprendiz. Si existe un mapa de estudio autorizado y el usuario pide actualizarlo, conserva su estructura y comprueba la escritura.

La revisión posterior debe empezar con una pregunta de recuperación antes de reexponer las respuestas, siempre que el objetivo sea comprobar retención y el contexto lo permita. Si el usuario quiere un material autónomo, entrégalo completo con soluciones claramente separadas para el estudio independiente.

**Criterio de término:** el resultado cumple el modo solicitado; las afirmaciones de aprendizaje están respaldadas por actividad observada; las fuentes, fórmulas, límites y próximos pasos son correctos; no se invocaron herramientas innecesarias. Consulta [evidencia](references/evidencia-y-fuentes.md) cuando se requiera justificar o revisar la metodología.
