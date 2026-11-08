# Fuente del plan de talleres 2027

Esta fuente genera una presentación de ocho diapositivas con texto, formas y conectores nativos de PowerPoint. El contenido y las notas se definen en `create_deck.mjs`.

## Entorno utilizado

- Node.js 24.19.0.
- `@oai/artifact-tool` 2.8.99, instalado en el runtime de producción.
- Python 3, biblioteca estándar para las comprobaciones de contenido.
- Fuente Nimbus Sans, regular y negrita, disponible en el entorno de renderizado.
- Utilidades de validación de Presentations del host para integridad y geometría.

La generación requiere un entorno con esa biblioteca. El paquete ZIP no incluye dependencias propietarias del host ni instala programas. La fuente no presupone acceso a servicios externos.

## Reconstrucción en el entorno utilizado

Desde la carpeta que contiene `source/`, ejecutar:

```bash
bash source/rebuild.sh plan-talleres-2027-reconstruido.pptx
```

Las variables `CODEX_PRIMARY_RUNTIME_NODE`, `CODEX_PRIMARY_RUNTIME_NODE_MODULES` y `CODEX_PRIMARY_RUNTIME_PYTHON` deben apuntar a las dependencias instaladas. La variable opcional `PRESENTATIONS_SKILL_DIR` permite indicar la ubicación de los validadores del host. Si el archivo de salida ya existe, se solicita otro nombre mediante el argumento de la orden. El script no sobrescribe ese PPTX.

El proceso produce el borrador en `build/`, el PPTX en `output/`, ocho vistas PNG en `renders/` y comprobaciones en `checks/`. Solo escribe dentro de la carpeta que contiene `source/`. La prueba de edición modifica una copia desechable en `build/`.

## Archivos

- `create_deck.mjs`: contenido, estilo, geometría y notas de exposición.
- `notes.json`: notas y tiempos sugeridos, generados a partir de la fuente principal.
- `validate_deck.py`: conteo, contenido, notas, texto nativo y conectores en el paquete OOXML.
- `render_final.mjs`: vuelve a importar el PPTX final y renderiza sus ocho láminas.
- `verify_native_edit.mjs`: modifica el texto y la posición de un nodo en una copia y reexporta.
- `capture_validator.py`: ejecuta un validador y guarda de forma atómica el comando, código de salida, stdout, stderr e informe interpretado. Una salida vacía se registra como BLOCKED y detiene la secuencia.
- `rebuild.sh`: secuencia de generación, validación directa, exportación y render.

## Editabilidad y límites

Las 38 formas que contienen texto son objetos nativos. El diagrama de la tercera lámina utiliza tres rectángulos y dos conectores con extremos asociados a sus nodos. No contiene imágenes rasterizadas.

Las notas distribuyen 300 segundos entre las ocho láminas. Incluyen 556 palabras de texto hablado, además de tiempos y transiciones. Son orientativas; no hubo un ensayo cronometrado.

No se abrió Microsoft PowerPoint ni se probó su interfaz. El render y la prueba de edición se realizaron con Artifact Tool. En equipos sin Nimbus Sans, PowerPoint puede sustituir la fuente; esa sustitución no se comprobó.

El finalizador integrado del host se intentó y falló por `spawnSync EPERM`. Se ejecutaron directamente los validadores de integridad y geometría, que devolvieron cero hallazgos, y se inspeccionó el PPTX por separado. Una exportación complementaria a PDF también se intentó, pero falló por un módulo `#standard-fonts/Helvetica` ausente. El PDF no formaba parte del encargo y no se entrega.
