# Catálogo de 25 Patrones de Layout y Recetas CSS Grid

Los patrones y cálculos siguientes son referencias para adaptar al contenido, densidad, viewport y tarea. Las tablas de spans y el código CSS suponen como ejemplo una rejilla 12-8-4; no son un layout obligatorio ni un estándar universal.

## 1. Tabla de Ejemplo de Colapso Responsivo (Preset 12-8-4)

| # | Patrón de Layout | Columnas Desktop (`12 col`) | Columnas Tablet (`8 col`) | Columnas Mobile (`4 col`) | Caso de Uso Posible |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | Hero Centrado Focal | `Span 8` (offset 2) + Media `Span 10` | `Span 8` | `Span 4` | SaaS, lanzamientos de producto, demostraciones visuales, si hay Hero |
| **2** | Columna Editorial (`65ch`) | `Span 8` (max `680px` centrado) | `Span 6` (offset 1) | `Span 4` | Artículos, documentación, historias de marca |
| **3** | Banner Full-Bleed | `100vw` con contenido en `Span 10` | `100vw` (`Span 8`) | `100vw` (`Span 4`) | Llamadas a la acción globales, cierres de página |
| **4** | Flujo Vertical Timeline | `Span 8` con eje vertical izquierdo | `Span 8` | `Span 4` | Procesos clínicos/técnicos, hojas de ruta, historia |
| **5** | Contenedor Focal de Tarea | `Span 4` o `Span 6` centrado (`max 480px`) | `Span 6` centrado | `Span 4` | Login, onboarding, calculadoras, checkout paso a paso |
| **6** | Split Hero Asimétrico | `Span 7` (Copy) + `Span 5` (Visual) | `Span 8` apilado | `Span 4` apilado | Propuesta de valor + formulario o vista previa de app |
| **7** | Zig-Zag Alternado | `Span 5` + `Span 6` (offset 1, alternando) | `Span 4 + Span 4` o apilado | `Span 4` (Visual -> Copy) | Explicación detallada de beneficios con capturas |
| **8** | Sticky Narrative Scroll | `Span 5` (`sticky`) + `Span 7` (scroll) | `Span 8` apilado | `Span 4` apilado | Storytelling interactivo, desgloses de arquitectura |
| **9** | Comparativa Lado a Lado | `Span 6` + `Span 6` | `Span 4` + `Span 4` | `Span 4` apilado o tabs | Antes vs. Después, comparación de planes o enfoques |
| **10** | Sidebar + Workspace | `280px` fijo + `1fr` (fluido) | Drawer colapsable + `Span 8` | Bottom Nav / Drawer + `Span 4` | Dashboards, IDEs, sistemas de historia clínica, wikis |
| **11** | Tríada de Valor | `3 x Span 4` | `Span 8` (1 destacada + 2 abajo) | `3 x Span 4` apiladas | 3 pilares del producto, 3 características principales |
| **12** | Matriz de Precios (3 Tiers) | `3 x Span 4` (central elevada `-8px`) | `Span 8` apilado (Destacado 1ro) | `Span 4` apilado | Planes de suscripción Free / Pro / Enterprise |
| **13** | Bento Grid 3 Celdas | Fila 1: `8 + 4`; Fila 2: `4 + 8` | `4 + 4` | `Span 4` apilado | Resumen de capacidades heterogéneas con ritmo visual |
| **14** | Feed Editorial Destacado | `Span 6` (Principal) + `2 x Span 3` | `Span 8` + `2 x Span 4` | `Span 4` apilado | Portadas de noticias, blogs, publicaciones científicas |
| **15** | Panel en 3 Bandas (Master-Detail) | `260px` + `1fr` + `320px` | `240px` + `1fr` (Inspector en drawer) | Navegación por vistas (`Span 4`) | Clientes de correo, gestores de tickets, diseño UI |
| **16** | Banda de KPIs / Métricas | `4 x Span 3` | `2 x Span 4` (`2x2`) | `2 x Span 2` (`2x2`) | Estadísticas clave, telemetría en tiempo real |
| **17** | Catálogo / Galería | `4 x Span 3` | `2 x Span 4` | `2 x Span 2` o `1 x Span 4` | E-commerce, bibliotecas de plantillas o componentes |
| **18** | Bento Grid Modular 4x | Celdas `2x2` (`Span 6`) + `1x1` (`Span 3`) | Celdas `Span 8` y `Span 4` | `Span 4` apilado | Showcases para especificaciones |
| **19** | Matriz de Testimonios / Equipo | `4 x Span 3` | `2 x Span 4` | Carrusel horizontal o `Span 4` | Prueba social, directorio de especialistas |
| **20** | Mega-Footer en 4 Pilares | `Span 3` (Marca) + `3 x Span 3` (Links) | `2 x Span 4` | Acordeón o `2 x Span 2` | Navegación de cierre, enlaces legales y mapa del sitio |
| **21** | Cinta de Logos (Social Proof) | `5 a 7` columnas `flex` / `grid` | `3 a 4` por fila | `2 a 3` por fila o marquee | Logos de clientes, certificaciones, universidades |
| **22** | Matriz de Integraciones | `6 x Span 2` | `4 x Span 2` | `2 x Span 2` | Ecosistema de conectores, plugins, APIs |
| **23** | Tabla de Datos Densa | `Span 12` (`table-layout: fixed`) | Scroll-x con 1ra col `sticky` | Cards resumidas o 1ra col `sticky` | Registros financieros, logs, resultados de laboratorio |
| **24** | Tablero Kanban Multi-Etapa | `N x 300px` en scroll horizontal | `N x 280px` scroll-x | Vista por columna con selector/tabs | Gestión de flujos de trabajo y estados de tareas |
| **25** | Galería Masonry / Mosaico | `4 a 5` columnas de altura variable | `3` columnas | `2` columnas | Inspiración visual, fotografía, moodboards |

> Adapta las columnas y spans de la tabla a la grilla elegida. Las alternativas responsive también dependen del contenido y deben comprobarse para los viewports que importen.

## 2. Implementación CSS Ilustrativa (Preset 12-8-4 y Variables de Espaciado)

Este CSS ilustra un preset posible. Cambia columnas, breakpoints, gutters, márgenes y pasos espaciales para ajustarlos al proyecto; no es una receta normativa.

```css
:root {
  /* Preset opcional: valores iniciales Desktop */
  --grid-columns: 12;
  --grid-gutter: 24px;
  --grid-margin: 64px;
  --container-max: 1280px;

  /* Un ejemplo de escala de agrupación, ajustable al contenido */
  --space-micro: 16px;   /* Intra-componente */
  --space-meso: 32px;    /* Entre grupos cercanos */
  --space-macro: 104px;  /* Entre secciones */
}

@media (max-width: 1023px) {
  :root {
    /* Ejemplo Tablet */
    --grid-columns: 8;
    --grid-gutter: 20px;
    --grid-margin: 32px;
    --space-micro: 14px;
    --space-meso: 24px;
    --space-macro: 72px;
  }
}

@media (max-width: 767px) {
  :root {
    /* Ejemplo Mobile */
    --grid-columns: 4;
    --grid-gutter: 16px;
    --grid-margin: 16px;
    --space-micro: 12px;
    --space-meso: 20px;
    --space-macro: 56px;
  }
}

.layout-grid {
  display: grid;
  grid-template-columns: repeat(var(--grid-columns), minmax(0, 1fr));
  gap: var(--grid-gutter);
  max-width: var(--container-max);
  margin-inline: auto;
  padding-inline: var(--grid-margin);
}

.section-block {
  padding-block: var(--space-macro);
}
```
