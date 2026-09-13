---
name: diagram-auditor
description: "Use when auditing clinical or technical diagrams against evidence, validating flowcharts before delivery, or classifying diagram elements as confirmed/inferred/fabricated. Triggers: 'audita el diagrama', 'audit this flowchart', 'lint the diagram', 'verifica el diagrama'. Do NOT use for visual design review, diagram generation, or Mermaid syntax-only checks (use mmdc or standalone syntax validator)."
search_hints: diagram audit flowchart evidence validation clinical flujograma audit-assume fabricate confirm stakeholder
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.7.0"
  triggers:
    - "audita el diagrama"
    - "audita el flujograma"
    - "audit this diagram against evidence"
    - "lint the clinical flow diagram"
    - "verifica el diagrama contra lo que sabemos"
    - "audita el diagrama en proceso.md"
  role: specialist
  scope: architecture
---

# Diagram Auditor Skill

Systematic evidence-based audit for diagrams and flowcharts. Every node, label, role, and connection must be classified and validated before delivery.

## Core Principle

**No diagram leaves this session with unverified claims presented as facts.**

## Audit Process (Steps 0–5)

### Step -1: Diagram Generation (when no diagram exists yet)

**Trigger:** Stakeholder provides raw data (transcription, notes, prose) but no diagram.

**Read:** `skills/diagram-maker-plus/SKILL.md`

**Protocol:**
1. Analyze stakeholder data → identify nodes, edges, phases
2. Use diagram-maker-plus to generate Mermaid/SVG/HTML
3. Output goes into Step 0 of this audit pipeline
4. Generated diagrams are always DRAFT — audit is mandatory before delivery

---

## Step 0: Syntax Validation (Mermaid + SVG)

If the diagram source is `.mmd`, `.svg`, or `.html`, validate syntax BEFORE content audit.

**Mermaid:**
1. **Mermaid file (.mmd):** Run `python3 skills/diagram-auditor/scripts/validate_mermaid.py diagram.mmd` (or `mmdc -i diagram.mmd -o /dev/null` if Mermaid CLI is installed)
2. **Embedded in Markdown:** Extract blocks first (→ `resources/mermaid-extract.md`), then validate each

**SVG / Inline SVG in HTML:**
1. **SVG file (.svg):** Parse with `xml.etree` — check well-formedness, extract viewBox, count elements (→ `resources/svg-extract.md`)
2. **HTML with inline SVG:** Extract `<svg>` block via regex, then parse as SVG
3. **No text elements found:** SYNTAX-FAIL (image-only SVG, no extractable labels)

**Non-Mermaid, non-SVG (prose, image):** Skip Step 0. Add note: "No syntax validation performed."

**Results:** Syntax OK → Step 0.5 | Syntax FAIL → SYNTAX-FAIL, skip content audit | Tools unavailable → skip, add warning

### Step 0.5: Check Prior Audits (Memory)

1. Run `memory_search("audit diagram {diagram-name}")` for prior audits
2. If found → show prior verdict, delta comparison, highlight changes
3. If not found → proceed normally
4. If memory unavailable → skip, add note to report

### Step 1: Inventory — Extract Every Claim

Parse the diagram and extract every discrete claim. For each element: node label, assigned role, process description, connections.

**For SVG sources:** Use automated extraction (→ `resources/svg-extract.md`) to produce deterministic inventory from `<text>`, `<title>`, and container elements. This replaces ad-hoc visual interpretation.

**For Mermaid sources:** Parse Mermaid syntax to extract node IDs, labels, and edges.

**For prose/descriptions:** Manual extraction from text.

Output: flat list `ELEMENT-01, ELEMENT-02, ... ELEMENT-N`

### Step 2: Classify Each Element

| Tag | Symbol | Meaning | Action |
|-----|--------|---------|--------|
| **CONFIRMED** | 🟢 | Stated by stakeholder or official docs | Keep as-is |
| **INFERRED** | 🟡 | Reasonable assumption, not verified | Flag for confirmation |
| **ASSUMED** | 🟠 | Plausible guess, no evidence | Mark clearly, ask before delivery |
| **FABRICATED** | 🔴 | Invented by agent, no basis | Remove or replace with "TBD" |
| **OUTDATED** | ⚪ | Was true but stakeholder corrected | Replace with corrected version |

### Step 3: Evidence Mapping

For each element, document: tag, source, confidence, action, correction. → See `resources/audit-report-template.md` for full format.

### Step 3.1: Evidence Enrichment

For elements tagged 🟡 INFERRED or 🟠 ASSUMED, query external evidence sources to attempt tag upgrades.

→ Full protocol: `resources/evidence-sources.md`

**Summary:** Query PubMed/Papers MCP in priority order. If evidence found with confidence ≥ 0.7 → upgrade to 🟢. If < 0.7 → upgrade to 🟡. If not found → keep tag, add to grill questions. 🔴 FABRICATED never auto-upgrades.

### Step 3.5: Scope Selection

- **Full audit (Steps 1–5 + grill):** >5 elements or stakeholder-facing delivery
- **Quick audit (Steps 1–2 + verdict):** ≤5 elements or internal drafts

### Step 4: Generate Audit Report

Produce structured report with verdict, tag summary, findings by severity, and questions for stakeholders. Persist via `memory_save`.

→ Full template: `resources/audit-report-template.md`

### Step 4.5: Grill Phase (when stakeholder present)

If the stakeholder is available in the session, **resolve questions interactively** before Step 5.

→ Full protocol: `resources/grill-phase.md`

**Summary:** For each non-🟢 element, ask the stakeholder. Reclassify based on answers. Re-calculate verdict. Skip if no stakeholder present.

**UX Validation Extension:** For stakeholder-facing diagrams, perform UX validation to:
- Validate diagram clarity with target audience
- Check information hierarchy matches stakeholder mental model
- Identify cognitive load issues (too many nodes, ambiguous labels)
- Produce recommendations before Step 5 fixes

### Step 5: Fix or Flag

- **🔴 FABRICATED** → Replace with `TBD` or remove. Never deliver.
- **⚪ OUTDATED** → Apply correction immediately.
- **🟠 ASSUMED** → Add `(por confirmar)` label, or replace with `TBD`.
- **🟡 INFERRED** → Add `(inferido)` label.
- **🟢 CONFIRMED** → Keep as-is.

Apply visual cues to the diagram source. → See `resources/annotation-convention.md`

### Step 5.5: Wiki Sync

Persist audit results to the wiki for durability.

→ Full protocol: `resources/wiki-sync.md`

**Summary:** Update diagram page frontmatter with audit metadata. Append audit log entry. Detect orphan references from removed 🔴 elements.

## Step 6: Batch Audit (optional)

When auditing multiple diagrams in one session (thesis, wiki, project review), use batch mode.

→ Full protocol: `resources/batch-mode.md`

**Summary:** Glob → individual audit per diagram → cross-diagram consistency check → aggregate rollup report.

## Step 5.8: Design Polish (for HTML/SVG diagrams)

After audit fixes are applied, apply the design polish checklist to ensure presentation quality.

**Trigger:** Output is `.html` or `.svg` AND diagram will be shown to stakeholders.

**Apply these checks to the diagram:**

1. **Design Direction** — Personality right for audience? (medical = Sophistication & Trust)
2. **Color for Meaning Only** — Gray builds structure? Accent for one semantic meaning only?
3. **4px Grid** — All spacing on grid? Symmetrical padding?
4. **Contrast Hierarchy** — 4 levels (foreground → secondary → muted → faint) consistent?
5. **Typography** — System fonts? Headlines 600? Monospace for data/PMID?
6. **Border Radius** — Consistent system (not mixing sharp and soft)?
7. **Depth Strategy** — One approach only (not mixed)?
8. **Anti-patterns** — No thick borders (>1.2px)? No gradients? No asymmetric padding?
9. **Dark Mode** — CSS media query inverts correctly?
10. **Print** — White background, no decorative color?

**If checks fail:** Fix in-place before delivery. Clinically accurate + bad design = undermined credibility.

---

## Verdict Table

| Verdict | Condition |
|---------|-----------|
| **SYNTAX-FAIL** | Mermaid syntax invalid (Step 0) |
| **PASS** | All elements 🟢 → deliverable |
| **PASS-WITH-WARNINGS** | 🟢 + 🟡 only → deliverable with caveats |
| **FAIL** | ≥20% elements 🔴 or 🟠 → not deliverable |

## Rules

1. **Never deliver unvalidated.** Drafts with explicit "DRAFT — not validated" disclaimers are OK for review.
2. **Every role must have a source.** Unknown roles → "TBD", not a guess.
3. **Every step verified against stakeholder or docs.** Not "how it usually works" — how it works HERE.
4. **>50% elements 🟡 or worse → DRAFT** (configurable, default 50%).
5. **Stakeholder corrections = 🟢 immediately.**
6. **Register audit results in project wiki.**
7. **Persist audit state.** `memory_save` type `pattern`, topic_key `audit/diagram-{name}`.

## When Not to Use

- **Visual design review** → use UI/UX skills instead
- **Diagram generation** → this skill audits, does not create (use `diagram-maker-plus`)
- **Mermaid syntax-only checks** → use `scripts/validate_mermaid.py` or Mermaid CLI directly
- **Code flow analysis** → use `authority-flow-audit` or code review workflows

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Diagram source | Yes | `.mmd` file, embedded Mermaid in `.md`, SVG/HTML, or prose description |
| Stakeholder (user) | No | If present → Step 4.5 Grill Phase activates for interactive resolution |
| Prior audit | Auto | Skill checks `memory_search` for previous audits of same diagram |

## Step 7: Stakeholder Deck (optional)

**Trigger:** Diagram needs to be presented in a formal meeting (board, committee, external partner).

**Read:** `skills/scripting-technical-presentations/SKILL.md`

**Protocol:**
1. Build structured deck using 10-20-30 framework + Pyramid Principle
2. Diagram becomes one or more slides with context
3. Include: purpose, audience analysis, evidence summary, key decisions, next steps
4. Deck follows Duarte storytelling arc

---

## Resources

| File | Purpose | When to Load |
|------|---------|-------------|
| `scripts/validate_mermaid.py` | Standalone Mermaid syntax validator | Step 0 |
| `resources/audit-report-template.md` | Full report template + memory_save format | Step 4 |
| `resources/grill-phase.md` | Interactive stakeholder interrogation protocol | Step 4.5 |
| `resources/annotation-convention.md` | Visual cues (SVG/Mermaid) + wiki integration | Step 5 |
| `resources/example-clinical-audit.md` | Complete clinical nutrition referral audit example | On demand |
| `resources/mermaid-extract.md` | Extraction patterns for embedded Mermaid blocks | Step 0 |
| `resources/svg-extract.md` | Automated SVG element extraction (nodes, connectors, validation) | Step 0-1 |
| `resources/batch-mode.md` | Multi-diagram audit with cross-diagram consistency | Step 6 |
| `resources/evidence-sources.md` | External evidence adapters (PubMed, Papers MCP) for tag upgrades | Step 3.1 |
| `resources/wiki-sync.md` | Persist audit results to wiki + orphan detection | Step 5.5 |
| `skills/diagram-maker-plus/SKILL.md` | Diagram generation from raw data | Step -1 |

## Key Distinctions

| Confusion | diagram-auditor | The other thing |
|-----------|----------------|-----------------|
| Audit vs Review | Classifies evidence quality (🟢🟡🟠🔴⚪) | Review checks style/patterns |
| Audit vs Generation | Audits existing diagrams | Generation creates new ones |
| Syntax vs Content | Step 0 validates Mermaid syntax | Steps 1-5 audit factual accuracy |
| Grill vs Ask | Step 4.5 resolves questions interactively | Step 4 generates questions passively |
| DRAFT vs FAIL | DRAFT = >50% unconfirmed (still useful) | FAIL = ≥20% fabricated/assumed (not deliverable) |

---

## Testing

```bash
pytest skills/diagram-auditor/tests/test_diagram_auditor.py -v
```

Covers: Mermaid extraction, SVG parsing, element inventory, verdict calculation, inline SVG in HTML, edge cases (empty, single node, nested fences, malformed SVG).

**Version:** 1.7.0
**Created:** 2026-05-27
**Updated:** 2026-06-02
**Author:** Felipe Gonzalez
**Status:** Active
**Changelog:**
- v1.5.0 — Autoresearch third pass. Added evidence enrichment (Step 3.1 with PubMed/Papers MCP adapters) + wiki sync (Step 5.5 with frontmatter + audit log + orphan detection). +13 tests (36 total).
- v1.4.0 — Autoresearch second pass. Added batch mode + test suite (23 tests). Cross-diagram consistency checking.
- v1.3.0 — Added SVG extraction engine. Step 0 validates SVG. Step 1 uses automated extraction.
- v1.2.0 — Progressive disclosure refactor. Added Step 4.5 Grill Phase. Split into resources/.
- v1.1.0 — Step 0 (syntax validation), Step 0.5 (memory), persistence, embedded extraction, example
- v1.0.0 — Initial release
