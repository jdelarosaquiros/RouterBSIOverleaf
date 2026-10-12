# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib==3.10.8"]
# ///
"""Refresh the temporary test nDCG@5 comparison, including the GatedRouter alternate run."""
from pathlib import Path
import argparse
import csv
import hashlib
import io
import json
import math

ROOT = Path(__file__).resolve().parents[2]
TABLE = ROOT / 'BayesGSI/tables/routing_performance_by_iteration/results.csv'
ALT_RUN = ROOT / '.wisc/results/GatedRouter/sra_full_skillsight_f1_i10_l400_qwen3.5_4b/run_1'
OPT_RUNS = {
    'Both Enabled': ROOT / '.wisc/results/RouterBSI/sra_full_skillsight_f1_i10_l400_qwen3.5_4b_optimized/run_1',
    'Only Gate': ROOT / '.wisc/results/RouterBSI/sra_full_skillsight_f1_i10_l400_qwen3.5_4b_optimized_gate_only/run_1',
}
OUTPUT = ROOT / 'RouterBSIPaper/figs/mbr_replay_test_ndcg@5_temp'
BASE_METHODS = ['Both Enabled', 'Only Gate', 'Both Disabled', 'Only MBR']
COVERAGE = {'Both Enabled': 10, 'Only Gate': 8, 'Both Disabled': 8, 'Only MBR': 8, 'Only MBR Alt': 10}
STYLES = {
    'Both Enabled': dict(color='#009E73', marker='D', linestyle='-.'),
    'Only Gate': dict(color='#D55E00', marker='s', linestyle='--'),
    'Both Disabled': dict(color='#7A7A7A', marker='^', linestyle=':'),
    'Only MBR': dict(color='#0072B2', marker='o', linestyle='-'),
    'Only MBR Alt': dict(color='#CC79A7', marker='X', linestyle=(0, (4, 1.5))),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def initial_ndcg_point(method, run_path):
    path = run_path / 'predictions' / 'initial_test.jsonl'
    if not path.is_file():
        return None
    values, task_ids = [], set()
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        task = record['task_id']
        if task in task_ids:
            raise ValueError(f'Duplicate initial test task: {method}/{task}')
        task_ids.add(task)
        relevant, ranking = set(record['required_ids']), record['ranked_ids']
        hits = [(rank, skill) for rank, skill in enumerate(ranking[:5], 1) if skill in relevant]
        dcg = sum(1 / math.log2(rank + 1) for rank, _ in hits)
        ideal = sum(1 / math.log2(rank + 1) for rank in range(1, min(5, len(relevant)) + 1))
        values.append(dcg / ideal if ideal else 1.0)
    if len(task_ids) != 748:
        raise ValueError(f'Initial test count mismatch for {method}: {len(task_ids)}')
    return {'Method': method, 'Split': 'test', 'Evaluation': 'initial_snapshot',
            'Iteration': 0, 'n_tasks': len(values), 'nDCG@5': sum(values) / len(values),
            'Source': str(path), 'Source_SHA256': sha(path)}


def optimized_run_points(method, run_path):
    completion_path = run_path / 'completion.json'
    completion = json.loads(completion_path.read_text())
    points, evidence = [], []
    expected_ids = None
    i = 1
    while True:
        checkpoint = run_path / 'iterations' / f'{i:02d}'
        metric_path, ledger_path = checkpoint / 'metrics.json', checkpoint / 'ledger.json'
        prediction_path = checkpoint / f'test_accepted_{i:02d}.jsonl'
        if not (metric_path.is_file() and ledger_path.is_file() and prediction_path.is_file()):
            break
        metrics, ledger = json.loads(metric_path.read_text()), json.loads(ledger_path.read_text())
        test = metrics.get('test_accepted', {}).get('all', {})
        if ledger.get('accepted') is not True or test.get('count') != 748:
            break
        ids, scores = set(), []
        with prediction_path.open() as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                task = record['task_id']
                if task in ids:
                    raise ValueError(f'Duplicate optimized test task: {method}/{i}/{task}')
                ids.add(task)
                relevant, ranking = set(record['required_ids']), record['ranked_ids']
                hits = [(rank, skill) for rank, skill in enumerate(ranking[:5], 1) if skill in relevant]
                dcg = sum(1 / math.log2(rank + 1) for rank, _ in hits)
                ideal = sum(1 / math.log2(rank + 1) for rank in range(1, min(5, len(relevant)) + 1))
                scores.append(dcg / ideal if ideal else 1.0)
        if len(ids) != 748 or len(scores) != 748:
            raise ValueError(f'Optimized test prediction count mismatch: {method}/{i}: {len(ids)}')
        if expected_ids is None:
            expected_ids = ids
        elif ids != expected_ids:
            raise ValueError(f'Optimized test task membership changes across checkpoints: {method}/{i}')
        points.append({'Method': method, 'Split': 'test', 'Evaluation': 'accepted',
                       'Iteration': i, 'n_tasks': len(scores), 'nDCG@5': sum(scores) / len(scores),
                       'Source': str(prediction_path), 'Source_SHA256': sha(prediction_path)})
        evidence.append({'iteration': i, 'metrics': str(metric_path), 'metrics_sha256': sha(metric_path),
                         'ledger': str(ledger_path), 'ledger_sha256': sha(ledger_path),
                         'accepted': True, 'accepted_hash': ledger.get('accepted_hash'),
                         'predictions': str(prediction_path), 'predictions_sha256': sha(prediction_path),
                         'test_count': len(ids)})
        i += 1
    if not points:
        raise ValueError(f'No complete accepted test checkpoints found for {method}: {run_path}')
    later = sorted(d.name for d in (run_path / 'iterations').iterdir()
                   if d.is_dir() and d.name.isdigit() and int(d.name) >= i)
    return points, {'run': str(run_path), 'completion': completion,
                    'completion_path': str(completion_path), 'completion_sha256': sha(completion_path),
                    'latest_contiguous_completed_iteration': points[-1]['Iteration'],
                    'checkpoint_evidence': evidence, 'later_unplotted_checkpoints': later}


def load_points(table_path, alt_run, run_map_path):
    raw = table_path.read_bytes()
    table_rows = list(csv.DictReader(io.StringIO(raw.decode())))
    run_map = json.loads(run_map_path.read_text())['Qwen3.5 4B']['SkillSight']
    points = []
    initial_points = []
    coverage = dict(COVERAGE)
    optimized_sources = {}
    for method in BASE_METHODS:
        if method in OPT_RUNS:
            method_points, source_info = optimized_run_points(method, OPT_RUNS[method])
            points.extend(method_points)
            coverage[method] = source_info['latest_contiguous_completed_iteration']
            optimized_sources[method] = source_info
            continue
        point = initial_ndcg_point(method, Path(run_map[method]))
        if point is not None:
            points.append(point)
            initial_points.append(point)
        rows = [r for r in table_rows if r['Model'] == 'Qwen3.5 4B'
                and r['Retriever'] == 'SkillSight' and r['Method'] == method
                and r['Dataset'] == 'Average' and r['Split'] == 'test'
                and r['Evaluation'] == 'accepted' and r['Iteration'].isdigit()
                and 1 <= int(r['Iteration']) <= coverage[method]]
        rows.sort(key=lambda r: int(r['Iteration']))
        if [int(r['Iteration']) for r in rows] != list(range(1, coverage[method] + 1)):
            raise ValueError(f'Missing/duplicate CSV nDCG@5 checkpoints: {method}')
        for r in rows:
            y = float(r['nDCG@5'])
            if int(r['n_tasks']) != 748 or not math.isfinite(y) or not 0 <= y <= 1:
                raise ValueError(f'Invalid source table value: {method}/{r["Iteration"]}')
            points.append({'Method': method, 'Split': 'test', 'Evaluation': 'accepted',
                           'Iteration': int(r['Iteration']), 'n_tasks': 748, 'nDCG@5': y,
                           'Source': str(table_path), 'Source_SHA256': sha(table_path)})
    completion_path = alt_run / 'completion.json'
    completion = json.loads(completion_path.read_text())
    if completion.get('status') not in {'completed_noncanonical', 'completed'} or not completion.get('passed'):
        raise ValueError('Alternate run is not completed/passed')
    initial_alt = initial_ndcg_point('Only MBR Alt', alt_run)
    if initial_alt is not None:
        points.append(initial_alt)
        initial_points.append(initial_alt)
    if completion.get('split_counts', {}).get('test') != 748:
        raise ValueError('Alternate run test split count is not 748')
    metric_files, ledger_files = [], []
    for i in range(1, 11):
        checkpoint = alt_run / 'iterations' / f'{i:02d}'
        metric_path, ledger_path = checkpoint / 'metrics.json', checkpoint / 'ledger.json'
        metrics = json.loads(metric_path.read_text())
        ledger = json.loads(ledger_path.read_text())
        if ledger.get('accepted') is not True:
            raise ValueError(f'Alternate run iteration {i} was not accepted')
        test = metrics['test_accepted']['all']
        if test.get('count') != 748:
            raise ValueError(f'Alternate run iteration {i} test count mismatch')
        y = test['nDCG@5']
        if not math.isfinite(y) or not 0 <= y <= 1:
            raise ValueError(f'Invalid alternate nDCG@5 at iteration {i}')
        points.append({'Method': 'Only MBR Alt', 'Split': 'test', 'Evaluation': 'accepted',
                       'Iteration': i, 'n_tasks': 748, 'nDCG@5': y,
                       'Source': str(metric_path), 'Source_SHA256': sha(metric_path)})
        metric_files.append({'path': str(metric_path), 'sha256': sha(metric_path)})
        ledger_files.append({'path': str(ledger_path), 'sha256': sha(ledger_path),
                             'accepted': True, 'accepted_hash': ledger.get('accepted_hash')})
    expected = sum(coverage.values()) + len(initial_points)
    if len(points) != expected:
        raise AssertionError(f'Expected {expected} points, got {len(points)}')
    for method, end in coverage.items():
        xs = [p['Iteration'] for p in points if p['Method'] == method]
        expected_xs = ([0] if method in {p['Method'] for p in initial_points} else []) + list(range(1, end + 1))
        if xs != expected_xs:
            raise AssertionError(f'Wrong plotted checkpoints for {method}: {xs}')
    return points, initial_points, {'table_sha256': sha(table_path), 'table_rows': len(table_rows),
                    'run_map': run_map, 'run_map_sha256': sha(run_map_path),
                                        'initial_points': initial_points,
                    'unavailable_initial_test': [m for m in BASE_METHODS + ['Only MBR Alt']
                                                 if m not in {p['Method'] for p in initial_points}],
                    'initial_metric': 'task-macro nDCG@5 computed from ranked_ids/required_ids',
                    'initial_prediction_sha256': {p['Method']: p['Source_SHA256'] for p in initial_points},
                    'alternate_run': str(alt_run), 'completion_path': str(completion_path),
                    'completion_sha256': sha(completion_path), 'completion': completion,
                    'alternate_metric_files': metric_files, 'alternate_ledger_files': ledger_files,
                    'optimized_sources': optimized_sources, 'coverage': coverage}


def render(points, initial_points, output, provenance, coverage):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'],
                         'font.size': 10, 'axes.labelsize': 11, 'legend.fontsize': 8.5,
                         'pdf.fonttype': 42, 'ps.fonttype': 42, 'axes.spines.top': False,
                         'axes.spines.right': False, 'axes.grid': True,
                         'grid.alpha': .22, 'grid.linewidth': .5, 'savefig.bbox': 'tight'})
    fig, ax = plt.subplots(figsize=(7.0, 3.65), layout='constrained')
    for method, end in coverage.items():
        pp = [p for p in points if p['Method'] == method]
        xs, ys = [p['Iteration'] for p in pp], [p['nDCG@5'] for p in pp]
        line, = ax.plot(xs, ys, label=method, linewidth=1.8, markersize=4.6,
                        markeredgewidth=.6, markeredgecolor='white', **STYLES[method])
        expected_xs = ([0] if method in {p['Method'] for p in initial_points} else []) + list(range(1, end + 1))
        assert list(line.get_xdata()) == expected_xs
        assert list(line.get_ydata()) == ys
    assert len(ax.lines) == 5 and len(ax.collections) == 0
    ax.set_title('Qwen3.5 4B / SkillSight — Test', fontsize=10, pad=10)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('nDCG@5')
    ax.set_xticks(range(0, 11), ['Initial'] + [str(i) for i in range(1, 11)])
    ax.set_xlim(-.25, 10.25)
    vals = [p['nDCG@5'] for p in points]
    ax.set_ylim(max(0, min(vals) - .07), min(1, max(vals) + .045))
    ax.xaxis.grid(False)
    ax.legend(ncol=2, loc='lower right', framealpha=.94)
    for line in ax.lines:
        assert all(ax.get_ylim()[0] <= y <= ax.get_ylim()[1] for y in line.get_ydata())
    output.mkdir(parents=True, exist_ok=True)
    fig.savefig(output / 'preview.pdf', metadata={'CreationDate': None, 'ModDate': None})
    fig.savefig(output / 'preview.png', dpi=300)
    plt.close(fig)
    description = ('Test-split nDCG@5 across replay and validation-gate conditions. '
                   'Lines show archived initial values where available and task-weighted nDCG@5 at accepted checkpoints. '
                   f'Both Enabled (optimized) and Only Gate (optimized) end at iterations {coverage["Both Enabled"]} and {coverage["Only Gate"]}, respectively. '
                   f'Both Disabled and Only MBR end at {coverage["Both Disabled"]}; Only MBR Alt ends at {coverage["Only MBR Alt"]}. '
                   'Optimized runs are in progress and analysis-only; no values beyond the latest complete checkpoint are shown.')
    (output / 'description.text').write_text(description + '\n')
    label = 'fig:mbr_replay_test_ndcg@5_temp'
    caption = 'Test-split nDCG@5 across replay and validation-gate conditions'
    (output / 'table.tex').write_text('\\begin{figure}[!htbp]\n\\centering\n'
        '\\includegraphics[width=\\linewidth]{figs/mbr_replay_test_ndcg@5_temp/preview.pdf}\n'
        f'\\caption[{caption}]{{\\input{{figs/mbr_replay_test_ndcg@5_temp/description.text}}}}\n'
        f'\\label{{{label}}}\n\\end{{figure}}\n')
    with (output / 'selected_data.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(points[0]))
        writer.writeheader()
        writer.writerows(points)
    manifest = dict(provenance, artifact='mbr_replay_test_ndcg@5_temp', metric='nDCG@5',
                    panels=['test'], coverage=coverage, n_tasks={'test': 748},
                    selected_row_count=len(points), points=points,
                    aggregation='task-macro nDCG@5 from each source run; 748 test tasks',
                    reportable=False, uncertainty='not estimated; no bands',
                    output_sha256={f: sha(output / f) for f in
                        ['preview.pdf', 'preview.png', 'description.text', 'table.tex', 'selected_data.csv']})
    (output / 'selection.json').write_text(json.dumps(manifest, indent=2) + '\n')
    optimized_lines = []
    for method in OPT_RUNS:
        info = provenance['optimized_sources'][method]
        optimized_lines.append(
            f'{method} uses optimized run {info["run"]}; latest contiguous complete accepted test checkpoint '
            f'{info["latest_contiguous_completed_iteration"]}; run status={info["completion"].get("status")}, '
            f'passed={info["completion"].get("passed")}. nDCG@5 derived from stored ranked_ids/required_ids; '
            f'test count=748. Later/unplotted checkpoints={info["later_unplotted_checkpoints"]}.')
    (output / 'provenance.text').write_text(
        'Artifact: mbr_replay_test_ndcg@5_temp\nMetric: nDCG@5; Split=test; Evaluation=accepted.\n'
        'Both Enabled and Only Gate now use their optimized RouterBSI runs; scores are task-macro nDCG@5 derived from archived test predictions.\n'
        + '\n'.join(optimized_lines) + '\n'
        'Both Disabled and Only MBR remain sourced from routing_performance_by_iteration/results.csv.\n'
        'Only MBR Alt remains from .wisc/results/GatedRouter/sra_full_skillsight_f1_i10_l400_qwen3.5_4b/run_1.\n'
        'Initial values are included only for unchanged series with archived initial-test snapshots; optimized runs have no plotted initial point.\n'
        'Coverage by method: ' + json.dumps(coverage, sort_keys=True) + '.\n'
        'No observations after each series latest verified completed checkpoint are included; no interpolation or extrapolation.\n'
        'Optimized run archives are in progress, passed=false, and reportable=false; this chart is analysis-only.\n'
        'Exact prediction, metric, ledger, and completion hashes are recorded in selection.json.\n'
        'Regenerate: uv run --script RouterBSIPaper/scripts/refresh_mbr_test_ndcg5_temp.py\n')
    print(f'PASS: {len(points)} points; optimized Both Enabled through {coverage["Both Enabled"]}; '
          f'optimized Only Gate through {coverage["Only Gate"]}; Only MBR Alt through {coverage["Only MBR Alt"]}; nDCG@5.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-table', type=Path, default=TABLE)
    parser.add_argument('--alternate-run', type=Path, default=ALT_RUN)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    run_map_path = args.source_table.parent / 'input_runs.json'
    points, initial_points, provenance = load_points(args.source_table, args.alternate_run, run_map_path)
    render(points, initial_points, args.output, provenance, provenance['coverage'])
    assert sha(args.source_table) == provenance['table_sha256']


if __name__ == '__main__':
    main()
