# Escalas Matemáticas Alternativas, Fórmula `clamp()` y Recetas CSS

## 1. Escala Armónica por Raíces de la Proporción Áurea ($\sqrt{\phi} = 1.272$ / $\sqrt[3]{\phi} = 1.174$)

Esta progresión puede servir como punto de partida para sitios editoriales, marcas o portfolios que buscan un contraste más pronunciado en Desktop y una progresión suave en Mobile. Adáptala al contenido, la fuente y los dispositivos del proyecto:

| Token | Paso ($n$) | Desktop ($\times 1.272^n$, redond. 4px) | Mobile ($\times 1.174^n$, redond. 2px/4px) | `line-height` inicial | `letter-spacing` inicial |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `--text-display` | $+5$ | `56px` (`3.50rem`) | `36px` (`2.25rem`) | `1.08` | `-0.03em` |
| `--text-h1` | $+4$ | `44px` (`2.75rem`) | `30px` (`1.875rem`) | `1.14` | `-0.02em` |
| `--text-h2` | $+3$ | `32px` (`2.00rem`) | `26px` (`1.625rem`) | `1.20` | `-0.015em` |
| `--text-h3` | $+2$ | `26px` (`1.625rem`) | `22px` (`1.375rem`) | `1.25` | `-0.01em` |
| `--text-h4` | $+1$ | `20px` (`1.25rem`) | `18px` (`1.125rem`) | `1.35` | `-0.005em` |
| `--text-body` | $0$ | `16px` (`1.00rem`) | `16px` (`1.00rem`) | `1.50` | `0em` |
| `--text-body-sm` | $-1$ | `14px` (`0.875rem`) | `14px` (`0.875rem`) | `1.43` | `+0.005em` |
| `--text-caption` | $-2$ | `12px` (`0.75rem`) | `12px` (`0.75rem`) | `1.33` | `+0.02em` |

## 2. Fórmula para Calcular `clamp()` con Componente en `rem`

Para interpolar linealmente entre un tamaño mínimo $S_{\min}$ (en `rem`) a un viewport $V_{\min}$ (en `rem`, ej. $375\text{px} / 16 = 23.4375\text{rem}$) y un tamaño máximo $S_{\max}$ a un viewport $V_{\max}$ (ej. $1280\text{px} / 16 = 80\text{rem}$):

$$\text{Slope } (m) = \frac{S_{\max} - S_{\min}}{V_{\max} - V_{\min}}$$

$$\text{Intercept } (b) = S_{\min} - (m \times V_{\min})$$

$$\text{CSS} = \texttt{clamp(} S_{\min}\text{rem, } b\text{rem + } (m \times 100)\text{vw, } S_{\max}\text{rem)}$$

> Incluir un componente en `rem` puede ayudar a que el valor fluido responda al tamaño de texto base/preferencias. Es una recomendación de implementación, no una prueba de SC 1.4.4; comprueba el comportamiento de redimensionado aplicable en el producto.

## 3. Hoja de Estilos Base (`typography.css`, ilustrativa)

```css
:root {
  /* Ejemplo de escala fluida 375px -> 1280px; adapta al proyecto. */
  --text-display: clamp(2.5rem, 1.98rem + 2.21vw, 3.75rem);
  --text-h1: clamp(2rem, 1.59rem + 1.77vw, 3rem);
  --text-h2: clamp(1.75rem, 1.54rem + 0.88vw, 2.25rem);
  --text-h3: clamp(1.5rem, 1.4rem + 0.44vw, 1.75rem);
  --text-h4: clamp(1.25rem, 1.15rem + 0.44vw, 1.5rem);
  --text-h5: clamp(1.125rem, 1.07rem + 0.22vw, 1.25rem);
  --text-body-lg: clamp(1rem, 0.95rem + 0.22vw, 1.125rem);
  --text-body: 1rem;
  --text-body-sm: 0.875rem;
  --text-caption: 0.75rem;
  --text-overline: 0.75rem;

  /* Medidas orientativas de lectura */
  --measure-narrow: 45ch;
  --measure-reading: 65ch;
  --measure-wide: 75ch;
}

h1, .h1, h2, .h2, h3, .h3, h4, .h4 {
  text-wrap: balance;
  color: var(--text-primary);
}

h1, .h1 {
  font-size: var(--text-h1);
  line-height: 1.15;
  letter-spacing: -0.02em;
  font-weight: 700;
}

h2, .h2 {
  font-size: var(--text-h2);
  line-height: 1.2;
  letter-spacing: -0.015em;
  font-weight: 600;
}

h3, .h3 {
  font-size: var(--text-h3);
  line-height: 1.28;
  letter-spacing: -0.01em;
  font-weight: 600;
}

p, .body-copy {
  font-size: var(--text-body);
  line-height: 1.55;
  letter-spacing: 0em;
  max-width: var(--measure-reading);
  text-wrap: pretty;
  color: var(--text-secondary);
}

.overline {
  font-size: var(--text-overline);
  line-height: 1.33;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 600;
}
```

> Estos valores son ejemplos de CSS, no resultados de pruebas. Para SC 1.4.12 comprueba simultáneamente los cuatro overrides (`line-height: 1.5`, espaciado entre párrafos `2em`, `letter-spacing: 0.12em`, `word-spacing: 0.16em`) y que no se pierda contenido. Para SC 1.4.4 comprueba el redimensionado/zoom pertinente (incluido 200% cuando aplique); una unidad CSS por sí sola no demuestra cumplimiento.
