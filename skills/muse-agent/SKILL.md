---
name: muse-agent
description: "Invoca al CLI de Muse en modo headless via `muse exec`, con modelo elegible en cada uso (sin default). Lectura libre, escritura solo con aviso. Usar cuando el usuario pida correr una tarea con Muse de forma no interactiva. Differentiator vs codex/pi/opencode/agy-agent: esta skill invoca el CLI de Muse (`muse exec`), no los otros CLIs."
search_hints: muse muse exec headless no interactivo correr tarea con Muse workspace model prompt-file disable-write
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
  triggers:
    - "muse"
    - "muse exec"
    - "headless"
    - "no interactivo"
    - "correr tarea con Muse"
---

# Muse Agent

Invoca a Muse en modo headless.

- Binario: `$(command -v muse)` (esperado: `~/.local/bin/muse` o en PATH)
- Modo: `muse exec` (no interactivo)

## Preflight

```sh
muse --version   # alcanzable? si falla, lane bloqueada
```

- Degradación explícita: el CLI no expone comando de auth-status (`muse auth --help` solo ofrece `auth set --api-key-stdin`; `muse login` es OAuth por browser sin chequeo previo). No inventar `muse auth status`.
- Si un `exec` falla por credenciales ausentes/inválidas → frenar y pedir al usuario que corra `muse login` (o `muse auth set`); nunca leer, imprimir ni copiar credenciales.

## Invocación

```sh
TIMEOUT_BIN=$(command -v timeout || command -v gtimeout)
[ -z "$TIMEOUT_BIN" ] && { echo "BLOCK: timeout/gtimeout required for bounded execution" >&2; exit 1; }

OUT=$(mktemp /tmp/muse-out.XXXXXX)
$TIMEOUT_BIN 60 muse exec --disable-write --workspace /path/to/repo --model "<ID>" "prompt completo" </dev/null > "$OUT" 2>&1
git -C /path/to/repo diff --stat; git -C /path/to/repo status --short   # revisar diff y archivos untracked antes de dar por hecha la tarea
cat "$OUT"
```

- Workdir explícito: siempre `--workspace <PATH>` (flag verificado en `muse exec --help`); no asumir cwd del launcher.
- Captura a archivo: redirigir stdout y stderr a `"$OUT"` (`> "$OUT" 2>&1`; no existe flag `--output` en `muse exec --help`; la redirección shell es el mecanismo).
- `</dev/null` mandatorio: stdin abierto puede dejar el proceso esperando EOF en shells background/scripts; cerrarlo evita el bloqueo.
- Prompt largo? Usar `--prompt-file /tmp/task.md` (flag verificado) en vez del argumento posicional.
- El worker arranca ciego: `muse exec` no ve la conversación. Molde de 5 campos en cada prompt:
  1. **Objective** — una oración.
  2. **Constraints** — solo-lectura vs implementar; sin git push; sin writes a prod.
  3. **Deliverable** — qué debe devolver.
  4. **Validation** — cómo sabe que terminó.
  5. **Report** — resumen corto + archivos cambiados (nunca dumps ni transcripts crudos).
- One-task-per-launch: una tarea acotada por invocación; partir trabajos grandes en varias llamadas.

## Modelo (obligatorio en cada uso)

- Pasar siempre `--model <ID>`.
- Esta skill NO tiene modelo por defecto hardcodeado. Si el uso no indica `<ID>`, pedirlo y esperar — nunca asumir ni inventar uno.
- El CLI SÍ defaultea en silencio si se omite `--model` (probado: corre sin error); por eso el agente debe frenar y pedir `<ID>` ANTES de invocar — nunca invocar sin `--model` para descubrir el default.
- NO hacer: `muse exec "prompt"` (usa default implícito).
- `--model` solo es válido con el provider default (`meta`); con `--provider echo` es error (exit 2).
- Lookup parcial documentado: el CLI no expone comando de listado de modelos (`--help` no lista ninguno); el `<ID>` siempre lo indica el usuario — pedirlo y esperar, nunca adivinarlo ni hardcodear catálogos.

## Permisos: lectura libre + escritura con aviso

- Lectura libre del repo: leer archivos, listar directorios, responder preguntas.
- Cualquier escritura, edición o apply solo tras aviso explícito al usuario en el mismo uso.
- Antes de cualquier escritura: (1) aviso explícito en el mismo uso, (2) confirmar que el comando NO lleva `--disable-write`, (3) nunca `--yolo`/`--disable-approval` sin aviso.
- Mantener approval on-request (default del CLI); no activar modo auto-approve global (`--yolo`, `--disable-approval`) sin aviso explícito.
- Nota: se evaluó `disable-model-invocation: true` y se rechazó — la skill debe seguir invocable por el modelo; el control es el aviso previo en escrituras, no el bloqueo de invocación.

## Ejemplo (solo lectura)

```sh
TIMEOUT_BIN=$(command -v timeout || command -v gtimeout)
[ -z "$TIMEOUT_BIN" ] && { echo "BLOCK: timeout/gtimeout required" >&2; exit 1; }

OUT=$(mktemp /tmp/muse-out.XXXXXX)
$TIMEOUT_BIN 60 muse exec --disable-write --workspace /path/to/repo --model "<ID>" "$(cat <<'EOF'
Objective: listar los archivos del repo sin modificar nada.
Constraints: READ ONLY. Sin cambios de código, sin git writes.
Deliverable: lista de archivos.
Validation: no hay diff ni untracked tras correr (git status limpio).
Report: resumen corto, sin dumps.
EOF
)" </dev/null > "$OUT" 2>&1
cat "$OUT"
git -C /path/to/repo diff --stat; git -C /path/to/repo status --short
```

Reemplazar `"<ID>"` por el ID real (con comillas: sin comillas el shell lo interpreta como redirección y falla con exit 1).
Reportar corto: qué se pidió, qué devolvió, qué cambió (`git diff --stat` + `git status --short`). Nunca volcar el prompt ni el transcript crudo.

## Unhappy paths

- Binario ausente → lane bloqueada, reportar y no avanzar (señal esperada: `muse: command not found`, exit 127).
- Timeout ausente → si ni `timeout` ni `gtimeout` están disponibles, BLOQUEAR la ejecución bounded; nunca correr indefinidamente.
- Cuelgue o sin salida en 60s → matar por timeout y reportar.
- Modelo omitido → pedirlo, no defaultear.
- Failure modes: auth ausente/inválida → `muse login` (ver §Preflight); flag inexistente → solo valen los flags de `muse --help` / `muse exec --help` (no `--cd`, no `--output`, no `--sandbox`, no `--service-tier`/`--reasoning-level` de otros CLIs); modelo inválido → pedir un `<ID>` válido al usuario, no reintentar en loop.
- Approval degradado a auto sin aviso → frenar y avisar.
- Escritura sin aviso previo → frenar y avisar.
- Solo los flags documentados acá son válidos; no inventar otros.
