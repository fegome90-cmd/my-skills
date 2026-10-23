import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { FileBlob, PresentationFile } from '@oai/artifact-tool';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const name = process.argv[2] || 'plan-talleres-2027.pptx';
if (name !== path.basename(name) || !name.endsWith('.pptx')) throw new Error('Expected a PPTX basename.');
const finalPath = path.join(root, 'output', name);
const p = await PresentationFile.importPptx(await FileBlob.load(finalPath));
const before = await p.inspect({ select: '$.slides[2].elements[*]', include: ['id', 'name', 'kind', 'text', 'position'] });
await fs.writeFile(path.join(root, 'checks', 'diagram-before-edit.ndjson'), before.ndjson);

// Exercise a real object edit on a disposable copy, leaving the deliverable unchanged.
const stage = p.slides.items[2].shapes.items.find(s => s.name === 'etapa-1');
if (!stage) throw new Error('The native stage object was not found after import.');
const beforeX = stage.position.left;
stage.text = 'Diagnóstico (comprobación)';
stage.position = { ...stage.position, left: beforeX + 16 };
const probePath = path.join(root, 'build', 'editability-probe.pptx');
await (await PresentationFile.exportPptx(p)).save(probePath);
const report = {
  finalPath, probePath, changedObject: 'slide 3 / etapa-1', changedText: 'Diagnóstico (comprobación)',
  beforeLeft: beforeX, afterLeft: stage.position.left,
  application: '@oai/artifact-tool 2.8.99', powerPointUI: 'NOT_RUN',
};
await fs.writeFile(path.join(root, 'checks', 'editability-probe.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
