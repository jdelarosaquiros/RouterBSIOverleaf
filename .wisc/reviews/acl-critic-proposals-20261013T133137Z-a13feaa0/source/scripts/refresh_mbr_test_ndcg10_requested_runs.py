#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib==3.10.8"]
# ///
"""Regenerate test-split nDCG@10 from the four requested GatedRouter run_1 archives."""
from pathlib import Path
import csv
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'RouterBSIPaper/.temp/mbr_replay_test_ndcg@10'
RUNS = {
    'Both Enabled': ROOT / '.wisc/results/GatedRouter/sra_full_skillsight_f1_i10_l400_qwen3.5_4b/run_1',
    'Both Disabled': ROOT / '.wisc/results/GatedRouter/sra_full_skillsight_f1_i10_l400_qwen3.5_4b_disabled_mbr_validation/run_1',
    'Only MBR': ROOT / '.wisc/results/GatedRouter/sra_full_skillsight_f1_i10_l400_qwen3.5_4b_only_mbr/run_1',
    'Only Gate': ROOT / '.wisc/results/GatedRouter/sra_full_skillsight_f1_i10_l400_qwen3.5_4b_only_val/run_1',
}
STYLES = {
    'Both Enabled': dict(color='#009E73', marker='D', linestyle='-.'),
    'Only Gate': dict(color='#D55E00', marker='s', linestyle='--'),
    'Both Disabled': dict(color='#7A7A7A', marker='^', linestyle=':'),
    'Only MBR': dict(color='#0072B2', marker='o', linestyle='-'),
}
N_TEST = 748
CUTOFF = 10


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ndcg(record):
    relevant = set(record['required_ids'])
    ranking = record['ranked_ids'][:CUTOFF]
    dcg = sum(1 / math.log2(rank + 1) for rank, skill in enumerate(ranking, 1) if skill in relevant)
    ideal = sum(1 / math.log2(rank + 1) for rank in range(1, min(CUTOFF, len(relevant)) + 1))
    return dcg / ideal if ideal else 1.0


def read_prediction(path, method, iteration, expected_ids=None):
    records = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    ids = [r['task_id'] for r in records]
    if len(ids) != N_TEST or len(set(ids)) != N_TEST:
        raise ValueError(f'{method}/{iteration}: expected {N_TEST} unique test tasks, found {len(ids)}/{len(set(ids))}')
    current = set(ids)
    if expected_ids is not None and current != expected_ids:
        raise ValueError(f'{method}: test task membership changed at iteration {iteration}')
    return records, current


def collect_series(method, run):
    completion_path = run / 'completion.json'
    completion = json.loads(completion_path.read_text())
    if completion.get('status') not in {'completed_noncanonical', 'completed'} or completion.get('passed') is not True:
        raise ValueError(f'{method}: run_1 is not completed/passed')
    if completion.get('reportable') is not False:
        raise ValueError(f'{method}: expected completed non-reportable archive')
    points, evidence = [], []
    expected_ids = None
    initial_path = run / 'predictions/initial_test.jsonl'
    if initial_path.is_file():
        records, expected_ids = read_prediction(initial_path, method, 'Initial')
        points.append({'Method': method, 'Split': 'test', 'Evaluation': 'initial_snapshot', 'Iteration': 0,
                       'n_tasks': N_TEST, 'nDCG@10': sum(ndcg(r) for r in records) / N_TEST,
                       'Source': str(initial_path), 'Source_SHA256': sha(initial_path)})
    for i in range(1, 11):
        d = run / 'iterations' / f'{i:02d}'
        metrics_path, ledger_path = d / 'metrics.json', d / 'ledger.json'
        prediction_path = d / f'test_accepted_{i:02d}.jsonl'
        if not all(p.is_file() for p in (metrics_path, ledger_path, prediction_path)):
            raise ValueError(f'{method}: missing iteration {i} evidence')
        metrics, ledger = json.loads(metrics_path.read_text()), json.loads(ledger_path.read_text())
        test = metrics.get('test_accepted', {}).get('all', {})
        if ledger.get('accepted') is not True or test.get('count') != N_TEST:
            raise ValueError(f'{method}: iteration {i} not accepted or wrong test count')
        records, expected_ids = read_prediction(prediction_path, method, i, expected_ids)
        if any(r.get('library_hash') != ledger.get('accepted_hash') for r in records):
            raise ValueError(f'{method}: iteration {i} prediction does not match ledger accepted hash')
        value = sum(ndcg(r) for r in records) / N_TEST
        stored = test.get('nDCG@10')
        if stored is not None and not math.isclose(value, float(stored), rel_tol=0, abs_tol=1e-12):
            raise ValueError(f'{method}: iteration {i} nDCG@10 disagrees with metrics.json')
        points.append({'Method': method, 'Split': 'test', 'Evaluation': 'accepted', 'Iteration': i,
                       'n_tasks': N_TEST, 'nDCG@10': value, 'Source': str(prediction_path),
                       'Source_SHA256': sha(prediction_path)})
        evidence.append({'iteration': i, 'metrics': str(metrics_path), 'metrics_sha256': sha(metrics_path),
                         'ledger': str(ledger_path), 'ledger_sha256': sha(ledger_path),
                         'accepted_hash': ledger['accepted_hash'], 'predictions': str(prediction_path),
                         'predictions_sha256': sha(prediction_path), 'test_count': len(records),
                         'stored_nDCG@10': stored, 'recomputed_nDCG@10': value})
    expected_iterations = ([0] if initial_path.is_file() else []) + list(range(1, 11))
    if [p['Iteration'] for p in points] != expected_iterations:
        raise AssertionError(f'{method}: unexpected checkpoint sequence')
    return points, {'run': str(run), 'completion': completion, 'completion_sha256': sha(completion_path),
                    'initial_test_prediction': str(initial_path) if initial_path.is_file() else None,
                    'initial_test_prediction_sha256': sha(initial_path) if initial_path.is_file() else None,
                    'latest_contiguous_completed_iteration': 10, 'checkpoint_evidence': evidence}


def render(points, sources):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'],
                         'font.size': 10, 'axes.labelsize': 11, 'legend.fontsize': 8.5,
                         'pdf.fonttype': 42, 'ps.fonttype': 42, 'axes.spines.top': False,
                         'axes.spines.right': False, 'axes.grid': True,
                         'grid.alpha': .22, 'grid.linewidth': .5, 'savefig.bbox': 'tight'})
    fig, ax = plt.subplots(figsize=(7.0, 3.65), layout='constrained')
    for method in RUNS:
        series = [p for p in points if p['Method'] == method]
        xs, ys = [p['Iteration'] for p in series], [p['nDCG@10'] for p in series]
        line, = ax.plot(xs, ys, label=method, linewidth=1.8, markersize=4.6,
                        markeredgewidth=.6, markeredgecolor='white', **STYLES[method])
        expected = ([0] if sources[method]['initial_test_prediction'] else []) + list(range(1, 11))
        assert list(line.get_xdata()) == expected and list(line.get_ydata()) == ys
    ax.set_title('Qwen3.5 4B / SkillSight — Test', fontsize=10, pad=10)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('nDCG@10')
    ax.set_xticks(range(0, 11), ['Initial'] + [str(i) for i in range(1, 11)])
    ax.set_xlim(-.25, 10.25)
    values = [p['nDCG@10'] for p in points]
    ax.set_ylim(max(0, min(values) - .07), min(1, max(values) + .045))
    ax.xaxis.grid(False)
    ax.legend(ncol=2, loc='lower right', framealpha=.94)
    assert len(ax.lines) == len(RUNS)
    for line in ax.lines:
        assert all(ax.get_ylim()[0] <= y <= ax.get_ylim()[1] for y in line.get_ydata())
    OUTPUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT / 'preview.pdf', metadata={'CreationDate': None, 'ModDate': None})
    fig.savefig(OUTPUT / 'preview.png', dpi=300)
    plt.close(fig)
    description = ('Test-split nDCG@10 across four replay and validation-gate conditions. '
                   'Lines show task-macro nDCG@10 at initialization where archived and accepted iterations 1–10. '
                   'Each condition uses run_1 from its specified GatedRouter archive. '
                   'All four runs are completed_noncanonical and non-reportable; analysis-only.')
    (OUTPUT / 'description.text').write_text(description + '\n')
    (OUTPUT / 'table.tex').write_text(
        '\\begin{figure}[!htbp]\n\\centering\n'
        '\\includegraphics[width=\\linewidth]{figs/mbr_replay_test_ndcg@10/preview.pdf}\n'
        '\\caption[Test-split nDCG@10 across replay and validation-gate conditions]{\\input{figs/mbr_replay_test_ndcg@10/description.text}}\n'
        '\\label{fig:mbr_replay_test_ndcg@10}\n\\end{figure}\n')


def main():
    points, sources = [], {}
    for method, run in RUNS.items():
        series, info = collect_series(method, run)
        points.extend(series)
        sources[method] = info
    render(points, sources)
    with (OUTPUT / 'selected_data.csv').open('w', newline='') as stream:
        fields = ['Method', 'Split', 'Evaluation', 'Iteration', 'n_tasks', 'nDCG@10', 'Source', 'Source_SHA256']
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(points)
    manifest = {'artifact': 'mbr_replay_test_ndcg@10', 'metric': 'nDCG@10', 'cutoff': 10, 'split': 'test',
                'conditions': list(RUNS), 'sources': sources,
                'coverage': {m: ([0] if sources[m]['initial_test_prediction'] else []) + list(range(1, 11)) for m in RUNS},
                'task_count': N_TEST, 'selected_row_count': len(points), 'points': points,
                'aggregation': 'Task-macro binary-relevance nDCG@10 computed from archived ranked_ids and required_ids.',
                'reportable': False, 'uncertainty': 'not estimated; one run per condition; no bands',
                'outputs_sha256': {f: sha(OUTPUT / f) for f in ['preview.pdf', 'preview.png', 'description.text', 'table.tex', 'selected_data.csv']}}
    (OUTPUT / 'selection.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (OUTPUT / 'provenance.text').write_text(
        'Artifact: mbr_replay_test_ndcg@10\nMetric: task-macro nDCG@10; cutoff=10; Split=test.\n'
        'Each condition is sourced from its specified GatedRouter run_1; exact paths and hashes are in selection.json.\n'
        'Iterations 1–10 are accepted test predictions (748 unique tasks), verified against each iteration ledger accepted_hash.\n'
        'Initial values are included only where initial_test.jsonl is archived.\n'
        'All four archives are completed_noncanonical and reportable=false; analysis-only.\n'
        'The generator reads archived data only; no inference/evaluation is run.\n'
        'Regenerate: uv run --script RouterBSIPaper/scripts/refresh_mbr_test_ndcg10_requested_runs.py\n')
    print(f'PASS: {len(points)} nDCG@10 points; four requested run_1 sources; 10 accepted test checkpoints each; initial snapshots where archived.')


if __name__ == '__main__':
    main()
