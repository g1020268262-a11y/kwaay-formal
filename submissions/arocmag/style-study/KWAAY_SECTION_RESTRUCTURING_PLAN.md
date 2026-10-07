# K-Waay 英文母稿到中文期刊版重组计划（冻结版）

## 1. 重组目标

英文母稿约 9,200 词，采用 Introduction、协议问题、Security Objective and Threat Model、Formal Modeling、Formal Analysis、Discussion、Related Work、Conclusion 八个一级章。中文稿不删减核心技术证据，但压缩重复的身份说明、模型免责声明、结果边界和独立相关工作。

最终一级章固定为：

0 引言；1 K-Waay批处理接纳与参与方区分问题；2 批处理接纳的形式化建模；3 形式化验证与结果分析；4 结果讨论与适用范围；5 结束语。

## 2. 样本使用权重

P1 Tamarin-MQTT 和 P2 形式化辅助建模是结构主参考，用于决定模型、属性、攻击者和结果章节的顺序。P3～P7 只提供中文安全论文的引言、公式、图表和结束语写法。认证协议的流程图、ROR 证明和性能实验不迁移到 K-Waay。

## 3. 英文内容映射

| 英文母稿内容 | 中文去向 | 保留与压缩决定 |
|---|---|---|
| Abstract | 中英文摘要 | 保留问题、受控比较、三项结果；复现事实只给一句，不列命令 |
| Introduction 前三段 | 0 引言第 1～2 段 | 保留批组成问题、K-Waay 和 different-party condition |
| Introduction: Questions and approach | 0 引言第 5 段；1.3 | 引言给方法概述；RQ1～RQ3 在 1.3 各一句 |
| Introduction: Results and contribution | 0 引言第 5～6 段 | 保留三项结果和三项以内贡献；不把三个配置写成创新点 |
| Introduction: Scope | 2.1、3.1、4.3 | 删除引言 Scope 段，按三个冻结位置分配 |
| Sec. 2.1 K-Waay and BatchReceive | 1.1 | 只保留 Send、BatchReceive、输入向量、共享接收方状态 |
| Sec. 2.2 Stated Distinct-Party Condition | 1.1 | 明确条件来自原协议；本文只分析其语义 |
| Sec. 2.3 Identity Coordinates | 1.2、表 1 | 合并身份坐标与 source-to-abstraction；删除重复定义 |
| Sec. 2.4 Motivating Identity Problem | 1.2 | 保留一个最小实例；非蕴含只说一次 |
| Sec. 2.5 Research Questions | 1.3 | 三问各一句，不附长 non-goal |
| Sec. 3.1 Party-Level Batch Identity Objective | 2.1 | 保留 `DistinctPartyPerBatch(B)` 核心公式 |
| Sec. 3.2 Batch-Composition Adversary | 2.1 | 合并 Dolev–Yao 和选择、重放、排列、重复条目能力 |
| Sec. 3.3 Analysis Boundary | 2.1 一句；4.3 完整说明 | 2.1 只保留理解模型必需的局部边界 |
| Sec. 4.1 Modeling Objective and Abstraction | 1.2 表 1；2.2 | 来源映射进入表 1，抽象目的进入共同生命周期 |
| Sec. 4.2 Common Two-Slot Lifecycle | 2.2、图 1 | 以共同骨架图和短文替代长段落 |
| Sec. 4.3～4.5 三个模型 | 2.3、表 2 | 改称三种接纳配置，用一表说明，不分别展开长小节 |
| Sec. 4.6 Events and Analysis Properties | 2.3 | 保留性质类别和事件语义；完整公式留模型/复现材料 |
| Sec. 5.1 Relaxed Admission | 3.1、图 2 | 保留精确来源重复接受、injectivity 反例和来源对应 |
| Sec. 5.2 Message-Level Restriction | 3.2 | 保留三项关键机器结果，机器见证支撑非替代性 |
| Sec. 5.3 Party-Level Restoration | 3.3 | 改称 positive control；保留目标性质和非真空性 |
| Sec. 5.4 Controlled Comparison | 3.4 | 与结果汇总合并，不单独重复比较 |
| Sec. 5.5 Verification Summary | 3.4、表 3、完整 14 项材料 | 主表 7 项关键结果；完整 14 项不删除 |
| Sec. 5.6 Verification Environment | 3.4 | 更新为 2026-09-16 独立复核；细节指向 evidence 目录 |
| Sec. 6.1、6.2、6.4 | 4.1 | 合并消息、发生注入性和参与方坐标的语义讨论 |
| Sec. 6.3、6.5 | 4.2 | 合并不变量/执行机制与接口责任 |
| Sec. 6.6 Limitations | 4.3 | 集中全部限制和 reviewer rerun 边界 |
| Sec. 7 Related Work 五小节 | 0 引言第 3 段 | 压缩为三组问题导向的引用；不保留独立章 |
| Sec. 8 Conclusion | 5 结束语 | 保留四项最终结论；删工具环境和限制重复 |
| Appendix: model properties | 完整结果/复现材料 | 不把完整量词公式搬入正文 |
| Appendix: trace details | 3.1 图 2 说明；复现材料 | 正文给核心事件链，其余可追踪 |
| Appendix: reproducibility | 3.4 一句；`reviews/2026-09-16-evidence/` | 采用更新后的独立复核事实 |

## 4. 记号重组

中文稿统一使用：

\[
E_i=(A_i,\mathit{oid}_i,m_i).
\]

其中 `oid` 是发送发生坐标，对应现有 Tamarin 文件中的 `sid`。改名只用于避免读者把该坐标自动理解为完整协议 session identifier；不得修改模型，也不得声称 `oid` 是原 K-Waay 接口字段。表 1 必须显式给出 `oid ↔ sid` 映射。

正文独立编号公式压缩为条目、`DistinctPartyPerBatch`、核心反例事件链三项。最小实例、消息不等式和参与方不等式用行内数学或表 2 表达。

## 5. 三种接纳配置的定位

- **放宽配置**：不约束身份坐标，是反例基线；
- **消息级配置**：约束消息坐标，是替代性对照；
- **参与方级配置**：约束目标参与方坐标，是 positive control。

它们共享相同的发送、网络暴露、两槽收集、精确来源匹配、顺序处理和 `ReceiverAccept` 骨架。中文稿不得使用“协议 R/M/P”“修复模型”或“三套新协议”。

## 6. 结果重组

### 正文关键结果

表 3 列 7 项：

1. `one_send_two_accepts_exists`；
2. relaxed `receiver_accept_injective`；
3. `accepted_batch_has_distinct_messages`；
4. message-level `receiver_accept_injective`；
5. `same_party_different_messages_batch_exists`；
6. `accepted_batch_has_distinct_parties`；
7. `distinct_party_batch_exists`。

正文以自然语言性质为主，lemma 名退居括号或次要列。

### Supporting properties

`normal_relaxed_batch_exists`、三个 `receiver_accept_has_send`、两个 rejection reachability 和 party-level `receiver_accept_injective` 合并解释。完整状态与 steps 保留在 14 项结果材料。详见 `FULL_14_RESULT_PLACEMENT_DECISION.md`。

## 7. Scope/Non-goal 的唯一位置

1. **2.1**：固定两槽；组合能力是分析假设；证据止于 `ReceiverAccept`。
2. **3.1**：放宽配置反例不是满足原 different-party condition 的完整 K-Waay 攻击。
3. **4.3**：fixed two-slot、ideal exact origin、no full crypto、no KEY/TEST、no consumer、no refinement、no deployment exploit claim、rejection witness 限制和独立复跑 provenance。

其他章节不重复整段边界；引言不设 Scope；结束语不复述限制。

## 8. 图表迁移

- `attack-trace.tex` 的论证内容保留为图 2，但后续需按中文记号重构；本任务不画图。
- `identity-control-comparison.tex` 不再作为独立图，有效信息进入表 2 和表 3。
- identity coordinates 与 source-to-abstraction 合并为表 1。
- admission model design 与 model comparison 合并为表 2。
- verification results 分为正文 7 项关键表和完整 14 项复现表。

图表的目的、输入、必须表达和禁止表达以 `FINAL_CHINESE_PAPER_BLUEPRINT.md` 为准。

## 9. 统一复现事实

2026-09-16，后续独立 reviewer rerun 在 Tamarin 1.12.0、Maude 3.5.1、WSL Ubuntu-24.04 下对三个未修改模型完成 parse/prove；14/14 项 lemma 的结果状态与 proof steps 均与既有记录一致，并保存原始 stdout/stderr、manifest、模型及输出哈希和 7 个导出 graph。该复跑是新的 reviewer-generated evidence，不是历史运行日志恢复；它证明当前抽象结果可复现，不建立完整 K-Waay refinement，也不扩大协议级或部署级安全结论。

英文母稿仍保留早期 provenance 表述，本任务禁止修改英文稿；下一阶段中文 LaTeX 必须采用上述更新口径。

## 10. 重组后的主论证

原协议已有不同参与方条件 → 参与方、消息和发送发生是不同坐标 → 在相同两槽骨架上控制接纳坐标 → 放宽配置出现重复精确来源接受 → 消息级配置虽满足自身性质但仍有同一参与方见证 → 参与方级 positive control 维持目标且非真空 → 批处理接口必须明确参与方关系及维护责任。

三个接纳配置是产生证据的方法；论文主线始终是 different-party condition 所维护的批内参与方关系。

