# Movimiento mínimo

En una presentación el movimiento tiene un solo trabajo: **orientar**. Dice que la slide cambió, en qué dirección se
avanzó y, a veces, en qué orden leer. El presentador avanza decenas de veces por sesión, así que cualquier espera se
multiplica. Todo lo que no orienta, distrae.

## 1. Qué se anima y qué no

| Situación | Movimiento | Por qué |
|---|---|---|
| Cambio de slide | Fundido + desplazamiento corto (6–16 px) en la dirección del avance | Señala el cambio y la dirección |
| Bloques al entrar la slide | Fundido con escalonado corto, opcional | Sugiere orden de lectura |
| Build progresivo (paso a paso) | Solo si el orden es parte del argumento | Evita que el público lea el final antes de tiempo |
| Cambio de estado (activo, hover, seleccionado) | Solo color, 150–160 ms | Respuesta inmediata |
| Pulsar un control | `scale(0.97)` breve | Confirma la pulsación |
| Barra de progreso | `transform: scaleX()` con la duración del cambio de slide | Sin recalcular layout |
| Paleta de comandos, buscador | Nada | Se abre muchas veces seguidas |
| Decoración continua (loops, parallax, partículas, texto que rebota) | Nada | Compite con quien habla |

## 2. Duraciones y curvas

- Cambio de estado: **150–160 ms**. Entrada de slide: **200–250 ms**. Ningún elemento de una slide sobre
  **400 ms**.
- Escalonado: pasos de **30 ms**, tope en **90 ms** (el último bloque visible ≤ ~310 ms después de pulsar).
- La salida es más rápida que la entrada (o instantánea): el sistema cede el paso.
- Curvas:
  - Entrada de elementos: *ease-out* (por ejemplo `cubic-bezier(0.2, 0, 0, 1)`). Arranca rápido, que es cuando se
    espera respuesta.
  - Movimiento que cruza la pantalla (progreso, paneles): *ease-in-out*.
  - Cambios de color: `ease`.
  - Nunca `linear` para movimiento espacial (se ve mecánico), salvo progreso continuo de tiempo.
- Duraciones y curvas son **tokens** del perfil; nunca milisegundos sueltos en las reglas.

## 3. Propiedades

- Anima solo **`opacity` y `transform`**. Animar `width`, `height`, `top`, `margin` o `box-shadow` recalcula layout o
  repinta en cada cuadro y se ve entrecortado en equipos modestos o en proyección por HDMI de un notebook.
- Nunca `transition: all`: anima cosas que no se pretendía animar (el ancho del punto de navegación activo, por
  ejemplo). Enumera las propiedades.
- Desplazamientos pequeños (6–16 px). Un objeto que viaja media pantalla obliga al ojo a seguirlo.
- Sin `scale` de entrada mayor que 0,95 → 1, ni rotaciones o rebotes.

## 4. Hover y punteros

- En proyección el puntero del presentador pasa por encima de todo. Los elementos **no interactivos no reaccionan al
  hover**.
- Los desplazamientos en hover solo dentro de `@media (hover: hover) and (pointer: fine)`; en pantallas táctiles el
  hover se queda «pegado».
- El cambio de color en hover vale para todos los punteros.

## 5. Movimiento reducido

Con `prefers-reduced-motion: reduce`, **menos movimiento no es ningún movimiento**:

- Se quitan desplazamientos, escalonados y escalas.
- Se **conserva un fundido de opacidad** (~150 ms) al cambiar de slide, para que el cambio siga siendo perceptible.
- Las transiciones de hover y estado pueden ser instantáneas.

```css
@media (prefers-reduced-motion: reduce) {
  @keyframes slide-in { from { opacity: 0; } to { opacity: 1; } }
  .stagger > * { animation-delay: 0ms; }
}
```

## 6. Builds progresivos

Úsalos cuando revelar todo de una vez arruina el argumento: una pregunta antes de la respuesta, los pasos de un
proceso que se explican uno por uno, un antes y después. Reglas:

- Cada paso de build lo dispara el presentador (tecla), no un temporizador.
- El estado final de la slide debe ser legible por sí solo (impresión, respaldo, PDF).
- Los elementos aún no revelados ocupan su lugar (sin saltos de layout): `opacity: 0` o `visibility: hidden`, no
  `display: none`.
- Si el deck exporta a PDF o se imprime, todo se muestra (`@media print`).

## 7. Verificación

- DevTools › Animations al 10 %: solo `opacity`/`transform` en entradas y solo color en estados.
- El script de revisión lista las animaciones activas de cada slide con su duración y propiedades, y repite la
  medición con `prefers-reduced-motion: reduce` para avisar si queda algún desplazamiento.
- Avanza 10 slides seguidas rápido: nada debe sentirse lento ni acumularse.
