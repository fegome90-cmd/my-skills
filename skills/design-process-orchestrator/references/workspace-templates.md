# Optional project workspace templates

These are starting points, not required artifacts or universal standards. Use only when the selected mode, project context and explicit write authorization call for them. Do not create four governing documents for a light adjustment; do not create a missing `DESIGN.md` merely to record an audit or decision. Adapt, omit or defer sections that are out of scope, and preserve the project's existing structure and source ownership.

All output paths below are relative to the **project root**. Keep those prefixes when linking from a root-level `DESIGN.md`.

## 1. Optional `PRODUCT.md` — intent and use context

```markdown
# PRODUCT: <Product name>

## Problem and intended outcome
- **Problem:** <friction this work addresses>
- **Outcome:** <intended user/product result>
- **Out of scope:** <only if useful>

## Users and context
- **Primary audience:** <known role/context; mark unknowns>
- **Platforms/locales:** <in-scope environments>
- **Emotional/structural cues:** <optional, grounded in the brief>

## Jobs and critical views (if relevant)
| Job | View / flow | Important action or constraint |
|---|---|---|
| <job> | <route/view> | <context> |
```

## 2. Optional `STACK.md` — project-owned technical decisions

```markdown
# STACK: <Product> (project-owned decisions)

> Record only decisions that are relevant, evidenced and owned by this project.
> A manifest is evidence of declared dependencies, not permission to add or change them.

| Concern | Existing/project-approved choice | Source/owner | Open question or constraint |
|---|---|---|---|
| UI framework | <choice or unknown> | <source> | <constraint> |
| Styling/tokens | <choice or unknown> | <source> | <constraint> |
| Primitives/accessibility | <choice or unknown> | <source> | <constraint> |
| Typography loading | <choice or unknown> | <source> | <constraint> |
| Color/themes | <choice or unknown> | <source> | <constraint> |
| Icons/assets | <choice or unknown> | <source> | <constraint> |
| Motion | <choice or unknown> | <source> | <constraint> |
```

These concerns are examples for documenting relevant context, not seven decisions that every project must lock before design. Do not add dependencies or change a choice without the applicable authorization.

## 3. Optional `CONTEXT.md` — project vocabulary

```markdown
# CONTEXT: <Project vocabulary>

| Canonical term | Meaning in this project | Ambiguity or owner guidance |
|---|---|---|
| <term> | <definition> | <if relevant> |
```

Use the project's existing glossary when one governs. Avoid inventing “prohibited” synonyms unless the domain owner establishes that constraint.

## 4. Optional root `DESIGN.md` — concise index

The links below are relative to the project root. Include only artifacts that exist or are explicitly in scope; remove unused sections instead of implying completion. `DESIGN.md` is not automatically a single source of truth if the project has another authoritative owner/source.

```markdown
# DESIGN: <Product or effort>

## Scope and sources
- **Mode / in-scope work:** <mode and bounded scope>
- **Canonical sources and owners:** <paths and owners>
- **Open conflicts / decisions:** <none, or state what needs resolution>

## Design outputs (include only when applicable)
- Art direction: [`design-system/01-art-direction.md`](design-system/01-art-direction.md)
- Typography selection: [`design-system/02-typography-selection.md`](design-system/02-typography-selection.md)
- Typography scale: [`design-system/03-typography-scales.md`](design-system/03-typography-scales.md)
- Color: [`design-system/04-color-system.md`](design-system/04-color-system.md)
- Layout: [`design-system/05-layout-and-hierarchy.md`](design-system/05-layout-and-hierarchy.md)
- Tokens/components: [`design-system/06-tokens-and-components.md`](design-system/06-tokens-and-components.md)
- Motion/handoff: [`design-system/07-motion-and-handoff.md`](design-system/07-motion-and-handoff.md)
- Tokens: [`design-system/tokens/design-tokens.json`](design-system/tokens/design-tokens.json), [`design-system/tokens/theme.css`](design-system/tokens/theme.css)
- Component references: [`design-system/components/`](design-system/components/)

## Contextual decisions
- **Hero:** <only if in scope; identify the intended protagonist when relevant>
- **Materiality:** <0–2 layers, each justified by product/function/identity; zero is valid>
- **Typography, color and layout:** <selected project-specific decisions, not defaults>
- **Implementation/handoff:** <only if code or an implementation handoff is in scope>

## Coverage and verification
| Domain | Coverage | Method/evidence | Verification |
|---|---|---|---|
| <domain> | <Reviewed / NotReviewed / NotApplicable + reason> | <observed source/result> | <Verified / Failed / NotVerified + method/evidence; use — when coverage is NotApplicable> |
```

If a token tree is used, its format/version and validation basis belong to the project; do not claim a W3C standard or schema conformance without evidence. A local `Brand -> Alias -> Mapped` structure is an architectural choice, not an imposed DTCG requirement. A geometry relation such as `R_ext = R_int + padding` is conditional; check the actual values before claiming it holds.

## Optional phase deliverables

Create only the phase documents needed for the authorized work, using the project's existing naming and layout when present. If these starter paths are chosen, each path remains root-relative under `design-system/`. Token files belong under `design-system/tokens/`; component references belong under `design-system/components/`. Never emit the same output sometimes under `tokens/` and sometimes under `design-system/tokens/`.
