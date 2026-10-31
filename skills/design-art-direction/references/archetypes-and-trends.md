# Catálogo Extendido de Arquetipos Estéticos, Rima Visual y Tendencias

## 1. Matriz Técnica de los 6 Arquetipos Estéticos

| Dimensión | 1. Minimalismo Industrial | 2. Precisión de Alta Ingeniería | 3. Calidez Orgánica | 4. Editorial Audaz | 5. Deconstrucción Conceptual | 6. Escala Cinemática |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Relación Fondo/Figura** | Alto espacio blanco (`>= 50%`), superficies luminosas | Oscuridad profunda (`#0B0F17`), figuras emergen por luz | Fondos cálidos (`#FAF6F0`), contraste suave sin dureza | Contraste extremo Blanco/Negro o bloque cromático | Estructura visible, grillas de `1px` expuestas | Atmósfera envolvente, viñeteado sutil, escala monumental |
| **Bordes y Radios** | Continuos (*squircle*) `12px-24px` | Nítidos `4px-8px`, bisel técnico de `1px` | Redondeados suaves `16px-32px` | Rectos `0px-2px` en fotos, cortes editoriales | Rectos `0px` o industriales con marcas de corte | Rectos o micro-radio `2px-4px`, proporción 21:9 / 16:9 |
| **Tratamiento de Luz** | Cenital difusa, sombras largas de baja opacidad | Emisión de luz interna (glow controlado en datos clave) | Luz solar matutina lateral, sombras coloreadas cálidas | Luz de estudio dura, sombras recortadas | Plana de plano técnico / blueprint | Contraluz dramático, neblina volumétrica sutil |
| **Motivo de Rima Visual** | Curvatura del hardware replicada en tarjetas y botones | Ángulos de `45°` o indicadores tipo telemetría en esquinas | Formas botánicas/arcos suaves en máscaras de imagen y badges | Contraste entre filetes finos (`0.5px`) y bloques gruesos | Comillas `"..."`, numeración de serie `01 / 04`, coordenadas | Líneas de horizonte y escalas de tiempo milimétricas |

## 2. Recetas CSS Opcionales para Capas de Profundidad Táctil

Usa ninguna, una o ambas recetas solo cuando el brief justifique su función o identidad. Son opciones, no una composición predeterminada.

### Opción de Capa 1: Micro-Textura de Grano Analógico (SVG Data URI sin peticiones externas)

```css
.surface-grain {
  position: relative;
}
.surface-grain::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.03; /* Mantener siempre entre 0.02 y 0.04 */
  mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
```

### Opción de Capa 2: Glassmorphism Funcional con Borde Especular Direccional

```css
.surface-glass {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px) saturate(140%);
  -webkit-backdrop-filter: blur(12px) saturate(140%);
  /* Luz cenital: borde superior más brillante que los laterales e inferior */
  border-top: 1px solid rgba(255, 255, 255, 0.16);
  border-left: 1px solid rgba(255, 255, 255, 0.10);
  border-right: 1px solid rgba(255, 255, 255, 0.06);
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.28);
}
```

## 3. Incorporación Crítica de Tendencias (Filtro de Longevidad)

Toda tendencia visual (Bento Grids, tipografía cinética, gradientes de malla, cursores personalizados, texturas 3D) debe pasar por **3 preguntas de validación** antes de entrar en la dirección de arte:

1. **¿Refuerza la Semilla Narrativa?** Si la tendencia es intercambiable con cualquier otra landing page de IA o cripto, descártala.
2. **¿Respeta el presupuesto de rendimiento y lectura?** Ningún efecto de fondo debe degradar el LCP ni reducir el contraste de texto por debajo de WCAG AA; verifica con evidencia pertinente al proyecto.
3. **¿Pasa la prueba de envejecimiento de 24 meses?** Considera las tendencias como acento y contrástalas con principios de proporción y legibilidad. La proporción de acento es una heurística, no un requisito universal.
