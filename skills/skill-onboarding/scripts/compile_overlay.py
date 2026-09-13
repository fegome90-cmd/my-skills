#!/usr/bin/env python3
"""
compile_overlay.py - Deterministic Candidate Registry Overlay Compiler
Calculates: OVERLAY = (LIVE_BASE - OLD_SKILL_ENTRY) + CANDIDATE_ENTRY
Compliant with python-patterns, python-production, and atomic write semantics.
"""

from __future__ import annotations
import sys
import os
import re
import argparse
from pathlib import Path

def compile_overlay(
    live_registry_path: str | Path,
    candidate_compact_rules_path: str | Path,
    skill_name: str,
    output_path: str | Path
) -> None:
    live_path = Path(live_registry_path)
    candidate_path = Path(candidate_compact_rules_path)
    out_path = Path(output_path)

    if not candidate_path.is_file():
        print(f"Error: Candidate compact rules file '{candidate_path}' not found.", file=sys.stderr)
        sys.exit(1)

    if live_path.is_file():
        live_content = live_path.read_text(encoding="utf-8")
    else:
        live_content = "# Skill Registry\n\n## Compact Rules\n\n"

    candidate_rules = candidate_path.read_text(encoding="utf-8").strip()

    # Remove existing skill section if updating an existing skill
    pattern = rf"### {re.escape(skill_name)}\n(?:(?!### ).)*"
    cleaned_content = re.sub(pattern, "", live_content, flags=re.DOTALL).strip()

    # Append new candidate rules under Compact Rules
    if "## Compact Rules" in cleaned_content:
        parts = cleaned_content.split("## Compact Rules", 1)
        overlay_content = f"{parts[0]}## Compact Rules\n\n{candidate_rules}\n\n{parts[1].lstrip()}"
    else:
        overlay_content = f"{cleaned_content}\n\n## Compact Rules\n\n{candidate_rules}\n"

    # Atomic write via temporary file
    out_path.parent.mkdir(parents=True, exist_ok=True)
    temp_out = out_path.with_suffix(".tmp")
    temp_out.write_text(overlay_content, encoding="utf-8")
    temp_out.replace(out_path)

    print(f"Overlay successfully written to: {out_path}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic Candidate Registry Overlay Compiler")
    parser.add_argument("live_registry", help="Path to live registry markdown base")
    parser.add_argument("candidate_rules", help="Path to candidate compact rules markdown")
    parser.add_argument("skill_name", help="Name of candidate skill")
    parser.add_argument("output_overlay", help="Output path for compiled candidate overlay")

    args = parser.parse_args()
    compile_overlay(args.live_registry, args.candidate_rules, args.skill_name, args.output_overlay)

if __name__ == "__main__":
    main()
