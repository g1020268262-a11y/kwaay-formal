# 14 项 Tamarin 结果的放置决定

## 1. 决定

中文投稿版正文表 3 只突出 7 项直接支撑主论证的关键结果。完整 14 项结果不得删除，保留在附属/复现材料中，并由正文给出明确指针。

这样处理有三个理由：

1. P1/P2 的同类写法以性质分组和代表性结果解释为主，不让工具代码名替代论文论证；
2. 7 项关键结果已经完整覆盖放宽反例、消息级分离和参与方级正控制三条证据链；
3. 其余 7 项用于排除死模型、无来源接受或验证拒绝分支可达，属于必要 supporting properties，但不需要与核心结论等权占据主表。

## 2. 正文表 3 的 7 项关键结果

正文表 3 使用“配置—自然语言性质—类型—结果—论证作用”五类主要信息。lemma 标识放在最后一列，也可在排版时改为括号或次要小字号信息；proof steps 不进入正文主表。

| 配置 | 正文自然语言性质 | 类型 | 结果 | 直接论证作用 | lemma 标识（次要信息） |
|---|---|---|---|---|---|
| 放宽 | 一个精确发送来源支持同一批中的两个接受发生 | exists-trace | verified | 给出重复接受见证 | `one_send_two_accepts_exists` |
| 放宽 | 精确来源在同一批上下文中的作用域内发生注入性 | all-traces | falsified | 由反例确认两个接受发生不重合 | `receiver_accept_injective` |
| 消息级 | 同一批中的不同接受发生具有不同消息 | all-traces | verified | 说明消息级配置维护其目标坐标 | `accepted_batch_has_distinct_messages` |
| 消息级 | 精确来源的作用域内发生注入性 | all-traces | verified | 排除放宽配置的精确重复形状 | `receiver_accept_injective` |
| 消息级 | 同一参与方的不同发送发生、不同消息仍可同批接受 | exists-trace | verified | 机器见证支撑“消息级不能替代参与方级” | `same_party_different_messages_batch_exists` |
| 参与方级 | 同一批中的不同接受发生具有不同参与方 | all-traces | verified | 验证目标参与方关系 | `accepted_batch_has_distinct_parties` |
| 参与方级 | 有效的不同参与方批次可达 | exists-trace | verified | 排除全拒绝造成的真空成立 | `distinct_party_batch_exists` |

表后正文只解释三条链：放宽配置的重复接受；消息级配置“自身成功但替代失败”；参与方级配置的目标性质和非真空性。

## 3. Supporting properties 的 7 项结果

以下结果不放入正文主表的独立行。正文 3.1、3.3 或 3.4 用一到两句合并说明，完整状态与 steps 保留在附属/复现表中。

| 配置 | lemma 标识 | 状态 | steps | 放置 | 作用与不进入主表的理由 |
|---|---|---|---:|---|---|
| 放宽 | `normal_relaxed_batch_exists` | verified | 10 | 3.1 合并说明；完整表 | 排除死模型，但不是核心安全结论 |
| 放宽 | `receiver_accept_has_send` | verified | 8 | 3.1 合并说明；完整表 | 确认精确来源对应，为反例提供支持 |
| 消息级 | `repeated_message_rejection_exists` | verified | 4 | 3.2 注释或 3.4 supporting properties；完整表 | 只证明拒绝分支可达，不是所有无效输入最终拒绝 |
| 消息级 | `receiver_accept_has_send` | verified | 8 | 3.4 supporting properties；完整表 | 与其他配置同类，可合并报告 |
| 参与方级 | `same_party_rejection_exists` | verified | 5 | 3.3 注释或 3.4 supporting properties；完整表 | 公式未把发送条目绑定到被拒批次，不能作为强拒绝结论 |
| 参与方级 | `receiver_accept_has_send` | verified | 8 | 3.4 supporting properties；完整表 | 与其他配置同类，可合并报告 |
| 参与方级 | `receiver_accept_injective` | verified | 33 | 3.3/3.4 合并说明；完整表 | 支持正控制，但目标参与方性质和非真空性更直接 |

## 4. 完整 14 项表的承载位置

完整 14 项复现表应至少保留以下列：模型/配置、lemma 标识、量词/性质类型、状态、proof steps、语义角色。proof steps 只保留在这份完整材料中，不回填正文表 3。其权威数据来源为：

- `reviews/2026-09-16-evidence/result-comparison.tsv`；
- 三个 `*-prove.stdout.txt`；
- `independent-rerun-manifest.json`；
- 现有 `manuscript/tables/verification-results.tex` 的早期汇总。

下一阶段优先顺序：

1. **可提交附属材料时**：正文表 3 放 7 项关键结果；附属材料放完整 14 项表、精确 lemma 公式、命令、哈希和 graph 索引。
2. **期刊只允许复现仓库链接时**：正文表 3 放 7 项；正文 3.4 指向仓库中的完整 14 项表和 `reviews/2026-09-16-evidence/`。
3. **最终确认既不能提交附属材料，也不能可靠指向复现材料时**：将完整 14 项压缩为正文跨栏表或文后附表；7 项关键结果仍用加粗/分组突出，避免所有代码名等权呈现。

在确认投稿系统限制之前，不把完整 14 项重新塞回正文主表。

## 5. 与 2026-09-16 独立复核的对应

独立复核的 `result-comparison.tsv` 显示 14/14 行均为 `MATCH`：13 项 verified，1 项 falsified；状态和 proof steps 均与既有记录一致。三组模型的 parse/prove 均退出 0，证明输出报告 wellformedness 成功。

7 个导出 graph 对应存在性见证或反例，包括 relaxed 3 个、message-level 2 个、party-level 2 个。graph 可能包含与目标见证无关的 `Send` 事件，不能直接当作最小协议轨迹；图 2 仍应根据核心事件关系进行论文式重构，并标明其功能。

## 6. 正文复核句

正文 3.4 统一使用以下事实，不展开文件清单：

> 后续独立复核在 Tamarin 1.12.0、Maude 3.5.1、WSL Ubuntu 24.04 下重新执行三个未修改模型，14 项结果状态及证明步数全部匹配。

详细命令、模型与输出哈希、stdout、stderr、manifest 和导出 graph 保留在复现材料。

## 7. 决定状态

**MAIN_TABLE_7_RESULTS_FULL_SET_14_PRESERVED**

