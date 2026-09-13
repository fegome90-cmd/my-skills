# my-skills

> Colección curada de **Agent Skills** para arquitectura, mantenimiento y configuración declarativa de estaciones de trabajo macOS (Darwin).  
> **Autor:** Felipe Gonzalez  
> **Licencia:** MIT

---

## 🎯 Filosofía y Principios Arquitectónicos

Este repositorio nuclea las skills forjadas y verificadas empíricamente en macOS para gobernar el sistema operativo, automatizar el mantenimiento preventivo y operar con seguridad destructiva cero:

1. **Gestión Segura de Almacenamiento (Fail-Closed):**
   - El espacio en disco se recupera mediante transacciones separadas: *Diagnóstico → Manifiesto Inmutable → Aprobación HITL → Ejecución*.
   - Clasificación estricta de riesgo (R0 a R3) y **Active-Owner Gate** para proteger sockets UNIX, descriptores de procesos vivos y daemons MCP en caliente.

2. **Inmutabilidad y Fronteras Claras (Nix + Darwin):**
   - Respeto absoluto a la frontera entre el store inmutable (`/nix/store`) y las superficies de usuario (`~/.config/fish/functions/`, `conf.d/`).
   - Gestión determinística de dependencias mediante Nix Flakes y Home Manager.

3. **Disciplina de Shell (Fish 4.3):**
   - Cero ambigüedad en el orden de carga: `/etc` → `hm-session-vars` → `conf.d` → `config.fish`.
   - Regla de formateo no negociable con `fish_indent` y testing de funciones antes de promoverlas a producción.

---

## 🧭 Catálogo de Skills

| Skill | Descripción | Componentes Incluidos | Disparadores / Triggers |
|---|---|---|---|
| **[`disk-cleanup-macos-safe`](skills/disk-cleanup-macos-safe/SKILL.md)** | Diagnóstico, auditoría y recuperación segura de almacenamiento en macOS. Modelo APFS, detección de gaps, aislamiento de caches regenerables (R1) y protección de datos críticos (R2/R3). | `SKILL.md`, `README.md`, `audits/`, `references/`, `scripts/`, `tests/` | *"liberar espacio", "disco lleno", "limpieza macos", "storage audit", "apfs purge"* |
| **[`nix-fish-homemanager`](skills/nix-fish-homemanager/SKILL.md)** | Guía de arquitectura y estándares para gestionar Fish Shell, Nix Flakes y Home Manager en macOS sin romper symlinks, PATH ni Keychain secrets. | `SKILL.md`, `assets/`, `references/` | *"nix flake", "home manager", "fish config", "darwin rebuild", "keychain secrets"* |
| **[`fish-shell-config`](skills/fish-shell-config/SKILL.md)** | Configuración verified-on-machine de Fish: delimitación de superficies editables vs inmutables, orden léxico de `conf.d`, y validación obligatoria con `fish_indent`. | `SKILL.md`, `references/` | *"alias para la terminal", "funcion de fish", "config.fish", "fish_indent", "conf.d"* |
| **[`dots-maintenance`](skills/dots-maintenance/SKILL.md)** | Protocolo de actualización y auditoría de salud a través de 7 subsistemas (Brew, Nix, Bun, uv, Rustup, PNPM, Fisher) con comandos `sysup` y `sysdoc`. | `SKILL.md`, `references/` | *"actualizar paquetes", "system maintenance", "sysup", "sysdoc", "dots-update"* |
| **[`starship-nix-manager`](skills/starship-nix-manager/SKILL.md)** | Gestión del prompt Starship en Nix: reglas de escaping multilínea (`''${...}`) y módulos nativos para Apple Silicon (`ioreg` para GPU y RAM). | `SKILL.md` | *"starship nix", "starship apple silicon", "escapar variables starship"* |
| **[`starship-prompt`](skills/starship-prompt/SKILL.md)** | Arquitectura y directrices de diseño para prompts cross-shell en terminales modernas: statusline, glyphs Nerd Fonts, y paletas visuales. | `SKILL.md`, `references/` | *"customizar starship", "prompt terminal", "powerline glyphs", "paleta starship"* |

---

## 🚀 Instalación e Integración con Agentes de IA

Cada skill cumple con la especificación abierta de **Agent Skills** (`SKILL.md` con frontmatter YAML estandarizado), lo que permite utilizarlas de forma transparente en múltiples asistentes (Claude Code, Pi, Google Antigravity, OpenAI Codex, OpenCode, OpenClaw).

### Symlink Global a la Red de Agentes

Para exponer estas skills a todos los entornos locales sin duplicar almacenamiento:

```bash
# Ejemplo para Agent Skills canónico (~/.agents/skills)
for skill in ~/Developer/my-skills/skills/*; do
  ln -s "$skill" ~/.agents/skills/$(basename "$skill")
done
```

---

## 📄 Licencia

Distribuido bajo la Licencia **MIT**. Consulta el archivo [`LICENSE`](LICENSE) para más información.
