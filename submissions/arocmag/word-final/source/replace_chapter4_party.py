"""Deterministic author-text replacement of chapter4 only, preserving other blocks."""
import argparse
import copy
import json
import re
import sys
import zipfile
from pathlib import Path
from lxml import etree
from update_working_chapters_1_2 import Migration, NS, q, child, text, canonical, sha

HERE=Path(__file__).resolve().parent
OUT=HERE.parent
WORK=OUT/'K-Waay-AROCMAG-submission-working.docx'
SOURCE=HERE/'chapter4-party-author-approved.md'
QA=OUT/'qa/chapter4-party-replacement'
SUBS={'₁':'1','₂':'2','ₙ':'n','ᵢ':'i','ⱼ':'j'}
TOKEN=re.compile(r'B=\(E₁,…,Eₙ\)|party\(Eᵢ\)|m₁≠m₂|A≠B|(?:sid|[AEmr])[₁₂ₙᵢⱼ]|k_j|(?<![A-Za-z0-9_])(?:bid|rst|sid|[ABijs])(?![A-Za-z0-9_])')

def latex(s):
    if re.search('[\u4e00-\u9fff]',s):
        # Chinese labels remain native editable math-text runs, not Latin variables.
        return re.sub(r'([\u4e00-\u9fff]+[0-9：]*)',lambda m:r'\text{'+m[0]+'}',s).replace('→',r'\to ')
    s=s.replace('≠',r'\ne ').replace('⇔',r'\Leftrightarrow ').replace('∀',r'\forall ').replace('，',',')
    s=re.sub(r'([A-Za-z]+)([₁₂ₙᵢⱼ])',lambda m:m[1]+'_{'+SUBS[m[2]]+'}',s)
    s=re.sub(r'\b(DistinctPartyPerBatch|ReceiverAccept|Send|KEY|TEST|party)\b',lambda m:r'\mathsf{'+m[0]+'}',s)
    s=re.sub(r'\b(sid|bid|rst)\b',lambda m:r'\mathit{'+m[0]+'}',s)
    return s

def norm(s):
    s=s.translate(str.maketrans(SUBS)).replace('′',"'").replace('，',',')
    return re.sub(r'[\s_`*,]','',s)

class Edit(Migration):
    def __init__(self,package,deps):
        sys.path.insert(0,str(deps))
        from latex2mathml.converter import convert
        from mathml2omml import convert as omml
        self.to_mathml,self.to_omml=convert,omml
        self.root=etree.fromstring(package['word/document.xml'])
        self.body=self.root.find('w:body',NS);self.original=list(self.body)
        self.start=self.find_heading('K-Waay 批内重放攻击与安全影响分析')
        self.end=self.find_heading('K-Waay 批内去重与组合加固')
        old=self.original[self.start:self.end]
        self.h1=old[0]
        def style(n):return next(p for p in old if p.xpath('./w:pPr/w:pStyle[@w:val="'+n+'"]',namespaces=NS))
        self.h2=style('66');self.h3=style('68');self.prose=style('71');self.display=style('74')
        self.caption=next(p for p in old if re.match(r'表\s*3',text(p)))
        self.table_base=next(p for p in old if p.tag==q('w','tbl'))
        self.blocks=[];self.math_records=[];self.source_records=[];self.rows=[];self.number=20

    def para(self,src,template=None):
        template=template if template is not None else self.prose
        p=self.blank(template);src=src.replace('**','')
        for i,segment in enumerate(re.split(r'`([^`]+)`',src)):
            if i%2:
                if segment in ('one_send_two_accepts_exists','receiver_accept_injective'):
                    self.run(p,segment,template=template)
                else:p.append(self.math(latex(segment)))
                continue
            pos=0
            for match in TOKEN.finditer(segment):
                self.run(p,segment[pos:match.start()],template=template)
                p.append(self.math(latex(match[0])));pos=match.end()
            self.run(p,segment[pos:],template=template)
        self.source_records.append({'kind':'paragraph','source':src,'actual':text(p)})
        return p

    def formula(self,src):
        p=self.blank(self.display);parts=[src];number=None
        if src.startswith('DistinctPartyPerBatch(B)'):
            first,second=src.split('⇔');parts=[first,'⇔ '+second]
        elif src.startswith('ReceiverAccept('):
            first,second=src.split('(',1);parts=[first,'('+second]
        elif '，' in src:parts=src.split('，')
        for i,part in enumerate(parts):
            if i:child(child(p,'w','r'),'w','br')
            child(child(p,'w','r'),'w','tab');p.append(self.math(latex(part)))
        # Number definitions, not every event trace or explanatory arrow example.
        if src.startswith(('DistinctPartyPerBatch(B)','Eᵢ =')):
            self.number+=1;number=self.number
            child(child(p,'w','r'),'w','tab');self.run(p,'('+str(number)+')',template=self.display)
        self.source_records.append({'kind':'equation','source':src,'actual':text(p),'number':number,'lines':parts})
        return p

    def make_table(self,rows):
        assert len(rows)==6 and all(len(row)==3 for row in rows)
        tbl=copy.deepcopy(self.table_base);prototypes=tbl.findall('w:tr',NS)
        for row in prototypes:tbl.remove(row)
        widths=[860,2632,1100]
        grid=tbl.find('w:tblGrid',NS)
        for c in list(grid):grid.remove(c)
        for width in widths:
            c=child(grid,'w','gridCol');c.set(q('w','w'),str(width))
        tw=tbl.find('w:tblPr/w:tblW',NS);tw.set(q('w','w'),str(sum(widths)));tw.set(q('w','type'),'dxa')
        for i,values in enumerate(rows):
            row=copy.deepcopy(prototypes[0] if i==0 else prototypes[-1] if i==len(rows)-1 else prototypes[1])
            cells=row.findall('w:tc',NS)
            for c in cells[3:]:row.remove(c)
            for c,width,value in zip(cells[:3],widths,values):
                c.find('w:tcPr/w:tcW',NS).set(q('w','w'),str(width))
                prototype=c.find('w:p',NS);p=self.blank(prototype)
                self.run(p,value,template=prototype)
                pp=p.find('w:pPr',NS)
                jc=pp.find('w:jc',NS)
                if jc is None:jc=child(pp,'w','jc')
                jc.set(q('w','val'),'center' if i==0 or c is cells[0] else 'left')
                for x in list(c):
                    if x.tag!=q('w','tcPr'):c.remove(x)
                c.append(p)
            # No fixed row heights: let the longer author text wrap naturally.
            for height in row.xpath('./w:trPr/w:trHeight',namespaces=NS):height.getparent().remove(height)
            tbl.append(row)
        self.rows=rows;return tbl

    def build(self,src):
        for chunk in re.split(r'\n\s*\n',src.strip()):
            if chunk.startswith('#'):
                m=re.fullmatch(r'(#{1,3})\s+[\d.]+\s+(.+)',chunk);assert m
                self.blocks.append(self.para(m[2],[self.h1,self.h2,self.h3][len(m[1])-1]))
            elif chunk.startswith('|'):
                rows=[[v.strip() for v in line.strip('|').split('|')] for line in chunk.splitlines() if not re.match(r'\|\s*-',line)]
                self.blocks.append(self.make_table(rows))
            elif chunk.startswith('**表3 '):self.blocks.append(self.para(chunk,self.caption))
            elif re.fullmatch(r'`[^`]+`',chunk):self.blocks.append(self.formula(chunk[1:-1]))
            else:self.blocks.append(self.para(chunk))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--expected-sha',required=True);ap.add_argument('--math-deps',type=Path,required=True);a=ap.parse_args()
    original=WORK.read_bytes();assert sha(original)==a.expected_sha,'Work changed; inspect before replacing'
    with zipfile.ZipFile(WORK) as z:infos=z.infolist();package={n:z.read(n) for n in z.namelist()}
    edit=Edit(package,a.math_deps);edit.build(SOURCE.read_text('utf-8'))
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
    assert len([p for p in edit.blocks if p.xpath('./w:pPr/w:pStyle[@w:val="66"]',namespaces=NS)])==4
    assert len([p for p in edit.blocks if p.xpath('./w:pPr/w:pStyle[@w:val="68"]',namespaces=NS)])==4
    assert edit.number==22
    assert not any(p.xpath('.//w:drawing|.//w:ins|.//w:del',namespaces=NS) for p in edit.blocks)
    package['word/document.xml']=etree.tostring(edit.root,xml_declaration=True,encoding='UTF-8',standalone=True)
    tmp=WORK.with_suffix('.party-ch4.tmp.docx')
    with zipfile.ZipFile(tmp,'w') as z:
        for info in infos:z.writestr(info,package[info.filename])
    with zipfile.ZipFile(tmp) as z:
        assert z.testzip() is None
        for n in z.namelist():
            if n.endswith('.xml') or n.endswith('.rels'):etree.fromstring(z.read(n))
    assert sha(WORK.read_bytes())==a.expected_sha
    tmp.replace(WORK)
    QA.mkdir(parents=True,exist_ok=True)
    manifest={'before_sha256':a.expected_sha,'after_sha256':sha(WORK.read_bytes()),'source_sha256':sha(SOURCE.read_bytes()),
       'other_chapters_canonical_preserved':True,'unchanged_package_parts':[n for n in package if n!='word/document.xml'],
       'heading_styles':{'level1':'65','level2':'66','level3':'68'},'new_math_objects':len(edit.math_records),
       'numbered_definitions':[21,22],'trace_equations':'editable OMML, intentionally unnumbered',
       'table3':edit.rows,'source_equivalence':'every paragraph, formula and table cell passed',
       'wording_changes':[],'visual_review':'Deferred under existing user instruction; WPS not opened',
       'pending':['Chapter4 closing transition refers to participant admission, while current unchanged chapter5 still covers message dedup/composition',
                  'Old chapter5 retains equations30/31; gap23–29 awaits chapter5 replacement and final numbering review',
                  'Final physical table/formula wrapping and page layout need actual rendered review'],
       'source_records':edit.source_records}
    (QA/'replacement-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
    (QA/'formula-conversion.json').write_text(json.dumps(edit.math_records,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k not in ('unchanged_package_parts','source_records','table3')},ensure_ascii=False,indent=2))

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');main()
