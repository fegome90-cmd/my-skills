#!/usr/bin/env python3
"""Read-only macOS storage inventory and local HTML report generator.

The helper separates capacity, allocation, indexed discovery, activity signals,
cloud residency, and cleanup approval. It never performs cleanup operations.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import datetime as dt
import hashlib
import html
import json
import os
import platform
import plistlib
import shutil
import stat as statmod
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

VERSION = "4.0.0-draft"
DEFAULT_LARGE_GIB = 1.0
DEFAULT_INACTIVE_DAYS = 180
DEFAULT_ACTIVITY_LIMIT = 10_000
DEFAULT_RAW_MIB = 2.0
DEFAULT_LOW_SPACE_MIB = 256
HARD_MIN_OUTPUT_MIB = 32
PACKAGE_SUFFIXES = {
    ".app",
    ".appex",
    ".backupbundle",
    ".bundle",
    ".framework",
    ".key",
    ".numbers",
    ".pages",
    ".photoslibrary",
    ".playground",
    ".rtfd",
    ".sparsebundle",
    ".xcarchive",
    ".xcodeproj",
    ".xcworkspace",
}


@dataclasses.dataclass
class CommandResult:
    name: str
    argv: list[str]
    exit_code: int | None
    timed_out: bool
    stdout_file: str
    stderr_file: str
    stdout_bytes: int
    stderr_bytes: int
    stdout_truncated: bool
    stderr_truncated: bool


@dataclasses.dataclass
class DuMeasurement:
    allocated_bytes: int | None
    exit_code: int | None
    timed_out: bool
    stderr_bytes: int
    complete: bool


@dataclasses.dataclass
class DirectoryRecord:
    scope: str
    path: str
    path_id: str
    allocated_bytes: int | None
    logical_bytes: int | None
    mtime_epoch: float | None
    birthtime_epoch: float | None
    newest_content_mtime_epoch: float | None
    activity_files_scanned: int
    activity_scan_complete: bool
    permission_errors: int
    device: int | None
    inode: int | None
    mount_point: str | None
    is_symlink: bool
    is_package: bool
    role: str
    activity_label: str
    confidence: str
    du_exit_code: int | None
    du_timed_out: bool
    du_stderr_bytes: int
    du_complete: bool
    delta_bytes: int | None = None


@dataclasses.dataclass
class ItemRecord:
    path: str
    path_id: str
    item_kind: str
    logical_bytes: int
    allocated_bytes: int
    mtime_epoch: float
    birthtime_epoch: float | None
    device: int
    inode: int
    mount_point: str | None
    source: str
    is_package: bool
    is_ubiquitous: bool | None = None
    is_downloaded: bool | None = None
    is_uploading: bool | None = None
    has_unresolved_conflicts: bool | None = None
    downloading_status: str | None = None
    cloud_probe_status: str = "not-probed"
    delta_bytes: int | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a read-only macOS storage inventory and local HTML report."
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory. Default: ./macos-storage-audit-<timestamp>",
    )
    parser.add_argument(
        "--scope",
        action="append",
        type=Path,
        default=[],
        help="Top-level attribution scope. Repeatable. Defaults to $HOME and /Applications.",
    )
    parser.add_argument(
        "--deep-activity",
        action="store_true",
        help="Recursively inspect candidate activity with a bounded file limit.",
    )
    parser.add_argument(
        "--activity-file-limit",
        type=int,
        default=DEFAULT_ACTIVITY_LIMIT,
        help="Maximum files inspected per candidate in deep-activity mode.",
    )
    parser.add_argument(
        "--inactive-days",
        type=int,
        default=DEFAULT_INACTIVE_DAYS,
        help="Age threshold used only to label low-activity candidates.",
    )
    parser.add_argument(
        "--large-gib",
        type=float,
        default=DEFAULT_LARGE_GIB,
        help="Minimum logical GiB for large-item candidates.",
    )
    parser.add_argument(
        "--skip-spotlight",
        action="store_true",
        help="Do not use Spotlight as a candidate accelerator.",
    )
    parser.add_argument(
        "--deep-large-files",
        action="store_true",
        help="Walk selected scopes for large files; can be I/O intensive.",
    )
    parser.add_argument(
        "--redact-paths",
        action="store_true",
        help="Redact displayed/structured paths. Raw evidence still contains private paths.",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        help="Prior summary.json used only for diagnostic growth deltas.",
    )
    parser.add_argument(
        "--max-raw-mib",
        type=float,
        default=DEFAULT_RAW_MIB,
        help="Maximum bytes retained per stdout/stderr stream for each command.",
    )
    parser.add_argument(
        "--low-space-mib",
        type=int,
        default=DEFAULT_LOW_SPACE_MIB,
        help="Below this free-space threshold, automatically use minimal audit mode.",
    )
    return parser.parse_args()


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def path_id(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", "surrogateescape")).hexdigest()[:20]


def safe_name(value: str) -> str:
    digest = path_id(value)[:10]
    cleaned = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in value)
    return f"{cleaned[:48]}-{digest}"


def display_path(value: str, redact: bool) -> str:
    if not redact:
        return value
    p = Path(value)
    base = p.name or "root"
    return f"{base} [path:{path_id(value)[:12]}]"


def write_private(path: Path, content: str) -> None:
    with path.open("w", encoding="utf-8", errors="surrogateescape") as handle:
        handle.write(content)
    path.chmod(0o600)


def truncate_text(value: str, limit: int) -> tuple[str, bool, int]:
    encoded = value.encode("utf-8", "surrogateescape")
    original = len(encoded)
    if original <= limit:
        return value, False, original
    marker = f"\n--- OUTPUT TRUNCATED: original_bytes={original}, retained_bytes={limit} ---\n"
    kept = encoded[: max(0, limit - len(marker.encode()))]
    result = kept.decode("utf-8", "surrogateescape") + marker
    return result, True, original


def run_capture(
    raw_dir: Path,
    name: str,
    argv: list[str],
    timeout: int,
    max_stream_bytes: int,
) -> CommandResult:
    stem = safe_name(name)
    stdout_path = raw_dir / f"{stem}.stdout.txt"
    stderr_path = raw_dir / f"{stem}.stderr.txt"
    try:
        proc = subprocess.run(
            argv,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="surrogateescape",
            timeout=timeout,
            check=False,
        )
        stdout, stdout_truncated, stdout_bytes = truncate_text(proc.stdout, max_stream_bytes)
        stderr, stderr_truncated, stderr_bytes = truncate_text(proc.stderr, max_stream_bytes)
        write_private(stdout_path, stdout)
        write_private(stderr_path, stderr)
        return CommandResult(
            name=name,
            argv=argv,
            exit_code=proc.returncode,
            timed_out=False,
            stdout_file=stdout_path.name,
            stderr_file=stderr_path.name,
            stdout_bytes=stdout_bytes,
            stderr_bytes=stderr_bytes,
            stdout_truncated=stdout_truncated,
            stderr_truncated=stderr_truncated,
        )
    except subprocess.TimeoutExpired as exc:
        raw_out = exc.stdout or ""
        raw_err = exc.stderr or ""
        if isinstance(raw_out, bytes):
            raw_out = raw_out.decode("utf-8", "surrogateescape")
        if isinstance(raw_err, bytes):
            raw_err = raw_err.decode("utf-8", "surrogateescape")
        raw_err += f"\nTIMEOUT after {timeout}s\n"
        stdout, stdout_truncated, stdout_bytes = truncate_text(raw_out, max_stream_bytes)
        stderr, stderr_truncated, stderr_bytes = truncate_text(raw_err, max_stream_bytes)
        write_private(stdout_path, stdout)
        write_private(stderr_path, stderr)
        return CommandResult(
            name=name,
            argv=argv,
            exit_code=None,
            timed_out=True,
            stdout_file=stdout_path.name,
            stderr_file=stderr_path.name,
            stdout_bytes=stdout_bytes,
            stderr_bytes=stderr_bytes,
            stdout_truncated=stdout_truncated,
            stderr_truncated=stderr_truncated,
        )
    except OSError as exc:
        message = f"{type(exc).__name__}: {exc}\n"
        write_private(stdout_path, "")
        write_private(stderr_path, message)
        return CommandResult(
            name=name,
            argv=argv,
            exit_code=None,
            timed_out=False,
            stdout_file=stdout_path.name,
            stderr_file=stderr_path.name,
            stdout_bytes=0,
            stderr_bytes=len(message.encode()),
            stdout_truncated=False,
            stderr_truncated=False,
        )


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def du_measure(path: Path, timeout: int = 45) -> DuMeasurement:
    if not command_exists("du"):
        return DuMeasurement(None, None, False, 0, False)
    try:
        proc = subprocess.run(
            ["du", "-skx", str(path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="surrogateescape",
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stderr = exc.stderr or ""
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", "surrogateescape")
        return DuMeasurement(None, None, True, len(stderr.encode()), False)
    except OSError:
        return DuMeasurement(None, None, False, 0, False)

    value: int | None = None
    if proc.stdout.strip():
        first = proc.stdout.splitlines()[0].split(maxsplit=1)[0]
        try:
            value = int(first) * 1024
        except ValueError:
            value = None
    complete = proc.returncode == 0 and value is not None and not proc.stderr.strip()
    return DuMeasurement(
        allocated_bytes=value,
        exit_code=proc.returncode,
        timed_out=False,
        stderr_bytes=len(proc.stderr.encode("utf-8", "surrogateescape")),
        complete=complete,
    )


def lstat_summary(path: Path) -> os.stat_result | None:
    try:
        return path.lstat()
    except OSError:
        return None


def is_package_path(path: Path) -> bool:
    return path.suffix.casefold() in PACKAGE_SUFFIXES


def find_mount_point(path: Path) -> Path | None:
    try:
        current = path.resolve(strict=True)
        device = current.stat().st_dev
    except OSError:
        return None
    while current.parent != current:
        try:
            if current.parent.stat().st_dev != device:
                break
        except OSError:
            break
        current = current.parent
    return current


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def normalize_scopes(raw: list[Path], home: Path, protected: list[Path]) -> tuple[list[Path], list[dict[str, str]]]:
    requested = raw or [home, Path("/Applications")]
    accepted: list[Path] = []
    exclusions: list[dict[str, str]] = []
    for candidate in requested:
        expanded = candidate.expanduser()
        try:
            if expanded.is_symlink():
                exclusions.append({"path": str(expanded), "reason": "symlink scope rejected"})
                continue
            resolved = expanded.resolve(strict=True)
        except OSError as exc:
            exclusions.append({"path": str(expanded), "reason": f"unavailable: {exc}"})
            continue
        if any(resolved == existing or is_within(resolved, existing) for existing in accepted):
            exclusions.append({"path": str(resolved), "reason": "nested or duplicate scope"})
            continue
        nested_existing = [existing for existing in accepted if is_within(existing, resolved)]
        for existing in nested_existing:
            accepted.remove(existing)
            exclusions.append({"path": str(existing), "reason": f"superseded by parent scope {resolved}"})
        if any(resolved == item for item in protected):
            exclusions.append({"path": str(resolved), "reason": "protected report evidence"})
            continue
        accepted.append(resolved)
    return accepted, exclusions


def scan_activity(
    path: Path,
    root_device: int,
    enabled: bool,
    file_limit: int,
) -> tuple[float | None, int, bool, int, int | None]:
    st = lstat_summary(path)
    if st is None:
        return None, 0, False, 1, None
    package = is_package_path(path)
    if not enabled or not statmod.S_ISDIR(st.st_mode) or statmod.S_ISLNK(st.st_mode) or package:
        logical = st.st_size if statmod.S_ISREG(st.st_mode) else None
        return st.st_mtime, 0, not package, 0, logical

    newest = st.st_mtime
    scanned = 0
    complete = True
    permission_errors = 0
    logical_total = 0

    def walk_error(_: OSError) -> None:
        nonlocal permission_errors, complete
        permission_errors += 1
        complete = False

    for current, dirs, files in os.walk(path, topdown=True, followlinks=False, onerror=walk_error):
        try:
            current_stat = os.lstat(current)
        except OSError:
            permission_errors += 1
            complete = False
            dirs[:] = []
            continue
        if current_stat.st_dev != root_device:
            dirs[:] = []
            continue

        filtered_dirs: list[str] = []
        for dirname in dirs:
            child = Path(current) / dirname
            try:
                child_stat = child.lstat()
            except OSError:
                permission_errors += 1
                complete = False
                continue
            if child_stat.st_dev != root_device or statmod.S_ISLNK(child_stat.st_mode):
                continue
            if is_package_path(child):
                newest = max(newest, child_stat.st_mtime)
                continue
            filtered_dirs.append(dirname)
        dirs[:] = filtered_dirs

        for filename in files:
            child = Path(current) / filename
            try:
                child_stat = child.lstat()
            except OSError:
                permission_errors += 1
                complete = False
                continue
            if child_stat.st_dev != root_device:
                continue
            newest = max(newest, child_stat.st_mtime)
            logical_total += child_stat.st_size
            scanned += 1
            if file_limit > 0 and scanned >= file_limit:
                complete = False
                dirs[:] = []
                break
        if file_limit > 0 and scanned >= file_limit:
            break

    if permission_errors:
        complete = False
    return newest, scanned, complete, permission_errors, logical_total


def activity_label(
    newest_epoch: float | None,
    activity_complete: bool,
    du_complete: bool,
    threshold_epoch: float,
    deep_enabled: bool,
) -> tuple[str, str]:
    if newest_epoch is None:
        return "unknown", "low"
    if not deep_enabled:
        return "activity-not-assessed", "low"
    if not activity_complete or not du_complete:
        return "measurement-partial", "low"
    if newest_epoch < threshold_epoch:
        return "low-activity-candidate", "medium"
    return "recent-activity-observed", "medium"


def iter_children(scope: Path, protected: Iterable[Path] = ()) -> Iterable[Path]:
    protected_paths = list(protected)
    try:
        with os.scandir(scope) as entries:
            children = []
            for entry in entries:
                child = Path(entry.path)
                if any(child == item or is_within(item, child) for item in protected_paths):
                    continue
                children.append(child)
    except OSError:
        return []
    return sorted(children, key=lambda p: p.name.casefold())


def directory_record(
    scope: Path,
    path: Path,
    role: str,
    deep_activity: bool,
    activity_limit: int,
    threshold_epoch: float,
) -> DirectoryRecord:
    st = lstat_summary(path)
    if st is None:
        return DirectoryRecord(
            scope=str(scope), path=str(path), path_id=path_id(str(path)),
            allocated_bytes=None, logical_bytes=None, mtime_epoch=None,
            birthtime_epoch=None, newest_content_mtime_epoch=None,
            activity_files_scanned=0, activity_scan_complete=False,
            permission_errors=1, device=None, inode=None, mount_point=None,
            is_symlink=False, is_package=is_package_path(path), role=role,
            activity_label="unknown", confidence="low", du_exit_code=None,
            du_timed_out=False, du_stderr_bytes=0, du_complete=False,
        )
    measurement = du_measure(path)
    newest, scanned, complete, errors, logical = scan_activity(
        path, st.st_dev, deep_activity, activity_limit
    )
    label, confidence = activity_label(
        newest, complete, measurement.complete, threshold_epoch, deep_activity
    )
    mount = find_mount_point(path)
    return DirectoryRecord(
        scope=str(scope),
        path=str(path),
        path_id=path_id(str(path)),
        allocated_bytes=measurement.allocated_bytes,
        logical_bytes=logical,
        mtime_epoch=st.st_mtime,
        birthtime_epoch=getattr(st, "st_birthtime", None),
        newest_content_mtime_epoch=newest,
        activity_files_scanned=scanned,
        activity_scan_complete=complete,
        permission_errors=errors,
        device=st.st_dev,
        inode=st.st_ino,
        mount_point=str(mount) if mount else None,
        is_symlink=statmod.S_ISLNK(st.st_mode),
        is_package=is_package_path(path),
        role=role,
        activity_label=label,
        confidence=confidence,
        du_exit_code=measurement.exit_code,
        du_timed_out=measurement.timed_out,
        du_stderr_bytes=measurement.stderr_bytes,
        du_complete=measurement.complete,
    )


def getconf_path(key: str) -> Path | None:
    if not command_exists("getconf"):
        return None
    try:
        proc = subprocess.run(
            ["getconf", key], capture_output=True, text=True, timeout=15, check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    candidate = Path(proc.stdout.strip()).expanduser()
    return candidate if candidate.is_dir() else None


def cache_roots(home: Path) -> list[Path]:
    roots: list[Path] = [home / "Library" / "Caches"]
    darwin_cache = getconf_path("DARWIN_USER_CACHE_DIR")
    if darwin_cache:
        roots.append(darwin_cache)
    unique: list[Path] = []
    seen: set[str] = set()
    for item in roots:
        try:
            resolved = item.resolve(strict=True)
        except OSError:
            continue
        if str(resolved) not in seen:
            seen.add(str(resolved))
            unique.append(resolved)
    return unique


def add_large_item(path: Path, source: str, seen: set[tuple[int, int]]) -> ItemRecord | None:
    try:
        st = path.lstat()
    except OSError:
        return None
    if not statmod.S_ISREG(st.st_mode):
        return None
    identity = (st.st_dev, st.st_ino)
    if identity in seen:
        return None
    seen.add(identity)
    mount = find_mount_point(path)
    return ItemRecord(
        path=str(path),
        path_id=path_id(str(path)),
        item_kind="regular-file",
        logical_bytes=st.st_size,
        allocated_bytes=getattr(st, "st_blocks", 0) * 512,
        mtime_epoch=st.st_mtime,
        birthtime_epoch=getattr(st, "st_birthtime", None),
        device=st.st_dev,
        inode=st.st_ino,
        mount_point=str(mount) if mount else None,
        source=source,
        is_package=False,
    )


def spotlight_large_items(
    scopes: list[Path], minimum_bytes: int, raw_dir: Path, max_stream_bytes: int
) -> list[ItemRecord]:
    if not command_exists("mdfind"):
        return []
    records: list[ItemRecord] = []
    seen: set[tuple[int, int]] = set()
    query = f"kMDItemFSSize >= {minimum_bytes}"
    for scope in scopes:
        result = run_capture(
            raw_dir,
            f"mdfind-large-items-{scope}",
            ["mdfind", "-onlyin", str(scope), query],
            180,
            max_stream_bytes,
        )
        if result.exit_code != 0 or result.stdout_truncated:
            continue
        try:
            lines = (raw_dir / result.stdout_file).read_text(
                encoding="utf-8", errors="surrogateescape"
            ).splitlines()
        except OSError:
            continue
        for line in lines:
            record = add_large_item(Path(line), "spotlight-verified", seen)
            if record and record.logical_bytes >= minimum_bytes:
                records.append(record)
    return records


def deep_large_items(scopes: list[Path], minimum_bytes: int, protected: list[Path]) -> list[ItemRecord]:
    records: list[ItemRecord] = []
    seen: set[tuple[int, int]] = set()
    protected_strings = {str(item) for item in protected}
    for scope in scopes:
        try:
            root_stat = scope.lstat()
        except OSError:
            continue
        for current, dirs, files in os.walk(scope, topdown=True, followlinks=False):
            if current in protected_strings:
                dirs[:] = []
                continue
            try:
                current_stat = os.lstat(current)
            except OSError:
                dirs[:] = []
                continue
            if current_stat.st_dev != root_stat.st_dev:
                dirs[:] = []
                continue
            safe_dirs: list[str] = []
            for dirname in dirs:
                child = Path(current) / dirname
                try:
                    child_stat = child.lstat()
                except OSError:
                    continue
                if child_stat.st_dev != root_stat.st_dev or statmod.S_ISLNK(child_stat.st_mode):
                    continue
                if is_package_path(child):
                    continue
                safe_dirs.append(dirname)
            dirs[:] = safe_dirs
            for filename in files:
                path = Path(current) / filename
                try:
                    st = path.lstat()
                except OSError:
                    continue
                if st.st_dev != root_stat.st_dev or not statmod.S_ISREG(st.st_mode):
                    continue
                if st.st_size >= minimum_bytes:
                    record = add_large_item(path, "deep-filesystem-scan", seen)
                    if record:
                        records.append(record)
    return records


def read_command_text(raw_dir: Path, commands: list[CommandResult], name: str) -> str | None:
    result = next((item for item in commands if item.name == name), None)
    if result is None or result.exit_code != 0 or result.stdout_truncated:
        return None
    try:
        return (raw_dir / result.stdout_file).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def parse_df_text(value: str | None) -> dict[str, int | str] | None:
    if not value:
        return None
    lines = value.strip().splitlines()
    if len(lines) < 2:
        return None
    parts = lines[-1].split()
    if len(parts) < 6:
        return None
    try:
        return {
            "filesystem": parts[0],
            "capacity_bytes": int(parts[1]) * 1024,
            "used_bytes": int(parts[2]) * 1024,
            "available_bytes": int(parts[3]) * 1024,
            "mount_point": parts[-1],
        }
    except ValueError:
        return None


def parse_plist_text(value: str | None) -> dict[str, Any] | None:
    if not value:
        return None
    try:
        parsed = plistlib.loads(value.encode("utf-8", "surrogateescape"))
    except (ValueError, plistlib.InvalidFileException):
        return None
    return parsed if isinstance(parsed, dict) else None


def parse_json_text(value: str | None) -> dict[str, Any] | list[Any] | None:
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def get_by_key_fragment(mapping: dict[str, Any], fragment: str) -> Any:
    fragment = fragment.casefold()
    for key, value in mapping.items():
        if fragment in key.casefold():
            return value
    return None


def combine_volume_record(
    label: str,
    path: str,
    df_data: dict[str, Any] | None,
    diskutil_data: dict[str, Any] | None,
    foundation_data: dict[str, Any] | None,
) -> dict[str, Any]:
    foundation_data = foundation_data or {}
    diskutil_data = diskutil_data or {}
    return {
        "label": label,
        "path": path,
        "df": df_data,
        "device_identifier": diskutil_data.get("DeviceIdentifier"),
        "volume_name": diskutil_data.get("VolumeName"),
        "mount_point": diskutil_data.get("MountPoint") or (df_data or {}).get("mount_point"),
        "filesystem_type": diskutil_data.get("FilesystemType"),
        "apfs_container_reference": diskutil_data.get("APFSContainerReference"),
        "apfs_volume_group_id": diskutil_data.get("APFSVolumeGroupID"),
        "volume_uuid": diskutil_data.get("VolumeUUID") or get_by_key_fragment(foundation_data, "volumeuuid"),
        "read_only": diskutil_data.get("ReadOnlyVolume") if "ReadOnlyVolume" in diskutil_data else get_by_key_fragment(foundation_data, "volumeisreadonly"),
        "internal": diskutil_data.get("Internal") if "Internal" in diskutil_data else get_by_key_fragment(foundation_data, "volumeisinternal"),
        "total_capacity_bytes": get_by_key_fragment(foundation_data, "volumetotalcapacity"),
        "ordinary_available_bytes": get_by_key_fragment(foundation_data, "volumeavailablecapacitykey"),
        "important_usage_available_bytes": get_by_key_fragment(foundation_data, "availablecapacityforimportantusage"),
        "opportunistic_usage_available_bytes": get_by_key_fragment(foundation_data, "availablecapacityforopportunisticusage"),
        "foundation_probe_status": foundation_data.get("probe_status", "unavailable"),
    }


def collect_native_commands(
    raw_dir: Path,
    max_stream_bytes: int,
    helper_dir: Path,
    minimal_mode: bool,
) -> list[CommandResult]:
    data_path = Path("/System/Volumes/Data")
    commands: list[tuple[str, list[str], int]] = [
        ("date-utc", ["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], 15),
        ("sw-vers", ["sw_vers"], 15),
        ("uname-architecture", ["uname", "-m"], 15),
        ("df-root", ["df", "-kP", "/"], 30),
        ("diskutil-info-root", ["diskutil", "info", "-plist", "/"], 60),
        ("diskutil-list", ["diskutil", "list", "-plist"], 60),
        ("diskutil-apfs-list", ["diskutil", "apfs", "list", "-plist"], 90),
        ("diskutil-apfs-snapshots-root", ["diskutil", "apfs", "listSnapshots", "/"], 90),
        ("tmutil-local-snapshots", ["tmutil", "listlocalsnapshots", "/"], 90),
        ("mdutil-root-status", ["mdutil", "-s", "/"], 30),
        ("getconf-user-cache", ["getconf", "DARWIN_USER_CACHE_DIR"], 15),
        ("getconf-user-temp", ["getconf", "DARWIN_USER_TEMP_DIR"], 15),
    ]
    if data_path.exists():
        commands.extend(
            [
                ("df-data", ["df", "-kP", str(data_path)], 30),
                ("diskutil-info-data", ["diskutil", "info", "-plist", str(data_path)], 60),
                ("diskutil-apfs-snapshots-data", ["diskutil", "apfs", "listSnapshots", str(data_path)], 90),
                ("mdutil-data-status", ["mdutil", "-s", str(data_path)], 30),
            ]
        )
    if not minimal_mode:
        commands.extend(
            [
                ("system-profiler-storage", ["system_profiler", "-json", "-detailLevel", "mini", "SPStorageDataType"], 180),
                ("pmset-battery", ["pmset", "-g", "batt"], 30),
                ("pmset-thermal", ["pmset", "-g", "therm"], 30),
            ]
        )

    probe = helper_dir / "macos_resource_probe.swift"
    if command_exists("swift") and probe.is_file():
        paths = ["/"] + ([str(data_path)] if data_path.exists() else [])
        commands.append(("foundation-volume-capacity", ["swift", str(probe), "volume", *paths], 120))

    results: list[CommandResult] = []
    for name, argv, timeout in commands:
        if command_exists(argv[0]):
            results.append(run_capture(raw_dir, name, argv, timeout, max_stream_bytes))

    if minimal_mode:
        return results

    optional: list[tuple[str, list[str], int]] = []
    if command_exists("docker"):
        optional.extend(
            [
                ("docker-system-df-json", ["docker", "system", "df", "--format", "json"], 90),
                ("docker-system-df-verbose", ["docker", "system", "df", "-v"], 90),
                ("docker-containers-size", ["docker", "ps", "-a", "--size"], 90),
                ("docker-volumes", ["docker", "volume", "ls"], 60),
            ]
        )
    if command_exists("brew"):
        optional.extend(
            [
                ("homebrew-cache", ["brew", "--cache"], 60),
                ("homebrew-config", ["brew", "config"], 90),
                ("homebrew-cleanup-dry-run", ["brew", "cleanup", "-n"], 180),
                ("homebrew-autoremove-dry-run", ["brew", "autoremove", "--dry-run"], 120),
            ]
        )
    if command_exists("xcode-select"):
        optional.append(("xcode-select-path", ["xcode-select", "-p"], 30))
    if command_exists("xcrun"):
        optional.extend(
            [
                ("xcode-simctl-runtimes", ["xcrun", "simctl", "list", "runtimes"], 120),
                ("xcode-simctl-devices", ["xcrun", "simctl", "list", "devices"], 120),
            ]
        )
    if command_exists("npm"):
        optional.append(("npm-cache-path", ["npm", "config", "get", "cache"], 60))
    if command_exists("pnpm"):
        optional.append(("pnpm-store-path", ["pnpm", "store", "path"], 60))
    if command_exists("yarn"):
        optional.append(("yarn-cache-dir", ["yarn", "cache", "dir"], 60))
    if command_exists("uv"):
        optional.append(("uv-cache-dir", ["uv", "cache", "dir"], 60))
    if command_exists("python3"):
        optional.append(("pip-cache-dir", ["python3", "-m", "pip", "cache", "dir"], 60))

    for name, argv, timeout in optional:
        results.append(run_capture(raw_dir, name, argv, timeout, max_stream_bytes))
    return results


def foundation_items_probe(
    items: list[ItemRecord],
    raw_dir: Path,
    helper_dir: Path,
    max_stream_bytes: int,
) -> CommandResult | None:
    probe = helper_dir / "macos_resource_probe.swift"
    if not items or not command_exists("swift") or not probe.is_file():
        return None
    selected = items[:100]
    return run_capture(
        raw_dir,
        "foundation-large-item-metadata",
        ["swift", str(probe), "item", *[item.path for item in selected]],
        180,
        max_stream_bytes,
    )


def apply_foundation_item_metadata(
    items: list[ItemRecord], raw_dir: Path, result: CommandResult | None
) -> None:
    if result is None or result.exit_code != 0 or result.stdout_truncated:
        return
    try:
        payload = json.loads((raw_dir / result.stdout_file).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    by_path = {str(entry.get("path")): entry for entry in payload.get("items", []) if isinstance(entry, dict)}
    for item in items:
        entry = by_path.get(item.path)
        if not entry:
            continue
        item.cloud_probe_status = str(entry.get("probe_status", "unknown"))
        item.is_ubiquitous = get_by_key_fragment(entry, "isubiquitousitem")
        item.is_downloaded = get_by_key_fragment(entry, "ubiquitousitemisdownloaded")
        item.is_uploading = get_by_key_fragment(entry, "ubiquitousitemisuploading")
        item.has_unresolved_conflicts = get_by_key_fragment(entry, "hasunresolvedconflicts")
        status = get_by_key_fragment(entry, "ubiquitousitemdownloadingstatus")
        item.downloading_status = str(status) if status is not None else None
        allocated = get_by_key_fragment(entry, "totalfileallocatedsize")
        if isinstance(allocated, int) and allocated >= 0:
            item.allocated_bytes = allocated
        package = get_by_key_fragment(entry, "ispackage")
        if isinstance(package, bool):
            item.is_package = package


def parse_volumes(raw_dir: Path, commands: list[CommandResult]) -> list[dict[str, Any]]:
    root_df = parse_df_text(read_command_text(raw_dir, commands, "df-root"))
    data_df = parse_df_text(read_command_text(raw_dir, commands, "df-data"))
    root_diskutil = parse_plist_text(read_command_text(raw_dir, commands, "diskutil-info-root"))
    data_diskutil = parse_plist_text(read_command_text(raw_dir, commands, "diskutil-info-data"))
    foundation_payload = parse_json_text(read_command_text(raw_dir, commands, "foundation-volume-capacity"))
    foundation_by_path: dict[str, dict[str, Any]] = {}
    if isinstance(foundation_payload, dict):
        for item in foundation_payload.get("items", []):
            if isinstance(item, dict) and item.get("path"):
                foundation_by_path[str(item["path"])] = item
    volumes = [
        combine_volume_record("System/root view", "/", root_df, root_diskutil, foundation_by_path.get("/"))
    ]
    if Path("/System/Volumes/Data").exists():
        volumes.append(
            combine_volume_record(
                "Writable Data view",
                "/System/Volumes/Data",
                data_df,
                data_diskutil,
                foundation_by_path.get("/System/Volumes/Data"),
            )
        )
    return volumes


def load_baseline(path: Path | None) -> dict[str, int]:
    if path is None:
        return {}
    try:
        payload = json.loads(path.expanduser().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    result: dict[str, int] = {}
    for key in ("directories", "cache_candidates", "large_item_candidates", "large_file_candidates"):
        for item in payload.get(key, []):
            pid = item.get("path_id")
            size = item.get("allocated_bytes")
            if isinstance(pid, str) and isinstance(size, int):
                result[pid] = size
    return result


def apply_baseline(records: Iterable[DirectoryRecord | ItemRecord], baseline: dict[str, int]) -> None:
    for record in records:
        previous = baseline.get(record.path_id)
        current = record.allocated_bytes
        if previous is not None and isinstance(current, int):
            record.delta_bytes = current - previous


def device_summaries(scopes: list[Path], directories: list[DirectoryRecord]) -> list[dict[str, Any]]:
    by_device: dict[int, dict[str, Any]] = {}
    for scope in scopes:
        try:
            st = scope.stat()
            usage = shutil.disk_usage(scope)
        except OSError:
            continue
        mount = find_mount_point(scope)
        entry = by_device.setdefault(
            st.st_dev,
            {
                "device": st.st_dev,
                "mount_point": str(mount) if mount else None,
                "capacity_bytes": usage.total,
                "used_bytes": usage.used,
                "available_bytes": usage.free,
                "scopes": [],
                "measured_complete_bytes": 0,
                "partial_records": 0,
            },
        )
        entry["scopes"].append(str(scope))
    for record in directories:
        if record.device is None or record.device not in by_device:
            continue
        if record.du_complete and record.allocated_bytes is not None:
            by_device[record.device]["measured_complete_bytes"] += record.allocated_bytes
        else:
            by_device[record.device]["partial_records"] += 1
    for entry in by_device.values():
        entry["unattributed_or_outside_scopes_bytes"] = max(
            0, entry["used_bytes"] - entry["measured_complete_bytes"]
        )
        entry["accounting_semantics"] = (
            "used bytes minus complete measurements inside selected scope children; "
            "includes data outside scopes and measurement differences"
        )
    return list(by_device.values())


def human_bytes(value: int | float | None) -> str:
    if value is None:
        return "unknown"
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    size = float(value)
    for unit in units:
        if abs(size) < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{value} B"


def signed_bytes(value: int | None) -> str:
    if value is None:
        return "—"
    prefix = "+" if value > 0 else ""
    return prefix + human_bytes(value)


def iso_time(epoch: float | None) -> str:
    if epoch is None:
        return "unknown"
    return dt.datetime.fromtimestamp(epoch, dt.timezone.utc).replace(microsecond=0).isoformat()


def svg_bar_chart(rows: list[tuple[str, int]], width: int = 920) -> str:
    rows = [(label, value) for label, value in rows if value >= 0][:20]
    if not rows:
        return "<p>No measured data.</p>"
    max_value = max(value for _, value in rows) or 1
    row_h = 34
    label_w = 320
    chart_w = width - label_w - 145
    height = 30 + row_h * len(rows)
    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="Storage bar chart">']
    for index, (label, value) in enumerate(rows):
        y = 24 + index * row_h
        bar_w = max(1, int(chart_w * value / max_value))
        parts.append(f'<text x="0" y="{y + 15}" class="chart-label">{html.escape(label)}</text>')
        parts.append(f'<rect x="{label_w}" y="{y}" width="{bar_w}" height="20" rx="3" class="bar"/>')
        parts.append(f'<text x="{label_w + bar_w + 8}" y="{y + 15}" class="chart-value">{html.escape(human_bytes(value))}</text>')
    parts.append("</svg>")
    return "".join(parts)


def command_status(result: CommandResult) -> str:
    if result.timed_out:
        return "timeout"
    if result.exit_code == 0:
        suffix = " (truncated)" if result.stdout_truncated or result.stderr_truncated else ""
        return "ok" + suffix
    return f"exit {result.exit_code}" if result.exit_code is not None else "unavailable"


def bool_text(value: bool | None) -> str:
    if value is None:
        return "unknown"
    return "yes" if value else "no"


def render_html(
    metadata: dict[str, Any],
    volumes: list[dict[str, Any]],
    devices: list[dict[str, Any]],
    directories: list[DirectoryRecord],
    caches: list[DirectoryRecord],
    items: list[ItemRecord],
    commands: list[CommandResult],
    redact: bool,
) -> str:
    top_dirs = sorted(
        [item for item in directories if item.allocated_bytes is not None],
        key=lambda item: item.allocated_bytes or 0,
        reverse=True,
    )[:20]
    dir_chart = svg_bar_chart(
        [(display_path(item.path, redact), item.allocated_bytes or 0) for item in top_dirs]
    )

    volume_rows: list[str] = []
    capacity_charts: list[str] = []
    for volume in volumes:
        df_data = volume.get("df") or {}
        capacity_charts.append(
            f"<h3>{html.escape(str(volume['label']))}</h3>" + svg_bar_chart(
                [
                    ("Used (df)", int(df_data.get("used_bytes", 0))),
                    ("Available (df)", int(df_data.get("available_bytes", 0))),
                ]
            )
        )
        volume_rows.append(
            "<tr>"
            f"<td>{html.escape(str(volume.get('label')))}</td>"
            f"<td>{html.escape(str(volume.get('volume_name') or 'unknown'))}</td>"
            f"<td>{html.escape(str(volume.get('mount_point') or volume.get('path')))}</td>"
            f"<td>{html.escape(str(volume.get('device_identifier') or 'unknown'))}</td>"
            f"<td>{html.escape(human_bytes(df_data.get('used_bytes')))}</td>"
            f"<td>{html.escape(human_bytes(df_data.get('available_bytes')))}</td>"
            f"<td>{html.escape(human_bytes(volume.get('important_usage_available_bytes')))}</td>"
            f"<td>{html.escape(human_bytes(volume.get('opportunistic_usage_available_bytes')))}</td>"
            f"<td>{html.escape(bool_text(volume.get('read_only')))}</td>"
            "</tr>"
        )

    device_rows: list[str] = []
    for device in devices:
        device_rows.append(
            "<tr>"
            f"<td>{html.escape(str(device.get('device')))}</td>"
            f"<td>{html.escape(display_path(str(device.get('mount_point') or 'unknown'), redact))}</td>"
            f"<td>{html.escape(human_bytes(device.get('used_bytes')))}</td>"
            f"<td>{html.escape(human_bytes(device.get('measured_complete_bytes')))}</td>"
            f"<td>{html.escape(human_bytes(device.get('unattributed_or_outside_scopes_bytes')))}</td>"
            f"<td>{html.escape(str(device.get('partial_records')))}</td>"
            "</tr>"
        )

    cache_rows: list[str] = []
    for item in sorted(caches, key=lambda value: value.allocated_bytes or 0, reverse=True)[:60]:
        measurement = "complete" if item.du_complete and item.activity_scan_complete else "partial"
        cache_rows.append(
            "<tr>"
            f"<td>{html.escape(display_path(item.path, redact))}</td>"
            f"<td>{html.escape(human_bytes(item.allocated_bytes))}</td>"
            f"<td>{html.escape(signed_bytes(item.delta_bytes))}</td>"
            f"<td>{html.escape(iso_time(item.newest_content_mtime_epoch))}</td>"
            f"<td>{html.escape(item.activity_label)}</td>"
            f"<td>{html.escape(measurement)}</td>"
            f"<td>{html.escape(bool_text(item.is_package))}</td>"
            "<td>Candidate only; ownership and regeneration unproven</td>"
            "</tr>"
        )

    item_rows: list[str] = []
    for item in sorted(items, key=lambda value: value.allocated_bytes, reverse=True)[:60]:
        cloud = (
            f"ubiquitous={bool_text(item.is_ubiquitous)}, "
            f"downloaded={bool_text(item.is_downloaded)}, "
            f"uploading={bool_text(item.is_uploading)}, "
            f"conflicts={bool_text(item.has_unresolved_conflicts)}"
        )
        item_rows.append(
            "<tr>"
            f"<td>{html.escape(display_path(item.path, redact))}</td>"
            f"<td>{html.escape(human_bytes(item.logical_bytes))}</td>"
            f"<td>{html.escape(human_bytes(item.allocated_bytes))}</td>"
            f"<td>{html.escape(signed_bytes(item.delta_bytes))}</td>"
            f"<td>{html.escape(iso_time(item.mtime_epoch))}</td>"
            f"<td>{html.escape(item.source)}</td>"
            f"<td>{html.escape(cloud)}</td>"
            "</tr>"
        )

    command_rows: list[str] = []
    for item in commands:
        command_rows.append(
            "<tr>"
            f"<td>{html.escape(item.name)}</td>"
            f"<td>{html.escape(command_status(item))}</td>"
            f"<td><code>{html.escape(' '.join(item.argv))}</code></td>"
            f"<td>{html.escape(human_bytes(item.stdout_bytes))} / {html.escape(human_bytes(item.stderr_bytes))}</td>"
            f"<td><code>raw/{html.escape(item.stdout_file)}</code></td>"
            "</tr>"
        )

    partial_count = sum(1 for item in directories + caches if not item.du_complete or not item.activity_scan_complete)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>macOS Storage Audit v4</title>
<style>
:root {{ color-scheme: light dark; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
body {{ max-width: 1180px; margin: 0 auto; padding: 32px; line-height: 1.45; }}
h1, h2 {{ letter-spacing: -0.02em; }}
.notice {{ border: 2px solid currentColor; padding: 14px 16px; border-radius: 10px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(220px,1fr)); gap: 12px; }}
.card {{ border: 1px solid color-mix(in srgb, currentColor 25%, transparent); padding: 14px; border-radius: 10px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid color-mix(in srgb, currentColor 20%, transparent); vertical-align: top; }}
code {{ overflow-wrap: anywhere; }}
svg {{ width: 100%; min-height: 120px; }}
.bar {{ fill: currentColor; opacity: .72; }}
.chart-label, .chart-value {{ fill: currentColor; font-size: 13px; }}
.small {{ opacity: .75; font-size: .9rem; }}
</style>
</head>
<body>
<h1>macOS Storage Audit v4</h1>
<p class="notice"><strong>Read-only evidence.</strong> Size, activity, cloud residency, and tool reports are diagnostic signals. Nothing here authorizes deletion, pruning, snapshot removal, or emptying Trash.</p>
<div class="grid">
  <div class="card"><strong>Generated</strong><br>{html.escape(str(metadata['generated_at']))}</div>
  <div class="card"><strong>Mode</strong><br>{html.escape(str(metadata['audit_mode']))}</div>
  <div class="card"><strong>Scopes</strong><br>{len(metadata['scopes'])}</div>
  <div class="card"><strong>Partial measurements</strong><br>{partial_count}</div>
  <div class="card"><strong>Raw stream cap</strong><br>{html.escape(human_bytes(metadata['max_stream_bytes']))}</div>
</div>

<h2>Volume capacity views</h2>
<p class="small">System and Data views can belong to the same APFS volume group. Ordinary, important-usage, and opportunistic capacity are distinct, non-additive metrics and are not guaranteed reclaimable bytes.</p>
{''.join(capacity_charts)}
<table><thead><tr><th>View</th><th>Volume</th><th>Mount</th><th>Device</th><th>Used (df)</th><th>Available (df)</th><th>Important usage</th><th>Opportunistic</th><th>Read-only</th></tr></thead>
<tbody>{''.join(volume_rows)}</tbody></table>

<h2>Per-device attribution</h2>
<p class="small">“Unattributed/outside scopes” means filesystem used bytes minus complete measurements under selected scope children. It includes everything outside the scopes and measurement differences; it is not “system junk”.</p>
<table><thead><tr><th>Device</th><th>Mount</th><th>Used</th><th>Measured complete</th><th>Outside scopes/unattributed</th><th>Partial records</th></tr></thead>
<tbody>{''.join(device_rows) or '<tr><td colspan="6">No device summary.</td></tr>'}</tbody></table>

<h2>Largest measured directories</h2>
{dir_chart}
<p class="small">Only complete `du` measurements are suitable for accounting. APFS clones, snapshots, sparse files, hard links, package boundaries, and permissions still prevent an exact reclaim estimate.</p>

<h2>Cache candidates</h2>
<table><thead><tr><th>Path</th><th>Allocated</th><th>Delta</th><th>Newest observed activity</th><th>Activity</th><th>Measurement</th><th>Package</th><th>Status</th></tr></thead>
<tbody>{''.join(cache_rows) or '<tr><td colspan="8">No cache candidates measured.</td></tr>'}</tbody></table>

<h2>Large-item candidates</h2>
<table><thead><tr><th>Path</th><th>Logical</th><th>Allocated</th><th>Delta</th><th>Modified</th><th>Source</th><th>Cloud state</th></tr></thead>
<tbody>{''.join(item_rows) or '<tr><td colspan="7">No large items measured.</td></tr>'}</tbody></table>

<h2>Native command evidence</h2>
<table><thead><tr><th>Name</th><th>Status</th><th>Command</th><th>Original stdout/stderr</th><th>Output</th></tr></thead>
<tbody>{''.join(command_rows)}</tbody></table>

<h2>Required next step</h2>
<p>Resolve partial coverage, verify Spotlight and cloud-sync state, identify exact owners, and select candidates for a separate immutable cleanup manifest. Any cloud upload/conflict, package boundary, unknown ownership, or incomplete measurement remains R2/R3.</p>
</body></html>"""


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, dialect="excel-tab", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    path.chmod(0o600)


def sha256_manifest(output_dir: Path) -> None:
    lines: list[str] = []
    for path in sorted(output_dir.rglob("*")):
        if not path.is_file() or path.name == "SHA256SUMS.txt":
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(output_dir)}")
    write_private(output_dir / "SHA256SUMS.txt", "\n".join(lines) + "\n")


def existing_parent(path: Path) -> Path:
    current = path.expanduser().absolute()
    while not current.exists() and current.parent != current:
        current = current.parent
    return current


def main() -> int:
    args = parse_args()
    if platform.system() != "Darwin":
        print("ERROR: this audit helper must run on macOS (Darwin).", file=sys.stderr)
        return 2
    if (
        args.activity_file_limit < 0
        or args.inactive_days < 0
        or args.large_gib <= 0
        or args.max_raw_mib <= 0
        or args.low_space_mib < HARD_MIN_OUTPUT_MIB
    ):
        print("ERROR: invalid numeric arguments.", file=sys.stderr)
        return 2

    os.umask(0o077)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = (args.output or Path.cwd() / f"macos-storage-audit-{stamp}").expanduser().absolute()
    parent = existing_parent(output_dir)
    try:
        parent_free = shutil.disk_usage(parent).free
    except OSError as exc:
        print(f"ERROR: cannot inspect output filesystem: {exc}", file=sys.stderr)
        return 2

    hard_min = HARD_MIN_OUTPUT_MIB * 1024**2
    low_threshold = args.low_space_mib * 1024**2
    if parent_free < hard_min:
        print(
            "ERROR: insufficient room for a trustworthy report bundle. Choose an external output "
            "path, for example --output /Volumes/<external>/macos-storage-audit.",
            file=sys.stderr,
        )
        return 3
    low_space_mode = parent_free < low_threshold
    max_stream_bytes = int(args.max_raw_mib * 1024**2)
    if low_space_mode:
        max_stream_bytes = min(max_stream_bytes, 256 * 1024)
        args.deep_activity = False
        args.deep_large_files = False

    output_dir.mkdir(parents=True, exist_ok=False)
    output_dir.chmod(0o700)
    raw_dir = output_dir / "raw"
    raw_dir.mkdir(mode=0o700)

    home = Path.home().resolve()
    scopes, scope_exclusions = normalize_scopes(args.scope, home, [output_dir])
    protected_paths = [output_dir]
    generated_at = now_utc()
    threshold = dt.datetime.now(dt.timezone.utc).timestamp() - args.inactive_days * 86400
    helper_dir = Path(__file__).resolve().parent

    commands = collect_native_commands(
        raw_dir, max_stream_bytes, helper_dir, minimal_mode=low_space_mode
    )
    volumes = parse_volumes(raw_dir, commands)

    directories: list[DirectoryRecord] = []
    for scope in scopes:
        for child in iter_children(scope, protected_paths):
            directories.append(
                directory_record(
                    scope, child, "scope-child", args.deep_activity,
                    args.activity_file_limit, threshold,
                )
            )

    caches: list[DirectoryRecord] = []
    for root in cache_roots(home):
        if any(root == protected or is_within(root, protected) for protected in protected_paths):
            continue
        for child in iter_children(root, protected_paths):
            caches.append(
                directory_record(
                    root, child, "cache-candidate", args.deep_activity,
                    args.activity_file_limit, threshold,
                )
            )

    minimum_bytes = int(args.large_gib * 1024**3)
    items: list[ItemRecord] = []
    if not args.skip_spotlight and not low_space_mode:
        items.extend(spotlight_large_items(scopes, minimum_bytes, raw_dir, max_stream_bytes))
    if args.deep_large_files and not low_space_mode:
        deep = deep_large_items(scopes, minimum_bytes, protected_paths)
        identities = {(item.device, item.inode) for item in items}
        items.extend([item for item in deep if (item.device, item.inode) not in identities])

    item_probe = foundation_items_probe(items, raw_dir, helper_dir, max_stream_bytes)
    if item_probe is not None:
        commands.append(item_probe)
        apply_foundation_item_metadata(items, raw_dir, item_probe)

    baseline = load_baseline(args.baseline)
    apply_baseline(directories, baseline)
    apply_baseline(caches, baseline)
    apply_baseline(items, baseline)
    devices = device_summaries(scopes, directories)

    tcc_or_permission_limited = any(
        item.permission_errors > 0 or not item.du_complete for item in directories + caches
    )
    spotlight_status = [
        {"name": item.name, "status": command_status(item)}
        for item in commands if item.name.startswith("mdutil-")
    ]
    metadata = {
        "version": VERSION,
        "generated_at": generated_at,
        "host": platform.node(),
        "macos_release": platform.mac_ver()[0],
        "architecture": platform.machine(),
        "scopes": [display_path(str(scope), args.redact_paths) for scope in scopes],
        "scope_exclusions": scope_exclusions,
        "deep_activity": args.deep_activity,
        "activity_file_limit": args.activity_file_limit,
        "inactive_days": args.inactive_days,
        "large_gib": args.large_gib,
        "redacted": args.redact_paths,
        "audit_mode": "minimal-low-space" if low_space_mode else "standard-read-only",
        "output_parent_free_bytes_at_start": parent_free,
        "max_stream_bytes": max_stream_bytes,
        "tcc_or_permission_limited": tcc_or_permission_limited,
        "spotlight_status": spotlight_status,
        "baseline_used": bool(baseline),
        "protected_evidence_path": display_path(str(output_dir), args.redact_paths),
        "caveats": [
            "Read-only inventory; no target is deletion-approved.",
            "System and Data views may share one APFS container and must not be added.",
            "Foundation ordinary, important-usage, and opportunistic capacity values are non-additive and not reclaim guarantees.",
            "Incomplete du/TCC/Spotlight coverage lowers confidence and remains visible.",
            "Directory allocation, logical size, APFS sharing/clones, snapshots, cloud placeholders, and reclaimable bytes are not equivalent.",
            "Cloud uploading, conflicts, or unknown provider state blocks eviction/deletion recommendations.",
            "Package directories are atomic boundaries by default.",
            "Raw evidence can contain sensitive local paths and must remain private.",
        ],
    }

    structured = {
        "metadata": metadata,
        "volumes": volumes,
        "device_summaries": devices,
        "directories": [
            {
                **dataclasses.asdict(item),
                "path": display_path(item.path, args.redact_paths),
                "scope": display_path(item.scope, args.redact_paths),
                "mount_point": display_path(item.mount_point, args.redact_paths) if item.mount_point else None,
                "mtime": iso_time(item.mtime_epoch),
                "birthtime": iso_time(item.birthtime_epoch),
                "newest_content_mtime": iso_time(item.newest_content_mtime_epoch),
            }
            for item in directories
        ],
        "cache_candidates": [
            {
                **dataclasses.asdict(item),
                "path": display_path(item.path, args.redact_paths),
                "scope": display_path(item.scope, args.redact_paths),
                "mount_point": display_path(item.mount_point, args.redact_paths) if item.mount_point else None,
                "mtime": iso_time(item.mtime_epoch),
                "birthtime": iso_time(item.birthtime_epoch),
                "newest_content_mtime": iso_time(item.newest_content_mtime_epoch),
                "status": "candidate-only-not-approved",
            }
            for item in caches
        ],
        "large_item_candidates": [
            {
                **dataclasses.asdict(item),
                "path": display_path(item.path, args.redact_paths),
                "mount_point": display_path(item.mount_point, args.redact_paths) if item.mount_point else None,
                "mtime": iso_time(item.mtime_epoch),
                "birthtime": iso_time(item.birthtime_epoch),
                "status": "candidate-only-not-approved",
            }
            for item in items
        ],
        "commands": [dataclasses.asdict(item) for item in commands],
    }
    write_private(output_dir / "summary.json", json.dumps(structured, indent=2, ensure_ascii=False) + "\n")
    write_private(
        output_dir / "report.html",
        render_html(metadata, volumes, devices, directories, caches, items, commands, args.redact_paths),
    )

    write_tsv(
        output_dir / "directory-sizes.tsv",
        ["path_id", "scope", "path", "allocated_bytes", "delta_bytes", "device", "mount_point", "du_complete", "activity_label", "confidence"],
        [dataclasses.asdict(item) for item in directories],
    )
    write_tsv(
        output_dir / "cache-candidates.tsv",
        ["path_id", "scope", "path", "allocated_bytes", "delta_bytes", "newest_content_mtime_epoch", "du_complete", "activity_scan_complete", "is_package", "activity_label", "confidence"],
        [dataclasses.asdict(item) for item in caches],
    )
    write_tsv(
        output_dir / "large-items.tsv",
        ["path_id", "path", "item_kind", "logical_bytes", "allocated_bytes", "delta_bytes", "source", "is_ubiquitous", "is_downloaded", "is_uploading", "has_unresolved_conflicts", "downloading_status"],
        [dataclasses.asdict(item) for item in items],
    )
    sha256_manifest(output_dir)

    print(f"Read-only storage audit written to: {output_dir}")
    print(f"Open locally: {output_dir / 'report.html'}")
    if low_space_mode:
        print("NOTICE: minimal low-space mode was enforced; deep and optional scans were skipped.")
        print("For fuller evidence, rerun with --output on an external volume.")
    print("No cleanup operation was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
