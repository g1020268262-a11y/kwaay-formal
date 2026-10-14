"""Restore official Word typography without changing approved scientific text.

Uses the existing submission working package. Published-paper observations guide
readability, not manuscript scope. All OMML subtrees and table cell text remain
unchanged. Only typography/layout and caption whitespace may change.
"""
import argparse
import copy
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from lxml import etree as E

OUT=Path(__file__).resolve().parent.parent
WORK=OUT/'K-Waay-AROCMAG-submission-working.docx'
TEMPLATE=OUT/'source/official-template-converted.docx'
QA=OUT/'qa/journal-typography-repair'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M='http://schemas.openxmlformats.org/officeDocument/2006/math'
NS={'w':W,'m':M}
def q(n): return '{'+W+'}'+n
def tx(p): return ''.join(p.xpath('.//w:t/text()|.//m:t/text()',namespaces=NS))
def canon(p): return E.tostring(p,method='c14n')
def sha(data): return hashlib.sha256(data).hexdigest()
def set_property(parent,name,value):
    el=parent.find(q(name))
    if el is None: el=E.SubElement(parent,q(name))
    el.set(q('val'),str(value))
    return el
def rpr(run):
    pr=run.find(q('rPr'))
    if pr is None: pr=E.Element(q('rPr')); run.insert(0,pr)
    return pr
def fonts(pr,latin,asian,size,bold=False):
    font=pr.find(q('rFonts'))
    if font is None: font=E.Element(q('rFonts')); pr.insert(0,font)
    for key in list(font.attrib):
        if key.rsplit('}',1)[-1].endswith('Theme'): del font.attrib[key]
    for key,value in [('ascii',latin),('hAnsi',latin),('eastAsia',asian),('cs','Times New Roman')]: font.set(q(key),value)
    for name,value in [('sz',size),('szCs',size),('b',int(bold)),('bCs',int(bold)),('color','000000')]: set_property(pr,name,value)
def format_run_copy(original,value,superscript=False):
    r=copy.deepcopy(original)
    for c in list(r):
        if c.tag!=q('rPr'): r.remove(c)
    if superscript: set_property(rpr(r),'vertAlign','superscript')
    t=E.SubElement(r,q('t')); t.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); t.text=value
    return r

def refine_table2(expected_sha):
    """Resolve a visually confirmed orphan header without changing total width."""
    original_bytes=WORK.read_bytes()
    assert sha(original_bytes)==expected_sha,'Working copy changed; inspect again.'
    with zipfile.ZipFile(WORK) as z:
        infos=z.infolist(); parts={n:z.read(n) for n in z.namelist()}
    root=E.fromstring(parts['word/document.xml'])
    body=root.find('w:body',NS)
    table=body.findall('w:tbl',NS)[1]
    old_table_text=tx(table)
    old_math=[canon(p) for p in root.xpath('//m:oMath',namespaces=NS)]
    old_sections=[canon(p) for p in root.xpath('//w:sectPr',namespaces=NS)]
    columns=table.findall('w:tblGrid/w:gridCol',NS)
    previous=[int(c.get(q('w'))) for c in columns]
    assert previous==[2494,850,1248],previous
    revised=[2314,850,1428]  # Transfer 9 pt from property column to HMAC header.
    assert sum(previous)==sum(revised)
    for column,width in zip(columns,revised): column.set(q('w'),str(width))
    for row in table.findall('w:tr',NS):
        cells=row.findall('w:tc',NS); assert len(cells)==3
        for cell,width in zip(cells,revised):
            cell_width=cell.find('w:tcPr/w:tcW',NS)
            assert cell_width is not None
            cell_width.set(q('w'),str(width)); cell_width.set(q('type'),'dxa')
    assert old_table_text==tx(table)
    assert old_math==[canon(p) for p in root.xpath('//m:oMath',namespaces=NS)]
    assert old_sections==[canon(p) for p in root.xpath('//w:sectPr',namespaces=NS)]
    parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    temporary=WORK.with_suffix('.typography.tmp.docx')
    with zipfile.ZipFile(temporary,'w') as z:
        for info in infos: z.writestr(info,parts[info.filename])
    with zipfile.ZipFile(temporary) as z: assert z.testzip() is None
    assert sha(WORK.read_bytes())==expected_sha
    temporary.replace(WORK)
    manifest=json.loads((QA/'formatting-manifest.json').read_text('utf-8'))
    manifest['working_sha256']=sha(WORK.read_bytes())
    manifest['table2_column_widths_twips']={'before':previous,'after':revised,'total_preserved':sum(revised)}
    manifest['visual_qa']='WPS 7-page preview inspected; final table2 refinement pending re-export'
    (QA/'formatting-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({'working_sha256':manifest['working_sha256'],'table2_column_widths_twips':manifest['table2_column_widths_twips']},ensure_ascii=False))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--expected-sha',required=True)
    ap.add_argument('--refine-table2',action='store_true'); args=ap.parse_args()
    if args.refine_table2:
        refine_table2(args.expected_sha); return
    original_bytes=WORK.read_bytes(); assert sha(original_bytes)==args.expected_sha,'Working copy changed; inspect again.'
    with zipfile.ZipFile(WORK) as z: infos=z.infolist(); before={n:z.read(n) for n in z.namelist()}
    with zipfile.ZipFile(TEMPLATE) as z: official_styles=E.fromstring(z.read('word/styles.xml'))
    parts=dict(before); root=E.fromstring(parts['word/document.xml']); body=root.find('w:body',NS)
    old_text=[tx(p) for p in body]
    old_math=[canon(p) for p in root.xpath('//m:oMath',namespaces=NS)]
    old_sect=[canon(p) for p in root.xpath('//w:sectPr',namespaces=NS)]
    old_rows=[[tx(cell) for cell in row.findall('w:tc',NS)] for tbl in body.findall('w:tbl',NS) for row in tbl.findall('w:tr',NS)]
    changes=[]; superscript_count=0; plain_citations=[]; body_bold=0; captions=[]
    heading_specs={'40':('Arial','黑体',32),'42':('Times New Roman','宋体',24),
                   '65':('Arial','黑体',21),'66':('Arial','黑体',18),'68':('Times New Roman','楷体',18),
                   '77':('Times New Roman','宋体',16),'82':('Arial','黑体',21),
                   '43':('Times New Roman','楷体',18),'44':('Times New Roman','楷体',18),
                   '84':('Times New Roman','楷体',15)}
    for i,p in enumerate(body):
        style=p.find('w:pPr/w:pStyle',NS)
        sid=style.get(q('val')) if style is not None else ''
        runs=p.findall('w:r',NS)
        if sid in heading_specs:
            spec=heading_specs[sid]
            for r in runs: fonts(rpr(r),*spec)
            changes.append({'block':i,'role':sid,'format':spec,'text_prefix':tx(p)[:45]})
        elif sid=='45':
            # Both abstract languages use the official 9 pt text size.
            for r in runs:
                label=tx(r).strip() in ('摘 要：','摘  要：','关键词：','Abstract:','Key words:')
                chinese_label=label and tx(r).strip() in ('摘 要：','摘  要：','关键词：')
                fonts(rpr(r),'Arial' if chinese_label else 'Times New Roman',
                      '黑体' if chinese_label else '楷体',18,label and not chinese_label)
            changes.append({'block':i,'role':'abstract/keywords/metadata','format':'楷体/TNR 9pt; distinct labels'})
        elif sid=='71':
            for r in runs:
                if r.xpath('./w:rPr/w:b[not(@w:val="0")]',namespaces=NS): body_bold+=1
                fonts(rpr(r),'Times New Roman','宋体',18)
            # Keep all OMML/italics/approved text. Normalize only the contribution-list indent.
            if re.match(r'^[123]\. ',tx(p)):
                indent=p.find('w:pPr/w:ind',NS)
                if indent is not None:
                    for key in ('firstLine','firstLineChars','hangingChars','leftChars'):
                        if q(key) in indent.attrib: del indent.attrib[q(key)]
                    indent.set(q('left'),'360'); indent.set(q('hanging'),'360')
            ptext=tx(p)
            for r in list(p.findall('w:r',NS)):
                value=tx(r)
                matches=list(re.finditer(r'\[[0-9]+(?:[,-][0-9]+)*\]',value))
                if not matches: continue
                texts=r.findall('w:t',NS)
                assert len(texts)==1 and all(c.tag in (q('rPr'),q('t')) for c in r)
                at=list(p).index(r); pos=0; pieces=[]
                for m in matches:
                    if m.start()>pos: pieces.append(format_run_copy(r,value[pos:m.start()]))
                    global_start=ptext.find(value)+m.start()
                    narrative=bool(re.search(r'(?:文献|参考文献)$',ptext[:global_start]))
                    pieces.append(format_run_copy(r,m[0],not narrative))
                    if narrative: plain_citations.append(m[0])
                    else: superscript_count+=1
                    pos=m.end()
                if pos<len(value): pieces.append(format_run_copy(r,value[pos:]))
                p.remove(r)
                for j,piece in enumerate(pieces): p.insert(at+j,piece)
        elif sid=='74':
            # Official centered/right tabs eliminate equation-number drift caused
            # by paragraph centering. OMML subtrees themselves are untouched.
            pr=p.find('w:pPr',NS)
            # WPS had wrapped some lines in block math containers. Use the
            # same inline OMML objects with the template's paragraph tab stops.
            for wrapper in list(p.findall('m:oMathPara',NS)):
                position=list(p).index(wrapper)
                expressions=wrapper.findall('m:oMath',NS)
                assert expressions and all(c.tag in ('{'+M+'}oMath','{'+M+'}oMathParaPr') for c in wrapper)
                p.remove(wrapper)
                for j,expression in enumerate(expressions): p.insert(position+j,expression)
            set_property(pr,'jc','left')
            tabs=pr.find(q('tabs'))
            if tabs is not None: pr.remove(tabs)
            tabs=E.SubElement(pr,q('tabs'))
            for align,pos in [('center','2548'),('right','4914')]:
                stop=E.SubElement(tabs,q('tab')); stop.set(q('val'),align); stop.set(q('pos'),pos)
            def leading_tab():
                r=E.Element(q('r')); E.SubElement(r,q('tab')); return r
            content=[c for c in p if c.tag!=q('pPr')]
            assert content and content[0].tag=='{'+M+'}oMath'
            p.insert(list(p).index(content[0]),leading_tab())
            for c in content:
                if c.tag==q('r') and c.find(q('br')) is not None:
                    assert not tx(c)
                    p.insert(list(p).index(c)+1,leading_tab())
            for r in p.findall('w:r',NS): fonts(rpr(r),'Times New Roman','宋体',18)
        if sid=='77':
            value=tx(p); match=re.fullmatch(r'表\s*(\d+)\s+(.+)',value)
            if match:
                new='表 '+match[1]+'\u3000'+match[2]
                # Only whitespace changes; rebuild the caption with official font.
                for r in list(p.findall('w:r',NS)): p.remove(r)
                r=E.SubElement(p,q('r')); fonts(rpr(r),'Times New Roman','宋体',16)
                t=E.SubElement(r,q('t')); t.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); t.text=new
                captions.append({'before':value,'after':new})
    # Correct the one style definition that drifted from the retained official base.
    styles=E.fromstring(parts['word/styles.xml'])
    ref_style=next(s for s in styles if s.get(q('styleId'))=='84')
    official_ref=next(s for s in official_styles if s.get(q('styleId'))=='84')
    ref_style.replace(ref_style.find(q('rPr')),copy.deepcopy(official_ref.find(q('rPr'))))
    parts['word/styles.xml']=E.tostring(styles,xml_declaration=True,encoding='UTF-8',standalone=True)
    new_text=[tx(p) for p in body]
    assert len(old_text)==len(new_text)
    for a,b in zip(old_text,new_text): assert re.sub(r'\s','',a)==re.sub(r'\s','',b),(a,b)
    assert old_math==[canon(p) for p in root.xpath('//m:oMath',namespaces=NS)]
    assert old_sect==[canon(p) for p in root.xpath('//w:sectPr',namespaces=NS)]
    assert old_rows==[[tx(cell) for cell in row.findall('w:tc',NS)] for tbl in body.findall('w:tbl',NS) for row in tbl.findall('w:tr',NS)]
    parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    temporary=WORK.with_suffix('.typography.tmp.docx')
    with zipfile.ZipFile(temporary,'w') as z:
        for info in infos: z.writestr(info,parts[info.filename])
    with zipfile.ZipFile(temporary) as z:
        assert z.testzip() is None
        for n in before:
            if n not in ('word/document.xml','word/styles.xml'): assert z.read(n)==before[n]
    assert sha(WORK.read_bytes())==args.expected_sha; temporary.replace(WORK)
    QA.mkdir(parents=True,exist_ok=True)
    result={'base_sha256':args.expected_sha,'working_sha256':sha(WORK.read_bytes()),
            'authority':'retained official-template-converted.docx and artifact.md; published PDF observations are secondary',
            'academic_text_preserved':True,'caption_whitespace_only':captions,'omml_objects_preserved':len(old_math),
            'section_geometry_preserved':True,'table_cell_text_preserved':True,
            'body_bold_runs_normalized':body_bold,'marker_citations_superscripted':superscript_count,
            'narrative_citations_kept_baseline':plain_citations,'equation_alignment':'official center tab2548/right tab4914; all expressions and numbers preserved',
            'modified_parts':['word/document.xml','word/styles.xml'],'role_changes':changes,'visual_qa':'pending WPS verification'}
    (QA/'formatting-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='role_changes'},ensure_ascii=False))

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8'); main()
