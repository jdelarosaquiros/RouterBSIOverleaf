# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib==3.10.8"]
# ///
"""Focused offline tests; run with uv run --script test_generate.py -v."""
import csv
import copy
import hashlib
import json
import tempfile
import importlib.util
import math
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / "BayesGSI/tables/routing_performance_by_iteration_std_all_splits/results.csv"
METHODS = ["Both Enabled", "Both Disabled", "Only MBR", "Only Gate"]


def load_generator():
    spec = importlib.util.spec_from_file_location("ndcg1_generator", HERE / "generate.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SelectionTests(unittest.TestCase):
    def test_exact_source_selection_and_population_std(self):
        self.assertTrue((HERE / "generate.py").is_file(), "standalone generator is missing")
        generator = load_generator()
        with SOURCE.open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        points = generator.select_rows(rows)
        expected = {(r["Method"], r["Iteration"]): r for r in rows
                    if r["Model"] == "Qwen3.5 4B" and r["Retriever"] == "SkillSight"
                    and r["Split"] == "test" and r["Dataset"] == "Average"
                    and r["Iteration"] != "final"}
        self.assertEqual(len(points), 44)
        self.assertEqual([(p["Method"], p["Iteration"]) for p in points],
                         [(m, i) for m in METHODS for i in ["initial", *map(str, range(1, 11))]])
        for point in points:
            source = expected[point["Method"], point["Iteration"]]
            for field in ["Model", "Retriever", "Method", "Split", "Evaluation", "Dataset",
                          "n_tasks", "Iteration", "n_runs", "Hit@1_mean", "Hit@1_variance"]:
                self.assertEqual(point[field], source[field])
            self.assertEqual(float(point["Hit1_std"]), math.sqrt(float(source["Hit@1_variance"])))
            self.assertEqual(point["x"], 0 if source["Iteration"] == "initial" else int(source["Iteration"]))


    def test_invalid_selections_fail_closed(self):
        generator = load_generator()
        with SOURCE.open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        good = [r for r in rows if all(r[k] == v for k, v in generator.IDENTITY.items())
                and r["Iteration"] != "final"]
        cases = {"missing_point": good[1:], "duplicate_point": good + [good[0].copy()]}
        for field, bad_values in {
            "Hit@1_mean": ["nan", "inf", "-0.01", "1.01", "", "no"],
            "Hit@1_variance": ["-0.000001", "nan", "inf", "0.26", "", "no"],
            "n_runs": ["2", "4", "3.0"], "n_tasks": ["747", "749", "748.0"],
            "Split": ["train", "validation"], "Evaluation": ["accepted", "prequential"],
            "Iteration": ["0", "01", "11"], "Method": ["unknown"],
            "Model": ["other"], "Retriever": ["other"], "Dataset": ["other"],
        }.items():
            for value in bad_values:
                mutated = [r.copy() for r in good]
                mutated[0][field] = value
                cases[f"{field}={value}"] = mutated
        wrong_stage = [r.copy() for r in good]
        wrong_stage[1]["Evaluation"] = "snapshot"
        cases["numbered_snapshot"] = wrong_stage
        for name, changed in cases.items():
            with self.subTest(case=name), self.assertRaises(ValueError):
                generator.select_rows(changed)


class ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.generator = load_generator()

    def test_source_integrity_and_manifest_failures(self):
        self.assertTrue(hasattr(self.generator, "load_source"), "missing source integrity validation")
        points, provenance = self.generator.load_source()
        self.assertEqual(len(points), 44)
        self.assertEqual(provenance["source_sha256"], hashlib.sha256(SOURCE.read_bytes()).hexdigest())
        source_manifest = SOURCE.with_name("manifest.json")
        self.assertEqual(provenance["source_manifest_sha256"], hashlib.sha256(source_manifest.read_bytes()).hexdigest())
        self.assertTrue(provenance["diagnostic_only"])
        self.assertFalse(provenance["reportable"])
        original = json.loads(source_manifest.read_text())
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            fixture = Path(tmp)
            csv_path = fixture / "results.csv"
            manifest_path = fixture / "manifest.json"
            csv_path.write_bytes(SOURCE.read_bytes())
            cases = []
            for key, value in [("sha256", "0" * 64), ("bytes", 1)]:
                changed = copy.deepcopy(original)
                changed["output"][key] = value
                cases.append(changed)
            for key, value in [("row_count", 44), ("diagnostic_only", False)]:
                changed = copy.deepcopy(original)
                changed[key] = value
                cases.append(changed)
            changed = copy.deepcopy(original)
            changed["runs"].pop()
            cases.append(changed)
            changed = copy.deepcopy(original)
            changed["runs"][1] = changed["runs"][0]
            cases.append(changed)
            for mutation in ["split", "iterations", "reportable", "completion"]:
                changed = copy.deepcopy(original)
                run = changed["runs"][0]
                if mutation == "split":
                    run["split_sizes"]["test"] = 747
                elif mutation == "iterations":
                    run["iterations"].pop()
                elif mutation == "reportable":
                    run["completion"]["reportable"] = True
                else:
                    del run["completion"]
                cases.append(changed)
            for index, changed in enumerate(cases):
                manifest_path.write_text(json.dumps(changed))
                with self.subTest(manifest_case=index), self.assertRaises(ValueError):
                    self.generator.load_source(csv_path, manifest_path)
            manifest_path.write_text(json.dumps(original))
            csv_path.write_bytes(SOURCE.read_bytes() + b"\n")
            with self.assertRaises(ValueError):
                self.generator.load_source(csv_path, manifest_path)

    def test_actual_lines_bands_styles_and_axis(self):
        self.assertTrue(hasattr(self.generator, "build_figure"), "missing nDCG@1 renderer")
        points, _ = self.generator.load_source()
        fig, ax = self.generator.build_figure(points)
        try:
            fig.canvas.draw()
            self.assertEqual(len(fig.axes), 1)
            self.assertEqual(len(ax.lines), 4)
            self.assertEqual(len(ax.collections), 4)
            self.assertEqual(ax.get_ylabel(), "nDCG@1")
            self.assertEqual(ax.get_xlabel(), "Iteration (0 = initial)")
            styles = [("#009E73", "D", "-."), ("#7A7A7A", "^", ":"),
                      ("#0072B2", "o", "-"), ("#D55E00", "s", "--")]
            for method, line, band, style in zip(METHODS, ax.lines, ax.collections, styles):
                rows = [p for p in points if p["Method"] == method]
                self.assertEqual(list(line.get_xdata()), list(range(11)))
                self.assertEqual(list(line.get_ydata()), [float(r["Hit@1_mean"]) for r in rows])
                self.assertEqual((line.get_color(), line.get_marker(), line.get_linestyle()), style)
                self.assertEqual(line.get_label(), method)
                self.assertEqual(band.get_alpha(), .13)
                vertices = band.get_paths()[0].vertices
                for p in rows:
                    ys = [float(y) for x, y in vertices if x == p["x"]]
                    lower = float(p["Hit@1_mean"]) - p["Hit1_std"]
                    upper = float(p["Hit@1_mean"]) + p["Hit1_std"]
                    self.assertEqual(min(ys), lower)
                    self.assertEqual(max(ys), upper)
                    self.assertLessEqual(ax.get_ylim()[0], lower)
                    self.assertGreaterEqual(ax.get_ylim()[1], upper)
        finally:
            import matplotlib.pyplot as plt
            plt.close(fig)

    def test_generated_outputs_hashes_and_fail_closed_publication(self):
        self.assertTrue(hasattr(self.generator, "generate"), "missing artifact publication")
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            out = Path(tmp)
            manifest = self.generator.generate(output=out)
            names = {"preview.pdf", "preview.png", "selected_data.csv", "selection_manifest.json",
                     "description.text", "provenance.text", "table.tex"}
            self.assertEqual({p.name for p in out.iterdir()}, names)
            self.assertEqual(manifest["artifact"], "mbr_replay_test_ndcg@1_std")
            self.assertEqual(manifest["selected_row_count"], 44)
            self.assertEqual(manifest["metric"], "Hit@1")
            self.assertEqual(manifest["display_metric"], "nDCG@1")
            self.assertEqual(json.loads((out / "selection_manifest.json").read_text()), manifest)
            for name, digest in manifest["output_sha256"].items():
                self.assertEqual(hashlib.sha256((out / name).read_bytes()).hexdigest(), digest)
            self.assertTrue((out / "preview.pdf").read_bytes().startswith(b"%PDF-"))
            self.assertTrue((out / "preview.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))
            with (out / "selected_data.csv").open(newline="") as stream:
                saved = list(csv.DictReader(stream))
            expected, _ = self.generator.load_source()
            self.assertEqual(len(saved), 44)
            for row, point in zip(saved, expected):
                for key, value in point.items():
                    self.assertEqual(row[key], str(value))
            wrapper = (out / "table.tex").read_text()
            self.assertIn("{figs/mbr_replay_test_ndcg@1_std/preview.pdf}", wrapper)
            self.assertIn("{fig:mbr_replay_test_ndcg@1_std}", wrapper)
            self.assertIn("{figs/mbr_replay_test_ndcg@1_std/description.text}", wrapper)
            caption = (out / "description.text").read_text()
            expected_caption = (
                "Routing performance with MBR replay and held-out validation gating enabled or disabled. "
                "Lines show task-weighted test nDCG@1 (Hit@1) averaged across three runs; "
                "shaded bands indicate one population standard deviation. "
                "Iteration 0 denotes initialization. Analysis-only: source runs remain non-reportable."
            )
            self.assertEqual(self.generator.CAPTION, expected_caption)
            self.assertEqual(caption, expected_caption + "\n")
            self.assertEqual((HERE / "description.text").read_text(), caption)
            self.assertTrue(manifest["diagnostic_only"])
            self.assertFalse(manifest["reportable"])
            provenance = (out / "provenance.text").read_text()
            self.assertEqual((HERE / "provenance.text").read_text(), provenance)
            for required in [
                "Hit@1 displayed as nDCG@1 (equal under binary relevance)",
                "Coverage: initial/snapshot at x=0, then 1--10/accepted; final snapshots excluded.",
                "not temporal variation, task-level dispersion, a standard error, or a confidence interval.",
                "diagnostic_only=true; reportable=false; completed_noncanonical.",
                "Analysis-only, non-reportable: this rendering does not establish publication eligibility.",
                "Scope: manuscript integration; no publication-eligibility promotion or sibling changes.",
            ]:
                self.assertIn(required, provenance)
            self.assertNotIn("standalone inactive artifact", provenance)
            for run in manifest["source_runs"]:
                self.assertFalse(run["completion"]["reportable"])
                self.assertEqual(run["completion"]["status"], "completed_noncanonical")
                self.assertIn(run["completion"]["nonreportable_reason"], provenance)
            published = json.loads((HERE / "selection_manifest.json").read_text())
            self.assertTrue(published["diagnostic_only"])
            self.assertFalse(published["reportable"])
            self.assertEqual(published["generator_sha256"],
                             hashlib.sha256((HERE / "generate.py").read_bytes()).hexdigest())
            for name, digest in published["output_sha256"].items():
                self.assertEqual(hashlib.sha256((HERE / name).read_bytes()).hexdigest(), digest)
            for name in ["description.text", "provenance.text", "table.tex"]:
                self.assertNotIn("F1", (out / name).read_text())
            before = {p.name: p.read_bytes() for p in out.iterdir()}
            with tempfile.TemporaryDirectory(dir=HERE) as fixture_dir:
                fixture = Path(fixture_dir)
                with SOURCE.open(newline="") as stream:
                    rows = list(csv.DictReader(stream))
                index = next(i for i, r in enumerate(rows) if r["Dataset"] == "Average"
                             and r["Split"] == "test" and r["Iteration"] == "initial")
                for mutation in ["missing", "negative_variance"]:
                    changed = copy.deepcopy(rows)
                    if mutation == "missing":
                        del changed[index]
                    else:
                        changed[index]["Hit@1_variance"] = "-0.01"
                    csv_path = fixture / "results.csv"
                    with csv_path.open("w", newline="") as stream:
                        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                        writer.writeheader()
                        writer.writerows(changed)
                    source_manifest = json.loads(SOURCE.with_name("manifest.json").read_text())
                    source_manifest["output"].update(sha256=hashlib.sha256(csv_path.read_bytes()).hexdigest(),
                                                      bytes=csv_path.stat().st_size)
                    source_manifest["row_count"] = len(changed)
                    manifest_path = fixture / "manifest.json"
                    manifest_path.write_text(json.dumps(source_manifest))
                    with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                        self.generator.generate(output=out, source=csv_path, source_manifest=manifest_path)
                    self.assertEqual(before, {p.name: p.read_bytes() for p in out.iterdir()})


if __name__ == "__main__":
    unittest.main()
