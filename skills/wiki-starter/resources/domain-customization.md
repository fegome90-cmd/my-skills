# Domain Customization Guide

How to tailor the wiki starter to a specific domain.

## Required Customizations

### 1. Purpose (schema file)

Replace the placeholder with a one-paragraph domain description.

Example oncology: "Knowledge base for oncology nursing exam preparation, covering 20 cancer types, treatments, pharmacology, and nursing care plans."

Example engineering: "Architecture decisions and patterns for the AgentH platform, including infrastructure, CI/CD, and deployment."

### 2. Tagging Taxonomy

Define 3-5 categories with 3-8 tags each.

**Oncology example:**
- Cancer type: solid-tumor, hematologic, pediatric
- Treatment: chemotherapy, radiotherapy, immunotherapy, surgery
- Nursing: assessment, intervention, evaluation, education
- Scope: foundational, advanced, exam-critical
- Status: well-established, emerging, investigational

**Engineering example:**
- Layer: frontend, backend, infrastructure, devops
- Decision type: architecture, pattern, config, tooling
- Status: implemented, planned, deprecated, experimental
- Scope: project-wide, component-specific, one-off

### 3. Custom Page Types

Add domain-specific types beyond the defaults:

| Default | Custom additions |
|---------|-----------------|
| concept, entity, summary, synthesis, journal | disease, treatment, component, case, experiment |

For each custom type, define:
- Directory name
- Required sections
- Template (in page-templates.md)
- Index format

### 4. Required Sections Per Type

Define minimum content for each page type.

Example: "Every disease page MUST have: Definition, Epidemiology, Fisiopatología, Estadificación TNM, Tratamiento, Pronóstico, Cuidados de Enfermería."

### 5. Language

- Page content language (English, Spanish, mixed)
- Tag language (English recommended for consistency)
- Naming convention language (usually English)

### 6. Naming Conventions

Adjust for domain:
- Oncology: `cancer-mama`, `leucemia-linfatica-aguda`
- Engineering: `auth-middleware`, `jwt-refresh-flow`
- Legal: `case-roe-wade`, `statute-gdpr-article-5`

### 7. Source Standards

Define what counts as a valid source:
- Peer-reviewed articles (PubMed, DOI)
- Official guidelines (NCCN, ASCO)
- Internal documentation
- Expert transcripts
- Minimum quality bar for acceptance

## Optional Customizations

### Confidence Calibration

Adjust confidence definitions for domain rigor:
- Medical: require multiple peer-reviewed sources for "high"
- Engineering: require code evidence for "high"
- Legal: require case law citations for "high"

### Workflow Triggers

Add domain-specific triggers:
- Oncology: "agregar MOA" → update treatment page with mechanism of action
- Engineering: "record decision" → create architecture decision page
- Research: "ingest paper" → fetch from PubMed, create summary

### Integration Hooks

Connect to external tools:
- PubMed MCP → evidence-backed content
- GitHub → link commits/PRs to wiki pages
- CI/CD → auto-lint on push
- Obsidian → Dataview, Charts, Spaced Repetition

## Migration from Existing Content

If you have existing notes/documents:

1. Copy all sources to `raw/` (preserve originals)
2. Run ingest on each source
3. Lint to find gaps
4. Customize domain settings based on what emerged
5. Iterate: ingest more sources, refine taxonomy
