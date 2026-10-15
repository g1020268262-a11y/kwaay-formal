"""Keep figure/caption paired in native paragraph frames with top/bottom wrap.

No image re-encoding or academic-text edits. Hash guard and restricted pPr diff.
"""
import copy
import hashlib
import json
import zipfile
from pathlib import Path
from lxml import etree

OUT=Path(__file__).resolve().parent.parent
WORK=OUT/'K-Waay-AROCMAG-submission-working.docx'
QA=OUT/'qa/figure-flow-repair'
EXPECTED='664c86135f21e3ff265d3fe2f0666be4a51b6df6ca8ebe97bbd58463734a3d2c'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
W=NS['w']
def q(s):return '{'+W+'}'+s
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(p):return etree.tostring(p,method='c14n')

def main():
    original=WORK.read_bytes();assert sha(original)==EXPECTED,'Manuscript changed; inspect first'
    with zipfile.ZipFile(WORK) as z:infos=z.infolist();parts={n:z.read(n) for n in z.namelist()}
    root=etree.fromstring(parts['word/document.xml']);body=list(root.find('w:body',NS))
    before=copy.deepcopy(root);before_body=list(before.find('w:body',NS))
    fig_indices=[i for i,p in enumerate(body) if p.xpath('.//w:drawing',namespaces=NS)]
    assert len(fig_indices)==5
    records=[];allowed=set()
    for n,i in enumerate(fig_indices,1):
        image,caption=body[i],body[i+1]
        label=''.join(caption.xpath('.//w:t/text()',namespaces=NS));assert label.startswith('图'+str(n)+' ')
        width=int(image.find('.//wp:extent',NS).get('cx'));assert width==3126105
        frame_attrs={'w':str(round(width/635)),'hRule':'auto','wrap':'notBeside',
                     'hAnchor':'text','vAnchor':'text','xAlign':'center','y':'0',
                     'hSpace':'0','vSpace':'80','anchorLock':'1'}
        for p in (image,caption):
            pp=p.find('w:pPr',NS);assert pp is not None
            assert pp.find('w:framePr',NS) is None
            frame=etree.Element(q('framePr'))
            for key,val in frame_attrs.items():frame.set(q(key),val)
            # OOXML CT_PPr ordering: framePr follows pageBreakBefore and precedes spacing.
            before_nodes={'widowControl','numPr','suppressLineNumbers','pBdr','shd','tabs',
                          'suppressAutoHyphens','kinsoku','wordWrap','overflowPunct','topLinePunct',
                          'autoSpaceDE','autoSpaceDN','bidi','adjustRightInd','snapToGrid','spacing',
                          'ind','contextualSpacing','mirrorIndents','suppressOverlap','jc','textDirection',
                          'textAlignment','textboxTightWrap','outlineLvl','divId','cnfStyle','rPr','sectPr'}
            insert=next((j for j,c in enumerate(pp) if etree.QName(c).localname in before_nodes),len(pp))
            pp.insert(insert,frame)
            pagebreak=pp.find('w:pageBreakBefore',NS)
            if pagebreak is None:
                pagebreak=etree.Element(q('pageBreakBefore'));pp.insert(insert,pagebreak)
            pagebreak.set(q('val'),'0')
        # Only the picture-caption pair stays together; following prose remains free-flowing.
        for p,keep in ((image,'1'),(caption,'0')):
            k=p.find('w:pPr/w:keepNext',NS);assert k is not None;k.set(q('val'),keep)
        allowed.update((i,i+1))
        assert canonical(image.find('w:pPr/w:framePr',NS))==canonical(caption.find('w:pPr/w:framePr',NS))
        records.append({'figure':n,'image_block':i,'caption_block':i+1,'caption':label,'frame':frame_attrs})
    for i,(a,b) in enumerate(zip(before_body,body)):
        if i not in allowed:assert canonical(a)==canonical(b)
        else:
            ac=copy.deepcopy(a);bc=copy.deepcopy(b)
            for c in list(ac):
                if c.tag==q('pPr'):ac.remove(c)
            for c in list(bc):
                if c.tag==q('pPr'):bc.remove(c)
            assert canonical(ac)==canonical(bc),'Changed content in figure block'
    assert len(root.xpath('//w:framePr',namespaces=NS))==10
    QA.mkdir(parents=True,exist_ok=True)
    (QA/'before-document.xml').write_bytes(parts['word/document.xml'])
    parts['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    tmp=WORK.with_suffix('.figure-flow.tmp.docx')
    with zipfile.ZipFile(tmp,'w') as z:
        for info in infos:z.writestr(info,parts[info.filename])
    with zipfile.ZipFile(tmp) as z:assert z.testzip() is None
    assert sha(WORK.read_bytes())==EXPECTED;tmp.replace(WORK)
    report={'before_sha256':EXPECTED,'after_sha256':sha(WORK.read_bytes()),'only_changed_part':'word/document.xml',
            'only_change':'Native top/bottom paragraph frames for five existing picture-caption pairs; explicit no forced page break',
            'body_text_order_math_table_image_bytes_preserved':True,'frames':records,'visual_review':'pending'}
    (QA/'layout-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='frames'},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
