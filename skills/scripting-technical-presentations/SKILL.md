---
name: scripting-technical-presentations
description: "Use when drafting or auditing technical presentation scripts, speaker notes, or slide outlines while preserving evidence, limits, and audience decisions."
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
---

# Technical Presentation Scripting

## Activation Contract

Use only to create, restructure, or audit technical-presentation scripts, speaker notes, and slide outlines. Establish audience, intended outcome, timing, source evidence, and either the decision/proposal or the framing decisional question/hypothesis (for research and incident postmortems, avoid premature conclusion bias) before drafting. Ask one high-impact question only when a missing fact prevents a faithful result; otherwise state bounded assumptions.

## Hard Rules

- Preserve evidence, uncertainty, limitations, confidentiality, and causal boundaries.
- For research and incident reviews, frame around the investigable hypothesis or postmortem timeline/causal question rather than a preselected conclusion.
- Exclude by default source code, `src/`, `deck.yml`, `compiled-deck.json`, rendering, pipelines, and compiled artifacts.
- Do not turn slides into a teleprompter or use narrative drama to replace evidence.
- Keep one defensible thesis or central question; distinguish observation, inference, hypothesis, recommendation, and projection.
- Protect identity and dignity in clinical, safety, and incident material.

## Decision Gates

| Need | Choose |
| --- | --- |
| Audience must learn a model | conceptual-change pattern |
| Audience must assess research | research pattern (frame central hypothesis & methodology) |
| Audience must decide | technical-decision pattern (frame proposal & tradeoffs) |
| Audience must examine a failure | incident pattern (frame causal timeline & systemic learning) |
| Audience must observe a solution | demonstration pattern |

Use `references/narrative-patterns.md` only when selecting or combining a pattern.

## Execution Steps

1. Write a complete thesis, or formulate the decisive question / hypothesis with its evidence and limits.
2. Order the reasoning: current model or problem, question, discriminating evidence, alternatives, conclusion/findings, uncertainty, and implication.
3. Create a timed beat sheet: block, claim, evidence, visual support, transition, and duration.
4. Draft spoken language as speaker notes; give each slide outline one cognitive task and a conclusion-style heading.
5. Cut known background, redundant examples, and non-decisive detail before cutting the thesis, decisive evidence, or limits.

## Output Contract

Return only the requested script, notes, outline, or audit. For a full package, provide audience brief, thesis, selected pattern, timed beat sheet, speaker notes, slide outline, evidence-and-uncertainty register, and likely questions. Do not create or modify presentation source, render outputs, or build artifacts.

## References

- `references/narrative-patterns.md` — pattern selection and guardrails.
- `references/evaluation-scenarios.md` — maintainer-only evaluation reference; not runtime instructions.
