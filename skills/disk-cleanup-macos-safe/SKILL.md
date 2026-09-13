---
disable-model-invocation: true
name: disk-cleanup-macos-safe
description: Use when diagnosing storage usage or identifying space reclamation candidates on macOS (read-only diagnosis, risk classification, and candidate discovery only; autonomous destructive execution is strictly prohibited).
compatibility: macOS; POSIX shell. Python 3 and Swift are optional but recommended for the included local observability helpers. Tool-specific CLIs are used only when installed.
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "4.0.0"
  scope: read-only-diagnosis
---

# Safe macOS Storage Diagnosis and Candidate Discovery

## Core contract (Read-Only Diagnosis & Proposal Only)

This skill is strictly a **read-only diagnostic, discovery, and proposal engine**. Autonomous destructive execution by AI agents is strictly prohibited by contract.

1. **Diagnostic & Advisory Scope Only:** This skill discovers storage consumers, calculates APFS capacity models, classifies risk, and generates a structured cleanup proposal. It NEVER executes autonomous deletions, prunes, or mutations.
2. Explain the storage system before proposing cleanup: physical storage, APFS container, System/Data volume group, snapshots, per-device capacity, scoped allocation, tool-owned data, cloud residency, and unresolved gaps.
3. Never collapse `df`, Foundation available capacity, logical size, allocated size, APFS snapshot size, Docker virtual size, and expected reclaim into one number.
4. Discovery produces candidates and proposals only. All destructive actions must be performed manually and intentionally by the human user outside agent workflows.
5. Never use globs, implicit path expansion, or broad prune commands.
6. Unknown, old, large, under `Caches`, or absent from recent-use metadata is not safe.
7. Keep reports local and private. They may expose patient names, projects, usernames, and cloud paths.

## Risk classes (Diagnostic Classification)

| Class | Meaning | Default |
|---|---|---|
| R0 | Read-only local inspection | Proceed within explicit scope and resource limits |
| R1 | Proven regenerable artifact with documented owner and no local state | Manifest + exact approval |
| R2 | User data, repo, worktree, package, cloud item, container/volume, mixed cache, or uncertain recovery | Verified backup + exact approval |
| R3 | System path, snapshot, active/syncing item, incomplete evidence, ambiguous target, unsafe boundary, or failed precondition | Refuse or escalate |

## Workflow

### Stage 0 — define scope and audit budget

Record:

- storage symptom and minimum space needed;
- scan roots and exclusions;
- internal, external, network, and cloud-backed volumes in scope;
- quick vs deep scan;
- path-redaction requirement;
- active clinical, development, backup, VM, and database workloads;
- output location and free-space budget.

Normalize scopes before scanning. Remove duplicates and nested scopes. Group results by filesystem/device. Protect the report directory from candidate discovery and later cleanup.

If the report filesystem has very little free space, use minimal mode or write the report to a verified external volume. The diagnostic must not consume the remaining capacity with unbounded raw output or deep traversal.

### Stage 1 — macOS/APFS capacity model

Use multiple read-only views:

```bash
# Mounted filesystem views
df -kP /
df -kP /System/Volumes/Data

# APFS and volume roles
diskutil info -plist /
diskutil info -plist /System/Volumes/Data
diskutil list -plist
diskutil apfs list -plist
system_profiler -json -detailLevel mini SPStorageDataType

# Snapshots and index status
diskutil apfs listSnapshots /
diskutil apfs listSnapshots /System/Volumes/Data
tmutil listlocalsnapshots /
mdutil -s /
mdutil -s /System/Volumes/Data
```

When Swift/Foundation is available, also read:

- volume total capacity;
- ordinary available capacity;
- capacity available for important usage;
- capacity available for opportunistic usage;
- internal/local/read-only/removable flags and volume UUID.

These values are **non-additive**. “Available for important usage” is not free space already reclaimed and is not a promise that a cleanup will return that amount.

Treat `/` and `/System/Volumes/Data` as paired views when they belong to one APFS volume group. Do not add their capacities. User-controlled cleanup normally concerns the writable Data volume; the sealed/read-only System volume is R3.

Cross-check **System Settings → General → Storage → All Volumes** and **Disk Utility → View → Show APFS Snapshots** when interpretation remains uncertain.

### Stage 2 — bounded allocation and coverage

Start at depth one and descend iteratively:

```bash
du -x -k -d 1 "$HOME"
du -x -k -d 1 "$HOME/Library"
```

`du -d 1` attributes only subdirectories. Large loose files at a directory's root (a SQLite database, a tarball backup, a single model file) fold into the directory total and do not appear as a named child. When the parent total exceeds the sum of its `du -d 1` children, sweep for loose files before calling the gap "unattributed":

```bash
find "$SCOPE" -maxdepth 1 -type f -exec du -k {} \; | sort -rn
```

Prefer `find -maxdepth 1 -type f` for discovery (it lists every root file; `du -a` is not equivalent — it also emits sizes and directory aggregates). A size threshold such as `-size +500M` is an optional refinement, not a discovery default: a small loose file would be silently dropped.

For every measurement preserve:

- exact scope, device, and mount point;
- allocated bytes and timestamp;
- command status, timeout, and stderr;
- permission/TCC failures;
- whether traversal was complete or truncated.

A nonzero `du`, permission denial, timeout, or truncated activity scan makes the measurement partial and low-confidence. Do not silently redirect errors away in an evidence-producing run.

Never subtract allocations from the wrong filesystem. Report per-device:

```text
filesystem used
complete allocation measured inside selected scopes
partial or omitted measurements
outside-scopes / unattributed difference
```

The difference is not “system junk”. It can include data outside scope, snapshots, protected paths, APFS semantics, and measurement error.

### Stage 3 — candidate discovery

Maintain separate sets: large item, cache candidate, low-activity candidate, package, cloud-resident item, and tool-native candidate. None is deletion-approved.

#### Spotlight

Spotlight accelerates discovery only when index status is known:

```bash
mdfind -onlyin "$HOME" 'kMDItemFSSize >= 1073741824'
```

Revalidate each result with `lstat`/`stat`, allocated blocks, identity, mount, and current timestamps. Disabled, rebuilding, stale, or unknown indexing lowers coverage; it never authorizes filesystem conclusions.

#### Packages and libraries

Treat `.photoslibrary`, `.sparsebundle`, `.backupbundle`, `.app`, `.xcarchive`, and other Finder/Foundation packages as atomic R2/R3 boundaries. Do not walk inside and offer internal members as independent cache fragments unless an owner-specific protocol explicitly supports that operation.

#### Version-stacking (old self-binaries and runtimes)

Some tools retain prior versions of themselves. "Unused" must be proven **per manager** — the absence of a symlink is **not** sufficient: a version with no symlink can still be the default alias, resolved by a project pin, or carry global state. Split by category:

- **Self-binary / runtime stacks** — `claude/versions/*`, fnm/nvm `node-versions/*`, rustup toolchains, pyenv/rbenv versions. Resolve the active version via the manager (default alias, `readlink` of the launcher) AND via project pins: `.nvmrc`, `.node-version`, `rust-toolchain.toml`, `.python-version`, `.ruby-version`. A major pin like `24` resolves to the latest `24.x` — check resolution, not just exact match.
- **Language-runtime managers** — pyenv/rbenv/asdf (`global` + the pin files above).
- **Managed-app venvs** — pipx apps and `uv tool` apps. Each app is a **managed object** owned by that manager's metadata (pipx: `~/.local/pipx/venvs/<app>`; uv: `~/.local/share/uv/tools/<app>`). Address by app, remove only via `pipx uninstall <app>` / `uv tool uninstall <app>` — never as a version sibling, and never key on directory name (pipx and uv can both install the same app name; ownership lives in metadata, not the symlink).
- **Platform runtimes** — nix home-manager, Homebrew, `system`. Owned by the package manager; never stack-reclaim.

Reclaim an older sibling only with **positive evidence**: it is not the default alias, not resolved by any pin file in scope, and carries no global packages or installed components tied to that version (`npm ls -g`, rustup `components`). Two managers for the same runtime (e.g. fnm + nvm) may duplicate a version — flag as a user decision, do not auto-resolve.

#### Cloud and File Provider data

For large candidates, use Foundation metadata when available:

- ubiquitous/cloud-backed status;
- downloaded/local residency;
- uploading state;
- unresolved conflicts;
- downloading status;
- logical and allocated size.

A cloud-only logical size is not local reclaimable allocation. Uploading, conflicts, provider errors, or unknown state blocks deletion/eviction recommendations. For iCloud Drive, prefer the Finder/provider-native **Remove Download** workflow after sync verification; deleting or moving an item can affect cloud data across devices.

Third-party File Provider state may remain opaque. Label it unknown and require provider/Finder verification rather than guessing from path names.

#### Activity

Use **low-activity candidate**, never “unused”. Combine bounded recursive newest mtime, birth/mtime, Spotlight last-used metadata where meaningful, Git/app metadata, open handles/running process evidence, baseline growth, and user confirmation.

`atime`, directory mtime, age, or a zero growth delta alone is insufficient.

### Stage 4 — owner-native inventory

Prefer structured, read-only, or dry-run output:

```bash
# Docker: preserve shared/unique/virtual/reclaimable semantics
docker system df --format json
docker system df -v
docker ps -a --size
docker volume ls

# Homebrew
brew --cache
brew cleanup -n
brew autoremove --dry-run

# Xcode
xcode-select -p
xcrun simctl list runtimes
xcrun simctl list devices

# macOS per-user cache/temp roots
getconf DARWIN_USER_CACHE_DIR
getconf DARWIN_USER_TEMP_DIR
```

#### Owner-native reclaim (prefer over rm, scoped to the approved target)

When a tool ships a dedicated clean command, prefer it over `rm` — but only when scoped to the approved target. A clean with no package/formula argument is a **global** operation and is treated as broad-prune (forbidden by the core contract). Resolve the real target via each tool's own config command, not by assuming a path.

| tool | scoped clean (prefer) | real target (via tool config) | notes |
|---|---|---|---|
| npm | `npm cache verify` (safe); `npm cache clean --force` (deprecated, gated) | `npm config get cache` | `clean` refuses without `--force`; `verify` is the safe integrity rebuild |
| uv | `uv cache clean <pkg>` (scoped) | `uv cache dir` | **refuse when `link-mode=symlink`** (breaks venvs); `--force` bypasses the in-use guard |
| bun | `bun pm cache rm` | `bun pm cache` | `bun pm cache` (no `rm`) is read-only; hardlinks survive |
| pnpm | `pnpm store prune` | `pnpm store path` | removes only unreferenced packages; `--force` also removes alien dirs |
| brew | `brew cleanup -s <formula> --dry-run` | `brew --cache` | **`--prune=all` with no formula is broad-prune (global)** — forbidden; `-s` scrubs even latest-version downloads |

`cargo cache -a` is **not** core Cargo — it is the third-party `cargo-cache` crate and fails if not installed. Do not list it as owner-native; core Cargo has no cache subcommand (manual `rm` of `~/.cargo/registry/cache` is the only path).

A clean command that fails with a lock means the owner is active — do not `--force`; defer until the owner is stopped.

Also inspect configured npm, pnpm, Yarn, pip, and uv stores when installed. A dry run is evidence, not execution approval. Never sum Docker virtual image sizes as independently reclaimable; shared layers must remain explicit.

### Stage 5 — local report

Run the included read-only helper:

```bash
python3 scripts/macos_storage_audit.py
python3 scripts/macos_storage_audit.py \
  --scope "$HOME/Developer" \
  --scope "$HOME/Library" \
  --deep-activity \
  --large-gib 1

# Compare growth against a prior run
python3 scripts/macos_storage_audit.py \
  --baseline /path/to/prior/summary.json

# When the startup disk is critically full
python3 scripts/macos_storage_audit.py \
  --output /Volumes/External/macos-storage-audit
```

The bundle contains:

```text
report.html
summary.json
directory-sizes.tsv
cache-candidates.tsv
large-items.tsv
raw/*.stdout.txt
raw/*.stderr.txt
SHA256SUMS.txt
```

Required report semantics:

- System/Data and per-device capacity views;
- ordinary vs important/opportunistic available capacity, clearly non-additive;
- largest complete scoped allocations;
- partial/TCC/Spotlight coverage warnings;
- cloud and package state;
- baseline deltas as signals only;
- bounded/truncated raw command evidence;
- outside-scopes/unattributed difference, never “junk”.

**Reference:** Read `references/macos-storage-observability.md` before interpreting the report.

## Human Manual Execution Handoff

This skill is strictly diagnostic and read-only. AI agents MUST NOT autonomously delete, trash, move, or mutate files.

When candidate items for cleanup are identified:
1. Present the candidate list to the human operator with lexical and resolved paths, allocated sizes, risk tiers, and verified owner/subsystem context.
2. Provide exact copy-pasteable manual shell or Finder commands for the human operator to inspect and execute at their discretion.
3. Explicitly advise the human operator to verify current backups (Time Machine or off-disk) before executing destructive operations.
4. If capacity must be re-measured after manual human cleanup, run the diagnostic audit script again to observe updated allocation deltas.

