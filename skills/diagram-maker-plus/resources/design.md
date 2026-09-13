# Design System — Linear × Stripe Dark (documentos HTML)

**Skill:** diagram-maker-plus v2.0.0 · **Spec:** Linear × Stripe Dark + Plannotator B2
**Artefacto validado (referencia):** `apps/pae-wizard/outputs/disenos/prp-hook-openclaw-engram-2026-08-14-r5.html` (PRP técnico, 440+ líneas, verificado 2026-08-14)
**Uso:** documentos HTML autocontenidos de PLAN/ARQUITECTURA/PIPELINE con contenido técnico denso (tablas, código, notas de evidencia). No es para diagramas `.comp` interactivos (usar el boilerplate del SKILL.md); es el mismo sistema de tokens aplicado a formato documento largo.

---

## 1. Principios

1. **Dark-only por defecto** (`color-scheme: dark`). No hay modo claro en pantalla; el **print stylesheet** es el único modo claro (papel).
2. **Contenido = evidencia.** El diseño NUNCA altera el contenido; cualquier iteración se verifica por **diff estructural** (ver §4).
3. **Standalone.** Sin dependencias de red obligatorias (fuentes = stack sistema; no Google Fonts).
4. **Tokens fijos.** Copiar el bloque `:root` EXACTO (§2). Prohibido inventar colores fuera de la paleta semántica.

## 2. Tokens CSS (copiar exactamente)

```css
:root{
  --bg: color-mix(in oklab, #0d253d 72%, #04060d 28%);
  --surface: color-mix(in oklab, #1c1e54 30%, #0c1322 70%);
  --surface-warm: color-mix(in oklab, #1c1e54 18%, #111a30 82%);
  --fg: color-mix(in oklab, #ffffff 96%, #b9b9f9 4%);
  --fg-2: color-mix(in oklab, #ffffff 78%, #64748d 22%);
  --muted: #94a3b8; --meta: #64748d;
  --border: color-mix(in oklab, #64748d 34%, transparent 66%);
  --border-soft: color-mix(in oklab, #64748d 22%, transparent 78%);
  --color-antigravity: #60a5fa; /* azul: core/orquestador */
  --color-plannotator: #f472b6; /* rosa: revisión humana */
  --color-adapter:     #fbbf24; /* ámbar: bridge/normalizador */
  --color-opendesign:  #34d399; /* esmeralda: live design */
  --ok: #34d399;  --ok-bg: color-mix(in oklab, #34d399 14%, transparent);
  --warn: #fbbf24; --warn-bg: color-mix(in oklab, #fbbf24 14%, transparent);
  --danger: #f87171; --danger-bg: color-mix(in oklab, #f87171 14%, transparent);
  --pending: #94a3b8; --pending-bg: color-mix(in oklab, #94a3b8 14%, transparent);
  --font-display: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
  --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
  --font-mono: ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Consolas, monospace;
  --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px; --radius-pill: 9999px;
  --elev-flat: none;
  --elev-raised: rgba(50,50,93,.45) 0px 30px 45px -30px, rgba(0,0,0,.55) 0px 18px 36px -18px;
  --elev-deep: rgba(3,3,39,.50) 0px 14px 21px -14px, rgba(0,0,0,.55) 0px 8px 17px -8px;
  --accent: #533afd; --accent-on: #ffffff;
  --focus-ring: 0 0 0 2px var(--accent), 0 0 0 5px color-mix(in oklab, var(--accent), transparent 75%);
  --motion-fast: 150ms; --motion-base: 200ms; --ease-standard: cubic-bezier(0.2,0,0,1);
  color-scheme: dark;
}
```

Body: `background-color: var(--bg)` + dos radiales de acento (elipse 90% 60% at 50% -18% rgba(83,58,253,.16); elipse 60% 45% at 110% 8% rgba(83,58,253,.10)). Fuente body: `var(--font-body)`.

## 3. Estructura del documento (patrón validado en r5)

```
.wrap (max-width 1100px)
├── header.hero.card
│   ├── .badge-top          # pill mono uppercase ok-bg: "🦞 PRP · Plan · rN · fecha"
│   ├── h1 (+ .sub2 como subtítulo block)
│   ├── p.sub               # muted, max-width 820px
│   └── .meta > .pill       # pills de metadata (fecha, estado, autor)
├── .card.toc#toc
│   ├── h2 > .secnum ≡ + "Índice"
│   └── .toc-grid > a[href=#id] (.tocnum) / a.toc-sub   # anclas a h2/h3
├── .card (por sección)
│   ├── h2 id="..." > .secnum (chip número) + label
│   ├── h3 id="..."         # con ::before cuadrado accent 7px
│   ├── table (thead sticky, th dark, zebra, hover accent 10%)
│   ├── pre > code          # surface-warm, border-left 3px accent
│   ├── code inline         # rgba(255,255,255,.07) bg, color #a5b4fc
│   ├── .tag.{green,amber,red,blue}   # badges semánticos uppercase
│   ├── .note / .note.ok    # warn-bg/ok-bg, border-left 3px
│   └── ul/ol/p
└── .footer                 # meta, mono, border-top, link ↑ Índice
```

**Reglas de componentes:**
- `.secnum`: chip pill `rgba(83,58,253,.25)` bg + border `rgba(139,125,255,.45)`, mono, blanco.
- `h2`: 1.28rem, weight 500, #fff, border-bottom `--border-soft`. `h3::before`: cuadrado accent con glow (`box-shadow 0 0 8px rgba(83,58,253,.8)`).
- Tablas: `th` bg `rgba(255,255,255,.06)`; `td` color `--fg-2`; zebra `rgba(255,255,255,.025)`; hover fila `rgba(83,58,253,.10)`; `thead{position:sticky;top:0}`.
- Badges: `.tag-green`→ok, `.tag-amber`→warn, `.tag-red`→danger, `.tag-blue`→antigravity (bg 14% + borde 30%).
- Cards: `--surface`, borde `--border`, `--elev-raised`, animación `fadeIn .4s` escalonada (nth-of-type delays .05s), respeta `prefers-reduced-motion`.
- TOC: links mono `--muted`, hover `#fff` + `rgba(83,58,253,.15)`; `.toc-sub` indent 26px.

**Print stylesheet (obligatorio):** override `:root` a claro (`--bg:#fff; --fg:#1a202c; --muted:#4a5568; --border:#cbd5e0`), cards sin sombra con `break-inside:avoid`, `.toc{display:none}`, `thead{position:static}`, hero sin `::before`.

## 4. Verificación OBLIGATORIA antes de entregar (determinista)

```bash
# 1. Balance de divs
python3 -c "
import re
c = open('doc.html', encoding='utf-8').read()
o, cl = len(re.findall(r'<div\b', c)), len(re.findall(r'</div>', c))
assert o == cl, f'divs {o}/{cl}'
print('divs OK', o, cl)"
# 2. Anclas TOC resuelven + ids únicos
python3 -c "
import re
c = open('doc.html', encoding='utf-8').read()
ids = set(re.findall(r'<h[23] id=\"([^\"]+)\"', c))
hrefs = {a or b for a,b in re.findall(r'<a class=\"toc-sub\" href=\"#([^\"]+)\"|<a href=\"#([^\"]+)\"', c)}
missing = hrefs - ids - {'toc'}
assert not missing, f'missing: {missing}'
from collections import Counter
dups = {k:v for k,v in Counter(re.findall(r'<h[23] id=\"([^\"]+)\"', c)).items() if v>1}
assert not dups, f'dups: {dups}'
print('anclas OK', len(hrefs), 'ids', len(ids))"
# 3. Diff estructural vs versión previa (solo cambios intencionales)
python3 - <<'EOF'
import re, difflib
prev = open('prev.html', encoding='utf-8').read()
new  = open('new.html', encoding='utf-8').read()
def body(h): return re.sub(r'<style>.*?</style>', '/*S*/', h, flags=re.S)
sm = difflib.SequenceMatcher(None, body(prev), body(new))
n = sum(1 for op,_,_,_,_ in sm.get_opcodes() if op != 'equal')
print('bloques de cambio:', n, '(deben ser SOLO los intencionales)')
EOF
# 4. Screenshot real (Chrome headless) para el humano
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --screenshot=/tmp/preview.png --window-size=1200,1600 --hide-scrollbars \
  "file://$PWD/doc.html"
```

**Criterio de aceptación:** contenido idéntico a la versión previa (salvo cambios intencionales), divs balanceados, anclas 100% resueltas, 0 ids duplicados. Si el modelo no puede ver imágenes, el diff estructural + DOM counts son suficientes — declararlo en el reporte.

## 5. Gotchas (aprendidos en r5, 2026-08-14)

1. **El edit tool falla con emojis/acentos en anchors** → usar scripts Python con `io.open(encoding='utf-8')` y anclas ASCII cortas.
2. **Nunca `c.find()` + slicing con offsets** para reemplazar bloques — un offset mal calculado rompe tags. Usar `replace()` con la cadena completa.
3. **Verificar contexto ANTES del replace** (`print(repr(c[idx-80:idx+80]))`).
4. **Normalización de diffs de texto**: los checks de contenido con `.replace()` de normalización dan falsos positivos por espacios/emojis → el diff estructural (sin `<style>`) es el definitivo.
5. **Headless Chrome**: usar `file://` directo (el browser tool bloquea `file:`/`localhost` por policy). Las fuentes del stack sistema renderizan sin red.
6. **Vision models pueden no estar disponibles** (401/403): el diff determinista es la verificación canónica; el screenshot es para el humano.
7. **Versionar iteraciones**: `nombre-r1.html` → `-r2` → `-r3`... conservar versiones previas como evidencia; el footer lleva crédito `Design: diagram-maker-plus v2.0 (Linear × Stripe Dark)`.

## 6. Cómo replicar (checklist del agente)

- [ ] Copiar `:root` EXACTO de §2 + body con radiales de acento
- [ ] Estructura §3: hero+badge-top → TOC → cards por sección → footer
- [ ] Chips `.secnum` en h2, ids únicos en h2/h3
- [ ] Tablas sticky + zebra + hover; pre con border-left accent
- [ ] Badges semánticos (.tag-green/amber/red/blue) y notes (.note/.note.ok)
- [ ] Print stylesheet claro + `prefers-reduced-motion`
- [ ] Verificación §4 completa (divs, anclas, diff, screenshot)
- [ ] Reportar: ruta, verificaciones, bloques de diff intencionales
