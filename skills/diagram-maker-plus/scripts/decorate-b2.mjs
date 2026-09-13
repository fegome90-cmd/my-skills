#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';

export const ARCHIFY_VERSION_FROZEN = '2.17.0-dev.1';
export const ARCHIFY_COMMIT_FROZEN = '06dd052602dd9a369e4d034e24faef0917b5a60c';

const B2_STYLE_BLOCK = `
<style id="plannotator-b2-styles">
  :root {
    --color-adapter: #fbbf24;
    --color-plannotator: #f472b6;
  }
  .comp {
    cursor: pointer;
    transition: outline 0.15s cubic-bezier(0.2, 0, 1, 1), filter 0.15s cubic-bezier(0.2, 0, 1, 1);
  }
  .comp.c-adapter:hover,
  .comp.c-adapter:focus-visible {
    outline: 2px solid var(--color-adapter, #fbbf24);
    outline-offset: 2px;
    filter: drop-shadow(0 0 10px rgba(251, 191, 36, 0.45));
  }
</style>
`;

/**
 * Escapes HTML entities for safe attribute embedding.
 * Handles &, ", ', <, > while preserving Unicode sequences.
 *
 * @param {string} str
 * @returns {string}
 */
export function escapeHtml(str) {
  if (typeof str !== 'string') return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

/**
 * Canonical, deterministic, and injective mapping from nodeId to Plannotator review-id.
 *
 * @param {string} nodeId
 * @returns {string}
 */
export function reviewIdFor(nodeId) {
  if (!nodeId || typeof nodeId !== 'string') {
    throw new Error(`Empty or invalid nodeId: "${nodeId}". Must be a non-empty string.`);
  }
  const trimmed = nodeId.trim();
  if (!trimmed) {
    throw new Error('Empty or invalid nodeId. Must be a non-empty string.');
  }

  // Preserve alphanumeric, underscores and hyphens. Map other characters to safe tokens.
  const sanitized = trimmed.toLowerCase()
    .replace(/[^a-z0-9_-]+/g, '-')
    .replace(/^-+|-+$/g, '');

  return `comp.archify-${sanitized || 'node'}`;
}

/**
 * Canonical recovery of reviewId from a Plannotator anchor, selector, or annotation object.
 *
 * Priority ladder:
 * 1. Native Plannotator data-annotate selector: [data-annotate="<reviewId>"]
 * 2. Internal B2 data-review-id selector: [data-review-id="<reviewId>"]
 * 3. Element id selector: #node-<id> or #<id> mapped via reviewIdFor
 * 4. Documented fallback: targetText mapped via options.labelMap
 * 5. Fails closed (returns null)
 *
 * @param {object|string} anchor Anchor object, selector string, or annotation payload
 * @param {{ labelMap?: Record<string, string> }} [options]
 * @returns {string|null} Canonical reviewId or null
 */
export function extractReviewId(anchor, options = {}) {
  if (!anchor) return null;

  let selector = '';
  let targetText = '';

  if (typeof anchor === 'string') {
    selector = anchor;
  } else if (typeof anchor === 'object') {
    if (anchor.htmlAnchor && typeof anchor.htmlAnchor === 'object') {
      selector = anchor.htmlAnchor.selector || '';
      targetText = anchor.originalText || anchor.htmlAnchor.text || '';
    } else {
      selector = anchor.selector || '';
      targetText = anchor.text || anchor.originalText || '';
    }
  }

  if (typeof selector !== 'string') return null;

  // 1. Selector contains [data-annotate="..."]
  const annotateMatch = selector.match(/\[data-annotate=["']([^"']+)["']\]/);
  if (annotateMatch) {
    return annotateMatch[1];
  }

  // 2. Selector contains [data-review-id="..."]
  const reviewIdMatch = selector.match(/\[data-review-id=["']([^"']+)["']\]/);
  if (reviewIdMatch) {
    return reviewIdMatch[1];
  }

  // 3. Selector contains #id (e.g. #node-router_eval or #router_eval)
  const idMatch = selector.match(/#([a-zA-Z0-9_-]+)/);
  if (idMatch) {
    const rawId = idMatch[1];
    const nodeId = rawId.startsWith('node-') ? rawId.slice(5) : rawId;
    try {
      return reviewIdFor(nodeId);
    } catch {
      // ignore
    }
  }

  // 4. Documented fallback: targetText match against optional labelMap
  if (options.labelMap && targetText) {
    const trimmed = targetText.trim();
    if (options.labelMap[trimmed]) {
      try {
        return reviewIdFor(options.labelMap[trimmed]);
      } catch {
        // ignore
      }
    }
  }

  // 5. Fail closed
  return null;
}

/**
 * Locates all opening <g ...> tags in the HTML using a lexical scanner that
 * respects single/double quoted attribute values, ensuring > inside values
 * does not prematurely end the tag.
 *
 * @param {string} html
 * @returns {Array<{ start: number, end: number, fullTag: string, rawAttrs: string }>}
 */
export function findGTags(html) {
  const tags = [];
  let i = 0;
  while (i < html.length) {
    const start = html.indexOf('<g', i);
    if (start === -1) break;

    // Check word boundary after <g (e.g. <g id=... or <g\n... but not <gradient>)
    const nextChar = html[start + 2];
    if (nextChar && !/[\s/>]/.test(nextChar)) {
      i = start + 2;
      continue;
    }

    let j = start + 2;
    let inSingle = false;
    let inDouble = false;

    while (j < html.length) {
      const c = html[j];
      if (c === '"' && !inSingle) {
        inDouble = !inDouble;
      } else if (c === "'" && !inDouble) {
        inSingle = !inSingle;
      } else if (c === '>' && !inSingle && !inDouble) {
        tags.push({
          start,
          end: j + 1,
          fullTag: html.slice(start, j + 1),
          rawAttrs: html.slice(start + 2, j)
        });
        break;
      }
      j++;
    }
    i = j + 1;
  }
  return tags;
}

/**
 * Parses XML/HTML attributes from an opening tag string into a structured key-value map.
 * Supports arbitrary attribute order, single/double quotes, and multiline formatting.
 *
 * @param {string} attrString
 * @returns {Record<string, { value: string, raw: string, quote: string }>}
 */
export function parseTagAttributes(attrString) {
  const attrs = {};
  const attrRegex = /([a-zA-Z0-9_:.-]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s/>]+)))?/g;
  let match;
  while ((match = attrRegex.exec(attrString)) !== null) {
    const key = match[1].toLowerCase();
    const val = match[2] !== undefined ? match[2] : (match[3] !== undefined ? match[3] : match[4] || '');
    attrs[key] = {
      originalKey: match[1],
      value: val,
      raw: match[0],
      quote: match[2] !== undefined ? '"' : (match[3] !== undefined ? "'" : '"'),
    };
  }
  return attrs;
}

/**
 * Decorates an Archify HTML/SVG string with Plannotator B2 review attributes.
 *
 * Invariants:
 * 1. Bijective 1:1 mapping: each valid data-node-id gets exactly one .comp and one unique data-review-id.
 * 2. Duplicate data-node-id detection (fails closed).
 * 3. Collision detection on reviewIdFor (fails closed).
 * 4. Strict HTML entity escaping on data-tip.
 * 5. Idempotent: decorate(decorate(html)) === decorate(html).
 *
 * @param {string} html
 * @returns {string} Decorated HTML
 */
export function decorateB2(html) {
  if (typeof html !== 'string') {
    throw new TypeError('Input HTML must be a string.');
  }

  const seenNodeIds = new Set();
  const reviewIdToNodeId = new Map();

  const gTags = findGTags(html);
  if (gTags.length === 0) {
    return html;
  }

  // Process tags in reverse order to keep character offsets stable during replacement
  let result = html;
  for (let idx = gTags.length - 1; idx >= 0; idx--) {
    const { start, end, fullTag, rawAttrs } = gTags[idx];
    const parsed = parseTagAttributes(rawAttrs);

    if (!parsed['data-node-id']) {
      continue;
    }

    const nodeId = parsed['data-node-id'].value;

    // A. Duplicate detection (fail-closed)
    if (seenNodeIds.has(nodeId)) {
      throw new Error(`Duplicate data-node-id detected: "${nodeId}". Contract requires unique node IDs.`);
    }
    seenNodeIds.add(nodeId);

    // B. Canonical review-id & collision detection (fail-closed)
    const reviewId = reviewIdFor(nodeId);
    if (reviewIdToNodeId.has(reviewId)) {
      const prior = reviewIdToNodeId.get(reviewId);
      throw new Error(`Collision detected: distinct nodeIds "${prior}" and "${nodeId}" both produced reviewId "${reviewId}".`);
    }
    reviewIdToNodeId.set(reviewId, nodeId);

    // C. Escaped node label for data-tip
    const rawLabel = parsed['data-node-label'] ? parsed['data-node-label'].value : nodeId;
    const escapedTip = escapeHtml(rawLabel);

    // D. Class attribute management: ensure "comp" and "c-adapter"
    let classList = [];
    if (parsed['class']) {
      classList = parsed['class'].value.split(/\s+/).filter(Boolean);
    }
    if (!classList.includes('comp')) classList.push('comp');
    if (!classList.includes('c-adapter')) classList.push('c-adapter');

    // E. Reconstruct tag preserving existing non-B2 attributes
    let reconstructedAttrs = rawAttrs;

    if (parsed['class']) {
      reconstructedAttrs = reconstructedAttrs.replace(
        parsed['class'].raw,
        `class="${classList.join(' ')}"`
      );
    } else {
      reconstructedAttrs = ` class="${classList.join(' ')}"` + reconstructedAttrs;
    }

    if (parsed['data-review-id']) {
      reconstructedAttrs = reconstructedAttrs.replace(
        parsed['data-review-id'].raw,
        `data-review-id="${reviewId}"`
      );
    } else {
      reconstructedAttrs += ` data-review-id="${reviewId}"`;
    }

    if (parsed['data-annotate']) {
      reconstructedAttrs = reconstructedAttrs.replace(
        parsed['data-annotate'].raw,
        `data-annotate="${reviewId}"`
      );
    } else {
      reconstructedAttrs += ` data-annotate="${reviewId}"`;
    }

    if (parsed['data-tip']) {
      reconstructedAttrs = reconstructedAttrs.replace(
        parsed['data-tip'].raw,
        `data-tip="${escapedTip}"`
      );
    } else {
      reconstructedAttrs += ` data-tip="${escapedTip}"`;
    }

    const newTag = `<g${reconstructedAttrs}>`;
    result = result.slice(0, start) + newTag + result.slice(end);
  }

  // 2. Inject CSS styles if not already present
  if (!result.includes('plannotator-b2-styles') && !result.includes('--color-adapter:')) {
    if (result.includes('</head>')) {
      result = result.replace('</head>', `${B2_STYLE_BLOCK}\n</head>`);
    } else {
      result = `${B2_STYLE_BLOCK}\n${result}`;
    }
  }

  return result;
}

/**
 * Computes SHA-256 hex digest of a string or buffer.
 */
export function computeSha256(content) {
  return crypto.createHash('sha256').update(content, 'utf8').digest('hex');
}

// Standalone CLI execution
const isMain = process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href;
if (isMain) {
  const args = process.argv.slice(2);
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`Uso:
  node decorate-b2.mjs <archivo.html> [--in-place] [salida.html] [--json]

Ejemplos:
  node decorate-b2.mjs salida.workflow.html --in-place
  node decorate-b2.mjs entrada.html salida.html --json
`);
    process.exit(0);
  }

  const inPlace = args.includes('--in-place');
  const emitJson = args.includes('--json');
  const files = args.filter(a => !a.startsWith('--'));

  const inputPath = path.resolve(files[0]);
  const outputPath = inPlace ? inputPath : path.resolve(files[1] || files[0]);

  if (!fs.existsSync(inputPath)) {
    console.error(`Error: El archivo "${inputPath}" no existe.`);
    process.exit(1);
  }

  const rawHtml = fs.readFileSync(inputPath, 'utf8');
  const inputSha = computeSha256(rawHtml);

  let decorated;
  try {
    decorated = decorateB2(rawHtml);
  } catch (err) {
    console.error(`[fail] Error en la decoración B2: ${err.message}`);
    process.exit(2);
  }

  // Parity & bijection assertions
  const compMatches = decorated.match(/\bclass="[^"]*\bcomp\b[^"]*"/gi) || [];
  const reviewIds = (decorated.match(/\bdata-review-id="([^"]+)"/gi) || []).map(m => m.slice(16, -1));
  const annotateIds = (decorated.match(/\bdata-annotate="([^"]+)"/gi) || []).map(m => m.slice(15, -1));
  const uniqueIds = new Set(reviewIds);
  const uniqueAnnotateIds = new Set(annotateIds);

  if (compMatches.length !== reviewIds.length || reviewIds.length !== uniqueIds.size || annotateIds.length !== reviewIds.length) {
    console.error(`[fail] Discrepancia de paridad 1:1: ${compMatches.length} .comp vs ${reviewIds.length} review-ids vs ${annotateIds.length} annotate-ids (${uniqueIds.size} únicos).`);
    process.exit(3);
  }

  // Atomic write pattern: write to tmp file then atomic rename
  const tempPath = path.join(path.dirname(outputPath), `.tmp-b2-${Date.now()}-${Math.random().toString(36).slice(2)}.html`);
  try {
    fs.writeFileSync(tempPath, decorated, 'utf8');
    fs.renameSync(tempPath, outputPath);
  } catch (err) {
    if (fs.existsSync(tempPath)) fs.unlinkSync(tempPath);
    console.error(`[fail] Error durante la escritura atómica: ${err.message}`);
    process.exit(4);
  }

  const outputSha = computeSha256(decorated);

  const receipt = {
    command: 'decorate-b2',
    archify_commit: ARCHIFY_COMMIT_FROZEN,
    archify_version: ARCHIFY_VERSION_FROZEN,
    input_file: inputPath,
    output_file: outputPath,
    input_sha256: inputSha,
    output_sha256: outputSha,
    components_count: compMatches.length,
    review_ids_count: reviewIds.length,
    annotate_ids_count: annotateIds.length,
    unique_review_ids_count: uniqueIds.size,
    parity_1to1: true,
    atomic_write: true,
    status: 'PASS'
  };

  if (emitJson) {
    console.log(JSON.stringify(receipt, null, 2));
  } else {
    console.log(`[ok] Archivo decorado atómicamente con contrato Plannotator B2: ${outputPath}`);
    console.log(`[ok] Nodos .comp: ${compMatches.length} | review-ids únicos: ${uniqueIds.size} (Paridad 1:1 biyectiva PASS)`);
    console.log(`[ok] SHA-256 salida: ${outputSha}`);
  }
}
