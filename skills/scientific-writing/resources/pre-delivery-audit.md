# Pre-Delivery Audit — Scientific Documents

> Resource for `scientific-writing` skill. Run BEFORE sending any scientific document to stakeholders, email, or submission.

## Overview

This is a systematic, reproducible audit protocol. Every item must pass before delivery. No partial deliveries with "TODO" items.

**Principle:** Zero technical debt. If it's not verified, it doesn't ship.

---

## 1. Data Audit

Every statistic must trace to a source.

| # | Check | How to Verify |
|---|-------|---------------|
| 1.1 | Every % has a source ref | `grep -oE '[0-9]+[,\.][0-9]+%|[0-9]+%' FILE` → each hit must have [N] nearby |
| 1.2 | Every sample size (n=/N=) has source | `grep -oE 'n=[0-9]+\|N=[0-9]+' FILE` → each must have [N] or be own methodology |
| 1.3 | Every OR, RR, HR has IC95% | `grep -iE 'OR [0-9]\|RR [0-9]\|HR [0-9]' FILE` → must include confidence interval |
| 1.4 | Every p-value has context | `grep -oE 'p[<>][0-9,.]+' FILE` → must state what comparison |
| 1.5 | No fabricated numbers | Cross-check every number against source PDF/abstract |
| 1.6 | Percentages add up | Sum categorical percentages → must be ~100% (or explain missing) |

### Verification Commands

```bash
# Extract all statistics
grep -oE '[0-9]+[,\.][0-9]+%|[0-9]+%|n=[0-9]+|N=[0-9]+|OR [0-9,.]+|IC95%|p[<>][0-9,.]+' FILE

# Check each stat has a nearby citation
grep -B2 -A2 '[0-9]\+%' FILE | grep -c '\[[0-9]\+\]'
```

---

## 2. Citation Audit

Every [N] must be traceable and every ref must be cited.

| # | Check | How to Verify |
|---|-------|---------------|
| 2.1 | Every [N] in text has matching Reference entry | Count unique [N] in text → must match refs list |
| 2.2 | Every Reference entry is cited at least once | For each ref N: `grep -c "\[N\]" FILE` must be >0 |
| 2.3 | Citation numbers are sequential | No gaps: [1][2][3], not [1][3][5] |
| 2.4 | Author names verified against PubMed | For each ref: lookup PMID → compare authors, title, journal |
| 2.5 | Journal name, volume, pages verified | Compare against PubMed/esummary output |
| 2.6 | DOI included where available | `grep "^[0-9]*\." FILE \| grep -c "doi:"` → maximize coverage |
| 2.7 | PMID included where available | Same as above for PMID |
| 2.8 | No "et al." when authors are verifiable | For refs with ≤6 authors: list all. >6: first 3 + et al. is OK |
| 2.9 | **Bibliografía inmutable en merge multi-documento** | Si se fusionan múltiples archivos (ej. marco teórico + metodología), la bibliografía del archivo verificado debe pasarse como **bloque inmutable** al subagent/merger. Verificar post-merge: comparar refs 1–N contra original → deben ser idénticas salvo refs nuevas añadidas al final. |
| 2.10 | **Subagent no modificó refs existentes** | `grep -oE '\[[0-9]+\]' MERGED | sort -n | uniq` → cada [N] del original debe apuntar al mismo autor/título. Si [10] era Villanueva en el original, sigue siendo Villanueva en el merge. |

### Verification Commands

```bash
# Check all 19 refs cited (adjust range)
for i in $(seq 1 19); do
  if grep -qE "\[$i\]|\[1-$i\]|\[$i-[0-9]+\]" FILE 2>/dev/null; then
    echo "[$i] ✅"
  else
    echo "[$i] ❌ NOT CITED"
  fi
done

# Find refs with "et al." that could be completed
grep "^[0-9]*\." FILE | grep "et al\."

# Count DOI/PMID coverage
grep "^[0-9]*\." FILE | grep -c "doi:\|PMID:"
```

### PubMed Verification Script

```bash
# For each ref with PMID, verify title/authors
PMID=XXXXXXX
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=${PMID}&retmode=json" | \
  python3 -c "
import sys,json
d=json.load(sys.stdin)
r=d['result']['${PMID}']
authors=', '.join([a['name'] for a in r['authors']])
print(f'Title: {r[\"title\"]}')
print(f'Authors: {authors}')
print(f'Journal: {r[\"source\"]} {r.get(\"volume\",\"?\")}({r.get(\"issue\",\"?\")}):{r.get(\"pages\",\"?\")}')
"
```

### Common Ref Errors to Flag

- ❌ Wrong journal (e.g., "JAMA Otolaryngol" when it's actually "Laryngoscope")
- ❌ Wrong volume/pages
- ❌ Wrong year
- ❌ Author name misspelled or fabricated
- ❌ Title simplified/paraphrased (must be exact or clearly translated with brackets)
- ❌ Conference paper cited as journal article
- ❌ DOI that doesn't resolve to the correct paper

---

## 3. Style Audit (Paragraph-First Rule)

| # | Check | How to Verify |
|---|-------|---------------|
| 3.1 | No bullet points in Abstract | `grep -n "^- " FILE` in abstract section |
| 3.2 | No bullet points in Introduction | Same |
| 3.3 | No bullet points in Results/Discussion | Same |
| 3.4 | Lists only in Methods | Inclusion/exclusion criteria, materials = OK |
| 3.5 | Flowing prose with transitions | Read each paragraph — must have connective tissue |

---

## 4. Language Audit (Spanish Académico)

| # | Check | How to Verify |
|---|-------|---------------|
| 4.1 | No anglicisms | "baseline" → línea base, "outcome" → resultado/desenlace, "survivor" → sobreviviente |
| 4.2 | No calques | "evidenciando" used correctly, not as direct translation of "evidencing" |
| 4.3 | Consistent terminology | Same term throughout (not "habla"/"voz"/"comunicación" interchangeably) |
| 4.4 | Correct tildes/orthography | `grep -i "inglés\|difícil\|también\|más\|aún\|aqui" FILE` |
| 4.5 | Vancouver [N] with brackets | No superscripts, no (Author, Year) unless explicitly requested |

---

## 5. Completeness Audit

| # | Check | How to Verify |
|---|-------|---------------|
| 5.1 | Every section has content | No empty sections or "[TBD]" placeholders |
| 5.2 | Tables/figures referenced in text | Each table must be mentioned before it appears |
| 5.3 | Abbreviations defined at first use | First occurrence: "Hospital Anxiety and Depression Scale (HADS)" |
| 5.4 | STROBE/GRAMMS/COREQ mentioned (if applicable) | `grep -c "STROBE\|GRAMMS\|COREQ" FILE` must be >0. Verify context: must appear in Methods/design section, not just checklist. |
| 5.5 | **No terminología mixta post-subagent** | Ej: si se decidió usar "CCC" en vez de "HNC", verificar: `grep -c "HNC" FILE` → debe ser 0. **Documentar glosario de términos aprobados ANTES de generar contenido.** |
| 5.6 | Ethical approval statement included | IRB/committee name + approval status |
| 5.7 | Funding/conflicts declared | Even if "none declared" |
| 5.8 | No "[mes/año]" placeholders | All dates filled or clearly marked as "por confirmar" |

---

## 6. Institutional Context Audit (FALP-specific)

| # | Check | How to Verify |
|---|-------|---------------|
| 6.1 | FALP mentioned in population | "atendidos en la Fundación Arturo López Pérez" |
| 6.2 | Chilean context present | At least one Chilean data point or justification |
| 6.3 | Instruments validated in Spanish | SECEL español, HADS español |
| 6.4 | AJCC 8th edition TNM specified | Not generic "TNM" |
| 6.5 | REDCap or data platform mentioned | How data will be collected |

---

## 7. Delivery Audit

| # | Check | How to Verify |
|---|-------|---------------|
| 7.1 | Saved to correct output path | `apps/pae-wizard/outputs/` |
| 7.2 | Sent via AgentMail with descriptive subject | Subject includes document type + version |
| 7.3 | Confirmation sent to Felipe | Explicit "Enviado 📧" in chat |
| 7.4 | Wiki updated if applicable | New refs saved to wiki if significant |
| 7.5 | **Post-subagent audit obligatorio** | Si se usó subagent para generar/mergear: (a) verificar refs con checks 2.1–2.10, (b) verificar terminología con check 5.5, (c) ejecutar diff de bibliografía contra original verificado. **NO editar el documento post-subagent antes de este audit.** |

---

## Audit Report Template

After completing the audit, append to the document:

```markdown
### Audit Report — [DATE]

| Dimension | Score | Issues Found | Issues Resolved |
|-----------|-------|-------------|-----------------|
| Data      | X/Y   | N issues    | N resolved      |
| Citations | X/Y   | N issues    | N resolved      |
| Style     | X/Y   | N issues    | N resolved      |
| Language  | X/Y   | N issues    | N resolved      |
| Completeness | X/Y | N issues  | N resolved      |
| Institutional | X/Y | N issues | N resolved      |
| Delivery  | X/Y   | N issues    | N resolved      |

**Remaining debt:** [0 or list items with justification]
```

---

## Quick Run Command

```bash
# Full audit in one pass
echo "=== DATA ===" && grep -oE '[0-9]+[,\.][0-9]+%|[0-9]+%|n=[0-9]+|N=[0-9]+|OR [0-9,.]+|IC95%|p[<>][0-9,.]+' FILE && \
echo "=== REFS CITED ===" && for i in $(seq 1 19); do grep -qE "\[$i\]|\[1-$i\]|\[$i-[0-9]+\]" FILE 2>/dev/null && echo "[$i] ✅" || echo "[$i] ❌"; done && \
echo "=== ET AL ===" && grep "^[0-9]*\." FILE | grep "et al\." && \
echo "=== DOI/PMID ===" && grep "^[0-9]*\." FILE | tail -19 | grep -c "doi:\|PMID:" && \
echo "=== PLACEHOLDERS ===" && grep -in "\[TBD\]\|\[mes/año\]\|\[por confirmar\]" FILE
```

---

*Version: 1.1.0 — Updated with merge subagent learnings (2026-05-24)*
*33 items across 7 dimensions. Zero-tolerance for delivery with open items.*
