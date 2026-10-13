"""Generate appendix numeric companions from frozen result-figure selections.

Run from any directory: python3 scripts/generate_result_figure_tables.py [--check]
Never writes source CSVs, figure selections, or artwork.
"""
from pathlib import Path
from fractions import Fraction
import argparse
import json
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'sections/appendix'
ALIASES = {'Retriever baseline': 'Retriever', 'RouterBSI strict': r'$\mathrm{RouterBSI}_{\mathrm{strict}}$', 'RouterBSI top-5': r'$\mathrm{RouterBSI}_{\mathrm{top}5}$'}


def retention():
    data = json.loads((ROOT / 'figs/average_retention_degradation/selection.json').read_text())
    methods = list(dict.fromkeys(p['Method'] for p in data['points']))
    ks = [1, 5, 10, 25, 50]
    assert len(methods) == 6 and len(data['points']) == 30
    points = {(p['Method'], p['x']): p for p in data['points']}
    lines = [r'\begin{table}[t]', r'\centering', r'\small',
             r'\setlength{\tabcolsep}{3pt}',
             r'\begin{tabular}{lrrrrr}', r'\toprule',
             r'Method & @1 & @5 & @10 & @25 & @50 \\', r'\midrule']
    for method in methods:
        values = []
        for k in ks:
            p = points[method, k]
            operands = p['source_operands']
            assert {x['Retriever'] for x in operands} == {'BM25', 'Vector', 'SkillSight'}
            value = sum(100 * Fraction(str(x['numerator'])) / Fraction(str(x['denominator'])) for x in operands) / 3
            assert math.isclose(float(value), p['y'], abs_tol=1e-10)
            values.append(f'{float(value):.1f}')
        lines.append(ALIASES.get(method, method) + ' & ' + ' & '.join(values) + r' \\')
    lines += [r'\bottomrule', r'\end{tabular}', r'\caption{Mean retention across BM25, Vector, and SkillSight for all cutoffs in Figure~\ref{fig:average_recall_degradation}. Values are percentages. For each retriever, Ret@$k$ is $100\,\mathrm{Recall}@k/\mathrm{Recall}@50$ using task-mean recalls; the table averages the three ratios equally.}', r'\label{tab:app-retention-mean}', r'\end{table}', '']
    return '\n'.join(lines)


def downstream():
    data = json.loads((ROOT / 'figs/downstream_average/selection.json').read_text())
    assert len(data['selected_rows']) == 7 and len(data['reference_methods']) == 2
    retrievers = ['BM25', 'Vector', 'SkillSight']
    rows = []
    for row in data['selected_rows']:
        by_r = {r['retriever']: r for r in row['retriever_values']}
        assert set(by_r) == set(retrievers)
        values = []
        for r in retrievers:
            x = by_r[r]
            assert x['n_tasks'] == 748
            assert sum(int(y['Correct']) for y in x['constituent_rows']) == x['correct']
            assert sum(int(y['n_tasks']) for y in x['constituent_rows']) == x['n_tasks']
            values.append(Fraction(x['correct'], x['n_tasks']))
        mean = sum(values) / 3
        assert math.isclose(float(mean), row['accuracy'], abs_tol=1e-12)
        rows.append((row['method'], values + [mean]))
    rankings = [sorted({values[j] for _, values in rows}, reverse=True)[:2] for j in range(4)]
    def cell(x, j):
        s = f'{float(x):.3f}'
        return r'\textbf{' + s + '}' if x == rankings[j][0] else (r'\underline{' + s + '}' if x == rankings[j][1] else s)
    lines = [r'\begin{table}[!htbp]', r'\centering', r'\small',
             r'\setlength{\tabcolsep}{3pt}',
             r'\begin{tabular}{lrrrr}', r'\toprule',
             r'Method & BM25 & Vector & SkillSight & Mean \\', r'\midrule']
    for method, values in rows:
        lines.append(ALIASES.get(method, method) + ' & ' + ' & '.join(cell(x, j) for j, x in enumerate(values)) + r' \\')
    lines += [r'\midrule']
    for ref in data['reference_methods']:
        value = Fraction(ref['correct'], ref['n_tasks'])
        assert abs(float(value)-ref['accuracy']) < 0.00000051
        lines.append(ref['method'] + r' & \multicolumn{4}{c}{' + f'{float(value):.3f}' + r' (retriever-independent)} \\')
    lines += [r'\bottomrule', r'\end{tabular}', r'\caption{Downstream success rates underlying Figure~\ref{fig:downstream_average}. Each retriever column pools 748 test tasks; Mean averages the three retriever rates equally, rather than averaging benchmark rates. Bold and underline identify the best and second-best methods within each column, excluding the retriever-independent reference conditions.}', r'\label{tab:app-downstream-mean}', r'\end{table}', '']
    # Share the existing wide appendix-float queue instead of creating an
    # isolated single-column float page immediately before the detailed table.
    lines[0] = r'\begin{table*}[t]'
    lines[-2] = r'\end{table*}'
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    outputs = {'retention_mean_table.tex': retention(), 'downstream_mean_table.tex': downstream()}
    for name, text in outputs.items():
        p = OUT / name
        if args.check:
            assert p.read_text() == text, f'Stale table: {name}'
        else:
            p.write_text(text)
        print(('Verified ' if args.check else 'Wrote ') + name)


if __name__ == '__main__':
    main()
