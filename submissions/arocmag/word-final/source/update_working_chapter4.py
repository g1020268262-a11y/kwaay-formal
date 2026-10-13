"""Mechanical, hash-guarded chapter 4 replacement in the existing working DOCX.

Preserves every body block outside chapter 4 and all package parts except
document.xml/core.xml. No proof execution, manuscript rewriting or GUI use.
"""
from __future__ import annotations
import argparse
import copy
import json
import re
import sys
import zipfile
from pathlib import Path
from lxml import etree
from update_working_chapter3 import Chapter3, NS, q, child, text, canonical, sha

HERE=Path(__file__).resolve().parent
OUT=HERE.parent
WORK=OUT/'K-Waay-AROCMAG-submission-working.docx'
SOURCE=HERE/'chapter4-approved.md'
QA=OUT/'qa/working-chapter4'
EVENTS=('ConfirmedSend','ConfirmedReceiverAccept','BatchComplete',
        'ReceiverAccept','InstallSession','AcceptOutputCreated')
VARIABLE=r'(?:idx|aid)[₁₂]|h[₁₂]|(?:bid|rst|sid|tag|aid|idx|[ABMmhk])'
TOKEN=re.compile(r'(?<![A-Za-z0-9_])(?:M=\(m,tag\)|(?:idx|aid)[₁₂]≠(?:idx|aid)[₁₂]|h₁≠h₂|'+VARIABLE+r')(?![A-Za-z0-9_])')


def latex4(src):
    src=src.replace('≠',r'\ne ')
    src=re.sub(r'([A-Za-z]+)([₁₂])',lambda m: m[1]+'_{'+{'₁':'1','₂':'2'}[m[2]]+'}',src)
    src=re.sub(r'\b(confirm_key|HMAC|'+'|'.join(EVENTS)+r')\b',
               lambda m: r'\mathsf{'+m[0].replace('_',r'\_')+'}',src)
    src=re.sub(r'\b(bid|rst|sid|tag|aid|idx)\b',lambda m:r'\mathit{'+m[0]+'}',src)
    return src


def normalize(src):
    return re.sub(r'[\s_*`]','',src.translate(str.maketrans({'₁':'1','₂':'2','′':"'"})))


class Chapter4(Chapter3):
    def __init__(self,package,deps):
        sys.path.insert(0,str(deps))
        from latex2mathml.converter import convert
        from mathml2omml import convert as omml
        self.to_mathml,self.to_omml=convert,omml
        self.package=package
        self.root=etree.fromstring(package['word/document.xml'])
        self.body=self.root.find('w:body',NS)
        self.original=list(self.body)
        self.start=self.find_heading('结果讨论与适用范围')
        self.end=self.find_heading('结束语')
        self.h1=self.original[self.start]
        self.h2=self.original[self.start+1]
        self.h3=next(p for p in self.original[:self.start]
                     if p.xpath('./w:pPr/w:pStyle[@w:val="68"]',namespaces=NS))
        self.prose=self.original[self.start+2]
        self.display=next(p for p in self.original[:self.start]
                         if p.xpath('./w:pPr/w:pStyle[@w:val="74"]',namespaces=NS))
        self.caption=next(p for p in self.original[:self.start] if text(p).startswith('表2 '))
        self.table_base=next(p for p in self.original[:self.start]
                             if p.tag==q('w','tbl') and len(p.find('w:tr',NS).findall('w:tc',NS))==4)
        self.blocks,self.math_records,self.source_records=[],[],[]
        self.number=21
        self.rows=[]

    def rich(self,p,src,template,bold=False):
        pos=0
        for match in re.finditer(r'\*\*(.+?)\*\*|`([^`]+)`',src):
            self.plain_math(p,src[pos:match.start()],template,bold)
            if match[1] is not None:
                self.rich(p,match[1],template,True)
            elif any(match[2]==name or match[2].startswith(name+'(') for name in EVENTS):
                p.append(self.math(latex4(match[2])))
            else:
                # Lemma names are code identifiers, not subscripted formulas.
                self.put_run(p,match[2],template,bold)
            pos=match.end()
        self.plain_math(p,src[pos:],template,bold)

    def plain_math(self,p,src,template,bold):
        pos=0
        for match in TOKEN.finditer(src):
            self.put_run(p,src[pos:match.start()],template,bold)
            p.append(self.math(latex4(match[0])))
            pos=match.end()
        self.put_run(p,src[pos:],template,bold)

    def formula(self,src):
        p=self.blank(self.display)
        parts=[src]
        if src.startswith(('ConfirmedReceiverAccept(','AcceptOutputCreated(')):
            cut=src.index('(')
            parts=[src[:cut],src[cut:]]
        for i,part in enumerate(parts):
            if i: child(child(p,'w','r'),'w','br')
            p.append(self.math(latex4(part),display=True))
        self.number+=1
        r=child(p,'w','r')
        rp=self.display.find('w:r/w:rPr',NS)
        if rp is not None: r.append(copy.deepcopy(rp))
        child(r,'w','tab')
        child(r,'w','t').text='('+str(self.number)+')'
        self.source_records.append({'kind':'equation','source':src,'number':self.number,'layout_lines':parts})
        return p

    def make_table(self,rows):
        assert len(rows)==8 and all(len(row)==4 for row in rows)
        tbl=copy.deepcopy(self.table_base)
        prototypes=tbl.findall('w:tr',NS)
        for row in prototypes: tbl.remove(row)
        widths=[1020,1842,991,739]  # total 4592 twips, a single 8.1 cm column
        for c,width in zip(tbl.find('w:tblGrid',NS),widths):
            c.set(q('w','w'),str(width))
        tw=tbl.find('w:tblPr/w:tblW',NS)
        tw.set(q('w','w'),str(sum(widths))); tw.set(q('w','type'),'dxa')
        for i,values in enumerate(rows):
            row=copy.deepcopy(prototypes[0] if i==0 else prototypes[-1] if i==len(rows)-1 else prototypes[1])
            for cell,width,value in zip(row.findall('w:tc',NS),widths,values):
                cell.find('w:tcPr/w:tcW',NS).set(q('w','w'),str(width))
                prototype=cell.find('w:p',NS)
                p=self.blank(prototype)
                self.rich(p,value,prototype)
                for c in list(cell):
                    if c.tag!=q('w','tcPr'): cell.remove(c)
                cell.append(p)
            tbl.append(row)
        self.rows=rows
        return tbl

    def consume_approved(self,src):
        for chunk in re.split(r'\n\s*\n',src.strip()):
            if chunk.startswith('#'):
                match=re.fullmatch(r'(#{1,3})\s+[0-9.]+\s+(.+)',chunk)
                assert match,chunk
                self.blocks.append(self.para(match[2],[self.h1,self.h2,self.h3][len(match[1])-1]))
            elif chunk.startswith('|'):
                rows=[[v.strip() for v in line.strip('|').split('|')]
                      for line in chunk.splitlines() if not re.match(r'\|\s*-',line)]
                self.blocks.append(self.make_table(rows))
            elif chunk.startswith('**表3 '):
                self.blocks.append(self.para(chunk[2:-2],self.caption))
            elif re.fullmatch(r'`[^`]+`',chunk):
                self.blocks.append(self.formula(chunk[1:-1]))
            elif chunk.startswith('*【图3'):
                p=self.para(chunk[1:-1])
                for rp in p.xpath('./w:r/w:rPr',namespaces=NS): child(rp,'w','i')
                self.blocks.append(p)
            else:
                self.blocks.append(self.para(chunk))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--expected-sha',required=True)
    ap.add_argument('--math-deps',type=Path,required=True)
    args=ap.parse_args()
    data=WORK.read_bytes()
    assert sha(data)==args.expected_sha,'Working manuscript changed; inspect again.'
    with zipfile.ZipFile(WORK) as z:
        infos=z.infolist(); package={n:z.read(n) for n in z.namelist()}
    edit=Chapter4(package,args.math_deps)
    source=SOURCE.read_text('utf-8')
    edit.consume_approved(source)
    prefix=edit.original[:edit.start]; tail=edit.original[edit.end:]
    for p in edit.original[edit.start:edit.end]: edit.body.remove(p)
    for i,p in enumerate(edit.blocks): edit.body.insert(edit.start+i,p)
    assert [canonical(p) for p in list(edit.body)[:edit.start]]==[canonical(p) for p in prefix]
    assert [canonical(p) for p in list(edit.body)[edit.start+len(edit.blocks):]]==[canonical(p) for p in tail]
    assert edit.number==29
    for record,p in zip(edit.source_records,[p for p in edit.blocks if p.tag!=q('w','tbl')]):
        actual=text(p)
        if record['kind']=='equation': actual=actual.removesuffix('('+str(record['number'])+')')
        assert normalize(record['source'])==normalize(actual),(record['source'],actual)
    assert not any(p.xpath('.//w:drawing|.//w:pict|.//w:del|.//w:ins|.//w:vanish',namespaces=NS) for p in edit.blocks)
    package['word/document.xml']=etree.tostring(edit.root,xml_declaration=True,encoding='UTF-8',standalone=True)
    core=etree.fromstring(package['docProps/core.xml'])
    dc='http://purl.org/dc/elements/1.1/'
    desc=core.find('{'+dc+'}description')
    if desc is not None: desc.text='部分更新工作稿：第1至4章已替换；第5章及后续内容尚待衔接；非最终可投稿版本。公式为可编辑 OMML，非 MathType OLE。本次仅完成文件级检查，未做实际排版验收。'
    package['docProps/core.xml']=etree.tostring(core,xml_declaration=True,encoding='UTF-8',standalone=True)
    temp=WORK.with_suffix('.chapter4.tmp.docx')
    with zipfile.ZipFile(temp,'w') as z:
        for info in infos: z.writestr(info,package[info.filename])
    with zipfile.ZipFile(temp) as z:
        assert z.testzip() is None
        assert z.namelist()==[info.filename for info in infos]
        assert z.read('word/document.xml')==package['word/document.xml']
    assert sha(WORK.read_bytes())==args.expected_sha
    temp.replace(WORK)
    QA.mkdir(parents=True,exist_ok=True)
    manifest={'base_working_sha256':args.expected_sha,'working_sha256':sha(WORK.read_bytes()),
              'approved_source_sha256':sha(SOURCE.read_bytes()),
              'prefix_blocks_preserved':len(prefix),'tail_blocks_preserved':len(tail),
              'original_chapter4_blocks_removed':edit.end-edit.start,'new_chapter4_blocks':len(edit.blocks),
              'unchanged_package_parts':[n for n in package if n not in ('word/document.xml','docProps/core.xml')],
              'heading_styles':{'level1':'65','level2':'66','level3':'68'},
              'equation_numbers':list(range(22,30)),
              'chapter4_omml_count':len(edit.math_records),'math_format':'editable OMML, not MathType OLE',
              'table3':[[v.replace('**','') for v in row] for row in edit.rows],
              'figure3':'author-supplied italic reservation text only; no image',
              'verbatim_content_audit':'all author paragraphs and displays passed',
              'visual_qa':'not performed; no WPS or Word opened, no preview PDF generated',
              'remaining_issue':'第5章当前仍为旧版结束语，新第4章所述第5章去重与组合加固尚未替换；旧摘要、引言与结尾仍待作者提供后续正文。',
              'source_records':edit.source_records}
    (QA/'replacement-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
    (QA/'formula-conversion.json').write_text(json.dumps(edit.math_records,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k not in ('source_records','unchanged_package_parts')},ensure_ascii=False))


if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
