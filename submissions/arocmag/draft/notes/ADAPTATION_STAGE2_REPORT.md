# 《计算机应用研究》中文稿适配第2阶段报告

阶段：`AROCMAG_MANUSCRIPT_ADAPTATION_STAGE_2`  
日期：2026-10-02（Asia/Shanghai）

## 1. 本阶段实际创建的文件

### 正文初稿

- `sections/00-introduction.md`
- `sections/01-batch-admission-problem.md`
- `sections/02-symbolic-modeling.md`

### 审计与复核记录

- `notes/NOTATION_CONSISTENCY.md`
- `notes/FORMAL_RELATION_AUDIT.md`
- `notes/KWAAY_INTERFACE_AUDIT.md`
- `notes/STAGE2_SELF_REVIEW.md`
- `notes/ADAPTATION_STAGE2_REPORT.md`

本阶段没有修改 Stage 1 的 outline、report 或 README，没有编写第 3～5 章。

## 2. 第0～2章内容概要

### 0 引言

引言从异步后量子安全通信中的组合边界切入，介绍 K-Waay 和 `BatchReceive`，明确原协议已经规定批内不同元素对应不同参与方。随后区分单条输入的精确来源与多个输入之间的参与方组合关系，引出参与方、消息和发送实例三个坐标。正文以 R/M/P 三个共同生命周期模型为方法主线，概括 R 的精确来源重复接受、M 的同参与方不同消息见证和 P 的参与方安全性/非空性，并把贡献压缩为建模、受控比较和有限接口启示三点。末段集中声明固定两槽、理想来源、`ReceiverAccept` 终点和无 refinement/key/deployment 结论。

### 1 K-Waay批处理接纳及参与方区分问题

1.1 依据 K-Waay full PDF 的 Secs. 4.1、4.2、5.1 和 Fig. 10 重建与研究问题相关的接口：接收方状态、输入向量、参与方下标、逐分量 $k_j$、batch-wide failure 和原文 different-party condition。安全游戏中的 receiver `pid/sid/k` 向量及 `KEY/TEST(i,s,j)` 仅用于解释 party-indexed component 的动机。重复 $j$ 下的输出选择被明确标为未建立。

1.2 定义 $E=(A,oid,m)$、槽位、批次、接收方上下文和一般有限批次上的 `DistinctPartyPerBatch`。机器范围随后收缩到 $n=2$。正文分别给出精确重复条目与同参与方不同消息条目，说明 origin correspondence 不自动给出 batch composition relation。

1.3 定义 batch-composition adversary 的选择、重放和排列能力，说明它是分析边界能力而非部署攻击证据。研究问题压缩为“放宽 party condition 后的事件行为”和“message condition 能否替代 party relation”两项。直接观察终点固定为 `ReceiverAccept`。

### 2 批处理接纳机制的符号建模

2.1 通过 source-to-model 表区分 K-Waay 输入/状态/输出和模型条目/上下文/事件，解释 $!Sent(A,oid,m)$ 的理想来源语义及全部省略项。

2.2 逐步描述三个模型共有的 `CreateParty`、`SendMessage`、`CreateBatch`、两槽收集、接纳、顺序处理和完成状态，没有增加模型中不存在的处理步骤。

2.3 以表格比较 R/M/P：R 无不等限制，M 比较消息，P 比较参与方；P 明示为目标条件的正控制，而非唯一实现方案。

2.4 定义 sender-origin correspondence、$P_\tau$、$M_\tau$ 和 $I_\tau$，区分全称安全性质、存在性见证与弱 rejection reachability，并简要记录独立复核证据。详细结果保留给第 3 章。

## 3. 相对于英文母稿的重构

1. 将英文 Introduction、Section 2 的接口背景、Section 3 的 threat model 和 Section 4 的 abstraction 重组为“问题—定义—模型”三段证据链，而非逐句翻译。
2. 把原英文稿三个 RQ 压缩成两个：P guard 的效果不再作为未知型研究问题。
3. 将长篇 related work 压为引言中的组合边界、身份语义和形式化方法定位；未逐篇罗列。
4. 将 source-to-abstraction gap 前移到第 2.1 节主线，并明确抽象既不能自动视为保守近似，也没有 refinement theorem。
5. 把重复的 scope disclaimer 集中到引言末段、1.3 和 2.1，而不是每段重复防御性表述。
6. 用 K-Waay 原始 PDF 直接重审接口索引，修正 Stage 1 中可能把 $j$ 同时说成位置/party 的含混表达。
7. 用独立复核事实更新英文稿“没有 independent rerun/raw transcripts”的过时状态。

## 4. sid/oid处理结果

最终决定：中文论文采用

$$
oid\equiv sid_{model}.
$$

原协议 `sid` 保留其 transcript/session identifier 含义；模型源码 `sid` 只在源码、lemma 名称和原始结果引用中保留。论文解释性公式一律使用 $oid$。这一变化没有修改 `.spthy` 文件，也没有改变任何已验证性质。完整记号表见 `NOTATION_CONSISTENCY.md`。

## 5. P/M/I推导审查结果

无歧义关系为

$$
(P_\tau\Rightarrow M_\tau)\land(M_\tau\Leftrightarrow I_\tau),
\qquad M_\tau\not\Rightarrow P_\tau.
$$

- $M_\tau\Rightarrow I_\tau$：同一 exact tuple 的两个不同接受必共享消息，与 message distinction 冲突。
- $I_\tau\Rightarrow M_\tau$：利用每次 `SendMessage` 的 fresh $m$、已验证的 origin correspondence 和完整三元组匹配；相同 $m$ 的两个接受必须追溯到同一 Send，随后由 $I_\tau$ 排除不同接受时间点。
- $P_\tau\Rightarrow M_\tau$：相同 $m$ 同样迫使来源及参与方相同，与 party distinction 冲突。
- $M_\tau\not\Rightarrow P_\tau$：M 的 `accepted_batch_has_distinct_messages` 与 `same_party_different_messages_batch_exists` 共同提供机器证据。

前三个方向是人工规则推导；最后的非蕴含有 Tamarin safety + existence witness 支持。没有新增 lemma。详见 `FORMAL_RELATION_AUDIT.md`。

## 6. K-Waay索引语义审查结果

直接 PDF 审查得到：

1. Sec. 4.1 和 Fig. 10 中，$j$ 是声称发送方/对端参与方索引，出现在 $(pk_j,prek_j,m_j)$ 及输出 $k_j$ 上。
2. receiver session 的 `pid`、`sid` 和 $k$ 是 vectors；安全游戏允许一个 receiver 对应多个 sender counterparts。
3. `KEY(i,s,j)` 在 receiver 分支读取 $k_j$；`TEST(i,s,j)` 要求 $j$ 属于 receiver `pid` 并选择 $k_j$ 作为 real-or-random 对象。
4. 因此，在原文合法输入域内，共同下标 $j$ 关联参与方、输入分量和输出分量。
5. 原文没有 first-class slot，也没有定义同一 $j$ 重复出现时的输出/查询扩展语义。独立的 `slot ↔ party ↔ output` 双射和 duplicate-$j$ semantics 均为 **NOT ESTABLISHED**。
6. 当前模型没有 $k_j$、`KEY/TEST` 或 session status，不能从 `ReceiverAccept` 推出密钥接口后果。

详细位置和允许/禁止解释见 `KWAAY_INTERFACE_AUDIT.md`。

## 7. 尚未解决的研究和表述问题

- **研究增量**：M1 的非平凡性风险仍在。P 是定义驱动的正控制，M 的现实候选来源尚无实现或规范证据；中文改写没有掩盖这一点。
- **协议连接**：`!Sent` 仍是无 recipient/prekey/context binding 的 ideal origin；没有 source-to-model refinement 或具体 K-Waay witness lifting。
- **索引扩展域**：原文不定义重复 party index 的 output selection；当前稿不补写，因而不能提出 KEY/TEST consequence。
- **拒绝证据**：M/P rejection lemma 的前置 Send 不绑定被拒 tuple，只能报告 branch reachability。
- **批次范围**：一般定义适用于有限 $n$，机器验证仍仅为 $n=2$。
- **相关工作完整性**：2025 K-Waay 后续工作是否改变接口前提留待完整 Related Work 阶段核查；本阶段未新增未经核验的引用。
- **期刊格式**：摘要口径、附录/补充材料和特殊在线文献类型仍需后续确认，但不阻塞第 3 章 Markdown 写作。

## 8. 引用与原始来源核对

正文使用 8 个现有 BibTeX key：`collins2024kwaay`、`collins2024kwaayfull`、`cohngordon2020signal`、`bhargavan2024pqxdh`、`cremers2023session`、`lupetti2006names`、`lowe1997hierarchy`、`meier2013tamarin`。全部存在于 `manuscript/bibliography/references.bib`，未虚构文献。

K-Waay 核心接口不依赖母稿转述，已直接核对项目内 full PDF：

- Sec. 4.1 p.15：算法语法、输入向量和 key vector；
- Sec. 4.2.1–4.2.3 pp.16–18：receiver vector fields、EXEC、KEY/TEST；
- Sec. 5.1 Fig. 10 p.21：构造、逐分量 $k_j$、失败语义；
- Fig. 10 后 p.21：different-party condition；
- Sec. 5.2 pp.22–23：安全证明使用 `TEST(i,s,j*)` 的上下文，仅作索引语义交叉核对。

期刊参考文献指南已复核：后续 Word 阶段仍需按首次引用顺序转为期刊参考 GB/T 7714—2005 口径，多于 3 位作者按规则缩略。本阶段只保留可追踪 citation key，没有执行格式转换。

## 9. 需要用户确认的事项

进入第 3 章写作没有阻塞性确认事项。下列选择会影响后续整稿，但可在第 3 章完成后决定：

1. 是否继续接受“窄的、固定两槽形式语义案例”作为投稿定位，并承担 M1 的贡献强度风险；
2. 后续是否把 source-to-abstraction 表保留为正式正文表；
3. 是否在完整 Related Work 阶段纳入并核对 2025 K-Waay 后续工作；
4. 是否向编辑部确认补充材料/附录政策和摘要字数冲突。

作者、单位、基金和联系方式仍未填写，也不影响当前 Markdown 研究正文。

## 10. 进入第3章的条件判断

已具备进入“3 形式化验证与结果分析”写作的条件：

- R/M/P 模型和共同生命周期已精确描述；
- $oid$ 记号已统一；
- $P_\tau$、$M_\tau$、$I_\tau$ 已定义并完成依赖审查；
- 14 个模型—引理实例及独立复核证据可直接用于结果表；
- rejection、K-Waay interface 和 source-to-model 的限制已经冻结；
- 自检未发现与 `CLAIM_EVIDENCE_MATRIX.md` 冲突的强主张。

这里的 `READY` 仅表示第 0～2 章初稿及其证据接口可供人工审查，并可在另行授权后继续写第 3 章；不表示全文、Word 版或投稿包完成。

**AROCMAG_STAGE2_READY**

