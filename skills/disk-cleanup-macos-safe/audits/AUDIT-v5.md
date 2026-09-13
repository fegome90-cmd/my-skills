# Audit v5 — field-tested gaps from a real cleanup session (REVISED)

**Date:** 2026-08-12 (revised 2026-08-13 after governed audit)
**Status:** Audit complete. P1/P4/P5 APPLIED to `SKILL.md`. P2 = REVISE (field-test limit). P3 = DESCARTED (VACUUM) → normative observation only.
**Session context:** macOS 26.6, disk 97% → ~88%, +38.7 GiB reclaimed using v4 under HITL.
**Governed audit:** AUDIT-v5 treated as candidate evidence, not authority. Each patch verified against the live repo + host commands before disposition.

## Disposition summary

| Patch | Disposition | Reason |
|---|---|---|
| P1 owner-native clean | **APPLIED** | brew `-s --prune=all` is broad-prune (violates core contract); `cargo cache -a` is 3rd-party, not core; claims "atomic/manifest-aware" unproven |
| P2 active-owner gate | **REVISE** | `pgrep => R2/R3` is single-evidence; redesign as 3-state proportional gate |
| P3 SQLite VACUUM | **DESCARTED** | generic VACUUM violates "databases require owner-specific protocols"; decision: keep as normative observation only |
| P4 loose files | **APPLIED** | premise empirically confirmed; corrected "equivalent" claim; prose-only Stage 2 |
| P5 version stacking | **APPLIED** | `no symlink => R1` unsound (3 counter-examples on host); split into 4 categories |

## Epistemic labels used below

- **[FIELD OBSERVATION]** — measured in the real session (GiB, commands run).
- **[INFERENCE]** — derived reasoning, not directly measured.
- **[NORMATIVE RULE]** — a rule the skill should state; derived from v4 invariants.
- **[EXTERNAL EVIDENCE]** — verified via the tool's own CLI/docs on this host.
- **[PENDING LIMITATION]** — known gap not closed in this audit.

---

## P1 — owner-native reclaim → REVISE

**[FIELD OBSERVATION]** `npm cache clean --force` reclaimed 8.77 GiB (74% of cache reclaim) — the principle "prefer owner-native over rm" is valid.

**[EXTERNAL EVIDENCE]** verification per tool (host commands, `/tmp/disk-v5-verify-p1.md`):

| tool | clean-cmd | owner-native? | real-target (via tool config) | verdict |
|---|---|---|---|---|
| npm | `npm cache clean --force` | YES | `npm config get cache` → `~/.npm` | clean deprecated since npm@5, gated behind `--force`; `npm cache verify` is the safe rebuild |
| uv | `uv cache clean [PKG]` | YES | `uv cache dir` → `~/.cache/uv` | link-mode=clone (APFS default) → venvs survive; **refuse if `link-mode=symlink`**; `--force` bypasses in-use guard |
| bun | `bun pm cache rm` | YES | `bun pm cache` → `~/.bun/install/cache` | `bun pm cache` (no `rm`) is read-only; hardlinks survive |
| pnpm | `pnpm store prune` | YES | `pnpm store path` → store/v10 | removes only unreferenced pkgs; safe; `--force` also removes alien dirs |
| brew | `brew cleanup -s <formula> --dry-run` | YES | `brew --cache` | **`--prune=all` + no formula = BROAD PRUNE (global)** — violates exact-target HITL; `-s` scrubs even latest downloads |
| cargo | ~~`cargo cache -a`~~ | **NO — 3rd-party crate** | `~/.cargo/registry/cache` | `cargo-cache` (v0.8.3) NOT installed → cmd FAILS; core Cargo has no cache subcommand |

**[NORMATIVE RULE]** owner-native clean is preferred over `rm`, but only when scoped to the approved target. A global clean (no package/formula arg) is broad-prune and is forbidden by the core contract.

**[INFERENCE]** the table's "invariant preserved / manifest-aware / atomic" claims were not demonstrable for every tool; replace them with the per-tool evidence above (uv in-use checks, pnpm referenced-aware, npm verify=safe).

**Corrected patch P1** (proposed, not applied): the table with brew scoped to `<formula>`, cargo removed (or marked "requires `cargo install cargo-cache`"), and claims replaced by per-tool evidence. Add: refuse `uv cache clean` when `link-mode=symlink`.


**Applied change** (SKILL.md Stage 4): owner-native reclaim table — brew scoped to `<formula>`, `--prune=all`/no-arg flagged as broad-prune (forbidden); cargo `cache -a` removed (3rd-party crate); per-tool evidence replaces unproven 'atomic/manifest-aware' claims; refuse `uv cache clean` when `link-mode=symlink`.

---

## P2 — active-owner gate → REVISE

**[FIELD OBSERVATION]** `uv cache clean` failed with a 300s lock timeout; ~10 GiB of caches had to be preserved because their owners were active.

**[INFERENCE]** v4 already names "active/syncing item" (R3) and "open handles" (3 sites), but never as an operational step.

**[NORMATIVE RULE]** the gate must use proportional evidence, not a single signal. Three states:

1. `owner-exists` (pgrep) — weak; does not reclassify alone.
2. `target-actually-locked` — strong: `lsof`/flock on target, owner-native clean fails with lock, or target mtime recent while owner runs.
3. `activity-undeterminable` (TCC/opaque tool) → **fail-closed R2/R3**.

This does NOT change the R0–R3 taxonomy: `locked`→R3 (already covered), `undeterminable`→R2 (uncertain, already covered). It only operationalises the check v4 already requires.

**[PENDING LIMITATION]** AUDIT-v5 admits a second field test is missing → P2 cannot be PASS until that test runs.

**Corrected patch P2** (proposed, not applied): 3-state gate + 4 regression scenarios added to `pressure-scenarios.md` (owner inactive / owner active target-not-implicated / target locked / lock undeterminable).

---

## P3 — SQLite VACUUM → DESCARTED (normative observation)

**[FIELD OBSERVATION]** `opencode.db` (3.2 GiB) + `kilo.db` (1.1 GiB) were user state, not cache; `du -d 1` hid them.

**[NORMATIVE RULE]** `*.db` does not demonstrate "cache" or "state" — owner and semantics must be discovered. SKILL.md (Controlled execution) requires *"databases … require their dedicated owner-specific protocols."* A generic VACUUM violates that invariant.

**[EXTERNAL EVIDENCE]** the script has zero SQLite/`*.db`/VACUUM awareness (explored: full gap).

**Decision (user, 2026-08-13):** discard generic VACUUM from the cleanup flow. Keep only the normative observation: *app `*.db` files are user state (R2/R3); never `rm`; if reclamation is needed, the owning app must provide its own compact/maintenance protocol — do not model a universal SQLite step in this skill.*

No patch applied. The "10–40% reclaim" heuristic is removed (no reproducible evidence; was an unsound universal claim).

---

## P4 — loose files → APPLIED

**[FIELD OBSERVATION]** 4.3 GiB of state DBs were invisible to the first `du -d 1` pass — they appeared only as an unexplained gap.

**[EXTERNAL EVIDENCE]** empirical fixture test (`/tmp/disk-v5-verify-p4.md`):

| method | surfaces loose root files? |
|---|---|
| `du -d 1` | **NO** — bytes fold into the dir aggregate, files never listed |
| `find -maxdepth 1 -type f` | YES — bare paths, minimal-sufficient |
| `du -a -d 1` | YES — but emits sizes + aggregates too (NOT equivalent to find) |
| `find … -size +500M` | conditional — lossy filter; silently drops small loose files |

**[NORMATIVE RULE]** pair every Stage 2 `du -d 1` with a loose-file sweep; prefer `find -maxdepth 1 -type f` for discovery; treat size thresholds as optional refinement, not default.

**[EXTERNAL EVIDENCE]** the script's `iter_children` (line 522) already captures root files via `os.scandir` — so the gap is in the prose `du` command, not the helper. The fix is prose-only.

**Applied change** (SKILL.md Stage 2, before "For every measurement preserve:"): warning + `find "$SCOPE" -maxdepth 1 -type f -exec du -k {} \; | sort -rn` fallback; "equivalent" claim removed; size-filter labelled optional.

---

## P5 — version stacking → REVISE

**[FIELD OBSERVATION]** claude/versions (0.47 GiB) + fnm/nvm node (0.8 GiB) were reclaimable in the session.

**[EXTERNAL EVIDENCE]** `no symlink => R1` is unsound — 3 counter-examples on this host (`/tmp/disk-v5-verify-p5.md`):

- **Case A**: rustup `1.97.0` has no symlink but is pinned by `Developer/arsenalero/rust-toolchain.toml` → deleting breaks `cargo build`.
- **Case B**: fnm `v24.18.0` has no symlink but is pin-resolved by `Developer/open-design/.node-version`=`24` (major→latest v24.x).
- **Case C**: pipx `graphifyy` — symlink exists but points at a uv-tool object (cross-manager); pipx entry is a stale orphan. Symlink misleads in both directions.

**[NORMATIVE RULE]** split into 4 categories: (1) self-binary/runtime stacks, (2) language-runtime managers, (3) managed-app venvs (pipx/`uv tool`), (4) platform runtimes (nix/brew/system). "Unused" is per-manager: native `list` + pin-file resolution (`.nvmrc`/`.node-version`/`rust-toolchain.toml`/`.python-version`) + default-alias + global-state guard. pipx/uv apps are **managed objects** (remove via `uninstall <app>`), never version siblings.

**[PENDING LIMITATION]** nvm not installed on this host → its alias logic verified by spec only.

**Corrected patch P5** (proposed, not applied): category split + per-manager unused criteria + managed-object modelling for pipx/uv.


**Applied change** (SKILL.md Stage 3): version-stacking section split into 4 categories; 'no symlink => unused' explicitly rejected; pin-file resolution (`.nvmrc`/`.node-version`/`rust-toolchain.toml`/`.python-version`/`.ruby-version`, incl. major-pin resolution) + default-alias + global-state guard required; pipx/`uv tool` apps modelled as managed objects (remove via `uninstall <app>`, never version siblings).

---

## Scope chosen

**B (pragmatic):** P4 applied (prose) + regression evidence (test + pressure scenarios) + P1/P2/P5 documented as normative rules for later review. **Not C:** the script already captures root files via `os.scandir`; new TSVs/detectors are over-engineering for prose-level gaps.

## Verification evidence added

- `tests/test_audit_logic.py`: `test_iter_children_captures_loose_root_files` — proves the helper already surfaces loose files (so P4 is prose-only, not a code change).
- `tests/pressure-scenarios.md` #47–51: 4 active-owner-gate scenarios (P2) + 1 loose-file-gap scenario (P4).

## Limitations of this audit

- P2 not PASS until the second field test runs.
- nvm alias semantics verified by spec, not live (nvm not installed).
- pipx/uv overlap (graphifyy) shows ownership can cross managers — P5 reformulation must key on ownership metadata, not dir name.
