# Fuentes y nivel de evidencia

De dónde sale cada regla de la skill y cuánto peso tiene. Niveles:

- **Norma**: requisito de un estándar (WCAG 2.2). No se negocia.
- **Repo**: decisión aceptada y probada en el repo presentaciones-falp (`DESIGN.md` y `plans/`). Se respeta en el perfil correspondiente.
- **Oficio**: heurística de práctica profesional con valores de partida. Se ajusta al contenido y se declara.
- **Adaptación**: valor derivado por esta skill para slides a partir de reglas web; razonado, no medido. Revisar con
  uso real.

Los nodos OKF están en la carpeta de la wiki OKF del Drive del propietario del repo; el resto son públicos.

| Regla | Dónde se usa | Fuente | Nivel |
|---|---|---|---|
| Contraste 4,5:1 / 3:1 texto; 3:1 no textual; color no única señal | `color.md` §3 | WCAG 2.2, criterios 1.4.3, 1.4.11, 1.4.1 | Norma |
| Texto ampliable y espaciado ajustable sin pérdida | `tipografia.md` | WCAG 2.2, criterios 1.4.4 y 1.4.12 (OKF-137) | Norma |
| Movimiento reducido con fundido | `movimiento.md` §5 | `plans/004`; WCAG 2.2, criterio 2.3.3 (OKF-136) | Repo + Norma |
| Duraciones 150/160/220 ms, escalonado 30 ms con tope 90 ms | `movimiento.md` §2 | `DESIGN.md`, `plans/003`; criterios de Emil Kowalski (OKF-078) | Repo |
| Solo `opacity`/`transform`; sin `transition: all`; progreso con `scaleX` | `movimiento.md` §3 | `plans/001`, `plans/002` | Repo |
| Hover con movimiento solo con puntero fino; `scale(0.97)` al pulsar | `movimiento.md` §4 | `plans/005` | Repo |
| Nada animado en paletas de comandos | `movimiento.md` §1 | `plans/006` | Repo |
| Curvas ease-out / ease-in-out / drawer | `movimiento.md` §2 | `plans/002`, `plans/007`; OKF-078 | Repo |
| Grilla 12 columnas, colapso 12-8-4 | `grilla-y-espacio.md` §3 | Misterek, *Master Website Layouts* (OKF-136) | Oficio |
| Escala de 8, distancia entre grupos ≈ doble que dentro del grupo | `grilla-y-espacio.md` §4 | Misterek, *5 Skills* y *9 Hacks*; Ley de proximidad (OKF-136) | Oficio |
| Equilibrio simétrico, diagonal, asimétrico | `grilla-y-espacio.md` §7 | Misterek, *Ultimate Layout Guide* (OKF-136) | Oficio |
| Máximo cuatro bloques por fila | `grilla-y-espacio.md` §3 | Adaptado del catálogo de 33 layouts (OKF-136) | Adaptación |
| Márgenes seguros 5–6 % / 6–9 % | `grilla-y-espacio.md` §2 | Práctica de *title-safe* en video y proyección | Oficio |
| Espacio vacío 30–50 % | `grilla-y-espacio.md` §5 | Misterek (*whitespace*, OKF-136) | Adaptación |
| Escala modular (1,25 / 1,333) | `tipografia.md` §1 | Misterek y Schöndorfer (OKF-137, OKF-153) | Oficio |
| Tamaños para proyección (cuerpo 28–32 px, mínimo 1/60 del alto) | `tipografia.md` §1 | Adaptación de la escala web a lectura a distancia | Adaptación |
| 35–60 caracteres por línea | `tipografia.md` §3 | Butterick 45–90; Misterek 50–75 (OKF-137), acortado para slides | Adaptación |
| Interlineado titular 1–1,15, cuerpo ~1,4 | `tipografia.md` §1 | OKF-137 (Spotify, Butterick) | Oficio |
| Tracking negativo en titulares, positivo en mayúsculas | `tipografia.md` §5 | Misterek, *Hack #5*; Schöndorfer (OKF-137) | Oficio |
| Una familia → superfamilia → fuente ancla del titular | `tipografia.md` §4 | Misterek, *6 Easy Tips* (OKF-137, OKF-151) | Oficio |
| Display en textos breves (7–10 palabras) | `tipografia.md` §4 | Schöndorfer (OKF-137) | Oficio |
| Opacidad 100/87/70/60 % solo tras medir contraste | `tipografia.md` §5 | Material Design 2; Misterek (OKF-151) | Oficio |
| 60-30-10 | `color.md` §1 | Misterek, *5 Skills* (OKF-138) | Oficio |
| Tintes del mismo color en vez de colores nuevos; calibración HSB | `color.md` §5 | Misterek; Matteo Valentino (OKF-138) | Oficio |
| Objetivo 7:1 para proyección | `color.md` §3 | Razonamiento sobre pérdida de contraste del proyector | Adaptación |
| Título como afirmación (*assertion–evidence*) | `jerarquia.md` §1 | Michael Alley, *The Craft of Scientific Presentations* | Oficio (con estudios en educación de ingeniería) |
| Prueba de entrecerrar los ojos; tres preguntas de fijación; prueba de 3 s | `jerarquia.md` §4 | Misterek, *9 Hacks* y *11 years* (OKF-138) | Oficio (cualitativo) |
| Presupuesto de palabras (≈40 en cuerpo, 3–4 viñetas) | `jerarquia.md` §3 | Adaptación; coherente con *chunking* (OKF-137) | Adaptación |
| Rima visual y elemento protagonista | `jerarquia.md` §5 | Misterek, *6 Easy Tips* (OKF-138, OKF-151) | Oficio |
| Sin sombras en tarjetas; dorado con contorno y etiqueta | `perfiles/falp.md` | `DESIGN.md` | Repo |
| Arquitectura de la skill: reglas cortas + referencias por tema + tokens con descripción | `SKILL.md`, plantilla de perfil | Kirk McNeill, 3 skills modulares (OKF-143) | Oficio |

## Nodos OKF consultados

OKF-136 (grilla y layouts), OKF-137 (tipografía), OKF-138 (color y dirección de arte), OKF-143 (IA y sistemas de
diseño), OKF-151 (técnicas de elevación visual). Relacionados no incorporados en detalle: OKF-078 (movimiento,
Kowalski; sus reglas llegan por `plans/`), OKF-082 (diagramas), OKF-132 (credibilidad estética), OKF-144/145/149
(tokens y escalas en Figma), OKF-146 (catálogo de ejemplos), OKF-150 (arquetipos), OKF-152/153 (compendios
tipográficos).
