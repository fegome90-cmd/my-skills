# Audit v4 — macOS storage diagnosis before destructive cleanup

**Date:** 2026-07-16  
**Status:** Draft; static and portable verification only. No claim of macOS runtime validation.

## Executive judgment

The v3 skill was materially safer than the original for deletion, but its observability helper still had several ways to produce a confident-looking but incomplete or semantically wrong report. The v4 addresses the highest-risk gaps without adding destructive capabilities.

## Findings incorporated

### 1. System and Data were not modeled explicitly

Modern macOS separates the read-only System volume from the writable Data volume while Finder presents a merged view. A root-only `df`/`diskutil` interpretation can therefore misattribute user data or double-count related views.

**Change:** inventory `/` and `/System/Volumes/Data`, record volume group/container identifiers, and state that paired views are non-additive.

Primary source: Apple Support, “About the read-only system volume in macOS Catalina or later” — https://support.apple.com/en-us/101400

### 2. `df` did not express all OS capacity semantics

The Foundation URL resource API exposes ordinary available capacity and separate capacity values for important and opportunistic usage. These are not interchangeable with `df` and cannot be summed or called guaranteed reclaim.

**Change:** add a read-only Swift/Foundation probe and render the metrics as distinct non-additive fields.

Primary sources:

- https://developer.apple.com/documentation/foundation/urlresourcekey/volumeavailablecapacityforimportantusagekey
- https://developer.apple.com/documentation/foundation/urlresourcekey/volumeavailablecapacityforopportunisticusagekey

### 3. Partial `du` results could disappear behind `None`

The v3 helper discarded command status and stderr from exact-child `du`. TCC or permissions could therefore make a scan incomplete without explaining why.

**Change:** every directory measurement carries return code, timeout, stderr bytes, completeness, activity coverage, and confidence. Partial measurements are excluded from exact accounting claims.

Primary source: Apple Platform Security, “Controlling app access to files in macOS” — https://support.apple.com/guide/security/controlling-app-access-to-files-secddd1d86a6/web

### 4. Overlapping scopes and multiple filesystems could distort accounting

Supplying `$HOME`, `$HOME/Library`, and an external scope could double-count or subtract allocation from the wrong filesystem.

**Change:** canonicalize scopes, remove parent/child overlap, group by device/mount, and calculate only a per-device “outside scopes or unattributed” difference with explicit semantics.

### 5. Spotlight confidence was not tied to index status

Spotlight is useful for bounded metadata queries but can be disabled, rebuilding, excluded, or stale.

**Change:** capture `mdutil` status, preserve truncation, and keep filesystem revalidation mandatory. Truncated indexed output is never treated as a complete candidate set.

Primary source: Apple Developer Documentation Archive, “File Metadata Query Expression Syntax” — https://developer.apple.com/library/archive/documentation/Carbon/Conceptual/SpotlightQuery/Concepts/QueryFormat.html

### 6. Cloud logical size could be mistaken for local allocation

A cloud-only file can present a large logical size while consuming little local storage. Deleting or moving an iCloud item also differs materially from removing its local download.

**Change:** probe public Foundation ubiquitous-item metadata for selected large candidates; block recommendations when uploading/conflicted/unknown; distinguish local eviction from deletion and direct iCloud items to Finder’s Remove Download workflow after sync verification.

Primary sources:

- Apple Support, “Work with folders and files in iCloud Drive” — https://support.apple.com/guide/mac-help/work-with-folders-and-files-in-icloud-drive-mchl1a02d711/mac
- Foundation FileManager `evictUbiquitousItem(at:)` — https://developer.apple.com/documentation/foundation/filemanager/evictubiquitousitem(at:)

### 7. Package directories needed atomic boundaries

Photos libraries, sparse bundles, applications, archives, and project packages can contain critical internal state. A generic recursive walker must not offer their children as independent cleanup fragments.

**Change:** known package suffixes and Foundation package metadata are treated as atomic R2/R3 boundaries; deep file scanning prunes them.

### 8. The audit itself could worsen a nearly full disk

The v3 raw command capture was unbounded. A large native command result or deep report could consume the remaining capacity.

**Change:** check output-filesystem free space, refuse below a hard minimum, automatically enter minimal mode below a configured threshold, cap every stdout/stderr stream, mark truncation, skip optional/deep scans, and recommend an external output path.

### 9. Docker virtual size could be overclaimed

Docker reports virtual, shared, and unique image sizes. Summing virtual sizes as if independently reclaimable is incorrect.

**Change:** collect structured JSON and verbose engine evidence, retain shared/unique semantics, and forbid virtual-size summation.

Primary source: Docker CLI reference, `docker system df` — https://docs.docker.com/reference/cli/docker/system/df/

### 10. Homebrew ownership evidence was incomplete

The v3 used `brew cleanup -n` but omitted dry-run orphan dependency evidence.

**Change:** add `brew autoremove --dry-run`, retain `brew cleanup -n`, cache path, and config.

Primary source: Homebrew `brew(1)` manpage — https://docs.brew.sh/Manpage

### 11. Repeated reports lacked a stable diagnostic trend

A single old timestamp is weak evidence. Growth over time can identify active caches or runaway artifacts, but still does not prove disposability.

**Change:** optional baseline comparison uses a stable local path fingerprint and allocated-size delta. Deltas are explicitly diagnostic only.

### 12. APFS snapshots remain a separate protected class

Snapshot presence and private/cumulative size can explain discrepancies, but generic cleanup approval must not remove them.

**Change:** query both root/Data views, retain Disk Utility cross-check, and keep snapshots R3 under generic cleanup.

Primary source: Apple Disk Utility User Guide, “View APFS snapshots in Disk Utility on Mac” — https://support.apple.com/guide/disk-utility/view-apfs-snapshots-dskuf82354dc/mac

## Deliberately not added

More commands are not automatically safer. The following remain outside the default path:

- broad `sudo du /` scans;
- continuous `fs_usage` tracing;
- recursive `lsof +D` across large trees;
- private Storage Management frameworks/APIs;
- automated Full Disk Access changes;
- automated iCloud/File Provider eviction;
- generic snapshot thinning;
- automatic cache deletion based on age/path;
- opaque third-party disk-cleaner utilities.

They are either invasive, privileged, expensive, unstable, or too easy to misinterpret.

## Verification performed in this environment

- Python bytecode compilation.
- 13 portable unit tests for scope normalization, device separation, partial measurements, packages, output truncation, baseline identity, cloud-key lookup, and `df` parsing.
- Swift syntax parse on Linux; the inactive macOS Foundation branch was not runtime/type-checked against a macOS SDK.
- Static scan for destructive subprocess commands in executable helpers.
- Synthetic HTML report generation.
- YAML frontmatter parse.
- ZIP integrity and SHA-256 inventory.

## Remaining blockers before production

1. Compile and run the Swift probe on each supported macOS family.
2. Capture real `diskutil -plist` and Foundation fixtures from Intel and Apple silicon Macs.
3. Test TCC-denied and Full-Disk-Access environments without changing permissions automatically.
4. Test Spotlight disabled, rebuilding, and excluded volumes.
5. Test iCloud downloaded, cloud-only, uploading, conflicted, and third-party File Provider cases.
6. Test Photos libraries, sparse bundles, Xcode archives, VMs, and other packages.
7. Test APFS clones, sparse files, hard links, snapshots, and external filesystems.
8. Test Docker Desktop shared layers, volumes, writable layers, and disk-image accounting.
9. Run all 46 pressure scenarios RED without the skill and GREEN with it using independent agents.
10. Enforce immutable per-call HITL in the actual runtime/tool wrapper; prose alone cannot guarantee no harm.

## Final assessment

The v4 is a stronger diagnostic and planning skill, not a production-ready autonomous cleaner. Its main improvement is epistemic discipline: it tells the agent what is known, what is partial, what shares capacity, what is cloud-only, and what remains unsafe to infer.
