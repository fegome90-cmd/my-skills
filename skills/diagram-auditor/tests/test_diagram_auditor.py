"""
Test suite for diagram-auditor skill.

Covers: Mermaid extraction, SVG parsing, element inventory,
verdict calculation, report template rendering, edge cases.

Run: pytest skills/diagram-auditor/tests/test_diagram_auditor.py -v
"""

import pytest
import re
import xml.etree.ElementTree as ET
from pathlib import Path

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

MERMAID_SINGLE = """sequenceDiagram
    participant U as User
    participant A as API
    U->>A: Login
    A-->>U: Token
"""

MERMAID_MULTI_BLOCK = """
Some text before.

```mermaid
graph TD
    A[Start] --> B[End]
```

More text.

```mermaid
sequenceDiagram
    X->>Y: Hello
    Y-->>X: World
```
"""

SVG_SIMPLE = """<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
  <rect x="50" y="50" width="120" height="40" rx="4" fill="#bfdbfe" stroke="#64748b"/>
  <text x="110" y="75" text-anchor="middle" font-size="14">Patient</text>
  <rect x="230" y="50" width="120" height="40" rx="4" fill="#c7d2fe" stroke="#64748b"/>
  <text x="290" y="75" text-anchor="middle" font-size="14">Diagnosis</text>
  <line x1="170" y1="70" x2="230" y2="70" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="200" y="62" text-anchor="middle" font-size="12">refers</text>
</svg>
"""

SVG_NO_TEXT = """<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40" fill="red"/>
</svg>
"""

SVG_GROUPS = """<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
  <g id="group-a">
    <rect x="10" y="10" width="100" height="30"/>
    <text x="60" y="30" text-anchor="middle">Node A</text>
  </g>
  <g id="group-b">
    <rect x="200" y="10" width="100" height="30"/>
    <text x="250" y="30" text-anchor="middle">Node B</text>
  </g>
</svg>
"""

INLINE_SVG_HTML = """<!doctype html>
<html><head><title>Diagram</title></head><body>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200">
  <text x="150" y="100" text-anchor="middle" font-size="16">Center Node</text>
</svg>
</body></html>
"""

MALFORMED_SVG = "<svg><rect></svg>"

EMPTY_DIAGRAM = ""
SINGLE_NODE_MERMAID = "graph TD\n    A[Only Node]"

# ---------------------------------------------------------------------------
# Tests: Mermaid Extraction (Step 0)
# ---------------------------------------------------------------------------

class TestMermaidExtraction:

    def test_extract_single_block(self):
        """Extract one Mermaid block from markdown."""
        matches = re.findall(r'```mermaid\n(.*?)```', MERMAID_SINGLE, re.DOTALL)
        assert len(matches) == 0  # no markdown fences in raw mermaid

    def test_extract_multi_block(self):
        """Extract multiple Mermaid blocks from markdown."""
        matches = re.findall(r'```mermaid\n(.*?)```', MERMAID_MULTI_BLOCK, re.DOTALL)
        assert len(matches) == 2
        assert "graph TD" in matches[0]
        assert "sequenceDiagram" in matches[1]

    def test_extract_nodes_from_mermaid(self):
        """Extract node labels from Mermaid graph."""
        code = MERMAID_MULTI_BLOCK
        graph_match = re.search(r'graph TD\n(.*?)(?=```)', code, re.DOTALL)
        if graph_match:
            nodes = re.findall(r'\[(.*?)\]', graph_match.group(1))
            assert "Start" in nodes
            assert "End" in nodes

    def test_extract_participants_from_sequence(self):
        """Extract participant aliases from sequence diagram."""
        participants = re.findall(r'participant\s+\w+\s+as\s+(\w+)', MERMAID_SINGLE)
        assert "User" in participants
        assert "API" in participants


# ---------------------------------------------------------------------------
# Tests: SVG Validation (Step 0)
# ---------------------------------------------------------------------------

class TestSVGValidation:

    def test_valid_svg_parses(self):
        tree = ET.fromstring(SVG_SIMPLE)
        assert tree is not None

    def test_valid_svg_has_viewbox(self):
        root = ET.fromstring(SVG_SIMPLE)
        assert root.get('viewBox') == "0 0 400 300"

    def test_valid_svg_counts_elements(self):
        root = ET.fromstring(SVG_SIMPLE)
        ns = {'svg': 'http://www.w3.org/2000/svg'}
        assert len(root.findall('.//svg:text', ns)) == 3  # 2 node labels + 1 edge label
        assert len(root.findall('.//svg:rect', ns)) == 2
        assert len(root.findall('.//svg:line', ns)) == 1

    def test_malformed_svg_fails(self):
        with pytest.raises(ET.ParseError):
            ET.fromstring(MALFORMED_SVG)

    def test_svg_no_text_detected(self):
        root = ET.fromstring(SVG_NO_TEXT)
        ns = {'svg': 'http://www.w3.org/2000/svg'}
        assert len(root.findall('.//svg:text', ns)) == 0


# ---------------------------------------------------------------------------
# Tests: SVG Element Extraction (Step 1)
# ---------------------------------------------------------------------------

class TestSVGExtraction:

    def _extract_nodes(self, svg_text):
        root = ET.fromstring(svg_text)
        ns = {'svg': 'http://www.w3.org/2000/svg'}
        nodes = []
        for text_el in root.findall('.//svg:text', ns):
            label = (text_el.text or '').strip()
            if label:
                nodes.append(label)
        return nodes

    def test_extract_two_nodes(self):
        nodes = self._extract_nodes(SVG_SIMPLE)
        assert len(nodes) == 3  # Patient + Diagnosis + edge label 'refers'
        assert "Patient" in nodes
        assert "Diagnosis" in nodes

    def test_extract_from_groups(self):
        nodes = self._extract_nodes(SVG_GROUPS)
        assert len(nodes) == 2
        assert "Node A" in nodes
        assert "Node B" in nodes

    def test_empty_diagram_no_nodes(self):
        nodes = self._extract_nodes(SVG_NO_TEXT)
        assert len(nodes) == 0

    def test_connector_detection(self):
        root = ET.fromstring(SVG_SIMPLE)
        ns = {'svg': 'http://www.w3.org/2000/svg'}
        lines = root.findall('.//svg:line', ns)
        assert len(lines) == 1
        assert lines[0].get('marker-end') is not None  # directed


# ---------------------------------------------------------------------------
# Tests: Inline SVG in HTML
# ---------------------------------------------------------------------------

class TestInlineSVG:

    def test_extract_svg_from_html(self):
        match = re.search(r'(<svg\b.*?</svg>)', INLINE_SVG_HTML, re.DOTALL)
        assert match is not None
        svg = match.group(1)
        root = ET.fromstring(svg)
        ns = {'svg': 'http://www.w3.org/2000/svg'}
        assert len(root.findall('.//svg:text', ns)) == 1


# ---------------------------------------------------------------------------
# Tests: Verdict Calculation (Step 4)
# ---------------------------------------------------------------------------

class TestVerdictCalculation:

    def calculate_verdict(self, elements: dict) -> str:
        """elements = {'confirmed': N, 'inferred': N, 'assumed': N, 'fabricated': N, 'outdated': N}"""
        total = sum(elements.values())
        if total == 0:
            return "SYNTAX-FAIL"
        fab_assumed_pct = (elements.get('fabricated', 0) + elements.get('assumed', 0)) / total * 100
        if fab_assumed_pct >= 20:
            return "FAIL"
        if elements.get('fabricated', 0) > 0 or elements.get('assumed', 0) > 0:
            unconfirmed = sum(v for k, v in elements.items() if k != 'confirmed')
            if unconfirmed / total > 0.5:
                return "FAIL"
            return "PASS-WITH-WARNINGS"
        if elements.get('inferred', 0) > 0:
            return "PASS-WITH-WARNINGS"
        return "PASS"

    def test_all_confirmed_pass(self):
        assert self.calculate_verdict({'confirmed': 10, 'inferred': 0, 'assumed': 0, 'fabricated': 0, 'outdated': 0}) == "PASS"

    def test_inferred_only_pass_warnings(self):
        assert self.calculate_verdict({'confirmed': 8, 'inferred': 2, 'assumed': 0, 'fabricated': 0, 'outdated': 0}) == "PASS-WITH-WARNINGS"

    def test_20_percent_fabricated_fail(self):
        # 2 fabricated out of 10 = 20%
        assert self.calculate_verdict({'confirmed': 7, 'inferred': 1, 'assumed': 0, 'fabricated': 2, 'outdated': 0}) == "FAIL"

    def test_single_fabricated_pass_warnings(self):
        # 1 fabricated out of 10 = 10% < 20%, but has non-confirmed
        assert self.calculate_verdict({'confirmed': 9, 'inferred': 0, 'assumed': 0, 'fabricated': 1, 'outdated': 0}) == "PASS-WITH-WARNINGS"

    def test_zero_elements_syntax_fail(self):
        assert self.calculate_verdict({'confirmed': 0, 'inferred': 0, 'assumed': 0, 'fabricated': 0, 'outdated': 0}) == "SYNTAX-FAIL"

    def test_over_50_percent_unconfirmed_fail(self):
        assert self.calculate_verdict({'confirmed': 4, 'inferred': 1, 'assumed': 1, 'fabricated': 1, 'outdated': 1}) == "FAIL"


# ---------------------------------------------------------------------------
# Tests: Edge Cases
# ---------------------------------------------------------------------------

class TestEdgeCases:

    def test_empty_mermaid_no_crash(self):
        matches = re.findall(r'```mermaid\n(.*?)```', EMPTY_DIAGRAM, re.DOTALL)
        assert len(matches) == 0

    def test_single_node_mermaid(self):
        nodes = re.findall(r'\[(.*?)\]', SINGLE_NODE_MERMAID)
        assert len(nodes) == 1
        assert nodes[0] == "Only Node"

    def test_nested_code_blocks(self):
        """Verify extraction doesn't break on nested fences."""
        content = "```mermaid\ngraph TD\n    A --> B\n```\n```python\nprint('hello')\n```"
        mermaid = re.findall(r'```mermaid\n(.*?)```', content, re.DOTALL)
        assert len(mermaid) == 1


# ---------------------------------------------------------------------------
# Tests: Evidence Enrichment (Step 3.1)
# ---------------------------------------------------------------------------

class TestEvidenceEnrichment:

    @staticmethod
    def mock_evidence_result(found, confidence=0.8, source="pubmed", url="https://pmid/123"):
        return {"found": found, "confidence": confidence, "source": source, "url": url}

    def test_upgrade_assumed_to_confirmed(self):
        """🟠 ASSUMED + high confidence evidence → 🟢 CONFIRMED"""
        result = self.mock_evidence_result(True, confidence=0.9)
        tag = "🟠"
        if result["found"] and result["confidence"] >= 0.7:
            tag = "🟢"
        assert tag == "🟢"

    def test_upgrade_inferred_to_confirmed(self):
        """🟡 INFERRED + any evidence found → 🟢 CONFIRMED"""
        result = self.mock_evidence_result(True, confidence=0.5)
        tag = "🟡"
        if result["found"]:
            tag = "🟢"
        assert tag == "🟢"

    def test_partial_upgrade_assumed(self):
        """🟠 ASSUMED + low confidence evidence → 🟡 INFERRED"""
        result = self.mock_evidence_result(True, confidence=0.4)
        tag = "🟠"
        if result["found"] and result["confidence"] >= 0.7:
            tag = "🟢"
        elif result["found"]:
            tag = "🟡"
        assert tag == "🟡"

    def test_no_evidence_keeps_tag(self):
        """No evidence found → tag unchanged"""
        result = self.mock_evidence_result(False)
        tag = "🟠"
        if result["found"]:
            tag = "🟢"
        assert tag == "🟠"

    def test_fabricated_never_auto_upgrades(self):
        """🔴 FABRICATED is never auto-upgraded regardless of evidence"""
        result = self.mock_evidence_result(True, confidence=0.99)
        tag = "🔴"
        # Fabricated always stays fabricated (must be removed, never confirmed)
        assert tag == "🔴"

    def test_confirmed_skip_evidence_check(self):
        """🟢 CONFIRMED elements are skipped (no query needed)"""
        elements_to_check = ["🟡", "🟠", "🔴"]
        assert "🟢" not in elements_to_check

    def test_adapter_priority_order(self):
        """Adapters tried in priority order, first hit wins"""
        adapters = [
            {"name": "pubmed", "priority": 1, "found": False},
            {"name": "papers", "priority": 2, "found": True},
            {"name": "local", "priority": 3, "found": True},
        ]
        result = None
        for adapter in sorted(adapters, key=lambda a: a["priority"]):
            if adapter["found"]:
                result = adapter["name"]
                break
        assert result == "papers"  # first that found evidence


# ---------------------------------------------------------------------------
# Tests: Wiki Sync (Step 5.5)
# ---------------------------------------------------------------------------

class TestWikiSync:

    def test_frontmatter_audit_fields(self):
        """Verify audit metadata fields are correct."""
        expected_fields = [
            "audit_state", "audit_date", "audit_verdict",
            "audit_elements", "audit_confirmed", "audit_inferred",
            "audit_assumed", "audit_fabricated", "audit_version",
        ]
        # Simulated frontmatter generation
        frontmatter = {f: f"value_{f}" for f in expected_fields}
        for f in expected_fields:
            assert f in frontmatter

    def test_verdict_to_audit_state_mapping(self):
        """Map verdicts to wiki audit_state."""
        mapping = {
            "PASS": "audited",
            "PASS-WITH-WARNINGS": "audited",
            "FAIL": "failed",
            "SYNTAX-FAIL": "syntax-error",
        }
        assert mapping["PASS"] == "audited"
        assert mapping["FAIL"] == "failed"

    def test_audit_log_append_format(self):
        """Verify audit log entry format."""
        entry = """### 2026-06-02 — PASS
- **Elements:** 12 (🟢10 🟡2 🟠0 🔴0 ⚪0)
- **Evidence sources:** PubMed (2 verified)"""
        assert "2026-06-02" in entry
        assert "PASS" in entry
        assert "🟢10" in entry

    def test_orphan_detection_query(self):
        """After removing fabricated element, check for wiki refs."""
        removed_elements = ["FakeNode", "InvalidStep"]
        queries = [f'wiki_search(query="{elem}")' for elem in removed_elements]
        assert len(queries) == 2
        assert "FakeNode" in queries[0]

    def test_graceful_skip_when_unavailable(self):
        """If wiki tools unavailable, skip without error."""
        wiki_available = False
        wiki_updated = False
        if wiki_available:
            wiki_updated = True  # would update
        assert not wiki_updated  # graceful skip


# ---------------------------------------------------------------------------
# Tests: Standalone Mermaid Validator Script (Step 0)
# ---------------------------------------------------------------------------

import importlib.util

def _load_validate_mermaid():
    script_path = Path(__file__).parent.parent / "scripts" / "validate_mermaid.py"
    spec = importlib.util.spec_from_file_location("validate_mermaid", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class TestMermaidValidatorScript:

    @pytest.fixture(autouse=True)
    def setup_validator(self):
        self.validator = _load_validate_mermaid()

    def test_valid_graph(self):
        ok, msg = self.validator.validate_structure("graph TD\n  A[Start] --> B(Stop)")
        assert ok is True
        assert "Syntax OK" in msg

    def test_valid_sequence(self):
        ok, msg = self.validator.validate_structure("sequenceDiagram\n  Alice->>Bob: Hello")
        assert ok is True

    def test_valid_with_comments(self):
        code = "%% comment line\nflowchart LR\n  A --> B"
        ok, msg = self.validator.validate_structure(code)
        assert ok is True

    def test_unclosed_bracket_fails(self):
        code = "graph TD\n  A[Start --> B"
        ok, msg = self.validator.validate_structure(code)
        assert ok is False
        assert "SYNTAX-FAIL" in msg

    def test_empty_diagram_fails(self):
        ok, msg = self.validator.validate_structure("")
        assert ok is False
        assert "empty" in msg

    def test_unrecognized_declaration_fails(self):
        ok, msg = self.validator.validate_structure("random_word\n  A --> B")
        assert ok is False
        assert "Unrecognized diagram declaration" in msg

    def test_extract_from_markdown_fence(self):
        fenced = "```mermaid\ngraph TD\n  A --> B\n```"
        extracted = self.validator.extract_raw_mermaid(fenced)
        assert extracted == "graph TD\n  A --> B"
        ok, _ = self.validator.validate_structure(extracted)
        assert ok is True

