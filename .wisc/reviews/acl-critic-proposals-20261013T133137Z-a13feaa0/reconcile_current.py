"""Capture concurrent revision and refresh the current review; never edits paper files."""
from pathlib import Path
import json,hashlib,shutil,re,collections,copy
import fitz
R=Path(__file__).resolve().parent; ROOT=R.parents[2]
load=lambda n:json.loads((R/n).read_text())
J=load('REVIEW_JSON.json');F=load('REVISION_REPORT.json');before=load('protected_before.json')
C=R/'current_snapshot';C.mkdir(exist_ok=True)
paths=set(before)|{'sections/appendix/data_scope.tex','sections/appendix/implementation_software.tex'}
current={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(paths)}
shutil.copy2(ROOT/'main.pdf',C/'main.pdf')
for p in (R/'source').rglob('*'):
 if p.is_file():
  rel=p.relative_to(R/'source');dest=C/'source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,dest)
for rel in paths-set(before):
 dest=C/'source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,dest)
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in current.items())
changes=[p for p,h in before.items() if current[p]!=h]
D={'initial_pdf_sha256':J['provenance']['pdf_sha256'],'initial_pages':29,'current_pdf_sha256':current['main.pdf'],'current_pages':len(fitz.open(C/'main.pdf')),'changed_preexisting_files':changes,'new_paper_source_files':sorted(paths-set(before)),'review_actions_modified_manuscript':False,'attribution':'Changes were detected outside this review-only action set; actor not inferred.','resolved_issue_ids':['ISSUE-001'],'partially_addressed_issue_ids':['ISSUE-006','ISSUE-007'],'notes':['New PDF contains already-corrected non-increasing replay wording, narrowed objective and equality-aware Figure 2 caption.','New Appendix D.4 specifies BM25/vector/SkillSight, SkillRouter input truncation and frozen released 0.6B reranker, task evaluators, ReAct defaults and split software.','New Appendix E.1 explicitly describes single runs, no significance tests and non-distinct-seed repetitions. Paired uncertainty remains unavailable.','New Appendix C.4 discusses language scope, constituent licenses and privacy/safety boundaries. Actual compliance and portal forms still need human verification.']}
(R/'concurrent_changes.json').write_text(json.dumps(D,indent=2));(C/'protected_baseline.json').write_text(json.dumps(current,indent=2))
# Keep the pre-drift draft for provenance, not as current advice.
H=R/'initial_review_draft';H.mkdir(exist_ok=True)
for name in ['REVIEW_JSON.json','REVISION_REPORT.json']:shutil.copy2(R/name,H/name)
J['issues']=[x for x in J['issues'] if x['id']!='ISSUE-001'];X={x['id']:x for x in J['issues']}
x=X['ISSUE-006'];x['severity']='minor';x['problem']='The main setup still contradicts itself on retriever training and leaves two listed models without a clear role, although the new appendix now specifies baseline and task-evaluation software.'
x['reasoning_chain']=['Step 1: Main Section 5.4 says retrievers are trained, whereas 5.5 says pretrained/lexical retrievers need no training. Section 5.3 lists five models but the backbone comparison reports three.','Step 2: The concurrent Appendix D.4 now specifies the released frozen 0.6B SkillRouter reranker, its input fields and limits, retrieval implementations and task evaluators. The earlier claim of wholly missing operational baseline/evaluator detail is no longer current.','Step 3: Correct the conflicting main antecedent, point to D.4 and map the remaining models to verified experiment roles. This is a remaining reporting alignment issue, not proof of an invalid comparison.']
x['fix']['instruction']='Use Appendix D.4 to correct the main train/freeze statement and insert one concise SkillRouter description/cross-reference. Ask for the actual experiment roles of Llama-3.3-70B-Instruct and GPT-5.4; remove unused names from the evaluated-model statement if appropriate. Do not duplicate the newly added software/evaluator paragraphs.'
x['fix']['target_text']='We use frozen BM25, vector and SkillSight retrieval implementations. SkillRouter reranks the retrieved candidates with its released 0.6B model in evaluation mode without gradients; Appendix D.4 specifies inputs and software. Model roles for the remaining listed models must be confirmed before adding definitive text.'
x['fix']['required_inputs']=['Author-confirmed roles for Llama-3.3-70B-Instruct and GPT-5.4; confirmation the described frozen components match reported runs.']
x['fix']['acceptance_criteria']=['The main train/freeze statements agree with Appendix D.4.','SkillRouter has a concise main description and appendix pointer.','Every model listed in the main setup maps to a verified role or is removed as unused.'];x['proposal_class']='remaining_alignment_after_concurrent_revision'
x=X['ISSUE-007'];x['reasoning_chain'][0]='Step 1: Table 1 and Figure 4 report primary comparison point estimates. Newly added Appendix E.1 explicitly says these are single evaluations, not repeated seeds, and that statistical-significance tests are not reported; it correctly labels component bands as population SD.'
x['reasoning_chain'][2]='Step 3: Honest disclosure now resolves the reporting ambiguity, but does not estimate paired precision for headline differences. Prefer a saved-prediction analysis; alternatively retain explicitly descriptive claims and remove unsupported significantly wording without fabricating intervals.'
x['fix']['instruction']+=' Preserve the newly added statistical-reporting paragraph. If the outputs are unavailable, the proposal-only fallback is to keep explicitly descriptive point estimates and remove unsupported significance language; no automatic rerun.'
# Update primary anchors to the new immutable PDF and line-check the relevant source.
def normalize(raw):
 chars=list(raw);mapping=list(range(len(raw)))
 def remove(pattern):
  nonlocal chars,mapping
  s=''.join(chars);bad=set(i for m in re.finditer(pattern,s,flags=re.M) for i in range(m.start(),m.end()))
  chars=[c for i,c in enumerate(chars) if i not in bad];mapping=[p for i,p in enumerate(mapping) if i not in bad]
 remove(r'^\d{1,4}\s*\n');remove(r'-\n(?=[a-z])')
 s=''.join(chars);out=[];mp=[]
 for m in re.finditer(r'\S+|\s+',s):
  if m.group().isspace():out.append(' ');mp.append(mapping[m.start()])
  else:out.extend(m.group());mp.extend(mapping[m.start():m.end()])
 return ''.join(out),mp
pdf=fitz.open(C/'main.pdf');pages=[]
for p in pdf:
 raw=p.get_text();clean,mp=normalize(raw);pages.append({'raw':raw,'clean':clean,'map':mp})
for x in J['issues']:
 hits=[i for i,p in enumerate(pages) if x['readable_anchor'] in p['clean']];assert hits,x['id']
 i=x['location']['page']-1 if x['location']['page']-1 in hits else hits[0]
 p=pages[i];s=p['clean'].index(x['readable_anchor']);end=s+len(x['readable_anchor'])
 x['location']['page']=i+1;x['location']['quoted_text']=p['raw'][p['map'][s]:p['map'][end-1]+1]
 if x['source_anchor']:
  txt=(C/'source'/x['location']['tex_file']).read_text();assert x['source_anchor'] in txt
  line=txt[:txt.index(x['source_anchor'])].count('\n')+1;x['location']['line_range']=[line,line+x['source_anchor'].count('\n')]
 x['version_status']='retained_after_current_pdf_recheck'
# Update formal fields and narrow obsolete conclusions.
J['execution_order']=[i for i in J['execution_order'] if i!='ISSUE-001']
J['severity_counts']=dict(collections.Counter(x['severity'] for x in J['issues']))
J['resolved_during_review']=[{'id':'ISSUE-001','status':'resolved_by_concurrent_revision_not_by_this_review','evidence':'New PDF pp2–3; concurrent_changes.json','proposal':'No further source/PDF synchronization fix requested for these passages.'}]
J['concurrent_revision']=D
J['provenance'].update({'pdf_sha256':current['main.pdf'],'pages':len(pdf),'reviewed_pdf_snapshot':str(C/'main.pdf'),'reviewed_source_snapshot':str(C/'source'),'initial_pdf_sha256':D['initial_pdf_sha256'],'concurrent_changes_report':'concurrent_changes.json'})
J['headline_verdict']='The paper has a concrete NLP-agent contribution and reproducible headline aggregate arithmetic. The strongest remaining concern is heterogeneous initialization in the nominally common-initialization three-run component study. Main/appendix method and split differences, paired uncertainty and an unsupported backbone ceiling also need attention. A concurrent revision resolved the stale-PDF issue and improved baseline/evaluator/statistical documentation; those improvements are credited rather than reported as absent. This is an internal review, not an official ARR score or acceptance prediction.'
J['review_form']['weaknesses']=[x['id']+': '+x['problem'] for x in J['issues'] if x['severity']=='major']
J['review_form']['questions'][1]='Do the frozen retrieval and released SkillRouter descriptions in new Appendix D.4 apply to every reported run, and what are the two remaining main-listed model roles?'
J['open_questions_for_human_author'][1]=J['review_form']['questions'][1]
J['submission_readiness']['reasoning']='Internal scientific judgment: reconcile ablation initialization and main/appendix method/split differences, clarify primary-comparison uncertainty, remove unsupported ceiling wording, and finish minor model-role alignment. New appendix reproducibility material is credited. No mandatory-policy blocker was confirmed; stage and logistics remain unknown.'
J['internal_scores']['presentation']['justification']='Thesis and results are recoverable and the new appendix improves documentation; method/split inconsistencies, captions and label sizes still need attention.'
J['acl_arr_compliance']['page_budget_note']='Current PDF has 30 pages; main content ends on p8. Fits assumed long review budget; active limit unknown.'
J['acl_arr_compliance']['evidence_notes']['total_pages']=30
J['acl_arr_compliance']['evidence_notes']['ai_disclosure']=J['acl_arr_compliance']['evidence_notes']['ai_disclosure']
J['acl_arr_compliance']['evidence_notes']['template_freshness_caveat']='Bundled archive equality checked at initial snapshot; current PDF fixes identified stale passages. Full build-source closure not independently certified.'
J['acl_arr_compliance']['anonymity_note']+=' Concurrent Appendix C.4 adds explicit component-license and privacy/safety caveats; these do not certify completed compliance checks.'
J['acl_arr_compliance']['compliance_gaps'][2]['evidence']='The style matches its bundled ACL archive; the current rebuild resolves identified stale passages. External supplements and build-source closure remain unverified.'
J['section_by_section_comments']['related_work']=['JTPRO/SkillRouter already cited; stale error-direction claim is now resolved in current PDF. Optional GEPA positioning remains optional.']
J['section_by_section_comments']['experiments']=['Correct global split and remaining main train/freeze/model-role statements; new Appendix D.4 now specifies retrieval, baseline inputs and task evaluation.']
J['section_by_section_comments']['reproducibility_details']=['New software and statistical-reporting paragraphs are useful. Historical initialization binding and paired uncertainty remain unresolved.']
J['adversarial_pass_findings']['pass_1_rejection_reasons'][2]='ISSUE-004: actual constrained global split differs from main per-dataset allocation; remaining model-role issue is now minor after Appendix D.4.'
J['adversarial_pass_findings']['pass_2_claims_outrunning_evidence']=[s for s in J['adversarial_pass_findings']['pass_2_claims_outrunning_evidence'] if 'ISSUE-001' not in s]
J['writing_diagnostics']['overclaims']=[a for a in J['writing_diagnostics']['overclaims'] if 'non-decreasing' not in a['phrase']]
# Figure IDs are stable but appendix pagination shifted; retain original renders only as archived evidence.
for f in J['figure_diagnostics']:
 hits=[i+1 for i,p in enumerate(pdf) if re.search(r'Figure\s+'+f['figure_id'].split()[-1]+r':',p.get_text())];assert len(hits)==1
 f['page']=hits[0];f['linked_issues']=[a for a in f['linked_issues'] if a!='ISSUE-001']
 f['render_version']='Initial snapshot; unchanged graphical asset checked against unchanged figure-file hashes. Current page number remapped.'
 if f['figure_id']=='Figure 2':
  f['problems']=[s for s in f['problems'] if 'omits equality' not in s]
  f['recommendation']='Current caption now includes equality. Optional diagram precision: name replay/validation risk symbols and mark example numbers illustrative. No required gate correction remains.'
  f['exact_caption_pdf_text']=None
J['self_containment_audit']['version_note']='Appendix locations originally mapped on 29-page snapshot; section/table identifiers stay stable. Current PDF adds pages/reflows; exact issue anchors remapped.'
J['narrative_diagnostics']['narrative_issues']=[s.replace('Strongest baseline is inadequately specified: ISSUE-006.','New Appendix D.4 addresses baseline detail; remaining main/model-role alignment is ISSUE-006.') for s in J['narrative_diagnostics']['narrative_issues']]
J['author_response_prep']=J['review_form']['questions'][:4]
# Rebuild proposal-only maps, preserving the no-execution contract.
F['venue_context']=copy.deepcopy(J['venue_context']);F['acl_arr_compliance']=copy.deepcopy(J['acl_arr_compliance']);F['paper_source']=str(C/'source');F['execution_order']=J['execution_order'];F['concurrent_revision']=D
F['revision_log']=[x for x in F['revision_log'] if x['issue_id']!='ISSUE-001'];F['unresolved_issues']=[x for x in F['unresolved_issues'] if x['issue_id']!='ISSUE-001'];F['proposals']=[]
for x,entry,un in zip(J['issues'],F['revision_log'],F['unresolved_issues']):
 assert x['id']==entry['issue_id']==un['issue_id']
 entry['location_before']=copy.deepcopy(x['location']);entry['acceptance_criteria_status']=[{'criterion':c,'status':'fail','evidence':'Not executed. Manuscript changes were not authorized; this is not an attempted edit failure.'} for c in x['fix']['acceptance_criteria']]
 un['what_is_needed']='Explicit author approval. '+('; '.join(x['fix']['required_inputs']) or 'No new measurements needed for the wording-only route.')
 F['proposals'].append({'issue_id':x['id'],'status':'proposed_not_applied','proposal_class':x['proposal_class'],'old_pdf_text':x['readable_anchor'],'old_source_text':x['source_anchor'],'source_mapping_status':x['source_mapping_status'],'proposed_text_or_action':x['fix']['target_text'] or x['fix']['instruction'],'conditional_inputs':x['fix']['required_inputs'],'acceptance_criteria':x['fix']['acceptance_criteria'],'depends_on':x['depends_on']})
for f,diag in zip(F['figures_pass'],J['figure_diagnostics']):
 f['problems']=diag['problems'];f['current_state']=diag['current_state']
 if f['figure_id']=='Figure 2':f['revised_specification']=diag['recommendation']
F['writing_pass_metrics']['acceptance_criteria_status'][1]['evidence']='Not authorized; unresolved current issues remain pending. ISSUE-001 was resolved outside this review action set.'
F['author_response_prep']['anticipated_reviewer_questions']=J['review_form']['questions'][:4];F['todos_for_human_author']=J['open_questions_for_human_author']
F['resolved_outside_this_review']=J['resolved_during_review']
for name,obj in [('REVIEW_JSON.json',J),('REVISION_REPORT.json',F)]: (R/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False))
print(json.dumps({'current_pdf_sha256':current['main.pdf'],'pages':len(pdf),'active_issues':len(J['issues']),'severity_counts':J['severity_counts'],'resolved':['ISSUE-001'],'concurrent_changed_existing_files':len(changes)},indent=2))
