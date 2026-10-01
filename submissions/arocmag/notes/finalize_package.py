from pathlib import Path
import csv,json,re,hashlib,datetime

ROOT=Path(__file__).resolve().parents[1]
records=json.loads((ROOT/'notes/source_records.json').read_text('utf-8'))
byid={r['source_id']:r for r in records}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s): (ROOT/p).write_text(s,encoding='utf-8')
dates={'P01':'2024-06-26','P02':'2024-06-26','P04':'2022-07-24','P05':'2022-08-19','P07':'2026-08-04','P08':'2022-07-24','P09':'2024-10-09','P10':'2022-08-19','P11':'2022-07-24','P14':'2024-06-19','P17':'2024-06-26','P18':'2024-06-19','F01':'2023-10-13 16:41:40','F02':'2023-10-13 16:47:27','F03':'2023-10-13 16:45:05','F04':'2024-05-17 16:57:32','F05':'2023-10-13 16:38:02'}
summaries={
'P01':'系统投稿；Word优先/PDF可用；不收常规email和打印稿；不新增作者；审稿1-2个月/100天；录用后版面费；CCF第一作者85折；优先数字出版。正文部分旧.com链接不沿用。',
'P02':'MathType；OMML转换；尽量矢量EMF并嵌入到文字；编辑部会重排。旧go下载链接仅保留证据，原文件从.cn下载页获取。',
'P03':'5种官方附件及各自更新时间；月刊版权全体同意和单位盖章保密材料。列表本身无单一更新时间。',
'P04':'中文200-300字、第三人称、自含性；英文过去时/结论现在时；EI一般150词建议。与F01中文摘要长度不一致。',
'P05':'不刊登英文稿；系统投稿；送审不更新；旧邮箱/审稿费口径/邮寄发票描述与较新页不同。',
'P06':'期刊身份、作者登录、投稿必读（指向P01）、防假冒提示、.cn域名/邮箱；明确四川省科技厅主管。无整页更新时间，新闻日期不是页面更新时间。',
'P07':'最新处理流程：初审10工作日、外审1个月、终审1-2周；缴费修稿、电子发票、优先出版、PDF校对。',
'P08':'TP分类目录，只记录规则，未选当前论文分类号。',
'P09':'主办单位、ISSN/CN、办刊范围、唯一业务域名.cn和邮箱.cn。',
'P10':'旧版版权协议说明、扫描发送步骤；旧.com邮箱及增加作者措辞与较新材料不一致。直链F06与F04同哈希。',
'P11':'禁止新增作者、全部原作者签名、第一作者身份证；旧附件直链404，最新版从P03取得F05。',
'P12':'PDF清样修改批注方法，页面示例不作为独立模板。',
'P13':'投稿要求栏目入口，与P01-P12交叉核对。',
'P14':'四类优先采用文稿；综述/算法/软件方向；基金准确名称和编号。不是页数规则。',
'P15':'2026年7期正式目录，信息安全技术栏目。刊期不是页面更新时间。',
'P16':'2025年4期正式目录，信息安全技术栏目。刊期不是页面更新时间。',
'P17':'旧防假冒声明仍含arocmag.com和joural拼写；与较新P09及现首页不一致，不沿用。',
'P18':'学术不端处理公告；只作投稿政策背景，不作法律解释。',
'P19':'实际GET打开.cn登录入口；没有登录、注册或提交表单。',
'F01':'官网原件；3页；只读打开；2个MathType对象；首页基金作者页脚；摘要200字以内；原件SAVEDATE缓存2021/07/27。',
'F02':'22页，正文版本ver2.2.4，2018/04/02；完整文本已读取；本刊参考GB/T7714-2005。',
'F03':'6页，正文版本ver2.2.4 lite，2018/04/02；完整文本已读取；细则以F02为准。',
'F04':'实际后缀.dotx；保密证明单位盖章、版权全体作者签字；已打开检查。',
'F05':'原件.doc已打开检查；禁止新增作者、原作者签名、第一作者身份证。',
'F06':'P10所链旧路径下载的原始.dotx；字节与F04完全一致，属于同一内容别名，不是第6种独立材料。'}
for sid in ['P12','P13']:
 t=(ROOT/f'snapshots/{sid}.txt').read_text('utf-8').split('LINKS')[0]
 candidates=re.findall(r'^20\d\d-\d\d-\d\d$',t,re.M)
 if candidates: dates[sid]=candidates[0]
pub={
'A01':('2025-04-05','2025,42(4):1230-1238','随机预言模型+ProVerif；PUF多网关身份认证'),
'A02':('2025-10-05','2025,42(10):3152-3158','ROR Oracle+Proverif；医疗传感器匿名认证'),
'A03':('2026-02-05','2026,43(2):588-595','四方雾计算认证；ECC/PUF；摘要未声明符号工具'),
'A04':('2026-07-05','2026,43(7):2164-2172','RLWE多因素AKE；ROR形式化分析'),
'A05':('2025-01-05','2025,42(1):282-287','ID-BJM模型/RLWE；后量子身份认证'),
'A06':('2026-02-05','2026,43(2):577-587','UML结构映射和Coq一致性证明'),
'A07':('2023-10-05','2023,40(10):3132-3137,3143','Tamarin/MQTT3.1.1；历史方法证据，不计近两年'),
'A08':('2023-04-05','2023,40(4):1189-1193,1202','协议代码辅助建模/Tamarin；历史方法证据，不计近两年')}
for sid,(d,issue,s) in pub.items(): summaries[sid]=f'已打开摘要；正式出版日期={d}；{issue}；信息安全技术；{s}；发布历史不冒充页面更新时间。'
attachments={'P02':['F01'],'P03':['F04','F05','F01','F03','F02'],'P10':['F06'],'P11':['F05']}
cols=['source_id','title','official_url','page_updated_date','accessed_date','source_type','download_filename','local_path','sha256','has_download_attachment','attachment_names','download_urls','attachment_local_paths','text_snapshot','notes']
with (ROOT/'notes/SOURCE_MANIFEST.tsv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols,delimiter='\t'); w.writeheader()
 for r in records:
  sid=r['source_id']; children=[byid[x] for x in attachments.get(sid,[])]
  other=[a for a in r['links'] if ('/UpFile/' in a['url'] or 'go.arocmag.' in a['url'])]
  note=summaries[sid]
  if other: note+=' 原页其他/旧附件链接='+json.dumps(other,ensure_ascii=False,separators=(',',':'))
  w.writerow({k:v for k,v in dict(source_id=sid,title=r['title'],official_url=r['official_url'],page_updated_date=dates.get(sid,'NOT OFFICIALLY SPECIFIED'),accessed_date=r['accessed_date'],source_type=('official_article_abstract' if sid.startswith('A') else r['source_type']),download_filename=r['download_filename'],local_path=r['local_path'],sha256=r['sha256'],has_download_attachment=('YES' if children or other else ('ARTICLE_FULLTEXT_NOT_REQUESTED' if sid.startswith('A') else 'NO_SUBMISSION_ATTACHMENT_FOUND')),attachment_names=' | '.join(x['download_filename'] for x in children),download_urls=' | '.join(x['official_url'] for x in children),attachment_local_paths=' | '.join(x['local_path'] for x in children),text_snapshot=f'snapshots/{sid}.txt' if r['source_type']=='page' else '',notes=note).items() if k in cols})
 # Failure is a separate row: no claimed downloaded body/hash.
 w.writerow(dict(source_id='F07-BLOCKED',title='P11旧作者变更表直链',official_url='https://www.arocmag.cn/UpFile/201405/计算机应用研究题目及作者变更申请书.doc',page_updated_date='NOT OFFICIALLY SPECIFIED',accessed_date='2026-10-01',source_type='download_attempt_failed',download_filename='计算机应用研究题目及作者变更申请书.doc',notes='HTTP404；无附件本地实体；同用途原文件F05已从官方常用下载页成功获取。'))

audit=ROOT/'notes/TEMPLATE_AUDIT.md'
txt=audit.read_text('utf-8')
txt=txt.split('\n<!-- GENERATED HASH -->')[0]
txt+='\n<!-- GENERATED HASH -->\n\nF01 SHA-256：`'+byid['F01']['sha256']+'`。\n'
audit.write_text(txt,encoding='utf-8')

source_lines=[]
for r in records:
 if r['source_type']=='page':
  sid=r['source_id']; source_lines.append(f"- {sid} [{r['title']}]({r['official_url']})；页面更新时间：{dates.get(sid,'NOT OFFICIALLY SPECIFIED')}；[本地文本](../snapshots/{sid}.txt)。")
file_rows=[]
for r in records:
 if r['source_id'].startswith('F'):
  file_rows.append(f"| {r['source_id']} {r['download_filename']} | [官网原文件]({r['official_url']}) | [{r['local_path']}](../{r['local_path']}) | `{r['sha256']}` |")

report='''# 《计算机应用研究》投稿资料获取报告

## Overall Status

**AROCMAG_REQUIREMENTS_READY**

阶段：`OFFICIAL_REQUIREMENTS_ACQUISITION`。访问与整理日期：2026-10-01（Asia/Shanghai）。已完成官方资料获取、实际模板审查、17项规则归纳、当前稿件差异分析和栏目适配调查。“READY”仅表示资料包足以供后续改写规划使用，不代表论文已适配、已投稿或所有规则歧义已由编辑部澄清。

唯一权威来源为 `arocmag.cn`。保存27个官方页面的HTML及可追踪文本；下载5种独立官方文件，另保留1份同内容旧链接副本，共6个原始文件。所有原始下载均有SHA-256。没有从第三方取得模板或补充规则。

## Official Sources

'''+ '\n'.join(source_lines)+'''

下载URL、页面日期、附件名称、原格式、路径、散列、主要要求及旧链接均见 [SOURCE_MANIFEST.tsv](SOURCE_MANIFEST.tsv)；原始HTTP元信息在 `source_records.json`。页面上的论文出版日期与页面更新时间分开记录。

## Downloaded Files

| 原文件名 | 来源 | 本地路径 | SHA-256 |
|---|---|---|---|
'''+ '\n'.join(file_rows)+'''

F06 与 F04 SHA-256 相同，属于同一 `.dotx` 文件的两个官网入口，不计为两种独立资料。P11旧作者变更表附件链接返回404，但 F05 已从有效官方下载入口获得、打开，因此该旧链失效不阻塞本阶段。

## Key Requirements

1. 使用 `.cn` 官网系统投稿；不收常规email/纸质投稿，不能从旧页面的 `.com` 跳转推定当前入口。
2. FAQ明确暂不刊登英文稿件，当前英文主稿需要中文改写。
3. 推荐Word `.doc/.docx`，PDF可初投；录用编辑退修必须Word。
4. 投稿成功后不接受作者直接替换稿件；送审期需更新时按终止旧稿/重新投稿规则。
5. 投稿署名应一次确定，不允许新增作者；删除/调序需原作者签字及身份证明等手续。
6. 至少留一名作者手机号；通信作者写邮箱，没有通信作者时写第一作者邮箱。
7. 中英文摘要对应、客观第三人称，涵盖目的/方法/结果/结论。
8. 中文摘要专页建议200～300字，模板建议200字以内，口径未统一；英文150词是网页引用的EI建议，未确认为本刊硬限。
9. 模板建议3～8个关键词，中英文对应；英文一般小写，专名/缩写例外。
10. 网页要求MathType；OMML需按说明转换，公式不能用图片替代。
11. 尽量采用矢量图、Word增强型图元文件、嵌入到文字。
12. 正式出版正文双栏；初投稿可通栏。模板图表双语题注、三线表式为实际示例，部分说明待补充。
13. 本刊参考文献规则参考GB/T 7714—2005；按首次引用顺序编码，不以其他年份国标或现有BibTeX样式自动替代。
14. 参考文献超过3位作者只列前三位加等/et al；中文文献补对应英文信息；引文不要用尾注/书签/域代码承载。
15. 基金写准确名称和编号；基金与作者简介在模板首页页脚，不要转换时漏掉。
16. 月刊录用后需全体作者签署版权承诺、单位盖章保密证明；多单位盖章范围及精确截止日期未公布。
17. 整体审稿通常1～2个月，投稿100天未获处理意见可自行处理；最新流程另给初审约10工作日、外审约1个月、终审约1～2周。
18. 不预收审稿费，录用后收版面费；公开具体价格为 `PRICE NOT PUBLICLY SPECIFIED`；第一作者CCF会员在投稿注明会员号可享8.5折。
19. 月刊有官网/知网优先数字出版；不同意知网预先发表须投稿时声明；最新流程是电子发票、正式出版前约1个月PDF清样校对。
20. 未发现总页数/字数/最大篇幅数值限制；不能将模板3页、其他论文页数或FormaliSE要求当成本刊上限。

逐项证据、适用层次和冲突见 [SUBMISSION_REQUIREMENTS.md](SUBMISSION_REQUIREMENTS.md)。

## Template Status

**DOWNLOADED_AND_AUDITED**

官方 `.doc` 已以WPS COM只读方式打开，实际检查正文、样式、全部3页预览、三节单/双栏、页眉页脚、书签、域、公式OLE对象。确认2个Equation.DSMT4对象、1幅EMF图、首页基金/作者简介页脚。原件未保存修改。

额外DOCX/PDF/PNG仅为本次检查证据，置于snapshots，不作为官方原件。WPS转换件展开了原件SAVEDATE域，因此审计以原件COM记录为准。没有Microsoft Word或MathType编辑兼容性测试；这不影响原件已成功打开和结构已审查的事实。

## Current Manuscript Gap

主稿为英文、匿名、11pt article多文件LaTeX。最大差异是中文研究论述重构，以及Word/MathType/矢量图转换；还需双语元数据、经作者确认的署名/单位/基金、期刊格式引文。

已核实主稿用 `bibliographystyle{plain}`，不是IEEE/ACM专用样式；现有22条文献需要逐项转换。对RFC、ePrint、在线协议规范保留编号及版本，具体类型标志待确认。附录不能因尚未公布的页数上限直接删除。

模型、性质、历史执行记录及“非完整精化证明/非部署漏洞”的边界应保留；长复现清单只有在确认补充材料政策后才考虑移出正文。本次未执行任何改写、翻译、模型修改或证明运行。

## Scope Fit

**STRONG**，建议“信息安全技术 / 安全协议形式化分析”。已阅读并归档6篇2025—2026正式发表相邻论文的官网摘要，覆盖ProVerif认证分析、RLWE后量子密钥交换、多方认证及Coq证明；另外2篇2023年Tamarin论文仅作历史方法先例，不计入近两年证据。

这是主题与栏目的适配判断，不是录用概率。6篇的题名、出版日期、卷期页码、摘要方法及与本项目的差别，均在需求报告的Scope Fit表中。栏目最终由责任编辑确定。

## Open Questions

以下均为官网未明确说明或没有统一答复的事项；未向编辑部发邮件：

- 全文字数/页数上限，是否分研究论文/综述/短文，以及超页处理：`NOT OFFICIALLY SPECIFIED`。
- 中文摘要采用200字以内还是200～300字；英文150词是否为本刊硬性要求：未统一明确。
- 版面费具体金额和每页单价：`PRICE NOT PUBLICLY SPECIFIED`；其他减免及优先数字出版独立收费规则未公布。
- 图像DPI、彩色/黑白、位图格式清单、图内文字统一规范、三线表和双语题注的强制程度、表格单位摆放：`NOT OFFICIALLY SPECIFIED`。
- 全面数学正斜体规范、MathType以外最终可编辑公式格式的明确豁免：`NOT OFFICIALLY SPECIFIED`。
- RFC、IACR ePrint和协议网页规范的专门著录类别；机构上下级次序在官方参考文献材料中有不同说法。
- ORCID、独立匿名评审稿要求、作者字段后台必填细项：公开资料没有明确特殊规定。
- 版权/保密材料提交的精确截止日、与缴费的强制先后、多单位各自盖章范围；旧页邮箱尚未统一到.cn。
- 附录、补充材料、代码/数据artifact托管与审查要求，以及录用到刊出的固定等待时间：`NOT OFFICIALLY SPECIFIED`。

## Recommended Next Stage

`AROCMAG_MANUSCRIPT_ADAPTATION`。

本阶段到此结束，**未启动下一阶段**。后续另行授权后，在独立期刊目录规划中文改写和格式转换；先解决影响制稿的摘要口径、篇幅/附录和特殊文献类型问题。

## Verification

保护范围：manuscript/、tamarin/、docs/、artifact/、reviews/、results/、archive/、submissions/formalise2027/。开始时为clean工作树，新增资料均在submissions/arocmag/内。

交付前散列对比和Git边界核查见 `BOUNDARY_VERIFICATION.json`。本阶段未commit、push、注册账号、上传稿件、发邮件或付款。
'''
write('notes/AROCMAG_SETUP_REPORT.md',report)
write('README.md','''# 《计算机应用研究》官方投稿资料

当前项目目标期刊：《计算机应用研究》（Application Research of Computers）。本目录仅完成 `OFFICIAL_REQUIREMENTS_ACQUISITION`，状态 `AROCMAG_REQUIREMENTS_READY`。访问日期：2026-10-01。

- [获取报告与结论](notes/AROCMAG_SETUP_REPORT.md)
- [17项投稿规则、Scope Fit和主稿差异](notes/SUBMISSION_REQUIREMENTS.md)
- [实际Word模板审查](notes/TEMPLATE_AUDIT.md)
- [官方来源与下载清单](notes/SOURCE_MANIFEST.tsv)

`official/templates/`存官网原始.doc模板；`official/guidelines/`存两份参考文献PDF；`official/forms/`存版权/保密.dotx及作者变更.doc。保密表另有同哈希旧链接副本，五种内容共六个文件。所有格式和原始字节保留。

`snapshots/`存27个官网页面HTML与文本、附件文本、原件COM检查记录，以及仅供检查的DOCX/PDF/PNG派生文件。派生文件不是官方模板，不应用作稿件底稿。来源和日期以清单为准，HTML离线快照未打包远端CSS/图片，配套文本可独立阅读。

`notes/`保存调查结果、获取脚本、原始HTTP/来源记录及保护目录散列证据。重要歧义：中文摘要200以内/200～300冲突，旧.com地址与新.cn政策差异，篇幅/具体费用未公开。READY不表示这些歧义已解决，也不表示现稿可直接投稿。

FormaliSE副本仍在 `../formalise2027/`；本次未修改manuscript/、Tamarin、证据或历史提交版本。未注册、投稿、上传、付款、发邮件、commit或push。下一阶段名称为 `AROCMAG_MANUSCRIPT_ADAPTATION`，尚未执行。
''')

print('Wrote manifest, setup report, README; original files:',len([r for r in records if r['source_id'].startswith('F')]))
