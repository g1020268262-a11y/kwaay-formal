# Stage 6 研究贡献恢复与证据展示验收报告

任务：`AROCMAG_STAGE6_CONTRIBUTION_RESTORATION`

基线：`main`，`c0fa835b2b0da2e1cbc258bfc64bfa735c27ec20`。开始时工作区干净。修订和验收日期：2026-10-10至2026-10-11（Asia/Shanghai，跨午夜完成报告）。没有commit、push、投稿或新的Tamarin运行（包括parse-only）。

最终判定：**CONTRIBUTION_RESTORATION_COMPLETE**。

该判定表示本轮贡献保真审计、四项证据增强、独立Word/LaTeX交付及现有环境验收完成，**不表示已满足正式投稿的全部外部条件**。

## A. 原稿与终稿对比

先建立了[修订前贡献映射审计](STAGE6_CONTRIBUTION_RESTORATION_AUDIT.md)，然后修改正文。审计逐章比较最初Markdown底稿、英文母稿和当前中文稿，区分完整保留、合并保留、解释不足、有证据内容被删去及合理移除的推测。没有因旧稿篇幅较长而认定所有删减都不当。

主要发现与处理：

| 内容 | Stage 5现状 | Stage 6处理 | 论证功能 |
|---|---|---|---|
| 原协议→抽象映射 | 有输入向量与模型内部坐标表，但取舍较隐含 | 新表2及§1.1/1.2解释 | 使K-Waay接口、参与方关联、共享状态、分量输出与模型的关系可核查 |
| 三模型的设计控制 | 生命周期和图1已完整，资源选择理由较分散 | §2.2增加一段 | 解释持久来源与线性槽位、精确匹配及七条共同规则如何控制比较 |
| M模型关键见证 | 存在性结论主要为文字 | §3.2新增一个事件公式和投影说明 | 展示两个不同来源、共同批次、两次接受及必要时间偏序 |
| 完整14项结果 | 7项主表，其余概述，未填补充地址 | 保留7项主表为表5，新增完整表6 | 读者无需外部链接即可看到全部lemma、量词、状态、步数及作用 |
| 相关工作定位 | 引言一句压缩罗列 | 恢复3段有对象区别的比较 | 区分密钥/会话、会话组合、名称/认证单射与批次投影 |
| 历史复现来源声明 | 英文旧附录仍称缺少原始图/仅既有记录 | 使用2026-09-16独立复核事实 | 不把过时表述恢复到中文稿，也不冒称恢复历史日志 |

没有恢复HMAC攻击、KEY/TEST失败、密钥泄露、Double Ratchet失败、C_install-v2安装后果或部署漏洞等缺少当前R/M/P直接证据的主张。没有恢复冗长的外围MLS或误绑定综述；保留必要的分析对象区别即可。

官方[投稿须知](https://www.arocmag.cn/info/instruction/instructions)与[模板说明](https://www.arocmag.cn/info/instruction/template)的公开页面未规定本文必须6页或固定章节数。因此允许自然增页，但没有通过重复论述扩篇。

## B. 研究贡献与证据映射

| 正式贡献中的内容 | 直接依据 | 新稿位置与边界 |
|---|---|---|
| 条件提取及协议联系 | K-Waay full version物理/印刷第15页§4.1、第16页§4.2.1、第21页§5.1及图10；SOURCE_TO_MODEL_AUDIT | §1.1、§1.2、表2；原协议已经要求不同参与方；本表为研究者抽象而非精化定理 |
| 受控三模型 | CreateParty、SendMessage、CreateBatch、CollectSlot1/2、ProcessSlot1/2七条共同规则；独立common-rules-comparison | §2.2/2.3；持久!Sent与线性处理分工明确，准入为受控变化 |
| R的重复接受形状 | one_send_two_accepts_exists verified 13；receiver_accept_injective falsified 13；receiver_accept_has_send verified 8 | §3.1、原公式(3)、原图2；仅抽象接受，不是真实密钥安装 |
| M的非替代性 | same_party_different_messages_batch_exists verified 16；accepted_batch_has_distinct_messages verified 31；receiver_accept_has_send verified 8；receiver_accept_injective verified 33 | §3.2事件结构及表5/6；机器支持M不能推出P，M/I并非两项独立累积保证 |
| P的正控制与有效路径 | accepted_batch_has_distinct_parties verified 31；distinct_party_batch_exists verified 17 | §3.3；全称目标成立且不同参与方的两次接受可达，不依赖拒绝所有批次 |
| 支持性质及独立复核 | 14行result-comparison、三份prove stdout、7个trace图、独立manifest | §3.4及表6；6项exists-trace、8项all-traces；13 verified、1 falsified；步数不表示性能 |

核心依赖关系没有变化：`Pτ⇒Mτ⇔Iτ`仍是当前新鲜消息和精确来源规则下的**人工迹语义推导**；`Mτ⇏Pτ`由现有机器可达见证支持。完整表中的结果不是14项独立创新，也没有把来源对应性提升为完整密码学认证。

M见证与独立JSON逐项核对：`#s1/#s2`是同一`~a`的`(~sid,~m)`和`(~sid.1,~m.1)`发送；`#b`为AdmitDistinctMessages；`#r1/#r2`分别为ProcessSlot1/2，并各读自己的持久!Sent。后者产生BatchComplete。图中`#vr.4`还有不同oid和m的额外发送。新增公式只表达`s1<b`、`s2<b`、`b<r1<r2`，没有添加`s1<s2`或`s2<s1`。这是一份依据机器证据整理的关键结构，不是原始trace图，也没有声称整条执行只包含两次Send。

## C. 实际修改与独立交付

### 论文修改

| 文件 | 修改前→修改后及理由 |
|---|---|
| `latex-v2/sections/01-introduction.tex` | 一段概括相关工作→三段比较；贡献1补映射，贡献2补14项及复核证据；仍为3项贡献 |
| `latex-v2/sections/02-problem.tex` | 输入/坐标说明→增加原协议分量向量动机和映射前提；不改RQ |
| `latex-v2/sections/03-formal-modeling.tex` | 流程描述→补充持久/线性资源及七条共同规则的比较意义 |
| `latex-v2/sections/04-formal-analysis.tex` | M文字见证→事件公式与解释；其余7项概述→完整14项表及复核来源；删去未落实的匿名artifact URL注释 |
| `latex-v2/tables/source-to-abstraction.tex` | 新增6行映射表，区别于模型内部身份坐标表 |
| `latex-v2/tables/full-verification-results.tex` | 新增14行证据清单；结果按独立stdout核对 |
| `latex-v2/main.pdf` | 当前多文件工程重新编译的12页PDF |

摘要、Discussion、Conclusion源码、原有四张表、两个冻结图源、原有6个展示公式、RQ文本及参考文献数据库均未修改。表号自然顺延，未改章节结构。

### 交付文件

- Word：`word-final/K-Waay-AROCMAG-submission-stage6.docx`
- WPS实际导出PDF：`word-final/K-Waay-AROCMAG-submission-stage6-preview.pdf`
- 独立LaTeX源码及同内容PDF：`latex-stage6/`（21个构建输入，`SOURCE_MANIFEST.json`绑定哈希）
- 源码压缩包：`K-Waay-AROCMAG-stage6-latex-source.zip`
- 贡献审计：本目录`STAGE6_CONTRIBUTION_RESTORATION_AUDIT.md`
- 本报告：`STAGE6_CONTRIBUTION_RESTORATION_REPORT.md`

Stage 5目录和工作稿全部保留。Stage 6 DOCX在Stage 5包上保留23个未修改部件，最终仅正文XML和核心描述元数据变化；复用112个未变正文块，样式、编号、页眉页脚、设置、关系及媒体按字节保留。新增内容沿用既有排版，未引入新图。

### 构建及检查材料

新增`word-final/source/build_word_stage6.py`、`export_stage6_with_wps.ps1`、`audit_stage6.py`、`stage6-evidence-tables.py/.json`、`citation-order-stage6.json`，以及`formulas/formulas-stage6.json`。表格数据生成器只读模型和复核文件，不调用证明器。

`word-final/qa/stage6/`包含基线哈希、修订前章节快照、逐段覆盖记录、14项证据绑定、构建清单、公式清单、实际WPS导出记录、LaTeX编译日志、全文差异、全部页面图及视觉验收记录。脚本存在不等于验收完成；本轮实际运行结果见以下章节。

## D. 篇幅与实际版面

| 项目 | Stage 5 | Stage 6 |
|---|---:|---:|
| Word实际PDF总页数（含首页/参考文献） | 6 | 7 |
| LaTeX总页数（含首页/参考文献） | 11 | 12 |
| Word科学正文所占页面（正文起至结论止） | 1–6 | 1–7 |
| LaTeX科学正文所占页面 | 1–11 | 1–12 |
| 表格 | 4 | 6 |
| 图 | 2 | 2 |
| 编号展示公式 | 3 | 3 |
| 未编号展示公式 | 3 | 4 |
| Word OMML对象（含行内/分行公式） | 99 | 110 |
| 参考文献 | 8 | 8 |
| 一级章节/二级标题 | 6 / 13 | 6 / 13 |

页数仅记录排版结果，不作为质量或期刊合规指标。新表2承担抽象取舍核查，新表6承担完整证据索引，新增公式承担M见证结构呈现；三者没有用重复段落填充版面。

实际渲染采用本机**WPS Writer（KWPS.Application）**，只读打开DOCX、重新分页、导出PDF，再逐页渲染检查。COM版本字符串为12.0；不是Microsoft Word。标准`render_docx.py`已尝试，但因缺少LibreOffice `soffice.exe`失败，没有将失败的标准流程当作渲染完成。

视觉检查覆盖Word全部7页及LaTeX全部12页：

- Word第1页英文摘要保留左对齐，无新增异常拉伸；标题与中英文摘要完整。
- 第2页表1/2区分内部坐标与协议映射，四列内容无裁切；第3页图1及准入表正常。
- 第4页原性质表、公式与图2保持清晰；两条来源虚线、事件及图注可读。
- 第5页新增M公式七行完整，两个发送没有人为先后关系；关键7项结果仍为主表。
- 第6页完整14项结果在同页显示，lemma、量词、状态和步数可读。初次渲染曾在页尾拆表，已修复为表6从第6页开始。
- 第7页结论余文及8条参考文献完整；在第4条前自然换栏，左右基本平衡，保留篇幅决定的下部留白，没有拉大字距填页。
- LaTeX第4页映射表、第9页M结构、第10页两张结果表完整；图2在第8页独立浮动页。没有裁切或缺字；独立图页的留白未通过改图或删文消除。

LaTeX实际命令：`latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex`。结果：undefined references=0，undefined citations=0，missing glyphs=0，overfull boxes=0。保留1条underfull hbox提示（第3.3节含长lemma的段落）；页面已检查，未溢出或丢字。

按编辑器要求也调用了内置编译器，但其单文件环境无法找到`preamble/packages.tex`，返回失败。此限制与本地多文件XeLaTeX成功编译分开记录；没有虚报内置预览编译成功。

## E. 科学与产物一致性

实际检查结果见`word-final/qa/stage6/content-audit.json`：

- 14行Word结果表全部与独立prove stdout的lemma、量词、状态、步数一致；合计13 verified、1 falsified。
- 86段正文/标题/条目的中文序列逐段覆盖；另对新增公式完整符号串、RQ全文、参考文献全文和表格逐项检查。中文序列覆盖只是自动漏项检查，不代替语义审查；第B节记录了新内容与证据的实际核对。
- 原有6个展示公式和4个Word表格逐字节保留；新增M公式逐式核对两个Send、两个ReceiverAccept、共同bid/rst、不等式及偏序。
- 8条Word参考文献全文及顺序未变，仍对应既有8个引用键；没有新增或臆造出版事实。
- 摘要、Discussion、Conclusion和RQ文本未变；P⇒M⇔I仍是人工规则推导，M⇏P仍来自机器见证。
- 200个受保护文件SHA-256未变，覆盖Tamarin、原始复核证据、英文母稿、研究底稿、官方模板、style-study、Stage5包及冻结图源等。
- 独立`latex-stage6`每个构建输入与当前`latex-v2`对应文件一致；PDF逐字节相同。Word的新表、见证和四处增强均同步。
- `git diff --check`通过；实际变更范围为本轮论文呈现及交付/QA材料，没有模型、证明、图源或Stage5变更。

## F. 仍需外部处理

1. Word仍使用110个可编辑OMML，不是真正MathType对象。新的逐式清单为`word-final/qa/stage6/FORMULA_CHECKLIST_STAGE6.csv`；后续转换需覆盖本轮新增对象，不能只用Stage5的99项清单。状态仍为`MATHTYPE_CONVERSION_BLOCKED`。
2. 当前环境只有WPS实际渲染，尚未完成Microsoft Word终检。作者应在目标Word环境打开Stage6文件，并在MathType转换后重新导出检查。
3. 真实作者、单位、基金及通信信息仍缺失，保留原占位。作者应私下填写，不向公开仓库提交敏感信息。
4. 初投稿署名/匿名规则和系统生成PDF仍需作者登录投稿系统确认。本轮不自动投稿。
5. 图1/2继续使用已验收的360dpi PNG；冻结TikZ/PDF矢量源保留。没有EMF转换成果，亦未将“尽可能使用矢量图”的建议升级为科学交付阻塞。

没有发现阻止本轮贡献恢复交付的科学冲突。上述事项属于正式投稿的外部条件，不应因此虚报`READY_FOR_SUBMISSION`。

辅助文件清理说明：自动审批策略拦截了清理本轮生成的LaTeX辅助文件和Python缓存目录的操作，仅返回`blocked by policy`，未提供更具体原因。因此保留这些本地缓存，不再尝试删除；它们没有收入独立LaTeX源码压缩包，不影响论文交付。没有要求用户为此确认或改变科学交付状态。

## G. 十项验收回答与最终判定

| 验收问题 | 结论 | 实际证据 |
|---|---|---|
| 1. 是否更充分展示工作？ | 是 | 表2、表6、M事件公式与七条共同规则说明，分别展示映射、验证清单和设计控制 |
| 2. 英文核心论证是否保留？ | 是，在当前证据及已修正语义范围内 | 原稿到中文逐章审计；R/M/P、来源关系、正控制、边界均保留；不恢复旧M/I独立性表述 |
| 3. 是否恢复有证据的弱化内容？ | 是 | 原协议§4.1/4.2.1/5.1映射；独立14行输出；M的Send/Accept结构 |
| 4. 是否增加不必要重复？ | 未发现新增无功能重复 | 主表保留7项摘要，完整表是精确证据索引；新映射表与旧坐标表对象不同；未恢复全部相关工作小节 |
| 5. K-Waay特定性是否提高？ | 是 | 解释输入公钥/预密钥、接收共享状态、参与方索引和分量输出，而非只介绍抽象变量 |
| 6. 结果是否更可核查？ | 是 | 正文直接列14项精确lemma、类型、状态、步数和作用；无虚构artifact链接 |
| 7. 是否展示见证非平凡性？ | 是 | §3.2同参与方不同来源经过收集、准入、顺序处理并产生两次接受；未人为排序Send |
| 8. 与已有工作区别是否清楚？ | 是 | 引言分别比较Signal/PQXDH密钥会话、Cremers会话组合、Lupetti名称及Lowe单射一致性 |
| 9. 是否有未经证明的更强主张？ | 本轮未引入 | 新表明确理想来源、正确投影假设和非精化；§4.3/结论原样保留；模型和证据不变 |
| 10. 是否人为改变范围？ | 否 | 仍为固定两槽机器范围，概念定义适用于有限批次；不以6页限制研究，也不新增攻击/实验/安全游戏 |

**CONTRIBUTION_RESTORATION_COMPLETE**

本轮到此停止，不进入新实验、下一轮全文润色或正式投稿阶段。
