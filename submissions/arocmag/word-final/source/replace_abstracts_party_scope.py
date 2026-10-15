"""Replace only the author's four abstract/keyword paragraphs; keep all else."""
import copy
import json
import zipfile
from pathlib import Path
from lxml import etree
from align_abstracts_introduction import tx, canon, sha, labeled, NS

OUT=Path(__file__).resolve().parent.parent
WORK=OUT/'K-Waay-AROCMAG-submission-working.docx'
QA=OUT/'qa/abstracts-party-scope-replacement'
EXPECTED='a33fadf6d13d89b18e6fec29c52ce0ca078b568a3d65979121b8d66a3dad5a9b'
CN='后量子认证密钥交换协议 K-Waay 通过批量接收机制提高异步通信效率，但其接收安全不仅涉及会话参数的一致性，还依赖批次内参与方的身份约束。为分析相关安全条件的作用，采用 ProVerif 和 Tamarin 对协议接收过程进行形式化研究。结果表明，密文重组攻击可导致收发双方会话参数失配，HMAC 密钥确认能够阻断相应攻击路径；批内原子消息去重虽可防止相同消息重复接受，却无法保证不同输入对应不同参与方。进一步分析发现，同一参与方的不同合法消息仍可能违反原协议的批次身份约束。针对这一问题，提出基于参与方绑定的批次准入机制，并通过形式化验证证明其在固定两槽模型中能够恢复参与方互异性质，同时保持合法批次的正常执行。研究结果揭示了消息级保护与批次身份约束的不同安全作用，为 K-Waay 接收端安全加固提供了依据。'
CNKEY='K-Waay；形式化验证；密文重组；批次身份约束；参与方绑定；HMAC'
EN="K-Waay, a post-quantum authenticated key exchange protocol, improves the efficiency of asynchronous communication through batch reception. However, its receiver-side security depends not only on session parameter consistency but also on party-identity constraints within each batch. To investigate these security conditions, ProVerif and Tamarin are employed to formally analyze the protocol's receiving process. The results show that a ciphertext recomposition attack can cause a session parameter mismatch between the sender and receiver, while HMAC-based key confirmation prevents the corresponding attack. Although atomic intra-batch message deduplication prevents duplicate acceptance of identical messages, it cannot ensure that distinct batch entries correspond to distinct parties. Further analysis demonstrates that different legitimate messages from the same party can still violate the protocol's distinct-party condition. To address this issue, a party-binding-based batch admission mechanism is proposed. Formal verification shows that the mechanism restores the distinct-party property in a fixed two-slot model while preserving the reachability of valid batch executions. These findings clarify the different security roles of message-level protection and batch-level identity constraints, providing a formal basis for strengthening receiver-side security in K-Waay."
ENKEY='K-Waay; formal verification; ciphertext recomposition; batch identity constraints; party binding; HMAC'

def main():
    data=WORK.read_bytes();assert sha(data)==EXPECTED,'Working file changed; inspect before replacing'
    with zipfile.ZipFile(WORK) as z:infos=z.infolist();original={n:z.read(n) for n in z.namelist()}
    package=dict(original);root=etree.fromstring(package['word/document.xml']);body=root.find('w:body',NS)
    blocks=list(body);before=[canon(p) for p in blocks]
    changes=[];allowed=set()
    for start,label,value in [('摘 要：','摘 要：',CN),('关键词：','关键词：',CNKEY),('Abstract:','Abstract:',EN),('Key words:','Keywords:',ENKEY)]:
        matches=[(i,p) for i,p in enumerate(blocks) if tx(p).startswith(start)]
        assert len(matches)==1,(start,len(matches))
        i,p=matches[0];assert i<12
        new=labeled(p,label,value)
        assert etree.tostring(new.find('w:pPr',NS),method='c14n',exclusive=True)==etree.tostring(p.find('w:pPr',NS),method='c14n',exclusive=True)
        assert tx(new)==label+' '+value
        assert len(new.findall('w:r',NS))==2
        assert new.findall('w:r',NS)[0].find('w:rPr/w:b',NS).get('{'+NS['w']+'}val')=='1'
        assert new.findall('w:r',NS)[1].find('w:rPr/w:b',NS).get('{'+NS['w']+'}val')=='0'
        body.replace(p,new);allowed.add(i)
        changes.append({'block':i,'before':tx(p),'after':tx(new),'pPr_preserved':True,'label_bold_body_regular':True})
    assert allowed=={3,4,9,10}
    for i,p in enumerate(body):
        if i not in allowed:assert canon(p)==before[i],'Unexpected change outside abstracts'
    package['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    for n in original:
        if n!='word/document.xml':assert package[n]==original[n]
    tmp=WORK.with_suffix('.abstracts.tmp.docx')
    with zipfile.ZipFile(tmp,'w') as z:
        for info in infos:z.writestr(info,package[info.filename])
    with zipfile.ZipFile(tmp) as z:
        assert z.testzip() is None
        for n in original:
            if n!='word/document.xml':assert z.read(n)==original[n]
    assert sha(WORK.read_bytes())==EXPECTED;tmp.replace(WORK)
    QA.mkdir(parents=True,exist_ok=True)
    report={'before_sha256':EXPECTED,'after_sha256':sha(WORK.read_bytes()),'changed_blocks':sorted(allowed),
        'only_package_part_changed':'word/document.xml','academic_source_text_exact':True,
        'all_other_body_blocks_and_picture_layout_preserved':True,'existing_template_pPr_and_font_properties_preserved':True,
        'changes':changes,'visual_review':'Not performed; picture-layout work remains paused; no WPS opened this turn'}
    (QA/'replacement-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='changes'},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
