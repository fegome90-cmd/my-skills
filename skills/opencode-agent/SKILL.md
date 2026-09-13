---
name: opencode-agent
description: "Invoca al CLI de opencode en modo headless via `opencode run`, con modelo elegible en cada uso (sin default). Lectura libre, escritura solo con aviso. Usar cuando el usuario pida correr una tarea con opencode de forma no interactiva. Differentiator vs codex/pi/muse/agy-agent: esta skill invoca el CLI de opencode (`opencode run`), no los otros CLIs."
search_hints: "opencode, opencode run, headless, no interactivo, correr tarea con opencode"
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
  triggers:
    - "opencode"
    - "opencode run"
    - "headless"
    - "no interactivo"
    - "correr tarea con opencode"
---

# Opencode Agent

Invoca a opencode en modo headless.

- Binario: `$(command -v opencode)` (esperado: `~/.opencode/bin/opencode` o en PATH)
- Modo: `opencode run` (no interactivo)

## Modelo (obligatorio en cada uso)

- Pasar siempre `-m <provider/model>`.
- Esta skill NO tiene modelo por defecto hardcodeado. Si el uso no indica `<provider/model>`, pedirlo y esperar — nunca asumir ni inventar uno.
- Verificar que cada invocación incluya `-m` explícito; el CLI defaultea silencioso si se omite (`opencode run "hola"` corre sin error). Si el CLI resolvió un default, abortar e informar el modelo usado en vez de continuar.
- Lookup antes de invocar: `opencode models` (o `opencode models <provider>`, ambos verificados en `opencode --help`); usar solo el `<provider/model>` del catálogo que el usuario nombró, nunca adivinar IDs.

## Permisos: lectura libre + escritura con aviso

- Lectura libre del repo: leer archivos, listar directorios, responder preguntas.
- Cualquier escritura, edición o apply solo tras aviso explícito al usuario en el mismo uso.
- Prohibido `--auto` en todos los usos (auto-aprueba permisos); cualquier escritura, edición, apply o attach requiere aviso explícito previo en el mismo uso.
- No usar `--agent`, `--command`, `-f`/`--file` ni `--dir` salvo aviso explícito; ejecutar únicamente el patrón del ejemplo documentado.
- Sin bypass de permisos por defecto.
- Nota: se evaluó `disable-model-invocation: true` y se rechazó — la skill debe seguir invocable por el modelo; el control es el aviso previo en escrituras, no el bloqueo de invocación.

## Invocación

Preflight antes de invocar (degradado explícito: `opencode` no expone `login status`; `opencode --help` solo ofrece `providers` [alias `auth`] para credenciales):

```sh
command -v opencode  # esperado: ~/.opencode/bin/opencode o en PATH
opencode providers   # gestiona credenciales; si falla por auth, frenar y pedir credenciales al usuario
opencode models [<provider>]  # lookup = señal de listo; usar solo IDs del catálogo
```

Forma canónica (workdir explícito + captura de output a archivo):

```sh
TIMEOUT_BIN=$(command -v timeout || command -v gtimeout)
[ -z "$TIMEOUT_BIN" ] && { echo "BLOCK: timeout/gtimeout required for bounded execution" >&2; exit 1; }

OUT=$(mktemp /tmp/opencode-out.XXXXXX)
cd <DIR> && $TIMEOUT_BIN 60 opencode run -m "<provider/model>" "<prompt del worker>" > "$OUT" 2>&1 </dev/null
cat "$OUT"
```

- Workdir explícito siempre vía `cd <DIR>`, nunca cwd implícito. `--dir` existe en `opencode run --help` pero está prohibido sin aviso (§Permisos); no usarlo en el patrón canónico.
- `opencode run --help` no expone flag de captura (no hay `-o`): el output queda en `$OUT` por redirección shell; leerlo con `cat "$OUT"`.
- `</dev/null` mandatorio en shells background/scripts: cierra stdin y evita bloqueos esperando EOF. (`run --help` no documenta lectura de stdin, así que no se afirma que lo anexe como contexto — es cierre preventivo, misma disciplina que las skills hermanas.)
- One-task-per-launch: una tarea acotada por corrida; post-ejecución revisar `git diff --stat` y `git status --short` en `<DIR>` antes de declarar done.
- El worker arranca ciego (no ve esta conversación): escribir el brief completo en el prompt con el molde de 5 campos — Objective / Constraints (solo-lectura vs implementar, sin push; archivos a tocar) / Deliverable / Validation (cómo sabe que terminó) / Report (resumen corto, ver §Ejemplo).
- Reportes cortos: devolver resumen + diff/files changed; nunca volcar el prompt ni transcripts crudos.
- Frontmatter `disable-model-invocation`: evaluado y excluido — esta skill existe para invocar un modelo vía CLI en cada uso; deshabilitar la invocación contradice su propósito.

## Ejemplo (solo lectura)

```sh
TIMEOUT_BIN=$(command -v timeout || command -v gtimeout)
[ -z "$TIMEOUT_BIN" ] && { echo "BLOCK: timeout/gtimeout required" >&2; exit 1; }

OUT=$(mktemp /tmp/opencode-out.XXXXXX)
cd "$PWD" && $TIMEOUT_BIN 60 opencode run -m "<provider/model>" "lista los archivos del directorio actual sin modificar nada" > "$OUT" 2>&1 </dev/null
cat "$OUT"
git diff --stat; git status --short
```

Plantilla NO ejecutable tal cual: reemplazar `<provider/model>` por el modelo real; pedirlo si falta.

## Unhappy paths (Failure modes)

- Binario ausente → reportar `opencode no encontrado en PATH ni en ~/.opencode/bin/opencode; lane bloqueada`, y no avanzar.
- Timeout ausente → si ni `timeout` ni `gtimeout` existen, BLOQUEAR la ejecución bounded; no correr indefinidamente.
- Auth ausente (`opencode providers` falla) → frenar; pedir credenciales al usuario. No intentar workarounds (no existe `login status` en este CLI).
- Modelo omitido → pedirlo, no defaultear.
- Modelo inválido o sin saldo/cuota → error (stdout vacío, `UnknownError` al final del stderr), reportar verbatim, cero reintentos.
- Flag inexistente → el CLI lo rechaza; no adivinar ni inventar flags.
- Errores en stderr → reportar todos los errores observados (incluyendo fallos de conexión de plugins o daemons de ruteo como omniroute); no silenciarlos ni ignorarlos.
- Sin salida con stdin abierto → matar y relanzar con `</dev/null` (stdin abierto = bloqueo esperando EOF).
- Sin salida en 60s → matar por timeout y reportar (no reintentar a ciegas).
- Escritura sin aviso previo → frenar y avisar.
- Solo los flags documentados acá son válidos (`-m`/`--model` en `opencode run`; `models`, `providers` a nivel top); no portar flags cruzados de otros subcomandos ni inventar otros.
