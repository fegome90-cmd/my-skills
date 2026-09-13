---
name: scientific-writing
description: "Use when writing, drafting, revising, or structuring scientific manuscripts, research papers, literature reviews, clinical reports, abstracts, marco teórico, reseña bibliográfica, or tesis sections. Also use for citation formatting (APA/AMA/Vancouver/Chicago/IEEE), reporting guidelines (CONSORT/STROBE/PRISMA), figure/table design, manuscript ethics, or addressing reviewer comments. Not for emails (→email-drafter) or literature search (→literature-search)."
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "2.0.0"
  openclaw:
    requires:
      bins: []
    emoji: "📝"
---

# Scientific Writing

## Overview

Write scientific manuscripts using IMRAD structure, citations, figures/tables, and reporting guidelines. **Always write in full paragraphs with flowing prose — never submit bullet points.** Use the two-stage process: outline first, then convert to prose.

## When to Use

**Activate when:**
- Writing or revising any manuscript section (abstract, introduction, methods, results, discussion)
- Structuring a research paper, review, case report, or clinical study
- Formatting citations (APA, AMA, Vancouver, Chicago, IEEE)
- Applying reporting guidelines (CONSORT, STROBE, PRISMA, STARD, TRIPOD, ARRIVE, CARE, SQUIRE, SPIRIT, CHEERS)
- Designing figures, tables, or data visualizations for a manuscript
- Drafting abstracts (structured or unstructured)
- Addressing reviewer comments or revising after rejection
- Planning a manuscript project timeline
- Writing marco teórico, reseña bibliográfica, or tesis sections

**Do NOT activate for (use other skills instead):**
- Systematic literature search → use `literature-search`
- Email drafting → use `email-drafter` or `agentmail`
- Presentation slides → use `presentation-builder`
- General diagrams → use `diagram-maker-plus`

## Resource Routing

| If you need to... | Read this resource |
|---|---|
| Structure a section (IMRAD detail) | `resources/imrad-structure.md` |
| Format citations or build a bibliography | `resources/citation-styles.md` |
| Design figures, tables, or visualizations | `resources/figures-tables.md` |
| Check reporting completeness (CONSORT, STROBE...) | `resources/reporting-guidelines.md` |
| Improve writing style or avoid AI-sounding prose | `resources/writing-principles.md` + `resources/ai-human-writing-guide.md` |
| Verify ethics, authorship, or COI | `resources/ethics-and-integrity.md` |
| Plan a manuscript from idea to submission | `resources/project-timeline.md` |
| Choose reference managers, statistics, or writing tools | `resources/tools.md` |
| Run the pre-delivery quality audit (33 items) | `resources/pre-delivery-audit.md` |
| Write a non-journal report (white paper, technical report) | `resources/professional-report-formatting.md` |

---

## Core Capabilities

### 1. Two-Stage Writing Process

**Stage 1 — Outline:** Use `literature-search` to gather evidence, then create a structured outline with key points, citations, and data marked per section. Bullet points are scaffolding, NOT the final manuscript.

**Stage 2 — Prose:** Transform outline into complete sentences with transitions, natural citation integration, and varied sentence structure. Every section must flow as connected prose.

### 2. Manuscript Structure (IMRAD)

Standard structure: Introduction → Methods → Results → Discussion. For section-by-section guidance, CARS model (territory → niche → occupy), and alternative structures (reviews, case reports, meta-analyses), refer to `resources/imrad-structure.md`.

For project planning, timeline, and phase breakdown, refer to `resources/project-timeline.md`.

### 3. Citations

Supported styles: AMA, Vancouver, APA, Chicago, IEEE. For comprehensive guides, refer to `resources/citation-styles.md`.

**Pipeline:** When using Quarto, cite with `[@key]` in `.qmd` files. Bibliography renders from `references.bib` via CSL. The agent never hand-writes the references section.

**Best practices:** Cite primary sources. Include recent literature (5-10 years). Verify all citations against original papers. Use reference management software (see `resources/tools.md`).

### 4. Figures and Tables

For design principles, when to use tables vs figures, and figure type guidance, refer to `resources/figures-tables.md`. Use `image_generate` for visual content when needed — but verify journal AI image policy first (see Ethics below).

### 5. Reporting Guidelines

Match guideline to study type. For checklists and details, refer to `resources/reporting-guidelines.md`.

| Guideline | Study Type |
|-----------|-----------|
| CONSORT | Randomized controlled trials |
| STROBE | Observational studies |
| PRISMA | Systematic reviews / meta-analyses |
| STARD | Diagnostic accuracy |
| TRIPOD | Prediction models |
| ARRIVE | Animal research |
| CARE | Case reports |
| SQUIRE | Quality improvement |
| SPIRIT | Trial protocols |
| CHEERS | Economic evaluations |

### 6. Writing Principles and Style

Core principles: **clarity** (precise language, defined terms), **conciseness** (eliminate redundancy, 15-20 word average), **accuracy** (exact values, consistent terminology), **objectivity** (no overstating, acknowledge conflicts).

For detailed guidance including hedging, anthropomorphism, abbreviation use, and paragraph coherence, refer to `resources/writing-principles.md`.

**Human voice:** Scientific writing must read like a human wrote it. AI prose has recognizable markers — filler phrases, uniform structure, lexical tells. See `resources/writing-principles.md` Section 3 (de-AI checklist) and `resources/ai-human-writing-guide.md` (evidence-based research, strategies, field-specific guidance). Run the de-AI pass before delivery.

### 7. Paragraph-First Rule

- ❌ **Never** leave bullet points in the final manuscript (Abstract, Introduction, Results, Discussion, Conclusions)
- ✅ **Acceptable** only in Methods: inclusion/exclusion criteria, materials lists
- ✅ **Acceptable** in Supplementary Materials: extended protocols, equipment lists

### 8. Ethics and Integrity

Ethics is not an afterthought — verify early and verify again before delivery. Refer to `resources/ethics-and-integrity.md` for the full framework (Helsinki, ICMJE, ARRIVE, GDPR, Ley 19.628).

**Minimum checklist:**
- Ethics committee approval stated (name + number)
- Informed consent described or waiver justified
- Privacy/de-identification steps stated
- All authors meet ICMJE 4 criteria; CRediT included
- COI and funding disclosed
- AI tool use disclosed per ICMJE 2023
- Plagiarism check run before submission

**AI image policy:** Verify journal policy before using `image_generate`. Many journals prohibit AI-generated figures or require disclosure.

---

## Field-Specific Terminology

**Biomedical:** Precise clinical terminology (ICD, DSM, SNOMED-CT). Generic drug names first. "Patients" for clinical, "participants" for community studies. SI units.

**Genetics:** Italics for genes (*TP53*), regular for proteins (p53). Uppercase human (*BRCA1*), sentence case mouse (*Brca1*).

**Chemistry:** IUPAC nomenclature. Standard units (mM, μM, nM).

**Nursing:** NIC/NOC/NANDA taxonomies. Gordon's functional patterns. Orem's self-care theory.

**Ecology:** Binomial nomenclature (*Homo sapiens*). Consistent ecological metrics.

## Instrument Referencing Rule

Every measurement instrument needs:
1. Original version citation (author, year, journal)
2. Validated Spanish version citation (if applicable)
3. Psychometric properties (α de Cronbach, test-retest)
4. Explicit language version stated

**Common gaps:** Citing only English original when using Spanish adaptation; missing psychometric properties; not stating which version was administered.

---

## Common Pitfalls

**Top rejection reasons:** Insufficient statistics, over-interpreted results, poor reproducibility, biased samples, weak literature review, unclear figures, ignoring reporting guidelines.

**Writing quality issues:** Mixed tenses, excessive jargon, poor transitions, inconsistent terminology.

---

## Writing Process

1. **Plan** — Define question, target journal, citation style
2. **Search** — Use `literature-search` for evidence base
3. **Outline** — Section outlines with key points (Stage 1)
4. **Write** — Convert to full paragraphs (Stage 2)
5. **Apply guideline** — Check against reporting standard
6. **Format citations** — Quarto/CSL pipeline
7. **Review** — Clarity, conciseness, accuracy, objectivity
8. **Audit** — Run `resources/pre-delivery-audit.md` (33 items) + `resources/ethics-and-integrity.md` checklist
9. **De-AI pass** — Run checklist from `resources/writing-principles.md` Section 3f
10. **Finalize** — Pre-submission checklist below

### Pre-Submission Checklist

- [ ] All sections as flowing prose (no bullet points)
- [ ] Reporting guideline checklist completed
- [ ] All citations verified against original sources
- [ ] Citation style matches journal requirements
- [ ] Figures and tables self-explanatory
- [ ] Word counts within limits
- [ ] Abbreviations defined at first use
- [ ] Consistent terminology throughout
- [ ] No uncited references or missing citations
- [ ] Abstract standalone and accurate
- [ ] Methods sufficient for replication
- [ ] Limitations acknowledged
- [ ] Ethics, COI, funding statements included
- [ ] De-AI checklist run (no filler phrases, varied structure, no lexical tells)
- [ ] AI tool use disclosed (if applicable)

---

## Fork: Non-Journal Documents

For research reports, white papers, technical reports, or grant reports that are NOT journal manuscripts, use `resources/professional-report-formatting.md` instead of the IMRAD structure above.

| Document Type | Approach |
|---|---|
| Journal manuscript | Journal guidelines + this skill |
| Research/white/technical report | `resources/professional-report-formatting.md` |
| Grant report | `resources/professional-report-formatting.md` |

---

## Resources

**Process:**
- `resources/project-timeline.md` — 8-phase manuscript timeline, time estimates, stalled-project diagnosis
- `resources/pre-delivery-audit.md` — 33-item zero-tolerance audit (data, citations, style, language, completeness, institutional, delivery)

**Style:**
- `resources/writing-principles.md` — Clarity, conciseness, hedging, de-AI checklist (Section 3)
- `resources/ai-human-writing-guide.md` — Evidence-based guide: AI fingerprints, voice preservation, practical strategies, field-specific advice, anti-patterns

**Compliance:**
- `resources/reporting-guidelines.md` — CONSORT, STROBE, PRISMA, STARD, TRIPOD, ARRIVE, CARE, SQUIRE, SPIRIT, CHEERS
- `resources/ethics-and-integrity.md` — Helsinki, ICMJE authorship, ARRIVE, COI, AI disclosure, plagiarism, GDPR/Ley 19.628

**Reference:**
- `resources/imrad-structure.md` — IMRAD format, CARS model, section-by-section content guide
- `resources/citation-styles.md` — APA, AMA, Vancouver, Chicago, IEEE complete guides
- `resources/figures-tables.md` — Visualization best practices, figure types, design principles
- `resources/tools.md` — Reference managers, statistics software, writing aids, decision matrix

**Fork:**
- `resources/professional-report-formatting.md` — Structure for non-journal professional documents

---

## Integration with Other Skills

- **`literature-search`** — Evidence gathering, systematic search, PDF download
- **Quarto + Pandoc + CSL + BibTeX** — Citation rendering pipeline
- **`paper-writer` CLI** — Full pipeline orchestration (if available)
- **`diagram-auditor`** — Run on clinical/technical diagrams before inclusion

---

*Version: 2.0.0 — Major reorganization. Triggers rewritten (Use-when format, Spanish keywords, negative triggers, disambiguation). Resource routing table added. Resources categorized (Process/Style/Compliance/Reference/Fork). Token efficiency applied. Anti-AI coverage consolidated across writing-principles + ai-human-writing-guide. Ethics as cross-cutting concern. Professional reports as fork.*
