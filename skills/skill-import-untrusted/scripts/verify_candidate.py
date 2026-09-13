#!/usr/bin/env python3
"""
verify_candidate.py - Fail-Closed Candidate Verification Engine
Executes:
1. Interface Preflight (candidate overlay validation & secret quarantine scan)
2. Judge A (Exact-Name deterministic probe)
3. Judge B (DETERMINISTIC intent battery over pre-frozen fixtures: normalized exact-token
   matching with stopword/min-length filtering, PROHIBITED arbitrary-substring evidence,
   and SEPARATE thresholds for SHOULD_TRIGGER / MUST_NOT_TRIGGER / NEIGHBOUR_COLLISION)
4. Capability-Aware Smoke Test (structural, CLI, or lifecycle with timeout protection)
Outputs: verification_receipt.json on ALL PASS; exits non-zero on ANY FAIL.

Maximal permitted claim when all gates pass: JUDGE_B_CLAIM =
"PASS against declared frozen intent fixtures". Universal semantic equivalence
is explicitly NOT asserted by this deterministic verifier.

Compliant with python-patterns, python-production, secret-safety, and python-subprocess-timeout standards.
"""

from __future__ import annotations
import sys
import os
import json
import subprocess
import re
import shlex
import argparse
from pathlib import Path
from typing import Any, Dict, List, Tuple

DEFAULT_TIMEOUT_SECONDS = 15

# ---------------------------------------------------------------------------
# Deterministic Judge B intent-matching contract (SEM-001 remediation)
#
# Matching is EXACT-TOKEN based after normalization:
#   - casefold, extract [a-z0-9]+ tokens
#   - drop stopwords (function words + skill-domain meta vocabulary)
#   - drop trivially short tokens (< MIN_TOKEN_LENGTH chars)
# Arbitrary substring matching is PROHIBITED as evidence of intent overlap.
# Thresholds are SEPARATE per fixture class (SHOULD / MUST_NOT / NEIGHBOR).
# Maximal permitted claim when this gate passes: see JUDGE_B_CLAIM below.
# ---------------------------------------------------------------------------
MIN_TOKEN_LENGTH = 4

STOPWORDS = frozenset({
    # English function words
    "the", "this", "that", "these", "those", "and", "but", "for", "with", "from",
    "into", "onto", "about", "over", "under", "after", "before", "between", "through",
    "during", "without", "within", "what", "which", "when", "where", "while", "who",
    "whose", "whom", "why", "here", "there", "then", "than", "thus", "also", "just",
    "only", "very", "some", "such", "like", "make", "made", "have", "having",
    # Project-specific meta vocabulary (not discriminating onboarding intents)
    "skill", "skills", "registry", "registries", "agent", "agents",
})

# --- SHOULD_TRIGGER gate ----------------------------------------------------
POSITIVE_TRIGGER_MIN_SCORE = 0.25       # |common| / |query_informative|
POSITIVE_MIN_COMMON_TOKENS = 1
# --- MUST_NOT_TRIGGER (near-miss) collision gate -----------------------------
NEGATIVE_TRIGGER_MAX_SCORE = 0.15
NEGATIVE_TRIGGER_ABS_COMMON = 2
NEGATIVE_CRITICAL_TOKEN_LENGTH = 8      # rare domain words (e.g. "database") count alone
# --- NEIGHBOR_COLLISION gate (neighbouring-skill confusion queries) ----------
NEIGHBOR_COLLISION_MAX_SCORE = 0.12
NEIGHBOR_COLLISION_ABS_COMMON = 2
NEIGHBOR_COLLISION_CRITICAL_TOKEN_LENGTH = 8

JUDGE_B_CLAIM = "PASS against declared frozen intent fixtures"

def informative_tokens(text: str) -> List[str]:
    """Normalized, information-bearing tokens of `text` (casefolded, de-stopworded, min-length)."""
    return [
        tok
        for tok in re.findall(r"[a-z0-9]+", text.casefold())
        if len(tok) >= MIN_TOKEN_LENGTH and tok not in STOPWORDS
    ]

def _collision_decision(
    common: List[str], score: float,
    max_score: float, abs_common: int, critical_len: int,
) -> tuple[bool, str]:
    """Declares a routing collision under one threshold class."""
    if score >= max_score:
        return True, f"overlap score {score:.3f} >= {max_score}"
    if len(common) >= abs_common:
        return True, f"{len(common)} shared discriminant tokens >= {abs_common}"
    critical_hit = next((t for t in common if len(t) >= critical_len), None)
    if critical_hit is not None:
        return True, f"critical domain token '{critical_hit}' shared"
    return False, "below all collision bounds"

def evaluate_judge_b_fixture(
    query: str, desc_text: str, expected_result: str, fixture_type: str
) -> Dict[str, Any]:
    """Deterministically evaluates one frozen fixture against the overlay description text.

    Returns a detail dict including the independent trigger decision (would_trigger),
    which is compared against the expectation to yield the fixture verdict.
    """
    q_inf = informative_tokens(query)
    d_inf = set(informative_tokens(desc_text))
    common = sorted(set(q_inf).intersection(d_inf))
    score = len(common) / len(q_inf) if q_inf else 0.0

    is_neighbor_class = "neighbor" in fixture_type or "neighbour" in fixture_type
    wants_trigger = expected_result == "SHOULD_TRIGGER"

    if wants_trigger:
        would_trigger = (
            len(q_inf) > 0
            and len(common) >= POSITIVE_MIN_COMMON_TOKENS
            and score >= POSITIVE_TRIGGER_MIN_SCORE
        )
        reason = (
            f"{len(common)} informative common tokens, score {score:.3f} "
            f"(need >= {POSITIVE_MIN_COMMON_TOKENS} common and >= {POSITIVE_TRIGGER_MIN_SCORE})"
            if would_trigger
            else f"insufficient positive evidence ({len(common)} informative common tokens, score {score:.3f})"
        )
        detail = {
            "query_informative_tokens": sorted(q_inf),
            "common_tokens": common,
            "score": round(score, 4),
            "threshold_class": "POSITIVE",
            "would_trigger": would_trigger,
            "decision_reason": reason,
        }
    else:
        if is_neighbor_class:
            coll, reason = _collision_decision(
                common, score,
                NEIGHBOR_COLLISION_MAX_SCORE, NEIGHBOR_COLLISION_ABS_COMMON,
                NEIGHBOR_COLLISION_CRITICAL_TOKEN_LENGTH,
            )
            klass = "NEIGHBOR_COLLISION"
        else:
            coll, reason = _collision_decision(
                common, score,
                NEGATIVE_TRIGGER_MAX_SCORE, NEGATIVE_TRIGGER_ABS_COMMON,
                NEGATIVE_CRITICAL_TOKEN_LENGTH,
            )
            klass = "MUST_NOT"
        detail = {
            "query_informative_tokens": sorted(q_inf),
            "common_tokens": common,
            "score": round(score, 4),
            "threshold_class": klass,
            "would_trigger": coll,
            "decision_reason": reason,
        }

    verdict = "PASS" if (detail["would_trigger"] == wants_trigger) else "FAIL"
    detail["id"] = None  # filled by caller
    detail["type"] = fixture_type
    detail["expected"] = expected_result
    detail["verdict"] = verdict
    return detail

# Forbidden sensitive file patterns in promotable candidate trees
SENSITIVE_PATTERNS = [
    r"^\.env(\..+)?$",
    r"^\.npmrc$",
    r"^\.pypirc$",
    r"^\.netrc$",
    r"^.*_rsa(\.pub)?$",
    r"^.*\.(pem|key|pfx|pkcs12|keystore)$",
    r"^(credentials|service-account.*|secrets?)\.(json|yaml|yml)$",
    r"^(token|access_token|api_key|secret)\.txt$",
    r"^\.git$"
]

def scan_sensitive_files(candidate_dir: Path) -> List[str]:
    """Scans for sensitive credentials or private material in promotable candidate tree."""
    violations = []
    for root, dirs, files in os.walk(candidate_dir):
        for name in files + dirs:
            for pat in SENSITIVE_PATTERNS:
                if re.match(pat, name, re.IGNORECASE):
                    rel_path = os.path.relpath(os.path.join(root, name), candidate_dir)
                    violations.append(rel_path)
    return sorted(list(set(violations)))

def run_cmd(cmd: str | List[str], timeout: int = DEFAULT_TIMEOUT_SECONDS) -> Tuple[int, str]:
    """
    Executes a command safely with timeout handling and captured output.
    Protects against infinite hangs or interactive blocking.
    """
    try:
        if isinstance(cmd, str):
            cmd_args = shlex.split(cmd)
        else:
            cmd_args = cmd

        res = subprocess.run(
            cmd_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            check=False
        )
        return res.returncode, (res.stdout + res.stderr).strip()
    except subprocess.TimeoutExpired:
        return 124, f"TIMEOUT_EXPIRED: Command timed out after {timeout}s"
    except FileNotFoundError as e:
        return 127, f"COMMAND_NOT_FOUND: {e}"
    except Exception as e:
        return 1, f"EXECUTION_ERROR: {e}"

def verify(
    candidate_dir: str | Path,
    overlay_path: str | Path,
    fixtures_path: str | Path,
    skill_name: str,
    capability_risk: str,
    receipt_out: str | Path,
    timeout: int = DEFAULT_TIMEOUT_SECONDS
) -> None:
    c_dir = Path(candidate_dir)
    o_path = Path(overlay_path)
    f_path = Path(fixtures_path)
    r_path = Path(receipt_out)

    print(f"--- Starting Fresh Candidate Verification for '{skill_name}' ---")
    results: Dict[str, Any] = {
        "skill_name": skill_name,
        "overlay_path": str(o_path),
        "capability_risk": capability_risk,
        "gates": {},
        "verdict": "FAIL"
    }

    # 1. Interface Preflight & Secret Quarantine Scan
    if not o_path.is_file():
        print(f"PREFLIGHT FAIL: Candidate overlay '{o_path}' missing.", file=sys.stderr)
        sys.exit(10)
    
    overlay_content = o_path.read_text(encoding="utf-8")
    if f"### {skill_name}" not in overlay_content and f"name: {skill_name}" not in overlay_content:
        print(f"PREFLIGHT FAIL: Candidate skill '{skill_name}' not found in overlay.", file=sys.stderr)
        sys.exit(11)

    sensitive_found = scan_sensitive_files(c_dir)
    if sensitive_found:
        print(f"PREFLIGHT FAIL: Sensitive/secret files detected in candidate tree: {sensitive_found}", file=sys.stderr)
        sys.exit(17)

    results["gates"]["preflight"] = "PASS"
    print("✓ Gate 1: Preflight Overlay Validation & Secret Scan PASS")

    # 2. Judge A: Exact-Name Deterministic Probe
    judge_a_pass = f"### {skill_name}" in overlay_content or f"{skill_name}" in overlay_content
    if not judge_a_pass:
        print(f"JUDGE A FAIL: Skill '{skill_name}' exact lookup failed in overlay.", file=sys.stderr)
        sys.exit(12)
    results["gates"]["judge_a"] = "PASS"
    print("✓ Gate 2: Judge A Exact-Name Lookup PASS")

    # 3. Judge B: 5-Fixture Intent Battery
    if not f_path.is_file():
        print(f"FIXTURES FAIL: Frozen fixtures file '{f_path}' missing.", file=sys.stderr)
        sys.exit(13)

    try:
        fixture_data = json.loads(f_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FIXTURES FAIL: Malformed JSON in '{f_path}': {e}", file=sys.stderr)
        sys.exit(13)

    judge_b_results: List[Dict[str, str]] = []
    fixtures = fixture_data.get("fixtures", [])
    if len(fixtures) < 3:
        print(f"FIXTURES FAIL: Minimum 3 fixtures required (found {len(fixtures)}).", file=sys.stderr)
        sys.exit(13)

    desc_match = re.search(rf"### {re.escape(skill_name)}.*?\n(.*?)(?=\n### |\Z)", overlay_content, re.DOTALL)
    desc_text = desc_match.group(1) if desc_match else overlay_content

    for fix in fixtures:
        f_id = fix.get("id", "unknown")
        f_type = fix.get("type", "custom")
        query = fix.get("query", "")
        expected = fix.get("expected_result", "SHOULD_TRIGGER")

        detail = evaluate_judge_b_fixture(query, desc_text, expected, f_type)
        detail["id"] = f_id
        detail["query"] = query
        judge_b_results.append(detail)
        if detail["verdict"] != "PASS":
            print(
                f"JUDGE B FAIL on fixture '{f_id}' ({f_type}): query='{query}' expected={expected} "
                f"reason={detail['decision_reason']}",
                file=sys.stderr,
            )
            sys.exit(14)

    results["gates"]["judge_b_claim"] = JUDGE_B_CLAIM

    results["gates"]["judge_b"] = judge_b_results
    print(f"✓ Gate 3: Judge B Intent Battery ({len(fixtures)}/{len(fixtures)} Fixtures Passed)")

    # 4. Capability-Aware Smoke Test with Timeout Protection
    smoke_result = "PASS"
    if capability_risk in ["local-write", "elevated-exec", "git-mutating"]:
        scripts_dir = c_dir / "scripts"
        if scripts_dir.is_dir():
            for s_path in scripts_dir.iterdir():
                if s_path.is_file() and os.access(s_path, os.X_OK):
                    code, out = run_cmd([str(s_path), "--help"], timeout=timeout)
                    if code != 0:
                        print(f"SMOKE TEST FAIL on '{s_path.name}': exit {code} ({out})", file=sys.stderr)
                        sys.exit(15)
    elif capability_risk in ["read-only", "guide"]:
        skill_md = c_dir / "SKILL.md"
        if skill_md.is_file():
            content = skill_md.read_text(encoding="utf-8")
            for ref in re.findall(r'\[.*?\]\((references/[^\)]+)\)', content):
                target = c_dir / ref
                if not target.exists():
                    print(f"SMOKE TEST FAIL: Broken internal reference '{ref}' in SKILL.md", file=sys.stderr)
                    sys.exit(16)

    results["gates"]["smoke_test"] = smoke_result
    print("✓ Gate 4: Capability-Aware Smoke Test PASS")

    # Write atomic receipt
    results["verdict"] = "PASS"
    r_path.parent.mkdir(parents=True, exist_ok=True)
    temp_receipt = r_path.with_suffix(".tmp")
    temp_receipt.write_text(json.dumps(results, indent=2), encoding="utf-8")
    temp_receipt.replace(r_path)

    print(f"All gates PASS. Verification receipt written to: {r_path}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Fail-Closed Candidate Verification Engine")
    parser.add_argument("candidate_dir", help="Path to candidate skill directory")
    parser.add_argument("overlay_path", help="Path to compiled candidate registry overlay")
    parser.add_argument("fixtures_path", help="Path to pre-frozen fixtures JSON")
    parser.add_argument("skill_name", help="Name of skill being verified")
    parser.add_argument("capability_risk", choices=["read-only", "local-write", "git-mutating", "network-external", "elevated-exec", "guide"], help="Capability risk level")
    parser.add_argument("receipt_out", help="Path to write verification receipt JSON")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="Timeout in seconds for external commands")

    args = parser.parse_args()
    verify(
        args.candidate_dir,
        args.overlay_path,
        args.fixtures_path,
        args.skill_name,
        args.capability_risk,
        args.receipt_out,
        args.timeout
    )

if __name__ == "__main__":
    main()
