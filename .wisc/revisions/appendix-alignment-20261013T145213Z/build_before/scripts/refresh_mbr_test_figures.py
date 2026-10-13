# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib==3.10.8"]
# ///
"""Refresh the standalone MBR test F1 plot; never launch evaluations.

Run from any directory with: uv run --script <this file>
Only Gate is explicitly capped at iteration 8 per the approved snapshot.
The historical research-repo-template generators do not govern these outputs.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import io
import json
import math

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "BayesGSI/tables/routing_performance_by_iteration/results.csv"
COVERAGE = {"Both Enabled": 10, "Only Gate": 8, "Both Disabled": 10, "Only MBR": 10}
# nDCG variants are governed by refresh_mbr_ndcg_figures.py.
ARTIFACTS = {"mbr_replay_test_f1": "F1"}
STYLES = {
    "Both Enabled": {"color": "#009E73", "marker": "D", "linestyle": "-."},
    "Both Disabled": {"color": "#7A7A7A", "marker": "^", "linestyle": ":"},
    "Only MBR": {"color": "#0072B2", "marker": "o", "linestyle": "-"},
    "Only Gate": {"color": "#D55E00", "marker": "s", "linestyle": "--"},
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def select(rows):
    selected = []
    for method, end in COVERAGE.items():
        candidates = [r for r in rows if r['Model'] == 'Qwen3.5 4B'
                      and r['Retriever'] == 'SkillSight' and r['Dataset'] == 'Average'
                      and r['Split'] == 'test' and r['Evaluation'] == 'accepted'
                      and r['Method'] == method and r['Iteration'].isdigit()
                      and 1 <= int(r['Iteration']) <= end]
        candidates.sort(key=lambda r: int(r['Iteration']))
        if [int(r['Iteration']) for r in candidates] != list(range(1, end + 1)):
            raise ValueError(f'Missing or duplicate required test checkpoints: {method}')
        for r in candidates:
            if int(r['n_tasks']) != 748:
                raise ValueError('Unexpected test task count')
            for metric in ARTIFACTS.values():
                value = float(r[metric])
                if not math.isfinite(value) or not 0 <= value <= 1:
                    raise ValueError(f'Invalid {metric}')
        selected.extend(candidates)
    assert len(selected) == sum(COVERAGE.values())
    return selected


def check_fail_closed(rows):
    selected = select(rows)
    bad = [r for r in rows if r is not selected[0]]
    for fixture in [bad, rows + [selected[0]], [dict(r, Split='validation') for r in rows]]:
        try:
            select(fixture)
        except ValueError:
            continue
        raise AssertionError('Missing, duplicate, or wrong-split fixture was accepted')


def render(name, metric, selected, source, output, provenance):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'],
                         'font.size': 10, 'axes.labelsize': 11, 'legend.fontsize': 9,
                         'pdf.fonttype': 42, 'ps.fonttype': 42, 'axes.spines.top': False,
                         'axes.spines.right': False, 'axes.grid': True, 'grid.alpha': .22,
                         'grid.linewidth': .5, 'savefig.bbox': 'tight'})
    fig, ax = plt.subplots(figsize=(6.75, 3.4), layout='constrained')
    points = []
    for method in COVERAGE:
        rr = [r for r in selected if r['Method'] == method]
        xs = [int(r['Iteration']) for r in rr]
        ys = [float(r[metric]) for r in rr]
        line, = ax.plot(xs, ys, label=method, linewidth=1.8, markersize=4.5,
                        markeredgewidth=.6, markeredgecolor='white', **STYLES[method])
        assert list(line.get_xdata()) == xs and list(line.get_ydata()) == ys
        points.extend({'Method': method, 'Split': 'test', 'Iteration': x, metric: y}
                      for x, y in zip(xs, ys))
    assert len(ax.lines) == 4 and len(ax.collections) == 0
    assert list(ax.lines[1].get_xdata()) == list(range(1, 9))
    ax.set_title('Qwen3.5 4B / SkillSight — Test', fontsize=10, pad=10)
    ax.set_xlabel('Iteration')
    ax.set_ylabel(metric)
    ax.set_xticks(range(1, 11))
    ax.set_xlim(.75, 10.25)
    values = [float(r[metric]) for r in selected]
    ax.set_ylim(max(0, min(values) - (.10 if metric == 'F1' else .075)),
                min(1, max(values) + .04))
    ax.xaxis.grid(False)
    ax.legend(ncol=2, loc='lower right', framealpha=.92)
    output.mkdir(parents=True, exist_ok=True)
    fig.savefig(output / 'preview.pdf', metadata={'CreationDate': None, 'ModDate': None})
    fig.savefig(output / 'preview.png', dpi=300)
    plt.close(fig)
    description = (f'Replay and held-out validation-gate ablation on the test split. '
                   f'Lines show task-weighted {metric} at accepted checkpoints. '
                   'Only Gate ends at iteration 8; other conditions extend through iteration 10. '
                   'Analysis-only; conditions mix refreshed and historical runs.')
    (output / 'description.text').write_text(description + '\n')
    title = f'Replay and validation-gate ablation: test {metric}'
    (output / 'table.tex').write_text(
        '\\begin{figure}[!htbp]\n\\centering\n'
        f'\\includegraphics[width=\\linewidth]{{figs/{name}/preview.pdf}}\n'
        f'\\caption[{title}]{{\\input{{figs/{name}/description.text}}}}\n'
        f'\\label{{fig:{name}}}\n\\end{{figure}}\n')
    with (output / 'selected_data.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(selected[0]))
        writer.writeheader()
        writer.writerows(selected)
    manifest = dict(provenance, artifact=name, metric=metric, selected_rows=selected,
                    points=points, selected_row_count=len(selected),
                    output_sha256={p: digest(output / p) for p in
                                   ['preview.pdf', 'preview.png', 'description.text', 'table.tex', 'selected_data.csv']})
    (output / 'selection.json').write_text(json.dumps(manifest, indent=2) + '\n')
    notes = (f'Artifact: {name}\nMetric: {metric}\nSource: {source}\n'
             f'Source SHA256: {provenance["source_sha256"]}\n'
             f'Source rows: {provenance["source_row_count"]}; selected rows: {len(selected)}.\n'
             'Selection: Qwen3.5 4B / SkillSight; Dataset=Average; Split=test; Evaluation=accepted.\n'
             'Coverage: Both Enabled, Both Disabled, Only MBR: 1–10; Only Gate: 1–8 (explicit user-approved cap).\n'
             'Average is task-instance weighted over 748 test tasks, not an equal mean over datasets.\n'
             'F1 is full selected-set F1; nDCG@10 is ranked-skill performance.\n'
             'No initialization/final snapshots, interpolation, extrapolation, padding, or uncertainty bands.\n'
             'This replaces the historical all-splits/three-run nDCG figure with a test-only single-panel figure.\n'
             'Both Enabled and Only Gate use refreshed RouterBSI run_1; Both Disabled and Only MBR retain historical CSV rows.\n'
             'Analysis-only/non-reportable: mixed run families, incomplete Only Gate and unresolved publication validity.\n'
             'Completion metadata is a snapshot, not proof that historical CSV rows were regenerated.\n'
             'Regenerate: uv run --script RouterBSIPaper/scripts/refresh_mbr_test_figures.py\n'
             'See selection.json for completion metadata, source/run-map hashes and exact plotted points.\n'
             'snapshot-manifest.json remains the historical packaging manifest, not this refresh manifest.\n')
    (output / 'provenance.text').write_text(notes)
    print(f'{name}: PASS; metric={metric}; test-only; points={len(points)}; coverage={COVERAGE}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--output-root', type=Path, default=ROOT / 'RouterBSIPaper/figs')
    args = parser.parse_args()
    raw = args.source.read_bytes()
    rows = list(csv.DictReader(io.StringIO(raw.decode())))
    selected = select(rows)
    check_fail_closed(rows)
    run_map_path = SOURCE.parent / 'input_runs.json'
    run_map = json.loads(run_map_path.read_text())['Qwen3.5 4B']['SkillSight']
    statuses = {}
    for method, root in run_map.items():
        completion = Path(root) / 'completion.json'
        if completion.exists():
            data = json.loads(completion.read_text())
            statuses[method] = {'path': str(completion), 'sha256': digest(completion),
                                'status': data.get('status'), 'passed': data.get('passed'),
                                'reportable': data.get('reportable')}
        else:
            statuses[method] = {'path': str(completion), 'status': 'unavailable', 'reportable': None}
    provenance = {'source': str(args.source), 'source_sha256': hashlib.sha256(raw).hexdigest(),
                  'source_row_count': len(rows), 'run_map_sha256': digest(run_map_path),
                  'run_map': run_map, 'completion_snapshot': statuses,
                  'coverage': {m: list(range(1, end + 1)) for m, end in COVERAGE.items()},
                  'aggregation': 'source task-weighted Average over 748 test instances',
                  'reportable': False, 'uncertainty': 'not estimated; no bands',
                  'missing_data_policy': 'fail on missing required points; Only Gate explicitly capped at 8',
                  'generator': str(Path(__file__).relative_to(ROOT)), 'generator_sha256': digest(Path(__file__))}
    for name, metric in ARTIFACTS.items():
        render(name, metric, selected, args.source, args.output_root / name, provenance)
    assert hashlib.sha256(args.source.read_bytes()).hexdigest() == provenance['source_sha256']
    print('PASS: missing/duplicate/wrong-split rejection tests; source unchanged.')


if __name__ == '__main__':
    main()
