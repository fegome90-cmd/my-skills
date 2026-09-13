# Annotation Convention & Diagram Integration

## Visual Cues for Diagrams with Mixed Confidence

When delivering diagrams with elements at different confidence levels, apply visual cues:

| Confidence | SVG/HTML | Mermaid | Description |
|-----------|----------|---------|-------------|
| 🟢 CONFIRMED | Solid border, full color | Normal node style | No disclaimer needed |
| 🟡 INFERRED | `stroke-dasharray="6 3"` | `style "stroke-dasharray: 6 3"` | Dashed border |
| 🟠 ASSUMED | `stroke-dasharray="4 4"` | `style "stroke-dasharray: 4 4"` | Dotted border |
| 🔴 FABRICATED | Red border / strikethrough / `opacity="0.4"` | Remove before delivery | Never deliver |
| ⚪ OUTDATED | Gray / faded / `opacity="0.6"` | Replace before delivery | Fix before delivery |

### Labels

- 🟡 elements: append `(inferido)` to node label
- 🟠 elements: append `(por confirmar)` to node label
- 🔴 elements: replace label with `TBD` or remove entirely
- ⚪ elements: replace with corrected text

### Confidence Legend Block

Add this to any HTML diagram after the audit:

```html
<div style="max-width:900px; margin:1rem auto 0; padding:1rem; background:white; border-radius:8px; box-shadow:0 1px 3px rgba(0,0,0,0.1);">
    <p style="font-size:0.75rem; font-weight:700; color:#0f172a; margin-bottom:0.5rem;">Confidence Legend (diagram-auditor v1.2.0)</p>
    <div style="display:flex; gap:1rem; flex-wrap:wrap; font-size:0.7rem; color:#64748b;">
        <span>🟢 CONFIRMED ({N})</span>
        <span>🟡 INFERRED — dashed border ({N})</span>
        <span>🟠 ASSUMED — dotted border ({N})</span>
        <span>⚪ OUTDATED — faded ({N})</span>
        <span>🔴 FABRICATED ({N})</span>
    </div>
    <p style="font-size:0.65rem; color:#94a3b8; margin-top:0.5rem;">Veredicto: {VERDICT}. {Additional context}</p>
</div>
```

## Wiki Integration

After each audit:

1. Update the diagram page with audit results
2. Add `review_state: draft | reviewed | validated` to frontmatter
3. List open questions in `## Open Questions` section
4. Track corrections in `## Audit Log` section

**Fallback:** If no wiki, save audit report as markdown alongside the diagram (e.g., `voice-banking-flow-audit.md`).

## Embedded Mermaid Extraction

When the diagram is embedded in a Markdown file (```mermaid blocks), extract before auditing.

→ Full patterns and commands: `resources/mermaid-extract.md`
