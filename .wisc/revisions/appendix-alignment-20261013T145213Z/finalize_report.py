"""Generate concise WISC and revision reports from executed verification."""
from pathlib import Path
import json,re,datetime,difflib,hashlib
import fitz
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
load=lambda f:json.loads((R/f).read_text())
v=load('verification.json');a=load('subsection_audit.json');edits=load('edits_approved.json');visual=load('visual_review.json')
assert visual['status']=='pass'
assert all((ROOT/e['file']).read_text().find(e['new'])>=0 for e in edits if e['new'])
revision=[];old_words=0;new_words=0;diff=[]
for f in v['changed_files']:
 old=(R/'before'/f).read_text();new=(ROOT/f).read_text();old_words+=len(old.split());new_words+=len(new.split());diff.extend(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile='before/'+f,tofile='after/'+f))
for i,e in enumerate(edits,1):
 revision.append({'issue_id':f'APPENDIX-{i:02d}','action_taken':'rewrite','summary':e['reason'],'location_before':{'section':e['file'],'quoted_text':e['old']},'location_after':{'section':e['file'],'new_text':e['new']},'page_impact':'appendix only; first eight rendered pages unchanged','fix_window':'unknown','acceptance_criteria_status':[{'criterion':'Exact approved replacement applied in appendix only','status':'pass','evidence':e['file']},{'criterion':'Numeric tokens, tables, display equations, prompt blocks and citations unchanged','status':'pass','evidence':'verification.json'}]})
for u in a['unresolved']:
 revision.append({'issue_id':u['id'],'action_taken':'not_executed','summary':u['description'],'location_before':{'section':', '.join(u['appendix']),'quoted_text':None},'location_after':{'section':', '.join(u['appendix']),'new_text':None},'page_impact':'none','fix_window':'unknown','acceptance_criteria_status':[{'criterion':'Resolve factual alignment without unsupported claims or main-section edits','status':'partial','evidence':u['needed']}]})
doc=fitz.open(R/'build_after/main.pdf'); fonts=set()
for p in doc:
 for f in p.get_fonts(full=True):fonts.add(f[0])
import subprocess
font_output=subprocess.run(['pdffonts',str(R/'build_after/main.pdf')],capture_output=True,text=True,check=True).stdout
font_rows=[line for line in font_output.splitlines()[2:] if line.strip()]
font_check=bool(font_rows) and all(line.rsplit(None,5)[1]=='yes' for line in font_rows)
assert all(abs(p.rect.width-595.276)<1 and abs(p.rect.height-841.89)<1 for p in doc)
(R/'font_verification.txt').write_text(font_output)
# Embedded Type 3 fonts do not expose extract_font bytes; pdffonts checks embedding.
report={'revision_date':datetime.datetime.now(datetime.timezone.utc).date().isoformat(),'venue':'unknown','venue_context':{'target_venue':'unknown','year':None,'track':'unknown','arr_cycle':'unknown','paper_type':'long','paper_type_confirmed':False,'current_instructions_verified':False,'deadline':'unknown','pdf_revision_permission':'unknown','response_visibility':'unknown'},'revision_mode':'unknown','authorization':'Explicit local appendix edits only; no submitted-PDF revision or upload','experimental_results':[],'acl_arr_compliance':{'main_text_pages':8,'active_page_limit':None,'page_count_compliant':'unknown','style_file':'acl','template_compliance':'needs_human_check','review_mode':True,'a4_two_column_embedded_fonts':'verified' if font_check else 'needs_human_check','responsible_nlp_checklist':'needs_human_check','appendix_present':True,'appendix_after_references_same_pdf':True,'appendix_format':'two_column','ai_disclosure_status':'needs_human_check','compliance_gaps':[{'requirement':'Venue/cycle/stage and submission authorization','status':'unverified','evidence':'Only local source revisions authorized','required_action':'Author handles submission details','owner':'human_author','linked_issues':[]}]},'revision_log':revision,'self_containment_resolutions':[{'content':'Appendix operational definitions versus frozen main wording','resolution':'left_with_justification','justification_if_left':'Main edits expressly prohibited; unresolved factual discrepancies documented outside paper.'}],'figures_pass':[{'figure_id':'All existing figures','current_state':'Assets and main captions unchanged','problems':[],'revised_specification':None,'caption_rewrite':None,'generation_code':None,'acceptance_criteria_status':[{'criterion':'No figure asset or main caption modified','status':'pass','evidence':'Full-tree before/after hashes'}]}],'writing_pass_metrics':{'words_cut':old_words-new_words,'word_count_method':'Whitespace token count over changed TeX files, including comments; not a prose-only word estimate','acceptance_criteria_status':[{'criterion':'Remove unhelpful process/provenance commentary without suppressing relevant evidence','status':'pass','evidence':'Exact edits and retained qualifications in APPENDIX_AUDIT.md'}]},'narrative_arc':{'thesis_sentence':'Editable applicability predicates improve skill routing through bounded replay and held-out validation.','acceptance_criteria_status':[{'criterion':'Review every appendix subsection against main claims','status':'pass','evidence':'49 files / 31 subsections enumerated in subsection_audit.json'},{'criterion':'Complete factual main/appendix consistency','status':'partial','evidence':'Five unresolved items requiring evidence or main-text authority'}]},'unresolved_issues':[{'issue_id':u['id'],'reason':'requires author judgment','what_is_needed':u['needed']} for u in a['unresolved']],'todos_for_human_author':[u['needed'] for u in a['unresolved']],'author_response_prep':{'anticipated_reviewer_questions':[],'prepared_responses':[],'missing_evidence':[],'permission_checks':['No author response or upload requested']},'verification':v,'visual_review':visual,'main_pdf_replaced':False,'commits':0,'model_runs':0,'uploads':0}
(R/'REVISION_REPORT.json').write_text(json.dumps(report,indent=2));(R/'appendix_only.diff').write_text(''.join(diff))
text=f'''# WISC execution report — appendix alignment

## Outcome
Audited all **{a['counts']['active_subsections']} active appendix subsections** and **{a['counts']['active_tex_files']} TeX files**. Applied **{len(edits)} exact prose/caption replacements in {len(v['changed_files'])} appendix source files**. Main sources, main captions/figures, bibliography, numeric results and original `main.pdf` are unchanged. The edits are local, unsubmitted changes, not a claim of venue compliance.

**Full factual alignment remains incomplete.** The requested shared-initialization sentence was not added because inspected saved libraries differ across the Both Enabled runs; their historical binding to Figure 5 remains unresolved. This is a manuscript-versus-artifact issue, not a main-versus-appendix contradiction. The existing disputed sentence is unchanged. The other unresolved items are replay definition/support, ranking-rule scope, global versus per-dataset splits, and the main paper's incompatible retriever-training statements. See the [complete subsection audit](APPENDIX_AUDIT.md).

## Changes
- Removed checksum/journal-verification assertions, legacy temperature-field commentary, a credential-archive aside, irrelevant archive qualifiers and repository-relative wording.
- Renamed Artifact Coverage and Reuse to Dataset Coverage and Reuse; preserved language, privacy, licensing and safety content.
- Corrected the appendix/main cross-reference, iteration acceptance terminology and plural downstream-table reference.
- Replaced saved-snapshot language with measured-policy terminology, retaining all task counts and results.
- Preserved useful token-coverage, uncertainty, evaluator-adjudication, data-scope and observational-versus-causal qualifications.

## Verification
- Clean baseline and revised isolated builds passed; revised PDF has {v['revised_pdf_pages']} pages.
- First eight pages render pixel-identically to the clean pre-edit baseline.
- No changes outside appendix sources among {v['protected_file_count']} protected files.
- Numeric tokens, table bodies, display equations, quoted prompt blocks and citations preserved in every edited file.
- Build has no fatal errors, undefined references or overfull boxes; existing small-font substitution warnings remain.
- Existing repository check passed in the revised build. All modified appendix regions and their following transitions were visually checked in contact sheets.

## WISC record
- SELECT: live main text/captions, complete appendix include tree and dirty working-tree baseline.
- ISOLATE: three independent audits plus parent reconciliation; no artifact/model runs.
- WRITE: `.wisc/plans/appendix-alignment-20261013T145213Z.md` and exact replacement allowlist.
- IMPLEMENT: edits restricted to `sections/appendix/*.tex`; isolated `make build` and `make check`.
- COMPRESS: audit, diff, revision/verification JSON and this report. No commit; unrelated existing changes remain untouched. TaskMaster tools unavailable; Hermes task checklist used.

## Deliverables
- [Revised review PDF](build_after/main.pdf) — isolated build; original `main.pdf` not overwritten.
- [Every-subsection audit](APPENDIX_AUDIT.md)
- [Exact appendix-only diff](appendix_only.diff)
- [Revision report](REVISION_REPORT.json)
- [Verification](verification.json)

## Next decision
Resolve the disputed historical initialization binding and allow corrections to the frozen main claims where necessary. No benchmark rerun, figure regeneration, commit or upload was authorized or performed.
'''
(R/'WISC_REPORT.md').write_text(text)
print(json.dumps({'edits':len(edits),'files':len(v['changed_files']),'subsections':len(a['subsections']),'unresolved':len(a['unresolved']),'tex_words_cut':old_words-new_words,'pdf_pages':len(doc),'font_resources_embedded':font_check},indent=2))
