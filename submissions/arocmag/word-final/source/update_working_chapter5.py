"""Replace author-approved chapter 5 only, preserving the inspected working ZIP.

Uses a SHA guard and canonical outside-range comparisons. No research, GUI,
new figures, or regeneration of the paper. Formula transport is native OMML.
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
SOURCE=HERE/'chapter5-approved.md'
QA=OUT/'qa/working-chapter5'
TOKEN=re.compile(r'(?<![A-Za-z0-9_])(?:m=\(ct_l,ct_k,ct_s\)|m[₁₂]|m)(?![A-Za-z0-9_])')


def latex5(src):
    src=re.sub(r'([A-Za-z]+)([₁₂ᵢ])',lambda m:m[1]+'_{'+{'₁':'1','₂':'2','ᵢ':'i'}[m[2]]+'}',src)
    src=re.sub(r'\b(confirm_key|HMAC)\b',lambda m:r'\mathsf{'+m[0].replace('_',r'\_')+'}',src)
    src=re.sub(r'\b(tag|sid)\b',lambda m:r'\mathit{'+m[0]+'}',src)
    src=re.sub(r'ct_([lks])',lambda m:r'\mathit{ct}_{'+m[1]+'}',src)
    return src


def norm(src):
    return re.sub(r'[\s_*`]','',src.translate(str.maketrans({'₁':'1','₂':'2','ᵢ':'i'})))


class Chapter5(Chapter3):
    def __init__(self,package,deps):
        sys.path.insert(0,str(deps))
        from latex2mathml.converter import convert
        from mathml2omml import convert as omml
        self.to_mathml,self.to_omml=convert,omml
        self.package=package
        self.root=etree.fromstring(package['word/document.xml'])
        self.body=self.root.find('w:body',NS)
        self.original=list(self.body)
        self.start=self.find_heading('结束语')
        matches=[i for i,p in enumerate(self.body) if text(p)=='参考文献' and
                 p.xpath('./w:pPr/w:pStyle[@w:val="82"]',namespaces=NS)]
        assert len(matches)==1
        self.end=matches[0]
        self.h1=self.original[self.start]
        self.h2=next(p for p in self.original[:self.start] if p.xpath('./w:pPr/w:pStyle[@w:val="66"]',namespaces=NS))
        self.prose=self.original[self.start+1]
        self.display=next(p for p in self.original[:self.start] if p.xpath('./w:pPr/w:pStyle[@w:val="74"]',namespaces=NS))
        self.caption=next(p for p in self.original[:self.start] if text(p).startswith('表2 '))
        self.table_base=next(p for p in self.original[:self.start] if p.tag==q('w','tbl') and
                             len(p.find('w:tr',NS).findall('w:tc',NS))==3)
        self.blocks,self.math_records,self.source_records=[],[],[]
        self.number=29
        self.rows=[]

    def plain_math(self,p,src,template,bold):
        pos=0
        for match in TOKEN.finditer(src):
            self.put_run(p,src[pos:match.start()],template,bold)
            p.append(self.math(latex5(match[0])))
            pos=match.end()
        self.put_run(p,src[pos:],template,bold)

    def rich(self,p,src,template,bold=False):
        pos=0
        for match in re.finditer(r'\*\*(.+?)\*\*|`([^`]+)`',src):
            self.plain_math(p,src[pos:match.start()],template,bold)
            if match[1] is not None: self.rich(p,match[1],template,True)
            else: p.append(self.math(latex5(match[2])))
            pos=match.end()
        self.plain_math(p,src[pos:],template,bold)

    def formula(self,src):
        p=self.blank(self.display)
        p.append(self.math(latex5(src),display=True))
        self.number+=1
        r=child(p,'w','r')
        rp=self.display.find('w:r/w:rPr',NS)
        if rp is not None: r.append(copy.deepcopy(rp))
        child(r,'w','tab')
        child(r,'w','t').text='('+str(self.number)+')'
        self.source_records.append({'kind':'equation','source':src,'number':self.number})
        return p

    def make_table(self,rows):
        assert len(rows)==7 and all(len(row)==3 for row in rows)
        tbl=copy.deepcopy(self.table_base)
        prototypes=tbl.findall('w:tr',NS)
        for row in prototypes: tbl.remove(row)
        for i,values in enumerate(rows):
            row=copy.deepcopy(prototypes[0] if i==0 else prototypes[-1] if i==len(rows)-1 else prototypes[1])
            for cell,value in zip(row.findall('w:tc',NS),values):
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
                match=re.fullmatch(r'(#{1,2})\s+[0-9.]+\s+(.+)',chunk)
                assert match,chunk
                self.blocks.append(self.para(match[2],self.h1 if len(match[1])==1 else self.h2))
            elif chunk.startswith('|'):
                rows=[[v.strip() for v in line.strip('|').split('|')]
                      for line in chunk.splitlines() if not re.match(r'\|\s*-',line)]
                self.blocks.append(self.make_table(rows))
            elif chunk.startswith('**表4 '): self.blocks.append(self.para(chunk[2:-2],self.caption))
            elif chunk=='**m₁ = m₂**': self.blocks.append(self.formula(chunk[2:-2]))
            elif re.fullmatch(r'`[^`]+`',chunk): self.blocks.append(self.formula(chunk[1:-1]))
            elif chunk.startswith('*【图4'):
                p=self.para(chunk[1:-1])
                for rp in p.xpath('./w:r/w:rPr',namespaces=NS): child(rp,'w','i')
                self.blocks.append(p)
            else: self.blocks.append(self.para(chunk))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--expected-sha',required=True)
    ap.add_argument('--math-deps',type=Path,required=True)
    args=ap.parse_args()
    original=WORK.read_bytes()
    assert sha(original)==args.expected_sha,'Working manuscript changed; inspect again.'
    with zipfile.ZipFile(WORK) as z:
        infos=z.infolist(); before={n:z.read(n) for n in z.namelist()}
    package=dict(before)
    edit=Chapter5(package,args.math_deps)
    edit.consume_approved(SOURCE.read_text('utf-8'))
    prefix=edit.original[:edit.start]; tail=edit.original[edit.end:]
    for p in edit.original[edit.start:edit.end]: edit.body.remove(p)
    for i,p in enumerate(edit.blocks): edit.body.insert(edit.start+i,p)
    assert [canonical(p) for p in list(edit.body)[:edit.start]]==[canonical(p) for p in prefix]
    assert [canonical(p) for p in list(edit.body)[edit.start+len(edit.blocks):]]==[canonical(p) for p in tail]
    assert edit.number==31
    for record,p in zip(edit.source_records,[p for p in edit.blocks if p.tag!=q('w','tbl')]):
        actual=text(p)
        if record['kind']=='equation': actual=actual.removesuffix('('+str(record['number'])+')')
        assert norm(record['source'])==norm(actual),(record['source'],actual)
    tbl=next(p for p in edit.blocks if p.tag==q('w','tbl'))
    actual_rows=[[text(c) for c in r.findall('w:tc',NS)] for r in tbl.findall('w:tr',NS)]
    assert actual_rows==edit.rows
    assert not any(p.xpath('.//w:drawing|.//w:pict|.//w:del|.//w:ins|.//w:vanish',namespaces=NS) for p in edit.blocks)
    package['word/document.xml']=etree.tostring(edit.root,xml_declaration=True,encoding='UTF-8',standalone=True)
    core=etree.fromstring(package['docProps/core.xml'])
    desc=core.find('{http://purl.org/dc/elements/1.1/}description')
    if desc is not None: desc.text='部分更新工作稿：第1至5章已替换；后续讨论、结束语及前后文仍待衔接；非最终可投稿版本。公式为可编辑 OMML，非 MathType OLE。尚未实际排版验收。'
    package['docProps/core.xml']=etree.tostring(core,xml_declaration=True,encoding='UTF-8',standalone=True)
    temp=WORK.with_suffix('.chapter5.tmp.docx')
    with zipfile.ZipFile(temp,'w') as z:
        for info in infos: z.writestr(info,package[info.filename])
    with zipfile.ZipFile(temp) as z:
        assert z.testzip() is None
        assert z.namelist()==list(before)
        for name in before:
            if name not in ('word/document.xml','docProps/core.xml'): assert z.read(name)==before[name]
    assert sha(WORK.read_bytes())==args.expected_sha
    temp.replace(WORK)
    QA.mkdir(parents=True,exist_ok=True)
    result={'base_working_sha256':args.expected_sha,'working_sha256':sha(WORK.read_bytes()),
            'approved_source_sha256':sha(SOURCE.read_bytes()),'prefix_blocks_preserved':len(prefix),
            'reference_tail_blocks_preserved':len(tail),'old_chapter5_blocks_removed':edit.end-edit.start,
            'new_chapter5_blocks':len(edit.blocks),'equation_numbers':[30,31],
            'math_format':'editable OMML, not MathType OLE','chapter5_omml_count':len(edit.math_records),
            'table4':actual_rows,'figure4':'author-supplied italic reservation only; no image',
            'unchanged_package_parts':[n for n in before if n not in ('word/document.xml','docProps/core.xml')],
            'verbatim_content_audit':'all author paragraphs, displays and table cells passed',
            'visual_qa':'not performed; no WPS or Word opened; no preview PDF generated',
            'remaining_issue':'原第5章结束语已按要求替换；当前第5章后直接接参考文献，第6章讨论和第7章结束语尚待提供。',
            'source_records':edit.source_records}
    (QA/'replacement-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    (QA/'formula-conversion.json').write_text(json.dumps(edit.math_records,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_records','unchanged_package_parts')},ensure_ascii=False))


if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
