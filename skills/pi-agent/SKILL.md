---
name: pi-agent
description: "Invoca al CLI de pi en modo print/headless (`pi --print`), con modelo elegido de forma explícita en cada uso (sin default). Solo lectura por defecto; escritura solo con aviso. Usar cuando el usuario pida listar, inspeccionar o revisar archivos sin modificar nada. Diferenciador vs codex/muse/opencode/agy-agent: esta skill invoca el CLI de pi (`pi --print`), no los otros CLIs."
search_hints:
  - pi
  - pi --print
  - pi print
  - pi headless
  - listar sin modificar
  - inspeccionar archivos con pi
  - revisar sin modificar
  - solo lectura con pi
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
triggers:
  - lista archivos sin modificar nada
  - inspecciona el repo con pi
  - revisa codigo sin cambiar nada
  - usa pi en modo print
  - corre una tarea de solo lectura con pi
---

# pi-agent

Invoca al CLI `pi` en modo headless (no interactivo) para tareas de solo lectura por defecto.

## Invocación

- Binario: `$(command -v pi)` (esperado: `/opt/homebrew/bin/pi` o en PATH)
- Modo headless: `pi --print "<tarea>"`
- Flag de modelo (OBLIGATORIO en cada uso): `--model <pattern>`
  - Acepta `provider/id` y opcionalmente `:<thinking>`.
  - NUNCA hay default hardcodeado: si el usuario no indica el modelo, se le pide cada vez. No asumir ni reutilizar en silencio el de un uso anterior.
  - Verificá que tu comando incluya `--model` literal antes de invocar; el CLI tiene default propio y NO fallará si lo omitís (defaultea silencioso).
  - `<pattern>` no corre tal cual: reemplazar por un ID real de `pi --list-models` (tal cual falla con `Error: Model "<pattern>" not found`).
- Lookup mandatorio antes de invocar (no adivinar IDs): `pi --list-models [búsqueda]` y usar el ID del catálogo tal cual (acepta `provider/id` y opcionalmente `:<thinking>`).
- Provider por defecto: `google` (vía `--provider`, default del propio CLI). Documentado tal cual; no cambiar de provider sin aviso explícito al usuario en el mismo uso.
- Preflight antes de invocar: `pi --help` responde (exit 0) y `pi auth check --provider <provider>` en verde; si auth falla, frenar y pedir al usuario que autentique (no inventar flags de login: `pi --help` no lista ninguno).
- Workdir explícito + captura a archivo: `pi` no tiene `--cd` ni `--output` en su `--help`, así que fijar directorio con `cd /path/to/repo` (o `git -C`) y capturar con `OUT=$(mktemp /tmp/pi-out.XXXXXX)` + `... > "$OUT"`; el mensaje final = el entregable (`cat "$OUT"`).
- `</dev/null` mandatorio en cada invocación no interactiva: stdin abierto se interpreta como contexto extra y el proceso espera EOF para siempre (cuelgue sin output); siempre cerrar stdin.
- One-task-per-launch: una tarea autocontenida por invocación; tras ejecutar, revisar `git diff --stat` / `git status --short` en el workdir antes de declarar done.
- Molde ciego (el worker no ve tu contexto; todo va en el prompt): Objective (una frase) / Constraints (solo-lectura vs implementar, sin push, sin prod) / Deliverable (qué devolver) / Validation (cómo sabe que terminó) / Report (corto, ver §Ejemplo). Lo de "Skills/files to use" de la fuente se absorbe en Constraints.

## Política de permisos (lectura-libre + escritura-con-aviso)

- Lectura libre del repo/directorio de trabajo.
- Toda invocación read-only DEBE incluir `--tools read,grep,find,ls` (los tools `edit`, `write` y `bash` vienen habilitados por defecto y obedecen escritura sin aviso).
- Cualquier escritura, edición o apply SOLO tras aviso explícito al usuario en el mismo uso.
- Ante prompt de escritura/exfiltración: pedir aviso en el mismo uso; si hay duda, rehusar.
- No introducir flags de auto-approve / full-access por defecto.
- Nota: se evaluó `disable-model-invocation: true` y se rechazó — la skill debe seguir invocable por el modelo; el control es el aviso previo en escrituras, no el bloqueo de invocación.

## Ejemplo (solo lectura)

```sh
cd /path/to/repo  # workdir explícito: pi no tiene --cd
OUT=$(mktemp /tmp/pi-out.XXXXXX)
MODEL="<provider/id>"  # ID real de `pi --list-models`, nunca un pattern inventado
timeout 60 pi --print --model "$MODEL" --tools read,grep,find,ls "Objective: listar archivos sin modificar nada. Constraints: READ ONLY, sin writes. Deliverable: lista. Validation: sin cambios en git. Report: corto." > "$OUT" </dev/null
cat "$OUT"
git diff --stat
```

Notas: el modo "solo lectura" igual escribe `_ctx/`, `.atl/`, `.pi/` y `.gitignore` en el CWD — correr en scratch o sesión dedicada. La combinación `--print --no-session` puede colgar por extensiones en segundo plano; usar siempre el wrapper `timeout 60 ... < /dev/null`.

Reportes cortos sin dumps: devolver solo modelo usado, workdir, read-only vs implement y resultado/diff resumido; no volcar prompt ni output completo en el contexto padre.

## Failure modes

- Auth ausente (`pi auth check` falla) → frenar y pedir autenticación al usuario; no intentar workarounds.
- Flag inexistente (p. ej. `--cd`, `--output`, `--sandbox`) → no existe en `pi --help`; usar `cd` + redirección `>` en su lugar.
- Modelo inválido (`Error: Model "<pattern>" not found`) → re-hacer lookup con `pi --list-models [búsqueda]`; nunca adivinar IDs.
- Cuelgue sin output → stdin abierto o combinación `--print --no-session` con extensiones en segundo plano; matar, relanzar con `</dev/null` y wrapper `timeout 60`.

Solo flags documentados: `--print`, `--model <pattern>`, `--provider` (default `google`), `--tools`/`-t`, `--exclude-tools`/`-xt`, `--list-models`, `--no-session`, `--offline`.
