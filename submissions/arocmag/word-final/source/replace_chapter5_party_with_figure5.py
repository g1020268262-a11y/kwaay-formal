"""Replace approved chapter5 only; embed supplied figure5 with Word display crop."""
import argparse
import copy
import json
import re
import sys
import zipfile
from pathlib import Path
from lxml import etree
from PIL import Image
from update_working_chapters_1_2 import Migration, NS, q, child, text, canonical, sha
from replace_chapter4_party import latex as base_latex, norm, TOKEN

HERE=Path(__file__).resolve().parent
OUT=HERE.parent
WORK=OUT/'K-Waay-AROCMAG-submission-working.docx'
SOURCE=HERE/'chapter5-party-author-approved.md'
IMAGE=OUT/'figures/fig5-party-admission-author-supplied.png'
QA=OUT/'qa/chapter5-party-replacement'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
REL='http://schemas.openxmlformats.org/package/2006/relationships'
DRAW={'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
      'wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
      'pic':'http://schemas.openxmlformats.org/drawingml/2006/picture'}
TOKEN5=re.compile(r'B=\(E₁,…,Eₙ\)|(?:party|Bind)\(E[ᵢⱼ]?\)|(?:sid|[AEmr])[₁₂ₙᵢⱼ]|m₁≠m₂|A≠B|(?<![A-Za-z0-9_])(?:bid|rst|sid|[ABijE])(?![A-Za-z0-9_])')
def latex(s):
    return re.sub(r'\b(Bind|Admit)\b',lambda m:r'\mathsf{'+m[0]+'}',base_latex(s))

class Edit(Migration):
    def __init__(self,package,deps):
        sys.path.insert(0,str(deps))
        from latex2mathml.converter import convert
        from mathml2omml import convert as omml
        self.to_mathml,self.to_omml=convert,omml
        self.root=etree.fromstring(package['word/document.xml'])
        self.body=self.root.find('w:body',NS);self.original=list(self.body)
        self.start=self.find_heading('K-Waay 批内去重与组合加固');self.end=self.find_heading('结束语')
        old=self.original[self.start:self.end]
        self.h1=old[0]
        def style(n):return next(p for p in old if p.xpath('./w:pPr/w:pStyle[@w:val="'+n+'"]',namespaces=NS))
        self.h2=style('66');self.prose=style('71');self.display=style('74')
        self.h3=next(p for p in self.original[:self.start] if p.xpath('./w:pPr/w:pStyle[@w:val="68"]',namespaces=NS))
        self.table_caption=next(p for p in old if re.match(r'表\s*4',text(p)))
        self.table_base=next(p for p in old if p.tag==q('w','tbl'))
        self.table_four=next(p for p in self.original if p.tag==q('w','tbl') and len(p.find('w:tr',NS).findall('w:tc',NS))==4)
        self.fig4=next(p for p in self.original if p.xpath('.//wp:docPr[@name="K-Waay monochrome combined Figure 4"]',namespaces=DRAW))
        self.figure_caption=self.original[self.original.index(self.fig4)+1]
        self.rels=etree.fromstring(package['word/_rels/document.xml.rels'])
        self.blocks=[];self.math_records=[];self.source_records=[];self.rows=[];self.number=22

    def para(self,src,template=None):
        template=template if template is not None else self.prose
        p=self.blank(template);src=src.replace('**','')
        for i,segment in enumerate(re.split(r'`([^`]+)`',src)):
            if i%2:
                if segment=='accepted_batch_has_distinct_parties':self.run(p,segment,template=template)
                else:p.append(self.math(latex(segment)))
                continue
            pos=0
            for match in TOKEN5.finditer(segment):
                self.run(p,segment[pos:match.start()],template=template);p.append(self.math(latex(match[0])));pos=match.end()
            self.run(p,segment[pos:],template=template)
        self.source_records.append({'kind':'paragraph','source':src,'actual':text(p)})
        return p

    def formula(self,src):
        p=self.blank(self.display);parts=[src]
        if src.startswith('DistinctPartyPerBatch(B)'):
            first,second=src.split('⇔');parts=[first,'⇔ '+second]
        elif src.startswith('ReceiverAccept('):
            first,second=src.split('(',1);parts=[first,'('+second]
        for i,part in enumerate(parts):
            if i:child(child(p,'w','r'),'w','br')
            child(child(p,'w','r'),'w','tab');p.append(self.math(latex(part)))
        self.number+=1
        child(child(p,'w','r'),'w','tab');self.run(p,'('+str(self.number)+')',template=self.display)
        self.source_records.append({'kind':'equation','source':src,'actual':text(p),'number':self.number,'lines':parts})
        return p

    def make_table(self,rows):
        assert len(rows)==7 and all(len(r)==4 for r in rows)
        tbl=copy.deepcopy(self.table_four);prototypes=tbl.findall('w:tr',NS)
        for row in prototypes:tbl.remove(row)
        widths=[1620,850,1000,1122]
        for c,width in zip(tbl.find('w:tblGrid',NS),widths):c.set(q('w','w'),str(width))
        tw=tbl.find('w:tblPr/w:tblW',NS);tw.set(q('w','w'),str(sum(widths)));tw.set(q('w','type'),'dxa')
        for i,values in enumerate(rows):
            row=copy.deepcopy(prototypes[0] if i==0 else prototypes[-1] if i==len(rows)-1 else prototypes[1])
            for c,width,value in zip(row.findall('w:tc',NS),widths,values):
                c.find('w:tcPr/w:tcW',NS).set(q('w','w'),str(width))
                prototype=c.find('w:p',NS);p=self.blank(prototype);self.run(p,value,template=prototype)
                pp=p.find('w:pPr',NS);jc=pp.find('w:jc',NS)
                if jc is None:jc=child(pp,'w','jc')
                jc.set(q('w','val'),'center' if i==0 else 'left')
                for x in list(c):
                    if x.tag!=q('w','tcPr'):c.remove(x)
                c.append(p)
            for height in row.xpath('./w:trPr/w:trHeight',namespaces=NS):height.getparent().remove(height)
            if i==0:
                pr=row.find('w:trPr',NS)
                if pr is None:pr=etree.Element(q('w','trPr'));row.insert(0,pr)
                if pr.find('w:tblHeader',NS) is None:child(pr,'w','tblHeader')
            tbl.append(row)
        self.rows=rows;return tbl

    def add_figure(self):
        image=copy.deepcopy(self.fig4);rid='rIdKwaayFigure5PartyAdmission'
        assert not any(r.get('Id')==rid for r in self.rels)
        rel=etree.SubElement(self.rels,'{'+REL+'}Relationship');rel.set('Id',rid);rel.set('Type',R+'/image');rel.set('Target','media/kwaay-figure5-party-admission.png')
        for blip in image.xpath('.//a:blip',namespaces=DRAW):blip.set('{'+R+'}embed',rid)
        new_id=max(map(int,self.root.xpath('//wp:docPr/@id',namespaces=DRAW)))+1
        title='K-Waay批次身份绑定准入流程'
        for dp in image.xpath('.//wp:docPr',namespaces=DRAW):
            dp.set('id',str(new_id));dp.set('name','K-Waay Figure5 party admission');dp.set('descr',title)
        for dp in image.xpath('.//pic:cNvPr',namespaces=DRAW):dp.set('id',str(new_id));dp.set('name','Figure5 party admission')
        with Image.open(IMAGE) as im:iw,ih=im.size
        assert (iw,ih)==(1536,1024)
        width=3126105;cut=60;height=round(width*(ih-cut)/iw)
        fill=image.find('.//pic:blipFill',namespaces=DRAW)
        assert fill.find('a:srcRect',namespaces=DRAW) is None
        crop=etree.Element('{'+DRAW['a']+'}srcRect');crop.set('l','0');crop.set('t',str(round(100000*cut/ih)));crop.set('r','0');crop.set('b','0')
        fill.insert(1,crop)
        for ex in image.xpath('.//wp:extent|.//a:xfrm/a:ext',namespaces=DRAW):ex.set('cx',str(width));ex.set('cy',str(height))
        self.blocks.append(image)
        caption=self.blank(self.figure_caption);self.run(caption,'图',template=self.figure_caption)
        for kind,value in [('begin',None),('instruction',' SEQ Figure \\r 5 \\* ARABIC '),('separate',None),('result','5'),('end',None)]:
            run=child(caption,'w','r')
            if kind in ('begin','separate','end'):
                x=child(run,'w','fldChar');x.set(q('w','fldCharType'),kind)
            elif kind=='instruction':
                x=child(run,'w','instrText');x.set('{http://www.w3.org/XML/1998/namespace}space','preserve');x.text=value
            else:child(run,'w','t').text=value
        self.run(caption,' '+title,template=self.figure_caption);self.blocks.append(caption)
        self.figure_size={'width_cm':width/360000,'height_cm':height/360000,'crop_top_pixels':cut,'crop_top_value':crop.get('t')}

    def build(self,src):
        for chunk in re.split(r'\n\s*\n',src.strip()):
            if '【图5插入位置' in chunk:self.add_figure();continue
            if chunk.startswith('#'):
                m=re.fullmatch(r'(#{1,3})\s+[\d.]+\s+(.+)',chunk);assert m
                self.blocks.append(self.para(m[2],[self.h1,self.h2,self.h3][len(m[1])-1]))
            elif chunk.startswith('|'):
                rows=[[v.strip() for v in line.strip('|').split('|')] for line in chunk.splitlines() if not re.match(r'\|\s*-',line)]
                self.blocks.append(self.make_table(rows))
            elif chunk.startswith('**表4 '):self.blocks.append(self.para(chunk,self.table_caption))
            elif re.fullmatch(r'`[^`]+`',chunk):self.blocks.append(self.formula(chunk[1:-1]))
            else:self.blocks.append(self.para(chunk))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--expected-sha',required=True);ap.add_argument('--math-deps',type=Path,required=True);a=ap.parse_args()
    original=WORK.read_bytes();assert sha(original)==a.expected_sha,'Working file changed; inspect first'
    with zipfile.ZipFile(WORK) as z:infos=z.infolist();package={n:z.read(n) for n in z.namelist()}
    origparts=dict(package);edit=Edit(package,a.math_deps);edit.build(SOURCE.read_text('utf-8-sig'))
    for rec in edit.source_records:
        actual=rec['actual']
        if rec.get('number') is not None:actual=actual.removesuffix('('+str(rec['number'])+')')
        assert norm(rec['source'])==norm(actual),(ascii(rec['source']),ascii(actual))
    actualrows=[[text(c) for c in row.findall('w:tc',NS)] for row in next(p for p in edit.blocks if p.tag==q('w','tbl')).findall('w:tr',NS)]
    assert actualrows==edit.rows
    prefix=edit.original[:edit.start];tail=edit.original[edit.end:]
    for p in edit.original[edit.start:edit.end]:edit.body.remove(p)
    for i,p in enumerate(edit.blocks):edit.body.insert(edit.start+i,p)
    assert [canonical(p) for p in list(edit.body)[:edit.start]]==[canonical(p) for p in prefix]
    assert [canonical(p) for p in list(edit.body)[edit.start+len(edit.blocks):]]==[canonical(p) for p in tail]
    assert len([p for p in edit.blocks if p.xpath('./w:pPr/w:pStyle[@w:val="66"]',namespaces=NS)])==5
    assert len([p for p in edit.blocks if p.xpath('./w:pPr/w:pStyle[@w:val="68"]',namespaces=NS)])==6
    assert edit.number==32
    assert len(edit.root.xpath('//w:drawing',namespaces=NS))==5
    ids=edit.root.xpath('//wp:docPr/@id',namespaces=DRAW);assert len(ids)==len(set(ids))
    assert not any(p.xpath('.//w:del|.//w:ins',namespaces=NS) for p in edit.blocks)
    package['word/document.xml']=etree.tostring(edit.root,xml_declaration=True,encoding='UTF-8',standalone=True)
    package['word/_rels/document.xml.rels']=etree.tostring(edit.rels,xml_declaration=True,encoding='UTF-8',standalone=True)
    media='word/media/kwaay-figure5-party-admission.png';assert media not in package;package[media]=IMAGE.read_bytes()
    unchanged=[n for n in origparts if n not in ('word/document.xml','word/_rels/document.xml.rels')]
    for n in unchanged:assert package[n]==origparts[n]
    tmp=WORK.with_suffix('.party-ch5.tmp.docx')
    with zipfile.ZipFile(tmp,'w') as z:
        for info in infos:z.writestr(info,package[info.filename])
        z.writestr(media,package[media])
    with zipfile.ZipFile(tmp) as z:
        assert z.testzip() is None
        for n in z.namelist():
            if n.endswith('.xml') or n.endswith('.rels'):etree.fromstring(z.read(n))
        for n in unchanged:assert z.read(n)==origparts[n]
    assert sha(WORK.read_bytes())==a.expected_sha;tmp.replace(WORK)
    QA.mkdir(parents=True,exist_ok=True)
    manifest={'before_sha256':a.expected_sha,'after_sha256':sha(WORK.read_bytes()),'source_sha256':sha(SOURCE.read_bytes()),
        'figure5_sha256':sha(IMAGE.read_bytes()),'chapter0_4_and6_onwards_unchanged':True,'new_subsections':5,'new_subsubsections':6,
        'math':'Native editable OMML; not MathType OLE','chapter5_omml_count':len(edit.math_records),'chapter5_equation_numbers':list(range(23,33)),
        'source_equivalence':'Every author paragraph, equation, table cell passed; no academic wording changes',
        'table4':edit.rows,'figure5':edit.figure_size,'figure5_location':'5.3, author placeholder before existing explanation paragraph',
        'image_crop':'Non-destructive native Word display crop hides top duplicate title only; original PNG retained',
        'unchanged_package_parts':unchanged,'visual_review':'Not performed: standing instruction deferred WPS; no bundled LibreOffice was returned',
        'source_records':edit.source_records}
    (QA/'replacement-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
    (QA/'formula-conversion.json').write_text(json.dumps(edit.math_records,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k not in ('source_records','unchanged_package_parts','table4')},ensure_ascii=False,indent=2))

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');main()
