#!/usr/bin/env python3
"""
Mermaid Syntax Validator for diagram-auditor.

Validates standalone Mermaid (.mmd) files or stdin content.
First attempts validation via Mermaid CLI (mmdc) if installed.
Falls back to deterministic Python-based structural and syntax verification.

Usage:
    python3 validate_mermaid.py diagram.mmd
    cat diagram.mmd | python3 validate_mermaid.py
"""

import sys
import os
import re
import shutil
import subprocess
from pathlib import Path

# Recognized Mermaid diagram declarations (case-sensitive or lowercase variations)
MERMAID_DIAGRAM_TYPES = (
    "graph",
    "flowchart",
    "sequencediagram",
    "classdiagram",
    "classdiagram-v2",
    "statediagram",
    "statediagram-v2",
    "erdiagram",
    "gantt",
    "pie",
    "gitgraph",
    "journey",
    "mindmap",
    "quadrantchart",
    "timeline",
    "xychart",
    "xychart-beta",
    "architecture",
    "architecture-beta",
    "packet-beta",
    "block-beta",
    "sankey-beta",
    "c4context",
    "c4container",
    "c4component",
    "c4dynamic",
    "c4deployment",
    "zenuml",
)


def extract_raw_mermaid(content: str) -> str:
    """Extract mermaid code if wrapped in markdown code fence, otherwise strip."""
    content = content.strip()
    match = re.search(r"```mermaid\s*\n(.*?)```", content, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Strip any general code fences if present
    if content.startswith("```") and content.endswith("```"):
        lines = content.splitlines()
        return "\n".join(lines[1:-1]).strip()
    return content


def validate_with_cli(mermaid_text: str) -> tuple[bool, str]:
    """Validate using mmdc if available in system PATH."""
    mmdc_path = shutil.which("mmdc")
    if not mmdc_path:
        return False, "mmdc not found"

    try:
        proc = subprocess.run(
            [mmdc_path, "-i", "-", "-o", "/dev/null"],
            input=mermaid_text,
            text=True,
            capture_output=True,
            timeout=10,
        )
        if proc.returncode == 0:
            return True, "Valid (verified by mmdc)"
        return False, f"mmdc validation failed: {proc.stderr.strip()}"
    except Exception as e:
        return False, f"CLI validation error: {e}"


def validate_structure(mermaid_text: str) -> tuple[bool, str]:
    """Deterministic structural and syntax validation using Python."""
    if not mermaid_text or not mermaid_text.strip():
        return False, "SYNTAX-FAIL: Diagram content is empty"

    lines = [line.strip() for line in mermaid_text.splitlines() if line.strip()]
    # Remove directive or comment lines at top (e.g. %% comments or %%{init:...}%%)
    content_lines = []
    for line in lines:
        if line.startswith("%%"):
            continue
        content_lines.append(line)

    if not content_lines:
        return False, "SYNTAX-FAIL: Diagram contains only comments/directives without content"

    # Verify first content line begins with a recognized diagram type
    first_line = content_lines[0].lower()
    first_word = first_line.split()[0] if first_line.split() else ""
    
    # Check if first word or combination matches a valid diagram type
    type_matched = False
    for dtype in MERMAID_DIAGRAM_TYPES:
        if first_line.startswith(dtype):
            type_matched = True
            break

    if not type_matched:
        return (
            False,
            f"SYNTAX-FAIL: Unrecognized diagram declaration '{content_lines[0]}'. "
            f"Expected one of: {', '.join(MERMAID_DIAGRAM_TYPES[:10])}...",
        )

    # Bracket balance check across the entire text (ignoring escaped chars)
    # Stack for delimiters: [ ], ( ), { }
    stack = []
    pairs = {"]": "[", ")": "(", "}": "{"}
    in_quote = False
    quote_char = None
    escaped = False

    for idx, char in enumerate(mermaid_text):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char in ('"', "'"):
            if not in_quote:
                in_quote = True
                quote_char = char
            elif quote_char == char:
                in_quote = False
                quote_char = None
            continue
        if in_quote:
            continue

        if char in pairs.values():
            stack.append((char, idx))
        elif char in pairs:
            if not stack:
                return (
                    False,
                    f"SYNTAX-FAIL: Unmatched closing bracket '{char}' at character index {idx}",
                )
            last_open, last_idx = stack.pop()
            if last_open != pairs[char]:
                return (
                    False,
                    f"SYNTAX-FAIL: Mismatched bracket. Expected match for '{last_open}' (index {last_idx}), found '{char}' (index {idx})",
                )

    if in_quote:
        return False, "SYNTAX-FAIL: Unclosed quote string in diagram"

    if stack:
        unmatched = [f"'{c}' at {i}" for c, i in stack]
        return False, f"SYNTAX-FAIL: Unclosed opening delimiter(s): {', '.join(unmatched)}"

    return True, f"Syntax OK ({content_lines[0]})"


def validate_mermaid(content: str) -> tuple[bool, str]:
    """Validate Mermaid diagram text, trying CLI first and falling back to structure check."""
    cleaned = extract_raw_mermaid(content)
    # If mmdc is available, try it
    if shutil.which("mmdc"):
        cli_valid, cli_msg = validate_with_cli(cleaned)
        if cli_valid:
            return True, cli_msg
        # If CLI failed, return the failure
        return False, cli_msg

    # Fallback to structural validator
    return validate_structure(cleaned)


def main():
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        content = file_path.read_text(encoding="utf-8")
    else:
        if sys.stdin.isatty():
            print("Usage: validate_mermaid.py <diagram.mmd> or pass via stdin", file=sys.stderr)
            sys.exit(1)
        content = sys.stdin.read()

    is_valid, message = validate_mermaid(content)
    if is_valid:
        print(f"OK: {message}")
        sys.exit(0)
    else:
        print(f"FAIL: {message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
