---
name: design-process-orchestrator
description: "Coordina el proceso de diseño con alcance proporcional y consolida salidas de especialistas. Use for explicit greenfield work, a multi-specialist effort, or when a request needs orchestration. For one bounded design dimension, route to its specialist."
license: MIT
metadata:
  author: 'Felipe Gonzalez'
---

# Design Process Orchestrator

## Purpose

Coordina y consolida un proceso de diseño; no sustituye a las especialistas, sus criterios, ni la autoridad del proyecto o del harness. Respeta el proceso y los gates del harness anfitrión (por ejemplo, Gentle); no los duplica ni los reemplaza. Elige el modo mínimo que cubre el pedido, declara sus límites y conserva las fuentes canónicas. Es una skill portable, no una promesa de compatibilidad universal. PGE (Prompt Graph Engineering), formulado por Sandeco Macedo, inspira la coordinación modular; no convierte el flujo en una dependencia de runtime.

## Entry guards

- Selecciona **Greenfield** solo ante intención explícita de crear desde cero; una solicitud ambigua no implica ese permiso.
- Elige entre Greenfield, Subgraph, Ligero, Auditoría y Refactorización según el pedido y el contexto. Un ajuste de tres dimensiones/nodos no escala por conteo.
- En un proyecto existente, consulta las fuentes rectoras relevantes y reconoce su autoridad. No las sobrescribas ni cambies stack, herramientas, dependencias o decisiones por inferencia. Expón conflictos y pregunta antes de resolverlos.
- Auditoría es de solo lectura. Refactorización requiere autorización explícita antes de escribir. Un manifiesto presente no es autorización.
- El modo ligero no crea ni exige cuatro documentos rectores. No crees `DESIGN.md` inexistente para registrar una tarea: comunica la decisión en la respuesta. Actualiza un documento existente solo si está dentro del alcance autorizado.

## Run

1. Identifica el resultado solicitado, contexto, plataformas, capacidades disponibles, fuentes rectoras y límites de escritura. No inventes datos faltantes; pide una decisión cuando un conflicto de autoridad cambie el trabajo.
2. Selecciona especialistas solo para ámbitos solicitados. Consulta prerrequisitos pertinentes, declara dependencias y no dupliques sus reglas. Si solo se pide una dimensión, deriva directamente a su especialista.
3. Ejecuta el contrato del modo y las reglas de cobertura/evidencia descritos en [execution contracts](references/execution-contracts.md). Usa las capacidades/herramientas realmente disponibles y descubiertas; no exijas Figma MCP, una CLI propietaria, navegador ni harness particular.
4. Escribe únicamente artefactos autorizados y aplicables. Las plantillas de [workspace templates](references/workspace-templates.md) son opcionales; las rutas de salida se resuelven desde la raíz del proyecto.
5. Consolida resultados sin convertir cobertura parcial en aprobación global. Si falta una especialista, continúa el trabajo independiente, marca su ámbito `NotReviewed` y bloquea solo resultados dependientes. Sin navegador, la conducta visual queda `NotVerified`.

## Report

Declara modo, alcance, fuentes consultadas y conflictos, especialistas/ámbitos, dependencias, escrituras autorizadas y realizadas, cobertura, método, evidencia, verificación y limitaciones. Para cada ámbito separa:

- **Cobertura:** `Reviewed`, `NotReviewed` o `NotApplicable` (con razón).
- **Verificación:** `Verified`, `Failed` o `NotVerified`, siempre con método y evidencia. Si la cobertura es `NotApplicable`, deja verificación como `—` y explica la razón.

Una etapa omitida nunca es `PASS`; no presentes instrucciones, inspección estática o resultados parciales como prueba de comportamiento ni aprobación global. Conserva la distinción entre hallazgo, limitación y decisión pendiente.

## Further detail

Modos, autorización de escrituras, fuentes, dependencias, handoff condicional, calidad contextual y referencias técnicas atribuidas están en [execution contracts](references/execution-contracts.md).
