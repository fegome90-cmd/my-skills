# Page Templates

Reusable templates for each wiki page type.

## Concept Page

```markdown
---
title: "Concept Name"
type: concept
tags: [category, subcategory]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["raw/source.txt"]
confidence: medium
---

# Concept Name

## Definition
One-paragraph plain-language definition.

## How It Works
Mechanics, process, or structure.

## Key Parameters
Important variables, dimensions, or factors.

## When To Use
Situations and contexts where this applies.

## Risks & Pitfalls
Known failure modes, common mistakes, limitations.

## Related Concepts
- [[concepts/related-concept]]
- [[entities/related-entity]]

## Sources
- [Source Title](../raw/source.txt)
```

## Entity Page

```markdown
---
title: "Entity Name"
type: entity
tags: [entity-type, category]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["raw/source.txt"]
confidence: medium
---

# Entity Name

## Overview
What this entity is and why it matters.

## Characteristics
Key properties, attributes, structure.

## Common Strategies
Links to concept pages for associated methods:
- [[concepts/strategy-1]]
- [[concepts/strategy-2]]

## Related Entities
- [[entities/related-entity]]
```

## Summary Page

```markdown
---
title: "Summary: Source Title"
type: summary
tags: [summary, source-type]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["raw/source.txt"]
confidence: high
---

# Summary: Source Title

## Key Points
- Main claim or idea 1
- Main claim or idea 2
- Main claim or idea 3

## Relevant Concepts
- [[concepts/concept-1]]
- [[concepts/concept-2]]

## Relevant Entities
- [[entities/entity-1]]

## Source Metadata
- **Type:** Article / Transcript / Book / Notes
- **Author:** Name
- **Date:** YYYY-MM-DD
- **URL/ID:** link or identifier
```

## Synthesis Page

```markdown
---
title: "Synthesis: Topic Comparison"
type: synthesis
tags: [synthesis, comparison]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["raw/source-a.txt", "raw/source-b.txt"]
confidence: medium
---

# Synthesis: Topic Comparison

## Comparison

| Dimension | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Key trait | value | value | value |

## Analysis
Cross-cutting insights from comparing the options.

## Recommendations
When to prefer which approach and why.

## Pages Compared
- [[concepts/concept-a]]
- [[concepts/concept-b]]
- [[entities/entity-a]]
```

## Journal Page

```markdown
---
title: "Journal Entry — YYYY-MM-DD"
type: journal
tags: [journal]
date: YYYY-MM-DD
concepts_used: [concept-1, concept-2]
result: ""
---

# Journal Entry — YYYY-MM-DD

## Setup
What were you investigating?

## Process
Steps taken, decisions, why. Link pages: [[concepts/name]].

## Result
Outcome, what you learned.

## What Went Well
-

## What Could Improve
-
```

## Custom Page Types

Domains may need additional types. Example additions:

| Domain | Custom Type | Directory | Use Case |
|--------|------------|-----------|----------|
| Oncology | disease | `diseases/` | Cancer types with staging, treatment |
| Oncology | treatment | `treatments/` | Drug protocols, MOA, side effects |
| Engineering | component | `components/` | System components and interfaces |
| Research | experiment | `experiments/` | Lab results and methodology |
| Legal | case | `cases/` | Legal precedents and rulings |

Each custom type needs: directory, template, required sections, and index entry.
