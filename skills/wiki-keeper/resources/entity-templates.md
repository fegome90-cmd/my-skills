# Entity Templates

Templates for the optional `entities/` directory. Use for typed knowledge about people, tools, decisions, meetings, and external concepts.

## Person

```yaml
---
type: entity
entity-type: person
tags: [role, domain]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
name: Full Name
role: e.g. "Tech Lead", "Researcher"
org: Organization name
contact:
  email: optional
  url: optional
notes: >
  Brief context about this person's relevance
  to the wiki's domain.
---

# Person Name

Summary of who this person is and why they're relevant.

## Role & Expertise

Key areas of expertise, responsibilities.

## Contributions

Notable contributions to the domain, projects, or decisions documented in this wiki.

## See Also

- [[related-page]]
```

## Tool

```yaml
---
type: entity
entity-type: tool
tags: [category, language]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
name: Tool Name
url: https://example.com
version: x.y.z
license: MIT
purpose: >
  What this tool does and when to use it.
notes: >
  Integration notes, gotchas, alternatives.
---

# Tool Name

One-line description of the tool.

## Overview

What it does, why it exists, core value prop.

## Setup & Configuration

Key setup steps, config files, environment variables.

## Usage Patterns

Common usage patterns relevant to this wiki's domain.

## Alternatives

| Tool | Trade-off vs This Tool |
|------|----------------------|
| alt  | ... |

## See Also

- [[related-page]]
```

## Decision

```yaml
---
type: entity
entity-type: decision
tags: [domain, scope]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
title: Short Decision Title
decision-date: YYYY-MM-DD
deciders:
  - Person A
  - Person B
context: >
  What situation required this decision.
options-considered:
  - Option A: brief
  - Option B: brief
outcome: What was chosen and why.
consequences: >
  Known trade-offs, follow-up decisions needed.
---

# Decision: Short Title

## Context

Why this decision was needed.

## Options Considered

### Option A
Pros / cons.

### Option B
Pros / cons.

## Decision

What was chosen and the rationale.

## Consequences

Trade-offs accepted, risks, follow-ups.

## See Also

- [[related-page]]
```

## Meeting

```yaml
---
type: entity
entity-type: meeting
tags: [topic, format]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
title: Meeting Title
date: YYYY-MM-DD
participants:
  - Person A
  - Person B
action-items:
  - "[ ] Task description — assignee — due date"
summary: >
  Key outcomes and decisions from the meeting.
---

# Meeting: Title

## Summary

Key discussion points and outcomes.

## Action Items

- [ ] Task — assignee — due
- [ ] Task — assignee — due

## Decisions Made

Links to Decision entities if applicable.

## See Also

- [[related-page]]
```

## Concept (External)

```yaml
---
type: entity
entity-type: concept-external
tags: [domain, field]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
name: Concept Name
source-url: https://example.com/paper
domain: e.g. "Machine Learning", "Systems Design"
related-wiki-pages:
  - "[[internal-page]]"
notes: >
  Why this external concept is relevant to the wiki.
---

# Concept Name

One-line description.

## Overview

What the concept is, where it comes from.

## Key Ideas

Core principles or mechanisms.

## Relevance

Why this matters for this wiki's domain.

## References

- [Source Title](url)

## See Also

- [[related-page]]
```
