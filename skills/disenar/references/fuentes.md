# Procedencia y fuentes

Revisión de esta síntesis: **23 de octubre de 2026**. El procedimiento es propio y transversal. Las fuentes informan criterios concretos; no son dependencias de ejecución ni catálogos obligatorios. Consulta documentación primaria vigente cuando cambien versiones, APIs o formatos. Las revisiones de repositorios indicadas fijan lo examinado, no garantizan su estado futuro.

## Material del usuario

| Fuente examinada | Revisión | Aporte y tratamiento |
|---|---|---|
| [my-skills](https://github.com/fegome90-cmd/my-skills/tree/df8fc14837c5b9566ffe231640958586bfe2832f) | `df8fc14837c5b9566ffe231640958586bfe2832f` | Diseño de slides, dirección visual, narrativa, diagramas y componentes. Se preserva criterio de composición y evidencia; se separa marca, stack y banco del procedimiento general |
| [presentaciones-falp](https://github.com/fegome90-cmd/presentaciones-falp/tree/82185c0d3a201b34ced5b302096594cfe554161f) | `82185c0d3a201b34ced5b302096594cfe554161f` | Ejemplo de producción y perfil de marca; no se distribuyen marca, componentes ni assets como valores predeterminados |
| [ui-kit](https://github.com/fegome90-cmd/ui-kit/tree/4ae9b6e04afbfa50f5a9196a6a0d35d5458d8ec4) | `4ae9b6e04afbfa50f5a9196a6a0d35d5458d8ec4` | Ejemplo de registro y reutilización; permanece opcional y separado del alojamiento de esta skill |
| [creador_diapos](https://github.com/fegome90-cmd/creador_diapos/tree/b6d6eea48101dd0298f7a5fff090a5ecc078645c) | `b6d6eea48101dd0298f7a5fff090a5ecc078645c` | Referencia de producción Slidev; no obliga a usar Vue, Slidev o una marca particular |
| ZIP `design-process-skills-suite-v1.1.zip` | SHA-256 `425745fff0789c049d04762e18d9ace17052b224456e48811522fef8cba6d742` | Comparación de alcance, modos y verificaciones. No se copian sus archivos ni su script; no se aportó una licencia de redistribución en el paquete examinado |

No se transfieren permisos de los repositorios a fuentes tipográficas, imágenes, marcas o recursos enlazados. Los archivos concretos reutilizados en futuros encargos requieren su propia procedencia. Los repositorios privados citados no son necesarios para ejecutar este paquete.

## Emil Kowalski

Fuente canónica: [sitio del autor](https://emilkowal.ski/skill) y [emilkowalski/skills](https://github.com/emilkowalski/skills/tree/2d228630ba1446365f614a108cb8252f1feda202), revisión `2d228630ba1446365f614a108cb8252f1feda202`. La colección declara [MIT, copyright 2026 Emil Kowalski](https://github.com/emilkowalski/skills/blob/2d228630ba1446365f614a108cb8252f1feda202/LICENSE).

Se consultaron especialmente `emil-design-eng`, `animate`, `animation-performance`, `pick-ui-library`, `break-ui`, `prototype`, `review-animations` e `improve-animations`. Informan propósito y frecuencia del movimiento, continuidad ante interrupción, datos adversos plausibles, alternativas estructurales y entrega real de código.

Se contextualizan tiempos, curvas, escalas y preferencias estéticas. No se incorpora un catálogo cerrado de bibliotecas ni se sustituye una biblioteca elegida por el usuario. Se contrasta la aceleración con la documentación de la versión real: las generalizaciones sobre transformaciones independientes de Motion no se trasladan como reglas actuales. No se accedió a contenido de pago ni se reproducen recetas o scripts del autor.

## Impeccable

Fuente canónica: [impeccable.style](https://impeccable.style) y [pbakaus/impeccable](https://github.com/pbakaus/impeccable/tree/5cb95eea9c96479f57afe0732a45470d30183326), revisión `5cb95eea9c96479f57afe0732a45470d30183326`. El repositorio declara [Apache License 2.0](https://github.com/pbakaus/impeccable/blob/5cb95eea9c96479f57afe0732a45470d30183326/LICENSE) y [NOTICE](https://github.com/pbakaus/impeccable/blob/5cb95eea9c96479f57afe0732a45470d30183326/NOTICE.md) con atribuciones adicionales.

El núcleo examinado es [`skill/SKILL.src.md`](https://github.com/pbakaus/impeccable/blob/5cb95eea9c96479f57afe0732a45470d30183326/skill/SKILL.src.md), junto con referencias de contexto, tipografía, composición, adaptación, motion, robustez, auditoría y crítica. Informan la separación conceptual de hechos del producto, identidad y superficie; la distinción entre refinamiento y rediseño; y la necesidad de declarar método y cobertura.

No se incorporan su CLI, sus plantillas, su sistema de generación, puntuaciones de apariencia ni predicciones de abandono. Sus modos de superficie se usan como heurística. Se evita convertir rondas de preguntas, números de propuestas, vetos estéticos o medidas de recetas en obligaciones universales. Los tests de escaneo fueron leídos como contrato estático, no ejecutados como prueba de sus resultados.

## Normas y documentación técnica

| Fuente primaria | Aplicación y límite |
|---|---|
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Criterios, niveles y excepciones aplicables a contenido web. Una revisión selectiva no declara conformidad global |
| [Contraste mínimo 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) y [luminancia relativa](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html#dfn-relative-luminance) | Cálculo del helper propio para pares sRGB opacos y uniformes; el criterio real exige considerar contexto y excepciones |
| [Redimensionamiento 1.4.4](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html) y [espaciado 1.4.12](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html) | Verificar ampliación y tolerancia a ajustes; no prohibir unidades ni imponer esos valores como estilo inicial |
| [Foco no oculto 2.4.11](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html) y [apariencia del foco 2.4.13](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html) | Distinguir requisitos y niveles AA/AAA; no intercambiar sus identificadores |
| [Tamaño de objetivo mínimo 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) | Aplicar dimensión, espaciado y excepciones pertinentes; no universalizar una receta de 44 px |
| [WAI-ARIA APG: antes de usar](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/) y [patrones](https://www.w3.org/WAI/ARIA/apg/patterns/) | Comportamiento de controles personalizados; un rol no implementa teclado ni acredita compatibilidad con tecnologías de asistencia |
| [DTCG formato 2025.10](https://www.designtokens.org/TR/2025.10/format/) y [color 2025.10](https://www.designtokens.org/TR/2025.10/color/) | Declarar formato y versión de intercambio; validar valores tipados. Es una especificación de grupo comunitario, no una Recomendación W3C |
| [Motion: rendimiento](https://motion.dev/docs/performance) | Comprobar aceleración por versión, API y navegador; medir antes de afirmar fluidez o atribuir un cuello de botella |
| [Slidev: exportación](https://sli.dev/guide/exporting) | Distinguir `pptx`, `pptx-editable`, versión instalada y rasterizaciones reales |
| [Vercel Web Interface Guidelines](https://vercel.com/design/guidelines) | Contraste adicional de interacción, contenido, formularios y foco. Sus preferencias estéticas o específicas de framework no son requisitos generales; no trasladar recetas que impidan zoom |

## Derechos y actualización

Los textos y el helper de este paquete son una síntesis e implementación propias; no se incluyen archivos, assets ni ejecutables de las colecciones externas. Las citas identifican procedencia intelectual y límites de adaptación. Si posteriormente se incorporan copias o porciones sustanciales de otra fuente, conserva sus avisos y licencia aplicable dentro de la distribución correspondiente.

Al actualizar: fija la revisión nueva, lee el cambio relevante, distingue instrucciones de fuente de requisitos del usuario y vuelve a comprobar los comportamientos afectados. No conviertas una fuente popular ni un resultado de lint en prueba de eficacia del sistema.
