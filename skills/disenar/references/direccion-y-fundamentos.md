# Dirección y fundamentos

Lee esta referencia al elegir o revisar lenguaje visual. Consulta solo las secciones que resuelvan el encargo. Un cambio local puede terminar con el artefacto y una explicación breve; no exige documentos rectores ni un número fijo de alternativas.

## Sitúa la decisión

Identifica resultado, audiencia, uso, contenido, medio y condiciones de lectura o interacción. Inspecciona lo existente antes de preguntar. Conserva los hechos y decisiones confirmados; etiqueta inferencias y pregunta únicamente por vacíos que cambien materialmente la entrega.

Separa tres responsabilidades, aunque se documenten juntas:

- **Producto o encargo:** propósito, contenido, funcionamiento y restricciones verificadas.
- **Marca o identidad:** activos, voz y decisiones visuales autorizadas.
- **Superficie:** tarea y organización de esta pantalla, página, lámina o pieza.

Reconoce una identidad coherente en sus artefactos aunque no exista un archivo de diseño. En refinamientos, preserva lo que queda fuera de alcance; en rediseños, sustituye el lenguaje autorizado conservando hechos y función pertinentes. Aplica el brief y las convenciones observadas antes que las preferencias de una referencia externa.

Usa **operar, leer, persuadir o experimentar** como heurísticas para elegir prioridades. Un editor puede favorecer estabilidad; una campaña, expresión; un manual, continuidad de lectura. Decide por superficie y admite combinaciones justificadas. No conviertas esas categorías en predicciones de conducta.

## Define una dirección proporcional

Relaciona cada decisión relevante con su función: densidad para el contenido disponible, jerarquía para el recorrido, contraste para distinguir roles, ritmo para agrupar, profundidad para explicar relaciones y movimiento para comunicar cambios. Justifica materiales, ornamentación y estilo con el encargo.

Explora alternativas estructurales cuando haya una incertidumbre de dirección. Hazlas comparables mediante contenido y condiciones comunes. Si la solicitud ya fija una solución, desarróllala sin imponer una competición de conceptos. No prohíbas fuentes, gradientes, etiquetas sobre títulos, sombras o estilos por pertenecer a un catálogo.

## Tipografía

Define roles antes de elegir familias: título, lectura, etiqueta, dato, nota o código según necesidad. Conserva las fuentes de una marca vigente; para elecciones nuevas, compara cobertura de caracteres, formas, pesos disponibles, legibilidad del rol, carga y licencia de los archivos reales.

Prueba palabras, acentos, cifras, signos y textos largos del contenido. Ajusta tamaño, peso, ancho, interlínea, tracking y separación sobre el resultado visible. Introduce otra familia solo si aporta un rol útil. Comprueba fallback, pesos ausentes, carga y reflujo; no supongas que una fuente variable o tabular siempre es necesaria.

En web, verifica ampliación y ajustes de espaciado sin pérdidas. `px`, `rem` o `clamp()` aislados no acreditan cumplimiento. Los valores de espaciado de WCAG describen ajustes que deben tolerarse, no una receta tipográfica inicial. Consulta [redimensionamiento](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html) y [espaciado](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html) cuando apliquen.

## Color y contraste

Asigna roles de fondo, texto, acción, estado y datos. Preserva significados establecidos y acompaña señales necesarias con formas, texto u otros medios pertinentes. Elige armonías y acentos por contenido, contexto y marca; no impongas porcentajes universales ni atribuyas calma, confianza o comprensión como efectos demostrados.

Mide los pares utilizados en sus estados y fondos reales. Considera transparencia, imágenes, gradientes, superposiciones y temas antes de emitir un resultado. Para texto web, aplica el criterio y las excepciones de [WCAG 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html); no clasifiques texto como grande solo por un token anterior a su escalado. Un cálculo entre HEX opacos cubre ese par, no toda la interfaz.

## Composición, símbolos y tokens

Ordena el contenido por tarea o argumento. Agrupa lo relacionado y distingue niveles mediante espacio, escala, alineación y contraste. Selecciona grilla, contenedores y densidad desde esas relaciones; adapta la estructura cuando cambien espacio, input o contenido. Revisa orden visual, lectura y foco cuando correspondan.

Elige iconos por significado y contexto. Comprueba consistencia de familia, peso, geometría, espacio y tamaño final; usa etiquetas cuando el reconocimiento no esté establecido. Una biblioteca es opcional: puedes seleccionar otra, adaptar una pieza compatible o crear un original con procedencia clara.

Conserva valores compartidos como tokens cuando exista una necesidad real de reutilización. Distingue primitivos, roles semánticos y decisiones del componente sin imponer una jerarquía única. Declara formato y versión al intercambiarlos; valida la conversión al destino. Tener `$type` y `$value` no prueba conformidad con [DTCG](https://www.designtokens.org/TR/2025.10/format/).

Inspecciona finalmente el artefacto en sus condiciones de uso. Registra decisiones útiles y comprobaciones pendientes; entrega la pieza solicitada, no solo su especificación.

## Procedencia

Síntesis original informada por [Impeccable: contexto y modos](https://github.com/pbakaus/impeccable/blob/5cb95eea9c96479f57afe0732a45470d30183326/skill/SKILL.src.md) y sus referencias de tipografía y composición. Se contextualizan sus heurísticas; no se incorporan su CLI, plantillas ni vetos estéticos.
