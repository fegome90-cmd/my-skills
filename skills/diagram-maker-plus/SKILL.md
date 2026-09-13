---
name: diagram-maker-plus
description: "Extended diagram generation: Interactive Live HTML (Plannotator B2 + Open Design Dark Mode), Archify router (cloud architecture, workflow pipelines, dataflow lineage, state machines, sequence traces), Mermaid.js, SVG. Generates 1-shot high-fidelity, reviewable, accessible diagrams."
when:
  - "User wants an interactive HTML plan diagram for Plannotator, Open Design, or architectural review"
  - "User wants deep architecture topology, cloud infrastructure, microservices, or multi-cloud systems"
  - "User wants DAG workflow pipelines, CI/CD runbooks, or ETL/data lineage diagrams"
  - "User wants state machine lifecycles, transition diagrams, or interactive sequence traces"
  - "User specifies engine: archify or provides Archify JSON-IR specs"
  - "User asks for Mermaid diagram, sequence diagram, class diagram, ER diagram, Gantt chart, mind map, state diagram, pie chart, or flowchart"
  - "User wants interactive diagrams with tooltips, sticky tabs, animated flow connectors, or hover states"
  - "User wants a diagram described in text (diagram-to-explanation)"
  - "User wants to visualize code structure, AST, or data flow from source code"
  - "User wants mobile-responsive diagrams with dark/light aesthetics"
examples:
  - "Crea un diagrama HTML interactivo del plan de arquitectura para revisar en Plannotator"
  - "Genera un pipeline workflow formal con Archify decorado para Plannotator B2"
  - "Diagrama de topología cloud en Archify con contrato B2"
  - "Genera un diagrama de diseño vivo compatible con Open Design y Plannotator B2"
  - "Diagrama de secuencia del login flow"
  - "ER diagram de la base de datos"
  - "Mind map de los conceptos clave"
  - "Gantt del sprint"
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "2.0.0"
  openclaw:
    requires:
      bins: ["node"]
    emoji: "🗺️"
---

# Diagram Maker Plus

Generador de diagramas técnicos de alta fidelidad. Soporta:
1. **Modo Live HTML Interactivo** (Estándar insignia para planes, Plannotator B2 y Open Design).
2. **Motor Avanzado Archify** (Topologías complejas, pipelines DAG, máquinas de estado y trazas interactivas con contrato B2).
3. **Mermaid.js** (CDN para diagramas estándar: secuencia, ER, Gantt, etc.).
4. **SVG Puro** (Secuencia, ER, Mindmap, Gantt embebidos).

---

## Output Modes & Routing

| Mode | Format | Best For |
|------|--------|----------|
| `live-html` (Recomendado) | `.html` (Standalone, CSS tokens + JS) | **Planes de arquitectura, revisión con Plannotator B2, diseño vivo con Open Design, dashboards de decisión** |
| `archify` (Enrutado) | `.html` (Archify + B2 Decorator) | **Topologías cloud/infra (`architecture`), pipelines (`workflow`), data lineage (`dataflow`), state machines (`lifecycle`), o trazas interactivas (`sequence`)** |
| `mermaid` | `.html` (CDN-rendered) | Secuencias simples, clases, ER rápido, Gantt, pie, estados |
| `sequence-svg` | `.html` (inline SVG) | Diagramas de secuencia detallados con notas/alt/opt personalizados |
| `er-svg` | `.html` (inline SVG) | Esquemas de base de datos con cardinalidad estricta |
| `mindmap-svg` | `.html` (inline SVG) | Mapas conceptuales radiales y brainstorming |
| `gantt-svg` | `.html` (inline SVG) | Cronogramas, sprints y roadmaps visuales |
| `code-diagram` | `.html` (inline SVG) | Visualización de AST y flujo de datos desde código |

### 🧭 Enrutamiento a Motor Avanzado (Archify-B2)

Para requerimientos de arquitectura profunda, pipelines o máquinas de estado, delegar la compilación a Archify mediante el CLI transaccional:

```bash
# 1-Paso atómico: valida (showcase 9/9), renderiza, decora B2, verifica paridad y sella el recibo
node skills/diagram-maker-plus/scripts/archify-b2.mjs build <type> <input.json> <output.html>

# Diagnóstico de salud del runtime congelado (commit 06dd052)
node skills/diagram-maker-plus/scripts/archify-b2.mjs doctor
```

> 📖 **Especificación completa:** Consultar [`resources/ARCHIFY-ROUTER.md`](resources/ARCHIFY-ROUTER.md) para schemas JSON-IR, directiva `engine: auto|native|archify`, matriz de calificación 5/5 y estructura del recibo criptográfico.

---

## 🌟 Modo Live HTML (Linear × Stripe Dark + Plannotator B2)

Este es el formato estándar para **cualquier plan, arquitectura o sistema revisable**. Cualquier agente debe ser capaz de generarlo en **una sola iteración** siguiendo las especificaciones a continuación.

### 1. Sistema de Tokens CSS (Linear × Stripe Dark Canvas)

Copiar exactamente este bloque `:root` en el `<style>` del documento:

```css
:root {
  /* ─── Canvas & Superficies (Linear Dark Palette) ─── */
  --bg:            color-mix(in oklab, #0d253d 72%, #04060d 28%);
  --surface:       color-mix(in oklab, #1c1e54 30%, #0c1322 70%);
  --surface-warm:  color-mix(in oklab, #1c1e54 18%, #111a30 82%);
  --fg:            color-mix(in oklab, #ffffff 96%, #b9b9f9 4%);
  --fg-2:          color-mix(in oklab, #ffffff 78%, #64748d 22%);
  --muted:         #94a3b8;
  --meta:          #64748d;
  --border:        color-mix(in oklab, #64748d 34%, transparent 66%);
  --border-soft:   color-mix(in oklab, #64748d 22%, transparent 78%);

  /* ─── Paleta Semántica por Capa de Arquitectura ─── */
  --color-antigravity: #60a5fa;   /* Azul: Orquestador / Core System */
  --color-plannotator: #f472b6;   /* Rosa: Human Review Surface / UI */
  --color-adapter:     #fbbf24;   /* Ámbar: Normalizador / Bridge / B2 */
  --color-opendesign:  #34d399;   /* Esmeralda: Live Design Engine */

  /* ─── Estados Semánticos ─── */
  --ok:         #34d399;
  --ok-bg:      color-mix(in oklab, #34d399 14%, transparent);
  --warn:       #fbbf24;
  --warn-bg:    color-mix(in oklab, #fbbf24 14%, transparent);
  --danger:     #f87171;
  --danger-bg:  color-mix(in oklab, #f87171 14%, transparent);
  --pending:    #94a3b8;
  --pending-bg: color-mix(in oklab, #94a3b8 14%, transparent);

  /* ─── Tipografía ─── */
  --font-display: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
  --font-body:    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
  --font-mono:    ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Consolas, monospace;

  /* ─── Radios & Elevación Cromática (Stripe Shadow Spec) ─── */
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   12px;
  --radius-pill: 9999px;

  --elev-flat:   none;
  --elev-raised:
    rgba(50, 50, 93, 0.45) 0px 30px 45px -30px,
    rgba(0, 0, 0, 0.55) 0px 18px 36px -18px;
  --elev-deep:
    rgba(3, 3, 39, 0.50) 0px 14px 21px -14px,
    rgba(0, 0, 0, 0.55) 0px 8px 17px -8px;

  /* ─── Foco Accesible & Animación ─── */
  --accent:       #533afd;
  --accent-on:    #ffffff;
  --focus-ring:   0 0 0 2px var(--accent), 0 0 0 5px color-mix(in oklab, var(--accent), transparent 75%);
  --motion-fast:  150ms;
  --motion-base:  200ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
}
```

---

### 2. Invariantes del Contrato Plannotator B2 (Fail-Closed)

Para que el diagrama sea compatible con la UI de **Plannotator** y el conversor W3C **Adapter B2**, **TODO elemento interactivo/revisable DEBE cumplir con estas reglas inviolables**:

1. **Clase `.comp` y clase de color:** `<div class="comp c-{sistema}" ...>` donde `{sistema}` es `antigravity`, `plannotator`, `adapter`, `opendesign` o `danger`.
2. **Atributo `data-review-id` obligatorio y único:** `data-review-id="slug-descriptivo"`.
   * *Regla 1:1:* La cantidad de elementos `.comp` debe ser **idéntica** a la cantidad de atributos `data-review-id`. Cero duplicados.
3. **Tooltip descriptivo `data-tip`:** Breve resumen funcional (1 oración) para el controller flotante.
4. **Transporte Dual y Compatibilidad de Anclaje Plannotator:**
   En artefactos compilados por Archify o enriquecidos para Plannotator, el decorador B2 inyecta además `data-annotate="slug-descriptivo"`. La función normalizadora `extractReviewId(anchor)` resuelve selectores de cualquier formato (`#node-<id>`, `data-annotate`, o W3C targets) hacia el `reviewId` canónico B2.
5. **Estructura interna estándar:**
   ```html
   <div class="comp c-antigravity" data-review-id="comp.orquestador-core" data-tip="Controlador principal del ciclo de ejecución">
     <div class="comp-header">
       <span class="comp-title">Orquestador Core</span>
       <span class="comp-id-tag">orquestador-core</span>
     </div>
     <p class="comp-desc">Gestiona el ciclo de vida, estado de memoria y distribución de tareas.</p>
   </div>
   ```

---

### 3. Componentes Visuales Estándar

#### A. Conector de Flujo Animado (`.flow-connector`)
Representa el puente dinámico entre capas o fases:
```html
<div class="flow-connector">
  <div class="connector-line"></div>
  <div class="connector-node"></div>
  <span class="connector-label">⬇️ Ciclo de Ejecución Autónomo</span>
  <div class="connector-node"></div>
  <div class="connector-line"></div>
</div>
```

#### B. Navegación por Tabs Accesible (`.tabs-nav` + `.tab-pane`)
Permite organizar múltiples vistas (Arquitectura, Flujos, Matriz de Decisiones, Roadmap):
```html
<nav class="tabs-nav" role="tablist" aria-label="Vistas del diagrama">
  <button class="tab-btn active" data-tab="tab-1" role="tab" aria-selected="true">
    <span>🏛️</span> 1. Arquitectura
  </button>
  <button class="tab-btn" data-tab="tab-2" role="tab" aria-selected="false">
    <span>🔄</span> 2. Ciclo de Flujo
  </button>
</nav>

<section id="tab-1" class="tab-pane active" role="tabpanel"> ... </section>
<section id="tab-2" class="tab-pane" role="tabpanel"> ... </section>
```

#### C. Floating Tooltip Controller (JS Ligero y Bounded)
Vanilla JavaScript que garantiza que los tooltips nunca se corten en los bordes de la pantalla:
```javascript
document.addEventListener("DOMContentLoaded", () => {
  // Tabs switcher
  const buttons = document.querySelectorAll(".tab-btn");
  const panes = document.querySelectorAll(".tab-pane");

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-tab");
      buttons.forEach(b => { b.classList.remove("active"); b.setAttribute("aria-selected", "false"); });
      panes.forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      btn.setAttribute("aria-selected", "true");
      const targetPane = document.getElementById(targetId);
      if (targetPane) targetPane.classList.add("active");
    });
  });

  // Tooltip controller
  const tooltip = document.getElementById("tooltip");
  const comps = document.querySelectorAll(".comp[data-tip]");

  comps.forEach(comp => {
    comp.addEventListener("mouseenter", (e) => {
      const tipText = comp.getAttribute("data-tip");
      if (!tipText) return;
      tooltip.textContent = tipText;
      tooltip.classList.add("visible");
      positionTooltip(e);
    });
    comp.addEventListener("mousemove", positionTooltip);
    comp.addEventListener("mouseleave", () => tooltip.classList.remove("visible"));
  });

  function positionTooltip(e) {
    const x = Math.min(e.clientX + 14, window.innerWidth - 320);
    const y = e.clientY + 14;
    tooltip.style.left = `${x}px`;
    tooltip.style.top = `${y}px`;
  }
});
```

---

### 4. Plantilla Boilerplate Completa (1-Shot Template)

Cualquier agente puede copiar este esqueleto base y reemplazar los títulos y cajas `.comp`:

```html
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TITULO_DEL_DIAGRAMA</title>
  <style>
    :root {
      --bg: color-mix(in oklab, #0d253d 72%, #04060d 28%);
      --surface: color-mix(in oklab, #1c1e54 30%, #0c1322 70%);
      --surface-warm: color-mix(in oklab, #1c1e54 18%, #111a30 82%);
      --fg: color-mix(in oklab, #ffffff 96%, #b9b9f9 4%);
      --fg-2: color-mix(in oklab, #ffffff 78%, #64748d 22%);
      --muted: #94a3b8;
      --meta: #64748d;
      --border: color-mix(in oklab, #64748d 34%, transparent 66%);
      
      --color-antigravity: #60a5fa;
      --color-plannotator: #f472b6;
      --color-adapter:     #fbbf24;
      --color-opendesign:  #34d399;
      --danger:            #f87171;

      --ok: #34d399;
      --ok-bg: color-mix(in oklab, #34d399 14%, transparent);
      --warn: #fbbf24;
      --warn-bg: color-mix(in oklab, #fbbf24 14%, transparent);
      --danger-bg: color-mix(in oklab, #f87171 14%, transparent);

      --radius-sm: 4px;
      --radius-md: 8px;
      --radius-lg: 12px;
      --radius-pill: 9999px;

      --elev-raised: rgba(50, 50, 93, 0.45) 0px 30px 45px -30px, rgba(0, 0, 0, 0.55) 0px 18px 36px -18px;
      --elev-deep: rgba(3, 3, 39, 0.50) 0px 14px 21px -14px, rgba(0, 0, 0, 0.55) 0px 8px 17px -8px;
      --focus-ring: 0 0 0 2px #533afd, 0 0 0 5px rgba(83, 58, 253, 0.25);
      --ease-standard: cubic-bezier(0.2, 0, 0, 1);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
      background-color: var(--bg);
      background-image:
        radial-gradient(ellipse 90% 60% at 50% -18%, rgba(83, 58, 253, 0.16), transparent 62%),
        radial-gradient(ellipse 60% 45% at 110% 8%, rgba(83, 58, 253, 0.10), transparent 60%);
      color: var(--fg);
      line-height: 1.5;
      padding: 2.5rem 1.5rem 5rem;
      min-height: 100vh;
    }

    .container { max-width: 1100px; margin: 0 auto; }
    header { text-align: center; margin-bottom: 2.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border); }
    .badge-top { display: inline-flex; align-items: center; gap: 0.5rem; background: var(--ok-bg); color: var(--ok); border: 1px solid rgba(52, 211, 153, 0.3); border-radius: var(--radius-pill); padding: 0.25rem 0.85rem; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 1rem; }
    h1 { font-size: clamp(2rem, 4vw, 2.75rem); font-weight: 400; margin-bottom: 0.6rem; color: #fff; }
    .subtitle { color: var(--muted); font-size: 1rem; max-width: 760px; margin: 0 auto; }

    .tabs-nav { display: flex; flex-wrap: wrap; gap: 4px; background: rgba(13, 37, 61, 0.75); backdrop-filter: blur(12px); padding: 4px; border-radius: var(--radius-md); border: 1px solid var(--border); margin-bottom: 2rem; position: sticky; top: 10px; z-index: 40; }
    .tab-btn { flex: 1; min-width: 160px; background: transparent; border: none; color: var(--muted); padding: 0.75rem 1rem; border-radius: var(--radius-sm); font-size: 0.88rem; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.5rem; transition: all 0.2s; }
    .tab-btn:hover { color: #fff; background: rgba(255, 255, 255, 0.05); }
    .tab-btn.active { color: #fff; background: rgba(83, 58, 253, 0.25); box-shadow: inset 0 0 0 1px rgba(139, 125, 255, 0.45); }

    .tab-pane { display: none; }
    .tab-pane.active { display: block; animation: fadeIn 0.25s ease-out forwards; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }

    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin-bottom: 1.5rem; }
    .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.25rem; margin-bottom: 1.5rem; }
    .card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1.5rem; box-shadow: var(--elev-raised); transition: all 0.2s; }
    .card:hover { border-color: rgba(139, 125, 255, 0.5); transform: translateY(-2px); }
    .card-title { font-size: 1.1rem; font-weight: 500; color: #fff; margin-bottom: 1rem; display: flex; align-items: center; justify-content: space-between; }

    .comp { background: var(--surface-warm); border: 1px solid var(--border); border-left: 3px solid var(--comp-color, #533afd); border-radius: var(--radius-md); padding: 1rem; margin-bottom: 0.85rem; cursor: pointer; transition: all 0.2s; }
    .comp:hover { background: color-mix(in oklab, var(--surface-warm) 80%, #533afd 20%); border-color: var(--comp-color, #533afd); transform: translateY(-2px); box-shadow: var(--elev-deep); }
    .comp.c-antigravity { --comp-color: var(--color-antigravity); }
    .comp.c-plannotator { --comp-color: var(--color-plannotator); }
    .comp.c-adapter     { --comp-color: var(--color-adapter); }
    .comp.c-opendesign  { --comp-color: var(--color-opendesign); }
    .comp.c-danger      { --comp-color: var(--danger); }

    .comp-header { display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; margin-bottom: 0.4rem; }
    .comp-title { font-size: 0.95rem; font-weight: 500; color: var(--fg); }
    .comp-id-tag { font-family: var(--font-mono); font-size: 0.68rem; color: var(--comp-color, #fff); background: rgba(255,255,255,0.06); padding: 0.15rem 0.45rem; border-radius: var(--radius-sm); border: 1px solid rgba(255,255,255,0.12); }
    .comp-desc { font-size: 0.82rem; color: var(--muted); line-height: 1.45; }

    .flow-connector { display: flex; align-items: center; justify-content: center; gap: 12px; padding: 1.5rem 0; }
    .connector-line { flex: 1; max-width: 200px; height: 1px; background: var(--border); }
    .connector-node { width: 10px; height: 10px; border-radius: 50%; background: #533afd; box-shadow: 0 0 12px #533afd; }
    .connector-label { padding: 0.4rem 0.9rem; border-radius: var(--radius-md); background: var(--surface-warm); border: 1px solid var(--border); font-size: 0.85rem; color: var(--fg-2); }

    .badge { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.15rem 0.55rem; border-radius: var(--radius-sm); font-size: 0.72rem; font-weight: 600; text-transform: uppercase; }
    .badge-ok   { background: var(--ok-bg); color: var(--ok); border: 1px solid rgba(52,211,153,0.3); }
    .badge-warn { background: var(--warn-bg); color: var(--warn); border: 1px solid rgba(251,191,36,0.3); }

    .tooltip-bubble { position: fixed; opacity: 0; pointer-events: none; z-index: 9999; max-width: 290px; background: #0b1120; color: var(--fg-2); padding: 0.5rem 0.85rem; border-radius: var(--radius-md); font-size: 0.78rem; border: 1px solid rgba(83, 58, 253, 0.4); box-shadow: var(--elev-deep); transition: opacity 0.15s; }
    .tooltip-bubble.visible { opacity: 1; }

    footer { margin-top: 3.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border); text-align: center; color: var(--meta); font-size: 0.82rem; }
  </style>
</head>
<body>

  <div class="container">
    <header>
      <div class="badge-top">v1.0 · Sistema Activo</div>
      <h1>TITULO_DEL_DIAGRAMA</h1>
      <p class="subtitle">DESCRIPCION_DEL_PLAN_O_ARQUITECTURA</p>
    </header>

    <nav class="tabs-nav" role="tablist">
      <button class="tab-btn active" data-tab="tab-sys" role="tab" aria-selected="true"><span>🏛️</span> 1. Vista Principal</button>
      <button class="tab-btn" data-tab="tab-flows" role="tab" aria-selected="false"><span>🔄</span> 2. Flujos &amp; Contratos</button>
    </nav>

    <section id="tab-sys" class="tab-pane active" role="tabpanel">
      <div class="grid-2">
        <div class="card">
          <div class="card-title">
            <span>Fase 1: Entrada &amp; Orquestación</span>
            <span class="badge badge-ok">Ready</span>
          </div>

          <div class="comp c-antigravity" data-review-id="comp.orquestador" data-tip="Nodo orquestador central">
            <div class="comp-header">
              <span class="comp-title">Orquestador Principal</span>
              <span class="comp-id-tag">orquestador</span>
            </div>
            <p class="comp-desc">Coordina sub-agentes y distribuye tareas.</p>
          </div>
        </div>

        <div class="card">
          <div class="card-title">
            <span>Fase 2: Superficie de Revisión</span>
            <span class="badge badge-ok">Active</span>
          </div>

          <div class="comp c-plannotator" data-review-id="comp.review-surface" data-tip="Superficie de revisión visual Plannotator">
            <div class="comp-header">
              <span class="comp-title">Plannotator UI</span>
              <span class="comp-id-tag">review-surface</span>
            </div>
            <p class="comp-desc">Permite anotaciones humanas estructuradas en el navegador.</p>
          </div>
        </div>
      </div>
    </section>

    <section id="tab-flows" class="tab-pane" role="tabpanel">
      <!-- Vistas secundarias -->
    </section>

    <footer>
      <span>Plannotator B2 · Open Design Standard</span>
    </footer>
  </div>

  <div id="tooltip" class="tooltip-bubble"></div>

  <script>
    document.addEventListener("DOMContentLoaded", () => {
      const tabButtons = document.querySelectorAll(".tab-btn");
      const tabPanes = document.querySelectorAll(".tab-pane");
      tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
          const targetId = btn.getAttribute("data-tab");
          tabButtons.forEach(b => { b.classList.remove("active"); b.setAttribute("aria-selected", "false"); });
          tabPanes.forEach(p => p.classList.remove("active"));
          btn.classList.add("active");
          btn.setAttribute("aria-selected", "true");
          const targetPane = document.getElementById(targetId);
          if (targetPane) targetPane.classList.add("active");
        });
      });

      const tooltip = document.getElementById("tooltip");
      const comps = document.querySelectorAll(".comp[data-tip]");
      comps.forEach(comp => {
        comp.addEventListener("mouseenter", (e) => {
          tooltip.textContent = comp.getAttribute("data-tip") || "";
          tooltip.classList.add("visible");
          positionTooltip(e);
        });
        comp.addEventListener("mousemove", positionTooltip);
        comp.addEventListener("mouseleave", () => tooltip.classList.remove("visible"));
      });

      function positionTooltip(e) {
        const x = Math.min(e.clientX + 14, window.innerWidth - 310);
        const y = e.clientY + 14;
        tooltip.style.left = `${x}px`;
        tooltip.style.top = `${y}px`;
      }
    });
  </script>
</body>
</html>
```

---

## Script de Verificación Rápida (Playwright / Python)

Antes de entregar cualquier diagrama HTML a Plannotator o al usuario, ejecutar esta validación de paridad 1:1:

```bash
python3 -c "
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'docs/mi-diagrama.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Quitar style y script para contar solo nodos DOM reales
body = re.sub(r'<style.*?</style>', '', c, flags=re.DOTALL)
body = re.sub(r'<script.*?</script>', '', body, flags=re.DOTALL)

# Buscar elementos con clase 'comp'
exact_comps = [cls for cls in re.findall(r'<[a-zA-Z0-9]+[^>]*\bclass=\"([^\"]+)\"[^>]*>', body) if 'comp' in cls.split()]
review_ids = re.findall(r'data-review-id=\"([^\"]+)\"', body)

print(f'Total .comp elements: {len(exact_comps)}')
print(f'Total data-review-id: {len(review_ids)}')
print(f'Unique review IDs:    {len(set(review_ids))}')

assert len(exact_comps) == len(review_ids) == len(set(review_ids)), 'ERROR: Mismatch or duplicate data-review-id!'
print('✅ VERIFICACIÓN PASS: Paridad 1:1 estricta y unicidad de IDs garantizada.')
" docs/diagrama-plan-open-design-live.html
```

---

## Mermaid.js Mode (Modo Clásico)

Para diagramas rápidos de flujo, secuencia estándar o Gantt sin superficie de revisión Plannotator:

### Template Mermaid Wrapper
```html
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Diagram</title>
<style>
  body { margin: 0; background: #0b1120; color: #f8fafc; display: flex; justify-content: center; padding: 32px 16px; font-family: system-ui, sans-serif; }
  .mermaid { max-width: 980px; width: 100%; display: flex; justify-content: center; }
  @media (max-width: 600px) { body { padding: 16px 8px; } .mermaid { font-size: 14px; overflow-x: auto; } }
</style>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>mermaid.initialize({ startOnLoad: true, theme: 'dark', securityLevel: 'loose' });</script>
</head>
<body>
<pre class="mermaid">
REPLACE_WITH_MERMAID_CODE
</pre>
</body>
</html>
```

---

## Reglas de Oro (Checklist de Entrega)

- [ ] **Modo Live HTML:** ¿Todos los nodos `.comp` tienen `data-review-id` único y `data-tip`?
- [ ] **Modo Archify:** ¿Pasó validación `showcase` (9/9 checks), biyección cross-layer (`IR_IDS == SVG_NODE_IDS`) y emitió `.bridge-receipt.json`?
- [ ] **Paridad 1:1:** ¿`exact_comps == len(review_ids) == len(set(review_ids))`?
- [ ] **Paleta Semántica:** ¿Se usan `--color-antigravity`, `--color-plannotator`, `--color-adapter`, `--color-opendesign` en lugar de colores arbitrarios?
- [ ] **Navegación:** ¿Los tabs tienen ARIA (`role="tab"`, `role="tabpanel"`) y cambian de vista con cero errores de consola?
- [ ] **Tooltip Controller:** ¿El tooltip se mantiene visible dentro del viewport?
- [ ] **Standalone:** ¿El archivo funciona 100% offline sin dependencias externas obligatorias?

---

**Version:** 2.1.0 | **Updated:** 2026-09-04 | **Design Spec:** Linear × Stripe Dark + Plannotator B2 W3C Contract + Archify Router

---

## Recursos

- `resources/ARCHIFY-ROUTER.md` — **Router por capacidades y puente Archify-B2**: Contrato JSON-IR (schemas v2), directiva `engine`, matriz de calificación 5/5, ejecución transaccional atómica, recibo criptográfico y claim boundary formal.
- `resources/design.md` — **Design system para DOCUMENTOS HTML** (PRP/planes/arquitectura en formato documento largo, no diagrama `.comp`): tokens Linear × Stripe Dark exactos, estructura hero+TOC+cards+tablas, verificación determinista (divs/anclas/diff estructural) y gotchas. Artefacto validado: `apps/pae-wizard/outputs/disenos/prp-hook-openclaw-engram-2026-08-14-r5.html`. Leerlo ANTES de producir un documento HTML extenso.
- `resources/design-diagrams.md` — **Design system para DIAGRAMAS VIVOS INTERACTIVOS (.comp)**: Especificación canónica exportada de Open Design para diagramas interactivos Plannotator B2 (sprite SVG 17 iconos Feather, roving tabindex, `.tab-indicator`, `.flow-connector` interactivo, invariante 1:1 `data-review-id`, anti-slop rules).
- `resources/live-diagram-template.html` — template 1-shot para diagramas interactivos `.comp` (Plannotator B2).
