# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib==3.10.8"]
# ///
"""Offline verification: uv run --script test_generate.py -v."""
import copy
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import statistics
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("trajectory_generator", HERE / "generate.py")
assert spec is not None and spec.loader is not None
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


class RawSourceTests(unittest.TestCase):
    def test_exact_raw_matrix_and_population_statistics(self):
        self.assertEqual(g.ARTIFACT, "routerbsi_test_ndcg@1_std")
        points, rows, provenance = g.load_source()
        self.assertEqual(len(points), 12)
        self.assertEqual([(r['run'], r['checkpoint']) for r in rows],
                         [(r, c) for r in g.RUNS for c in g.CHECKPOINTS])
        for p in points:
            vals = [r['ndcg1'] for r in rows if r['checkpoint'] == p['checkpoint']]
            self.assertEqual(p['mean'], statistics.mean(vals))
            self.assertAlmostEqual(p['population_variance'], statistics.pvariance(vals), places=16)
            self.assertAlmostEqual(p['population_sd'], statistics.pstdev(vals), places=16)
        for r in rows:
            self.assertEqual(r['n_tasks'], 748)
            self.assertEqual(r['ndcg1'], r['hits_at_1'] / 748)
            self.assertEqual(r['mrr10_crosscheck'], 'verified')
            self.assertEqual(r['policy_binding'], 'all_candidate_statements_verified')
            self.assertFalse(r['reportable'])
        self.assertEqual({r['status'] for r in rows}, {'completed_noncanonical'})
        self.assertTrue(provenance['diagnostic_only'])
        self.assertFalse(provenance['reportable'])


class FailureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        r = g.SOURCE / 'run_1'
        cls.records = [json.loads(line) for line in (r / 'predictions/initial_test.jsonl').read_text().splitlines()]
        cls.policy = json.loads((r / 'conditions_initial.json').read_text())
        cls.tasks = set(json.loads((r / 'test_state.json').read_text())['task_ids'])

    def test_tampered_policy_payload_fails_even_with_unchanged_hash_tag(self):
        policy = copy.deepcopy(self.policy)
        policy['conditions']['sra']['unretrieved_test_skill'] = ['altered predicate']
        with self.assertRaisesRegex(ValueError, 'policy content hash'):
            g.evaluate_records(self.records, self.tasks, policy)

    def test_invalid_prediction_evidence_fails_closed(self):
        good, gold = g.evaluate_records(self.records, self.tasks, self.policy)
        cases = {'missing_task': self.records[:-1],
                 'duplicate_task': self.records[:-1] + [self.records[0]]}
        for key, value in [('required_ids', []), ('required_ids', ['x', 'x']),
                           ('ranked_ids', None), ('ranked_ids', ['x', 'x']),
                           ('task_id', 'unknown'), ('tier', 'validation'),
                           ('label_source', 'unknown'), ('library_hash', '0' * 64),
                           ('candidate_statements', [])]:
            row = dict(self.records[0]); row[key] = value
            cases[f'{key}={value}'] = [row, *self.records[1:]]
        row = copy.deepcopy(self.records[0]); row['candidate_statements'][0] = ['tampered']
        cases['statement_mismatch'] = [row, *self.records[1:]]
        for name, rows in cases.items():
            with self.subTest(case=name), self.assertRaises(ValueError):
                g.evaluate_records(rows, self.tasks, self.policy)
        changed = copy.deepcopy(gold)
        changed[next(iter(changed))]['required_ids'] = ['wrong-gold']
        with self.assertRaisesRegex(ValueError, 'gold/task identity drift'):
            g.evaluate_records(self.records, self.tasks, self.policy, changed)
        empty_rank = dict(self.records[0]); empty_rank['ranked_ids'] = []
        values, _ = g.evaluate_records([empty_rank, *self.records[1:]], self.tasks, self.policy)
        expected = good['hits_at_1'] - int(self.records[0]['ranked_ids'][0] in self.records[0]['required_ids'])
        self.assertEqual(values['hits_at_1'], expected)

    def test_bad_metrics_completion_and_input_hashes_fail(self):
        values, _ = g.evaluate_records(self.records, self.tasks, self.policy)
        good = {'all': {'count': 748, 'Hit@1': values['ndcg1'], 'MRR@10': values['mrr10']}}
        self.assertEqual(g.crosscheck_metrics(good, values)['hit1_crosscheck'], 'verified')
        absent = copy.deepcopy(good); del absent['all']['Hit@1']
        self.assertEqual(g.crosscheck_metrics(absent, values)['hit1_crosscheck'], 'unavailable_not_stored')
        for key, value in [('count', 747), ('Hit@1', float('nan')), ('Hit@1', 0),
                           ('MRR@10', None), ('MRR@10', float('inf')), ('MRR@10', 0)]:
            changed = copy.deepcopy(good); changed['all'][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                g.crosscheck_metrics(changed, values)
        completion = json.loads((g.SOURCE / 'run_1/completion.json').read_text())
        for key, value in [('reportable', True), ('status', 'running'), ('nonreportable_reason', ''),
                           ('passed', False), ('analysis_ready', False)]:
            changed = dict(completion); changed[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                g.validate_completion(changed)
        with tempfile.TemporaryDirectory(dir=HERE) as temp:
            file = Path(temp) / 'input.json'; file.write_text('{"ok": true}')
            inputs = {}; g.read_source(file, inputs)
            g.verify_input_hashes(inputs)
            file.write_text('{"ok": false}')
            with self.assertRaisesRegex(ValueError, 'Source drift'):
                g.verify_input_hashes(inputs)
            with self.assertRaisesRegex(ValueError, 'Source drift'):
                g.read_source(file, inputs)
            file.unlink()
            with self.assertRaisesRegex(ValueError, 'Missing source'):
                g.read_source(file, {})

    def test_invalid_matrix_or_renderer_statistics_fail(self):
        points, rows, _ = g.load_source()
        for changed in [rows[:-1], rows + [rows[0]], list(reversed(rows))]:
            with self.assertRaises(ValueError):
                g.aggregate(changed)
        for key, value in [('mean', float('nan')), ('population_sd', -1), ('x', 12), ('run_1', 1.1)]:
            changed = copy.deepcopy(points); changed[0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                g.build_figure(changed)
        with self.assertRaisesRegex(ValueError, 'Outputs must stay'):
            g.generate(output=HERE.parent)


class ArtifactTests(unittest.TestCase):
    def test_renderer_and_reproducible_artifacts(self):
        self.assertTrue(hasattr(g, 'generate'), 'missing standalone publisher')
        points, _, _ = g.load_source()
        fig, ax = g.build_figure(points)
        try:
            self.assertEqual(len(fig.axes), 1)
            self.assertEqual(len(ax.lines), 1)
            self.assertEqual(len(ax.collections), 1)
            line = ax.lines[0]
            self.assertEqual(line.get_label(), 'RouterBSI')
            self.assertEqual(line.get_color(), '#009E73')
            self.assertEqual(list(line.get_xdata()), list(range(12)))
            self.assertEqual(list(line.get_ydata()), [p['mean'] for p in points])
            self.assertEqual(ax.get_ylabel(), 'nDCG@1')
            self.assertEqual([t.get_text() for t in ax.get_xticklabels()], list(g.LABELS))
            vertices = ax.collections[0].get_paths()[0].vertices
            for p in points:
                ys = [float(y) for x, y in vertices if x == p['x']]
                self.assertEqual(min(ys), p['lower'])
                self.assertEqual(max(ys), p['upper'])
                self.assertLess(ax.get_ylim()[0], p['lower'])
                self.assertGreater(ax.get_ylim()[1], p['upper'])
            renderer = fig.canvas.get_renderer()
            boxes = [t.get_window_extent(renderer) for t in ax.get_xticklabels()]
            for a, b in zip(boxes, boxes[1:]):
                self.assertFalse(a.overlaps(b), 'overlapping category labels')
            for box in boxes:
                self.assertGreaterEqual(box.x0, 0)
                self.assertGreaterEqual(box.y0, 0)
                self.assertLessEqual(box.x1, fig.bbox.width)
                self.assertLessEqual(box.y1, fig.bbox.height)
            self.assertAlmostEqual(fig.get_figwidth() * 72, 218)
            self.assertTrue(all(8 <= t.get_fontsize() <= 9 for t in ax.get_xticklabels()))
        finally:
            import matplotlib.pyplot as plt
            plt.close(fig)
        with tempfile.TemporaryDirectory(dir=HERE) as temp:
            out = Path(temp)
            manifest = g.generate(output=out)
            self.assertEqual(manifest['artifact'], 'routerbsi_test_ndcg@1_std')
            self.assertEqual(manifest['evaluation_count'], 36)
            self.assertEqual(manifest['selected_row_count'], 12)
            self.assertEqual(manifest['generator_sha256'], g.digest((HERE / 'generate.py').read_bytes()))
            for filename, sha in manifest['output_sha256'].items():
                self.assertEqual(g.digest((out / filename).read_bytes()), sha)
            for filename, n in [('selected_data.csv', 12), ('per_run_data.csv', 36)]:
                with (out / filename).open() as stream:
                    data = list(csv.DictReader(stream))
                self.assertEqual(len(data), n)
            with (out / 'selected_data.csv').open() as stream:
                saved = list(csv.DictReader(stream))
            for row, point in zip(saved, points):
                for key in ['mean', 'population_variance', 'population_sd', *g.RUNS]:
                    self.assertEqual(float(row[key]), point[key])
            wrapper = (out / 'table.tex').read_text()
            self.assertIn('{figs/routerbsi_test_ndcg@1_std/preview.pdf}', wrapper)
            self.assertIn('{fig:routerbsi_test_ndcg@1_std}', wrapper)
            self.assertIn('{figs/routerbsi_test_ndcg@1_std/description.text}', wrapper)
            self.assertNotIn('ablation', (out / 'description.text').read_text().lower())
            before = {f.name: f.read_bytes() for f in out.iterdir()}
            g.generate(output=out)
            self.assertEqual(before, {f.name: f.read_bytes() for f in out.iterdir()},
                             'regeneration is not byte reproducible')
            with self.assertRaises(ValueError):
                g.generate(output=out, source=out / 'missing-source')
            self.assertEqual(before, {f.name: f.read_bytes() for f in out.iterdir()})


if __name__ == "__main__":
    unittest.main()
