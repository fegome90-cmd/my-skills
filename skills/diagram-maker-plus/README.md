# diagram-maker-plus

Generador de diagramas técnicos de alta fidelidad con arquitectura multi-motor y soporte para el contrato de revisión visual **Plannotator B2**.

---

## Modos de Operación

1. **Live HTML B2 (`live-html`):** Diagramas interactivos y planes visuales construidos sobre el canvas **Linear × Stripe Dark** con tabs accesibles, tooltips flotantes y anclajes `.comp`.
2. **Motor Avanzado Archify (`archify`):** Delegación transaccional a Archify (v2.17.0-dev.1) para topologías cloud (`architecture`), pipelines DAG (`workflow`), linaje de datos (`dataflow`), máquinas de estado (`lifecycle`) y trazas distribuidas (`sequence`).
3. **Mermaid.js / SVG Puro:** Diagramas ligeros (<10 KB), esquemas ER relacionales y mapas conceptuales sin dependencias pesadas.

---

## Estructura del Directorio

```text
skills/diagram-maker-plus/
├── SKILL.md                          # Guía principal de operación para agentes
├── README.md                         # Entrada canónica y mapa de componentes
├── resources/
│   ├── ARCHIFY-ROUTER.md             # Especificación técnica del router Archify-B2
│   ├── design.md                     # Sistema de diseño para documentos HTML extensos
│   ├── design-diagrams.md            # Especificación de componentes interactivos y sprite SVG
│   └── live-diagram-template.html    # Plantilla interactiva 1-shot B2
└── scripts/
    ├── archify-b2.mjs                # CLI transaccional 1-paso (build, doctor)
    ├── decorate-b2.mjs               # Decorador léxico B2, dual transport y extractReviewId()
    ├── cross-layer-verifier.mjs      # Verificador biyectivo formal y emisor de recibos
    ├── decorate-b2.test.mjs          # Pruebas unitarias del decorador (11 tests PASS)
    └── archify-b2.test.mjs           # Pruebas de integración, E2E y runtime real (13 tests PASS)
```

---

## Comandos Rápidos

### 1. Compilación Transaccional Archify-B2
Ejecuta validación `showcase` (9/9 checks), render, deliver, decoración B2 dual transport, verificación biyectiva y emisión del recibo criptográfico en un solo paso atómico:

```bash
node skills/diagram-maker-plus/scripts/archify-b2.mjs build <type> <input.json> <output.html>
```

Tipos soportados: `workflow`, `architecture`, `dataflow`, `lifecycle`, `sequence`.

### 2. Diagnóstico del Runtime Congelado
Verifica la identidad de Archify (commit `06dd052`, working tree limpio) y la integridad de los scripts del bridge:

```bash
node skills/diagram-maker-plus/scripts/archify-b2.mjs doctor
```

### 3. Ejecución de Suites de Pruebas
```bash
# Pruebas unitarias del decorador (11 tests)
node --test skills/diagram-maker-plus/scripts/decorate-b2.test.mjs

# Pruebas de integración, E2E y runtime Plannotator real (13 tests)
node --test skills/diagram-maker-plus/scripts/archify-b2.test.mjs
```

---

## Contrato de Identidad y Plannotator B2

- **Biyección 1:1 Estricta:** Todo nodo interactivo porta la clase `.comp` y un `data-review-id` unívoco.
- **Dual Transport:** Los artefactos Archify inyectan además `data-annotate` como primitiva de transporte reconocida por Plannotator.
- **Normalización de Anclajes (`extractReviewId`):** Resuelve cualquier selector nativo emitido por Plannotator (`#node-<id>`, `data-annotate`, o W3C targets) hacia el `reviewId` canónico B2 sin pérdida de identidad.
- **Cadena Criptográfica:** Cada compilación emite un `*.bridge-receipt.json` sellado con SHA-256 que certifica especificación de entrada, artefactos generados y programas del bridge.
