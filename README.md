# my-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Darwin-000000.svg?logo=apple&logoColor=white)](https://apple.com)
[![Standard](https://img.shields.io/badge/Standard-Agent%20Skills%20Spec-blueviolet.svg)](https://github.com/fegome90-cmd/my-skills)
[![Tests](https://img.shields.io/badge/Tests-Passing%20(14%2F14)-brightgreen.svg)](skills/disk-cleanup-macos-safe/tests/)

> Repositorio canónico de **Agent Skills** para arquitectura de estaciones de trabajo macOS (Darwin), depuración segura de almacenamiento APFS, configuración determinista con Nix Flakes & Home Manager, y disciplina de shell en Fish 4.3.

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

## 🧭 Catálogo de Skills

| Skill | Descripción | Componentes Clave | Disparadores Sugeridos |
|---|---|---|---|
| **[`disk-cleanup-macos-safe`](skills/disk-cleanup-macos-safe/SKILL.md)** | Diagnóstico, auditoría y recuperación segura de almacenamiento en macOS. Modela la partición System/Data, Foundation API, snapshots locales, aislamiento de caches R1 y protección de R2/R3. | `SKILL.md`<br>`README.md`<br>`scripts/`<br>`tests/`<br>`audits/` | *"liberar espacio", "disco lleno", "limpieza macos", "storage audit", "apfs purge"* |
| **[`nix-fish-homemanager`](skills/nix-fish-homemanager/SKILL.md)** | Arquitectura y directrices de Darwin: Nix Flakes, Fish 4.3 y Home Manager sin romper symlinks, orden léxico de PATH ni Keychain secrets. | `SKILL.md`<br>`assets/`<br>`references/` | *"nix flake", "home manager", "fish config", "darwin rebuild", "keychain secrets"* |
| **[`fish-shell-config`](skills/fish-shell-config/SKILL.md)** | Configuración de Fish shell verificada en máquina: superficies editables vs inmutables, autoload de funciones, y validación estricta con `fish_indent`. | `SKILL.md`<br>`references/` | *"alias terminal", "funcion fish", "config.fish", "fish_indent", "conf.d"* |
| **[`dots-maintenance`](skills/dots-maintenance/SKILL.md)** | Protocolo de actualización y auditoría de salud modular a través de 7 subsistemas (Brew, Nix, Bun, uv, Rustup, PNPM, Fisher) con `sysup` y `sysdoc`. | `SKILL.md`<br>`references/` | *"actualizar paquetes", "system maintenance", "sysup", "sysdoc", "dots-update"* |
| **[`starship-nix-manager`](skills/starship-nix-manager/SKILL.md)** | Configuración y gestión de Starship en Nix: escaping multilínea (`''${...}`) y módulos para hardware Apple Silicon (`ioreg` GPU/RAM). | `SKILL.md` | *"starship nix", "starship apple silicon", "escapar variables starship"* |
| **[`starship-prompt`](skills/starship-prompt/SKILL.md)** | Arquitectura y guía visual de diseño para prompts cross-shell: statusline, glyphs Nerd Fonts, y paletas visuales (Catppuccin, Kanagawa). | `SKILL.md`<br>`assets/`<br>`references/` | *"customizar starship", "prompt terminal", "powerline glyphs", "paleta starship"* |

---

## 📂 Estructura del Proyecto

```
my-skills/
├── .gitignore
├── LICENSE
├── README.md
└── skills/
    ├── disk-cleanup-macos-safe/
    │   ├── SKILL.md                 # Contrato operativo, clasificación R0-R3 y workflow
    │   ├── README.md                # Guía de uso de la herramienta de almacenamiento
    │   ├── audits/                  # Auditorías de diseño y arquitectura de seguridad (v2-v6)
    │   ├── references/              # Observabilidad de storage APFS y diseño UI
    │   ├── scripts/
    │   │   ├── macos_resource_probe.swift # Sonda Foundation API para capacidades reales
    │   │   └── macos_storage_audit.py     # Motor Python de auditoría y detección de gaps
    │   └── tests/
    │       ├── test_audit_logic.py        # Suite de pruebas unitarias (14 tests)
    │       ├── pressure-scenarios.md      # Escenarios de estrés y límites de disco
    │       └── synthetic-report.html      # Fixture de reporte HTML sintético
    ├── dots-maintenance/
    │   ├── SKILL.md                 # Matriz de actualización modular de 7 subsistemas
    │   └── references/runbook.md    # Runbook operativo de mantenimiento
    ├── fish-shell-config/
    │   ├── SKILL.md                 # Reglas de autoría de funciones y conf.d
    │   └── references/              # Migración bash-to-fish, secretos y testing
    ├── nix-fish-homemanager/
    │   ├── SKILL.md                 # Arquitectura de integración Darwin + Nix
    │   ├── assets/                  # Plantillas de flakes, módulos y loaders
    │   └── references/              # Bug registry (BUG-001 Fisher), Keychain y Nixpkgs
    ├── starship-nix-manager/
    │   └── SKILL.md                 # Escaping Nix y hardware Apple Silicon
    └── starship-prompt/
        ├── SKILL.md                 # Diseño visual cross-shell
        ├── assets/                  # Presets toml y módulos Nix
        └── references/              # Tabla de módulos y glifos Nerd Fonts
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
