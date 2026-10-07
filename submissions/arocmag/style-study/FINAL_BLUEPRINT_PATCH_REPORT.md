# AROCMAG 最终蓝图小范围补丁报告

## 1. 任务边界

本次只修订冻结蓝图及其四份配套风格/重组文件，并新增本报告。未修改章节结构、研究问题、7 项关键结果选择或研究结论；未修改 `manuscript/`、`tamarin/`、`reviews/`、`docs/`、`artifact/` 及 `submissions/arocmag/` 下的 LaTeX、draft、Word 和 official 目录。

## 2. Patch 1：核心验证性质的形式化语义

`FINAL_CHINESE_PAPER_BLUEPRINT.md` 的 2.3 现要求正文用小型语义表说明四类性质：

1. 精确来源对应：每个 `ReceiverAccept(A,oid,m,bid,rst)@r` 都存在更早的 `Send(A,oid,m)@s`，对应完整 `(A,oid,m)` 元组；
2. 作用域内发生注入性：所有变量均全称量化；同一 `Send(A,oid,m)@s` 若早于两个共享 `(A,oid,m,bid,rst)` 的接受事件，则二者必须是同一事件；
3. 消息区分：同一 `(bid,rst)` 中两个不同接受事件的消息坐标不同；
4. 参与方区分：同一 `(bid,rst)` 中两个不同接受事件的参与方坐标不同。

上述语义直接核对三个 `tamarin/rq-v2-minimal/*.spthy` 中的真实 lemma。蓝图明确说明：作用域内发生注入性只检查一个精确来源是否对应多个不同接受事件，不直接检查批内参与方唯一性，也不是一般密码协议定理。正文可给一个未编号注入性式，核心独立编号公式仍保持三项。

## 3. Patch 2：正文结果表与完整复现表分工

正文表 3 的主要列冻结为：配置、自然语言性质、类型、结果、论证作用。lemma 标识只作为括号、最后一列或次要小字号信息；proof steps 已从正文关键结果表删除。

正文 7 项关键结果及状态保持不变：

| 配置 | lemma | 结果 |
|---|---|---|
| 放宽 | `one_send_two_accepts_exists` | verified |
| 放宽 | `receiver_accept_injective` | falsified |
| 消息级 | `accepted_batch_has_distinct_messages` | verified |
| 消息级 | `receiver_accept_injective` | verified |
| 消息级 | `same_party_different_messages_batch_exists` | verified |
| 参与方级 | `accepted_batch_has_distinct_parties` | verified |
| 参与方级 | `distinct_party_batch_exists` | verified |

完整 14 项复现表继续保留模型/配置、lemma、量词/性质类型、状态、proof steps 和语义角色。权威数据仍为 `reviews/2026-09-16-evidence/result-comparison.tsv`；该文件保持 14 行且每行均有 steps，本次未修改。

## 4. Patch 3：条件式设计结论

4.2 的“维护责任”现明确为从原协议条件出发的条件式接口要求：若实现需要满足 K-Waay 所述的批内不同参与方条件，负责批次构造或接纳的组件才需要依据适当的参与方表示维护该关系。蓝图同时禁止把这一结论扩张为所有实现的强制检查、某一部署缺失检查的证据或唯一执行机制。

结束语同步改为：若批处理接口需要满足 K-Waay 所述的不同参与方条件，则其批次构造或接纳过程需要维护相应的参与方关系。

## 5. 术语与复现口径

蓝图已增加下一阶段正文术语规则：首次出现可写“不同参与方条件（different-party condition）”和“正控制（positive control）”，此后只用中文；身份坐标语境中的 `occurrence` 统一译为“发送发生”；复现语境中的 `reviewer rerun` 统一写“后续独立复核”。配套文件采用同一口径。

## 6. 最终 12 项检查

1. **通过**：冻结的一级、二级章节结构逐项匹配，未改变。
2. **通过**：2.3 已能独立解释作用域内发生注入性的量词、完整坐标、上下文和时间条件。
3. **通过**：精确来源对应、消息区分和参与方区分均有独立语义说明。
4. **通过**：四类性质与 `tamarin/rq-v2-minimal/` 中的真实 lemma 一致。
5. **通过**：正文表 3 不再含 proof steps 列或数值。
6. **通过**：完整 14 项材料仍明确保留 proof steps；权威 TSV 的 14 行 steps 均存在。
7. **通过**：7 项关键结果选择及 verified/falsified 状态未改变。
8. **通过**：4.2 的维护责任已改为以满足原协议条件为前提的条件式要求。
9. **通过**：结束语已同步改为条件式。
10. **通过**：未新增研究问题、研究结论或证据主张。
11. **通过**：未生成或修改中文论文正文。
12. **通过**：未生成正式图；未修改 Word。

## 7. 修改文件

- `FINAL_CHINESE_PAPER_BLUEPRINT.md`
- `FULL_14_RESULT_PLACEMENT_DECISION.md`
- `AROCMAG_STYLE_GUIDE_FOR_KWAAY.md`
- `KWAAY_SECTION_RESTRUCTURING_PLAN.md`
- `STYLE_STUDY_REPORT.md`
- `FINAL_BLUEPRINT_PATCH_REPORT.md`（新增）

未执行 commit 或 push。

**AROCMAG_FINAL_BLUEPRINT_PATCH_READY**
