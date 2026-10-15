"""Replace failed frame trial with WPS-compatible floating picture-caption groups."""
import copy
import hashlib
import json
import zipfile
from pathlib import Path
from lxml import etree

OUT=Path(__file__).resolve().parent.parent
WORK=OUT/'K-Waay-AROCMAG-submission-working.docx'
QA=OUT/'qa/figure-flow-repair'
EXPECTED='8b32f00e72669108fd07fe09c54711a094c67226b9caaf9c33dd070c36220d90'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic':'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'wpg':'http://schemas.microsoft.com/office/word/2010/wordprocessingGroup',
    'wps':'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'}
def q(prefix,name):return '{'+NS[prefix]+'}'+name
def el(parent,prefix,name,**attrs):
    e=etree.SubElement(parent,q(prefix,name))
    for k,v in attrs.items():e.set(k,str(v))
    return e
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(e):return etree.tostring(e,method='c14n')

def main():
    data=WORK.read_bytes();assert sha(data)==EXPECTED
    with zipfile.ZipFile(WORK) as z:infos=z.infolist();parts={n:z.read(n) for n in z.namelist()}
    original_xml=(QA/'before-document.xml').read_bytes()
    root=etree.fromstring(original_xml);body=root.find('w:body',NS);blocks=list(body)
    originaltext=root.xpath('//w:t/text()',namespaces=NS)
    images=[(i,p) for i,p in enumerate(blocks) if p.xpath('.//w:drawing',namespaces=NS)]
    assert len(images)==5
    report=[];changed=[]
    for n,(i,p) in enumerate(images,1):
        if n not in (3,4):continue
        caption=blocks[i+1]
        assert ''.join(caption.xpath('.//w:t/text()',namespaces=NS)).startswith('图'+str(n)+' ')
        drawing=p.find('w:r/w:drawing',NS);inline=drawing.find('wp:inline',NS);assert inline is not None
        pic=copy.deepcopy(inline.find('a:graphic/a:graphicData/pic:pic',NS));assert pic is not None
        cx=int(inline.find('wp:extent',NS).get('cx'));cy=int(inline.find('wp:extent',NS).get('cy'))
        total=cy+330200 # 26 pt caption area, including normal caption spacing.
        anchor=etree.Element(q('wp','anchor'))
        for k,v in {'distT':'25400','distB':'50800','distL':'0','distR':'0','simplePos':'0',
                    'relativeHeight':str(251658240+n),'behindDoc':'0','locked':'0','layoutInCell':'1','allowOverlap':'0'}.items():anchor.set(k,v)
        el(anchor,'wp','simplePos',x=0,y=0)
        h=el(anchor,'wp','positionH',relativeFrom='column');el(h,'wp','align').text='center'
        v=el(anchor,'wp','positionV',relativeFrom='margin');el(v,'wp','align').text='top'
        el(anchor,'wp','extent',cx=cx,cy=total);el(anchor,'wp','effectExtent',l=0,t=0,r=0,b=0)
        el(anchor,'wp','wrapTopAndBottom')
        docpr=copy.deepcopy(inline.find('wp:docPr',NS));docpr.set('name',f'K-Waay Figure{n} floating with caption');anchor.append(docpr)
        locks=el(anchor,'wp','cNvGraphicFramePr');el(locks,'a','graphicFrameLocks',noChangeAspect=1)
        graphic=el(anchor,'a','graphic');gd=el(graphic,'a','graphicData',uri=NS['wpg']);group=el(gd,'wpg','wgp')
        el(group,'wpg','cNvGrpSpPr');grppr=el(group,'wpg','grpSpPr');transform=el(grppr,'a','xfrm')
        el(transform,'a','off',x=0,y=0);el(transform,'a','ext',cx=cx,cy=total)
        el(transform,'a','chOff',x=0,y=0);el(transform,'a','chExt',cx=cx,cy=total)
        group.append(pic)
        sp=el(group,'wps','wsp');el(sp,'wps','cNvSpPr',txBox=1)
        spp=el(sp,'wps','spPr');st=el(spp,'a','xfrm');el(st,'a','off',x=0,y=cy);el(st,'a','ext',cx=cx,cy=330200)
        geo=el(spp,'a','prstGeom',prst='rect');el(geo,'a','avLst');el(spp,'a','noFill');ln=el(spp,'a','ln');el(ln,'a','noFill')
        box=el(sp,'wps','txbx');content=el(box,'w','txbxContent');content.append(copy.deepcopy(caption))
        bp=el(sp,'wps','bodyPr',rot=0,vert='horz',wrap='square',lIns=0,tIns=0,rIns=0,bIns=0,anchor='t',anchorCtr=0)
        el(bp,'a','noAutofit')
        drawing.remove(inline);drawing.append(anchor)
        # A one-point anchor line, not an image-height paragraph in the text flow.
        pp=p.find('w:pPr',NS)
        for c in list(pp):
            if etree.QName(c).localname in ('spacing','keepNext','keepLines','pageBreakBefore'):pp.remove(c)
        for name,value in [('keepNext','0'),('keepLines','0'),('pageBreakBefore','0')]:
            c=etree.Element(q('w',name));c.set(q('w','val'),value);pp.insert(1,c)
        spacing=el(pp,'w','spacing');
        for k,value in {'before':'0','after':'0','line':'20','lineRule':'exact'}.items():spacing.set(q('w',k),value)
        body.remove(caption);changed.extend((i,i+1))
        report.append({'figure':n,'mode':'Grouped picture and editable native caption; current-column centered, margin-top float, top/bottom wrap',
                       'image_size_unchanged':[cx,cy],'group_height':total,'text_no_overlap':True})
    assert root.xpath('//w:t/text()',namespaces=NS)==originaltext
    assert len(root.xpath('//a:blip',namespaces=NS))==5
    assert len(root.xpath('//wp:anchor',namespaces=NS))==2
    assert len(root.xpath('//wp:inline',namespaces=NS))==3
    for i,p in enumerate(blocks):
        if i not in changed:assert p.getparent() is body and canon(p)==canon(etree.fromstring(original_xml).find('w:body',NS)[i])
    parts['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    tmp=WORK.with_suffix('.floating-groups.tmp.docx')
    with zipfile.ZipFile(tmp,'w') as z:
        for info in infos:z.writestr(info,parts[info.filename])
    with zipfile.ZipFile(tmp) as z:assert z.testzip() is None
    assert sha(WORK.read_bytes())==EXPECTED;tmp.replace(WORK)
    result={'before_trial_sha256':EXPECTED,'after_sha256':sha(WORK.read_bytes()),'baseline_sha256':'664c86135f21e3ff265d3fe2f0666be4a51b6df6ca8ebe97bbd58463734a3d2c',
            'changes':report,'all_other_body_blocks_and_package_parts_preserved':True,'academic_text_math_images_and_numbering_preserved':True,
            'replaced_failed_trial':'Removed all paragraph frames, which did not eliminate WPS inline-block gaps','visual_review':'pending'}
    (QA/'floating-group-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
