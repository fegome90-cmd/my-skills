---
disable-model-invocation: true
name: grill-me-dual-herdr
description: "Trigger: grill-me, grillme, dos agentes, grill-a/grill-b. Entrevista un plan alternadamente con evidencia real usando Herdr + OpenCode."
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "3.0"
---

## Activation Contract

Carga esta skill cuando el usuario pida interrogar adversarialmente un plan, diseño o arquitectura con dos agentes que se respondan. Requiere un entorno Herdr real (HERDR_ENV=1), herdr y opencode.

**El modelo NO es decisión de los agentes del grill.** El modelo lo define el orquestador (el coordinador), en acuerdo con el usuario, ANTES de arrancar cualquier agente. Grill A y Grill B nunca eligen ni cambian su modelo: solo reciben (1) su agent md (rol) y (2) las instrucciones que esta skill pide de ellos. Si el modelo efectivo deriva durante la corrida, es falla del orquestador, no del agente.

## Hard Rules

- Ejecuta diálogo alternado real; nunca dos veredictos paralelos.
- Cada claim verificable exige lectura live (git, grep, find, pruebas read-only) y evidencia ruta:línea o salida de comando.
- No mutar el repositorio/Git: no stash, reset, clean, fetch, switch, stage, commit, push, merge ni delete. No falsificar HERDR_ENV; nunca detener el servidor Herdr.
- **El modelo lo fija el orquestador, nunca el agente.** Antes de crear panes, pregunta al usuario qué modelos usan Grill A y Grill B y fíjalos (agent md con `model:` o `-m`). Los agentes grill reciben solo su agent md + las instrucciones de la skill; no se les pide elegir modelo ni se les permite cambiarlo durante la corrida. Si el modelo deriva (por agent default de sesión, plugin omniroute, ctrl+x m u otra causa), es responsabilidad del orquestador detectarlo y reportarlo — no culpa del agente ni se resuelve preguntándole a él.
- Usa los pane_id devueltos por JSON. Espera cada prompt y no informes antes de cerrar la tanda.
- **Escribe los artefactos del grill en el temp dir pre-aprobado de opencode, no en /tmp.** En macOS es `$TMPDIR/opencode/grill-<slug>/` (equivale a `/var/folders/<uuid>/T/opencode/grill-<slug>/`). El agente default (`build`) tiene `external_directory: ask` para `*` pero `allow` para `$TMPDIR/opencode/*`; `/tmp` queda bajo el patrón `ask` y cada lectura de los agentes grill dispara el diálogo de permisos. Usar `$TMPDIR/opencode/` elimina esa fricción. Si `$TMPDIR` no está definido o la ruta no existe, créala con `mkdir -p` y úsala igual. No escribir en /tmp salvo autorización explícita.

## Decision Gates

| Gate | Acción |
|---|---|
| Preflight, modelo o HERDR_ENV falla | Detén el grill; no simules el entorno. |
| El modelo efectivo de un agente difiere del acordado | Detén la ronda; reporta al usuario con evidencia (agent get / pantalla / argv) y pide instrucción. No continúes ni dupliques el prompt. |
| grill-a/b ya existe | Reutiliza si está idle o cierra su pane exacto con herdr pane close <pane_id>. |
| Agente blocked | Lee visible; resuelve permisos con send-keys y verifica estado. |
| Timeout | Inspecciona estado/read; no dupliques el prompt automáticamente. |
| Claim sin evidencia | Pide verificación puntual antes de aceptarlo. |

## Execution Steps

1. Materializa el plan completo y su criterio de diseño en `$TMPDIR/opencode/grill-<slug>/PLAN-grill-<slug>.md`; guarda checksum y baseline en el mismo directorio.
2. Preflight: valida HERDR_ENV, binarios, agentes previos. **Pregunta al usuario los modelos de Grill A y Grill B** (pueden ser iguales o distintos) y fíjalos antes de crear panes. Crea dos panes con --no-focus, registra sus IDs y arranca grill-a/grill-b con OpenCode usando el modelo acordado (`--agent <agent-md>` o `-m <modelo>`). Verifica el modelo en el `argv` devuelto por `agent start`; si el `argv` no contiene el modelo acordado, corrige antes de continuar.
3. Setup: a cada agente le entregas (a) su agent md (rol, definido por el orquestador) y (b) las instrucciones que esta skill pide de él (plan, reglas de evidencia, formato de salida). Ambos leen el plan, verifican claims contra el repo y responden LISTO. El setup no incluye preguntas sobre modelo: el modelo ya está fijado por el orquestador y el agente no lo elige.
4. Ejecuta la entrevista: A formula exactamente 3 preguntas; B responde 1–3 y formula 4–6; A responde 4–6 y formula 7–8; B responde 7–8. Las respuestas conservan la numeración y conceden/refutan con evidencia. Antes de cada ronda, verifica que el modelo efectivo de ambos agentes sigue siendo el acordado (agent get / pantalla / argv); ante cualquier deriva, aplica el gate correspondiente y no continúes hasta que el usuario decida.
5. Pide a ambos una consolidación de máximo 8 hallazgos en `$TMPDIR/opencode/grill-<slug>/grill-a-consolidation.md` y `$TMPDIR/opencode/grill-<slug>/grill-b-consolidation.md`; verifica CONSOLIDADO y la existencia de ambos archivos.
6. Une los hallazgos en máximo 10 fixes ordenados, distingue confirmado/inferido/no probado y no declares PASS si un gate quedó bloqueado.
7. Cierra los panes por sus IDs exactos con herdr pane close; verifica que no queden grill-a/b. No cierres el pane principal.

## Output Contract

Devuelve: preflight (incluyendo los modelos acordados con el usuario y su verificación), evidencia live, diálogo completo resumido, hallazgos confirmados, riesgos no resueltos, fixes mínimos ordenados, artefactos temporales y estado de cleanup. Solo crea artefactos persistentes con autorización explícita.

## References

- AGENTS.md — reglas del workspace cuando el grill corre dentro de un repositorio.
- Verifica el CLI instalado con herdr agent --help y herdr pane --help; no asumas subcomandos ausentes.

