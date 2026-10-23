import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

// Reproducible source. All generated files remain beneath this source's parent.
const sourceDir = path.dirname(fileURLToPath(import.meta.url));
const workspaceDir = path.resolve(sourceDir, '..');
const buildDir = path.join(workspaceDir, 'build');
const outputDir = path.join(workspaceDir, 'output');
const renderDir = path.join(workspaceDir, 'renders');
const checkDir = path.join(workspaceDir, 'checks');
const filename = process.argv[2] || 'plan-talleres-2027.pptx';
if (filename !== path.basename(filename) || !filename.endsWith('.pptx')) {
  throw new Error('The optional output argument must be a PPTX basename.');
}
for (const dir of [buildDir, outputDir, renderDir, checkDir]) {
  await fs.mkdir(dir, { recursive: true });
}

const FONT = 'Nimbus Sans';
const C = {
  ink: '#18363D', paper: '#F7F7F3', teal: '#28675F',
  muted: '#4F6368', mint: '#BCD9C8', rule: '#CCD6D3', pale: '#E7EEEA', white: '#FFFFFF',
};
const W = 1280, H = 720;
const presentation = Presentation.create({ slideSize: { width: W, height: H } });
const noLine = { style: 'solid', fill: 'none', width: 0 };

function text(slide, name, value, x, y, w, h, size = 36, color = C.ink, bold = false) {
  const shape = slide.shapes.add({
    name, geometry: 'textbox',
    position: { left: x, top: y, width: w, height: h },
    fill: 'none', line: noLine,
  });
  shape.text = value;
  shape.text.style = {
    typeface: FONT, fontSize: size, color, bold,
    alignment: 'left', verticalAlignment: 'top',
    autoFit: 'none', wrap: 'square', insets: 0,
  };
  return shape;
}

function rule(slide, name, x, y, w, color = C.rule) {
  return slide.shapes.add({
    name, geometry: 'line', position: { left: x, top: y, width: w, height: 0 },
    fill: 'none', line: { style: 'solid', fill: color, width: 1.5 },
  });
}

function page(title, dark = false) {
  const slide = presentation.slides.add();
  slide.background.fill = dark ? C.ink : C.paper;
  if (title) text(slide, 'titulo', title, 88, 67, 1104, 80, 48, dark ? C.white : C.ink, true);
  return slide;
}

const notes = [
  {
    seconds: 25,
    talk: 'Presentamos el plan de talleres para 2027 con una idea central: aprender haciendo. Es una propuesta de trabajo interno para nuestro equipo de doce personas. La intención es reservar un espacio común para trabajar sobre criterios compartidos y avanzar hacia un prototipo. Hoy recorreremos el objetivo, la organización y la decisión que necesitamos tomar para iniciar.',
    transition: 'Para empezar, veamos qué queremos conseguir con este recorrido.',
  },
  {
    seconds: 35,
    talk: 'El objetivo tiene dos partes que debemos mantener conectadas. Primero, alinear criterios para que el equipo pueda conversar y tomar decisiones sobre una base compartida. Segundo, producir un prototipo común que permita concretar esas decisiones. En las sesiones podremos hacer explícitas las diferencias de criterio y trabajarlas juntos. El prototipo será el objeto de trabajo que nos ayude a dar forma a lo que acordemos.',
    transition: 'Para organizar ese trabajo, proponemos tres etapas.',
  },
  {
    seconds: 45,
    talk: 'El recorrido comienza con diagnóstico, continúa con diseño y termina con prototipo. Reservamos dos sesiones para diagnóstico, dos para diseño y tres para prototipo. En diagnóstico pondremos sobre la mesa el punto de partida y los criterios que necesitamos alinear. En diseño daremos forma a una propuesta compartida. En prototipo construiremos una versión concreta de esa propuesta. La secuencia ayuda a relacionar cada etapa con la siguiente. Las cantidades de sesiones son parte del plan que estamos presentando.',
    transition: 'Veamos cómo se distribuyen estas etapas en el calendario.',
  },
  {
    seconds: 40,
    talk: 'La primera semana corresponde a diagnóstico y la segunda a diseño. Las semanas tres y cuatro se dedican a prototipo. Este calendario expresa el orden de trabajo que proponemos. Todavía necesitamos acordar una fecha de inicio para convertir las semanas en fechas concretas. También tendremos que coordinar la disponibilidad del equipo al agendar las sesiones. La etapa de prototipo ocupa dos semanas, dentro de las cuales distribuiremos las tres sesiones previstas.',
    transition: 'Además del calendario, necesitamos claridad sobre quién hace cada cosa.',
  },
  {
    seconds: 35,
    talk: 'La coordinación organiza el trabajo. La facilitación guía el desarrollo de las sesiones. Los participantes construyen el contenido y el prototipo compartido. Estos roles nos dan una distribución sencilla de responsabilidades para preparar y realizar los talleres. Podemos usar esta distinción al acordar las personas responsables, sin asignar nombres antes de que el equipo lo decida. La participación de las doce personas se organiza alrededor de ese trabajo común.',
    transition: 'Para que las sesiones puedan realizarse, revisemos los recursos necesarios.',
  },
  {
    seconds: 30,
    talk: 'Los recursos previstos son una sala, un equipo de proyección y materiales de trabajo. La sala permite reunir al equipo. La proyección nos ayuda a compartir lo que estemos revisando, y los materiales permiten trabajar durante las actividades. Al preparar el inicio, conviene concretar la disponibilidad de estos recursos junto con las fechas. La lista mantiene la preparación en un nivel sencillo y manejable.',
    transition: 'Hay tres riesgos que conviene anticipar al organizar el plan.',
  },
  {
    seconds: 50,
    talk: 'El primer riesgo es la disponibilidad del equipo. La respuesta prevista es agendar con anticipación para poder coordinar la participación. El segundo son los retrasos. Si aparecen, la respuesta es priorizar el alcance y concentrar el trabajo en lo que resulte esencial para el prototipo compartido. El tercer riesgo son las dificultades técnicas. Para ese caso, prepararemos una alternativa sencilla que nos permita continuar la actividad. Son medidas de preparación del plan. Podemos revisarlas al fijar las fechas y las responsabilidades.',
    transition: 'Con este marco, podemos pasar a la decisión necesaria para empezar.',
  },
  {
    seconds: 40,
    talk: 'La próxima decisión es acordar la fecha de inicio y las personas responsables. Propongo cerrar esta presentación con dos preguntas al equipo: ¿qué fecha podemos comprometer para comenzar? ¿Quién asumirá la coordinación y la facilitación? Con ese acuerdo podremos organizar las sesiones y concretar la preparación. Si la fecha no puede cerrarse ahora, identifiquemos qué disponibilidad falta por confirmar. El objetivo de esta conversación es dejar claro cómo daremos el siguiente paso.',
    transition: 'Pausa para recoger la decisión del equipo.',
  },
];

// 1. Cover. All content remains native text.
{
  const s = page(null, true);
  text(s, 'plan', 'Plan de talleres 2027:', 88, 184, 1104, 100, 68, C.white, true);
  text(s, 'idea-central', 'aprender haciendo', 88, 285, 1104, 100, 68, C.mint, true);
  text(s, 'audiencia', 'Plan interno para un equipo de 12 personas', 88, 510, 1104, 45, 28, C.white);
  text(s, 'contexto', 'Caso de planificación sintético', 88, 565, 1104, 35, 23, C.mint);
}

// 2. Objective. One shared objective, presented in its two parts.
{
  const s = page('Objetivo');
  text(s, 'criterios', 'Alinear criterios', 88, 238, 1104, 95, 60, C.ink, true);
  text(s, 'prototipo', 'Producir un prototipo\ncompartido', 88, 365, 1104, 180, 60, C.teal, true);
}

// 3. Required editable process diagram. Native rectangles, text and attached connectors.
{
  const s = page('Tres etapas');
  const labels = [ ['Diagnóstico', '2 sesiones'], ['Diseño', '2 sesiones'], ['Prototipo', '3 sesiones'] ];
  const nodes = labels.map(([name, count], i) => {
    const n = s.shapes.add({
      name: `etapa-${i + 1}`, geometry: 'rect',
      position: { left: 88 + i * 392, top: 270, width: 320, height: 180 },
      fill: i === 2 ? C.ink : C.pale,
      line: { style: 'solid', fill: i === 2 ? C.ink : C.rule, width: 1.5 },
    });
    n.text = [
      { runs: [{ run: name, style: { typeface: FONT, fontSize: '27pt', bold: true } }], spaceAfter: 14 },
      { runs: [{ run: count, style: { typeface: FONT, fontSize: '22.5pt' } }] },
    ];
    n.text.style = { typeface: FONT, fontSize: 36, color: i === 2 ? C.white : C.ink,
      verticalAlignment: 'middle', alignment: 'center', insets: 16, wrap: 'none', autoFit: 'none' };
    return n;
  });
  for (let i = 0; i < 2; i++) {
    const connector = s.shapes.connect(nodes[i], nodes[i + 1], {
      kind: 'straight', fromSide: 'right', toSide: 'left',
      line: { style: 'solid', fill: C.teal, width: 2.5 },
      tail: { type: 'triangle', width: 'med', length: 'med' },
    });
    connector.name = `conexion-${i + 1}`;
  }
}

// 4. Schedule. Native text and dividers keep the mapping directly editable.
{
  const s = page('Calendario');
  const rows = [ ['Semana 1', 'Diagnóstico'], ['Semana 2', 'Diseño'], ['Semanas 3 y 4', 'Prototipo'] ];
  rows.forEach(([week, stage], i) => {
    const y = 229 + i * 125;
    text(s, `periodo-${i + 1}`, week, 88, y, 430, 65, 34, C.muted);
    text(s, `trabajo-${i + 1}`, stage, 560, y - 2, 632, 70, 44, C.ink, true);
    if (i < 2) rule(s, `separador-${i + 1}`, 88, y + 86, 1104);
  });
}

// 5. Roles.
{
  const s = page('Roles');
  const rows = [ ['Coordinación', 'Organiza'], ['Facilitación', 'Guía'], ['Participantes', 'Construyen'] ];
  rows.forEach(([role, action], i) => {
    const y = 229 + i * 125;
    text(s, `rol-${i + 1}`, role, 88, y, 500, 65, 36, C.muted);
    text(s, `responsabilidad-${i + 1}`, action, 640, y - 2, 552, 70, 44, C.teal, true);
    if (i < 2) rule(s, `separador-${i + 1}`, 88, y + 86, 1104);
  });
}

// 6. Resources.
{
  const s = page('Recursos');
  ['Sala', 'Equipo de proyección', 'Materiales de trabajo'].forEach((item, i) => {
    const y = 224 + i * 124;
    text(s, `recurso-${i + 1}`, item, 88, y, 1104, 75, 48, C.ink, true);
    if (i < 2) rule(s, `separador-${i + 1}`, 88, y + 87, 1104);
  });
}

// 7. Risks and planned responses.
{
  const s = page('Riesgos y respuestas');
  const rows = [
    ['Disponibilidad', 'Agendar con anticipación'],
    ['Retrasos', 'Priorizar alcance'],
    ['Dificultades técnicas', 'Preparar una alternativa sencilla'],
  ];
  rows.forEach(([risk, response], i) => {
    const y = 224 + i * 128;
    text(s, `riesgo-${i + 1}`, risk, 88, y, 445, 84, 33, C.ink, true);
    text(s, `respuesta-${i + 1}`, response, 596, y, 596, 90, 33, C.teal);
    if (i < 2) rule(s, `separador-${i + 1}`, 88, y + 90, 1104);
  });
}

// 8. Decision.
{
  const s = page('Próxima decisión', true);
  text(s, 'acuerdo', 'Acordar fecha de inicio\ny responsables', 88, 265, 1104, 210, 64, C.white, true);
}

let elapsed = 0;
for (let i = 0; i < notes.length; i++) {
  const n = notes[i];
  const stamp = seconds => `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, '0')}`;
  const timing = `Tiempo sugerido: ${n.seconds} segundos (${stamp(elapsed)} a ${stamp(elapsed + n.seconds)}).`;
  presentation.slides.items[i].speakerNotes.text = `${timing}\n\n${n.talk}\n\nTransición: ${n.transition}`;
  elapsed += n.seconds;
}

await fs.writeFile(path.join(sourceDir, 'notes.json'), JSON.stringify(notes, null, 2));
await fs.writeFile(path.join(buildDir, 'presentation.json'), JSON.stringify(presentation.toProto(), null, 2));
const candidatePath = path.join(buildDir, 'candidate.pptx');
await (await PresentationFile.exportPptx(presentation)).save(candidatePath);

// Validation runs from the shell, so the environment does not need Node spawnSync.
// The original finalizer was attempted but its subprocess wrapper reported EPERM.
console.log(JSON.stringify({ candidatePath, intendedOutput: filename, slides: presentation.slides.items.length,
  noteDurationSeconds: elapsed, font: FONT, canvas: [W, H] }, null, 2));
