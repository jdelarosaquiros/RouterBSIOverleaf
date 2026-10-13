"""Verify proposal contracts, real anchors, coverage and untouched original paper."""
from pathlib import Path
import json,hashlib,collections,subprocess,re
import fitz
R=Path(__file__).resolve().parent
ROOT=R.parents[2]
def strict(n):
 return json.loads((R/n).read_text(),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
J=strict('REVIEW_JSON.json');F=strict('REVISION_REPORT.json');M=J['provenance'];before=strict('current_snapshot/protected_baseline.json');original=strict('protected_before.json');drift=strict('concurrent_changes.json')
assert str(ROOT)==M['paper_root']
required_review=['paper_id','review_date','venue','venue_context','revision_mode','acl_arr_compliance','submission_readiness','overall_recommendation','headline_verdict','review_form','internal_scores','issues','self_containment_audit','figure_diagnostics','writing_diagnostics','narrative_diagnostics','missing_citations','required_new_experiments','section_by_section_comments','adversarial_pass_findings','author_response_prep','open_questions_for_human_author','execution_order','pre_submission_action_plan']
required_fixer=['revision_date','venue','venue_context','revision_mode','acl_arr_compliance','revision_log','self_containment_resolutions','figures_pass','writing_pass_metrics','narrative_arc','unresolved_issues','author_response_prep','todos_for_human_author']
assert set(required_review)<=J.keys();assert set(required_fixer)<=F.keys()
assert J['revision_mode']==F['revision_mode']=='unknown'
assert J['venue_context']==F['venue_context']; assert J['acl_arr_compliance']==F['acl_arr_compliance']
assert F['scope']=='proposal_only' and F['actual_manuscript_edits']==0 and not F['revised_manuscript_produced']
assert not F['experimental_results'] and F['build_status'].startswith('not_run')
for k in ['soundness','presentation','contribution','overall','confidence']:
 assert type(J['internal_scores'][k]['score']) is int and 1<=J['internal_scores'][k]['score']<=5
 assert J['internal_scores'][k]['justification']
assert J['internal_scores']['rubric']=='internal_1_to_5_not_official_arr'
ids=[i['id'] for i in J['issues']]; assert len(ids)==len(set(ids))==12
assert set(J['execution_order'])==set(ids)
assert [x['issue_id'] for x in F['revision_log']]==ids
assert [x['issue_id'] for x in F['proposals']]==ids
assert {x['issue_id'] for x in F['unresolved_issues']}==set(ids)
pdf=fitz.open(R/'current_snapshot/main.pdf');sanchors=0
allowed_cat=set('methodology claims baselines ablations theory writing figures narrative citations reproducibility ethics structure compliance self_containment ai_disclosure limitations nlp_contribution'.split())
allowed_fix=set('rewrite add_experiment add_citation add_ablation add_analysis add_theory restructure add_limitation redesign_figure tighten_writing sharpen_narrative promote_from_appendix add_ai_disclosure add_reproducibility_statement'.split())
for x,rev,p in zip(J['issues'],F['revision_log'],F['proposals']):
 assert x['severity'] in ['blocker','major','minor'] and x['category'] in allowed_cat
 assert x['adversarial_pass'] in list('12345SFWN')
 assert x['location']['quoted_text'] in pdf[x['location']['page']-1].get_text(),x['id']
 assert x['location']['anchor_kind'] in ['existing_span','adjacent_insertion']
 if x['source_anchor']:
  source=(R/'current_snapshot/source'/x['location']['tex_file']).read_text()
  a,z=x['location']['line_range']; assert x['source_anchor'] in '\n'.join(source.splitlines()[a-1:z]),x['id']
  sanchors+=1
 assert len(x['reasoning_chain'])>=3 and x['predicted_reviewer_objection'].startswith('Simulated objection:')
 assert x['fix']['type'] in allowed_fix and x['fix']['instruction'] and x['fix']['acceptance_criteria']
 assert type(x['fix']['blocks_submission']) is bool and x['fix_window']=='unknown'
 assert x['fix']['estimated_effort'] in ['trivial','small','medium','large']
 for dep in x['depends_on']: assert J['execution_order'].index(dep)<J['execution_order'].index(x['id'])
 assert rev['action_taken']=='not_executed' and rev['location_after']['new_text'] is None
 assert [a['criterion'] for a in rev['acceptance_criteria_status']]==x['fix']['acceptance_criteria']
 assert all(a['status']=='fail' and a['evidence'].startswith('Not executed.') for a in rev['acceptance_criteria_status'])
 assert p['status']=='proposed_not_applied' and p['proposed_text_or_action']
for collection in [J['figure_diagnostics'],F['figures_pass']]:
 assert {f['figure_id'] for f in collection}=={f'Figure {i}' for i in range(1,9)}
for f in J['figure_diagnostics']:
 assert (R/f['render']).exists() and set(f['linked_issues'])<=set(ids)
for a in J['self_containment_audit']['load_bearing_content_in_appendix']:assert set(a['linked_issues'])<=set(ids)
assert set(re.findall(r'Figure\s+([1-8]):','\n'.join(str(p.get_text('text')) for p in pdf)))==set('12345678')
# Compare original protected files, including their timestamps-independent exact bytes.
after={};missing=[]
for rel in before:
 p=ROOT/rel
 if not p.is_file():missing.append(rel)
 else:after[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
changed=[rel for rel,h in before.items() if rel in after and after[rel]!=h]
assert not missing and not changed,{'missing':missing,'changed':changed}
assert len(original)==332
assert {p for p,h in original.items() if after[p]!=h}==set(drift['changed_preexisting_files'])
pdfhash=hashlib.sha256((ROOT/'main.pdf').read_bytes()).hexdigest()
assert pdfhash==M['pdf_sha256']==hashlib.sha256((R/'current_snapshot/main.pdf').read_bytes()).hexdigest()
assert len(pdf)==30
# Recheck all 12 external initial-policy files against the saved parent audit.
audit=strict('parent_initial_policy_verification.json');assert len(audit)==12
for a in audit:
 data=Path(a['path']).read_bytes(); assert hashlib.sha256(data).hexdigest()==a['file_sha256']
assert len({a['predicate_payload_sha256'] for a in audit})==3
font=subprocess.run(['pdffonts',str(R/'current_snapshot/main.pdf')],capture_output=True,text=True,check=True)
font_lines=[l for l in font.stdout.splitlines()[2:] if l.strip()]
assert font_lines
font_flags=[re.search(r'\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$',l) for l in font_lines]
assert all(m is not None and m.group(1)=='yes' for m in font_flags)
assert all(abs(p.rect.width-595.276)<0.02 and abs(p.rect.height-841.89)<0.02 for p in pdf)
(R/'protected_after.json').write_text(json.dumps(after,indent=2))
(R/'pdffonts_verification.txt').write_text(font.stdout)
result={'status':'pass','issues_checked':len(ids),'source_anchors_checked':sanchors,'proposal_count':len(F['proposals']),'revision_log_count':len(F['revision_log']),'unresolved_issue_count':len(F['unresolved_issues']),'figure_count':len(J['figure_diagnostics']),'severity_counts':dict(collections.Counter(i['severity'] for i in J['issues'])),'all_dependencies_valid':True,'strict_json_and_contract_checks':'pass','all_pdf_quotes_literal':True,'source_anchors_literal_and_line_checked':True,'protected_file_count':len(before),'changed_protected_files':changed,'missing_protected_files':missing,'pdf_sha256':pdfhash,'pdf_pages':len(pdf),'main_text_ends_on_page':8,'main_page_count_evidence':'Visual page-8 conclusion then Limitations/ethics/disclosure/references; active stage unknown.','a4_all_pages':True,'font_resources':len(font_lines),'all_fonts_embedded':True,'initial_policy_files_verified':12,'distinct_initial_predicate_payloads':3,'new_benchmark_runs':0,'manuscript_build':'not_run_by_design','manuscript_edits':0,'uploads':0,'scope_caveats':['Existing source/PDF drift is preserved, not repaired.','Local run paths match review-time hashes; historical plotted-source binding still needs author confirmation.','Manuscript acceptance criteria remain unexecuted, not passed.','No claim of exhaustive portal/ethics/anonymity verification.']}
result.update({'status':'pass_with_documented_concurrent_changes','protected_file_count':len(original),'current_snapshot_protected_count':len(before),'changed_protected_files_since_start':drift['changed_preexisting_files'],'new_paper_source_files_since_start':drift['new_paper_source_files'],'unchanged_since_current_snapshot':True,'initial_pdf_sha256':drift['initial_pdf_sha256'],'scope_caveats':['Paper changed outside this review-only action set during the review; no attribution is inferred.','Final issue anchors and proposals were reconciled against the new immutable 30-page snapshot.','Local run paths match review-time hashes; historical plotted-source binding still requires author confirmation.','Manuscript acceptance criteria are proposals, not completed edits.']})
(R/'verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
