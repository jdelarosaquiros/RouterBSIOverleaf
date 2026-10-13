from pathlib import Path
import hashlib
import json
import subprocess
import sys
from docx import Document
import fitz
from PIL import Image

here = Path(__file__).resolve().parent
root = here.parents[2]
pack = json.loads((here / 'minimal_changes_proposals.json').read_text())
validator = '/workspace/storage/.hermes/skills/productivity/docx/scripts/docx_validate.py'
images, report = [], []
assert hashlib.sha256((here / 'before.pdf').read_bytes()).hexdigest() == pack['snapshot_sha256']
for stem, code in [('replay_guarantee_minimal_changes', '2_'), ('protocol_details_minimal_changes', '5_')]:
    validation = subprocess.run([sys.executable, validator, str(here / (stem + '.docx'))], capture_output=True, text=True, check=True)
    health = json.loads(validation.stdout)
    assert health['ok']
    doc = Document(str(here / (stem + '.docx')))
    text = '\n'.join(p.text for p in doc.paragraphs)
    proposals = [r for r in pack['proposals'] if r['document'].startswith(code)]
    assert all(r['old'] in text and r['new'] in text for r in proposals)
    for row in proposals:
        source = (root / row['file']).read_text()
        assert source.count(row['old']) == 1
        assert source[:source.index(row['old'])].count('\n') + 1 == row['source_line_start']
        for ev in row['evidence']:
            assert ev['quote'] in (root / ev['file']).read_text()
    assert 'superseded' not in text
    assert 'contradictory historical' not in text
    pdf = fitz.open(here / (stem + '.pdf'))
    assert len(pdf) == 3
    bounds = []
    for page in pdf:
        pix = page.get_pixmap(matrix=fitz.Matrix(.9, .9))
        images.append(Image.frombytes('RGB', [pix.width, pix.height], pix.samples))
        bounds.extend(list(b[:4]) for b in page.get_text('blocks') if b[0] < 0 or b[1] < 0 or b[2] > page.rect.width + .5 or b[3] > page.rect.height + .5)
    assert not bounds
    report.append({'document': stem, 'pages': len(pdf), 'proposal_count': len(proposals), 'package_validation': health, 'exact_old_new_readback': True, 'source_quotes_and_evidence_reverified': True, 'out_of_page_text_blocks': bounds, 'docx_sha256': hashlib.sha256((here / (stem + '.docx')).read_bytes()).hexdigest(), 'pdf_sha256': hashlib.sha256((here / (stem + '.pdf')).read_bytes()).hexdigest()})
w, h = max(i.width for i in images), max(i.height for i in images)
sheet = Image.new('RGB', (w * 3, h * 2), (220, 220, 220))
for i, image in enumerate(images):
    sheet.paste(image, ((i % 3) * w, (i // 3) * h))
sheet.save(here / 'proposal_docs_contact_sheet.png')
(here / 'proposal_docs_verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
