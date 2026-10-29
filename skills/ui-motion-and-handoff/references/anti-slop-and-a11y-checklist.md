# Tokens de Movimiento en CSS, Checklist Anti-Slop y Auditoría WCAG 2.2 de Handoff

## 1. Tokens de Movimiento y Ejemplo CSS (`motion.css`)

```css
:root {
  /* Curvas de movimiento (Emil Kowalski) */
  --ease-out-quart: cubic-bezier(0.165, 0.84, 0.44, 1);
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out-cubic: cubic-bezier(0.65, 0, 0.35, 1);

  /* Duraciones orientativas */
  --duration-instant: 100ms;
  --duration-fast: 150ms;
  --duration-normal: 220ms;
  --duration-slow: 300ms;
}

/* Declara las propiedades necesarias; esto no garantiza composición por GPU ni FPS. */
.btn-interactive {
  transition:
    transform var(--duration-fast) var(--ease-out-quart),
    background-color var(--duration-fast) var(--ease-out-quart),
    box-shadow var(--duration-fast) var(--ease-out-quart);
}

.btn-interactive:active:not(:disabled) {
  transform: scale(0.98);
  background-color: var(--button-active-bg);
  box-shadow: var(--button-active-shadow);
}

/* Entrada de Popover / Modal (desde 0.96, nunca desde 0) */
@keyframes surface-enter {
  from {
    opacity: 0;
    transform: scale(0.96) translateY(4px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Movimiento reducido: elimina escala/traslación; conserva feedback de color/sombra. */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  .btn-interactive {
    transition-property: background-color, box-shadow;
    transition-duration: 120ms !important;
  }

  /* Mismo selector que el estado active y regla posterior: vence en esta cascada. */
  .btn-interactive:active:not(:disabled) {
    transform: none !important;
  }

  /* Conserva el cambio de opacidad, pero elimina el movimiento espacial del keyframe. */
  @keyframes surface-enter {
    from { opacity: 0; transform: none; }
    to   { opacity: 1; transform: none; }
  }
}
```

`transform`/`opacity` son opciones preferidas para movimiento espacial, no una garantía universal de composición o rendimiento. `background-color` y `box-shadow` son excepciones de pintura explícitas usadas aquí para feedback; `clip-path`/`filter` requieren justificación y comprobación contextual. Evita `transition: all`; mide antes de informar FPS o aceleración por GPU.

## 2. Checklist de Destilación contra "AI Slop" (10 Puntos de Poda)

| # | Síntoma de AI Slop | Acción de Destilación (*Distill & Quieter*) |
| :--- | :--- | :--- |
| **1** | Gradientes neón violeta-azul-rosa en textos y fondos sin relación con la marca | Evaluar si expresan intención; si son decorativos y genéricos, considerar un color sólido de alta intención y un único *Star of the Show* |
| **2** | Tarjetas con borde + sombra pesada + fondo coloreado + icono en círculo coloreado en cada celda | Evaluar qué ornamentos sobran; dejar que la rejilla y el espaciado agrupen cuando sea suficiente |
| **3** | Badges y *pills* de colores en todas las tarjetas ("NEW", "AI-POWERED", "FAST") | Usar el 10% de *Highlighting* (Lidwell) como heurística, no como límite universal; reservar énfasis para anomalías o acciones relevantes |
| **4** | Titulares con todas las palabras en Inicial Mayúscula (*Title Case* artificial en español) | Considerar mayúscula inicial estándar de oración salvo nombres propios o guía de marca distinta |
| **5** | Simetría monótona de 3 tarjetas idénticas repetidas en la misma página | Revisar variaciones de patrón según contenido, no variar por variar |
| **6** | Iconos decorativos redundantes junto a cada etiqueta obvia | Conservar iconos cuando aceleran el escaneo o aportan redundancia semántica (WCAG 1.4.1) |
| **7** | Solo existe el estado ideal con textos de 3 palabras perfectamente simétricas | Probar con contenido real y diseñar `Empty`, `Loading` y `Error` cuando correspondan |
| **8** | Sombras negras opacas (`rgba(0,0,0,0.5)`) que ensucian el modo claro o son invisibles en modo oscuro | Comprobar si la sombra comunica jerarquía y es visible en el tema objetivo; preferir soluciones coherentes con sus superficies |
| **9** | Botones implementados con `<div class="btn">` sin soporte de `Tab`, `Enter` ni `Space` | Usar `<button type="button">` para acciones y `<a href="...">` para navegación |
| **10** | Controles pequeños pegados entre sí (ej. botón de cerrar o borrar fila) | Comprobar 24x24px CSS o una excepción válida para WCAG 2.5.8; 44x44px es el criterio AAA de 2.5.5 y puede servir como recomendación de comodidad, no como requisito AA |

## 3. Matriz de Verificación WCAG 2.2 para Developer Handoff

| Criterio WCAG 2.2 | Nivel | Regla Técnica de Verificación en Código / Figma |
| :--- | :--- | :--- |
| **SC 1.4.1 Use of Color** | A | Ningún estado de error, éxito o selección depende exclusivamente de cambiar un color; incluye icono o texto |
| **SC 1.4.3 Contrast (Minimum)** | AA | Texto normal `>= 4.5:1`, texto grande (`>= 24px` o `>= 18.66px bold`) `>= 3:1` |
| **SC 1.4.4 Resize Text** | AA | Fuentes en `rem` / `clamp()` con base `rem`; soporta zoom del `200%` sin cortar texto |
| **SC 1.4.10 Reflow** | AA | A `320px` de ancho CSS no aparece scroll horizontal en vistas de lectura (salvo tablas de datos o lienzos 2D) |
| **SC 1.4.11 Non-text Contrast** | AA | Bordes de inputs, estados de foco e iconos informativos tienen contraste `>= 3:1` contra la superficie adyacente |
| **SC 1.4.12 Text Spacing** | AA | Los contenedores usan `min-height` en lugar de `height` fijo para no truncar texto al ampliar el espaciado |
| **SC 2.3.3 Animation from Interactions** | AAA | Si se implementa el criterio, permite desactivar animaciones de interacción no esenciales; `prefers-reduced-motion` es una técnica posible, no una prueba automática del criterio |
| **SC 2.4.7 Focus Visible** | AA | La operación por teclado tiene una indicación visible del foco; evalúa el contexto y el componente |
| **SC 2.4.11 Focus Not Obscured (Minimum)** | AA | Al recibir foco, el componente no está totalmente oculto por contenido creado por el autor; comprobar overlays y cabeceras fijas |
| **SC 2.4.13 Focus Appearance** | AAA | Si se evalúa AAA, comprobar los requisitos de área y contraste de cambio de apariencia definidos por el criterio; un outline de 2px por sí solo no demuestra conformidad |
| **SC 2.5.7 Dragging Movements** | AA | Cualquier control con movimiento de arrastre ofrece una alternativa de puntero sin arrastre, salvo que el arrastre sea esencial |
| **SC 2.5.8 Target Size (Minimum)** | AA | Regla general: objetivo de al menos `24x24px` CSS. Evaluar las excepciones normativas: spacing, equivalent, inline, user-agent control y essential; no imponer 44x44 como AA |
| **SC 2.5.5 Target Size (Enhanced)** | AAA | `44x44px` CSS es el mínimo de este criterio AAA cuando se evalúa; no es requisito de SC 2.5.8 AA |
| **SC 4.1.2 Name, Role, Value** | A | Uso nativo de `<button>`, `<a href>`, `<label for>`, `aria-expanded`, `aria-live="polite"` en notificaciones |

Referencias normativas: [WCAG 2.2 SC 2.5.8](https://www.w3.org/TR/WCAG22/#target-size-minimum), [SC 2.4.11](https://www.w3.org/TR/WCAG22/#focus-not-obscured-minimum), [SC 2.4.13](https://www.w3.org/TR/WCAG22/#focus-appearance). Un borde de foco visible puede aportar evidencia para SC 2.4.7, pero no demuestra por sí solo SC 2.4.11 ni SC 2.4.13.
