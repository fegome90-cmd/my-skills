# Professional Report Formatting

> Adapted from K-Dense scientific-writing (MIT License)

# Professional Report Formatting for Scientific Documents


---

## When to Use Professional Report Formatting

### Use This Style For:

- **Research reports** - Internal and external research summaries
- **Technical reports** - Detailed technical documentation and analyses
- **White papers** - Position papers and thought leadership documents
- **Grant reports** - Progress reports and final grant reports
- **Policy briefs** - Research-informed policy recommendations
- **Industry reports** - Technical reports for industry audiences
- **Internal research summaries** - Team and stakeholder communications
- **Feasibility studies** - Technical and research feasibility assessments
- **Project documentation** - Research project deliverables

### Do NOT Use This Style For:

- **Journal manuscripts** → Follow journal author guidelines
- **Conference papers** → Follow conference submission guidelines
- **Academic theses/dissertations** → Use institutional templates
- **Peer-reviewed submissions** → Follow journal author guidelines

**Key Distinction**: Professional report formatting prioritizes visual appeal and readability for general audiences, while journal manuscripts must follow strict publisher requirements.

---

## Overview of Professional Report Styling


| Feature | Description |
|---------|-------------|
| Typography | Helvetica font family for modern, professional appearance |
| Color Scheme | Coordinated blues, greens, oranges, and purples |
| Box Environments | Colored boxes for organizing content types |
| Tables | Professional styling with alternating rows |
| Figures | Consistent caption formatting |
| Headers/Footers | Professional page headers and footers |
| Scientific Commands | Shortcuts for p-values, effect sizes, statistics |

### Basic Document Setup


---

## Box Environments for Content Organization

### Purpose and Usage

Colored boxes help readers quickly identify different types of content. Use them strategically to highlight important information.

### Available Box Environments

| Environment | Color | Purpose |
|-------------|-------|---------|
| `keyfindings` | Blue | Major findings, discoveries, key takeaways |
| `methodology` | Green | Methods, procedures, study design |
| `resultsbox` | Blue-green | Statistical results, data highlights |
| `recommendations` | Purple | Recommendations, action items, implications |
| `limitations` | Orange | Limitations, cautions, caveats |
| `criticalnotice` | Red | Critical warnings, safety notices |
| `definition` | Gray | Definitions, notes, supplementary info |
| `executivesummary` | Blue (shadow) | Executive summaries |
| `hypothesis` | Light blue | Research hypotheses |

### Key Findings Box

Use for major findings and important discoveries:


**Best Practices:**
- Use sparingly (1-3 per chapter maximum)
- Reserve for genuinely important findings
- Include specific numbers and statistics
- Write concisely

### Methodology Box

Use for highlighting methods and procedures:


**Best Practices:**
- Summarize key methodological features
- Use at the start of methods sections
- Include sample size and design type
- Keep technical but accessible

### Results Box

Use for highlighting specific statistical results:


**Best Practices:**
- Report complete statistical information
- Use scientific notation commands
- Include effect sizes alongside p-values
- One box per major analysis

### Recommendations Box

Use for recommendations and implications:


**Best Practices:**
- Make recommendations specific and actionable
- Prioritize with clear labels
- Link to supporting evidence
- Include implementation guidance

### Limitations Box

Use for limitations, caveats, and cautions:


**Best Practices:**
- Be honest and thorough
- Explain implications of each limitation
- Suggest how future research could address limitations
- Don't over-qualify findings

### Critical Notice Box

Use for critical warnings or safety information:


**Best Practices:**
- Reserve for genuinely critical information
- Be clear and direct
- Include specific actions to take
- Provide contact information if relevant

### Definition Box

Use for definitions and explanatory notes:


**Best Practices:**
- Define technical terms at first use
- Keep definitions concise
- Include practical interpretation guidance
- Use for audience-appropriate terms

---

## Professional Table Formatting

### Design Principles

1. **Clean appearance**: Use `booktabs` rules (`\toprule`, `\midrule`, `\bottomrule`)
2. **Alternating rows**: Apply `\rowcolor{tablealt}` to every other row
3. **Clear headers**: Bold headers for column identification
4. **Appropriate precision**: Report statistics to appropriate decimal places
5. **Complete information**: Include sample sizes, units, and notes

### Standard Data Table


### Results Table with Significance Indicators


### Comparison Table with Quality Ratings


---

## Figure and Caption Styling

### Caption Formatting

The style package automatically formats captions with:
- Blue, bold figure labels
- Gray descriptive text
- Centered alignment with margins

### Standard Figure


### Figure with Source Attribution


### Figure with Explanatory Note


---

## Color Palette and Visual Hierarchy

### Color Usage Guidelines

| Color | Use For | Avoid Using For |
|-------|---------|-----------------|
| Primary Blue | Headers, important findings | Warnings, cautions |
| Science Green | Methods, positive results | Negative findings |
| Orange | Cautions, limitations | Positive findings |
| Red | Critical warnings | Routine content |
| Purple | Recommendations | Findings, methods |
| Gray | Definitions, notes | Key findings |

### Visual Hierarchy

1. **Executive summary boxes** (shadow effect) - Most prominent
2. **Colored content boxes** - High prominence for key content
3. **Tables with color** - Medium prominence for data
4. **Body text** - Standard prominence
5. **Definition boxes** - Lower prominence for supplementary info

### Accessibility Considerations

- Color palette is designed to be distinguishable for common color vision deficiencies
- All boxes have both color AND structural indicators (borders, backgrounds)
- Text maintains sufficient contrast ratios
- Don't rely solely on color to convey meaning

---

## Typography Guidelines

### Font Specifications

| Element | Font | Size | Color |
|---------|------|------|-------|
| Body text | Helvetica | 11pt | Dark gray (#424242) |
| Chapter titles | Helvetica Bold | Huge | Primary blue (#003366) |
| Section headings | Helvetica Bold | Large | Primary blue (#003366) |
| Subsections | Helvetica Bold | large | Secondary blue (#4A90E2) |
| Subsubsections | Helvetica Bold | normalsize | Dark gray (#424242) |

### Spacing

- Line spacing: 1.15 (for readability)
- Paragraph spacing: 0.5em between paragraphs
- Page margins: 1 inch on all sides

### Best Typography Practices

1. **Consistency**: Use the same formatting for similar elements
2. **Hierarchy**: Use visual weight to indicate importance
3. **Readability**: Adequate spacing and contrast
4. **Professionalism**: Avoid mixing fonts or excessive formatting

---

## Scientific Notation Commands Reference

### Statistical Reporting

| Command | Output | When to Use |
|---------|--------|-------------|
| `\pvalue{0.023}` | *p* = 0.023 | Report p-values |
| `\psig{< 0.001}` | ***p*** = < 0.001 | Significant p-values (bold) |
| `\CI{0.45}{0.72}` | 95% CI [0.45, 0.72] | Confidence intervals |
| `\effectsize{d}{0.75}` | d = 0.75 | Effect sizes |
| `\samplesize{250}` | *n* = 250 | Sample sizes |
| `\meansd{42.5}{8.3}` | 42.5 ± 8.3 | Mean with SD |

### Significance Indicators

| Command | Output | Meaning |
|---------|--------|---------|
| `\sigone` | * | p < 0.05 |
| `\sigtwo` | ** | p < 0.01 |
| `\sigthree` | *** | p < 0.001 |
| `\signs` | ns | not significant |
| `\siglegend` | Full legend | For table footnotes |

### Quality and Evidence Ratings

| Command | Output | Meaning |
|---------|--------|---------|
| `\qualityhigh` | **HIGH** (green) | High quality |
| `\qualitymedium` | **MEDIUM** (orange) | Moderate quality |
| `\qualitylow` | **LOW** (red) | Low quality |
| `\evidencestrong` | **Strong** (green) | Strong evidence |
| `\evidencemoderate` | **Moderate** (orange) | Moderate evidence |
| `\evidenceweak` | **Weak** (red) | Weak evidence |

### Trend Indicators

| Command | Symbol | Meaning |
|---------|--------|---------|
| `\trendup` | ▲ (green) | Increasing trend |
| `\trenddown` | ▼ (red) | Decreasing trend |
| `\trendflat` | → (gray) | Stable/no change |

---

## Complete LaTeX Examples

### Executive Summary Example


### Methods Section Example


### Results Section Example


### Discussion Section Example


---

## Checklist: Professional Report Quality

Before finalizing your report, verify:

### Formatting
- [ ] Helvetica font rendering correctly
- [ ] Colors displaying properly

### Content Organization
- [ ] Executive summary present and complete
- [ ] Key findings highlighted in boxes
- [ ] Methods clearly described
- [ ] Results properly formatted with statistics
- [ ] Limitations acknowledged
- [ ] Recommendations are specific and actionable

### Tables
- [ ] All tables have captions and labels
- [ ] Alternating row colors applied
- [ ] Significance indicators explained
- [ ] Numbers formatted consistently

### Figures
- [ ] All figures have captions and labels
- [ ] Sources attributed where appropriate
- [ ] Resolution sufficient for printing (300 DPI)
- [ ] Referenced in text

### Statistical Reporting
- [ ] P-values reported appropriately
- [ ] Effect sizes included
- [ ] Confidence intervals where relevant
- [ ] Sample sizes stated

### Professional Appearance
- [ ] Consistent formatting throughout
- [ ] No orphaned headers or widows
- [ ] Page breaks at appropriate locations
- [ ] References complete and formatted

---

## Resources

### Files in This Skill

- `assets/scientific_report_template.tex` - Complete report template
- `assets/REPORT_FORMATTING_GUIDE.md` - Quick reference guide

### Related Skills

- Journal-specific templates - Follow target journal author guidelines
- `scientific-schematics` - For generating diagrams and figures
- `generate-image` - For creating illustrations and graphics

### External Resources

- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX) - General LaTeX reference
- [Booktabs Package Documentation](https://ctan.org/pkg/booktabs) - Professional table styling
- [tcolorbox Package Documentation](https://ctan.org/pkg/tcolorbox) - Colored box environments


---

## Note on Formatting Tools

This resource provides conceptual guidance for structuring professional reports. For actual formatting:

- **Journal manuscripts**: Follow journal author guidelines directly
- **Professional reports**: Use Quarto with appropriate templates, or Markdown/PDF export
- **Tables and figures**: Use Quarto/Pandoc table syntax or create with data visualization tools

Professional reports benefit from visual hierarchy: colored boxes for key findings, structured methodology sections, and formatted tables. These concepts apply regardless of the rendering tool used (Word, Google Docs, Quarto/Pandoc).
