#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib==3.10.8"]
# ///
"""Build separate temporary nDCG@5 charts for train, validation, and test."""
from pathlib import Path
import csv
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'RouterBSIPaper/.temp/mbr_replay_test_ndcg@5_temp_all_split'
RUNS = {
    'Both Enabled': ROOT / '.wisc/results/RouterBSI/sra_full_skillsight_f1_i10_l400_qwen3.5_4b_optimized/run_1',
    'Only Gate': ROOT / '.wisc/results/RouterBSI/sra_full_skillsight_f1_i10_l400_qwen3.5_4b_optimized_gate_only/run_1',
    'Both Disabled': ROOT / '.wisc/results/GatedRouter/sra_full_skillsight_f1_i10_l400_qwen3.5_4b_disabled_mbr_validation/run_1',
    'Only MBR': ROOT / '.wisc/results/GatedRouter/sra_full_skillsight_f1_i10_l400_qwen3.5_4b_only_mbr/run_1',
    'Only MBR Alt': ROOT / '.wisc/results/GatedRouter/sra_full_skillsight_f1_i10_l400_qwen3.5_4b/run_1',
}
STYLE = {
    'Both Enabled': dict(color='#009E73', marker='D', linestyle='-.'),
    'Only Gate': dict(color='#D55E00', marker='s', linestyle='--'),
    'Both Disabled': dict(color='#7A7A7A', marker='^', linestyle=':'),
    'Only MBR': dict(color='#0072B2', marker='o', linestyle='-'),
    'Only MBR Alt': dict(color='#CC79A7', marker='X', linestyle=(0, (4, 1.5))),
}
SPLIT_COUNTS = {'train': 3491, 'validation': 748, 'test': 748}
STAGES = {'train': 'prequential', 'validation': 'accepted_candidate', 'test': 'accepted'}


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


def ndcg5(record):
    relevant = set(record['required_ids'])
    ranking = record['ranked_ids'][:5]
    dcg = sum(1 / math.log2(rank + 1) for rank, skill in enumerate(ranking, 1) if skill in relevant)
    ideal = sum(1 / math.log2(rank + 1) for rank in range(1, min(5, len(relevant)) + 1))
    return dcg / ideal if ideal else 1.0


def records_and_hash(path, iteration=None):
    chosen, raw = [], []
    with path.open('rb') as stream:
        for line in stream:
            if not line.strip():
                continue
            record = json.loads(line)
            if iteration is None or record.get('iteration') == iteration:
                chosen.append(record)
                raw.append(line)
    return chosen, sha_bytes(b''.join(raw))


def validate_records(method, split, iteration, records):
    expected = SPLIT_COUNTS[split]
    ids = [r['task_id'] for r in records]
    if len(ids) != expected or len(set(ids)) != expected:
        raise ValueError(f'{method}/{split}/{iteration}: expected {expected} unique tasks, found {len(ids)}/{len(set(ids))}')
    values = [ndcg5(r) for r in records]
    return sum(values) / len(values), set(ids)


def collect():
    points, source_info = [], {}
    for method, run in RUNS.items():
        completion_path = run / 'completion.json'
        completion = json.loads(completion_path.read_text())
        if completion.get('status') not in {'completed_noncanonical', 'completed', 'in_progress'}:
            raise ValueError(f'Unexpected completion status for {method}: {completion.get("status")}')
        max_iter = 0
        evidence = []
        split_task_ids = {s: None for s in SPLIT_COUNTS}
        i = 1
        while True:
            d = run / 'iterations' / f'{i:02d}'
            metric_path, ledger_path = d / 'metrics.json', d / 'ledger.json'
            val_path, test_path = d / 'validation_candidate.jsonl', d / f'test_accepted_{i:02d}.jsonl'
            train_path = run / 'prequential.jsonl'
            if not all(x.is_file() for x in [metric_path, ledger_path, val_path, test_path, train_path]):
                break
            metrics = json.loads(metric_path.read_text())
            ledger = json.loads(ledger_path.read_text())
            if ledger.get('accepted') is not True:
                break
            train_records, train_hash = records_and_hash(train_path, i)
            val_records, val_hash = records_and_hash(val_path)
            test_records, test_hash = records_and_hash(test_path)
            by_split = {'train': (train_records, train_hash), 'validation': (val_records, val_hash), 'test': (test_records, test_hash)}
            for split, (records, digest) in by_split.items():
                score, ids = validate_records(method, split, i, records)
                if split == 'train':
                    metric_count = metrics['train_prequential']['all']['count']
                elif split == 'validation':
                    metric_count = metrics['validation_accepted']['all']['count']
                else:
                    metric_count = metrics['test_accepted']['all']['count']
                if metric_count != SPLIT_COUNTS[split]:
                    raise ValueError(f'{method}/{split}/{i}: metrics task count mismatch')
                reference = split_task_ids[split]
                if reference is None:
                    split_task_ids[split] = ids
                elif ids != reference:
                    raise ValueError(f'{method}/{split}: task membership changed at iteration {i}')
                points.append({'Method': method, 'Split': split, 'Iteration': i, 'Evaluation': STAGES[split], 'n_tasks': len(records), 'nDCG@5': score, 'Source': str(train_path if split == 'train' else val_path if split == 'validation' else test_path), 'Source_SHA256': digest, 'Source_SHA256_Scope': f'raw {split} records for iteration {i}' if split == 'train' else 'whole prediction JSONL'})
            evidence.append({'iteration': i, 'metrics': str(metric_path), 'metrics_sha256': sha(metric_path), 'ledger': str(ledger_path), 'ledger_sha256': sha(ledger_path), 'candidate_hash': ledger['candidate_hash'], 'accepted_hash': ledger['accepted_hash'], 'candidate_equals_accepted': ledger['candidate_hash'] == ledger['accepted_hash'], 'prediction_hashes': {'train': train_hash, 'validation_candidate': val_hash, 'test_accepted': test_hash}, 'task_counts': SPLIT_COUNTS})
            max_iter = i
            i += 1
        if not max_iter:
            raise ValueError(f'No complete accepted checkpoints for {method} at {run}')
        source_info[method] = {'run': str(run), 'completion': completion, 'completion_sha256': sha(completion_path), 'latest_contiguous_completed_iteration': max_iter, 'checkpoints': evidence}
    return points, source_info


def render(points, source_info):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'], 'font.size': 10, 'axes.labelsize': 11, 'legend.fontsize': 8.5, 'pdf.fonttype': 42, 'ps.fonttype': 42, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True, 'grid.alpha': .22, 'grid.linewidth': .5, 'savefig.bbox': 'tight'})
    OUT.mkdir(parents=True, exist_ok=True)
    outputs = []
    coverage = {s: {m: info['latest_contiguous_completed_iteration'] for m, info in source_info.items()} for s in SPLIT_COUNTS}
    for split in SPLIT_COUNTS:
        fig, ax = plt.subplots(figsize=(7.0, 3.65), layout='constrained')
        for method in RUNS:
            data = sorted((p for p in points if p['Split'] == split and p['Method'] == method), key=lambda p: p['Iteration'])
            expected = list(range(1, coverage[split][method] + 1))
            assert [p['Iteration'] for p in data] == expected
            line, = ax.plot([p['Iteration'] for p in data], [p['nDCG@5'] for p in data], label=method, linewidth=1.8, markersize=4.6, markeredgewidth=.6, markeredgecolor='white', **STYLE[method])
            assert list(line.get_xdata()) == expected
        ax.set_title(f'Qwen3.5 4B / SkillSight — {split.capitalize()}', fontsize=10, pad=10)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('nDCG@5')
        ax.set_xticks(range(1, 11))
        ax.set_xlim(.75, 10.25)
        vals = [p['nDCG@5'] for p in points if p['Split'] == split]
        ax.set_ylim(max(0, min(vals) - .07), min(1, max(vals) + .045))
        ax.xaxis.grid(False)
        ax.legend(ncol=2, loc='lower right', framealpha=.94)
        for line in ax.lines:
            assert all(ax.get_ylim()[0] <= y <= ax.get_ylim()[1] for y in line.get_ydata())
        pdf, png = OUT / f'{split}.pdf', OUT / f'{split}.png'
        fig.savefig(pdf, metadata={'CreationDate': None, 'ModDate': None})
        fig.savefig(png, dpi=300)
        plt.close(fig)
        outputs.extend([pdf.name, png.name])
    return coverage, outputs


def main():
    points, source_info = collect()
    coverage, outputs = render(points, source_info)
    fields = ['Method', 'Split', 'Iteration', 'Evaluation', 'n_tasks', 'nDCG@5', 'Source', 'Source_SHA256', 'Source_SHA256_Scope']
    with (OUT / 'selected_data.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(points)
    outputs.append('selected_data.csv')
    coverage_counts = {s: {m: len([p for p in points if p['Split'] == s and p['Method'] == m]) for m in RUNS} for s in SPLIT_COUNTS}
    manifest = {'artifact': 'mbr_replay_test_ndcg@5_temp_all_split', 'metric': 'nDCG@5', 'panels': list(SPLIT_COUNTS), 'coverage': coverage, 'point_counts': coverage_counts, 'task_counts': SPLIT_COUNTS, 'points': points, 'point_count': len(points), 'sources': source_info, 'aggregation': 'Task-macro nDCG@5 computed from each archived split prediction record ranked_ids/required_ids.', 'evaluation_semantics': {'train': 'prequential records filtered by iteration', 'validation': 'candidate-state validation predictions (not necessarily accepted state)', 'test': 'accepted test predictions'}, 'reportable': False, 'caveat': 'Both Enabled and Only Gate optimized archives are in progress and reportable=false; remaining ablation curves use completed_noncanonical GatedRouter archives and reportable=false. The chart is analysis-only. No interpolation or extrapolation.', 'outputs_sha256': {name: sha(OUT / name) for name in outputs}}
    (OUT / 'selection.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (OUT / 'description.text').write_text('Separate train, validation, and test nDCG@5 charts with all five ablation conditions. Each line ends at that run’s latest contiguous accepted checkpoint. Training is prequential, validation shows the candidate-state predictions for each iteration (which may differ from the accepted state), and test uses accepted predictions. All runs are analysis-only/non-reportable; run-family provenance is recorded per condition.\n')
    (OUT / 'provenance.text').write_text('Generator: RouterBSIPaper/scripts/refresh_mbr_ndcg5_all_splits_temp.py\nAll five conditions are shown in every split. Exact source run paths, statuses, checkpoints, hashes, and plotted values are in selection.json and selected_data.csv.\nNo inference or evaluation was run during figure generation.\n')
    print(f'PASS: three split charts; {len(points)} points; all five conditions shown for train, validation, and test; endpoints={coverage}')


if __name__ == '__main__':
    main()
