# Color

El color en una slide sirve para tres cosas: dar identidad, separar zonas y señalar el foco. Cada color que no hace
una de las tres compite con el que sí.

## 1. Roles, no colores

Define la paleta por **rol**, como tokens del perfil. El nombre del token dice para qué se usa, no qué color es.

| Rol | Proporción orientativa | Uso |
|---|---|---|
| Fondo y superficies neutras | ~60 % | Fondo de la slide, tarjetas, separadores |
| Estructura de marca | ~30 % | Títulos, bloques de sección, iconos, gráficos |
| Acento | ~10 % | El punto focal de la slide, y nada más |
| Semánticos | Según necesidad | Éxito, alerta, error, estado; no se usan como decoración |

La proporción 60-30-10 es una guía de composición, no una ley: sirve para detectar cuándo el acento dejó de ser
acento.

## 2. Un acento por slide

- El acento marca **una sola cosa** por slide: la cifra, la palabra clave del título, la opción recomendada, el
  paso actual. Si aparece en tres lugares, ya no señala nada.
- No uses el acento para decorar (barras, fondos, iconos que no son el foco).
- Si el perfil tiene un acento de bajo contraste (amarillo, cian claro), úsalo como relleno o subrayado detrás de
  texto oscuro, o compleméntalo con un contorno y una etiqueta oscuros; nunca como color de texto sobre fondo claro.

## 3. Contraste con margen para proyección

Requisitos WCAG 2.2:

- Texto normal **4,5:1**; texto grande (≥ 24 px, o ≥ 18,66 px en negrita) **3:1**.
- Elementos gráficos con significado y bordes de controles **3:1** (criterio 1.4.11).
- El color nunca es la única señal: un estado o una categoría también se distinguen con texto, forma, posición o
  contorno (criterio 1.4.1).

Para slides apunta más alto. Un proyector en una sala iluminada aplana el contraste: lo que en el monitor da 4,5:1
puede leerse como mucho menos en la pared. Objetivos de trabajo (heurística, no requisito):

- Cuerpo y títulos: **≥ 7:1**.
- Etiquetas, fuentes y textos secundarios: **≥ 4,5:1** aunque sean grandes.

Mide sobre el color **efectivo**: si el texto tiene opacidad o el fondo es un tinte semitransparente, calcula el
color resultante. El script de revisión lo hace para fondos sólidos y semitransparentes, y en los degradados toma la
peor parada de color. Texto sobre **imagen** queda **sin medir**: pon una capa sólida detrás del texto o revisa la
captura a mano y decláralo.

## 4. Claro u oscuro

- Sala iluminada, proyector modesto o lectura posterior en pantalla: **fondo claro**.
- Sala oscura, pantalla LED o escenario: el fondo oscuro cansa menos y hace brillar el acento.
- Un deck usa **un solo modo**. Una slide oscura aislada (por ejemplo, una sección o una cita) funciona como
  pausa, pero no alternes.

## 5. Calibración

- Evita blanco y negro puros si el perfil lo permite: un blanco papel (#F5F9FD, #FAFAF7) y una tinta muy oscura
  (#12385F, #1A1A1A) se ven más editoriales y cansan menos.
- El carácter de una paleta depende más de la saturación y del brillo que del tono. Si se ve estridente, baja la
  saturación antes de cambiar de color.
- Amplía la paleta con **tintes del mismo color** (por ejemplo al 5, 15 y 40 %) para fondos de tarjeta y bordes, en
  vez de agregar colores nuevos.
- Sin degradados decorativos ni sombras en cada tarjeta. La profundidad se logra con superficies y líneas
  finas; una sombra suave, si acaso, separa el marco de la presentación del fondo.

## 6. Gráficos y diagramas

- Los datos usan los colores de estructura; el acento marca la serie o el valor del que habla el título. El resto de
  las series van en grises o tintes.
- Para gráficos con varias categorías, carga la skill `dataviz` y valida la paleta con su script.
