# Escenarios de evaluación (solo para mantenedores)

> Referencia para evaluar y mantener esta skill; no son instrucciones de ejecución en tiempo de uso.

## Método

Para cada escenario:

1. solicitar a un agente sin la skill que genere el entregable;
2. registrar fallos de estructura, rigor, audiencia y formato;
3. repetir con la skill habilitada y sin filtrar las conclusiones esperadas;
4. comparar con los criterios de aceptación;
5. modificar la skill solo para corregir fallos observados;
6. volver a probar hasta que el comportamiento sea estable.

## Escenario 1: gran ronda clínica

**Prompt:** Convertir material sobre un piloto de preservación de voz en oncología en una charla de 20 minutos para oncólogos, enfermería, fonoaudiología, tecnología y dirección.

**Debe lograr:** hilo común accesible, profundidad por capas, evidencia y privacidad, diferencia entre implementación e investigación, próximos decision gates.

**Fallo crítico:** historia emocional de paciente que reemplaza la evidencia o expone información sensible.

## Escenario 2: comité de arquitectura

**Prompt:** Preparar una presentación de 12 minutos para decidir entre tres diseños de una plataforma distribuida.

**Debe lograr:** decisión al inicio, criterios antes de opciones, trade-offs simétricos, recomendación, reversibilidad y próximo hito.

**Fallo crítico:** ocultar la recomendación hasta el final o describir tecnologías sin conectarlas con la decisión.

## Escenario 3: resultado científico negativo

**Prompt:** Redactar una charla de congreso sobre un estudio bien diseñado cuyo resultado primario fue negativo y cuyos análisis exploratorios sugieren una señal.

**Debe lograr:** preservar resultado primario, separar análisis confirmatorio y exploratorio, explicar valor del resultado negativo y evitar causalidad excesiva.

**Fallo crítico:** convertir la señal exploratoria en conclusión principal para mejorar la historia.

## Escenario 4: incidente de seguridad clínica

**Prompt:** Crear un guion para presentar un evento adverso a un comité de calidad.

**Debe lograr:** enfoque sistémico, cronología solo donde aporte causalidad, barreras, controles, riesgo residual y protección de identidad.

**Fallo crítico:** culpabilizar a una persona o dramatizar el daño.

## Escenario 5: capacitación con concepción errónea

**Prompt:** Enseñar a personal técnico por qué una métrica de rendimiento puede mejorar mientras el sistema real empeora.

**Debe lograr:** predicción, modelo intuitivo, contraejemplo, explicación, segundo caso de transferencia y límite del nuevo modelo.

**Fallo crítico:** exposición clara pero pasiva que nunca obliga a confrontar la concepción previa.

## Escenario 6: demo para audiencia mixta

**Prompt:** Preparar una demo de 10 minutos de una herramienta de IA para especialistas, líderes y usuarios operativos.

**Debe lograr:** problema y línea base, prueba observable, caso límite, supervisión humana, impacto por perfil y decisión siguiente.

**Fallo crítico:** demo feliz, afirmaciones promocionales o ausencia de límites.

## Rúbrica mínima

Puntuar 0–2 cada dimensión:

- objetivo y audiencia;
- tesis principal;
- lógica narrativa;
- selección de evidencia;
- fidelidad técnica;
- incertidumbre y límites;
- relación entre voz y visuales;
- utilidad del cierre;
- adecuación temporal;
- preparación para preguntas.

No desplegar como estándar si existe un fallo crítico o alguna dimensión obtiene 0 en dos pruebas consecutivas.
