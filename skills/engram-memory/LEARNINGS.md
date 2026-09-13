# Engram Memory - Aprendizajes

## Fecha de creación

2026-03-08

## Lo que SÍ funciona:

- ✅ `engram save` - Guardar memorias con tipo, proyecto, topic
- ✅ `engram search` - Búsqueda full-text
- ✅ `engram context` - Contexto de sesiones anteriores
- ✅ `engram timeline` - Ver historial de una observación
- ✅ `engram stats` - Estadísticas
- ✅ Topic keys - Upserts actualizan misma memoria
- ✅ Tipos: decision, bugfix, discovery, learning, pattern, config
- ✅ Export/Import JSON

## Lo que NO funciona / Limitaciones:

- ❌ OpenClaw no tiene soporte MCP nativo configurado
- ❌ La skill usa CLI wrapper, no MCP directo
- ⚠️ Engram MCP server configurado en ~/.config/opencode/ pero OpenClaw no lo lee

## Integración futura

Para integración MCP completa con OpenClaw:
1. Agregar `mcp` al schema de OpenClaw (feature request)
2. O usar skill wrapper (actual) + triggers naturales

## Comandos probados

```bash
# Guardar
engram save "titulo" "contenido" --type learning --project examen_grado

# Buscar
engram search "API"

# Contexto
engram context

# Timeline
engram timeline 5

# Stats
engram stats
```

## Base de datos

- Ubicación: `~/.engram/engram.db`
- Tamaño actual: ~14KB
- Total observaciones: 6
