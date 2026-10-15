"""Exact author text replacement; restore reliable inline figures and re-place pairs."""
import copy
import json
import re
import zipfile
from pathlib import Path
from lxml import etree
from align_abstracts_introduction import tx,canon,sha,blank,run,NS

OUT=Path(__file__).resolve().parent.parent
WORK=OUT/'K-Waay-AROCMAG-submission-working.docx'
SOURCE=OUT/'source/intro-conclusion-party-author-approved.md'
QA=OUT/'qa/intro-conclusion-and-flow'
EXPECTED='167c8462fea8c60ea9dbab45165da3a4819b136ce246d95d49e79ca6b6e15c66'
W=NS['w']
DRAW={'wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
def find_title(blocks,title):
    found=[p for p in blocks if tx(p)==title and p.xpath('./w:pPr/w:pStyle/@w:val',namespaces=NS)==['65']]
    assert len(found)==1,title;return found[0]
def paragraph(prototype,source,citepr):
    p=blank(prototype);pr=prototype.find('w:r/w:rPr',NS)
    for i,segment in enumerate(re.split(r'\*\*(.*?)\*\*',source)):
        pos=0
        for m in re.finditer(r'\[\d+(?:-\d+)?\]',segment):
            run(p,segment[pos:m.start()],pr,bool(i%2));run(p,m[0],citepr,False);pos=m.end()
        run(p,segment[pos:],pr,bool(i%2))
    assert tx(p)==source.replace('**','')
    return p

def main():
    data=WORK.read_bytes();assert sha(data)==EXPECTED
    with zipfile.ZipFile(WORK) as z:infos=z.infolist();parts={n:z.read(n) for n in z.namelist()}
    originals=dict(parts);root=etree.fromstring(parts['word/document.xml']);body=root.find('w:body',NS)
    blocks=list(body);snapshot=[canon(p) for p in blocks]
    oldintro=find_title(blocks,'引言');one=find_title(blocks,'K-Waay协议及安全问题')
    ending=find_title(blocks,'结束语');refs=next(p for p in blocks if tx(p)=='参考文献')
    istart=blocks.index(oldintro)+1;iend=blocks.index(one)
    estart=blocks.index(ending)+1;eend=blocks.index(refs)
    assert eend-estart==2
    src=SOURCE.read_text('utf-8');intro_src,ending_src=src.split('# 6 结束语')
    intro=re.split(r'\n\s*\n',intro_src.split('# 0 引言',1)[1].strip())
    conclusion=re.split(r'\n\s*\n',ending_src.strip());assert len(intro)==7 and len(conclusion)==2
    citepr=next((r.find('w:rPr',NS) for p in blocks[istart:iend] for r in p.findall('w:r',NS)
                 if re.fullmatch(r'\[\d+(?:-\d+)?\]',tx(r))),None)
    if citepr is None:
        citepr=copy.deepcopy(blocks[istart].find('w:r/w:rPr',NS))
        v=etree.SubElement(citepr,'{'+W+'}vertAlign');v.set('{'+W+'}val','superscript')
    newintro=[paragraph(blocks[istart] if i<4 else blocks[iend-1],s,citepr) for i,s in enumerate(intro)]
    newend=[paragraph(blocks[estart],s,citepr) for s in conclusion]
    changed=set(range(istart,iend))|set(range(estart,eend))
    for p in blocks[istart:iend]:body.remove(p)
    at=list(body).index(oldintro)+1
    for i,p in enumerate(newintro):body.insert(at+i,p)
    for p in blocks[estart:eend]:body.remove(p)
    at=list(body).index(ending)+1
    for i,p in enumerate(newend):body.insert(at+i,p)
    # Restore the original editable picture/caption paragraphs from the pre-trial XML.
    baseroot=etree.parse(str(OUT/'qa/figure-flow-repair/before-document.xml'))
    baseblocks=list(baseroot.find('w:body',NS));pairs={}
    for n in (3,4):
        image=next(p for p in list(body) if p.xpath('.//wp:docPr/@name',namespaces=DRAW)==[f'K-Waay Figure{n} floating with caption'])
        oldidx=blocks.index(image);changed.add(oldidx)
        basecap=next(p for p in baseblocks if tx(p).startswith('图'+str(n)+' '))
        baseimage=baseblocks[baseblocks.index(basecap)-1]
        assert baseimage.xpath('.//w:drawing',namespaces=NS)
        pairs[n]=(copy.deepcopy(baseimage),copy.deepcopy(basecap))
        body.remove(image)
    # Fill previous blank space with existing prose. Preserve prose relative order.
    after3=next(p for p in body if tx(p).startswith('其中，HMAC 负责验证发送与接收会话参数的一致性'))
    after4=next(p for p in body if tx(p).startswith('上述研究解决的是会话参数确认与相同消息重复接受问题'))
    for n,anchor in ((3,after3),(4,after4)):
        at=list(body).index(anchor)+1
        for j,p in enumerate(pairs[n]):body.insert(at+j,p)
    # Untouched academic blocks are byte/canonical-identical and in the same order.
    expected_other=[p for i,p in enumerate(blocks) if i not in changed]
    actual_other=[p for p in body if p not in newintro+newend+list(pairs[3])+list(pairs[4])]
    assert len(expected_other)==len(actual_other)
    assert [canon(p) for p in expected_other]==[canon(p) for p in actual_other]
    assert len(root.xpath('//wp:anchor',namespaces=DRAW))==0
    assert len(root.xpath('//wp:inline',namespaces=DRAW))==5
    assert len(root.xpath('//w:drawing',namespaces=NS))==5
    assert [canon(p) for p in newintro+newend if p.find('w:pPr',NS) is None]==[]
    parts['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    for n in originals:
        if n!='word/document.xml':assert parts[n]==originals[n]
    tmp=WORK.with_suffix('.intro-conclusion-flow.tmp.docx')
    with zipfile.ZipFile(tmp,'w') as z:
        for info in infos:z.writestr(info,parts[info.filename])
    with zipfile.ZipFile(tmp) as z:assert z.testzip() is None
    assert sha(WORK.read_bytes())==EXPECTED;tmp.replace(WORK)
    QA.mkdir(parents=True,exist_ok=True)
    manifest={'before_sha256':EXPECTED,'after_sha256':sha(WORK.read_bytes()),'source_sha256':sha(SOURCE.read_bytes()),
              'intro_paragraphs':7,'conclusion_paragraphs':2,'author_text_exact':True,
              'all_other_academic_blocks_preserved':True,'abstracts_preserved':True,
              'figure_trial_removed':'Both floating groups replaced by original inline picture/caption pairs',
              'figure3_new_position':'After first two mechanism overview paragraphs of3.5, before the basic-message definition',
              'figure4_new_position':'After3.6 summary and before chapter4; citation remains in3.5',
              'image_sizes_crops_media_bytes_unchanged':True,'only_changed_part':'word/document.xml','visual_review':'pending'}
    (QA/'replacement-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
