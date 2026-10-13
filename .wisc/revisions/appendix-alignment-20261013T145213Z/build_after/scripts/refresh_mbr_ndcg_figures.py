# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib==3.10.8"]
# ///
"""Render test nDCG (1–8) and available three-split trajectories without inference."""
from pathlib import Path
import argparse
import csv
import hashlib
import io
import json
import math

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'BayesGSI/tables/routing_performance_by_iteration/results.csv'
METHODS = ['Both Enabled', 'Only Gate', 'Both Disabled', 'Only MBR']
STAGES = {'train': 'prequential', 'validation': 'ledger_accepted_candidate', 'test': 'accepted'}
COUNTS = {'train': 3491, 'validation': 748, 'test': 748}
SPEC = {
    'mbr_replay_test_ndcg': {'test': dict.fromkeys(METHODS, 8)},
    'mbr_replay_test_ndcg@5': {'test': dict.fromkeys(METHODS, 8)},
    'mbr_replay_ndcg_all_splits': {
        'train': {'Both Enabled': 10, 'Only Gate': 8},
        'validation': {'Both Enabled': 10, 'Only Gate': 8},
        'test': {'Both Enabled': 10, 'Only Gate': 8, 'Both Disabled': 10, 'Only MBR': 10},
    },
}
METRICS = {name: ('nDCG@5' if name == 'mbr_replay_test_ndcg@5' else 'nDCG@10')
           for name in SPEC}
STYLES = {
    'Both Enabled': dict(color='#009E73', marker='D', linestyle='-.'),
    'Only Gate': dict(color='#D55E00', marker='s', linestyle='--'),
    'Both Disabled': dict(color='#7A7A7A', marker='^', linestyle=':'),
    'Only MBR': dict(color='#0072B2', marker='o', linestyle='-'),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def select(rows, spec, metric='nDCG@10'):
    selected = []
    for split, coverage in spec.items():
        for method, end in coverage.items():
            rr = [r for r in rows if r['Model'] == 'Qwen3.5 4B'
                  and r['Retriever'] == 'SkillSight' and r['Dataset'] == 'Average'
                  and r['Split'] == split and r['Evaluation'] == STAGES[split]
                  and r['Method'] == method and r['Iteration'].isdigit()
                  and 1 <= int(r['Iteration']) <= end]
            rr.sort(key=lambda r: int(r['Iteration']))
            if [int(r['Iteration']) for r in rr] != list(range(1, end + 1)):
                raise ValueError(f'Missing/duplicate checkpoints: {split}/{method}')
            for r in rr:
                value = float(r[metric])
                if int(r['n_tasks']) != COUNTS[split] or not math.isfinite(value) or not 0 <= value <= 1:
                    raise ValueError('Invalid metric or split task count')
            selected.extend(rr)
    assert len(selected) == sum(sum(v.values()) for v in spec.values())
    return selected


def initial_ndcg_points(run_map, methods, metric):
    cutoff = int(metric.split('@')[1])
    points, hashes = [], {}
    for method in methods:
        run_path = Path(run_map[method])
        prediction_path = run_path / 'predictions' / 'initial_test.jsonl'
        if not prediction_path.is_file():
            continue
        values, task_ids = [], set()
        for line in prediction_path.read_text().splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            task = record['task_id']
            if task in task_ids:
                raise ValueError(f'Duplicate initial test task: {method}/{task}')
            task_ids.add(task)
            relevant = set(record['required_ids'])
            ranking = record['ranked_ids']
            hits = [(rank, skill) for rank, skill in enumerate(ranking[:cutoff], 1) if skill in relevant]
            dcg = sum(1 / math.log2(rank + 1) for rank, _ in hits)
            ideal = sum(1 / math.log2(rank + 1) for rank in range(1, min(cutoff, len(relevant)) + 1))
            values.append(dcg / ideal if ideal else 1.0)
        if len(task_ids) != COUNTS['test']:
            raise ValueError(f'Initial test count mismatch for {method}: {len(task_ids)}')
        points.append({'Method': method, 'Split': 'test', 'Evaluation': 'initial_snapshot',
                       'Iteration': 0, metric: sum(values) / len(values),
                       'n_tasks': len(values), 'source': str(prediction_path),
                       'source_sha256': sha(prediction_path)})
        hashes[method] = sha(prediction_path)
    return points, hashes


def test_selection(rows, spec, metric='nDCG@10'):
    selected = select(rows, spec, metric)
    # Independently remove/duplicate/corrupt each selected split's first row.
    for split in spec:
        row = next(r for r in selected if r['Split'] == split)
        fixtures = [[r for r in rows if r is not row], rows + [row],
                    [dict(r, Evaluation='snapshot') if r is row else r for r in rows]]
        for fixture in fixtures:
            try:
                select(fixture, spec, metric)
            except ValueError:
                continue
            raise AssertionError('Bad fixture accepted')


def render(name, rows, source, output, common):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    spec = SPEC[name]
    metric = METRICS[name]
    selected = select(rows, spec, metric)
    test_selection(rows, spec, metric)
    initial_points, initial_hashes = ({}, {})
    if name in {'mbr_replay_test_ndcg', 'mbr_replay_test_ndcg@5'}:
        initial_points, initial_hashes = initial_ndcg_points(common['run_map'], METHODS, metric)
    multi = len(spec) > 1
    plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'],
                         'font.size': 10, 'axes.labelsize': 11, 'legend.fontsize': 9,
                         'pdf.fonttype': 42, 'ps.fonttype': 42, 'axes.spines.top': False,
                         'axes.spines.right': False, 'axes.grid': True,
                         'grid.alpha': .22, 'grid.linewidth': .5, 'savefig.bbox': 'tight'})
    fig, axes = plt.subplots(1, len(spec), figsize=(11.8, 3.7) if multi else (6.75, 3.4),
                             sharey=True, squeeze=False)
    fig.subplots_adjust(left=.065 if multi else .11, right=.985,
                        bottom=.25 if multi else .17, top=.80 if multi else .87, wspace=.12)
    values = [float(r[metric]) for r in selected] + [p[metric] for p in initial_points]
    ylim = (max(0, min(values) - .03), min(1, max(values) + .03))
    points, line_handles = list(initial_points), {}
    for ax, (split, coverage) in zip(axes.flat, spec.items()):
        for method, end in coverage.items():
            rr = [r for r in selected if r['Split'] == split and r['Method'] == method]
            initial = next((p for p in initial_points if p['Method'] == method), None)
            xs = ([0] if initial is not None else []) + [int(r['Iteration']) for r in rr]
            ys = ([initial[metric]] if initial is not None else []) + [float(r[metric]) for r in rr]
            line, = ax.plot(xs, ys, label=method, linewidth=1.8, markersize=4.5,
                            markeredgewidth=.6, markeredgecolor='white', **STYLES[method])
            expected_x = ([0] if initial is not None else []) + list(range(1, end + 1))
            assert list(line.get_xdata()) == expected_x
            assert list(line.get_ydata()) == ys
            line_handles[method] = line
            points.extend({'Method': method, 'Split': split, 'Evaluation': STAGES[split],
                           'Iteration': int(r['Iteration']), metric: float(r[metric]),
                           'n_tasks': int(r['n_tasks']), 'source': str(source),
                           'source_sha256': common['source_sha256']} for r in rr)
        assert len(ax.lines) == len(coverage) and not ax.collections
        ax.set_title(split.capitalize() if multi else 'Qwen3.5 4B / SkillSight — Test', fontsize=10)
        ax.set_xlabel('Iteration')
        end = max(coverage.values())
        if initial_points:
            ax.set_xticks(range(0, end + 1), ['Initial'] + [str(i) for i in range(1, end + 1)])
            ax.set_xlim(-.25, end + .25)
        else:
            ax.set_xticks([1, 2, 4, 6, 8, 10] if multi else range(1, 9))
            ax.set_xlim(.75, end + .25)
        ax.set_ylim(*ylim)
        ax.xaxis.grid(False)
        if multi and split != 'test':
            ax.text(.5, -.31, 'Both Disabled / Only MBR: unavailable', transform=ax.transAxes,
                    ha='center', fontsize=8, color='#555555')
    axes[0, 0].set_ylabel(metric)
    if multi:
        fig.suptitle('Qwen3.5 4B / SkillSight', fontsize=11, y=.99)
        fig.legend([line_handles[m] for m in METHODS], METHODS, ncol=4,
                   loc='upper center', bbox_to_anchor=(.52, .95), frameon=False, fontsize=9)
        description = ('Replay and held-out validation-gate ablation across train, validation, and test. '
                       f'Lines show task-weighted {metric}. Training uses prequential scores; validation uses '
                       'ledger-accepted candidates; test uses accepted checkpoints. Only Gate ends at iteration 8; '
                       'other available curves extend through 10. Both Disabled and Only MBR have test data only '
                       'in the refreshed CSV. Analysis-only; conditions mix refreshed and historical runs.')
        title = f'Replay and validation-gate {metric} by split'
    else:
        # Keep the shared palette but leave clearance below the lowest series.
        axes[0, 0].set_ylim(max(0, min(values) - .075), min(1, max(values) + .04))
        axes[0, 0].legend(ncol=2, loc='lower right', framealpha=.92)
        description = ('Replay and held-out validation-gate ablation on the test split. '
                       f'Lines show task-weighted {metric} at iteration 0 (initial, where archived) and accepted '
                       'checkpoints through iteration 8. The refreshed Only Gate run has no archived initial-test '
                       'snapshot, so its curve starts at iteration 1. Analysis-only; conditions mix run sources.')
        title = f'Replay and validation-gate ablation: test {metric}'
    for ax in axes.flat:
        assert all(ax.get_ylim()[0] <= y <= ax.get_ylim()[1] for line in ax.lines for y in line.get_ydata())
    output.mkdir(parents=True, exist_ok=True)
    fig.savefig(output / 'preview.pdf', metadata={'CreationDate': None, 'ModDate': None})
    fig.savefig(output / 'preview.png', dpi=300)
    plt.close(fig)
    (output / 'description.text').write_text(description + '\n')
    (output / 'table.tex').write_text('\\begin{figure}[!htbp]\n\\centering\n'
        f'\\includegraphics[width=\\linewidth]{{figs/{name}/preview.pdf}}\n'
        f'\\caption[{title}]{{\\input{{figs/{name}/description.text}}}}\n'
        f'\\label{{fig:{name}}}\n\\end{{figure}}\n')
    with (output / 'selected_data.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(points[0]))
        writer.writeheader()
        writer.writerows(points)
    missing = {s: [m for m in METHODS if m not in coverage] for s, coverage in spec.items()}
    unavailable_initial = [m for m in METHODS if m not in {p['Method'] for p in initial_points}]
    manifest = dict(common, artifact=name, metric=metric, panels=list(spec), coverage=spec,
                    initial_points=initial_points, unavailable_initial_test=unavailable_initial,
                    initial_metric='task-macro nDCG@k computed from predictions/initial_test.jsonl ranked_ids and required_ids',
                    initial_prediction_sha256=initial_hashes,
                    unavailable_series=missing, evaluation_stages={s: STAGES[s] for s in spec},
                    n_tasks={s: COUNTS[s] for s in spec}, selected_rows=points,
                    selected_row_count=len(points), points=points,
                    output_sha256={f: sha(output / f) for f in ['preview.pdf', 'preview.png',
                        'description.text', 'table.tex', 'selected_data.csv']})
    (output / 'selection.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (output / 'provenance.text').write_text(
        f'Artifact: {name}\nSource: {source}\nSource SHA256: {common["source_sha256"]}\n'
        f'Source rows: {len(rows)}; selected rows: {len(selected)}.\nMetric: {metric}\n'
        f'Coverage by split (inclusive iteration 1 through endpoint): {json.dumps(spec)}\n'
        f'Unavailable series in the refreshed CSV: {json.dumps(missing)}\n'
        'Selection: Model=Qwen3.5 4B; Retriever=SkillSight; Dataset=Average.\n'
        'Task-weighted within each split; train=3491, validation=748, test=748 tasks.\n'
        'Train=prequential; validation=ledger_accepted_candidate; test=accepted.\n'
        'Only Gate has no initial-test snapshot in its refreshed run and therefore starts at iteration 1.\n'
        'Initial nDCG computed task-wise from archived ranked_ids and required_ids; see selection.json for hashes.\n'
        'Analysis-only/non-reportable: mixed run families and unresolved publication validity.\n'
        f'Regenerate: uv run --script RouterBSIPaper/scripts/refresh_mbr_ndcg_figures.py --artifact {name}\n'
        'Exact data, completion snapshots, hashes and coverage: selection.json.\n'
        'Historical snapshot-manifest.json is not rewritten.\n')
    print(f'PASS {name}: {len(points)} points; panels={list(spec)}; coverage={spec}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--output-root', type=Path, default=ROOT / 'RouterBSIPaper/figs')
    parser.add_argument('--artifact', choices=list(SPEC), help='Render only this artifact')
    args = parser.parse_args()
    raw = args.source.read_bytes()
    rows = list(csv.DictReader(io.StringIO(raw.decode())))
    mapping = SOURCE.parent / 'input_runs.json'
    run_map = json.loads(mapping.read_text())['Qwen3.5 4B']['SkillSight']
    statuses = {}
    for method, path in run_map.items():
        p = Path(path) / 'completion.json'
        data = json.loads(p.read_text()) if p.exists() else {}
        statuses[method] = {'path': str(p), 'sha256': sha(p) if p.exists() else None,
                           **{k: data.get(k) for k in ['status', 'passed', 'reportable']}}
    common = {'source': str(args.source), 'source_sha256': hashlib.sha256(raw).hexdigest(),
              'source_row_count': len(rows), 'run_map': run_map, 'run_map_sha256': sha(mapping),
              'completion_snapshot': statuses, 'reportable': False,
              'aggregation': 'source task-weighted Average within split',
              'uncertainty': 'not estimated; no bands',
              'missing_data_policy': 'fail on missing required points; unavailable series omitted and labeled',
              'generator': str(Path(__file__).relative_to(ROOT)), 'generator_sha256': sha(Path(__file__))}
    for name in ([args.artifact] if args.artifact else SPEC):
        render(name, rows, args.source, args.output_root / name, common)
    assert sha(args.source) == common['source_sha256']
    print('PASS source unchanged; per-split missing/duplicate/wrong-stage rejection tests.')


if __name__ == '__main__':
    main()
