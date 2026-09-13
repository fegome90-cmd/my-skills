#!/usr/bin/env python3
"""Detect plan domain from a plan file. Used by the orchestrator shell script."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from resources.agents.base_agent import detect_plan_domain, validate_domain


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: detect_domain.py <plan_path> [forced_domain]", file=sys.stderr)
        sys.exit(1)

    plan_path = Path(sys.argv[1]).expanduser()

    if len(sys.argv) >= 3:
        forced = sys.argv[2]
        print(validate_domain(forced))
        return

    if not plan_path.exists():
        print("generic")
        return

    try:
        lines = plan_path.read_text(encoding="utf-8").splitlines()
        print(detect_plan_domain(lines))
    except (UnicodeDecodeError, OSError):
        print("generic")


if __name__ == "__main__":
    main()
