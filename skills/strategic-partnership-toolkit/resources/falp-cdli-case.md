---
name: falp-cdli-case
description: Worked example applying all 6 tools to the real FALP/CDLI/ElevenLabs partnership. Contains real names and partnership data. Do not load in shared contexts.
scope: private
---

# Applied Case: FALP / CDLI / ElevenLabs Partnership

**⚠️ Scope:** This case contains real partnership data (names, emails, terms). Do not load in shared contexts (Discord, group chats, sessions with external participants).

**Worked example using all 6 tools on the real Richard Cave email.**

*Reference: Email Richard Cave → Felipe/Pablo FALP, 2026-05-28*

---

## Source Evidence Ledger (Applied)

| ID | Claim or input | Source class | Source detail | Confidence | Used for | Limitation |
|---|---|---|---|---|---|---|
| S1 | Email from Richard Cave offering partnership | Primary | Email to Felipe/Pablo, 2026-05-28 | High | All phases | Private communication, not public |
| S2 | CDLI/UCL is ElevenLabs Impact Partner | Primary | Stated in email (S1) | High | Situation, Pilot, Risk | Not independently verified with ElevenLabs |
| S3 | Free voice cloning licences available now | Primary | Stated in email (S1) | High | Pilot, Risk | Tier, duration, BAA unspecified |
| S4 | ASR works in Colombian Spanish with excellent feedback | Primary | Stated in email (S1) | Medium | Pilot, Conference | No published validation study cited |
| S5 | Richard wants to present at Chilean conference | Primary | Stated in email (S1) | Medium | Conference | Conference name and date unknown |
| S6 | CDLI 2025: 3 countries, 12 languages, 3000h recorded | Public | cdl-inclusion.com/annual-summary | High | Situation | May not reflect 2026 figures |
| S7 | ElevenLabs Impact Program: 800+ nonprofits | Public | elevenlabs.io/impact-program | High | Situation | PR figure, not audited |
| S8 | Ley 21.719 (Chile, Dec 2024) classifies voice as personal data | Public | leychile.cl | High | Risk | Implementation details still pending |
| S9 | ElevenLabs has HIPAA-eligible service | Public | elevenlabs.io/docs/eleven-agents/legal/hipaa | High | Risk | "Eligible" ≠ confirmed BAA for this project |
| S10 | FALP has formal Comité Oncológico | Public | falp.org/comite-oncologico-falp/ | High | Stakeholder | Web confirms structure |
| S11 | Colombia ahead of Chile in CDLI partnership | Inference | S4 (Colombian works) + S6 (expansion) | Medium | Situation | No confirmation CDLI has Colombian partner |
| S12 | If FALP delays, Colombia becomes LatAm reference | Inference | S11 + CDLI expansion cycle | Low | Situation | Speculative competitive pressure |

---

## Tool 1: Strategic Situation Assessment — Applied

### Veredicto

Richard Cave offers a complete technology stack (ASR + TTS) with free licences and research collaboration. This is a high-value, time-sensitive opportunity where FALP's main asset is patient access and clinical context. The implicit clock is CDLI's 2026 expansion — if FALP doesn't move, another LatAm partner (likely Colombia) will.

### Qué está explícito
- Richard met FALP team in person, was impressed
- CDLI/UCL is ElevenLabs Impact Partner ("11 Labs - UCL")
- Free voice cloning licences available for FALP patients NOW
- ASR for impaired speech works in Colombian Spanish with excellent feedback
- Richard wants to present at a Chilean conference "later this year"
- Richard wants to test ASR with Chilean Spanish impaired speech
- Partnership would cover ASR + TTS + research

### Qué está implícito

| Inference | Confidence | Why |
|-----------|-----------|-----|
| CDLI needs Chilean Spanish data for their 2026 expansion | High | CDLI annual summary shows expansion is core mission |
| Colombia is ahead of Chile in this partnership | Medium | Colombian Spanish already works; Chilean doesn't |
| Richard personally drives this, not CDLI institutionally | High | All offers flow through Richard as admin of Impact Partner |
| Conference presentation is a forcing function for pilot readiness | High | Richard mentions it as context for the partnership |
| ElevenLabs licence terms are undefined (tier, duration, BAA) | High | Richard says "free" but no specifics on scope |

### Actores e incentivos

| Actor | Likely interest | What they need | Risk if ignored |
|-------|----------------|----------------|-----------------|
| Richard/CDLI | Expand to new language + country + population | Chilean Spanish impaired speech data; oncology use case | Gets data from Colombia instead |
| ElevenLabs | 1M voices mission; healthcare stories | Distribution via partners; impact stories | Many other Impact Partners exist |
| FALP | Voice banking for oncology patients; innovation | Tech stack + licences + expertise | Loses first-mover in LatAm |

### Reloj estratégico

- **Explicit:** "Later this year" conference
- **Implicit:** CDLI 2026 expansion cycle (India AI Summit was Feb 2026 — they're actively adding countries)
- **Competitive:** Colombia already has working ASR. If Chile delays, Colombia becomes the LatAm reference case.

### Recomendación

Respond within 1 week confirming interest. Request video call to clarify technical + legal questions. Define 2-3 patients for immediate ElevenLabs licence pilot.

---

## Tool 2: Stakeholder Power Map — Applied

### Mapa de actores

| Stakeholder | Role | Power | Interest | Alignment | Main concern | Best message |
|-------------|------|-------|----------|-----------|--------------|--------------|
| Richard Cave | External partner + tech provider | High | High | Ally | Expanding CDLI to new language | "We have patients + clinical context" |
| Pablo (FALP) | Internal clinical lead | High | High | Ally | Patient safety, institutional reputation | Clinical rationale + pilot design |
| Felipe | Technical/research bridge | Medium | High | Ally | Making this real, not just talk | Feasibility + evidence framework |
| Comité Oncológico FALP | Formal decision maker | High | Medium | Unknown | Institutional risk, governance | Structured proposal with risk controls |
| UIEC FALP | Research unit | Medium | Medium | Ally | Publishable evidence | Research design + ethics |
| ElevenLabs | Vendor | Low | Low | Neutral | Impact stories | Patient stories + Chilean context |
| Pacientes | Beneficiaries | Low (no voice) | High | Ally | Dignity, communication, safety | "Your voice preserved" |

### Secuencia recomendada

1. **Align:** Felipe + Pablo confirm shared vision
2. **Clarify:** Video call with Richard (technical + legal questions)
3. **Pilot design:** Felipe drafts pilot protocol with Pablo's clinical input
4. **Governance:** Present to Comité Oncológico for pilot approval
5. **Execute:** 3-5 patient pilot with ElevenLabs licences
6. **Conference:** Present early results with Richard

---

## Tool 3: Pilot Readiness Map — Applied

### Pregunta piloto

"Can ElevenLabs voice cloning combined with CDLI ASR provide meaningful communication support for Chilean Spanish-speaking oncology patients with altered laryngeal function?"

### Tipo de piloto

**Feasibility + Technical validation** — testing whether the tools work in this specific population, not measuring clinical efficacy.

### Alcance mínimo
- Participants: 5-8 patients
- Setting: FALP outpatient oncology
- Tool: ElevenLabs PVC + CDLI ASR app
- Duration: 8-12 weeks
- Workflow: Identify → consent → voice capture → surgery → post-op communication with cloned voice → feedback at 2, 4, 8 weeks

### Criterios
- **Inclusión:** CCC patients, scheduled laryngectomy, Spanish chileno hablante, ≥18 años, consentimiento informado
- **Exclusión:** Urgent surgery (<72h), cognitive impairment, unable to complete 1h voice recording

### Métricas

| Metric | Why | How | Minimum signal |
|--------|-----|-----|----------------|
| Voice capture completion | Feasibility | % patients completing recording | ≥70% |
| Cloned voice quality | Technical | MOS score (patient + blinded SLP) | ≥3.5/5 |
| Communication usefulness | Patient experience | SECEL (validated in Spanish) | Improvement |
| ASR accuracy chileno | Technical | Word error rate on impaired speech | <40% WER |
| Patient satisfaction | Experience | Likert + qualitative interview | ≥3/5 |

### Límites de claims
- **Can say:** "Feasible to implement", "Patients report satisfaction", "Technical validation completed"
- **Cannot say:** "Improves clinical outcomes", "Should be standard of care", "Validated therapy"

---

## Tool 4: Risk Governance Review — Applied

### Veredicto de riesgo

**Moderate-High.** Voice is biometric data. Ley 21.719 (Chile, Dec 2024) classifies voice as personal data. Cross-border transfer to ElevenLabs (US) requires evaluation.

### Datos involucrados

| Data type | Sensitivity | Who accesses | Concern | Control |
|-----------|-------------|-------------|---------|---------|
| Voice recordings | HIGH (biometric) | ElevenLabs cloud | US storage, no BAA confirmed | Confirm Impact Partner terms, data residency |
| Clinical status | HIGH | FALP team | Oncology = sensitive | De-identify for any external sharing |
| ASR training data | HIGH | CDLI/UCL | Cross-border to UK | Data processing agreement |
| Consent records | HIGH | FALP legal | Must comply with Ley 21.719 | Chilean legal review |

### Riesgos priorizados

| Risk | Prob | Severity | Mitigation | Stop condition |
|------|------|----------|------------|----------------|
| Voice data stored in US without adequate legal basis | High | High | Confirm BAA or data residency with Richard before any patient recording | If no data agreement, do not proceed |
| Patient expectations exceed evidence | Medium | Medium | Clear consent: "experimental, not treatment" | If consent form overpromises |
| CDLI uses Chilean voice data for other purposes | Low | High | Define data scope in MOU | If MOU not signed before data collection |
| Richard leaves CDLI | Low | High | Formalize with CDLI/UCL not just Richard | Ongoing — maintain institutional contact |

### Lo permitido ahora
- Respond to Richard expressing interest
- Internal alignment meeting Felipe + Pablo
- Review deck and prepare technical questions

### Lo no permitido todavía
- Recording any patient voice
- Sharing any clinical data externally
- Public announcements
- Committing to any timeline with Richard

---

## Tool 5: Conference Readiness Map — Applied

### Veredicto

**Not ready.** No confirmed event, no pilot data, no ethics approval. Conference mention is an opportunity marker, not a commitment.

### Claims ladder

| Category | Statements |
|----------|------------|
| Safe now | "Exploring partnership with UCL for voice banking accessibility" |
| Safe after pilot | "Feasibility pilot completed with N patients" |
| Hypothesis only | "Voice banking may improve patient communication experience" |
| Do not say | "Voice banking is an effective treatment for laryngectomy patients" |

### Backward plan (assuming conference ~Oct-Nov 2026)

- T-20w (Jun): Respond to Richard, start alignment
- T-16w (Jul): Video call, clarify terms
- T-12w (Aug): Ethics submission
- T-8w (Sep): Ethics approval, start pilot
- T-4w (Oct): Early data from first patients
- T-2w (Oct): Slide deck + internal review
- T-1w (Nov): Final rehearsal

### Próximo correo

Ask Richard: "What conference did you have in mind? Approximate dates? Would this be a joint presentation or solo?"

---

## Tool 6: Decision Memo — Applied

```
## MEMORANDUM

**DECISION REQUIRED:** Should FALP proceed as ElevenLabs Impact Partner 
via CDLI/UCL for a voice banking pilot with oncology patients?

**RECOMMENDATION:** Proceed with a narrow 5-8 patient feasibility pilot. 
Respond to Richard Cave within 1 week confirming interest. Schedule 
video call to clarify legal and technical terms before any patient contact.

**WHY NOW:** CDLI is in active 2026 expansion. Colombian Spanish ASR 
already works. If FALP delays, Colombia becomes the LatAm reference 
case. Richard's email shows momentum from the in-person meeting.

### Options

| Option | Description | Risk |
|--------|-------------|------|
| A: Defer | Wait for more internal alignment | Opportunity passes to Colombia |
| B: Narrow pilot | 5-8 patients, feasibility only | Moderate — manageable scope |
| C: Broader initiative | Full program with multiple cohorts | High — premature without pilot data |

### Recommended scope
- In: Feasibility pilot, 5-8 patients, ElevenLabs PVC + CDLI ASR, 
       SECEL/HADS/V-RQoL measurement, 12-week duration
- Out: Clinical efficacy claims, broad rollout, public announcements

### Next 14 days
1. Respond to Richard confirming interest
2. Internal meeting Felipe + Pablo to align on pilot design
3. Prepare list of technical + legal questions for Richard
4. Request deck access (PDF version)
5. Identify 2-3 candidate patients for immediate ElevenLabs licences
```

---

## Key takeaways from this case

1. **The signal was real and high-value** — Richard's email is not marketing, it's a specific offer from a credible partner
2. **The clock is ticking** — CDLI's 2026 expansion + Colombia ahead = urgency
3. **Risk is manageable** — Ley 21.719 requires legal review but is not a blocker
4. **The pilot should be narrow** — feasibility first, efficacy never claimed
5. **Voice is biometric data** — every governance decision must treat it as such
6. **Richard is the key node** — formalize with CDLI/UCL institutionally, not just Richard personally

---

*Applied case for Strategic Partnership Toolkit v1.0.0*
*Based on real email and audit data from 2026-05-28*
