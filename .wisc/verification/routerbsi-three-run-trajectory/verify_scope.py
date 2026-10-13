"""Independent closure checks for the scoped RouterBSI figure refresh."""
from pathlib import Path
import hashlib,json,csv,math

HERE=Path(__file__).resolve().parent
PAPER=HERE.parents[2]
TARGET=PAPER/'figs/routerbsi_test_ndcg@1_std'

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()

def main():
    before=json.loads((HERE/'paper_before.json').read_text())
    changed=[]; missing=[]; authorized=[]
    for rel,sha in before.items():
        path=PAPER/rel
        if not path.is_file(): missing.append(rel); continue
        if digest(path)!=sha:
            (authorized if rel.startswith('figs/routerbsi_test_ndcg@1_std/') else changed).append(rel)
    refs=[]
    for path in PAPER.rglob('*.tex'):
        rel=path.relative_to(PAPER)
        if any(x in rel.parts for x in ('.wisc','.temp','.git')): continue
        if path.is_relative_to(TARGET): continue
        if 'routerbsi_test_ndcg@1_std' in path.read_text(): refs.append(str(rel))
    manifest=json.loads((TARGET/'selection_manifest.json').read_text())
    assert manifest['artifact']=='routerbsi_test_ndcg@1_std'
    assert not refs, f'Unrequested manuscript integration: {refs}'
    for name in ['table.tex','description.text','provenance.text']:
        assert 'mbr_replay_test_ndcg@1_std' not in (TARGET/name).read_text(), name
    wrapper=(TARGET/'table.tex').read_text()
    assert 'figs/routerbsi_test_ndcg@1_std/preview.pdf' in wrapper
    assert 'fig:routerbsi_test_ndcg@1_std' in wrapper
    assert 'figs/routerbsi_test_ndcg@1_std/description.text' in wrapper
    assert '\\input{figs/routerbsi_test_ndcg@1_std/table.tex}' in (HERE/'wrapper.tex').read_text()
    import fitz
    pdf=fitz.open(TARGET/'preview.pdf')
    pages=[json.loads(str(p.get_text('json'))) for p in pdf]
    spans=[s for page in pages for b in page['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']]
    assert len(pdf)==1
    assert min(s['size'] for s in spans)>=7.5
    raw=json.loads((HERE/'raw_sources_before.json').read_text())
    raw_changed=[path for path,sha in raw.items() if digest(Path(path))!=sha]
    assert not raw_changed, raw_changed
    output={
        'protected_raw_source_files':len(raw),
        'raw_source_hashes_unchanged':not raw_changed,
        'protected_existing_paper_files':len(before),
        'authorized_changed_files':authorized,
        'unrelated_concurrent_changes':changed,
        'missing_original_files':missing,
        'manuscript_pdf_unchanged':digest(PAPER/'main.pdf')==before['main.pdf'],
        'target_not_integrated_into_manuscript':not refs,
        'target_pdf_size_pt':[pdf[0].rect.width,pdf[0].rect.height],
        'min_pdf_font_pt':min(s['size'] for s in spans),
        'target_file_sha256':{p.name:digest(p) for p in TARGET.iterdir() if p.is_file()},
    }
    (HERE/'parent_preservation.json').write_text(json.dumps(output,indent=2)+'\n')
    assert not missing, missing
    # Concurrent edits are reported, never reverted or silently attributed.
    print(json.dumps(output,indent=2))

if __name__=='__main__': main()
