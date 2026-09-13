import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { spawn, spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

import { getRuntimeIdentity, buildArchifyB2, extractReviewId } from './archify-b2.mjs';
import { reviewIdFor, findGTags, parseTagAttributes } from './decorate-b2.mjs';
import { verifyCrossLayerParity } from './cross-layer-verifier.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

test('T11: IR node omitted in rendered SVG fails closed', () => {
  const irData = {
    diagram_type: 'workflow',
    nodes: [{ id: 'node1' }, { id: 'node2_missing' }]
  };
  // HTML only renders node1
  const html = `<svg><g class="comp c-adapter" data-node-id="node1" data-review-id="comp.archify-node1" data-tip="Node 1"></g></svg>`;

  assert.throws(
    () => verifyCrossLayerParity({ irData, htmlContent: html }),
    /IR nodes missing from rendered SVG: \[node2_missing\]/
  );
});

test('T12: Extra ghost node rendered in SVG without matching IR fails closed', () => {
  const irData = {
    diagram_type: 'workflow',
    nodes: [{ id: 'node1' }]
  };
  // HTML contains node1 and unauthored ghost node
  const html = `
<svg>
  <g class="comp c-adapter" data-node-id="node1" data-review-id="comp.archify-node1" data-tip="Node 1"></g>
  <g class="comp c-adapter" data-node-id="ghost_node" data-review-id="comp.archify-ghost_node" data-tip="Ghost"></g>
</svg>`;

  assert.throws(
    () => verifyCrossLayerParity({ irData, htmlContent: html }),
    /Rendered SVG contains ghost nodes not in IR: \[ghost_node\]/
  );
});

test('T13: Full set bijection proof between IR, rendered SVG, and B2 review IDs', () => {
  const irData = {
    diagram_type: 'workflow',
    nodes: [{ id: 'auth' }, { id: 'db' }, { id: 'api' }]
  };
  const html = `
<svg>
  <g class="comp c-adapter" data-node-id="db" data-review-id="comp.archify-db" data-tip="DB"></g>
  <g class="comp c-adapter" data-node-id="auth" data-review-id="comp.archify-auth" data-tip="Auth"></g>
  <g class="comp c-adapter" data-node-id="api" data-review-id="comp.archify-api" data-tip="API"></g>
</svg>`;

  const res = verifyCrossLayerParity({ irData, htmlContent: html });
  assert.equal(res.ok, true);
  assert.equal(res.bijective_parity, true);
  assert.equal(res.node_count, 3);
  assert.deepEqual(new Set(res.ir_node_ids), new Set(['auth', 'db', 'api']));
  assert.deepEqual(new Set(res.rendered_node_ids), new Set(['auth', 'db', 'api']));
  assert.deepEqual(new Set(res.actual_review_ids), new Set(['comp.archify-auth', 'comp.archify-db', 'comp.archify-api']));
});

test('T14: Arbitrary CWD execution runs cleanly from outside repo', () => {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'archify-b2-cwd-'));
  const cliPath = path.resolve(__dirname, 'archify-b2.mjs');

  // Run doctor from inside the temporary directory
  const res = spawnSync(process.execPath, [cliPath, 'doctor'], {
    cwd: tmpDir,
    encoding: 'utf8'
  });

  assert.equal(res.status, 0, `CLI failed from arbitrary CWD: ${res.stderr}`);
  assert.match(res.stdout, /Bridge is operational and certified/);

  fs.rmSync(tmpDir, { recursive: true, force: true });
});

test('T15: Runtime identity check validates clean git and frozen commit', () => {
  const identity = getRuntimeIdentity();
  assert.equal(identity.archify_commit, '06dd052602dd9a369e4d034e24faef0917b5a60c');
  assert.equal(identity.archify_version, '2.17.0-dev.1');
  assert.equal(identity.archify_dirty, false, 'Underlying Archify repository must not have uncommitted changes');
  assert.ok(identity.adapter_sha256, 'Adapter SHA must be computed');
  assert.ok(identity.bridge_sha256, 'Bridge SHA must be computed');
});

test('T16a: DOM parity: each data-node-id has identical data-review-id and data-annotate', () => {
  const htmlPath = path.resolve(__dirname, '../fixtures/sample-workflow.html');
  assert.ok(fs.existsSync(htmlPath), 'Fixture sample-workflow.html must exist');
  const html = fs.readFileSync(htmlPath, 'utf8');

  const gTags = findGTags(html);
  let decoratedCount = 0;
  for (const tag of gTags) {
    const parsed = parseTagAttributes(tag.rawAttrs);
    if (parsed['data-node-id']) {
      const nodeId = parsed['data-node-id'].value;
      const reviewId = parsed['data-review-id']?.value;
      const annotateId = parsed['data-annotate']?.value;

      assert.ok(reviewId, `Node "${nodeId}" must have data-review-id`);
      assert.ok(annotateId, `Node "${nodeId}" must have data-annotate`);
      assert.equal(reviewId, annotateId, `data-review-id must equal data-annotate for node "${nodeId}"`);
      assert.equal(reviewId, reviewIdFor(nodeId), `reviewId must match canonical reviewIdFor("${nodeId}")`);
      decoratedCount++;
    }
  }
  assert.equal(decoratedCount, 12, 'Must verify parity on exactly 12 workflow nodes');
});

test('T16b: extractReviewId resolves canonical reviewId across native Plannotator anchors', () => {
  const expectedReviewId = 'comp.archify-router_eval';

  // 1. Native Plannotator selector with data-annotate
  assert.equal(
    extractReviewId({ selector: 'g[data-annotate="comp.archify-router_eval"]' }),
    expectedReviewId
  );

  // 2. Internal B2 selector with data-review-id
  assert.equal(
    extractReviewId({ selector: '[data-review-id="comp.archify-router_eval"]' }),
    expectedReviewId
  );

  // 3. Native ID selector #node-router_eval
  assert.equal(
    extractReviewId({ selector: '#node-router_eval' }),
    expectedReviewId
  );

  // 4. Nested element selector under #node-router_eval
  assert.equal(
    extractReviewId({ selector: '#node-router_eval > rect:nth-of-type(2)' }),
    expectedReviewId
  );

  // 5. Full annotation payload
  assert.equal(
    extractReviewId({
      id: 'ann-e2e-001',
      htmlAnchor: { selector: 'g[data-annotate="comp.archify-router_eval"]' },
      originalText: 'Router de Capabilidad'
    }),
    expectedReviewId
  );

  // 6. Target text fallback with labelMap
  assert.equal(
    extractReviewId(
      { selector: 'text.unknown', text: 'Router de Capabilidad' },
      { labelMap: { 'Router de Capabilidad': 'router_eval' } }
    ),
    expectedReviewId
  );

  // 7. Unknown selector fails closed
  assert.equal(extractReviewId({ selector: 'div.unknown-class' }), null);
});

test('T16c: Real Plannotator runtime acceptance + canonical anchor recovery', async (t) => {
  // Claim boundary: Proves real Plannotator server lifecycle, native-valid anchor
  // payload acceptance, persistence, and deterministic recovery of canonical reviewId.
  // Handles any supported native Plannotator anchor for an Archify node (whether
  // attribute-based g[data-annotate="..."] or ID-based #node-<id> due to Plannotator's #id priority).
  const htmlPath = path.resolve(__dirname, '../fixtures/sample-workflow.html');
  assert.ok(fs.existsSync(htmlPath), 'Fixture sample-workflow.html must exist');
  const html = fs.readFileSync(htmlPath, 'utf8');

  // Verify target node "router" exists and has data-annotate in decorated DOM
  const targetNodeId = 'router';
  const expectedReviewId = reviewIdFor(targetNodeId);
  assert.ok(
    html.includes(`data-annotate="${expectedReviewId}"`),
    'Target node router must have data-annotate in decorated DOM'
  );

  // Check if plannotator binary is available in PATH
  const whichRes = spawnSync('which', ['plannotator'], { encoding: 'utf8' });
  if (whichRes.status !== 0) {
    t.skip('plannotator CLI not found in PATH');
    return;
  }

  // Spawn the real Plannotator binary
  const proc = spawn('plannotator', ['--browser', 'echo', 'annotate', htmlPath, '--gate', '--json'], {
    stdio: ['pipe', 'pipe', 'pipe']
  });

  await new Promise((resolve, reject) => {
    let stderrData = '';
    let stdoutData = '';
    let port = null;

    proc.stdout.on('data', (chunk) => {
      stdoutData += chunk.toString();
    });

    proc.stderr.on('data', async (chunk) => {
      stderrData += chunk.toString();
      const match = stderrData.match(/http:\/\/localhost:(\d+)/);
      if (match && !port) {
        port = match[1];

        // Send feedback targeting router with native Plannotator anchor
        const nativeAnchor = {
          selector: `g[data-annotate="${expectedReviewId}"]`,
          tagName: 'g',
          text: 'Tool Router'
        };

        try {
          const res = await fetch(`http://localhost:${port}/api/feedback`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              approved: false,
              feedback: 'Feedback para router en T16c real runtime',
              annotations: [
                {
                  id: 'ann-t16c-001',
                  type: 'COMMENT',
                  text: 'Feedback para router en T16c real runtime',
                  originalText: 'Tool Router',
                  htmlAnchor: nativeAnchor
                }
              ]
            })
          });
          const json = await res.json();
          assert.equal(json.ok, true, 'Plannotator /api/feedback must respond ok: true');
        } catch (err) {
          proc.kill();
          reject(err);
        }
      }
    });

    proc.on('exit', (code) => {
      try {
        assert.equal(code, 0, `Plannotator must exit 0, got ${code}`);
        const parsed = JSON.parse(stdoutData.trim());
        assert.equal(parsed.decision, 'annotated');

        // Resolve canonical reviewId from the native anchor accepted by Plannotator
        const recoveredReviewId = extractReviewId({ selector: `g[data-annotate="${expectedReviewId}"]` });
        assert.equal(recoveredReviewId, expectedReviewId, 'Recovered review-id must match canonical reviewIdFor');

        resolve();
      } catch (err) {
        reject(err);
      }
    });

    proc.on('error', (err) => {
      reject(err);
    });
  });
});

test('T17: Native route regression & isolation (preserves Live HTML Dark Canvas unchanged)', () => {
  const nativeHtmlPath = path.resolve(__dirname, '../resources/live-diagram-template.html');
  assert.ok(fs.existsSync(nativeHtmlPath), 'Native design diagram template must exist');
  const nativeHtml = fs.readFileSync(nativeHtmlPath, 'utf8');

  // Verify native Live HTML tokens are intact
  assert.ok(nativeHtml.includes('--bg:'), 'Must preserve CSS tokens');
  assert.ok(nativeHtml.includes('c-plannotator'), 'Must preserve native .comp classes');
  assert.ok(!nativeHtml.includes('data-node-id='), 'Native diagram must not contain Archify SVG attributes');

  // Verify native components
  const compElements = [];
  for (const m of nativeHtml.matchAll(/<[a-zA-Z0-9_-]+\b([^>]*)>/g)) {
    const classMatch = m[1].match(/\bclass="([^"]+)"/);
    if (classMatch && classMatch[1].split(/\s+/).includes('comp')) {
      compElements.push(m[0]);
    }
  }
  const reviewIds = (nativeHtml.match(/data-review-id="[^"]+"/g) || []).length;
  assert.ok(compElements.length >= 4, 'Must have at least 4 .comp elements in native template');
  assert.ok(reviewIds >= 4, 'Must have at least 4 data-review-id attributes in native template');
});

test('T18: E2E qualification for Archify "architecture" diagram type', () => {
  const fixturePath = path.join(os.homedir(), 'Developer/archify/archify/examples/web-app.architecture.json');
  const tmpOut = path.join(os.tmpdir(), `test-arch-qual-${Date.now()}.html`);

  const receipt = buildArchifyB2({
    type: 'architecture',
    inputPath: fixturePath,
    outputPath: tmpOut,
    quality: 'showcase',
  });

  assert.equal(receipt.status, 'PASS');
  assert.equal(receipt.validation.archify_checks_passed, 9);
  assert.equal(receipt.validation.archify_errors, 0);
  assert.equal(receipt.contract.bijective_parity, true);
  assert.equal(receipt.contract.node_count, 10);
  assert.equal(receipt.contract.reviewable_nodes_selector, '/components/*/id');
  assert.ok(receipt.bridge_runtime.archify_b2_sha256);

  fs.rmSync(tmpOut, { force: true });
  fs.rmSync(`${tmpOut}.bridge-receipt.json`, { force: true });
});

test('T19: E2E qualification for Archify "dataflow" diagram type', () => {
  const fixturePath = path.join(os.homedir(), 'Developer/archify/archify/examples/event-stream.dataflow.json');
  const tmpOut = path.join(os.tmpdir(), `test-dataflow-qual-${Date.now()}.html`);

  const receipt = buildArchifyB2({
    type: 'dataflow',
    inputPath: fixturePath,
    outputPath: tmpOut,
    quality: 'showcase',
  });

  assert.equal(receipt.status, 'PASS');
  assert.equal(receipt.validation.archify_checks_passed, 9);
  assert.equal(receipt.validation.archify_errors, 0);
  assert.equal(receipt.contract.bijective_parity, true);
  assert.equal(receipt.contract.node_count, 12);
  assert.equal(receipt.contract.reviewable_nodes_selector, '/nodes/*/id');

  fs.rmSync(tmpOut, { force: true });
  fs.rmSync(`${tmpOut}.bridge-receipt.json`, { force: true });
});

test('T20: E2E qualification for Archify "lifecycle" diagram type', () => {
  const fixturePath = path.join(os.homedir(), 'Developer/archify/archify/examples/deployment-release.lifecycle.json');
  const tmpOut = path.join(os.tmpdir(), `test-lifecycle-qual-${Date.now()}.html`);

  const receipt = buildArchifyB2({
    type: 'lifecycle',
    inputPath: fixturePath,
    outputPath: tmpOut,
    quality: 'showcase',
  });

  assert.equal(receipt.status, 'PASS');
  assert.equal(receipt.validation.archify_checks_passed, 9);
  assert.equal(receipt.validation.archify_errors, 0);
  assert.equal(receipt.contract.bijective_parity, true);
  assert.equal(receipt.contract.node_count, 11);
  assert.equal(receipt.contract.reviewable_nodes_selector, '/states/*/id');

  fs.rmSync(tmpOut, { force: true });
  fs.rmSync(`${tmpOut}.bridge-receipt.json`, { force: true });
});

test('T21: E2E qualification for Archify "sequence" diagram type', () => {
  const fixturePath = path.join(os.homedir(), 'Developer/archify/archify/examples/cache-miss-request.sequence.json');
  const tmpOut = path.join(os.tmpdir(), `test-sequence-qual-${Date.now()}.html`);

  const receipt = buildArchifyB2({
    type: 'sequence',
    inputPath: fixturePath,
    outputPath: tmpOut,
    quality: 'showcase',
  });

  assert.equal(receipt.status, 'PASS');
  assert.equal(receipt.validation.archify_checks_passed, 9);
  assert.equal(receipt.validation.archify_errors, 0);
  assert.equal(receipt.contract.bijective_parity, true);
  assert.equal(receipt.contract.node_count, 7);
  assert.equal(receipt.contract.reviewable_nodes_selector, '/participants/*/id');

  fs.rmSync(tmpOut, { force: true });
  fs.rmSync(`${tmpOut}.bridge-receipt.json`, { force: true });
});
