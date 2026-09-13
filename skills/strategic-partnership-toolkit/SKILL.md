---
name: strategic-partnership-toolkit
description: >
  Use this skill pack when analyzing strategic partnerships, stakeholder dynamics,
  pilot readiness, conference preparation, risk governance, or decision memos in
  health innovation, AI accessibility, voice banking, or institutional collaboration contexts.
  Progressive disclosure: SKILL.md orchestrates, resources/ contain deep phases,
  harnesses/ enforce full-chain execution with audit.
  v1.5.1: Aligned versions, harness flow, and output-path contract. Context Discovery
  remains mandatory before analysis.
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.5.1"
---

# Strategic Partnership Toolkit

## Purpose

Convert ambiguous institutional signals into clear decisions and action.

16 tools + source discipline + self-audit + execution harness.

## When to activate

- Email from a potential partner with vague but promising terms
- Meeting notes that need political reading
- A pilot opportunity that must be scoped before it drifts
- A conference mention that implies a deadline
- A vendor/partner relationship with unclear risk
- A decision that needs an executive memo

## Architecture

```
strategic-partnership-toolkit/
├── SKILL.md                                    ← you are here
├── resources/
│   ├── phase-1-quick-assessment.md             ← always read first
│   ├── source-evidence-ledger.md               ← source discipline (before analysis)
│   ├── strategic-situation-assessment.md        ← tool 1
│   ├── stakeholder-power-map.md                ← tool 2 (now with 2-layer model)
│   ├── source-lock-gate.md                     ← MANDATORY pre-analysis
│   ├── actor-separation-checkpoint.md          ← MANDATORY Phase 1
│   ├── perspective-pack.md                     ← tool 0.5: anti-bias, no recommendation
│   ├── decision-matrix-weighted.md             ← tool 3.5 (NEW: weighted multi-state matrix)
│   ├── decision-gates.md                       ← tool 3.5b (NEW: post-meeting GO/PAUSE/STOP)
│   ├── data-flow-diagram.md                    ← tool 3.5c (NEW: mandatory before any patient data protocol)
│   ├── claim-ledger.md                         ← tool 3.5d (NEW: systematic claim tracking)
│   ├── verdict-levels.md                       ← tool 3.5e (NEW: 4-level verdict system)
│   ├── pilot-readiness-map.md                  ← tool 3
│   ├── risk-governance-review.md               ← tool 4
│   ├── conference-readiness-map.md             ← tool 5
│   ├── decision-memo-writer.md                 ← tool 6
│   ├── output-templates.md                     ← formatted output structures (updated)
│   ├── strategic-analysis-audit-checklist.md   ← self-audit (after analysis)
│   └── falp-cdli-case.md                       ← worked example (real data, scope-limited)
└── harnesses/
    ├── falp-strategic-analysis-harness.md      ← full-chain execution guide
    ├── falp_strategy_harness.py               ← CLI gatekeeper (Python, 10-phase)
    └── skill_gate.sh                           ← portable validator (Bash, embed-in-markdown)
scripts/
    └── claim-audit.sh                         ← bash: audit claim ledger (tags, thresholds, JSON)
    └── enforce-envelope                        ← python: validate output envelope (form, evidence, artifacts)
```

**Context reduction:** SKILL.md = ~6% of total. Load phase-1 + 1-2 tools + source ledger = ~20% per session. Full harness = ~40%.

## Two validation layers

| Layer | Script | Scope | When to use |
|-------|--------|-------|-------------|
| **Python harness** | `harnesses/falp_strategy_harness.py` | 10-phase folder validation | Full strategic analysis with separate phase files |
| **Bash gate** | `harnesses/skill_gate.sh` | Embedded block in markdown | Quick validation of final output before delivery |

The Python harness creates and validates a run folder with 10 phase files.
The Bash gate validates a `<!-- skillgate:start/end -->` block embedded in any markdown file.
Use both for high-stakes analysis. Use Bash gate alone for quick checks.

### Stage mapping: Bash gate ↔ Python harness

| Bash stage | Python phases |
|------------|---------------|
| `intake` | `00_INPUT` |
| `analysis` | `01_SOURCE_EVIDENCE_LEDGER` + `02_STRATEGIC_SITUATION` + `03_STAKEHOLDER_MAP` + `04_PILOT_READINESS` + `05_RISK_GOVERNANCE` + `06_CONFERENCE_READINESS` |
| `output` | `07_DECISION_MEMO` |
| `self_audit` | `08_CROSS_SKILL_AUDIT` + `09_CLAIM_VERIFICATION` |
| `handoff` | `10_FINAL_DELIVERABLE` |

When using both layers: complete Python phases → map to bash stages → embed skillgate block in final deliverable.

## Tools

| # | Tool | Resource | When to use | Time |
|---|------|----------|-------------|------|
| **PREREQUISITE** | **Source Lock Gate** | `resources/source-lock-gate.md` | MANDATORY before any analysis | 3 min |
| **PREREQUISITE** | **Actor Separation** | `resources/actor-separation-checkpoint.md` | MANDATORY in Phase 1 | 3 min |
| 0 | **Source Evidence Ledger** | `resources/source-evidence-ledger.md` | Before any analysis: classify sources | 5 min |
| 0.5 | **Perspective Pack** | `resources/perspective-pack.md` | User wants blind spots/biases, NOT a decision | 20 min |
| 1 | **Strategic Situation Assessment** | `resources/strategic-situation-assessment.md` | Ambiguous signal → decision frame | 15 min |
| 2 | **Stakeholder Power Map** | `resources/stakeholder-power-map.md` | Political landscape → message strategy (2-layer: formal + informal) | 20 min |
| 3 | **Weighted Decision Matrix** | `resources/decision-matrix-weighted.md` | Opportunity → phased scores (exploration/due diligence/pilot) | 15 min |
| 3b | **Decision Gates** | `resources/decision-gates.md` | Post-meeting → GO/PAUSE/STOP classification | 10 min |
| 3c | **Data Flow Diagram** | `resources/data-flow-diagram.md` | Before any patient data protocol | 15 min |
| 3d | **Claim Ledger** | `resources/claim-ledger.md` | During/after analysis → verify/discard hypotheses | 10 min |
| 3e | **Verdict Levels** | `resources/verdict-levels.md` | Final assessment → 4-level verdict | 5 min |
| 4 | **Pilot Readiness Map** | `resources/pilot-readiness-map.md` | Opportunity → testable narrow pilot | 25 min |
| 5 | **Risk Governance Review** | `resources/risk-governance-review.md` | Excitement → risk inventory + controls | 20 min |
| 6 | **Conference Readiness Map** | `resources/conference-readiness-map.md` | Event mention → backward plan | 15 min |
| 7 | **Decision Memo Writer** | `resources/decision-memo-writer.md` | Analysis → one-page decision ask | 10 min |
| GRILL | **User Interrogation** | `grill-me` pattern | AFTER analysis, BEFORE output | 10-20 min |
| 8 | **Audit Checklist** | `resources/strategic-analysis-audit-checklist.md` | After all skills + grill: consistency check | 10 min |

## Two execution modes

### Mode A: Flexible (default)

Use Phase 1 to classify the signal, then load only the tools needed.

1. Run Context Discovery (Step 0 below)
2. Read `resources/phase-1-quick-assessment.md`
3. Pass Source Lock Gate + Actor Separation
4. Create source ledger (`resources/source-evidence-ledger.md`)
5. Run recommended tools in sequence
6. Grill assumptions with the user when available
7. Run audit checklist (`resources/strategic-analysis-audit-checklist.md`)
8. Deliver output

### Mode B: Full harness (for high-stakes decisions)

Read `harnesses/falp-strategic-analysis-harness.md` for the full protocol.

Use the CLI gatekeeper to enforce structure:

```bash
# Initialize run
python harnesses/falp_strategy_harness.py init --input email.md --out runs/partner_analysis

# Check status anytime
python harnesses/falp_strategy_harness.py status --run runs/partner_analysis

# Reset a phase if needed
python harnesses/falp_strategy_harness.py reset --run runs/partner_analysis --phase 03

# Validate all phases (blocks if incomplete)
python harnesses/falp_strategy_harness.py validate --run runs/partner_analysis

# Create final deliverable (only if validation passes)
python harnesses/falp_strategy_harness.py final --run runs/partner_analysis
```

Forces: context discovery → source lock → actor separation → source ledger → core tools → grill → audit → claim verification → final deliverable.

**Use when:** institutional commitment involved, patient-facing decisions, partner negotiations, conference commitments.

## Tool selection by user intent

Match tools to what the user actually asked for. Do not over-correct toward scoring/gates when the user asked for exploration.

| User intent | Primary artifact | Use these tools | Avoid these tools |
|---|---|---|---|
| "Help me see blind spots" | Perspective Pack | 0 (ledger), source lock, actor sep, perspective pack | Decision matrix, gates, verdict levels |
| "Should we do this?" | Decision memo | Full pipeline (0 → 1 → 2 → 3 → 4 → 6 → 7) | None |
| "What are the risks?" | Risk governance review | 0 (ledger), 2 (stakeholders), 4 (risk), data flow | Gates, verdict levels, perspective pack |
| "Is this pilot ready?" | Pilot readiness map | 0, 2, 3, data flow, claim ledger | Perspective pack (too broad), gates (premature) |
| "What happened in that meeting?" | Decision gates | 0, source lock, 3.5b (gates) | Full pipeline, perspective pack |

**Anti-pattern:** If the user asked for perspective or exploration, do NOT produce a weighted matrix with GO/PAUSE/STOP. More tools ≠ more rigor. The right tool for the right question.

## Sequences by signal type

| Signal type | Sequence | Rationale |
|-------------|----------|-----------|
| **Partner outreach** | 0 → 1 → 2 → 3 → 4 → 6 → 7 | Full pipeline with source discipline |
| **Internal proposal** | 0 → 2 → 3 → 4 → 6 → 7 | Politics known, skip situation read |
| **Opportunity window** | 0 → 1 → 5 → 3 → 6 → 7 | Conference = forcing function |
| **Risk event** | 0 → 4 → 2 → 6 → 7 | Risk first, then politics |
| **Decision pending** | 0 → 1 → 2 → 6 → 7 | Quick read + politics + memo |
| **Political misalignment** | 0 → 2 → 6 → 7 | Just map and write memo |

## Quick start

### Step 0: Context Discovery (mandatory — ask before analyzing)

**Before reading any source or running any tool, ask the user:**

1. **Existing profiles:** "Do you have wiki entries, CRM data, org charts, or notes about the people/institutions involved? Point me to them."
2. **Prior context:** "Has there been previous analysis, meetings, or decisions about this partnership? Where are those notes?"
3. **Key people not mentioned:** "Who else is involved that I might miss from the primary source alone?"

**Why:** The primary source (email, meeting notes) rarely mentions everyone. Missing a key person leads to incomplete stakeholder maps, wrong actor classification, and blind spots. Example: the FALP × Cave case missed Pablo Valenzuela's role (salud digital) because the email only addressed him as a recipient, and his profile existed in a separate wiki (`tqt_app/docs/wiki/ops/07-personas/`).

**What to do with answers:**
- Read every profile/wiki page the user points to
- Add each person/institution to the source evidence ledger with a new source class: `Context (user-provided)`
- Incorporate into actor separation and stakeholder mapping
- If a profile reveals a role that changes the analysis frame (e.g., vendor employee discovered, not external partner), flag immediately

**Gate condition:** If the user says they have profiles but doesn't provide paths, do NOT proceed with analysis. Ask again. Context discovery is prerequisite, not optional.

### Step 1: Phase 1 + Source Ledger (always)

Read `resources/phase-1-quick-assessment.md` then `resources/source-evidence-ledger.md`.

Classify the signal. Classify every source (including user-provided context from Step 0). Then proceed.

### Step 2: Deep Analysis (as needed)

Load only the resources Phase 1 recommends. Each tool is independent.

### Step 5: Grill (mandatory — stress-test findings with user before output)

Before producing final output, grill the user on every assumption, hypothesis, and decision in the analysis.

**Purpose:** The agent's analysis will always have blind spots. The user holds institutional knowledge that no source document contains. Grill forces that knowledge to surface.

**How:**
1. List every hypothesis (not fact) in the analysis
2. For each hypothesis, ask the user: "Is this true? What am I missing?"
3. Walk down each decision branch: "What happens if X fails? What if Y changes?"
4. If a question can be answered by reading existing files/wiki, read them instead of asking
5. Update source ledger, actor separation, and claim ledger based on answers
6. Re-score any affected items

**Pattern:** Adapted from `grill-me` skill (~/.agents/skills/grill-me/SKILL.md). Interview relentlessly until shared understanding.

**Gate condition:** Do not produce final output until all user-identified corrections are incorporated into the analysis.

### Step 6: Output Envelope

Read `resources/output-templates.md` for formatted output structures.

### Step 7: Self-Audit (always before delivery)

Read `resources/strategic-analysis-audit-checklist.md`. Run the 10-point check.

### Step 8: Enforce Envelope

`scripts/enforce-envelope <output_file> --root <project_root>` must exit 0.

### Step 9: Applied Case (reference)

Read `resources/falp-cdli-case.md` for the FALP/CDLI/ElevenLabs partnership as a worked example.

⚠️ **Scope:** The applied case contains real partnership data. Do not load in shared contexts.

## Operating rules

1. **No claims without evidence.** Separate verified facts from inferences from hypotheses. Use the claim ledger.
2. **No overcommitment.** The output must help decide, not create institutional obligations.
3. **Name the clock.** Every strategic situation has a timeline. Find it.
4. **Political realism.** Power is not org-chart position. Map informal influence. Use two layers.
5. **Narrow pilots.** Fast but narrow > comprehensive but stalled.
6. **Honest claims.** Distinguish feasibility from efficacy. Always.
7. **Authority stays with institutional owners.** These skills do not authorize commitments. Clinical, ethical, legal, and technical authority belongs to the corresponding responsible parties. Skills clarify decisions; they do not replace governance.
8. **Source discipline.** Every claim must trace to a source class. Never treat interpretation as fact.
9. **Self-audit before delivery.** Run the audit checklist. Flag unsupported claims. Mark preliminary work as preliminary.
10. **No binary PASS/FAIL.** Use the 4-level verdict system (structural, methodological, factual, institutional).
11. **No data flow = no protocol.** Any pilot involving patient/sensitive data requires a complete data flow diagram before the protocol.
12. **Decision gates after every key meeting.** Convert meeting answers into GO/PAUSE/STOP. Stop gates block phase advancement.
13. **Phase separation is non-negotiable.** Exploration ≠ due diligence ≠ pilot. Never mix phases in a single verdict.
14. **Discarded claims must disappear.** If claim verification killed an inference, it must not appear in conclusions. Mark as "discarded" in the ledger only.
15. **No entity conflation.** When multiple entities converge (person + institution + vendor), each must be analyzed separately. A person is not their employer. An institution is not its representative. A vendor is not a partner institution. If in doubt, split.
16. **Context discovery before analysis.** Always ask the user for existing profiles, wiki entries, meeting notes, or org charts before starting analysis. Primary sources rarely mention everyone involved. Missing a key person creates blind spots that compound through the entire pipeline.
17. **Grill before output.** After completing analysis but before producing final deliverable, grill the user on every hypothesis. Walk down each decision branch. Update analysis with corrections. Never output with untested assumptions when the user is available.

## Cross-cutting quality gates

These apply to every tool output. Each tool also has its own specific quality gates.

- [ ] No claim treated as fact unless in the input
- [ ] Recommendation does not overcommit the institution
- [ ] Implied deadline identified if one exists
- [ ] Next step is operational, not motivational
- [ ] Opportunity separated from proof
- [ ] Patient vulnerability addressed (health contexts)
- [ ] Voice treated as sensitive biometric when applicable
- [ ] Source ledger exists and claims trace to source classes
- [ ] Claim ledger exists with no leakage from discarded claims
- [ ] Audit checklist completed before final delivery
- [ ] 4-level verdict used instead of binary PASS/FAIL
- [ ] Data flow diagram exists if patient/sensitive data involved
- [ ] Decision gates documented if a key meeting occurred
- [ ] Phases separated (no mixing exploration with pilot in single verdict)
- [ ] Source lock gate passed (verbatim quote + IS/IS NOT frame)
- [ ] Actor separation checkpoint passed (no conflation)
- [ ] Tool selection matches user intent (no over-correction)
- [ ] If output envelope required: `scripts/enforce-envelope <output_file> --root <project_root>` exits 0

## Fail-closed conditions

Do not produce a confident final recommendation if:

- No source ledger exists
- The recommendation depends on an unverified conference date
- Patient data is involved but consent/governance is not addressed
- External partner actions are assumed without confirmation
- Institutional approval is implied but not documented
- The proposed pilot is actually a full product in disguise
- A public claim goes beyond available evidence
- Risks have no mitigation or stop condition

Instead: output "Preliminary only — not ready for institutional decision" + list exactly what must be resolved.

---

*Strategic Partnership Toolkit v1.5.1*
*Progressive disclosure architecture*
*16 tools + source ledger + audit checklist + execution harness + grill phase*
*19 resources, 3 harness files, 1 worked case*
