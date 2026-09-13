# Ethics and Integrity in Scientific Writing

> Resource for `scientific-writing` skill. Consult before finalizing any manuscript involving human subjects, animal data, sensitive populations, or secondary data use.

---

## 1. Foundational Frameworks

These are the internationally recognized frameworks that journals expect you to follow. Cite the applicable one(s) in your Methods section.

| Framework | Scope | When to Cite |
|-----------|-------|--------------|
| **Declaration of Helsinki** (2013 rev.) | Human medical research | Any study involving human participants |
| **ICH-GCP (E6 R2)** | Clinical trials | Drug/device interventional trials |
| **CIOMS International Guidelines** | Epidemiological research | Observational studies, public health |
| **CONSORT / STROBE / PRISMA** | Reporting standards | Study-type specific (see reporting-guidelines.md) |
| **ICMJE Recommendations** (2023 rev.) | Authorship, editing, publishing | All biomedical journals following ICMJE |
| **GDPR (EU 2016/679)** | Data privacy (EU) | Studies with EU participant data |
| **HIPAA** | Data privacy (US) | Studies with US patient data |
| **Ley 19.628** | Data privacy (Chile) | Studies with Chilean patient data |
| **ARRIVE 2.0** | Animal research | Any study involving live animals |

---

## 2. Authorship and Contribution

### ICMJE Four Criteria (all must be met)

1. **Substantial contributions** to conception or design, or to data acquisition, analysis, or interpretation
2. **Drafting or critically revising** the manuscript for important intellectual content
3. **Final approval** of the version to be published
4. **Accountability** for all aspects of the work

**If any criterion is missing → contributor, not author.** Use CRediT taxonomy for non-author contributions.

### Common Authorship Violations

- ❌ **Gift authorship** — adding someone who didn't contribute meaningfully
- ❌ **Ghost authorship** — omitting someone who wrote substantial portions (common with medical writers)
- ❌ **Coercion authorship** — supervisor demands authorship without meeting criteria
- ❌ **Salami slicing** — splitting one study into multiple papers to inflate publication count
- ❌ **Duplicate publication** — publishing the same data in two journals

### CRediT Taxonomy Roles

Use these for contribution statements: Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Resources, Data curation, Writing – original draft, Writing – review & editing, Visualization, Supervision, Project administration, Funding acquisition.

---

## 3. Human Subjects

### Ethics Committee Approval

- Name the approving committee explicitly (e.g., "Comité de Ética Científico de la FALP")
- Include approval number/date if available
- If multiple sites: list each committee and approval separately
- If waived: state the waiver rationale and which committee granted it

### Informed Consent

- Describe the consent process (written, verbal, electronic)
- State if consent was waived and the justification (e.g., retrospective chart review)
- For minors or incapacitated populations: describe guardian consent + assent where applicable
- Specify language and reading level of consent forms

### Privacy and Data Protection

- Describe de-identification steps (anonymized, pseudonymized, or coded)
- State data storage location and access controls
- For EU data: mention GDPR compliance and lawful basis
- For Chilean data under Ley 19.628: mention compliance
- State whether data will be shared, and under what terms (controlled access, repository, etc.)

### Vulnerable Populations

Extra protections required for:
- Pregnant women, fetuses, neonates
- Prisoners or detainees
- Cognitively impaired individuals
- Children and adolescents
- Economically or educationally disadvantaged persons
- Elderly with cognitive decline

---

## 4. Animal Research (ARRIVE 2.0)

### Essential Elements

- **Species and strain**: scientific justification for choice
- **Sample size**: power calculation, not arbitrary
- **Randomization**: how animals were assigned to groups
- **Blinding**: investigator blinding during outcome assessment
- **Welfare standards**: housing, enrichment, husbandry conditions
- **Humane endpoints**: pre-defined criteria for euthanasia or intervention
- **IACUC/ethics approval**: committee name and approval number

---

## 5. Conflicts of Interest and Funding

### Conflict of Interest (COI)

Disclose ALL financial and non-financial relationships:
- **Financial**: employment, consultancies, stock ownership, patents, speaker fees, research grants
- **Non-financial**: personal relationships, academic competitions, intellectual passion

**Rule:** When in doubt, disclose. "None declared" is acceptable only after genuine review.

### Funding

- Name the funding source and grant number
- State the sponsor's role: did they design, conduct, analyze, or write? Or were they uninvolved?
- If unfunded: state "No external funding received"

---

## 6. Data Integrity

### Honest Reporting

- Report ALL pre-specified outcomes, not just favorable ones
- Report protocol deviations and how they were handled
- Report missing data and the method for handling it (complete case, multiple imputation, etc.)
- Report negative results — publication bias is an ethical problem
- Do not selectively cite literature that supports your findings

### Image and Figure Manipulation

- No splicing, cloning, or selective enhancement of images
- Western blots/gels: show full uncropped images in supplementary
- Microscopy: state acquisition parameters and any post-processing
- AI-generated images: check journal policy (ICMJE 2023: AI cannot be an author; AI use for writing assistance must be disclosed)

### Reproducibility

- Share analysis code when possible (GitHub, Zenodo)
- Deposit datasets in repositories (figshare, Dryad, institutional)
- Preregister trials (ClinicalTrials.gov, ISRCTN)
- Preregister systematic reviews (PROSPERO)

---

## 7. Plagiarism and Self-Plagiarism

### Plagiarism Types

| Type | Description | Example |
|------|-------------|---------|
| **Verbatim** | Copying text without quotes | Copying a paragraph from a paper without citation |
| **Mosaic** | Mixing copied phrases with own words | Patchwriting from multiple sources |
| **Ideas** | Using someone's concept without credit | Presenting another's hypothesis as your own |
| **Self-plagiarism** | Reusing your own published text without citation | Copying methods section from your prior paper |

### Acceptable Self-Reuse

- Methods sections: can reuse your own published methods with citation ("as described in [N]")
- Reference lists: not copyrightable
- Short phrases of standard terminology: acceptable

### Detection Tools

- **iThenticate** / **Turnitin** — journal-standard, institutional access
- **Grammarly Plagiarism** — accessible for individuals
- Self-check: search suspicious phrases in quotes via Google Scholar

---

## 8. AI and Language Models

### ICMJE Position (2023+)

- AI tools (ChatGPT, Claude, etc.) **cannot be authors**
- AI use for writing assistance **must be disclosed** in Methods or Acknowledgments
- Authors remain **fully responsible** for AI-assisted content accuracy
- AI should not be used to generate fake data, citations, or images presented as real

### Recommended Disclosure Language

> "During the preparation of this work, the author(s) used [Tool Name] to [specific use: edit grammar, translate, format references]. After using this tool, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication."

---

## 9. Ethics Checklist (Pre-Submission)

- [ ] Ethics committee named with approval number
- [ ] Consent process described (or waiver justified)
- [ ] Privacy/de-identification steps stated
- [ ] Vulnerable population protections (if applicable)
- [ ] Animal welfare compliance stated (if applicable)
- [ ] All conflicts of interest disclosed
- [ ] Funding source and sponsor role stated
- [ ] All authors meet ICMJE 4 criteria
- [ ] CRediT contribution statement included
- [ ] No plagiarism or self-plagiarism (ran detection tool)
- [ ] No salami slicing or duplicate publication
- [ ] Data sharing statement included
- [ ] Preregistration number cited (if applicable)
- [ ] AI tool use disclosed (if applicable)

---

*Sources: ICMJE Recommendations (2023), Declaration of Helsinki (2013), ARRIVE 2.0, CRediT taxonomy, CONSORT 2010.*
*Version: 1.0.0 — Expanded from Arias-Carrión (2024) integration + ICMJE 2023 updates.*
