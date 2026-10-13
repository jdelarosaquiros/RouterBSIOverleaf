"""Read-only numerical coverage check for the five active result figures.
Writes the audit report only when --report PATH is supplied.
"""
from pathlib import Path
from fractions import Fraction
import argparse
import csv
import hashlib
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'sections/appendix'
NAMES = ['average_retention_degradation', 'downstream_average', 'mbr_replay_test_ndcg@1_std', 'performance_token_usage', 'routing_performance_across_llms_init']

def load(name):
    folder = ROOT/'figs'/name
    selection = folder/('selection.json' if (folder/'selection.json').exists() else 'selection_manifest.json')
    d = json.loads(selection.read_text())
    source = d['source']
    path = ROOT.parent/(source['path'] if isinstance(source,dict) else source)
    expected = source['sha256'] if isinstance(source,dict) else d['source_sha256']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, f'Changed source: {name}'
    return d

def cells(filename):
    text = (APP/filename).read_text()
    for inc in re.findall(r'\\input\{([^}]+)\}',text):
        text += '\n' + (ROOT/(inc+'.tex')).read_text()
    return [line.split('&') for line in text.splitlines() if '&' in line and not line.lstrip().startswith('\\caption')]

def numbers(cell):
    return [float(x) for x in re.findall(r'(?<![A-Za-z])\d+\.\d+',cell)]

def match(x, value, digits=3):
    assert x == float(f'{value:.{digits}f}'), (x,value,digits)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--report', type=Path);args=parser.parse_args()
    reports=[]
    # Retention: explicitly recompute each ratio before equal-weight retriever averaging.
    d=load(NAMES[0]);rows=cells('retention_mean_table.tex');ks=[1,5,10,25,50]
    for point in d['points']:
        method = 'Retriever' if point['Method']=='Retriever baseline' else point['Method']
        row=next(r for r in rows if r[0].strip()==method)
        value=sum(Fraction(str(op['numerator']))/Fraction(str(op['denominator'])) for op in point['source_operands'])*100/3
        assert math.isclose(float(value), point['y'],abs_tol=1e-10)
        match(numbers(row[ks.index(point['x'])+1])[0],float(value),1)
    reports.append(dict(figure=NAMES[0],table='tab:app-retention-mean',points=len(d['points']),metric='100 * Recall@k / Recall@50 per retriever; arithmetic mean of three ratios',status='PASS'))
    # Downstream: exact pooled counts within retriever, arithmetic mean between retrievers.
    d=load(NAMES[1]); rows=cells('downstream_mean_table.tex')
    for point in d['selected_rows']:
        method=point['method']
        if method=='Retriever baseline': key='Retriever'
        elif method=='RouterBSI strict': key=r'$\mathrm{RouterBSI}_{\mathrm{strict}}$'
        elif method=='RouterBSI top-5': key=r'$\mathrm{RouterBSI}_{\mathrm{top}5}$'
        else:key=method
        row=next(r for r in rows if r[0].strip()==key)
        values=[]
        for j,retriever in enumerate(['BM25','Vector','SkillSight']):
            op=next(x for x in point['retriever_values'] if x['retriever']==retriever)
            value=Fraction(sum(int(r['Correct']) for r in op['constituent_rows']),sum(int(r['n_tasks']) for r in op['constituent_rows']))
            assert value==Fraction(op['correct'],op['n_tasks'])
            match(numbers(row[j+1])[0],float(value));values.append(value)
        mean=sum(values)/3;assert math.isclose(float(mean),point['accuracy'],abs_tol=1e-12)
        match(numbers(row[4])[0],float(mean))
    for ref in d['reference_methods']:
        row=next(r for r in rows if r[0].strip()==ref['method'])
        match(numbers(row[1])[0],ref['correct']/ref['n_tasks'])
    reports.append(dict(figure=NAMES[1],table='tab:app-downstream-mean',points=len(d['selected_rows'])+len(d['reference_methods']),metric='pooled task success per retriever; equal-weight mean of three retrievers; two independent references',status='PASS'))
    # Trajectory: preserve the exact uncertainty rendered, sqrt of serialized variance.
    d=load(NAMES[2]);rows=cells('ablation_components.tex')
    header=next(r for r in rows if r[0].strip()=='Iteration')
    order=[re.sub(r'\\\\.*','',x).strip() for x in header[1:]]
    for point in d['points']:
        row=next(r for r in rows if r[0].strip()==str(point['x']))
        values=numbers(row[order.index(point['Method'])+1]);assert len(values)==2,(point,values)
        match(values[0],float(point['Hit@1_mean']))
        sd=math.sqrt(float(point['Hit@1_variance']))
        assert math.isclose(sd,float(point['Hit1_std']),abs_tol=1e-14)
        match(values[1],sd)
    reports.append(dict(figure=NAMES[2],table='tab:app-ablation-trajectory',points=len(d['points']),uncertainty_values=len(d['points']),metric='nDCG@1 (source Hit@1), task-weighted test means then three-run mean; population SD from plotted variance',status='PASS'))
    # Cost plot: both coordinates must appear, not just the quality metric.
    d=load(NAMES[3]);rows=cells('ablation_cost_capacity.tex')
    for point in d['points']:
        row=next(r for r in rows if r[0].strip()==point['Method'])
        match(numbers(row[2])[0],point['y']);match(numbers(row[3])[0],point['x'])
        assert point['x']==int(point['total_tokens'])/1000000
    reports.append(dict(figure=NAMES[3],table='tab:app-ablation-tokens',points=len(d['points']),coordinates_per_point=2,metric='final-test nDCG@1 (source Hit@1) and known run-local total tokens / 1e6; one run',status='PASS'))
    # Backbone: include reference bar in addition to initial/final pairs.
    d=load(NAMES[4]);rows=cells('ablation_backbones.tex')
    for point in d['points']:
        if point['Method']=='SkillSight':row=next(r for r in rows if 'SkillSight' in r[0])
        else:
            stage='Initial' if point['Method']=='RouterBSI_init' else 'Final'
            row=next(r for r in rows if r[0].strip()==point['Model'] and r[1].strip()==stage)
        match(numbers(row[3])[0],point['y'])
    reports.append(dict(figure=NAMES[4],table='tab:app-backbone',points=len(d['points']),metric='nDCG@1 (source Hit@1); task-weighted test rate per model/stage, no averaging between models',status='PASS'))
    assert [r['points'] for r in reports]==[30,9,44,4,7]
    result={'figures':reports,'figure_count':len(reports),'plotted_points_and_references':sum(r['points'] for r in reports),'scope':'All active numerical result/ablation figures; excludes two conceptual diagrams and inactive archived figures.'}
    if args.report:
        args.report.parent.mkdir(exist_ok=True,parents=True);args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
