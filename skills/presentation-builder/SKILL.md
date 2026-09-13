---
name: presentation-builder
description: 'Walk through a rigorous context deep-dive before building any deck. Interview the user relentlessly about purpose, audience, power dynamics, institutional context, and evidence — resolving each branch of the decision tree before generating slides. Then build a structured deck using the 10-20-30 framework, Duarte storytelling, and Pyramid Principle.'
when: 'When the user asks to create, build, or structure a presentation, pitch deck, or slide deck. Also when they say "armar presentación", "crear deck", "presentation builder", "build slides", or want help preparing a talk.'
examples:
  - "armar presentación"
  - "crear deck para investors"
  - "presentation builder"
  - "build slides for board meeting"
  - "necesito una presentación de ventas"
  - "help me structure a TEDx talk"
  - "reunión con experto externo"
  - "presentación para consulta"
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
  openclaw:
    requires:
      bins: []
    emoji: "🎯"
    primaryEnv: null
---

# Presentation Builder

> **OBJECTIVE:** First, understand the context deeply. Then build presentations that are well-structured and immediately usable.
> A bad output from this skill = a deck built without understanding the room. A good output = a deck shaped by the context, power dynamics, and institutional constraints before a single slide is written.

---

## CRITICAL: Read This First

This skill has TWO distinct modes depending on what you need:

**1. Full context deep-dive (recommended for first use):**
Start at Phase 1 and interview the user branch by branch. Do NOT generate slides before completing Phase 1.

**2. Quick generation (when context is already known):**
If the user has already provided full context (purpose, audience, power dynamics, evidence, constraints), you may skip Phase 1 and start at Phase 2.

Read before generating:
1. **This file** (SKILL.md) — the complete workflow
2. **`resources/templates.md`** — slide-by-slide templates per type
3. **`resources/frameworks-quick-ref.md`** — the 4 frameworks condensed

For deep reference on specific topics, read from the wiki (see §Wiki Resources below).

---

## Phase 1: Context Deep-Dive (Grill Style)

**Do NOT generate any slides yet.** Interview the user relentlessly about every aspect of the context until reaching shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one by one.

For each question:
1. Ask the question
2. Provide a **recommended answer** based on context you already have
3. If the question can be answered by exploring the codebase, explore instead
4. Do NOT advance to the next branch without a real answer

One question at a time. This is not a form to fill — it's a conversation that reveals what kind of deck this needs to be.

### Branch 1 — Purpose & Intent
> Why are we presenting? What's the real goal?
>
> Options:
> - **pitch** (persuade to invest/buy)
> - **board/corporate** (recommend a decision to internal stakeholders)
> - **expert-briefing** (present context so an expert can evaluate and guide)
> - **educational** (teach a skill or concept)
> - **conference** (share an idea with peers)
> - **academic** (defend research)
> - **other** (describe)

For **expert-briefing**: the goal is NOT to persuade the expert. The goal is to give them enough context so their guidance is well-informed. The audience is your own team + the expert. The expert's role is referent, not target.

> Recommended: _(infer from context, or say "I need help distinguishing")_

### Branch 2 — Audience & Power Dynamics
> Who is in the room? What are their relationships and hierarchies?
>
> Map each person/role:
> - Name / Role
> - What do they need from this meeting?
> - What power do they hold?
> - Should they appear on slides? (Rule: only if it reinforces their position as decision-maker, never if it assigns them tasks)
>
> List them all. If there's an external expert in the room, flag their role explicitly.

### Branch 3 — Expert/Stakeholder Positioning
> If there is an external expert in the room: what is their relationship to the project? To the institution? To the other attendees?
>
> Critical rule: **Expert personal requests are oral, not projected.**
> - If the meeting involves asking an expert for guidance, do NOT put that request on a slide
> - The question is delivered orally after the slide, maintaining the expert's position as referent, not operational resource
> - Projecting "what we need from you" on a slide subordinates the expert and turns the rest of the room into spectators

### Branch 4 — Institutional Context & Boundaries
> What institution are you presenting FROM or AT? What are the political, ethical, regulatory, or cultural constraints?
>
> Check:
> - Is the institution presenting itself, or is this a partnership pitch?
> - Are there claims that could harm institutional credibility if overstated?
> - Are there data privacy or ethical boundaries (patient data, voice data, AI)?
> - Is the tone expected to be assertive or exploratory?
>
> Key rule for institutional contexts: **soften absolute claims**
> - ❌ "no existe" → ✅ "no hemos identificado"
> - ❌ "puede ofrecer" → ✅ "podría explorar"
> - ❌ "siempre" / "nunca" → ✅ "consistentemente" / "no hemos visto"

### Branch 5 — Evidence & Claims Safety
> What evidence do you have? What's solid vs risky?
>
> For each piece of evidence, classify:
> - **Solid**: published, peer-reviewed, institutionally validated
> - **Soft**: estimated, extrapolated, internally collected
> - **Risky**: unvalidated clinical numbers, invented outcomes, absolute claims
>
> **Risky evidence must be:**
> - Removed from main deck (move to appendix)
> - Replaced with honest caveats
> - Flagged in speaker notes as "if asked"
>
> Checklist:
> - [ ] No absolute claims ("no existe", "siempre", "todos")
> - [ ] No unvalidated clinical numbers or estimated outcomes
> - [ ] No data category confusion (e.g., TQT ≠ laryngectomy)
> - [ ] No moral pressure tone ("solo falta voluntad")

### Branch 6 — Format & Logistics
> - Time limit: _ (default: 20 min)
> - Slide limit: _ (default: 10-16)
> - Language: _ (default: same as conversation)
> - Venue: _ (auditorium, boardroom, video call?)
> - Brand/style requirements: _
> - What should happen AFTER the presentation? (Decision? Q&A? Workshop?)

---

## Phase 2: Quick Discovery (informed by deep-dive)

If Phase 1 was completed, you already have these answers. Use them.

If Phase 1 was skipped (quick mode), confirm these 5 points before generating:

### Q1 — Purpose & Format
> What type of presentation is this?
>
> Options: pitch deck (investors) | sales pitch | board/corporate meeting | expert-briefing | educational/training | conference/TEDx talk | academic defense | other (describe)

### Q2 — Audience & Transformation
> Who is the audience and what transformation do you want?
>
> - **For persuasion types:** "They walk in as [current state], they walk out as [desired state]"
> - **For expert-briefing:** "What context does the expert need to evaluate? What question are you asking them?"

### Q3 — Core Message (SCQA)
> What's the situation, complication, and answer?
>
> - **For persuasion:** **S** (what they know) → **C** (what changed) → **Q** (question) → **A** (your recommendation)
> - **For expert-briefing:** **S** (context they need) → **C** (local reality) → **Q** (open question — no A, that's what you're asking them)

### Q4 — Key Evidence
> What are your 3 strongest pieces of evidence? (Mark any that are soft/risky.)

### Q5 — Constraints
> - Time limit: _ (default: 20 min)
> - Slide limit: _ (default: 10-16)
> - Language: _ (default: same as conversation)
> - Brand/style requirements: _
> - What should happen AFTER the presentation? (CTA): _

---

## Phase 3: Generate the Deck

### Output Format — EXACTLY This Structure

For **EACH** slide, output this format:

```markdown
---
### Slide N: [ACTION TITLE]

**Duarte tag:** [What is | What could be | New bliss | CTA]
**Type:** [title | data | recommendation | demo | closing]
**Time:** [X min]

**ON THE SLIDE** (what the audience sees):
- [Max 3 bullets. Short. Visual. No paragraphs.]
- [Chart: describe type and what it shows]
- [Image: describe what image and why]

**SPEAKER NOTES** (what to SAY — this is NOT what's on the slide):
[2-4 sentences of exactly what the presenter says. Written as they would speak it. Include the transition FROM the previous slide.]

**VISUAL SUGGESTION:** [Layout: full-bleed image | split text/image | data chart | big number | title card]
```

### Rules for Action Titles
- State WHAT the data MEANS, not what it shows
- ❌ "Revenue by quarter" → ✅ "Revenue grew 15% in Q4, signaling turnaround"
- ❌ "Team overview" → ✅ "A team with 3 exits and 40 years combined experience"
- **Test:** Read all titles in sequence. Does the argument flow?

#### Advisory for institutional/expert-briefing contexts
Strong action titles can become **overclaims** when the audience includes experts or decision-makers who know the domain. In these contexts, exploratory framing may be more credible:
- ❌ "FALP puede ofrecer un entorno que no existe" → ✅ "FALP podría explorar un rol aún poco desarrollado"
- ❌ "No hay partner clínico" → ✅ "No hemos identificado un modelo equivalente"
- ❌ "Solo falta voluntad" → ✅ "Las condiciones institucionales están parcialmente alineadas"

**Rule of thumb in institutional contexts:** If your title says something definitively about what doesn't exist or what you uniquely offer, ask: "Can I prove this with a verifiable source? If not, soften it."

### Rules for Speaker Notes
- Written as SPOKEN language, not written language
- They ADD information not on the slide, they don't repeat it
- Include the bridge/transition from previous slide
- Mark contrast moments with **[CONTRAST]** when shifting "what is" → "what could be"
- Include specific phrases: "Imagine...", "But here's the problem...", "Now watch what happens..."

#### Expert question rule (expert-briefing only)
**Expert personal requests are NOT in speaker notes that go on slides.** They are delivered as oral transitions AFTER the slide:
> ✅ Speaker notes end with: *"[Transición oral — no se proyecta] La pregunta al experto se hace en voz alta, sin slide."*
>
> ❌ Never: *"Richard, necesitamos que nos ayudes con tres preguntas"* on a slide.

The question to the expert:
- Goes AFTER the slide closes
- Is addressed to the room first, then to the expert
- Asks for their **criteria**, not their labor
- Example: *"Richard, desde tu experiencia, ¿qué señal mirarías para distinguir entre una idea atractiva y una iniciativa preparada para avanzar?"*

This preserves the expert as **referent who comments**, not **resource who is tasked**.

### Rules for Slide Content
- Maximum 3 bullets per slide
- Each bullet ≤ 10 words
- If you need more, split into 2 slides
- No paragraphs on slides. Ever.

### Example — Good Output vs Bad Output

**❌ BAD (what NOT to do):**
```
### Slide 3: Nuestra Solución

**Content:**
- Nuestro producto utiliza IA avanzada
- Machine learning para predecir demanda
- Integración con ERP existente
- Dashboard en tiempo real
- Alertas automatizadas
- API REST para conectividad
- Soporte 24/7

**Speaker notes:**
Hablar sobre las features del producto y cómo funciona la tecnología.
```

Problems: title is a label (not an action title), 7 bullets (too many), speaker notes say "talk about" instead of saying WHAT to say, no Duarte tag, no timebox, no visual suggestion.

**✅ GOOD (what TO do):**
```
---
### Slide 4: Un sistema que reduce tiempo de espera en 60%

**Duarte tag:** What could be
**Type:** solution
**Time:** 2 min

**ON THE SLIDE:**
- "Antes: 90 días promedio de espera"
- "Después: 36 días con triage automático"
- Chart: Before/after bar chart, 2 bars, dramatic difference

**SPEAKER NOTES:**
"Hasta ahora les mostré el problema. **[CONTRAST]** Pero imaginen esto: en lugar de 90 días, sus pacientes esperan 36. No es magia — es un sistema de triage que prioriza automáticamente basado en gravedad. Déjenme mostrar cómo funciona."

**VISUAL SUGGESTION:** Big number layout — "60%" en font 120pt centrado, con before/after bars debajo
```

### Duarte Pattern Verification

After generating all slides, output this verification:

**For persuasion decks (pitch, sales, conference):**
```
**Duarte Pattern Check:**
[ ] Slides alternate between "What is" and "What could be" (no 3+ consecutive of same type)
[ ] At least 3 contrast moments marked with [CONTRAST] in speaker notes
[ ] Ends with "New bliss" + specific CTA
[ ] Does NOT end with "¿Preguntas?" or "Gracias"
```

**For expert-briefing decks:**
The standard Duarte arc (What is → What could be → New bliss) assumes you're persuading. For expert briefings, the arc shifts:

```
**Expert-Briefing Arc:**
[ ] Arc: Context → Evidence → Options → Oral ask (not persuasion)
[ ] "New bliss" is replaced by "responsible decision by the group"
[ ] No slide projects a personal request to the expert
[ ] Closing asks the room to choose a path, not to approve a recommendation
[ ] Expert question is marked as oral, outside slides
```

### 10-20-30 Verification

```
**10-20-30 Check:**
[ ] Total slides: [N] (target: ≤16)
[ ] Total time: [N] min (target: ≤20)
[ ] Every slide has action title (not label)
[ ] Max 3 bullets per slide
[ ] Font ≥30pt implied (no dense text)
```

---

## Phase 4: Delivery Notes

After the deck, provide these 4 sections:

### Opening Hook (first 30 seconds)
Write the exact first words the presenter says. Not "start with a hook" — the actual words.

Example:
> "¿Saben cuántos pacientes en Chile esperan más de 90 días para una consulta oncológica? [pause] Doce mil. Doce mil personas esperando, mientras el cáncer avanza."

### Bridge Phrases (3-5)
Exact phrases for transitions between major sections:
- Problem → Solution: "Ese es el problema. Pero hay una forma de cambiarlo."
- Data → Insight: "Los números son claros. Ahora, ¿qué significan para ustedes?"
- Evidence → CTA: "Todo lo que les mostré apunta a una conclusión."

### Closing Line
The exact last sentence. NOT "gracias". Something they'll remember.

Example:
> "En 12 meses, podemos reducir la espera de 90 a 36 días. No con más recursos — con mejor priorización. El primer paciente que no espere 90 días podría ser el suyo."

### Q&A Prep (3 questions)
| Likely question | Suggested answer (60 seconds max) |
|----------------|----------------------------------|
| [Toughest question they'll ask] | [Direct answer + evidence] |

---

## Phase 5: Quality Gate

### Technical Quality
Before delivering to the user, verify ALL of these:

- [ ] Every slide has an ACTION TITLE (conclusion, not label)
- [ ] Every slide has a DUARTE TAG
- [ ] Speaker notes are WRITTEN AS SPOKEN (not "talk about X")
- [ ] No slide has >3 bullets
- [ ] Duarte pattern alternates (no 3+ consecutive same tag)
- [ ] SCQA is present in the first 2 slides
- [ ] Ends with specific CTA, not "¿Preguntas?"
- [ ] Total time ≤20 min for main content
- [ ] Total slides ≤16
- [ ] Opening hook has exact words written out
- [ ] Closing line has exact words written out

### Institutional Safety Gate
If this is an institutional or expert-briefing presentation, ALSO verify:

- [ ] No absolute claims ("no existe", "siempre", "todos") — use "no hemos identificado", "aún poco desarrollado"
- [ ] No unvalidated clinical numbers or estimated outcomes
- [ ] No personal requests projected on slides — expert questions are oral
- [ ] No data category confusion (e.g., TQT ≠ laryngectomy)
- [ ] No moral pressure tone ("solo falta voluntad", "no podemos seguir esperando")

**If ANY of these fail, fix before showing to the user.**

---

## Framework Reference

For detailed templates and framework breakdowns:
- `resources/templates.md` — Slide-by-slide templates per presentation type
- `resources/frameworks-quick-ref.md` — 4 frameworks one-page reference

## Wiki Resources (TQTApp)

Deep reference material in `~/Developer/tqt_app/docs/wiki/references/`:
- `presentation-10-20-30-rule.md` — Marco completo con receta paso a paso y ejemplos before/after
- `presentation-opening-techniques.md` — 7 técnicas de apertura con ejemplos
- `presentation-closing-techniques.md` — 8 técnicas de cierre + selector por contexto
- `presentation-data-visualization.md` — Selector de gráficos y data storytelling
- `presentation-common-mistakes.md` — 14 errores comunes con fixes
- `presentation-delivery.md` — Voz, body language, presencia, Q&A, entrega virtual
- `presentation-psychology.md` — Cognitive load, eye-tracking, curva de atención
- `presentation-case-studies.md` — Jobs (iPhone), MLK, TED, pitch decks deconstruidos
- `presentation-storytelling.md` — Three-Act, Duarte contrast, Hero's Journey
- `presentation-audience-adaptation.md` — 5 filtros de prioridad, executive vs técnico
- `presentation-preparation.md` — Three-Pass rehearsal, distributed practice, checklist

**When to read wiki:** When the user needs deep expertise on a specific area (e.g., "how to present to CFOs" → read audience-adaptation). For normal presentation building, the skill files + this SKILL.md are sufficient.
