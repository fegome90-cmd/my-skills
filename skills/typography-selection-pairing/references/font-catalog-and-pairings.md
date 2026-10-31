# Catálogo Inicial de Candidatas y Emparejamientos Tipográficos

## 1. Candidatas para UI, Cuerpo y Datos (Font Follows Function)

Las familias de la tabla son candidatas para investigar, no propiedades técnicas ya verificadas. Altura-x y notas de glifos son indicios orientativos; comprueba pesos/estilos, idioma y glifos requeridos, features, archivos y licencia en fuentes primarias antes de afirmarlo o seleccionarlas para el proyecto. Registra las fuentes consultadas.

| Familia | Categoría | Altura-x (orientativa) | Pista de desambiguación `1Il` / `0O` | Posible aplicación |
| :--- | :--- | :--- | :--- | :--- |
| **Inter** | Neo-Grotesca UI | Alta (`0.53`, por verificar) | Investigar variantes `cv05`, `cv08`, `zero` | SaaS, dashboards densos y sistemas de diseño |
| **Plus Jakarta Sans** | Geométrica Humanista | Alta (`0.52`, por verificar) | Revisar muestra de glifos requerida | Interfaces modernas; posible monofuente o Body |
| **IBM Plex Sans** | Grotesca Técnica | Media-Alta (`0.52`, por verificar) | Revisar diseño de `1`, `I`, `l` en la versión usada | Banca, salud e ingeniería |
| **Source Sans 3** | Humanista | Media-Alta (`0.50`, por verificar) | Revisar muestra de glifos requerida | Lectura prolongada; posible par con *Source Serif 4* |
| **Atkinson Hyperlegible** | Humanista Accesible | Alta (`0.53`, por verificar) | Investigar distinción de glifos en la versión usada | Interfaces con necesidades de legibilidad específicas |
| **Geist / Geist Mono** | Neo-Grotesca Técnica | Alta (`0.53`, por verificar) | Revisar muestra de glifos requerida | Interfaces de desarrollo, terminales y telemetría |

## 2. Candidatas para Titulares y Dirección de Arte (Font Follows Feeling)

Los ejemplos orientan una búsqueda de tono y emparejamiento; no verifican propiedades, licencia ni disponibilidad de archivos.

| Familia | Categoría | Personalidad / Arquetipo (orientativo) | Posible emparejamiento (Body/UI) |
| :--- | :--- | :--- | :--- |
| **Instrument Serif** | Serif Condensada Editorial | Sofisticada, intelectual, *Editorial Audaz* / *Minimalismo* | *Inter* o *Instrument Sans* |
| **Fraunces** | Old-Style Soft Serif (investigar `WONK`, `opsz`) | Cálida, expresiva, *Calidez Orgánica* | *Plus Jakarta Sans* o *Work Sans* |
| **Newsreader** | Serif Editorial (investigar eje `opsz`) | Periodística, literaria, ensayos y lectura profunda | *Inter* o *Source Sans 3* |
| **Space Grotesk** | Sans Geométrica idiosincrática | Tecnológica, brutalista sutil, *Precisión de Ingeniería* | *Inter* o *IBM Plex Sans* |
| **Syne** | Display Art-House | Cultural, vanguardista, *Deconstrucción* / *Editorial* | *Plus Jakarta Sans* o *DM Sans* |
| **Cabinet Grotesk / Satoshi** | Sans Geométrica Contemporánea | Limpia, arquitectónica, startups y productos digitales | Monofuente o combinada con *JetBrains Mono* |

## 3. Receta CSS de Higiene Tipográfica y OpenType Features

Ejemplo ilustrativo; comprueba los archivos y features de las fuentes seleccionadas antes de activar ejes o features específicos.

```css
:root {
  --font-display: 'Instrument Serif', Georgia, serif;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', 'IBM Plex Mono', monospace;
}

/* Activa features de desambiguación solo si la fuente y el diseño las soportan. */
body {
  font-family: var(--font-sans);
  /* Ejemplo sujeto a comprobar en la fuente elegida: */
  /* font-feature-settings: "cv05" 1, "cv08" 1; */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Aplica tabular-nums solo donde los datos requieran cifras alineadas. */
.numeric-data {
  font-variant-numeric: tabular-nums lining-nums;
  font-feature-settings: "tnum" 1, "lnum" 1;
}
```
