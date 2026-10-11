"""Generate the two added presentation tables from reviewed evidence; no prover run."""
import csv, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
LATEX = ROOT / 'submissions/arocmag/latex-v2'
source = {
 'caption': '表 2　原协议对象到两槽抽象的映射',
 'widths': [3.3, 3.0, 4.0, 5.5],
 'rows': [
  ['原协议对象', '形式化表示', '保留语义', '省略内容与假设'],
  ['输入中的公钥、预密钥束及其参与方关联', '$A_i$', '比较条目所关联的参与方', '假设参与方投影正确；不验证密钥编码、预密钥及身份解析'],
  ['一次发送及其协议消息', '$(\\mathit{oid}_i,m_i)$', '区分发送实例及其新鲜符号消息', '不表示原协议transcript会话标识，不展开密文结构或密钥派生'],
  ['条目的发送来源', '\\texttt{!Sent(A,oid,m)}', '处理时要求完整元组精确匹配；来源可被重复读取', '理想化来源事实，不证明签名、解封装或完整密码学认证'],
  ['输入向量$S$中的两个位置', '$(E_1,E_2)$及线性槽位', '有序收集、攻击者组合和顺序处理', '机器范围固定为两槽，不推广为任意批长验证'],
  ['同次调用与共享接收方临时状态', '$(\\mathit{bid},\\mathit{rst})$', '限定共同批次和接收方上下文', '不是协议线路字段或完整临时密码状态'],
  ['按输入分量组织的接收结果', '\\texttt{ReceiverAccept}观察事件', '观察各槽位来源匹配后的抽象接受', '不产生真实会话标识或密钥，不表示密钥安装；分量输出仅构成动机'],
 ],
 'note': '注：表1解释模型内部比较坐标，本表解释原接口到抽象模型的取舍；该映射由研究者建立，尚无协议精化证明。'
}
roles = {
 ('rqv2_relaxed','normal_relaxed_batch_exists'): '基本准入及一次接受可达',
 ('rqv2_relaxed','one_send_two_accepts_exists'): '一源两接受的完整见证',
 ('rqv2_relaxed','receiver_accept_injective'): '来源复用的反例',
 ('rqv2_message_dedup','repeated_message_rejection_exists'): '消息重复拒绝分支可达',
 ('rqv2_message_dedup','same_party_different_messages_batch_exists'): '消息约束非替代性的见证',
 ('rqv2_message_dedup','accepted_batch_has_distinct_messages'): '确认消息级目标成立',
 ('rqv2_message_dedup','receiver_accept_injective'): '排除同一精确来源复用',
 ('rqv2_party_admission','same_party_rejection_exists'): '参与方重复拒绝分支可达',
 ('rqv2_party_admission','distinct_party_batch_exists'): '有效不同参与方批次可达',
 ('rqv2_party_admission','accepted_batch_has_distinct_parties'): '确认参与方级目标成立',
 ('rqv2_party_admission','receiver_accept_injective'): '目标对照的来源单射关系',
}
rows = list(csv.DictReader((ROOT/'reviews/2026-09-16-evidence/result-comparison.tsv').open(encoding='utf-8-sig'),delimiter='\t'))
full={'caption':'表 6　完整Tamarin验证结果及论证作用','widths':[0.7,6.1,2.0,1.4,0.8,4.8],
 'rows':[['模型','lemma名称','迹量词','结果','步数','论证作用']],
 'note':'注：R、M、P分别为无互异、消息互异、参与方互异约束模型；exists-trace为存在性，all-traces为全称性。步数为既有证明器记录，不代表运行时间或性能。'}
records=[]
for row in rows:
 model,lemma=row['model'],row['lemma']
 text=(ROOT/'tamarin/rq-v2-minimal'/f'{model}.spthy').read_text()
 decl=re.search(r'lemma\s+'+re.escape(lemma)+r'\s*:(.*?)(?=\nlemma|\nend)',text,re.S).group(1)
 kind='exists-trace' if 'exists-trace' in decl.split('"')[0] else 'all-traces'
 role=roles.get((model,lemma),'每个接受均有精确匹配发送')
 short={'rqv2_relaxed':'R','rqv2_message_dedup':'M','rqv2_party_admission':'P'}[model]
 full['rows'].append([short,lemma,kind,row['status'],row['steps'],role])
 records.append(dict(row,type=kind,role=role))
assert len(rows)==14 and sum(r['status']=='verified' for r in rows)==13
assert sum(r['type']=='exists-trace' for r in records)==6
tables={'source-to-abstraction':source,'full-verification-results':full}
(Path(__file__).parent/'stage6-evidence-tables.json').write_text(json.dumps(tables,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'submissions/arocmag/word-final/qa/stage6/result-bindings.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name,data in tables.items():
 caption=re.sub(r'^表 \d+　','',data['caption'])
 cols=r'@{}L{0.19\linewidth}L{0.17\linewidth}L{0.23\linewidth}Y@{}' if name=='source-to-abstraction' else r'@{}L{0.035\linewidth}L{0.36\linewidth}L{0.12\linewidth}L{0.09\linewidth}L{0.045\linewidth}Y@{}'
 lines=[r'\begin{table}[htbp]',r'  \centering',r'  \caption{'+caption+'}',r'  \label{tab:'+name+'}',r'  \footnotesize',r'  \setlength{\tabcolsep}{3pt}',r'  \begin{tabularx}{\linewidth}{'+cols+'}',r'    \toprule']
 for i,row in enumerate(data['rows']):
  values=list(row)
  if name=='full-verification-results' and i:
   values[1]=r'{\scriptsize\path{'+values[1]+'}}'
   values[2]=r'{\scriptsize '+values[2]+'}'
  lines.append('    '+' & '.join(values)+r' \\')
  if i==0: lines.append(r'    \midrule')
 lines += [r'    \bottomrule',r'  \end{tabularx}',r'  \par\smallskip',r'  \begin{minipage}{\linewidth}',r'    \scriptsize '+data['note'],r'  \end{minipage}',r'\end{table}','']
 (LATEX/'tables'/f'{name}.tex').write_text('\n'.join(lines),encoding='utf-8')
print('Generated source mapping and full 14-result tables; types read from existing models.')
