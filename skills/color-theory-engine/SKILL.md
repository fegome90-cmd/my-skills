---
name: color-theory-engine
description: Use when tasked with generating, analyzing, or correcting color palettes, designing UI/UX themes, or evaluating WCAG accessibility contrast ratios. Trigger this skill whenever the user mentions "color schemes", "contrast issues", "UI palettes", or needs mathematical color harmonies.
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
---

# Color Theory & Application Engine

## Overview
Esta skill implementa un enfoque estructurado y matemático para la teoría del color. Progresa desde la comprensión semántica hasta la generación armónica avanzada y el cumplimiento de accesibilidad.

## Progressive Workflow

Sigue estos niveles secuencialmente. No saltes a la generación avanzada sin establecer la base teórica y semántica.

- [ ] **Level 1: Foundation & Semantics**
  - Identifica el requerimiento central (ej. "dashboard accesible en modo oscuro").
  - Consulta `patterns/color-patterns.json` para identificar la base semántica apropiada.
  - Revisa `reference/color-theory-foundations.md` para la fundamentación de armonías en espacio HSL y cálculo de luminancia relativa.
- [ ] **Level 2: Harmonic Generation**
  - Determina la armonía requerida (Monocromática, Complementaria, Análoga, Triádica).
  - Ejecuta `scripts/color_engine.py` usando el comando `harmony` para derivar la paleta matemáticamente.
- [ ] **Level 3: Accessibility Validation**
  - Ejecuta el comando `contrast` en `scripts/color_engine.py` para todos los pares de texto/fondo.
  - Ajusta los pasos de luminancia hasta cumplir con los estándares WCAG 2.1: AA Normal / AAA Large (4.5:1), AA Large (3.0:1), o AAA Normal (7.0:1).

## Contexto de Ejecución
- **Script**: `python scripts/color_engine.py <command> <args>`
- **Referencias**: Carpeta `reference/` para teoría y fórmulas.
- **Patrones**: Carpeta `patterns/` para esquemas JSON validados y semánticos.
