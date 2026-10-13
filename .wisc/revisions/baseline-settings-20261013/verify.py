from pathlib import Path
import hashlib,json,re,fitz
R=Path(__file__).resolve().parent
root=R.parents[2]
rel='sections/appendix/implementation_software.tex'
before=(R/'implementation_software.before.tex').read_text()
addition=(R/'addition.tex').read_text()
actual=(root/rel).read_text()
assert actual==before.replace('\\paragraph{Task evaluation.}',addition+'\\paragraph{Task evaluation.}',1)
manifest=json.loads((R/'before.json').read_text())
changed=[f for f,h in manifest.items() if hashlib.sha256((root/f).read_bytes()).hexdigest()!=h]
assert set(changed)=={rel,'main.pdf'},changed
assert (root/'sections/ablations.tex').read_bytes()==(R/'ablations.before.tex').read_bytes()
bib=(root/'references.bib').read_text()
assert all(re.search(r'@\w+\{'+re.escape(k)+r',',bib) for k in re.findall(r'\\citep\{([^}]+)\}',addition))
old=fitz.open(R/'before.pdf');new=fitz.open(root/'main.pdf')
assert all(old[i].get_text()==new[i].get_text() for i in range(8))
# Exclude line-number gutters geometrically; preserve body numbers.
text='\n'.join(str(new[i].get_text('text',clip=fitz.Rect(60,0,535,new[i].rect.height))) for i in range(len(new)))
normalized=re.sub(r'\s+',' ',text)
assert 'we freeze the existing skills' in normalized
assert 'We evaluate SkillDAG with its default settings' in normalized
assert 'expansion produces more than k candidates' in normalized
pages=[i for i,p in enumerate(new) if 'Skill-Pro represents' in p.get_text() or 'We evaluate SkillDAG' in p.get_text()]
assert pages
render_pages=sorted(set(pages+[max(pages)+1]))
for i in render_pages:
 if i<len(new):new[i].get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(R/f'page-{i+1}.png')
log=(root/'main.log').read_text(errors='replace')
fatal=[line for line in log.splitlines() if 'undefined' in line.lower() or line.startswith('!')]
assert not fatal,fatal
result={'status':'pass','changed_protected_files':changed,'main_first_eight_pages_text_identical':True,'pages_before':len(old),'pages_after':len(new),'addition_pages':[i+1 for i in pages],'rendered_pages':[i+1 for i in render_pages if i<len(new)],'proposal_unapplied':True,'citation_keys_resolved':True,'fatal_or_undefined_log_lines':fatal,'pdf_sha256':hashlib.sha256((root/'main.pdf').read_bytes()).hexdigest()}
(R/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
