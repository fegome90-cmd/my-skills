---
disable-model-invocation: true
name: learned-accuracy-fallacy-audit
description: Use when reviewing declarative prose that makes factual claims — presentation scripts, papers, exam answers, medical/legal/technical documentation, news, marketing copy, regulatory briefs — for factual accuracy against authoritative sources and/or for logical fallacies and inaccuracies. Triggers on "audit accuracy", "verify claims", "check for fallacies", "verificar datos", "cazar falacias", "revisar el guion/paper/brief", "confirmar datos contra fuentes", "fact-check", "review for errors", "check for inaccuracies".
---

# Accuracy + Fallacy Audit of Declarative Prose

## Context
Any accuracy/quality review of content that asserts facts — scripts, papers, exams, legal briefs, technical docs, specs, news, docs, books. Domain-agnostic: the workflow is the same whether the claims are clinical thresholds, legal citations, protocol parameters, historical dates, or statistics. NOT for code review (use code-review skills).

## Problem
Three failure modes that reviewers conflate:
1. **Internal inconsistency** (doc A vs doc B) — the easy, mechanical check.
2. **External inaccuracy** (doc vs ground truth) — the hard check most skip; needs authoritative verification.
3. **Logical fallacies** (overstatement, false dichotomy, appeal to authority, post hoc, hasty generalization) — a different reasoning layer than fact-checking.

A doc can pass #1 and still fail #2 or #3. Don't let a green consistency check create false confidence.

## Solution — 5-phase workflow

### Phase 1: Scope + lens selection
- Confirm WHICH lens the user wants: internal-consistency, external-accuracy, fallacy-hunt, or all three. They are different jobs.
- If a prior consistency audit exists, READ it as a risk map but do not redo its work.

### Phase 2: Claim extraction (write it down, don't keep it mental)
- Read source in **batched** reads (group small files; 8-10 per pass) to save context.
- Build a **claims table on disk**: every definition, number, threshold, citation, causal claim, statistic, named entity/date. One row per claim with location + verbatim.
- Mental inventories lose traceability and weaken the report.

### Phase 3: Identify the authoritative source FOR THAT DOMAIN, then verify in parallel
Sources are domain-specific — pick the right kind:
| Domain | Authoritative primary sources |
|---|---|
| Medicine/clinical | Society guidelines (IDSA, ASCO, WHO, regional consensus), RCTs, Cochrane reviews |
| Legal | Statutes, binding case law, regulations, official gazettes |
| Technical/eng | RFCs, ISO/ANSI/IEEE standards, official specs, vendor reference docs |
| Academic | Peer-reviewed papers (original > review), canonical textbooks |
| News/current | Primary records, official statements, wire services, archives |
| Product/marketing | Spec sheets, datasheets, regulatory filings, official docs |

- Consultar fuentes autorizadas (búsqueda web, consulta de documentación oficial o fetch de fuentes) **en paralelo** para las afirmaciones de mayor riesgo.
- **Consultar con precisión acotada** para evitar sobrecarga de contexto. Un volcado documental masivo inunda el contexto. Preferir consultas puntuales (`"MASCC score 21 low risk"`, no `"IDSA febrile neutropenia guideline"`) o lectura de la sección específica.
- Cite the **primary source**, not a secondary one citing it (a blog citing IDSA ≠ IDSA; a tutorial citing RFC 2616 ≠ RFC 2616).
- **KEY TACTIC — prefer the authority the AUDIENCE recognizes**: if presenting to a local/regional/expert audience, ground contested claims in the authority *they* defer to. Examples: regional medical consensus (SOCHINF for Chile, SEOM for Spain), the jurisdiction's own statute, the team's canonical spec, the field's seminal paper. The recognized authority often phrases the claim the same way the doc does — converting a debatable claim into a bulletproof one for that audience.

### Phase 4: Separate fallacy lens
- Re-read specifically hunting reasoning errors: overstatement ("sin base"/"siempre"/"nunca"), false dichotomy, appeal to authority, post hoc, hasty generalization, unsupported causality, cherry-picking.
- Flag **hedging quality**: good prose attenuates claims ("según protocolo local", "en la mayoría de los casos", "sujeto a X"). Absence of hedging on strong claims is itself a signal.

### Phase 5: Verdict report (structured, one row per claim)
Format: `claim → verdict (✅ correct / ⚠️ overstatement / ❌ incorrect / 🔍 unverified) → evidence (source + quote) → recommended action`. Separate hard errors (wrong data) from soft issues (branding, overstatement, citation year). End with a prioritized action list.

## Examples (multiple domains)

**Medical** — 28-chapter neutropenia script: 12 claims extracted; parallel-verified vs IDSA/ASCO/CISNE/MASCC/SEOM/SSC + regional SOCHINF 2023. 0 hard errors, 1 overstatement, 1 branding mismatch. The regional consensus (SOCHINF) stated the contested claim verbatim — anchored the rewording on it.

**Technical** — API doc claiming "HTTP/2 multiplexing eliminates head-of-line blocking": verify against RFC 7540 §5 (it does at the stream level, NOT the connection level for TCP) — likely an overstatement to correct.

**Legal** — brief citing "Ley 19.628 de 1999": verify against the official statute text and any amending laws; confirm the year and whether it's still in force.

**Academic** — paper citing "Smith et al. 2020 showed X": fetch the actual paper; confirm X is what they found, not a paraphrase drift.

## Gotchas
- **Edit tool with accented/special paths can fail** ("paths[0] must be string"). Fall back to `write` with full file content — don't burn >2 attempts.
- **Internal-consistency ≠ accuracy.** Perfectly consistent docs can be factually wrong.
- **"Unverified" ≠ "wrong".** When no source is found in time, label 🔍 and ask the author — don't guess.
- **Primary > secondary.** Always cite the original guideline/statute/paper/RFC, not something quoting it.
- **Don't invent an authority.** If the recognized regional/expert source doesn't exist or doesn't say what you need, label the claim 🔍 — regional grounding is a credibility multiplier, not a substitute for missing evidence.

## Activation Signals
- "revisá este guion/paper/brief/script por errores"
- "verificar los datos contra las fuentes/guías/norma"
- "cazar falacias / fallacies / incorrecciones"
- "audit de precisión / fact-check / accuracy audit"
- "confirmar que no haya datos incorrectos"
- Reviewing exam answers, medical/legal/technical/academic/news content for factual correctness
- Author about to present/submit content to a specialist/regulator/expert audience
