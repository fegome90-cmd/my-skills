# Router y Puente Transaccional: diagram-maker-plus ↔ Archify-B2

Guía canónica de enrutamiento por capacidades, ejecución transaccional y verificación biyectiva entre `diagram-maker-plus` y el motor Archify con contrato Plannotator B2.

**Identidad de Runtime Congelada:**
- **Versión de Archify:** `2.17.0-dev.1` (prerelease / dev build)
- **Commit de Archify:** `06dd052602dd9a369e4d034e24faef0917b5a60c` (verificado `dirty: false`)
- **Launcher canónico:** `~/.local/bin/archify` (apuntando a `~/Developer/archify/archify/bin/archify.mjs`)
- **Puente Transaccional:** `skills/diagram-maker-plus/scripts/archify-b2.mjs`
- **Decorador Léxico B2:** `skills/diagram-maker-plus/scripts/decorate-b2.mjs`
- **Verificador Biyectivo Cross-Layer:** `skills/diagram-maker-plus/scripts/cross-layer-verifier.mjs`

---

## 1. Contrato JSON-IR (Producer ↔ Consumer)

Todo artefacto delegado a Archify se rige bajo este contrato formal:

| Propiedad | Definición |
|---|---|
| **Producer** | `diagram-maker-plus` |
| **Consumer** | `archify` (CLI engine v2.17.0-dev.1) |
| **Schema canónico** | `~/Developer/archify/archify/schemas/{type}.schema.json` (schema_version: 2) |
| **Nodos revisables** | `/nodes/*/id` (`workflow`, `dataflow`), `/components/*/id` (`architecture`), `/states/*/id` (`lifecycle`), `/participants/*/id` (`sequence`) |
| **Validación previa** | `archify validate <type> <input.json> --quality showcase` (0 errores, 0 advertencias) |

---

## 2. Enrutamiento Basado en Capacidades

El enrutador clasifica por la **capacidad técnica requerida**:

| Capacidad Requerida | Backend | Modo de Salida / Justificación |
|---|---|---|
| Dashboard de decisión, plan maestro o revisión visual en Plannotator | `native` (`live-html`) | Diseño Dark Canvas propio (Linear × Stripe) con contrato B2 nativo |
| Intercambio simple de mensajes, endpoints API, auth o flujo de red | `native` (`mermaid` / `sequence-svg`) | Markdown inline o SVG vectorial ligero (<10 KB), sin overhead |
| Esquema relacional de base de datos o cardinalidad estricta | `native` (`er-svg` / `mermaid`) | SVG vectorial puro o render CDN |
| Cronograma, sprints, roadmap temporal lineal | `native` (`gantt-svg` / `mermaid`) | SVG puro embebible |
| Mapas conceptuales radiales y lluvia de ideas | `native` (`mindmap-svg`) | SVG puro |
| **Topología Cloud, microservicios, seguridad o infraestructura** | `archify` (`architecture`) | Layout topológico validado con 9 checks + export multi-formato |
| **Flujos de aprobación, CI/CD, runbooks o pipelines con branching** | `archify` (`workflow`) | DAG de procesos con validación de estados terminales |
| **Cadenas asíncronas distribuidas, trazas multi-etapa con vistas** | `archify` (`sequence`) | Reproductor de trazas interactivo con timeline y roles tipados |
| **Pipelines ETL/ELT, linaje y gobierno de datos** | `archify` (`dataflow`) | DAG de datos con schemas de entrada/salida |
| **Máquinas de estado complejas, políticas de reintento y transiciones** | `archify` (`lifecycle`) | State machine formal con validación de terminal states |

### Matriz de Calificación por Tipo (T18–T21)

| Tipo | Fixture Calificado | Validate (9/9) | Deliver | Fórmula Biyectiva | Bridge Receipt |
|---|---|:---:|:---:|:---:|:---:|
| `workflow` | `router-pipeline.workflow.json` | PASS | PASS | PASS (8/8) | PASS |
| `architecture` | `web-app.architecture.json` | PASS | PASS | PASS (10/10) | PASS |
| `dataflow` | `event-stream.dataflow.json` | PASS | PASS | PASS (12/12) | PASS |
| `lifecycle` | `deployment-release.lifecycle.json` | PASS | PASS | PASS (11/11) | PASS |
| `sequence` | `cache-miss-request.sequence.json` | PASS | PASS | PASS (7/7) | PASS |

### Control Explícito de Motor (`engine`)
- `engine: auto` (default): Resuelve dinámicamente según la capacidad requerida.
- `engine: native`: Fuerza el motor interno de `diagram-maker-plus` (Mermaid / SVG / Live HTML).
- `engine: archify`: Fuerza la compilación transaccional vía `archify-b2` (requiere JSON-IR válido).

---

## 3. Ejecución Transaccional: `archify-b2 build`

En lugar de coordinar pasos manuales expuestos a errores de secuencia, el agente invoca una única transacción atómica:

```bash
node skills/diagram-maker-plus/scripts/archify-b2.mjs build <type> <input.json> <output.html> [--quality showcase] [--receipt <path.json>]
```

### Qué ejecuta internamente la transacción:
1. **Runtime Identity Check:** Comprueba commit `06dd052602dd9a369e4d034e24faef0917b5a60c`, estado `dirty: false` y versión de Node.
2. **Validación Fail-Closed:** Ejecuta `archify validate` bajo `--quality showcase`. Si `ok: false` o código $\neq 0$, aborta.
3. **Render a Staging Aislado:** Compila el SVG en un directorio temporal sin tocar el destino.
4. **Deliver Snapshot:** Ejecuta `archify deliver` en staging para emitir el recibo de especificación.
5. **Cálculo de Hash Pre-B2:** Computa el SHA-256 del HTML renderizado antes de la decoración.
6. **Decoración B2 Dual Transport:** Inyecta `.comp c-adapter`, `data-review-id` canónico y `data-annotate` nativo de Plannotator con escape estricto de entidades HTML. Provee la función `extractReviewId()` para normalizar selectores (`#node-<id>`, `data-annotate`, targets W3C) hacia el `reviewId` canónico.
7. **Verificación Biyectiva Cross-Layer:** Comprueba formalmente:
   - $\text{IR\_IDS} == \text{SVG\_NODE\_IDS}$ (sin nodos faltantes ni fantasmas)
   - $\text{EXPECTED\_B2\_IDS} = \{ \text{reviewIdFor}(id) \mid id \in \text{IR\_IDS} \}$
   - $\text{EXPECTED\_B2\_IDS} == \text{ACTUAL\_B2\_REVIEW\_IDS}$
   - Cero duplicados en cualquier capa. Si falla, aborta.
8. **Generación del Bridge Receipt:** Emite el recibo final que une la cadena criptográfica completa (incluyendo `bridge_runtime`).
9. **Promoción Atómica:** Escribe a archivo temporal y ejecuta `fs.renameSync` para garantizar reemplazo atómico en disco.

---

## 4. Estructura del Recibo Criptográfico Final (Bridge Receipt v2.1)

El archivo `.bridge-receipt.json` certifica la trazabilidad completa:

```json
{
  "schema_version": 2,
  "command": "archify-b2 build",
  "timestamp": "2026-09-04T15:23:13.005Z",
  "status": "PASS",
  "runtime": {
    "archify_version": "2.17.0-dev.1",
    "archify_commit": "06dd052602dd9a369e4d034e24faef0917b5a60c",
    "archify_dirty": false,
    "node_version": "v26.8.1",
    "launcher_realpath": "~/Developer/archify/archify/bin/archify.mjs"
  },
  "bridge_runtime": {
    "archify_b2_sha256": "0b70ebf7417613c0549ae966367bee0bf02bdf5d1bf81bcb4f7f95e5473032dc",
    "decorate_b2_sha256": "d3518e9a94b0215a69f452135a6123ecdf2bf2cf761e3d687ef56b0703f384f8",
    "cross_layer_verifier_sha256": "d1bc3d535d56c1c316190e4ed9595a82ff0e567b6c67bd365ec9823c446b0afe"
  },
  "contract": {
    "producer": "diagram-maker-plus",
    "consumer": "archify",
    "diagram_type": "workflow",
    "ir_schema_version": 2,
    "reviewable_nodes_selector": "/nodes/*/id",
    "node_count": 8,
    "bijective_parity": true,
    "bijective_mapping": {
      "formula": "reviewIdFor(nodeId) -> comp.archify-{sanitized(nodeId)}",
      "ir_equals_svg_nodes": true,
      "expected_equals_actual_review_ids": true
    }
  },
  "cryptographic_chain": {
    "specification_sha256": "c6c9c07a73130625f37c21920829c5483fbe473593be8b642b8fbadcb1b641d5",
    "archify_deliver_artifact_sha256": "4c5b92a3716534acdcaf94bd98a657f2d03f4f67da8e4863555572e66b5d4151",
    "archify_deliver_receipt_sha256": "7666c2ca955529236d9ab5b857e80f30d16dbe617dd3689ea038c00bcd7c526f",
    "rendered_pre_b2_sha256": "4c5b92a3716534acdcaf94bd98a657f2d03f4f67da8e4863555572e66b5d4151",
    "decorated_final_sha256": "1765070740f6421fb9b0c69c81803f2281fbb049660f3a7d47f3d312c78c7958"
  },
  "validation": {
    "archify_checks_passed": 9,
    "archify_errors": 0,
    "archify_warnings": 0,
    "b2_paridad_1to1": true,
    "cross_layer_parity": true
  }
}
```

---

## 5. Diagnóstico de Salud del Puente

Para verificar que el runtime congelado, symlinks y hashes de scripts se encuentran en estado nominal:

```bash
node skills/diagram-maker-plus/scripts/archify-b2.mjs doctor
```

---

## 6. Acotación Formal de Garantías (Claim Boundary)

La suite de verificación automatizada contiene 24 quality gates (11 unitarios en `decorate-b2.test.mjs` y 13 de integración/E2E en `archify-b2.test.mjs`).

Respecto a la interacción con el runtime de Plannotator:
- **T16a:** Prueba la paridad en el DOM de que cada nodo Archify decorado posee `data-review-id` y `data-annotate` idénticos.
- **T16b:** Prueba que la escalera de normalización de `extractReviewId()` resuelve unívocamente cualquier selector válido emitido por Plannotator.
- **T16c (`Real Plannotator runtime acceptance + canonical anchor recovery`):** Prueba el ciclo de vida del proceso real de Plannotator v0.27.12 aceptando el artefacto decorado B2, persistiendo el comentario y recuperando el anclaje canónico vía `extractReviewId()`.
- **Límite del Claim:** La UI de Plannotator prioriza selectores nativos `#id` sobre `data-annotate` cuando existen IDs en los elementos SVG. El adapter resuelve esto en la capa de lectura; la propiedad formal garantizada y probada es:
  $$\forall s \in \text{NativeAnchors}(\text{Node}),\ \text{extractReviewId}(s) = \text{reviewIdFor}(id)$$

