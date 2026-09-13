# DESIGN.md — Plannotator B2 ↔ Open Design Live Pipeline

Guía de diseño y contrato de edición para agentes que trabajen sobre este proyecto.
Artefacto canónico: `index.html` (plan de arquitectura interactivo, es-ES, 1 archivo standalone).

## 1. Qué es este proyecto

Un diagrama de arquitectura de un ciclo de revisión anotable: **Plannotator B2** (anotación humana)
↔ **Open Design** (motor de diseño vivo), con un **Adapter W3C** de normalización. No es un sitio web:
es un *plan de arquitectura* presentado como panel de control interactivo — 26 componentes con
contrato `data-review-id`, 4 pestañas, conectores animados y quality gates.

- `index.html` — artefacto canónico (≈1570 líneas: tokens + CSS ≈1000, HTML + sprite + JS).
- `index-v2.html` — copia de seguridad de una revisión previa. **No editar como fuente.**
- `_ctx/telemetry/` — telemetría de runs del daemon. Datos, no diseño.

## 2. Design system: Stripe (tema oscuro)

El sistema es **Inspired by Stripe** (`design-systems/stripe`) con un **tema oscuro override**
propio. Los tokens viven en tres bloques `:root` del `<style>` inicial, en este orden:

1. **Línea 15** — `:root` de `tokens.css` del sistema Stripe, copiado **verbatim** (no reescribir,
   no añadir hex nuevos fuera de él).
2. **Línea 255** — override de tema oscuro (el canvas real del artefacto).
3. **Línea 997** — `@media print` que re-enlaza a claro (el plan se imprime en light).

### Paleta oscura (override, línea 255)

| Token | Valor | Rol |
|---|---|---|
| `--bg` | `color-mix(in oklab, #0d253d 72%, #04060d 28%)` | canvas (navy profundo) |
| `--surface` | `color-mix(in oklab, #1c1e54 30%, #0c1322 70%)` | superficie tarjetas |
| `--surface-warm` | `color-mix(in oklab, #1c1e54 18%, #111a30 82%)` | paneles anidados, labels de conector |
| `--fg` | `color-mix(in oklab, #ffffff 96%, #b9b9f9 4%)` | texto principal (navy→casi blanco con tinte violeta) |
| `--muted` | `#94a3b8` | texto secundario |
| `--meta` | `#64748d` | metadatos |
| `--border` | `color-mix(in oklab, #64748d 34%, transparent 66%)` | bordes |
| `--accent` | `#533afd` (heredado de Stripe) | CTA, foco, nodos de conector, selección |
| `--panel` / `--panel-raised` / `--panel-hover` | mezclas de `--surface` con `#533afd` | superficies de `.comp` |
| `--ok` / `--warn` / `--danger` / `--pending` | `#34d399` / `#fbbf24` / `#f87171` / `#94a3b8` + `--*-bg` al 14% | badges de estado |
| `--shadow-sm` / `--shadow-md` | `rgba(0,0,0,.35/.45)` | elevación |

**Regla de oro:** toda edición usa `var(--…)` o `color-mix(in oklab, …)`; **cero hex nuevos**
fuera de los bloques de tokens citados. El comentario `#stripe N` del token original se conserva.

### Tipografía

- `--font-display` / `--font-body`: `sohne-var → Söhne → SF Pro Display → system`. **`font-feature-settings: "ss01"` en todo texto**; weight 300 en headings y body; 400 en botones/labels.
- `--font-mono`: `SourceCodePro` para `code`/`pre`.
- Escala: hero `clamp(2.1rem, 5vw, var(--text-4xl))` con `-0.025em` tracking; subtítulo `var(--text-lg)` muted; títulos de card `var(--text-xl)` (22px) weight 300; body 16px weight 300.
- Números tabulares (`font-variant-numeric: tabular-nums`) solo en datos (badges).

### Radios, sombras, movimiento

- Radius: `--radius-sm` 4px (botones, badges, comps), `--radius-md` 6px (nav, connector-label), `--radius-lg` 8px (cards). **Nunca pill** en superficies interactivas.
- Sombras: `--elev-raised` (multi-capa azulada Stripe) en hover de cards; `--elev-deep` en hover de comps; `--focus-ring` (halo púrpura) en `:focus-visible`.
- Motion: `--motion-fast` 150ms / `--motion-base` 200ms / `--ease-standard`; hover solo cambia color/sombra/transform suave, nunca escala ni nudge agresivo; `riseIn` 520ms con `--d` de stagger para entradas.

## 3. Estructura del documento

```
<body>
  <svg class="sprite">   ← 17 <symbol> (íconos Feather 24×24, stroke 1.7, round)
  <div class="container">
    <header data-od-id="page-header">      badge-top + h1 + .subtitle
    <nav class="tabs-nav" data-od-id="tabs-nav" role="tablist">
      .tab-indicator#tab-indicator  +  4 × button.tab-btn[role=tab]
    <section#tab-system.tab-pane.active data-od-id="tab-architecture">   ← Fase 1/3 + Gates
    <section#tab-loop.tab-pane data-od-id="tab-loop">                    ← 3 pasos del ciclo
    <section#tab-matrix.tab-pane data-od-id="tab-matrix">                ← M1–M6 matrix + error boundary
    <section#tab-roadmap.tab-pane data-od-id="tab-roadmap">              ← Fases 1–3 roadmap
    <footer data-od-id="page-footer">
  </div>
  <div id="tooltip" class="tooltip-bubble" role="status" aria-live="polite">
  <script>                                                              ← tabs, tooltip, a11y
```

Dentro de cada pane: `div.grid-2`/`grid-3` > `div.card` > `.card-title` (`.card-title-label` + `.badge`) > lista de `.comp`.

## 4. Componentes

### `.card`
Superficie con `linear-gradient(180deg, white 4%, transparent)` sobre `--surface`, borde `--border`,
radius `--radius-lg`, hover: `translateY(-3px)` + `--elev-raised` + línea superior `#b9b9f9` al 70%.

### `.comp` — el componente de revisión (contrato crítico)

```html
<div class="comp c-antigravity" data-review-id="comp.antigravity-authoring" data-tip="…">
  <div class="comp-header">
    <span class="comp-title"><svg class="comp-icon" aria-hidden="true" width="16" height="16"><use href="#icon-cpu"/></svg>Antigravity Orchestrator</span>
    <span class="badge badge-ok">Ready</span>   <!-- o .comp-id-tag -->
  </div>
  <p class="comp-desc">…</p>
</div>
```

- **`data-review-id`**: identificador único, formato `comp.<dominio>-<nombre>`. **Invariante 1:1** con `.comp` (ver §7).
- **`data-tip`**: texto del tooltip; el JS lo expone a lectores de pantalla vía `aria-describedby="tooltip"` y añade `tabindex="0"`.
- **Clases de rol** → `--comp-color` (el color del rol vive en la **línea superior de gradiente** `.comp::before`, siempre visible al 55% de opacidad, refuerzo al hover; el icono y el id-tag comparten el tono):

| Clase | Color | Rol |
|---|---|---|
| `c-antigravity` | `--color-antigravity` `#60a5fa` azul | orquestador / agentes LLM |
| `c-plannotator` | `--color-plannotator` `#f472b6` rosa | superficie de anotación humana |
| `c-adapter` | `--color-adapter` `#fbbf24` ámbar | normalizador B2 |
| `c-opendesign` | `--color-opendesign` `#34d399` esmeralda | motor live |
| `c-danger` | `--danger` `#f87171` rojo | error boundary |

- Hover: `--panel-hover`, borde teñido del rol, `translateY(-2px)`, sombra con `color-mix` del rol. `:active` comprime. `:focus-visible` → `--focus-ring`.
- **Anti-slop vigente:** NO volver a "tarjeta redondeada + borde lateral de color". El color es la línea superior + icono + id-tag.

### `.badge` y estados
`.badge-ok` / `-warn` / `-danger` / `-pending` — bg `--*-bg` (14% alpha), texto del tono, borde al 36%,
uppercase 0.7rem tabular-nums. Uso: estado real del componente ("Ready", "Tested (24/24 PASS)", "Strict DoD").

### `.flow-connector`
Rail animado entre grupos: `--connector-line` (línea animada con gradiente `--accent`), `.connector-node`
(círculo `--accent` con anillo pulsante `nodePulse`), `.connector-label` (chip `--surface-warm` con
`.connector-arrow` `<use href="#icon-arrow-down">` 14px). Hover del rail acelera la línea (0.9s) y escala los nodos (1.3).
En móvil se oculta la línea y el label permite salto de línea.

## 5. Sistema de iconos (sprite)

- **17 `<symbol>`** al inicio del `<body>` (`.sprite`), Feather-style: `viewBox 0 0 24 24`,
  `fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"`.
- Catálogo: `icon-layers refresh-cw grid flag arrow-down cpu server message repeat zap check shield alert-triangle file-text database link edit`.
- Consumo **solo vía `<use href="#icon-…">`** — nunca paths sueltos fuera del sprite.
- Tamaños por contexto: `.comp-icon` 16px (coloreado `var(--comp-color)` del rol), `.card-title-icon` 18px (`--muted`), `.connector-arrow` 14px, iconos de tab 16px.
- Añadir icono nuevo = nuevo `<symbol>` en el sprite + `<use>`; stroke unificado 1.7.

## 6. Interacción y accesibilidad (JS)

- **Tabs**: `role=tablist`/`tab`/`tabpanel` con **roving tabindex** (solo el activo en la secuencia de Tab),
  flechas ←/→ para moverse, `aria-selected`, `.tab-indicator` animado que sigue al activo, re-posicionado en `resize`.
  `staggerCards()` asigna `--d` (0–540ms, paso 45ms) a cards y comps del pane activo.
- **Tooltip**: un único `#tooltip` `role=status aria-live=polite`; se muestra en `mouseenter`/`focus` de
  `.comp[data-tip]` y se posiciona centrado arriba del elemento (abajo si no cabe), con clamp a los bordes.
- **A11y de lectura**: todo `pre` recibe `tabindex="0"` (scroll horizontal operable con teclado);
  todo `.comp[data-tip]` recibe `tabindex="0"` + `aria-describedby="tooltip"`.
- **`prefers-reduced-motion: reduce`**: animaciones y transiciones a ~0ms.
- **Print**: reinicia `:root` a claro, fondo blanco, y los 4 paneles se imprimen en secuencia.

## 7. Contratos inmutables (no romper)

1. **26 `.comp` = 26 `data-review-id` únicos, 1:1, 0 duplicados.** `verify-diagram-playwright.cjs`
   (validador fail-closed externo) lo exige. Un `.comp` nuevo = un `data-review-id` nuevo; nunca reutilizar.
2. **17/17 símbolos** definidos **y** usados; sin referencias colgantes; 0 paths fuera del sprite.
3. **Tokens**: sin hex nuevos fuera de los tres bloques `:root` citados; `ss01` en todo texto.
4. **`data-od-id`** en regiones/controles clave (ya presentes: `page-header`, `tabs-nav`,
   `tab-architecture`, `tab-loop`, `tab-matrix`, `tab-roadmap`, `flow-connector-*`, `page-footer`).
5. Contenido en **es-ES**; los `data-review-id`/`data-tip`/títulos de componente son el texto de referencia
   del ciclo de revisión — no renombrar sin cambiar también el verifier.

## 8. Verificación antes de cerrar

```bash
# 1:1 comp ↔ data-review-id (26/26, sin duplicados)
grep -o 'class="comp c-[a-z-]*"' index.html | wc -l
grep -o 'data-review-id="[^"]*"' index.html | sort | uniq -d          # debe salir vacío

# sprite: símbolos definidos y usados
grep -c '<symbol id="icon-' index.html
grep -o 'href="#icon-[^"]*"' index.html | sort -u | wc -l             # debe ser ≤ nº símbolos

# paths fuera del sprite (dentro de <body> pero fuera de <svg class="sprite">) → 0

# render (opcional, vía daemon)
"$OD_NODE_BIN" "$OD_BIN" export index.html --project "$OD_PROJECT_ID" --format image --out /tmp/check.png
```

Revisar también: etiquetas balanceadas, `aria-selected` coherente, foco visible, y que en ≤640px
el nav siga siendo una fila con scroll (no apilado) y sin overflow horizontal.

## 9. Reglas de edición

- Editar `index.html` en su sitio; preservar los tres bloques de tokens y el sprite.
- No re-introducir `border-left` de color en `.comp`; no apilar los tabs en móvil; no poner
  `white-space: nowrap` en `.connector-label`.
- Icono nuevo → `<symbol>` (nunca path suelto); unificar `stroke-width` 1.7.
- Cualquier cambio en el contrato (§7) debe venir con el verifier actualizado y validación 1:1 verde.
