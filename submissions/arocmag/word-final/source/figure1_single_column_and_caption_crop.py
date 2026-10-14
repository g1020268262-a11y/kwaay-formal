"""Word picture formatting only: single-column figure1 and non-destructive crops.

No bitmap edits or regenerated diagrams. Source images stay byte-identical.
"""
import copy
import hashlib
import json
import zipfile
from pathlib import Path
from lxml import etree

OUT=Path(__file__).resolve().parent.parent
WORK=OUT/'K-Waay-AROCMAG-submission-working.docx'
QA=OUT/'qa/figure-title-display'
EXPECTED='1979d77b3c68d64c984da58ee1297fddba9396ef56708e34ee520a05ac3fd210'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
    'wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'pic':'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(p):return etree.tostring(p,method='c14n')
def txt(p):return ''.join(p.xpath('.//w:t/text()',namespaces=NS))

def main():
    before=WORK.read_bytes();assert sha(before)==EXPECTED,'Working manuscript changed; inspect first'
    with zipfile.ZipFile(WORK) as z:infos=z.infolist();package={n:z.read(n) for n in z.namelist()}
    original=dict(package)
    root=etree.fromstring(package['word/document.xml']);body=root.find('w:body',NS)
    blocks=list(body);snapshots=[canon(p) for p in blocks]
    rels=etree.fromstring(package['word/_rels/document.xml.rels'])
    ids={n:next(x.get('Id') for x in rels if x.get('Target','').endswith(f'kwaay-confirmed-figure{n}.png')) for n in (1,2,3)}
    drawings={n:root.xpath('//w:drawing[.//a:blip[@r:embed="'+rid+'"]]',namespaces=NS) for n,rid in ids.items()}
    assert all(len(v)==1 for v in drawings.values())
    drawings={n:v[0] for n,v in drawings.items()}
    parents={n:drawings[n].getparent().getparent() for n in drawings}
    assert all(p.tag=='{'+NS['w']+'}p' for p in parents.values())
    i=blocks.index(parents[1]);assert i==33
    close_two=blocks[i-1];caption=blocks[i+1]
    assert txt(close_two)=='' and not close_two.xpath('.//w:drawing',namespaces=NS)
    assert close_two.xpath('./w:pPr/w:sectPr/w:cols/@w:num',namespaces=NS)==['2']
    assert txt(caption)=='图1 K-Waay核心发送与批量接收流程'
    assert caption.xpath('./w:pPr/w:sectPr/w:cols/@w:num',namespaces=NS)==['1']
    # Remove only the temporary figure1 full-width section boundaries.
    body.remove(close_two)
    sp=caption.find('w:pPr/w:sectPr',NS);sp.getparent().remove(sp)
    widths=[int(drawings[n].find('.//wp:extent',NS).get('cx')) for n in (2,3)]
    assert widths==[3126105,3126105]
    cuts={1:60,2:66,3:54} # Visually verified blank bands below titles, above diagram borders.
    report=[]
    for n,drawing in drawings.items():
        width=widths[0] if n==1 else int(drawing.find('.//wp:extent',NS).get('cx'))
        height=round(width*(1086-cuts[n])/1448)
        fill=drawing.find('.//pic:blipFill',NS);assert fill is not None
        assert fill.find('a:srcRect',NS) is None,'Unexpected pre-existing crop'
        crop=etree.Element('{'+NS['a']+'}srcRect')
        crop.set('l','0');crop.set('t',str(round(100000*cuts[n]/1086)));crop.set('r','0');crop.set('b','0')
        fill.insert(list(fill).index(fill.find('a:blip',NS))+1,crop)
        for ex in drawing.xpath('.//wp:extent|.//a:xfrm/a:ext',namespaces=NS):
            ex.set('cx',str(width));ex.set('cy',str(height))
        report.append({'figure':n,'top_hidden_pixels':cuts[n],'crop_top_percent':int(crop.get('t'))/1000,
                       'display_width_cm':width/360000,'display_height_cm':height/360000})
    changed={blocks.index(parents[n]) for n in (1,2,3)}|{i+1}
    remaining=[(j,p) for j,p in enumerate(blocks) if p is not close_two]
    assert list(body)==[p for j,p in remaining]
    for j,p in remaining:
        if j not in changed:assert canon(p)==snapshots[j],f'Unexpected change at body block{j}'
    assert root.xpath('//w:sectPr/w:cols/@w:num',namespaces=NS)==['1','2','1','2']
    # Every actual prose/caption string remains exactly the same.
    assert ''.join(txt(p) for p in body)==''.join(txt(p) for p in blocks)
    assert len(root.xpath('//w:drawing',namespaces=NS))==4
    package['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    for n in original:
        if n!='word/document.xml':assert original[n]==package[n]
    tmp=WORK.with_suffix('.single-column-crop.tmp.docx')
    with zipfile.ZipFile(tmp,'w') as z:
        for info in infos:z.writestr(info,package[info.filename])
    with zipfile.ZipFile(tmp) as z:
        assert z.testzip() is None
        for n in original:
            if n!='word/document.xml':assert original[n]==z.read(n)
    assert sha(WORK.read_bytes())==EXPECTED;tmp.replace(WORK)
    manifest={'before_sha256':EXPECTED,'after_sha256':sha(WORK.read_bytes()),'figures':report,
              'bitmap_bytes_unchanged':True,'only_package_part_changed':'word/document.xml',
              'all_prose_math_caption_text_preserved':True,'figure1_fullwidth_section_boundaries_removed':True,
              'figure4':'Already has no embedded top title; unchanged',
              'crop_method':'Word native a:srcRect display crop; originals retained; no raster regeneration',
              'visual_review':'Original images inspected to choose safe title-band cuts; WPS/full pagination review not performed'}
    QA.mkdir(parents=True,exist_ok=True)
    (QA/'single-column-crop-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
