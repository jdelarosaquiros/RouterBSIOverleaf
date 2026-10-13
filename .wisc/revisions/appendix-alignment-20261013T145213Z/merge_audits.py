"""Merge independently read appendix coverage; preserve unresolved factual boundaries."""
from pathlib import Path
import json,collections,re
R=Path(__file__).resolve().parent
ROOT=R.parents[2]
load=lambda f:json.loads((R/f).read_text())
active=load('active_inventory.json');numbered=load('numbered_subsections.json');edits=load('edits_approved.json')
entries={}
for label in 'ABC':
 data=load('audit_'+label+'.json')
 for item in data['files']:
  path=item['file']
  if path.startswith(str(ROOT)+'/'):path=path[len(str(ROOT))+1:]
  if not path.startswith('sections/appendix/'):path='sections/appendix/'+path
  item['file']=path
  item['reviewer_group']=label
  assert path not in entries,('duplicate coverage',path)
  entries[path]=item
# Root include wrapper is verified by the parent recursive source traversal.
wrapper='sections/appendix/appendix.tex'
entries.setdefault(wrapper,{'file':wrapper,'headings':[],'main_anchors':['main.tex:74'],'assessment':'All eight appendix section wrappers are active after references; no main-source edits needed.','action':'keep','proposed_edits':[],'unresolved':[],'reviewer_group':'parent'})
assert set(entries)==set(active['active_files']),{'missing':sorted(set(active['active_files'])-set(entries)),'extra':sorted(set(entries)-set(active['active_files']))}
unresolved=[
 {'id':'INIT','kind':'evidence conflict','appendix':['G.1'],'main':'Figure 5 caption; sections/ablations.tex','description':'The main caption and appendix agree textually on shared initialization. The separate artifact audit found different saved initial predicate libraries across the three Both Enabled runs, while the other configurations reuse the first run\'s library. Their historical binding to Figure 5 remains unresolved. The existing manuscript sentence is unchanged.','needed':'Immutable historical initialization bindings demonstrating that different runs produced Figure 5, or authorization for a truthful correction of the main caption and appendix.'},
 {'id':'REPLAY','kind':'definition mismatch','appendix':['A.2','A.3','A.5','D.1','D.3','G.2'],'main':'Section 4.2 replay-set equation and replay description','description':'Main defines the scoring set as two historical buckets, each bounded by N. Appendix includes the current task as well, with up to 2N+1 distinct tasks. Main also describes error over tasks retrieving the skill, while appendix history construction does not state that retrieval restriction. No scored task or bound was removed to force textual agreement.','needed':'Clarify the intended experimental definition and authorize any necessary main-text correction; no new run is automatically required.'},
 {'id':'RANK','kind':'general rule mismatch','appendix':['A.1'],'main':'Sections 5.4 and 5.5 label-plus-retrieval-score rule','description':'Appendix specifies selected-first lexicographic ranking. It explains equivalence to additive labels for SkillSight reciprocal-rank scores, but arbitrary raw-score addition is not generally equivalent across retrievers.','needed':'Confirm per-retriever scoring transformations or authorize a main-rule clarification.'},
 {'id':'SPLIT','kind':'allocation-description mismatch','appendix':['C.1'],'main':'Section 5.1 per-dataset 70/15/15 statement','description':'Appendix reports a constrained global 3491/748/748 allocation and non-70/15/15 per-dataset final counts. Numeric counts and coverage constraints were preserved.','needed':'Clarify target versus final per-dataset ratios in the main text; appendix wording now states the allocation without editorial precedence commentary.'},
 {'id':'TRAIN','kind':'main-internal inconsistency','appendix':['D.4'],'main':'Section 5.4 trained retrievers versus Section 5.5 pretrained/lexical no-training statement','description':'The frozen main paper gives incompatible retriever-training descriptions. Appendix reports concrete retrieval/evaluation settings without inventing task-split training.','needed':'Confirm actual fitting scope and authorize resolution of the main-text inconsistency.'}
]
notes=[
 {'topic':'Backbone ceiling','appendix':'G.4','status':'supported numerical expansion retained; unsupported main inference not propagated','detail':'The appendix confirms the endpoint ordering and 99.64% ratio, consistent with rounded main values. These endpoints alone do not establish an irreducible capacity ceiling.'},
 {'topic':'F1 and fixed-budget outputs','appendix':'E.1 / H.5 / H.6','status':'useful metric and set distinctions retained','detail':'Selected-set F1 differs from F1@k; top-k can pad or truncate the selected set. These explanations prevent misreading simplified main wording.'},
 {'topic':'Token scope and uncertainty','appendix':'E.1 / G.2 / G.3','status':'scientifically material qualifications retained','detail':'Recorded token counts are not complete cost accounts, single-run results are distinct from three-run component means, and model adjudication is not human-validated accuracy.'}
]
subs=[]
for item in numbered:
 e=entries[item['file']];after=(ROOT/item['file']).read_text();match=re.search(r'\\subsection\{([^}]+)\}',after)
 assert match is not None,item['file']
 title=match.group(1)
 item=dict(item);item['heading_after']=title;item['main_anchors']=e.get('main_anchors',[]);item['assessment']=e.get('assessment','');item['edits']=[x for x in edits if x['file']==item['file']];item['unresolved_ids']=[u['id'] for u in unresolved if item['id'] in u['appendix']];item['status']='edited_with_unresolved_alignment' if item['edits'] and item['unresolved_ids'] else 'unresolved_alignment' if item['unresolved_ids'] else 'edited' if item['edits'] else 'reviewed_unchanged'
 subs.append(item)
result={'scope':'appendix-only source revisions; no new experiments; original main PDF not rebuilt','files':[entries[f] for f in active['active_files']],'subsections':subs,'unresolved':unresolved,'retained_interpretation_notes':notes,'counts':{'active_tex_files':len(entries),'active_subsections':len(subs),'edited_files':len({x['file'] for x in edits}),'exact_replacements':len(edits),'unresolved_items':len(unresolved)}}
(R/'subsection_audit.json').write_text(json.dumps(result,indent=2))
lines=['# Appendix alignment audit','','## Scope','All active appendix subsection files and their table/wrapper inputs were checked against the frozen main paper. Edits remove process narration and improve cross-references without changing experimental values. Full scientific alignment is **not certified**: the unresolved items below require evidence or main-text authorization.','','## Every subsection','| Appendix | Subsection | Result | Unresolved |','|---|---|---|---|']
for x in subs:lines.append('| '+x['id']+' | '+x['heading_after']+' | '+x['status'].replace('_',' ')+' | '+(', '.join(x['unresolved_ids']) or 'None identified in this source audit')+' |')
lines+=['','## Unresolved factual alignment']
for x in unresolved:lines+=['','### '+x['id']+' — '+x['kind'],'**Locations:** '+', '.join(x['appendix'])+'; '+x['main'],x['description'],'**Needed:** '+x['needed']]
lines+=['','## Retained qualifications']
for x in notes:lines+=['','- **'+x['topic']+' ('+x['appendix']+'):** '+x['detail']]
lines+=['','## Per-subsection evidence and actions']
for x in subs:
 lines+=['','### '+x['id']+' '+x['heading_after'],'Source: `'+x['file']+'`','Main anchors: '+json.dumps(x['main_anchors']),str(x['assessment'])]
 for e in x['edits']:lines+=['','**Change:** '+e['reason'],'','Before:','```tex',e['old'],'```','After:','```tex',e['new'] or '[removed]','```']
(R/'APPENDIX_AUDIT.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(result['counts'],indent=2))
