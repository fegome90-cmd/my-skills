#!/usr/bin/env swift
import Foundation

#if os(macOS)

func normalize(_ value: Any) -> Any {
    if let date = value as? Date {
        return date.timeIntervalSince1970
    }
    if let url = value as? URL {
        return url.path
    }
    if let error = value as? NSError {
        return [
            "domain": error.domain,
            "code": error.code,
            "description": error.localizedDescription
        ] as [String : Any]
    }
    if value is NSNull || value is NSString || value is NSNumber {
        return value
    }
    return String(describing: value)
}

func probe(_ path: String, keys: Set<URLResourceKey>) -> [String: Any] {
    let url = URL(fileURLWithPath: path)
    var result: [String: Any] = [
        "path": url.path,
        "path_id": String(url.path.hashValue)
    ]
    do {
        let values = try url.resourceValues(forKeys: keys)
        for (key, value) in values.allValues {
            result[key.rawValue] = normalize(value)
        }
        result["probe_status"] = "ok"
    } catch {
        let nsError = error as NSError
        result["probe_status"] = "error"
        result["probe_error"] = [
            "domain": nsError.domain,
            "code": nsError.code,
            "description": nsError.localizedDescription
        ]
    }
    return result
}

let args = Array(CommandLine.arguments.dropFirst())
guard args.count >= 2 else {
    fputs("usage: macos_resource_probe.swift <volume|item> <path>...\n", stderr)
    exit(2)
}

let mode = args[0]
let paths = Array(args.dropFirst())
let volumeKeys: Set<URLResourceKey> = [
    .volumeNameKey,
    .volumeUUIDStringKey,
    .volumeTotalCapacityKey,
    .volumeAvailableCapacityKey,
    .volumeAvailableCapacityForImportantUsageKey,
    .volumeAvailableCapacityForOpportunisticUsageKey,
    .volumeIsLocalKey,
    .volumeIsInternalKey,
    .volumeIsReadOnlyKey,
    .volumeIsRemovableKey,
    .volumeIsEjectableKey
]
let itemKeys: Set<URLResourceKey> = [
    .nameKey,
    .fileSizeKey,
    .fileAllocatedSizeKey,
    .totalFileSizeKey,
    .totalFileAllocatedSizeKey,
    .creationDateKey,
    .contentModificationDateKey,
    .isRegularFileKey,
    .isDirectoryKey,
    .isSymbolicLinkKey,
    .isPackageKey,
    .isUbiquitousItemKey,
    .ubiquitousItemDownloadingStatusKey,
    .ubiquitousItemIsUploadingKey,
    .ubiquitousItemUploadingErrorKey,
    .ubiquitousItemHasUnresolvedConflictsKey
]

let keys: Set<URLResourceKey>
switch mode {
case "volume": keys = volumeKeys
case "item": keys = itemKeys
default:
    fputs("invalid mode: \(mode)\n", stderr)
    exit(2)
}

let payload: [String: Any] = [
    "mode": mode,
    "generated_at": ISO8601DateFormatter().string(from: Date()),
    "items": paths.map { probe($0, keys: keys) }
]
let data = try JSONSerialization.data(withJSONObject: payload, options: [.prettyPrinted, .sortedKeys])
FileHandle.standardOutput.write(data)
FileHandle.standardOutput.write("\n".data(using: .utf8)!)

#else
fputs("macos_resource_probe.swift requires macOS\n", stderr)
exit(2)
#endif
