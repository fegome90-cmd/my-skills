# Audit v6 — closure audit after governed Scope B+ application

**Date:** 2026-08-13
**Status:** Closure. Verifies the post-application state of `disk-cleanup-macos-safe` after AUDIT-v5 was audited and P1/P4/P5 were applied (P3 discarded, P2 left with a field-test limit).
**Predecessor:** `AUDIT-v5.md` (revised) — dispositions and reformulations.

## Executive judgment

The governed audit of AUDIT-v5 closed three patches (P1, P4, P5) into the `SKILL.md`, discarded one (P3, VACUUM) for violating an invariant, and left one (P2) with an honest field-test limit. Every applied change was **additive discipline** — none weakened a v4 safety property. This closure audit re-verifies the final artifact: the helper suite passes, the v4 invariants are intact in the prose, the three inserts are present exactly once, and the markdown is well-formed.

## Changes applied in this cycle

| Patch | Location (semantic anchor) | Nature | Hash delta |
|---|---|---|---|
| P4 — loose-file sweep | Stage 2, before "For every measurement preserve:" | prose-only; warns `du -d 1` hides root files; recommends `find -maxdepth 1 -type f` | +698 B |
| P1 — owner-native reclaim (scoped) | Stage 4, before "Also inspect configured…" | prose table; brew target-scoped, `--prune=all`/no-arg flagged broad-prune, cargo `cache -a` removed (3rd-party), per-tool evidence | table |
| P5 — version-stacking | Stage 3, before "#### Cloud and File Provider data" | prose; 4 categories, "no symlink ⇒ unused" rejected, pin-file resolution, pipx/uv as managed objects | section |

P3 (generic SQLite VACUUM) was **not** applied: it violates the Controlled-execution invariant *"databases … require their dedicated owner-specific protocols."* It remains a normative observation only.

P2 (active-owner gate) was **not** applied to `SKILL.md`: the 3-state gate is designed and its 4 scenarios (#47–50) are in `pressure-scenarios.md`, but AUDIT-v5 admits a second field test is missing. It stays `REVISE (LIMIT)`.

## Verification performed (fresh, this run)

- **Helper suite:** `python3 tests/test_audit_logic.py` → **14 tests, OK, exit 0** (13 v4 + 1 P4 regression `test_iter_children_captures_loose_root_files`).
- **Invariant presence (grep, live `SKILL.md`):**
  - Core contract bans intact — "broad prune commands", "sticky approval", "globs", "privilege escalation" still present.
  - Risk classes R0–R3 table intact (4 rows).
  - Controlled-execution DB clause intact ("databases … dedicated owner-specific protocols") — P3 did not weaken it.
- **Insert integrity:** each of P1/P4/P5 present **exactly once** (no double-insert, no drift).
- **Markdown well-formedness:** 18 ``` fences (balanced); 6 `### Stage N` headers (0–5); no orphan code blocks.

## Invariants preserved (the test that matters)

The cycle's claim is that the skill became **stricter, not laxer**. Evidence:

- P1 **strengthens** the broad-prune ban: it now names `brew --prune=all` (no formula) and unscoped owner-native cleans as forbidden, where v4 only said "broad prune commands" abstractly.
- P4 **strengthens** measurement coverage: a `du -d 1` gap can no longer be silently labelled "unattributed" without a loose-file sweep.
- P5 **strengthens** the R1 bar: "no symlink ⇒ R1" is now explicitly rejected; R1 requires positive pin/default/global-state evidence.
- P3 **preserves** the owner-specific-DB invariant by refusing to add a universal SQLite step.
- No HITL binding, no per-target approval, no one-target-at-a-time, no fail-closed default, no report-privacy clause was altered.

## Artifacts (final state)

| File | Hash (sha1) | Change |
|---|---|---|
| `SKILL.md` | `59f041cad5a9…` | +P1+P4+P5 (267 → 302 lines); orig `bd9e25a1…` |
| `audits/AUDIT-v5.md` | `c39944572c6a…` | revised: dispositions, epistemic labels, P1/P5 → APPLIED |
| `tests/test_audit_logic.py` | `3ea7d3de…` | +1 P4 regression (14 tests) |
| `tests/pressure-scenarios.md` | `179445cc…` | +7 scenarios (46 → 53): #47–50 P2, #51 P4, #52 P5, #53 P1 |
| `/tmp/disk-v5-verify-{p1,p4,p5}.md` | — | fresh evidence from the verify sub-agents |

## Remaining work

1. **P2 field test** — run the 4 gate scenarios (#47–50) with an independent agent (RED without the gate, GREEN with). Until then P2 cannot be `PASS`.
2. **nvm live check** — nvm was not installed on the audit host; its alias logic was verified by spec only. Re-confirm when nvm is present.
3. **pipx/uv overlap** — the host showed `graphifyy` installed by both pipx and uv tool (cross-manager ownership). P5's reformulation keys on ownership metadata, not directory name; worth one more field case to confirm.

## Final assessment

The skill leaves this cycle materially safer: three real seams a cleanup session exposed (loose files, unscoped owner-native clean, version-stack false-positives) are now normative rules with regression evidence, and one over-reach (generic VACUUM) was refused rather than rationalised. The only open item (P2) is an honest limit, not a hidden gap. The draft is not yet production-autonomous (the deployment gate's 5 points still stand), but as an assisted HITL protocol it is tighter than v4.
