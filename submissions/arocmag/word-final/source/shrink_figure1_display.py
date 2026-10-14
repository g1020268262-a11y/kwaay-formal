"""Shrink only Figure 1's OOXML drawing dimensions; keep image bytes and prose."""
import copy
import hashlib
import json
import zipfile
from pathlib import Path
from lxml import etree

OUT=Path(__file__).resolve().parent.parent
WORK=OUT/'K-Waay-AROCMAG-submission-working.docx'
EXPECTED='442c08e16ee0a979212180676faed37077b5fc1f171f5e5c4ebae1cc98744c13'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
    'wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}

def digest(data):return hashlib.sha256(data).hexdigest()

def main():
    before=WORK.read_bytes();assert digest(before)==EXPECTED,'Manuscript changed; re-inspect first'
    with zipfile.ZipFile(WORK) as z:
        infos=z.infolist();parts={n:z.read(n) for n in z.namelist()}
    original=dict(parts)
    rels=etree.fromstring(parts['word/_rels/document.xml.rels'])
    ids=[x.get('Id') for x in rels if x.get('Target','').endswith('kwaay-confirmed-figure1.png')]
    assert len(ids)==1
    root=etree.fromstring(parts['word/document.xml'])
    snapshot=copy.deepcopy(root)
    figures=root.xpath('//w:drawing[.//a:blip[@r:embed="'+ids[0]+'"]]',namespaces=NS)
    assert len(figures)==1
    extent=figures[0].find('.//wp:extent',NS)
    old=(int(extent.get('cx')),int(extent.get('cy')))
    assert old==(6480810,4860608)
    new=tuple(round(x*0.75) for x in old)
    extents=figures[0].xpath('.//wp:extent|.//a:xfrm/a:ext',namespaces=NS)
    assert len(extents)==2
    for ex in extents:
        assert (int(ex.get('cx')),int(ex.get('cy')))==old
        ex.set('cx',str(new[0]));ex.set('cy',str(new[1]))
    # Revert just these attributes in a check copy: the whole document must match.
    check=copy.deepcopy(root)
    for ex in check.xpath('//w:drawing[.//a:blip[@r:embed="'+ids[0]+'"]]//wp:extent|//w:drawing[.//a:blip[@r:embed="'+ids[0]+'"]]//a:xfrm/a:ext',namespaces=NS):
        ex.set('cx',str(old[0]));ex.set('cy',str(old[1]))
    assert etree.tostring(check,method='c14n')==etree.tostring(snapshot,method='c14n')
    parts['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    for n in original:
        if n!='word/document.xml':assert parts[n]==original[n]
    tmp=WORK.with_suffix('.figure1-size.tmp.docx')
    with zipfile.ZipFile(tmp,'w') as z:
        for info in infos:z.writestr(info,parts[info.filename])
    with zipfile.ZipFile(tmp) as z:assert z.testzip() is None
    assert digest(WORK.read_bytes())==EXPECTED
    tmp.replace(WORK)
    report={'before_sha256':EXPECTED,'after_sha256':digest(WORK.read_bytes()),'scale':0.75,
        'old_size_cm':[x/360000 for x in old],'new_size_cm':[x/360000 for x in new],
        'only_change':'Figure1 wp:extent and picture transform extents',
        'image_bytes_prose_caption_sections_other_figures_preserved':True,
        'visual_review':'WPS not opened; final visual pagination review deferred'}
    qa=OUT/'qa/figure1-display-size';qa.mkdir(parents=True,exist_ok=True)
    (qa/'resize-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
