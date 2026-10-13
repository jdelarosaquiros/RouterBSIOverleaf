"""Offline, disposable publishing-cleanup contract tests (no source generators)."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("publishing_cleanup.py")


class PublishingCleanupTest(unittest.TestCase):
    def test_cli_archives_and_preserves_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "figs/example"
            folder.mkdir(parents=True)
            (root / "tables").mkdir()
            original = '{\n  "reportable": false,\n  "score": 0.75,\n  "source": "raw/results.csv",\n  "sha256": "' + 'a' * 64 + '",\n  "nested": {"analysis_only": true, "count": 748}\n}\n'
            (folder / "selection.json").write_text(original)
            (folder / "description.text").write_text("Analysis-only (non-reportable or unknown source provenance). No uncertainty is estimated.\n")
            (folder / "selected_data.csv").write_text("score\n0.75\n")
            (folder / "preview.pdf").write_bytes(b"fixture-preview")
            record = root / ".wisc/revisions/test/cleanup.json"
            backup = root / ".wisc/revisions/test/backup"
            backup.mkdir(parents=True)
            def run(mode):
                return subprocess.run([sys.executable, "-B", str(SCRIPT), mode, "--root", str(root), "--record", str(record), "--backup", str(backup)], capture_output=True, text=True)
            result = run("plan")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((folder / "selection.json").read_text(), original)
            result = run("apply")
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads((folder / "selection.json").read_text())
            self.assertEqual(data, {"score": 0.75, "source": "raw/results.csv", "sha256": 'a' * 64, "nested": {"count": 748}})
            self.assertEqual((folder / "description.text").read_text(), "No uncertainty is estimated.\n")
            self.assertEqual((folder / "selected_data.csv").read_text(), "score\n0.75\n")
            self.assertEqual((folder / "preview.pdf").read_bytes(), b"fixture-preview")
            self.assertIn(original, [p.read_text() for p in backup.rglob("selection.json")])
            self.assertEqual(run("verify").returncode, 0)
            self.assertEqual(run("apply").returncode, 0)
            (folder / "selected_data.csv").write_text("score\n0.76\n")
            self.assertNotEqual(run("verify").returncode, 0)

    def test_explicit_preview_refresh_exception_is_verify_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "figs").mkdir()
            folder = root / "tables/retrieval_and_reranking_performance"
            folder.mkdir(parents=True)
            (folder / "preview.pdf").write_bytes(b"before")
            (folder / "table.tex").write_text("Analysis-only. Uncertainty is unknown.\n")
            backup = root / ".wisc/revisions/test/backup"
            backup.mkdir(parents=True)
            record = backup.parent / "plan.json"
            def run(mode, *extra):
                return subprocess.run([sys.executable, "-B", str(SCRIPT), mode, "--root", str(root), "--record", str(record), "--backup", str(backup), *extra], capture_output=True, text=True)
            self.assertEqual(run("plan").returncode, 0)
            self.assertEqual(run("apply").returncode, 0)
            (folder / "preview.pdf").write_bytes(b"parent-refresh")
            self.assertNotEqual(run("verify").returncode, 0)
            result = run("verify", "--allow-preview-refresh")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotEqual(run("apply", "--allow-preview-refresh").returncode, 0)
            (folder / "table.tex").write_text("Changed metric 0.99\n")
            self.assertNotEqual(run("verify", "--allow-preview-refresh").returncode, 0)

    def test_drift_and_unknown_wording_fail_before_writes(self):
        for mutation in ("caption", "csv", "unknown", "numeric_flag", "archive"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "tables").mkdir()
                folder = root / "figs/example"
                folder.mkdir(parents=True)
                target = folder / "description.text"
                original = "Analysis-only. No uncertainty is estimated.\n"
                target.write_text(original)
                csv = folder / "source.csv"
                csv.write_text("score\n0.75\n")
                backup = root / ".wisc/revisions/test/backup"
                backup.mkdir(parents=True)
                record = backup.parent / "plan.json"
                def run(mode):
                    return subprocess.run([sys.executable, "-B", str(SCRIPT), mode, "--root", str(root), "--record", str(record), "--backup", str(backup)], capture_output=True, text=True)
                if mutation == "unknown":
                    target.write_text("An unreviewed noncanonical warning.\n")
                    self.assertNotEqual(run("plan").returncode, 0)
                    self.assertFalse(record.exists())
                    continue
                if mutation == "numeric_flag":
                    (folder / "selection.json").write_text('{"analysis_only": 748}')
                    self.assertNotEqual(run("plan").returncode, 0)
                    self.assertFalse(record.exists())
                    continue
                self.assertEqual(run("plan").returncode, 0)
                if mutation == "caption":
                    target.write_text(original + "Concurrent edit.\n")
                elif mutation == "csv":
                    csv.write_text("score\n0.99\n")
                else:
                    archive = Path(json.loads(record.read_text())["files"][0]["backup"])
                    archive.parent.mkdir(parents=True)
                    archive.write_text("preexisting unrelated bytes")
                before = target.read_bytes()
                self.assertNotEqual(run("apply").returncode, 0)
                self.assertEqual(target.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
