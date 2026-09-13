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

## Estructura Canónica de un Skill

```
skills/<skill-name>/
├── SKILL.md                 # Definición central, frontmatter YAML, contratos e instrucciones
├── scripts/                 # (Opcional) Scripts ejecutables acotados
│   └── helper.py
├── references/              # (Opcional) Documentación técnica y guías de referencia
│   └── guide.md
├── assets/                  # (Opcional) Plantillas y recursos estáticos
└── tests/                   # (Requerido si hay scripts) Tests y regresiones
    └── test_helper.py
```

## Creación de Scaffold

Para crear un nuevo skill, crear directamente la estructura de carpetas y el archivo `SKILL.md` canónico:

```bash
# 1. Crear directorio del skill
mkdir -p "skills/<skill-name>"

# 2. Inicializar SKILL.md con frontmatter válido
cat << 'EOF' > "skills/<skill-name>/SKILL.md"
---
name: <skill-name>
description: "Use when <trigger y alcance claro>. Do NOT use for <límites negativos>."
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
---

# <Skill Name>

## Cuándo usar / Cuándo NO usar
- **Usar cuando:** ...
- **NO usar para:** ...

## Instrucciones y Procedimiento
1. Paso 1...
2. Paso 2...
EOF
```

## Templates por Categoría

- **guidelines**: Procedimiento + Checklist + Ejemplos
- **guardrails**: Política + Bloqueos + Validación
- **workflows**: Pasos + Scripts + Validación
- **generators**: Templates + Configuración
- **test**: Estrategia + Casos + Métricas
