# 内容精简与格式转换计划

## 1. 精简原则

精简的目标是让证据链更清楚，不是以删掉假设或负面结果换取篇幅。官网未公布全文页数、字数或最大篇幅，本文件中的比例和压缩目标均为作者规划，不是《计算机应用研究》的强制限制。

中文稿每个核心事实只承担一次主要解释：

- 来源条件在第 1 章定义；
- 模型假设在第 2 章定义；
- 机器结果和人工推导在第 3 章报告；
- 协议含义和限制在第 4 章解释；
- 摘要、引言和结论只作必要的前后呼应。

## 2. 重复内容清单与处置

| 当前重复/过长内容 | 主要位置 | 处置 | 不得丢失的事实 |
|---|---|---|---|
| “message 不同不代表 party 不同”多次完整解释 | Sections 2、3、4.4、5.2、5.4、6.1–6.4、7.4–7.5、Conclusion | 第 1 章给直观例子，第 3.2 给机器 witness，第 3.4 给一次公式，第 4.1 给一次含义；其余改交叉引用 | M 的 same-party/different-message witness；`M_tau !=> P_tau` |
| party/message/session/slot/batch identity distinction 的多轮定义 | Sections 2、3、6、7 | 合并成 1.2 的一张坐标清单；后文只使用已定义符号 | party 是显式模型坐标，不能自动等同账号、公钥字节或数据库实体 |
| 每节重复“不是完整协议攻击/不是部署漏洞” | Abstract、Sections 3–7、Conclusion | 摘要一句、1.3 一句、4.3 集中边界、结论一句 | 直接证据止于 `ReceiverAccept`；无 refinement/key/consumer/deployment |
| R/M/P 每个 lemma 的逐句释义 | Section 5、Appendix B | 正文只细讲 6 个核心实例；14 个结果统一放表 2；完整 lemma 由模型源/附录承载 | lemma 名、status、steps、核心 witness、弱 rejection 限制 |
| R/M/P 共同规则的重复描述 | Section 4、Appendix A/B | 2.2 统一写一次共同生命周期；2.3 只列 admission 差异 | 三模型比较只改变 admission/rejection/restriction 与 lemma 集 |
| authentication、replay、deduplication 的防御性讨论 | Section 6.4、Section 7.4 | 合并为 4.1 的一至两段 | origin correspondence 不是完整 authentication；batch-local injectivity 不是全局 replay resistance |
| enforcement placement 的多种可能性反复列举 | Section 6.3、6.5 | 4.2 一段列 caller/builder/admission 三类可能位置 | 本文未验证任何真实实现的责任位置 |
| 固定两槽、无 arbitrary-`n` 的重复提醒 | Sections 3–7、appendices | 1.2 首次说明；2.2 精确定义；4.3 集中限制 | 两槽是最小违反对，不是任意批规模 theorem |
| source-to-abstraction gap 被多处解释 | Sections 4、6、7 | 2.1 用结构化映射集中说明；4.3 只总结其后果 | `!Sent` 理想 origin；无 recipient/prekey/context；不能称自然保守抽象 |
| 长 Related Work taxonomy | Section 7 五个小节 | 不保留独立章；引言末 1–2 段 + 4.1/4.2 的必要定位 | K-Waay 是直接来源；composition、identity semantics、injectivity、Tamarin 都是先行工作；本文只做协议特定应用 |
| 原 freeze 的可复现性免责声明 | Section 5.6、Appendix C | 用 2026-09-16 独立 rerun 更新；旧 freeze 与新证据分开写 | 14/14 匹配；新日志不是历史日志恢复；复现不证明协议连接 |

## 3. 必须保留的最小证据包

以下内容不能因中文重组、版式或篇幅考虑而删除：

1. K-Waay 原文的 different-party condition、Fig. 10 接口事实和准确版本/页码。
2. `DistinctPartyPerBatch` 定义，并同时说明一般语义定义与固定两槽机器范围。
3. source-to-abstraction mapping，尤其 `(pk,prek,m)` 到 `(A,oid,m)` 的投影和省略的密码/接收上下文。
4. R/M/P 三模型的唯一差异与共同生命周期。
5. R 的 `one_send_two_accepts_exists` 和 `receiver_accept_injective` 反例。
6. M 的 `same_party_different_messages_batch_exists`，以及 message safety/scoped injectivity 不是独立发现。
7. P 的 `accepted_batch_has_distinct_parties` 和 `distinct_party_batch_exists`。
8. `P_tau => M_tau <=> I_tau`、`M_tau !=> P_tau` 的层次标注：前三个关系为规则推导，最后的非蕴含有机器 witness。
9. 全部 14 个 model–lemma 结果、steps 和独立复核 match；不把 steps 当性能基准。
10. rejection lemma 未绑定被拒 tuple 的限制。
11. freshness、ideal origin、composition control、fixed-two-slot、receiver-event endpoint 和无 refinement 的限制。

## 4. 相关工作压缩方案

英文稿的 Related Work 不再形成中文独立一级章。建议保留约 6–9 篇最直接来源作为正文论证骨架，其余仍可留在文献表，但只有在正文实际引用时保留：

| 主题 | 正文功能 | 处置 |
|---|---|---|
| K-Waay full version | condition、algorithm、output/game interface 的直接来源 | 必留，准确区分 full version 与 proceedings |
| K-Waay 2025 后续 split-KEM 工作 | 检查接口前提是否变化 | 待核对后用一句交代，不据题名推断 |
| secure-messaging composition | 说明 composition layer 可有独立关系 | 留最接近的一项，不扩展成综述 |
| X3DH/PQXDH/Signal formal analysis | 区分完整 session/key analysis 与本文 admission abstraction | 合并为一段，限对比对象 |
| name/identity semantics | 说明名称唯一性与身份表示并非本文新理论 | 留一至两项 |
| injective agreement/replay | 说明术语先行性，防止把 scoped diagnostic 包装成新概念 | 留经典来源 + 一项方法来源 |
| MLS/group messaging、misbinding/UKS | 只用于排除错误分类 | 若篇幅紧，改在 4.3 一句或删除正文引用；不影响核心证据 |
| Tamarin tool paper | 方法来源 | 必留一项 |

压缩后仍须避免“现有工作没有研究 identity/composition”式宽泛新颖性声明。可写的空缺仅是：这些工作没有直接回答本文固定两槽的 K-Waay batch-admission party projection 比较。

## 5. 结果叙述压缩方案

### 正文详细解释的6个实例

1. R `one_send_two_accepts_exists` — verified 13。
2. R `receiver_accept_injective` — falsified 13。
3. M `same_party_different_messages_batch_exists` — verified 16。
4. M `accepted_batch_has_distinct_messages` / `receiver_accept_injective` — 作为一组解释，verified 31/33。
5. P `accepted_batch_has_distinct_parties` — verified 31。
6. P `distinct_party_batch_exists` — verified 17。

### 只在表中完整保留、正文短述的实例

- 三个 `receiver_accept_has_send`：共同 origin correspondence，均 8 steps。
- R `normal_relaxed_batch_exists`：基本可执行性，10 steps。
- 两条 rejection existence：4/5 steps，只表明 branch reachability。
- P `receiver_accept_injective`：33 steps，作为 `P_tau => M_tau => I_tau` 的一致性结果，不单列贡献。

### Trace文字

- R：正文用图 2 + 一段，说明一个 origin、同 tuple 两槽、两个接受 timepoint。
- M：正文用一段，说明两个不同 origin、同 A、不同 `oid/m`、两次接受。
- P：正文用一段说明正控制和 non-vacuity。
- 逐规则序列移至附录/补充材料候选；不把 JSON graph 中的无关 Send 当成最小攻击步骤。

## 6. 图表精简方案

| 项目 | 计划 | 理由 |
|---|---|---|
| 图 1 BatchReceive与参与方关系 | 后续新绘，保留 | 提供 M4 所需的协议接口动机与 source/model 边界 |
| 图 2 R representative trace | 基于现图重制，保留 | 核心负向 witness；必须标记人工整理 |
| 现有 identity-control-comparison | 合并入表 1 和 `P/M/I` 公式 | 与表/正文高度重复 |
| 表 1 R/M/P语义 | 重制并保留 | 最紧凑地交代 controlled comparison |
| 表 2 14项结果 | 重制并保留 | 防止选择性报告，承载 status/steps/rerun match |
| source-to-abstraction表 | 强烈建议保留为表 3；若版面紧再改结构化正文 | M2 不能通过一句 limitation 处理 |

## 7. 附录与补充材料处置

期刊公开资料没有明确附录、补充材料或 artifact 托管政策，因此本阶段不删除附录内容，也不假设它们一定能随稿提交。

建议优先级：

1. 正文必须自足地含目标定义、关键模型假设、6 个核心结果和限制。
2. 精确 lemma、详细 trace 与完整复现命令作为附录候选。
3. raw stdout/stderr、JSON graphs、manifest 和 SHA-256 作为电子补充材料候选；即使不能上传，也在本地证据包保留。
4. 如果编辑部不接收补充材料，再在不改变主张的前提下决定哪些精确公式进入正文；不能先删除后补证据。

## 8. 后续Word和格式转换计划

本节只列任务，不执行转换。

| 转换项 | 后续工作 | 主要风险 | 验收点 |
|---|---|---|---|
| LaTeX → Word | 在官方 `.doc` 模板副本中重建标题、摘要、正文、图表、页眉页脚 | 样式、单双栏、交叉引用和公式编号丢失；WPS 重存兼容性未验证 | 用官方原件副本；逐页与模板审计记录比对；不得覆盖 official 原件 |
| 英文正文 → 中文正文 | 按本结构重写，不逐句机翻 | 技术术语漂移、主张被强化、英文旧 provenance 状态被误带入 | 每节与 `CLAIM_EVIDENCE_MATRIX.md` 逐条核对 |
| LaTeX公式 → MathType | 将正式公式重录为可编辑 MathType 对象 | Unicode、上下标、量词和事件时间点出错；不能用图片代替 | 逐式对照 `.spthy` / 原 LaTeX；检查行内/独立公式与编号 |
| TikZ → 可编辑矢量图/EMF | 重绘两幅计划图，嵌入正文 | EMF 字体替换、线宽和双语题注不一致；手工 trace 被误标为 prover export | 保留可编辑源；图 2 caption 明示人工整理；Word 中放大检查 |
| BibTeX → 期刊格式 | 按首次引用顺序转为 GB/T 7714—2005 口径，手工核对 22 条现有文献 | `plain` 顺序/字段不可直接沿用；三人以上、中文双语、ePrint/RFC 类型 | 每项对照官方 PDF 指南；移除域代码/尾注承载；保留 DOI/版本 |
| 匿名信息 → 正式作者信息 | 用户确认后填作者、单位、通信邮箱/手机等 | 署名提交后变更受限；公开规则未明确匿名初审特殊要求 | 不猜测；一次收齐作者顺序、单位、通信作者和联系方式 |
| 基金/作者简介 | 用户确认后填模板首页页脚 | 基金名称/编号、简介、单位遗漏或错位 | 与正式证明材料核对；不从历史稿猜测 |
| 中文/英文图表题注 | 按模板样例统一 | 翻译不对应、表格非三线、单位位置不清 | 逐图表双语核对，保留可编辑对象 |
| 初投稿版式 | 决定通栏/双栏并生成投稿文件 | 官网允许初投通栏，但正式出版双栏；无官方总页限 | 将版式选择记录为作者决定，不写成官方页限 |

## 9. 精简后的质量门槛

进入完整中文写作前，应满足：

- 每个核心结论在 `CLAIM_EVIDENCE_MATRIX.md` 有唯一证据入口；
- M 与 I 不再被计为独立的两项发现；
- P safety 明确是正控制，M1 的发表价值风险在引言和报告中可见；
- source-to-model gap 位于方法主线而非脚注；
- 表 2 可由独立复核输出逐行核对；
- 任何“攻击”“漏洞”“身份绑定”“认证”“重放防护”措辞都带准确作用域，或改成模型内事件描述；
- 摘要、引言、结果、结论中的最强句子彼此一致。

