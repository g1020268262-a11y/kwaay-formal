"""Move only Figure 3 and its caption to let existing prose fill the prior column."""
import json, zipfile
from pathlib import Path
from lxml import etree
from align_abstracts_introduction import tx, canon, sha, NS

OUT=Path(__file__).resolve().parent.parent
WORK=OUT/'K-Waay-AROCMAG-submission-working.docx'
EXPECTED='19809cfa91e560e2e369d027bb57e8dd1ac20f2e971496432e76bd61d01bdd9c'
data=WORK.read_bytes()
assert sha(data)==EXPECTED
with zipfile.ZipFile(WORK) as z:
    infos=z.infolist(); parts={n:z.read(n) for n in z.namelist()}
root=etree.fromstring(parts['word/document.xml']); body=root.find('w:body',NS)
blocks=list(body)
caption=next(p for p in blocks if tx(p).startswith('图3 '))
picture=blocks[blocks.index(caption)-1]
assert picture.xpath('.//w:drawing',namespaces=NS)
pair=[picture,caption]
before=[canon(p) for p in blocks if p not in pair]
anchor=next(p for p in blocks if tx(p).startswith('去重机制比较的是完整基础消息'))
for p in pair:body.remove(p)
at=list(body).index(anchor)+1
for i,p in enumerate(pair):body.insert(at+i,p)
assert before==[canon(p) for p in body if p not in pair]
parts['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
tmp=WORK.with_suffix('.flow.tmp.docx')
with zipfile.ZipFile(tmp,'w') as z:
    for info in infos:z.writestr(info,parts[info.filename])
with zipfile.ZipFile(tmp) as z:assert z.testzip() is None
assert sha(WORK.read_bytes())==EXPECTED
tmp.replace(WORK)
manifest={'before_sha256':EXPECTED,'after_sha256':sha(WORK.read_bytes()),
          'change':'Figure3 picture/caption pair moved after deduplication-key explanation in3.5',
          'all_other_blocks_identical':True,'all_non_document_parts_unchanged':True}
(OUT/'qa/intro-conclusion-and-flow/figure3-final-flow.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
