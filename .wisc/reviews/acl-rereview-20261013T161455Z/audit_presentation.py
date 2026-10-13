from pathlib import Path
import fitz,json,hashlib,subprocess
from PIL import Image,ImageOps,ImageDraw
R=Path(__file__).parent
p=R/'source/main.pdf'
doc=fitz.open(p)
out=R/'renders';out.mkdir(exist_ok=True)
records=[]
for i,page in enumerate(doc):
    text=page.get_text(sort=True)
    (out/f'page-{i+1:02}.txt').write_text(text)
    page.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(str(out/f'page-{i+1:02}.png'))
    spans=[s for b in page.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']]
    overflow=[{'text':s['text'],'bbox':s['bbox']} for s in spans if (s['bbox'][0]<0 or s['bbox'][2]>page.rect.width or s['bbox'][1]<0 or s['bbox'][3]>page.rect.height)]
    captions=[l for l in page.get_text().splitlines() if l.startswith(('Figure ','Table '))]
    records.append({'page':i+1,'size':[page.rect.width,page.rect.height],'text_chars':len(text),'caption_starts':captions,'out_of_page_spans':overflow,'render':f'renders/page-{i+1:02}.png'})
for start in range(0,len(doc),4):
    sheet=Image.new('RGB',(1200,1740),'#aaaaaa')
    draw=ImageDraw.Draw(sheet)
    for j in range(4):
        if start+j>=len(doc):break
        im=Image.open(out/f'page-{start+j+1:02}.png');im.thumbnail((590,835))
        x=(j%2)*600;y=(j//2)*870
        sheet.paste(im,(x,y+25));draw.text((x+5,y+5),f'PDF page {start+j+1}',fill='black')
    sheet.save(out/f'sheet-{start+1:02}-{min(start+4,len(doc)):02}.png')
fonts=subprocess.check_output(['pdffonts',str(p)],text=True)
(R/'pdffonts.txt').write_text(fonts)
report={'pdf_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'page_count':len(doc),'metadata':doc.metadata,'pages':records,'fonts_report':'pdffonts.txt'}
(R/'presentation_physical.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
