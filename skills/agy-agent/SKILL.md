---
name: agy-agent
description: "Invoca al CLI de agy en modo headless via `agy --print`, con modelo elegible en cada uso (sin default). Lectura libre, escritura solo con aviso. Usar cuando el usuario pida correr una tarea con agy de forma no interactiva. Differentiator vs codex/pi/muse/opencode-agent: esta skill invoca el CLI de agy (`agy --print`), no los otros CLIs."
search_hints: agy agy --print agy print headless no interactivo correr tarea con agy model models
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
  triggers:
    - "agy"
    - "agy --print"
    - "agy print headless"
    - "no interactivo"
    - "correr tarea con agy"
---

# agy-agent

Invoca a agy en modo headless.

- Binario: `$(command -v agy)` (esperado: `~/.local/bin/agy` o en PATH)
- Modo: `agy --print` (no interactivo, una sola respuesta impresa)

## Modelo (obligatorio en cada uso)

- Pasar siempre `--model <MODEL>` (ver `agy models` para la lista disponible).
- Lookup antes de invocar: `agy models`; usar solo el ID del catálogo que el usuario nombró, nunca adivinar IDs.
- Esta skill NO tiene modelo por defecto hardcodeado. Si el uso no indica `<MODEL>`, pedirlo y esperar — nunca asumir ni inventar uno.
- NOTA: el CLI trae modelo por defecto; omitir `--model` NO falla (verificado: `agy --print` responde igual). El agente DEBE pedir `<MODEL>` antes de ejecutar aunque el CLI no lo exija.

## Permisos: lectura libre + escritura con aviso

- Lectura libre del repo: leer archivos, listar directorios, responder preguntas.
- Cualquier escritura, edición o apply solo tras aviso explícito al usuario en el mismo uso.
- PROHIBIDO `--dangerously-skip-permissions` por defecto. Nunca agregarlo salvo aviso explícito al usuario en el mismo uso.
- El enforcement real hoy lo dan las reglas globales del CLI; esta sección es directiva del agente, no un gate técnico.
- Nota: se evaluó `disable-model-invocation: true` y se rechazó — la skill debe seguir invocable por el modelo; el control es el aviso previo en escrituras, no el bloqueo de invocación.

## Invocación

Preflight antes de invocar (degradado explícito: `agy` no expone `login status`; ningún subcomando de auth en `--help`):

```sh
command -v agy  # esperado: ~/.local/bin/agy o en PATH
agy models      # lookup = señal de listo; si falla por auth, frenar y pedir credenciales al usuario
```

Forma canónica (workdir explícito + captura de output a archivo):

```sh
OUT=$(mktemp /tmp/agy-out.XXXXXX)
cd <DIR> && timeout 60 agy --model "<MODEL>" --print "<prompt del worker>" > "$OUT" 2>&1 </dev/null
cat "$OUT"
```

- Workdir explícito siempre vía `cd <DIR>`, nunca cwd implícito. `--add-dir` existe en `agy --help` pero agrega un directorio al workspace, no fija el workdir; no usarlo en el patrón canónico.
- `agy --help` no expone flag de captura a archivo: el output queda en `$OUT` por redirección shell; leerlo con `cat "$OUT"`.
- `</dev/null` mandatorio en shells background/scripts: cierra stdin y evita bloqueos esperando EOF. (Solo `--input-format stream-json` lee stdin; en `text` —el default— no se afirma que lo anexe como contexto: es cierre preventivo, misma disciplina que las skills hermanas.)
- One-task-per-launch: una tarea acotada por corrida; post-ejecución revisar `git diff --stat` y `git status --short` en `<DIR>` antes de declarar done.
- El worker arranca ciego (no ve esta conversación): escribir el brief completo en el prompt con el molde de 5 campos — Objective / Constraints (solo-lectura vs implementar, sin push; archivos a tocar) / Deliverable / Validation (cómo sabe que terminó) / Report (resumen corto, ver §Ejemplo).
- Reportes cortos: devolver resumen + diff/files changed; nunca volcar el prompt ni transcripts crudos.
- Frontmatter `disable-model-invocation`: evaluado y excluido — esta skill existe para invocar un modelo vía CLI en cada uso; deshabilitar la invocación contradice su propósito.

## Ejemplo (solo lectura)

```sh
OUT=$(mktemp /tmp/agy-out.XXXXXX)
cd "$PWD" && timeout 60 agy --model "<MODEL>" --print "lista los archivos del directorio actual sin modificar nada" > "$OUT" 2>&1 </dev/null
cat "$OUT"
git diff --stat; git status --short
```

Plantilla NO ejecutable tal cual: reemplazar `<MODEL>` por el modelo real; pedirlo si falta.

NOTA: el orden de flags es irrelevante (flags estilo Go; `--print ... --model ...` funciona igual). No asumir error por orden. `--print` opera sobre el workspace de agy, no necesariamente el cwd del shell.

## Unhappy paths

- Binario ausente → lane bloqueada, reportar y no avanzar.
- Modelo omitido → pedirlo, no defaultear.
- Modelo inválido → el CLI imprime `Error: invalid model selection` pero sale con código 0; verificar el output, no solo `$?`.
- Escritura sin aviso previo → frenar y avisar.
- Auth ausente (`agy models` falla) → frenar; pedir credenciales al usuario. No intentar workarounds (no existe `login status` en este CLI).
- Flag inexistente → el CLI lo rechaza; no adivinar ni inventar flags.
- Sin salida con stdin abierto → matar y relanzar con `</dev/null` (stdin abierto = bloqueo esperando EOF).
- Sin salida en 60s → matar por timeout y reportar (no reintentar a ciegas).
- Solo los flags documentados acá son válidos (`--print`/`-p`, `--model`; subcomando `models`); no portar flags cruzados de otros CLIs ni inventar otros.
