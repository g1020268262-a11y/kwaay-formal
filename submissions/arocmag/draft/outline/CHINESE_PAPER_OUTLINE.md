# 中文论文结构设计

阶段：`AROCMAG_MANUSCRIPT_ADAPTATION_STAGE_1`

## 1. 结构判断与文章定位

候选结构适合《计算机应用研究》的常见技术论文论证顺序，建议保留六个正文一级标题，并将英文稿中独立的 Threat Model、Related Work 和大部分附录内容重新分配：

```text
0 引言
1 K-Waay批处理接纳及参与方区分问题
2 批处理接纳机制的符号建模
3 形式化验证与结果分析
4 讨论与局限性
5 结束语
```

建议将“机制”改为“接纳”，避免让读者误以为模型覆盖完整的 KEM、签名、KDF 和密钥输出流程。文章定位为**固定两槽接纳抽象中的受控语义比较**：K-Waay 原文已经规定一次 `BatchReceive` 的不同输入对应不同 party；本文不发现缺失条件，也不提出协议修补，而是分析该条件所约束的坐标，以及消息级限制能否替代参与方级限制。

可供后续确认的题名：

- 中文：`K-Waay批处理接纳中参与方区分条件的形式化分析`
- 英文：`Formal Analysis of the Distinct-Party Condition in K-Waay Batch Admission`

上述题名刻意限定在 condition、admission 和 formal analysis，避免“协议漏洞”“身份绑定攻击”等无证据扩张。

官方资料未公布全文页数或字数上限。以下百分比是作者规划，按正文计，不包含中英文摘要、参考文献、作者信息及可能的附录。

| 部分 | 建议占正文比例 | 主要功能 |
|---|---:|---|
| 0 引言 | 12% | 提出接口问题、研究缺口、证据范围和贡献 |
| 1 问题定义 | 18% | 建立 K-Waay 来源、身份坐标和目标性质 |
| 2 符号建模 | 25% | 公开抽象映射、对手能力、三模型差异和性质 |
| 3 验证与结果 | 30% | 给出 R/M/P 的机器结果、代表性执行与派生关系 |
| 4 讨论与局限 | 12% | 解释协议意义、不可替代性、证据边界和复现 |
| 5 结束语 | 3% | 只收束已证结论 |

## 2. 摘要、关键词与前置元数据

摘要不单列为正文一级标题，但应在后续中文稿中同时给出中文和英文版本，并逐项对应目的、方法、结果、结论。中文摘要应围绕一个窄问题组织：不同坐标上的接纳限制是否维持同一批次的参与方区分。不要把 14 个 model–lemma 实例写成 14 项独立发现。

摘要必须出现的事实：固定两槽；R/M/P 三种接纳语义；R 的精确 origin 重复接受；M 的同 party/不同 message 可达执行；P 的 safety 与 non-vacuity；直接证据止于 `ReceiverAccept`。摘要中可用一句话披露理想 origin、fresh message 和无 refinement theorem。独立复核作为可重复性事实放在正文，不必挤入摘要。

建议关键词为 5 个：`K-Waay`、`BatchReceive`、`形式化验证`、`Tamarin`、`批处理接纳`。中英文关键词需一一对应，最终数量按官方模板建议控制在 3～8 个。

中文摘要字数口径存在官网“200～300字”和模板“200字以内”的冲突，当前标记为 `NEEDS_CONFIRMATION`；本阶段不虚构作者、单位、中图分类号、基金、作者简介和联系方式。

## 3. 0 引言

### 本章要回答的问题

为什么 K-Waay 的 `BatchReceive` 是一个值得单独分析的批处理接口；本文确切研究哪个关系；现有证据能够回答到什么程度。

### 组织方式

遵循官方模板中“0 引言”的版式，成稿不再设置 0.1、0.2 等标题，使用四至五个紧凑自然段：

1. K-Waay、异步接收与批处理接口背景；
2. 原文明确的 different-party 输入条件及其 party-indexed 输出/查询动机；
3. 问题：消息不同或精确 origin 不重复是否能够替代 party 不同；
4. 方法：固定两槽、共同生命周期、R/M/P 三模型和独立复核；
5. 窄贡献与边界。

### 主要论点

- 原文条件已经存在；研究对象是它在受控接纳抽象中维持的关系。
- 单条输入具有匹配 origin，不自动推出多个输入的 party 投影互异。
- 核心比较是 message-level control 与 party-level invariant 的不可替代性，不是发现完整协议攻击。
- P 模型是公开的正控制；其 guard 导出相应 safety，不能包装成从密码运算中发现的新定理。

### 公式

引言只保留一句内联目标式：`message distinction / scoped injectivity ≠ party distinction`。完整定义和 `P_tau => M_tau <=> I_tau` 移至第 3 章。

### 图表

引言不放结果表。若版式允许，可在本章末提前引用图 1，但图体置于第 1 章。

### 英文稿来源与处置

- 来源：Abstract、Introduction、Section 2.1–2.2、Section 7.1 和 7.5。
- 合并：相关工作只留下最接近的 K-Waay、secure-messaging composition 与 Tamarin 背景。
- 缩减：英文稿贡献列表、论文结构导读、重复的否定性边界声明。
- 必须保留：原文条件不是本文发现；固定两槽；模型层结论；无完整协议/部署漏洞结论。

## 4. 1 K-Waay批处理接纳及参与方区分问题

### 本章要回答的问题

`BatchReceive` 的输入和输出如何使用 party 索引；“不同参与方”究竟约束哪个坐标；本文的安全目标和分析输入域是什么。

### 1.1 K-Waay的BatchReceive接口

主要论点：原算法接收由 `(pk_j, prek_j, m_j)` 组成的集合/向量，对每个 `j` 产生 `k_j` 或 `⊥`，并明确假设一次调用中每个元素来自不同 party；split-KEM 失败还可能触发 batch-wide failure。这里只说明与批处理索引有关的接口事实，不重述全部 DAKE 构造。

应出现的公式：

```text
S = ((pk_j, prek_j, m_j))_j,       BatchReceive(sk_i, st_i, S) -> {k_j}_j 或 ⊥^{|S|}
```

来源：英文 Section 2.1–2.2；K-Waay full version Sec. 5.1、Fig. 10。

### 1.2 身份坐标与批内参与方区分

主要论点：区分 party、message、model-local origin token、slot、batch/context；模型条目是分析投影，不是原 wire tuple。

应出现的公式：

```text
E_i = (A_i, oid_i, m_i)
DistinctPartyPerBatch(B) := forall i<j, party(E_i) != party(E_j)
```

`oid` 是中文稿建议记号，用来避免与原 K-Waay transcript `sid` 混淆；更名仅属于表述层，后续引用模型 lemma 时仍注明模型源文件使用 `sid`。

### 1.3 研究问题、对手能力与证据终点

主要论点：批处理组合对手可以选择、重放和排列已暴露的符号 tuple；精确重复与同 party/不同 tuple 是两种情况；接受仍要求理想化的精确 `!Sent` origin。直接证据止于 `ReceiverAccept`，没有 key、`KEY/TEST`、应用安装或部署行为。

研究问题压缩为两个：

- RQ1：放宽 party-level condition 后，当前接纳生命周期中可达什么 receiver-event 行为？
- RQ2：message-level restriction 能否替代 same-batch party distinction；直接维护 party relation 是否在非空有效执行中成立？

不再把“P guard 能否导出 P safety”列成独立发现型 RQ。

### 图表与处置

- 图 1：`BatchReceive输入条目、索引输出与参与方投影关系` / `Input Entries, Indexed Outputs, and Party Projections in BatchReceive`。基于 K-Waay Fig. 10 的接口事实重新绘制概念图，不复制原论文图；明确标出 source interface 与 symbolic projection 的边界。
- 合并：英文 Section 2 与 Section 3 的目标、坐标、对手和边界。
- 缩减：完整密码原语流程、重复的身份术语解释、三次重复的 same-party/different-message 例子。
- 必须保留：原文 condition 与准确引用；`DistinctPartyPerBatch`；精确重复和同 party/不同 message 的区别；固定两槽只是最小违反对。

## 5. 2 批处理接纳机制的符号建模

### 本章要回答的问题

模型保留了哪些源接口事实，又主动省略了什么；R/M/P 三个 theory 只在哪个 guard 上不同；各性质实际观察什么。

### 2.1 源接口到符号模型的映射

主要论点：`(pk,prek,m)` 被投影成 `(A,oid,m)`；模型保留批内位置、party 投影、共同 batch/context 和逐槽接受；省略签名、KEM、KDF、receiver/prekey binding、batch-wide failure 与 key 输出。`!Sent` 是理想 origin oracle，既不能宣称是保守 over-approximation，也不能提升为协议 refinement。

建议用一张紧凑映射表或正文项目列出“源对象—模型对象—保留关系—省略关系”。如果版面允许，该表作为表 1 之前的无编号小表；若只保留两张主表，则改为正文。

### 2.2 共同生命周期和两槽范围

主要论点：创建 party、fresh `oid/m`、公开 tuple、收集两个 slot、接纳、顺序 `ProcessSlot1/2`；`!Sent` 可复用，处理状态是线性的。`bid/rst` 只给出模型内作用域。机器证据固定 `n=2`，语义定义可写任意有限 `n`，但不得声称已证明任意 `n`。

应出现的性质公式：

```text
ReceiverAccept(A,oid,m,bid,rst)@r
  => exists s. Send(A,oid,m)@s & s<r
```

以及作用域内 exact-origin injectivity 的简化定义。正文解释这是模型内 origin correspondence，不等于完整 AKE authentication 或 replay resistance。

### 2.3 三种接纳语义

主要论点：R 不比较坐标；M 要求 `m_1 != m_2`；P 要求 `A_1 != A_2`。三模型共同规则已比对一致，变化集中在 admission/rejection/restriction 和 lemma 集。

- 表 1：`三种两槽接纳模型的语义比较` / `Admission Semantics of the Three Two-Slot Models`。
- 表中必须区分“guard”“允许的同 party/不同 message”“当前模型的 scoped injectivity”“party distinction”，并加脚注说明后两列不是互相独立的 2 项发现。

### 2.4 性质、运行证据与复核口径

主要论点：14 个 model–lemma 实例是覆盖表，不是 14 项贡献；结果以模型源、独立复核 stdout/stderr、JSON graphs、manifest 和 hash 为证。独立复核在 commit `3ebf8855f6226d7ebef8a78f2a7fae4a27679d57` 的 clean worktree 上使用 Tamarin 1.12.0 / Maude 3.5.1，14/14 状态与步数匹配。

来源：英文 Section 4、Appendix model-properties/reproducibility，以及独立复核证据。英文 Appendix C 中“未独立重跑、没有 raw transcript”的旧状态必须改写，不能带入中文稿。

### 合并、缩减和保留

- 合并：英文 Section 4 的坐标、共同规则、三变体和性质；Appendix B 中必要的精确性质。
- 缩减：逐条粘贴完整 Tamarin lemma；只在正文给出关键公式，完整 14 行放表 2。
- 必须保留：source-to-abstraction gap；freshness/origin 假设；R/M/P 只改接纳谓词的可比性；模型文件名、版本和独立复核 provenance。

## 6. 3 形式化验证与结果分析

### 本章要回答的问题

三种接纳语义分别允许或排除什么执行；哪些是机器结果，哪些是规则层人工推导；比较能够支持的最强结论是什么。

### 3.1 宽松模型：精确origin重复接受

主要论点：`one_send_two_accepts_exists` verified（13 steps）；`receiver_accept_injective` falsified（13 steps）；一个匹配 Send 的完整 tuple 被两个槽收集，并在同一 `(bid,rst)` 下产生两个不同时间点的 `ReceiverAccept`。无关 Send 可同时存在，不影响 lemma 的唯一匹配 origin 条件。

- 图 2：`宽松接纳模型中的代表性精确origin重复接受执行` / `Representative Exact-Origin Duplicate-Acceptance Execution in the Relaxed Model`。
- 图题必须写“依据模型规则和独立复核 graph 人工整理”，不能写“由 Tamarin 直接导出的攻击图”。

### 3.2 消息级模型：排除精确重复但不保证party区分

主要论点：`accepted_batch_has_distinct_messages` verified（31）；`receiver_accept_injective` verified（33）；`same_party_different_messages_batch_exists` verified（16）。两条不同 `oid/m` 的合法 origin 可以同属一个 `A` 并在同一批次各接受一次，因此 `M_tau` 不蕴含 `P_tau`。这不是 origin mismatch、identity ambiguity、UKS 或 misbinding。

### 3.3 参与方级模型：safety与non-vacuity

主要论点：`accepted_batch_has_distinct_parties` verified（31）；`distinct_party_batch_exists` verified（17）；`receiver_accept_injective` verified（33）。P 的 party guard 是公开的建模选择，safety 是该 guard 在共同生命周期中的保持；价值是正控制和非空性，不是从完整 K-Waay 密码学中发现新条件。

两条 rejection lemma 只作为分支可达性附带报告：M 为 verified（4），P 为 verified（5），但前置 Send 没有绑定到被拒 tuple。不得写成“这两条合法 sender 输入被拒绝”，也不得推导 liveness。

### 3.4 综合关系与结果表

应出现的公式：

```text
P_tau => M_tau <=> I_tau,       M_tau !=> P_tau
```

其中 `P_tau`、`M_tau`、`I_tau` 只针对当前 fresh message、exact-origin、固定两槽规则中的接受 trace。前三个蕴含方向由规则人工推导；`M_tau !=> P_tau` 由 M 模型的机器可达 witness 支持。必须在公式旁标注“derived relation, not a new Tamarin lemma”。

- 表 2：`三个接纳模型的Tamarin验证结果及独立复核` / `Tamarin Verification Results and Independent Reproduction for the Three Admission Models`。保留 14 行、状态、steps 和 independent match；正文只解释 6 个核心实例。
- 可选压缩图：现有 `identity-control-comparison.tex` 的信息与表 1 和公式重复，建议合并进表 1，不作为独立图保留。

### 英文稿来源与处置

- 来源：Section 5 全部、Appendix A、Appendix B、两张现有表和两幅 TikZ 图、独立复核证据。
- 合并：R/M/P 结果与横向比较在本章完成，不在第 4 章重复讲一遍。
- 缩减：逐 lemma 散文复述、同一非蕴含在多节重复、手工 trace 的逐规则长清单。
- 必须保留：R witness、M separation witness、P safety/non-vacuity、14 个结果、人工推导标识、rejection 限制和 independent rerun。

## 7. 4 讨论与局限性

### 本章要回答的问题

上述模型结果对 K-Waay 接口解释意味着什么；哪些解释可以进入论文，哪些只能作为未来研究；结论为何不能提升到完整协议或部署。

### 4.1 批处理组合关系的不可替代性

主要论点：单个 entry 的 origin correspondence 与多个 entry 的 party composition 是不同义务；当接口语义按 party 索引输出或查询 component 时，message、origin occurrence、slot 等坐标的区分不能在没有映射论证的情况下替代 party inequality。

### 4.2 K-Waay接口动机与条件性设计启示

主要论点：原算法返回 `{k_j}_j`，安全游戏以 party/component 索引使用接收结果，这使 party 投影成为协议特定动机。当前模型没有建立 output selection、`KEY/TEST` 或完整 game 的语义；因此只能提出条件性启示：负责构造或接纳批次的组件，应明确维持接口所要求的 participant relation，并说明 party attribution 的来源。不要指定某个真实实现一定应在 receiver 内新增检查。

### 4.3 局限性与复现边界

合并为一处列明：

- 固定两槽，无 arbitrary-`n` theorem；
- `!Sent` 理想 origin，缺 recipient/prekey/context binding；
- 无 KEM、签名、KDF、keys、`KEY/TEST`、consumer 和部署；
- 无 source-to-model refinement；
- composition control 是分析假设；
- rejection witness 未绑定具体输入且无 liveness；
- party representation/enforcement 未验证；
- 独立复核证明当前抽象结果可重现，不认证历史运行，也不补足协议连接和研究新颖性。

### 图表与处置

本章不新增图。避免把“没有漏洞”类免责声明分散到每一小节，统一放在 4.3，并在摘要/结论各用一句边界提醒。

来源：英文 Section 6；Section 7 中与本文定位最相关的材料；adversarial review M1–M7；独立复核 README/manifest。

## 8. 5 结束语

### 本章要回答的问题

在不引入新主张的前提下，最简洁地回答研究问题。

### 主要论点

一段或两段即可：R 显示放宽接纳的 receiver-event 行为；M 显示 message-level control 不替代 party distinction；P 给出该关系的正控制与非空性；因此批处理接口应显式陈述并维护与其解释一致的 participant relation。

### 公式、图表与来源

不新增公式和图表。来源为英文 Conclusion 和 Section 6 的 design implication。不得出现密钥泄露、实际漏洞、任意批规模、完整认证或 refinement 结论。

## 9. 总体证据链

```text
K-Waay源接口与different-party条件
        ↓ 仅提取party/slot/batch关系，明确省略项
固定两槽的共同接纳生命周期
        ↓ 仅替换admission guard
R无坐标限制 ─ M限制message ─ P限制party
        ↓                    ↓
机器结果与独立复核        规则层人工推导
        └──────────┬─────────┘
     受限的non-substitutability结论
        ↓
条件性接口设计启示 + 明确局限
```

这条链不能越过 `ReceiverAccept` 进入 key、application 或 deployment 层。

