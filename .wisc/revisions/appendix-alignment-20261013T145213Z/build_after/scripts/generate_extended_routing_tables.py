"""Regenerate only appendix routing Tables 5--7 and retention Table 9.
Read existing captions/labels; use exact Qwen3.5 4B rows, never rerun evaluation.
"""
from pathlib import Path
import argparse
import csv

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'sections/appendix'
SOURCE = ROOT.parent / 'BayesGSI/tables'
RETRIEVERS = ['BM25', 'Vector', 'SkillSight']
METHODS = ['BASE', 'LLM Select', 'SkillRouter', 'SkillDAG', 'Skill-Pro', 'RouterBSI_init', 'RouterBSI']
DATASETS = [('theoremqa', 'logicbench'), ('toolqa', 'medcalcbench'), ('champ', 'bigcodebench')]
NAMES = dict(zip(sum((list(x) for x in DATASETS), []), ['TheoremQA', 'LogicBench', 'ToolQA', 'MedCalc-Bench', 'CHAMP', 'BigCodeBench']))
METRICS = ['Hit@1', 'nDCG@10', 'Recall@5', 'Recall@10', 'F1', 'FullCoverage@5', 'FullCoverage@10']


def load(name):
    with (SOURCE / name / 'results.csv').open() as f:
        rows = [r for r in csv.DictReader(f) if r['Model'] == 'Qwen3.5 4B']
    index = {(r['Retriever'], r['Method'], r['Dataset']): r for r in rows}
    assert len(index) == len(rows)
    return index


def label(m):
    return r'$\mathrm{RouterBSI}_{\mathrm{init}}$' if m == 'RouterBSI_init' else m


def ranked(v, peers):
    order = sorted(set(peers), reverse=True)
    s = f'{v:.3f}'
    return r'\textbf{' + s + '}' if v == order[0] else r'\underline{' + s + '}' if len(order) > 1 and v == order[1] else s


def generate():
    routing, recall = load('routing_performance'), load('routing_recall')
    outputs = {}
    for i, datasets in enumerate(DATASETS, 1):
        # Preserve labels, method order and ranking scope; place ACL captions below.
        caption = f'Test routing performance on {NAMES[datasets[0]]} and {NAMES[datasets[1]]} with Qwen3.5-4B. N, R, and FC denote nDCG, Recall, and Full Coverage, respectively; F1 is set-level F1. Bold and underlined values indicate the best and second-best scores within each retriever group.'
        lines = [r'\begin{table*}[t]', r'\centering', r'\footnotesize', r'\setlength{\tabcolsep}{2pt}', r'\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}l' + 'r' * 14 + '@{}}', r'\toprule', 'Method & ' + ' & '.join(r'\multicolumn{7}{c}{' + NAMES[d] + '}' for d in datasets) + r' \\', r'\cmidrule(lr){2-8}\cmidrule(lr){9-15}', ' & ' + ' & '.join(['N@1', 'N@10', 'R@5', 'R@10', 'F1', 'FC@5', 'FC@10'] * 2) + r' \\']
        for retriever in RETRIEVERS:
            methods = [retriever if m == 'BASE' else m for m in METHODS]
            lines += [r'\midrule', r'\multicolumn{15}{l}{\textit{' + retriever + r'}} \\', r'\midrule']
            values = {}
            for method in methods:
                values[method] = []
                for d in datasets:
                    r, c = routing[retriever, method, d], recall[retriever, method, d]
                    assert r['n_tasks'] == c['n_tasks']
                    vals = [float((c if k.startswith('Recall') else r)[k]) for k in METRICS]
                    assert all(0 <= v <= 1 for v in vals)
                    values[method].extend(vals)
            for method in methods:
                cells = [ranked(v, [values[m][j] for m in methods]) for j, v in enumerate(values[method])]
                lines.append(label(method) + ' & ' + ' & '.join(cells) + r' \\')
        lines += [r'\bottomrule', r'\end{tabular*}', r'\caption{' + caption + '}', r'\label{tab:app-routing-' + str(i) + '}', r'\end{table*}']
        outputs[f'routing_table_{i}.tex'] = '\n'.join(lines) + '\n'
    # A pure column permutation preserves all original retention precision/text.
    text = (OUT / 'retention_table.tex').read_text()
    lines = text.splitlines()
    header = next(l for l in lines if l.startswith('Retriever & Method &'))
    if header.split(' & ')[-1].startswith('Recall@50'):
        outputs['retention_table.tex'] = text
    else:
        assert header.split(' & ')[2] == 'Recall@50'
        for i, line in enumerate(lines):
            if ' & ' in line:
                assert line.endswith(r' \\')
                cells = line[:-3].split(' & ')
                assert len(cells) == 7
                lines[i] = ' & '.join(cells[:2] + cells[3:] + cells[2:3]) + r' \\'
        outputs['retention_table.tex'] = '\n'.join(lines) + '\n'
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, text in generate().items():
        p = OUT / name
        if args.check:
            assert p.read_text() == text, name
        else:
            p.write_text(text)
        print(('Verified ' if args.check else 'Wrote ') + name)


if __name__ == '__main__':
    main()
