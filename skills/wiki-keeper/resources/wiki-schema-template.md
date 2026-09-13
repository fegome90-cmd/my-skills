# WIKI-SCHEMA.md — {{WIKI_NAME}} Configuration

> Template base para wikis Karpathy-style.
> Copiar a la raíz de cada wiki y reemplazar {{PLACEHOLDERS}}.
> Las secciones universales (frontmatter, cross-refs, naming) se actualizan desde este template.

## Directory Structure

```
{{WIKI_ROOT}}/
├── raw/                        # Immutable source documents (never modify)
│   ├── sources/                # PDFs, articles, clippings
│   └── assets/                 # Images, diagrams (local)
│
├── METHODOLOGY.md              # General wiki methodology (Karpathy pattern)
├── WIKI-SCHEMA.md              # This file — domain-specific conventions
├── index.md                    # Content catalog (read first on every query)
├── log.md                      # Append-only activity log
│
├── {{SECTION_A}}/              # Entity type A
├── {{SECTION_B}}/              # Entity type B
└── {{SECTION_C}}/              # Entity type C
```

## Page Types & Frontmatter

Every wiki page must have YAML frontmatter:

### Entity Pages (template)
```yaml
---
type: {{entity_type}}    # one of: {{TYPE_OPTIONS}}
tags: [{{domain}}, {{specific_tags}}]
sources:
  - "{{reference}}"
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active          # active | draft | needs-review | inbox
dates:                  # opcional — tracking de calidad
  ai_generated: full    # none | partial | full — qué % fue generado por AI
  caveats: false        # true si se verificaron limitaciones explícitamente
---
```

### Status Key
- `active` — revisada y aprobada
- `draft` — en construcción
- `needs-review` — requiere verificación humana
- `inbox` — captura sin procesar (vía pipeline web-capture)

## Cross-Reference Typing

Para hacer las conexiones más semánticas, los wikilinks pueden incluir un tipo de relación:

```markdown
- [[page-a|trata]] — 💊 relación de tratamiento
- [[page-b|causa]] — 🔗 relación causal
- [[page-c|asociado-a]] — ↔️ asociación
```

### Tipos de relación (universales)

| 🔤 Tipo | Emoji | Significado |
|---|---|---|
| `trata` | 💊 | Relación de tratamiento |
| `indica` | 🔬 | Indicación |
| `usa` | 🧠 | Concepto usado |
| `causa` | 🔗 | Relación causal |
| `complica` | ⚠️ | Complicación potencial |
| `asociado-a` | ↔️ | Asociación no causal |
| `ver-tambien` | 📖 | Lectura relacionada |

### Tipos específicos del dominio

*Añadir aquí los tipos de relación propios de {{WIKI_NAME}}.*

## Page Templates

### {{SECTION_A}} Structure
```markdown
# [Entity Name]

[One-paragraph summary]

## Definición
## Componentes / Secciones
## Referencias
```

### {{SECTION_B}} Structure
```markdown
# [Entity Name]

[One-paragraph summary]

## Definición
## Componentes / Secciones
## Referencias
```

*Personalizar secciones según el dominio.*

## Workflows

### Ingest (new source)
1. Source goes to `raw/sources/`
2. LLM reads source, discusses takeaways
3. Create/update wiki pages with proper frontmatter
4. Update `index.md`
5. Cross-reference: link related pages
6. Append to `log.md`: `## [YYYY-MM-DD] ingest | Source Title`
7. Run caveats check (ver `caveats: true` antes de `status: active`)

### Query
1. Read `index.md` first
2. Identify relevant pages
3. Read those pages, synthesize answer with `[[wikilink]]` citations
4. If answer is substantial → file as new wiki page

### Lint (run periodically)
- [ ] All pages have valid frontmatter with `type`, `tags`, `updated`
- [ ] No orphan pages (every page linked from index or another page)
- [ ] No broken `[[wikilink]]` links
- [ ] `updated` dates are current
- [ ] No contradictions between related pages
- [ ] Concepts referenced in pages have their own page

## Cross-Reference Conventions

- Use `[[wikilink]]` for internal links
- Every page links to its related pages
- Bidirectional cross-refs when possible
- Prefer typed refs: `[[page|tipo]]`

## Naming Conventions

- Files: `kebab-case.md` (e.g., `my-entity.md`)
- Tags: `kebab-case` (e.g., `{{domain}}-tag`)

## Language

{{LANGUAGE}} — Technical terms in original language.

---
*Template base v1.0.0 — Fuente: wiki-keeper v1.7.0*
*Última actualización: 2026-07-26*
