---
name: output-templates
description: Formatted output structures for all tools. Load when producing final output.
---

# Output Templates

Standard output structures for each tool.

---

## Output Envelope (mandatory for final deliverables)

All final deliverables from this skill must include an envelope header that passes `scripts/enforce-envelope`.

```
Status: PASS | FAIL | BLOCKED
Summary: [one-line description]
Artifacts: [file1.md, file2.md] or []
Evidence: [what supports this output]
Risks: [known limitations]
Next: [what happens next]
```

The envelope does NOT replace the analysis content. It sits at the top of the file, separated by `---`.

Validation: `python3 scripts/enforce-envelope <file> --root <project_root>`

---

## Tool 1: Strategic Situation Assessment

```
### Veredicto
[2-4 sentence strategic reading]

### Qué está explícito
- [direct facts from input]

### Qué está implícito
| Inference | Confidence | Why |
|-----------|-----------|-----|
| ... | High/Med/Low | ... |

### Actores e incentivos
| Actor | Likely interest | What they need | Risk if ignored |
|-------|----------------|----------------|-----------------|
| ... | ... | ... | ... |

### Reloj estratégico
[Timeline pressure + what must exist before next milestone]

### Riesgos principales
| Risk | Probability | Severity | Exposure |
|------|-------------|----------|----------|
| ... | ... | ... | ... |

### Opciones
| Option | Description | Risk |
|--------|-------------|------|
| Conservative | ... | Low |
| Focused fast | ... | Medium |
| Ambitious | ... | High |

### Recomendación
One move, one owner, one artifact, one boundary.

### Frase útil para responder
[Draft response preserving optionality]
```

---

## Tool 2: Stakeholder Power Map

```
### Veredicto político
[Plain political reality]

### Mapa de actores
| Stakeholder | Role | Power | Interest | Alignment | Main concern | Best message | Ask |
|-------------|------|-------|----------|-----------|--------------|--------------|-----|
| ... | ... | H/M/L | H/M/L | Ally/Neutral/Blocker | ... | ... | ... |

### Riesgos de manejo
- [top political risks + avoidance]

### Secuencia recomendada
1. [Align inner cell]
2. [Secure gatekeepers]
3. [Brief influencers]
4. [Prepare decision memo]
5. [Expand to wider group]

### Mensajes por actor
[Concise tailored language per stakeholder]

### Próximo movimiento
[One meeting/memo/action]
```

---

## Tool PREREQUISITE: Source Lock Gate

```
### Source Lock Gate — [date]

**Source:** [what was analyzed]

**Verbatim:**
> [exact quote]

**Frame:**
- IS about: [list]
- IS NOT about: [list]

**Entities (N):**
1. [Name] — [description]
2. ...

**Conflation check:** [PASS / FAIL]
```

## Tool PREREQUISITE: Actor Separation

```
### Actor Separation Checkpoint

| Entity | Nature | Status | Authority | Key risk |
|--------|--------|--------|-----------|----------|

**SPOFs:** [list]
**Ambiguities:** [list]
**Check:** [PASS / FAIL]
```

## Tool 0.5: Perspective Pack

```
### Perspective Pack — [date]

**This document contains NO recommendation.**

### 1. Source Lock Statement
[verbatim + IS/IS NOT frame]

### 2. Actor Separation
[table]

### 3. Alternative Readings (7+)
For each: what must be TRUE, evidence for, evidence against.

### 4. Bias Map
[table per actor]

### 5. What Different Actors Would Ask
[one question per actor type]

### 6. Uncomfortable Questions (12+)

### 7. Evidence Gaps
[table with SOURCE GAP markers]
```

---

## Tool 3.5: Weighted Decision Matrix

```
### Matriz de Decisión Ponderada

**Criterios:**
| # | Criterio | Peso | Definición |
|---|---------|------|------------|
| 1 | ... | 5 | ... |

**Scores por estado:**
| # | Criterio | Peso | Exploración | Due Diligence | Piloto Clínico | Evidencia |
|---|---------|------|:-----------:|:-------------:|:-------------:|----------|

**Totales:**
| Estado | Ponderado | Normalizado (/5) | Nivel |
|-------|-----------|-----------------|-------|

**Interpretación:**
[What the scores mean for each phase]
```

## Tool 3.5b: Decision Gates

```
### Decision Gates (post-meeting: [description])

| # | Pregunta | GO | PAUSA | STOP | Evidencia requerida |
|---|----------|----|------|------|-------------------|

**Resumen:** X GO, Y PAUSA, Z STOP
**Decisión:** [Cannot proceed until STOP gates G1, G2... resolved]
```

## Tool 3.5c: Data Flow Diagram

```
### Diagrama de Flujo de Datos

[ASCII flow: PACIENTE → GRABACIÓN → SUBIDA → PROCESAMIENTO → ALMACENAMIENTO → ACCESO → ELIMINACIÓN]

| Nodo | Quién | Dónde | Cómo | Duración | Revocación | Auditoría |
|------|------|-------|------|----------|-----------|----------|

### Gaps críticos
1. [gap] — severidad

### Protocolo de revocación
[paso a paso]
```

## Tool 3.5d: Claim Ledger

```
### Claim Ledger

| # | Afirmación | Estado | Fuente / Evidencia | Notas |
|---|-----------|--------|-------------------|-------|

**Resumen:** X verificadas, Y parciales, Z descartadas, W hipótesis
```

## Tool 3.5e: Verdict Levels

```
### Veredicto por Niveles

| Dimensión | Veredicto | Justificación |
|-----------|---------|---------------|
| Estructural | [PASS/PARTIAL/FAIL/NYA] | ... |
| Metodológico | [...] | ... |
| Factual | [...] | ... |
| Institucional | [...] | ... |

### Comparación con versión anterior
[Table showing changes]
```

---

## Tool 3.5b: Decision Gates

```
| # | Question | GO | PAUSE | STOP | Evidence required |
|---|----------|----|------|------|-------------------|
**Summary:** X GO, Y PAUSE, Z STOP
**Decision:** [What must resolve before proceeding]
```

See `resources/decision-gates.md` for full method.

## Tool 3.5c: Data Flow Diagram

```
[PACIENTE] → [CAPTURE] → [UPLOAD] → [PROCESSING] → [STORAGE] → [ACCESS] → [DELETION]

| Node | WHO | WHERE | HOW | DURATION | REVOCATION |
```

See `resources/data-flow-diagram.md` for full method.

## Tool 3.5d: Claim Ledger

```
| # | Claim | Status (✅⚠️❌🟡) | Source | Notes |
**Summary:** X verified, Y partial, Z discarded, W hypotheses
```

See `resources/claim-ledger.md` for full method.

## Tool 3.5e: Verdict Levels

```
| Dimension | Verdict | Justification |
|-----------|---------|---------------|
| Structural | PASS/PARTIAL/FAIL/NYA | ... |
| Methodological | ... | ... |
| Factual | ... | ... |
| Institutional | ... | ... |
```

See `resources/verdict-levels.md` for full method.

---

## Tool 3: Pilot Readiness Map

```
### Veredicto
[Viable / Premature / Unsafe]

### Pregunta piloto
[One primary question]

### Tipo de piloto
[Feasibility / Usability / Technical / Workflow / Experience / Pre-research]

### Alcance mínimo
- Participants: [n]
- Setting: [where]
- Tool: [what]
- Duration: [weeks]

### Criterios
- Inclusión: [list]
- Exclusión: [list]

### Gobernanza mínima
| Area | Owner | Responsibility | Blocking risk |
|------|-------|----------------|---------------|
| ... | ... | ... | ... |

### Métricas
| Metric | Why | How | Minimum signal |
|--------|-----|-----|----------------|
| ... | ... | ... | ... |

### Límites de claims
- Can say: [list]
- Cannot say: [list]
```

---

## Tool 4: Risk Governance Review

```
### Veredicto de riesgo
[Low / Moderate / High / Not enough info]

### Etapa real del proyecto
[Current stage + what is not yet authorized]

### Datos involucrados
| Data type | Sensitivity | Who accesses | Concern | Control |
|-----------|-------------|-------------|---------|---------|
| ... | ... | ... | ... | ... |

### Riesgos priorizados
| Risk | Prob | Severity | Exposure | Mitigation | Stop condition |
|------|------|----------|----------|------------|----------------|
| ... | ... | ... | ... | ... | ... |

### Autoridades necesarias
| Authority | Why | Before what action |
|-----------|-----|-------------------|
| ... | ... | ... |

### Lo permitido ahora
- [safe actions]

### Lo no permitido todavía
- [blocked actions requiring approval]
```

---

## Tool 5: Conference Readiness Map

```
### Veredicto
[Ready / Near-ready / Not ready]

### Evento y ambigüedad
- Named: [yes/no]
- Date: [confirmed/TBD]
- Slot: [confirmed/TBD]
- Audience: [type]

### Objetivo de presentación
[One primary objective]

### Evidencia mínima requerida
| Evidence | Needed for | Status | Owner | Deadline |
|----------|-----------|--------|-------|----------|
| ... | ... | ... | ... | ... |

### Claims ladder
| Category | Statements |
|----------|------------|
| Safe now | ... |
| Safe after data | ... |
| Hypothesis only | ... |
| Do not say | ... |

### Backward plan
T-12w: ...
T-8w: ...
T-4w: ...
T-2w: ...
T-1w: ...
```

---

## Tool 6: Decision Memo

```
## MEMORANDUM

**DECISION REQUIRED:** [one sentence]

**RECOMMENDATION:** [one paragraph]

**WHY NOW:** [deadline/opportunity/risk of inaction]

### Context
[Factual background, 3-5 sentences]

### Options
| Option | Description | Pros | Cons | Risk |
|--------|-------------|------|------|------|
| A: Defer | ... | ... | ... | Low |
| B: Narrow pilot | ... | ... | ... | Medium |
| C: Broader initiative | ... | ... | ... | High |

### Recommended scope
- In scope: [list]
- Out of scope: [list]

### Governance
- Approvals needed: [list]
- Owners: [list]

### Risks
| Risk | Mitigation | Owner |
|------|------------|-------|
| ... | ... | ... |

### Decision ask
[Specific approval/alignment requested]

### Next 14 days
1. ...
2. ...
3. ...
```

---

*Templates for Strategic Partnership Toolkit v1.5.1*
