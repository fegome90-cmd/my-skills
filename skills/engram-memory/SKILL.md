---
name: engram-memory
description: "Use when saving, searching, recalling, or managing persistent agent memory with Engram, SQLite, FTS5, or cross-session memory workflows."
when: "Cuando el usuario quiera guardar, recordar, buscar o gestionar memorias persistentes"
examples:
  - "recordá esto"
  - "busca en memoria"
  - "qué memorizamos antes"
  - "guarda esta información"
  - "memoria de API"
  - "busca sobre el examen"
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
  openclaw:
    requires:
      bins: ["engram"]
    emoji: "🧠"
---

# Skill: Engram Memory

> Sistema de memoria persistente para agentes de coding via Engram

## Descripción

Esta skill proporciona comandos para gestionar memoria persistente usando **Engram**:
- Guardar memorias con metadatos (tipo, proyecto, topic)
- Buscar memorias con full-text search (FTS5)
- Ver contexto de sesiones anteriores
- Timeline de observaciones
- Estadísticas del sistema de memoria

**Base de datos:** `~/.engram/engram.db`

## ⚡ Requisitos

- **Engram instalado:** `brew install gentleman-programming/tap/engram`
- **Verificar instalación:** `engram version`

## Configuración

### Instalación

```bash
# macOS / Linux
brew install gentleman-programming/tap/engram

# Verificar
engram version
```

### Proyecto por defecto

El proyecto por defecto es `examen_grado`. Para cambiar:

```bash
engram save "titulo" "contenido" --project mi-proyecto
```

## Comandos

### engram-save

Guardar una memoria.

```bash
# Uso básico
engram-save "titulo" "contenido"

# Con tipo
engram-save "titulo" "contenido" --type decision

# Tipos disponibles: decision, bugfix, discovery, learning, pattern, config

# Con proyecto
engram-save "titulo" "contenido" --project examen_grado

# Con topic (para upserts - misma info evoluciona)
engram-save "API Config" "Puerto 8080" --topic api-config
engram-save "API Config" "Puerto 8080, 3000" --topic api-config  # Actualiza el mismo
```

### engram-search

Buscar memorias.

```bash
# Buscar por keyword
engram-search "API"

# Buscar con tipo
engram-search "auth" --type decision

# Buscar en proyecto
engram-search "memoria" --project examen_grado
```

### engram-context

Ver contexto de sesiones anteriores.

```bash
# Ver todo
engram-context

# Ver de proyecto específico
engram-context examen_grado
```

### engram-timeline

Ver timeline alrededor de una observación.

```bash
# Uso
engram-timeline <id>

# Ejemplo
engram-timeline 5
```

### engram-stats

Ver estadísticas del sistema.

```bash
engram-stats
# Output: Sesiones, Observaciones, Proyectos, Database path
```

### engram-save-session

Registrar inicio de sesión.

```bash
engram-save-session
```

### engram-end-session

Marcar sesión como completada.

```bash
engram-end-session
```

## Uso en Conversación

### Guardar información importante

```
Usuario: La API de Fork está en el puerto 8080
Tu: engram-save "Fork API Config" "Puerto 8080, FORK_API_KEY configurada" --type decision
→ Memory saved: #N "Fork API Config" (decision)
```

### Recordar información previa

```
Usuario: qué sabes sobre la API?
Tu: engram-search "API"
→ #N "Fork API Config": Puerto 8080...
```

### Ver todo el contexto

```
Usuario: qué hemos hablado antes?
Tu: engram-context
→ Muestra todas las memorias de sesiones anteriores
```

## Ejemplos de Flujo

### Flujo 1: Guardar y buscar

```bash
# 1. Guardar
engram-save "Fork API" "http://127.0.0.1:8080" --type config

# 2. Buscar
engram-search "Fork"
# → #N (config) — Fork API: http://127.0.0.1:8080
```

### Flujo 2: Actualizar información (topic)

```bash
# 1. Crear
engram-save "Config" "v1: solo Fork API" --topic api

# 2. Actualizar (mismo topic)
engram-save "Config" "v2: Fork + Branch Review" --topic api

# 3. Ver timeline
engram-timeline <id>
# Muestra historial de revisiones
```

### Flujo 3: Contexto de sesión

```bash
# Al inicio de sesión
engram-context
# Muestra memorias de sesiones anteriores

# Al final
engram-end-session
```

## Integración con OpenClaw

### Estado actual

✅ **Engram MCP ACTIVO desde 2026-08-08** — el server está registrado en `mcp.servers.engram` con `enabled: true` (args `mcp --tools=agent`). En runtime están disponibles **18 tools** `engram__mem_*` (mem_save, mem_search, mem_get_observation, mem_capture_passive, mem_session_summary, mem_context, mem_update, mem_compare, mem_judge, mem_review, mem_pin, mem_unpin, mem_suggest_topic_key, mem_session_start, mem_session_end, mem_save_prompt, mem_current_project, mem_doctor).

Config real en `~/.openclaw/openclaw.json`:
```json5
mcp: {
  servers: {
    engram: {
      command: "engram",
      args: ["mcp", "--tools=agent"],
      cwd: "${PROJECT_ROOT}",
      enabled: true
    }
  }
}
```

**Preferir las tools MCP (`engram__mem_*`) sobre el CLI** cuando estén disponibles en runtime. El CLI (`engram save/search/...`) sigue funcionando como fallback.

### Alternativa: Skill wrapper

Esta skill funciona como wrapper de CLI. Los comandos internally llaman a `engram save`, `engram search`, etc.

## Errores Comunes

| Error | Solución |
|-------|----------|
| `engram: command not found` | Instalar: `brew install gentleman-programming/tap/engram` |
| `unknown command: save` | Verificar versión: `engram version` (debe ser >1.0) |
| No encuentra memorias | Verificar proyecto: `engram search "query" --project examen_grado` |

## atajos

| Alias | Comando |
|-------|---------|
| `m-save` | engram-save |
| `m-search` | engram-search |
| `m-context` | engram-context |
| `m-timeline` | engram-timeline |
| `m-stats` | engram-stats |

## Notas

- Las memorias se guardan en `~/.engram/engram.db`
- Full-text search usa SQLite FTS5
- Topics permiten upserts (actualizaciones)
- Tipos: decision, bugfix, discovery, learning, pattern, config
- scope: project (por defecto) o personal
