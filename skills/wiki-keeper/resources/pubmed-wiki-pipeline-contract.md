# PubMed Wiki Pipeline Contract

**Versión:** 1.0.0  
**Estado:** Activo  
**Aplica a:** `wiki-keeper`, `literature-search`, `pubmed-cli` (si se reactiva)

Este documento define las invariantes operativas del pipeline de ingestión bibliográfica para la wiki oncológica. Cualquier script o skill que interactúe con el proceso de extracción atómica o actualización de la wiki debe adherirse a estas reglas.

---

## 1. Contexto de Ejecución (REPO_ROOT)

Ningún componente del pipeline debe depender del directorio de trabajo actual (`cwd`). Todas las rutas deben resolverse a partir de un **`REPO_ROOT` explícito**.

- **Regla:** El script o agente debe identificar la raíz del repositorio (`examen_grado`) de forma determinista (ej. usando `git rev-parse --show-toplevel` o una variable de entorno inyectada).
- **Fallo:** Si `REPO_ROOT` no se puede resolver, el proceso **debe abortar**. No asumir rutas relativas.

---

## 2. Ruta Canónica Atómica

Se resuelve la ambigüedad y el conflicto histórico entre `raw/` y `vault/raw/`.

- **Ruta Canónica Única:** `${REPO_ROOT}/vault/raw/sources/atomic/`
- **Convención de Nombre:** `{pmid}.md` (ej. `41963621.md`)
- **Regla de Lectura / Escritura:** 
  - Al extraer afirmaciones desde un artículo, se debe escribir el claim atómico **exclusivamente** en esta ruta.
  - Al integrar a la wiki, leer los claims desde esta ruta.
- **Manejo de Errores:** Si el directorio `${REPO_ROOT}/vault/raw/sources/atomic/` no existe, fallar con un error explícito. No crearlo automáticamente si falta toda la jerarquía de `vault/`.

---

## 3. Semántica de los Artefactos

Para evitar confusión entre los distintos niveles de procesamiento de información:

1. **Fuentes Raw (Raw Sources):** PDFs originales o JSON devuelto por APIs de PubMed.
2. **Claims Atómicos (Atomic Claims):** Archivos `{pmid}.md` ubicados en `vault/raw/sources/atomic/`. Contienen afirmaciones atómicas extraídas de *un único* paper (PMID) sin mezclar con otros conceptos. Sirven como buffer e historial inmutable de la extracción.
3. **Páginas Wiki:** Archivos en `vault/wiki/` (diseases, treatments, concepts). Integran y sintetizan múltiples claims atómicos bajo el patrón Karpathy.

---

## 4. Estado del Pipeline (`pubmed-pipeline-state.json`)

Se aclara la semántica histórica de los contadores para eliminar ambigüedades en la validación:

- `completedPages`: Lista (array) de las páginas procesadas en el ciclo actual. Los identificadores aquí deben ser únicos por ciclo.
- `stats.pagesUpdated`: Contador acumulado histórico que abarca todos los ciclos ejecutados (**no** representa páginas únicas). Indica la cantidad total de operaciones de actualización realizadas.
- **Deduplicación:** Las operaciones de limpieza del estado deben preservar los contadores acumulados (`stats.*`) intactos.

---

## 5. Ejemplos de Ejecución

Independiente de desde dónde se ejecute el comando (ej. desde `~` o desde `~/Developer`), la resolución debe ser estricta:

```bash
# Correcto (interno del script / agente)
REPO_ROOT="$(git rev-parse --show-toplevel)"
ATOMIC_DIR="${REPO_ROOT}/vault/raw/sources/atomic"
ATOMIC_FILE="${ATOMIC_DIR}/41963621.md"

# Incorrecto
ATOMIC_FILE="raw/sources/atomic/41963621.md"
ATOMIC_FILE="./vault/raw/sources/atomic/41963621.md"
```
