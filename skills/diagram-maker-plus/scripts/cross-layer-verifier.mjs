import { findGTags, parseTagAttributes, reviewIdFor } from './decorate-b2.mjs';

/**
 * Extracts author-defined reviewable node IDs from a JSON-IR specification.
 *
 * @param {object} irData Parsed JSON-IR object
 * @returns {string[]} List of node IDs defined in the IR
 */
export function extractIrNodeIds(irData) {
  if (!irData || typeof irData !== 'object') {
    throw new TypeError('Invalid JSON-IR: expected object.');
  }

  const diagramType = irData.diagram_type;
  let rawList = [];

  switch (diagramType) {
    case 'workflow':
      rawList = (irData.nodes || []).map(n => n.id);
      break;
    case 'architecture':
      rawList = (irData.components || irData.nodes || []).map(c => c.id);
      break;
    case 'dataflow':
      rawList = (irData.nodes || []).map(n => n.id);
      break;
    case 'lifecycle':
      rawList = (irData.states || []).map(s => s.id);
      break;
    case 'sequence':
      rawList = (irData.participants || []).map(p => p.id);
      break;
    default:
      if (Array.isArray(irData.nodes)) {
        rawList = irData.nodes.map(n => n.id);
      } else if (Array.isArray(irData.components)) {
        rawList = irData.components.map(c => c.id);
      } else {
        throw new Error(`Cannot extract node IDs for unknown diagram_type: "${diagramType}"`);
      }
  }

  return rawList;
}

/**
 * Extracts rendered node IDs and B2 component review IDs from HTML.
 *
 * @param {string} html Content of rendered or decorated HTML
 * @returns {{ renderedNodeIds: string[], b2ComponentIds: string[], actualReviewIds: string[] }}
 */
export function extractHtmlNodeDetails(html) {
  const gTags = findGTags(html);
  const renderedNodeIds = [];
  const b2ComponentIds = [];
  const actualReviewIds = [];

  for (const tag of gTags) {
    const parsed = parseTagAttributes(tag.rawAttrs);
    if (parsed['data-node-id']) {
      const nodeId = parsed['data-node-id'].value;
      renderedNodeIds.push(nodeId);

      const classes = (parsed['class'] ? parsed['class'].value : '').split(/\s+/);
      if (classes.includes('comp') && classes.includes('c-adapter')) {
        b2ComponentIds.push(nodeId);
      }

      if (parsed['data-review-id']) {
        actualReviewIds.push(parsed['data-review-id'].value);
      }
    }
  }

  return { renderedNodeIds, b2ComponentIds, actualReviewIds };
}

/**
 * Proves bijective cross-layer parity across IR specification, rendered SVG,
 * and decorated B2 components.
 *
 * Proof requirements:
 * 1. len(ir_ids) == len(set(ir_ids)) — IR has no duplicate node IDs.
 * 2. len(rendered_ids) == len(set(rendered_ids)) — SVG has no duplicate node IDs.
 * 3. len(actual_review_ids) == len(set(actual_review_ids)) — B2 has no duplicate review IDs.
 * 4. set(ir_ids) == set(rendered_ids) — Bijective correspondence: no missing or ghost nodes.
 * 5. expected_review_ids == set(actual_review_ids) — Injective canonical mapping proven.
 * 6. len(b2_components) == len(actual_review_ids) — Every rendered node is decorated as B2 component.
 *
 * @param {{ irData: object, htmlContent: string }} params
 * @returns {{ ok: boolean, ir_node_ids: string[], rendered_node_ids: string[], actual_review_ids: string[], bijective_parity: boolean }}
 */
export function verifyCrossLayerParity({ irData, htmlContent }) {
  const irNodeIds = extractIrNodeIds(irData);
  const { renderedNodeIds, b2ComponentIds, actualReviewIds } = extractHtmlNodeDetails(htmlContent);

  const irSet = new Set(irNodeIds);
  const renderedSet = new Set(renderedNodeIds);
  const reviewSet = new Set(actualReviewIds);

  // 1. Cardinality vs Uniqueness check
  if (irNodeIds.length !== irSet.size) {
    throw new Error(`Cross-layer failure: IR contains duplicate node IDs (${irNodeIds.length} items vs ${irSet.size} unique).`);
  }
  if (renderedNodeIds.length !== renderedSet.size) {
    throw new Error(`Cross-layer failure: Rendered SVG contains duplicate data-node-id (${renderedNodeIds.length} items vs ${renderedSet.size} unique).`);
  }
  if (actualReviewIds.length !== reviewSet.size) {
    throw new Error(`Cross-layer failure: Decorated B2 contains duplicate data-review-id (${actualReviewIds.length} items vs ${reviewSet.size} unique).`);
  }

  // 2. Set equality check: IR nodes == Rendered SVG nodes
  const missingInRendered = irNodeIds.filter(id => !renderedSet.has(id));
  const ghostInRendered = renderedNodeIds.filter(id => !irSet.has(id));

  if (missingInRendered.length > 0) {
    throw new Error(`Cross-layer failure: IR nodes missing from rendered SVG: [${missingInRendered.join(', ')}].`);
  }
  if (ghostInRendered.length > 0) {
    throw new Error(`Cross-layer failure: Rendered SVG contains ghost nodes not in IR: [${ghostInRendered.join(', ')}].`);
  }

  // 3. Set equality check: expected_review_ids == actual_review_ids
  const expectedReviewIds = new Set(irNodeIds.map(reviewIdFor));
  const missingReviewIds = [...expectedReviewIds].filter(rId => !reviewSet.has(rId));
  const unexpectedReviewIds = actualReviewIds.filter(rId => !expectedReviewIds.has(rId));

  if (missingReviewIds.length > 0) {
    throw new Error(`Cross-layer failure: Missing expected review-ids in B2 decoration: [${missingReviewIds.join(', ')}].`);
  }
  if (unexpectedReviewIds.length > 0) {
    throw new Error(`Cross-layer failure: Unexpected review-ids found in B2 decoration: [${unexpectedReviewIds.join(', ')}].`);
  }

  // 4. B2 component class check
  if (b2ComponentIds.length !== renderedNodeIds.length) {
    throw new Error(`Cross-layer failure: Mismatch between rendered nodes (${renderedNodeIds.length}) and B2 .comp components (${b2ComponentIds.length}).`);
  }

  return {
    ok: true,
    ir_node_ids: irNodeIds,
    rendered_node_ids: renderedNodeIds,
    actual_review_ids: actualReviewIds,
    expected_review_ids: [...expectedReviewIds],
    bijective_parity: true,
    node_count: irNodeIds.length
  };
}
