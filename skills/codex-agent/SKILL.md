---
name: codex-agent
description: "Invoca al CLI de Codex en modo headless via `codex exec`, con modelo elegible en cada uso (sin default). Lectura libre, escritura solo con aviso. Usar cuando el usuario pida correr una tarea con Codex de forma no interactiva. Differentiator vs pi/muse/opencode/agy-agent: esta skill invoca el CLI de Codex (`codex exec`), no los otros CLIs."
search_hints: "codex, codex exec, headless, no interactivo, correr tarea con codex"
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
  triggers:
    - "codex"
    - "codex exec"
    - "headless"
    - "no interactivo"
    - "correr tarea con codex"
---

# Codex Agent

Invoca a Codex en modo headless.

- Binario: `$(command -v codex)` (esperado: `/opt/homebrew/bin/codex` o en PATH)
- Modo: `codex exec` (no interactivo)

## Modelo (obligatorio en cada uso)

- Pasar siempre `-m <MODEL>` (o `--model <MODEL>`).
- Esta skill NO tiene modelo por defecto hardcodeado. Si el uso no indica `<MODEL>`, pedirlo y esperar — nunca asumir ni inventar uno.
- Antes de ejecutar, verificar que el comando incluya `-m`/`--model` literal; si falta, detenerse y pedirlo (el CLI defaultea silencioso al model de config).
- Lookup parcial: este CLI no expone catálogo de modelos (`codex --help` / `codex exec --help` no listan comando de modelos) — no existe flag de listado que verificar, así que el "lookup" es: usar solo el modelo que el usuario nombró, nunca adivinar IDs.

## Permisos: sandbox read-only y escrituras con aviso

- Garantía operativa de solo lectura: se implementa mediante el sandbox nativo de Codex pasando `-s read-only`.
- Advertencia sobre escrituras del host: los hooks ambientales o del runtime pueden crear archivos de metadatos locales (como `.atl/`) en el workdir aun en `-s read-only`. Para aislamiento estricto, ejecutar en un scratch descartable (`-C <scratch>`) y verificar `git status`.
- Cualquier modo de escritura o apply (`-s workspace-write`) SOLO tras aviso explícito al usuario en el mismo uso.
- Fijar siempre `-s` explícito; nunca heredar el de config. El approval lo gobierna la config de Codex — esta versión de `codex exec` no expone flag `-a`/`--approval`, solo `-s`/`--sandbox`.
- No agregar flags de auto-approve / full-access por defecto. Prohibido `--dangerously-bypass-approvals-and-sandbox` en todos los usos.
- Nota: se evaluó `disable-model-invocation: true` y se rechazó — la skill debe seguir invocable por el modelo; el control es el aviso previo en escrituras, no el bloqueo de invocación.

## Invocación

Preflight de auth antes de invocar (verificado: `codex login --help` expone `status`):

```sh
codex login status  # exit 0 = listo; si falla, frenar y pedir al usuario `codex login`
```

Forma canónica (workdir explícito + captura de output a archivo):

```sh
TIMEOUT_BIN=$(command -v timeout || command -v gtimeout)
[ -z "$TIMEOUT_BIN" ] && { echo "BLOCK: timeout/gtimeout required" >&2; exit 1; }

OUT=$(mktemp /tmp/codex-out.XXXXXX)
$TIMEOUT_BIN 60 codex exec -C <DIR> -s read-only -m "$MODEL" \
  -o "$OUT" "<prompt del worker>" 2>&1 </dev/null
```

- `-C/--cd <DIR>` verificado en `codex exec --help`: workdir explícito siempre, nunca cwd implícito.
- `-o/--output-last-message <FILE>` verificado en `codex exec --help`: el mensaje final queda en `$OUT`; leerlo con `cat "$OUT"`.
- `</dev/null` mandatorio: `codex exec` lee instrucciones de stdin cuando falta el arg PROMPT o stdin viene pipeado (ver `codex exec --help`: stdin se anexa como bloque `<stdin>`); sin `</dev/null` la corrida puede bloquearse esperando EOF.
- One-task-per-launch: una tarea acotada por corrida; post-ejecución revisar `git -C <DIR> diff --stat` y `git -C <DIR> status --short` antes de declarar done.
- El worker arranca ciego (no ve esta conversación): escribir el brief completo en el prompt con el molde de 5 campos — Objective / Constraints (solo-lectura vs implementar, sin push; archivos a tocar) / Deliverable / Validation (cómo sabe que terminó) / Report (resumen corto, ver §Ejemplo).
- Reportes cortos: devolver resumen + diff/files changed; nunca volcar el prompt ni transcripts crudos.

## Ejemplo (solo lectura)

Precondición: cwd dentro de un dir confiable de Codex; si no, la corrida falla con "Not inside a trusted directory".

```sh
MODEL="<modelo-pedido>"  # reemplazar por el modelo real pedido en este uso
OUT=$(mktemp /tmp/codex-out.XXXXXX)

TIMEOUT_BIN=$(command -v timeout || command -v gtimeout)
[ -z "$TIMEOUT_BIN" ] && { echo "BLOCK: timeout/gtimeout required" >&2; exit 1; }

$TIMEOUT_BIN 60 codex exec -C "$PWD" -s read-only -m "$MODEL" -o "$OUT" "lista los archivos del directorio actual sin modificar nada" 2>&1 </dev/null
cat "$OUT"
git status --short
```

Nota: los hooks ambiente pueden escribir `.atl/` en el cwd aun en solo-lectura; correr en scratch o con `-C <scratch>`.

## Unhappy paths (Failure modes)

- Binario ausente → lane bloqueada, reportar y no avanzar.
- Auth ausente (`codex login status` exit != 0) → frenar; el usuario corre `codex login`. No intentar workarounds.
- Modelo omitido → pedirlo, no defaultear.
- Modelo inválido o flag inexistente → el CLI lo rechaza; no adivinar IDs ni inventar flags — solo los documentados acá son válidos.
- Falta de timeout → si ni `timeout` ni `gtimeout` están presentes en el host, bloquear antes de la ejecución.
- Sin salida en 60s con stdin abierto → relanzar con `</dev/null` (stdin abierto = bloqueo esperando EOF).
- Dir no confiable → registrar confianza o reintentar con `--skip-git-repo-check` solo en scratch descartable, nunca como default.
- Sin salida en 60s → matar por timeout y reportar (no reintentar a ciegas).
- Escritura sin aviso previo → frenar y avisar.
- Solo los flags documentados acá son válidos (`-m`/`--model`, `-s`, `-C`, `-c`, `-o`/`--output-last-message`, `--skip-git-repo-check`); no inventar otros.
