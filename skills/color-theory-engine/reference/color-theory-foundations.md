# Color Theory Foundations & Mathematics

Para manipular el color programáticamente, debemos mapear conceptos visuales a espacios de color matemáticos.

## 1. Color Spaces

### RGB (Red, Green, Blue)
El estándar para pantallas digitales. Es un modelo aditivo. Útil para hardware, pero no es perceptivo (un punto medio matemático en RGB no parece un punto medio visual para el ojo humano).

### HSL (Hue, Saturation, Lightness)
Representación cilíndrica de RGB.
- **Hue (Matiz)**: Grado en la rueda de colores (0-360). 0=Rojo, 120=Verde, 240=Azul.
- **Saturation (Saturación)**: Distancia desde el centro (0-100%).
- **Lightness (Luminosidad)**: Eje vertical (0-100%).

### CIELAB (L*a*b*)
Espacio de color perceptualmente uniforme diseñado para aproximarse a la visión humana.
- **L***: Luminosidad perceptual (0 = negro, 100 = blanco).
- **a***: Eje Verde-Rojo.
- **b***: Eje Azul-Amarillo.
*Usa LAB cuando necesites calcular deltas de color precisos o generar degradados UI suaves.*

## 2. Mathematical Harmonies (HSL-based)
Las armonías se calculan manteniendo la Saturación y Luminosidad constantes mientras se rota matemáticamente el valor de Hue (H).

* **Complementary**: `(H + 180) % 360`
* **Analogous**: `(H - 30) % 360` y `(H + 30) % 360`
* **Triadic**: `(H + 120) % 360` y `(H + 240) % 360`
