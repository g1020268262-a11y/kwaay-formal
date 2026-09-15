# 第五章审查报告

结论：`SECTION_5_NEEDS_REVISION`。

本次发现 3 处需要修改的问题：1 处证据解释问题、1 处交付内容不一致、1 处浮动体位置问题。无需因此否定三模型比较的主线，但当前版本不宜直接冻结。

## 审查范围与证据边界

审查第五章正文、两幅 TikZ 图、verification-results 表、第五章写作报告，以及当前 PDF 的第 8–15 页。直接对照三个 RQ-v2 模型、现有执行报告、evaluation draft 和冻结包中的环境、命令与哈希记录。

本次没有修改正文、图表、模型或原写作报告，没有重新执行 Tamarin，也没有重新编译论文。仅新增本审查报告。已有第四章及第五章工作区改动均保留。

“与记录一致”指与现有 execution report 一致，不代表本次独立重现证明。冻结环境文件明确标记 existing-report-only 和 prover_rerun=no；现有材料未提供可用于核对下述具体 rejection witness 的原始 prover trace。

## 1. [P1] 正文把未绑定的 Send 事件解释成了被拒绝的输入对

位置：[第五章第 155 行](D:/kwaay-formal/manuscript/sections/05-formal-analysis.tex:155)，相关表述从第 149 行开始；[写作报告第 70 行](D:/kwaay-formal/manuscript/notes/section5-writing-report.md:70) 同样将这一解释标记为 YES。

正文说 rejection witness 使用同一 party 的不同 session/message，并以此直接对照 message-level 下仍可接收的 composition。这将记录的存在性结果解释成了“两个不同消息构成的那个 batch 被拒绝”。

然而，[same_party_rejection_exists](D:/kwaay-formal/tamarin/rq-v2-minimal/rqv2_party_admission.spthy:85) 仅要求：

- 出现两个同属 A、sid 和 m 均不同的 Send 事件；
- 此后出现一个 Reject(bid,rst) 事件。

Reject 事件没有携带 party、sid 或 message 字段，公式中也没有其他条件把这两个 Send 元组连接到被拒绝的 batch。因此，此 lemma 不能识别被拒绝的究竟是哪两个输入。

一个基于当前规则的说明性调度即可展示这个缺口：先产生不同元组 E1=(A,sid1,m1) 和 E2=(A,sid2,m2) 的两个 Send，再把 E1 放进同一 batch 的两个 slot，触发 Reject。这个调度满足 lemma 的条件，但实际被拒绝的输入对是 E1、E1，而非不同消息 E1、E2。这是对公式及规则的逻辑检查，不是本次新运行的 Tamarin 反例。

[RejectRepeatedParty 规则](D:/kwaay-formal/tamarin/rq-v2-minimal/rqv2_party_admission.spthy:56) 本身确实对相同 party 的 collected pair 提供拒绝分支，且不要求消息相同。因此，“同 party、不同消息的组合也符合该拒绝规则”可以作为规则语义解释保留；不能仅依据当前 lemma 的 verified 状态将其包装成已核实的特定输入对 witness。

最小修改建议：保留该结果作为 rejection-branch reachability；将不同消息也可被拒绝的解释明确归于规则语义；删除或收窄“这个已验证 witness 正好拒绝了那两个 Send 元组”的表述，并同步修正写作报告。无需改变模型或重新证明即可完成这种保守的正文修订。若要新增更强的 machine-checked witness，需要另外授权扩展事件/性质或核对原始轨迹，并重新完成对应证据工作。

注意：正文已经正确区分 reachability 与 liveness，但这不能解决本项 tuple-to-batch binding 问题。message-level 的 rejection lemma 也没有把 Send 绑定到 Reject；目前正文仅据其描述相等消息拒绝分支可达，未产生同等程度的具体输入对过度解释。

## 2. [P2] 第五章宣称附录已有内容，但三个附录仍是占位

位置：[第五章第 268 行](D:/kwaay-formal/manuscript/sections/05-formal-analysis.tex:268)。

正文称完整 lemma、commands、hashes 和 reproducibility details 已在配套材料提供，并在 appendix 中汇总。但以下附录目前只有标题、label 和 TODO：

- [Exact Model Properties](D:/kwaay-formal/manuscript/appendix/model-properties.tex:3)
- [Detailed Counterexample Traces](D:/kwaay-formal/manuscript/appendix/trace-details.tex:3)
- [Reproducibility Details](D:/kwaay-formal/manuscript/appendix/reproducibility.tex:3)

当前 PDF 第 14 页也只有对应附录标题，未包含宣称的汇总。这不是 lemma、命令或哈希完全不存在：完整性质可在模型中找到，命令和哈希也有冻结材料。问题是正文把尚未写入论文附录的内容描述为已经完成。

最小修改建议：暂时删除“summarized in the appendix”，准确指向实际交付的模型和冻结材料，并在写作报告中保留附录待完成项。如果选择补写附录，则需将其作为另行明确的写作范围。

## 3. [P2] 完整结果表漂移至参考文献和附录之后

位置：[结果表第 1 行](D:/kwaay-formal/manuscript/tables/verification-results.tex:1) 使用仅浮动页位置 `[p]`；[第五章第 250 行](D:/kwaay-formal/manuscript/sections/05-formal-analysis.tex:250) 引入结果表。

已逐页检查当前 PDF 第 8–15 页，实际顺序为：

| PDF 页码 | 内容 |
| --- | --- |
| 8–10 | 第五章前半部分 |
| 11 | 5.4 与 5.5 开始 |
| 12 | 两幅第五章图 |
| 13 | 5.5 续文、5.6、第六至八章、参考文献开始 |
| 14 | 参考文献续文与三个空附录标题 |
| 15 | Table 3：完整 14 项验证结果 |

这使 5.5 的核心表格脱离结果章节，并出现在附录之后。没有 overfull/underfull 警告不能保证浮动体位置合理；当前图表本身没有发现裁切或文字重叠。

最小修改建议：调整表格的允许位置并在离开第五章前控制浮动体排出，使结果表跟随 5.5、两幅图靠近对应论证。具体方式应适配现有模板。修改后重新编译并查看实际页面，不能仅依赖编译日志验收。

## 已核对且可保留的部分

- 结果表的 14 项 lemma 名称、状态和 step counts 与现有执行报告一致，包括 relaxed receiver_accept_injective 的 falsified 状态。
- 三个当前模型的 SHA-256 与记录一致，没有发现“正文引用结果但模型版本已经漂移”的情况。
- relaxed 的 one_send_two_accepts_exists 将两个 ReceiverAccept 绑定到同一完整元组和 batch/state，并约束匹配 Send 的唯一性。正文对此的主要解释成立。
- message-level 的 same_party_different_messages_batch_exists 通过完整 ReceiverAccept 参数绑定两个不同 sender origins，支持“消息不同、同一 party 仍可被接收”的关键区分。
- party-level 的 accepted_batch_has_distinct_parties 与 distinct_party_batch_exists 分别支持所报告的安全性质和有效 batch 可达性；本次发现的 rejection witness 问题不推翻这两项结果。
- 正文主要维持了 two-slot、ReceiverAccept 与模型内 origin correspondence 边界，没有将 duplicate acceptance 直接写成 secrecy break 或已部署攻击。

## 非阻塞的文字建议

1. 第五章第 21–30 行的编号公式以小于号连接 Send/BatchReceive/ReceiverAccept 事件表达式。建议将事件断言和时间点顺序分开，或使用明确标注时序的箭头，避免把事件本身写成可进行大小比较的对象。
2. 多数 step counts 已在表格完整列出，正文可减少逐项重复；5.4 对“并非仅删除不等式”的两段相近解释也可合并。这些是可读性建议，不影响上述三项必须修订事项的优先级。

## 建议修订顺序

先收窄 party-level rejection witness 的证据表述，再修正附录完成状态，最后处理浮动体位置并重新检查 PDF。同步更新原写作报告中“rejection witness uses distinct session and message coordinates: YES”“Overclaim count: 0”和“None within Section 5”等过强的验收结论。

完成上述保守修订不需要改变现有 Tamarin 模型或增加任何验证结果。当前状态为需要定向修订，而非需要重写第五章。
