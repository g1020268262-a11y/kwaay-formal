"""Finish author-approved chapter 6 only in the inspected Word working file.

No previous chapters are rebuilt. Every outside-range body block and every
package part other than document/core metadata is preserved and checked.
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
SOURCE=OUT/'source/chapter6-approved.md'
QA=OUT/'qa/working-chapter6'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M='http://schemas.openxmlformats.org/officeDocument/2006/math'
NS={'w':W,'m':M}
def tx(p): return ''.join(p.xpath('.//w:t/text()|.//m:t/text()',namespaces=NS))
def canonical(p): return E.tostring(p,method='c14n')
def sha(s): return hashlib.sha256(s).hexdigest()
def paragraph(template,value):
    p=copy.deepcopy(template)
    rp=template.find('w:r/w:rPr',NS)
    for c in list(p):
        if c.tag!='{'+W+'}pPr': p.remove(c)
    r=E.SubElement(p,'{'+W+'}r')
    if rp is not None: r.append(copy.deepcopy(rp))
    t=E.SubElement(r,'{'+W+'}t')
    t.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); t.text=value
    return p

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--expected-sha',required=True); args=ap.parse_args()
    data=WORK.read_bytes(); assert sha(data)==args.expected_sha,'Working copy changed; inspect again.'
    with zipfile.ZipFile(WORK) as z:
        infos=z.infolist(); original={n:z.read(n) for n in z.namelist()}
    parts=dict(original); root=E.fromstring(parts['word/document.xml']); body=root.find('w:body',NS)
    blocks=list(body)
    headings=[(i,tx(p)) for i,p in enumerate(blocks) if p.xpath('./w:pPr/w:pStyle[@w:val="65"]',namespaces=NS)]
    fifth=next(i for i,title in headings if title=='K-Waay 批内去重与组合加固')
    ref=next(i for i,p in enumerate(blocks) if tx(p)=='参考文献' and p.xpath('./w:pPr/w:pStyle[@w:val="82"]',namespaces=NS))
    candidates=[i for i,title in headings if fifth<i<ref]
    start=min(candidates,default=ref)
    # Delete any existing conclusion/discussion range only; never chapter 5.
    prefix=blocks[:start]; tail=blocks[ref:]; removed=blocks[start:ref]
    assert all(title in ('讨论与适用边界','结束语') for i,title in headings if start<=i<ref)
    approved=re.split(r'\n\s*\n',SOURCE.read_text('utf-8').strip())
    assert approved[0]=='# 6 结束语' and len(approved)==3
    h1=blocks[fifth]; prose=blocks[fifth+2]
    assert prose.xpath('./w:pPr/w:pStyle[@w:val="71"]',namespaces=NS)
    added=[paragraph(h1,'结束语')]+[paragraph(prose,s) for s in approved[1:]]
    for p in removed: body.remove(p)
    for i,p in enumerate(added): body.insert(start+i,p)
    after=list(body)
    assert [canonical(p) for p in after[:start]]==[canonical(p) for p in prefix]
    assert [canonical(p) for p in after[start+3:]]==[canonical(p) for p in tail]
    titles=[tx(p) for p in after if p.xpath('./w:pPr/w:pStyle[@w:val="65"]',namespaces=NS)]
    assert len(titles)==7 and titles[-1]=='结束语' and titles.count('结束语')==1
    assert [tx(p) for p in added[1:]]==approved[1:]
    old_refs=[{'block':i,'text':tx(p)} for i,p in enumerate(prefix) if re.search(r'第[67](?:章|\.\d)',tx(p))]
    assert not old_refs,'Old chapter references require inspection.'
    parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    core=E.fromstring(parts['docProps/core.xml'])
    desc=core.find('{http://purl.org/dc/elements/1.1/}description')
    if desc is not None: desc.text='部分更新工作稿：第1至6章已按作者确认稿替换；正文结构为0至6章，不单列讨论章节。前文与整体排版仍待审查，非最终可投稿版本。'
    parts['docProps/core.xml']=E.tostring(core,xml_declaration=True,encoding='UTF-8',standalone=True)
    temporary=WORK.with_suffix('.chapter6.tmp.docx')
    with zipfile.ZipFile(temporary,'w') as z:
        for info in infos: z.writestr(info,parts[info.filename])
    with zipfile.ZipFile(temporary) as z:
        assert z.testzip() is None
        assert z.namelist()==list(original)
        for name in original:
            if name not in ('word/document.xml','docProps/core.xml'): assert z.read(name)==original[name]
    assert sha(WORK.read_bytes())==args.expected_sha
    temporary.replace(WORK)
    QA.mkdir(parents=True,exist_ok=True)
    result={'base_working_sha256':args.expected_sha,'working_sha256':sha(WORK.read_bytes()),
            'source_sha256':sha(SOURCE.read_bytes()),'old_discussion_or_conclusion_blocks_removed':len(removed),
            'before_structure':'chapters0-5 followed immediately by references' if not removed else 'existing closing chapters replaced',
            'chapter6_blocks_added':3,'chapters0_5_blocks_preserved':len(prefix),'reference_tail_blocks_preserved':len(tail),
            'unchanged_package_parts':[n for n in original if n not in ('word/document.xml','docProps/core.xml')],
            'final_h1_titles':titles,'conclusion_paragraphs_exact':True,'old_chapter6_7_cross_references':old_refs,
            'new_formulas_tables_images_references':0,'new_blank_paragraphs_pagebreaks':0,
            'visible_prior_draft_notice':'preserved unchanged as part of protected prefix',
            'visual_qa':'pending actual WPS/Word opening'}
    (QA/'replacement-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8'); main()
