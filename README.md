# my-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Darwin-000000.svg?logo=apple&logoColor=white)](https://apple.com)
[![Standard](https://img.shields.io/badge/Standard-Agent%20Skills%20Spec-blueviolet.svg)](https://github.com/fegome90-cmd/my-skills)
[![Tests](https://img.shields.io/badge/Tests-Passing%20(14%2F14)-brightgreen.svg)](skills/disk-cleanup-macos-safe/tests/)

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
                  │       FASE 2: MANIFIESTO INMUTABLE     │
                  │   (R0-R3, Caches R1 vs R2/R3 Críticos) │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │       FASE 3: APROBACIÓN HITL          │
                  │    (Human-In-The-Loop, non-sticky)     │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │          FASE 4: EJECUCIÓN             │
                  │ (Active-Owner Gate, 0 Sockets Vivos)   │
                  └────────────────────────────────────────┘
```

1. **Gestión Segura de Almacenamiento (Fail-Closed):**
   - La recuperación de disco nunca es un script ciego (`rm -rf` o `prune` global). Separa diagnóstico, clasificación de riesgo (R0 a R3), aprobación explícita y ejecución atómica.
   - **Active-Owner Gate:** Protección de descriptores abiertos, sockets UNIX (`pi-intercom`, `marksman`) y procesos MCP vivos (`uv`, `npm/_npx`) para evitar caídas en caliente.
2. **Inmutabilidad y Límites Declarativos (Nix + Darwin):**
   - Delimitación estricta entre el store inmutable de solo lectura (`/nix/store`) y los directorios mutables de usuario (`~/.config/fish/functions/`, `conf.d/`).
   - Cero secretos en archivos `.nix`: integración dinámica con el Keychain de macOS mediante loaders desacoplados.
3. **Disciplina de Shell (Fish 4.3):**
   - Comprensión del orden de arranque: `/etc` → `hm-session-vars` → `conf.d` → `config.fish`.
   - Regla de formateo no negociable mediante `fish_indent` y testing de funciones antes de ser añadidas al entorno interactivo.

---

## 🧭 Catálogo de Skills (31 Skills)

### 🖥️ 1. Arquitectura de Estación de Trabajo y macOS (6 skills)

| Skill | Descripción | Componentes Clave | Disparadores Sugeridos |
|---|---|---|---|
| **[`disk-cleanup-macos-safe`](skills/disk-cleanup-macos-safe/SKILL.md)** | Diagnóstico, auditoría y recuperación segura de almacenamiento en macOS. Modela la partición System/Data, Foundation API, snapshots locales, aislamiento de caches R1 y protección de R2/R3. | `SKILL.md`<br>`scripts/`<br>`tests/`<br>`audits/` | *"liberar espacio", "disco lleno", "limpieza macos", "storage audit", "apfs purge"* |
| **[`nix-fish-homemanager`](skills/nix-fish-homemanager/SKILL.md)** | Arquitectura y directrices de Darwin: Nix Flakes, Fish 4.3 y Home Manager sin romper symlinks, orden léxico de PATH ni Keychain secrets. | `SKILL.md`<br>`assets/`<br>`references/` | *"nix flake", "home manager", "fish config", "darwin rebuild", "keychain secrets"* |
| **[`fish-shell-config`](skills/fish-shell-config/SKILL.md)** | Configuración de Fish shell verificada en máquina: superficies editables vs inmutables, autoload de funciones, y validación estricta con `fish_indent`. | `SKILL.md`<br>`references/` | *"alias terminal", "funcion fish", "config.fish", "fish_indent", "conf.d"* |
| **[`dots-maintenance`](skills/dots-maintenance/SKILL.md)** | Protocolo de actualización y auditoría de salud modular a través de 7 subsistemas (Brew, Nix, Bun, uv, Rustup, PNPM, Fisher) con `sysup` y `sysdoc`. | `SKILL.md`<br>`references/` | *"actualizar paquetes", "system maintenance", "sysup", "sysdoc", "dots-update"* |
| **[`starship-nix-manager`](skills/starship-nix-manager/SKILL.md)** | Configuración y gestión de Starship en Nix: escaping multilínea (`''${...}`) y módulos para hardware Apple Silicon (`ioreg` GPU/RAM). | `SKILL.md` | *"starship nix", "starship apple silicon", "escapar variables starship"* |
| **[`starship-prompt`](skills/starship-prompt/SKILL.md)** | Arquitectura y guía visual de diseño para prompts cross-shell: statusline, glyphs Nerd Fonts, y paletas visuales (Catppuccin, Kanagawa). | `SKILL.md`<br>`assets/`<br>`references/` | *"customizar starship", "prompt terminal", "powerline glyphs", "paleta starship"* |

### 🛡️ 2. Ciclo de Vida, Seguridad y Onboarding de Skills (4 skills)

| Skill | Descripción | Componentes Clave | Disparadores Sugeridos |
|---|---|---|---|
| **[`skill-onboarding`](skills/skill-onboarding/SKILL.md)** | Motor transaccional de onboarding de skills: importación con procedencia segura, reparación de licencias, semantic-lock refactoring y verificación candidate overlay con recibos durables. | `SKILL.md`<br>`resources/`<br>`scripts/` | *"onboard skill", "instalar skill", "import skill", "repair license", "refactor skill"* |
| **[`skill-import-untrusted`](skills/skill-import-untrusted/SKILL.md)** | Protocolo de aislamiento, cuarentena y promoción atómica de skills externas o repositorios no confiables con validación de procedencia y secretos. | `SKILL.md`<br>`resources/`<br>`scripts/` | *"importar skill untrusted", "quarantine skill", "verificar skill externa", "promote candidate"* |
| **[`skill-vetting`](skills/skill-vetting/SKILL.md)** | Escáner estático de seguridad (`scan.py`) contra prompt injections, ejecución de código malicioso (`eval`, `exec`, reverse shells) y auditoría de riesgo en skills de terceros. | `SKILL.md`<br>`scripts/`<br>`references/` | *"vetting skill", "auditar skill", "escanear skill", "analizar seguridad skill"* |
| **[`template-skill`](skills/template-skill/SKILL.md)** | Scaffold y boilerplate canónico estándar para generar nuevas agent skills con frontmatter y estructura de carpetas preconfigurada. | `SKILL.md` | *"template skill", "plantilla skill", "scaffold skill", "crear starter skill"* |

### 🏗️ 3. Arquitectura de Software, Calidad y Planificación (5 skills)

| Skill | Descripción | Componentes Clave | Disparadores Sugeridos |
|---|---|---|---|
| **[`quality-plan-loop`](skills/quality-plan-loop/SKILL.md)** | Quality Plan Loop (QPL) — Ciclo iterativo de convergencia Planificador ↔ Auditor independiente con presupuestos acotados y stop conditions formales. | `SKILL.md`<br>`templates/`<br>`examples/` | *"quality plan loop", "iterar plan", "auditar plan de arquitectura", "planificador auditor"* |
| **[`work-closeout`](skills/work-closeout/SKILL.md)** | Cierre higiénico de unidades de trabajo: clasificación de residuo con evidencia (R7), cuarentena reversible y emisión de recibos de verificación. | `SKILL.md`<br>`references/`<br>`templates/` | *"close out", "limpiar temporales", "work closeout", "receipt clean reset"* |
| **[`diagram-maker-plus`](skills/diagram-maker-plus/SKILL.md)** | Generador multi-motor de diagramas técnicos de alta fidelidad: Live HTML interactivo (Plannotator B2 / Open Design), Archify JSON-IR, Mermaid.js y SVG. | `SKILL.md`<br>`resources/`<br>`scripts/` | *"crear diagrama", "diagrama interactivo", "archify router", "plannotator b2", "diagrama mermaid"* |
| **[`diagram-auditor`](skills/diagram-auditor/SKILL.md)** | Auditoría sistemática basada en evidencia para diagramas y flujogramas: clasificación estricta de afirmaciones en confirmadas, inferidas o fabricadas. | `SKILL.md`<br>`resources/`<br>`tests/` | *"audita el diagrama", "lint flowchart", "verifica diagrama contra evidencia"* |
| **[`code-path-cartographer`](skills/code-path-cartographer/SKILL.md)** | Cartografía de rutas de código: rastreo de entrypoints, llamadas entrantes/salientes, detección de símbolos huérfanos y diagramas de conectividad. | `SKILL.md`<br>`resources/` | *"mapear rutas", "code connectivity", "call paths", "buscar simbolos huerfanos"* |

### 🤖 4. Orquestación Multi-Agente y Supervisión (4 skills)

| Skill | Descripción | Componentes Clave | Disparadores Sugeridos |
|---|---|---|---|
| **[`fork-pilot`](skills/fork-pilot/SKILL.md)** | Orquestación multi-agente en tmux con separación estricta de roles: el orquestador planifica y monitorea; los agentes de fork ejecutan tareas en paralelo. | `SKILL.md`<br>`resources/` | *"fork pilot", "lanzar agentes en paralelo", "orquestar con fork", "tmux fork"* |
| **[`herdr`](skills/herdr/SKILL.md)** | Control y supervisión de terminal multiplexer para agentes de código: gestión de workspaces, tabs, paneles y captura de telemetría de ejecución. | `SKILL.md`<br>`resources/` | *"herdr", "controlar paneles", "herdr inspect", "terminal layout"* |
| **[`tmux-plan-auditor`](skills/tmux-plan-auditor/SKILL.md)** | Auditoría paralela de planes de arquitectura ejecutando 4 agentes concurrentes: lógica, calidad de código, fallos silenciosos y estrategia de testing. | `SKILL.md`<br>`resources/`<br>`scripts/`<br>`tests/` | *"auditar plan en paralelo", "tmux plan auditor", "auditoria 4 agentes"* |
| **[`picoclaw-expert`](skills/picoclaw-expert/SKILL.md)** | Base de conocimiento, patrones arquitectónicos y directrices operativas del asistente hardened de estudio PicoClaw y su runtime de ejecución. | `SKILL.md` | *"picoclaw", "hardened agent", "picoclaw patterns", "picoclaw architecture"* |

### 🧠 5. Grafos de Conocimiento, Wikis y Memoria (3 skills)

| Skill | Descripción | Componentes Clave | Disparadores Sugeridos |
|---|---|---|---|
| **[`wiki-starter`](skills/wiki-starter/SKILL.md)** | Bootstrap de bases de conocimiento LLM-maintained desde cero siguiendo el patrón Karpathy con enriquecimiento progresivo y scaffolding determinista. | `SKILL.md`<br>`resources/` | *"create wiki", "start wiki", "bootstrap wiki", "nueva wiki"* |
| **[`wiki-keeper`](skills/wiki-keeper/SKILL.md)** | Fachada y router del pipeline decomposed F0–F7 para mantenimiento, ingesta, lint y registry centralizado de wikis activas del sistema. | `SKILL.md`<br>`resources/` | *"maintain wiki", "lint wiki", "wiki health", "wiki keeper", "ingest into wiki"* |
| **[`engram-memory`](skills/engram-memory/SKILL.md)** | Protocolo de hidratación y memoria persistente en 2 pasos (`mem_search` → `mem_get_observation`) para retención durable de decisiones y descubrimientos. | `SKILL.md`<br>`scripts/` | *"engram", "guardar memoria", "mem_search", "memoria persistente"* |

### 🔬 6. Investigación Autónoma, Redacción y Herramientas Especializadas (9 skills)

| Skill | Descripción | Componentes Clave | Disparadores Sugeridos |
|---|---|---|---|
| **[`literature-search`](skills/literature-search/SKILL.md)** | Búsqueda sistemática de literatura académica y científica con filtrado riguroso por relevancia, scoring y deduplicación basada en benchmarks. | `SKILL.md`<br>`resources/`<br>`scripts/` | *"buscar papers", "literature search", "revisión bibliográfica", "buscar evidencia"* |
| **[`pi-autoresearch`](skills/pi-autoresearch/SKILL.md)** | Motor de investigación autónoma iterativa en terminal: matrices de riesgo, procedimientos de gate y protocolos de experimentación controlada. | `SKILL.md`<br>`resources/` | *"pi autoresearch", "investigacion autonoma", "bucle autoresearch"* |
| **[`scientific-writing`](skills/scientific-writing/SKILL.md)** | Redacción de manuscritos científicos, tesis y papers con estructura IMRAD y pautas de reporte formal (CONSORT, STROBE, PRISMA). | `SKILL.md`<br>`resources/` | *"escribir paper", "scientific writing", "manuscrito", "redaccion cientifica"* |
| **[`paper-writer-cli`](skills/paper-writer-cli/SKILL.md)** | Herramienta CLI para automatización y particionamiento modular de secciones en redacción de artículos científicos extensos. | `SKILL.md`<br>`resources/` | *"paper writer cli", "seccionar paper", "redactar seccion"* |
| **[`strategic-partnership-toolkit`](skills/strategic-partnership-toolkit/SKILL.md)** | Framework integral para alianzas estratégicas, auditorías de claims comerciales/técnicos, y matrices de evaluación de propuestas. | `SKILL.md`<br>`resources/`<br>`scripts/` | *"alianza estrategica", "partnership toolkit", "auditar claims", "propuesta institucional"* |
| **[`tts-lab`](skills/tts-lab/SKILL.md)** | Laboratorio de clonación y síntesis de voz a partir de audio de referencia con modelos Qwen3-TTS y creación de perfiles acústicos. | `SKILL.md`<br>`resources/` | *"tts lab", "clonar voz", "qwen3 tts", "sintesis de voz", "speaker profile"* |
| **[`presentation-builder`](skills/presentation-builder/SKILL.md)** | Diseñador de presentaciones técnicas, estructuras de diapositivas de alto impacto y frameworks conceptuales para conferencias o defensas. | `SKILL.md`<br>`resources/` | *"crear presentacion", "presentation builder", "slides tecnicos", "diapositivas"* |
| **[`color-theory-engine`](skills/color-theory-engine/SKILL.md)** | Motor determinista de teoría del color: generación de paletas accesibles (WCAG AAA), matrices de contraste y esquemas cromáticos UI. | `SKILL.md`<br>`scripts/`<br>`reference/` | *"teoria del color", "color engine", "generar paleta", "contraste accesible"* |
| **[`mcp-trifecta-server`](skills/mcp-trifecta-server/SKILL.md)** | Servidor MCP para integración de memoria, contexto de proyecto y herramientas en entornos multi-agente. | `SKILL.md`<br>`scripts/` | *"mcp trifecta", "servidor mcp", "trifecta memory"* |

---

## 📂 Estructura del Proyecto

```
my-skills/
├── .gitignore
├── LICENSE
├── README.md
└── skills/
    ├── code-path-cartographer/        # Cartografía de rutas de código y dependencias
    ├── color-theory-engine/           # Motor de teoría del color y accesibilidad
    ├── diagram-auditor/               # Auditoría de diagramas contra evidencia
    ├── diagram-maker-plus/            # Generador de diagramas Live HTML, Archify y SVG
    ├── disk-cleanup-macos-safe/       # Recuperación y auditoría de almacenamiento APFS
    ├── dots-maintenance/             # Mantenimiento de 7 subsistemas de workstation
    ├── engram-memory/                 # Memoria persistente y registro de decisiones
    ├── fish-shell-config/             # Configuración de Fish 4.3 y testing de funciones
    ├── fork-pilot/                    # Orquestación multi-agente en tmux
    ├── herdr/                         # Control de multiplexer de terminal para agentes
    ├── literature-search/             # Búsqueda y deduplicación de literatura científica
    ├── mcp-trifecta-server/           # Servidor MCP de contexto y herramientas
    ├── nix-fish-homemanager/          # Arquitectura Darwin Nix Flakes + Home Manager
    ├── paper-writer-cli/              # Automatización CLI de redacción académica
    ├── pi-autoresearch/               # Motor de investigación autónoma en terminal
    ├── picoclaw-expert/               # Directrices de arquitectura del agente PicoClaw
    ├── presentation-builder/          # Diseñador de diapositivas y estructuras técnicas
    ├── quality-plan-loop/             # Ciclo Planificador ↔ Auditor de convergencia
    ├── scientific-writing/            # Redacción formal de papers y estructura IMRAD
    ├── skill-import-untrusted/        # Cuarentena y promoción atómica de skills externas
    ├── skill-onboarding/              # Motor transaccional de onboarding y overlay
    ├── skill-vetting/                 # Escáner estático de seguridad para skills
    ├── starship-nix-manager/          # Escaping Nix y hardware Apple Silicon
    ├── starship-prompt/               # Diseño visual cross-shell y statuslines
    ├── strategic-partnership-toolkit/ # Framework de alianzas y auditoría de claims
    ├── template-skill/                # Scaffold estándar para nuevas skills
    ├── tmux-plan-auditor/             # Auditoría paralela de planes con 4 agentes
    ├── tts-lab/                       # Síntesis y clonación de voz con Qwen3-TTS
    ├── wiki-keeper/                   # Fachada y router del pipeline decomposed F0-F7
    ├── wiki-starter/                  # Bootstrap de bases de conocimiento LLM
    └── work-closeout/                 # Cierre higiénico de tareas y reset de workbench
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

El repositorio cuenta con validación estática y pruebas unitarias para los motores de diagnóstico:

```bash
# 1. Ejecutar tests unitarios de lógica de auditoría de disco (14 tests)
python3 skills/disk-cleanup-macos-safe/tests/test_audit_logic.py

# 2. Validar sintaxis y compilación de la sonda Foundation Swift
swiftc -o /dev/null skills/disk-cleanup-macos-safe/scripts/macos_resource_probe.swift

# 3. Validar sintaxis de plantillas de shell con fish_indent
fish_indent --check skills/nix-fish-homemanager/assets/keychain-loader-template.fish
```

---

## 🔒 Privacidad y Seguridad

- **Zero Hardcoded Secrets:** Este repositorio no contiene secretos, claves privadas ni archivos de entorno `.env`.
- **Rutas Sanitizadas:** Todas las plantillas y scripts utilizan `$USER`, variables de entorno o marcadores genéricos (`<username>`).
- **Aislamiento de Diagnósticos:** Los volcados crudos de hardware o telemetría local de ejecuciones previas están explícitamente excluidos en `.gitignore`.

---

## 👥 Contribuciones y Autoría

Desarrollado y mantenido por **Felipe Gonzalez**.  
Las contribuciones, correcciones y sugerencias para mejorar el ecosistema de macOS son bienvenidas mediante Pull Requests convencionales.

Distribuido bajo la Licencia [MIT](LICENSE).
