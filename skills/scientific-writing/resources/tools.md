# Recommended Tools for Scientific Writing

> Resource for `scientific-writing` skill. Recommend tools based on the task, not on habit. Match the tool to the user's level, budget, and workflow.

---

## Decision Matrix: Quick Recommendations

| "I need to..." | Tool | Why |
|----------------|------|-----|
| Manage references | **Zotero** | Free, open-source, integrates with everything |
| Run statistical analysis | **R / RStudio** | Reproducible, publication-quality figures, free |
| Write and render with citations | **Quarto + BibTeX** | Our default pipeline; separates content from formatting |
| Check grammar | **Grammarly (free)** | Catches common errors; premium adds advanced suggestions |
| Simplify dense prose | **Hemingway App** | Highlights overly complex sentences |
| Collaborate on drafts | **Google Docs** or **Overleaf** | Real-time multi-author editing |
| Build a PRISMA flow diagram | **PRISMA2020 web app** | Generates compliant flow diagrams |

---

## 1. Reference Managers

### Zotero ⭐ Recommended default

- **Cost:** Free, open-source
- **Best for:** Most researchers; our default recommendation
- **Strengths:** Browser extension grabs citations; 9000+ citation styles; integrates with Word/LibreOffice/Google Docs; local storage with sync; tag and organize with collections
- **Weaknesses:** PDF annotation is basic; no social features
- **Setup tip:** Install Zotero Connector browser extension. Set up a group library for collaborative projects.

### Mendeley

- **Cost:** Free (Elsevier account)
- **Best for:** Users already in the Elsevier ecosystem
- **Strengths:** PDF reader with annotation; social network features; large crowdsourced database
- **Weaknesses:** Elsevier ownership raises privacy concerns; new Mendeley Reference Manager has mixed reviews

### EndNote

- **Cost:** Paid (institutional license typical)
- **Best for:** Institutions that standardize on it
- **Strengths:** Robust; handles massive libraries (10,000+ refs); excellent CWYW integration
- **Weaknesses:** Expensive; locked to Thomson Reuters ecosystem; less flexible than Zotero

### JabRef

- **Cost:** Free, open-source
- **Best for:** LaTeX/Quarto users who want direct `.bib` editing
- **Strengths:** Native BibTeX management; clean; Java-based; cross-platform
- **Weaknesses:** No browser extension; manual entry more common

---

## 2. Statistical Analysis

### R / RStudio (Posit) ⭐ Recommended default

- **Cost:** Free, open-source
- **Best for:** Reproducible analysis, publication-quality figures (ggplot2)
- **Strengths:** Unlimited flexibility; 18,000+ packages; RMarkdown/Quarto integration; literate programming; free forever
- **Weaknesses:** Learning curve; some clinical teams prefer point-and-click
- **Key packages:** `tidyverse` (data wrangling), `ggplot2` (figures), `survival` (Kaplan-Meier), `lme4` (mixed models), `gtsummary` (publication tables), `broom` (tidy model output)
- **Setup tip:** Install R first, then RStudio/Posit IDE. Use `renv` for project-specific package management.

### Python (Scientific Stack)

- **Cost:** Free, open-source
- **Best for:** Data cleaning, automation, machine learning, large datasets
- **Key libraries:** `pandas` (data frames), `numpy` (numerical), `scipy` (statistics), `statsmodels` (regression), `matplotlib`/`seaborn` (figures), `scikit-learn` (ML)
- **Strengths:** General-purpose; excellent for ETL and pipelines; Jupyter notebooks for exploration
- **Weaknesses:** Statistical packages less mature than R for specialized biostatistics

### jamovi

- **Cost:** Free, open-source
- **Best for:** Users who want SPSS-like interface without the cost
- **Strengths:** GUI-based; built on R; reproducible syntax mode; formatted APA tables out of the box
- **Weaknesses:** Limited to common analyses; less extensible than R

### SPSS

- **Cost:** Paid (expensive without institutional license)
- **Best for:** Clinical teams standardized on it
- **Strengths:** Familiar; point-and-click; comprehensive
- **Weaknesses:** Proprietary format; expensive; not reproducible by default (no code/log unless syntax mode used)

### Stata

- **Cost:** Paid (perpetual license)
- **Best for:** Epidemiology, health economics
- **Strengths:** Excellent survey/complex-sample commands; reproducible `.do` files; strong panel-data tools
- **Weaknesses:** One-license-per-machine; smaller community than R

---

## 3. Writing and Editing

### Quarto + Pandoc ⭐ Our default pipeline

- **Cost:** Free, open-source
- **Best for:** Manuscripts with automated citations, reproducible formatting
- **How it works:** Write `.qmd` → cite with `[@key]` → render to Word/PDF/HTML with CSL style
- **Strengths:** Separates content from formatting; integrates R/Python code; version-controllable; consistent citation style
- **Setup:** `quarto install` + CSL files from <https://github.com/citation-style-language/styles>

### Word / Google Docs

- **Cost:** Word (paid), Google Docs (free)
- **Best for:** Co-authors who can't/won't use Quarto; journal submission formatting
- **Pipeline:** Use Zotero Word plugin for `[@key]` insertion. For Word output from Quarto: `quarto render manuscript.qmd --to docx`
- **Tip:** Use `python-docx` for programmatic Word formatting when generating multiple versions.

### Overleaf (LaTeX)

- **Cost:** Free tier, paid for collaboration
- **Best for:** Math-heavy papers, physics/engineering, IEEE format
- **Strengths:** Beautiful typesetting; real-time collaboration on paid tier
- **Weaknesses:** Learning curve; collaboration limited on free tier

### Grammarly

- **Cost:** Free tier (good), Premium (~$12/mo)
- **Best for:** Grammar, spelling, clarity
- **Use:** Run after Phase 4 (first draft), not during drafting
- **Tip:** Don't blindly accept all suggestions — evaluate each against scientific style (avoid passive voice elimination when passive is appropriate)

### Hemingway App

- **Cost:** Free (web), paid (desktop)
- **Best for:** Identifying overly complex sentences
- **Use:** Run on Discussion and Introduction sections where prose tends to get dense
- **Tip:** Aim for Grade 10–14 readability for biomedical journals (lower is not always better — some complexity is inherent)

### LanguageTool

- **Cost:** Free (open-source), Premium
- **Best for:** Multi-language writing (better Spanish support than Grammarly)
- **Use:** Alternative to Grammarly for Spanish-language manuscripts

---

## 4. Collaboration and Project Management

### Trello / Notion / Obsidian

- **Best for:** Tracking manuscript phases and tasks
- **Use:** Kanban board with columns: Backlog → In Progress → Review → Done
- **Map** to the 8 phases in `resources/project-timeline.md`

### Google Drive / Dropbox

- **Best for:** File sharing, version history
- **Tip:** Use structured folder hierarchy: `01_protocol/`, `02_data/`, `03_analysis/`, `04_drafts/`, `05_submission/`

### GitHub / GitLab

- **Best for:** Version control of Quarto `.qmd` files, analysis code
- **Tip:** Use Git for `.qmd` and `.bib`; store large datasets via Git LFS or externally

---

## 5. Figures and Visualization

### R: ggplot2 ⭐ Recommended

- **Best for:** Publication-quality statistical figures
- **Extensions:** `patchwork` (multi-panel), `ggpubr` (stat comparisons), `ggsurvplot` (Kaplan-Meier)
- **Output:** Vector (PDF/SVG) for journals; 300+ DPI raster (PNG/TIFF) when required

### Python: matplotlib + seaborn

- **Best for:** Users already in Python pipeline
- **Strengths:** Full control; integrates with data pipeline

### BioRender

- **Cost:** Paid (academic discount available)
- **Best for:** Schematic diagrams, pathway figures, graphical abstracts
- **Tip:** Check if your institution has a license

### draw.io / Lucidchart

- **Cost:** Free / freemium
- **Best for:** Flowcharts, CONSORT diagrams, study design schematics

### PRISMA2020 Flow Generator

- **URL:** <https://prisma.shinyapps.io/prisma_2020/>
- **Cost:** Free
- **Best for:** Systematic review flow diagrams (compliant with PRISMA 2020)

---

## 6. Ethics and Compliance Tools

| Tool | Purpose | Cost |
|------|---------|------|
| **iThenticate** | Plagiarism detection (journal standard) | Institutional |
| **Grammarly Plagiarism** | Plagiarism check (individual) | Premium |
| **ClinicalTrials.gov** | Trial preregistration | Free |
| **PROSPERO** | Systematic review preregistration | Free |
| **OSF (Open Science Framework)** | Preregistration, data sharing, project DOI | Free |

---

## Tool Selection Heuristic

```
Need references?         → Zotero (unless institution forces EndNote)
Need statistics?         → R/RStudio (unless team needs SPSS)
Need reproducible doc?   → Quarto + BibTeX
Need quick draft?        → Google Docs + Zotero plugin
Need figures?            → ggplot2 (stats), BioRender (schematics)
Need grammar check?      → Grammarly (English), LanguageTool (Spanish)
Need collaboration?      → Google Docs (simple), GitHub (code), Overleaf (LaTeX)
Need plagiarism check?   → iThenticate (institutional), Grammarly (personal)
```

---

*Version: 1.0.0 — Compiled from Arias-Carrión (2024) recommendations + workflow-specific additions.*
