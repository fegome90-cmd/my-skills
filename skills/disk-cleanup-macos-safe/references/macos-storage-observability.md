# macOS storage observability reference — v4

Use this during the read-only discovery phase. It defines measurement semantics and failure modes; it does not authorize cleanup.

## 1. Measurement model

Do not collapse these layers:

| Layer | Question | Preferred evidence | Common error |
|---|---|---|---|
| Physical device | What storage hardware exists? | `system_profiler -json SPStorageDataType`, `diskutil list -plist` | Equating hardware capacity with usable or reclaimable capacity. |
| APFS container | Which volumes share capacity? | `diskutil apfs list -plist` | Adding free/used values from volumes in the same container. |
| System/Data group | Which view is read-only and which stores user data? | `diskutil info -plist /`, `/System/Volumes/Data` | Treating `/` and Data as separate additive disks. |
| Mounted filesystem | What does POSIX accounting report? | `df -kP <mount>` | Using one `df` number to infer directory ownership. |
| Foundation capacity | What capacity can the OS expose for ordinary, important, or opportunistic use? | `URLResourceKey` volume capacity keys | Calling important/opportunistic capacity “free”, “purgeable”, or guaranteed reclaim. |
| Snapshots | Is retained history associated with a volume? | Disk Utility snapshot view, `diskutil apfs listSnapshots`, `tmutil listlocalsnapshots` | Deleting snapshots under a generic cleanup approval or summing snapshot columns as immediate reclaim. |
| Directory allocation | Which scoped trees currently account for allocated blocks? | exact-child `du -skx`, bounded `du -d 1` | Suppressing errors and presenting partial output as complete. |
| File logical/allocated size | Which items appear large and how much local allocation is visible? | `lstat`, `st_blocks`, Foundation file size keys | Counting sparse/cloud-only logical bytes as local allocation. |
| Package boundary | Is this directory an atomic application/document package? | Foundation `isPackage`, known package suffixes | Traversing Photos libraries, sparse bundles, apps, or archives and offering internal fragments. |
| Cloud residency | Is a cloud item local, uploading, conflicted, or cloud-only? | Foundation ubiquitous-item keys plus Finder/provider status | Deleting or moving an item to free local space when Remove Download/eviction was intended. |
| Activity | Which candidates have little observed activity? | bounded recursive mtime, birthtime, Git/app metadata, open handles, baseline | Calling “old” or “not recently used” equivalent to disposable. |
| Native ownership | What does Docker/Homebrew/Xcode/etc. say? | structured inventory and dry runs | Inferring tool state solely from directory names. |

## 2. System and Data volume interpretation

Modern macOS presents a read-only System volume and a writable Data volume in one Finder view. Collect both:

```bash
df -kP /
df -kP /System/Volumes/Data

diskutil info -plist /
diskutil info -plist /System/Volumes/Data
diskutil apfs list -plist
```

Interpret `APFSVolumeGroupID`, container reference, mount point, volume role, and read-only state. If System and Data belong to one volume group/container, do not add their capacities. Ordinary cleanup candidates should come from the Data/user/application side, not the sealed system side.

## 3. Foundation volume capacity

The included Swift helper reads public `URLResourceKey` values:

```bash
swift scripts/macos_resource_probe.swift volume / /System/Volumes/Data
```

Keep these columns separate:

- total capacity;
- ordinary available capacity;
- available capacity for important usage;
- available capacity for opportunistic usage.

They are not additive. The latter two express OS-level capacity policy for classes of work, not bytes already reclaimed by the user and not an exact cleanup target.

## 4. Scope normalization and per-device accounting

Before scanning:

1. Resolve each root.
2. reject missing or unsafe scope roots;
3. remove duplicates;
4. if a parent and child are both supplied, keep the parent and record the exclusion;
5. identify device and mount point;
6. group attribution by device;
7. protect the report directory.

Never compute:

```text
internal used - internal scope - external scope
```

A safe per-device summary is:

```text
filesystem used
sum of complete measurements within selected child scopes
count/size unknown because measurements were partial
used outside selected scopes or otherwise unattributed
```

The final difference includes data outside scope and measurement semantics. It is not a cleanup estimate.

## 5. Complete vs partial `du`

For every `du` invocation preserve:

- return code;
- timeout;
- stderr byte count/content in bounded evidence;
- parsed size;
- complete/partial flag.

A size returned alongside an error is partial evidence. Do not discard stderr with `2>/dev/null` in the audit helper. TCC, unreadable subtrees, disappearing files, and I/O errors all lower coverage.

## 6. TCC and privacy coverage

macOS can require consent for Desktop, Documents, Downloads, iCloud Drive, network volumes, removable volumes, and full internal storage access. A terminal/helper without permission may produce a structurally valid but incomplete report.

Rules:

- do not enable Full Disk Access automatically;
- never imply the user must grant it merely to continue;
- identify which scopes failed and preserve errors;
- offer a narrower user-approved scan or explicit manual permission decision;
- label completeness independently from size.

## 7. Spotlight confidence

Collect index status before relying on indexed discovery:

```bash
mdutil -s /
mdutil -s /System/Volumes/Data
```

Then use bounded queries:

```bash
mdfind -onlyin "$HOME" 'kMDItemFSSize >= 1073741824'
```

Spotlight can be disabled, rebuilding, excluded, stale, or missing metadata importers. Every result must be revalidated against the current filesystem. A truncated raw result set is incomplete and should not be consumed as a complete list.

## 8. Packages and atomic boundaries

Treat Finder/Foundation packages as one item by default. Examples:

```text
*.photoslibrary
*.sparsebundle
*.backupbundle
*.app
*.appex
*.framework
*.xcarchive
*.xcodeproj
*.xcworkspace
```

A package can contain databases, media, indexes, version history, or internal references. Large-file walkers should prune package directories rather than traverse them. Any owner-supported internal cleanup must be a separate protocol with backup and exact HITL.

## 9. Cloud-backed items

The Swift helper reads public ubiquitous-item metadata for selected large candidates:

```bash
swift scripts/macos_resource_probe.swift item /path/to/candidate ...
```

Relevant states:

- cloud-backed/ubiquitous;
- locally downloaded;
- currently uploading;
- unresolved conflicts;
- downloading status;
- logical and allocated size.

Interpretation:

| State | Meaning for cleanup |
|---|---|
| cloud-only/not downloaded | Large logical size may consume little local allocation; do not count it as reclaim opportunity. |
| downloaded, synchronized | Candidate for provider-native local eviction after user review; not a deletion candidate by default. |
| uploading | Block eviction/deletion recommendation. |
| unresolved conflict or error | R3 until resolved and verified. |
| third-party provider/unknown | Require Finder/provider-native status; do not infer from the path. |

For iCloud Drive, Finder’s **Remove Download** removes the local download while retaining the cloud item. Moving an item out of iCloud Drive is semantically different and can remove it from iCloud across devices.

## 10. Activity and trend evidence

Use several independent signals:

1. newest recursive content mtime within bounded coverage;
2. birthtime and directory mtime;
3. meaningful Spotlight last-used metadata;
4. Git status, branches, upstreams, stashes, worktrees, reflog, and LFS/submodules;
5. owner-app recent projects/history;
6. running processes and open handles;
7. comparison with a previous `summary.json`;
8. user confirmation.

Baseline comparison uses a local path fingerprint and allocated size. A positive/zero/negative delta is diagnostic only. It does not prove value, inactivity, recoverability, or safety.

## 11. Native tool semantics

### Docker

```bash
docker system df --format json
docker system df -v
docker ps -a --size
docker volume ls
```

Preserve:

- virtual size;
- shared size;
- unique size;
- reclaimable figure reported by Docker;
- active references;
- volumes and container writable layers.

Never sum virtual sizes as independent allocation. Do not substitute filesystem size of Docker’s disk image for engine-level ownership. Any prune filters and targets require a new manifest and approval.

### Homebrew

```bash
brew --cache
brew config
brew cleanup -n
brew autoremove --dry-run
```

Dry runs identify what the installed Homebrew version considers removable. They remain candidate evidence and can change between discovery and execution.

### Xcode

```bash
xcode-select -p
xcrun simctl list runtimes
xcrun simctl list devices
```

Separate DerivedData/build caches from Archives, projects, simulator state, and device support. “Unavailable” simulator metadata is not by itself deletion authorization.

### Per-user macOS cache roots

```bash
getconf DARWIN_USER_CACHE_DIR
getconf DARWIN_USER_TEMP_DIR
```

These identify per-user Darwin cache/temp locations, but their contents still require owner/activity checks. Do not recursively purge the roots.

## 12. Report no-harm budget

The audit itself writes data and performs I/O. It must:

- check free space on the output filesystem before creating the bundle;
- refuse when there is insufficient room for minimal trustworthy evidence;
- automatically disable deep/optional scans in low-space mode;
- cap every stdout/stderr stream and mark truncation;
- offer an external output volume;
- use `umask 077` and user-only permissions;
- protect the report from candidate/cleanup selection;
- never upload reports automatically.

A truncated command can still prove that output exists, but not that the retained list is complete.

## 13. Report interpretation

Minimum outputs:

```text
report.html
summary.json
directory-sizes.tsv
cache-candidates.tsv
large-items.tsv
raw/
SHA256SUMS.txt
```

Minimum visuals/tables:

1. System/root and writable Data capacity views;
2. ordinary, important, and opportunistic available capacity as separate non-additive fields;
3. per-device measured vs outside-scope/unattributed values;
4. top complete directory allocations;
5. partial/TCC/Spotlight coverage;
6. package and cloud state;
7. baseline growth deltas;
8. native command status and truncation.

Never render a “safe to delete” chart before ownership, recoverability, backup, immutable manifest, and exact approval.

## 14. Known limitations

Even v4 cannot calculate exact reclaimable bytes before a controlled operation because APFS clones/shared extents, snapshots, compression, hard links, sparse files, cloud providers, Docker layers, and system-managed capacity interact. The correct output is a range with uncertainty, followed by post-action measurement—not a confident single number.
