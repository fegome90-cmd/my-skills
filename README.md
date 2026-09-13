# my-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Darwin-000000.svg?logo=apple&logoColor=white)](https://apple.com)
[![Standard](https://img.shields.io/badge/Standard-Agent%20Skills%20Spec-blueviolet.svg)](https://github.com/fegome90-cmd/my-skills)
[![Tests](https://img.shields.io/badge/Tests-Passing%20(92%2F92)-brightgreen.svg)](skills/)

> Repositorio canónico de **Agent Skills** desarrollado por Felipe Gonzalez: arquitectura de estaciones de trabajo macOS (Darwin), depuración de almacenamiento APFS, configuración determinista con Nix Flakes & Home Manager, motor transaccional de onboarding y escaneo de seguridad de skills, y patrones avanzados de arquitectura de software y calidad.

**Autor:** [Felipe Gonzalez](https://github.com/fegome90-cmd)  
**Licencia:** [MIT](LICENSE)

---

## 🎯 Filosofía y Principios de Ingeniería

Cada skill en este repositorio fue diseñada bajo estándares de ingeniería de sistemas de producción, priorizando la resiliencia operativa y la seguridad destructiva cero:

```
                  ┌────────────────────────────────────────┐
                  │          FASE 1: DIAGNÓSTICO           │
                  │ (Read-only, APFS System/Data, Sockets) │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │       FASE 2: CLASIFICACIÓN DE RIESGO  │
                  │   (R0-R3, Caches R1 vs R2/R3 Críticos) │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │     FASE 3: REPORTE Y PROPUESTA        │
                  │ (Deltas Medidos, Candidatos Explícitos)│
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │    FASE 4: TRASPASO MANUAL AL HUMANO   │
                  │ (Comandos Copy-Paste, 0 Mutación AI)   │
                  └────────────────────────────────────────┘
```

1. **Gestión Segura de Almacenamiento (Diagnóstico Estricto y Propuesta):**
   - La recuperación de disco nunca es un script ciego (`rm -rf` o `prune` global) ni otorga autoridad destructiva autónoma a los agentes de IA. Separa diagnóstico estricto de solo lectura, clasificación rigurosa de riesgo (R0 a R3), detección de descriptores abiertos y sockets UNIX (`pi-intercom`, `marksman`), y genera propuestas con comandos copy-pasteables explícitos para ejecución manual y soberana por parte del operador humano.
   - **Active-Owner Gate:** Protección de descriptores abiertos, sockets UNIX (`pi-intercom`, `marksman`) y procesos MCP vivos (`uv`, `npm/_npx`) para evitar caídas en caliente.
2. **Inmutabilidad y Límites Declarativos (Nix + Darwin):**
   - Delimitación estricta entre el store inmutable de solo lectura (`/nix/store`) y los directorios mutables de usuario (`~/.config/fish/functions/`, `conf.d/`).
   - Cero secretos en archivos `.nix`: integración dinámica con el Keychain de macOS mediante loaders desacoplados.
3. **Disciplina de Shell (Fish 4.3):**
   - Comprensión del orden de arranque: `/etc` → `hm-session-vars` → `conf.d` → `config.fish`.
   - Regla de formateo no negociable mediante `fish_indent` y testing de funciones antes de ser añadidas al entorno interactivo.

---

## 🧭 Catálogo de Skills (30 Skills Canónicas)

### 🖥️ 1. Arquitectura de Estación de Trabajo y macOS (6 skills)

| Skill | Descripción | Componentes Clave | Disparadores Sugeridos |
|---|---|---|---|
| **[`disk-cleanup-macos-safe`](skills/disk-cleanup-macos-safe/SKILL.md)** | Diagnóstico, auditoría y propuesta segura de recuperación de almacenamiento en macOS. Modela la partición System/Data, Foundation API, snapshots locales, aislamiento de caches R1 y protección de R2/R3. | `SKILL.md`<br>`scripts/`<br>`tests/`<br>`audits/` | *"liberar espacio", "disco lleno", "limpieza macos", "storage audit", "apfs purge"* |
| **[`nix-fish-homemanager`](skills/nix-fish-homemanager/SKILL.md)** | Arquitectura y directrices de Darwin: Nix Flakes, Fish 4.3 y Home Manager sin romper symlinks, orden léxico de PATH ni Keychain secrets. | `SKILL.md`<br>`assets/`<br>`references/` | *"nix flake", "home manager", "fish config", "darwin rebuild", "keychain secrets"* |
| **[`fish-shell-config`](skills/fish-shell-config/SKILL.md)** | Configuración de Fish shell verificada en máquina: superficies editables vs inmutables, autoload de funciones, y validación estricta con `fish_indent`. | `SKILL.md`<br>`references/` | *"alias terminal", "funcion fish", "config.fish", "fish_indent", "conf.d"* |
| **[`dots-maintenance`](skills/dots-maintenance/SKILL.md)** | Protocolo de actualización y auditoría de salud modular a través de 7 subsistemas (Brew, Nix, Bun, uv, Rustup, PNPM, Fisher) con `sysup` y `sysdoc`. | `SKILL.md`<br>`references/` | *"actualizar paquetes", "system maintenance", "sysup", "sysdoc", "dots-update"* |
| **[`starship-nix-manager`](skills/starship-nix-manager/SKILL.md)** | Configuración y gestión de Starship en Nix: escaping multilínea (`''${...}`) y módulos para hardware Apple Silicon (`ioreg` GPU/RAM). | `SKILL.md` | *"starship nix", "starship apple silicon", "escapar variables starship"* |
| **[`starship-prompt`](skills/starship-prompt/SKILL.md)** | Arquitectura y guía visual de diseño para prompts cross-shell: statusline, glyphs Nerd Fonts, y paletas visuales (Catppuccin, Kanagawa). | `SKILL.md`<br>`assets/`<br>`references/` | *"customizar starship", "prompt terminal", "powerline glyphs", "paleta starship"* |

### 🤖 2. Invocación y Orquestación de Agentes CLI y Subagentes (6 skills)

| Skill | Descripción | Componentes Clave | Disparadores Sugeridos |
|---|---|---|---|
| **[`agy-agent`](skills/agy-agent/SKILL.md)** | Invocación no interactiva de Antigravity CLI (`agy --print`) con selección obligatoria de modelo, captura atómica a archivo y política de lectura libre con aviso de escritura. | `SKILL.md` | *"agy", "agy --print", "correr tarea con agy", "headless agy"* |
| **[`codex-agent`](skills/codex-agent/SKILL.md)** | Invocación headless de Codex CLI (`codex exec`) con modelo explícito, sandbox granular (`-s read-only` / `workspace-write`) y redirección segura de stdin. | `SKILL.md` | *"codex", "codex exec", "correr tarea con codex", "headless codex"* |
| **[`interagent-dispatch`](skills/interagent-dispatch/SKILL.md)** | Estructuración de contratos tipados de ejecución (`BASIC`, `CONTROLLED`, `GOVERNED`, `FULL_ANTIDRIFT`) y recibos estructurados (`result_receipt`) para delegación y subagentes. | `SKILL.md`<br>`resources/` | *"subagent dispatch", "task delegation", "worker contracts", "result receipt"* |
| **[`muse-agent`](skills/muse-agent/SKILL.md)** | Invocación headless de Muse CLI (`muse exec`) con workspace obligatorio, modelo explícito, flag `--disable-write` para solo lectura y control estricto de aprobaciones. | `SKILL.md` | *"muse", "muse exec", "correr tarea con muse", "headless muse"* |
| **[`opencode-agent`](skills/opencode-agent/SKILL.md)** | Invocación headless de OpenCode CLI (`opencode run`) con modelo obligatorio (`-m`), captura atómica a archivo y prohibición de bypass de permisos sin aviso. | `SKILL.md` | *"opencode", "opencode run", "correr tarea con opencode", "headless opencode"* |
| **[`pi-agent`](skills/pi-agent/SKILL.md)** | Invocación headless de Pi CLI (`pi --print`) con modelo explícito (`--model`), catálogo de solo lectura (`--tools read,grep,find,ls`) y timeout acotado. | `SKILL.md` | *"pi", "pi --print", "solo lectura con pi", "inspeccionar repo con pi"* |

### 🎯 3. Gobernanza de Tareas y Worktrees (3 skills)

| Skill | Descripción | Componentes Clave | Disparadores Sugeridos |
|---|---|---|---|
| **[`anchoring-tasks`](skills/anchoring-tasks/SKILL.md)** | Preservación del envelope de trabajo mediante `ANCHOR.yaml` o límites declarativos (`intent`, `done_when`, `not_doing`) para frenar sobreingeniería y scope drift. | `SKILL.md` | *"anchoring", "anchor task", "fijar limites", "evitar sobreingenieria", "anchor.yaml"* |
| **[`herdr-worktrunk`](skills/herdr-worktrunk/SKILL.md)** | Gestión aislada de git worktrees mediante Herdr y plugin Worktrunk, soportando creación, conmutación, hooks de ciclo de vida e inspección JSON. | `SKILL.md`<br>`references/` | *"worktrunk", "herdr worktree", "isolated worktree", "wt switch", "worktree hooks"* |
| **[`grill-me-dual-herdr`](skills/grill-me-dual-herdr/SKILL.md)** | Entrevista socrática adversarial alternada entre dos agentes en Herdr + OpenCode para poner a prueba planes y arquitecturas con evidencia de código real. | `SKILL.md` | *"grill-me", "grillme", "dos agentes", "grill-a/grill-b", "estresar plan"* |

### 🔧 4. Diagnóstico de Infraestructura, SSH y Runtime (2 skills)

| Skill | Descripción | Componentes Clave | Disparadores Sugeridos |
|---|---|---|---|
| **[`learned-ssh-agent-vm-bootstrap`](skills/learned-ssh-agent-vm-bootstrap/SKILL.md)** | Diagnóstico en 5 capas de conectividad SSH a VMs Linux para agentes: resolución de config, llaves públicas, descubrimiento de binarios, túneles y reachability de protocolos. | `SKILL.md`<br>`references/` | *"ssh agent vm", "diagnostico ssh", "batchmode failure", "ssh tunnel health", "vm bootstrap"* |
| **[`pi-startup-diagnostics`](skills/pi-startup-diagnostics/SKILL.md)** | Diagnóstico acotado y resolución de colisiones de extensiones duplicadas, colisiones de puertos y carreras de registro en Pi CLI. | `SKILL.md`<br>`evals/` | *"pi startup", "tool conflicts with", "failed to load extension", "port in use", "pi diagnostics"* |

### 🛡️ 5. Ciclo de Vida, Seguridad y Onboarding de Skills (4 skills)

| Skill | Descripción | Componentes Clave | Disparadores Sugeridos |
|---|---|---|---|
| **[`skill-onboarding`](skills/skill-onboarding/SKILL.md)** | Motor transaccional de onboarding de skills: importación con procedencia segura, reparación de licencias, semantic-lock refactoring y verificación candidate overlay con recibos durables. | `SKILL.md`<br>`resources/`<br>`scripts/`<br>`tests/` | *"onboard skill", "instalar skill", "import skill", "repair license", "refactor skill"* |
| **[`skill-import-untrusted`](skills/skill-import-untrusted/SKILL.md)** | Protocolo de aislamiento, verificación de procedencia y routing seguro hacia vetting estático y motor transaccional de onboarding. | `SKILL.md` | *"importar skill untrusted", "quarantine skill", "verificar skill externa", "promote candidate"* |
| **[`skill-vetting`](skills/skill-vetting/SKILL.md)** | Escáner estático de seguridad (`scan.py`) contra prompt injections, ejecución de código malicioso (`eval`, `exec`, reverse shells) y señales de riesgo en skills de terceros. | `SKILL.md`<br>`scripts/`<br>`references/` | *"vetting skill", "auditar skill", "escanear skill", "analizar seguridad skill"* |
| **[`template-skill`](skills/template-skill/SKILL.md)** | Scaffold estándar para generar nuevas agent skills con frontmatter canónico y estructura de carpetas estándar. | `SKILL.md` | *"template skill", "plantilla skill", "scaffold skill", "crear starter skill"* |

### 🏗️ 6. Arquitectura de Software, Calidad y Planificación (7 skills)

| Skill | Descripción | Componentes Clave | Disparadores Sugeridos |
|---|---|---|---|
| **[`authority-flow-audit`](skills/authority-flow-audit/SKILL.md)** | Auditoría de arquitectura operativa, flujo de control y mutación de estado: mapeo de superficies (T1-T3), detección de doble-escritura (H1-H13), conflictos de pipeline y verificación estricta de SSOT. | `SKILL.md`<br>`resources/` | *"authority", "flow audit", "responsibility map", "SSOT", "double writer", "repo audit", "change audit"* |
| **[`quality-plan-loop`](skills/quality-plan-loop/SKILL.md)** | Ciclo iterativo y acotado de revisión de planes (Planificador ↔ Auditor independiente) con límites claros de convergencia y stop conditions formales. | `SKILL.md`<br>`templates/`<br>`examples/` | *"quality plan loop", "iterar plan", "auditar plan de arquitectura", "planificador auditor"* |
| **[`work-closeout`](skills/work-closeout/SKILL.md)** | Inspección diagnóstica y clasificación higiénica de residuo de trabajo (R7) con emisión de recibos estructurados, sin mutación destructiva autónoma. | `SKILL.md`<br>`references/`<br>`templates/` | *"close out", "limpiar temporales", "work closeout", "receipt clean reset"* |
| **[`diagram-auditor`](skills/diagram-auditor/SKILL.md)** | Auditoría sistemática basada en evidencia para diagramas y flujogramas: clasificación estricta de afirmaciones en confirmadas, inferidas o fabricadas. | `SKILL.md`<br>`resources/`<br>`tests/` | *"audita el diagrama", "lint flowchart", "verifica diagrama contra evidencia"* |
| **[`code-path-cartographer`](skills/code-path-cartographer/SKILL.md)** | Cartografía de rutas de código: rastreo de entrypoints, llamadas entrantes/salientes, detección de símbolos huérfanos y diagramas de conectividad. | `SKILL.md`<br>`resources/` | *"mapear rutas", "code connectivity", "call paths", "buscar simbolos huerfanos"* |
| **[`tmux-plan-auditor`](skills/tmux-plan-auditor/SKILL.md)** | Auditoría paralela de planes de arquitectura ejecutando 4 agentes concurrentes: lógica, calidad de código, fallos silenciosos y estrategia de testing. | `SKILL.md`<br>`resources/`<br>`scripts/`<br>`tests/` | *"auditar plan en paralelo", "tmux plan auditor", "auditoria 4 agentes"* |
| **[`scripting-technical-presentations`](skills/scripting-technical-presentations/SKILL.md)** | Redacción y auditoría de guiones técnicos, speaker notes y esquemas de diapositivas preservando límites de causalidad, evidencia e hipótesis. | `SKILL.md`<br>`agents/`<br>`references/` | *"technical presentation", "speaker notes", "guion tecnico", "auditar presentacion"* |

### 🧠 7. Sistemas de Conocimiento y Motores de Diseño (2 skills)

| Skill | Descripción | Componentes Clave | Disparadores Sugeridos |
|---|---|---|---|
| **[`wiki-starter`](skills/wiki-starter/SKILL.md)** | Bootstrap de bases de conocimiento LLM-maintained desde cero siguiendo el patrón Karpathy con enriquecimiento progresivo y scaffolding determinista. | `SKILL.md`<br>`resources/` | *"create wiki", "start wiki", "bootstrap wiki", "nueva wiki"* |
| **[`color-theory-engine`](skills/color-theory-engine/SKILL.md)** | Motor determinista de teoría del color: generación de paletas accesibles (WCAG AAA), matrices de contraste y esquemas cromáticos UI. | `SKILL.md`<br>`scripts/`<br>`reference/` | *"teoria del color", "color engine", "generar paleta", "contraste accesible"* |

---

## 📂 Estructura del Proyecto

```
my-skills/
├── .gitignore
├── LICENSE
├── README.md
└── skills/
    ├── agy-agent/                        # Invocación headless de Antigravity CLI
    ├── anchoring-tasks/                  # Preservación de boundaries con ANCHOR.yaml
    ├── authority-flow-audit/             # Auditoría de autoridad, flujo y doble-escritura
    ├── code-path-cartographer/           # Cartografía de rutas de código y dependencias
    ├── codex-agent/                      # Invocación headless de Codex CLI con sandbox
    ├── color-theory-engine/              # Motor de teoría del color y accesibilidad
    ├── diagram-auditor/                  # Auditoría de diagramas contra evidencia
    ├── disk-cleanup-macos-safe/          # Diagnóstico y propuesta de almacenamiento APFS
    ├── dots-maintenance/                # Mantenimiento de 7 subsistemas de workstation
    ├── fish-shell-config/                # Configuración de Fish 4.3 y testing de funciones
    ├── grill-me-dual-herdr/              # Entrevista socrática adversarial dual con Herdr
    ├── herdr-worktrunk/                  # Gestión aislada de git worktrees y hooks
    ├── interagent-dispatch/              # Contratos tipados de ejecución y recibos A2A
    ├── learned-ssh-agent-vm-bootstrap/   # Diagnóstico SSH en 5 capas para VMs Linux
    ├── muse-agent/                       # Invocación headless de Muse CLI
    ├── nix-fish-homemanager/             # Arquitectura Darwin Nix Flakes + Home Manager
    ├── opencode-agent/                   # Invocación headless de OpenCode CLI
    ├── pi-agent/                         # Invocación headless de Pi CLI en solo lectura
    ├── pi-startup-diagnostics/           # Diagnóstico de colisiones de extensiones en Pi
    ├── quality-plan-loop/                # Ciclo Planificador ↔ Auditor de convergencia
    ├── scripting-technical-presentations/# Redacción y auditoría de guiones técnicos
    ├── skill-import-untrusted/           # Cuarentena y enrutamiento seguro de skills externas
    ├── skill-onboarding/                 # Motor transaccional de onboarding y overlay
    ├── skill-vetting/                    # Escáner estático de seguridad para skills
    ├── starship-nix-manager/             # Escaping Nix y hardware Apple Silicon
    ├── starship-prompt/                  # Diseño visual cross-shell y statuslines
    ├── template-skill/                   # Scaffold estándar para nuevas skills
    ├── tmux-plan-auditor/                # Auditoría paralela de planes con 4 agentes
    ├── wiki-starter/                     # Bootstrap de bases de conocimiento LLM
    └── work-closeout/                    # Cierre higiénico y reporte diagnóstico de tareas
```

---

## ⚡ Requisitos del Sistema

| Componente | Requisito Mínimo | Notas |
|---|---|---|
| **Sistema Operativo** | macOS 14.0+ (Sonoma / Sequoia) | Soporta Apple Silicon (M1–M4) e Intel |
| **Shell** | Fish Shell 4.0+ | Compatible con validación `fish_indent` |
| **Gestor de Paquetes** | Nix Flakes + Home Manager | Opcional, requerido para las skills de Nix |
| **Python** | Python 3.10+ | Requerido por el motor de auditoría de disco |
| **Swift** | Swift 5.9+ / Xcode CLI Tools | Para compilar y ejecutar la sonda Foundation |

---

## 🤖 Instalación en Agentes de IA

Todas las skills siguen el formato estándar de la comunidad **Agent Skills** (`SKILL.md` con frontmatter YAML compatible). Podés vincularlas a cualquiera de tus asistentes de IA favoritos:

### 1. Claude Code
```bash
mkdir -p ~/.claude/skills
for skill in ~/Developer/my-skills/skills/*; do
  ln -s "$skill" ~/.claude/skills/$(basename "$skill")
done
```

### 2. Pi Agent / OpenCode / Codex / Antigravity
```bash
# Para Pi Agent
mkdir -p ~/.pi/agent/skills
for skill in ~/Developer/my-skills/skills/*; do
  ln -s "$skill" ~/.pi/agent/skills/$(basename "$skill")
done

# Para Agent Skills global (~/.agents/skills)
mkdir -p ~/.agents/skills
for skill in ~/Developer/my-skills/skills/*; do
  ln -s "$skill" ~/.agents/skills/$(basename "$skill")
done
```

---

## 🧪 Validación y Pruebas

El repositorio cuenta con suites de pruebas automatizadas y validación estática para todos los motores ejecutables (92 tests pasando):

```bash
# 1. Ejecutar suite completa de tests automatizados (92 tests)
python3 -m pytest skills/*/tests/

# 2. Validar sintaxis y compilación de la sonda Foundation Swift
swiftc -o /dev/null skills/disk-cleanup-macos-safe/scripts/macos_resource_probe.swift

# 3. Validar sintaxis de plantillas de shell con fish_indent
fish_indent --check skills/nix-fish-homemanager/assets/keychain-loader-template.fish
```


---

## 👥 Contribuciones y Autoría

Desarrollado y mantenido por **Felipe Gonzalez**.  
Las contribuciones, correcciones y sugerencias para mejorar el ecosistema de macOS son bienvenidas mediante Pull Requests convencionales.

Distribuido bajo la Licencia [MIT](LICENSE).
