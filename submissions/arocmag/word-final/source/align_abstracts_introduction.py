"""Apply the author's bounded alignment request to the existing Word package.

Source text is parsed from the supplied request, not regenerated. Preserve all
non-allowlisted body blocks, displayed equations, reference blocks, tables2-4,
and package parts except document/core metadata. Run with bundled Python -B.
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
QA=OUT/'qa/abstract-introduction-alignment'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M='http://schemas.openxmlformats.org/officeDocument/2006/math'
NS={'w':W,'m':M}
def tx(p): return ''.join(p.xpath('.//w:t/text()|.//m:t/text()',namespaces=NS))
def canon(p): return E.tostring(p,method='c14n')
def sha(s): return hashlib.sha256(s).hexdigest()
def blank(p):
    result=copy.deepcopy(p)
    for c in list(result):
        if c.tag!='{'+W+'}pPr': result.remove(c)
    return result
def run(p,value,rp,bold=None):
    r=E.SubElement(p,'{'+W+'}r')
    pr=copy.deepcopy(rp) if rp is not None else E.Element('{'+W+'}rPr')
    if bold is not None:
        b=pr.find('{'+W+'}b')
        if b is None: b=E.SubElement(pr,'{'+W+'}b')
        b.set('{'+W+'}val','1' if bold else '0')
    r.append(pr)
    t=E.SubElement(r,'{'+W+'}t'); t.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); t.text=value
def para(template,value,rich=False):
    p=blank(template); rp=template.find('w:r/w:rPr',NS)
    if rich:
        pos=0
        for match in re.finditer(r'\*\*(.+?)\*\*',value):
            run(p,value[pos:match.start()],rp,False); run(p,match[1],rp,True); pos=match.end()
        run(p,value[pos:],rp,False)
    else: run(p,value,rp)
    return p
def labeled(template,label,value):
    p=blank(template); runs=template.findall('w:r',NS)
    run(p,label,runs[0].find('w:rPr',NS),True)
    run(p,' '+value,runs[-1].find('w:rPr',NS),False)
    return p
def replace_text(p,old,new):
    matches=[t for t in p.xpath('.//w:t',namespaces=NS) if old in (t.text or '')]
    assert len(matches)==1,(old,tx(p))
    matches[0].text=matches[0].text.replace(old,new)
def delete_inline_span(p,fragment):
    source=tx(p); start=source.index(fragment); end=start+len(fragment); pos=0
    for el in list(p):
        if el.tag=='{'+W+'}pPr': continue
        val=tx(el); finish=pos+len(val)
        left=max(start,pos); right=min(end,finish)
        if left<right:
            if left==pos and right==finish: p.remove(el)
            else:
                texts=el.xpath('.//w:t',namespaces=NS)
                assert el.tag=='{'+W+'}r' and len(texts)==1
                offset1=left-pos; offset2=right-pos
                texts[0].text=val[:offset1]+val[offset2:]
        pos=finish
    assert tx(p)==source.replace(fragment,'',1)

def approved(request):
    def section(start,end): return request.split(start,1)[1].split(end,1)[0]
    titles=section('## 二、最终标题','## 三、替换中文摘要')
    cn_title=re.search(r'中文标题：\s*\*\*(.*?)\*\*',titles,re.S)[1]
    en_title=re.search(r'英文标题：\s*\*\*(.*?)\*\*',titles,re.S)[1]
    cn=section('## 三、替换中文摘要','## 四、替换英文摘要')
    en=section('## 四、替换英文摘要','## 五、替换第0章')
    abstract_cn=re.search(r'\*\*摘 要：\*\*\s*(.+)',cn)[1]
    keywords_cn=re.search(r'\*\*关键词：\*\*\s*(.+)',cn)[1]
    abstract_en=re.search(r'\*\*Abstract:\*\*\s*(.+)',en)[1]
    keywords_en=re.search(r'\*\*Key words:\*\*\s*(.+)',en)[1]
    intro=section('### 0 引言','引言修改要求：').strip()
    paragraphs=re.split(r'\n\s*\n',intro)
    assert len(paragraphs)==8 and paragraphs[4]=='本文主要贡献如下：'
    summary=section('## 八、第5章局部修正','## 九、全文一致性检查')
    summary=re.search(r'“(第3章的 ProVerif 验证表明，.+?)”',summary,re.S)[1]
    return dict(title_cn=cn_title,title_en=en_title,abstract_cn=abstract_cn,abstract_en=abstract_en,
                keywords_cn=keywords_cn,keywords_en=keywords_en,intro=paragraphs,summary5=summary)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--request',type=Path,required=True); ap.add_argument('--expected-sha',required=True)
    args=ap.parse_args(); request=args.request.read_text('utf-8').replace('\r\n','\n'); auth=approved(request)
    data=WORK.read_bytes(); assert sha(data)==args.expected_sha,'Working manuscript changed; inspect again.'
    with zipfile.ZipFile(WORK) as z:
        infos=z.infolist(); before={n:z.read(n) for n in z.namelist()}
    parts=dict(before); root=E.fromstring(parts['word/document.xml']); body=root.find('w:body',NS)
    blocks=list(body); originals={id(p):canon(p) for p in blocks}
    assert tx(blocks[0])=='K-Waay批次准入中参与方互异条件的形式化分析'
    assert tx(blocks[13])=='引言' and tx(blocks[25])=='K-Waay协议及安全问题'
    allowed=set([0,1,4,5,7,10,11,*range(14,25),52,55,65,67,132,223])
    changes=[]
    def replace(index,new,location):
        old=blocks[index]; changes.append({'location':location,'before':tx(old),'after':tx(new)})
        body.replace(old,new)
    replace(0,para(blocks[0],auth['title_cn']),'中文标题')
    replace(7,para(blocks[7],auth['title_en']),'英文标题')
    for i,key,label,loc in [(4,'abstract_cn','摘 要：','中文摘要'),(5,'keywords_cn','关键词：','中文关键词'),
                           (10,'abstract_en','Abstract:','英文摘要'),(11,'keywords_en','Key words:','英文关键词')]:
        replace(i,labeled(blocks[i],label,auth[key]),loc)
    assert '部分更新工作稿' in tx(blocks[1]); body.remove(blocks[1])
    changes.append({'location':'首页非学术工作稿说明','before':tx(blocks[1]),'after':''})
    insertion=list(body).index(blocks[14])
    for old in blocks[14:25]: body.remove(old)
    for i,value in enumerate(auth['intro']):
        new=para(blocks[14] if i<5 else blocks[22],value,rich=True)
        body.insert(insertion+i,new)
        assert tx(new)==value.replace('**','')
    changes.append({'location':'第0章','before_paragraphs':11,'after_paragraphs':8,'author_text_exact':True})
    old52='V6/V7 用于验证状态和生命周期约束，其中 V7 为固定四槽模型；批内重放与后续加固主要采用固定两槽模型。'
    new52='有界批次模型用于验证状态和生命周期约束；批内重放与后续加固采用固定两槽模型。'
    p=copy.deepcopy(blocks[52]); replace_text(p,old52,new52); replace(52,p,'§2.3 有界批次模型表述')
    p=copy.deepcopy(blocks[55]);
    fragment='独立的 RQ-v2 准入原型只比较消息和参与方坐标，其发送发生标识并非协议会话标识 sid。'
    assert fragment in tx(p)
    delete_inline_span(p,fragment); replace(55,p,'§2.3 删除独立 RQ-v2 原型说明')
    p=copy.deepcopy(blocks[65]); rows=p.findall('w:tr',NS)
    assert len(rows)==7 and tx(rows[-1]).startswith('参与方互异')
    removed_row=rows[-1]; p.remove(removed_row)
    # Move the bottom line onto P3; preserve all remaining table text/styles.
    for current,last in zip(rows[-2].findall('w:tc',NS),removed_row.findall('w:tc',NS)):
        borders=current.find('w:tcPr/w:tcBorders',NS); old=borders.find('w:bottom',NS)
        borders.replace(old,copy.deepcopy(last.find('w:tcPr/w:tcBorders/w:bottom',NS)))
    replace(65,p,'表1 删除参与方互异/独立准入原型行，并续接底线')
    p=copy.deepcopy(blocks[67]); replace_text(p,'条件化影响和准入比较','条件化影响'); replace(67,p,'§2.4 删除独立准入比较验证任务')
    sentence=tx(blocks[132]).replace('；同时将发送完成事件安排在确认消息公开之前。','。')
    sentence+='原始模型在基础密文消息公开之后记录发送完成事件；HMAC 加固模型在确认消息公开之前记录发送完成事件。'
    sentence+='原始模型与加固模型分别依据基础消息发送和确认消息发送过程设置发送完成观察点，相关对应关系验证结果应结合各自事件定义理解。'
    assert not blocks[132].xpath('.//m:oMath',namespaces=NS)
    replace(132,para(blocks[132],sentence),'§3.4 明确两个模型各自发送完成观察点')
    replace(223,para(blocks[223],auth['summary5']),'§5.4 使用作者指定的分模型限定总结')
    # Every non-allowlisted block remains the same XML, including chapters1/4/6.
    for i,p in enumerate(blocks):
        if i not in allowed:
            assert p.getparent() is body and canon(p)==originals[id(p)],i
    displayed_before=[canon(p) for p in blocks if p.xpath('./w:pPr/w:pStyle[@w:val="74"]',namespaces=NS)]
    displayed_after=[canon(p) for p in body if p.xpath('./w:pPr/w:pStyle[@w:val="74"]',namespaces=NS)]
    assert displayed_before==displayed_after and len(displayed_after)==32
    all_text='\n'.join(tx(p) for p in body)
    assert all(s not in all_text for s in ['RQ-v2','V6/V7','独立准入原型','部分更新工作稿','Distinct-Party Condition in K-Waay Batch Admission'])
    assert 'DistinctPartyPerBatch' in all_text
    h1=[tx(p) for p in body if p.xpath('./w:pPr/w:pStyle[@w:val="65"]',namespaces=NS)]
    assert len(h1)==7 and h1[0]=='引言' and h1[-1]=='结束语'
    # Record unused references without deleting/reordering bibliography.
    ref=next(i for i,p in enumerate(body) if tx(p)=='参考文献')
    cited=set()
    for p in list(body)[:ref]:
        for match in re.finditer(r'\[([0-9,\-]+)\]',tx(p)):
            for item in match[1].split(','):
                if '-' in item:
                    a,b=map(int,item.split('-')); cited.update(range(a,b+1))
                else: cited.add(int(item))
    refs=[tx(p) for p in list(body)[ref:] if p.xpath('./w:pPr/w:pStyle[@w:val="84"]',namespaces=NS)]
    assert len(refs)==8 and cited.issubset(set(range(1,9)))
    assert 'K-Waay' in refs[1] and '2024/120' in refs[2] and 'Signal' in refs[3] and 'PQXDH' in refs[4]
    parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    core=E.fromstring(parts['docProps/core.xml']); dc='{http://purl.org/dc/elements/1.1/}'
    for key,value in [('title',auth['title_cn']),('description','论文工作稿：中英文标题、摘要、引言及第2、3、5章科学表述已按作者确认稿对齐。正文结构0至6章；未改动冻结研究证据。')]:
        node=core.find(dc+key)
        if node is None: node=E.SubElement(core,dc+key)
        node.text=value
    parts['docProps/core.xml']=E.tostring(core,xml_declaration=True,encoding='UTF-8',standalone=True)
    temporary=WORK.with_suffix('.alignment.tmp.docx')
    with zipfile.ZipFile(temporary,'w') as z:
        for info in infos: z.writestr(info,parts[info.filename])
    with zipfile.ZipFile(temporary) as z:
        assert z.testzip() is None
        assert z.namelist()==list(before)
        for n in before:
            if n not in ('word/document.xml','docProps/core.xml'): assert z.read(n)==before[n]
    assert sha(WORK.read_bytes())==args.expected_sha; temporary.replace(WORK)
    QA.mkdir(parents=True,exist_ok=True)
    manifest={'base_sha256':args.expected_sha,'working_sha256':sha(WORK.read_bytes()),'request_sha256':sha(args.request.read_bytes()),
              'frontmatter_and_introduction_exact_author_text':True,'protected_chapters':[1,4,6],
              'unchanged_display_math_paragraphs':len(displayed_after),'unchanged_table_numbers':[2,3,4],
              'unchanged_bibliography_entries':8,'cited_reference_numbers':sorted(cited),
              'uncited_references':[{'number':i+1,'entry':s} for i,s in enumerate(refs) if i+1 not in cited],
              'reference2_to5_checked':'K-Waay proceedings; K-Waay full ePrint; Signal; PQXDH, respectively',
              'unchanged_package_parts':[n for n in before if n not in ('word/document.xml','docProps/core.xml')],
              'final_chapter_titles':h1,'changes':changes,'visual_qa':'pending actual WPS inspection'}
    (QA/'approved-text.json').write_text(json.dumps(auth,ensure_ascii=False,indent=2)+'\n','utf-8')
    (QA/'alignment-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k not in ('changes','unchanged_package_parts')},ensure_ascii=False))

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8'); main()
