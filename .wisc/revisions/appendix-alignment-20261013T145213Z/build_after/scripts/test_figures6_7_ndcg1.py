#!/usr/bin/env python3
"""Focused tests: /usr/bin/python3 -B RouterBSIPaper/scripts/test_figures6_7_ndcg1.py

Old-style control uses ONLY the original renderer in temporary output folders;
never invoke the broad template artifact generator. Optional before snapshots
are read-only and are not needed for the enduring numeric/artist tests.
"""
import copy
import csv
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

import figures6_7_ndcg1 as g

EXPECTED = {
    g.TOKEN: [0.7419786096256684, 0.553475935828877, 0.6844919786096256, 0.643048128342246],
    g.LLMS: [0.470588, 0.520053, 0.741979, 0.635027, 0.802139, 0.685829, 0.744652],
}
TOKENS = [1324250594, 840052489, 1181025935, 866352051]


def rows(artifact):
    path = g.ROOT / "BayesGSI/tables" / g.SPECS[artifact][0] / "results.csv"
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


class FigureTests(unittest.TestCase):
    def tearDown(self):
        g.plt.close("all")

    def test_exact_selection_and_source_alias(self):
        for name in g.SPECS:
            source, selection = g.read_selection(name)
            self.assertEqual([p["y"] for p in selection["points"]], EXPECTED[name])
            self.assertTrue(all(p["metric"] == "Hit@1" and p["display_metric"] == "nDCG@1" for p in selection["points"]))
            if name == g.TOKEN:
                self.assertEqual([p["x"] for p in selection["points"]], [v/1e6 for v in TOKENS])
                self.assertEqual([p["Method"] for p in selection["points"]], list(g.STYLES))
            else:
                self.assertEqual([(p["Model"], p["Method"]) for p in selection["points"]], [(g.MODELS[0], "SkillSight")] + [(m, method) for m in g.MODELS for method in g.METHODS])
            # If Hit@1 changes, plotted selection must change; nDCG@10 must not drive y.
            source_rows = rows(name)
            target = next(r for r in source_rows if r == selection["selected_rows"][0])
            target["Hit@1"] = "0.123456"
            self.assertEqual(g.select_data(name, source_rows)["points"][0]["y"], .123456)

    def test_missing_invalid_metrics_fail_closed(self):
        for name in g.SPECS:
            for invalid in [None, "", "NaN", "inf", "-0.1", "1.1", "garbage"]:
                rr = rows(name)
                target = next(r for r in rr if name == g.TOKEN or (r["Dataset"] == "Average" and r["Method"] == "SkillSight" and r["Model"] == g.MODELS[0]))
                if invalid is None:
                    del target["Hit@1"]
                else:
                    target["Hit@1"] = invalid
                with self.subTest(artifact=name, value=invalid), self.assertRaises(ValueError):
                    g.select_data(name, rr)

    def test_source_hash_count_identity_and_tokens_fail_closed(self):
        for name in g.SPECS:
            with self.assertRaises(ValueError):
                g.select_data(name, rows(name)[:-1])
            rr = rows(name)
            rr[0]["Model"] = "wrong"
            if name == g.LLMS:
                rr[6]["Model"] = "wrong"
            with self.assertRaises(ValueError):
                g.select_data(name, rr)
            with tempfile.TemporaryDirectory() as tmp:
                changed = Path(tmp) / "results.csv"
                changed.write_text("missing,data\n")
                with self.assertRaisesRegex(ValueError, "source drift"):
                    g.read_selection(name, changed)
        for value in ["", "nan", "1.1", "-1", "0"]:
            rr = rows(g.TOKEN)
            rr[0]["Total Tokens"] = value
            with self.assertRaises(ValueError):
                g.select_data(g.TOKEN, rr)
        rr = rows(g.LLMS)
        rr[6] = rr[13].copy()
        with self.assertRaises(ValueError):
            g.select_data(g.LLMS, rr)

    def test_actual_artist_values_annotations_and_style(self):
        for name in g.SPECS:
            _, selection = g.read_selection(name)
            fig, ax = g.render(name, selection)
            fig.canvas.draw()
            self.assertEqual(ax.get_ylabel(), "nDCG@1")
            self.assertEqual(len(fig.axes), 1)
            if name == g.TOKEN:
                self.assertEqual(len(ax.collections), 4)
                np.testing.assert_array_equal([c.get_offsets()[0, 0] for c in ax.collections], [v/1e6 for v in TOKENS])
                np.testing.assert_array_equal([c.get_offsets()[0, 1] for c in ax.collections], EXPECTED[name])
                self.assertEqual(len(ax.texts), 0)  # Preserve old scatter with no numeric annotations.
                self.assertLess(ax.get_ylim()[0], min(EXPECTED[name]))
                self.assertGreater(ax.get_ylim()[1], max(EXPECTED[name]))
            else:
                self.assertEqual(len(ax.patches), 7)
                self.assertEqual([p.get_height() for p in ax.patches], EXPECTED[name])
                self.assertEqual([t.get_text() for t in ax.texts], [f"{v:.3f}" for v in EXPECTED[name]])
                self.assertEqual([t.get_position()[1] for t in ax.texts], [v+.018 for v in EXPECTED[name]])
                self.assertEqual(ax.get_ylim(), (0, 1))
                self.assertEqual([p.get_hatch() for p in ax.patches], [None, "///", None, "///", None, "///", None])
                self.assertEqual([p.get_alpha() for p in ax.patches], [None, .55, None, .55, None, .55, None])
                self.assertEqual([t.get_text() for t in ax.get_xticklabels()], ["SkillSight", *g.MODELS])
                self.assertEqual(ax.get_legend().get_texts()[0].get_text(), r"$\mathrm{RouterBSI}_{\mathrm{init}}$")
                self.assertEqual(ax.get_legend().get_texts()[0].get_math_fontfamily(), "dejavuserif")

    def test_old_metric_control_pixel_exact_and_new_style_unchanged(self):
        sys.path.insert(0, str(g.ROOT / "research-repo-template/paper"))
        original = importlib.import_module("artifact_rendering")
        report = []
        for name in g.SPECS:
            selection = g.select_data(name, rows(name), metric="nDCG@10")
            old_fig, old_ax = g.render(name, selection, display_metric="nDCG@10")
            old_state = g.artist_state(name, old_fig, old_ax)
            with tempfile.TemporaryDirectory() as tmp:
                tmp = Path(tmp)
                original.plot_figure(name, selection, tmp)
                copy_path = tmp / "copied.png"
                # Match the original PDF-then-PNG draw sequence (constrained layout).
                old_fig.savefig(tmp / "copied.pdf", metadata={"CreationDate": None, "ModDate": None})
                old_fig.savefig(copy_path, dpi=300)
                np.testing.assert_array_equal(np.asarray(Image.open(copy_path)), np.asarray(Image.open(tmp / "preview.png")))
                baseline = g.ROOT / ".wisc/verification/figures6-7-ndcg1/before/figs" / name / "preview.png"
                baseline_checked = baseline.exists()
                if baseline_checked:
                    np.testing.assert_array_equal(np.asarray(Image.open(copy_path)), np.asarray(Image.open(baseline)))
            _, new_selection = g.read_selection(name)
            new_fig, new_ax = g.render(name, new_selection)
            new_state = g.artist_state(name, new_fig, new_ax)
            # Explicitly permitted deltas: y, metric label, adaptive scatter ylim,
            # and Figure7 numeric annotations. Every other serialized style is equal.
            old_state.pop("ylabel"); new_state.pop("ylabel")
            if name == g.TOKEN:
                old_state.pop("ylim"); new_state.pop("ylim")
                for state in [old_state, new_state]:
                    for scatter in state["scatter"]:
                        scatter["xy"][0][1] = 0
            else:
                for state in [old_state, new_state]:
                    for bar in state["bars"]:
                        bar["y"] = 0
                    for annotation in state["annotations"]:
                        annotation["text"] = ""
                        annotation["position"][1] = 0
            self.assertEqual(old_state, new_state)
            report.append({"artifact": name, "copied_vs_original_renderer": "pixel-exact", "copied_vs_before_png": "pixel-exact" if baseline_checked else "not available", "nonmetric_artist_style": "equal"})
        print("CONTROL_REPORT=" + json.dumps(report))

    def test_alias_nonempty_universe_and_empty_gold_failure(self):
        evidence = g.validate_alias_evidence()
        self.assertEqual(evidence["total_tasks"], 5400)
        self.assertEqual(evidence["empty_gold_tasks"], 0)
        # A matching hash is insufficient: independently reject empty annotations.
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            p = tmp / "BayesGSI/data/bench/instances/example.json"
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps([{"instance_id": "x", "dataset": "x", "skill_annotations": []}]))
            fixture = {"annotations": [{"path": str(p.relative_to(tmp)), "sha256": g.sha256(p), "tasks": 1}], "total_tasks": 1, "empty_gold_tasks": 0, "source_evaluator_files": []}
            with self.assertRaisesRegex(ValueError, "empty/invalid gold"):
                g.validate_alias_evidence(tmp, fixture)
        sys.path.insert(0, str(g.ROOT / "BayesGSI/tables"))
        evaluator = importlib.import_module("table_utils")
        self.assertEqual(evaluator._hit_at((), (), 1), 0)
        self.assertEqual(evaluator._ndcg_at((), (), 1), 1)
        for ranking in [(), ("a",), ("b",), ("b", "a")]:
            for gold in [("a",), ("a", "c")]:
                self.assertEqual(evaluator._hit_at(ranking, gold, 1), evaluator._ndcg_at(ranking, gold, 1))

    def test_generated_artifacts_and_hash_closure(self):
        for name in g.SPECS:
            out = g.PAPER / "figs" / name
            manifest = json.loads((out / "selection_manifest.json").read_text())
            self.assertEqual(manifest["artifact"], name)
            self.assertEqual(manifest["metric"], "Hit@1")
            self.assertEqual(manifest["display_metric"], "nDCG@1")
            for item in [manifest["source"], manifest["generator"], manifest["alias_evidence_file"], *manifest["outputs"], *manifest["manuscript_bindings"]]:
                self.assertEqual(g.sha256(g.ROOT / item["path"]), item["sha256"], item["path"])
            with (out / "selected_data.csv").open(newline="") as handle:
                selected = list(csv.DictReader(handle))
            self.assertEqual(selected, g.read_selection(name)[1]["selected_rows"])
            self.assertEqual([float(row["Hit@1"]) for row in selected], EXPECTED[name])


if __name__ == "__main__":
    unittest.main(verbosity=2)
