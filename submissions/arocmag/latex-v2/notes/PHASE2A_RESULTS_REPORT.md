# AROCMAG Chinese LaTeX Phase 2A Results Report

任务：`AROCMAG_CHINESE_LATEX_PHASE2A_RESULTS`

前置检查：`PHASE1_FINAL_PATCH_REPORT.md` 已存在，状态为 `AROCMAG_PHASE1_FINAL_PATCH_READY`。

## 1. 创建与修改文件

所有本次写入均位于 `submissions/arocmag/latex-v2/`：

- 新建 `sections/04-formal-analysis.tex`；
- 新建 `tables/key-verification-results.tex`；
- 修改 `paper-content.tex`，接入第3章；
- 更新 `figures/README.md`，增加图2要求；
- 更新 `notes/SOURCE_MAPPING.md`，按正文22个段落标记及结果表记录来源；
- 新建 `notes/PHASE2A_RESULTS_QA.md`；
- 新建本报告 `notes/PHASE2A_RESULTS_REPORT.md`；
- 重新编译 `main.pdf`。

本次开始前已有 Phase 1 patch 的未提交改动，保持原样；没有将这些历史改动计入本次写作。
开始/结束哈希核对确认，摘要、引言、第1/2章与三张既有表未变，三个 Tamarin 模型也未变。

## 2. 第3章实际结构

3 形式化验证与结果分析

- 3.1 放宽参与方条件后的重复接受
- 3.2 消息级限制的替代性
- 3.3 参与方级条件下的性质验证
- 3.4 综合验证结果

没有其他 subsection。正文含2614个汉字（去除注释，含标题，不含外部结果表），高于当前引言、第1章和第2章，是当前全文篇幅最大的一级章。

## 3. 七项核心结果覆盖

| 配置 | 核心性质 | 类型 | 状态 |
|---|---|---|---|
| 放宽 | 一个精确来源支持两个同批接受 | exists-trace | verified |
| 放宽 | 作用域内发生注入性 | all-traces | falsified |
| 消息级 | 消息区分 | all-traces | verified |
| 消息级 | 作用域内发生注入性 | all-traces | verified |
| 消息级 | 同一参与方不同消息批次可达 | exists-trace | verified |
| 参与方级 | 参与方区分 | all-traces | verified |
| 参与方级 | 有效不同参与方批次可达 | exists-trace | verified |

七项全部覆盖，选择和状态与冻结要求一致。正式表用中文结果并附量词类型解释，不列 proof steps。

## 4. Supporting properties

放宽正常路径、三项精确来源对应、两项拒绝分支可达性和参与方级注入性共7项，在相应小节提供必要解释，3.4合为一段。未新建第二张大表。
完整14项及步骤继续保存在既有 `reviews/2026-09-16-evidence/result-comparison.tsv` 等复现材料中，没有复制进正文或修改证据文件。

## 5. 放宽配置反例

采用一条编号事件链显示一个匹配 Send、一次 BatchReceive、两个完全同坐标的 ReceiverAccept，满足 `s<b<r1<r2`。两个槽位使用相同 `(A,oid,m)`，并说明唯一来源只针对匹配元组，不排除无关发送。
存在性见证与注入性 falsified 解释为同一重复接受形状的两种验证表述；来源对应仍 verified，因此不是凭空接受。
末段用唯一一句完整协议攻击边界收束。

## 6. 消息级机器见证

先说明消息区分与作用域内发生注入性成功，且精确来源对应继续成立，再以机器见证展示 `(A,oid1,m1)` 与 `(A,oid2,m2)` 各自有来源，oid和m均不同但A相同，两者同批接受。
非替代性来自实际模型中可达执行，而不是仅由抽象非蕴含推断。未新增非蕴含编号公式。

## 7. 参与方级正控制

直接比较参与方坐标；以全迹目标性质 verified 和有效批次存在性 verified 为主线，后者排除全部拒绝导致的真空成立。来源对应与注入性放在支持位置，没有写成修复方案或K-Waay安全证明。

## 8. 拒绝性质限制

消息拒绝性质仅说明相等消息拒绝分支有可达执行。参与方拒绝性质还明确保留“此前Send条目未绑定最终被拒候选元组”的限制。二者均不解释为任意无效输入最终拒绝或完整liveness。

## 9. 独立复核表述

3.4末段采用2026-09-16后续独立复核口径：Tamarin 1.12.0、Maude 3.5.1、WSL Ubuntu 24.04，重新执行三个未修改模型，14/14状态与证明步数匹配。正文仅给相对证据目录。
本次逐项匹配 TSV 与三个 stdout 的lemma、状态和steps，共14/14通过，合计13 verified / 1 falsified；没有在本任务中新跑 Tamarin。

## 10. 图2未生成

用户将图2制作安排为独立任务。本次只在3.1写入规定两行注释，并更新 `figures/README.md` 的来源、同坐标、同上下文、两接受时序和分析性重构要求。未生成正式图、TikZ、Mermaid或图资产，也没有未定义figure引用。

## 11. 新增编号公式

新增1个，即式(3) `eq:relaxed-duplicate-witness`。前两式保留，全文核心编号公式总数3个。

## 12. 表格编号

既有性质语义表仍为表3；关键Tamarin结果表自然顺延为表4，标签 `tab:key-verification-results`。
正文使用small，lemma次要信息使用footnotesize；未整体缩放表格或缩至极小字体。

## 13. 编译状态

执行：`latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex`，退出0。

| 最终日志验收项 | 数量 |
|---|---:|
| undefined references | 0 |
| undefined citations | 0 |
| missing characters | 0 |
| overfull boxes | 0 |

有两处非阻塞underfull hbox，badness分别为1158（原第2章）和1082（新3.2），无可见溢出。8页逐页检查未发现裁切、遮挡或表格越界。

## 14. 当前PDF

`main.pdf`：A4，8页；匿名元数据保留。第3章从第5页开始，到第7页结束，参考文献续至第8页。

## 15. Phase 2B适用性与停止边界

第3章结果、来源映射、公式与结果表均已就绪，可作为后续Phase 2B的输入。本任务在此停止，未撰写第4/5章，未制作Word，未执行commit/push。

**AROCMAG_CHINESE_LATEX_PHASE2A_READY**
