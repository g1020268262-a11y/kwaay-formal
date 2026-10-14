"""Local, hash-guarded Chapter 3 replacement; retains all other academic text.

Moves existing figures 2/3 without re-encoding; adds the approved monochrome
figure 4. Uses the existing tested editable-OMML conversion and journal styles.
"""
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

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
WORK = OUT / 'K-Waay-AROCMAG-submission-working.docx'
SOURCE = HERE / 'chapter3-combined-author-approved.md'
IMAGE = OUT / 'figures/fig4-combined-flow-monochrome-v1.png'
QA = OUT / 'qa/chapter3-combined-replacement'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
DRAW = {'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
        'wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'pic':'http://schemas.openxmlformats.org/drawingml/2006/picture'}
TOKEN = re.compile(r"\b(?:confirm_key|prekey|sid|tag|ct|pk|[mMkK])_[ABlksij]'?|\bidx[₁₂]|\b(?:sid|tag|bid|rst|[ABMmijk])(?![\w-])")

def latex(s):
    s = s.replace('≠', r'\ne ').replace('，', ',').replace(' 且 ', r'\land ')
    s = s.replace('idx₁', r'\mathit{idx}_{1}').replace('idx₂', r'\mathit{idx}_{2}')
    s = re.sub(r'\b(confirm_key|HMAC|KDF|SID|DistinctPartyPerBatch)\b',
               lambda m: r'\mathsf{' + m[0].replace('_', r'\_') + '}', s)
    s = re.sub(r'\b(prekey|sid|tag|ct|pk|bid|rst)\b', lambda m:r'\mathit{'+m[0]+'}', s)
    s = re.sub(r'\b(prekey|sid|tag|ct|pk)_([ABlksij])',
               lambda m:r'\mathit{'+m[1]+'}_{'+m[2]+'}', s)
    return s

class Edit(Migration):
    def __init__(self, package, deps):
        sys.path.insert(0, str(deps))
        from latex2mathml.converter import convert
        from mathml2omml import convert as omml
        self.to_mathml, self.to_omml = convert, omml
        self.root = etree.fromstring(package['word/document.xml'])
        self.body = self.root.find('w:body',NS)
        self.original = list(self.body)
        self.start = self.find_heading('K-Waay 消息篡改攻击与 HMAC 确认加固')
        self.end = self.find_heading('K-Waay 批内重放攻击与安全影响分析')
        old = self.original[self.start:self.end]
        self.h1 = old[0]
        self.h2 = next(p for p in old if p.xpath('./w:pPr/w:pStyle[@w:val="66"]',namespaces=NS))
        self.prose = next(p for p in old if p.xpath('./w:pPr/w:pStyle[@w:val="71"]',namespaces=NS))
        self.display = next(p for p in old if p.xpath('./w:pPr/w:pStyle[@w:val="74"]',namespaces=NS))
        self.table = copy.deepcopy(next(p for p in old if p.tag==q('w','tbl')))
        self.table_caption = next(p for p in old if re.match(r'表\s*2',text(p)))
        rels = etree.fromstring(package['word/_rels/document.xml.rels'])
        self.rels = rels
        targets = {r.get('Id'):r.get('Target') for r in rels}
        self.figures = {}
        self.figure_indices = {}
        for i,p in enumerate(self.original):
            for rid in p.xpath('.//a:blip/@r:embed', namespaces={**DRAW,'r':R}):
                for n in (2,3):
                    if targets.get(rid,'').endswith(f'kwaay-confirmed-figure{n}.png'):
                        assert n not in self.figures
                        self.figures[n] = (copy.deepcopy(p),copy.deepcopy(self.original[i+1]))
                        self.figure_indices[n] = (i,i+1)
        assert set(self.figures)=={2,3}
        assert self.start<=self.figure_indices[2][0]<self.end
        assert self.figure_indices[3][0]>=self.end
        self.blocks=[]; self.math_records=[]; self.source_records=[]; self.number=7
        self.wording_changes=[]

    def para(self, src, template=None):
        template = template if template is not None else self.prose
        p = self.blank(template)
        # Author Markdown emphasis is not copied as heavy manuscript emphasis.
        src = src.replace('**','')
        for n,segment in enumerate(re.split(r'`([^`]+)`',src)):
            if n%2:
                p.append(self.math(latex(segment)))
                continue
            pos=0
            for match in TOKEN.finditer(segment):
                self.run(p,segment[pos:match.start()],template=template)
                p.append(self.math(latex(match[0])))
                pos=match.end()
            self.run(p,segment[pos:],template=template)
        self.source_records.append({'kind':'paragraph','source':src,'actual':text(p)})
        return p

    def formula(self, src):
        p=self.blank(self.display)
        parts=[src]
        if src.startswith("sid_B' = SID"):
            at=src.index('prekey_A'); parts=[src[:at],src[at:]]
        elif '，' in src:
            parts=src.split('，')
        for i,part in enumerate(parts):
            if i: child(child(p,'w','r'),'w','br')
            child(child(p,'w','r'),'w','tab')
            p.append(self.math(latex(part)))
        self.number+=1
        child(child(p,'w','r'),'w','tab')
        self.run(p,'('+str(self.number)+')',template=self.display)
        self.source_records.append({'kind':'equation','source':src,'number':self.number,'actual':text(p)})
        return p

    def caption(self,n,title):
        p=self.blank(self.figures[3][1])
        self.run(p,'图',template=self.figures[3][1])
        for kind,value in [('begin',None),('instruction',f' SEQ Figure \\r {n} \\* ARABIC '),('separate',None),('result',str(n)),('end',None)]:
            run=child(p,'w','r')
            if kind in ('begin','separate','end'):
                x=child(run,'w','fldChar'); x.set(q('w','fldCharType'),kind)
            elif kind=='instruction':
                x=child(run,'w','instrText');x.set('{http://www.w3.org/XML/1998/namespace}space','preserve');x.text=value
            else: child(run,'w','t').text=value
        self.run(p,' '+title,template=self.figures[3][1])
        return p

    def add_figure(self,n):
        titles={2:'K-Waay密文重组攻击流程',3:'K-Waay批内重复接受与条件化安全影响示意',4:'K-Waay消息级组合加固后的发送与批量接收流程'}
        references={2:'上述密文重组攻击过程如图2所示。',3:'上述批内重复接受过程及其条件化安全影响如图3所示。',4:'消息级组合加固后的发送与批量接收流程如图4所示。'}
        self.blocks.append(self.para(references[n]))
        if n in (2,3): image=copy.deepcopy(self.figures[n][0])
        else:
            image=copy.deepcopy(self.figures[3][0])
            rid='rIdKwaayCombinedFigure4'
            assert not any(r.get('Id')==rid for r in self.rels)
            rel=etree.SubElement(self.rels,'{'+REL+'}Relationship')
            rel.set('Id',rid);rel.set('Type',R+'/image');rel.set('Target','media/kwaay-combined-figure4-monochrome.png')
            for blip in image.xpath('.//a:blip',namespaces=DRAW):blip.set('{'+R+'}embed',rid)
            maxid=max(int(x) for x in self.root.xpath('//wp:docPr/@id',namespaces=DRAW))
            for dp in image.xpath('.//wp:docPr',namespaces=DRAW):
                dp.set('id',str(maxid+1));dp.set('name','K-Waay monochrome combined Figure 4');dp.set('descr',titles[n])
            with Image.open(IMAGE) as im: iw,ih=im.size
            width=3126105; height=round(width*ih/iw)
            for ex in image.xpath('.//wp:extent|.//a:xfrm/a:ext',namespaces=DRAW):
                ex.set('cx',str(width));ex.set('cy',str(height))
        self.blocks.extend([image,self.caption(n,titles[n])])

    def build(self,src):
        for chunk in re.split(r'\n\s*\n',src.strip()):
            if chunk.startswith('图4建议'):
                self.wording_changes.append({'original':chunk,'replacement':None,'reason':'制图说明不属于论文正文'})
                continue
            if '【图' in chunk:
                self.add_figure(int(re.search(r'【图([234])',chunk)[1]));continue
            if chunk.startswith('#'):
                m=re.fullmatch(r'(#{1,2})\s+[\d.]+\s+(.+)',chunk);assert m
                self.blocks.append(self.para(m[2],self.h1 if len(m[1])==1 else self.h2))
            elif chunk.startswith('|'):
                rows=[[v.strip() for v in line.strip('|').split('|')] for line in chunk.splitlines() if not re.match(r'\|\s*-',line)]
                existing=[[text(c) for c in row.findall('w:tc',NS)] for row in self.table.findall('w:tr',NS)]
                assert rows==existing,(rows,existing)
                widths=[2314,850,1428]
                for c,w in zip(self.table.find('w:tblGrid',NS),widths):c.set(q('w','w'),str(w))
                for row in self.table.findall('w:tr',NS):
                    for cell,w in zip(row.findall('w:tc',NS),widths):cell.find('w:tcPr/w:tcW',NS).set(q('w','w'),str(w))
                self.blocks.append(self.table)
            elif chunk.startswith('**表2'):
                self.blocks.append(self.para(chunk,self.table_caption))
            elif re.fullmatch(r'`[^`]+`',chunk): self.blocks.append(self.formula(chunk[1:-1]))
            else:
                original=chunk
                if chunk.startswith('HMAC 能够确认'):
                    chunk='在第3.3节验证的无密钥泄露符号配置下，'+chunk
                if chunk.startswith('进一步分析表明'):
                    chunk += '该消费模型并非上述 HMAC-only 模型的直接扩展，因此不将二者描述为同一条已验证的联合攻击轨迹。'
                if chunk!=original:self.wording_changes.append({'original':original,'replacement':chunk,'reason':'保留既有科学结论的模型及无泄露边界'})
                self.blocks.append(self.para(chunk))

def norm(s):
    s=s.replace('′',"'").replace('’',"'").replace('，',',').replace('且','∧').replace('₁','1').replace('₂','2')
    return re.sub(r'[\s_`*,]','',s)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--expected-sha',required=True);ap.add_argument('--math-deps',type=Path,required=True);a=ap.parse_args()
    before=WORK.read_bytes();assert sha(before)==a.expected_sha
    with zipfile.ZipFile(WORK) as z: infos=z.infolist(); package={n:z.read(n) for n in z.namelist()}
    original_package=dict(package)
    edit=Edit(package,a.math_deps);edit.build(SOURCE.read_text('utf-8'))
    # Local author-text audit, with only explicitly recorded wording corrections.
    for rec in edit.source_records:
        actual=rec['actual']
        if rec['kind']=='equation':actual=actual.removesuffix('('+str(rec['number'])+')')
        assert norm(rec['source'])==norm(actual),(ascii(rec['source']),ascii(actual))
    prefix=edit.original[:edit.start]
    removed=set(edit.figure_indices[3])
    tail=[p for i,p in enumerate(edit.original) if i>=edit.end and i not in removed]
    for p in list(edit.body):edit.body.remove(p)
    for p in prefix+edit.blocks+tail:edit.body.append(p)
    assert [canonical(p) for p in list(edit.body)[:edit.start]]==[canonical(p) for p in prefix]
    assert [canonical(p) for p in list(edit.body)[edit.start+len(edit.blocks):]]==[canonical(p) for p in tail]
    assert edit.number==20
    assert len([p for p in edit.blocks if p.xpath('./w:pPr/w:pStyle[@w:val="66"]',namespaces=NS)])==6
    assert len(edit.root.xpath('//w:drawing',namespaces=NS))==4
    ids=edit.root.xpath('//wp:docPr/@id',namespaces=DRAW);assert len(ids)==len(set(ids))
    assert not edit.root.xpath('//w:del|//w:ins',namespaces=NS)
    package['word/document.xml']=etree.tostring(edit.root,xml_declaration=True,encoding='UTF-8',standalone=True)
    package['word/_rels/document.xml.rels']=etree.tostring(edit.rels,xml_declaration=True,encoding='UTF-8',standalone=True)
    media='word/media/kwaay-combined-figure4-monochrome.png';assert media not in package;package[media]=IMAGE.read_bytes()
    ct=etree.fromstring(package['[Content_Types].xml']);assert any(x.get('Extension')=='png' for x in ct)
    unchanged=[n for n in original_package if n not in ('word/document.xml','word/_rels/document.xml.rels')]
    for n in unchanged:assert package[n]==original_package[n]
    tmp=WORK.with_suffix('.combined-ch3.tmp.docx')
    with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for info in infos:z.writestr(info,package[info.filename])
        z.writestr(media,package[media])
    with zipfile.ZipFile(tmp) as z:
        assert z.testzip() is None
        for n in z.namelist():
            if n.endswith('.xml') or n.endswith('.rels'):etree.fromstring(z.read(n))
    assert sha(WORK.read_bytes())==a.expected_sha;tmp.replace(WORK)
    QA.mkdir(parents=True,exist_ok=True)
    manifest={'before_sha256':a.expected_sha,'after_sha256':sha(WORK.read_bytes()),'source_sha256':sha(SOURCE.read_bytes()),
      'figure4_sha256':sha(IMAGE.read_bytes()),'chapter3_subsections':6,'chapter3_display_equation_numbers':list(range(8,21)),
      'math':'Editable native OMML; not MathType OLE','math_count_new_chapter3':len(edit.math_records),
      'chapter0_2_prefix_preserved':True,'chapter4_onwards_academic_text_preserved':True,'tail_only_change':'Figure3 drawing and caption moved into new chapter3',
      'unchanged_package_parts':unchanged,'wording_changes':edit.wording_changes,'figure_positions':{'2':'3.2','3':'3.4','4':'3.5'},
      'table2':'Original native editable three-line table retained; author rows checked; column widths adjusted',
      'visual_review':'Not performed: user deferred WPS/final pagination until image insertion completed',
      'pending':['Current chapter4/5 repeat new chapter3 content; user will replace later','Section3.6 next-chapter transition awaits replacement of chapter4',
                 'Existing chapter5 Figure4 placeholder preserved per scope','New equations8–20; existing later equations22–31 retained; gap21 awaits chapter4/5 replacements',
                 'Current captions have moved; duplicate old chapter4 prose reference to Figure3 remains intentionally unchanged','Final figure widths and pagination require journal-layout review'],
      'source_records':edit.source_records}
    (QA/'replacement-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
    (QA/'formula-conversion.json').write_text(json.dumps(edit.math_records,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k not in ('source_records','unchanged_package_parts','wording_changes')},ensure_ascii=False,indent=2))

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');main()
