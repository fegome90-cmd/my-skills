# Audit addendum — observability and macOS-native diagnosis

## Verdict

The v2 draft is strong at preventing unsafe deletion but weak at explaining *why* the disk is full. It begins too close to target classification and does not require a reproducible storage map, candidate report, or visual accounting of unexplained usage.

This v3 draft adds a read-only observability phase before the existing HITL cleanup transaction.

## What was missing

1. **No layered storage model.** `df`, APFS containers/volumes, snapshots, directory allocation, logical file sizes, and reclaimable bytes were not separated clearly enough.
2. **Insufficient macOS-native inventory.** The skill mentioned only a subset of `diskutil` and `tmutil`, and did not require `system_profiler`, volume roles, raw plist/JSON evidence, or a GUI cross-check.
3. **No reproducible space attribution.** There was no iterative depth-one scan, scope coverage, permission/error accounting, or “unattributed” remainder.
4. **No candidate taxonomy.** Large files, cache paths, low-activity directories, tool-owned data, and approved cleanup targets could be conflated.
5. **Weak inactivity semantics.** Directory mtime and age needed explicit rejection as sufficient proof. Recursive content activity, app/Git signals, open handles, coverage, and confidence are now required.
6. **No visual decision artifact.** The skill did not require charts, source provenance, confidence, or local/private handling of paths.
7. **Too much judgment left in prose.** A local read-only helper now performs repeatable collection and creates structured evidence without containing destructive actions.

## Added architecture

### Stage 1 — native capacity and APFS

Collects mounted filesystem, device, APFS container/volume, storage profiler, and snapshot evidence.

### Stage 2 — bounded attribution

Measures exact top-level children of user-approved scopes. No `sudo`, no recursive `/` scan, no cross-volume traversal by default.

### Stage 3 — candidates

Separates:

- large-file candidates;
- cache candidates;
- low-activity candidates;
- tool-native reclaimable-data reports;
- approved cleanup targets.

### Stage 4 — native owners

Uses Docker, Homebrew, Xcode/simctl, and package-manager inventory or dry runs when those tools are installed.

### Stage 5 — local report

Creates:

- `report.html` with embedded SVG charts;
- `summary.json`;
- raw command stdout/stderr and exit status;
- SHA-256 evidence manifest.

The report explicitly labels the difference between filesystem usage and selected-scope attribution as **unattributed**, not “junk”.

## Safety properties of the helper

`scripts/macos_storage_audit.py`:

- exits unless running on macOS;
- sets `umask 077` and user-only output permissions;
- runs only read-only inventory/dry-run commands;
- has no delete, move, prune execution, snapshot thinning, Trash emptying, or privilege escalation;
- stays on each selected filesystem during recursive scans;
- revalidates Spotlight candidates with `lstat`;
- records logical and allocated bytes separately;
- limits activity scans and labels truncated scans low confidence;
- keeps raw evidence local;
- hashes the final report bundle.

## Known limitations

1. The helper has been syntax-checked but not executed on a real macOS host in this environment.
2. `du`, APFS clone sharing, snapshots, hard links, sparse files, and filesystem accounting can still diverge; the report treats reclaimable bytes as uncertain.
3. `mdfind` emits line-oriented paths. Results are candidates only and are revalidated; deep filesystem mode is the safer path for unusual filenames.
4. Open-handle checks are intentionally deferred to selected candidates because recursive `lsof +D` can be expensive and privacy-sensitive.
5. Tool-native commands vary by installed version; failures are retained as evidence rather than silently ignored.
6. Behavioral RED–GREEN agent testing and controlled macOS fixtures remain required before deployment.

## New pressure tests

Scenarios 21–32 cover:

- single-number diagnosis;
- unsafe full-root scans;
- cache-name and mtime fallacies;
- stale Spotlight metadata;
- unreliable access time;
- APFS clone overestimation;
- snapshot/accounting blind spots;
- report privacy leaks;
- misleading graphics;
- unbounded deep scans;
- failure to use app-native dry runs.
