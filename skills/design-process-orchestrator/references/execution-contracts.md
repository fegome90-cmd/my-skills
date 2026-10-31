# Execution contracts and coordination reference

## Role and operating boundaries

The orchestrator routes, sequences and consolidates work. The relevant specialist owns domain-specific rules and judgments; the project and its harness own their documents, decisions and capabilities. Do not restate a specialist's detailed checklist as an orchestrator gate, create a parallel review authority, or install a missing specialist from memory. Continue independent work when a specialist is absent; mark that domain `NotReviewed` and block only dependent results.

This contract is harness-agnostic. Use capabilities and tools that are actually available and discovered in the active environment. Figma MCP, a proprietary CLI, a browser, two harnesses, or any particular runtime are not prerequisites. A missing capability limits what can be verified; it does not itself prove a defect. Respect the host agent's workflow and gates (for example, Gentle); do not duplicate or replace them.

## Mode contracts

Choose the smallest mode that satisfies the explicit request. Report the preconditions, scope, dependencies, permitted outputs and writes before work. A mode never grants permission broader than the user's request or project authority.

| Mode | Preconditions | Work and outputs | Writes |
|---|---|---|---|
| **Greenfield** | Explicit intent to create a design system/product direction from zero; scope and any consequential missing choices are clear or resolved. A new repository alone is not intent. | Plan only requested/in-scope specialist stages; declare prerequisites and gates. Offer scaffolding only where useful and authorized; do not imply every artifact or test is required. | Only artifacts explicitly requested or authorized. Optional governing docs and design-system artifacts may be scaffolded when in scope; no automatic four-document requirement. |
| **Subgraph** | Request names or clearly implies a bounded set of stages in an existing or new effort. | Consult relevant existing prerequisites, declare selected stages and dependencies, and report omitted stages separately. A missing prerequisite becomes a surfaced dependency/conflict, not permission to overwrite it. | Only authorized outputs for selected stages; do not scaffold unrelated stages. |
| **Lightweight** | Bounded adjustment or one/few related dimensions in an existing project. | Inspect only relevant canonical sources, route to the needed specialist(s), and return the decision/result. A request touching three nodes does not by itself become Greenfield or a full pipeline. | No four-document scaffolding and no creation of a missing `DESIGN.md`. Record the response in the handoff; update an existing relevant document only when that write is authorized. |
| **Audit** | Explicit request to inspect or report findings on an existing design/interface/system. | Read relevant sources and report observations, coverage, evidence, limits and proposed fixes separately. Do not treat a finding as permission to fix it. | Read-only: no project/source/document edits or generated artifacts. Any later fix requires a separate authorized task. |
| **Refactor** | Explicit authorization to change existing structure/content, with scope and writable surfaces clear. | Plan changes against canonical sources and specialist ownership; unresolved conflicts pause only the affected work. | Only authorized files/areas. An audit request, suggestion, or inferred technical benefit is not refactor permission. Ask before writing if authorization or scope is ambiguous. |

If intent, source authority, or write permission is ambiguous in a way that changes the plan, stop that affected work and ask a concrete question. Do not guess, silently resolve conflicts, or overwrite the source that disagrees.

## Sources, routing and dependencies

1. Identify the project's root/index and relevant canonical documents, their owners, applicable constraints, and existing capabilities. The presence of a package manifest does not approve a dependency or make it canonical.
2. Reuse the owner's source and existing capabilities first. For an implementation need, consider in order: eliminate, use a native capability, reuse, correct an existing choice, then add. Justify an addition; never impose a preference for Redux, Axios, Figma, or another library/tool without project evidence and authorization.
3. Route only requested domains to specialists. Declare actual prerequisites/dependencies for a subgraph; do not turn a prompt's node count into a mode rule. Preserve domain ownership rather than copying detailed specialist rules into the orchestration checklist.
4. When a proposal conflicts with an existing source, cite the source and conflict and ask the responsible person to resolve it. Do not automatically edit the source, stack, tools, dependencies, or prior design decision.
5. A design-only task does not require code architecture/API/flow/test or dependency checks. If code is in scope, consult project sources for relevant layers, public APIs, affected flows, pertinent tests, and lifecycle/status of libraries. Evaluate a dependency only when one is under consideration. Distinguish observed evidence from estimates.

## Coverage, verification and gate reporting

Coverage and behavior verification are independent dimensions. Report only gates relevant to the scope: there is no mandatory set of eight gates or eight `PASS` results. For each relevant gate/domain, report owner/specialist, source consulted, coverage, method, evidence and verification state. Use a compact table if useful:

| Domain / owner | Source and method | Coverage | Evidence | Verification |
|---|---|---|---|---|
| `<domain>` | `<source; inspection/test/tool>` | `Reviewed`, `NotReviewed`, or `NotApplicable (reason)` | `<observed artifact/result>` | `Verified`, `Failed`, or `NotVerified` with method/evidence; use `—` when coverage is `NotApplicable` and state why |

- `NotReviewed` means no review coverage; it is never a pass. `NotApplicable` requires a reason tied to scope/platform.
- `Verified` requires observed evidence for the stated behavior and method. Static instruction/source inspection does not prove runtime behavior. With no browser, visual behavior is `NotVerified`; do not claim rendering was checked.
- An absent specialist leaves its domain `NotReviewed`; continue independent domains and block results that depend on it. State the blocked dependency and what evidence/capability is missing.
- An omitted stage is not an approved stage. Never mark omitted gates `PASS`, conceal omissions in an aggregate, or turn partial results into global approval. Report failures and limitations as observed; a review is not release authorization.

## Contextual quality and proportional checks

Apply controls only when relevant to request, content, platform, supported locales and evidence. A non-applicable check is reported with its reason, not silently claimed complete. Do not create an extra universal “stage 7” for these concerns.

- **Visual direction:** Ground decisions in the brief and existing brand/product constraints. A hero is only in scope if the request includes one; then identify its protagonist. Materiality is optional: default to zero layers when they do not serve the product; allow zero to two justified layers. Do not require two layers, a hero, a fixed motif count, grid preset, ratio, or aesthetic. Treat materiality, proportions, and layout presets as contextual heuristics, not defects by themselves.
- **Content and internationalization:** When applicable, consider copy, locale/plural behavior, long or non-Latin text, truncation and recovery, zoom/text spacing and RTL only for supported locales/platforms and relevant components. Do not require all of them for every task.
- **States and interaction:** Check reachable states and hostile inputs when pertinent to the in-scope component/flow. Test only available, authorized methods; distinguish source review from exercised interaction. Keep required accessibility criteria and conformance levels accurate, and do not infer conformance from a checklist.
- **Implementation handoff:** Only when code is included, pass along relevant architecture, public API, affected flow, library lifecycle and test context from project sources. Do not prescribe a testing framework or assert performance without measurement.

## Canonical project artifact paths

When the project authorizes these deliverables, resolve generated paths from the **project root**, not from this skill's directory or the current working directory:

- Root-level optional indexes/governance: `PRODUCT.md`, `STACK.md`, `CONTEXT.md`, `DESIGN.md`.
- Phase notes: `design-system/01-art-direction.md` through `design-system/07-motion-and-handoff.md`, only for in-scope phases.
- Tokens: `design-system/tokens/design-tokens.json`, `design-system/tokens/theme.css`.
- Component references: `design-system/components/CRD-<ComponentName>.md`.

Four root documents are optional project artifacts, not universal prerequisites. Do not create them just because a task is light or an audit occurred. If a root `DESIGN.md` index is authorized, its links to token/component artifacts must be `design-system/tokens/...` and `design-system/components/...`. Do not silently replace a project's existing index or document layout.

## Technical lineage and references

Preserve the original technical references and their attribution when they are useful to the requested work. These are frameworks/inspirations, not universal acceptance criteria or proof of compliance:

- Prompt Graph Engineering (PGE): Sandeco Macedo; modular coordination and anti-drift framing.
- Art direction: Brandon Sanderson's “Star of the Show” framing and visual rhyming; use only when a hero/direction is in scope.
- Typography: Oliver Schöndorfer's “Font Follows Feeling / Function”, Massimo Vignelli's pairing canon, and the MEGATYPOS specimen.
- Type scale and microtype: Chris Misterek's letter-spacing triad and Matthew Butterick's measure/readability guidance; values remain contextual, not tests by themselves.
- Color and interaction: Rex Hartson and Pardha Pyla's grayscale-first, color/interaction framing; applicable accessibility claims require the relevant actual pair/state and evidence.
- Layout: Gestalt principles, the Squint Test, pattern catalogs, 12-8-4 grids and 8-point spacing are selectable methods/presets, not mandates.
- Tokens/components: DTCG is the Design Tokens Community Group format; Brand/Alias/Mapped is a local architecture choice, not a W3C-mandated three-layer model. State a format version and validate against a selected schema before claiming conformance.
- Motion/handoff: Emil Kowalski's motion principles, Hartson and Pyla's interaction-cycle framing, Widget-First and anti-slop distillation are attributed methods. Prefer suitable compositor-friendly properties while allowing contextual exceptions; do not claim FPS/performance without measurement.

Do not turn OKF-170 or any comparative skill/source into universal authority, require the three OKF documents, or impose another author's aesthetic values. For this suite, the owner has declared authorship and explicitly selected MIT; the terms travel with each skill in its [bundled licence](../LICENSE). The suite-level PROVENANCE.md records that declaration but is not a runtime dependency of a standalone skill. This is not independent authentication and does not relicense referenced third-party assets. For other sources whose provenance is missing, report the gap instead of inventing metadata or permissions. Legal rights under MIT are separate from the operator's permission for this agent to install, register, promote or publish; perform those operational actions only when expressly authorised.
