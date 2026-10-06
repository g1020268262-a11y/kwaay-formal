# K-Waay 英文母稿到中文期刊结构的重组计划

## 1. 母稿现状

本次只读检查覆盖：

- `manuscript/paper-content.tex`；
- `manuscript/sections/00-abstract.tex`～`08-conclusion.tex`；
- `manuscript/tables/model-comparison.tex` 与 `verification-results.tex`；
- `manuscript/figures/tikz/attack-trace.tex` 与 `identity-control-comparison.tex`。

正文约 9,200 个英文词，结构为 Introduction、协议问题、Security Objective and Threat Model、Formal Modeling、Formal Analysis、Discussion、Related Work、Conclusion 八个一级章。正文实际使用 2 幅 TikZ 图和 4 张内嵌/输入表；`model-comparison.tex` 当前未被正文输入，但其中的比较维度可用于中文稿压缩。

重组遵循两个原则：技术证据不丢失；重复边界和英语论文式章节分隔被压缩。

## 2. 逐节映射

| 英文母稿 | 中文稿建议去向 | 处理动作 | 理由 |
|---|---|---|---|
| Abstract | 中文摘要/英文摘要 | 保留问题、方法、三项结果和边界；压缩模型细节 | 摘要应给结论链，不复述全部假设 |
| Introduction | 0 引言 | 保留首三段问题背景；吸收 Related Work；压缩 RQ、结果、贡献和 scope | 同类样本多在引言完成综述与贡献 |
| Sec. 2.1 K-Waay and BatchReceive | 1.1 BatchReceive 接口与不同参与方条件 | 保留接口、批输入和共同接收状态；删去对完整握手“不做什么”的重复说明 | 背景只写到理解问题所需 |
| Sec. 2.2 Stated Distinct-Party Condition | 1.1 | 与接口说明连续呈现；明确条件来自 K-Waay 原文，本文只给分析名称 | 防止把既有条件误写成本文发现 |
| Sec. 2.3 Identity Coordinates | 1.2 身份坐标与最小问题实例 | 保留 (A,sid,m,slot,batch,rst) 的区分；与 source-to-abstraction 表合并 | 这是论文语义贡献的基础，但无需两张重复表 |
| Sec. 2.4 Motivating Identity Problem | 1.2 | 保留同一参与方、不同发生与消息的两槽实例；把两条重复非蕴含式合并 | 用一个最小例子建立研究问题 |
| Sec. 2.5 Research Questions | 1.3 研究问题与分析目标；部分进入引言贡献 | 将 RQ1～RQ3 压缩为三句，不保留每个 RQ 后的长 non-goal | 中文节奏需要更快进入建模 |
| Sec. 3.1 Party-Level Batch Identity Objective | 2.1 安全目标与批组成攻击者 | 保留任意有限批的定义，并明确机器证据固定两槽 | 先说明要维持的关系，再说明模型 |
| Sec. 3.2 Batch-Composition Adversary | 2.1 | 保留选择、重放、排列和组合能力；攻击者不是部署能力的边界写一次 | 威胁模型不必独立一级章 |
| Sec. 3.3 Analysis Boundary | 2.1 末尾给一句总边界；完整内容移至 4.3 | 模型端点说明首次出现时必须有，但密码过程/消费者/refinement 等限制集中一次 | 避免每节重复 scope/non-goal |
| Sec. 4.1 Modeling Objective and Abstraction | 2.2 共同两槽生命周期与抽象 | 保留来源映射、两槽理由、Tamarin 方法；将两张设计表重组 | 建立源协议到符号模型的桥接 |
| Sec. 4.2 Common Two-Slot Lifecycle | 2.2 | 改为图 1 + 关键事件文字；保留精确 origin tuple | 图比长段落更适合期刊节奏 |
| Sec. 4.3～4.5 三种模型 | 2.3 受控准入变体与安全性质 | 三种变体放在同一小节和一张表；不把它们包装成三套协议 | 模型是实验控制，不是论文主线 |
| Sec. 4.6 Events and Analysis Properties | 2.3 | 保留五类动作事实与四类性质；完整 lemma 公式不进正文 | 读者只需知道观察对象和性质类型 |
| Sec. 5.1 Relaxed Admission | 3.1 放宽准入的重复发生反例 | 保留非空性、核心见证、injectivity 反例、origin correspondence；保留轨迹图 | 回答 RQ1/RQ2 的第一条证据链 |
| Sec. 5.2 Message-Level Restriction | 3.2 消息级限制的对照结果 | 保留消息不同与 injectivity 成功、同一参与方不同消息仍可达 | 中心非蕴含结论，不可删 |
| Sec. 5.3 Party-Level Restoration | 3.3 参与方级约束的恢复结果 | 保留规则语义、全迹安全、有效批次可达；压缩 rejection lemma 的重复限定 | 形成正控制和非空性闭环 |
| Sec. 5.4 Controlled Comparison | 3.4 结果汇总与语义解释 | 与 Verification Summary 合并；跨模型解释一次 | 避免先比较、再用表重复比较 |
| Sec. 5.5 Verification Summary | 3.4 | 保留 14 条完整结果表；步骤数可转附属材料 | 保持证据完整和可审查性 |
| Sec. 5.6 Verification Environment | 3.4 末段或脚注 | 保留版本、记录执行、哈希/命令所在位置；不暗示新运行 | provenance 必须保留但不抢主线 |
| Sec. 6.1～6.4 | 4.1 身份坐标的非蕴含关系 | 合并“超过 guard removal”“身份/消息/发生注入性”“认证/重放/去重” | 这些段落共同回答结果的语义含义 |
| Sec. 6.3、6.5 | 4.2 组合不变量与执行责任 | 合并 invariant/enforcement 和三条 design implications | 从模型结论导出清楚的接口责任 |
| Sec. 6.6 Limitations | 4.3 适用范围与局限 | 固定两槽、抽象端点、拒绝证据、表示/执行、记录 provenance 各保留一次 | 集中边界，同时不牺牲严谨性 |
| Sec. 7 Related Work | 0 引言 | 五小节压缩为三组文献定位；删去反复的“不是新的一般理论”句式 | 5/7 样本在引言完成相关工作 |
| Sec. 8 Conclusion | 5 结束语 | 保留两段逻辑，压缩为问题回答、设计含义、扩展条件 | 与样本的短结束语一致 |
| Appendix: model properties | 附属材料/仓库，不进入主文 | 主文结果表保留 lemma 名和结果；完整量词公式留现有材料 | 双栏正文不宜转录全部性质 |
| Appendix: trace details | 3.1 的图注和短说明；其余留附属材料 | 主文给关键事件序列和 provenance | 足够支持读者理解反例 |
| Appendix: reproducibility | 3.4 末段 + 附属材料 | 主文写版本和证据位置，命令/哈希保留外部 | 兼顾可复现与篇幅 |

## 3. Scope/Non-goal 的集中方案

### 第一次结果前必须出现

在 2.1 末尾用一段说明：分析对象是固定两槽的批准入抽象；攻击者控制组合是模型假设；直接证据止于 `ReceiverAccept`。这是理解结果所必需的局部边界。

### 第一次关键结果出现时

在 3.1 的反例解释末尾写：该见证属于放宽模型，不能读成满足原不同参与方条件的 K-Waay 执行，也不直接证明密码学或部署漏洞。只写一次，不在 3.2/3.3 重复整段。

### Discussion/Limitations

在 4.3 集中说明：

- (n=2) 的有界证据；
- 未建模 KEM、签名、密钥导出、ratchet 和 compromise；
- 无完整协议到抽象的 refinement theorem；
- `ReceiverAccept` 不等于 K-Waay 安全模型中的接收或应用安装；
- rejection lemma 的存在性与规则语义差异；
- 未建立部署批构造器可被攻击者控制；
- 结果来自既有执行记录，未包含原始 prover transcript。

结论只用一句收束“扩展到完整协议或部署需要额外连接”，不再重复清单。

## 4. R/M/P 模型的定位

R/M/P 不应成为中文稿的三个并列“方案”。建议使用以下叙事：

- **主问题**：K-Waay 的不同参与方条件维持什么批内身份关系；
- **方法**：在共同两槽生命周期上改变准入坐标；
- **基线**：relaxed 展示移除不变量后可达的重复发生；
- **替代对照**：message-level 检验“不同消息是否足以替代不同参与方”；
- **正控制**：party-level 直接约束目标坐标并验证非空性。

中文名称统一为“放宽准入变体”“消息级限制变体”“参与方级准入变体”。在标题中不使用孤立的 R/M/P 字母，也不称“协议 R/M/P”。

## 5. 图表重组

- `attack-trace.tex` → 图 2，保留并压缩；
- `identity-control-comparison.tex` → 不作为独立图，其信息进入表 2；
- `identity-coordinates` + `source-abstraction` → 合并为表 1；
- `admission-model-design` + 未输入的 `model-comparison.tex` → 合并为表 2；
- `verification-results.tex` → 表 3，保留全部 14 条结果，必要时移除 Steps 列；
- 新的生命周期图只在后续正文制作阶段绘制，本任务不画正式图。

## 6. 重组后的论证主线

读者最终应按以下链条理解论文：原协议已有不同参与方条件 → 参与方、消息和发送发生是不同坐标 → 用共享生命周期的三个变体检验坐标替代 → 消息级成功不推出参与方级成功 → 参与方级正控制维持目标且非空 → 因而批组成边界必须明确保存目标参与方关系。模型服务于这条论证，而不是取代它。

