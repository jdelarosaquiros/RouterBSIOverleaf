"""Check appendix-only edits and compare a clean baseline with the revised build."""
from pathlib import Path
import hashlib,json,re,collections,sys
import fitz
R=Path(__file__).resolve().parent
ROOT=R.parents[2]
load=lambda f:json.loads((R/f).read_text())
before=load('before.json')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
changed=[f for f,h in before.items() if (ROOT/f).exists() and sha(ROOT/f)!=h]
missing=[f for f in before if not (ROOT/f).is_file()]
assert not missing,missing
assert all(f.startswith('sections/appendix/') and f.endswith('.tex') for f in changed),changed
edits=load('edits_approved.json')
expected={x['file'] for x in edits}
assert set(changed)==expected,{'unexpected':set(changed)-expected,'not_changed':expected-set(changed)}
checks=[]
for f in changed:
 old=(R/'before'/f).read_text();new=(ROOT/f).read_text()
 # Results and quantitative settings cannot change in this prose-only task.
 nums=lambda t:re.findall(r'(?<![A-Za-z])\d+(?:\.\d+)?',t)
 assert nums(old)==nums(new),(f,'numeric token change')
 equations=lambda t:re.findall(r'\\\[.*?\\\]',t,re.S)
 assert equations(old)==equations(new),(f,'display equation change')
 tables=lambda t:re.findall(r'\\begin\{tabular\*?\}.*?\\end\{tabular\*?\}',t,re.S)
 assert tables(old)==tables(new),(f,'table value/layout change')
 prompts=lambda t:re.findall(r'\\begingroup\s*\\small\\ttfamily.*?\\endgroup',t,re.S)
 assert prompts(old)==prompts(new),(f,'prompt/example change')
 cites=lambda t:re.findall(r'\\cite\w*\{([^}]+)\}',t)
 assert cites(old)==cites(new),(f,'citation change')
 checks.append({'file':f,'numeric_tokens_unchanged':True,'display_math_unchanged':True,'tables_unchanged':True,'quoted_prompt_blocks_unchanged':True,'citations_unchanged':True})
# Every original active subsection and table/wrapper file must be audited.
active=load('active_inventory.json')
audit=load('subsection_audit.json')
assert {x['file'] for x in audit['files']}==set(active['active_files'])
assert len(audit['subsections'])==len(active['active_subsections'])
# Main body render must stay unchanged, not merely source text.
baseline=fitz.open(R/'build_before/main.pdf'); revised=fitz.open(R/'build_after/main.pdf')
main_pages=[]
for i in range(8):
 a=baseline[i].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
 b=revised[i].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
 same=(a.width,a.height,a.samples)==(b.width,b.height,b.samples)
 assert same,('main page changed',i+1)
 main_pages.append(i+1)
log=(R/'build_after/main.log').read_text(errors='replace')
for bad in ['Undefined control sequence','There were undefined references','There were multiply-defined labels','LaTeX Error','Overfull \\hbox','Overfull \\vbox']:
 assert bad not in log,bad
result={'status':'pass_with_unresolved_scientific_conflicts','changed_files':changed,'protected_file_count':len(before),'outside_appendix_changes':[],'missing_files':missing,'active_tex_files_audited':len(audit['files']),'subsections_audited':len(audit['subsections']),'numeric_and_structure_checks':checks,'main_render_identical_pages':main_pages,'baseline_pdf_pages':len(baseline),'revised_pdf_pages':len(revised),'revised_pdf_sha256':sha(R/'build_after/main.pdf'),'original_main_pdf_unchanged':sha(ROOT/'main.pdf')==before['main.pdf'],'build_errors':[],'font_warnings':[l for l in log.splitlines() if 'LaTeX Font Warning' in l],'unresolved':audit['unresolved']}
(R/'verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
