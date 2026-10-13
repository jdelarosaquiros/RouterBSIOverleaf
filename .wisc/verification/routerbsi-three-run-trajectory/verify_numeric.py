"""Compare final exported values against independent scout and archived series."""
from pathlib import Path
import csv,json,math,hashlib
HERE=Path(__file__).resolve().parent
PAPER=HERE.parents[2]
TARGET=PAPER/'figs/routerbsi_test_ndcg@1_std'

def main():
    scout=json.loads((HERE/'scout.json').read_text())
    rows=list(csv.DictReader((TARGET/'selected_data.csv').open()))
    per_run=list(csv.DictReader((TARGET/'per_run_data.csv').open()))
    assert len(rows)==12 and len(per_run)==36
    for i,(row,independent) in enumerate(zip(rows,scout['table'])):
        expected='initial' if i==0 else 'final' if i==11 else str(i)
        assert row['checkpoint']==expected
        for key,other in [('mean','mean'),('population_sd','population_sd')]:
            assert math.isclose(float(row[key]),independent[other],rel_tol=0,abs_tol=1e-15),(i,key)
        for run,value in zip(['run_1','run_2','run_3'],independent['scores_by_run']):
            assert float(row[run])==value,(i,run)
            matched=[r for r in per_run if r['run']==run and r['checkpoint']==expected]
            assert len(matched)==1 and float(matched[0]['ndcg1'])==value
    manifest=json.loads((TARGET/'selection_manifest.json').read_text())
    assert manifest['generator_sha256']==hashlib.sha256((TARGET/'generate.py').read_bytes()).hexdigest()
    for name,expected in manifest['output_sha256'].items():
        assert hashlib.sha256((TARGET/name).read_bytes()).hexdigest()==expected,name
    for path,record in manifest['inputs'].items():
        assert hashlib.sha256((PAPER.parent/path).read_bytes()).hexdigest()==record['sha256'],path
    result={'points_checked':len(rows),'run_checkpoint_values_checked':len(per_run),
            'all_values_match_independent_scout':True,
            'raw_inputs_and_output_hashes_verified':True,
            'generator_hash_verified':True,
            'initial':{'mean':float(rows[0]['mean']),'population_sd':float(rows[0]['population_sd'])},
            'final':{'mean':float(rows[-1]['mean']),'population_sd':float(rows[-1]['population_sd'])}}
    (HERE/'numeric_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
