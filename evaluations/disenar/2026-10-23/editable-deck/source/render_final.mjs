import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { FileBlob, PresentationFile } from '@oai/artifact-tool';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const name = process.argv[2] || 'plan-talleres-2027.pptx';
if (name !== path.basename(name) || !name.endsWith('.pptx')) throw new Error('Expected a PPTX basename.');
const finalPath = path.join(root, 'output', name);
const p = await PresentationFile.importPptx(await FileBlob.load(finalPath));
if (p.slides.items.length !== 8) throw new Error('Expected exactly eight slides.');
for (const [i, slide] of p.slides.items.entries()) {
  const stem = `slide-${String(i + 1).padStart(2, '0')}`;
  const png = await p.export({ slide, format: 'png', scale: 1 });
  await fs.writeFile(path.join(root, 'renders', `${stem}.png`), new Uint8Array(await png.arrayBuffer()));
  const layout = await slide.export({ format: 'layout' });
  await fs.writeFile(path.join(root, 'checks', `${stem}.layout.json`), await layout.text());
}
console.log(JSON.stringify({ finalPath, renders: 8, engine: '@oai/artifact-tool 2.8.99' }, null, 2));
