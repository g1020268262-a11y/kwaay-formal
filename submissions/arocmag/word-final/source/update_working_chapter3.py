"""Replace only the approved chapter 3 in the inspected Word working package.

Run with bundled Python, --expected-sha and --math-deps. Never rebuild from
Stage 6. All body blocks before chapter 3 and from chapter 4 onward, and every
other ZIP part, must be byte/canonical-identical. The Markdown is author text.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from lxml import etree
from update_working_chapters_1_2 import Migration, NS, W, M, q, child, text, canonical, sha

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
WORK = OUT / 'K-Waay-AROCMAG-submission-working.docx'
SOURCE = HERE / 'chapter3-approved.md'
QA = OUT / 'qa/working-chapter3'
TOKEN = re.compile(r"(?:RecvDone|SendDone)\([^)]*\)|confirm_key|(?:prekey|sid|tag|ct|pk|[mMkK])_[ABlks]'?|(?<![A-Za-z])(?:tag|sid)(?![A-Za-z_])|(?<![A-Za-z])(?:A|B|m)(?![A-Za-z_-])")


def latex(s):
    s = s.replace('≠', r'\ne ').replace('、', ',')
    s = re.sub(r'\b(confirm_key|RecvDone|SendDone|HMAC|KDF|SID)\b',
               lambda m: r'\mathsf{' + m[0].replace('_', r'\_') + '}', s)
    s = re.sub(r'\b(prekey|sid|tag|ct|pk)\b', lambda m: r'\mathit{' + m[0] + '}', s)
    s = re.sub(r'\b(prekey|sid|tag|ct|pk)_([ABlks])',
               lambda m: r'\mathit{' + m[1] + '}_{' + m[2] + '}', s)
    return s


class Chapter3(Migration):
    def __init__(self, package, deps):
        sys.path.insert(0, str(deps))
        from latex2mathml.converter import convert
        from mathml2omml import convert as omml
        self.to_mathml, self.to_omml = convert, omml
        self.package = package
        self.root = etree.fromstring(package['word/document.xml'])
        self.body = self.root.find('w:body', NS)
        self.original = list(self.body)
        self.start = self.find_heading('形式化验证与结果分析')
        self.end = self.find_heading('结果讨论与适用范围')
        self.h1 = self.original[self.start]
        self.h2 = self.original[self.start+1]
        self.h3 = copy.deepcopy(self.h2)
        self.h3.find('w:pPr/w:pStyle', NS).set(q('w', 'val'), '68')
        # Explicit paragraph numPr, if inherited, must use the existing level 2.
        for level in self.h3.xpath('./w:pPr/w:numPr/w:ilvl', namespaces=NS):
            level.set(q('w', 'val'), '2')
        self.prose = self.original[self.start+2]
        self.display = next(p for p in self.original[:self.start]
                            if p.xpath('./w:pPr/w:pStyle[@w:val="74"]', namespaces=NS))
        self.caption = next(p for p in self.original[:self.start] if text(p).startswith('表 1'))
        self.table_base = next(p for p in self.original[:self.start] if p.tag == q('w', 'tbl'))
        self.blocks, self.math_records, self.source_records = [], [], []
        self.number = 7
        self.rows = []

    def put_run(self, p, s, template, bold=False):
        before = len(p)
        self.run(p, s, template=template)
        if bold and len(p)>before:
            rp = p[-1].find('w:rPr', NS)
            b = rp.find('w:b', NS)
            if b is None: child(rp, 'w', 'b')
            else: b.set(q('w','val'),'1')

    def rich(self, p, src, template, bold=False):
        pos = 0
        for match in re.finditer(r'\*\*(.+?)\*\*|`([^`]+)`', src):
            self.plain_math(p, src[pos:match.start()], template, bold)
            if match[1] is not None: self.rich(p, match[1], template, True)
            elif match[2] in ('false','true'):
                self.put_run(p, match[2], template, bold)
            else:
                p.append(self.math(latex(match[2])))
            pos = match.end()
        self.plain_math(p, src[pos:], template, bold)

    def plain_math(self, p, src, template, bold):
        pos = 0
        for match in TOKEN.finditer(src):
            self.put_run(p, src[pos:match.start()], template, bold)
            p.append(self.math(latex(match[0])))
            pos = match.end()
        self.put_run(p, src[pos:], template, bold)

    def para(self, src, template=None):
        template = template if template is not None else self.prose
        p = self.blank(template)
        self.rich(p, src, template)
        self.source_records.append({'kind':'paragraph','source':src})
        return p

    def formula(self, src):
        p = self.blank(self.display)
        parts = [src]
        if src.startswith("sid_B' = SID"):
            point = src.index('prekey_A')
            parts = [src[:point], src[point:]]
        for i, part in enumerate(parts):
            if i: child(child(p,'w','r'),'w','br')
            p.append(self.math(latex(part), display=True))
        # Shared-secret enumeration is not an equation and gets no number.
        number = None
        if '、' not in src:
            self.number += 1
            number = self.number
            r = child(p,'w','r')
            rp = self.display.find('w:r/w:rPr',NS)
            if rp is not None: r.append(copy.deepcopy(rp))
            child(r,'w','tab')
            child(r,'w','t').text = '(' + str(number) + ')'
        self.source_records.append({'kind':'equation','source':src,'number':number,'layout_lines':parts})
        return p

    def make_table(self, rows):
        assert len(rows)==6 and all(len(r)==3 for r in rows)
        tbl = copy.deepcopy(self.table_base)
        original = tbl.findall('w:tr',NS)
        for row in original: tbl.remove(row)
        widths = [2494, 850, 1248]  # total 8.1 cm, fits one template column
        grid = tbl.find('w:tblGrid',NS)
        for c in list(grid): grid.remove(c)
        for width in widths:
            c = child(grid,'w','gridCol'); c.set(q('w','w'),str(width))
        tw = tbl.find('w:tblPr/w:tblW',NS)
        tw.set(q('w','w'),str(sum(widths))); tw.set(q('w','type'),'dxa')
        for i, values in enumerate(rows):
            row = copy.deepcopy(original[0] if i==0 else original[-1] if i==len(rows)-1 else original[1])
            cells = row.findall('w:tc',NS)
            for cell in cells[3:]: row.remove(cell)
            for cell, width, value in zip(cells[:3], widths, values):
                cell.find('w:tcPr/w:tcW',NS).set(q('w','w'),str(width))
                prototype = cell.find('w:p',NS)
                p = self.blank(prototype)
                self.rich(p,value,prototype)
                for c in list(cell):
                    if c.tag!=q('w','tcPr'): cell.remove(c)
                cell.append(p)
            tbl.append(row)
        self.rows = rows
        return tbl

    def consume_approved(self, src):
        for chunk in re.split(r'\n\s*\n',src.strip()):
            if chunk.startswith('#'):
                m = re.fullmatch(r'(#{1,3})\s+[0-9.]+\s+(.+)',chunk)
                if not m: raise ValueError(chunk)
                self.blocks.append(self.para(m[2], [self.h1,self.h2,self.h3][len(m[1])-1]))
            elif chunk.startswith('|'):
                rows = [[v.strip() for v in line.strip('|').split('|')]
                        for line in chunk.splitlines() if not re.match(r'\|\s*-',line)]
                self.blocks.append(self.make_table(rows))
            elif chunk.startswith('**表2 '):
                self.blocks.append(self.para(chunk[2:-2],self.caption))
            elif re.fullmatch(r'`[^`]+`',chunk):
                self.blocks.append(self.formula(chunk[1:-1]))
            else:
                self.blocks.append(self.para(chunk))
        # Reserve Figure 2 as a zero-width bookmark, not an image or caption.
        idx = next(i for i,p in enumerate(self.blocks) if text(p)=='基于 HMAC 的接收确认加固')
        anchor = self.blocks[idx-1]
        ids = [int(x) for x in self.root.xpath('//w:bookmarkStart/@w:id',namespaces=NS)]
        ident = str(max(ids,default=0)+1)
        mark = child(anchor,'w','bookmarkStart'); mark.set(q('w','id'),ident)
        mark.set(q('w','name'),'Fig2_Ciphertext_HMAC_Reserved')
        end = child(anchor,'w','bookmarkEnd'); end.set(q('w','id'),ident)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--expected-sha',required=True)
    ap.add_argument('--math-deps',type=Path,required=True)
    args = ap.parse_args()
    data = WORK.read_bytes()
    assert sha(data)==args.expected_sha, 'Working manuscript changed; inspect again.'
    with zipfile.ZipFile(WORK) as z:
        infos=z.infolist(); package={n:z.read(n) for n in z.namelist()}
    edit = Chapter3(package,args.math_deps)
    src = SOURCE.read_text('utf-8')
    edit.consume_approved(src)
    prefix=edit.original[:edit.start]; tail=edit.original[edit.end:]
    for p in edit.original[edit.start:edit.end]: edit.body.remove(p)
    for i,p in enumerate(edit.blocks): edit.body.insert(edit.start+i,p)
    assert [canonical(p) for p in list(edit.body)[:edit.start]]==[canonical(p) for p in prefix]
    assert [canonical(p) for p in list(edit.body)[edit.start+len(edit.blocks):]]==[canonical(p) for p in tail]
    assert edit.number==21
    chapter_text=''.join(text(p) for p in edit.blocks)
    assert '形式化验证与结果分析' not in chapter_text
    assert not any(p.xpath('.//w:drawing|.//w:pict|.//w:del|.//w:ins|.//w:vanish',namespaces=NS) for p in edit.blocks)
    # Author-text audit: strip only formatting, source subscripts and whitespace.
    # Math glyph primes and enumeration comma are equivalent representations.
    def norm(s):
        s=s.replace('′',"'").replace('’',"'").replace('、',',')
        return re.sub(r'[\s_`*]','',s)
    for record,p in zip(edit.source_records,[p for p in edit.blocks if p.tag!=q('w','tbl')]):
        source=record['source']
        actual=text(p)
        if record['kind']=='equation' and record['number'] is not None:
            actual=actual.removesuffix('('+str(record['number'])+')')
        assert norm(source)==norm(actual), (source,actual)
    replacement = etree.tostring(edit.root,xml_declaration=True,encoding='UTF-8',standalone=True)
    package['word/document.xml']=replacement
    # Metadata declares the replacement; visible pre-existing draft notice stays intact.
    core=etree.fromstring(package['docProps/core.xml'])
    dc='http://purl.org/dc/elements/1.1/'
    desc=core.find('{'+dc+'}description')
    if desc is not None:
        desc.text='部分更新工作稿：第1至3章已替换；第4章及后续内容尚待衔接；非最终可投稿版本。公式为可编辑 OMML，非 MathType OLE。'
    package['docProps/core.xml']=etree.tostring(core,xml_declaration=True,encoding='UTF-8',standalone=True)
    temp=WORK.with_suffix('.chapter3.tmp.docx')
    with zipfile.ZipFile(temp,'w') as z:
        for info in infos: z.writestr(info,package[info.filename])
    with zipfile.ZipFile(temp) as z:
        assert z.testzip() is None
        unchanged=[n for n in package if n not in ('word/document.xml','docProps/core.xml')]
        for name in unchanged: assert z.read(name)==package[name]
    assert sha(WORK.read_bytes())==args.expected_sha
    temp.replace(WORK)
    QA.mkdir(parents=True,exist_ok=True)
    manifest={'base_working_sha256':args.expected_sha,'working_sha256':sha(WORK.read_bytes()),
              'approved_source_sha256':sha(SOURCE.read_bytes()),'source':'source/chapter3-approved.md',
              'prefix_blocks_preserved':len(prefix),'tail_blocks_preserved':len(tail),
              'unchanged_package_parts':unchanged,'chapter3_blocks':len(edit.blocks),
              'heading_styles':{'level1':'65','level2':'66','level3':'68'},
              'equation_numbers':list(range(8,22)), 'shared_secret_enumeration_numbered':False,
              'math_format':'editable OMML, not MathType OLE','chapter3_omml_count':len(edit.math_records),
              'table2':[[re.sub(r'\*\*','',v) for v in row] for row in edit.rows],
              'figure2_reserved_bookmark':'Fig2_Ciphertext_HMAC_Reserved',
              'figure2_planned_caption':'图2 K-Waay 密文重组攻击及 HMAC 确认加固对照',
              'source_text_equivalence_assertions':'all author paragraphs and displays passed',
              'original_blocks_removed':edit.end-edit.start,'source_records':edit.source_records}
    (QA/'replacement-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
    (QA/'formula-conversion.json').write_text(json.dumps(edit.math_records,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k not in ('source_records','unchanged_package_parts')},ensure_ascii=False))


if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
