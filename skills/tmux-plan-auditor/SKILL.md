---
name: tmux-plan-auditor
description: "Use for parallel plan auditing with 4 agents: logic, code-quality, silent-failures, testing. Fast mode (default, ~1.3s) or interactive mode (--interactive, tmux). Do NOT use for single-agent review."
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "2.1.0"
  triggers:
    - "audit plan"
    - "review plan"
    - "parallel agents"
    - "tmux agents"
    - "plan review"
  role: specialist
  scope: review
search_hints: plan-audit parallel-agents tmux code-review logic silent-failures testing handoff json multi-agent review checklist domain-detection
---

# tmux Plan Auditor (JSON handoff v2)

Corre 4 agentes en paralelo y genera salida `.json` optimizada para handoff entre agentes.

**Modo rápido (default)**: ~1.3s por run, sin tmux.
**Modo interactivo**: `--interactive`, agentes en ventanas tmux para debugging.

## Parámetros de auditoría (4 frentes)

1. **Lógica del plan** - Ambigüedades, alcance, criterios
2. **Calidad / simplificación de código** - Refactors, smells, cambios estructurales
3. **Silent failures** - Observabilidad, manejo de errores, degradación
4. **Testing estático y cobertura** - Quality gates, validación

## Inputs

- `PLAN_PATH` (requerido)
- `-w|--workflow` (opcional, default `feature`)
- `-i|--interactive` (opcional, activa modo tmux)
- `-s|--session` (opcional, default `plan-audit`)

## Configuración

Variables de entorno:

| Variable | Default | Descripción |
|----------|---------|-------------|
| `AUDITOR_AGENT_TIMEOUT` | `300` | Timeout por agente en segundos |
| `AUDITOR_AUTO_CLEANUP` | `true` | Cerrar sesión tmux tras éxito (solo interactive) |
| `AUDITOR_INTERACTIVE` | `false` | Forzar modo interactivo (alternativa a `--interactive`) |
| `AUDITOR_PROJECT_ROOT` | `$(pwd)` | Root del proyecto para reglas y static checks |
| `AUDITOR_PLAN_DOMAIN` | auto-detect | Forzar dominio (`tui-rich\|web-api\|cli\|generic`) |
| `AUDITOR_WORKFLOW` | `feature` | Forzar workflow (`feature\|bugfix\|refactor\|security`) |

Reglas personalizadas:

Crea `.pi/auditor-rules.yaml` en tu proyecto para sobreescribir reglas por defecto. Las reglas soportan `applies_to` para filtrar por dominio.

## Ejecución

```bash
# Fast mode (default, ~1.3s)
bash scripts/run_tmux_plan_audit.sh <PLAN_PATH>

# Interactive mode (tmux)
bash scripts/run_tmux_plan_audit.sh <PLAN_PATH> --interactive

# Con workflow
bash scripts/run_tmux_plan_audit.sh <PLAN_PATH> -w security
```

## Detección de Dominio

El auditor clasifica automáticamente el plan:

| Dominio | Keywords | Ejemplo |
|---------|----------|---------|
| `tui-rich` | Rich, Textual, Textualize | Plans de UI terminal |
| `web-api` | FastAPI, Flask, Express.js, endpoint | Plans de API/HTTP |
| `cli` | CLI, terminal, Typer, Click | Plans de herramientas CLI |
| `generic` | (ningún keyword) | Cualquier otro plan |

Las reglas con `applies_to` se filtran según el dominio detectado. Override con `AUDITOR_PLAN_DOMAIN`.

## Salida esperada

En `_ctx/review_runs/<RUN_ID>/`:
- `agent-logic.json` - Hallazgos del agente de lógica
- `agent-code-quality.json` - Hallazgos de calidad
- `agent-silent-failure.json` - Hallazgos de silent failures
- `agent-testing-static.json` - Hallazgos de testing + resultados de comandos
- `handoff.json` - **Principal** (v2)
- `patch-confirmation-template.json` - Plantilla para decisiones del usuario
- `summary.md` - Resumen legible

## Contrato de `handoff.json` (v2)

```json
{
  "schema_version": "2.0",
  "plan_domain": "tui-rich",
  "execution_summary": {
    "total_duration_ms": 1337,
    "overall_confidence": 0.98,
    "agents_completed": 4,
    "agents_failed": 0,
    "agents_timeout": 0,
    "agents_missing": 0,
    "agents_invalid": 0,
    "session_cleaned_up": true
  },
  "findings": [...],
  "deduplicated_patch_candidates": [...],
  "decision_rules": {
    "allowed_user_decisions": ["approved", "rejected", "deferred"]
  }
}
```

## Contrato de `patch-confirmation-template.json`

Plantilla para que el agente padre capture decisión final por parche:
- `patch_id`
- `user_decision` (`approved|rejected|deferred`)
- `user_notes`
- `approved_by`
- `approved_at`

## Regla de handoff al agente padre

El agente padre debe:
1. Leer `handoff.json`.
2. Presentar **solo** `deduplicated_patch_candidates` al usuario.
3. Capturar decisiones en `patch-confirmation-template.json`.
4. Aplicar únicamente parches con `user_decision = approved`.
5. Reportar qué parches fueron rechazados o diferidos.

## Arquitectura

```
resources/
├── agents/           # Agentes modulares (Python)
│   ├── base_agent.py           # Core: domain detection, rule engine, CLI
│   ├── logic_agent.py          # Ambigüedades y alcance
│   ├── code_quality_agent.py   # Refactors y smells
│   ├── silent_failure_agent.py # Observabilidad y errores
│   └── testing_static_agent.py # Quality gates y comandos
├── rules/            # Reglas externalizadas
│   ├── loader.py               # Rule loading + caching + merge
│   └── default.yaml            # Reglas base por agente
└── handoff_builder.py          # Agregador de resultados v2
scripts/
├── run_tmux_plan_audit.sh      # Orquestador
└── detect_domain.py            # Detección de dominio standalone
tests/                          # 21 tests unitarios
├── conftest.py
├── test_detect_domain.py
├── test_loader.py
├── test_handoff_builder.py
└── test_static_commands.py
```

## Criterios de calidad

- No hacer refactors grandes sin aprobación.
- Priorizar alto impacto / bajo esfuerzo.
- Evitar silent failures en el propio reporte.
- Mantener evidencia trazable por archivo/línea.
- Contexto de propuestas: detectar cuando el plan **propone** algo vs cuando **carece** de algo.
- Findings con confidence < 0.3 se filtran automáticamente.

## Testing

```bash
cd skills/tmux-plan-auditor
python3 -m pytest tests/ -v
```

21 tests: domain detection, rule loading/caching, payload validation, stack detection.

## Comandos de inspección

```bash
# Ver sesión tmux activa (solo interactive mode)
tmux attach -t <SESSION_TARGET>

# Ver último handoff
cat _ctx/review_runs/*/handoff.json | python3 -m json.tool | tail -20

# Ver reglas por defecto
cat ~/.pi/agent/skills/tmux-plan-auditor/resources/rules/default.yaml
```
