import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { spawnSync } from 'node:child_process';
import { decorateB2, reviewIdFor, extractReviewId, escapeHtml } from './decorate-b2.mjs';

test('T01: normal single node gets B2 decoration', () => {
  const html = `<svg><g id="node-auth" data-node-id="auth" data-node-label="Auth Service" tabindex="0"><rect/></g></svg>`;
  const decorated = decorateB2(html);
  assert.match(decorated, /class="comp c-adapter"/);
  assert.match(decorated, /data-review-id="comp\.archify-auth"/);
  assert.match(decorated, /data-annotate="comp\.archify-auth"/);
  assert.match(decorated, /data-tip="Auth Service"/);
});

test('T02: multiple nodes with distinct IDs receive bijective 1:1 review-ids and data-annotate', () => {
  const html = `
<svg>
  <g id="node-1" data-node-id="req_portal" data-node-label="Request Portal"></g>
  <g id="node-2" data-node-id="auth_srv" data-node-label="Auth Gateway"></g>
  <g id="node-3" data-node-id="db_store" data-node-label="Postgres DB"></g>
</svg>`;
  const decorated = decorateB2(html);
  const comps = decorated.match(/\bclass="[^"]*\bcomp\b[^"]*"/g) || [];
  const reviewIds = (decorated.match(/\bdata-review-id="([^"]+)"/g) || []).map(m => m.slice(16, -1));
  const annotateIds = (decorated.match(/\bdata-annotate="([^"]+)"/g) || []).map(m => m.slice(15, -1));
  const uniqueIds = new Set(reviewIds);
  const uniqueAnnotateIds = new Set(annotateIds);

  assert.equal(comps.length, 3);
  assert.equal(reviewIds.length, 3);
  assert.equal(annotateIds.length, 3);
  assert.equal(uniqueIds.size, 3);
  assert.equal(uniqueAnnotateIds.size, 3);
  assert.deepEqual(reviewIds, annotateIds, 'data-review-id and data-annotate must have identical values');
  assert.match(decorated, /data-review-id="comp\.archify-req_portal"/);
  assert.match(decorated, /data-annotate="comp\.archify-req_portal"/);
  assert.match(decorated, /data-review-id="comp\.archify-auth_srv"/);
  assert.match(decorated, /data-annotate="comp\.archify-auth_srv"/);
  assert.match(decorated, /data-review-id="comp\.archify-db_store"/);
  assert.match(decorated, /data-annotate="comp\.archify-db_store"/);
});

test('T03: preserves existing classes when adding comp c-adapter', () => {
  const html = `<svg><g id="node-1" class="archify-node highlight" data-node-id="node1" data-node-label="Test"></g></svg>`;
  const decorated = decorateB2(html);
  assert.match(decorated, /class="archify-node highlight comp c-adapter"/);
});

test('T04: attribute order variants and multiline tags are parsed robustly', () => {
  const html = `
<svg>
  <g
    tabindex="0"
    role="group"
    data-node-label="Multiline Service"
    id="node-multi"
    data-node-id="multi_srv"
    aria-label="Multi">
  </g>
</svg>`;
  const decorated = decorateB2(html);
  assert.match(decorated, /data-review-id="comp\.archify-multi_srv"/);
  assert.match(decorated, /data-annotate="comp\.archify-multi_srv"/);
  assert.match(decorated, /data-tip="Multiline Service"/);
  assert.match(decorated, /class="[^"]*\bcomp c-adapter\b[^"]*"/);
});

test('T05: escapes HTML entities in data-tip while preserving Unicode and tag syntax', () => {
  // Label containing <Tag>, &, quotes, and Unicode
  const html = `<svg><g data-node-id="edge" data-node-label='Input <Tag> & "Quotes" Single 日本語'></g></svg>`;
  const decorated = decorateB2(html);
  assert.match(decorated, /data-tip="Input &lt;Tag&gt; &amp; &quot;Quotes&quot; Single 日本語"/);
});

test('T06: duplicate data-node-id fails closed with diagnostic error', () => {
  const html = `
<svg>
  <g id="node-1" data-node-id="duplicate_id" data-node-label="First"></g>
  <g id="node-2" data-node-id="duplicate_id" data-node-label="Second"></g>
</svg>`;
  assert.throws(() => decorateB2(html), /Duplicate data-node-id detected: "duplicate_id"/);
});

test('T07: reviewIdFor collision fails closed', () => {
  // Two distinct nodeIds that would map to identical sanitized strings
  const html = `
<svg>
  <g data-node-id="user/auth" data-node-label="Slash"></g>
  <g data-node-id="user.auth" data-node-label="Dot"></g>
</svg>`;
  assert.throws(() => decorateB2(html), /Collision detected/);
});

test('T08: strict idempotence: decorate(decorate(x)) === decorate(x)', () => {
  const html = `
<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
  <svg>
    <g id="node-1" data-node-id="srv1" data-node-label="Service 1"></g>
    <g id="node-2" data-node-id="srv2" data-node-label="Service 2"></g>
  </svg>
</body>
</html>`;
  const pass1 = decorateB2(html);
  assert.match(pass1, /data-annotate="comp\.archify-srv1"/);
  assert.match(pass1, /data-annotate="comp\.archify-srv2"/);
  const pass2 = decorateB2(pass1);
  assert.equal(pass2, pass1, 'Second decoration pass must be strictly identical to first');
});

test('T09: reviewIdFor edge cases and determinism', () => {
  assert.equal(reviewIdFor('AuthGateway'), 'comp.archify-authgateway');
  assert.equal(reviewIdFor('  user_session  '), 'comp.archify-user_session');
  assert.equal(reviewIdFor('service-1'), 'comp.archify-service-1');
  assert.throws(() => reviewIdFor(''), /Empty or invalid nodeId/);
  assert.throws(() => reviewIdFor(null), /Empty or invalid nodeId/);
});

test('T10: atomic write CLI writes via tempfile and validates correctly', () => {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'b2-test-'));
  const testFile = path.join(tmpDir, 'test.html');
  const validHtml = `<svg><g data-node-id="node1" data-node-label="Node 1"></g></svg>`;
  fs.writeFileSync(testFile, validHtml, 'utf8');

  const cliPath = path.resolve('skills/diagram-maker-plus/scripts/decorate-b2.mjs');
  const res = spawnSync(process.execPath, [cliPath, testFile, '--in-place', '--json'], { encoding: 'utf8' });

  assert.equal(res.status, 0, `CLI failed: ${res.stderr}`);
  const receipt = JSON.parse(res.stdout);
  assert.equal(receipt.status, 'PASS');
  assert.equal(receipt.parity_1to1, true);
  assert.equal(receipt.atomic_write, true);
  assert.equal(receipt.components_count, 1);
  assert.equal(receipt.review_ids_count, 1);
  assert.equal(receipt.annotate_ids_count, 1);
  assert.equal(receipt.archify_version, '2.17.0-dev.1');
  assert.equal(receipt.archify_commit, '06dd052602dd9a369e4d034e24faef0917b5a60c');

  // Cleanup
  fs.rmSync(tmpDir, { recursive: true, force: true });
});

test('T10b: extractReviewId resolves correctly across formats and ladders', () => {
  // 1. Native Plannotator data-annotate selector
  assert.equal(extractReviewId('g[data-annotate="comp.archify-srv1"]'), 'comp.archify-srv1');
  assert.equal(extractReviewId({ selector: 'g[data-annotate="comp.archify-srv1"]' }), 'comp.archify-srv1');

  // 2. Internal B2 data-review-id selector
  assert.equal(extractReviewId('[data-review-id="comp.archify-srv1"]'), 'comp.archify-srv1');

  // 3. ID selector
  assert.equal(extractReviewId('#node-srv1'), 'comp.archify-srv1');
  assert.equal(extractReviewId('#node-srv1 > rect:nth-of-type(1)'), 'comp.archify-srv1');

  // 4. Annotation object
  assert.equal(extractReviewId({
    id: 'ann-1',
    htmlAnchor: { selector: 'g[data-annotate="comp.archify-srv1"]' }
  }), 'comp.archify-srv1');

  // 5. Fallback via labelMap
  assert.equal(extractReviewId({ selector: 'span.label', text: 'Service 1' }, { labelMap: { 'Service 1': 'srv1' } }), 'comp.archify-srv1');

  // 6. Fail closed
  assert.equal(extractReviewId({ selector: 'body > div' }), null);
  assert.equal(extractReviewId(null), null);
});
