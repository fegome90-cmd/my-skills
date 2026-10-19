# Perfil FALP

Perfil de marca por defecto en el repo [presentaciones-falp](https://github.com/fegome90-cmd/presentaciones-falp). **No
duplica valores**: la fuente normativa es [`DESIGN.md`](https://github.com/fegome90-cmd/presentaciones-falp/blob/main/DESIGN.md) y los tokens se generan en `registry/falp/themes/falp.css` desde
`vendor/falp-brand-system/tokens/*.json` con `scripts/build-registry.mjs`. Este archivo dice cómo aplicar las
reglas generales de la skill con esos tokens y dónde FALP decide distinto.

Si este archivo y `DESIGN.md` discrepan, manda `DESIGN.md`; avisa la diferencia.

## Contexto

- Audiencia: formación y reuniones clínicas FALP en Chile. Español; términos metodológicos en inglés cuando son
  nombres propios (Discover, Define…).
- Lectura: proyección y escritorio; las ampliaciones también se consultan desde móvil. **Modo responsivo**
  (`grilla-y-espacio.md` §1): verificar 1920×1080, 1366×768, 1024×600 y 390 px.
- Registro: contenido y presentación, sin captura de datos ni transacciones. No convertir una relación analítica en
  una afirmación de causalidad clínica.

## Roles → tokens

| Rol de la skill | Token FALP | Contraste medido |
|---|---|---|
| Fondo de página | `--background` (`--falp-blue-canvas` #F5F9FD) | — |
| Superficie / tarjeta | `--card` (blanco), `--surface-tint`, `--surface-mist`, `--secondary` (azul suave) | — |
| Tinta (títulos y cuerpo) | `--foreground` / `--ink` (#12385F) | 11,95:1 sobre blanco; 11,30:1 sobre canvas |
| Estructura de marca | `--primary` / `--blue` (#004990) | 8,91:1 sobre blanco |
| Texto secundario | `--muted-foreground` (#50677E) | 5,86:1 sobre blanco; 5,54:1 sobre canvas |
| Texto terciario | `--tertiary-foreground` (#6B7C93) | **4,26:1 sobre blanco: no alcanza 4,5:1**; solo texto grande o no esencial |
| Técnico (etiquetas) | `--technical-foreground` (#00769F) | 5,13:1 sobre blanco |
| Cian decorativo | `--technical` (#009FE3) | 2,97:1: solo formas y fondos, nunca texto |
| Acento | `--highlight` / `--gold` (#F5C300) | 1,66:1 sobre blanco: nunca texto ni borde único |
| Texto sobre acento | `--on-gold` (#12385F) | 7,22:1 sobre dorado |
| Líneas | `--border` / `--line` (#D7E4EF) | Decorativas; los límites con significado necesitan 3:1 |

Ratios calculados con la fórmula de luminancia WCAG sobre los valores de `falp.css`.

## Decisiones propias de FALP

- **Dorado = fase activa y anotación clave.** Una sola mitad dorada por mapa activo. Como no tiene contraste
  suficiente, siempre va con contorno tinta de 3 px y etiqueta tinta con texto blanco. El hover de otros elementos
  no usa dorado.
- **Tipografía**: Montserrat para títulos (750–850), Inter para lectura y controles (400–650); cifras 700–800 con dos
  dígitos en secuencias. Fuentes locales en `public/fonts`, cargadas una vez por el tema. No agregar familias.
- **Tracking de títulos**: los decks usan `letter-spacing: -0.045em` en títulos Montserrat; es una decisión aceptada
  del perfil, más cerrada que el rango general (−0,01 a −0,03 em). No la cambies en decks existentes.
- **Superficies sin sombra**: jerarquía por alineación, espacio y superficies; tarjetas sin sombra. Solo el marco de
  la presentación lleva una sombra suave. Bordes de 1 px.
- **Radios**: tarjeta 14 px (`--radius-card`), control 10 px (`--radius-control`), paso 8 px (`--radius-step`).
- **Notas**: regla dorada lateral (`.decision-box`).
- **Iconos**: Lucide o `PhaseIcon`, línea de 1,5 px, sin relleno; complementan el texto, nunca lo reemplazan.
- **Sin** paleta nueva, degradados decorativos ni tema oscuro.

## Movimiento

Tokens en `registry/falp/themes/falp.css` y keyframes en `registry/falp/themes/falp-motion.css`:

| Uso | Token |
|---|---|
| Hover y color | `--motion-fast` (150 ms) con `ease` |
| Cambio de estado | `--motion-state` (160 ms) |
| Entrada de slide | `--motion-slide` / `--motion-fade` (220 ms) con `--ease-standard` |
| Movimiento que cruza la pantalla | `--ease-in-out` |
| Paneles laterales | `--ease-drawer` |
| Entrada de slide | `falp-slide-in` (respeta `data-direction="back"`) |
| Bloques | `falp-rise-in` + utilidad `stagger` (30 ms, tope 90 ms) |

Con movimiento reducido el tema ya deja solo el fundido. Si un deck necesita otro token, agrégalo en
`scripts/build-registry.mjs` (array `scales`) y regenera; nunca edites `falp.css` ni escribas milisegundos sueltos.
Los planes en `plans/001–008` documentan por qué cada regla es así.

## Divergencias conocidas con la skill

Los decks existentes se diseñaron antes de esta skill. No los corrijas sin que te lo pidan; repórtalas si las ves
en una revisión:

- **Tamaños**: el `.lead` usa `clamp(1rem, 1.25vw, 1.2rem)` (≈19 px a 1920) y el `.eyebrow` 0,75 rem (12 px). Para
  proyección en sala la skill pide cuerpo de 28–32 px y un mínimo de 18 px a 1080. En slides nuevas usa la escala de
  la skill; en las existentes, el script lo marcará como hallazgo.
- **Densidad**: algunas slides combinan título, lead, nota y panel con varias tarjetas; revisa el presupuesto de
  palabras.

## Plantilla para otro perfil

Copia este bloque a `perfiles/<marca>.md` y complétalo. Cada token lleva una línea de **cuándo usarlo y cuándo no**:
sin esa descripción el agente adivina entre nombres parecidos.

```markdown
# Perfil <marca>

- Fuente normativa: <manual, repo o archivo de tokens> (revisión <hash o fecha>)
- Contexto de lectura: <proyección / pantalla / móvil>
- Modo: <lienzo fijo escalado | slide responsiva>

| Rol | Token | Valor | Usar para / no usar para | Contraste |
|---|---|---|---|---|
| Fondo | | | | |
| Tinta | | | | |
| Estructura | | | | |
| Secundario | | | | |
| Acento | | | | |

- Tipografía: <título> + <cuerpo> (licencia, origen) · pesos: <…>
- Movimiento: <tokens de duración y curvas>
- Decisiones propias que se apartan de la skill: <valor, motivo>
- Deuda que no se toca: <lo que existe por razones históricas y no debe normalizarse>
```
