# El recorrido del taller

Panel original en HTML, CSS y JavaScript, sin dependencias ni recursos remotos. La fuente está implementada y las comprobaciones descritas abajo se ejecutaron. La inspección y la interacción en un navegador real quedan pendientes porque este entorno no dispone de un motor instalado.

## Uso

1. Mantén `index.html`, `styles.css` y `script.js` juntos y abre `index.html` en un navegador moderno. No requiere instalación, servidor ni conexión.
2. Elige **Preparar**, **Explorar**, **Construir** o **Compartir** para ver su descripción, pregunta guía y resultado propuesto. Elegir una etapa detiene la reproducción.
3. **Reproducir** inicia desde la etapa elegida. El botón cambia a **Pausar**; al detenerlo, **Reanudar** conserva el tiempo que quedaba en esa etapa.
4. **Reiniciar** vuelve a Preparar y deja el recorrido detenido. Para recorrer las cuatro etapas desde el principio, pulsa Reiniciar y después Reproducir.

Cada etapa permanece seis segundos; un recorrido completo dura 24 segundos de tiempo activo. Al terminar, **Repetir recorrido** inicia de nuevo desde Preparar. La barra muestra la posición de la etapa: 25 %, 50 %, 75 % y 100 %. No representa tareas realmente completadas por las personas del taller.

La reproducción comienza solo mediante una acción de la persona. Salir de la pestaña o de la página la pausa. Con movimiento reducido se eliminan las transiciones y sigue disponible la secuencia con cambios instantáneos. Activar esa preferencia durante la reproducción la pausa; reanudar requiere otra acción.

Los selectores y controles son botones nativos: usa Tab para recorrerlos y Enter o Espacio para activarlos. Se han incluido foco visible, selección expresada con texto y `aria-pressed`, una barra `progress` y avisos de estado. La conducta de teclado y lector de pantalla aún necesita comprobarse en navegador.

## Decisiones de diseño

Tipografía del sistema, fondo claro `#f3f6f3`, texto oscuro `#172c2a` y acento verde azulado `#086f67`. El recorrido precede a la descripción; la pregunta guía acompaña la etapa y los controles están junto al avance. La cuadrícula está configurada para pasar de cuatro a dos columnas y el contenido a una columna en espacios estrechos. Esta adaptación está implementada en CSS, pero no se ha inspeccionado su render.

El contenido es una propuesta genérica de facilitación, editable en el arreglo `stages` de `script.js`. Si cambias la primera etapa, actualiza también su contenido inicial en `index.html`. La duración se controla con `STEP_MS`; si la cambias, actualiza la ayuda visible de seis segundos en HTML.

## Comprobaciones ejecutadas y límites

Entorno observado el 23 de octubre de 2026: Node v24.19.0 y Python 3.12.14. Se aplicó el procedimiento `disenar`, con sus referencias de dirección, web, movimiento y verificación.

| Comprobación | Método y cobertura | Estado |
| --- | --- | --- |
| Sintaxis JavaScript | `node --check script.js` terminó con código 0. | PASS |
| Conducta del recorrido | `node verificar.cjs`: 10 pruebas ejecutadas sobre `script.js`, con DOM mínimo y reloj simulados. Cubren selección de las cuatro etapas, avance, final, repetición, pausa con tiempo restante, reinicio, cancelación al seleccionar, preferencia de movimiento inicial y dinámica, ocultación, salida y activaciones rápidas. | PASS |
| Estructura estática HTML | Python `HTMLParser`: idioma español, identificadores únicos, referencias a identificadores existentes, seis botones nativos y script local. No es validación completa del estándar HTML. | PASS |
| Recursos locales | Lectura de fuentes y comprobaciones de archivos: HTML enlaza únicamente CSS y JS locales; no hay importaciones, fuentes externas ni llamadas de red en esas fuentes. | PASS |
| Contraste de pares declarados | Helper `contrast.py` del procedimiento: nueve pares de texto con umbral 4,5:1 y un par barra/carril con umbral 3:1. Valores completos en `contraste.json`. | PASS |
| Reglas de movimiento reducido | Lectura y detección de reglas CSS; pruebas de la lógica del evento `change` mediante el doble de `MediaQueryList`. No prueba cómo el navegador dibuja o aplica las reglas. | PASS |
| Render e interacción en navegador | Playwright está disponible, pero faltan los ejecutables que declara en las revisiones `chromium-1234`, `firefox-1538` y `webkit-2336`; tampoco hay Chromium, Chrome o Firefox en PATH. No se instaló un navegador. | BLOCKED |
| Reflujo, ampliación, espaciado, foco visible y teclado real | La ausencia de motor impide inspección visual y activación nativa. No se afirman resultados por las declaraciones CSS o por los dobles del DOM. | BLOCKED |
| Reproducción observada y temporización real | Solo se ejecutó tiempo simulado: no se observó una secuencia de 24 segundos ni se midió fluidez o latencia de un navegador. | BLOCKED |
| Lectores de pantalla, dispositivos físicos y pruebas con personas | No se ejecutaron esas pruebas. | NOT_RUN |
| Publicación o despliegue | Fuera del encargo. | NOT_APPLICABLE |

El menor contraste calculado entre los pares de texto es **5,312140:1**; barra/carril obtiene **4,791160:1**. Los cálculos abarcan colores sRGB opacos y uniformes. No evalúan tamaño efectivo, antialiasing, bordes decorativos ni accesibilidad global.

Para repetir las comprobaciones de lógica y sintaxis desde esta carpeta:

```sh
node --check script.js
node verificar.cjs
```

`resultados-node.txt` conserva la salida de las diez pruebas. El comprobador no sustituye un navegador: simula los eventos y el paso del tiempo, y no calcula estilos, distribución ni semántica accesible del motor.

## Referencias técnicas

Se consultaron fuentes primarias para la preferencia de movimiento y su actualización durante la ejecución:

- [CSS Media Queries, prefers-reduced-motion](https://drafts.csswg.org/mediaqueries-5/#prefers-reduced-motion).
- [CSSOM View, MediaQueryList y evento change](https://drafts.csswg.org/cssom-view/#the-mediaquerylist-interface).

Se usaron las funciones estables descritas por esos documentos, sin incorporar las APIs experimentales de preferencias que también figuran en los borradores. Todo el diseño, los textos y los iconos SVG de la pieza se crearon para este encargo.

## Archivos

- `index.html`: entrada del panel y contenido inicial.
- `styles.css`: diseño, adaptación a ancho y reglas de movimiento reducido.
- `script.js`: contenido de etapas, estado y temporizadores.
- `verificar.cjs`: comprobaciones reproducibles en Node, sin paquetes externos.
- `resultados-node.txt`: salida real de las pruebas.
- `contraste.json`: resultados completos de los diez pares calculados.
- `README.md`: uso, decisiones, comprobaciones y límites.
