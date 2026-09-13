import importlib.util
import tempfile
import unittest
import sys
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "macos_storage_audit.py"
spec = importlib.util.spec_from_file_location("audit", SCRIPT)
audit = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = audit
spec.loader.exec_module(audit)


class AuditLogicTests(unittest.TestCase):
    def test_nested_scopes_are_deduplicated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            child = root / "child"
            child.mkdir()
            scopes, excluded = audit.normalize_scopes([root, child], root, [])
            self.assertEqual(scopes, [root.resolve()])
            self.assertTrue(any("nested" in item["reason"] for item in excluded))

    def test_parent_scope_supersedes_existing_child(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            child = root / "child"
            child.mkdir()
            scopes, excluded = audit.normalize_scopes([child, root], root, [])
            self.assertEqual(scopes, [root.resolve()])
            self.assertTrue(any("superseded" in item["reason"] for item in excluded))

    def test_partial_du_forces_low_confidence(self):
        label, confidence = audit.activity_label(
            newest_epoch=1,
            activity_complete=True,
            du_complete=False,
            threshold_epoch=2,
            deep_enabled=True,
        )
        self.assertEqual(label, "measurement-partial")
        self.assertEqual(confidence, "low")

    def test_package_suffixes_are_atomic(self):
        self.assertTrue(audit.is_package_path(Path("Library.photoslibrary")))
        self.assertTrue(audit.is_package_path(Path("Disk.sparsebundle")))
        self.assertFalse(audit.is_package_path(Path("ordinary-folder")))

    def test_raw_output_is_bounded_and_marked(self):
        text, truncated, original = audit.truncate_text("x" * 100, 50)
        self.assertTrue(truncated)
        self.assertEqual(original, 100)
        self.assertIn("OUTPUT TRUNCATED", text)

    def test_path_id_is_stable_without_disclosing_path(self):
        first = audit.path_id("/Users/example/secret")
        second = audit.path_id("/Users/example/secret")
        self.assertEqual(first, second)
        self.assertNotIn("secret", first)

    def test_df_parser_keeps_mount_separate(self):
        parsed = audit.parse_df_text(
            "Filesystem 1024-blocks Used Available Capacity Mounted on\n/dev/test 100 60 40 60% /\n"
        )
        self.assertEqual(parsed["used_bytes"], 60 * 1024)
        self.assertEqual(parsed["mount_point"], "/")

    def test_device_summaries_do_not_mix_devices(self):
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            record = audit.DirectoryRecord(
                scope=str(scope), path=str(scope / "x"), path_id="x",
                allocated_bytes=1024, logical_bytes=None, mtime_epoch=None,
                birthtime_epoch=None, newest_content_mtime_epoch=None,
                activity_files_scanned=0, activity_scan_complete=True,
                permission_errors=0, device=scope.stat().st_dev, inode=1,
                mount_point=str(audit.find_mount_point(scope)), is_symlink=False,
                is_package=False, role="scope-child", activity_label="recent",
                confidence="medium", du_exit_code=0, du_timed_out=False,
                du_stderr_bytes=0, du_complete=True,
            )
            summaries = audit.device_summaries([scope], [record])
            self.assertEqual(len(summaries), 1)
            self.assertEqual(summaries[0]["measured_complete_bytes"], 1024)

    def test_baseline_delta_uses_path_fingerprint(self):
        item = audit.ItemRecord(
            path="/x", path_id="abc", item_kind="regular-file",
            logical_bytes=20, allocated_bytes=15, mtime_epoch=0,
            birthtime_epoch=None, device=1, inode=2, mount_point="/",
            source="test", is_package=False,
        )
        audit.apply_baseline([item], {"abc": 10})
        self.assertEqual(item.delta_bytes, 5)


    def test_symlink_scope_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "target"
            target.mkdir()
            link = root / "link"
            link.symlink_to(target, target_is_directory=True)
            scopes, excluded = audit.normalize_scopes([link], root, [])
            self.assertEqual(scopes, [])
            self.assertTrue(any("symlink" in item["reason"] for item in excluded))

    def test_protected_nested_report_excludes_containing_child(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            child = root / "Developer"
            report = child / "audit"
            report.mkdir(parents=True)
            visible = root / "Documents"
            visible.mkdir()
            children = list(audit.iter_children(root, [report]))
            self.assertNotIn(child, children)
            self.assertIn(visible, children)

    def test_volume_capacity_metrics_remain_separate(self):
        record = audit.combine_volume_record(
            "Data", "/System/Volumes/Data",
            {"used_bytes": 1, "available_bytes": 2}, {},
            {
                "NSURLVolumeAvailableCapacityKey": 2,
                "NSURLVolumeAvailableCapacityForImportantUsageKey": 3,
                "NSURLVolumeAvailableCapacityForOpportunisticUsageKey": 4,
            },
        )
        self.assertEqual(record["ordinary_available_bytes"], 2)
        self.assertEqual(record["important_usage_available_bytes"], 3)
        self.assertEqual(record["opportunistic_usage_available_bytes"], 4)

    def test_cloud_key_fragment_lookup_is_case_insensitive(self):
        mapping = {"NSURLUbiquitousItemIsUploadingKey": True}
        self.assertTrue(audit.get_by_key_fragment(mapping, "isuploading"))

    def test_iter_children_captures_loose_root_files(self):
        # P4 regression: du -d 1 hides loose files at a dir root; the helper's
        # iter_children must surface root-level files (via os.scandir), not only
        # subdirectories. Proves the script already handles loose files, so the
        # P4 fix is prose-only (Stage 2), not a code change.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "loose1.bin").write_bytes(b"x" * 1024)
            (root / "loose2.bin").write_bytes(b"x" * 512)
            (root / "subdir").mkdir()
            (root / "subdir" / "inside.bin").write_bytes(b"x" * 2048)
            children = list(audit.iter_children(root))
            names = sorted(c.name for c in children)
            self.assertIn("loose1.bin", names)
            self.assertIn("loose2.bin", names)
            self.assertIn("subdir", names)


if __name__ == "__main__":
    unittest.main()
