from pathlib import Path
import hashlib, json, re

ROOT = Path('D:/kwaay-formal')
OUT = ROOT/'submissions/arocmag/terminology-study'
EV = OUT/'evidence'
def write(name, text):
    (OUT/name).write_text(text.rstrip()+'\n', encoding='utf-8')
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
protected = ['submissions/arocmag/latex-v2','manuscript','tamarin/rq-v2-minimal','reviews','submissions/arocmag/style-study']
manifest = {p.relative_to(ROOT).as_posix(): digest(p) for d in protected for p in (ROOT/d).rglob('*') if p.is_file()}
manifest_path = EV/'protected-inputs.sha256.json'
if manifest_path.exists():
    original = json.loads(manifest_path.read_text(encoding='utf-8'))
    if original != manifest:
        raise RuntimeError('Protected inputs changed; do not overwrite the audit baseline.')
else:
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
files = []
for d in ['submissions/arocmag/latex-v2/sections','submissions/arocmag/latex-v2/tables','submissions/arocmag/latex-v2/notes','manuscript/sections','manuscript/tables','tamarin/rq-v2-minimal']:
    files += [p for p in (ROOT/d).rglob('*') if p.is_file() and p.suffix in ('.tex','.md','.spthy')]
files.append(ROOT/'manuscript/paper-content.tex')
texts = {p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for p in sorted(files)}
# English | current Chinese | frozen expression | class | evidence | risk/definition
# T tool concept; A established academic concept; M model/author-defined phrase.
DATA = r'''
party; protocol principal|参与方；协议主体|参与方|A|P2 p5；P3 p3；M|A是建模主体，不自动等同于账户、公钥字节串或预密钥
party identity|参与方身份；参与方坐标|参与方标识|M|P3 p3（身份概念）；M|指条目中A分量；不得据此主张身份认证
party projection|参与方投影；身份投影|参与方投影|M|E2；M|保留数学投影party(E)，即从条目取出A；不用身份认证
message identity; message coordinate|消息坐标|消息标识维度；元组中称消息分量|M|E2；M|m为模型中的符号消息；不是实现中的message ID字段
sender occurrence|发送发生|发送实例|M|P3 p3、P6 p4（仅支持实例一词）；M|一次SendMessage规则实例化产生的发送实例，不是完整协议会话
sender occurrence coordinate; sid; oid|发送发生坐标；一次发送发生|发送实例标识|M|T1 Fresh Names；M SendMessage|oid对应模型sid；与事件时间点s分开，禁止完整会话标识
sender-origin tuple|发送来源元组；精确元组|发送来源元组|M|E4；M !Sent|完整(A,oid,m)，不是仅A，也不是网络编码
exact sender origin|精确发送来源；精确来源|精确发送来源|M|E4；M Send/!Sent|首次解释为与完整(A,oid,m)匹配的发送来源；禁止真实来源认证
identity coordinate; comparison dimension|身份坐标；坐标|标识维度|M|E2；M|用于比较A、oid、m、槽位和上下文；不是几何坐标或均为人的身份属性
tuple component|分量；坐标|元组分量|A|E2；M|解释E=(A,oid,m)时用分量；槽位和上下文不擅自加入该三元组
batch|批次；批处理|批次|M|E2；M CreateBatch|一组有序候选条目；处理过程才称批处理
batch admission|批处理接纳；接纳|批次准入|M|A1；A2（均仅支持准入）；E2/M|本文分析边界，非K-Waay原协议算法名；不等于接受事件
batch composition|批组成；批次组合|批次组合|M|E3；M CollectSlot1/2|选择、排列、重复已有候选条目，非密码组件的可组合安全定理
receiver context|接收方上下文；接收上下文|接收方上下文|M|E4；M CreateBatch|rst是模型标识，不是完整接收方临时密码状态
batch context; same-batch scope|批次上下文；作用域|批次上下文；同一批次上下文内|M|E4；M|性质中的共同上下文为同一(bid,rst)，简称批内须先定义
slot; position|槽位；位置|槽位|M|E2；M CollectSlot1/2|批次内位置，两个槽位不推出两消息或两参与方不同
entry; candidate tuple|条目；候选元组|条目；候选条目|M|E2；M|候选条目、准入条目、已产生接受事件的条目不可混同
trace; execution trace|迹；执行；执行轨迹；符号迹|执行轨迹；理论定义后可简称迹|T|S2（迹语义）；T2|运行叙述用执行轨迹；不把符号轨迹称真实网络日志
trace semantics|迹语义|迹语义|T|S2 §1.2；T2|保留专业表达并定义本文动作事实序列的语义；不移植MSC半序定义
trace property|迹性质|迹性质|T|T2；M lemma|理论语境保留；正文也可说关于执行轨迹的性质
all-traces; all traces|全迹；全迹性质；全迹验证|全称性质（all-traces）|T|T2；M 默认lemma|表中简称全称性；对模型所有执行轨迹量化，不是无限协议能力保证
exists-trace|存在迹；存在迹性质|存在性性质（exists-trace）|T|T2；T3；M|表中简称存在性；本文相关性质可解释为某类执行可达，但不是所有exists-trace都叫可达性
witness|见证；机器见证；存在性见证|按语境：见证值／满足性质的执行轨迹|M|T2/T3（语义）；E5/M|不得把所有witness一律改成反例或攻击
witness value|见证值（正文未直接使用）|见证值|A|T2 量词；M Ex|逻辑存在量词的取值；复合中文用法未在本次中文样本建立共识
witness execution; witness trace|见证；机器见证|满足存在性性质的执行轨迹|M|T2/T3；M exists-trace|简写可达执行或该执行轨迹；需标明满足哪项性质
same-party/different-message witness|同一参与方见证；同参与方不同消息见证|同一参与方不同消息批次的可达执行|M|E5；M same_party_different_messages_batch_exists|同一A，不同oid和m，两个匹配Send及两个同上下文接受
counterexample; counterexample trace|反例；反例轨迹|反例；反例轨迹|A|P1 p4；T2|反驳指定全称性质的执行；不是完整K-Waay攻击
attack trace|攻击轨迹；完整协议攻击|攻击轨迹（仅已建立攻击语义时）|A|P1 p4（攻击路径）；S1|当前两槽结果称反例轨迹或可达执行，不升级为部署攻击
reachability|可达性；可达执行|可达性|A|P6 p5；T3|存在所需事件及次序的执行，不是所有输入都能到达
correspondence|对应；对应关系|对应关系；性质名称用对应性|A|T2 Authentication；S1 表3|匹配字段、方向、时间及量词均须定义；不默认是认证
origin correspondence|精确来源对应；来源对应|精确发送来源对应性|M|E4/E5；M receiver_accept_has_send|ReceiverAccept蕴含先前完整元组匹配Send；不等于源真实性
injectivity|注入性；认证注入性|单射性（抽象数学语境）|A|P1 p3；S1 §2.1.1；T2|具体性质按下列完整名；文献回顾Lowe概念用单射一致性
occurrence injectivity; scoped occurrence injectivity|作用域内发生注入性；发生注入性|批次上下文内的发送—接受单射对应性|M|M receiver_accept_injective；T2（对照定义）|简称批内单射对应性；同一(bid,rst)下给定先前精确Send最多对应一次接受
injective agreement|单射一致性（待审计术语）|单射一致性|A|P1 p3；S1 §2.1.1/表3；T2|只用于Lowe认证概念；不能命名本文receiver_accept_injective
distinct-party condition; different-party condition|不同参与方条件|批内参与方互异条件|M|E2；M；P3（仅基础名词）|原协议已有条件；本文命名而非原文正式算法；限定同次调用
party distinction|参与方区分|批内参与方互异性|M|M accepted_batch_has_distinct_parties；E5|同一(bid,rst)不同接受事件具有不同A，不是身份认证或全局唯一
message distinction|消息区分|批内消息互异性|M|M accepted_batch_has_distinct_messages；E5|不同接受事件的m不等；不是密码学可区分性或机密性
positive control|正控制|目标对照|M|E2/E5；M party_admission|首次用直接施加目标约束的对照模型（positive control）；非修复方案
relaxed admission|放宽配置；放宽|无互异约束的批次准入模型|M|M rqv2_relaxed；E4|仅不施加消息/参与方互异约束，仍有来源和顺序约束；禁无约束模型
message-level restriction; message-level configuration|消息级限制；消息级配置|消息互异约束的批次准入模型|M|M rqv2_message_dedup；E4|比较m1与m2；并非新协议或实现中的全部去重策略
party-level admission; party-level configuration|参与方级配置；参与方级正控制|参与方互异约束的批次准入模型|M|M rqv2_party_admission；E4|比较A1与A2；用作目标对照，禁止修复协议
controlled comparison|受控比较；受控配置|受控比较|M|E4/E5；M共同规则|相同生命周期下改变准入约束，非随机实验或三种真实实现
fact|事实；来源事实|事实|T|P2 p2–3；T1|模型符号对象，不表示经验证的真实世界事实
action fact|动作事实；动作|动作事实|T|P2 p2（动作/action事实）；T1|记录事件供性质使用，区分状态事实与动作标签
persistent fact|持久事实；持久来源事实|持久事实|T|T1；M !Sent/!Party|可被多次匹配，不是数据库持久化，也不自动产生多个Send事件
linear fact; state fact|线性槽位；收集状态|线性事实；状态事实|T|T1；M OpenSlot/AdmittedSlot|线性事实使用时消耗；不要把槽位本身误称不可复用的消息
multiset rewriting|多集重写|多集重写|T|P2 p2（多重集合改写）；T1|允许多重集重写/多重集合改写；同文优先多集重写
rule; rule-level semantics|规则；规则层；规则语义|规则；规则语义|T|P2 p2；T1；M|约束执行构造方式，不等于已验证性质
restriction|不等式约束；限制|限制条件（restriction）|T|T2 Restrictions；M Inequality|工具关键字限制允许的轨迹；与普通message-level restriction区别
guard; admission condition|接纳条件；约束|准入条件|M|M Neq+Inequality；T2|Neq动作联合restriction落实不等式，不能称独立布尔guard即全部实现
lemma|lemma；性质；引理|待验证性质（lemma）|T|P1 p1；P2 p2；T2|lemma是声明类别，可能被否定；不统一称已证明引理
fresh name; fresh value|新鲜；新鲜坐标|新鲜值；新鲜标识|T|T1 Fresh Names；M Fr|符号新鲜性不等同现实随机数碰撞概率；sid与m分别生成
timepoint; event occurrence|时间条件；事件发生；接受发生数|事件时间点；一次事件发生|T|T2；M #s/#r|r1与r2表示事件位置，不是sid/oid；接受发生数改接受事件数
Send; send event|Send动作；发送事件|发送事件（Send）|M|M SendMessage；E4|模型动作不是完整原协议Send算法的全部语义
ReceiverAccept; acceptance event|接收事件；接受事件；ReceiverAccept|接受事件（ReceiverAccept）|M|M ProcessSlot1/2；E4|不是In网络接收，不是完整会话接受，不是成功密钥建立
BatchReceive action|BatchReceive动作；批次接纳|批次准入事件（模型中的BatchReceive）|M|M admission规则；E4|必须与规范BatchReceive操作区分；准入不等于两槽均已接受
rejection branch; rejection reachability|拒绝分支；拒绝见证|拒绝分支可达性|M|M 两个rejection_exists|存在性不蕴含所有无效输入最终拒绝，且Send未绑定被拒元组
non-vacuity; vacuous truth|非真空性；真空成立|排除因无相关接受事件而成立的情形（non-vacuity）|M|T3；M distinct_party_batch_exists|中文短名NO_STABLE_CONSENSUS；结果处用有效批次可达性及明确解释
refinement; refinement theorem|refinement；refinement theorem|精化；精化定理|A|S3（检索摘要）；E6|当前未建立模型到完整协议/实现的精化定理；不把映射说明称精化证明
symbolic model; symbolic abstraction|符号模型；两槽抽象|符号模型；符号抽象|A|P1/P2；T1；M|固定两槽不等于整个模型仅两次会话，也不是任意批长定理
Dolev–Yao adversary; attacker|攻击者；对手；敌手|Dolev–Yao攻击者；攻击者|A|P1 p3；P4 p6；P6|文献中的敌手可保留引用；模型实例能力以规则为准
replay; repeated acceptance|重放；重复接受|重放；重复接受|A|P1；P4 p6；M|重复接受是抽象行为，重放候选元组不推出完整协议重放攻击
authentication; secrecy|认证；保密性；密钥安全|认证；保密性|A|P1 p3；P4 p6；S1|仅背景或边界说明；来源对应和消息互异不升级为这些性质
authenticated key exchange; deniable|认证密钥交换；可否认|认证密钥交换；可否认性|A|P3/P7（认证密钥协商）；E1/E2|原协议背景，不是本模型新增证明
KEM; split-KEM; prekey bundle|KEM；split-KEM；预密钥束|KEM；split-KEM；预密钥束|A|E2及其引用|保留源协议术语；首次KEM可注密钥封装机制，split-KEM不强造拆分中文标准
transcript; session identifier; wire representation|transcript；session标识；线路编码|协议交互记录；会话标识；传输编码|A|E2；P3 p3（会话标识）|说明oid不是完整协议交互记录或会话标识；勿把抽象元组写成网络字段
non-implication; non-substitutability|非蕴含；非替代性|不蕴含；不能替代|M|E2/E5；M|逻辑例子和机器可达执行分别给证据，不将常识例子充当机器结果
verified; falsified; proof steps|已验证；被反例否定；证明步数|验证通过；被否定；证明步数|T|T2/T3；E5结果表|全称falsified可称被反例否定；exists-trace的falsified不可照搬；steps不是运行时间
bounded abstraction; arbitrary batch sizes|固定两槽；任意批长|固定两槽抽象；任意批次长度|M|E3/E6；M|两槽界限是每批槽数；批次/发送实例总数未被固定为2
matching origin; idealized origin relation|来源匹配；精确来源关系|精确发送来源匹配；抽象来源关系|M|E4；M !Sent|!Sent是持久事实的建模假设，不是实现的密码学认证机制
sequential processing; common lifecycle|顺序处理；共同生命周期；共同骨架|顺序处理；共同生命周期|M|E4；M ProcessSlot1/2|三模型共同处理过程，不推断现实网络时序完全相同
scope; global uniqueness|作用域；全局唯一性|作用域；全局唯一性|A|M 量词；E2|批内性质不声称跨批唯一；但模型Fr确实令新生成sid/m在一条执行中新鲜，不可否认这一规则事实
aliveness; liveness|liveness；存活性|Lowe存活性；活性（liveness）|A|P1 p3；T2；E5|区分Lowe认证层级aliveness与最终发生的活性性质；拒绝存在性不证明后者
supporting property; key result|支持性质；核心结果|支持性质；核心结果|M|E5；当前表4|论文取舍标签，非工具安全等级；不可删去量词类型
source-to-abstraction mapping|来源到抽象映射；模型映射|协议来源与模型抽象的对应说明|M|E4；E6|说明性映射不等于精化证明，不能把缺失机制当已实现
composition boundary; cryptographic component|组合边界；密码组件|组合边界；密码组件|M|E1/E3/E6|批内关系区别于组件安全，不主张新的通用组合定理
receiver ephemeral state|接收方临时状态；共享状态|接收方临时状态|A|E2|原协议状态与模型rst标识分开；不复制完整密码结构
unknown key-share; misbinding|UKS；misbinding（notes边界）|未知密钥共享（UKS）；错误绑定（misbinding）|A|E6/notes|本任务仅界限清单；不得把同A的两次接受命名为UKS或错误绑定攻击
implementation; deployment|实现；部署缺陷|实现；部署|A|E3/E6；notes|抽象模型结果不等同部署漏洞或客户端遗漏检查
reachability sanity check|正常路径；非真空性支持|正常路径可达性检查|M|T3；M normal_relaxed_batch_exists|这里只要求准入及后续一次接受，不证明两个不同参与方完成
one-send/two-accepts witness|一个精确来源支持两个同批接受|一个精确发送来源对应两个同批接受事件的可达执行|M|M one_send_two_accepts_exists；E5|唯一匹配Send仅限完整元组；不排除无关发送事件
valid distinct-party batch|有效不同参与方批次|有效的不同参与方批次|M|M distinct_party_batch_exists；E5|两匹配Send和两个接受均存在；有效仅在本抽象中解释
'''
rows=[]
for line in DATA.strip().splitlines():
    en,cur,final,kind,ev,scope=line.split('|')
    rows.append(dict(id=f'T{len(rows)+1:02d}',en=en,current=cur,final=final,kind=kind,evidence=ev,scope=scope))
def hits(r, domain=None):
    needles = [x.strip() for x in re.split('[;；]',r['en']+';'+r['current']) if len(x.strip())>1]
    out=[]
    for f,t in texts.items():
        if domain and not f.startswith(domain): continue
        for n,line in enumerate(t.splitlines(),1):
            if any(re.search(re.escape(x),line,re.I) for x in needles):
                out.append({'file':f,'line':n,'text':line})
    return out
idx={r['id']:hits(r) for r in rows}
(EV/'term-scan-index.json').write_text(json.dumps(idx,ensure_ascii=False,indent=2),encoding='utf-8')
(EV/'term-decisions.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
def table(headers, rr):
    return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(str(x).replace('|','／').replace('\n',' ') for x in r)+' |\n' for r in rr)
def locations(hh,maxn=3):
    return '；'.join(f"`{h['file']}:{h['line']}`" for h in hh[:maxn]) or '审计扩展概念；见语义来源（非声称当前稿逐字出现）'
write('TERM_INVENTORY.md', '# 术语清单\n\n审计日期：2026-10-07。扫描对象为当前中文5份section、4份table、6份notes，英文paper-content、全部section/table，以及三个模型。下表收录'+str(len(rows))+'组概念；近义词合并记录。T=工具概念，A=既有学术概念，M=本文模型或分析性表达。分类说明词的来源，不自动证明某个中文译名已形成共识。\n\n正文实际词形与审计扩展候选严格分开；没有逐字命中的概念仍可来自符号定义或用户要求。全部逐行匹配见 [term-scan-index.json](evidence/term-scan-index.json)，检索是子串定位，不能把命中次数当独立概念计数。模型与段落语义已另行人工核对。\n\n'+table(['编号','English term','当前中文/当前出现状态','类别','扫描位置示例'],[[r['id'],r['en'],r['current'],r['kind'],locations(idx[r['id']])] for r in rows])+'\n## 完整输入清单\n\n'+table(['路径','行数','SHA-256'],[[f,len(t.splitlines()),manifest[f]] for f,t in texts.items()]))
# Evidence claims are deliberately conservative; a model defines meaning, never Chinese consensus.
def evidence_status(r):
    if r['kind']=='M': return ('未建立完整复合词的稳定刊内用法','仅组成词或语义有证据；完整词组 NO_STABLE_CONSENSUS')
    if 'P1' in r['evidence'] or 'P2' in r['evidence'] or 'P3' in r['evidence'] or 'P4' in r['evidence'] or 'P6' in r['evidence'] or 'P7' in r['evidence']:
        return ('有基础词/相近用法；以所列页码为限','按来源对应具体概念；不外推词频或唯一标准')
    return ('P1–P7未建立该完整中文词形共识','官方英文语义/局部中文例证；中文名称 NO_STABLE_CONSENSUS')
er=[]
for r in rows:
    ev=r['evidence'].split('；')
    target, formal=evidence_status(r)
    er.append([r['id']+' '+r['en'],r['current'],r['current']+' / '+r['final'],ev[0], '；'.join(ev[1:]) or 'M（语义核对，不是中文证据）',target,formal,r['scope'],r['final']])
write('TERM_EVIDENCE_MATRIX.md','# 术语证据矩阵\n\n日期：2026-10-07。来源编号、页码口径和证据摘录见 [SOURCE_REGISTER.md](evidence/SOURCE_REGISTER.md)。E与M是项目语义来源，绝不能充当外部中文惯用证据；Tamarin英文手册证明工具语义，不证明中文译名。来源2不足时如实记录，不凑两篇假共识。\n\n**NO_STABLE_CONSENSUS** 表示本次限定样本与正式来源检索没有建立稳定中文对应，不表示全领域不存在该说法。本文仍可依据模型精确定义冻结工作用语。表中“基础词有用法”不等于完整复合译名有共识。中文证据不足的工具译名仍保留英文并列。\n\n'+table(['English term','当前中文','候选中文','来源1','来源2','目标期刊是否使用','形式化验证文献是否使用','语义风险','建议'],er))
# Default first-use and short forms, overridden for high-risk terms below.
special={
'message identity; message coordinate':('消息标识维度（message identity），在条目元组中由消息分量m表示','消息分量','比较不同对象时说消息维度','消息ID字段（模型未定义）；参与方身份'),
'sender occurrence':('发送实例（sender occurrence），指模型中一次SendMessage规则实例化所对应的发送','发送实例','某次发送；涉及事件时写发送事件','发送发生；发送会话；真实session ID'),
'identity coordinate; comparison dimension':('标识维度（identity coordinate），用于区分参与方、发送实例、消息、槽位及批次上下文的比较维度','标识维度','数学公式逐项解释时用分量；参与方投影保留','身份属性（统称所有分量）；几何坐标'),
'occurrence injectivity; scoped occurrence injectivity':('批次上下文内的发送—接受单射对应性（scoped occurrence injectivity），按本文同一(bid,rst)的条件唯一性公式定义','批内单射对应性','在已明确上下文的连续论述中用单射对应性','单射一致性；全局单射性；双射；一一交付'),
'origin correspondence':('精确发送来源对应性（origin correspondence）：每个接受事件都有先前的完整元组匹配Send','来源对应性','发送来源对应性；精确来源对应关系','来源认证；源真实性；身份认证'),
'positive control':('直接施加目标约束的对照模型（positive control），下文称目标对照','目标对照','目标对照模型；直接施加参与方互异约束的对照模型','正控制；修复方案；安全加固协议'),
'relaxed admission':('无互异约束的批次准入模型（relaxed admission）','无互异约束模型','无互异约束配置；表内无互异约束','无约束模型；原始K-Waay模型'),
'message-level restriction; message-level configuration':('消息互异约束的批次准入模型（message-level restriction）','消息互异约束模型','消息互异约束配置；表内消息互异约束','消息级安全协议；全面防重放模型'),
'party-level admission; party-level configuration':('参与方互异约束的批次准入模型（party-level admission）','参与方互异约束模型','参与方互异约束配置；表内参与方互异约束','修复模型；新认证协议'),
'trace; execution trace':('执行轨迹（trace），即由模型执行产生的动作事实序列；理论段下文简称迹','理论：迹；运行叙述：执行轨迹','具体运行；事件序列（仅描述所展示片段）','将符号轨迹称真实抓包记录'),
'all-traces; all traces':('对所有执行轨迹量化的全称性质（all-traces）','表格：全称性；正文：全称性质','理论连续论述：全迹性质','所有真实协议执行均安全'),
'exists-trace':('存在满足指定公式的执行轨迹，即存在性性质（exists-trace）','表格：存在性；正文：存在性性质','本文有目标事件时称可达性性质','存在迹（作为无解释表项）；把验证通过写成所有执行成立'),
'witness':('按对象给出：存在量词的见证值，或满足指定存在性性质的执行轨迹','按语境决定','见CONTEXT_SENSITIVE_TERMS.md','机器见证（无所指）；同一参与方见证'),
'non-vacuity; vacuous truth':('通过有效批次可达性，排除性质仅因没有相关接受事件而成立的情形（non-vacuity）','结果叙述：有效批次可达性；解释：排除空真成立','空真成立须首次解释；理论讨论可保留non-vacuity','非真空性（无解释）；非空性（未指明对象）；所有输入均可完成'),
}
gr=[]
for r in rows:
    first,short,alt,ban=special.get(r['en'],(r['final']+'（'+r['en'].split(';')[0]+'）',r['final'],'在已定义语境中按含义自然转述，不新增安全主张','任何超出右列定义的替换'))
    gr.append([r['id']+' '+r['en'],r['final'],first,short,alt,ban,r['scope']+('；NO_STABLE_CONSENSUS：本文工作命名' if r['kind']=='M' else '')])
write('FROZEN_TERMINOLOGY_GLOSSARY.md','# 冻结术语表 v1\n\n状态：**AROCMAG_TERMINOLOGY_FREEZE_READY**。冻结日期：2026-10-07。权威范围：后续中文稿的术语选择；本轮没有应用到正文。此表优先于旧语言QA中“统一使用发送发生/正控制”的要求，但不改动历史报告。\n\n冻结表示本文用语已作明确决策，不表示所有词都有行业标准。证据矩阵中的NO_STABLE_CONSENSUS一并有效。摘要采用中文短名；英文括注放正文首次定义处。数学符号、事件名、lemma键、引用键、标签和结果状态均不改；首次出现格式是定义模板，后续重写应融入句子，不能把全部英文别名塞进一处。\n\n'+table(['英文术语','最终中文术语','首次出现格式','后续简称','允许替代','禁止表达','语境说明'],gr)+'\n## 优先执行规则\n\n1. 注入性统一按数学用语改为单射性，但Lowe的injective agreement单独叫单射一致性。\n2. “批内”在性质段先定义为同一(bid,rst)；不能省略接收方上下文而加强结论。\n3. 标识维度是分析视角，三元组分量是数学结构；槽位及上下文不增补进E的三元组。\n4. 新鲜发送实例标识与事件时间点不同。Send事件、!Sent持久事实、In网络输入和ReceiverAccept接受事件严格区分。\n5. 规则或restriction施加约束；lemma验证执行是否满足性质。表述不能互换。\n6. 本表不授权全文重写、改变研究问题、增添模型机制或新增证明。\n')
print(json.dumps({'terms':len(rows),'input_files':len(texts),'protected_files':len(manifest)},ensure_ascii=False))
