# my-skills

Este repositorio guarda skills creadas y curadas para agentes, bajo control de versiones y disponibles para revisión. Su propósito es conservarlas como un registro personal que pueda trasladarse a otra máquina, no funcionar como producto, marketplace ni runtime único.

## Qué guarda este repositorio

Cada paquete vive en `skills/<nombre>/` y contiene un `SKILL.md`; según sus necesidades, también puede incluir recursos locales como `scripts/`, `tests/`, `references/`, `resources/`, `templates/`, `assets/`, `evals/` o ejemplos. Este README es el mapa general, pero el archivo `skills/<nombre>/SKILL.md` de cada paquete es la autoridad sobre su alcance, requisitos y forma de uso. El inventario actual reúne 39 paquetes de skills versionados.

## Inventario

### Wrappers de CLI de agentes

- [`agy-agent`](skills/agy-agent/SKILL.md): documenta la invocación no interactiva de `agy --print`, con modelo explícito y aviso previo a cualquier escritura.
- [`codex-agent`](skills/codex-agent/SKILL.md): documenta `codex exec` en modo headless, con modelo y sandbox declarados.
- [`muse-agent`](skills/muse-agent/SKILL.md): documenta `muse exec` con workspace y modelo explícitos, usando `--disable-write` para tareas de lectura.
- [`opencode-agent`](skills/opencode-agent/SKILL.md): documenta `opencode run` con selección explícita de modelo y límites de permisos.
- [`pi-agent`](skills/pi-agent/SKILL.md): documenta `pi --print` para tareas headless, con modelo explícito y herramientas de solo lectura por defecto.

### Estación de trabajo y runtime

- [`disk-cleanup-macos-safe`](skills/disk-cleanup-macos-safe/SKILL.md): guía diagnósticos de almacenamiento en macOS, clasifica riesgos y propone candidatos sin ejecutar eliminaciones.
- [`dots-maintenance`](skills/dots-maintenance/SKILL.md): guía mantenimiento, diagnóstico y rollback de los gestores usados por una estación de trabajo concreta.
- [`fish-shell-config`](skills/fish-shell-config/SKILL.md): documenta los límites entre configuración Fish administrada y editable, junto con sus comprobaciones.
- [`learned-ssh-agent-vm-bootstrap`](skills/learned-ssh-agent-vm-bootstrap/SKILL.md): separa el diagnóstico SSH hacia una VM en capas de configuración, autenticación, runtime, transporte y protocolo.
- [`nix-fish-homemanager`](skills/nix-fish-homemanager/SKILL.md): reúne criterios para gestionar Fish, Nix Flakes y Home Manager en macOS.
- [`pi-extension-builder`](skills/pi-extension-builder/SKILL.md): reúne referencias y plantillas para diseñar, implementar y revisar extensiones TypeScript para Pi.
- [`pi-startup-diagnostics`](skills/pi-startup-diagnostics/SKILL.md): diagnostica arranques fallidos de Pi por extensiones duplicadas, herramientas en conflicto o puertos ocupados.
- [`prompt-doctor`](skills/prompt-doctor/SKILL.md): crea y diagnostica plantillas de prompts de Pi, incluidos frontmatter YAML, descubrimiento y expansión de argumentos.
- [`starship-nix-manager`](skills/starship-nix-manager/SKILL.md): cubre configuración de Starship desplegada mediante Nix y Home Manager, incluido el escaping propio de Nix.
- [`starship-prompt`](skills/starship-prompt/SKILL.md): guía el diseño y ajuste de prompts Starship en distintos shells y en Home Manager.

### Ciclo de vida de skills

- [`learned-progressive-disclosure`](skills/learned-progressive-disclosure/SKILL.md): separa una skill extensa en un punto de entrada breve y recursos específicos por fase.
- [`skill-import-untrusted`](skills/skill-import-untrusted/SKILL.md): enruta la incorporación de skills no confiables a revisión estática y onboarding transaccional.
- [`skill-onboarding`](skills/skill-onboarding/SKILL.md): define un flujo transaccional para importar, normalizar, verificar y promover skills existentes.
- [`skill-vetting`](skills/skill-vetting/SKILL.md): combina escaneo estático y revisión manual para evaluar skills de terceros antes de adoptarlas.
- [`template-skill`](skills/template-skill/SKILL.md): ofrece una estructura inicial para crear un paquete de skill con metadatos y recursos opcionales.

### Coordinación y control del trabajo

- [`ai-work-prompting-gates`](skills/ai-work-prompting-gates/SKILL.md): es una guía y lista de chequeo de referencia para prompts con separación de audiencias, compuertas ejecutables, staging/rollback y disciplina de evidencia.
- [`anchoring-tasks`](skills/anchoring-tasks/SKILL.md): conserva los límites de intención, resultado esperado y exclusiones de una tarea.
- [`claude-md-optimizer`](skills/claude-md-optimizer/SKILL.md): analiza `CLAUDE.md` y propone cambios usando las plantillas incluidas para programación funcional en Python y Clean Architecture en TypeScript.
- [`grill-me-dual-herdr`](skills/grill-me-dual-herdr/SKILL.md): organiza una entrevista adversarial alternada entre dos agentes sobre un plan o diseño.
- [`herdr-worktrunk`](skills/herdr-worktrunk/SKILL.md): gestiona worktrees aislados mediante Herdr y Worktrunk, incluidos sus hooks de ciclo de vida.
- [`interagent-dispatch`](skills/interagent-dispatch/SKILL.md): estructura contratos tipados y recibos para delegar trabajo entre agentes.
- [`learned-pr-feedback-resolution`](skills/learned-pr-feedback-resolution/SKILL.md): organiza feedback automatizado de CodeRabbit y Copilot por severidad y WorkOrders.
- [`quality-plan-loop`](skills/quality-plan-loop/SKILL.md): define un ciclo acotado entre planificación y auditoría independiente de planes.
- [`tmux-plan-auditor`](skills/tmux-plan-auditor/SKILL.md): audita planes en paralelo desde cuatro perspectivas y produce un handoff en JSON.
- [`work-closeout`](skills/work-closeout/SKILL.md): inspecciona y clasifica residuos de trabajo sin realizar limpieza destructiva.

### Inspección, conocimiento y herramientas enfocadas

- [`authority-flow-audit`](skills/authority-flow-audit/SKILL.md): audita autoridad, flujos, escritores en competencia y supuestas fuentes únicas de verdad.
- [`code-path-cartographer`](skills/code-path-cartographer/SKILL.md): rastrea entrypoints, referencias y alcanzabilidad sin emitir veredictos de autoridad.
- [`color-theory-engine`](skills/color-theory-engine/SKILL.md): genera y analiza paletas, armonías y relaciones de contraste para interfaces.
- [`diagram-auditor`](skills/diagram-auditor/SKILL.md): contrasta diagramas con evidencia y clasifica sus afirmaciones antes de entregarlos.
- [`learned-accuracy-fallacy-audit`](skills/learned-accuracy-fallacy-audit/SKILL.md): audita afirmaciones separando consistencia interna, verificación factual externa y errores de razonamiento.
- [`learned-keynote-to-mp4-pipeline`](skills/learned-keynote-to-mp4-pipeline/SKILL.md): documenta un pipeline específico de macOS: Keynote → PDF/imágenes → MP4 sincronizado con audio.
- [`learned-structured-review`](skills/learned-structured-review/SKILL.md): estructura revisiones con hallazgos numerados, severidades BLOCK/WARN/SUGGEST y correcciones concretas.
- [`scripting-technical-presentations`](skills/scripting-technical-presentations/SKILL.md): redacta o audita guiones, notas y esquemas de presentaciones técnicas preservando evidencia y límites.
- [`wiki-starter`](skills/wiki-starter/SKILL.md): prepara la estructura inicial de una wiki mantenida por LLM y su flujo de enriquecimiento progresivo.

## Llevarlo a otra máquina

Cloná el repositorio desde su origen y definí una variable para no depender de una ruta personal fija:

```sh
git clone https://github.com/fegome90-cmd/my-skills.git
cd my-skills
SKILLS_REPO=$PWD
export SKILLS_REPO
```

El directorio donde un agente descubre skills depende del consumidor. En el entorno actual se usan, por ejemplo, `~/.pi/agent/skills`, `~/.agents/skills` y `~/.claude/skills`; antes de elegir uno, verificá la convención vigente en la documentación del agente de destino.

Para vincular una sola skill, elegí el destino y el nombre. El chequeo con `-e` y `-L` detecta tanto rutas existentes como enlaces simbólicos rotos; el ejemplo nunca reemplaza ni elimina el destino:

```sh
SKILLS_TARGET=$HOME/.pi/agent/skills
skill=pi-agent
src=$SKILLS_REPO/skills/$skill
dst=$SKILLS_TARGET/$skill

if [ ! -f "$src/SKILL.md" ]; then
  printf '%s\n' "No existe un paquete válido en: $src" >&2
  exit 1
fi

mkdir -p "$SKILLS_TARGET"
if [ -e "$dst" ] || [ -L "$dst" ]; then
  printf '%s\n' "Destino ocupado; no se modificó: $dst" >&2
  exit 1
fi

ln -s "$src" "$dst"
```

Para vincular todas las skills sin pisar destinos existentes:

```sh
SKILLS_TARGET=$HOME/.pi/agent/skills
mkdir -p "$SKILLS_TARGET"

for src in "$SKILLS_REPO"/skills/*; do
  [ -f "$src/SKILL.md" ] || continue
  skill=${src##*/}
  dst=$SKILLS_TARGET/$skill

  if [ -e "$dst" ] || [ -L "$dst" ]; then
    printf '%s\n' "Omitida por colisión: $dst" >&2
    continue
  fi

  ln -s "$src" "$dst"
done
```

Los enlaces apuntan al checkout clonado. Si luego lo movés, actualizá los enlaces de manera consciente en vez de ocultar la colisión con una sobrescritura.

## Dependencias

No hay requisitos globales para todo el repositorio: cada `SKILL.md` declara o explica lo que necesita su propio flujo. Por ejemplo, las skills de estación de trabajo pueden depender de macOS, Nix o Fish; algunos helpers usan Python o Swift; y las skills de coordinación pueden requerir tmux o un CLI de agente específico. Instalá o configurá esas herramientas sólo al usar la skill correspondiente y siguiendo su documentación.

## Validación

La colección amplia de pruebas disponible en los paquetes con `tests/` puede ejecutarse desde la raíz con:

```sh
python3 -m pytest skills/*/tests/
```

También se puede comprobar un paquete por separado cuando se está trabajando en él:

```sh
python3 -m pytest skills/color-theory-engine/tests/
python3 -m pytest skills/diagram-auditor/tests/
python3 -m pytest skills/disk-cleanup-macos-safe/tests/
python3 -m pytest skills/skill-onboarding/tests/
python3 -m pytest skills/tmux-plan-auditor/tests/
```

Estas órdenes usan archivos rastreados por Git, pero sus dependencias siguen siendo específicas de cada skill. Consultá el `SKILL.md` y los recursos del paquete antes de interpretar un fallo o agregar herramientas al sistema.

## Procedencia y licencias

El repositorio reúne trabajo creado y curado. Al incorporar o redistribuir una skill, conservá sus datos de procedencia, atribución y licencia upstream.

La raíz se distribuye bajo la [licencia MIT](LICENSE), con copyright 2026 Felipe Gonzalez. Además, `skills/skill-import-untrusted/SKILL.md` y `skills/skill-onboarding/SKILL.md` declaran Apache-2.0 a nivel de cada skill; esa declaración no reemplaza la revisión de los archivos y metadatos de cada paquete antes de redistribuirlo.

## Mantenimiento

Al agregar una skill o preparar otra máquina:

- Confirmá que el paquete tenga `SKILL.md` y que sus enlaces relativos resuelvan.
- Revisá alcance, dependencias, procedencia y licencia en el paquete, no sólo en este mapa.
- Actualizá este inventario cuando cambien las skills rastreadas.
- Ejecutá las comprobaciones del paquete afectado y registrá sólo contenido portable.
- Revisá `git status` antes de sincronizar; `.pi/`, `.pytest_cache/`, `.atl/`, `_ctx/`, `__pycache__/` y otros estados o caches locales no forman parte del contenido portable.
