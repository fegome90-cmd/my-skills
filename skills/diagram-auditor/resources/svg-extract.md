# SVG Extraction Patterns

Automated extraction of diagram elements from SVG sources for deterministic audit inventories.

## When to Use

- Input diagram is `.svg` or `.html` with inline SVG
- Need deterministic element inventory (vs visual interpretation)
- Batch processing multiple SVG diagrams

## Extraction Pipeline

### 1. Validate Well-Formedness

```python
import xml.etree.ElementTree as ET

def validate_svg(path: str) -> dict:
    """Check SVG is parseable and extract metadata."""
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        ns = {'svg': 'http://www.w3.org/2000/svg'}
        
        # Extract viewBox
        viewbox = root.get('viewBox', root.get('width', 'unknown'))
        
        # Count elements
        text_count = len(root.findall('.//svg:text', ns))
        rect_count = len(root.findall('.//svg:rect', ns))
        line_count = len(root.findall('.//svg:line', ns))
        path_count = len(root.findall('.//svg:path', ns))
        circle_count = len(root.findall('.//svg:circle', ns))
        group_count = len(root.findall('.//svg:g', ns))
        
        return {
            "status": "VALID",
            "viewBox": viewbox,
            "elements": {
                "text": text_count,
                "rect": rect_count,
                "line": line_count,
                "path": path_count,
                "circle": circle_count,
                "group": group_count,
            },
            "has_text": text_count > 0,
        }
    except ET.ParseError as e:
        return {"status": "PARSE_ERROR", "error": str(e)}
```

### 2. Extract Node Inventory

```python
def extract_nodes(svg_path: str) -> list[dict]:
    """Extract all labeled elements as audit items."""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    
    nodes = []
    counter = 0
    
    # Extract from <text> elements
    for text_el in root.findall('.//svg:text', ns):
        label = (text_el.text or '').strip()
        if not label:
            continue
        counter += 1
        
        # Find parent container for context
        parent = text_el
        container_type = "text"
        while parent is not None:
            tag = parent.tag.replace(f'{{{ns["svg"]}}}', '')
            if tag in ('rect', 'circle', 'ellipse', 'g'):
                container_type = tag
                break
            parent = parent.getparent() if hasattr(parent, 'getparent') else None
        
        nodes.append({
            "id": f"ELEMENT-{counter:02d}",
            "label": label,
            "container": container_type,
            "source": "svg:text",
            "tag": "UNCLASSIFIED",  # auditor will classify
        })
    
    # Extract from <title> inside shapes (common pattern)
    for shape in root.findall('.//svg:*', ns):
        title = shape.find('svg:title', ns)
        if title is not None and title.text and title.text.strip():
            counter += 1
            nodes.append({
                "id": f"ELEMENT-{counter:02d}",
                "label": title.text.strip(),
                "container": shape.tag.replace(f'{{{ns["svg"]}}}', ''),
                "source": "svg:title",
                "tag": "UNCLASSIFIED",
            })
    
    return nodes
```

### 3. Extract Connectors

```python
def extract_connectors(svg_path: str) -> list[dict]:
    """Extract directed and undirected connections."""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    
    connectors = []
    
    # Lines
    for line in root.findall('.//svg:line', ns):
        connectors.append({
            "type": "line",
            "from": (line.get('x1'), line.get('y1')),
            "to": (line.get('x2'), line.get('y2')),
            "directed": line.get('marker-end') is not None,
        })
    
    # Paths (arrows, curves)
    for path in root.findall('.//svg:path', ns):
        d = path.get('d', '')
        markers = [k for k in path.attrib if 'marker' in k.lower()]
        connectors.append({
            "type": "path",
            "d_attr": d[:80],  # truncated for readability
            "directed": len(markers) > 0,
        })
    
    return connectors
```

### 4. Full Audit Inventory

```python
def audit_inventory(svg_path: str) -> dict:
    """Produce full inventory for Steps 1-2 of diagram-auditor."""
    validation = validate_svg(svg_path)
    
    if validation["status"] != "VALID":
        return {
            "verdict": "SYNTAX-FAIL",
            "reason": validation.get("error", "SVG parse error"),
        }
    
    if not validation["has_text"]:
        return {
            "verdict": "SYNTAX-FAIL",
            "reason": "No text elements found — diagram may be image-only",
        }
    
    nodes = extract_nodes(svg_path)
    connectors = extract_connectors(svg_path)
    
    return {
        "verdict": "READY_FOR_AUDIT",
        "svg_meta": {
            "viewBox": validation["viewBox"],
            "element_counts": validation["elements"],
        },
        "nodes": nodes,
        "connectors": connectors,
        "total_elements": len(nodes),
        "audit_checklist": [f"[ ] {n['id']}: {n['label']}" for n in nodes],
    }
```

## Integration with diagram-auditor

Insert between Step 0 and Step 1:

| Step | Before | After |
|------|--------|-------|
| Step 0 | Mermaid syntax only | + SVG well-formedness check |
| Step 1 | Manual visual extraction | + Automated `extract_nodes()` for SVG |
| Step 2 | Classify manually | Classify from automated inventory |

## Inline SVG in HTML

When diagram is `.html` with inline SVG, extract the SVG block first:

```python
import re

def extract_svg_from_html(html_path: str) -> str | None:
    """Extract first <svg>...</svg> block from HTML file."""
    with open(html_path) as f:
        content = f.read()
    match = re.search(r'(<svg\b.*?</svg>)', content, re.DOTALL)
    if match:
        return match.group(1)
    return None
```

## Edge Cases

| Case | Behavior |
|------|----------|
| SVG with no text (image-based) | SYNTAX-FAIL: "No extractable labels" |
| SVG with CSS classes (no inline labels) | Extract from class names, flag low confidence |
| Grouped elements (`<g>` containers) | Walk into groups, extract nested text |
| ForeignObject (HTML in SVG) | Parse HTML content within, extract text nodes |
| Multiple SVGs in one file | Process each separately, prefix IDs (SVG1-, SVG2-) |

## Dependencies

- Python 3.10+ standard library (`xml.etree.ElementTree`, `re`)
- No external packages required

---

**Version:** 1.0.0 | **Updated:** 2026-06-02
