---
name: template-skill
description: "Use when generating a starter template, scaffold, or boilerplate for a new skill and you want preconfigured metadata and structure."
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
when: "Al crear un nuevo skill necesitas una plantilla base"
examples:
  - "Template skill"
  - "Plantilla skill"
  - "Skill scaffold"
---

# Template Skill

## Objetivo

Generar templates de alta calidad para nuevos skills.

## Comandos

```bash
# Crear template
skills create-template <category> <skill-name> --type <type>

# Generar recursos
skills generate-resources <skill-id>

# Validar template
skills validate-template <template-path>
```

## Templates por Categoría

- **guidelines**: Procedimiento + Checklist + Ejemplos
- **guardrails**: Política + Bloqueos + Validación
- **workflows**: Pasos + Scripts + Validación
- **generators**: Templates + Configuración
- **test**: Estrategia + Casos + Métricas
