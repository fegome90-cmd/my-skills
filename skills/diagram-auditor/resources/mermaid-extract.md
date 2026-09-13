# Mermaid Extraction Reference

Patterns for extracting Mermaid diagram blocks from Markdown files. Used by `diagram-auditor` Step 0 when the source is an embedded diagram.

## Multi-Pass Extraction (RECOMMENDED)

### Using awk (POSIX — works on macOS and Linux)

Extract ALL mermaid blocks from a Markdown file, saving each to a numbered `.mmd` file:

```bash
awk '
  /^```mermaid$/ { found=1; next }
  found && /^```$/ { found=0; count++; close(output) }
  found {
    output = sprintf("diagram-%02d.mmd", count+1)
    print > output
  }
' input.md
```

**Why awk, not grep?** Single-pass `grep | sed '/^```$/q'` quits after the first closing fence, missing all subsequent diagrams. This is a known limitation — see "Anti-patterns" below.

### Using Python (more robust)

```python
import re
from pathlib import Path

def extract_mermaid_blocks(md_path: Path) -> list[str]:
    """Extract all ```mermaid``` blocks from a Markdown file."""
    content = md_path.read_text()
    pattern = r"```mermaid\n(.*?)```"
    return re.findall(pattern, content, re.DOTALL)

# Usage
blocks = extract_mermaid_blocks(Path("input.md"))
for i, block in enumerate(blocks, 1):
    Path(f"diagram-{i:02d}.mmd").write_text(block)
```

## Single-Diagram Shortcut

If you know the file has exactly one mermaid block:

```bash
awk '/^```mermaid$/{found=1; next} found && /^```$/{exit} found{print}' input.md > diagram.mmd
```

## Multi-Diagram Numbering Convention

When a Markdown file contains multiple mermaid blocks:

| Block # | Temp file | Audit reference |
|---------|-----------|----------------|
| 1st | `diagram-01.mmd` | ELEMENT-01..N (diagram 1 of M) |
| 2nd | `diagram-02.mmd` | ELEMENT-01..N (diagram 2 of M) |
| Nth | `diagram-NN.mmd` | ELEMENT-01..N (diagram N of M) |

Each diagram is audited independently with its own element inventory.

## Anti-Patterns (DO NOT USE)

### ❌ Single-pass grep with sed quit

```bash
# ONLY extracts the FIRST diagram — misses all others
grep -A 1000 '```mermaid' file.md | sed '/^```$/q' | tail -n +2 | sed '$d'
```

**Problem:** `sed '/^```$/q'` quits after the first closing fence (` ``` `). REQ-04 requires supporting multiple diagrams per file.

### ❌ head -n -1 (non-portable)

```bash
# head -n -1 may not work on all systems
grep -A 1000 '```mermaid' file.md | sed '/^```$/q' | tail -n +2 | head -n -1
```

**Problem:** While `head -n -1` works on modern macOS, it's not POSIX-standard. Use `sed '$d'` instead if you need to strip the last line.

## Edge Cases

| Case | Behavior |
|------|----------|
| Empty mermaid block (` ```mermaid\n``` `) | Skipped — no content to audit |
| Nested code block inside mermaid | Extracted as-is — may fail syntax validation (caught by Step 0) |
| Mermaid block with language variant (` ```mermaid {title:"..."}`) | awk pattern `/^```mermaid/` handles variants; Python regex may need adjustment |
| No mermaid blocks found | Step 0 skipped — proceed to prose/visual audit |

## Verification

Test extraction against existing project files with embedded Mermaid:

```bash
# Find files with mermaid blocks
grep -rl '```mermaid' docs/ apps/

# Test extraction on a specific file
awk '/^```mermaid$/{found=1; next} found && /^```$/{found=0; count++; close(output)} found{output=sprintf("diagram-%02d.mmd",count+1); print > output}' docs/pae-forensic-analysis/01-system-architecture/overview.md

# Verify extracted files
ls -la diagram-*.mmd

# Validate extracted diagram syntax
python3 skills/diagram-auditor/scripts/validate_mermaid.py diagram-01.mmd
```
