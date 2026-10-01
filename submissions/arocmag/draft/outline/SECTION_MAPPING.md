# 英文母稿到中文稿的章节映射

标签含义：`KEEP` 保留研究事实；`MERGE` 与其他部分合并；`REWRITE` 按中文论证重写；`SHORTEN` 压缩；`MOVE_TO_APPENDIX` 仅保留在附录/补充材料；`NEEDS_CONFIRMATION` 需作者或期刊进一步确认。

一个来源可以同时带多个标签，例如 `KEEP + REWRITE + SHORTEN` 表示保留其事实，但不保留原段落组织和长度。

## 1. 总映射

| 英文母稿位置 | 操作 | 中文新位置 | 具体处理与核对点 |
|---|---|---|---|
| Abstract | `KEEP` `REWRITE` `SHORTEN` | 中英文摘要 | 保留 R/M/P、固定两槽、直接证据止于 `ReceiverAccept`；删除“没有独立重跑/没有 raw transcript”的旧状态，改用 2026-09-16 独立复核事实；不逐句翻译。 |
| Introduction | `KEEP` `MERGE` `REWRITE` `SHORTEN` | 0 引言 | 合并 K-Waay 接口动机、问题、方法、窄贡献与边界；删除英文稿的 paper roadmap；将三条相似贡献压成“受控比较 + non-substitutability + 有限设计启示”。 |
| Section 2, K-Waay BatchReceive and the Identity Problem | `KEEP` `MERGE` `REWRITE` | 1.1、1.2、1.3；少量进入 0 引言 | 保留 source condition、输入向量、identity coordinates、`E_i=(A_i,oid_i,m_i)`、same-party/different-message 例子；把三个原 RQ 合并为两个；将 model-local `sid` 在叙述层改称 `oid` 并声明源模型仍用 `sid`。 |
| Section 3, Security Objective and Threat Model | `KEEP` `MERGE` `REWRITE` `SHORTEN` | 1.2、1.3、2.2、4.3 | 保留任意有限批的语义定义、固定两槽的机器范围、batch-composition adversary、exact duplicate 与 same-party/different-tuple 区分、`ReceiverAccept` 终点；删除多处重复边界。 |
| Section 4, Formal Modeling | `KEEP` `MERGE` `REWRITE` `SHORTEN` | 第 2 章 | source-to-abstraction mapping 必须显著保留；合并共同生命周期、R/M/P admission、事件/性质；正文只给关键公式，不复制全部 lemma；明确 `!Sent` 理想 origin 不是完整 authentication。 |
| Section 5, Formal Analysis | `KEEP` `REWRITE` `SHORTEN` | 第 3 章 | 保留核心结果和 steps；R/M/P 各一节，最后给规则推导 `P_tau => M_tau <=> I_tau` 和 `M_tau !=> P_tau`；弱 rejection lemma 只作为 branch reachability。 |
| Section 6, Discussion and Design Implications | `KEEP` `MERGE` `REWRITE` `SHORTEN` | 第 4 章；一小部分进入 5 结束语 | 将 identity distinction、deduplication、authentication、enforcement 的重复解释合并；保留“composition relation 与 per-entry origin 不同”；把 limitations 集中到 4.3；P guard 不写成唯一实现。 |
| Section 7, Related Work | `KEEP` `MERGE` `SHORTEN` | 0 引言末段 + 4.1/4.2 的定位句 | 不保留独立长章。保留 K-Waay、secure-messaging composition、identity/name semantics、injectivity/Tamarin 的最接近工作；MLS/group messaging 与 misbinding/UKS 只在确有定位需要时一句带过；检查 2025 K-Waay 后续工作是否改变接口前提。 |
| Conclusion | `KEEP` `REWRITE` `SHORTEN` | 5 结束语 | 保留三模型最窄结论和条件性设计启示；不重复完整 limitations；不增加协议攻击或部署含义。 |
| Appendix A, Detailed Counterexample Traces | `KEEP` `SHORTEN` `MOVE_TO_APPENDIX` | 3.1、3.2 的简短执行说明；其余待定附录 | R/M 代表性执行在正文各保留一段；逐规则序列可放中文稿附录或补充材料。独立复核已有 JSON graph 后，仍应把绘图称为人工整理，除非直接展示原 graph。 |
| Appendix B, Exact Model Properties | `KEEP` `SHORTEN` `MOVE_TO_APPENDIX` | 2.4、表 2；精确公式附录 | 正文给 common correspondence、injectivity 和派生关系；完整 lemma 文本由模型文件作为权威，是否随稿附录取决于期刊补充材料政策。 |
| Appendix C, Reproducibility Details | `KEEP` `REWRITE` `SHORTEN` `MOVE_TO_APPENDIX` | 2.4、4.3；详细 manifest 作为补充材料候选 | 旧“existing-report-only、无独立重跑”的叙述已过时。改为明确日期/commit 的新 reviewer rerun；同时说明它不是历史日志恢复，也不证明 source-to-model refinement。 |
| `model-comparison.tex` | `KEEP` `REWRITE` | 表 1 | 改为中文三线表，补 admission guard 和证据层次；“injectivity/party uniqueness”不写成彼此独立的两类发现。 |
| `verification-results.tex` | `KEEP` `REWRITE` | 表 2 | 保留 14 行、状态和 steps，新增 independent match；caption 使用“验证结果及独立复核”，不写 benchmark。 |
| `attack-trace.tex` | `KEEP` `REWRITE` | 图 2 | 转为可编辑矢量图/EMF；依据模型规则与复核 graph 人工整理；不称“机器直接导出的攻击图”。 |
| `identity-control-comparison.tex` | `MERGE` `SHORTEN` | 合入表 1 与 3.4 公式 | 信息与模型比较表、综合公式高度重合，建议不单独占图；若作者坚持保留，则需删减表 1 的重复列。 |
| `references.bib` | `KEEP` `REWRITE` `NEEDS_CONFIRMATION` | references 工作区，后续转换 | 保留可验证来源，按首次引用顺序重排并转 GB/T 7714—2005 风格；中文文献补英文信息；RFC/ePrint/在线规范类型等待确认。 |

## 2. 英文章节内部的细化映射

### Introduction

| 原内容 | 标签 | 新位置 | 说明 |
|---|---|---|---|
| K-Waay 与 `BatchReceive` 背景 | `KEEP` `SHORTEN` | 0 第 1 段、1.1 | 引言只给问题背景，接口细节放 1.1。 |
| source distinct-party condition | `KEEP` | 0、1.1 | 首次出现即说明条件由原文提出。 |
| 三模型概述 | `KEEP` `SHORTEN` | 0、2.3 | 引言一段；规则差异放表 1。 |
| contribution list | `REWRITE` `SHORTEN` | 0 末段 | 以“控制比较的证据”组织，不把 P 正控制和 14 条结果拆成多项贡献。 |
| paper organization | `SHORTEN` | 删除独立段 | 中文稿目录已短，无需逐章导读。 |

### Section 2 + Section 3

| 原内容 | 标签 | 新位置 | 说明 |
|---|---|---|---|
| 原算法输入、输出和 batch-wide failure | `KEEP` `SHORTEN` | 1.1 | 保留与索引/条件相关部分。 |
| identity-coordinate table | `KEEP` `REWRITE` | 1.2、图 1 | `sid` 改称 model-local `oid` 以防与原协议 transcript `sid` 混淆。 |
| same-party/different-message motivating composition | `KEEP` `MERGE` | 1.2 | 只出现一次；机器 witness 留到 3.2。 |
| 三个 RQ | `MERGE` `REWRITE` | 1.3 | 合并为两问，降低定义决定型的“正控制问题”。 |
| `DistinctPartyPerBatch` arbitrary-`n` definition | `KEEP` | 1.2 | 紧接固定两槽限定。 |
| composition adversary | `KEEP` `SHORTEN` | 1.3 | 不说已证明真实 batch builder 受攻击者控制。 |
| evidence boundary | `KEEP` `MERGE` | 1.3、4.3 | 详细限制只在 4.3 集中列出。 |

### Section 4 + Appendix B

| 原内容 | 标签 | 新位置 | 说明 |
|---|---|---|---|
| source-to-abstraction table | `KEEP` `REWRITE` | 2.1 | 审稿 M2 的核心；不能压成脚注。 |
| fixed two slots | `KEEP` | 2.2 | 与 arbitrary-`n` 语义定义并排说明。 |
| shared lifecycle | `KEEP` `SHORTEN` | 2.2 | 用流程文字或简图，不逐 rule 复述。 |
| R/M/P variant definitions | `KEEP` `MERGE` | 2.3、表 1 | 三条 guard 放同一张表。 |
| events/properties | `KEEP` `SHORTEN` | 2.4 | 正文给关键公式，完整源码是权威。 |
| all exact lemma listings | `MOVE_TO_APPENDIX` | 待定附录/补充材料 | 期刊未公开补充材料政策，不能擅自删除。 |

### Section 5 + Appendix A/C

| 原内容 | 标签 | 新位置 | 说明 |
|---|---|---|---|
| R normal witness | `KEEP` `SHORTEN` | 表 2、3.1 一句 | 仅用于 non-vacuity baseline，不作核心发现。 |
| R exact-origin witness and injectivity failure | `KEEP` | 3.1、图 2、表 2 | 说明同一完整 tuple、一个匹配 Send、两个接受 timepoint。 |
| M message safety/injectivity | `KEEP` `MERGE` | 3.2、3.4 | 与规则推导的 `M_tau <=> I_tau` 一起解释，避免双重计数。 |
| M same-party/different-message witness | `KEEP` | 3.2、表 2 | 核心 non-implication witness。 |
| P safety/non-vacuity | `KEEP` | 3.3、表 2 | 明示为正控制。 |
| rejection reachability | `KEEP` `SHORTEN` | 3.3 脚注/一段、表 2 | 不把 antecedent Sends 写成被拒 tuple。 |
| recorded-run limitations | `REWRITE` | 2.4、4.3 | 用独立复核更新；原 freeze 与新 rerun 分开。 |
| step-by-step reconstructed traces | `SHORTEN` `MOVE_TO_APPENDIX` | 图 2 caption + 附录候选 | 避免正文过长。 |

### Section 6 + Section 7 + Conclusion

| 原内容 | 标签 | 新位置 | 说明 |
|---|---|---|---|
| more-than-guard-removal | `REWRITE` `SHORTEN` | 4.1 | 不把定义层差异包装成强新颖性；强调受控证据作用。 |
| identity/message/injectivity explanation | `MERGE` `SHORTEN` | 3.4、4.1 | 公式一次、含义一次。 |
| invariant/enforcement | `KEEP` `SHORTEN` | 4.2 | caller/builder/admission 是可能位置，不是已验证部署事实。 |
| authentication/replay/dedup | `MERGE` `SHORTEN` | 4.1 | 只用于划清性质。 |
| design implications | `KEEP` `REWRITE` | 4.2、5 | 保留条件性措辞。 |
| six limitation paragraphs | `KEEP` `MERGE` | 4.3 | 合并成一张紧凑边界清单。 |
| long related-work taxonomy | `SHORTEN` `MERGE` | 0、4.1/4.2 | 不保留独立 Related Work 章。 |
| final conclusion | `KEEP` `SHORTEN` | 5 | 不重新展开模型与限制。 |

## 3. 图表映射

| 计划编号 | 原位置/来源 | 操作 | 中文题名 | English title | 要说明的事实 |
|---|---|---|---|---|---|
| 图 1 | K-Waay Fig. 10 的接口事实 + 英文 Section 2 identity coordinates；无现成同图 | `REWRITE`，后续新绘 | K-Waay BatchReceive输入条目、索引输出与参与方投影关系 | Input Entries, Indexed Outputs, and Party Projections in K-Waay BatchReceive | 原接口按 `j` 处理输入并返回 component；模型只投影 party/origin/message；source 与 abstraction 的边界。 |
| 图 2 | `manuscript/figures/tikz/attack-trace.tex` + independent rerun JSON graph | `KEEP` `REWRITE` | 宽松接纳模型中的代表性精确origin重复接受执行 | Representative Exact-Origin Duplicate-Acceptance Execution in the Relaxed Model | 同一匹配 origin 可在同一 context 产生两个接受；人工整理，非原始 prover 图。 |
| 现有 identity-control-comparison 图 | `manuscript/figures/tikz/identity-control-comparison.tex` | `MERGE` `SHORTEN` | 合入表 1/公式，不单独编号 | — | 信息与表 1、`P/M/I` 关系重复。 |
| 表 1 | `manuscript/tables/model-comparison.tex` | `KEEP` `REWRITE` | 三种两槽接纳模型的语义比较 | Admission Semantics of the Three Two-Slot Models | R/M/P 只改变的接纳坐标、同 party/不同 message、当前模型性质。 |
| 表 2 | `manuscript/tables/verification-results.tex` + `result-comparison.tsv` | `KEEP` `REWRITE` | 三个接纳模型的Tamarin验证结果及独立复核 | Tamarin Verification Results and Independent Reproduction for the Three Admission Models | 14 个 model–lemma 实例、状态、steps、复核匹配。 |

## 4. 暂不能决定的去向

- `NEEDS_CONFIRMATION`：是否允许正文附录或在线补充材料；这决定完整 lemma、命令和 manifest 的载体，但不允许删除它们。
- `NEEDS_CONFIRMATION`：是否保留第三张 source-to-abstraction 表；从审稿 M2 看强烈建议保留，若篇幅紧张才改成结构化正文。
- `NEEDS_CONFIRMATION`：中文摘要采用模板“200字以内”还是网页“200～300字”。
- `NEEDS_CONFIRMATION`：匿名初审稿的作者字段处理。公开资料没有明确特殊匿名规则；正式作者、单位、基金和联系方式只能由用户提供。
- `NEEDS_CONFIRMATION`：RFC、IACR ePrint、协议网页的最终文献类型标识。

